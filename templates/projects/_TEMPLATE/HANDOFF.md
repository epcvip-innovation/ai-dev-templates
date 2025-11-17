# [Project Name] - Session Handoff

<!--
This file is for SESSION CONTINUITY - helping the next person/AI resume work.

PURPOSE: Answer "Where were we? What's next?"
AUDIENCE: Next session (Claude AI or human developer)
UPDATE FREQUENCY: Every session (end of each work session)

KEEP IT CURRENT: This should reflect the LATEST state, not historical.
If you want to keep old handoffs, move them to archive/session-[date].md
-->

**Session Date**: YYYY-MM-DD
**Worked By**: [Name or "Claude AI"]
**Duration**: [X hours]
**Next Session**: [Planned date or "TBD"]

---

## Current State Summary

<!--
One-paragraph answer to: "Where are we in this project?"
-->

[2-3 sentences describing current progress, what phase we're in, overall status]

**Current Phase**: [Phase X: Name from tasks.md]
**Current Task**: [Task X.Y from tasks.md with link]
**Overall Progress**: ~XX% complete

---

## What Was Accomplished This Session

<!--
Bullet list of completed work.
Link to specific commits if applicable.
-->

- ✅ [Completed task 1] - `src/file.ts` modified | [Commit SHA if applicable]
- ✅ [Completed task 2] - Tests added | All passing
- ✅ [Completed task 3] - Integration validated | Checkpoint 2.1 passed

**Key Changes**:
- [File/component modified]: [What changed and why]
- [New file created]: [Purpose]
- [Dependency added/updated]: [Reason]

**Tests Added**:
- [ ] Unit tests for [component] - XX tests added
- [ ] Integration test for [feature] - Validates [scenario]

**Commits**:
- `abc1234` - [Commit message]
- `def5678` - [Commit message]

---

## What's Next (Immediate Next Steps)

<!--
Clear instructions for next session to pick up immediately.
Be specific - don't make next person/AI guess.
-->

### Next Task: [Task X.Y from tasks.md]

**Objective**: [One sentence - what needs to be accomplished]

**Specific Steps**:
1. [Concrete action 1] - Location: `src/file.ts:123`
2. [Concrete action 2] - Expected outcome: [testable result]
3. [Concrete action 3] - Validation: `[command to run]`

**Files to Modify**:
- `src/file1.ts` - [What changes are needed]
- `src/file2.ts` - [What changes are needed]

**Files to Create**:
- `src/new-file.ts` - [Purpose and initial structure]

**Success Criteria**:
- [ ] [Specific testable outcome 1]
- [ ] [Specific testable outcome 2]
- [ ] [Validation command passes]

**Checkpoint**: After completing this task, run:
```bash
[specific test command]
# Expected output: [what you should see]
```

---

## Known Issues / Blockers

<!--
What's preventing progress or needs attention?
-->

### Active Blockers

| Issue | Impact | Owner | Status | Target Resolution |
|-------|--------|-------|--------|-------------------|
| [Blocker 1] | High | [Name] | Open | YYYY-MM-DD |
| [Blocker 2] | Medium | [Name] | Waiting | YYYY-MM-DD |

### Issues to Investigate

- ⚠️ [Issue 1]: [Brief description] - Location: `file.ts:123`
- ⚠️ [Issue 2]: [Brief description] - Needs research

### Technical Debt Created (To Address Later)

- [Shortcut taken]: [Why we did it] - TODO: [What needs fixing]
- [Temporary solution]: [Reason] - TODO: [Proper fix needed]

---

## Important Decisions Made This Session

<!--
Document WHY choices were made - prevents re-litigating later.
-->

**Decision 1**: [What was decided]
- **Context**: [Why decision was needed]
- **Options Considered**: [A vs B vs C]
- **Chosen**: [Option X]
- **Rationale**: [Why we chose this]
- **Documented In**: [Link to decision record if formal ADR created]

**Decision 2**: [What was decided]
- **Context**: [Why decision was needed]
- **Chosen**: [Approach]
- **Rationale**: [Reasoning]

---

## Context for Next Session

<!--
Critical information Claude/human needs to know to continue effectively.
-->

### Where to Start

1. **Read First**: [Link to relevant section in plan.md or tasks.md]
2. **Current Focus**: [What we're working on and why]
3. **Recent Changes**: [Quick summary of what changed since last session]

### Commands to Run (To Resume Work)

```bash
# Get project running locally
[command to start dev environment]

# Verify current state
[command to run tests]

# See current implementation
[command to view relevant files]
```

**Expected Output**: [What you should see if everything is working]

### Scope Reminder (For Claude)

**ONLY work on**:
- [Specific task from tasks.md]
- [Specific files or components]

**DO NOT** (out of scope this session):
- [ ] Don't refactor [unrelated code]
- [ ] Don't add features not in tasks.md
- [ ] Don't fix unrelated bugs (document in BUGS section of tasks.md)

---

## Questions for User

<!--
What needs clarification before proceeding?
-->

- [ ] **Q1**: [Question about approach or requirement]
  - **Context**: [Why this matters]
  - **Options**: [A or B?]

- [ ] **Q2**: [Technical decision needed]
  - **Tradeoffs**: [Option A: pros/cons vs Option B: pros/cons]

---

## Lessons Learned / Notes

<!--
Capture insights while they're fresh.
-->

- 💡 [Insight 1]: [What we discovered or learned]
- 💡 [Insight 2]: [Pattern that worked well]
- ⚠️ [Gotcha]: [Thing to watch out for]
- 📝 [Note]: [Important context for future work]

---

## Related Updates

<!--
Other documents updated this session.
-->

- [x] `tasks.md` - Updated tasks 2.3-2.5 status, added checkpoint results
- [x] `plan.md` - Updated architecture section with [change]
- [ ] `README.md` - Needs progress % update
- [ ] `integration-notes.md` - Document [new dependency]

---

## For Claude: Session-Specific Guidance

<!--
AI-specific reminders for this particular session.
-->

### This Session's Focus

**You are currently in**: [Phase X, Task Y]
**Goal for THIS session**: [Specific, bounded objective]

### Validation Before Continuing

Before marking task complete, verify:
```bash
# Run these exact commands
[test command 1]
[test command 2]
```

**All must pass** before proceeding to next task.

### Stop Points

**Stop and ask user if**:
- [ ] Any test fails
- [ ] Unexpected errors occur
- [ ] Implementation is taking significantly longer than estimated
- [ ] You discover missing requirements or ambiguities
- [ ] Current approach isn't working as planned

---

## Session Log (Historical)

<!--
Quick reference to previous sessions.
Keep last 3-5 sessions, archive older ones.
-->

### Session: YYYY-MM-DD
- **Worked on**: [Tasks]
- **Completed**: [Summary]
- **Key outcomes**: [What was achieved]
- **Archive**: [Link to detailed session notes if archived]

### Session: YYYY-MM-DD
- **Worked on**: [Tasks]
- **Completed**: [Summary]
- **Key outcomes**: [What was achieved]

*For older session notes, see [archive/](./archive/)*

---

**Last Updated**: YYYY-MM-DD HH:MM
**Updated By**: [Name or "Claude AI"]
**Next Update Expected**: YYYY-MM-DD (end of next session)
