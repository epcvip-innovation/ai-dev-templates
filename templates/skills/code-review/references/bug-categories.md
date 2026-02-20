# Bug Categories

Framework for categorizing bugs by root cause, determining whether a tactical fix is sufficient, and identifying when strategic improvements are warranted.

---

## Bug Categorization

| Category | Examples | Typical Root Cause |
|----------|----------|--------------------|
| **State sync** | Component A updated, component B wasn't | No single source of truth |
| **Missing validation** | Input assumed valid, edge case broke it | Implicit trust of data |
| **Tight coupling** | Change in X required change in Y | Related concerns scattered across files |
| **Race condition** | Timing-dependent failure | Shared state across async boundaries |
| **Resource lifecycle** | Cleanup missing, leak, or double-free | No ownership model for resources |
| **Protocol mismatch** | Client/server disagreed on message format | Implicit contract between systems |

---

## Root Cause Heuristics

### "Why was this easy to introduce?"

- Was there no single source of truth?
- Were related concerns scattered across files?
- Was the failure silent (no error, just wrong behavior)?
- Did the fix require knowing about code in multiple places?

### "Would a new developer make the same mistake?"

If yes, the code structure itself is the problem, not just this instance. Consider strategic fixes.

If no, the tactical fix is sufficient — it was an isolated oversight.

---

## Forward-Looking Questions

Use sparingly — only when the bug category suggests broader implications:

- **Portability**: If this app moves to another platform, does this fix rely on platform-specific behavior?
- **Scale**: If usage 10x'd, would this approach still work?
- **Testability**: Can this bug be caught by automated tests now?

---

## Output Templates

### For Simple Bugs

Most bugs are simple. Don't over-analyze.

```markdown
**Fix**: [The change]

**Root cause**: [One sentence — why it happened]

**No strategic changes needed** — this was a straightforward oversight.
```

### For Complex or Recurring Bugs

```markdown
## Tactical Fix (implement now)
[The minimal change that fixes this specific bug]

## Root Cause Analysis
**Bug category**: [From table above]
**Pattern**: [Is this a one-off or part of a theme?]
**Why it was easy to introduce**: [What made this mistake possible?]

## Strategic Consideration
**If this recurs**: [What structural change would help — describe the improvement, not a pattern name]
**Recommendation**: Implement now / Add to backlog / Just monitor
```

---

## Don't Over-Engineer

### Signs the Tactical Fix IS the Answer

- First time this type of bug appeared in this area
- The fix is obvious once you see it
- Adding abstraction would cost more than occasional bugs
- The code is rarely touched

### Traps to Avoid

- Don't recommend refactoring for every bug
- Don't use pattern names without explaining the actual benefit
- Don't imply platform portability matters for every fix
- Don't suggest state machines, dependency injection, or other heavyweight solutions unless the pain justifies it
- Don't assume a bug reveals an architecture problem — most bugs are just bugs
