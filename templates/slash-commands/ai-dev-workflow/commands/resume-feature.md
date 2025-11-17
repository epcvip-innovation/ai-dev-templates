---
description: Resume work on a feature after a break by rebuilding context from planning docs and handoffs
argument-hint: feature-name
allowed-tools: read_file, list_dir, glob_file_search, run_terminal_cmd, todo_write, grep, codebase_search
---

## Command

You are resuming work on this feature after a break. Follow this systematic checklist to rebuild context efficiently and ensure code quality:

## Step 1: Load Project Standards

**Read ONLY:**
- **`CLAUDE.md`** - Project conventions, code quality standards, and anti-patterns

**DO NOT read at this stage:**
- ~~FEATURES_BACKLOG.md~~ (use discovery script in Step 2)
- ~~PLAN_QUALITY_RUBRIC.md~~ (validator script handles this in Step 4.5)
- ~~Any HANDOFF.md files~~ (load after user selects feature in Step 4)
- ~~Any plan.md files~~ (load after user selects feature in Step 4)

**Why minimal?** Saves 40%+ context for actual feature work.

---

## Step 2: Discover Active Features

**Run discovery script:**
```bash
python3 .claude/utils/feature_discovery.py
```

**Expected output:** JSON with feature count and structured details:
```json
{
  "count": 2,
  "active_features": [
    {"name": "session-based-auth", "remaining_hours": 12, "blocked": true, ...},
    {"name": "query-reorganization", "remaining_hours": 3, "blocked": false, ...}
  ]
}
```

**CRITICAL:** This script enforces grep-only discovery. It physically CANNOT read the full FEATURES_BACKLOG.md file.

**Parse the JSON to determine next step** (see Step 3).

---

## Step 3: Smart Feature Selection

**Based on feature count from Step 2:**

### If count = 0
```
No features in progress.

Run /start-feature to begin working on a new feature.
```
**STOP HERE.**

### If count = 1
```
Resuming: [feature-name]
```
**Auto-select this feature, continue to Step 4.**

### If count = 2+
```
You have [N] active features:

1. session-based-auth (12h remaining, ⚠️ BLOCKED - [status_summary])
2. query-reorganization (3h remaining, ✅ READY - [status_summary])

Which feature? [Enter number or name]
```

**CRITICAL:** Wait for user response before continuing to Step 4.

**Only after user selects:** Proceed to load that feature's context.

## Step 4: Load Selected Feature Context

**Run handoff loader for SELECTED feature only:**
```bash
python3 .claude/utils/handoff_loader.py [feature-name]
```

**Expected output:** JSON with feature context:
```json
{
  "feature_name": "session-based-auth",
  "handoff_content": "...",
  "plan_content": "...",
  "files_loaded": [
    "docs/planning/features/session-based-auth/HANDOFF.md",
    "docs/planning/features/session-based-auth/plan.md"
  ],
  "lines_loaded": 911
}
```

**Parse JSON output:**
- Display `files_loaded` for transparency
- Extract `handoff_content` and `plan_content` for context
- Note `lines_loaded` count

**This replaces manual file reading** - script loads only selected feature (not all active features).

If handoff_content is null: That's fine, use plan_content as source of truth.

---

## Step 5: Verify Current State

**Pre-flight Check:** Before running shell commands with file paths, execute `pwd` to confirm your current working directory and adjust paths if necessary to ensure they are relative to the project root.

Run verification checks (adapt commands to your project's tooling):

1. **Check what files exist:**
```bash
   # For TypeScript/React projects:
   find src -type f -name "*.ts" -o -name "*.tsx" 2>/dev/null | head -20

   # For Python projects:
   find . -type f -name "*.py" 2>/dev/null | grep -v __pycache__ | head -20

   # For general projects:
   git ls-files | head -20
```

2. **Run validation/tests:**
```bash
   # Try common validation commands:
   npm run validate 2>/dev/null || npm test 2>/dev/null || pytest 2>/dev/null || echo "No validation script found"
```

3. **Check dev server/build:**
```bash
   # Check if dev server is configured:
   npm run dev --help 2>/dev/null || python manage.py runserver --help 2>/dev/null || echo "Dev server command not found"
```

## Step 6: Check for Drift

Compare task list status with actual codebase:

- Do completed tasks (✅) have corresponding files?
- Are there unexpected files that shouldn't exist yet?
- Does existing code follow CLAUDE.md standards?
- Flag any discrepancies for user to resolve

---

## Step 6.5: Validate Plan Still Applies

**Run validation script:**
```bash
python3 .claude/utils/plan_validator.py [feature-name]
```

**Expected output:** JSON with validation category:
```json
{
  "category": "valid",
  "checks": {
    "goal_unchanged": true,
    "dependencies_met": true,
    "approach_sound": true
  },
  "issues": [],
  "recommendation": "Continue with current plan"
}
```

**This script:**
- ✅ Runs the 3 boolean checks (Goal/Dependencies/Approach)
- ✅ Returns valid/update/invalid category
- ✅ Does NOT load PLAN_QUALITY_RUBRIC.md

**Categories:**
- **"valid"** → All checks pass, continue to Step 7
- **"update"** → 1 check fails, update plan.md to reflect changes, then continue
- **"invalid"** → Multiple checks fail, recommend /replan-feature or /check-drift

**CRITICAL:** The validator script enforces lightweight validation. DO NOT manually load PLAN_QUALITY_RUBRIC.md unless user explicitly runs `/check-drift` for detailed analysis.

**Parse JSON output and take action based on category.**

---

## Step 7: Summarize Status

Provide clear summary in this exact format:
```
📍 RESUMING WORK
├─ Last Session: [Date from handoff or "Unknown"]
├─ Completed: [List tasks with ✅ from task list]
├─ Current State: [1 sentence: what's working]
├─ Plan Drift: [✅ None / ⚠️ Minor / 🚫 Major]  ← NEW
├─ Code Quality: [Quick check: matches CLAUDE.md standards? Yes/Issues found]
└─ Next Task: [Exact task number and name from task list] (Est: [X]h - see TASK_ESTIMATION_GUIDE.md)  ← NEW

🎯 IMMEDIATE CONTEXT
[2-3 sentences: what was built and why we stopped]

⚠️ REMINDERS (from CLAUDE.md)
[Bullet list of 2-3 key principles or anti-patterns from CLAUDE.md]

⚡ NEXT STEPS
1. [First concrete action from next task]
2. [Second concrete action]
3. [Verification step against CLAUDE.md standards]

📊 Estimation Guidance: See `docs/planning/TASK_ESTIMATION_GUIDE.md` for similar tasks  ← NEW
```

## Step 8: Ready to Continue

After providing summary, ask ONE clear question:

**"Should I proceed with [Next Task Name], or do you want to adjust the plan first?"**

Wait for user confirmation before taking action.

---

## Important Notes

- **Never skip CLAUDE.md** - Read it FIRST
- **Validate plan on resume** - Check if still applicable (Step 4.5)
- **Reference estimation guide** - Use `TASK_ESTIMATION_GUIDE.md` for sizing
- **Check drift systematically** - Use boolean checks, not intuition
- **Be explicit about file paths** - Use actual paths found, not assumptions
- **Highlight inconsistencies** - Between docs and code state
- **Reference CLAUDE.md throughout session** - To maintain quality standards
- **Don't make assumptions** - Verify with file checks, not memory
- **Keep summary concise** - User can read docs themselves if needed

---

## References (Load Only When Needed)

**Standards (Conditional Loading):**
- `docs/planning/PLAN_QUALITY_RUBRIC.md` - ⚠️ Load ONLY if `/check-drift` called
- `docs/planning/TASK_ESTIMATION_GUIDE.md` - ⚠️ Load ONLY if `/add-task` called

**Related Commands:**
- `/check-drift` - If plan seems off (will load rubric)
- `/replan-feature` - If plan invalidated
- `/add-task` - Add discovered work (will load estimation guide)

---

## Quality Checklist

Before presenting summary, verify:
- [ ] CLAUDE.md was read first
- [ ] **feature_discovery.py was used (not manual file read)**
- [ ] **User was prompted for feature selection BEFORE loading any contexts**
- [ ] **handoff_loader.py was used with selected feature only**
- [ ] **plan_validator.py was used (no manual PLAN_QUALITY_RUBRIC.md loading)**
- [ ] Only selected feature's files were loaded (not all active features)
- [ ] Actual files were checked (not assumed)
- [ ] Drift between tasks and code was assessed (Step 6)
- [ ] Plan validation completed (Step 6.5)
- [ ] Next task is clearly identified from task list
- [ ] Estimation reference included in summary
- [ ] Reminders from CLAUDE.md are included
- [ ] Summary is concise (<20 lines)
