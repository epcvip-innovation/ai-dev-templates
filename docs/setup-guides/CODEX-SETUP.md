# Codex CLI Setup Guide

[← Back to Main README](../../README.md) | [Getting Started (all platforms) →](../getting-started/SETUP-GUIDE-2026.md)

**Last Updated**: 2026-02-13
**Time Required**: 5-10 minutes

Guide to installing Codex CLI and using it alongside Claude Code for a dual-tool development workflow.

---

## What is Codex CLI?

Codex CLI is OpenAI's terminal-based AI coding assistant ([github.com/openai/codex](https://github.com/openai/codex)). It runs in your terminal, similar to Claude Code, but uses OpenAI's GPT models.

> **Not the old Codex API**: OpenAI's original Codex API was sunset in 2024. Codex CLI is a separate, actively-maintained tool released in 2025. Don't confuse the two.

**Current version**: v0.100.0+
**Default model**: GPT-5.3-codex
**Speed variant**: GPT-5.3-codex-spark (real-time, 15x faster — released Feb 12, 2026)

**Official Repository**: [https://github.com/openai/codex](https://github.com/openai/codex)

---

## Why We Use Both Claude Code + Codex CLI

We recommend running Claude Code and Codex CLI simultaneously as a dual-tool workflow:

- **Different models catch different issues** — Claude (Opus 4.6) and Codex (GPT-5.3) have different strengths and blind spots
- **Cross-review** — One tool writes code, the other reviews it
- **Split terminals** — Run both side-by-side on the same project
- **MCP integration** — Can run Codex as an MCP server inside Claude Code, or vice versa

> **Note**: Claude Code and Codex handle MCPs differently — crucially, Claude Code uses Tool Search (lazy loading) for ~89% context savings. See [MCP Context & Efficiency](../mcp/MCP-CONTEXT.md) for the comparison.

**Claude Code is our primary tool.** Codex is the secondary tool for cross-review and comparison. If you only want one tool, start with Claude Code.

---

## Prerequisites

- Node.js 22+ and npm (for npm install) — or Homebrew on macOS (no Node.js needed)
- A paid ChatGPT account (Plus, Pro, Team, or Enterprise)

**Check if already installed**:
```bash
which codex
codex --version
```

---

## Installation

```bash
npm install -g @openai/codex
```

Or via Homebrew (macOS):
```bash
brew install --cask codex
```

Verify installation:
```bash
codex --version
```

---

## Authentication

### ChatGPT Account Sign-In

Codex CLI authenticates via your ChatGPT account (not an API key):

```bash
codex
# Follow the browser prompts to sign in with your ChatGPT account
# Requires a paid ChatGPT plan (Plus, Pro, Team, or Enterprise)
```

---

## Usage

### Basic Usage

```bash
# Start in current directory
cd ~/repos/your-project
codex

# Ask questions, write code, run commands — similar to Claude Code
```

### Common Commands

```
help     # Show available commands
exit     # Exit Codex
```

---

## Dual-Tool Workflow

This is our recommended way to use both tools together.

### Split Terminal Setup

Open two terminal windows (or use tmux/split pane):

```
┌─────────────────────────┬─────────────────────────┐
│ Terminal 1: Claude Code  │ Terminal 2: Codex CLI    │
│                          │                          │
│ $ cd ~/repos/my-project  │ $ cd ~/repos/my-project  │
│ $ claude                 │ $ codex                  │
│                          │                          │
│ "Add input validation    │ "Review the changes in   │
│  to the users API        │  src/api/users.ts —      │
│  endpoint"               │  any issues?"            │
│                          │                          │
└─────────────────────────┴─────────────────────────┘
```

### Workflow Patterns

**Pattern 1: Write + Review**
1. Use Claude Code to implement a feature
2. Switch to Codex and ask it to review the changes
3. Fix any issues either tool catches

**Pattern 2: Competing Approaches**
1. Ask both tools the same question
2. Compare their approaches
3. Pick the better solution (or combine them)

**Pattern 3: MCP Cross-Use**
Run Codex as an MCP server inside Claude Code (or vice versa). This lets one tool invoke the other programmatically. See [Claude Code Config](../reference/CLAUDE-CODE-CONFIG.md) for MCP setup.

---

## Troubleshooting

### Issue: "command not found: codex"

**Solution**: Ensure npm global bin is in your PATH:
```bash
# Check npm global prefix
npm config get prefix

# Add to PATH if needed
export PATH="$PATH:$(npm config get prefix)/bin"

# Reinstall
npm install -g @openai/codex
```

### Issue: Authentication fails

**Solution**:
```bash
# Re-run codex and follow the browser prompts
codex

# If browser doesn't open, check your default browser setting
# Ensure you have a paid ChatGPT plan (Plus, Pro, Team, or Enterprise)
```

---

## Performance Tips

- Keep sessions focused on one project
- Clear context between tasks
- Use version control — review AI suggestions before committing
- For comparison workflows, keep both tools on the same codebase directory

---

## See Also

**Setup Guides**:
- [Getting Started](../getting-started/SETUP-GUIDE-2026.md) — Platform-agnostic setup for both tools
- [Claude Code Setup](./CLAUDE-CODE-SETUP.md) — Primary AI assistant (recommended)
- [Daily Workflow](./DAILY-WORKFLOW.md) — Using AI tools daily
- [Cursor WSL Setup](./CURSOR-WSL-SETUP.md) — IDE integration

**Reference**:
- [Commands Reference](../reference/COMMANDS.md) — All available commands
- [Advanced Workflows](../reference/ADVANCED-WORKFLOWS.md) — Model selection strategy, dual-tool patterns

**Official**:
- [OpenAI Codex CLI (GitHub)](https://github.com/openai/codex)
- [Codex CLI Official Documentation](https://developers.openai.com/codex/)
- [Codex CLI Quickstart](https://developers.openai.com/codex/quickstart/)

---

**Next Steps**:
1. Codex CLI installed
2. Set up [Claude Code](./CLAUDE-CODE-SETUP.md) if you haven't already
3. Try the [dual-tool workflow](#dual-tool-workflow) with split terminals
4. Read [Daily Workflow](./DAILY-WORKFLOW.md) guide
