---
description: Start a new feature by selecting from backlog and setting up planning docs
argument-hint: feature-name or feature-number
allowed-tools: read_file, list_dir, glob_file_search, run_terminal_cmd, todo_write, grep, codebase_search, search_replace, write
---

## Command

You are helping the user start work on a new feature. Follow this systematic process to select the right feature, plan it properly, and begin implementation.

## Step 1: Load Context

**Read in this order:**

1. **`CLAUDE.md`** - Project standards and current status
2. **Feature backlog:** `docs/planning/FEATURES_BACKLOG.md` (to identify active features)
3. **Task estimation guide:** `docs/planning/TASK_ESTIMATION_GUIDE.md` (for sizing guidance)

## Step 1.5: Feature Input Method

**Ask user:** "What would you like to work on?"

**Three paths:**

### Path A: From Backlog
If FEATURES_BACKLOG.md exists:
→ Show prioritized list
→ User selects number

### Path B: New Feature (Direct Description)
User describes feature:
→ Assess size and handle accordingly

### Path C: No Input (Interactive)
User runs `/start-feature` without argument:
→ "Describe feature or select from backlog: [list]"

**Handle all three gracefully** - backlog is optional.

## Step 2: Show Available Features

If feature backlog exists and user didn't provide description, present features grouped by priority/tier:

```
🎯 HIGH PRIORITY (High Value, Low Risk)
1. Feature #2: [Feature name] ([X] hours)
   - [Key value proposition]
   - [Why it's low risk]

2. Feature #4: [Feature name] ([X] hours)
   - [Key value proposition]

📋 MEDIUM PRIORITY (High Value, Manage Risk)
3. Feature #3: [Feature name] ([X] hours)
   - [Key value proposition]
   - [Risk to manage]

...and [N] more features in lower priority
```

**Ask user:**
"Which feature would you like to work on? (Enter number, or describe a new feature)"

## Step 2.5: Auto-Breakdown for Large Features

**After feature selection, assess size using TASK_ESTIMATION_GUIDE.md:**

### If >15 Hours (Tier 3)
🚫 **Stop - break down first:**
- Show MVP approach (6-hour version)
- Identify features that can be split
- User picks starting feature
- Defer others to backlog

**Example:**
```
This feature is estimated at 20 hours (Tier 3).

I recommend breaking it down:
- Feature A: OAuth authentication only (8h) ⭐ START HERE
- Feature B: Query generation API (12h) - defer to backlog

Which feature would you like to start with?
```

---

### If 7-15 Hours (Tier 2)
⚠️ **Warn about multi-session:**
- This will require 2-3 sessions
- Add checkpoints every 6 hours
- Mark pause safety (🟢 Safe pause / 🟡 Risky / 🔴 Must complete)
- Ensure phases are independently shippable

**Continue to Step 3 (Create feature doc with checkpoints)**

---

### If ≤6 Hours (Tier 1)
✅ **Proceed immediately:**
- Single session feature
- No checkpoints needed
- **Continue to Step 3 (Create feature doc)**

**Reference:** See `docs/planning/TASK_ESTIMATION_GUIDE.md` for calibration data and patterns.

---

## Step 3: Determine Feature Complexity

Based on user selection and size assessment, determine approach:

### Simple Feature (≤3 hours, Tier 1)
**Indicators:**
- Effort ≤ 3 hours
- No architectural decisions needed
- Single component, function, or module
- Self-contained changes

**Action:** Create lightweight plan, skip to Step 5 (Add to task list and start coding)

### Complex Feature (Multi-Session, Tier 1-2)
**Indicators:**
- Effort 3-15 hours (Tier 1-2)
- May require architectural decisions
- May span multiple components
- Needs detailed planning

**Action:** Continue to Step 4 (Create feature doc)

## Step 4: Choose Planning Depth

**For Tier 1 (≤6h):**
Ask user: "Start with lightweight README or full plan?"
- **Option A: Lightweight README** (recommended for simple features)
  - 5-20 line overview with key points
  - Can evolve to full plan.md if needed
  - Saves context, faster startup
- **Option B: Full plan.md** (if uncertainty exists)
  - Detailed breakdown with all sections
  - Use when technical approach unclear

**For Tier 2 (7-15h):**
**Recommend full plan.md** (but allow README option if user prefers)
- Multi-session features benefit from detailed planning
- Can still start with README and expand later

**For Tier 3 (>15h):**
Already rejected in Step 2.5 (must split)

---

## Step 4.1: Create Feature Directory

```bash
mkdir -p docs/planning/features/FEATURE_NAME
```

**Add to active features index:**
```bash
python3 .claude/utils/active_features_manager.py add "FEATURE_NAME"
```

---

## Step 4.2: Create Plan Document

### Option A: Lightweight README.md (Tier 1 default)

Create `docs/planning/features/FEATURE_NAME/README.md`:

```markdown
# [Feature Name]

**Effort:** [X]h | **Status:** In Progress

## Goal
[1-2 sentence goal - what we're building and why]

## Approach
- [Key technical decision 1]
- [Key technical decision 2]
- [Key technical decision 3]

## Tasks
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

## Files to Change
- `path/to/file1.py` - [what changes]
- `path/to/file2.py` - [what changes]

## Open Questions
- [Question 1]
```

**Then continue to Step 5 (no HANDOFF.md needed for lightweight)**

---

### Option B: Full plan.md (Tier 2+ or complex Tier 1)

1. Copy template:
   ```bash
   cp docs/planning/features/_TEMPLATE.md docs/planning/features/FEATURE_NAME/plan.md
   ```

2. Fill in the `plan.md` with:
   - Business context from backlog or user description
   - Technical approach (use `/plan-approaches` if multiple valid options)
   - Data models & API contracts (if applicable)
   - Migration strategy (if applicable)
   - Task breakdown with clear steps
   - Open questions

3. Create initial `HANDOFF.md`:
   ```bash
   touch docs/planning/features/FEATURE_NAME/HANDOFF.md
   ```

   Fill with:
   - Current state: "Planning complete"
   - Next session focus: First task from plan
   - Key context: Summary of approach
   - Blockers: None or list any

4. **Ask user to review:**
   "I've created `docs/planning/features/FEATURE_NAME/plan.md`. Review the approach and let me know if you want to adjust before I break it into tasks."

## Step 4.5: Validate Plan Quality (Auto-run)

**Run quality checks from `docs/planning/PLAN_QUALITY_RUBRIC.md`:**

### Quick Validation Checks

**1. Size check:**
- ≤6h (Tier 1): ✅ Single session
- 7-15h (Tier 2): ⚠️ Multi-session (has checkpoints?)
- >15h (Tier 3): 🚫 Must split

**2. Scope check:**
- Goal clear and measurable?
- Out-of-scope documented?
- No vague language ("improve", "enhance")?

**3. Tasks check:**
- Concrete steps (not "implement X")?
- Acceptance criteria defined?
- Files/components identified?

**4. CLAUDE.md standards:**
- Follows project anti-patterns?
- Example project-specific checks:
  - ✅ Validates queries before execution?
  - ✅ Uses proper data tables?
  - ✅ Includes required filters on large tables?

### Output Assessment

**✅ Ready (All checks pass):**
```
✅ Plan validation passed
- Size: [X]h (Tier [1/2])
- Scope: Clear and focused
- Tasks: Concrete with acceptance criteria
- Standards: Follows CLAUDE.md

Proceed to Step 5.
```

---

**⚠️ Needs Quick Fixes (1-2 checks fail):**
```
⚠️ Plan needs minor refinements

Issues found:
1. Missing checkpoints (Tier 2 feature, 12h)
2. Out-of-scope not documented

Fixes (10-15 min):
- Add checkpoint after Phase 1 (6h mark)
- Add "Out of Scope" section

Apply auto-fixes? [Y/n]
```

**If user approves:** Apply fixes, continue to Step 5
**If user declines:** Document issues, continue with caution

---

**🚫 Not Ready (Major issues):**
```
🚫 Plan has major quality issues

Critical problems:
1. Effort 20h (must split into ≤8h features)
2. Goal vague ("improve query performance")
3. No out-of-scope defined

Cannot proceed until fixed.

Actions:
- Split feature using Step 2.5 breakdown
- Define specific goal: "Reduce validation from 30s to <5s"
- Add out-of-scope section

Fix now or defer to backlog? [Fix/Defer]
```

**Block implementation until critical issues resolved.**

**Reference:** Full rubric at `docs/planning/PLAN_QUALITY_RUBRIC.md`

---

## Step 5: Update FEATURES_BACKLOG.md

**Add new feature to "🚧 In Progress" section:**

```markdown
### [Feature Name] ⭐
**Status:** In Progress (Phase 1)
**Started:** [Date]
**Effort:** [X]h total, 0h done (0%)
**Priority:** [High/Medium/Low]
**Feature Doc:** `docs/planning/features/[feature-name]/`

**Current Focus:** [First phase/task]

**Quick Status:**
- 📋 Just started
- Next: [First concrete task]

**Blockers:** None

**Description:** [1-2 sentence summary]
```

**Do NOT create CURRENT_SPRINT.md** - backlog is single source of truth for parallel Claude instances

## Step 6: Start Implementation

**For Simple Features:**
1. Update task list with new task
2. Ask: "Ready to start implementing [Feature Name]?"
3. If yes: Begin coding following CLAUDE.md standards

**For Complex Features:**
1. Update task list with reference to feature doc
2. Create feature doc at appropriate location
3. Ask: "Feature doc created. Ready to start Task [N.1]: [First subtask]?"
4. If yes: Begin coding first subtask

## Step 7: Set Up Tracking

**Create todo list** for the feature:
```typescript
[
  { content: "Task [N]: Feature Name", status: "in_progress", activeForm: "Working on Feature Name" },
  // Add subtasks if complex feature
]
```

**Remind user about handoffs (if applicable):**
"If this takes multiple sessions, consider creating a handoff doc when you pause."

---

## Decision Matrix

| Situation | Action |
|-----------|--------|
| Feature in backlog, simple (≤3h) | Add to task list → Start coding |
| Feature in backlog, complex (>3h) | Create feature doc → Break into tasks → Start first task |
| New feature idea (not in backlog) | Add to backlog → Follow matrix |
| User unsure which feature | Show high-priority options, recommend based on value/risk |

---

## Example Flows

### Example 1: Simple Feature
```
User: Let's add a copy-to-clipboard button
Claude: That's a simple feature (~1 hour). I'll add it to TASKS.md as Task 5.
[Adds task to task list]
Claude: Ready to implement? I'll create a CopyButton component.
User: Yes
[Start coding]
```

### Example 2: Complex Feature
```
User: Let's integrate with the external API
Claude: That's a complex feature (8+ hours). I'll create a feature doc first.
[Creates feature doc at appropriate location]
Claude: I've outlined 3 approaches:
  A. Direct API calls (simple but CORS issues)
  B. Backend proxy (secure, needs deployment)
  C. Hybrid (cache + API)
Which approach do you prefer?
User: Option B
[Updates feature doc, breaks into tasks]
Claude: Added Phase 3 with 4 tasks. Ready to start Task 3.1 (API contracts)?
User: Yes
[Start coding first task]
```

---

## Important Reminders

- **Check task list first** - Don't duplicate in-progress work
- **Reference CLAUDE.md** - Follow project standards throughout
- **Use existing features** - Pull from backlog when available
- **Keep it simple** - Don't over-plan, start with lightest viable approach
- **Feature docs are optional** - Only for complex, multi-session work
- **Adapt paths** - Use your project's actual documentation structure
- **Size enforcement** - >15h features must be broken down
- **Validate before starting** - Run Step 4.5 validation automatically

---

## References

**Standards:**
- `docs/planning/PLAN_QUALITY_RUBRIC.md` - Plan validation criteria
- `docs/planning/TASK_ESTIMATION_GUIDE.md` - Sizing guidance and calibration

**Related Commands:**
- `/validate-plan` - Full quality check (auto-run in Step 4.5)
- `/add-task` - Add discovered tasks during implementation
- `/check-drift` - Detailed drift analysis

---

## Output Format

After selecting feature, present:

```
✅ FEATURE SELECTED: [Feature Name]
├─ Priority: [High/Medium/Low]
├─ Effort: [X hours]
├─ Complexity: Simple | Complex
└─ Action: [Add to task list | Create feature doc]

📋 WHAT I'LL DO:
1. [Action 1]
2. [Action 2]
3. [Action 3]

⚡ FIRST STEP:
[Concrete next action: "Create component", "Write feature doc", etc.]

Ready to proceed?
```

Wait for user confirmation before making any changes.

