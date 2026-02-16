---
description: Complete a feature or task with cleanup, archiving, and documentation updates
allowed-tools: read_file, write_file, edit_file, run_terminal_cmd, grep, glob_file_search, todo_write
---

## Command

I'll complete this feature/task with proper cleanup, archiving, and documentation.

## Step 1: Review What Was Completed

**Read task tracking file** (adapt path to your project):
```bash
# Find and read task file
cat TASKS.md 2>/dev/null || cat backlog/TASKS.md 2>/dev/null || cat .projects/*/tasks.md 2>/dev/null
```

**Identify**:
1. What was completed this session/feature
2. What's in progress (if any)
3. What's pending for next work
4. Any drift from original plan

## Step 2: Quality & Cleanup Checks

Run comprehensive cleanup checks for your language/framework.

**See [CLEANUP_PATTERNS.md](./CLEANUP_PATTERNS.md) for**:
- Python cleanup patterns (pyc, pdb, print statements)
- TypeScript/JavaScript patterns (console.log, debugger)
- Generic patterns (temp files, TODO comments)

## Step 3: Run Validation

Run tests and validation (adapt commands to your project):

```bash
# Try common test/validation commands
npm run validate 2>/dev/null || npm test 2>/dev/null || pytest 2>/dev/null || python -m pytest 2>/dev/null || echo "No validation script found"

# Try linting
npm run lint 2>/dev/null || black . --check 2>/dev/null || flake8 2>/dev/null || echo "No linter configured"
```

Document validation status for handoff.

## Step 4: Archive Completed Work

### Option A: Create Session Archive (for docs-heavy projects)

```bash
# Create archive directory
mkdir -p archive/ 2>/dev/null || mkdir -p docs/archive/ 2>/dev/null || mkdir -p .projects/archive/ 2>/dev/null

# Generate timestamp
SESSION_TIME=$(date +"%Y%m%d-%H%M")
```

**Create archive file** at `archive/session-${SESSION_TIME}.md`:

```markdown
# Session Archive - [Date]

## What Was Completed
- [Task 1]: [Brief description]
- [Task 2]: [Brief description]

## Key Implementation Details
[Detailed notes that were in TASKS.md but should be archived]

## Decisions Made
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

## Files Modified
- `path/to/file` - [What changed]

## Issues Resolved
- [Issue 1]: [How it was fixed]
```

### Option B: Update CHANGELOG (for feature-focused projects)

**Append to CHANGELOG.md** (or create if doesn't exist):

```markdown
## [Date] - [Feature Name]

### Added
- [Feature or capability added]

### Changed
- [Existing functionality that changed]

### Fixed
- [Bugs that were fixed]

### Technical
- Files changed: [count], +[additions] -[deletions]
- Tests: [passing/total]
```

## Step 5: Update Feature Tracking

### Update Feature Plan Frontmatter

Update the plan's YAML frontmatter:
```yaml
---
status: complete
completed: YYYY-MM-DD
effort_actual: Xh  # Fill with actual time spent
---
```

### Update _BACKLOG.md

Move feature from "🚧 In Progress" to "✅ Recently Completed" section.

## Step 5.5: Consolidate Task List

Update task tracking file to reduce verbosity:

### For Completed Phases:
Replace detailed task lists with summaries:

```markdown
## Phase N: [Phase Name] ✅ COMPLETED
**Completed**: [Date range]
**What was built**:
- [Key deliverable 1]
- [Key deliverable 2]
- [Key deliverable 3]

**Key files**: `path/`, `path/file.ts`
**Result**: [One-sentence outcome]
**Details**: See archive/session-[timestamp].md
```

### For Active/Future Work:
Keep as-is, just update priority markers if needed.

## Step 6: Create or Update Handoff

**Create/update handoff document** at appropriate location:
- `backlog/[feature]/HANDOFF.md`
- `docs/HANDOFF.md` (project-wide)
- `HANDOFF.md` (root, if simple project)

```markdown
# Handoff: [Feature/Project Name]

**Last Updated**: [Timestamp]
**Status**: [Feature complete / Phase complete / Ready for next task]

## What Was Completed
[2-3 sentence summary of this work]

## Current State
- **Working**: [What's functional]
- **Quality**: [Validation status - tests passing, lint clean, etc.]
- **Known Issues**: [Any remaining issues or technical debt]

## Key Files Modified
- `path/to/file` - [What it does now]
- `path/to/file` - [What changed]

## Changes from Original Plan
[Only document significant drift]
- **Change**: [What differed]
  - **Why**: [Rationale]
  - **Impact**: [Effect on future work]

## Next High-Priority Tasks
[List 3-5 tasks in priority order]

1. **Task [N]: [Name]**
   - **Why**: [Business/technical reason]
   - **Estimated effort**: [S/M/L or hours]

2. **Task [N]: [Name]**
   - **Why**: [Reason]

## Context for Next Session
**Read first**:
1. `CLAUDE.md` - Project standards
2. `[task tracking file]` - Consolidated tasks
3. This handoff

**Commands**:
- Dev server: `[command]`
- Tests: `[command]`
- Lint: `[command]`
```

## Step 7: Clean Up Temporary Files

**Pre-flight Check:** Before running shell commands with file paths, execute `pwd` to confirm your current working directory and adjust paths if necessary to ensure they are relative to the project root.

Based on Step 2 findings, remove temporary files:

```bash
# Remove temp files (adapt patterns to your project)
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.log" -delete 2>/dev/null
find . -name "test-*.html" -delete 2>/dev/null
find . -name "*-temp.*" -delete 2>/dev/null

# Remove Python cache
find . -name "*.pyc" -delete 2>/dev/null
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null

# Remove build artifacts if not needed
rm -rf dist/ build/ 2>/dev/null

echo "✓ Cleanup complete"
```

## Step 8: Provide Completion Summary

Present this format:

```
🏁 FEATURE/TASK COMPLETION

✅ COMPLETED
├─ Tasks: [List completed task numbers/names]
├─ Validation: [Tests passing / Lint clean / etc.]
├─ Files changed: [Count]
└─ Archived: [Archive file path]

🧹 CLEANUP
├─ Temp files removed: [Count]
├─ Debug code: [Removed or "None found"]
├─ Console logs: [Removed or "None found"]
└─ Git status: [Clean or "N files uncommitted"]

📋 DOCUMENTATION
├─ Task list: [Consolidated / Updated]
├─ CHANGELOG: [Updated or "N/A"]
├─ Handoff: [Created/Updated at path]
└─ Archive: [Created at path]

🎯 NEXT UP
1. [Next task name]
   Why: [Reason]

2. [Alternative task]
   Why: [Reason]

📊 SESSION STATS
- Duration: [Estimate from task timestamps]
- Major achievement: [Key accomplishment]
- Quality: [Validation summary]

Ready for next feature/task!
```

---

## Important Reminders

### Completion Criteria

Only use this command when:
- ✅ Feature/task actually works
- ✅ Tests pass (or none needed)
- ✅ Code reviewed (manually via `/ai-review` or similar)
- ✅ No known critical bugs
- ✅ User acceptance obtained (if applicable)

### What to Archive

**DO archive**:
- Detailed implementation notes from completed work
- Decisions made and rationale
- Problems encountered and solutions
- Code snippets showing approach
- Test results and validation notes

**DON'T archive**:
- Code itself (it's in git)
- Information that should be in code comments
- Redundant summaries
- Future plans (keep in task list)

### Cleanup Balance

- **Too aggressive**: Might delete needed files
- **Too conservative**: Leaves clutter
- **Right balance**: Remove obvious temp files, flag uncertain ones for user review

---

## Quality Checklist

Before marking complete, verify:
- [ ] Feature/task actually works as intended
- [ ] Tests passing (or documented why not applicable)
- [ ] No debug code or console logs
- [ ] No temporary/test files remaining
- [ ] Task list consolidated or updated
- [ ] Handoff created/updated
- [ ] Archive created with implementation details
- [ ] CHANGELOG updated (if using changelog approach)
- [ ] Next priorities clearly identified
- [ ] Git status clean or documented

---

## Example Workflow

```
# Just finished implementing user authentication feature

/feature-complete

[Command runs through all steps]

Result:
- Removed 3 console.log statements
- Deleted 5 test-*.html files
- Created archive/session-20250101-1430.md
- Consolidated 8 completed tasks in TASKS.md
- Updated HANDOFF.md with next priorities
- Updated CHANGELOG.md
- All tests passing, lint clean

Next up: Task 3 - Add password reset flow (high priority, 2-3 hours)

Ready to start next task!
```

---

Feature/task completion checklist satisfied!

