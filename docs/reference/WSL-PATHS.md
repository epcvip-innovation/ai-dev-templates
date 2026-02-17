# WSL Paths Reference Guide

**Last Updated**: 2025-11-16

Complete reference for understanding and using filesystem paths in WSL (Windows Subsystem for Linux).

---

## Overview

WSL creates a bridge between Windows and Linux filesystems, which means understanding **two different path systems**:

1. **Linux paths** (in WSL): `~/repos` or `/home/YOUR_USERNAME/repos`
2. **Windows paths**: `C:\Users\YOUR_USERNAME\repos`
3. **Windows accessing WSL**: `\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos`
4. **WSL accessing Windows**: `/mnt/c/Users/YOUR_USERNAME/repos`

---

## Path Syntax Quick Reference

| Context | Path Format | Example | Speed |
|---------|-------------|---------|-------|
| **WSL (Linux)** | `~/` or `/home/user/` | `~/repos/project` | Fast (2.4 GB/s) |
| **Windows→WSL** | `\\wsl.localhost\Distribution\` | `\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos` | Fast |
| **Windows→WSL (Legacy)** | `\\wsl$\Distribution\` | `\\wsl$\Ubuntu\home\YOUR_USERNAME\repos` | Fast |
| **WSL→Windows** | `/mnt/c/`, `/mnt/d/` | `/mnt/c/Users/YOUR_USERNAME/repos` | Slow (200 MB/s) |
| **Windows native** | `C:\`, `D:\` | `C:\Users\YOUR_USERNAME\repos` | Slow |

---

## Linux Filesystem (Primary for Development)

### Structure

```
~/                          # User home (or /home/YOUR_USERNAME/)
  ├── repos/              # All development projects (FAST)
  │   ├── project1/
  │   ├── project2/
  │   └── ai-dev-templates/
  ├── bin/                # Custom scripts
  ├── knowledge-base/     # Documentation symlinks
  └── .bashrc             # Shell configuration
```

### Usage

```bash
# Navigate
cd ~                    # Go to home
cd ~/repos              # Go to repos
cd ~/repos/project1     # Go to specific project

# Create directories
mkdir -p ~/repos/new-project

# List files
ls ~/repos
```

### Performance

- **Read/Write**: ~2.4 GB/s (measured with `perf --disk`)
- **Git operations**: Fast (native Linux filesystem)
- **File searches**: Fast (`grep`, `find`)

**Recommendation**: Keep all code repositories here.

---

## Windows Accessing WSL

### Modern Path (Preferred)

```
\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos
```

**How to access**:
1. Open Windows Explorer
2. Type in address bar: `\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos`
3. Or navigate from Network locations

**Features**:
- Works in all Windows apps
- Drag & drop support
- Direct file editing
- Fast access

### Legacy Path (Still Works)

```
\\wsl$\Ubuntu\home\YOUR_USERNAME\repos
```

**Note**: `\\wsl$\` is older syntax, still supported. Use `\\wsl.localhost\` for new work.

### From PowerShell

```powershell
# Access WSL files
cd \\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos

# Or use wsl command
wsl ls ~/repos
```

---

## WSL Accessing Windows

### Structure

```
/mnt/c/                   # C: drive
  ├── Users/
  │   └── YOUR_USERNAME/
  │       ├── Documents/
  │       ├── Downloads/
  │       └── Desktop/
  ├── Program Files/
  └── Windows/

/mnt/d/                   # D: drive (if exists)
```

### Usage

```bash
# Navigate to Windows Documents
cd /mnt/c/Users/YOUR_USERNAME/Documents

# List Windows files
ls /mnt/c/Users/YOUR_USERNAME/Downloads

# Access Windows programs
/mnt/c/Program\ Files/SomeApp/app.exe
```

### Performance

- **Read/Write**: ~200 MB/s (10x slower than Linux FS)
- **Git operations**: Slow
- **File searches**: Slow

**Recommendation**: Only for accessing Windows-specific files, not for development.

---

## Performance Comparison

### Test Results (from `perf --disk`)

```
Write Test (1GB file):
  Linux FS (~):      2.4 GB/s  ✅ Fast
  Windows FS (/mnt/c): 200 MB/s  ⚠️ Slow (10x slower)

Read Test:
  Linux FS (~):      2.4 GB/s  ✅ Fast
  Windows FS (/mnt/c): 200 MB/s  ⚠️ Slow (10x slower)

Git Clone (large repo):
  Linux FS (~):      ~30 seconds  ✅ Fast
  Windows FS (/mnt/c): ~5 minutes   ⚠️ Slow (10x slower)
```

**Source**: [Microsoft WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/compare-versions#performance-across-os-file-systems)

---

## Where to Store What

### ✅ Store in Linux FS (~/repos/)

- **All code repositories**
- **Development projects**
- **Git repos**
- **Build artifacts**
- **Node modules**
- **Virtual environments**

**Why**: 10x faster file I/O

### ⚠️ Store in Windows FS (/mnt/c/)

- **Windows-only apps data**
- **Documents you edit in Windows apps**
- **Files shared with Windows tools**
- **One-off scripts that don't need performance**

**Why**: Accessible from Windows without WSL path syntax

### 🔄 Access From Both

- **Documentation** (can be symlinked)
- **Configuration files** (choose primary location)
- **Shared data files** (if performance not critical)

---

## Common Patterns

### Pattern 1: All Development in WSL

```bash
# All code
~/repos/project1
~/repos/project2
~/repos/dev-setup

# Access from Windows
\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos\project1
```

**Best for**: Fast development, Linux tooling

### Pattern 2: Mixed (Not Recommended)

```bash
# Some code in WSL
~/repos/linux-project

# Some code in Windows
/mnt/c/Users/YOUR_USERNAME/repos/windows-project
```

**Issues**: Inconsistent performance, confusing paths

### Pattern 3: Windows with WSL Access (Not Recommended for Dev)

```bash
# All code in Windows
/mnt/c/Users/YOUR_USERNAME/repos/project

# Access via WSL
cd /mnt/c/Users/YOUR_USERNAME/repos/project
```

**Issues**: 10x slower file operations

---

## Path Translation Examples

### Example 1: Project in WSL

| View From | Path |
|-----------|------|
| WSL | `~/repos/my-project` |
| WSL (absolute) | `~/repos/my-project` or `/home/YOUR_USERNAME/repos/my-project` |
| Windows Explorer | `\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos\my-project` |
| PowerShell | `\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos\my-project` |
| Cursor (WSL mode) | `~/repos/my-project` or `/home/YOUR_USERNAME/repos/my-project` |

### Example 2: File in Windows

| View From | Path |
|-----------|------|
| Windows Explorer | `C:\Users\YOUR_USERNAME\Documents\file.txt` |
| PowerShell | `C:\Users\YOUR_USERNAME\Documents\file.txt` |
| WSL | `/mnt/c/Users/YOUR_USERNAME/Documents/file.txt` |
| Bash script | `/mnt/c/Users/YOUR_USERNAME/Documents/file.txt` |

---

## Common Commands

### From WSL

```bash
# Open Windows Explorer in current WSL directory
explorer.exe .

# Open Windows app
/mnt/c/Program\ Files/App/app.exe

# Access Windows file
cat /mnt/c/Users/YOUR_USERNAME/file.txt

# Copy from Windows to WSL
cp /mnt/c/Users/YOUR_USERNAME/file.txt ~/
```

### From Windows

```powershell
# Run WSL command
wsl ls ~/repos

# Access WSL file
type \\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos\file.txt

# Copy from WSL to Windows
copy \\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos\file.txt C:\Users\YOUR_USERNAME\
```

---

## Troubleshooting

### Issue: Slow git operations

**Cause**: Repository on Windows filesystem (`/mnt/c/`)

**Solution**:
```bash
# Move to Linux filesystem
mv /mnt/c/Users/YOUR_USERNAME/repos/project ~/repos/
cd ~/repos/project
git status  # Much faster!
```

### Issue: Permission denied

**Cause**: File owned by Windows, WSL can't modify

**Solution**:
```bash
# Change ownership (for files in WSL)
sudo chown -R $USER:$USER ~/repos/project

# Or keep in Windows, edit from Windows
```

### Issue: Line ending issues (CRLF vs LF)

**Cause**: Windows uses CRLF (`\r\n`), Linux uses LF (`\n`)

**Solution**:
```bash
# Configure git to use LF
git config --global core.autocrlf input

# Convert existing files
find . -type f -exec dos2unix {} \;
```

### Issue: Can't find \\wsl.localhost\

**Cause**: WSL not running or old Windows version

**Solution**:
```bash
# Start WSL
wsl

# Update Windows (need recent build for \\wsl.localhost)

# Or use legacy path
\\wsl$\Ubuntu\home\YOUR_USERNAME\repos
```

---

## Best Practices

### 1. Keep Code in Linux FS

```bash
# Good
~/repos/project  # Fast

# Bad
/mnt/c/Users/YOUR_USERNAME/repos/project  # Slow
```

### 2. Use Relative Paths in Scripts

```bash
# Good (portable)
cd ~/repos
./script.sh

# Bad (breaks if moved)
cd ~/repos
./script.sh
```

### 3. Use $HOME Instead of Hard-coded Paths

```bash
# Good
cd $HOME/repos

# Bad
cd ~/repos
```

### 4. Access Windows Files Read-Only When Possible

```bash
# Reading is fine
cat /mnt/c/Users/YOUR_USERNAME/file.txt

# Writing can have permission issues
echo "data" > /mnt/c/Users/YOUR_USERNAME/file.txt  # May fail
```

---

## See Also

**Setup Guides**:
- [Why WSL?](../decisions/why-wsl.md) - Decision rationale
- [Daily Workflow](../setup-guides/DAILY-WORKFLOW.md) - Using paths daily
- [Cursor WSL Setup](../setup-guides/CURSOR-WSL-SETUP.md) - IDE integration

**Reference**:
- [Commands Reference](./COMMANDS.md) - Available commands

**Official**:
- [Microsoft WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [WSL File System](https://learn.microsoft.com/en-us/windows/wsl/filesystems)
- [WSL Performance](https://learn.microsoft.com/en-us/windows/wsl/compare-versions#performance-across-os-file-systems)

---

**Quick Reference**:
- **Fast**: `~/repos/` (Linux FS)
- **Slow**: `/mnt/c/` (Windows FS)
- **Windows access**: `\\wsl.localhost\Ubuntu\home\YOUR_USERNAME\repos`
- **Always check**: `pwd` to see where you are

