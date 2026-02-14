# Daily Workflow Guide

**Last Updated**: 2026-02-13

A practical guide to the daily development workflow using Claude Code, Codex, and Cursor IDE.

> **New here?** See [Getting Started](../getting-started/SETUP-GUIDE-2026.md) for platform-agnostic installation. This guide covers everyday usage patterns once tools are installed.

---

## Overview

**Environment**: Windows 11 + WSL2 (Ubuntu) + Cursor IDE  
**AI Tools**: Claude Code + Codex  
**Primary IDE**: Cursor with Remote-WSL extension

**Why this setup?** See [Why WSL?](../decisions/why-wsl.md) for the full rationale.

---

## Quick Start

### Starting a Development Session

```bash
# Option 1: Just Claude Code
cd ~/repos/your-project
claude

# Option 2: Just Codex
cd ~/repos/your-project
codex

# Option 3: Cursor IDE
cd ~/repos/your-project
cursor .  # Opens via Remote-WSL automatically

# Option 4: Using the dev script (Claude + Codex + Cursor)
dev your-project split
```

**Note**: The `dev` script is a convenience wrapper. You can use the tools individually.

---

## Common Workflows

### 1. Code with AI Assistance

**Using Claude Code**:
```bash
cd ~/repos/your-project
claude
```

Claude Code opens in terminal, provides AI pair programming, can edit files, run commands, etc.

**Using Codex**:
```bash
cd ~/repos/your-project
codex
```

Similar to Claude, alternative AI assistant.

**Using Both** (side-by-side):
Open two terminal windows or use the `dev` script to manage both.

**Setup Required**: See [Claude Code Setup](./CLAUDE-CODE-SETUP.md) and [Codex Setup](./CODEX-SETUP.md)

---

### 2. Edit Code in Cursor IDE

**From WSL terminal**:
```bash
cd ~/repos/your-project
cursor .
```

**From Windows**:
1. Open Cursor
2. `Ctrl+Shift+P` → "Remote-WSL: New Window"
3. Navigate to `~/repos/your-project`

**Verify Connection**:
- Check for `[WSL: Ubuntu]` indicator in bottom-left corner
- Terminal should show `adams@DESKTOP-...` (Linux prompt)

**Setup Required**: See [Cursor WSL Setup](./CURSOR-WSL-SETUP.md)

---

### 3. Working with Files

**From Windows Explorer**:
```
\\wsl.localhost\Ubuntu\home\adams\repos
```

**From WSL**:
```bash
# All repos
cd ~/repos

# Specific project
cd ~/repos/your-project

# Open in Windows Explorer from WSL
explorer.exe .
```

**Performance Note**: Always keep code in `~/repos/` (WSL filesystem), not `/mnt/c/` (Windows filesystem). See [WSL Paths Reference](../reference/WSL-PATHS.md) for details.

---

### 4. Running Commands

**In Claude Code / Codex**:
Commands run natively in WSL. Just type them.

**In Cursor Terminal**:
If connected via Remote-WSL, commands run natively in WSL.

**Verify**:
```bash
echo $HOME  # Should show /home/YOUR_USERNAME
pwd         # Should show Linux paths
```

---

## Daily Scenarios

### Scenario A: Start New Feature

```bash
# 1. Navigate to project
cd ~/repos/your-project

# 2. Start Claude for planning
claude
# Ask Claude to help plan the feature

# 3. Open Cursor for implementation
cursor .
# Implement while referencing Claude's plan

# 4. Test with Codex
codex
# Ask Codex to review or suggest tests
```

### Scenario B: Code Review with AI

```bash
# 1. Open Cursor in project
cd ~/repos/your-project
cursor .

# 2. Run Claude in another terminal for review
claude
# Ask: "Review the changes in [file]"
```

### Scenario C: Quick Fix

```bash
# Just use Claude directly
cd ~/repos/your-project
claude
# Make the fix, test, done
```

---

## Tool Integration

### Claude Code Features

- **AI pair programming**: Ask questions, get suggestions
- **File editing**: Claude can directly edit files
- **Command execution**: Run tests, git commands, etc.
- **Knowledge base**: Add `--add-dir` for project context

**Common commands**:
```bash
# Start in current directory
claude

# With additional context
claude --add-dir ~/knowledge-base

# Exit
exit
```

### Codex Features

- Similar to Claude Code
- Alternative AI model
- Use for comparison or different perspectives

### Cursor IDE Features

- **AI agent**: Built-in AI for code completion and suggestions
- **Remote-WSL**: Native Linux development from Windows UI
- **Terminal**: Integrated terminal runs in WSL
- **Git**: Native git operations in WSL

**Keyboard shortcuts**:
- `Ctrl+Shift+P`: Command palette
- `` Ctrl+` ``: Toggle terminal
- `Ctrl+B`: Toggle sidebar

---

## Common Issues

### Issue: Cursor terminal shows no output

**Solution**: Verify WSL connection
```
1. Check for [WSL: Ubuntu] indicator in bottom-left
2. If missing: Ctrl+Shift+P → "Remote-WSL: New Window"
3. Verify terminal profile: Ctrl+Shift+P → "Terminal: Select Default Profile" → "WSL Bash"
```

See [Cursor WSL Setup](./CURSOR-WSL-SETUP.md#troubleshooting) for details.

### Issue: Slow file operations

**Solution**: Ensure code is in WSL filesystem
```bash
pwd  # Should show ~/repos/... or /home/YOUR_USERNAME/repos/...
     # NOT /mnt/c/...
```

See [WSL Paths Reference](../reference/WSL-PATHS.md#performance) for explanation.

### Issue: Claude Code or Codex not found

**Solution**: Install using the [Getting Started guide](../getting-started/SETUP-GUIDE-2026.md) (covers all platforms).

```bash
# Check if installed
which claude
which codex
```

See setup guides: [Claude Code](./CLAUDE-CODE-SETUP.md) | [Codex](./CODEX-SETUP.md)

---

## See Also

**Setup Guides**:
- [Claude Code Setup](./CLAUDE-CODE-SETUP.md) - Installing and configuring Claude Code
- [Codex Setup](./CODEX-SETUP.md) - Installing and configuring Codex
- [Cursor WSL Setup](./CURSOR-WSL-SETUP.md) - Setting up Cursor with WSL
- [New PC Setup](./NEW-PC-SETUP.md) - Complete new machine setup

**Reference**:
- [WSL Paths Reference](../reference/WSL-PATHS.md) - Understanding WSL filesystem paths
- [Commands Reference](../reference/COMMANDS.md) - All available commands
- [Why WSL?](../decisions/why-wsl.md) - Architectural decision rationale

**Optional Tools**:
- [Obsidian WSL Setup](./OBSIDIAN-WSL-SETUP.md) - Note-taking and documentation editor

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│ Common Commands                                      │
├─────────────────────────────────────────────────────┤
│ claude              Start Claude Code                │
│ codex               Start Codex                      │
│ cursor .            Open Cursor (Remote-WSL)         │
│ dev project claude  Start Claude in project           │
│ explorer.exe .      Open in Windows Explorer         │
│ perf                Check system performance         │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Paths                                                │
├─────────────────────────────────────────────────────┤
│ From WSL:     ~/repos/project                        │
│ From Windows: \\wsl.localhost\Ubuntu\home\YOUR_USERNAME\... │
│ Windows FS:   /mnt/c/Users/YOUR_USERNAME/...         │
└─────────────────────────────────────────────────────┘
```

---

**Next Steps**: 
1. Complete [New PC Setup](./NEW-PC-SETUP.md) if haven't already
2. Set up [Claude Code](./CLAUDE-CODE-SETUP.md) and [Codex](./CODEX-SETUP.md)
3. Configure [Cursor WSL](./CURSOR-WSL-SETUP.md)
4. Start coding!

