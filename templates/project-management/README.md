# Project & Task Management

[← Back to Main README](../../README.md)

Templates for managing tasks, backlogs, and multi-session projects with Claude Code.

**Updated**: February 2026

---

## Choose Your Approach

| Situation | Approach | Setup | Location |
|-----------|----------|-------|----------|
| Single session, simple tasks | **Native Tasks** (built-in) | Zero | n/a |
| Multi-session, 1-2 week feature | **[.projects/ pattern](#pattern-1-projects-cross-session-context)** | 5 min | `.projects/[name]/` |
| Ongoing backlog, <10 items | **[Single-file backlog](#pattern-2-single-file-backlog)** | 5 min | `backlog/_BACKLOG.md` |
| Large project, 10+ items | **[Folder-based backlog](#pattern-3-folder-based-backlog)** | 30 min | `backlog/{type}/{name}/` |
| Full automation (experimental) | **[Backlog skills](#pattern-4-backlog-skills-experimental)** | 30 min | `.claude/skills/` |

**Start simple. Upgrade when you hit limits.** Most projects only need native Tasks + `.projects/`.

---

## Built-In: Native Tasks (Zero Setup)

Claude Code includes persistent task tracking since v2.1 (January 2025):

| Tool | Purpose |
|------|---------|
| `TaskCreate` | Add tasks with subject, description, status |
| `TaskList` | View all tasks with status and dependencies |
| `TaskGet` | Read full task details |
| `TaskUpdate` | Change status, add dependencies (addBlockedBy/addBlocks) |

**Strengths**: Zero setup, DAG dependency tracking, filesystem persistence (`~/.claude/tasks/`), reliable (built-in, always works).

**Limitations**: No effort tracking, no type categorization, no duplicate detection, text-only output, no cross-session context transfer.

**When to upgrade**: When you need effort calibration, structured YAML metadata, cross-session handoffs, or a team-visible backlog.

See [BUILTIN_VS_CUSTOM.md](../../docs/decisions/BUILTIN_VS_CUSTOM.md) for a detailed comparison.

---

## Pattern 1: .projects/ (Cross-Session Context)

**Problem solved**: AI has limited context windows. Complex multi-session work needs structured handoff files so Claude can resume effectively.

**When to use**: Features spanning 1-2+ weeks, 5+ files, multiple sessions.

### Quick Start

```bash
cp -r templates/project-management/projects/_TEMPLATE .projects/[feature-name]
```

### Essential Files

```
.projects/[feature-name]/
├── README.md      # Navigation hub — where to start
├── plan.md        # Main specification — WHY + WHAT + HOW
├── tasks.md       # Task breakdown — granular implementation steps
└── HANDOFF.md     # Session continuity — current state + what's next
```

**Key insight**: HANDOFF.md is critical. Update it at the end of every session with what was accomplished, what's next, and any blockers. This is what makes AI resumption work.

**Full documentation**: [projects/README.md](./projects/README.md)

---

## Pattern 2: Single-File Backlog

A lightweight `_BACKLOG.md` with priority sections and optional feature directories.

**When to use**: Ongoing backlog with <10 items, solo development, getting started.

### Quick Start

```bash
mkdir -p backlog
cp templates/project-management/backlog/_BACKLOG.md backlog/
cp templates/project-management/backlog/_TEMPLATE.md backlog/
```

### Structure

```
backlog/
├── _BACKLOG.md       # Main index (manual)
├── _TEMPLATE.md      # Template for new items
└── my-feature/
    └── plan.md       # Feature plan with YAML frontmatter
```

### Priority Levels

| Priority | Criteria | Response |
|----------|----------|----------|
| **P0** | Blocking users, security, data loss | Immediate |
| **P1** | High value, core functionality | This week |
| **P2** | Nice-to-have, improvements | When convenient |
| **P3** | Future ideas, optimization | Eventually |

---

## Pattern 3: Folder-Based Backlog

Organized by type with Python utilities for automation.

**When to use**: 10+ backlog items, need dependency tracking, want auto-generated indexes and duplicate detection.

### Quick Start

```bash
mkdir -p backlog/{feature,bug,tech-debt,research}
mkdir -p .claude/utils
cp -r templates/project-management/backlog/folder-based/* backlog/
cp templates/project-management/backlog/folder-based/utils/* .claude/utils/
```

### Structure

```
backlog/
├── _INDEX.md          # Auto-generated (don't edit)
├── _TEMPLATE.md       # Template for new items
├── feature/           # New functionality
│   └── my-feature/
│       └── plan.md
├── bug/               # Bug fixes
├── tech-debt/         # Code quality
└── research/          # Investigation
```

### Python Utilities

```bash
python3 .claude/utils/backlog_index.py --write     # Generate _INDEX.md
python3 .claude/utils/backlog_validate.py           # Validate all items
python3 .claude/utils/backlog_search.py "query"     # Search items
python3 .claude/utils/backlog_search.py --check-duplicate "Title"  # Duplicate detection
```

**Full documentation**: [backlog/folder-based/README.md](./backlog/folder-based/README.md)

---

## Pattern 4: Backlog Skills (Experimental)

Natural language-triggered skills for backlog management. Built on the folder-based system.

**Honest note**: Skills auto-trigger reliability varies. Native Tasks (TaskCreate/TaskList) are more reliable for basic tracking. These skills add value for **effort calibration**, **duplicate detection**, and **structured archival** — but you should test them in your workflow before relying on them.

| Skill | Triggers | What It Adds Over Built-in |
|-------|----------|---------------------------|
| `backlog-dashboard` | "show backlog", "/backlog" | Priority-sorted dashboard, next-item recommendations |
| `add-backlog` | "add to backlog" | Duplicate detection (85% similarity), auto-formatting |
| `backlog-complete` | "finished with X" | Effort calibration (estimate vs actual), archival |

### Install

```bash
# Copy skills
cp -r templates/project-management/skills/* ~/.claude/skills/
# Copy Python utilities (required)
cp templates/project-management/backlog/folder-based/utils/* .claude/utils/
```

**Full documentation**: [skills/README.md](./skills/README.md)

---

## YAML Frontmatter Schema

Both single-file and folder-based approaches use the same schema in `plan.md` files:

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

## Migration Paths

### Native Tasks → Single-File Backlog

When in-session tracking isn't enough:
1. Create `backlog/_BACKLOG.md`
2. Transfer persistent items from TaskList
3. Add YAML frontmatter for effort tracking

### Single-File → Folder-Based

When items exceed ~10:
1. Create type directories: `mkdir -p backlog/{feature,bug,tech-debt,research}`
2. Move items: `mv backlog/my-feature backlog/feature/my-feature`
3. Add `type` and `blocked_by` to frontmatter
4. Copy Python utilities, generate index

---

## Integration with Skills

| Skill | Purpose |
|---------|---------|
| `/start-feature` | Creates `.projects/[name]/` structure for complex features |
| `/resume-feature` | Checks `.projects/`, `backlog/` for HANDOFF.md |
| `/feature-complete` | Archives to `.projects/archive/[name]/` |

---

## See Also

- [BUILTIN_VS_CUSTOM.md](../../docs/decisions/BUILTIN_VS_CUSTOM.md) — When to use built-in vs custom
- [projects/README.md](./projects/README.md) — .projects/ pattern details
- [backlog/folder-based/README.md](./backlog/folder-based/README.md) — Advanced backlog system
- [skills/README.md](./skills/README.md) — Backlog management skills

---

**Last Updated**: 2026-02-15
