# Backlog Management Skills

[← Back to Project Management](../README.md)

Natural language-triggered skills for managing folder-based backlogs.

**Updated**: February 2026

---

## Before You Install

**Do you need these?** Claude Code's built-in native Tasks (TaskCreate/TaskList/TaskGet/TaskUpdate) handle basic task tracking with zero setup. These skills add value only if you need:

- **Effort calibration** — estimate vs actual tracking that improves over time
- **Duplicate detection** — 85% similarity matching before adding items
- **Structured archival** — completed items logged to `_ARCHIVE.md` with metadata
- **Priority-sorted dashboards** — persistent, shareable backlog views

**Auto-trigger reliability**: Skills trigger on natural language, but activation can be inconsistent. For reliable invocation, use explicit commands (`/backlog`, `/add-backlog`, `/backlog complete`) rather than relying on phrases like "what should I work on next."

**Requires**: [Folder-based backlog system](../backlog/folder-based/README.md) with Python utilities installed.

---

## Available Skills

| Skill | Triggers | Unique Value |
|-------|----------|-------------|
| [backlog-dashboard](./backlog-dashboard/) | "/backlog", "show backlog" | Priority-sorted dashboard, next-item recommendations |
| [add-backlog](./add-backlog/) | "/add-backlog", "add to backlog" | Duplicate detection, standardized formatting |
| [backlog-complete](./backlog-complete/) | "/backlog complete", "finished with X" | Effort calibration, archival, unblocked item detection |

---

## Install

```bash
# Copy skills (global)
cp -r templates/project-management/skills/backlog-dashboard ~/.claude/skills/
cp -r templates/project-management/skills/add-backlog ~/.claude/skills/
cp -r templates/project-management/skills/backlog-complete ~/.claude/skills/

# Copy Python utilities (required)
mkdir -p .claude/utils
cp templates/project-management/backlog/folder-based/utils/* .claude/utils/
```

---

## Dependencies

| Utility | Purpose |
|---------|---------|
| `backlog_index.py` | Generate _INDEX.md, JSON output for skills |
| `backlog_validate.py` | Validate frontmatter |
| `backlog_search.py` | Search items, duplicate detection |

---

## See Also

- [../README.md](../README.md) — Project & Task Management overview (start here)
- [../backlog/folder-based/README.md](../backlog/folder-based/README.md) — Folder-based backlog system
- [../../skills/SKILL-TEMPLATE.md](../../skills/SKILL-TEMPLATE.md) — Creating new skills

---

**Last Updated**: 2026-02-16
