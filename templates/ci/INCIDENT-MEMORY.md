# Incident Memory

[← Back to CI README](./README.md)

When a bug reaches production that CI should have caught, close the loop: document what happened, identify the harness gap, and add the missing test. This prevents the same class of bug from recurring.

## Incident Post-Mortem Template

Copy this into your post-mortem doc or GitHub issue:

```markdown
## Incident Post-Mortem: [Title]

**Date**: YYYY-MM-DD
**Severity**: Critical / High / Medium
**Duration**: Time from detection to resolution

### 1. Summary

One paragraph: what happened, who was affected, what was the impact.

### 2. Timeline

| Time | Event |
|------|-------|
| HH:MM | First user report / alert fired |
| HH:MM | Investigation started |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed |
| HH:MM | Verified resolved |

### 3. Root Cause

What was the actual bug? Be specific:
- What code path was affected?
- What input triggered it?
- Why did it pass code review?

### 4. Immediate Fix

- PR link: #NNN
- What was changed?
- Was it a hotfix or a proper fix?

### 5. Harness Gap

**What should have caught this?**

| Layer | Gap |
|-------|-----|
| Unit tests | Missing coverage for [specific case] |
| Integration tests | No test for [specific interaction] |
| Security review | Pattern not in security scanner rules |
| QA review | Flow not in QA checklist |
| Risk policy | Path not classified at correct tier |

**Action items:**
- [ ] Add test: [description] (owner: @name, SLA: 1 week)
- [ ] Update risk policy: reclassify [path] as [tier]
- [ ] Update QA persona checklist: add [flow]
```

## Harness-Gap Issue Template

For GitHub Issues — tracks the specific test that needs adding:

```markdown
---
name: Harness Gap
about: A regression that CI didn't catch
labels: harness-gap, testing
---

## What Wasn't Caught

**Incident**: Link to post-mortem or PR
**Bug class**: [e.g., auth bypass, null reference, UI state corruption]

## What Happened

Brief description of the production bug.

## Missing Coverage

**Layer**: Unit / Integration / E2E / Security / QA
**Specific gap**: What test or check would have caught this?

## Proposed Test

```[language]
// Pseudocode or actual test
test("description of what to test", () => {
  // setup
  // action that triggers the bug
  // assertion that would have failed
});
```

## SLA

- [ ] Test added by: YYYY-MM-DD
- [ ] Verified test catches the original bug
- [ ] Risk policy updated (if applicable)
```

## Connecting to Review Context

If you use the [code-review plugin](../plugins/code-review/README.md) or `/local-review`, past incidents should inform review focus:

1. **Maintain a `review-context.md`** in your project listing known fragile areas
2. **After each incident**, add the affected code area to review context
3. **Reviewers** (human or AI) check review context before starting

Example `review-context.md` entry:

```markdown
## Known Fragile Areas

### Auth token refresh (src/auth/refresh.ts)
- **Incident**: 2026-01-15 — stale token not cleared on 401, caused infinite retry loop
- **Watch for**: Any changes to error handling in auth flows
- **Test**: tests/auth/refresh-on-401.test.ts
```

## Workflow Integration

The incident memory pattern fits into the broader CI lifecycle:

```
Bug in production
  │
  ▼
Post-mortem (this template)
  │
  ├── Harness-gap issue filed
  │     │
  │     ▼
  │   Test written + merged
  │
  ├── Risk policy updated (if tier was wrong)
  │
  └── Review context updated (for local reviews)
```

Over time, your risk policy and QA checklists become **battle-tested** — shaped by real production incidents rather than theoretical risk assessments.

## See Also

- [RISK-GATING.md](./RISK-GATING.md) — Risk-based CI gating guide
- [DECISION_FRAMEWORK.md](./DECISION_FRAMEWORK.md) — Choose the right CI template
- [qa-persona.md.template](./qa-persona.md.template) — QA persona instructions
- [Code Review Plugin](../plugins/code-review/README.md) — Local review before PR
