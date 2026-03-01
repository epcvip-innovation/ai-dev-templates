---
id: context-engineering
title: "Context Engineering for Claude Code"
description: "Strategies for controlling context window usage, reducing waste, and keeping sessions productive at scale"
audience: power-user
tags: ["context-engineering", "optimization", "claude-code", "claudeignore"]
---

# Context Engineering for Claude Code

[← Back to Main README](../../README.md) | [Advanced Workflows](./ADVANCED-WORKFLOWS.md)

Strategies for controlling what enters the context window, how to reduce waste, and how to keep sessions productive as projects scale.

**Audience**: Developers who understand Claude Code basics and want to optimize how they use the 200k token context window across sessions.

---

## The Five Pillars

Context engineering is the discipline of curating what the model sees so that you get better results. Five strategies:

| Pillar | What It Controls | Key Lever |
|--------|-----------------|-----------|
| **Selection** | What enters context | `.claudeignore`, targeted reads, Grep before Read |
| **Compression** | How much space things take | `/compact`, plan files, subagent summaries |
| **Ordering** | What's fresh vs stale | Recency bias in attention, strategic compaction timing |
| **Isolation** | Keeping contexts clean | Subagents, worktrees, fresh sessions per workstream |
| **Format** | How efficiently info is encoded | Tables over prose, structured output, concise CLAUDE.md |

These map to Anthropic's three loading strategies:

| Strategy | When It Loads | Examples |
|----------|--------------|---------|
| **Deterministic** | Every session, always | CLAUDE.md, skill descriptions, MCP tool index |
| **Human-triggered** | On explicit invocation | `/compact`, skills |
| **LLM-determined** | Claude decides at runtime | Tool Search, file reads, subagent spawning |

**Implication**: Deterministic loads are the most expensive — they consume tokens *every turn*. Keep CLAUDE.md lean and skill descriptions short.

> **Source**: [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (2026), [Martin Fowler: Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html) (2025)

---

## .claudeignore

### What It Does

Prevents Claude Code from scanning specified files during codebase indexing. Uses `.gitignore` syntax. Place at project root.

### When You Need It

| Signal | Action |
|--------|--------|
| Initial scan is slow | Add build artifacts and dependencies |
| Context fills before useful work starts | Add generated files and lock files |
| Large binary assets in repo | Add media files and fonts |
| Monorepo with irrelevant packages | Add unrelated package directories |

### Starter Template

```gitignore
# Dependencies
node_modules/
.venv/
vendor/
.tox/

# Build artifacts
dist/
build/
.next/
out/
__pycache__/
*.pyc

# Lock files (large, low signal)
package-lock.json
yarn.lock
pnpm-lock.yaml
poetry.lock
Pipfile.lock

# Generated / compiled
*.min.js
*.min.css
*.map
coverage/
htmlcov/

# Large assets
*.png
*.jpg
*.gif
*.svg
*.woff
*.woff2
*.ttf
```

### Stack-Specific Additions

| Stack | Additional Patterns |
|-------|-------------------|
| **Python / FastAPI** | `.mypy_cache/`, `.pytest_cache/`, `*.egg-info/` |
| **React / Vite** | `.vite/`, `storybook-static/` |
| **Next.js** | `.next/`, `.vercel/` |
| **Monorepo** | Per-package `dist/`, shared `node_modules/` at root |

### Security Caveat

**`.claudeignore` is NOT a security boundary.** It controls scanning, not access. Claude can still read `.claudeignore`'d files if asked directly.

**For secrets**, use `settings.json` deny rules:

```json
{
  "permissions": {
    "deny": ["Read(.env)", "Read(.env.*)", "Read(credentials.json)"]
  }
}
```

See [AI Agent Security Guide](../../templates/security/AI-AGENT-SECURITY-GUIDE.md) for the full tiered approach.

---

## Token Optimization Techniques

### Know Your Budget

Claude Code's 200k token window fills from multiple sources simultaneously. Performance degrades before you hit the ceiling — quality drops noticeably past ~120k tokens due to attention diffusion.

**Detailed breakdown**: [Context Management at Scale](./ADVANCED-WORKFLOWS.md#1-context-management-at-scale)

### Reduce Initial Overhead

| Technique | Typical Savings | How | Details |
|-----------|----------------|-----|---------|
| `.claudeignore` | Up to 50%+ of initial scan | Add build artifacts, deps, lock files | See [above](#claudeignore) |
| Disable unused MCP servers | 0.5-30k per server | Project `.mcp.json`, not global | [MCP-CONTEXT.md](../mcp/MCP-CONTEXT.md) |
| Keep CLAUDE.md under 200 lines | 1-3k tokens baseline | Reference vs embed, link to detail docs | [CLAUDE-MD-GUIDELINES](../../templates/claude-md/CLAUDE-MD-GUIDELINES.md) |
| Tool Search (default on) | ~89% reduction in MCP overhead | Don't disable it | [MCP-CONTEXT.md](../mcp/MCP-CONTEXT.md) |
| Lean skill descriptions | ~2% of context budget | Keep descriptions short | [ADVANCED-WORKFLOWS.md S4](./ADVANCED-WORKFLOWS.md#4-extension-points-skills-hooks-mcp) |

### Reduce In-Session Growth

| Technique | What It Prevents |
|-----------|-----------------|
| Grep/Glob before Read | Reading entire files when you only need 5 lines |
| Subagents for exploration | Dumping 500 lines of search results into main context |
| `/compact` at phase boundaries | Stale investigation debris accumulating |
| Externalize to files | Re-debating decisions lost to compaction |
| Targeted file reads (offset/limit) | Loading 2000 lines when you need 20 |

**Deep dive**: [ADVANCED-WORKFLOWS.md Sections 1 & 3](./ADVANCED-WORKFLOWS.md)

---

## Isolation as Context Strategy

Isolation isn't just about parallel work — it's a context management technique. Every tool that runs in a separate context window keeps its noise out of your main conversation.

### Subagents as Scouts

Each subagent gets a **fresh 200k context window**. Parent context is not inherited. Only the summarized result (1-5k tokens) returns to the main conversation.

**The pattern**: Delegate anything that would generate >5k tokens of output.

| Task | Without Subagent | With Subagent |
|------|-----------------|---------------|
| Search 50 files for a pattern | ~25k tokens of grep output in your context | ~2k token summary returned |
| Read and analyze 10 test files | ~40k tokens of file content | ~3k findings summary |
| Review security of 5 endpoints | ~15k of code + reasoning | ~2k actionable report |

**Model selection for scouts**: Use haiku for pattern matching and file scanning (fast, cheap, sufficient). Use sonnet/opus for analysis that requires reasoning depth.

**Details**: [ADVANCED-WORKFLOWS.md Section 3](./ADVANCED-WORKFLOWS.md#3-agents-and-sub-agents) | [Custom Agents](../../templates/agents/README.md)

### Worktree Isolation

Worktrees provide **filesystem isolation** — a separate working copy of the repo. Combined with subagent **context isolation**, you get parallel work without file conflicts or context pollution.

```
Filesystem isolation (worktrees)     prevents merge conflicts
     +
Context isolation (subagents)        prevents token bloat
     =
Parallel work without interference
```

- **Session-level**: `claude --worktree` (or `-w`) starts a session in a new worktree
- **Agent-level**: `isolation: worktree` in agent frontmatter
- **Detached**: Add `--tmux` to fire-and-forget in a tmux session

**Details**: [GIT-WORKTREES.md](./GIT-WORKTREES.md) | [Custom Agents](../../templates/agents/README.md)

### Background Agents (Ctrl+B)

Press **Ctrl+B** to detach a running subagent to the background. Your main session returns immediately to the prompt. The background agent works in its own context and surfaces results when done.

**Context benefit**: Long-running operations (test suites, documentation fetches, code scanning) don't block your interactive work or consume your active context window.

### Agent Teams for Aggressive Context Management

Agent teams (experimental) coordinate via a **shared task list on disk**. Because tasks persist independently of conversation history, each teammate can `/compact` and `/clear` aggressively without losing the project roadmap.

| Approach | Context Model | Coordination | Best For |
|----------|--------------|--------------|----------|
| **Subagents** | Parent dispatches, child returns summary | Through parent | Sequential dependent tasks |
| **Agent teams** | Independent 200k windows per teammate | Shared task list + mailbox | Parallel independent tasks |

**Details**: [ADVANCED-WORKFLOWS.md Section 3](./ADVANCED-WORKFLOWS.md#agent-teams-experimental) | [Custom Agents](../../templates/agents/README.md)

---

## Scaling: Large Codebases & Long Projects

Context engineering matters more as codebases grow. A 5-file project doesn't need `.claudeignore`; a 300k-line monorepo is unworkable without it.

### Progressive Exploration

Never read entire files blind. Follow this pattern:

```
Grep/Glob  →  identify relevant files
     ↓
Read (offset/limit)  →  targeted sections only
     ↓
Subagent (Explore)  →  broad searches in isolated context
```

The Explore subagent is Claude's built-in scout — optimized for read-only codebase mapping at three thoroughness levels (quick, medium, very thorough). Use it for broad searches; use direct Grep/Glob for targeted lookups.

### Session-Per-Workstream

Treat sessions like git branches — one concern per session.

- `/clear` between unrelated tasks (don't mix a bug fix with a feature in the same session)
- `/rename` early for discoverability when resuming later
- Context from one workstream is noise for another

### Multi-Session Continuity

For work spanning multiple sessions:

| Mechanism | What It Does | When to Use |
|-----------|-------------|-------------|
| Plan files (`.claude/plans/`) | Survive compaction and restarts | Multi-step implementations |
| `HANDOFF.md` | Structured state for handoffs | Team handoffs, multi-day projects |
| Session Memory (v2.1.30+) | Automatic cross-session context | Simple continuity |

**Decision guide**: [Built-in vs Custom](../decisions/BUILTIN_VS_CUSTOM.md)

### When to Start Over

Start a fresh session when:

- Context has compacted 1-2 times and Claude re-debates settled decisions
- Switching from investigation to implementation phase
- The session feels "confused" — vague or repetitive responses
- You're switching between unrelated projects

The cost of starting fresh is low (CLAUDE.md reloads, plan files persist). The cost of continuing in a polluted context is higher — degraded reasoning, repeated mistakes, lost nuance.

---

## Session Management Strategies

### When to Start Fresh vs Continue

| Situation | Action | Why |
|-----------|--------|-----|
| New feature, clean scope | Fresh session | Clean context, no stale assumptions |
| Resuming mid-feature | `claude -c` or `--resume` | Preserves recent decisions |
| Context feels heavy (>120k) | `/compact` then continue | Reclaims space without losing thread |
| Switching between projects | Fresh session | Cross-project context is noise |
| After completing a phase | `/compact` with custom instructions | Clear investigation, keep decisions |
| After 1-2 compactions | Fresh session | Compacted context loses nuance |

### Compact Timing

Use `/compact` proactively at natural breakpoints — after investigation before implementation, before large test runs, between phases. Don't wait for auto-compact at 95%.

**Detailed rules by work type**: [ADVANCED-WORKFLOWS.md Section 1](./ADVANCED-WORKFLOWS.md#when-to-compact-deliberately)

### Externalizing State

Write decisions, plans, and findings to files instead of relying on conversation memory. The best context management is not needing context at all.

**Patterns and templates**: [ADVANCED-WORKFLOWS.md Section 1](./ADVANCED-WORKFLOWS.md#externalizing-state)

---

## Sources

| Source | Type | Date | What It Covers |
|--------|------|------|---------------|
| [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Official | 2026 | Three loading strategies, skills system, just-in-time context |
| [Anthropic: Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) | Official | 2026 | CLAUDE.md sizing, /clear, /compact, kitchen-sink anti-pattern |
| [Anthropic: Subagents](https://code.claude.com/docs/en/sub-agents) | Official | 2026 | Isolation, skill injection, memory, worktree support |
| [Anthropic: Agent Teams](https://code.claude.com/docs/en/agent-teams) | Official | 2026 | Task list, mailbox, teammate coordination |
| [Anthropic: Settings (.claudeignore)](https://code.claude.com/docs/en/settings) | Official | 2026 | .claudeignore syntax and behavior |
| [Martin Fowler: Context Engineering](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html) | Industry | 2025 | Five strategies, guidance vs instructions, build configs gradually |
| [Boris Cherny: Worktree Support](https://www.threads.com/@boris_cherny/post/DVAAnexgRUj) | Official | Feb 2026 | --worktree flag, subagent worktrees, non-git SCM hooks |
| [ClaudeLog: Token Optimization](https://claudelog.com/faqs/how-to-optimize-claude-code-token-usage/) | Community | 2026 | .claudeignore patterns, buffer reduction, MCP pruning |
| [matt1398/claude-devtools](https://github.com/matt1398/claude-devtools) | Community | 2026 | Per-turn token attribution, context reconstruction |

**Last verified**: 2026-02-21

---

## See Also

- [Consistency at Scale](./CONSISTENCY-AT-SCALE.md) — Unified consistency strategy: tiered context, routing tables, ADRs, refactoring coordination
- [ADVANCED-WORKFLOWS.md](./ADVANCED-WORKFLOWS.md) — Deep dive: compaction rules, externalizing state, subagent patterns, agent teams
- [CLAUDE-MD-GUIDELINES.md](../../templates/claude-md/CLAUDE-MD-GUIDELINES.md) — Keeping CLAUDE.md under 200 lines, decision tree, reference vs embed
- [MCP-CONTEXT.md](../mcp/MCP-CONTEXT.md) — Tool Search benchmarks, MCP token costs, Claude Code vs Codex
- [GIT-WORKTREES.md](./GIT-WORKTREES.md) — Worktree mechanics, Claude Code integration, parallel development
- [Custom Agents](../../templates/agents/README.md) — Agent frontmatter, patterns, memory, isolation, teams
- [AI Agent Security Guide](../../templates/security/AI-AGENT-SECURITY-GUIDE.md) — Settings.json deny rules for secrets
- [COST_OPTIMIZATION_GUIDE.md](../../templates/testing/COST_OPTIMIZATION_GUIDE.md) — Model pricing and testing costs
- [CLAUDE-CODE-STORAGE.md](./CLAUDE-CODE-STORAGE.md) — Session files, disk management, history search
- [Built-in vs Custom](../decisions/BUILTIN_VS_CUSTOM.md) — When to use built-in vs custom session continuity

---
