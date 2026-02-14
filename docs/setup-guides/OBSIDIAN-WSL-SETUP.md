# Obsidian in WSL Setup
**Date Configured:** September 2025 | **Last Reviewed:** February 2026
**Purpose:** Run Obsidian natively in WSL to avoid Windows filesystem access issues

## Why Obsidian in WSL?

When documentation repos are in WSL, Windows Obsidian cannot access them properly due to:
- EISDIR errors when trying to watch WSL directories
- Severe performance issues with `\\wsl$\` paths
- File watcher failures

Running Obsidian inside WSL with WSLg (GUI support) provides:
- Native filesystem access (fast)
- Full functionality
- Windows GUI experience
- No compatibility issues

## Installation

### Prerequisites
- WSLg enabled (check with `ls /tmp/.X11-unix`)
- Ubuntu 24.04 or similar

### Install Steps

```bash
# Download Obsidian
cd ~/Downloads
wget https://github.com/obsidianmd/obsidian-releases/releases/download/v1.9.12/obsidian_1.9.12_amd64.deb

# Install dependencies
sudo apt update
sudo apt install libasound2t64 ffmpeg

# Install Obsidian
sudo apt install ./obsidian_1.9.12_amd64.deb

# Launch
obsidian &
```

## Usage

### Quick Launch Script
Created at `~/bin/obs`:
```bash
#!/bin/bash
echo "Launching Obsidian (WSL version)..."
obsidian > /dev/null 2>&1 &
echo "✅ Obsidian launched in background"
```

### Daily Workflow

1. **Open Obsidian**: Run `obs` or `obsidian &` in terminal
2. **Vaults location**: `~/repos-epcvip/docs/[vault-name]`
3. **GUI appears**: On Windows desktop via WSLg
4. **Performance**: Native Linux filesystem speed

### Vault Paths

- Personal docs: `~/repos-epcvip/docs/personal-docs`
- Company docs: `~/repos-epcvip/docs/company-shared-docs`
- Data docs: `~/repos-epcvip/docs/query-docs`

## Integration with Workflow

### Home Computer
- WSL: Claude Code + Obsidian (both in WSL)
- Windows: Cursor IDE, browsers, Slack

### Work Computer
- Same setup - pull repos and work

### Git Workflow
```bash
# Before leaving location
cd ~/repos-epcvip/docs/personal-docs
git add . && git commit -m "changes"
git push

# At new location
git pull
```

## Benefits

1. **No freezing**: Eliminates 9P protocol issues
2. **Fast access**: Native filesystem speed
3. **Single source**: One location for all docs
4. **GUI experience**: Looks/feels like Windows app
5. **Compatible**: Works with Claude Code setup

## Troubleshooting

### Missing libraries error
```bash
sudo apt install libasound2t64 libgbm1 libnss3 libgtk-3-0t64
```

### Can't see GUI
Ensure WSLg is working:
```bash
ls /tmp/.X11-unix  # Should show X0
```

### Launch from Windows
Create PowerShell shortcut:
```powershell
wsl.exe obsidian
```

## Related Documentation

- [WSL Claude Freezing Fix](./WSL-CLAUDE-FREEZING-FIX.md)
- [Development Environment](./DEVELOPMENT-ENVIRONMENT.md)
- [README](./README.md)