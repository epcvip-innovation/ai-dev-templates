# Development Workflow

Complete cycle for working with the folder-based backlog system.

---

## Quick Reference

```
/backlog → /backlog start [id] → [code] → /review-recent → /push → /backlog complete [id]
```

---

## Step 1: View Backlog

**Command:** `/backlog` or "show backlog"

**What it does:**
- Runs `python3 .claude/utils/backlog_index.py --json`
- Displays dashboard with status counts
- Recommends next item based on priority

**Output:**
```
## Backlog Status

**In Progress:** 1
- spectate-mode (P1, 2h remaining)

**Blocked:** 0

**Ready (P0-P1):** 2
- auth-fix (P0, 2h)
- dashboard-v2 (P1, 4h)

**Total Backlog:** 15 items

**Recommended:** Start work on `auth-fix` (P0, 2h)
```

---

## Step 2: Start Work

**Command:** `/backlog start [id]` or "start working on auth-fix"

**What it does:**
1. Validates item exists and is not blocked
2. Updates frontmatter: `status: in_progress`, `started: [date]`
3. Loads full context (acceptance criteria, technical notes, files to modify)
4. Regenerates `_INDEX.md`

**Blockers:**
- If item has `blocked_by`, skill asks if you want to work on blocker instead
- Can force start with `--force`

---

## Step 3: Implement

Work on the feature using standard development workflow:

1. Read acceptance criteria
2. Make changes to listed files
3. Run tests as you go
4. Check off acceptance criteria in plan.md

**Quality gates during implementation:**
- `/ai-review` - Quick code quality check
- `/audit` - Full audit before major commits

---

## Step 4: Pre-Commit Review

**Command:** `/review-recent` or `/push --dry-run`

**Checks:**
- Changed files identification
- TypeScript/linting errors
- Security scan (secrets, debug code)
- Pattern consistency

---

## Step 5: Push Changes

**Command:** `/push`

**What it does:**
1. Safety checks (secrets, large files, conflicts)
2. Quality checks (lint, format, typecheck)
3. Stages all changes
4. Generates conventional commit message
5. Pushes to remote
6. Reports summary

---

## Step 6: Complete Item

**Command:** `/backlog complete [id]` or "finished with auth-fix"

**What it does:**
1. Validates all acceptance criteria checked
2. Checks for uncommitted changes (warns if any)
3. Records actual effort: `effort_actual: [time]`
4. Updates: `status: complete`, `completed: [date]`
5. Appends summary to `_ARCHIVE.md`
6. Checks for newly unblocked items
7. Regenerates `_INDEX.md`
8. Recommends next item

**Output:**
```
Completed: auth-fix
- Effort: 2h estimated → 1.5h actual
- Unblocked: 2 items (dashboard-v2, profile-page)

Recommended: Start work on `dashboard-v2` (P1, 4h)
```

---

## Adding New Items

**Command:** `/add-backlog` or "add to backlog: new feature idea"

**Process:**
1. Checks for duplicates (>85% title similarity)
2. Gathers info: title, type, priority, effort estimate
3. Creates folder: `backlog/{type}/{kebab-case-id}/`
4. Populates `plan.md` from template
5. Regenerates `_INDEX.md`

---

## Maintenance Commands

| Command | Purpose |
|---------|---------|
| `python3 .claude/utils/backlog_index.py --write` | Regenerate _INDEX.md |
| `python3 .claude/utils/backlog_validate.py` | Validate all items |
| `python3 .claude/utils/backlog_search.py "query"` | Search items |

---

## Priority Guidelines

| Priority | Criteria | Expected Response |
|----------|----------|-------------------|
| **P0** | Blocking users, security, data loss | Work on immediately |
| **P1** | High value, core functionality | This week |
| **P2** | Nice-to-have, improvements | When convenient |
| **P3** | Future ideas, optimization | Eventually |

---

## Status Flow

```
planned → in_progress → complete
              ↓
           blocked → in_progress → complete
```

---

## Tips

1. **One in_progress at a time** - Focus on completing items
2. **Update as you go** - Check off acceptance criteria during work
3. **Record blockers** - If blocked, update status and `blocked_by`
4. **Effort calibration** - Compare estimate vs actual to improve future estimates
5. **Validate regularly** - Run `backlog_validate.py` after manual edits
