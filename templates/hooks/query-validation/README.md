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

**Marker Creation**: `/validate-query` slash command creates marker after successful validation

```bash
# Command creates this marker:
/tmp/query_validated_<hash>.marker

# Hash is SHA256(absolute_query_path)[:16]
# Example: /tmp/query_validated_a1b2c3d4e5f6g7h8.marker
```

**Marker Consumption**: Hook deletes marker after allowing execution (one-time use)

**Why one-time use**: Ensures re-validation after query changes

**Marker lifetime**: Temporary (/tmp directory, cleared on reboot)

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

**If `~/.claude/settings.json` already has other settings**, add hooks section:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "statusLine": {
    "type": "command",
    "command": "ccstatusline"  // Install globally: npm install -g ccstatusline
  },
  "hooks": {  // ← Add this section
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

### Step 3: Reload Configuration

Option A: Run `/hooks` command in Claude Code

Option B: Restart Claude Code

### Step 4: Verify Installation

```bash
# Test hook directly
echo '{"tool_name":"Bash","tool_input":{"command":"python run_query.py test.sql"}}' | \
  python3 ~/.claude/hooks/validate-query-execution.py

# Expected output: Error message about missing validation marker (exit code 2)
```

### Step 5: Test in Claude Code

Ask Claude to run a query:
- If validation required, Claude should see error message
- If git/ls/etc. commands work without error, hook is working correctly

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

**When to use**:
- Hook malfunction
- Validation service down
- Time-sensitive query execution
- Debugging hook issues

**Warning**: Bypassing validation risks expensive queries, errors

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

**Why**: Performance - most Bash commands aren't query executions (95%+ early exit)

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

---

## Customization

### Add Custom Query Runners

Edit `~/.claude/hooks/validate-query-execution.py`, find `is_query_execution()` function:

```python
def is_query_execution(command):
    # ... existing code ...

    # Query execution patterns
    patterns = [
        r'python3?\s+run_validation_query\.py',
        r'python3?\s+run_query\.py',
        r'python3?\s+.*athena_client\.py',
        r'python3?\s+-m\s+core\.athena_client',
        r'python3?\s+my_custom_runner\.py',  # ← Add your runner
        r'node\s+run_bigquery\.js',          # ← Add BigQuery runner
    ]

    return any(re.search(pattern, command) for pattern in patterns)
```

---

### Add Custom Whitelist Commands

Edit hook, find early exit section:

```python
def is_query_execution(command):
    # Early exit for common non-query commands
    command_stripped = command.strip()
    if command_stripped.startswith(('ls', 'cd', 'cat', 'grep', 'find', 'echo',
                                    'pwd', 'mkdir', 'rm', 'cp', 'mv', 'touch',
                                    'head', 'tail', 'wc', 'sort', 'uniq', 'git',
                                    'npm', 'node', 'pip')):  # ← Add your commands
        return False
    # ... rest of function ...
```

---

### Change Marker Location

Edit hook, find `check_validation_marker()` function:

```python
def check_validation_marker(query_path):
    # ... existing code ...

    # Default: /tmp/query_validated_<hash>.marker
    marker_path = Path(f'/tmp/query_validated_{path_hash}.marker')

    # Custom: Use project directory
    # marker_path = Path(f'./.query_markers/validated_{path_hash}.marker')

    return marker_path.exists(), marker_path
```

**Note**: Must also update `/validate-query` slash command to use same location

---

### Adapt for Other Databases

This hook works with any database by updating patterns:

**BigQuery**:
```python
patterns = [
    r'python3?\s+run_bigquery\.py',
    r'bq\s+query',
]
```

**Snowflake**:
```python
patterns = [
    r'python3?\s+run_snowflake\.py',
    r'snowsql\s+-q',
]
```

**Postgres**:
```python
patterns = [
    r'psql\s+-f',
    r'python3?\s+run_postgres\.py',
]
```

---

## Troubleshooting

### Hook Blocks Legitimate Commands

**Symptom**: Hook blocks non-query commands (git, npm, etc.)

**Solution**: Add to whitelist

```python
# In is_query_execution() function
if command_stripped.startswith(('ls', 'cd', 'cat', 'your-command')):
    return False
```

---

### Hook Doesn't Block Query Execution

**Symptom**: Queries run without validation

**Check list**:
1. Is hook configured in `~/.claude/settings.json`? `cat ~/.claude/settings.json | grep -A5 hooks`
2. Is hook script at `~/.claude/hooks/validate-query-execution.py`? `ls -la ~/.claude/hooks/`
3. Is hook script executable? `chmod +x ~/.claude/hooks/validate-query-execution.py`
4. Does query command match patterns? Add logging to debug:

```python
# Add to is_query_execution() function
with open('/tmp/hook_debug.log', 'a') as f:
    f.write(f"Command: {command}\n")
    f.write(f"Matches patterns: {any(re.search(p, command) for p in patterns)}\n")
```

---

### Marker Not Found After Validation

**Symptom**: `/validate-query` runs successfully, but hook still blocks

**Check list**:
1. Are validation command and hook using same hash algorithm? (both use SHA256)
2. Is /tmp directory writable? `touch /tmp/test && rm /tmp/test`
3. Check marker file exists: `ls -la /tmp/query_validated_*.marker`
4. Are query paths matching? (absolute vs relative path issue)

**Debug**:
```bash
# In hook, add logging:
with open('/tmp/hook_debug.log', 'a') as f:
    f.write(f"Query path: {query_abs_path}\n")
    f.write(f"Path hash: {path_hash}\n")
    f.write(f"Marker path: {marker_path}\n")
    f.write(f"Marker exists: {marker_path.exists()}\n")
```

---

### Hook Performance Issues

**Symptom**: Claude feels slow when running Bash commands

**Solutions**:

1. **Verify early exit working**: Add logging to measure
```python
import time
start = time.time()
# ... early exit code ...
with open('/tmp/hook_timing.log', 'a') as f:
    f.write(f"Early exit time: {(time.time() - start) * 1000:.2f}ms\n")
```

2. **Profile hook execution**:
```bash
time echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | \
  python3 ~/.claude/hooks/validate-query-execution.py
```

Expected: <5ms total, <1ms for early exit commands

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

### Safe Practices ✅

- Hook runs validation, doesn't execute queries
- Markers stored in /tmp (not permanent)
- Emergency bypass available (user controls)
- No network calls or external dependencies
- No sensitive data logged

### Audit Trail

Hook logs validation decisions:

```python
# Optional: Add logging for compliance
import logging
logging.basicConfig(filename='/var/log/claude_queries.log')

if marker_exists:
    logging.info(f"ALLOWED: Query {query_path} (validated)")
else:
    logging.warning(f"BLOCKED: Query {query_path} (no validation)")
```

---

## Integration with Other Tools

### Works With /validate-query Slash Command

**Pattern**:
1. Slash command validates query → Creates `/tmp/query_validated_<hash>.marker`
2. User tries to execute query → PreToolUse hook checks for marker
3. If marker exists → Delete marker, allow execution
4. If no marker → Block execution, tell Claude to run `/validate-query`

**See also**: [`slash-commands/documentation/validate-query.md`](../../slash-commands/)

---

### Works With Permissions System

**Execution order**:
1. **Permissions** check allow/deny list (coarse filtering)
2. If allowed → **Hook runs** (fine-grained validation)
3. Hook can still block if validation fails

**Example** (`.claude/settings.local.json`):
```json
{
  "permissions": {
    "allow": ["Bash(python:*)"]  // Permission granted
  },
  "hooks": {
    "PreToolUse": [...]  // Hook validates after permission check
  }
}
```

---

### Adapting for Team Use

**Option 1: Recommend to team** (user global)
- Each team member installs in `~/.claude/hooks/`
- Consistent behavior across team
- Individual opt-out if needed

**Option 2: Project-level hook** (project shared)
- Copy hook to `.claude/hooks/` in project
- Configure in `.claude/settings.json`
- Commit both to git
- Team inherits automatically

---

## FAQ

### Q: Can I use this hook in just one repository?
**A**: Yes. Instead of user global (`~/.claude/settings.json`), configure in project-level `.claude/settings.json`:

```bash
# Copy to project
mkdir -p .claude/hooks
cp ~/.claude/hooks/validate-query-execution.py .claude/hooks/

# Configure in .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/validate-query-execution.py"
          }
        ]
      }
    ]
  }
}
```

### Q: What if I want to validate queries differently per project?
**A**: Use project-level hooks with custom validation logic:

```python
# .claude/hooks/validate-query-execution.py
import os

project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '')

if 'project-a' in project_dir:
    # Strict validation for project A
    require_partition_filter()
elif 'project-b' in project_dir:
    # Relaxed validation for project B
    pass
```

### Q: Does this work for databases other than Athena?
**A**: Yes! Customize patterns to match your database execution commands:

```python
# BigQuery
patterns = [r'python3?\s+run_bigquery\.py', r'bq\s+query']

# Snowflake
patterns = [r'python3?\s+run_snowflake\.py', r'snowsql\s+-q']

# Postgres
patterns = [r'psql\s+-f', r'python3?\s+run_postgres\.py']
```

### Q: Can I add more validation checks?
**A**: Yes! Extend hook to check query content:

```python
# After extracting query_path
with open(query_path) as f:
    query = f.read()

# Check for partition filters
if 'WHERE' not in query:
    block_execution("Missing WHERE clause - add partition filter")

# Check for expensive operations
if 'SELECT *' in query and 'LIMIT' not in query:
    block_execution("SELECT * without LIMIT - add row limit")
```

### Q: What happens if the hook script has a bug?
**A**: Hook returns exit code 1 (error), which logs the error but **doesn't block** execution. This prevents workflow breakage.

Add try/except to handle gracefully:

```python
try:
    # Validation logic
    validate_query(query_path)
except Exception as e:
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(1)  # Log error, don't block
```

---

## Related Documentation

- [**Hooks README**](../README.md) - Hook category overview
- [**Hooks Technical Reference**](../HOOKS_REFERENCE.md) - Complete hooks documentation
- [**Slash Commands**](../../slash-commands/) - `/validate-query` command integration

---

**Last Updated**: 2025-11-03
**Maintained By**: dev-setup template library
**Evidence**: Extracted from implementing query validation hook across 4+ data repositories
