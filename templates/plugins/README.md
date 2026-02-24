# Claude Code Plugins

[← Back to Main README](../../README.md)

Distributable bundles of commands, agents, hooks, and references — the packaging layer on top of skills.

---

## When to Use a Plugin vs a Skill

| Question | Answer → Use |
|----------|-------------|
| Single workflow, one SKILL.md file? | **Skill** |
| Multiple agents working together? | **Plugin** |
| Need to distribute to a team? | **Plugin** |
| Need hooks bundled with the workflow? | **Plugin** |
| Requires MCP server configuration? | **Plugin** |
| One person, one repo? | **Skill** (simpler) |

**Rule of thumb**: If you need more than one agent or want to share the workflow beyond your machine, make it a plugin. If it's a single guided workflow, make it a skill.

---

## Plugin Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json              # Required — manifest (name, version, description)
├── README.md                    # Human docs (not loaded into context)
├── commands/                    # Slash commands (entry points)
│   └── do-thing.md              #   Frontmatter: description, argument-hint, allowed-tools
├── agents/                      # Specialized agents (launched by commands)
│   ├── fast-checker.md          #   Frontmatter: name, description, model
│   └── deep-analyzer.md         #   Each agent runs in isolated context
├── hooks/                       # Optional — lifecycle hooks
│   └── pre-commit.sh            #   Shell scripts at PreToolUse, PostToolUse, etc.
└── references/                  # Optional — supporting docs loaded on demand
    └── patterns.md              #   Domain knowledge, checklists, examples
```

**Commands** are entry points — users invoke them via `/plugin-name:command-name`. Commands orchestrate agents.

**Agents** are workers — commands launch them via the Task tool. Each agent runs in isolated context with its own model and tools.

---

## Manifest Reference (plugin.json)

```json
{
  "name": "plugin-name",
  "description": "What this plugin does — shown in /plugin list",
  "author": {
    "name": "Your Name or Team",
    "email": "team@example.com"
  },
  "version": "1.0.0"
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Lowercase, hyphens only. Must match directory name. |
| `description` | Yes | One line. Shown in `/plugin list` and marketplace. |
| `author.name` | No | Person or team who maintains the plugin. |
| `version` | No | Semver. Helps teams track updates. |
| `mcpServers` | No | MCP server configs bundled with the plugin. |

---

## Agent Frontmatter

```yaml
---
name: agent-name
description: Use this agent to [action]. Launch when [context]. Pass it [what to include in the prompt].
model: haiku
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | How the agent appears in Task tool (`plugin:agent-name`) |
| `description` | Yes | Tells Claude when and how to launch this agent |
| `model` | No | `haiku` (fast/cheap), `sonnet` (balanced), `opus` (deep reasoning) |

**Model selection**: Use the cheapest model that produces reliable results. Pattern-matching tasks (link checking, linting) → haiku. Judgment calls (quality assessment, conflict detection) → sonnet. Complex multi-step reasoning → opus.

---

## Command Frontmatter

```yaml
---
description: "What this command does — shown in autocomplete"
argument-hint: "[file-or-directory] [--flag]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Edit", "Task"]
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `description` | Yes | Shown when user types `/plugin-name:` |
| `argument-hint` | No | Autocomplete hint for arguments |
| `allowed-tools` | No | Tools auto-approved when command runs. Always include `Task` if orchestrating agents. |

---

## Available Plugins

| Plugin | Agents | Purpose |
|--------|--------|---------|
| [doc-review](./doc-review/) | 4 (link-checker, content-quality, ai-pattern-detector, cross-file-analyzer) | Multi-agent documentation review |

---

## Installing Plugins

**Local marketplace** (one-time setup):
```bash
mkdir -p ~/.claude/marketplaces/local/.claude-plugin
# Create marketplace.json — see "Distributing Plugins" below for the format
# Then: copy plugin dirs into ~/.claude/marketplaces/local/
```

**Register and install**:
```bash
# In Claude Code:
/plugin marketplace add ~/.claude/marketplaces/local   # one time
/plugin install doc-review@local                       # install a plugin
```

**From a team marketplace**:
```bash
git clone https://github.com/your-org/claude-plugins ~/claude-plugins
# In Claude Code:
/plugin marketplace add ~/claude-plugins
/plugin install plugin-name@your-marketplace
```

**CLI commands**:
```bash
/plugin                          # Interactive plugin menu
/plugin list                     # Show installed plugins
/plugin install name@market      # Install from marketplace
/plugin uninstall name           # Remove plugin
/plugin enable name              # Enable (loads into context)
/plugin disable name             # Disable (saves tokens)
```

---

## Distributing Plugins

### Team marketplace pattern

A marketplace is a directory (usually a git repo) containing plugins and a manifest:

```
claude-plugins/                  # Git repo
├── .claude-plugin/
│   └── marketplace.json         # Lists all available plugins
├── doc-review/                  # Plugin 1
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── commands/
│   └── agents/
└── another-plugin/              # Plugin 2
    └── ...
```

**marketplace.json**:
```json
{
  "name": "epcvip-plugins",
  "owner": { "name": "EPCVIP Innovation" },
  "description": "Internal plugin collection",
  "plugins": [
    { "name": "doc-review", "source": "./doc-review", "description": "Documentation review agents" },
    { "name": "another-plugin", "source": "./another-plugin", "description": "..." }
  ]
}
```

Team members clone the repo and register it once. New plugins are available after `git pull`.

---

## Design Decisions

- **Agents over monolithic skills**: A single skill that needs to do 4 different analyses will load all instructions into one context and often skip steps. Agents run in isolated context, follow their procedure fully, and can use different models.
- **Commands as orchestrators**: Commands don't do the analysis — they determine scope, launch agents in parallel, and aggregate results. This keeps each piece testable.
- **Model selection per agent**: Cheap models for mechanical tasks, capable models for judgment. A plugin with 4 haiku agents costs roughly the same as 1 sonnet agent.
- **README not loaded into context**: Plugin READMEs are for humans browsing the template library. Agent and command markdown files are what Claude reads at runtime.

---

## See Also

- [Skills README](../skills/README.md) — Single-workflow skill patterns
- [PLUGIN-TEMPLATE.md](./PLUGIN-TEMPLATE.md) — Annotated template for creating new plugins
- [CLAUDE-CODE-CONFIG.md](../../docs/reference/CLAUDE-CODE-CONFIG.md#plugins) — Plugin mechanics, CLI commands, marketplace setup
- [ADVANCED-WORKFLOWS.md](../../docs/reference/ADVANCED-WORKFLOWS.md) — Agent patterns and model selection

---

**Last Updated**: 2026-02-24
