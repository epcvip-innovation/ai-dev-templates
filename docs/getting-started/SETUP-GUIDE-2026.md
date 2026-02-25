# Getting Started with AI Coding Assistants (February 2026)

[← Back to README](../../README.md)

**Last Updated**: February 13, 2026
**Time Required**: 10-15 minutes

Everything you need to start using AI coding assistants on any platform. This guide covers Claude Code (our primary tool) and Codex CLI (our recommended secondary tool for cross-review).

---

## Our Recommendation

**Claude Code** (primary) + **Codex CLI** (secondary), running simultaneously.

Why both? One writes code, the other reviews it. Different model families catch different issues. This dual-tool workflow is how our team gets the most value from AI-assisted development.

If you're just getting started, **begin with Claude Code only** and add Codex later.

---

## Part 1: Claude Code Setup

### Choose Your Platform

| Platform | Recommended Install | Notes |
|----------|-------------------|-------|
| **macOS** | Native installer | One command, auto-updates |
| **Windows** | Native PowerShell installer | Works without WSL |
| **Windows (WSL2)** | Linux installer inside WSL | Our power-user setup |
| **Linux** | Native installer | One command, auto-updates |

#### Windows Users: Which Path?

Both paths get you a fully working Claude Code setup. The difference is performance and environment:

| | **Windows Native** | **Windows + WSL2** |
|---|---|---|
| **Install time** | 2 minutes | 90 minutes (one-time) |
| **Complexity** | Just works | Two environments to learn |
| **File I/O speed** | ~200 MB/s | ~2.4 GB/s (10x faster) |
| **Shell** | PowerShell / Git Bash | Native bash |
| **Matches production** | No (servers run Linux) | Yes |
| **Best for** | Getting started fast, light usage | Heavy CLI, shell scripts, Docker |

**Our recommendation**: Start with **Windows Native** below to get productive today. If you hit friction with slow git operations or shell compatibility, upgrade to WSL2 later using the [Microsoft WSL install guide](https://learn.microsoft.com/en-us/windows/wsl/install).

**Why we use WSL2**: [Architecture Decision Record](../decisions/why-wsl.md)

### Installation

#### macOS / Linux (native installer — recommended)

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

#### macOS (Homebrew)

```bash
brew install --cask claude-code
```

#### Windows (native PowerShell)

```powershell
irm https://claude.ai/install.ps1 | iex
```

#### Windows (WinGet)

```powershell
winget install Anthropic.ClaudeCode
```

#### Windows (WSL2) — our power-user setup

Inside your WSL terminal, use the Linux installer:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

For the full WSL2 development environment, see the [Microsoft WSL install guide](https://learn.microsoft.com/en-us/windows/wsl/install) and [Why WSL](../decisions/why-wsl.md) for configuration recommendations.

#### npm (legacy, not recommended)

```bash
npm install -g @anthropic-ai/claude-code
```

> **Note**: The npm install method does not auto-update. You'll need to manually run `npm update -g @anthropic-ai/claude-code` to get new versions. The native installers handle updates automatically.

### Verify Installation

```bash
claude --version
```

### Authentication

Run `claude` and follow the prompts. You'll choose one of:

| Auth Method | Best For | Billing |
|-------------|----------|---------|
| **Claude Pro/Max** | Individual developers | Monthly subscription |
| **Claude Teams/Enterprise** | Organizations | Per-seat via admin |
| **Anthropic Console** | API-key billing | Pay-per-use |

```bash
# Start Claude — authentication happens on first launch
claude
```

The browser will open for OAuth. Sign in, then return to your terminal.

### Choose Your Interface

#### Terminal (default)

```bash
claude
```

The terminal interface is the most powerful way to use Claude Code. It has full access to file editing, command execution, and all features.

#### VS Code Extension (recommended for IDE users)

Install from the VS Code marketplace:

1. Open VS Code
2. `Cmd/Ctrl+Shift+X` to open Extensions
3. Search "Claude Code" (publisher: Anthropic)
4. Click Install

**Requirements**: VS Code 1.98.0+

You can also install via command line:

```bash
code --install-extension anthropic.claude-code
```

#### Cursor IDE

Cursor supports the Claude Code extension with a manual install workaround:

```
cursor:extension/anthropic.claude-code
```

Or install the `.vsix` file manually from the VS Code marketplace.

#### JetBrains IDEs

Install the [Claude Code plugin](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) from the JetBrains Marketplace (IntelliJ, PyCharm, WebStorm, etc.).

#### Desktop App (standalone)

Download the installer — no terminal or IDE required:
- **macOS**: [Download (.dmg)](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect)
- **Windows**: [Download (.exe)](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect)

#### Web-Based (no install)

Try Claude Code instantly at [claude.ai/code](https://claude.ai/code) — no installation needed. Limited compared to CLI/extension but useful for quick tasks or evaluation.

#### Both (terminal + IDE)

You can use terminal and IDE interfaces simultaneously. They share the same authentication and work with the same project. Use the terminal for complex multi-step tasks and the IDE extension for quick inline assistance.

---

## Part 2: Codex CLI Setup (Optional but Recommended)

Codex CLI is OpenAI's terminal-based coding assistant. We run it alongside Claude Code for a dual-tool workflow.

### Installation

```bash
npm install -g @openai/codex
```

Or via Homebrew (macOS):
```bash
brew install --cask codex
```

> **Note**: Codex CLI requires Node.js 22+ for npm install. If you're on macOS, `brew install --cask codex` doesn't require Node.js.

### Verify Installation

```bash
codex --version
```

### Authentication

Codex CLI authenticates via your ChatGPT account:

```bash
codex
# Follow the browser prompts to sign in with your ChatGPT account
# Requires a paid ChatGPT plan (Plus, Pro, Team, or Enterprise)
```

### Why Both Tools?

- **Different models catch different issues**: Claude (Opus 4.6) and Codex (GPT-5.3-codex) have different strengths
- **Cross-review workflow**: One writes code, the other reviews it
- **Split terminals**: Run both simultaneously on the same project
- **MCP integration**: Can run Codex as an MCP server inside Claude Code, or vice versa

---

## Part 3: First 5 Minutes

### Quick Wins with Claude Code

```bash
# Navigate to any project
cd ~/your-project

# Start Claude Code
claude

# Try these:
# "Explain the structure of this project"
# "Find all TODO comments in the codebase"
# "Write tests for the auth module"
# "Create a function that validates email addresses"
```

Useful built-in commands:

```
/help              # See all commands
/settings          # View/modify settings
/clear             # Clear conversation
exit               # Exit Claude Code
```

### Quick Wins with Codex CLI

```bash
cd ~/your-project

# Start Codex
codex

# Try similar prompts — compare the approaches
```

### Dual-Tool Workflow Example

Open two terminal windows (or split your terminal):

```
┌─────────────────────┬─────────────────────┐
│ Terminal 1           │ Terminal 2           │
│                      │                      │
│ $ cd ~/my-project    │ $ cd ~/my-project    │
│ $ claude             │ $ codex              │
│                      │                      │
│ "Add input           │ "Review the changes  │
│  validation to       │  in src/api/users.ts │
│  the users API"      │  — any issues?"      │
│                      │                      │
└─────────────────────┴─────────────────────┘
```

One writes, the other reviews. Swap roles as needed.

---

## What's Current (February 2026)

| Tool | Version | Default Model |
|------|---------|---------------|
| **Claude Code** | Latest (auto-updates) | Claude Opus 4.6 (since Feb 5, 2026) |
| **Codex CLI** | v0.100.0+ | GPT-5.3-codex |
| **Codex CLI (Spark)** | v0.100.0+ | GPT-5.3-codex-spark (real-time, 15x faster) |

**Recent changes**:
- Claude Opus 4.6 is the default model (Feb 5, 2026)
- VS Code extension is now the primary IDE interface for Claude Code
- Native installers (non-npm) are the recommended install method
- Agent Teams feature available (experimental, opt-in)
- GPT-5.3-codex-spark released Feb 12, 2026 (real-time speed variant)
- Release channels: `latest` (default) and `stable` available

---

## Next Steps

| You Want To... | Go Here |
|----------------|---------|
| Set up a new project with Claude Code | [New Project Setup](./NEW-PROJECT-SETUP.md) |
| Browse our template library | [Templates](../../templates/README.md) |
| Browse skill templates | [Skill Templates](../../templates/slash-commands/README.md) |
| Set up WSL2 on Windows | [Microsoft WSL install guide](https://learn.microsoft.com/en-us/windows/wsl/install) |
| Deep-dive on Claude Code configuration | [Claude Code Setup](../setup-guides/CLAUDE-CODE-SETUP.md) |
| Set up Playwright testing with Claude | [Testing Guide](../../templates/testing/PLAYWRIGHT_CLAUDE_GUIDE.md) |
| Understand our code quality standards | [Anti-Slop Standards](../../templates/standards/ANTI_SLOP_STANDARDS.md) |

---

## Sources

- [Claude Code Official Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Installation](https://docs.anthropic.com/en/docs/claude-code/installation)
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [OpenAI Codex CLI (GitHub)](https://github.com/openai/codex)
- [VS Code Marketplace — Claude Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
- [Codex CLI Official Documentation](https://developers.openai.com/codex/)
