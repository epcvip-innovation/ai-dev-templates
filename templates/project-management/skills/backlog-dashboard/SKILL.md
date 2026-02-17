---
name: backlog-dashboard
description: |
  Shows current backlog status and recommends next item to work on.
  Use when the user wants to see their backlog, decide what to work on,
  or check project status. Triggers on "show backlog", "backlog status",
  "what should I work on", "next task", or "/backlog".
  Do NOT use for basic in-session task tracking — use native Tasks
  (TaskCreate/TaskList) for that. This skill is for persistent,
  cross-session backlogs with YAML frontmatter.
---

# Backlog Dashboard

Shows current backlog status and recommends what to work on next.

**Note**: For basic in-session task tracking, consider native Tasks (TaskCreate/TaskList) first. This skill adds value for persistent backlogs with effort tracking, priority tiers, and dependency management.

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

## Troubleshooting

**Problem**: `backlog_index.py` exits with "backlog/ not found"
**Cause**: Script looks for `backlog/` in the current directory or parent directories
**Solution**: Run from the project root, or ensure `backlog/` directory exists with type subdirectories

**Problem**: Dashboard shows 0 items but files exist
**Cause**: Items must be in `backlog/{type}/{name}/plan.md` with valid YAML frontmatter
**Solution**: Run `python3 .claude/utils/backlog_validate.py` to diagnose frontmatter issues

**Problem**: Skill doesn't auto-trigger
**Cause**: Skills auto-triggering can be inconsistent. The skill may not activate on every phrasing
**Solution**: Use `/backlog` explicitly, or invoke the skill directly from the skills list
