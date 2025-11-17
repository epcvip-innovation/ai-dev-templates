# Scripts Reference

Detailed documentation for the `dev` and `perf` scripts used in this WSL2 development environment.

---

## `scripts/dev` - Primary Project Launcher

The main workflow script that launches AI assistants and IDE.

### Usage

```bash
dev <project-name> [mode] [options]
```

### Modes

| Mode | Description | Opens |
|------|-------------|-------|
| `claude` | Claude Code (default) | Claude Code CLI session |
| `codex` | Codex | Codex CLI session |
| `cursor` | Cursor IDE | Cursor IDE (Remote-WSL) |

### Options

| Option | Description |
|--------|-------------|
| `+kb` or `+knowledge-base` | *(Legacy)* Symlinks knowledge base into project - consider using `knowledge` command instead |

### Architecture Details

**Windows Integration**:
- Uses Cursor CLI with Remote-WSL connection
- Cursor runs in WSL context with `[WSL: Ubuntu]` indicator
- AI tools run natively in WSL

**Knowledge Base Linking** (with +kb option):
- Creates symlinks in project directory pointing to `~/knowledge-base/`
- Automatically updates `.git/info/exclude` to prevent accidental commits
- Claude launched with `--add-dir "$HOME/knowledge-base"` flag

### Examples

**Start Claude Code**:
```bash
dev my-project claude
```

**Start Codex**:
```bash
dev my-project codex
```

**Open Cursor IDE**:
```bash
dev my-project cursor
```

**With knowledge base context**:
```bash
dev my-project claude +kb              # Claude with KB
dev my-project claude +knowledge-base  # Same as +kb
```

### Common Workflows

**Daily Development**:
```bash
# Start Claude Code
dev my-project claude

# Or open Cursor
dev my-project cursor

# Exit when done
exit
```

**Quick Fixes**:
```bash
# Just Claude for quick changes
dev my-project claude

# Work on changes, then exit
exit
```

**Research with Knowledge Base**:
```bash
# Use knowledge command
knowledge                             # Opens docs repo with Claude Code

# Or add KB to specific project
dev my-project claude +kb
```

### Troubleshooting

**Cursor doesn't show [WSL: Ubuntu] indicator**:
- The `cursor` command should automatically use Remote-WSL
- If it doesn't, manually connect: `Ctrl+Shift+P` → "Remote-WSL: New Window"
- Verify extension installed: "Cursor Remote WSL"
- First connection may take 1-2 minutes (installs VS Code Server)

**Cursor terminal shows no output**:
- Check for `[WSL: Ubuntu]` indicator in bottom-left corner
- If missing, use Remote-WSL connection (see above)
- Terminal profile should be "WSL Bash" (check with `Ctrl+Shift+P` → "Terminal: Select Default Profile")
- See: [NEW-PC-SETUP.md](../setup-guides/NEW-PC-SETUP.md#cursor-terminal-shows-no-output-wsl) for full troubleshooting

**Claude/Codex not found**:
```bash
# Check if installed
which claude
which codex

# Install if missing - see setup guides
```

---

## `scripts/perf` - Performance Monitor

Quick system health check for WSL2 environment.

### Usage

```bash
perf              # Basic check (memory, CPU, sessions)
perf --disk       # Includes disk speed comparison (Linux FS vs Windows FS)
```

### What It Monitors

**Always Shown**:
- Memory usage (used/total, swap)
- CPU cores and load average
- Running Claude/Codex processes

**With `--disk` Flag**:
- Linux filesystem I/O speed (`~/repos/` - expected ~2.4 GB/s)
- Windows filesystem I/O speed (`/mnt/c/` - expected ~200 MB/s)
- Performance comparison (should show ~10x difference)

### Example Output

**Basic check**:
```bash
$ perf

=== System Performance ===
Memory: 8.2GB / 24GB (34%)
Swap: 0GB / 8GB
CPU: 32 cores, load average: 2.4, 2.1, 1.8

=== AI Processes ===
Claude processes: 2
Codex processes: 1
```

**With disk check**:
```bash
$ perf --disk

=== System Performance ===
Memory: 8.2GB / 24GB (34%)
Swap: 0GB / 8GB
CPU: 32 cores, load average: 2.4, 2.1, 1.8

=== AI Processes ===
Claude processes: 2
Codex processes: 1

=== Disk I/O Performance ===
Linux FS (~/repos/): 2.4 GB/s
Windows FS (/mnt/c/): 220 MB/s
Performance ratio: 10.9x faster on Linux FS
```

### Use Cases

**Daily health check**:
```bash
# Quick status before starting work
perf
```

**Investigating slowness**:
```bash
# Check if memory is exhausted
# Check if too many AI processes running
# Check CPU load
perf
```

**Verifying filesystem performance**:
```bash
# Ensure projects are on fast Linux FS
# Verify WSL2 performance is optimal
perf --disk
```

**Cleanup check**:
```bash
# See which AI processes are still running
perf

# Clean up if needed
pkill claude
pkill codex
```

### Performance Baselines

**Expected Values**:
- Memory: 1-2GB typical usage, 24GB available
- CPU load: <5 normal, >10 indicates heavy processing
- Linux FS: ~2.4 GB/s (SSD performance)
- Windows FS: ~200 MB/s (WSL2 overhead)

**Warning Signs**:
- Memory >20GB: Possible memory leak, consider `wsl --shutdown` (from PowerShell)
- CPU load >15: Heavy processing, might slow AI responses
- Linux FS <1 GB/s: Disk issues or resource contention
- Too many AI processes: Clean up with `pkill claude` or `pkill codex`

---

## Script Locations

**Installation**:
- `~/bin/dev` - Installed script (symlink or copy)
- `~/bin/perf` - Installed script (symlink or copy)

**Source**:
- `~/repos/ai-dev-templates/scripts/dev` - Source file
- `~/repos/ai-dev-templates/scripts/perf` - Source file

**Creating Your Own Global Commands:**

See [GLOBAL-CLI-SETUP.md](./GLOBAL-CLI-SETUP.md) for the complete pattern to make any repository script globally available as a CLI command.

**Editing**:
```bash
# Edit source file
vim ~/repos/dev-setup/scripts/dev

# Copy to installation (if not symlinked)
cp ~/repos/dev-setup/scripts/dev ~/bin/dev

# Or create symlink (recommended)
ln -sf ~/repos/dev-setup/scripts/dev ~/bin/dev
```

---

## Related Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Quick reference and project context
- **[README.md](./README.md)** - Main documentation with setup instructions
- **[DEVELOPMENT-ENVIRONMENT.md](./DEVELOPMENT-ENVIRONMENT.md)** - Complete system architecture
- **[NEW-PC-SETUP.md](./NEW-PC-SETUP.md)** - Setting up these scripts on a new machine
