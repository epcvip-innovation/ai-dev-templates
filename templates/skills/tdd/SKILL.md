---
name: tdd
description: |
  Enforce test-driven development with RED-GREEN-REFACTOR cycle. Use when
  implementing features, fixing bugs, or adding behavior. Triggers on "/tdd",
  "implement with tests", "add feature with TDD", "test-driven".
  Do NOT use for prototypes, config changes, or generated code.
---

# Test-Driven Development

Enforce test-first discipline: no production code without a failing test first.

## When to Use

**Always use TDD for:**
- New features and behavior
- Bug fixes (reproduce the bug as a failing test first)
- Refactoring that changes behavior
- Adding edge case handling

**Exceptions (ask your human partner first):**
- Throwaway prototypes and spikes (will be deleted)
- Configuration files (no testable behavior)
- Generated code (codegen tools own correctness)
- Glue code with no logic (pure wiring)

If you're unsure, default to TDD. The cost of an unnecessary test is low. The cost of untested production code is high.

## Guardrails

**NEVER:**
- Write production code before a failing test exists
- Keep production code that was written before its test — delete it and start over
- Skip running tests after writing them ("I'm sure it fails")
- Write tests that pass immediately — you haven't tested anything
- Mock behavior you could test with real code
- Rationalize skipping TDD ("too simple", "I'll add tests later", "I already tested manually")
- Add multiple behaviors in one RED-GREEN cycle — one test, one behavior

**ALWAYS:**
- Run the test and watch it fail (RED) before writing production code
- Run the test and watch it pass (GREEN) before moving on
- Write the minimal code to pass — no more
- Keep tests green during REFACTOR — run after every change
- Ask your human partner before skipping TDD for any reason

---

## The Iron Law

> **No production code exists without a failing test that demanded it.**

If you catch yourself writing production code first:
1. **Stop immediately**
2. **Delete the production code** (yes, delete it)
3. **Write the test first**
4. **Watch it fail**
5. **Then rewrite the production code**

This is not punitive. Tests written after code are fundamentally weaker — they verify what code *does*, not what it *should do*. The order matters.

---

## Step 1: RED — Write One Failing Test

Write a single test for the next behavior you need. One test. One behavior.

**Good test:**
```python
def test_login_rejects_empty_password():
    result = authenticate("alice", "")
    assert result.success is False
    assert result.error == "password required"
```

**Bad test:**
```python
def test_login():
    # Tests multiple behaviors — split these up
    assert authenticate("alice", "secret").success is True
    assert authenticate("alice", "").success is False
    assert authenticate("", "secret").success is False
```

A good test:
- Tests **one behavior** (split if the name has "and")
- Has a **clear name** describing the expected behavior
- Shows **intent** — demonstrates the API you want, not the implementation you have
- Uses **real code**, not mocks (unless external dependencies force it)

## Step 2: Verify RED — Run the Test

**This step is mandatory. Do not skip it.**

Run the test suite and confirm:
- [ ] The new test **fails**
- [ ] It fails for the **expected reason** (missing function, wrong return value — not a syntax error or import failure)
- [ ] All other tests still **pass**

If the test passes immediately, you're testing existing behavior. Fix or replace the test.

If it fails for the wrong reason (typo, import error), fix the test first. The test itself must be correct before you write production code.

## Step 3: GREEN — Write Minimal Code

Write the **simplest code** that makes the failing test pass. Nothing more.

**Good — minimal implementation:**
```python
def authenticate(username, password):
    if not password:
        return AuthResult(success=False, error="password required")
    return AuthResult(success=True, error=None)
```

**Bad — over-engineering during GREEN:**
```python
def authenticate(username, password):
    # Don't add validation framework, logging, rate limiting,
    # or password hashing during GREEN. Those are future tests.
    validator = InputValidator(rules=VALIDATION_RULES)
    validator.add_rule("password", RequiredRule())
    validator.add_rule("password", MinLengthRule(8))
    ...
```

During GREEN:
- Solve only what the failing test demands
- Don't add features the test doesn't require
- Don't refactor yet — that's the next step
- Hardcoding is acceptable if only one test demands the value

## Step 4: Verify GREEN — All Tests Pass

**This step is mandatory. Do not skip it.**

Run the full test suite and confirm:
- [ ] The new test **passes**
- [ ] All existing tests still **pass**
- [ ] Output is clean — no warnings, no errors, no deprecation notices

If any test fails, fix it before proceeding. Never continue with a broken suite.

## Step 5: REFACTOR — Clean Up While Green

Now — and only now — clean up:
- Remove duplication
- Improve names
- Extract helpers or constants
- Simplify conditionals

Rules during REFACTOR:
- **Run tests after every change** — stay green
- **Don't add behavior** — refactoring changes structure, not functionality
- **Stop if tests go red** — undo the last change and try a smaller refactoring

## Step 6: Repeat

Go back to Step 1 with the next behavior. Each cycle should be small — minutes, not hours.

---

## Why Order Matters

### "I'll write tests after the code"

Tests written after code verify what code *does*, not what it *should do*. They pass immediately, proving nothing. They mirror implementation details instead of specifying behavior. They miss edge cases because you're anchored to what you already wrote.

### "I tested it manually"

Manual testing has no record, no re-run capability, and no coverage guarantee. Under pressure, you'll forget cases. When the code changes next month, manual tests don't re-run themselves.

### "Deleting my working code is wasteful"

Sunk cost fallacy. The time is already spent. Your choice now is: rewrite with TDD (high confidence, tests as documentation) or keep untested code (unknown correctness, technical debt). Code without tests is a liability, not an asset.

### "TDD is too slow / too dogmatic"

TDD is faster than debugging. The "slowness" of writing a test first is repaid many times over by: catching bugs at write time instead of in production, enabling safe refactoring, and providing documentation of intended behavior. This isn't dogma — it's pragmatism.

---

## Common Rationalizations

When you're tempted to skip TDD, check this table. Every rationalization has been heard before.

| Rationalization | Reality |
|-----------------|---------|
| "Too simple to need a test" | Simple code breaks too. The test takes 30 seconds. Write it. |
| "I'll add tests after" | Tests that pass immediately prove nothing. They verify what code *does*, not what it *should do*. |
| "Tests after achieve the same goals" | Tests-after answer "what does this code do?" Tests-first answer "what *should* this code do?" Fundamentally different. |
| "I already tested it manually" | No record, no re-run, no coverage guarantee. You'll forget cases under pressure. |
| "Deleting X hours of work is wasteful" | Sunk cost fallacy. Untested code is technical debt, not an asset. |
| "Let me keep the code as reference" | You'll adapt instead of rewriting. That's tests-after with extra steps. |
| "I need to explore the design first" | Good — explore, then discard the spike and restart with TDD. Exploration code is not production code. |
| "This is hard to test — bad design signal" | Correct. Hard-to-test means hard-to-use. Simplify the interface. |
| "TDD will slow me down" | TDD is faster than debugging. Time "saved" skipping tests is spent 10x on debugging later. |
| "Manual testing is faster for this" | Manual testing can't prove edge cases and doesn't re-run when code changes. |
| "The existing code has no tests" | That's a reason to start adding them, not a reason to continue without them. |
| "This is just a small change" | Small changes cause production outages too. The test takes 30 seconds. |

---

## Red Flags — STOP and Start Over

If any of these occur, **delete the production code and restart with TDD**:

- You wrote production code before writing a test
- You added tests to already-written code
- A new test passes immediately without code changes
- You can't explain why a test fails (the test is wrong)
- You've been writing code for several minutes without running a test
- You're rationalizing why this case is an exception
- You're relying on "I tested it manually" as justification
- You're claiming tests-after serve the same purpose as tests-first
- You're keeping code "as reference" while writing tests for it
- You're treating sunk cost as justification for keeping untested code

These aren't arbitrary rules. Each one indicates the test-first feedback loop is broken, which means your tests aren't verifying what they should.

---

## Bug Fix Example

A user reports: "Login accepts empty email addresses."

### RED — Reproduce the bug as a failing test

```python
def test_login_rejects_empty_email():
    result = authenticate(email="", password="valid123")
    assert result.success is False
    assert result.error == "email required"
```

Run the test. It fails: `AssertionError: True is not False` — the function currently accepts empty emails. Good — this proves the bug exists.

### GREEN — Write minimal fix

```python
def authenticate(email, password):
    if not email:
        return AuthResult(success=False, error="email required")
    # ... existing logic
```

Run the test. It passes. All other tests still pass.

### REFACTOR — Clean up if needed

```python
def authenticate(email, password):
    if not email:
        return AuthResult(success=False, error="email required")
    if not password:
        return AuthResult(success=False, error="password required")
    # ... existing logic
```

Extract validation if there are multiple fields. Run tests — still green. Done.

---

## Verification Checklist

Before marking TDD work complete, confirm:

- [ ] Every new function/method has at least one test
- [ ] Every test was watched failing (RED) before production code was written
- [ ] Every failure was for the expected reason (missing feature, not a typo)
- [ ] Minimal code was written to pass each test (no speculative features)
- [ ] All tests pass (GREEN)
- [ ] Test output is clean — no warnings, no errors, no deprecation notices
- [ ] Tests use real code, not mocks (unless external dependencies require it)
- [ ] Edge cases and error conditions are covered

---

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test something | Write the API you *wish* existed. Write assertions for it. Then make it real. |
| Test is too complicated | The interface is too complex. Simplify the design, not the test. |
| Everything needs mocking | Code is too tightly coupled. Introduce dependency injection or extract pure functions. |
| Test setup is enormous | Extract test helpers. If still complex, the production design needs simplifying. |
| Test is flaky | Remove time-dependence, randomness, or shared state. Tests must be deterministic. |

---

## Integration

This skill complements (not replaces) existing tools:

| Tool | Role | How TDD relates |
|------|------|-----------------|
| **`feature-dev` Phase 5** | Implementation workflow | TDD provides the test-first discipline within Phase 5 |
| **`pr-test-analyzer`** | Reviews test quality after the fact | TDD ensures tests exist and were written first; analyzer checks they're thorough |
| **`/local-review` Test Skeptic** | Flags coverage gaps in review | TDD prevents gaps from forming; Test Skeptic catches what slips through |
| **Worktrees** | Isolated development branches | Use `/tdd` inside a worktree for safe experimentation with full test discipline |

**Intended flow**: TDD (tests exist, written first) → `pr-test-analyzer` (tests are thorough) → `/local-review` (code is correct)

---

## Troubleshooting

**Problem**: Test framework not set up in this project
**Cause**: New project without test infrastructure
**Solution**: Ask your human partner which framework to use. Set it up before starting TDD.

**Problem**: Existing codebase has no tests
**Cause**: Legacy code without test coverage
**Solution**: Don't try to backfill everything. Apply TDD to new changes and bug fixes. Coverage grows over time.

**Problem**: Tests are slow, breaking the RED-GREEN-REFACTOR rhythm
**Cause**: Tests hitting real databases, networks, or heavy setup
**Solution**: Isolate slow tests. Run fast unit tests during TDD cycles; run integration tests before pushing.

---

**Source**: Adapted from [Superpowers](https://github.com/obra/superpowers)
by Jesse Vincent (@obra). Internalized and restructured for ai-dev-templates conventions.
