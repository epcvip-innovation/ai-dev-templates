# Claude Code Setup Guide

[← Back to Main README](../../README.md) | [Getting Started (all platforms) →](../getting-started/SETUP-GUIDE-2026.md) | [Advanced Configuration →](../reference/CLAUDE-CODE-CONFIG.md)

**Last Updated**: 2026-02-13
**Time Required**: 5-10 minutes

Complete guide to installing and configuring Claude Code CLI for AI-assisted development.

> **New here?** The [Getting Started guide](../getting-started/SETUP-GUIDE-2026.md) covers all platforms (Mac, Windows, Linux) with our dual-tool recommendation. This page goes deeper on Claude Code configuration and troubleshooting.

---

## What is Claude Code?

Claude Code is Anthropic's CLI tool for AI pair programming. It provides:
- AI assistance directly in terminal or VS Code
- File editing capabilities
- Command execution
- Context-aware suggestions

**Official Documentation**: [https://docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code)

---

## Prerequisites

- **macOS, Windows, or Linux** (WSL2 optional on Windows)
- Anthropic API key OR Claude Pro/Max subscription
- Node.js 18+ only if using npm install method

**Check if already installed**:
```bash
which claude
claude --version
```

---

## Installation

### Option A: Native Installer (Recommended)

The native installer provides automatic updates and doesn't require Node.js.

**macOS / Linux / WSL2**:
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**macOS (Homebrew)**:
```bash
brew install --cask claude-code
```

**Windows (PowerShell)**:
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows (CMD)**:
```cmd
curl -fsSL https://claude.ai/install.bat | cmd
```

**Windows (WinGet)**:
```powershell
winget install Anthropic.ClaudeCode
```

Verify installation:
```bash
claude --version
```

### Option B: Via npm (Legacy)

```bash
npm install -g @anthropic-ai/claude-code
```

> **Note**: npm installs do not auto-update. You'll need to run `npm update -g @anthropic-ai/claude-code` manually. Prefer the native installer for automatic updates.

### Option C: Desktop App (standalone)

Download directly — no terminal or IDE required:
- **macOS**: [Download (.dmg)](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect)
- **Windows**: [Download (.exe)](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect)

See [Getting Started](../getting-started/SETUP-GUIDE-2026.md) for all entry points including web-based access.

### Option D: Other Methods

Check official documentation for additional installation methods:
[https://docs.anthropic.com/en/docs/claude-code/installation](https://docs.anthropic.com/en/docs/claude-code/installation)

---

## VS Code Extension

The Claude Code VS Code extension provides an integrated IDE experience.

### Install

1. Open VS Code (1.98.0+ required)
2. `Cmd/Ctrl+Shift+X` → search "Claude Code"
3. Install the extension by Anthropic

Or via command line:
```bash
code --install-extension anthropic.claude-code
```

### Cursor IDE

Cursor supports the Claude Code extension:
```
cursor:extension/anthropic.claude-code
```

You can also download the `.vsix` from the VS Code marketplace and install manually in Cursor.

### JetBrains IDEs

Install the [Claude Code plugin](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) from the JetBrains Marketplace (IntelliJ, PyCharm, WebStorm, etc.).

### Terminal + IDE Together

You can run Claude Code in the terminal and the VS Code extension simultaneously. They share authentication and project context. Use terminal for complex multi-step tasks, IDE for quick inline help.

---

## Authentication

### Method 1: OAuth (Recommended)

```bash
# Start Claude
claude

# Follow browser prompts to authenticate
# Choose your account type:
# - Claude Pro / Claude Max (individual subscription)
# - Claude Teams / Claude Enterprise (org billing)
# - Anthropic Console (API key billing)
```

### Method 2: API Key

```bash
# Set environment variable
export ANTHROPIC_API_KEY="your-api-key-here"

# Or add to ~/.bashrc / ~/.zshrc
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Get API key**: [https://console.anthropic.com/](https://console.anthropic.com/)

---

## Configuration

### Basic Configuration

Claude Code stores configuration in `~/.claude/`

**Verify config location**:
```bash
ls ~/.claude/
```

### Permission Modes

Claude Code has permission modes to control AI actions:

```bash
# Auto-accept file edits (faster workflow)
/permission-mode acceptEdits

# Always ask before edits (safer)
/permission-mode ask
```

Set in session or add to `~/.claude/settings.json`

---

## Usage

### Basic Usage

```bash
# Start in current directory
claude

# With additional context directory
claude --add-dir ~/knowledge-base

# Open specific project
cd ~/repos/your-project
claude
```

### Common Commands (inside Claude)

```
/help              # Show available commands
/settings          # View/modify settings
/permission-mode   # Change permission mode
/clear             # Clear conversation history
exit               # Exit Claude
```

### Adding Project Context

```bash
# Add knowledge base or docs
claude --add-dir ~/repos/docs

# Add multiple directories
claude --add-dir ~/docs --add-dir ~/config
```

---

## Troubleshooting

### Issue: "command not found: claude"

**If installed via native installer**:
```bash
# The installer adds claude to your PATH automatically
# Try opening a new terminal window/tab

# Check where it was installed
ls ~/.claude/bin/claude
```

**If installed via npm**:
```bash
# Verify npm global packages location
npm config get prefix

# If wrong, fix npm prefix
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Reinstall
npm install -g @anthropic-ai/claude-code
```

### Issue: Claude freezes every ~10 seconds (WSL)

**Cause**: DNS resolution issues in WSL

**Solution**:
```bash
# Fix DNS
sudo rm /etc/resolv.conf
echo -e "nameserver 8.8.8.8\nnameserver 1.1.1.1" | sudo tee /etc/resolv.conf
sudo chattr +i /etc/resolv.conf
echo -e "[network]\ngenerateResolvConf = false" | sudo tee -a /etc/wsl.conf

# Restart WSL (from PowerShell)
wsl --shutdown
wsl
```

**Note**: Modern WSL (2025+) typically doesn't have this issue.

### Issue: Authentication fails

**Solution**:
```bash
# Clear existing auth
rm -rf ~/.claude/auth

# Try authenticating again
claude
```

### Issue: Can't access knowledge base

**Solution**:
```bash
# Verify directory exists
ls ~/knowledge-base

# Check permissions
ls -la ~/knowledge-base

# Use absolute path
claude --add-dir $HOME/knowledge-base
```

---

## Best Practices

### 1. Use Permission Modes Wisely

**For solo work**:
```bash
/permission-mode acceptEdits  # Faster
```

**For team/production**:
```bash
/permission-mode ask  # Safer
```

### 2. Organize Project Context

```bash
# Good: Specific context
cd ~/repos/your-project
claude

# Better: With relevant docs
claude --add-dir ~/repos/docs/your-project-docs
```

### 3. Keep Sessions Focused

- One project per session
- Clear context between projects (`/clear`)
- Exit and restart for new tasks

### 4. Use With Version Control

```bash
# Always in a git repo
cd ~/repos/your-project
git status  # Verify clean state
claude      # Make changes
git diff    # Review before committing
```

---

## Integration with Other Tools

### With VS Code / Cursor

Use the Claude Code extension for inline assistance alongside the terminal for complex tasks. Both share authentication.

### With Codex CLI (Recommended)

Our dual-tool workflow: Claude Code writes, Codex reviews (or vice versa).

```bash
# Terminal 1: Claude Code
cd ~/repos/your-project
claude

# Terminal 2: Codex CLI
cd ~/repos/your-project
codex
```

See [Getting Started](../getting-started/SETUP-GUIDE-2026.md#part-2-codex-cli-setup-optional-but-recommended) for Codex setup.

### With Knowledge Base

```bash
claude --add-dir ./knowledge-base
```

---

## Advanced Configuration

### Custom Skills

**What are Skills?**: Modular task definitions that Claude loads dynamically from your project's `.claude/skills/` directory or the user-level `~/.claude/skills/`.

**Create Custom Skill**:
```bash
# Create skills directory
mkdir -p .claude/skills/my-project

# Create instructions
cat > .claude/skills/my-project/instructions.md << 'EOF'
# My Project Coding Standards
- Use TypeScript strict mode
- Follow ESLint rules
- Write tests for all functions
EOF
```

### MCPs (Model Context Protocol)

**Best Practice**: Only enable MCPs you actively need (saves tokens and reduces noise).

See [Claude Code Config Reference](../reference/CLAUDE-CODE-CONFIG.md) for MCP setup.

---

## Performance Tips

### Fast Workflow

1. **Keep sessions running**: Don't exit/restart frequently
2. **Use permission modes**: `acceptEdits` for trusted work
3. **Focused context**: Only add directories you need
4. **Clear old context**: `/clear` when switching tasks

### Resource Usage

Claude Code is lightweight:
- **RAM**: ~100-200MB per session
- **CPU**: Minimal when idle
- **Network**: Only during API calls

---

## Uninstallation

### Native Installer

```bash
# macOS / Linux
claude uninstall

# Or remove manually
rm -rf ~/.claude
```

### npm

```bash
npm uninstall -g @anthropic-ai/claude-code
rm -rf ~/.claude  # Remove configuration (optional)
```

### Windows

```powershell
# WinGet
winget uninstall Anthropic.ClaudeCode

# Or use Add/Remove Programs
```

---

## See Also

**Related Guides**:
- [Getting Started](../getting-started/SETUP-GUIDE-2026.md) — Platform-agnostic setup (start here if new)
- [Daily Workflow](./DAILY-WORKFLOW.md) — Using Claude in daily development
- [Codex Setup](./CODEX-SETUP.md) — Dual-tool workflow with Codex CLI
- [Cursor WSL Setup](./CURSOR-WSL-SETUP.md) — IDE integration (Windows/WSL)

**Reference**:
- [Commands Reference](../reference/COMMANDS.md) — All available commands
- [Claude Code Config](../reference/CLAUDE-CODE-CONFIG.md) — Advanced configuration

**Official**:
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic Console](https://console.anthropic.com/)

---

**Next Steps**:
1. Claude Code installed
2. Set up [Codex CLI](./CODEX-SETUP.md) for dual-tool workflow (optional)
3. Configure [VS Code extension](#vs-code-extension) or [Cursor IDE](#cursor-ide)
4. Read [Daily Workflow](./DAILY-WORKFLOW.md) guide
