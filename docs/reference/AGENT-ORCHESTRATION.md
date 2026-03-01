---
id: agent-orchestration
title: "Agent Orchestration Patterns"
description: "Monitoring, failure recovery, resource management, and multi-model coordination for multi-agent workflows"
audience: power-user
tags: ["agents", "orchestration", "multi-agent", "monitoring"]
---

# Agent Orchestration Patterns

[← Back to Main README](../../README.md) | [Advanced Workflows](./ADVANCED-WORKFLOWS.md)

Patterns for running multiple coding agents as a coordinated system rather than ad-hoc sub-agents. Covers the operational layer that sits above individual agent definitions: how to monitor fleets, recover from failures, assign models to review roles, and manage the hardware constraints of parallel work.

**Prerequisites**: Familiarity with [Custom Agents](../../templates/agents/README.md) (definitions, worktrees, memory) and [Advanced Workflows](./ADVANCED-WORKFLOWS.md) (sub-agents, agent teams, context management).

**When you need orchestration**: You're running 3+ agents regularly, agents depend on each other's output, you need monitoring beyond "check the terminal," or you want automated failure recovery instead of manual restarts.

**When you don't**: Single sub-agent tasks, one-off parallel explorers, anything where spawning an agent and reading its result is sufficient.

---

## 1. Two-Tier Context Separation

Context windows are zero-sum. Fill one with code and there's no room for business context. Fill it with customer history and there's no room for the codebase. The two-tier pattern avoids this tradeoff by splitting responsibilities:

**Orchestrator** (coordinator agent):
- Holds business context: customer requirements, past decisions, meeting notes, what worked and what failed
- Writes prompts for worker agents with exactly the context they need
- Tracks task state across workers
- Uses `MEMORY.md` for persistent strategy and learned patterns

**Workers** (implementer agents):
- Get clean context windows with only task-relevant information
- Focus exclusively on code: implementation, tests, PR creation
- Run in isolated worktrees so they can't interfere with each other
- Receive task-specific prompts written by the orchestrator, not raw requirements

> Subagents facilitate compression by operating in parallel with their own context windows, exploring different aspects of the question simultaneously.
>
> **Source**: [Anthropic: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)

**Claude Code implementation**: Define a coordinator agent with `tools: Task(worker, researcher)` and `memory: project`. The coordinator's MEMORY.md accumulates strategy ("this prompt structure works for billing features," "always include type definitions upfront"). Workers get fresh 200k-token windows with only the coordinator's task prompt. See [Context Engineering](./CONTEXT-ENGINEERING.md) for the broader context management strategy.

---

## 2. Deterministic Monitoring

Checking agent status by asking an LLM "is this agent done?" wastes tokens. Most status information is available through deterministic checks that cost nothing.

**The principle**: Exhaust filesystem, git, and CI checks before spending tokens. Only invoke an LLM when the deterministic checks indicate something needs human attention.

**Deterministic checks** (free, instant):
- Is the tmux session still alive? (`tmux has-session -t agent-name`)
- Has the agent created a PR? (`gh pr list --head branch-name`)
- Is CI passing? (`gh pr checks branch-name`)
- Are there merge conflicts? (`git merge-base --is-ancestor main branch`)

**LLM checks** (expensive, slow):
- Only when deterministic checks surface an issue that needs diagnosis
- Only when all automated gates pass and a human summary is needed

**Claude Code specifics**: The `TaskCompleted` hook fires when an agent teammate marks a task complete (exit 2 to reject). The `TeammateIdle` hook fires when a teammate is about to idle (exit 2 to keep working). These are deterministic gates that enforce quality without token cost. See [Custom Agents](../../templates/agents/README.md) for hook configuration.

**Implementation pattern**: A cron job or interval script reads a task registry file (JSON), runs the deterministic checks, and only alerts the human (via notification) when something needs attention. The script itself has zero LLM calls.

---

## 3. Multi-Model Code Review

Different models catch different classes of issues. Treating all models as interchangeable reviewers misses the value of their distinct strengths.

**Assign roles by strength**:

| Review Focus | Best Suited For | Why |
|-------------|----------------|-----|
| Edge cases, logic errors, thorough analysis | Models with strong reasoning depth | Catches subtle bugs that surface-level review misses |
| Security, scalability, performance | Models with broad knowledge | Identifies systemic issues beyond the immediate diff |
| Convention compliance, validation | Conservative models | Confirms what other reviewers flagged without over-generating new findings |

The specific model assignments will evolve as capabilities change. What persists is the pattern: assign distinct review roles rather than running three identical reviews.

**Workflow**: All reviewers post comments directly on the PR. The human reviewer reads the intersection of findings, not each review individually. A finding flagged by two independent models deserves more attention than one flagged by a single model.

**False positive management**: Track which models produce actionable findings vs noise over time. Calibrate trust per model per review focus area. Some models are systematically over-cautious; knowing this lets you skip their "consider adding..." suggestions and focus on findings they mark critical.

> Every PR gets reviewed by three AI models. They catch different things.
>
> **Source**: [OpenClaw: One-Person Dev Team](https://x.com/elvissun/status/2025920521871716562)

---

## 4. Failure Recovery with Enriched Context

When an agent fails, re-running the same prompt almost never works. The agent will make the same mistakes because it has the same context. Effective retry requires the orchestrator to diagnose the failure and rewrite the prompt.

**Enrichment strategies**:

| Failure Type | Enrichment |
|-------------|------------|
| Agent went off-track | Add corrected direction: "The requirement is X, not Y" |
| Agent ran out of context | Narrow file scope: "Focus only on these 3 files" |
| CI failed | Include the failure output and specific test names |
| Code review flagged issues | Include review comments as constraints |
| Agent needs domain knowledge | Add relevant docs, customer requirements, or error logs |

**Max retry count**: Set a hard limit before escalating to a human. Stripe caps at two CI rounds per agent; a common pattern is 2-3 total attempts with enriched context between each.

> At most two rounds of CI. There are diminishing marginal returns for an LLM to run many rounds.
>
> **Source**: [Stripe: Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)

**Claude Code implementation**: Use `--append-system-prompt` to add failure context to retried sessions without replacing the base prompt. For agent teams, the orchestrator can spawn a new worker with the enriched prompt while the original worker's worktree is preserved for diff comparison.

**Feedback loop**: When a retry succeeds, log what enrichment made the difference. Over time, the orchestrator learns which context is needed upfront ("always include the type definitions for billing features," "API endpoints need the auth middleware context"). This shifts from reactive retry to proactive prompt quality.

---

## 5. Resource Management

The bottleneck for parallel agents is usually hardware, not API costs. Each worktree agent needs its own dependency tree, build processes, and test runners. On a machine with limited RAM, the ceiling depends on your stack's memory footprint per worktree.

**Mitigation strategies**:
- **Stagger builds**: Don't let all agents compile simultaneously. Queue builds so only 1-2 run at a time.
- **Shared dependencies**: Symlink `node_modules` from a shared location where possible (watch for version conflicts).
- **Right-size concurrency**: Start with 2-3 parallel agents and increase only if your machine handles it without swapping. Memory pressure degrades all agents, not just the last one.

**Metric**: Track cost and effort per completed PR, not per token or per agent session. A PR that ships in one attempt at higher model cost is cheaper than three retries at a lower per-token rate. See [Cost Optimization Guide](../../templates/testing/COST_OPTIMIZATION_GUIDE.md) for model pricing details.

---

## 6. Agent Definition of Done

A PR existing is not the same as a PR being ready. Without an explicit definition of done, agents create PRs that still need significant human work, and humans get notified for work that isn't reviewable yet.

**Concrete checklist** (adapt to your project):

- [ ] PR created with description following project template
- [ ] Branch rebased on main (no merge conflicts)
- [ ] CI passing (lint, types, unit tests, E2E)
- [ ] Automated code review(s) passed (or only non-critical comments remain)
- [ ] Screenshots included (if the PR changes UI)

**Gate pattern**: Don't notify the human until all automated checks pass. The notification means "this is ready for your 5-10 minute review," not "this needs more work." If any gate fails, the agent (or orchestrator) handles it first.

> The target is a branch that pushes to CI and prepares a pull request. A minion run that's not entirely correct is often still an excellent starting point for an engineer's focused work.
>
> **Source**: [Stripe: Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)

**Claude Code implementation**: The `TaskCompleted` hook can enforce definition-of-done by running the checklist as a shell script. Exit code 2 rejects the completion and sends the agent back to fix the issue. This is deterministic enforcement, not a prompt suggestion.

---

## Sources

| Source | Type | Date | What It Covers |
|--------|------|------|---------------|
| [Stripe: Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) | Industry | 2026 | One-shot agents with deterministic orchestration, CI-gated PRs, devbox isolation, retry limits |
| [Anthropic: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) | Official | 2026 | Context separation, subagent fresh windows, summarized handoffs, memory-based continuity |
| [Anthropic: Agent Teams](https://code.claude.com/docs/en/agent-teams) | Official | 2026 | Shared task list, teammate coordination, quality gate hooks (TaskCompleted, TeammateIdle) |
| [OpenClaw: One-Person Dev Team](https://x.com/elvissun/status/2025920521871716562) | Community | 2026 | Two-tier context, cron monitoring, multi-model review, failure-driven prompt refinement |

**Last verified**: 2026-02-28

---

## See Also

- [Custom Agents](../../templates/agents/README.md) — Agent definitions, frontmatter, memory, worktree isolation, agent teams
- [Advanced Workflows](./ADVANCED-WORKFLOWS.md) — Context management, planning, sub-agents, predictability
- [Context Engineering](./CONTEXT-ENGINEERING.md) — Five pillars, token optimization, isolation strategies
- [Git Worktrees](./GIT-WORKTREES.md) — Worktree mechanics, parallel development
- [Cost Optimization Guide](../../templates/testing/COST_OPTIMIZATION_GUIDE.md) — Model pricing and testing costs
- [Codex Setup](../setup-guides/CODEX-SETUP.md) — Dual-tool workflow with Codex CLI

---
