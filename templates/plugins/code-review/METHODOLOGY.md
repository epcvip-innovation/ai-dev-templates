# Code Review Methodology

The philosophy behind multi-agent adversarial code review with built-in evaluation.

## Why Multi-Agent?

A single reviewer — human or AI — has blind spots. They focus on what they know. Multi-agent review uses **adversarial personas** that each attack the code from a different angle.

### Single-Pass vs Multi-Agent

```
Single Reviewer → Catches issues they're looking for
                → Misses issues outside their focus
                → Confirmation bias toward "looks fine"

5 Adversarial Agents → Each assumes the code is broken
                     → Different focus areas catch different issues
                     → Overlap provides confidence scoring
                     → No single blind spot dominates
```

## The Five Agents

Each agent is a **paranoid expert** in their domain. They assume the code will fail and look for proof.

| Agent | Mindset | Focus |
|-------|---------|-------|
| Security Auditor | "Attackers will find every weakness" | Input validation, injection, auth, secrets |
| Bug Hunter | "This will cause a 2am incident" | Null handling, edge cases, async, errors |
| Architecture Critic | "Will I understand this in 6 months?" | Duplication, coupling, abstractions, complexity |
| Test Skeptic | "These tests are lying to you" | Coverage, assertions, mock abuse, flaky patterns |
| Production Pessimist | "This will break under real traffic" | Scale, resource leaks, failure modes, observability |

## Self-Evaluation Protocol

Every agent follows the same pre-reporting checklist:

1. **Read the source file** — not just the diff
2. **Trace the execution path** — how is this called? What are the inputs?
3. **Self-evaluate confidence** — 0-100 score for certainty
4. **Check false-positive patterns** — is this a known false positive?
5. **Only report if confidence >= 70**

This reduces noise before findings even reach the evaluation phase.

## Built-In Evaluation Phase

**The key innovation.** Previous approaches required running evaluation as a separate step. The unified pipeline includes evaluation as Phase 3:

### 3-Question Framework

For each finding:
1. **Is the bug real?** Trace the actual call flow.
2. **Is the solution sustainable?** Will the fix create more complexity than the bug?
3. **Is there a better alternative?** Guard, fail-fast, or monitor-first?

### Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| REAL BUG | Confirmed via call flow tracing | Fix or backlog |
| MARGINAL | Theoretically possible, unlikely in practice | Note + low priority |
| FALSE POSITIVE | Not real given actual usage | Remove |
| LOW PRIORITY | Real but not worth fixing now | Monitor |

### Impact

In testing, the evaluation phase filters **60-90% of findings** from the agent phase. What remains is high-signal, actionable.

## Root-Cause Integration

For surviving bugs (REAL BUG or MARGINAL), the pipeline categorizes root causes:

| Category | Question |
|----------|----------|
| State sync | No single source of truth? |
| Missing validation | Implicit trust of data? |
| Tight coupling | Change in X requires change in Y? |
| Race condition | Shared state across async? |
| Resource lifecycle | No ownership model? |
| Protocol mismatch | Implicit contract between systems? |

Simple bugs get one-line root causes. Complex/recurring bugs get strategic analysis.

## Severity Scoring

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

**Default threshold: 60+.** Below that is noise for most projects.

## When to Use Quick vs Full

| Use Full (default) when | Use Quick (`--quick`) when |
|-------------------------|---------------------------|
| Major feature releases | Daily development work |
| Security-sensitive changes | Bug fixes and small changes |
| Infrastructure changes | Quick pre-commit sanity check |
| Before important deploys | Token budget is limited |
| Code you're not confident about | Code you're confident about |

## The Rule of Five

Diminishing returns apply:

```
Pass 1: Catches ~60% of real issues
Pass 2: Catches ~25% more (85% cumulative)
Pass 3: Catches ~10% more (95% cumulative)
Pass 4+: Mostly pedantic findings
```

**Recommendation**: 2-3 passes max. After that, you're optimizing for perfection, not safety.

## Customization

1. **Add agents** for your domain (e.g., "Accessibility Auditor")
2. **Adjust scoring** for your risk tolerance
3. **Add technology patterns** for your stack
4. **Create review-context.md** for project-specific exceptions

See [references/technology-patterns.md](./references/technology-patterns.md) for language-specific patterns.
