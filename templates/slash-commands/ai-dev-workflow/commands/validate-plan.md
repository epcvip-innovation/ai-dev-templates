---
description: Validate plan quality against rubric before implementation
allowed-tools: read_file, grep, codebase_search, search_replace
---

## Command

Run PLAN_QUALITY_RUBRIC.md checklist against feature plan, identify issues, suggest fixes.

**When to use:**
- **Automatic** - Built into `/start-feature` (runs after plan creation)
- **Automatic** - Built into `/resume-feature` (checks plan still valid)
- **Manual** - Mid-implementation when something feels off
- **Manual** - After major plan revision

**When NOT to use:**
- Plan was just validated (don't run twice in a row)
- No plan exists (ad-hoc work)
- Plan is <1 page (trivial task, validation overkill)

## Step 1: Load Rubric and Plan

### 1.1: Load Plan Quality Rubric

**Read rubric:**
- File: `docs/planning/PLAN_QUALITY_RUBRIC.md`
- Sections: Scope Clarity (5), Feasibility (4), Implementability (4), Size (3), Technical (3)

### 1.2: Load Plan Document

**Find plan:**
```bash
# Look for plan (common locations)
PLAN_FILE=$(find docs/planning/features -name "plan.md" 2>/dev/null | head -1)

echo "📋 Validating: $PLAN_FILE"
```

**Read plan completely** to extract:
- Goal/objective statement
- Success criteria
- Out-of-scope section
- Approach description
- Task breakdown
- Effort estimate
- Dependencies

---

## Step 2: Run Checklist (Boolean Evaluation)

For each rubric criterion, evaluate as **PASS** or **FAIL**. Quote evidence from plan.

### 2.1: Scope Clarity (5 checks)

#### Check 1: Goal is Specific and Measurable

**Criteria:**
- Not vague: "Improve X" ❌
- Specific: "Add OAuth restricted to @company.com" ✅

**Assessment:** [PASS / FAIL]

---

#### Check 2: Success Criteria are Testable

**Criteria:**
- Not subjective: "Fast enough" ❌
- Testable: "Query validation <5 seconds" ✅

**Assessment:** [PASS / FAIL]

---

#### Check 3: Out-of-Scope is Explicit

**Criteria:**
- Has "Out of scope" or "Not included" section
- Prevents scope creep

**Assessment:** [PASS / FAIL]

---

#### Check 4: No Vague Language

**Criteria:**
- No: "generally", "improve", "better", "more robust", "optimize"
- Yes: "add", "reduce from X to Y", "implement", "migrate"

**Assessment:** [PASS / FAIL]

---

#### Check 5: Dependencies Identified

**Criteria:**
- Lists required libraries, services, APIs
- Specifies versions or "already available"

**Assessment:** [PASS / FAIL]

---

### 2.2: Feasibility (4 checks)

#### Check 6: Required Resources Exist

**Criteria:**
- API keys, credentials available
- Infrastructure deployed
- Libraries installed or installable

**Assessment:** [PASS / FAIL]

---

#### Check 7: No Unknowns Without Resolution

**Criteria:**
- No "TBD" markers
- No "decide during implementation"
- If approach uncertain, research task exists

**Assessment:** [PASS / FAIL]

---

#### Check 8: Approach is Justified

**Criteria:**
- Has "Why this approach" explanation
- Not just "use X" but "use X because Y"

**Assessment:** [PASS / FAIL]

---

#### Check 9: No Blockers Exist

**Criteria:**
- Infrastructure ready
- Permissions granted
- Prerequisites complete

**Assessment:** [PASS / FAIL]

---

### 2.3: Implementability (4 checks)

#### Check 10: Tasks are Concrete

**Criteria:**
- Not "Implement X"
- Specific: "Create OAuth 2.0 credentials in Google Cloud Console"

**Assessment:** [PASS / FAIL]

---

#### Check 11: Acceptance Criteria Per Task

**Criteria:**
- Each task lists "how you know it's done"
- Observable outcomes

**Assessment:** [PASS / FAIL]

---

#### Check 12: Test Strategy Exists

**Criteria:**
- Has "Testing" section OR
- Tasks include test steps

**Assessment:** [PASS / FAIL]

---

#### Check 13: Files/Components Identified

**Criteria:**
- Lists specific files to modify
- Not "update code" but "modify streamlit_app.py, secrets.toml"

**Assessment:** [PASS / FAIL]

---

### 2.4: Size Appropriateness (3 checks)

#### Check 14: Effort ≤15 Hours

**Criteria:**
- Tier 1 (≤6h): ✅ Single session
- Tier 2 (7-15h): ⚠️ Multi-session, requires checkpoints
- Tier 3 (>15h): 🚫 Must split

**Assessment:** [PASS / FAIL]

---

#### Check 15: Checkpoints Every 6 Hours (Tier 2)

**Criteria:**
- If 7-15h: Must have checkpoints
- Marked clearly in task list

**Assessment:** [PASS / FAIL / N/A]

---

#### Check 16: Shippable Milestones (Multi-Session)

**Criteria:**
- Phases can deploy independently
- Each phase has value on its own

**Assessment:** [PASS / FAIL / N/A]

---

### 2.5: Technical Soundness (3 checks)

#### Check 17: Follows CLAUDE.md Standards

**Criteria:**
- Matches project anti-patterns
- Follows architectural patterns
- **Project-specific examples:**
  - ❌ Missing required filters on large tables
  - ❌ Missing timezone filters
  - ❌ Unvalidated queries before execution
  - ✅ Always validate queries with validation engine first
  - ✅ Use proper aggregation tables (not raw data)

**Assessment:** [PASS / FAIL]

---

#### Check 18: Architectural Decisions Documented

**Criteria:**
- If multiple approaches possible, decision rationale exists
- Trade-offs acknowledged

**Assessment:** [PASS / FAIL]

---

#### Check 19: Technical Debt Acknowledged

**Criteria:**
- If shortcuts taken, documented
- Has payback plan or timeline

**Assessment:** [PASS / FAIL / N/A]

---

## Step 3: Generate Validation Report

**Calculate results:**
- Total checks: 19
- Passed: [N]
- Failed: [M]
- Pass rate: [N/19 × 100]%

**Categorize overall:**
- ✅ **Ready** (All 19 pass) - Proceed immediately
- ⚠️ **Needs Refinement** (17-18 pass, 1-2 fails) - Fix in 10-30 min
- 🚫 **Not Ready** (≤16 pass, 3+ fails) - Major issues, replan

**Report format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PLAN VALIDATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: [Name]
Plan: [File path]
Date: [Current date]

---

📊 OVERALL ASSESSMENT: [✅ READY / ⚠️ REFINE / 🚫 NOT READY]

Results: [N]/19 checks passed ([X]%)

---

✅ PASSED (N checks):

1. Scope Clarity:
   ├─ [1] Goal specific: ✅
   ├─ [2] Success testable: ✅
   ├─ [3] Out-of-scope: ✅
   ├─ [4] Language concrete: ✅
   └─ [5] Dependencies: ✅

2. Feasibility:
   ├─ [6] Resources: ✅
   ├─ [7] No unknowns: ✅
   ├─ [8] Approach justified: ✅
   └─ [9] No blockers: ✅

3. Implementability:
   ├─ [10] Tasks concrete: ✅
   ├─ [11] Acceptance criteria: ✅
   ├─ [12] Testing: ✅
   └─ [13] Files identified: ✅

4. Size:
   ├─ [14] Effort appropriate: ✅
   ├─ [15] Checkpoints (if needed): ✅
   └─ [16] Milestones shippable: ✅

5. Technical:
   ├─ [17] Follows standards: ✅
   ├─ [18] Decisions documented: ✅
   └─ [19] Debt acknowledged: ✅

---

❌ FAILED (M checks):

[If any failures, list each with:]
- [Check #]: [Check name]
  - **Issue:** [What's wrong]
  - **Evidence:** [Quote from plan showing issue]
  - **Fix:** [Specific action to resolve]
  - **Effort:** [Time to fix: 5-30 min]

---

📝 RECOMMENDED ACTIONS:

[If ✅ Ready:]
Proceed with implementation immediately.
All quality checks passed.

[If ⚠️ Needs Refinement:]
Fix [N] issue(s) before proceeding:
1. [Fix for check #X]: [Specific action] (5-10 min)
2. [Fix for check #Y]: [Specific action] (10-20 min)

Total fix time: ~[X] minutes

[If 🚫 Not Ready:]
Major planning issues detected. Do NOT proceed.

Required actions:
1. [Critical fix 1]: [Action] (must address)
2. [Critical fix 2]: [Action] (must address)

Consider:
- Running `/plan-approaches` (if approach unclear)
- Splitting feature (if >15h)
- Deferring to backlog (if not ready)

Time to fix: [X hours] (substantial rework)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 4: Auto-Fix (If User Approves)

**For minor failures (⚠️ Needs Refinement), offer auto-fixes:**

### Example Auto-Fixes

**Missing checkpoints (Check 15 fail):**
```markdown
I can add checkpoint tasks automatically:

### Checkpoint 1: After Phase 1 (~6h)
- [ ] Run `/check-drift`
- [ ] Deploy/test Phase 1
- [ ] Review: Continue or adjust?

Add these? [Y/n]
```

**Missing out-of-scope (Check 3 fail):**
```markdown
I can add out-of-scope section:

## Out of Scope

This feature does NOT include:
- [Inferred exclusions based on goal]

Add this section? [Y/n]
```

---

## Step 5: Update Plan (If Auto-Fixes Applied)

If user approved auto-fixes:

1. **Update plan.md** with fixes
2. **Add validation note:**
   ```markdown
   ## Validation

   **Last validated:** [Date]
   **Result:** ✅ Passed validation (after refinements)
   **Issues fixed:** [List what was added/changed]
   ```

---

## Integration Points

### Called Automatically By:

**`/start-feature` (Step 4.5):**
- After creating plan
- If fails, offer fixes before proceeding

**`/resume-feature` (Step 4.5):**
- After loading context
- Quick validation (is plan still valid?)

**`/session-handoff` (via drift check):**
- If moderate/major drift
- Re-validate to ensure still sound

---

**This command ensures:**
- Plans meet minimum quality standards
- Common pitfalls caught early
- Consistent evaluation (not subjective)
- Clear path to fix issues
- Less drift during implementation

