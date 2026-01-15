---
name: backlog-complete
description: Mark backlog items as complete with effort tracking. Triggers on "finished with", "done with", "completed", or "/backlog complete [id]".
---

# Complete Backlog Item

Mark items as complete, record actual effort, and archive.

## Trigger Phrases

- "finished with [id]", "done with [id]"
- "completed [id]", "mark [id] complete"
- "/backlog complete", "/backlog complete [id]"

## Process

### Step 1: Identify Item

If ID not provided, check for in-progress items:

```bash
python3 .claude/utils/backlog_index.py --json | grep "in_progress"
```

- If one in-progress: assume that one
- If multiple: ask user which one
- If none: error - nothing to complete

### Step 2: Pre-Completion Validation

**Check for uncommitted changes:**
```bash
git status --porcelain
```

If uncommitted changes exist:
- Warn user
- Suggest running `/push` first
- Ask to continue anyway or abort

**Check acceptance criteria:**
- Read plan.md
- Count checked vs unchecked criteria
- If unchecked items remain, warn user

### Step 3: Record Actual Effort

Ask user: "How long did this actually take?"

Options: `30m`, `1h`, `2h`, `4h`, `8h`, `16h+`

Compare to estimate:
- If significantly different, note for calibration
- "Estimated 4h, actual 2h - good estimate!"
- "Estimated 2h, actual 8h - consider breaking down similar tasks"

### Step 4: Update Frontmatter

Update plan.md:
```yaml
status: complete
completed: {today}
effort_actual: {actual}
```

### Step 5: Archive

Append summary to `_ARCHIVE.md`:

```markdown
## {date} - {title}

- **ID**: {id}
- **Type**: {type}
- **Effort**: {estimate} estimated → {actual} actual
- **Summary**: {brief description of what was done}
```

### Step 6: Check for Unblocked Items

```bash
python3 .claude/utils/backlog_search.py --json | grep "blocked_by.*{id}"
```

If items were blocked by this one:
- List newly unblocked items
- Suggest starting one of them

### Step 7: Regenerate Index

```bash
python3 .claude/utils/backlog_index.py --write
```

### Step 8: Recommend Next

Show backlog dashboard with recommendation:
- "Completed: {title}"
- "Unblocked: {count} items"
- "Recommended next: {top P0-P1 item}"

## Example Output

```markdown
Completed: `auth-feature` - User Authentication Flow

**Effort calibration:**
- Estimated: 4h
- Actual: 3h
- Accuracy: Good (+/- 25%)

**Unblocked:** 2 items
- `protected-routes` (P1, 2h)
- `user-profile` (P2, 4h)

**Archived to:** backlog/_ARCHIVE.md

---

**Recommended next:** `protected-routes` (P1, 2h)
- Depends on auth (just completed)
- High priority

Start with `/backlog start protected-routes`?
```

## Notes

- Always regenerate index after completion
- Archive provides historical record and effort calibration data
- Unblocked check prevents forgotten dependencies
