# Folder-Based Backlog System

An advanced backlog structure for projects with 10+ items that benefit from organization by type.

---

## When to Use This

| Criteria | Single-File | Folder-Based |
|----------|-------------|--------------|
| Backlog size | <10 items | 10+ items |
| Team size | Solo | Solo or team |
| Item complexity | Simple | Detailed plans |
| Automation | Manual | Python utilities |

**Use folder-based when:**
- You have many items across different types (features, bugs, tech-debt)
- You want auto-generated indexes
- You need dependency tracking (blocked_by)
- You want duplicate detection when adding items

---

## Structure

```
backlog/
├── _INDEX.md          # Auto-generated dashboard
├── _TEMPLATE.md       # Template for new items
├── _ARCHIVE.md        # Completed items log
├── feature/           # New functionality
│   └── {feature-name}/
│       └── plan.md
├── bug/               # Bug fixes
│   └── {bug-name}/
│       └── plan.md
├── tech-debt/         # Code quality
│   └── {item-name}/
│       └── plan.md
└── research/          # Investigation tasks
    └── {item-name}/
        └── plan.md
```

---

## YAML Frontmatter Schema

Each `plan.md` must have YAML frontmatter:

```yaml
---
id: feature-name                # Unique slug (matches folder name)
title: Human Readable Title      # Display title
type: feature                    # feature | bug | tech-debt | research
status: planned                  # planned | in_progress | blocked | complete
priority: P2                     # P0 | P1 | P2 | P3
effort_estimate: 4h              # Estimated effort
effort_actual: null              # Filled on completion
created: 2026-01-14
started: null
completed: null
blocked_by: []                   # IDs of blocking items
related: []                      # Related items (non-blocking)
tags: [ui, backend]              # For filtering
---
```

---

## Python Utilities

Copy `utils/` to `.claude/utils/` in your project.

### backlog_index.py

Generate `_INDEX.md` from all plan.md files:

```bash
# Preview markdown output
python3 .claude/utils/backlog_index.py

# Write to disk
python3 .claude/utils/backlog_index.py --write

# Output JSON (for skills)
python3 .claude/utils/backlog_index.py --json
```

### backlog_validate.py

Validate all items:

```bash
python3 .claude/utils/backlog_validate.py
```

Checks:
- Required frontmatter fields
- Valid field values (status, priority, type)
- ID matches folder name
- Circular dependencies in blocked_by
- Missing blocked_by references

### backlog_search.py

Search and duplicate detection:

```bash
# Search by query
python3 .claude/utils/backlog_search.py "search query"

# Filter by type
python3 .claude/utils/backlog_search.py --type feature "query"

# Check for duplicates before adding
python3 .claude/utils/backlog_search.py --check-duplicate "New Feature Title"
```

---

## Workflow Integration

### With Skills (Optional)

Backlog skills provide natural language triggers. See [../../skills/README.md](../skills/README.md) for details and honest notes about auto-trigger reliability.

### Manual Commands

```bash
# View dashboard
python3 .claude/utils/backlog_index.py

# Add new item
mkdir -p backlog/feature/my-feature
cp backlog/_TEMPLATE.md backlog/feature/my-feature/plan.md
# Edit plan.md

# Regenerate index
python3 .claude/utils/backlog_index.py --write

# Validate
python3 .claude/utils/backlog_validate.py
```

---

## Priority Guidelines

| Priority | Criteria | Response Time |
|----------|----------|---------------|
| **P0** | Blocking users, data loss, security | Immediate |
| **P1** | High value, core functionality | This week |
| **P2** | Nice-to-have, polish | When convenient |
| **P3** | Future ideas, optimization | Eventually |

---

## Migration from Single-File

If you have an existing `_BACKLOG.md`:

1. Create type directories: `mkdir -p backlog/{feature,bug,tech-debt,research}`
2. For each item:
   - Create folder: `mkdir backlog/feature/item-name`
   - Create plan.md with frontmatter
   - Move content from single file
3. Generate index: `python3 .claude/utils/backlog_index.py --write`
4. Validate: `python3 .claude/utils/backlog_validate.py`

---

## See Also

- [_TEMPLATE.md](./_TEMPLATE.md) - Full plan template
- [../README.md](../../README.md) - Project & Task Management overview
- [../../skills/README.md](../../skills/README.md) - Backlog management skills
