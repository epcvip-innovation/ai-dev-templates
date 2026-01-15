---
name: backlog-dashboard
description: Shows current backlog status and recommends next item to work on. Triggers on "what's in backlog", "show backlog", "backlog status", "what should I work on", "next task", or "/backlog".
---

# Backlog Dashboard

Shows current backlog status and recommends what to work on next.

## Trigger Phrases

- "what's in backlog", "show backlog", "backlog status"
- "what should I work on", "next task", "what's next"
- "/backlog"

## Process

### Step 1: Get Current State

Run the index utility to get structured data:

```bash
python3 .claude/utils/backlog_index.py --json
```

### Step 2: Display Summary

Format the output as a dashboard:

```markdown
## Backlog Status

**In Progress:** {count}
{list each with title, priority, and effort remaining}

**Blocked:** {count}
{list each with blocker}

**Ready (P0-P1):** {count}
{list top 3 by priority}

**Total Backlog:** {count}
```

### Step 3: Recommend Next Item

**If nothing in progress:**
- Recommend top item from Ready (P0-P1) queue
- Show its acceptance criteria summary
- Ask if user wants to start it

**If something in progress:**
- Show current work with progress
- Ask if user wants to continue or switch

## Example Output

```markdown
## Backlog Status

**In Progress:** 1
- `auth-feature` (P1, ~2h remaining) - User Authentication Flow

**Blocked:** 0

**Ready (P0-P1):** 2
- `security-fix` (P0, 2h) - Fix XSS vulnerability
- `dashboard-v2` (P1, 4h) - Dashboard redesign

**Total Backlog:** 15 items

---

**Recommended:** Continue work on `auth-feature`

Current acceptance criteria:
- [x] Login endpoint working
- [x] JWT token generation
- [ ] Logout endpoint
- [ ] Session middleware

Would you like to continue, or pick a different item?
```

## Integration

This skill is the entry point for the backlog workflow:

```
/backlog → /backlog start [id] → [work] → /push → /backlog complete [id]
```

## Notes

- Always run the Python utility for accurate data (don't parse files manually)
- If utility fails, suggest running `backlog_validate.py` to check for issues
- Link to plan.md files so user can easily open them
