# False Positive Patterns

Common false positives in code review and how to identify them. Apply these patterns during the evaluation phase to filter out findings that are not real issues.

---

## 3-Question Evaluation Framework

For each finding, answer these three questions:

### 1. Is the bug real?

**Trace the actual call flow:**
- When/how is this code path triggered?
- What are the real-world conditions that cause the issue?
- Is this theoretical or does it happen in practice?

**Quantify attack surfaces:**
- How many combinations to brute force?
- What's the realistic attack time?
- What does the attacker gain?

### 2. Is the solution sustainable?

**Complexity check:**
- Does it add new state to manage?
- Does it require cleanup logic?
- Will it create more bugs than it fixes?

**Match to use case:**
- Is the solution designed for the actual usage pattern?
- Is it over-engineered for an edge case?

### 3. Is there a better alternative?

**Simpler fixes:**
- Can we add a guard instead of a refactor?
- Can we fail fast instead of handling every case?
- Can we monitor first, fix later?

**Higher-level solutions:**
- Is this a symptom of a design issue?
- Would a different architecture eliminate the problem class?

---

## Verdict Categories

| Verdict | Meaning | Action |
|---------|---------|--------|
| **REAL BUG** | Confirmed issue with traced call flow | Fix now or add to backlog |
| **MARGINAL** | Theoretically possible but unlikely in practice | Add guard or monitor |
| **FALSE POSITIVE** | Not a real issue given the actual usage | Skip |
| **LOW PRIORITY** | Real but low impact, not worth fixing now | Backlog as P3 or monitor |

---

## Common False Positives by Category

### JavaScript/TypeScript

| Pattern | Why It's False | What to Check Instead |
|---------|---------------|----------------------|
| "Race condition" in synchronous code | JS is single-threaded; `clear(x); set(x);` is NOT a race condition | Only flag async issues: missing `await`, shared state across `await`, `Promise.all` order |
| "TOCTOU" without `await` between check and act | Synchronous check-then-act is safe in JS event loop | Only flag when there's an `await` or callback between check and use |
| Timer clear/set sequences | `clearInterval(x); x = setInterval(...)` is atomic in event loop | Only flag if timer callback modifies shared state across await boundaries |

### Security

| Pattern | Why It's False | What to Check Instead |
|---------|---------------|----------------------|
| Rate limiting for impractical attacks | Billions of combinations = years to brute force | Calculate actual attack feasibility before flagging |
| Information disclosure that doesn't enable action | Knowing a room exists doesn't grant access | Flag only if leaked info enables escalation |
| Auth bypass requiring existing credentials | "If attacker has the token they can..." — that's how auth works | Flag only if auth can be circumvented without valid credentials |

### Architecture

| Pattern | Why It's False | What to Check Instead |
|---------|---------------|----------------------|
| "Missing abstraction" for one-time code | Not everything needs an abstraction layer | Flag only if the pattern repeats 3+ times |
| "Code duplication" for 2-3 similar lines | Premature abstraction costs more than minor repetition | Flag only if duplicated logic is complex or likely to diverge |
| "Tight coupling" in application-specific code | Internal app modules are allowed to know about each other | Flag only if coupling crosses architectural boundaries (e.g., UI → DB) |

---

## Evaluation Output Format

For each finding, produce:

```markdown
### [Finding Title] (Original Score: N)

**Is it real?**
[Trace call flow, identify when it actually triggers]

**Verdict:** REAL BUG | MARGINAL | FALSE POSITIVE | LOW PRIORITY

**Revised Score:** [adjusted score or "Skip"]

**If REAL BUG or MARGINAL:**
- Original fix: [describe]
- Issue with original: [if any]
- Better alternative: [if any]
```

---

## Example Evaluation

**Original Finding:**
> Race condition: `pendingResolver` singleton can be overwritten by concurrent calls (Score 85)

**Evaluation:**
- Traced call flow: `handleConnected()` → `attemptRejoin()` → `checkRoomExists()`
- WebSocket reconnect has 3s delay, timeout is 3s
- Flow is sequential, not concurrent
- **Verdict: MARGINAL** — Theoretically possible but unlikely

**Better Solution:**
```javascript
// Original proposed: Map-based tracking (complex)
// Better: Simple guard (matches actual use case)
if (pendingResolver) {
  return Promise.resolve({ exists: false });
}
```
