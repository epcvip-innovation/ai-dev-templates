---
description: Align and optimize project documentation when approaching context limits during active development
allowed-tools: read_file, write_file, edit_file, run_terminal_cmd, grep, glob_file_search
---

[!WARNING]
**This command is deprecated.**

Use `/session-handoff` instead, which provides:
- Better context optimization
- Automatic drift detection
- Structured handoff creation
- Quality gates

This command is kept for backward compatibility but is not recommended for new projects.

---

## Command

I'll optimize the project documentation to prepare for a context reset or session transition.

## Step 1: Assess Current Documentation State

First, checking the project structure and documentation:

**For .projects/ structure:**
```bash
# Check project exists
ls -la .projects/[feature-name]/ 2>/dev/null || echo "No .projects/ folder found"

# Count lines in key files
wc -l .projects/[feature-name]/*.md 2>/dev/null | sort -rn
```

**For backlog/ structure:**
```bash
ls -la backlog/ 2>/dev/null
wc -l backlog/*.md 2>/dev/null | sort -rn
```

**For features/ structure:**
```bash
ls -la features/[feature-name]/ 2>/dev/null
wc -l features/[feature-name]/*.md 2>/dev/null | sort -rn
```

## Step 2: Analyze Task Completion Status

Checking what's consuming context:

```bash
# For standard TASKS.md format
echo "📊 Task Status:"
grep -c "✅\|^\- \[x\]" [path-to-tasks.md] 2>/dev/null && echo "completed tasks"
grep -c "→\|^\- \[ \]" [path-to-tasks.md] 2>/dev/null && echo "pending tasks"

# Check last modification
ls -la [path-to-tasks.md]
```

## Step 3: Archive Completed Work Details

Creating session archive for completed tasks:

```bash
# Create archive directory (adapt path to your structure)
mkdir -p .projects/[feature-name]/archive
# OR
mkdir -p backlog/archive
# OR
mkdir -p features/[feature-name]/archive

# Generate session timestamp
SESSION_TIME=$(date +"%Y%m%d-%H%M")
```

**Create archive file** at appropriate location:
- `backlog/[feature-name]/archive/session-${SESSION_TIME}.md`
- `backlog/archive/session-${SESSION_TIME}.md`
- `.projects/[feature-name]/archive/session-${SESSION_TIME}.md`

Archive should contain:
- Detailed implementation notes from completed tasks
- Code snippets and decisions made
- Test results from this session
- Any debugging notes or discoveries

## Step 4: Simplify Task List

Updating task list to focus on what's next:

**Changes to make:**
- Move verbose completed task details to archive
- Keep only task titles and status for completed work
- Add "RESUME HERE:" marker at current position
- Insert relevant checkpoints:
  - "CHECKPOINT: Gather user feedback" (if UI changes made)
  - "CHECKPOINT: Code review" (if major phase completed)
  - "CHECKPOINT: Align docs" (before next long session)

**Example simplified task format:**
```markdown
### Completed This Session
- ✅ Task 1: Feature scaffolding (see archive/session-20250101-1400.md)
- ✅ Task 2: Data layer implementation (see archive)

### RESUME HERE: Current Task
→ Task 3: UI component integration
  - Completed: Component structure, props interface
  - Next: Wire up data fetching

### Upcoming
- Task 4: Error handling
- Task 5: Testing
```

## Step 5: Update HANDOFF Document

Creating/updating comprehensive handoff for next session:

**Update HANDOFF.md** (or create if doesn't exist) with:

```markdown
# Handoff: [Feature Name]

**Last Updated**: [Timestamp]
**Last Active**: [Specific component/file being worked on]

## Session Work Summary
- [What was accomplished this session]
- [Key decisions made]
- [Files modified]

## Current State
- What's working: [Brief status]
- What's in progress: [Current task]
- What's blocked: [Any blockers or questions]

## Next Steps
1. [Specific immediate action]
2. [Secondary action if first is blocked]
3. [Tertiary option]

## Key Files Modified This Session
- `src/components/[file].tsx` - [What changed]
- `src/utils/[file].ts` - [What changed]

## Test Status
- [Test results, if applicable]
- [Manual testing needed]

## Known Issues
- [Any bugs discovered]
- [Technical debt introduced]
```

## Step 6: Document Feedback Needs (If Applicable)

If UI changes, test files, or features need verification:

**Create/update feedback tracking:**
```markdown
# User Feedback Needed

## Features to Verify
- [ ] [Feature 1] - [What to test]
- [ ] [Feature 2] - [Expected behavior]

## Test Files/Locations
- `[path to test file]` - [What it demonstrates]

## Known Issues to Watch For
- [Issue 1]
- [Issue 2]

## Browser/Device Requirements
- [Any specific requirements]
```

## Step 7: Add Strategic Checkpoints

Insert checkpoints in task list based on development flow:

### User Feedback Checkpoints
Add when:
- New UI components created
- Interactive features implemented
- UX flow changes made

### Code Review Checkpoints
Add when:
- Major phase completed
- 500+ lines added
- Core functionality refactored
- New patterns introduced

### Documentation Alignment Checkpoints
Add when:
- Approaching ~140k context
- Switching between major phases
- After 3-4 hours continuous development
- Before anticipated break

## Step 8: Generate Session Summary

Provide a quick-reference summary:

```
📊 DOCUMENTATION ALIGNMENT COMPLETE
===================================

Session Stats:
- Time: [Current timestamp]
- Estimated Context: ~XXXk tokens
- Major Achievement: [Key accomplishment]

✅ Completed This Session:
- [Task 1]
- [Task 2]
- [Task 3]

⏳ Awaiting User Feedback:
- [Feedback item 1]
- [Or "None currently"]

🎯 Next Session Should:
1. [Specific next action]
2. [Secondary action]
3. [Tertiary option]

📝 Checkpoints Added:
- [Checkpoint 1]
- [Checkpoint 2]

📁 Archive Created:
- [Path to session archive]

Ready for context reset! New session can resume quickly with HANDOFF.md
```

---

## Quality Assurance Reminders

**For Next Session:**
- If user feedback was gathered → Apply changes before continuing
- If code review is due → Run review before new features
- If tests are failing → Fix before adding features
- If refactoring needed → Do it before phase changes

---

## Context Optimization Tips

**What to reference in next session:**
1. HANDOFF.md - Current state and next steps
2. TASKS.md - What to work on (simplified version)
3. Feedback tracking doc - If awaiting verification
4. CLAUDE.md - Always (project standards)

**What NOT to reference (unless specifically needed):**
- Completed phase archives
- Old code review files
- Detailed implementation notes from past sessions
- Historical test results

---

## Example Workflow

```
# Current state: 3 hours into development, context approaching 120k tokens

/align-project-docs

[Command runs through all steps]

Result:
- Created archive/session-20250101-1430.md (detailed notes)
- Simplified TASKS.md (30% smaller, still complete)
- Updated HANDOFF.md (ready for next session)
- Added 2 checkpoints to task list
- Generated summary showing next steps

# Next session (hours or days later):

/resume-feature

[Command reads HANDOFF.md and simplified TASKS.md]
[Context restored in <2 minutes vs 5-10 minutes with verbose docs]
```

---

Documentation aligned for efficient context usage!

