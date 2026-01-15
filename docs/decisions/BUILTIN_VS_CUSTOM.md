# When to Use Built-in vs Custom

Decision guide for choosing between Claude Code's built-in features and custom templates.

**Updated:** January 2026 (Claude Code v2.1.x)

---

## Quick Decision Matrix

| Task | Built-in | Custom | Recommendation |
|------|----------|--------|----------------|
| Feature planning | `/plan` mode | `/start-feature` | Built-in (plan files are persistent) |
| Session continuity | Auto-compact | `/session-handoff` | Built-in (auto-compact improved significantly) |
| Task tracking | TodoWrite tool | Custom backlog | Built-in for simple, Custom for complex |
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

### Session Memory (Auto-Compact)

**What it does:**
- Automatically summarizes conversation when context fills
- Preserves important context
- Session teleportation (resume anywhere)

**When to use built-in:**
- Most cases (significantly improved in 2025-2026)
- Solo development

**When to use custom (`/session-handoff`):**
- Multi-day complex features
- Team handoffs
- Audit trail required

### TodoWrite Tool

**What it does:**
- In-conversation task tracking
- Progress visualization
- Automatic status updates

**When to use built-in:**
- Session-scoped tasks
- <10 items
- No persistence needed

**When to use custom (backlog system):**
- Cross-session tracking
- 10+ items
- Dependency management
- Effort calibration

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
| "What should I work on?" | TodoWrite |
| "Continue from yesterday" | Auto-compact handles it |

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

### Level 3: Add Custom Commands (Light Setup)

```
.claude/commands/*.md → Slash commands
```

**Effort:** 1-2 hours
**Customization:** Workflows
**Best for:** Repeatable workflows like `/push`, `/audit`

### Level 4: Add Custom Skills (Moderate Setup)

```
.claude/skills/*/SKILL.md → Auto-triggered skills
.claude/utils/*.py → Enforcement utilities
```

**Effort:** 4-8 hours
**Customization:** Full workflow automation
**Best for:** Complex projects, teams

### Level 5: Full Custom Workflow (Heavy Setup)

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

## Key Insight: Plugins > Slash Commands

Based on real-world usage (fwaptile-wordle project):

### Why Plugins Win

| Feature | Slash Commands | Plugins |
|---------|---------------|---------|
| Trigger | Manual (`/command`) | Auto (natural language) |
| Sub-tasks | Can be skipped | Can't be ignored |
| Hooks | No | Yes (PreToolUse, PostToolUse, Stop) |
| Context | Limited | Full skill context |
| Enforcement | Suggestions | Programmatic |

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
2. **Plugins > slash commands** (auto-trigger, hooks, sub-tasks can't be ignored)
3. **Python utilities for data operations** (backlog indexing, validation, search)
4. **Combine approaches** - Skills call Python utilities for best of both
5. **Review quarterly** - Built-in features improve; reassess custom value

---

## See Also

- [../slash-commands/README.md](../../templates/slash-commands/README.md) - Command templates
- [../plugins/](../../templates/plugins/) - Skill templates
- [../features-backlog/folder-based/](../../templates/features-backlog/folder-based/) - Backlog system
- [RELIABLE_SOURCES.md](../../templates/resources/RELIABLE_SOURCES.md) - Where to track updates
