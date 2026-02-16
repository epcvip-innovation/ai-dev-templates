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
| [code-review](./code-review/) | 5 | Full multi-agent adversarial review | High |
| [code-review-lite](./code-review/) | 3 | Security + Bugs + Production focus | Medium |

---

## Quick Install

```bash
# Copy to global skills (available in all projects)
cp -r templates/plugins/code-review ~/.claude/skills/local-code-review
```

Or see [SKILL-INSTALLATION.md](./code-review/SKILL-INSTALLATION.md) for detailed options (global vs per-project).

---

## Quick Usage

```bash
# Full 5-agent review
/local-review

# Lightweight 3-agent review
/local-review-lite

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

### 1. Create the directory

```bash
mkdir -p ~/.claude/skills/your-plugin
```

### 2. Write `SKILL.md`

```yaml
---
name: your-plugin
description: What it does. Also controls auto-triggering — Claude matches
  natural language against this description.
---

# Your Plugin Name

## When to Use
Describe when Claude should activate this skill.

## Workflow
1. Step one...
2. Step two...
3. Step three...

## Output Format
Describe expected output structure.
```

### 3. Add references (optional)

Put supporting context in `references/` — patterns, checklists, or domain knowledge that the skill needs but that would bloat the main SKILL.md.

### 4. Add hooks (optional)

If your plugin needs deterministic enforcement (not just advisory guidance), add hook scripts and document the settings.json configuration in your SKILL.md.

### 5. Test

```bash
# Trigger manually
/your-plugin

# Or test auto-triggering with natural language
"review my code for security issues"
```

**Full example**: See [code-review/](./code-review/) for a production plugin with 5 agents, severity scoring, and project-specific context.

---

## See Also

- [Hooks README](../hooks/README.md) — Deterministic workflow enforcement
- [Slash Commands](../slash-commands/) — Simple prompt templates
- [BUILTIN_VS_CUSTOM.md](../../docs/decisions/BUILTIN_VS_CUSTOM.md) — When to customize vs use built-in
- [ADVANCED-WORKFLOWS.md](../../docs/reference/ADVANCED-WORKFLOWS.md) — Agent patterns and model selection

---

**Last Updated**: 2026-02-15
