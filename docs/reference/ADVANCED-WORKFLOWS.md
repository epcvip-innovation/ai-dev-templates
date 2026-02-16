# Advanced Workflows: Power-User Guide

[← Back to Main README](../../README.md)

Power-user guide for working effectively with Claude Code at scale. Covers conceptual foundations that setup guides don't: how context windows actually work, planning systems, sub-agents, extension points, engineering predictable outputs, tool strategy, and meta-level principles.

**Audience**: Developers already comfortable with Claude Code who want to work more effectively on complex, multi-session projects.

---

## 1. Context Management at Scale

### What Fills the Context Window

Claude Code's 200k token context window fills from multiple sources simultaneously:

| Source | Typical Size | Notes |
|--------|-------------|-------|
| CLAUDE.md (all levels) | 1-3k tokens | Loaded every session |
| Skill descriptions | Up to 2% of context | Always present when skills are configured (fallback: 16k chars) |
| MCP tool definitions | 0.5-2k per server | Fixed overhead; auto tool-search enables at 10% of context |
| Files read with Read tool | 1-10k per file | Accumulates fast during exploration |
| Tool output (Bash, Grep, etc.) | 0.5-5k per call | Large outputs get truncated |
| Sub-agent results | 1-5k per agent | Summarized, not raw |
| Conversation history | Grows continuously | The biggest consumer over time |

**Key insight**: Performance degrades *before* you hit the ceiling. Research suggests quality drops noticeably past ~120k tokens due to attention diffusion — the model has more to attend to, so each piece gets less focus.

### What to Avoid

These are the most common context wasters:

- **Dumping entire log files** — Pipe through `tail -50` or grep for the error first
- **Reading files you already read** — Claude remembers file contents within the session
- **Redundant instructions** — If it's in CLAUDE.md, don't repeat it in prompts
- **Unbounded searches** — `Grep` across the entire repo when you know the directory
- **Large MCP outputs** — MCP responses warn at 10k tokens and cap at 25k (configurable via `MAX_MCP_OUTPUT_TOKENS`)

### Treat Context as a Budget, Not a Container

The wrong mental model: "I have 200k tokens, so I can keep going until I run out."

The right mental model: "Context is scarce memory in a constrained system. Every token I spend on exploration is a token unavailable for implementation."

**Practical implications**:
- Read targeted sections of files, not entire files when you know what you need
- Use Grep/Glob to find what you need before reading
- Summarize investigation findings before moving to implementation
- Close investigation threads explicitly ("I've found the issue in X, moving on")

### Externalizing State

The most important context management technique: **write things down in files instead of relying on conversation memory**.

| What to Externalize | Where | Why |
|---------------------|-------|-----|
| Current plan + steps | `plan.md` or `.claude/plans/` | Survives compaction, restartable |
| Key decisions made | `decisions.md` or CLAUDE.md | Won't be re-debated |
| Modified files list | `HANDOFF.md` | Critical for session continuity |
| Open questions | `plan.md` TODO section | Prevents silent drops |

**Pattern**: At the start of complex work, create a plan file. Update it as you go. This file becomes the source of truth that survives context compaction and session restarts.

### Auto-Compact: What Survives and What Doesn't

Auto-compaction triggers at approximately **95% of context capacity**. When it fires, Claude Code summarizes the conversation to free space.

**Survives well**:
- Recent messages and tool calls
- CLAUDE.md content (reloaded fresh)
- Files currently open / recently read
- The current task or question

**Gets lost or degraded**:
- Early investigation findings
- Nuanced decisions from 50+ messages ago
- The "why" behind rejected approaches
- Intermediate reasoning steps

**Compact instructions in CLAUDE.md**: You can add a section telling Claude what to preserve during compaction:

```markdown
## On Context Compaction
When compacting, preserve:
- Current goal and active plan file path
- List of files modified this session
- Key decisions made and their rationale
- Open TODOs and blockers
```

### When to Compact Deliberately

Use `/compact` proactively at natural breakpoints:

- **After investigation, before implementation** — Clear exploration debris before writing code
- **Before large test runs** — Test output can flood context; start clean
- **Between phases** — Finished the API? Compact before starting the UI
- **After resolving tangents** — Got sidetracked debugging a dependency? Compact to refocus

### Compact Rules by Work Type

Different tasks need different information preserved. Add these to your compact instructions:

| Work Type | Preserve | Summarize |
|-----------|----------|-----------|
| **Refactors** | File list, naming conventions, patterns applied | Individual file diffs |
| **Bug hunts** | Reproduction steps, hypotheses tested, stack traces | Exploration dead-ends |
| **Release workflows** | Checklist, version numbers, deployment targets | Build logs, test output |
| **Multi-file features** | Architecture decisions, interface contracts, file dependency order | Individual implementation details |

---

## 2. Planning Systems

### Temporary vs Durable Plans

Not every task needs a plan file. Match the planning mechanism to the task:

| Task Scope | Planning Method | When |
|-----------|----------------|------|
| Single-file fix, <30 min | In-chat discussion | Quick tasks with clear scope |
| Multi-file, single session | `plan.md` in project root | Needs structure but won't span sessions |
| Multi-session or multi-person | `.claude/plans/feature-name.md` | Must survive restarts, handoffs |

### What Good Plans Contain

1. **Goal** — One sentence: what does "done" look like?
2. **Constraints** — What can't change? (API contracts, DB schema, performance budgets)
3. **Ordered steps** — Numbered, with dependencies explicit
4. **Verification** — How to confirm each step worked (test commands, expected output)
5. **Human checkpoints** — Where to pause for review before continuing

**See**: [PLAN_QUALITY_RUBRIC.md](../../templates/standards/PLAN_QUALITY_RUBRIC.md) for the full scoring framework.

### Mandatory Cleanup Phases

Plans that end at "feature works" accumulate debt. Every non-trivial plan should include:

1. **Code cleanup** — Remove dead code, debug statements, commented-out experiments
2. **Comment cleanup** — Delete resolved TODOs, update stale comments, remove obvious narration
3. **Lint/format pass** — Run the project's formatter and linter
4. **Final verification** — Tests pass, no regressions, `git diff` review for accidental changes

These aren't optional polish — they're the difference between "it works" and "it's shippable."

---

## 3. Agents and Sub-Agents

### Why Sub-Agents Exist

The Task tool spawns isolated Claude instances (sub-agents) that work independently and return summarized results. Three key benefits:

1. **Isolated context** — The sub-agent gets a clean context window, free from your conversation's accumulated state
2. **Parallel work** — Multiple agents can run simultaneously on independent tasks
3. **Summarized output** — Instead of dumping 500 lines of grep results into your context, an agent reads them and returns a 20-line summary

### Common Patterns

**Explorer** (read-only codebase mapping):
- "Find all API endpoints and their authentication requirements"
- "Map the data flow from user input to database write"
- Model: haiku (fast, cheap, sufficient for pattern matching)

**Reviewer** (edge-case hunting):
- "Review these changes for security issues, focusing on input validation"
- "Check if this refactor breaks any existing callers"
- Model: sonnet or opus (needs reasoning depth)

**Implementer** (scoped changes):
- "Update all test files to use the new fixture pattern"
- "Add error handling to these 5 API endpoints following the pattern in users.ts"
- Model: sonnet (balances speed and quality)

### The Task Tool: How It Works

```
Main conversation                    Sub-agent
┌──────────────┐                    ┌──────────────┐
│ Your context  │ ── Task call ──→  │ Fresh context │
│ (may be full) │                   │ (clean 200k)  │
│               │ ←── Summary ───   │ Does work...  │
│ Gets ~1-5k    │                   │ Returns result │
│ token summary │                   └──────────────┘
└──────────────┘
```

**When to use agents**:
- Exploration that would generate lots of output (searching across many files)
- Parallel independent tasks (review security AND check tests simultaneously)
- When your context is already heavy and you need focused work done

**When NOT to use agents**:
- Simple, targeted searches (just use Grep/Glob directly)
- Tasks that need your conversation's full context
- Sequential work where each step depends on the previous

### Model Selection for Agents

| Agent Task | Model Spectrum | Rationale |
|-----------|---------------|-----------|
| File scanning, pattern finding | haiku | Clear efficiency win — speed and cost, accuracy sufficient |
| Code review, implementation | sonnet → opus | Depends on stakes. Sonnet saves cost; opus gives deeper reasoning |
| Architecture, complex debugging | opus | Worth the premium — fewer iterations, better first-pass quality |

### Downsides to Know

- **Cost multiplier** — Each agent is a separate API call chain. 5 parallel agents = 5x the token cost of that work
- **Divergent edits** — Two agents modifying the same file will conflict. Assign non-overlapping scopes
- **No shared context** — Agent A doesn't know what Agent B found. You're the coordinator
- **Overhead** — For a 3-second Grep, spawning an agent adds 10-30 seconds of startup overhead
- **No nesting** — Sub-agents cannot spawn their own sub-agents. Design workflows with one level of delegation

### Model Selection Philosophy

Match the model to the stakes, not the other way around:

- **Haiku for bulk scanning** — File searches, pattern matching, summarization. A clear efficiency win where reasoning depth doesn't matter
- **Sonnet or opus for implementation** — Sonnet saves budget; opus often saves *time* through fewer iterations and better first-pass quality. Teams building quality software typically find top-tier models worth the cost
- **Opus for architecture/critical work** — Security reviews, design decisions, complex multi-file reasoning. The premium pays for itself in avoided rework

The right default depends on your team. Cost-sensitive workflows benefit from tiered selection. Quality-first teams often run opus for everything beyond scanning — and that's a valid choice.

---

## 4. Extension Points: Skills, Hooks, MCP

Claude Code's behavior can be extended through four mechanisms. This section covers the conceptual model — see linked READMEs for implementation details.

### Skills

Reusable instruction bundles that teach Claude new capabilities. Skills use progressive disclosure to manage context cost:

1. **Description** (always loaded) — Short summary, ~2% of context budget. Determines when the skill activates
2. **Full instructions** (on invocation) — Complete prompt with steps, examples, guardrails. Only loaded when triggered
3. **References** (on demand) — Supporting files read during execution. Loaded only if the skill needs them

**Key implication**: Skill descriptions are always in context. Keep them short. A 500-word description permanently consumes tokens every session.

**See**: [SKILL-TEMPLATE.md](../../templates/plugins/SKILL-TEMPLATE.md) for the creation pattern.

### Hooks

Shell commands that run at workflow events. The **determinism lever** — unlike prompt instructions (which Claude *might* follow), hooks enforce behavior through exit codes:

- **Exit 0**: Allow the operation
- **Exit 2**: Block the operation (Claude sees the error message and must adapt)

This is deterministic. No amount of prompt drift can bypass an exit code 2.

**Use hooks for**: query validation, secret detection, format enforcement, commit message standards.

**See**: [Hooks README](../../templates/hooks/README.md) for event types and implementation patterns.

### MCP (Model Context Protocol)

MCP servers give Claude access to external tools (databases, browsers, APIs). They work well but have hidden context costs:

- **Tool definitions consume context** — Each MCP server's tool schemas are loaded into context. More servers = less room for conversation
- **Auto tool-search** — When MCP tool definitions exceed 10% of context, Claude Code enables tool-search mode (tools are looked up on demand instead of all being present)
- **Output limits** — MCP responses warn at 10k tokens and hard-cap at 25k tokens by default
- **Monitor with** `MAX_MCP_OUTPUT_TOKENS` env var to adjust the cap when needed

**Practical advice**: Only enable the MCP servers you actually need for the current project. A Supabase + Playwright + Railway + GitHub setup may consume 5-10% of context before you type anything.

### Plugins (Team Distribution)

Plugins package skills + hooks + references into distributable bundles for team use. They're the delivery mechanism, not a separate concept.

**See**: [Plugins README](../../templates/plugins/README.md) for the full taxonomy (skills vs commands vs hooks vs plugins).

---

## 5. Engineering Predictability

### The Core Problem

LLM outputs are probabilistic. Ask the same question twice, get different answers. This is a feature for creative work and a liability for engineering workflows.

**Predictability must be engineered** — it doesn't emerge naturally from prompting alone.

### The Predictability Stack

From weakest to strongest enforcement:

```
Human checkpoints    ← Strongest (manual review at key moments)
Test gates           ← Strong (automated pass/fail)
Hooks                ← Strong (exit codes guarantee behavior)
Compact rules        ← Medium (survives context, but advisory)
Plan files           ← Medium (Claude follows, but can drift)
CLAUDE.md guidance   ← Weak-Medium (read every session, but advisory)
Prompt instructions  ← Weakest (can be forgotten mid-session)
```

### Reproducibility Techniques

Beyond hooks, these patterns improve consistency:

1. **Limit scope** — "Fix the null check in `processOrder()`" beats "improve error handling across the app"
2. **Explicit success criteria** — "Done when all 3 tests pass and the type error on line 47 is resolved"
3. **Verify before proceeding** — "Run the tests, show me the output, then move to the next file"
4. **Plan files as contracts** — Write the plan, get approval, execute against it. Drift is visible because the plan is written down
5. **Scoped diffs** — "Only modify files in `src/auth/` — don't touch anything else"
6. **Structured output expectations** — "Return a table with columns: file, change, reason" reduces ambiguity in responses

### When NOT to Enforce Predictability

Strict determinism is counterproductive for:
- **Exploration** — "What's in this codebase?" needs freedom to wander
- **Prototyping** — Rapid iteration benefits from creative latitude
- **Creative work** — UI design, naming, documentation tone
- **Learning** — Understanding unfamiliar code requires open-ended investigation

Match enforcement level to the task. Investigation gets loose reins; production deployment gets tight ones.

---

## 6. Claude Code vs Codex CLI

### Codex CLI

OpenAI's terminal-based coding agent. Included with ChatGPT paid plans (flat-rate, no per-token billing). Check OpenAI's pricing page for current tiers.

**Strengths**: Autonomous task delegation with approval gates, cost-predictable for heavy usage, good at batch operations.

**Workflow**: Give it a task, it proposes changes, you approve or reject. More "autonomous agent" than "pair programmer."

### Claude Code

Anthropic's terminal-based coding agent. Sub-agent ecosystem, skills/hooks/plugins for workflow customization, interactive tight-control workflow.

**Strengths**: Rich extension points (skills, hooks, MCP), fine-grained control over behavior, strong multi-file reasoning.

**Workflow**: Interactive pair programming — you guide, it implements, you verify. More "collaborative" than "autonomous."

### Strategic Usage

**Choose Claude Code for**:
- Interactive debugging where you need to steer the investigation
- Complex multi-step workflows requiring tight control at each stage
- Projects with custom skills, hooks, or MCP integrations
- Architecture decisions requiring deep reasoning (Opus)

**Choose Codex for**:
- Autonomous batch tasks ("update all test files to use new pattern")
- Cost-sensitive workflows with high token volume (flat-rate pricing)
- Quick, hands-off delegation where approval gates are sufficient
- Second-opinion reviews of Claude Code's output

**Cross-review pattern**: Build in one tool, review in the other. Different workflow philosophies, comparable accuracy on standard benchmarks. The value is in catching different classes of issues, not in one tool being "better."

**See**: [CODEX-SETUP.md](../setup-guides/CODEX-SETUP.md) for installation and dual-tool workflow.

---

## 7. Meta-Level Principles

Five themes that cut across every section of this guide:

1. **Context is scarce** — Treat it like memory in a constrained system. Every token spent on noise is unavailable for signal. Budget context deliberately.

2. **Externalize state** — Write decisions, plans, and findings to files. Conversation memory is volatile; files are durable. The best context management is not needing context at all.

3. **Choose models deliberately** — Match the model to the stakes. Haiku for bulk scanning, top-tier models for everything that requires reasoning. The premium pays for itself in fewer iterations.

4. **Engineer predictability** — Plans, hooks, compact rules, and scoped instructions stabilize behavior. Prompting alone is insufficient for repeatable workflows.

5. **Human checkpoints matter** — AI accelerates development; it doesn't replace architectural judgment. Insert review at security boundaries, irreversible operations, and cross-system integrations. The cost of pausing to review is minutes; the cost of an unreviewed mistake can be hours.

---

## See Also

- [CLAUDE-MD-GUIDELINES.md](../../templates/claude-md/CLAUDE-MD-GUIDELINES.md) — Keeping CLAUDE.md lightweight
- [PLAN_QUALITY_RUBRIC.md](../../templates/standards/PLAN_QUALITY_RUBRIC.md) — Scoring framework for implementation plans
- [Hooks README](../../templates/hooks/README.md) — Workflow automation and enforcement
- [Plugins README](../../templates/plugins/README.md) — Skills, commands, and plugin taxonomy
- [SKILL-TEMPLATE.md](../../templates/plugins/SKILL-TEMPLATE.md) — Creating new skills
- [COST_OPTIMIZATION_GUIDE.md](../../templates/testing/COST_OPTIMIZATION_GUIDE.md) — Model pricing and testing costs
- [CODEX-SETUP.md](../setup-guides/CODEX-SETUP.md) — Codex installation and dual-tool workflow
- [BUILTIN_VS_CUSTOM.md](../decisions/BUILTIN_VS_CUSTOM.md) — When to use built-in vs custom tooling

---

**Last Updated**: 2026-02-16
