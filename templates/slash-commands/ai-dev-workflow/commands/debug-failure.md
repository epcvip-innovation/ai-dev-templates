---
description: Debug a test failure using a structured, hypothesis-driven process
argument-hint: path/to/failing_test.py
---

## Command

You are assisting in debugging a test failure. Instead of immediately fixing the code, you will follow a "Socratic" process of analysis, hypothesis, and verification to ensure the true root cause is addressed, not just the symptoms.

**This prevents:**
- Hacking tests to pass without understanding why
- Fixing symptoms instead of root causes
- Churning through incorrect solutions

---

## Step 1: Analyze Failure Context

**1.1. Read the Test Failure Output:**
   - The user will provide the full test runner output. Identify the exact assertion that failed and the traceback.

**1.2. Read Relevant Code:**
   - **Read the failing test file completely:** Understand what the test is trying to achieve.
   - **Read the source code file being tested:** Focus on the functions/methods called in the traceback.

---

## Step 2: Formulate Root Cause Hypothesis

**Present this exact format to the user:**

```
### 🧠 Root Cause Hypothesis

**Symptom:**
- The test `[test_name]` fails at `[file:line]` with the error: `[error message]`.

**Potential Root Causes:**

**1. Hypothesis A: [Concise description of hypothesis]**
   - **Reasoning:** [Explain why this could be the cause, citing specific lines of code from the source or test].
   - **Confidence:** [High/Medium/Low]

**2. Hypothesis B: [Concise description of a different hypothesis]**
   - **Reasoning:** [Explain this alternative theory, citing different code or logic].
   - **Confidence:** [High/Medium/Low]

---

### 🔬 Verification Step

To confirm **Hypothesis A**, I propose a small, non-invasive change.

**Action:**
- **File:** `[path/to/source/code.py]`
- **Change:** Add a temporary logging statement at line [X] to inspect the value of `[variable]`.

```python
import logging
logging.basicConfig(level=logging.INFO)
def function_under_test(arg1, arg2):
    logging.info(f"DEBUG: The value of [variable] is {[variable]}")
    return result
```

This will not fix the issue but will prove whether our assumption about `[variable]` is correct.

**Do you approve this verification step? [Y/n]**

**CRITICAL: DO NOT propose a code fix yet. Wait for user approval.**

---

## Step 3: Verify and Propose Fix

**3.1. If user approves:**
   - Apply the logging statement using `edit_file`.
   - Ask the user to re-run the test and provide the output.

**3.2. Analyze verification output:**
   - If the log output confirms the hypothesis, proceed.
   - If it refutes the hypothesis, return to Step 2 and re-evaluate with the new information.

**3.3. Propose the Fix:**
   - Once the hypothesis is confirmed, propose the final code change.

```
### ✅ Hypothesis Confirmed & Proposed Fix

The log output confirmed that `[variable]` was `[unexpected_value]`, as suspected.

**I will now apply the following fix:**

- **File:** `[path/to/source/code.py]`
- **Rationale:** [Briefly explain *why* this fix works, tying it back to the confirmed root cause].

```python
# I will make the following change to correct the logic
```

**I will also remove the temporary logging statement.**

**Apply this fix? [Y/n]**

---

## Step 4: Confirm Resolution

**4.1. If user approves the fix:**
   - Use `edit_file` to apply the fix and remove the temporary logging code.

**4.2. Final Verification:**
   - Ask the user to run the tests one last time.
   - Confirm that the original test now passes and that no new tests have failed (no regressions).

**4.3. Complete:**
```
✅ **FIX CONFIRMED**

- The test `[test_name]` is now passing.
- No regressions were detected.
- The root cause was [briefly summarize].

Debugging complete.
```

---

## Workflow Principles

- **Analyze First:** Never jump to conclusions.
- **Hypothesize transparently:** Show your reasoning.
- **Verify Safely:** Use logging or other non-invasive means before changing logic.
- **Fix with Confidence:** Only propose a solution after the root cause is understood.
- **Keep the User in Control:** Every major step requires user approval.

