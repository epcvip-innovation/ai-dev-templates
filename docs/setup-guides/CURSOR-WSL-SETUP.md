# Cursor + WSL Setup Guide

**Last Updated**: 2026-02-13
**Time Required**: 10-15 minutes

Complete guide to setting up Cursor IDE with WSL for native Linux development from Windows.

> **On macOS or Linux?** Install the Claude Code extension directly in Cursor (`cursor:extension/anthropic.claude-code`) — no WSL setup needed. This guide covers the **Windows + WSL** configuration specifically.

---

## What is Cursor + WSL?

**Cursor**: VS Code-based IDE with built-in AI capabilities  
**Remote-WSL Extension**: Connects Cursor (Windows) to WSL (Linux) for native development

**Benefits**:
- AI agent runs commands natively in WSL (no `wsl` wrapper)
- Fast file operations (Linux filesystem)
- Proper Linux path handling
- Consistent with Claude Code environment

**Why WSL?** See [Why WSL Decision](../decisions/why-wsl.md) for full rationale.

---

## Prerequisites

- Windows 11
- WSL2 installed and configured
- Ubuntu (or other Linux distribution) in WSL

**Verify WSL**:
```bash
# In PowerShell
wsl --list --verbose
# Should show Ubuntu with version 2
```

---

## Step 1: Install Cursor IDE

### Download and Install

1. Visit [https://cursor.sh/](https://cursor.sh/)
2. Download Windows installer
3. Run installer (install on Windows, NOT in WSL)
4. Complete installation

**Installation Location**: Cursor installs on Windows (e.g., `C:\Users\<username>\AppData\Local\Programs\cursor\`)

---

## Step 2: Install Remote-WSL Extension

### Automatic Installation (Recommended)

```bash
# From WSL terminal
cd ~/repos/your-project
cursor .
```

**What happens**:
1. Cursor detects WSL
2. Automatically installs Remote-WSL extension
3. Installs VS Code Server in WSL (one-time, 1-2 minutes)
4. Connects to WSL

**Verify**: Look for `[WSL: Ubuntu]` in bottom-left corner of Cursor

### Manual Installation

If automatic doesn't work:

1. Open Cursor (on Windows)
2. `Ctrl+Shift+P` → "Extensions: Install Extension"
3. Search for "Remote - WSL"
4. Click Install
5. Click "Install in WSL" when prompted

---

## Step 3: Connect to WSL

### Method A: From WSL Terminal (Easiest)

```bash
cd ~/repos/your-project
cursor .
```

**Result**: Cursor opens with WSL connection automatically.

### Method B: From Cursor UI

1. Open Cursor (Windows)
2. `Ctrl+Shift+P` → "Remote-WSL: New Window"
3. Select "Ubuntu" (or your WSL distribution)
4. File → Open Folder → Navigate to `~/repos/your-project` or `/home/YOUR_USERNAME/repos/your-project`

### Method C: From Windows Explorer

1. In Windows Explorer: `\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos\your-project`
2. Right-click → "Open with Cursor"
3. Cursor should detect WSL and connect

---

## Step 4: Verify Setup

### Check Connection

**Visual indicators**:
- `[WSL: Ubuntu]` in bottom-left corner of Cursor
- Status bar shows "WSL: Ubuntu"

**Test in terminal** (`` Ctrl+` ``):
```bash
# Should show Linux prompt
echo $HOME
# Output: /home/YOUR_USERNAME

pwd
# Output: ~/repos/your-project or /home/YOUR_USERNAME/repos/your-project

uname -a
# Output: Linux ...
```

### Verify Native Execution

```bash
# In Cursor terminal
which git
# Output: /usr/bin/git (NOT /mnt/c/Program Files/Git/...)

echo $PATH
# Should show Linux paths, not Windows paths
```

---

## Configuration

### Terminal Profile

Ensure Cursor uses WSL Bash:

1. `Ctrl+Shift+P` → "Terminal: Select Default Profile"
2. Select "WSL Bash" or "Ubuntu (WSL)"
3. Open new terminal (`` Ctrl+` ``)

### Settings

**Recommended settings** (`.vscode/settings.json` in your project):

```json
{
  "terminal.integrated.defaultProfile.linux": "bash",
  "files.eol": "\n",
  "git.enabled": true
}
```

---

## Usage

### Opening Projects

**From WSL**:
```bash
cd ~/repos/your-project
cursor .
```

**From Cursor**:
1. `Ctrl+Shift+P` → "Remote-WSL: Open Folder in WSL"
2. Navigate to project directory

### Using AI Agent

Cursor's AI agent runs commands in WSL automatically when connected via Remote-WSL:

1. Ask AI to run a command
2. AI executes in WSL (native Linux)
3. No `wsl` wrapper needed

### File Operations

All file operations use Linux paths:
- Fast (Linux filesystem)
- Native permissions
- No path translation

---

## Troubleshooting

### Issue: No [WSL: Ubuntu] indicator

**Symptoms**: Cursor opens but doesn't connect to WSL

**Solution**:
```bash
# Option 1: Restart Cursor and try again
cursor .

# Option 2: Manually connect
# In Cursor: Ctrl+Shift+P → "Remote-WSL: New Window"

# Option 3: Reinstall VS Code Server
# Remove ~/.vscode-server in WSL
rm -rf ~/.vscode-server
cursor .  # Will reinstall
```

### Issue: Terminal shows no output

**Symptoms**: Commands execute but show no output

**Cause**: Cursor using PowerShell instead of WSL Bash

**Solution**:
1. `Ctrl+Shift+P` → "Terminal: Select Default Profile"
2. Select "WSL Bash" or "Ubuntu (WSL)"
3. Open new terminal (`` Ctrl+` ``)
4. Test: `echo "test"` should show output

### Issue: Slow performance

**Cause**: Files on Windows filesystem (`/mnt/c/`)

**Solution**:
```bash
# Move repos to Linux filesystem
cd ~
mkdir -p repos
mv /mnt/c/Users/YOUR_USERNAME/repos/* ~/repos/

# Always work from ~/repos
pwd  # Should show ~/repos/... or /home/YOUR_USERNAME/repos/...
```

See [WSL Paths Reference](../reference/WSL-PATHS.md) for explanation.

### Issue: First connection takes long time

**Expected**: First connection installs VS Code Server (~1-2 minutes)

**Solution**: Just wait. Subsequent connections will be fast.

### Issue: "Cannot connect to WSL"

**Solution**:
```bash
# Verify WSL is running
wsl --list --running

# Restart WSL if needed (PowerShell)
wsl --shutdown
wsl

# Try connecting again
cursor .
```

---

## Best Practices

### 1. Always Use Linux Filesystem

```bash
# Good
~/repos/your-project  # Fast (2.4 GB/s)

# Bad
/mnt/c/Users/YOUR_USERNAME/repos/your-project  # Slow (200 MB/s)
```

### 2. Use cursor . Command

```bash
# From WSL, always use
cd ~/repos/your-project
cursor .

# Not from Windows Explorer (unless necessary)
```

### 3. Keep Sessions Connected

- Leave Cursor connected to WSL
- Don't disconnect/reconnect frequently
- Fast operations when staying connected

### 4. Use Integrated Terminal

- Terminal in Cursor runs in WSL automatically
- No need for separate terminal windows
- AI agent can interact with terminal

---

## Integration with Other Tools

### With Claude Code

```bash
# Terminal 1: Cursor (for implementation)
cursor .

# Terminal 2: Claude Code (for planning)
claude
```

### With Git

Git operations are native in WSL:
```bash
# In Cursor terminal (or Cursor's source control)
git status
git add .
git commit -m "message"
git push
```

No `wsl git` wrapper needed!

---

## Advanced Configuration

### Extensions in WSL

Some extensions need to be installed in WSL separately:

1. Install extension in Cursor
2. Click "Install in WSL" button when prompted
3. Extension runs in WSL context

### Custom Keybindings

Create `.vscode/keybindings.json`:
```json
[
  {
    "key": "ctrl+shift+t",
    "command": "workbench.action.terminal.new"
  }
]
```

### Workspace Settings

Per-project settings (`.vscode/settings.json`):
```json
{
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/node_modules/**": true
  },
  "search.exclude": {
    "**/node_modules": true
  }
}
```

---

## Uninstallation

### Remove Cursor

Windows: Uninstall via Add/Remove Programs

### Remove VS Code Server from WSL

```bash
rm -rf ~/.vscode-server
```

---

## See Also

**Setup Guides**:
- [Daily Workflow](./DAILY-WORKFLOW.md) - Using Cursor in daily development
- [Claude Code Setup](./CLAUDE-CODE-SETUP.md) - AI assistant setup
- [Getting Started](../getting-started/SETUP-GUIDE-2026.md) - Platform-agnostic setup

**Reference**:
- [WSL Paths Reference](../reference/WSL-PATHS.md) - Understanding paths
- [Why WSL?](../decisions/why-wsl.md) - Decision rationale
- [Commands Reference](../reference/COMMANDS.md) - Available commands

**Official**:
- [Cursor Documentation](https://cursor.sh/docs)
- [VS Code Remote-WSL](https://code.visualstudio.com/docs/remote/wsl)
- [Microsoft WSL Docs](https://learn.microsoft.com/en-us/windows/wsl/)

---

**Next Steps**:
1. ✅ Cursor installed and connected to WSL
2. Install [Claude Code](./CLAUDE-CODE-SETUP.md)
3. Read [Daily Workflow](./DAILY-WORKFLOW.md) guide
4. Start coding!

