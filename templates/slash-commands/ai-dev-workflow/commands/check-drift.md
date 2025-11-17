---
description: Detect drift between plan and reality using AI-friendly boolean checks
allowed-tools: read_file, grep, search_replace, list_dir
---

## Command

Compare original plan against actual development progress to detect drift and recommend adjustments.

**When to use:**
- After completing each phase of a feature
- Before running `/session-handoff` (usually automatic)
- When approaching context limit (70-80%)
- When feature "feels off track"
- After adding multiple unplanned tasks

**When NOT to use:**
- First session of feature (nothing to compare against)
- Trivial tasks (<1 hour total)
- When plan was just created (no drift possible yet)

## Step 1: Load Plan and Current State

**Read in order:**
1. **Original plan** (`docs/planning/features/[name]/plan.md`)
2. **Handoff document** (`HANDOFF.md` if exists)
3. **Git log** (recent commits as fallback)
4. **Task tracking** (current task list or sprint file)

**Extract:**
- Original goal statement
- Original effort estimate
- Original task list
- Original approach description

**Current state:**
- Completed tasks
- Added tasks (not in original plan)
- Removed/deferred tasks
- Current approach
- Blockers discovered

---

## Step 2: Run Boolean Checklist

**Five key checks (boolean logic, no percentages):**

### Check 1: Goal Unchanged?

**Compare:**
- Original goal (from plan.md header or "Goal" section)
- Current goal (from HANDOFF.md or task list)

**Assessment:**
- ✅ **YES** - Goals match or only clarified (wording refined but same intent)
- ❌ **NO** - Goal changed (different outcome, different scope, different user)

---

### Check 2: Approach Unchanged or Refined?

**Compare:**
- Original approach (from "Technical Approach" section)
- Implemented approach (from HANDOFF, code, or commits)

**Assessment:**
- ✅ **SAME** - Same architecture, same libraries, same patterns
- ⚠️ **MINOR** - Minor tweaks (different library version, small refactor, pattern refinement)
- 🚫 **MAJOR** - Complete redesign (embedded → microservices, SQL → NoSQL, sync → async)

---

### Check 3: Task Drift ≤2?

**Calculate:**
```
planned_tasks = count(tasks in original plan.md)
completed_tasks = count(tasks marked done)
added_tasks = count(tasks NOT in original plan)
removed_tasks = count(planned tasks NOT completed and NOT in progress)

task_drift = added_tasks - removed_tasks
```

**Assessment:**
- ✅ **≤2** - Healthy evolution (1-2 edge cases discovered)
- ⚠️ **3-5** - Moderate drift (some unplanned work)
- 🚫 **>5** - Major drift (significant scope change)

---

### Check 4: No New Blockers?

**Check for:**
- Technical blockers mentioned in HANDOFF.md
- Dependency issues
- Infrastructure problems
- Discovered impossibilities

**Assessment:**
- ✅ **NO BLOCKERS** - All planned dependencies available, no issues
- ⚠️ **WORKAROUND EXISTS** - Blocker found but resolved with alternative approach
- 🚫 **FUNDAMENTAL BLOCKER** - Cannot proceed without major change

---

### Check 5: Time Drift <2x Estimate?

**Ask user:**
```
📊 Time Check

Original estimate: [X] hours
Work so far: [Ask user how many hours]

Did this take more than 2x the estimate?
- NO (≤2x): Proceed with checks
- YES (>2x): Major drift flagged
```

**Assessment:**
- ✅ **<2x** - Estimate was reasonable
- ⚠️ **1.5-2x** - Estimate low but explainable
- 🚫 **>2x** - Estimate way off OR scope changed significantly

---

## Step 3: Categorize Drift

### ✅ Healthy Evolution (All Checks Pass)

**Criteria:**
- Goal unchanged (✅)
- Approach same or minor refinement (✅ or ⚠️ minor)
- Task drift ≤2 (✅)
- No fundamental blockers (✅ or ⚠️ workaround)
- Time ≤2x estimate (✅)

**Action:**
- Document discoveries in HANDOFF.md
- Update plan.md with minor notes
- Continue implementation

```
✅ HEALTHY EVOLUTION

No significant drift detected:
- Goal: Unchanged
- Approach: Minor refinement (embedded → separate service)
- Tasks: +1 (edge case handling)
- Blockers: None
- Time: On track (~100% of estimate)

Action: Continue with current plan
```

---

### ⚠️ Moderate Drift (1-2 Checks Fail)

**Criteria:**
- Goal unchanged BUT
- 1-2 of these fail:
  - Approach has minor changes
  - Task drift 3-5
  - Workaround for blocker needed
  - Time 1.5-2x estimate

**Action:**
- Update plan.md with revised estimates
- Document why drift occurred
- Adjust remaining task estimates
- Continue (no replan needed)

```
⚠️ MODERATE DRIFT

Drift detected in 2 areas:
- Goal: ✅ Unchanged
- Approach: ⚠️ Architecture modified (embedded → separate)
- Tasks: ⚠️ +4 tasks (API endpoints, error handling)
- Blockers: ✅ None
- Time: ✅ On track

Reasons for drift:
1. API requirement discovered (not in original plan)
2. Error handling needed for production readiness

Action Required:
- Update plan.md: 6h → 8h (+2h for API work)
- Document architecture change rationale
- Continue with adjusted plan

Proceed with plan update? [Y/n]
```

---

### 🚫 Major Drift (Red Flag Present)

**Criteria (any ONE of these):**
- Goal changed from original
- Major approach overhaul
- Task drift >5
- Fundamental blocker exists
- Time >2x estimate

**Action:**
- Stop implementation
- Run `/replan-feature` (if command exists)
- User approval required before continuing

```
🚫 MAJOR DRIFT DETECTED

Critical issues found:
- Goal: 🚫 CHANGED (OAuth → OAuth + Audit Logging + Dashboard)
- Approach: ✅ Same
- Tasks: 🚫 +8 tasks (original 8 → current 16)
- Blockers: ✅ None
- Time: 🚫 >2x estimate (6h planned, 14h actual)

This is major scope expansion, not evolution.

Recommended Actions:
1. Stop current feature
2. Split into 2-3 separate features:
   - Feature A: OAuth (original scope) - 8h ✅ COMPLETE
   - Feature B: Audit Logging - 6h (defer)
   - Feature C: Dashboard - 4h (defer)
3. Ship Feature A now
4. Plan B & C separately

Run /replan-feature or /split-feature?
```

---

## Step 4: Generate Drift Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 DRIFT DETECTION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: [Name]
Plan: docs/planning/features/[name]/plan.md
Date: [Current date]

---

🔍 BOOLEAN CHECKLIST RESULTS:

1. Goal unchanged?
   ├─ Original: "[Quote from plan]"
   ├─ Current: "[Quote from handoff/reality]"
   └─ Assessment: [✅ YES / ❌ NO]

2. Approach unchanged or refined?
   ├─ Original: "[Quote approach]"
   ├─ Current: "[Quote implemented]"
   └─ Assessment: [✅ SAME / ⚠️ MINOR / 🚫 MAJOR]

3. Task drift ≤2?
   ├─ Planned tasks: [N]
   ├─ Added tasks: [N] ([list names])
   ├─ Removed tasks: [N] ([list names])
   ├─ Net drift: [+/-N]
   └─ Assessment: [✅ ≤2 / ⚠️ 3-5 / 🚫 >5]

4. No new blockers?
   ├─ Blockers found: [List or "None"]
   ├─ Workarounds: [List or "N/A"]
   └─ Assessment: [✅ NONE / ⚠️ WORKAROUND / 🚫 FUNDAMENTAL]

5. Time <2x estimate?
   ├─ Original estimate: [X]h
   ├─ Actual time so far: [Y]h
   ├─ Ratio: [Y/X = Z]x
   └─ Assessment: [✅ <2x / ⚠️ 1.5-2x / 🚫 >2x]

---

🎯 OVERALL ASSESSMENT: [✅ HEALTHY / ⚠️ MODERATE / 🚫 MAJOR]

[Detailed explanation of assessment]

---

📝 RECOMMENDED ACTIONS:

[Specific actions based on assessment]

1. [Action 1]
2. [Action 2]
3. [Action 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 5: Update Plan (If Approved)

**For Moderate Drift (if user approves):**

### Update Effort Estimate

In `plan.md` header:
```markdown
## Effort Estimation

**Original:** [X] hours (Tier [1/2])
**Revised:** [Y] hours (Tier [1/2]) - Updated [date]

**Revision reason:** [Why estimate changed]
- [Reason 1: e.g., API requirement discovered]
- [Reason 2: e.g., Additional error handling needed]
```

### Add Drift Notes Section

```markdown
## Drift Analysis

### [Date] - Moderate Drift Detected

**Changes from original plan:**
- Tasks added: [N] ([list])
- Tasks deferred: [N] ([list])
- Approach refined: [description]

**Reasons:**
1. [Why drift occurred - discovery, blocker, etc.]
2. [Additional context]

**Impact:**
- Timeline: [X]h → [Y]h (+[Z]%)
- Tier: [1/2] unchanged OR changed [1→2]
- Scope: Core goal unchanged

**Assessment:** Healthy evolution (not scope creep)
```

### Update HANDOFF.md

```markdown
## Plan Drift Assessment ([Date])

**Status:** ⚠️ Moderate drift detected

**Changes:**
- Estimate: [X]h → [Y]h
- Tasks: +[N] added, -[N] removed
- Approach: [SAME / Minor refinement]

**Rationale:** [Why changes are justified]

**Updated plan:** See plan.md (revised [date])
```

---

## Integration with Other Commands

### Auto-triggered by `/session-handoff`

In `/session-handoff` Step 1.5:
- Loads plan and current state
- Runs boolean checklist
- Categorizes drift
- Updates plan if moderate drift

### Referenced by `/validate-plan`

Checks if past drift suggests estimate problems:
- Multiple features with moderate drift → estimates systematically low
- Update TASK_ESTIMATION_GUIDE.md benchmarks

### Feeds into Calibration Log

After feature completes:
- Use drift data to update TASK_ESTIMATION_GUIDE.md
- Track patterns (auth always drifts? caching always faster?)

---

**This command updates:**
- `plan.md` (effort estimates, drift notes)
- `HANDOFF.md` (drift assessment, rationale)
- `TASK_ESTIMATION_GUIDE.md` (calibration data)

