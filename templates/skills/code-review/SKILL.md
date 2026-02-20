---
name: local-review
description: |
  Unified local code review with multi-agent analysis, false-positive
  filtering, and root-cause analysis. Runs 5 adversarial review agents,
  evaluates findings for validity, and categorizes root causes for real
  issues. Use for reviewing local changes before committing or creating PRs.
  Triggers on "/local-review", "review my changes", "review my code",
  "code review", "what did I break", "check my changes".
  Do NOT use for database schema reviews (use database-review skill).
  Do NOT use for PR reviews (use pr-review-toolkit plugin).
---

# Unified Code Review

Multi-agent adversarial code review with built-in false-positive filtering and root-cause analysis.

## Quick Reference

```
/local-review                          # Full review of uncommitted changes (5 agents + eval + root-cause)
/local-review --quick                  # Quick review (3 agents, no root-cause)
/local-review --scope staged           # Review only staged changes
/local-review --scope last-3           # Review last 3 commits
/local-review --scope branch           # Review branch vs main
```

For project-specific context, create `.claude/review-context.md` — see [review-context.md.template](./review-context.md.template).

---

## Guardrails

**NEVER:**
- Report a finding without reading the actual source file (not just the diff)
- Score a finding >60 without tracing the execution path (how is it called? what are the inputs?)
- Flag "race conditions" in synchronous JavaScript code (JS is single-threaded)
- Flag patterns listed as known exceptions in `review-context.md`
- Skip the evaluation phase — every finding must pass false-positive filtering
- Report a finding with confidence <70

**ALWAYS:**
- Read at least 20 lines of context around every flagged line
- Follow function calls one level deep before scoring
- Apply `references/false-positive-patterns.md` before including any finding in output
- Categorize surviving findings using `references/bug-categories.md`
- Complete all phases in order (gather → agents → evaluate → root-cause → output)

---

## Arguments

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--scope` | `uncommitted`, `staged`, `last`, `last-N`, `branch` | `uncommitted` | What to review |
| `--min-score` | 0-100 | 60 | Minimum severity to report |
| `--quick` | flag | false | 3 agents, no root-cause analysis |
| `--full` | flag | true | 5 agents + evaluation + root-cause |

---

## Phase 1: Gather Changes

### 1a. Get diff based on scope

```bash
# uncommitted (default)
git diff HEAD

# staged only
git diff --cached

# last commit
git show HEAD

# last N commits
git log -N --oneline && git diff HEAD~N..HEAD

# branch vs main
git diff main...HEAD
```

### 1b. Identify changed files and tech stack

```bash
git diff --name-only HEAD
ls package.json tsconfig.json pyproject.toml requirements.txt 2>/dev/null
```

### 1c. Load project context (optional)

```bash
cat .claude/review-context.md 2>/dev/null || echo "No project context"
```

If `review-context.md` exists, load:
- **App scale/context** — affects severity of scale-related findings
- **Known exceptions** — patterns to suppress (severity → 0)
- **Trusted data sources** — reduces false positive injection findings
- **Completed work** — one-time scripts get lower priority (severity × 0.5)

---

## Phase 2: Run Review Agents

Launch agents in parallel. Each agent reviews the SAME diff independently.

### Full mode (5 agents — default)

1. **Security Auditor** — Injection, auth bypass, secrets, OWASP top 10
2. **Bug Hunter** — Null checks, race conditions, error handling, edge cases
3. **Architecture Critic** — Code duplication, coupling, abstraction issues
4. **Test Skeptic** — Coverage gaps, weak assertions, missing edge cases
5. **Production Pessimist** — Scale issues, resource leaks, failure modes

### Quick mode (3 agents — `--quick`)

1. **Security Auditor** — Critical vulnerabilities only
2. **Bug Hunter** — Production-breaking bugs only
3. **Production Pessimist** — Reliability issues only

### Agent requirements

Each agent MUST follow these steps for every potential finding:

1. **Read the source file** — not just the diff. Open the file and read the surrounding context.
2. **Trace the execution path** — how is this function called? What are the realistic inputs?
3. **Self-evaluate confidence (0-100)** — how certain are you this is a real issue?
4. **Check false-positive patterns** — consult `references/false-positive-patterns.md`. Is this a known false positive?
5. **Only report if confidence >= 70** — drop anything below this threshold.

Agent persona details: see `references/agent-personas.md`.
Technology-specific patterns: see `references/technology-patterns.md` and `references/patterns-*.md`.
Scoring guidelines: see `references/severity-scoring.md`.

---

## Phase 3: Evaluate Findings

After all agents complete, evaluate every finding for validity.

### 3a. Cross-agent deduplication

- Same issue from multiple agents = higher confidence
- Keep highest score, merge context from each perspective
- Note cross-agent agreement in output

### 3b. Apply false-positive filtering

For each finding, apply the 3-question framework from `references/false-positive-patterns.md`:

1. **Is the bug real?** Trace the actual call flow.
2. **Is the solution sustainable?** Does the fix create more complexity than the bug?
3. **Is there a better alternative?** Simpler guard, fail-fast, monitor first?

### 3c. Apply review-context.md adjustments

If project context was loaded:
- **Known exceptions** → severity = 0, note "Known exception: {reason}"
- **Completed work** → severity × 0.5, note "Lower priority: completed work"
- **Trusted data sources** → severity = 0, note "Trusted data source"

### 3d. Assign verdicts

| Verdict | Criteria | Action |
|---------|----------|--------|
| **REAL BUG** | Traced call flow confirms the issue | Include in output |
| **MARGINAL** | Theoretically possible, unlikely in practice | Include with note |
| **FALSE POSITIVE** | Not a real issue given actual usage | Remove from output |
| **LOW PRIORITY** | Real but low impact | Include if above `--min-score` |

### 3e. Filter

Remove all FALSE POSITIVEs from the output. Apply `--min-score` threshold to remaining findings.

---

## Phase 4: Root-Cause Analysis

**Skipped in `--quick` mode.**

For each surviving finding with verdict REAL BUG or MARGINAL, apply the framework from `references/bug-categories.md`:

### 4a. Categorize the bug

Assign one category: state sync, missing validation, tight coupling, race condition, resource lifecycle, protocol mismatch.

### 4b. Determine output depth

**Simple bug** (first occurrence, obvious fix, rarely-touched code):
```
Root cause: [one sentence]
No strategic changes needed.
```

**Complex or recurring bug** (pattern detected, new-dev-would-repeat, cross-file fix):
```
Bug category: [category]
Why easy to introduce: [what made this possible]
If this recurs: [structural improvement — not a pattern name]
Recommendation: Fix now / Backlog / Monitor
```

---

## Phase 5: Output

### Report format

```markdown
# Code Review: {scope}

## Summary
- **Files Changed**: {count} | **Lines**: +{added}/-{removed}
- **Findings**: {total} found → {surviving} after evaluation
- **Verdicts**: {real_bug} real bugs, {marginal} marginal, {filtered} filtered out
- **Context Applied**: {yes/no} (from .claude/review-context.md)

## Critical Issues (80+)

### [{CATEGORY}] {Title}
**File**: {path}:{line}
**Score**: {score} | **Verdict**: {verdict} | **Agent**: {agent_name}
**Confidence**: {confidence}/100

**Problem**: {description}

**Evidence**:
```{lang}
{code snippet with context}
```

**Fix**:
```{lang}
{fixed code}
```

**Root Cause**: {category} — {one-line explanation}
{strategic note if complex bug}

---

## High Priority (60-79)
...

## Evaluation Summary
- **Total findings from agents**: {N}
- **False positives filtered**: {N} ({percentage}%)
- **Marginal (included with caveats)**: {N}
- **Context adjustments applied**: {N}
```

---

## Examples

### Quick staged review

```
/local-review --quick --scope staged
```

Runs 3 agents on staged changes. No root-cause phase. Fast pre-commit sanity check.

### Full branch review

```
/local-review --scope branch
```

Runs 5 agents on all changes since branching from main. Full evaluation and root-cause analysis. Use before creating a PR.

### Review with custom threshold

```
/local-review --scope last-3 --min-score 80
```

Reviews last 3 commits, showing only critical issues (80+).

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Too many false positives | Agents not reading source files | Verify guardrails are followed; create `review-context.md` |
| Review too slow | Full mode on large diff | Use `--quick` or narrow `--scope` to `staged` |
| Shallow findings | Agents only reading diff, not source | Guardrails require reading 20 lines of context + tracing calls |
| Phase skipping | Quick mode skips root-cause by design | Use `--full` (default) for complete analysis |
| Known patterns flagged | No project context file | Create `.claude/review-context.md` from template |
| All findings filtered | `--min-score` too high or too many known exceptions | Lower `--min-score` or audit your `review-context.md` |

---

## Integration

- **`/push` command** — run `/local-review --quick --scope staged` before pushing
- **Pre-commit hooks** — trigger review automatically on commit
- **CI/CD** — use `--scope branch --min-score 80` for automated PR checks

---

## References

| Reference | Purpose |
|-----------|---------|
| [agent-personas.md](./references/agent-personas.md) | Agent definitions and prompts |
| [severity-scoring.md](./references/severity-scoring.md) | Scoring guidelines |
| [technology-patterns.md](./references/technology-patterns.md) | Language-specific patterns |
| [patterns-typescript.md](./references/patterns-typescript.md) | TypeScript patterns |
| [patterns-react.md](./references/patterns-react.md) | React patterns |
| [patterns-python.md](./references/patterns-python.md) | Python patterns |
| [false-positive-patterns.md](./references/false-positive-patterns.md) | Evaluation framework and common false positives |
| [bug-categories.md](./references/bug-categories.md) | Root-cause categorization |
| [review-context.md.template](./review-context.md.template) | Project context template |
