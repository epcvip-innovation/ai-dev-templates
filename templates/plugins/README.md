# Claude Code Plugins

Reusable Claude Code skills for common development workflows.

---

## Taxonomy: Skills vs Commands vs Hooks vs Plugins

Claude Code has four extension mechanisms. They serve different purposes:

| Mechanism | What It Is | Trigger | Determinism | Best For |
|-----------|-----------|---------|-------------|----------|
| **Skills** | Markdown files teaching Claude workflows | Auto-triggered by natural language or `/skill-name` | Advisory (Claude follows, may drift) | Complex multi-step workflows |
| **Slash Commands** | Markdown prompt templates in `.claude/commands/` | Manual (`/command-name`) | Advisory | Repeatable prompts, team workflows |
| **Hooks** | Shell scripts at lifecycle events | Automatic (PreToolUse, PostToolUse, etc.) | **Deterministic** (exit codes enforce) | Validation, formatting, logging |
| **Plugins** | Packaged bundles of skills + hooks + references | Installed to `.claude/skills/` | Mixed (skills advisory, hooks deterministic) | Distributable workflow packages |

### When to Use What

- **Need to block an action?** Use a **hook** (exit code 2 = blocked, no exceptions)
- **Need a repeatable prompt?** Use a **slash command** (simple, explicit trigger)
- **Need Claude to learn a complex workflow?** Use a **skill** (multi-step, context-aware)
- **Need to distribute a workflow to a team?** Use a **plugin** (bundles everything together)

**Rationale**: Plugins combine skills + hooks into installable packages. For the "why plugins over standalone commands" decision, see [BUILTIN_VS_CUSTOM.md](../../docs/decisions/BUILTIN_VS_CUSTOM.md).

---

## Available Plugins

| Plugin | Agents | Purpose | Token Cost |
|--------|--------|---------|------------|
| [code-review](./code-review/) | 5 (full) / 3 (quick) | Unified review: agents + evaluation + root-cause | High / Medium |

**Note**: Backlog management skills have moved to [project-management/skills/](../project-management/skills/) as part of the unified project & task management templates.

---

## Quick Install

```bash
# Copy to global skills (available in all projects)
cp -r templates/plugins/code-review ~/.claude/skills/code-review
```

Or see [SKILL-INSTALLATION.md](./code-review/SKILL-INSTALLATION.md) for detailed options (global vs per-project, migration from old pipeline).

---

## Quick Usage

```bash
# Full review — 5 agents + evaluation + root-cause
/local-review

# Quick review — 3 agents, no root-cause
/local-review --quick

# Review staged changes only
/local-review --scope staged

# Show only critical issues
/local-review --min-score 80
```

---

## Plugin Structure

Each plugin follows this layout:

```
plugin-name/
├── SKILL.md              # Main skill definition (required)
│                         #   YAML frontmatter: name, description, trigger
│                         #   Markdown body: workflow steps, instructions
├── references/           # Supporting docs (optional)
│   ├── patterns.md       # Domain-specific patterns
│   └── prompts.md        # Agent/persona prompts
├── hooks/                # Deterministic enforcement (optional)
│   └── validate.py       # PreToolUse/PostToolUse scripts
└── scripts/              # Helper scripts (optional)
```

---

## Creating New Plugins

Start with the **[SKILL-TEMPLATE.md](./SKILL-TEMPLATE.md)** — it has the full annotated template, directory structure, description checklist, and testing guide.

### Quick steps

1. **Create directory**: `mkdir -p ~/.claude/skills/your-plugin`
2. **Copy template**: Use [SKILL-TEMPLATE.md](./SKILL-TEMPLATE.md) as your starting point
3. **Write the description** — this is the most critical field:

```yaml
---
name: your-plugin
description: |
  [Action + outcome]. Use when [context/file types/problems].
  Triggers on "/your-plugin", "[natural language phrase 1]",
  "[natural language phrase 2]".
---
```

4. **Add references/** (optional) — move content >50 lines to separate files for progressive disclosure
5. **Add hooks/** (optional) — for deterministic enforcement beyond advisory guidance
6. **Test** — try 5 trigger variations, check false positives, verify consistency

**Full examples**: [code-review/](./code-review/) (multi-agent review), [../project-management/skills/](../project-management/skills/) (backlog management)

---

## See Also

- [Hooks README](../hooks/README.md) — Deterministic workflow enforcement
- [Slash Commands](../slash-commands/) — Simple prompt templates
- [BUILTIN_VS_CUSTOM.md](../../docs/decisions/BUILTIN_VS_CUSTOM.md) — When to customize vs use built-in
- [ADVANCED-WORKFLOWS.md](../../docs/reference/ADVANCED-WORKFLOWS.md) — Agent patterns and model selection

---

**Last Updated**: 2026-02-15
