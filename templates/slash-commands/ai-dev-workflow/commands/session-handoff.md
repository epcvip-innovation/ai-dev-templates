---
description: Optimize context and create handoff for next session - replaces /compact with explicit control
allowed-tools: read_file, write_file, edit_file, run_terminal_cmd, grep, glob_file_search, todo_write
argument-hint: (optional: custom focus for handoff)
---

## Purpose

Replace Claude Code's opaque `/compact` command with explicit, structured context management.

**Use this when**:
- Approaching context limits (130K+ tokens)
- End of work session (any time)
- Switching projects/features
- After completing major milestone
- Before anticipated break

**This command will**:
1. ✅ Archive completed work details
2. ✅ Simplify task format (mark complete, reduce verbosity)
3. ✅ Create/update HANDOFF.md with resume context
4. ✅ Add strategic checkpoints
5. ✅ Run quality gates
6. ✅ Generate session summary

**Note**: For thorough markdown file cleanup, run `/audit-artifacts` separately (requires more context).

---

## Step 1: Locate Project Documentation

First, identify the project structure:

```bash
# Check for project documentation structure
if [ -d ".projects" ]; then
  echo "📁 Using .projects/ structure"
  PROJECT_DIR=".projects"
  ls -la .projects/
elif [ -d "docs/planning" ]; then
  echo "📁 Using docs/planning/ structure"
  PROJECT_DIR="docs/planning"
  ls -la docs/planning/
elif [ -d "features" ]; then
  echo "📁 Using features/ structure"
  PROJECT_DIR="features"
  ls -la features/
else
  echo "❌ No standard project structure found"
  echo "   Looked for: .projects/, docs/planning/, features/"
  echo "   Continue with root-level files only? [Y/n]"
fi
```

**Identify key files**:
- Task tracking: TASKS.md, tasks.md, TODO.md
- Current handoff: HANDOFF.md
- Project overview: plan.md, PROJECT_OVERVIEW.md

**Identify current feature name** (for summary):
```bash
# Option 1: Use feature discovery to find active features
python3 .claude/utils/feature_discovery.py

# Option 2: Check HANDOFF.md location
# If HANDOFF.md is at docs/planning/features/[feature-name]/HANDOFF.md
# The feature name is the directory name

# Option 3: Check .active-features file
cat .active-features 2>/dev/null | grep -v "^#" | head -1
```

**Store feature name** for use in Step 8 summary.

---

## Step 2: Analyze Task Completion Status

Read the task file and identify what's complete:

```bash
# Find task file
TASK_FILE=$(find ${PROJECT_DIR:-.} -name "TASKS.md" -o -name "tasks.md" -o -name "TODO.md" 2>/dev/null | head -1)

if [ -f "$TASK_FILE" ]; then
  echo "📊 Task Analysis: $TASK_FILE"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Count completed tasks
  COMPLETED=$(grep -c "✅\|^- \[x\]\|→.*COMPLETE" "$TASK_FILE" 2>/dev/null || echo "0")
  echo "Completed: $COMPLETED tasks"

  # Count pending tasks
  PENDING=$(grep -c "^- \[ \]\|→.*TODO\|→.*IN PROGRESS" "$TASK_FILE" 2>/dev/null || echo "0")
  echo "Pending: $PENDING tasks"

  # File size
  LINES=$(wc -l < "$TASK_FILE")
  echo "Total lines: $LINES"

  # Last modified
  ls -lh "$TASK_FILE" | awk '{print "Last modified: " $6, $7, $8}'
else
  echo "⚠️  No task file found"
fi
```

**Review task file** to understand:
- Which phases/tasks are complete?
- Which task are you currently on?
- What's the current focus?

---

## Step 2.5: Drift Detection (Auto-run for Non-Trivial Features)

**Skip drift check if**:
- Task <1 hour (trivial)
- First session (nothing to compare)
- No plan.md exists (ad-hoc work)

**Otherwise, run drift check inline**:

### Load Context for Drift Check

1. **Find plan document:** `docs/planning/features/[name]/plan.md`
2. **Read original:** goal, estimate, tasks, approach
3. **Read current state:** HANDOFF.md, git log (last 10-20 commits), task status

### Run Boolean Checklist

**5 quick checks**:

1. **Goal unchanged?** (✅ YES / ❌ NO)
   - Compare original plan goal vs current HANDOFF/reality

2. **Approach unchanged/refined?** (✅ SAME / ⚠️ MINOR / 🚫 MAJOR)
   - Compare original approach vs implemented approach

3. **Task drift ≤2?** (✅ ≤2 / ⚠️ 3-5 / 🚫 >5)
   - Count: added_tasks - removed_tasks

4. **No new blockers?** (✅ NONE / ⚠️ WORKAROUND / 🚫 FUNDAMENTAL)
   - Check HANDOFF or conversation for blockers discovered

5. **Time <2x estimate?** (✅ NO / 🚫 YES)
   - Ask user: "Did this take more than 2x the original estimate?"

### Categorize and Act

**All checks pass (✅ Healthy)**:
```
✅ DRIFT CHECK: Healthy Evolution

No significant drift detected.
- Goal: Unchanged
- Approach: [Same/Minor refinement]
- Tasks: [+N] (within normal range)
- Blockers: None
- Time: On track

Action: Document in handoff, continue to Step 3
```
→ Continue to Step 3 (archive and handoff)

---

**1-2 checks fail (⚠️ Moderate)**:
```
⚠️ DRIFT CHECK: Moderate Drift

Drift detected:
- [Issue 1 description]
- [Issue 2 description]

Recommended:
1. Update plan.md with revised estimate: [X]h → [Y]h
2. Document drift rationale in plan
3. Continue with adjusted plan

Update plan now? [Y/n]
```

**If user approves**:
- Update plan.md effort estimate
- Add drift notes to plan
- Continue to Step 3

**If user declines**:
- Note drift in HANDOFF.md only
- Continue to Step 3

---

**Red flag present (🚫 Major)**:
```
🚫 DRIFT CHECK: Major Drift Detected

Critical issue:
- [Red flag description - goal changed, >5 tasks, >2x time, etc.]

This requires replanning, not just handoff.

Recommended actions:
1. Stop current handoff
2. Run `/replan-feature` (if available) OR
3. Manually assess if feature should:
   - Be split into smaller features
   - Have scope reduced
   - Be replanned from scratch

Proceed with handoff anyway? [y/N] (not recommended)
```

**Default action:** Stop handoff, ask user to address drift first

---

**This replaces your manual question:** "Did anything unexpected happen?"

Now it's systematic, automatic, and uses deterministic boolean checks.

**Reference:** Full drift rubric at `docs/planning/PLAN_QUALITY_RUBRIC.md`

---

## Step 3: Archive Completed Work Details

Create timestamped archive for completed task details:

```bash
# Determine archive location based on structure
if [ -d "${PROJECT_DIR}" ]; then
  ARCHIVE_DIR="${PROJECT_DIR}/archive"
else
  ARCHIVE_DIR="./archive"
fi

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

# Generate session timestamp
SESSION_TIME=$(date +"%Y%m%d-%H%M")
ARCHIVE_FILE="${ARCHIVE_DIR}/session-${SESSION_TIME}.md"

echo "📁 Creating archive: $ARCHIVE_FILE"
```

**Create archive file** with:

```markdown
# Session Archive - [Date/Time]

**Session Duration**: [X hours]
**Focus**: [What phase/feature was worked on]
**Status**: [Completed/In Progress/Blocked]

---

## Completed Work Details

### [Phase/Task Name]

**What was implemented**:
- [Detailed implementation note 1]
- [Detailed implementation note 2]
- [Code snippets, if relevant]

**Files modified**:
- `path/to/file.ts` - [Specific changes made]
- `path/to/file2.ts` - [Specific changes made]

**Decisions made**:
- **Decision**: [What was decided]
  - **Rationale**: [Why this approach]
  - **Alternatives considered**: [What else was evaluated]
  - **Trade-offs**: [What was sacrificed]

**Test results**:
- [Test outcomes from this session]
- [Manual testing performed]

**Discoveries**:
- [Important findings]
- [Gotchas or edge cases discovered]

---

## Technical Details

**Approach taken**:
[Detailed explanation of implementation approach]

**Code patterns used**:
[Any patterns worth documenting]

**Dependencies added**:
- [Library] - [Why/what for]

---

## Notes for Future Reference

**If revisiting this work**:
- [Contextual note 1]
- [Contextual note 2]

**Known limitations**:
- [Limitation 1]
- [Limitation 2]
```

**Archive purpose**: Preserve detailed context without cluttering active task list.

---

## Step 4: Simplify Task Format

Update the task file to reduce verbosity while preserving essential information:

**Simplification rules**:

1. **For completed phases/tasks**:
   - Replace detailed implementation notes with summary
   - Keep one-line status: "✅ Task X: [Name] (see archive/session-TIMESTAMP.md)"
   - Preserve key decisions (1-2 sentences max)
   - List modified files

2. **For current task**:
   - Add "RESUME HERE:" marker
   - Keep detailed breakdown (what's done, what's next)
   - Include specific file references with line numbers
   - Document any blockers

3. **For future tasks**:
   - Keep as-is
   - Update priorities if they changed

**Example transformation**:

**Before** (verbose, 380 lines):
```markdown
## Phase 2: Authentication ✅ COMPLETED

### Task 2.1: Research authentication approaches
- Spent 2 hours researching JWT vs Session-based auth
- Read documentation for jsonwebtoken library
- Compared security implications of both approaches
- Evaluated refresh token strategies (rotation vs sliding window)
- Analyzed token storage options:
  - localStorage: Easy but XSS vulnerable
  - httpOnly cookies: Secure but CSRF considerations
  - sessionStorage: Per-tab, doesn't persist
- Created detailed comparison document
- Decision: JWT with httpOnly cookies + refresh tokens
- Implementation plan:
  - Access token: 15 min expiration
  - Refresh token: 7 day expiration
  - Rotation on refresh for security
  - Secure, httpOnly, sameSite=strict flags
- Files created: APPROACH_authentication-methods.md
- Time spent: 2 hours
- Status: Complete, decision documented, ready to implement

### Task 2.2: Implement JWT authentication
[... 50 more lines ...]
```

**After** (concise, 90 lines):
```markdown
## Phase 2: Authentication ✅ COMPLETED
**Completed**: [Date]
**Archive**: See archive/session-20250103-1430.md for details

### Completed Tasks
- ✅ Task 2.1: Authentication research (JWT with httpOnly cookies chosen)
- ✅ Task 2.2: JWT implementation (working, tests passing)
- ✅ Task 2.3: Password hashing (bcrypt, cost=12)

**Key Decisions**:
- JWT with httpOnly cookies (vs session-based)
- 15-min access token, 7-day refresh token
- All auth tests passing (12/12)

**Files**: `src/auth/jwt.ts`, `src/auth/password.ts`

---

## RESUME HERE: Phase 3 - User Management

### → Task 3.1: User registration endpoint (IN PROGRESS)

**Completed**:
- ✅ POST /api/users endpoint created
- ✅ Request validation (Zod schema)
- ✅ Email uniqueness check

**Next Steps**:
1. Add email verification flow
2. Create email templates
3. Send verification email

**Current Files**:
- `src/routes/users.ts` (lines 23-67) - Registration logic
- `src/middleware/validation.ts` (lines 45-78) - User schema

**Blocker**: Need SMTP credentials for email sending

### Task 3.2: Email verification (PENDING)
[Keep future tasks as-is]
```

**Context savings**: ~290 lines (76% reduction), details preserved in archive.

---

## Step 5: Create/Update HANDOFF.md

Generate comprehensive handoff for next session:

**Find or create HANDOFF.md**:
```bash
# Look for existing handoff
HANDOFF_FILE="${PROJECT_DIR}/HANDOFF.md"
if [ ! -f "$HANDOFF_FILE" ]; then
  # Try root directory
  HANDOFF_FILE="./HANDOFF.md"
fi

echo "📝 Updating: $HANDOFF_FILE"
```

**HANDOFF.md structure**:

**CRITICAL**: The `**Status:**` line MUST appear in the first 10 lines for discovery tools to work correctly.

```markdown
# Handoff: [Project/Feature Name]

**Last Updated**: [Timestamp]
**Session**: [Session number or date]
**Duration**: [X hours]
**Status**: [Brief one-liner status - e.g., "Phase 2 in progress", "Ready to start Phase 3"]

---

## Quick Resume (Read This First)

**Current Position**: [Phase X, Task Y]
**Last Working On**: [Specific file/component]
**Status**: [Brief one-liner status]

**Blocker** (if any): [Critical blocker or "None"]

**Next Action**: [Specific immediate next step]

---

## Drift Assessment (NEW)

**Last Checked**: [Date]
**Status**: [✅ Healthy / ⚠️ Moderate / 🚫 Major]

**Changes from Plan**:
- Tasks added: [N] ([list if >0])
- Tasks deferred: [N] ([list if >0])
- Estimate adjusted: [Original]h → [Current]h ([+/-N%])
- Approach: [Unchanged / Refined: [reason]]

**Assessment**: [Explanation of drift category]

**Reference**: See `docs/planning/TASK_ESTIMATION_GUIDE.md` for calibration

---

## Session Summary

**Completed This Session**:
- ✅ [Achievement 1]
- ✅ [Achievement 2]
- ✅ [Achievement 3]

**Key Decisions Made**:
- **Decision**: [What was decided]
  - **Rationale**: [Why this approach]
  - **Trade-off**: [What was sacrificed]
- **Decision**: [Another decision]
  - **Rationale**: [Reasoning]

**Drift from Plan** (if any):
- **Change**: [What differed from original plan]
  - **Why**: [Reason for deviation]
  - **Impact**: [How it affects future work]

---

## Current State

**What's Working**:
- [Component/feature 1 - status]
- [Component/feature 2 - status]

**What's In Progress**:
- [Current task with specific status]

**What's Blocked**:
- [Blocker 1 - impact and potential solution]
- [Or "None"]

---

## Files to Read (Next Session)

**Start here** (read first):
1. `path/to/file.ts` (lines X-Y) - [What to focus on]
2. This HANDOFF.md
3. TASKS.md ([Phase/Section])

**Reference if needed**:
4. `path/to/reference.ts` - [Context it provides]
5. `archive/session-TIMESTAMP.md` - [Detailed notes if needed]

**Skip unless debugging**:
- Archived sessions (decisions already made)
- Test files (all passing)
- Old exploration documents

---

## Next Steps (Priority Order)

### 1. [Immediate Next Task]
**Why**: [Reason this is priority]
**Action**: [Specific steps to take]
**Files**: `path/to/file.ts` (lines X-Y)
**Estimated**: [Time estimate]

### 2. [Secondary Task]
**Why**: [Reason]
**Action**: [Steps]
**Depends on**: [Prerequisites if any]

### 3. [Tertiary Task]
**Why**: [Reason]
**Alternative**: [If blocked, do this instead]

---

## Known Issues & Blockers

**Critical Blockers**:
- 🚫 [Blocker 1] - [Impact] - [Potential solution]

**Minor Issues**:
- ⚠️ [Issue 1] - [Impact: Low/Medium/High] - [Effort to fix]
- ⚠️ [Issue 2] - [When to address]

**Technical Debt**:
- [Shortcut taken] - [Why] - [When to fix: before X]

---

## Test Status

**Tests Passing**: X/Y
- ✅ [Test category 1] (X tests)
- ✅ [Test category 2] (Y tests)

**Tests Failing** (if any):
- ❌ [Test name] - [Error: brief description]

**Tests Needed**:
- [ ] [Feature that needs testing]
- [ ] [Edge case to verify]

**Manual Testing Done**:
- [Scenario tested] → [Result]

---

## Context for Next Session

**Mental Model**:
[Brief explanation of current understanding/approach]

**Key Files Modified This Session**:
- `path/to/file1.ts` - [What changed and why]
- `path/to/file2.ts` - [What changed and why]

**Important Patterns/Conventions**:
- [Pattern observed that should be followed]
- [Convention established]

**Gotchas**:
- ⚠️ [Specific pitfall to watch for]
- ⚠️ [Surprising behavior discovered]

---

## Quick Reference

**Start dev**: `[command]`
**Run tests**: `[command]`
**Current phase**: [Phase name]
**Next milestone**: [Milestone]

---

**Archive**: Details in `archive/session-[TIMESTAMP].md`
```

---

## Step 6: Add Strategic Checkpoints

Insert checkpoints into task list based on current state:

**Checkpoint types**:

### 1. User Feedback Checkpoint
Add when:
- UI components created this session
- Interactive features implemented
- UX flow changes made

```markdown
CHECKPOINT: Gather User Feedback
- [ ] Show [feature] to user
- [ ] Verify [behavior] meets expectations
- [ ] Collect feedback on [UI element]
```

### 2. Code Review Checkpoint
Add when:
- Major phase completed
- 500+ lines added
- Core functionality refactored
- New patterns introduced

```markdown
CHECKPOINT: Code Review
- [ ] Review [component/module] for anti-slop violations
- [ ] Check: Functions <50 lines
- [ ] Check: No console.log in production code
- [ ] Verify: TypeScript strict mode passing
```

### 3. Documentation Alignment Checkpoint
Add when:
- Long session (3-4+ hours)
- Major architectural changes
- Before switching to new phase

```markdown
CHECKPOINT: Documentation Alignment
- [ ] Update CLAUDE.md if new patterns introduced
- [ ] Verify TASKS.md reflects current priorities
- [ ] Ensure HANDOFF.md has latest blockers
```

**Insert checkpoints** at logical break points in task list, not at the very end.

---

## Step 7: Run Quality Gates

Execute validation checks before finalizing:

### 7.1 Test Status
```bash
# Run project tests (adapt to your stack)
echo "🧪 Running tests..."

# TypeScript/JavaScript
npm test 2>&1 | tail -20

# Python
# python -m pytest 2>&1 | tail -20

# Go
# go test ./... 2>&1 | tail -20
```

### 7.2 Linter Check
```bash
echo "🔍 Running linter..."

# TypeScript/JavaScript
npm run lint 2>&1 | tail -20

# Python
# ruff check . 2>&1 | tail -20

# Go
# golangci-lint run 2>&1 | tail -20
```

### 7.3 Code Quality Scan
```bash
echo "🔍 Checking for code quality issues..."

# Check for console.logs (JavaScript/TypeScript)
echo "Checking for console.log statements:"
grep -rn "console\.log" src/ --include="*.ts" --include="*.tsx" --include="*.js" 2>/dev/null | grep -v "// console" | head -10 || echo "✓ None found"

# Check for debugger statements
echo "Checking for debugger statements:"
grep -rn "debugger" src/ --include="*.ts" --include="*.tsx" --include="*.js" 2>/dev/null | head -10 || echo "✓ None found"

# Check for TODO comments (just count, don't fail)
echo "TODO comments in codebase:"
grep -rc "TODO\|FIXME" src/ --include="*.ts" --include="*.tsx" --include="*.js" 2>/dev/null | grep -v ":0$" | wc -l || echo "0"

# Check for unused imports (TypeScript)
# tsc --noEmit 2>&1 | grep "is declared but never used" | wc -l || echo "0"
```

**Document results** in handoff if issues found.

---

## Step 8: Generate Session Summary

Provide comprehensive summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SESSION HANDOFF COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🕐 Session Info:
├─ Timestamp: [Current date/time]
├─ Duration: [Estimated hours]
└─ Focus: [Main work area]

✅ Completed This Session:
├─ [Task 1]
├─ [Task 2]
└─ [Task 3]

📊 Drift Assessment: (NEW)
├─ Status: [✅ Healthy / ⚠️ Moderate / 🚫 Major]
├─ Estimate: [Original → Current] ([+/-N%])
├─ Tasks: [Added: N, Deferred: N]
└─ Approach: [Status]

📁 Context Optimization:
├─ Archived: session-[TIMESTAMP].md
├─ Simplified: TASKS.md ([X]% reduction, [Y] lines → [Z] lines)
├─ Updated: HANDOFF.md (with drift notes)
└─ Estimated token reduction: ~[X]%

🎯 Next Session Should:
1. [Immediate priority with reason]
2. [Secondary priority]
3. [Tertiary option if blocked]

✨ Quality Status:
├─ Tests: [X/Y passing] (or [Status])
├─ Linter: [Clean/Issues found]
├─ Code Quality: [No issues/X TODOs/Y console.logs]
└─ TypeScript: [No errors/X errors]

📝 Checkpoints Added:
├─ [Checkpoint 1]
└─ [Or "None needed"]

🚫 Blockers:
└─ [Critical blocker or "None"]

📚 Reference: `docs/planning/TASK_ESTIMATION_GUIDE.md` for next task sizing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Ready for Next Session!

Resume with:
1. Run `/resume-feature [feature-name]` (see below)
2. Or read HANDOFF.md (2-3 min) and continue manually
3. Continue from: [Specific file/line]

📌 Feature Name: `[feature-name]`
   → Resume with: `/resume-feature [feature-name]`

Or use /clear for fresh context (handoff preserved)

💡 For thorough markdown cleanup, run: /audit-artifacts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Important Notes

### What This Command Does NOT Do

**Skipped** (run `/audit-artifacts` separately if needed):
- ❌ Deep markdown file analysis
- ❌ Evaluation of temporary files
- ❌ Cleanup of exploratory documents

**Why**: Requires significant additional context. Run `/audit-artifacts` when context is comfortable.

### Drift Documentation

When simplifying TASKS.md, preserve **why** things changed from plan:
- Tasks that took longer/shorter than expected
- Unexpected technical challenges
- Additional tasks discovered
- Changes to approach
- Tasks skipped or deprioritized

**Example**:
```markdown
**Drift**: Task 2.3 required refactoring authentication flow (not planned)
- **Why**: Discovered security vulnerability in original approach
- **Impact**: +2 hours, but necessary for production readiness
```

### Integration with Resume

Next session workflow:
1. Start new session (or continue current)
2. Read HANDOFF.md (2-3 minutes)
3. Skim TASKS.md current section (1 minute)
4. Continue work from "RESUME HERE" marker

---

## Integration with Other Commands

This command now integrates with:
- `/check-drift` - Full drift analysis (auto-run in Step 2.5)
- `PLAN_QUALITY_RUBRIC.md` - Drift categorization
- `TASK_ESTIMATION_GUIDE.md` - Calibration updates

After each session, drift data feeds calibration log.

---

## References

**Standards:**
- `docs/planning/PLAN_QUALITY_RUBRIC.md` - Drift categories (Step 2.5)
- `docs/planning/TASK_ESTIMATION_GUIDE.md` - Update calibration log

**Related Commands:**
- `/check-drift` - Auto-run in Step 2.5
- `/add-task` - For unplanned tasks discovered
- `/validate-plan` - Re-validate after moderate drift

---

## Quality Checklist

Before completing, verify:
- [ ] Task file analyzed and completed work identified
- [ ] Drift check performed (Step 2.5) for non-trivial features
- [ ] Archive created with detailed session notes
- [ ] Task format simplified (completed → summary + archive ref)
- [ ] HANDOFF.md created/updated with comprehensive context (including drift assessment)
- [ ] Checkpoints added at appropriate locations
- [ ] Quality gates run (tests, linter, code scan)
- [ ] Summary generated showing next steps
- [ ] Drift from plan documented (if any)

---

Documentation optimized for next session! 🎉

