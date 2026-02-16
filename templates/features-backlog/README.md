# Backlog Templates

[← Back to Main README](../../README.md)

**Purpose**: Structure for managing feature ideas, bugs, and tech-debt with YAML frontmatter for tracking.

**Updated**: January 2026

---

## Choose Your Approach

| Approach | Best For | Setup Time |
|----------|----------|------------|
| **[Simple (Single-File)](#simple-single-file)** | <10 items, solo dev, getting started | 5 min |
| **[Folder-Based](#folder-based-advanced)** | 10+ items, dependency tracking, automation | 30 min |

---

## Simple (Single-File)

A single `_BACKLOG.md` file with feature directories.

### When to Use

- Starting out
- Small projects (<10 backlog items)
- No need for automation
- Solo development

### Quick Start

```bash
# Create backlog directory
mkdir -p your-project/backlog

# Copy templates
cp templates/features-backlog/_BACKLOG.md your-project/backlog/
cp templates/features-backlog/_TEMPLATE.md your-project/backlog/

# Start a feature
mkdir -p your-project/backlog/my-feature
cp your-project/backlog/_TEMPLATE.md your-project/backlog/my-feature/plan.md
```

### Structure

```
backlog/
├── _BACKLOG.md       # Main index (manual)
├── _TEMPLATE.md      # Template for new items
└── my-feature/
    └── plan.md       # Feature plan with YAML frontmatter
```

---

## Folder-Based (Advanced)

Organized by type (`feature/`, `bug/`, `tech-debt/`) with Python utilities for automation.

### When to Use

- 10+ backlog items
- Need dependency tracking (`blocked_by`)
- Want auto-generated indexes
- Want duplicate detection
- Team visibility required
- Effort calibration (estimate vs actual)

### Quick Start

```bash
# Create structure
mkdir -p your-project/backlog/{feature,bug,tech-debt,research}
mkdir -p your-project/.claude/utils

# Copy templates
cp -r templates/features-backlog/folder-based/* your-project/backlog/
cp templates/features-backlog/folder-based/utils/* your-project/.claude/utils/

# Create first item
mkdir your-project/backlog/feature/my-feature
cp your-project/backlog/_TEMPLATE.md your-project/backlog/feature/my-feature/plan.md

# Generate index
python3 your-project/.claude/utils/backlog_index.py --write
```

### Structure

```
backlog/
├── _INDEX.md          # Auto-generated (don't edit)
├── _TEMPLATE.md       # Template for new items
├── _ARCHIVE.md        # Completed items log
├── WORKFLOW.md        # Development workflow
├── feature/           # New functionality
│   └── my-feature/
│       └── plan.md
├── bug/               # Bug fixes
├── tech-debt/         # Code quality
└── research/          # Investigation
```

### Python Utilities

```bash
# Generate index from all plan.md files
python3 .claude/utils/backlog_index.py --write

# Validate all items
python3 .claude/utils/backlog_validate.py

# Search / check for duplicates
python3 .claude/utils/backlog_search.py "query"
python3 .claude/utils/backlog_search.py --check-duplicate "New Feature"
```

**Full documentation**: [folder-based/README.md](./folder-based/README.md)

---

## YAML Frontmatter

Both approaches use the same frontmatter schema:

```yaml
---
id: feature-name                # Unique slug (matches folder)
title: Human Readable Title
type: feature                   # feature | bug | tech-debt | research
status: planned                 # planned | in_progress | blocked | complete
priority: P2                    # P0 | P1 | P2 | P3
effort_estimate: 4h
effort_actual: null             # Fill on completion
created: 2026-01-14
started: null
completed: null
blocked_by: []                  # IDs of blocking items (folder-based)
related: []                     # Related items (folder-based)
tags: []
---
```

---

## Priority Guidelines

| Priority | Criteria | Response |
|----------|----------|----------|
| **P0** | Blocking users, security, data loss | Immediate |
| **P1** | High value, core functionality | This week |
| **P2** | Nice-to-have, improvements | When convenient |
| **P3** | Future ideas, optimization | Eventually |

---

## Integration with Claude Code

### Built-in Features

- **`/plan` mode** - Claude's built-in planning (good for simple cases)
- **TodoWrite tool** - In-session task tracking

### Custom Skills (folder-based)

If using folder-based, add the backlog management skills:

```bash
# Install skills
cp -r templates/plugins/backlog-management/* .claude/skills/
```

**Available skills:**

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `backlog-dashboard` | "show backlog", "/backlog" | View status, get recommendations |
| `add-backlog` | "add to backlog", "new feature" | Add items with duplicate detection |
| `backlog-complete` | "finished with X" | Archive with effort tracking |

**Full documentation:** [../plugins/backlog-management/README.md](../plugins/backlog-management/README.md)

---

## Workflow

### Simple Approach

```
Manual edit _BACKLOG.md → Create feature dir → Work → Update status
```

### Folder-Based Approach

```
/backlog → /backlog start [id] → Work → /push → /backlog complete [id]
```

**Full workflow**: [folder-based/WORKFLOW.md](./folder-based/WORKFLOW.md)

---

## Migration

### From Simple to Folder-Based

1. Create type directories: `mkdir -p backlog/{feature,bug,tech-debt,research}`
2. Move items: `mv backlog/my-feature backlog/feature/my-feature`
3. Add `type` and `blocked_by` to frontmatter
4. Copy Python utilities to `.claude/utils/`
5. Generate index: `python3 .claude/utils/backlog_index.py --write`

---

## Templates Included

| File | Purpose |
|------|---------|
| `_BACKLOG.md` | Simple: Main backlog index |
| `_TEMPLATE.md` | Simple: Feature plan template |
| `FEATURES_BACKLOG.md` | Tier-based backlog template (prioritized) |
| `folder-based/` | Advanced: Complete folder-based system |

---

## See Also

- [folder-based/README.md](./folder-based/README.md) - Advanced backlog system
- [folder-based/WORKFLOW.md](./folder-based/WORKFLOW.md) - Development workflow
- [../docs/decisions/BUILTIN_VS_CUSTOM.md](../../docs/decisions/BUILTIN_VS_CUSTOM.md) - When to use built-in vs custom

---

**Last Updated**: 2026-01-14
