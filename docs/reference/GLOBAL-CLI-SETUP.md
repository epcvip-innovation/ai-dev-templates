# Global CLI Commands Setup

How to make repository scripts globally available as CLI commands.

---

## The Pattern

**Problem:** You have useful scripts in a repo (`/path/to/repo/scripts/my-tool`) but need to run them from anywhere.

**Solution:** Symlinks in `~/bin/` pointing to your scripts.

**Why this works:**
- `~/bin/` is already in PATH (via `~/.profile`)
- Works in all shell types (login, non-login, interactive, WSL)
- Single source of truth (scripts stay in repo, symlinks just point there)
- Standard Unix pattern (used by npm, pipx, poetry, homebrew)

---

## Quick Start

**1. Create your script in your repo:**
```bash
# Example: /home/user/repos/my-tool/scripts/my-command
#!/bin/bash
echo "Hello from my-command!"
```

**2. Make it executable:**
```bash
chmod +x /home/user/repos/my-tool/scripts/my-command
```

**3. Create symlink in ~/bin/:**
```bash
ln -sf /home/user/repos/my-tool/scripts/my-command ~/bin/my-command
```

**4. Use from anywhere:**
```bash
cd ~/Documents
my-command  # Works!
```

---

## Real Example: Query Validator

From `data-query-tool` - shows complete pattern with wrapper scripts.

### Structure
```
data-query-tool/
├── scripts/
│   ├── validate-query           # Wrapper script
│   ├── validate-and-execute     # Wrapper script
│   ├── validate_query.py        # Actual Python implementation
│   └── validate_and_execute.py
└── core/                        # Python modules
```

### Wrapper Script Pattern

**Key challenge:** Python scripts need repo root for imports and venv.

**Solution:** Wrapper that resolves symlinks, finds repo, activates venv.

**Template:**
```bash
#!/bin/bash

# Resolve symlinks to find actual script location
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
REPO_DIR="$(dirname "$SCRIPT_DIR")"  # Go up to repo root

# Save current directory
ORIGINAL_DIR="$(pwd)"

# Convert relative paths to absolute
QUERY_PATH="$1"
if [[ ! "$QUERY_PATH" = /* ]]; then
    QUERY_PATH="$ORIGINAL_DIR/$QUERY_PATH"
fi

# Navigate to repo and activate venv
cd "$REPO_DIR" || exit 1
source venv/bin/activate

# Set PYTHONPATH for module imports
export PYTHONPATH="$REPO_DIR:$PYTHONPATH"

# Run the actual script
python scripts/actual_script.py "$QUERY_PATH"

# Cleanup
EXIT_CODE=$?
deactivate
cd "$ORIGINAL_DIR"
exit $EXIT_CODE
```

### Setup
```bash
ln -sf /home/user/repos/data-query-tool/scripts/validate-query ~/bin/validate-query
ln -sf /home/user/repos/data-query-tool/scripts/validate-and-execute ~/bin/validate-and-execute
```

### Usage
```bash
# From any directory
validate-query queries/my_query.sql
validate-and-execute queries/my_query.sql --output results.csv
```

---

## Why Symlinks (Not PATH Modification)

### ❌ Adding to PATH in ~/.bashrc Doesn't Work in WSL

**Problem:** WSL runs commands as non-interactive shells.
- `~/.bashrc` is NOT loaded
- PATH modifications in bashrc are invisible
- This is documented WSL behavior (2024-2025)

**Example that fails:**
```bash
# In ~/.bashrc
export PATH="/home/user/repos/my-tool/scripts:$PATH"

# Later, in WSL/Claude Code
my-command
# Error: command not found
```

### ✅ Symlinks in ~/bin/ Work Everywhere

**Why:**
- `~/.profile` adds `~/bin/` to PATH
- `~/.profile` IS loaded in non-interactive shells
- System PATH is always available

**Verified working in:**
- WSL interactive shells
- WSL non-interactive shells
- Claude Code bash sessions
- SSH sessions
- VS Code terminals

---

## Implementation Checklist

### For Simple Scripts (No Dependencies)

- [ ] Create script in `repo/scripts/`
- [ ] Add shebang (`#!/bin/bash` or `#!/usr/bin/env python3`)
- [ ] Make executable (`chmod +x`)
- [ ] Create symlink: `ln -sf $(pwd)/scripts/my-script ~/bin/my-script`
- [ ] Test: Run command from different directory

### For Python Scripts with venv/modules

- [ ] Create wrapper script in `repo/scripts/`
- [ ] Use `readlink -f` to resolve symlinks
- [ ] Navigate to repo root
- [ ] Activate venv
- [ ] Set PYTHONPATH
- [ ] Call actual Python script
- [ ] Deactivate and return to original dir
- [ ] Create symlink to wrapper
- [ ] Test from different directory

### For Scripts That Accept File Paths

- [ ] Convert relative paths to absolute before changing directories
- [ ] Save `$(pwd)` before any `cd` commands
- [ ] Use absolute paths when calling actual implementation

---

## Alternative Approaches

### Option A: Copy to ~/bin/
```bash
cp scripts/my-command ~/bin/
```

**Pros:** Simple, no symlink complexity
**Cons:** Must manually sync on every script update

### Option B: Add repo to PATH (doesn't work in WSL)
```bash
# In ~/.bashrc
export PATH="/home/user/repos/my-tool/scripts:$PATH"
```

**Pros:** Direct access to all scripts
**Cons:** Doesn't work in WSL non-interactive shells

### Option C: System-wide /etc/profile.d/
```bash
sudo echo 'export PATH="/path/to/scripts:$PATH"' > /etc/profile.d/my-tool.sh
```

**Pros:** Available to all users
**Cons:** Requires sudo, pollutes system, unnecessary for single-user setups

**Recommendation:** Use symlinks (Option A with automation)

---

## Troubleshooting

### Command not found

**Check if symlink exists:**
```bash
ls -la ~/bin/my-command
```

**Check if ~/bin/ is in PATH:**
```bash
echo $PATH | grep ~/bin
```

**Recreate symlink:**
```bash
ln -sf /absolute/path/to/repo/scripts/my-command ~/bin/my-command
```

### Symlink broken after moving repo

**Problem:** Symlinks point to old location.

**Fix:**
```bash
# Remove old symlinks
rm ~/bin/my-command

# Recreate from new location
cd /new/repo/location
ln -sf $(pwd)/scripts/my-command ~/bin/my-command
```

### Script runs but can't find modules/files

**Problem:** Script changing directory breaks relative paths.

**Fix in wrapper:**
```bash
# Save original directory
ORIGINAL_DIR="$(pwd)"

# Convert arguments to absolute paths BEFORE cd
ARG_PATH="$1"
if [[ ! "$ARG_PATH" = /* ]]; then
    ARG_PATH="$ORIGINAL_DIR/$ARG_PATH"
fi

# Now safe to cd
cd "$REPO_DIR"
```

### Python imports fail

**Add to wrapper:**
```bash
export PYTHONPATH="$REPO_DIR:$PYTHONPATH"
```

---

## Existing Examples in This Repo

### scripts/dev
- Symlinked to `~/bin/dev`
- Opens projects in editor with knowledge base
- Shows symlink setup for knowledge-base

### scripts/perf
- Performance monitoring tool
- Installed to PATH via symlink

See `docs/reference/COMMANDS.md` for usage.

---

## Team Workflow

**For tool creators:**
1. Create scripts in `scripts/` directory
2. Document in repo README
3. Provide symlink setup command
4. Include wrapper template if needed

**For tool users:**
1. Clone repo
2. Run provided symlink setup command
3. Commands now work globally

**Example setup script:**
```bash
#!/bin/bash
# install-commands.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ln -sf "$REPO_ROOT/scripts/command-1" ~/bin/command-1
ln -sf "$REPO_ROOT/scripts/command-2" ~/bin/command-2

echo "✅ Commands installed to ~/bin/"
echo "   command-1"
echo "   command-2"
```

---

## When to Use This Pattern

**Good fit:**
- Repository-specific tools (validators, builders, deployers)
- Python scripts with dependencies
- Scripts you run frequently from different directories
- Team tools that should "just work"

**Not needed:**
- One-off scripts
- Scripts only run from repo directory
- System tools (use package managers)
- Scripts with complex installation needs

---

## Summary

**Pattern:** Symlinks in `~/bin/` → wrapper scripts in `repo/scripts/` → actual implementation

**Benefits:**
- Works everywhere (WSL, SSH, all shells)
- Single source of truth
- No PATH hacks needed
- Standard Unix approach

**Template:**
```bash
# Create wrapper with symlink resolution
# Symlink to ~/bin/
# Done - works from anywhere
```

**Real examples:** validate-query, validate-and-execute, dev, perf
