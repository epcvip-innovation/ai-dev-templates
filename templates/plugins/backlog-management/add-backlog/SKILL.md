---
name: add-backlog
description: Add new items to the backlog with duplicate detection. Triggers on "add to backlog", "new feature", "new bug", "feature request", "bug report", or "/add-backlog".
---

# Add to Backlog

Add new items to the backlog with duplicate detection and standardized formatting.

## Trigger Phrases

- "add to backlog", "add to backlog: [title]"
- "new feature", "new bug", "new tech debt"
- "feature request", "bug report"
- "/add-backlog", "/add-backlog [title]"

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
- Next: "Edit plan.md to add details, or start with `/backlog start {id}`"

## Example Interaction

```
User: add to backlog: dark mode support