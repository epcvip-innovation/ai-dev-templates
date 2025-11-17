# Codex Setup Guide

**Last Updated**: 2025-11-16  
**Time Required**: 5-10 minutes

Guide to installing and configuring Codex CLI for AI-assisted development.

---

## What is Codex?

Codex is OpenAI's code generation AI, available as a CLI tool for terminal-based development assistance.

**Note**: As of 2024, OpenAI's Codex API was sunset. This guide documents the setup for historical reference (as of November 2025). Consider alternatives like:
- **Claude Code** (Anthropic) - See [Claude Code Setup](./CLAUDE-CODE-SETUP.md)
- **GitHub Copilot CLI** - `gh copilot`
- **OpenAI CLI** (GPT-4) - Direct API access

**Official Documentation**: Check [OpenAI Platform Docs](https://platform.openai.com/docs) for current status.

---

## Prerequisites

- WSL2 (Ubuntu) OR Windows native
- OpenAI API key
- Node.js/npm OR Python (depending on implementation)

**Check if already installed**:
```bash
which codex
codex --version
```

---

## Installation

### Historical Installation (Reference)

**Note**: If the original Codex CLI is no longer available, consider alternatives above.

```bash
# Example installation (if still available)
npm install -g codex-cli

# OR via pip (if Python-based)
pip install openai-codex

# Verify
codex --version
```

### Alternative: OpenAI CLI

```bash
# Install OpenAI CLI (2025)
pip install openai

# Or via npm if available
npm install -g openai-cli

# Authenticate
openai api-key set YOUR_API_KEY
```

---

## Authentication

### API Key Setup

```bash
# Set environment variable
export OPENAI_API_KEY="your-api-key-here"

# Add to ~/.bashrc for persistence
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Get API Key**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## Configuration

### Basic Configuration

Codex typically stores configuration in `~/.config/codex/` or similar.

```bash
# Check config location
ls ~/.config/codex/
# Or
codex config --show
```

---

## Usage

### Basic Usage

```bash
# Start in current directory
codex

# With specific context
cd ~/repos/your-project
codex
```

### Common Commands

Similar to Claude Code:
```
help     # Show available commands
exit     # Exit Codex
```

---

## Recommended Alternatives (2025)

### Option 1: Claude Code (Primary Recommendation)

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Use instead of Codex
claude
```

**Advantages**:
- Active development
- Better code understanding
- File editing capabilities
- Maintained by Anthropic

See [Claude Code Setup](./CLAUDE-CODE-SETUP.md) for details.

### Option 2: GitHub Copilot CLI

```bash
# Install gh CLI
# See: https://cli.github.com/

# Install Copilot extension
gh extension install github/gh-copilot

# Use
gh copilot suggest "your question"
gh copilot explain "code snippet"
```

**Advantages**:
- Integrated with GitHub
- Works with Copilot subscription
- Good for git operations

### Option 3: OpenAI Direct (GPT-4)

```bash
# Use OpenAI API directly
# Create custom wrapper script
```

---

## Troubleshooting

### Issue: Codex command not found

**Solution**: Codex may no longer be available. Use alternatives:

```bash
# Install Claude Code instead
npm install -g @anthropic-ai/claude-code
claude

# Or GitHub Copilot CLI
gh extension install github/gh-copilot
```

### Issue: API authentication fails

**Solution**:
```bash
# Verify API key
echo $OPENAI_API_KEY

# Test API access
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

---

## Migration Path

If you were using Codex and need to migrate:

### To Claude Code

1. Install Claude Code: See [Claude Code Setup](./CLAUDE-CODE-SETUP.md)
2. Update `dev` script to use `claude` instead of `codex`
3. Test workflow with Claude

### To GitHub Copilot CLI

1. Install gh CLI and Copilot extension
2. Update scripts to use `gh copilot`
3. Test integration

---

## Integration with Other Tools

### With Claude Code (Recommended)

Use both side-by-side for comparison:
```bash
# Terminal 1
claude

# Terminal 2
codex  # or alternative
```

### With Cursor IDE

1. Run AI assistant in terminal
2. Use Cursor for implementation
3. Verify changes before committing

---

## Performance Tips

Similar to Claude Code:
- Keep sessions focused
- Clear context between projects
- Use version control
- Review AI suggestions before applying

---

## See Also

**Setup Guides**:
- [Claude Code Setup](./CLAUDE-CODE-SETUP.md) - Primary AI assistant (recommended)
- [Daily Workflow](./DAILY-WORKFLOW.md) - Using AI tools daily
- [Cursor WSL Setup](./CURSOR-WSL-SETUP.md) - IDE integration

**Reference**:
- [Commands Reference](../reference/COMMANDS.md) - All available commands

**Official**:
- [OpenAI Platform](https://platform.openai.com/)
- [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli)

---

**Next Steps**:
1. Consider [Claude Code](./CLAUDE-CODE-SETUP.md) as primary AI assistant
2. Configure [Cursor IDE](./CURSOR-WSL-SETUP.md)
3. Read [Daily Workflow](./DAILY-WORKFLOW.md) guide
4. Update `dev` script if switching from Codex

