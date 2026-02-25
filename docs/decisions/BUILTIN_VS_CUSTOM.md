# When to Use Built-in vs Custom

Decision guide for choosing between Claude Code's built-in features and custom templates.

**Updated:** February 2026 (Claude Code v2.1.x)

---

## Quick Decision Matrix

| Task | Built-in | Custom | Recommendation |
|------|----------|--------|----------------|
| Feature planning | `/plan` mode | `/start-feature` | Built-in (plan files are persistent) |
| Session continuity | Session Memory (v2.1.30+) | HANDOFF.md in `.projects/` | Built-in for simple, custom for multi-day |
| Task tracking | Native Tasks (TaskCreate/TaskList) | Custom backlog | Built-in for simple, custom for effort tracking |
| Code review | `/local-review` skill | Custom review plugin | Custom (for project-specific patterns) |
| Commits | Built-in git tools | `/push` command | Custom (for quality gates) |
| Feature workflow | `/feature-dev:feature-dev` | Custom skills | Built-in + augment |

---

## Claude Code Built-in Features (v2.1.x)

### Plan Mode

**What it does:**
- Creates `.claude/plans/` directory with plan files
- Persistent across sessions
- Structured planning workflow

**When to use built-in:**
- One-off features
- Exploration/prototyping
- No backlog integration needed

**When to use custom:**
- Need backlog integration
- Want effort tracking
- Team visibility required

### Session Memory

**What it does:**
- Automatically summarizes conversation when context fills (auto-compact)
- Session Memory (v2.1.30+, Feb 2026) provides automatic cross-session context
- Preserves important context across conversations

**When to use built-in:**
- Most cases (significantly improved in 2025-2026)
- Solo development

**When to use custom (HANDOFF.md):**
- Multi-day complex features with specific scope boundaries
- Team handoffs where another person picks up the work
- Audit trail required

### Native Tasks

**What it does:**
- Persistent task tracking via TaskCreate, TaskList, TaskGet, TaskUpdate
- DAG dependency tracking with addBlockedBy/addBlocks
- Filesystem persistence (`~/.claude/tasks/`)
- Status workflow: pending → in_progress → completed
- Metadata fields for custom data

**When to use built-in:**
- In-session and short-term task tracking
- <10 items, no effort tracking needed
- Zero setup required

**When to use custom (backlog system):**
- Cross-session tracking with version-controlled history
- 10+ items with type categorization
- Effort calibration (estimate vs actual)
- Duplicate detection
- Team-visible dashboards

### Native Tasks vs Custom Backlog

| Capability | Native Tasks | Custom Backlog |
|------------|-------------|----------------|
| Setup cost | Zero | 30 minutes |
| Reliability | High (built-in) | Medium (skills may not auto-trigger) |
| Persistence | `~/.claude/tasks/` | Git-tracked YAML files |
| Dependencies | DAG (addBlockedBy) | `blocked_by: []` in frontmatter |
| Effort tracking | Not built-in | Estimate vs actual with calibration |
| Type categorization | Not built-in | feature/bug/tech-debt/research |
| Duplicate detection | Not built-in | 85% similarity via Python utility |
| Shareable dashboard | Text only (TaskList) | _INDEX.md (auto-generated, committed) |
| Priority tiers | Metadata (unstructured) | P0-P3 with documented criteria |

### `/feature-dev:feature-dev` Plugin

**What it does:**
- Guided feature development
- Codebase understanding
- Architecture focus

**When to use built-in:**
- General development
- New codebases
- Standard patterns

**When to use custom:**
- Project-specific workflows
- Non-standard architecture
- Domain-specific patterns

---

## When to Use Built-in

### Checklist

- [ ] Task is generic (planning, committing, reviewing)
- [ ] No project-specific requirements
- [ ] Testing a workflow
- [ ] Solo development
- [ ] Short-term (single session)

### Examples

| Scenario | Use Built-in |
|----------|-------------|
| "Plan this feature" | `/plan` mode |
| "Review my changes" | `/local-review` (if installed) |
| "What should I work on?" | Native Tasks (TaskList) |
| "Continue from yesterday" | Session Memory handles it |

---

## When to Use Custom

### Checklist

- [ ] Need project-specific quality gates
- [ ] Integrating with backlog system
- [ ] Team has specific conventions
- [ ] Need audit trail
- [ ] Cross-session persistence required
- [ ] Effort tracking needed

### Examples

| Scenario | Use Custom |
|----------|-----------|
| "Review with our patterns" | Custom code-review plugin with review-context.md |
| "Track our backlog" | Folder-based backlog with Python utilities |
| "Push with quality checks" | `/push` command with project-specific gates |
| "Add to our backlog" | `/add-backlog` skill with duplicate detection |

---

## Hierarchy of Customization

### Level 1: Use Built-in (Zero Setup)

```
Claude Code defaults → Works immediately
```

**Effort:** 0 minutes
**Customization:** None
**Best for:** Getting started, simple projects

### Level 2: Configure Built-in (Minimal Setup)

```
.claude/settings.json → Permissions, MCP servers
CLAUDE.md → Project context
```

**Effort:** 30 minutes
**Customization:** Permissions, context
**Best for:** Most projects

### Level 3: Add Custom Skills (Light to Moderate Setup)

```
.claude/commands/*.md → Flat-file skills (simple prompts, explicit /name invocation)
.claude/skills/*/SKILL.md → Directory skills (complex workflows with references/scripts)
.claude/utils/*.py → Enforcement utilities
```

**Effort:** 1-8 hours (flat-file: 1-2h, directory skills: 4-8h)
**Customization:** Workflows
**Best for:** Repeatable workflows like `/push`, `/audit` (flat-file) or complex multi-step workflows (directory)

**Note**: Use `disable-model-invocation: true` in directory skill frontmatter to prevent auto-triggering — the skill will only run when explicitly invoked via `/name`.

### Level 4: Full Custom Workflow (Heavy Setup)

```
Complete backlog system
Multiple skills with hooks
Python enforcement utilities
CI/CD integration
```

**Effort:** 16+ hours
**Customization:** Complete
**Best for:** Long-term projects, enterprise

---

## Skill Formats: Directory vs Flat-File

Skills and commands are unified — both produce `/name` and work the same way. Choose the format based on complexity:

| Feature | Flat-File (`.claude/commands/`) | Directory (`.claude/skills/name/`) |
|---------|-------------------------------|-----------------------------------|
| File structure | Single `.md` file | `SKILL.md` + optional `references/`, `scripts/` |
| Invocation | `/name` or natural language | `/name` or natural language |
| Supporting files | No | Yes (`references/`, `scripts/`, `assets/`) |
| `disable-model-invocation` | No | Yes (prevent auto-triggering) |
| Hooks frontmatter | No | Yes (skill-scoped hooks) |
| Best for | Simple prompts (`/push`, `/audit`) | Complex workflows (code-review, backlog) |

### Why Python Utilities Still Matter

Python utilities are valuable for:
- **Data operations** - Backlog indexing, validation, search
- **Enforcement** - Can't be ignored like markdown instructions
- **Reliability** - Consistent behavior every time

**Best combination:** Skills call Python utilities for data operations.

```
Skill (workflow) → Python utility (data) → Reliable output
```

---

## Migration Path

### From Custom to Built-in

If you have custom workflows that are now superseded:

1. **Test built-in first** - Try the native feature
2. **Compare results** - Is built-in good enough?
3. **Deprecate if equivalent** - Move custom to `_deprecated/`
4. **Keep if superior** - Custom adds value built-in lacks

### From Built-in to Custom

When built-in isn't enough:

1. **Start with built-in** - Use until you hit limits
2. **Identify gaps** - What's missing?
3. **Add incrementally** - Custom command → skill → full system
4. **Combine** - Built-in + custom augmentation

---

## Recommendations Summary

1. **Start with built-in** → Add custom only when needed
2. **Directory skills for complex workflows, flat-file skills for utilities** — each has strengths
3. **Python utilities for data operations** (backlog indexing, validation, search)
4. **Combine approaches** - Skills call Python utilities for best of both
5. **Review quarterly** - Built-in features improve; reassess custom value

---

## See Also

- [../../templates/slash-commands/README.md](../../templates/slash-commands/README.md) - Flat-file skill templates
- [../../templates/skills/](../../templates/skills/README.md) - Skill templates
- [../../templates/project-management/](../../templates/project-management/README.md) - Project & task management
