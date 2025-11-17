# Claude Code Setup Guide

[← Back to Main README](../../README.md) | [Advanced Configuration →](../reference/CLAUDE-CODE-CONFIG.md)

**Last Updated**: 2025-11-16  
**Time Required**: 5-10 minutes

Complete guide to installing and configuring Claude Code CLI for AI-assisted development.

---

## What is Claude Code?

Claude Code is Anthropic's CLI tool for AI pair programming. It provides:
- AI assistance directly in terminal
- File editing capabilities
- Command execution
- Context-aware suggestions

**Official Documentation**: [https://docs.claude.com/en/docs/claude-code](https://docs.claude.com/en/docs/claude-code)

---

## Prerequisites

-Windows 11 with WSL2 (Ubuntu) OR Windows native
- Node.js 18+ (for npm)
- Anthropic API key OR Claude Pro/Max subscription

**Check if already installed**:
```bash
which claude
claude --version
```

---

## Installation

### Option A: Via npm (Recommended)

```bash
# Install globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

### Option B: Alternative installation methods

Check official documentation for other installation methods:
[https://docs.claude.com/en/docs/claude-code/installation](https://docs.claude.com/en/docs/claude-code/installation)

---

## Authentication

### Method 1: OAuth (Recommended)

```bash
# Start Claude
claude

# Follow browser prompts to authenticate
# Choose your account type:
# - Anthropic Console (API key)
# - Claude Pro
# - Claude Max
# - Claude Team
# - Claude Enterprise
```

### Method 2: API Key

```bash
# Set environment variable
export ANTHROPIC_API_KEY="your-api-key-here"

# Or add to ~/.bashrc
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

### Issue: Claude freezes every ~10 seconds

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

**Note**: Modern WSL (2025) typically doesn't have this issue.

### Issue: Command not found

**Solution**:
```bash
# Verify npm global packages location
npm config get prefix

# Should be /usr/local or ~/.npm-global

# If wrong, fix npm prefix
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Reinstall
npm install -g @anthropic-ai/claude-code
```

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

### With Cursor IDE

1. Run Claude in one terminal
2. Open Cursor in another window
3. Use Claude for planning, Cursor for implementation

### With Codex

1. Use both for comparison
2. Claude for one approach, Codex for another
3. Side-by-side in terminal (split window)

### With Knowledge Base

```bash
# Link knowledge base to project
dev your-project split +kb

# Or manually
cd ~/repos/your-project
ln -s ~/knowledge-base .
claude --add-dir ./knowledge-base
```

---

## Advanced Configuration

### Custom Skills (October 2025 Feature)

**What are Skills?**: Modular task knowledge packs that Claude loads dynamically.

**Enable Skills** (Pro/Max/Team/Enterprise):
```bash
claude
/settings
# Toggle "Skills" on
```

**Create Custom Skill**:
```bash
# Create skills directory
mkdir -p ~/.claude/skills/my-project

# Create instructions
cat > ~/.claude/skills/my-project/instructions.md << 'EOF'
# My Project Coding Standards
- Use TypeScript strict mode
- Follow ESLint rules
- Write tests for all functions
EOF

# Load in Claude
/skill load ~/.claude/skills/my-project
```

### MCPs (Model Context Protocol)

**Best Practice 2025**: Only enable MCPs you actively need (saves tokens).

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

Check with `perf` script:
```bash
perf
# Shows Claude instances and resource usage
```

---

## Uninstallation

### Remove Claude Code

```bash
# Uninstall package
npm uninstall -g @anthropic-ai/claude-code

# Remove configuration (optional)
rm -rf ~/.claude
```

---

## See Also

**Related Guides**:
- [Daily Workflow](./DAILY-WORKFLOW.md) - Using Claude in daily development
- [Codex Setup](./CODEX-SETUP.md) - Alternative AI assistant
- [Cursor WSL Setup](./CURSOR-WSL-SETUP.md) - IDE integration

**Reference**:
- [Commands Reference](../reference/COMMANDS.md) - All available commands
- [Claude Code Config](../reference/CLAUDE-CODE-CONFIG.md) - Advanced configuration

**Official**:
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Anthropic Console](https://console.anthropic.com/)

---

**Next Steps**:
1. ✅ Claude Code installed
2. Set up [Codex](./CODEX-SETUP.md) (optional)
3. Configure [Cursor IDE](./CURSOR-WSL-SETUP.md)
4. Read [Daily Workflow](./DAILY-WORKFLOW.md) guide

