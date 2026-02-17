# Query Validation Hook

[← Back to Hooks Templates](../README.md)

**Purpose**: Enforce Athena query validation before execution across all repositories

**Type**: PreToolUse hook (blocking)

**Location**: `~/.claude/hooks/validate-query-execution.py` (user global)

**Configuration**: `~/.claude/settings.json`

---

## What It Does

This PreToolUse hook ensures all Athena queries are validated before execution by:

1. **Intercepting query execution commands** (python run_query.py, athena_client.py)
2. **Checking for validation marker** (created by `/validate-query` slash command)
3. **Blocking execution** if no marker exists
4. **Providing clear recovery instructions** to Claude

---

## Why It Exists

**Problem Without Hook**:
- Forgetting to validate queries before execution leads to:
  - Expensive full table scans (missing partition filters) →  $$$
  - Timezone handling errors → Wrong results
  - Syntax errors discovered at runtime → Wasted time
  - Queries that work in Trino but fail in Athena → Frustration

**Solution With Hook**:
- **Deterministic enforcement** - Hook guarantees validation runs
- **Clear recovery path** - Claude knows exactly what to do
- **Zero configuration per-project** - Works everywhere automatically
- **Emergency bypass available** - Doesn't break workflow

---

## How It Works

### Workflow Diagram

```
┌─────────────────────────────────────────┐
│ Claude wants to run query               │
│                                         │
│ Bash("python run_query.py query.sql")  │
└──────────────────┬──────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────┐
│ PreToolUse Hook Intercepts              │
│                                         │
│ 1. Is this a query execution command?  │
│    → Check regex patterns               │
│    → Early exit if 'git', 'ls', etc.   │
│                                         │
│ 2. Extract query path from command      │
│    → Look for .sql file in args         │
│                                         │
│ 3. Check for validation marker          │
│    → Hash query path                    │
│    → Look for /tmp/query_validated_*.marker │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ↓                     ↓
  Marker Exists         No Marker
        │                     │
        ↓                     ↓
  Delete marker         Block execution
  Allow query           Show error to Claude
  execution             with recovery steps
```

---

### Validation Marker System

- **Creation**: `/validate-query` creates `/tmp/query_validated_<hash>.marker` (hash = SHA256 of absolute query path, first 16 chars)
- **Consumption**: Hook deletes marker after allowing execution (one-time use — ensures re-validation after changes)
- **Lifetime**: Temporary (/tmp directory, cleared on reboot)

---

## Installation

### Step 1: Copy Hook Script

```bash
# Copy from this template to user hooks directory
cp templates/hooks/query-validation/validate-query-execution.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/validate-query-execution.py
```

### Step 2: Update Global Settings

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/validate-query-execution.py"
          }
        ]
      }
    ]
  }
}
```

If your settings file already has other entries, merge the `hooks` section into the existing JSON.

**Project-level alternative**: To use in a single repo instead of globally, place the hook in `.claude/hooks/` and configure in `.claude/settings.json` within that project.

### Step 3: Reload and Verify

Reload: Run `/hooks` in Claude Code, or restart Claude Code.

Test the hook directly:
```bash
echo '{"tool_name":"Bash","tool_input":{"command":"python run_query.py test.sql"}}' | \
  python3 ~/.claude/hooks/validate-query-execution.py
```

Expected: Error message about missing validation marker (exit code 2). Git/ls commands should work without error.

---

## Usage

### Normal Workflow

```
# 1. Claude tries to run query
python run_query.py my_query.sql

# 2. Hook blocks, shows error:
❌ Query execution blocked - validation required!

# 3. Claude runs validation:
/validate-query my_query.sql

# 4. Validation passes, marker created

# 5. Claude re-runs query:
python run_query.py my_query.sql

# 6. Hook finds marker, deletes it, allows execution
✅ Query executes successfully
```

### Emergency Bypass

```bash
# Skip hook validation for emergencies only
SKIP_QUERY_VALIDATION=1 python run_query.py my_query.sql
```

**When to use**: Hook malfunction, validation service down, time-sensitive execution, debugging.

**Warning**: Bypassing validation risks expensive queries and errors.

---

## Configuration

### Whitelisted Commands (Early Exit)

Hook skips validation for these command prefixes:

```python
SAFE_COMMANDS = [
    'ls', 'cd', 'cat', 'grep', 'find', 'echo',
    'pwd', 'mkdir', 'rm', 'cp', 'mv', 'touch',
    'head', 'tail', 'wc', 'sort', 'uniq', 'git'
]
```

**Why**: Performance — most Bash commands aren't query executions (95%+ early exit)

**Impact**: <1ms overhead for whitelisted commands

---

### Query Execution Patterns

Hook identifies query execution via regex patterns:

```python
PATTERNS = [
    r'python3?\s+run_validation_query\.py',  # Validation runner
    r'python3?\s+run_query\.py',             # Query runner
    r'python3?\s+.*athena_client\.py',       # Direct athena client
    r'python3?\s+-m\s+core\.athena_client',  # Module-based execution
]
```

**Matching logic**: Command must match at least one pattern to require validation

**Customization**: See [CUSTOMIZATION.md](./CUSTOMIZATION.md) to add custom runners, whitelist commands, or adapt for other databases.

---

## Troubleshooting

### Hook Blocks Legitimate Commands

**Symptom**: Hook blocks non-query commands (git, npm, etc.)

**Solution**: Add to whitelist in `is_query_execution()`:
```python
if command_stripped.startswith(('ls', 'cd', 'cat', 'your-command')):
    return False
```

---

### Hook Doesn't Block Query Execution

**Symptom**: Queries run without validation

**Check**: (1) Hook in `~/.claude/settings.json`? (2) Script at `~/.claude/hooks/`? (3) Script executable? (4) Command matches patterns? Add debug logging to `is_query_execution()` to trace matching.

---

### Marker Not Found After Validation

**Symptom**: `/validate-query` succeeds, but hook still blocks

**Check**: (1) Same hash algorithm? (both SHA256) (2) `/tmp` writable? (3) `ls /tmp/query_validated_*.marker` shows file? (4) Absolute vs relative path mismatch?

---

### Hook Performance Issues

**Symptom**: Claude feels slow. **Profile**: `time echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 ~/.claude/hooks/validate-query-execution.py` — expected <5ms total, <1ms for early exit.

---

### Hook Script Has a Bug

Hook returns exit code 1 on errors, which logs the error but **doesn't block** — preventing workflow breakage. Wrap validation logic in try/except with `sys.exit(1)` in the except block.

---

## Performance Impact

**Measured Impact** (from production usage):

- **Whitelisted commands** (git, ls, etc.): <1ms overhead
- **Query execution commands**: ~5ms (validation check)
- **Overall session impact**: Negligible (<0.1% slowdown)

**Why so fast**:
- Early exit for 95%+ of commands
- Simple regex matching
- File system check only (no database/API calls)
- Optimized Python code

---

## Security Considerations

### Safe Practices

- Hook runs validation, doesn't execute queries
- Markers stored in /tmp (not permanent)
- Emergency bypass available (user controls)
- No network calls or external dependencies
- No sensitive data logged

### Audit Trail

Optional: Add Python `logging` to the hook to record ALLOWED/BLOCKED decisions to a log file for compliance tracking.

---

## Integration with Other Tools

### Works With /validate-query Slash Command

1. Slash command validates query → Creates `/tmp/query_validated_<hash>.marker`
2. User tries to execute query → PreToolUse hook checks for marker
3. If marker exists → Delete marker, allow execution
4. If no marker → Block execution, tell Claude to run `/validate-query`

**See also**: [`slash-commands/documentation/validate-query.md`](../../slash-commands/)

### Works With Permissions System

**Execution order**: Permissions check (coarse) → Hook runs (fine-grained) → Hook can still block

### Adapting for Team Use

**User global**: Each team member installs in `~/.claude/hooks/` — consistent behavior, individual opt-out.

**Project-level**: Copy hook to `.claude/hooks/`, configure in `.claude/settings.json`, commit both — team inherits automatically.

---

## Related Documentation

- [**CUSTOMIZATION.md**](./CUSTOMIZATION.md) - Per-database patterns, custom runners, extension points
- [**Hooks README**](../README.md) - Hook category overview
- [**Hooks Technical Reference**](../HOOKS_REFERENCE.md) - Complete hooks documentation
- [**Slash Commands**](../../slash-commands/) - `/validate-query` command integration

---

**Last Updated**: 2026-02-16
**Maintained By**: ai-dev-templates library
**Evidence**: Extracted from implementing query validation hook across 4+ data repositories
