# Backlog Management Skills

Skills for managing folder-based backlogs with natural language triggers.

**Requires:** [Folder-based backlog system](../../features-backlog/folder-based/README.md) with Python utilities.

---

## Quick Install

```bash
# Copy skills to your project
cp -r templates/plugins/backlog-management/* ~/.claude/skills/
# OR for project-specific:
cp -r templates/plugins/backlog-management/* .claude/skills/

# Copy Python utilities (required)
cp templates/features-backlog/folder-based/utils/* .claude/utils/
```

---

## Available Skills

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `backlog-dashboard` | "show backlog", "/backlog" | View status, get recommendations |
| `add-backlog` | "add to backlog", "new feature" | Add items with duplicate detection |
| `backlog-complete` | "finished with X", "done with X" | Archive with effort tracking |

---

## Usage Examples

```
"show backlog"
→ Displays dashboard with in-progress, blocked, ready items

"add to backlog: user authentication"
→ Checks for duplicates, gathers info, creates plan.md

"finished with auth-feature"
→ Records effort, archives to _ARCHIVE.md, suggests next item
```

---

## Workflow Integration

```
/backlog → /backlog start [id] → [code] → /push → /backlog complete [id]
```

1. **`/backlog`** (backlog-dashboard) - See what's available, pick next task
2. **Start work** - Load context, mark in_progress
3. **Code** - Implement the feature
4. **`/push`** - Safe commit with quality checks
5. **`/backlog complete`** - Archive, record effort, get next recommendation

---

## Dependencies

These skills require Python utilities in `.claude/utils/`:

| Utility | Purpose |
|---------|---------|
| `backlog_index.py` | Generate _INDEX.md, JSON output for skills |
| `backlog_validate.py` | Validate frontmatter |
| `backlog_search.py` | Search items, duplicate detection |

---

## Customization

Each skill's `SKILL.md` can be customized:

- **Trigger phrases** - Add project-specific triggers
- **Output format** - Adjust dashboard layout
- **Validation rules** - Add project-specific checks

---

## See Also

- [../../features-backlog/README.md](../../features-backlog/README.md) - Backlog system overview
- [../../features-backlog/folder-based/WORKFLOW.md](../../features-backlog/folder-based/WORKFLOW.md) - Full workflow
- [../../slash-commands/ai-dev-workflow/commands/push.md](../../slash-commands/ai-dev-workflow/commands/push.md) - Push command
