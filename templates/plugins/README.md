# Claude Code Plugins

Reusable Claude Code skills for common development workflows.

## What Are Plugins?

Plugins are **Claude Code skills** - markdown files that teach Claude specialized workflows. They live in:
- `~/.claude/skills/` - Global (available in all projects)
- `.claude/skills/` - Per-project (project-specific)

## Available Plugins

| Plugin | Agents | Purpose | Token Cost |
|--------|--------|---------|------------|
| [code-review](./code-review/) | 5 | Full multi-agent adversarial review | High |
| [code-review-lite](./code-review/) | 3 | Security + Bugs + Production focus | Medium |

## Quick Install

```bash
# From this repo - copy to global skills
cp -r templates/plugins/code-review ~/.claude/skills/local-code-review
```

Or see [SKILL-INSTALLATION.md](./code-review/SKILL-INSTALLATION.md) for detailed options.

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

## Plugin Structure

Each plugin follows this structure:

```
plugin-name/
├── SKILL.md              # Main skill definition (required)
├── references/           # Supporting docs (optional)
│   ├── patterns.md       # Domain-specific patterns
│   └── prompts.md        # Agent/persona prompts
└── scripts/              # Helper scripts (optional)
```

## Creating New Plugins

1. Create a folder in `~/.claude/skills/your-plugin/`
2. Add `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: your-plugin
   description: What it does and when to trigger
   ---
   ```
3. Add workflow documentation in markdown
4. Optionally add `references/` for supporting content

See [code-review](./code-review/) for a complete example.
