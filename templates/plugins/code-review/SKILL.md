---
name: local-code-review
description: Multi-agent adversarial code review for local git changes. Triggers on "/local-review", "review my changes", "review recent work", "code review", or "what did I break". Runs 5 parallel review perspectives, scores findings by severity, and outputs actionable fixes.
---

# Local Code Review

Multi-agent adversarial code review for uncommitted or recently committed changes.

## Trigger Phrases

- "/local-review", "/local-code-review"
- "review my changes", "review my code"
- "code review", "review recent work"
- "what did I break", "check my changes"

## Arguments

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--scope` | `uncommitted`, `staged`, `last`, `last-N`, `branch` | `uncommitted` | What to review |
| `--min-score` | 0-100 | 60 | Minimum severity to report |
| `--lite` | flag | false | Use 3-agent lite version |

## Process

### Step 1: Load Project Context

Check for project-specific review context:

```bash
# Look for review context file
if [ -f ".claude/review-context.md" ]; then
  # Load context for severity adjustments
  cat .claude/review-context.md
fi
```

**If review-context.md exists:**
- Load known exceptions (reduce severity to 0)
- Load data trust model (adjust injection warnings)
- Load completed work paths (reduce priority)

**If no review-context.md:**
- Use default severity scoring
- Suggest creating one if many false positives

### Step 2: Get Changes to Review

Based on scope argument:

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

### Step 3: Run Review Agents

Launch 5 agents in parallel (or 3 for lite mode):

**Full Version (5 agents):**
1. **Security Auditor** - Injection, auth bypass, secrets, OWASP top 10
2. **Bug Hunter** - Null checks, race conditions, error handling, edge cases
3. **Architecture Critic** - Code duplication, coupling, abstraction issues
4. **Test Skeptic** - Coverage gaps, weak assertions, missing edge cases
5. **Production Pessimist** - Scale issues, resource leaks, failure modes

**Lite Version (3 agents):**
1. **Security Auditor** - Critical vulnerabilities only
2. **Bug Hunter** - Production-breaking bugs only
3. **Production Pessimist** - Reliability issues only

Each agent:
- Reviews all changed files
- Applies technology-specific patterns from `references/technology-patterns.md`
- Scores findings 0-100
- Provides code-level evidence and fixes

### Step 4: Apply Context Adjustments

If review-context.md was loaded:

```python
for finding in all_findings:
    # Check known exceptions
    if matches_known_exception(finding):
        finding.score = 0
        finding.note = "Known exception: {reason}"

    # Check completed work
    if in_completed_work_path(finding.file):
        finding.score *= 0.5
        finding.note = "Lower priority: completed work"

    # Check data trust model
    if is_trusted_data_source(finding.variable):
        finding.score = 0
        finding.note = "Trusted data source"
```

### Step 5: Consolidate and Output

Filter findings by `--min-score` and format:

```markdown
# Code Review: {scope}

## Summary
- **Files Changed**: {count} | **Lines**: +{added}/-{removed}
- **Critical (80+)**: {count} | **High (60-79)**: {count}
- **Context Applied**: {yes/no} (from .claude/review-context.md)

## Critical Issues (80+)

### [{CATEGORY}] {Title}
**File**: {path}:{line}
**Score**: {score}
**Agent**: {agent_name}

**Problem**: {description}

**Evidence**:
```{lang}
{code snippet}
```

**Fix**:
```{lang}
{fixed code}
```

---

## High Priority (60-79)
...

## Filtered by Context
- {N} findings reduced to 0 (known exceptions)
- {N} findings reduced priority (completed work)
```

### Step 6: Recommendations

At the end, suggest:

1. **If many false positives**: "Consider creating `.claude/review-context.md` - see template"
2. **If critical issues**: "Fix critical issues before committing"
3. **If clean**: "No critical issues found. Ready for commit."

## Integration

Works with:
- `/push` command - Run review before push
- Pre-commit hooks - Automatic review on commit
- CI/CD - Use headless mode in GitHub Actions

## References

- [agent-personas.md](./references/agent-personas.md) - Agent definitions
- [severity-scoring.md](./references/severity-scoring.md) - Scoring guidelines
- [technology-patterns.md](./references/technology-patterns.md) - Language patterns
- [review-context.md.template](./review-context.md.template) - Context template
