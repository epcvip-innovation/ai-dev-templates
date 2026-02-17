# Code Review Plugin

Unified multi-agent adversarial code review with built-in false-positive filtering and root-cause analysis. Designed for pre-PR review of uncommitted or recently committed work.

## Quick Start

```bash
# Full review — 5 agents + evaluation + root-cause (default)
/local-review

# Quick review — 3 agents, no root-cause (~40% less tokens)
/local-review --quick
```

## Pipeline

```
Phase 1: Gather Changes    → git diff, load review-context.md
Phase 2: Run Review Agents → 5 (full) or 3 (quick) agents in parallel
Phase 3: Evaluate Findings → false-positive filtering, verdict assignment
Phase 4: Root-Cause         → categorize surviving bugs (skipped in --quick)
Phase 5: Output            → consolidated report with verdicts + root causes
```

## Agents

| # | Agent | Focus | Mode |
|---|-------|-------|------|
| 1 | **Security Auditor** | Injection, auth bypass, secrets | Full + Quick |
| 2 | **Bug Hunter** | Null checks, race conditions, error handling | Full + Quick |
| 3 | **Architecture Critic** | Duplication, coupling, abstractions | Full only |
| 4 | **Test Skeptic** | Coverage gaps, weak assertions | Full only |
| 5 | **Production Pessimist** | Scale issues, resource leaks | Full + Quick |

All agents include self-evaluation: read source files, trace execution paths, confidence scoring (>=70 to report).

## Scope Options

| Command | Scope |
|---------|-------|
| `/local-review` | All uncommitted changes |
| `/local-review --scope staged` | Only staged changes |
| `/local-review --scope last` | Last commit |
| `/local-review --scope last-3` | Last 3 commits |
| `/local-review --scope branch` | Branch vs main |

## Severity Scoring

| Score | Severity | Action |
|-------|----------|--------|
| 80-100 | Critical | Must fix before merge |
| 60-79 | High | Should fix, real risk |
| 40-59 | Medium | Consider fixing |
| 0-39 | Low | Ignore unless critical |

Default: Show 60+ only. Use `--min-score 80` for critical only.

## Installation

See [SKILL-INSTALLATION.md](./SKILL-INSTALLATION.md) for:
- Global vs per-project installation
- Migration from old 3-skill pipeline
- Customizing patterns

## Documentation

| Doc | Purpose |
|-----|---------|
| [SKILL.md](./SKILL.md) | Main skill definition (unified pipeline) |
| [METHODOLOGY.md](./METHODOLOGY.md) | Why multi-agent review works |
| [SKILL-INSTALLATION.md](./SKILL-INSTALLATION.md) | Installation and migration |
| [references/agent-personas.md](./references/agent-personas.md) | Agent definitions with self-evaluation |
| [references/severity-scoring.md](./references/severity-scoring.md) | Scoring guidelines |
| [references/technology-patterns.md](./references/technology-patterns.md) | Language-specific patterns |
| [references/false-positive-patterns.md](./references/false-positive-patterns.md) | Evaluation framework |
| [references/bug-categories.md](./references/bug-categories.md) | Root-cause categorization |
| [review-context.md.template](./review-context.md.template) | Project context template |

## Best Practices

1. **Use staged scope** — review before commit, not after
2. **Start with 80+** — fix critical first, then high
3. **2-3 passes max** — diminishing returns after that
4. **Create review-context.md** — reduces false positives significantly
5. **Trust verdicts** — the evaluation phase filters pedantic suggestions

## See Also

- [INCIDENT-MEMORY.md](../../ci/INCIDENT-MEMORY.md) — Post-mortem templates for when bugs escape review
