# Claude Code Quick Reference

[← Back to Main README](../../README.md) | [Storage Reference →](./CLAUDE-CODE-STORAGE.md) | [Playwright MCP →](./PLAYWRIGHT-MCP.md) | [Basic Setup Guide →](../setup-guides/CLAUDE-CODE-SETUP.md)

Practical guide for managing Claude Code configuration, MCPs, and plugins.

## Configuration Files

### Main Config Locations
```bash
~/.claude/                    # Main Claude directory
├── settings.json            # Global settings
├── settings.local.json      # Local overrides (permissions, etc.)
├── .claude.json             # Project configs & MCP state
└── plugins/                 # Custom plugins
```

**Key Point**: Claude Code uses `~/.claude/`, NOT `~/.config/claude/`

## Status Line

### What Is The Status Line?

The status line displays at the bottom of Claude Code showing real-time info (model, git branch, tokens, etc.). You can customize it with external tools.

### Configuration

```json
// ~/.claude/settings.json
{
  "statusLine": {
    "type": "command",
    "command": "ccstatusline",
    "padding": 0
  }
}
```

### Performance Note

**Avoid `npx -y package@latest`** for status line commands. NPX checks the npm registry on every startup, causing 30-60 second delays.

```json
// BAD - checks npm registry every startup (slow)
"command": "npx -y ccstatusline@latest"

// GOOD - uses pre-installed binary (fast)
"command": "ccstatusline"
```

**Setup:**
```bash
# Install globally (one time)
npm install -g ccstatusline

# Update periodically
npm update -g ccstatusline
```

### Popular Status Line Tools

- **ccstatusline** (recommended) - Feature-rich, customizable TUI configuration
  - Install: `npm install -g ccstatusline`
  - GitHub: https://github.com/sirmalloc/ccstatusline
  - Config: `~/.config/ccstatusline/settings.json`

### ccstatusline Available Widgets (v2.0.23+)

| Widget | Description |
|--------|-------------|
| `model` | Claude model name |
| `claude-session-id` | Session ID (for resuming with `claude -r`) |
| `context-length` | Current context tokens |
| `context-percentage` | Context usage % |
| `context-percentage-usable` | Usable context % (80% auto-compact threshold) |
| `git-branch` | Current git branch |
| `git-changes` | Uncommitted changes (+/-) |
| `git-worktree` | Active worktree name |
| `current-working-dir` | CWD with configurable segments |
| `version` | Claude Code version |
| `session-clock` | Session elapsed time |
| `session-cost` | Session cost in USD |
| `tokens-input` / `tokens-output` / `tokens-total` | Token counts |
| `tokens-cached` | Cached tokens |
| `block-timer` | 5-hour block timer with progress |
| `custom-text` | Static text (labels, emojis) |
| `custom-command` | Shell command output (for custom data) |

### Custom Widgets with custom-command

You can add custom data via shell scripts:

```json
{
  "id": "my-widget",
  "type": "custom-command",
  "commandPath": "~/.claude/scripts/my-script.sh",
  "prefix": "Label:",
  "timeout": 500
}
```

The script receives Claude Code's JSON data via stdin (session_id, model, workspace, etc.).

### Plan File in Statusline (Workaround)

Claude Code doesn't expose plan file path to statuslines (GitHub issue #6227). Workaround:

```bash
# ~/.claude/scripts/current-plan.sh
#!/bin/bash
ls -t ~/.claude/plans/*.md 2>/dev/null | head -1 | xargs -I{} basename {} .md
```

Then add as custom-command widget to show most recent plan file name.

---

## MCP Servers (Model Context Protocol)

### What Are MCPs?
MCPs give Claude access to external tools and data sources:
- **Playwright**: Browser automation for frontend testing (see [Playwright MCP Guide](./PLAYWRIGHT-MCP.md))
- **Notion**: Search/update Notion workspace
- **Filesystem**: Read/write local files
- **Database**: Query databases
- **Custom**: Any tool you build

### Types of MCPs

#### 1. HTTP/Hosted MCP (e.g., Notion)
```json
{
  "type": "http",
  "url": "https://mcp.notion.com/mcp"
}
```
- Runs on remote server
- OAuth managed by provider
- Zero local setup
- Always up-to-date

#### 2. Stdio/Local MCP
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_TOKEN": "your-token"
  }
}
```
- Runs as local process
- You manage auth/updates
- More customizable
- Works offline

#### 3. Playwright MCP (Browser Automation)
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@playwright/mcp@latest", "--no-sandbox"]
}
```
- Enables Claude to control a browser
- Uses accessibility snapshots (faster/more reliable than screenshots)
- Great for frontend testing and web automation
- See [full Playwright MCP guide](./PLAYWRIGHT-MCP.md) for all options

### Managing MCPs

```bash
# List all configured MCPs
claude mcp list

# Get details about an MCP
claude mcp get notion

# Add an MCP
claude mcp add myserver https://example.com/mcp

# Add local stdio MCP
claude mcp add-json myserver '{"command":"node","args":["server.js"]}'

# Remove an MCP
claude mcp remove notion -s local    # Remove from current project
claude mcp remove notion -s global   # Remove globally
```

### MCP Scopes

- **Global**: Available in all projects
- **Local**: Only in current project (stored in `.claude.json`)
- **Project**: Via `.mcp.json` file in project root

### Token Cost

⚠️ **MCPs consume tokens!** Each MCP loads tool definitions into context.

Example: Notion MCP = ~30k tokens

**Strategy**: Use plugins to toggle MCPs on/off as needed.

## Plugins

### What Are Plugins?
Bundles of commands, agents, hooks, and MCPs you can toggle on/off.

**Key Benefit**: Save tokens by disabling unused functionality.

### Plugin Structure
```
~/.claude/plugins/plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required manifest
├── commands/                # Optional: slash commands
├── agents/                  # Optional: specialized agents
├── hooks/                   # Optional: workflow hooks
└── README.md               # Optional: documentation
```

### Plugin Manifest (plugin.json)
```json
{
  "name": "notion-mode",
  "version": "1.0.0",
  "description": "Notion integration (30k tokens)",
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

### Plugin Commands

```bash
# Interactive plugin menu
/plugin

# Install a plugin
/plugin install notion-mode

# Uninstall (saves tokens!)
/plugin uninstall notion-mode

# List installed plugins
/plugin list

# Enable/disable without uninstalling
/plugin enable notion-mode
/plugin disable notion-mode
```

### Creating a Local Plugin

1. Create marketplace and plugin structure:
```bash
mkdir -p ~/.claude/marketplaces/local/my-plugin/.claude-plugin
```

2. Create plugin manifest (`~/.claude/marketplaces/local/my-plugin/.claude-plugin/plugin.json`):
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does"
}
```

3. Create marketplace manifest (`~/.claude/marketplaces/local/.claude-plugin/marketplace.json`):
```json
{
  "name": "local",
  "owner": {
    "name": "Your Name"
  },
  "description": "Local plugins",
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./my-plugin",
      "description": "What this plugin does"
    }
  ]
}
```

4. Add marketplace (one time):
```bash
/plugin marketplace add ~/.claude/marketplaces/local
```

5. Install plugin:
```bash
/plugin install my-plugin@local
```

## Installed Plugins

### notion-mode
- **Location**: `~/.claude/marketplaces/local/notion-mode/`
- **Purpose**: Toggle Notion MCP (saves 30k tokens when disabled)
- **Setup**: One-time: `/plugin marketplace add ~/.claude/marketplaces/local`
- **Usage**:
  - Enable: `/plugin install notion-mode@local`
  - Disable: `/plugin uninstall notion-mode`

---

## Hooks

### What Are Hooks?

Shell commands that execute at specific workflow events (PreToolUse, PostToolUse, SessionStart, etc.) to automate enforcement, validation, and logging.

**Key Benefit**: Deterministic control over Claude's actions (vs hoping Claude follows instructions)

### Hook Configuration Locations

```bash
~/.claude/settings.json           # User global (all repos)
.claude/settings.json             # Project shared (team)
.claude/settings.local.json       # Project local (personal)
```

### Common Hook Types

**PreToolUse** (Before tool calls):
- Query validation (block execution without validation)
- Permissions checking
- File size limits
- Security validation

**PostToolUse** (After tool calls):
- Auto-formatting
- Syncing related files
- Updating documentation
- Running tests

**UserPromptSubmit** (User submits prompt):
- Content filtering
- Logging
- Rate limiting

### Managing Hooks

```bash
# Interactive hook configuration
/hooks

# Or edit settings.json manually
nano ~/.claude/settings.json
```

### Installed Hooks

#### Query Validation Hook (Production)

**Installed at**: `~/.claude/hooks/validate-query-execution.py`

**What it does**:
- Blocks Athena query execution without prior validation
- Checks for validation marker (created by `/validate-query`)
- Provides clear recovery instructions
- Whitelists common commands (git, ls, etc.) for performance

**Configuration** (`~/.claude/settings.json`):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/validate-query-execution.py"
          }
        ]
      }
    ]
  }
}
```

**Emergency bypass**:
```bash
SKIP_QUERY_VALIDATION=1 python run_query.py query.sql
```

### Hook Templates

See [templates/hooks/](./templates/hooks/) for:
- **Query validation** (production-ready) - Enforce query validation before execution
- **Pre-commit formatting** (example) - Auto-format code before git commits
- **Sensitive file blocker** (example) - Block edits to production config files
- **Command logger** (example) - Audit trail of all Bash commands
- **Complete hooks reference guide** - Full technical documentation

### Official Hook Documentation

- **Hooks Guide**: https://docs.claude.com/en/docs/claude-code/hooks-guide
- **Settings Reference**: https://docs.claude.com/en/docs/claude-code/settings

---

## Common Workflows

### Starting a Docs Session (No Notion)
```bash
cd ~/repos/docs
claude
# Notion disabled by default, saves 30k tokens
```

### Starting with Notion
```bash
cd ~/repos/docs
claude
/plugin install notion-mode@local
# Now can search/update Notion
```

### Check Current Setup
```bash
# See all active MCPs
claude mcp list

# See installed plugins
/plugin list

# Check token usage
/context
```

## Token Optimization

### Current Setup
- Base Claude: ~15k tokens (system prompt + tools)
- Notion MCP: ~30k tokens (when enabled)
- Other MCPs: Varies

### Strategy
1. **Default**: Minimal setup, no MCPs
2. **As-needed**: Install plugins when you need functionality
3. **After use**: Uninstall to reclaim tokens

## Troubleshooting

### MCP Not Working
```bash
# Check MCP status
claude mcp list

# Test MCP connection
claude --debug
# Look for MCP errors in output
```

### Plugin Not Loading
```bash
# Verify plugin structure
ls -la ~/.claude/plugins/plugin-name/.claude-plugin/

# Check plugin.json syntax
cat ~/.claude/plugins/plugin-name/.claude-plugin/plugin.json | jq .

# Debug mode
claude --debug
```

### Reset Project MCP Choices
```bash
claude mcp reset-project-choices
```

## Reference Documentation

### Official Docs
- **Claude Code Plugins**: https://docs.claude.com/en/docs/claude-code/plugins
- **Claude Code Plugins Reference**: https://docs.claude.com/en/docs/claude-code/plugins-reference
- **MCP Setup**: https://docs.claude.com/en/docs/claude-code/mcp
- **Notion MCP**: https://developers.notion.com/docs/mcp
- **Notion Hosted MCP Blog**: https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look

### Community Resources
- **MCP Registry**: https://github.com/modelcontextprotocol/registry
- **MCP Servers**: https://github.com/modelcontextprotocol/servers
- **MCP Specification**: https://modelcontextprotocol.io/specification/2025-06-18

## Quick Commands Cheat Sheet

```bash
# MCP Management
claude mcp list                          # List all MCPs
claude mcp get <name>                    # Get MCP details
claude mcp remove <name> -s local        # Remove from project
claude mcp add <name> <url>              # Add HTTP MCP

# Plugin Management
/plugin                                  # Interactive menu
/plugin install <name>                   # Install plugin
/plugin uninstall <name>                 # Uninstall (save tokens)
/plugin list                             # List plugins

# Context Management
/context                                 # Show token usage
/compact                                 # Compress context
/clear                                   # Clear conversation
```

---

Last Updated: January 2026
