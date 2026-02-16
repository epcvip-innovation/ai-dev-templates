---
name: add-backlog
description: |
  Add new items to the backlog with duplicate detection and standardized
  formatting. Use when the user wants to add a feature, bug, or tech-debt
  item to the project backlog. Triggers on "add to backlog", "new feature",
  "new bug", "feature request", "bug report", or "/add-backlog".
  Do NOT use for quick in-session tasks — use native Tasks (TaskCreate)
  for that.
---

# Add to Backlog

Add new items to the backlog with duplicate detection and standardized formatting.

**Note**: For quick in-session task tracking, use native Tasks (TaskCreate) instead. This skill is for persistent backlog items with effort estimates, type categorization, and duplicate detection.

## Process

### Step 1: Check for Duplicates

Run duplicate detection with 85% similarity threshold:

```bash
python3 .claude/utils/backlog_search.py --check-duplicate "Proposed Title"
```

**If duplicates found (>85% similarity):**
- Show similar items with similarity scores
- Ask user to confirm this is truly new
- Suggest updating existing item instead

**If no duplicates:**
- Continue to Step 2

### Step 2: Gather Information

Ask user for (if not provided):

| Field | Required | Default |
|-------|----------|---------|
| Title | Yes | - |
| Type | Yes | `feature` |
| Priority | Yes | `P2` |
| Effort estimate | Yes | - |
| Description | No | - |

**Type options:** `feature`, `bug`, `tech-debt`, `research`

**Priority guidance:**
- P0: Blocking users, security, data loss
- P1: High value, this week
- P2: Nice to have, when convenient
- P3: Future ideas

**Effort options:** `30m`, `1h`, `2h`, `4h`, `8h`, `16h+`

### Step 3: Create Item

1. Generate kebab-case ID from title:
   ```
   "User Authentication Flow" → "user-authentication-flow"
   ```

2. Create folder structure:
   ```bash
   mkdir -p backlog/{type}/{id}
   ```

3. Create plan.md from template with YAML frontmatter:
   ```yaml
   ---
   id: {id}
   title: {title}
   type: {type}
   status: planned
   priority: {priority}
   effort_estimate: {effort}
   effort_actual: null
   created: {today}
   started: null
   completed: null
   blocked_by: []
   related: []
   tags: []
   ---

   # {title}

   ## Problem
   {description or "TODO: Describe the problem"}

   ## Solution
   TODO: Describe the approach

   ## Acceptance Criteria
   - [ ] Criterion 1
   - [ ] Criterion 2
   ```

### Step 4: Regenerate Index

```bash
python3 .claude/utils/backlog_index.py --write
```

### Step 5: Confirm

Report to user:
- Created: `backlog/{type}/{id}/plan.md`
- Priority: {priority}
- Effort: {effort}
- Next: "Edit plan.md to add details, or start working on it"

## Troubleshooting

**Problem**: `backlog_search.py` fails with import error
**Cause**: Script requires Python 3.6+ with standard library only
**Solution**: Verify `python3 --version` is 3.6+. The utilities have no pip dependencies.

**Problem**: Duplicate detection too sensitive / not sensitive enough
**Cause**: 85% similarity threshold may not suit all projects
**Solution**: Edit the threshold in `backlog_search.py` (search for `SIMILARITY_THRESHOLD`)

**Problem**: Skill doesn't auto-trigger on "new feature" phrases
**Cause**: Broad trigger phrases like "new feature" may conflict with other skills or not activate consistently
**Solution**: Use "/add-backlog" explicitly for reliable invocation
