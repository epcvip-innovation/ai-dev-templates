# Code Review Methodology

The philosophy behind multi-agent adversarial code review.

## Why Multi-Agent?

A single reviewer—human or AI—has blind spots. They focus on what they know. Multi-agent review uses **adversarial personas** that each attack the code from a different angle.

### The Problem with Single-Pass Review

```
Single Reviewer → Catches issues they're looking for
                → Misses issues outside their focus
                → Confirmation bias toward "looks fine"
```

### Multi-Agent Advantage

```
5 Adversarial Agents → Each assumes the code is broken
                     → Different focus areas catch different issues
                     → Overlap provides confidence scoring
                     → No single blind spot dominates
```

## The Five Agents

Each agent is a **paranoid expert** in their domain. They assume the code will fail and look for proof.

### 1. Security Auditor
**Mindset**: "Attackers will find every weakness."

Reviews for:
- Input validation gaps
- Injection vectors (SQL, XSS, command)
- Auth/authz bypass risks
- Secrets exposure
- Insecure defaults

### 2. Bug Hunter
**Mindset**: "This code will cause a 2am incident."

Reviews for:
- Null/undefined handling
- Edge cases and boundary conditions
- Race conditions and async issues
- Error handling gaps
- Type confusion

### 3. Architecture Critic
**Mindset**: "Will I understand this in 6 months?"

Reviews for:
- Code duplication
- Tight coupling
- Wrong abstractions
- Inconsistent patterns
- Complexity hotspots

### 4. Test Skeptic
**Mindset**: "These tests are lying to you."

Reviews for:
- Coverage gaps
- Weak assertions
- Mock abuse (testing mocks, not behavior)
- Missing edge case tests
- Flaky patterns

### 5. Production Pessimist
**Mindset**: "This will break under real traffic."

Reviews for:
- Scale issues (O(n²), N+1 queries)
- Resource leaks
- Failure mode handling
- Data integrity risks
- Missing observability

## Severity Scoring

Each agent scores findings 0-100 based on impact and exploitability:

| Scenario | Score |
|----------|-------|
| Proven exploitable vulnerability | 95-100 |
| Data loss or corruption possible | 85-95 |
| Authentication bypass | 90-100 |
| Crash in production likely | 80-90 |
| Security best practice violation | 65-80 |
| Bug under specific conditions | 60-75 |
| Code smell, works but fragile | 45-60 |
| Style/preference issue | 20-40 |
| Nitpick | 0-20 |

### Why Scoring Matters

Without scoring, all issues look equal. Developers waste time on nitpicks while missing critical bugs. Scoring forces prioritization:

- **80+**: Stop. Fix this before continuing.
- **60-79**: Real risk. Should fix before merge.
- **40-59**: Consider fixing. Use judgment.
- **0-39**: Ignore unless security-critical codebase.

## The Rule of Five

Diminishing returns apply to code review:

```
Pass 1: Catches ~60% of real issues
Pass 2: Catches ~25% more (85% cumulative)
Pass 3: Catches ~10% more (95% cumulative)
Pass 4+: Mostly pedantic findings
```

**Recommendation**: Do 2-3 passes max. After that, you're optimizing for perfection, not safety.

## When to Use Lite vs Full

### Use Full (5 agents) when:
- Major feature releases
- Security-sensitive changes
- Infrastructure/architectural changes
- Code you're not confident about
- Before important deploys

### Use Lite (3 agents) when:
- Daily development work
- Bug fixes and small changes
- Code you're confident about
- Token budget is limited
- Quick pre-commit sanity check

## Merging Results

When multiple agents flag the same issue:
1. **Higher confidence** - Multiple perspectives validate the concern
2. **Keep highest score** - Worst-case severity wins
3. **Merge context** - Combine insights from each agent

Example:
```
Security Auditor: "Input not sanitized" (Score: 85)
Bug Hunter: "Could crash on malformed input" (Score: 70)
→ Merged: Score 85, combined description
```

## Customization

The methodology is adaptable:

1. **Add agents** for your domain (e.g., "Accessibility Auditor")
2. **Adjust scoring** for your risk tolerance
3. **Add patterns** specific to your tech stack
4. **Remove agents** if not relevant (e.g., no frontend = no XSS focus)

See [references/technology-patterns.md](./references/technology-patterns.md) for language-specific patterns.
