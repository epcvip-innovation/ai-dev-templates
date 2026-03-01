---
id: consistency-at-scale
title: "Consistency at Scale: Orchestrating Large Repos with Claude Code"
description: "Unified strategy for maintaining consistency across complex codebases — tiered context, routing, ADRs, refactoring coordination"
audience: power-user
---

# Consistency at Scale: Orchestrating Large Repos with Claude Code

[← Back to Main README](../../README.md) | [Context Engineering](./CONTEXT-ENGINEERING.md) | [Advanced Workflows](./ADVANCED-WORKFLOWS.md)

How to keep a large, multi-module codebase consistent when using Claude Code across many sessions, contributors, and features.

**Audience**: Developers working on repos large enough that Claude starts "forgetting" patterns, re-debating settled decisions, or producing inconsistent code across sessions.

---

## 1. When You Need This Guide

Not every project needs explicit consistency infrastructure. Use this decision tree:

```
Your repo has...
  >50 files across multiple modules?           → YES: Read on
  >3 people (or AI agents) making changes?     → YES: Read on
  Sessions spanning days/weeks on one feature?  → YES: Read on
  History of "Claude forgot X" across sessions? → YES: Read on

  None of the above?
  → A well-written CLAUDE.md is sufficient.
    See: CLAUDE-MD-GUIDELINES.md
```

The patterns below compose existing Claude Code mechanisms into a unified strategy. Each section cross-references the detailed guide rather than duplicating it.

---

## 2. The Three-Tier Context Model

Where does project knowledge live at runtime? Three tiers, from always-present to on-demand:

| Tier | What Lives Here | Claude Code Mechanism | Token Cost | Refresh Cadence |
|------|----------------|----------------------|------------|-----------------|
| **1 — Hot** | Routing, critical warnings, navigation | CLAUDE.md (auto-loaded every session) | 1-3k tokens (always) | Quarterly audit |
| **2 — Specialist** | Domain expertise, review patterns, conventions | Custom agents with `memory:` + skills | On-demand (per invocation) | When patterns change |
| **3 — Cold** | Full standards, ADRs, domain guides | Spoke docs (read when needed) | On-demand (per read) | When content changes |

### How It Works

**Tier 1 — Hot memory** is your CLAUDE.md. It's loaded every session, so every token counts. Keep it under 200 lines. Its job is *routing* — telling Claude where to find deeper knowledge, not containing that knowledge itself. See [CLAUDE-MD-GUIDELINES.md](../../templates/claude-md/CLAUDE-MD-GUIDELINES.md) for the decision tree and section limits.

**Tier 2 — Specialist knowledge** lives in custom agents and skills. An agent configured with `memory: project` accumulates knowledge in its `MEMORY.md` across sessions. Skills bundle instructions that load only when invoked. This tier handles domain expertise that doesn't need to be in every session. See [Custom Agents](../../templates/agents/README.md) for agent patterns and [Skills README](../../templates/skills/README.md) for skill design.

**Tier 3 — Cold reference** is your spoke documentation — coding standards, architecture decisions, domain guides, API docs. Claude reads these files when it encounters relevant work. The key is that Tier 1 (CLAUDE.md) points Claude to the right Tier 3 doc via routing tables (Section 4 below).

### Relationship to the Five Pillars

This model complements the [Five Pillars](./CONTEXT-ENGINEERING.md) in CONTEXT-ENGINEERING.md. The pillars describe *what you can control* (selection, compression, ordering, isolation, format). The three tiers describe *where knowledge lives at runtime*. Use the pillars to optimize each tier; use the tiers to organize your project's knowledge architecture.

---

## 3. Context Budget Discipline

**Core principle**: If a tool can enforce a rule deterministically, don't spend context tokens teaching it to Claude.

Every line in CLAUDE.md costs tokens in every session. Lines that duplicate what a linter, formatter, or pre-commit hook already enforces are wasted budget.

| Rule Type | Enforce With | NOT With CLAUDE.md |
|-----------|-------------|-------------------|
| Import order | Formatter (isort, Prettier) | Redundant if formatter runs |
| Line length | Linter (ESLint, Ruff) | Redundant if linter runs |
| No `console.log` | Pre-commit hook | Redundant if hook runs |
| Function length <50 lines | Pre-commit hook / CI | Redundant if hook runs |
| **Use project's error handling pattern** | **CLAUDE.md** | Tool can't know this |
| **Domain naming conventions** | **CLAUDE.md** | Tool can't know this |
| **Deprecated API patterns to avoid** | **CLAUDE.md** | Tool can't know this |

**The nuance**: If your linter runs automatically (pre-commit hook or CI), Claude will see the failure and self-correct. The CLAUDE.md entry is redundant. If your linter does NOT run automatically, the entry has value because Claude won't get corrective feedback.

**Decision rule**: Reserve CLAUDE.md for things only Claude can know — project-specific patterns, domain terminology, architectural decisions, and conventions that no tool can enforce.

See [Hooks README](../../templates/hooks/README.md) for enforcement patterns. See [ANTI_SLOP_STANDARDS.md](../../templates/standards/ANTI_SLOP_STANDARDS.md) for standards worth enforcing via hooks.

---

## 4. Routing Tables in CLAUDE.md

When a repo has multiple modules or areas, a routing table in CLAUDE.md tells Claude which spoke doc to read before working in a specific area. Low token cost, high impact.

### Template

```markdown
## Routing

| Working in... | Read first |
|--------------|-----------|
| `src/auth/` | [AUTH.md](docs/AUTH.md) — OAuth flow, token handling |
| `src/api/` | [API-CONVENTIONS.md](docs/API-CONVENTIONS.md) — endpoint patterns, error format |
| `tests/` | [TESTING.md](docs/TESTING.md) — fixture setup, naming conventions |
| Database migrations | [DB-GUIDE.md](docs/DB-GUIDE.md) — migration workflow, naming |
| Any architectural change | [docs/decisions/](docs/decisions/) — check for existing ADRs |
```

### When to Use

- **Use routing tables** when your repo has 5+ distinct areas with different conventions
- **Skip routing tables** when your repo has <5 areas — a simple "Documentation" section listing 2-3 docs is sufficient

### Why It Works

CLAUDE.md is always loaded, so the routing table is always available. When Claude starts working in `src/auth/`, it sees the routing entry and reads the AUTH.md spoke doc *before* generating code. This prevents Claude from applying generic patterns where project-specific ones exist.

The routing table follows the [CLAUDE-MD-GUIDELINES.md](../../templates/claude-md/CLAUDE-MD-GUIDELINES.md) section limit of 15 lines for Documentation Maps. Keep entries concise — one line per area.

---

## 5. Architectural Decision Records (ADRs) for AI Consistency

**The problem**: Claude re-debates decisions from previous sessions. You chose JWT over session cookies three weeks ago with good reasons. In a new session, Claude proposes session cookies because it doesn't know about the prior decision.

**The solution**: Lightweight ADRs that Claude reads before proposing alternatives.

### Template

```markdown
# ADR-001: Use JWT for Authentication

**Status**: Accepted
**Date**: 2026-01-15

## Context
We need stateless authentication for our API. Considered JWT and session cookies.

## Decision
JWT with httpOnly cookies. Access tokens expire in 15 min, refresh tokens in 7 days.

## Consequences
- Stateless — no server-side session store needed
- Trade-off: token revocation requires a blocklist
- All auth endpoints follow the pattern in AUTH.md
```

### Where to Put Them

Use a `docs/decisions/` directory. This repo already uses this pattern (see `docs/decisions/BUILTIN_VS_CUSTOM.md` and `docs/decisions/why-wsl.md`).

### How Claude Uses Them

Add one line to your CLAUDE.md routing table:

```markdown
| Any architectural change | [docs/decisions/](docs/decisions/) — check existing ADRs first |
```

When Claude encounters an architectural question, it reads the relevant ADR and respects the settled decision instead of re-debating from scratch.

### When to Create ADRs

- When a decision in a HANDOFF.md keeps recurring across sessions — promote it to a permanent ADR
- When you choose between two valid approaches and want to prevent future flip-flopping
- When the *why* behind a choice isn't obvious from the code alone

**Don't over-ADR**: Not every decision needs a record. Reserve them for choices that Claude is likely to question in future sessions. See [ADVANCED-WORKFLOWS.md](./ADVANCED-WORKFLOWS.md) Section 7 on externalizing state.

---

## 6. Coordinating Codebase-Wide Refactors

Large refactors (rename a pattern across 30 files, migrate from one library to another) exceed a single context window. Three approaches, from simplest to most controlled:

### Start with `/batch`

Claude Code's built-in `/batch` skill (v2.1.63+) handles parallel code migrations. It interactively plans the migration, then executes across dozens of agents, each in its own git worktree with isolation and testing before creating a PR.

**Use `/batch` when**: The migration is straightforward and mechanical (rename, library swap, pattern replacement). Example: `/batch migrate src/ from Solid to React`

**Use manual patterns when**: You need more control, the migration requires judgment calls, or `/batch` doesn't fit the change.

### Pattern 1 — Plan File as Contract

Best for: Medium refactors (10-30 files) where you want to stay in control.

1. Create `plan.md` with explicit file list, the pattern to apply, and verification criteria
2. Work through files in batches of 5-10
3. Run `/compact` between batches to keep context fresh
4. Track progress with checkboxes in the plan file

### Pattern 2 — Agent-Per-Batch

Best for: Large refactors (30+ files) that are mostly mechanical.

1. Define an implementer agent with `isolation: worktree`
2. Give each agent a non-overlapping file scope (e.g., `src/auth/`, `src/api/`)
3. Merge worktree PRs sequentially, resolving conflicts as they arise

See [Custom Agents](../../templates/agents/README.md) for the implementer pattern and [GIT-WORKTREES.md](./GIT-WORKTREES.md) for worktree mechanics.

### Pattern 3 — Phased

Best for: Mixed refactors with both mechanical and judgment-required changes.

1. **Phase 1 — Automated**: Use regex/sed for purely mechanical changes (renames, import paths)
2. **Phase 2 — AI-assisted**: Use Claude for changes requiring judgment (API redesign, logic migration)
3. **Phase 3 — Verification**: Run a reviewer agent against all changes to check consistency

### Decision Guide

| Situation | Approach |
|-----------|----------|
| Straightforward migration, <100 files | `/batch` |
| Medium refactor, want manual control | Plan file (Pattern 1) |
| Large mechanical refactor, parallelizable | Agent-per-batch (Pattern 2) |
| Mixed mechanical + judgment changes | Phased (Pattern 3) |
| Cross-repo consistency change | Pattern 2 with one agent per repo |

---

## 7. Large File Strategies

Claude's effectiveness tends to degrade with files over ~500 lines, and significantly above ~2000 lines. These aren't hard limits — some files (migrations, schemas, generated code) are necessarily large. But awareness helps.

### Detection

```bash
# Find largest files in your source directories
find src/ -name "*.ts" -o -name "*.py" | xargs wc -l | sort -rn | head -20
```

### Strategies

**For files that can be split**: Break into modules before asking Claude to work on them. A 1500-line utility file split into 3 focused modules is easier for Claude to reason about.

**For files that must stay large**: Use offset/limit when reading. Instead of loading the entire file, tell Claude to read specific sections:

```
Read src/schema.ts lines 200-350  # Just the user model
```

Point Claude to the right section via CLAUDE.md routing:

```markdown
| Schema changes | Read `src/schema.ts` lines 1-50 (index), then relevant model section |
```

**For generated files**: Add to `.claudeignore` so they don't consume context. See [CONTEXT-ENGINEERING.md](./CONTEXT-ENGINEERING.md) for `.claudeignore` patterns.

**Optional — warning hook**: A `PreToolUse` hook that warns (not blocks) when Claude reads a very large file without specifying a line range. This is a suggestion, not a gate — sometimes reading the full file is exactly what's needed. See [Hooks README](../../templates/hooks/README.md) for hook patterns.

---

## 8. The Consistency Stack

All the mechanisms above compose into a stack, ordered from strongest enforcement to weakest:

```
┌─────────────────────────────────────────────────────────┐
│  DETERMINISTIC ENFORCEMENT              ← strongest     │
│  Pre-commit hooks, linters, CI checks, formatters       │
│  → They run every time. Claude can't bypass them.       │
├─────────────────────────────────────────────────────────┤
│  STRUCTURAL CONSISTENCY                                 │
│  CLAUDE.md routing, spoke docs, ADRs, .claudeignore     │
│  → Shape what Claude sees. Guide without forcing.       │
├─────────────────────────────────────────────────────────┤
│  KNOWLEDGE CONTINUITY                                   │
│  Session handoffs, agent memory, plan files              │
│  → Preserve decisions across sessions and compaction.   │
├─────────────────────────────────────────────────────────┤
│  ISOLATION & PARALLEL SAFETY                            │
│  Worktrees, subagents, scoped changes                   │
│  → Prevent agents from stepping on each other.          │
├─────────────────────────────────────────────────────────┤
│  BUILT-IN SKILLS                                        │
│  /simplify (quality + compliance), /batch (migrations)  │
│  → Automated consistency checks and parallel execution. │
├─────────────────────────────────────────────────────────┤
│  ADVISORY GUIDANCE                      ← weakest       │
│  CLAUDE.md instructions, prompt conventions              │
│  → Claude follows them most of the time, but can drift. │
└─────────────────────────────────────────────────────────┘
```

**The common mistake**: Over-investing in the bottom (writing detailed CLAUDE.md instructions) while under-investing in the top (hooks and linters that enforce deterministically). A pre-commit hook that rejects functions over 50 lines is more reliable than a CLAUDE.md instruction saying "keep functions under 50 lines."

**Start from the top**: For any consistency concern, first ask: "Can a hook or linter enforce this?" If yes, add the hook. If no, move down the stack.

**`/simplify`**: Claude Code's built-in bundled skill (v2.1.63+) uses parallel agents for code quality, efficiency, and CLAUDE.md compliance. Try it before building custom review workflows — it's a ready-made consistency enforcer at the "built-in skills" tier.

See [ADVANCED-WORKFLOWS.md](./ADVANCED-WORKFLOWS.md) Section 5 for the Predictability Stack — the consistency stack is the predictability stack applied to multi-session, multi-contributor work.

---

## 9. Quarterly Consistency Audit

Consistency degrades over time. Run this checklist quarterly (or when onboarding a new contributor):

- [ ] **CLAUDE.md size**: Still under 200 lines? Run `/audit-claude-md` if available
- [ ] **Routing table**: Does it reflect the current repo structure? Any new modules missing?
- [ ] **Spoke docs**: Are they current? Any dead links? Run link-checker if available
- [ ] **Hooks**: Still running? Any new patterns that should be enforced deterministically?
- [ ] **ADRs**: Any decisions from recent HANDOFF.md files that should become permanent ADRs?
- [ ] **Agent memory**: Review agent `MEMORY.md` files for stale or incorrect knowledge
- [ ] **.claudeignore**: Any new generated/build directories that should be excluded?
- [ ] **Standards**: Do ANTI_SLOP_STANDARDS or project-specific standards need updates?

See [CLAUDE-MD-GUIDELINES.md](../../templates/claude-md/CLAUDE-MD-GUIDELINES.md) for the quarterly audit process and bloat detection.

---

## See Also

**Core Mechanisms** (detailed guides for each layer of the consistency stack):
- [CONTEXT-ENGINEERING.md](./CONTEXT-ENGINEERING.md) — Five pillars, .claudeignore, token optimization, session management
- [ADVANCED-WORKFLOWS.md](./ADVANCED-WORKFLOWS.md) — Context budgets, planning systems, subagents, predictability stack
- [GIT-WORKTREES.md](./GIT-WORKTREES.md) — Worktree mechanics, Claude Code integration, parallel development
- [CLAUDE-MD-GUIDELINES.md](../../templates/claude-md/CLAUDE-MD-GUIDELINES.md) — Keeping CLAUDE.md lightweight, decision tree, reference vs embed

**Enforcement & Standards**:
- [Hooks README](../../templates/hooks/README.md) — Deterministic enforcement patterns, 14 hook events
- [ANTI_SLOP_STANDARDS.md](../../templates/standards/ANTI_SLOP_STANDARDS.md) — Measurable quality gates with grep patterns
- [AI Agent Security Guide](../../templates/security/AI-AGENT-SECURITY-GUIDE.md) — Tiered security for AI agents

**Session Continuity**:
- [Custom Agents](../../templates/agents/README.md) — Agent memory, specialist patterns, worktree isolation
- [Session Handoff command](../../templates/slash-commands/ai-dev-workflow/commands/session-handoff.md) — Drift detection, HANDOFF.md, context continuity
- [Built-in vs Custom](../decisions/BUILTIN_VS_CUSTOM.md) — When to use built-in features vs custom tooling

---
