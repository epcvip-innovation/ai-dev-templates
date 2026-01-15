# Claude Code Quickstart

Get Claude Code running in 5 minutes.

---

## What is Claude Code?

Claude Code is an AI coding assistant that runs in your terminal. It can:
- Read and understand your entire codebase
- Write, edit, and refactor code
- Run terminal commands
- Help you build software faster

---

## Prerequisites

Before installing, verify you have:

```bash
# Node.js 18 or higher
node --version    # Should show v18.x.x or higher

# npm (comes with Node.js)
npm --version     # Should show 8.x.x or higher
```

**Don't have Node.js?** Install from [nodejs.org](https://nodejs.org/) (LTS version recommended).

**Authentication** - You'll need ONE of:
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))
- Claude Max subscription (uses OAuth)

---

## Install (2 minutes)

```bash
npm install -g @anthropic-ai/claude-code
```

Verify installation:
```bash
claude --version
```

---

## Authenticate (2 minutes)

Run the authentication command:
```bash
claude auth
```

This opens a browser window. Choose your auth method:
- **API Key**: Paste your Anthropic API key
- **Claude Max**: Sign in with your Anthropic account

---

## Verify It Works (1 minute)

Navigate to any project and ask Claude a question:

```bash
cd ~/any-project
claude "What files are in this directory?"
```

You should see Claude respond with a list of files.

**That's it! Claude Code is ready to use.**

---

## First Things to Try

```bash
# Ask about your codebase
claude "Explain the structure of this project"

# Get help with a task
claude "How do I add a new API endpoint?"

# Let Claude write code
claude "Create a function that validates email addresses"

# Run a built-in command
claude "/help"
```

---

## Next Steps

| What You Want | Where to Go |
|---------------|-------------|
| Set up a project properly | [New Project Setup](./NEW-PROJECT-SETUP.md) (30 min) |
| Learn slash commands | [Slash Commands](../../templates/slash-commands/README.md) |
| Understand best practices | [CLAUDE.md Guidelines](../../templates/claude-md/README.md) |
| Full dev environment setup | [New PC Setup](../setup-guides/NEW-PC-SETUP.md) (90 min) |

---

## Troubleshooting

### "command not found: claude"

npm's global bin directory isn't in your PATH. Fix:
```bash
# Find where npm installs global packages
npm config get prefix

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$(npm config get prefix)/bin"
```

### Authentication issues

```bash
# Re-run auth
claude auth

# Or check current auth status
claude auth status
```

### Permission errors on install

```bash
# Use sudo (Linux/macOS)
sudo npm install -g @anthropic-ai/claude-code

# Or fix npm permissions (better long-term)
# See: https://docs.npmjs.com/resolving-eacces-permissions-errors
```

---

## Learn More

- [Official Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Templates Library](../../templates/README.md)

---

**Time to complete**: ~5 minutes
**Last updated**: January 2026
