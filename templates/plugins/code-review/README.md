# Code Review Plugin

Multi-agent adversarial code review for local git changes. Designed for pre-PR review of uncommitted or recently committed work.

## Quick Start

```bash
# Review uncommitted changes
/local-review

# Lightweight review (3 agents, ~40% less tokens)
/local-review-lite
```

## Versions

| Version | Agents | Focus | Token Cost |
|---------|--------|-------|------------|
| **Full** | 5 | Complete coverage | ~100% |
| **Lite** | 3 | Security, Bugs, Production | ~60% |

### Full Version Agents
1. **Security Auditor** - Injection, auth bypass, secrets
2. **Bug Hunter** - Null checks, race conditions, error handling
3. **Architecture Critic** - Duplication, coupling, abstractions
4. **Test Skeptic** - Coverage gaps, weak assertions
5. **Production Pessimist** - Scale issues, resource leaks

### Lite Version Agents
1. **Security Auditor** - Critical vulnerabilities
2. **Bug Hunter** - Production bugs
3. **Production Pessimist** - Reliability issues

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
- Customizing patterns
- Adding project-specific rules

## Documentation

| Doc | Purpose |
|-----|---------|
| [METHODOLOGY.md](./METHODOLOGY.md) | Why multi-agent review works |
| [SKILL-INSTALLATION.md](./SKILL-INSTALLATION.md) | Installation and customization |
| [references/agent-personas.md](./references/agent-personas.md) | Agent definitions and prompts |
| [references/severity-scoring.md](./references/severity-scoring.md) | Scoring guidelines |
| [references/technology-patterns.md](./references/technology-patterns.md) | Language-specific patterns |

## Output Format

```markdown
# Code Review: uncommitted changes

## Summary
- Files Changed: 12 | Lines: +234/-56
- Critical: 1 | High: 3

## Critical Issues (80+)

### [SECURITY] SQL injection in search endpoint
**File**: src/api/search.ts:45
**Score**: 95
**Agent**: Security Auditor

**Problem**: User input directly interpolated into query.

**Evidence**:
[code block]

**Fix**:
[code block]
```

## Best Practices

1. **Use staged scope** - Review before commit, not after
2. **Start with 80+** - Fix critical first, then high
3. **2-3 passes max** - Diminishing returns after that
4. **Trust your judgment** - Filter pedantic suggestions
5. **Add project patterns** - Customize for your codebase
