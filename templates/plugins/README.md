# Claude Code Plugins

[← Back to Main README](../../README.md)

Distributable bundles of skills, agents, hooks, MCP servers, and more — the packaging layer on top of skills.

> **Official docs**: [Create plugins](https://code.claude.com/docs/en/plugins) · [Plugin reference](https://code.claude.com/docs/en/plugins-reference) · [Discover plugins](https://code.claude.com/docs/en/discover-plugins) · [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

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
│   └── plugin.json              # Optional — manifest (auto-discovery works without it)
├── README.md                    # Human docs (not loaded into context)
├── skills/                      # Recommended — skills as Markdown (SKILL.md per skill)
│   └── my-skill/
│       └── SKILL.md
├── commands/                    # Legacy — use skills/ for new plugins
│   └── do-thing.md              #   Frontmatter: description, argument-hint, allowed-tools
├── agents/                      # Specialized agents (launched by commands/skills)
│   ├── fast-checker.md          #   Frontmatter: name, description, model
│   └── deep-analyzer.md         #   Each agent runs in isolated context
├── hooks/
│   └── hooks.json               # Optional — lifecycle hooks (JSON config, same format as settings.json)
├── .mcp.json                    # Optional — MCP server configs for this plugin
├── .lsp.json                    # Optional — LSP server configs
├── settings.json                # Optional — default settings applied when plugin is enabled
├── outputStyles/                # Optional — custom output styles
└── references/                  # Optional — supporting docs loaded on demand
    └── patterns.md              #   Domain knowledge, checklists, examples
```

**Skills** are the recommended entry point — each `skills/<name>/SKILL.md` defines a workflow users invoke via `/plugin-name:skill-name`. Skills can orchestrate agents.

**Commands** (legacy flat-file format) still work — users invoke them via `/plugin-name:command-name`. Existing plugins using `commands/` don't need to migrate. Commands and skills are unified; `commands/` is simply the flat-file format.

**Agents** are workers — commands/skills launch them via the Task tool. Each agent runs in isolated context with its own model and tools.

> **Manifest is optional**: Claude Code auto-discovers components in their default directories (`skills/`, `commands/`, `agents/`, `hooks/`, etc.). The manifest lets you declare custom paths or add metadata, but isn't required.

> **`${CLAUDE_PLUGIN_ROOT}`**: Use this env var in hook commands and MCP configs to reference files relative to the plugin root (e.g., `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"`).

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
  "version": "1.0.0",
  "homepage": "https://github.com/your-org/plugin-name",
  "repository": "https://github.com/your-org/plugin-name",
  "license": "MIT",
  "keywords": ["review", "documentation"]
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Lowercase, hyphens only. Must match directory name. |
| `description` | Yes | One line. Shown in `/plugin list` and marketplace. |
| `author.name` | No | Person or team who maintains the plugin. |
| `version` | No | Semver. Helps teams track updates. |
| `homepage` | No | URL for plugin documentation or landing page. |
| `repository` | No | Source code URL. |
| `license` | No | SPDX license identifier (e.g., `MIT`, `Apache-2.0`). |
| `keywords` | No | Tags for marketplace search/discovery. |
| `commands` | No | Custom paths to command files (supplements `commands/` auto-discovery). |
| `agents` | No | Custom paths to agent files (supplements `agents/` auto-discovery). |
| `skills` | No | Custom paths to skill directories (supplements `skills/` auto-discovery). |
| `hooks` | No | Hook configurations (alternative to `hooks/hooks.json`). |
| `mcpServers` | No | MCP server configs (alternative to `.mcp.json`). |
| `lspServers` | No | LSP server configs (alternative to `.lsp.json`). |
| `outputStyles` | No | Custom output style definitions. |

> Component paths in the manifest **supplement** defaults — they don't replace auto-discovered directories. See [plugin reference](https://code.claude.com/docs/en/plugins-reference) for the full schema.

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

### Official marketplace

The Anthropic official marketplace (`claude-plugins-official`) is auto-available — no registration needed:
```bash
/plugin install frontend-design@claude-plugins-official
```

### From a GitHub marketplace

```bash
# GitHub shorthand — registers and installs in one step
/plugin marketplace add owner/repo
/plugin install plugin-name@marketplace-name
```

### Local marketplace (one-time setup)

```bash
mkdir -p ~/.claude/marketplaces/local/.claude-plugin
# Create marketplace.json — see "Distributing Plugins" below for the format
# Then: copy plugin dirs into ~/.claude/marketplaces/local/
/plugin marketplace add ~/.claude/marketplaces/local   # one time
/plugin install doc-review@local                       # install a plugin
```

### Installation scopes

| Scope | Flag | Stored In | Shared |
|-------|------|-----------|--------|
| `user` | `--scope user` (default) | `~/.claude/plugins/` | All your projects |
| `project` | `--scope project` | `.claude/plugins/` | Team via git |
| `local` | `--scope local` | `.claude/plugins/` (gitignored) | Just you, this project |
| `managed` | `--scope managed` | Admin-controlled | Organization-wide |

### CLI commands

```bash
/plugin                          # Interactive plugin menu
/plugin list                     # Show installed plugins
/plugin install name@market      # Install from marketplace
/plugin install name --scope project  # Install to project scope
/plugin uninstall name           # Remove plugin
/plugin enable name              # Enable (loads into context)
/plugin disable name             # Disable (saves tokens)
claude plugin validate           # Validate plugin structure (from shell)
claude plugin update             # Update installed plugins (from shell)
```

### Testing during development

```bash
# Load a plugin from a local directory without installing
claude --plugin-dir /path/to/your-plugin
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
│   ├── skills/
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

Plugin sources can also reference GitHub repos, URLs, npm packages, or pip packages — and support `ref`/`sha` pinning. See [plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) for all source types.

Team members clone the repo and register it once. New plugins are available after `git pull`. Marketplaces auto-update at Claude Code startup.

### Team setup via settings

For teams, pre-configure marketplaces and plugins in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": ["owner/repo"],
  "enabledPlugins": ["plugin-name@marketplace"]
}
```

Use `strictKnownMarketplaces: true` to restrict installations to approved marketplaces only (admin lockdown).

### Ecosystem

Active public marketplaces include [Expo](https://github.com/expo/claude-plugins), [Trail of Bits](https://github.com/trailofbits/claude-plugins), Stagehand, and Parallel Web Systems. The official Anthropic marketplace includes `frontend-design` and other skills.

---

## Design Decisions

- **Agents over monolithic skills**: A single skill that needs to do 4 different analyses will load all instructions into one context and often skip steps. Agents run in isolated context, follow their procedure fully, and can use different models.
- **Skills as orchestrators**: Skills don't do the analysis — they determine scope, launch agents in parallel, and aggregate results. This keeps each piece testable.
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
