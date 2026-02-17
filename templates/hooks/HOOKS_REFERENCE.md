# Claude Code Hooks: Complete Technical Reference

[← Back to Hooks README](README.md) | [← Back to Main README](../../README.md)

**Purpose**: Comprehensive technical reference for Claude Code hooks

**Audience**: Developers implementing custom hooks

**Source**: Official Claude Code documentation + production implementation experience

---

## Table of Contents

1. [Hook Events Reference](#hook-events-reference)
2. [Exit Code Reference](#exit-code-reference)
3. [Configuration Reference](#configuration-reference)
4. [Hook Input Format](#hook-input-format)
5. [Matcher Patterns Reference](#matcher-patterns-reference)
6. [Environment Variables](#environment-variables)
7. [Hook Performance Optimization](#hook-performance-optimization)
8. [Security Best Practices](#security-best-practices)
9. [Testing Hooks](#testing-hooks)
10. [Advanced Patterns](#advanced-patterns)
11. [Troubleshooting Reference](#troubleshooting-reference)

---

## Hook Events Reference

### PreToolUse Hook

**When**: Before tool calls execute
**Can block**: Yes (exit code 2)
**Use cases**: Validation, permissions, safety checks

**Environment Variables**:
- `$CLAUDE_TOOL_INPUT` - JSON with tool details

**Input Format**:
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "python run_query.py my_query.sql",
    "description": "Execute validated query"
  }
}
```

**Example - Query Validation**:
```python
#!/usr/bin/env python3
import sys
import json

data = json.load(sys.stdin)
tool_name = data['tool_name']
tool_input = data['tool_input']

if tool_name != 'Bash':
    sys.exit(0)  # Only validate Bash commands

command = tool_input.get('command', '')

if 'run_query.py' in command:
    # Check if query was validated
    if not validation_marker_exists(command):
        print("❌ Query not validated! Run /validate-query first", file=sys.stderr)
        sys.exit(2)  # Block execution

sys.exit(0)  # Allow
```

---

### PostToolUse Hook

**When**: After tool calls complete
**Can block**: No (exit code ignored)
**Use cases**: Auto-formatting, syncing, logging

**Environment Variables**:
- `$CLAUDE_TOOL_INPUT` - Original tool input
- `$CLAUDE_TOOL_OUTPUT` - Tool execution result

**Input Format**:
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "old_string": "...",
    "new_string": "..."
  },
  "tool_output": {
    "success": true,
    "message": "File edited successfully"
  }
}
```

**Example - Auto-Format After Edit**:
```python
#!/usr/bin/env python3
import sys
import json
import subprocess

data = json.load(sys.stdin)
tool_name = data['tool_name']

if tool_name not in ['Edit', 'Write']:
    sys.exit(0)

file_path = data['tool_input'].get('file_path', '')

if file_path.endswith('.py'):
    # Run black formatter
    subprocess.run(['black', file_path], capture_output=True)

sys.exit(0)  # Always allow for PostToolUse
```

---

### UserPromptSubmit Hook

**When**: User submits a prompt
**Can block**: Yes (exit code 2)
**Use cases**: Content filtering, logging, rate limiting

**Input Format**:
```json
{
  "prompt": "Help me implement feature X",
  "session_id": "abc123..."
}
```

**Example - Log User Prompts**:
```python
#!/usr/bin/env python3
import sys
import json
from datetime import datetime

data = json.load(sys.stdin)
prompt = data.get('prompt', '')

# Log to file
with open('/tmp/claude_prompts.log', 'a') as f:
    f.write(f"[{datetime.now()}] {prompt}\n")

sys.exit(0)  # Always allow
```

---

### SessionStart Hook

**When**: New or resumed session starts
**Can block**: No
**Use cases**: Setup, environment validation, logging

**Input Format**:
```json
{
  "session_id": "abc123...",
  "is_resumed": false
}
```

**Example - Session Logging**:
```bash
#!/bin/bash
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
echo "[$(date)] Session started: $SESSION_ID" >> /tmp/claude_sessions.log
exit 0
```

---

### SessionEnd Hook

**When**: Session terminates
**Can block**: No
**Use cases**: Cleanup, archiving, reporting

---

### Stop Hook

**When**: Claude finishes responding
**Can block**: No
**Use cases**: Metrics, logging, notifications

---

### SubagentStop Hook

**When**: Subagent task completes
**Can block**: No
**Use cases**: Subagent metrics, logging

---

### PreCompact Hook

**When**: Before context compaction
**Can block**: Yes
**Use cases**: Custom compaction strategy, archiving

---

### Notification Hook

**When**: Sending notifications
**Can block**: Yes
**Use cases**: Custom notification routing, filtering

---

## Exit Code Reference

| Code | Name | Effect | When to Use | Hook Types |
|------|------|--------|-------------|------------|
| **0** | Allow/Success | Continue normal execution | Validation passed, logging completed | All hooks |
| **1** | Error | Log error, **continue execution** | Hook malfunction, non-critical error | All hooks |
| **2** | Block | **Stop execution**, show stderr to Claude | Validation failed, policy violation | PreToolUse, UserPromptSubmit, PreCompact, Notification only |

### Exit Code Decision Tree

```
Is this a blocking hook type (PreToolUse, UserPromptSubmit, PreCompact, Notification)?
├─ YES
│  ├─ Should operation be allowed?
│  │  ├─ YES → exit 0
│  │  └─ NO → print error to stderr, exit 2
│  └─ Did hook encounter an error?
│     └─ YES → print error to stderr, exit 1 (log but don't block)
└─ NO (PostToolUse, SessionStart, etc.)
   └─ Always exit 0 (exit code ignored for non-blocking hooks)
```

### Examples

**Exit 0 - Allow**:
```python
# Validation passed
sys.exit(0)
```

**Exit 1 - Error (log but continue)**:
```python
try:
    validate_query(query)
except Exception as e:
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(1)  # Log error but don't block Claude
```

**Exit 2 - Block**:
```python
if not validation_passed:
    print("❌ Validation failed: Missing partition filter", file=sys.stderr)
    sys.exit(2)  # Block execution
```

---

## Configuration Reference

### User Global Settings (`~/.claude/settings.json`)

**Applies to**: All repositories on machine
**Use case**: Query validation, logging, personal standards
**Priority**: Lowest (overridden by project settings)

**Example**:
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
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
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/auto-format.py"
          }
        ]
      }
    ]
  }
}
```

**Path Resolution**:
- Use `~/` for home directory
- Use absolute paths (`/home/user/.claude/hooks/`)
- Hook script must be accessible from all repos

---

### Project Shared Settings (`.claude/settings.json`)

**Applies to**: All team members in project
**Use case**: Team standards, project-specific validation
**Committed to git**: Yes
**Priority**: Medium (overrides user global)

**Example**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/validate-file-size.py"
          }
        ]
      }
    ]
  }
}
```

**Path Resolution**:
- Use relative paths (`.claude/hooks/`)
- Hook script bundled with project
- Team inherits hook automatically

---

### Project Local Settings (`.claude/settings.local.json`)

**Applies to**: Only you in this project
**Use case**: Personal overrides, experiments
**Gitignored**: Yes
**Priority**: Highest (overrides everything)

**Example**:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/log-prompts.py"
          }
        ]
      }
    ]
  }
}
```

---

### Settings Hierarchy (Priority Order)

Higher number = higher priority (overrides lower)

1. **Enterprise settings** (managed by organization)
2. **CLI arguments** (`claude --config custom.json`)
3. **Project local** (`.claude/settings.local.json`) ← Gitignored
4. **Project shared** (`.claude/settings.json`) ← Version controlled
5. **User global** (`~/.claude/settings.json`) ← Personal defaults

**Merge behavior**: Hooks from multiple levels are **combined** (not overridden)

**Example - Effective Hooks**:
```
User global:   PreToolUse → Bash → validate-query.py
Project shared: PreToolUse → Bash → check-permissions.py
─────────────────────────────────────────────────────
Result:        PreToolUse → Bash → [validate-query.py, check-permissions.py]
                           (both hooks run in order)
```

---

## Hook Input Format

### Reading Hook Input

#### Python
```python
#!/usr/bin/env python3
import sys
import json

def read_hook_input():
    """Read JSON input from stdin."""
    try:
        data = json.load(sys.stdin)
        return data.get('tool_name'), data.get('tool_input', {})
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Hook error: Failed to parse input: {e}", file=sys.stderr)
        sys.exit(1)

tool_name, tool_input = read_hook_input()

# Access fields
if tool_name == 'Bash':
    command = tool_input.get('command', '')
elif tool_name == 'Edit':
    file_path = tool_input.get('file_path', '')
    old_string = tool_input.get('old_string', '')
    new_string = tool_input.get('new_string', '')
```

#### Bash
```bash
#!/bin/bash

# Read entire JSON input
INPUT=$(cat)

# Parse with jq
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Check conditions
if [ "$TOOL_NAME" = "Bash" ]; then
    echo "Processing bash command: $COMMAND"
fi

exit 0
```

#### Node.js
```javascript
#!/usr/bin/env node

const data = JSON.parse(require('fs').readFileSync(0, 'utf-8'));
const { tool_name, tool_input } = data;

if (tool_name === 'Bash') {
    const command = tool_input.command || '';
    console.log(`Processing: ${command}`);
}

process.exit(0);
```

---

### Common Tool Input Structures

#### Bash Tool
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "python script.py --arg value",
    "description": "Run analysis script",
    "timeout": 120000,
    "run_in_background": false
  }
}
```

#### Edit Tool
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "old_string": "def old_function():",
    "new_string": "def new_function():",
    "replace_all": false
  }
}
```

#### Write Tool
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/new_file.py",
    "content": "#!/usr/bin/env python3\nprint('Hello')"
  }
}
```

#### Read Tool
```json
{
  "tool_name": "Read",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "offset": 0,
    "limit": 1000
  }
}
```

---

## Matcher Patterns Reference

### Basic Matchers

| Pattern | Matches | Example Use Case |
|---------|---------|------------------|
| `"Bash"` | Only Bash tool | Command validation, query enforcement |
| `"Edit"` | Only Edit tool | Code formatting after edits |
| `"Write"` | Only Write tool | File size limits, permissions |
| `"Read"` | Only Read tool | Access logging, audit trail |
| `"Glob"` | Only Glob tool | File search logging |
| `"Grep"` | Only Grep tool | Content search logging |
| `"Task"` | Only Task tool | Subagent usage tracking |
| `"WebFetch"` | Only WebFetch tool | External request logging |
| `"WebSearch"` | Only WebSearch tool | Search query logging |

### Combined Matchers (Pipe Syntax)

| Pattern | Matches | Example Use Case |
|---------|---------|------------------|
| `"Edit\|Write"` | Edit OR Write | File modification hooks |
| `"Read\|Edit\|Write"` | Read OR Edit OR Write | File access logging |
| `"Bash\|Task"` | Bash OR Task | Command execution tracking |

**Note**: Use pipe character `|` (not comma or space)

### Universal Matcher

| Pattern | Matches | Example Use Case |
|---------|---------|------------------|
| `"*"` | All tools | Universal logging, metrics |

**Warning**: Performance impact - hook runs for every tool use

---

### Matcher Limitations

**Matchers only filter by tool name**, not tool input content.

**Example - What You CANNOT Do**:
```json
// ❌ This doesn't work - can't match command content
{
  "matcher": "Bash(python:*)",  // Invalid syntax
  "hooks": [...]
}
```

**Solution - Filter in Hook Script**:
```python
# ✅ Correct approach - filter in hook script
tool_name = data['tool_name']
if tool_name != 'Bash':
    sys.exit(0)  # Not Bash, allow

command = data['tool_input']['command']
if not 'python' in command:
    sys.exit(0)  # Not python command, allow

# ... validate python command ...
```

---

## Environment Variables

### Hook-Specific Variables

| Variable | Available In | Contains | Format |
|----------|--------------|----------|--------|
| `$CLAUDE_TOOL_INPUT` | PreToolUse, PostToolUse | Tool call details | JSON string |
| `$CLAUDE_TOOL_OUTPUT` | PostToolUse | Tool execution result | JSON string |
| `$CLAUDE_PROJECT_DIR` | All hooks | Current project directory | String (absolute path) |

### Standard Environment Variables

All hooks also have access to:
- `$HOME` - User home directory
- `$PATH` - System PATH
- `$USER` - Current username
- Custom variables set by user

---

### Using Environment Variables in Hooks

#### Access Project Directory
```python
import os

project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
print(f"Running in project: {project_dir}")
```

#### Escape Hatch Pattern
```python
# Custom environment variable for bypass
if os.environ.get('SKIP_VALIDATION') == '1':
    sys.exit(0)  # Emergency bypass
```

**Usage**:
```bash
SKIP_VALIDATION=1 python run_query.py query.sql
```

---

## Hook Performance Optimization

### 1. Early Exit Pattern ⭐ Most Important

**Problem**: Hook runs before EVERY tool use (hundreds of times per session)

**Solution**: Exit immediately for common cases

```python
#!/usr/bin/env python3
import sys
import json

data = json.load(sys.stdin)
tool_name = data.get('tool_name')

# Early exit #1: Wrong tool
if tool_name != 'Bash':
    sys.exit(0)

command = data.get('tool_input', {}).get('command', '')

# Early exit #2: Whitelisted commands
SAFE_COMMANDS = ['ls', 'cd', 'cat', 'git', 'grep', 'find', 'echo',
                 'pwd', 'mkdir', 'rm', 'cp', 'mv', 'touch',
                 'head', 'tail', 'wc', 'sort', 'uniq']

if any(command.startswith(cmd) for cmd in SAFE_COMMANDS):
    sys.exit(0)

# ... expensive validation logic (only runs for non-whitelisted commands) ...
```

**Impact**:
- Before: ~5ms per tool use
- After: <1ms for 95% of tool uses

---

### 2. Caching Pattern

**Problem**: Repeated expensive operations (database lookups, API calls)

**Solution**: Cache results

```python
import shelve
import hashlib

def get_cache_key(query_path):
    return hashlib.sha256(query_path.encode()).hexdigest()

def is_query_validated_cached(query_path):
    cache_key = get_cache_key(query_path)

    with shelve.open('/tmp/validation_cache') as cache:
        if cache_key in cache:
            return cache[cache_key]

        # Expensive validation
        result = expensive_validation(query_path)
        cache[cache_key] = result
        return result
```

**Impact**:
- First call: 50ms (expensive validation)
- Cached calls: 2ms (cache lookup)

---

### 3. Lazy Import Pattern

**Problem**: Import overhead on every hook execution

**Solution**: Import modules only when needed

```python
#!/usr/bin/env python3
import sys
import json

# Fast imports (always needed)
data = json.load(sys.stdin)
tool_name = data.get('tool_name')

# Early exit before expensive imports
if tool_name != 'Bash':
    sys.exit(0)

# Expensive imports (only after early exit)
import re
import subprocess
import hashlib
from pathlib import Path

# ... validation logic ...
```

**Impact**:
- Before: 10ms (import overhead on every call)
- After: <1ms for early exit, 10ms only when validation needed

---

### 4. Async Pattern (PostToolUse Only)

**Problem**: Slow operations block Claude's workflow

**Solution**: Run in background (PostToolUse hooks only)

```python
#!/usr/bin/env python3
import subprocess
import sys

# Start slow operation in background
subprocess.Popen(
    ['python3', 'slow_formatting.py', 'file.py'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Return immediately (don't wait)
sys.exit(0)
```

**Impact**:
- Synchronous: 500ms (blocks Claude)
- Asynchronous: 5ms (returns immediately)

**Warning**: Only use for PostToolUse hooks (PreToolUse must be synchronous for validation)

---

### 5. Compiled Regex Pattern

**Problem**: Recompiling regex on every call

**Solution**: Compile once

```python
import re

# ❌ Bad - recompiles on every call
def is_query_command(command):
    return bool(re.search(r'python3?\s+run_query\.py', command))

# ✅ Good - compiles once
QUERY_PATTERN = re.compile(r'python3?\s+run_query\.py')

def is_query_command(command):
    return bool(QUERY_PATTERN.search(command))
```

---

### Performance Benchmarking

```bash
# Test hook execution time
time echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 hook.py

# Run multiple times for average
for i in {1..100}; do
    echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 hook.py
done
```

**Target Performance**:
- Early exit: <1ms
- Simple validation: <10ms
- Complex validation: <50ms
- If >100ms: Needs optimization

---

## Security Best Practices

### Input Validation

**Always validate hook input** to prevent injection attacks

```python
import shlex

# ❌ Unsafe - direct command execution
command = data['tool_input']['command']
subprocess.run(command, shell=True)  # Injection risk!

# ✅ Safe - validate and sanitize
command = data['tool_input']['command']
safe_command = shlex.quote(command)  # Escape special characters
# Better: Don't use shell=True at all
```

---

### Least Privilege

**Don't require elevated permissions**

```python
# ❌ Bad - requires sudo
subprocess.run(['sudo', 'systemctl', 'restart', 'service'])

# ✅ Good - user-level operations only
subprocess.run(['git', 'status'])
```

---

### Audit Logging

**Log all hook decisions** for security review

```python
import logging

logging.basicConfig(
    filename='/var/log/claude_hooks.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def validate_query(query_path):
    if validation_passed:
        logging.info(f"ALLOWED: Query {query_path}")
        return True
    else:
        logging.warning(f"BLOCKED: Query {query_path} - missing partition filter")
        return False
```

---

### Sensitive Data Handling

**Never log sensitive data**

```python
# ❌ Bad - logs sensitive query
logging.info(f"Query: {query_content}")  # May contain PII

# ✅ Good - logs hash only
query_hash = hashlib.sha256(query_content.encode()).hexdigest()
logging.info(f"Query hash: {query_hash}")
```

---

### Secret Management

**Never hardcode secrets** in hooks

```python
# ❌ Bad - hardcoded API key
API_KEY = "sk-1234567890abcdef"

# ✅ Good - environment variable
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    print("Error: API_KEY not set", file=sys.stderr)
    sys.exit(1)
```

---

## Testing Hooks

### Unit Testing

```python
# test_hook.py
import json
import subprocess
import unittest

class TestQueryValidationHook(unittest.TestCase):

    def run_hook(self, tool_input):
        """Helper to run hook with test input"""
        result = subprocess.run(
            ['python3', 'validate-query-execution.py'],
            input=json.dumps(tool_input),
            capture_output=True,
            text=True
        )
        return result.returncode, result.stderr

    def test_allows_safe_commands(self):
        """Hook should allow whitelisted commands"""
        tool_input = {
            "tool_name": "Bash",
            "tool_input": {"command": "ls -la"}
        }
        exit_code, stderr = self.run_hook(tool_input)
        self.assertEqual(exit_code, 0)  # Should allow

    def test_blocks_unvalidated_query(self):
        """Hook should block query without validation marker"""
        tool_input = {
            "tool_name": "Bash",
            "tool_input": {"command": "python run_query.py test.sql"}
        }
        exit_code, stderr = self.run_hook(tool_input)
        self.assertEqual(exit_code, 2)  # Should block
        self.assertIn("validation required", stderr)

    def test_allows_validated_query(self):
        """Hook should allow query with validation marker"""
        # Create validation marker
        subprocess.run(['touch', '/tmp/query_validated_test.marker'])

        tool_input = {
            "tool_name": "Bash",
            "tool_input": {"command": "python run_query.py test.sql"}
        }
        exit_code, stderr = self.run_hook(tool_input)
        self.assertEqual(exit_code, 0)  # Should allow

if __name__ == '__main__':
    unittest.main()
```

---

### Integration Testing

```bash
#!/bin/bash
# integration_test.sh

echo "Testing query validation hook..."

# Test 1: Whitelisted command should pass
echo '{"tool_name":"Bash","tool_input":{"command":"git status"}}' | \
  python3 ~/.claude/hooks/validate-query-execution.py
if [ $? -eq 0 ]; then
    echo "✅ Test 1 passed: Whitelisted command allowed"
else
    echo "❌ Test 1 failed: Whitelisted command blocked"
fi

# Test 2: Unvalidated query should be blocked
echo '{"tool_name":"Bash","tool_input":{"command":"python run_query.py test.sql"}}' | \
  python3 ~/.claude/hooks/validate-query-execution.py
if [ $? -eq 2 ]; then
    echo "✅ Test 2 passed: Unvalidated query blocked"
else
    echo "❌ Test 2 failed: Unvalidated query allowed"
fi

# Test 3: Non-Bash tool should pass
echo '{"tool_name":"Read","tool_input":{"file_path":"test.txt"}}' | \
  python3 ~/.claude/hooks/validate-query-execution.py
if [ $? -eq 0 ]; then
    echo "✅ Test 3 passed: Non-Bash tool allowed"
else
    echo "❌ Test 3 failed: Non-Bash tool blocked"
fi
```

---

## Advanced Patterns

### Tool Input Modification

**Modify tool input before execution** (Claude Code v2.0.10+)

```python
#!/usr/bin/env python3
import sys
import json

data = json.load(sys.stdin)

# Modify tool input
if data['tool_name'] == 'Bash':
    # Add --verbose flag to all python commands
    command = data['tool_input']['command']
    if command.startswith('python'):
        data['tool_input']['command'] = command + ' --verbose'

# Output modified data
print(json.dumps(data))
sys.exit(0)
```

---

### Conditional Hooks (Project-Specific)

**Only run hook in specific projects**

```python
import os
from pathlib import Path

# Check for .enable-validation marker file
project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd()))
if not (project_dir / '.enable-validation').exists():
    sys.exit(0)  # Skip validation in this project

# ... validation logic ...
```

---

### Multi-Stage Hooks

**Chain multiple validations**

```python
def validate_syntax(query):
    # Check SQL syntax
    return True

def validate_security(query):
    # Check for SQL injection patterns
    return True

def validate_cost(query):
    # Estimate query cost, block if too expensive
    return True

# Run all validators
validators = [validate_syntax, validate_security, validate_cost]
for validator in validators:
    if not validator(query):
        print(f"❌ Validation failed: {validator.__name__}", file=sys.stderr)
        sys.exit(2)

sys.exit(0)  # All validations passed
```

---

### Dynamic Hook Loading

**Load hook configuration from external file**

```python
import json
from pathlib import Path

# Load hook config from project
config_file = Path('.claude/hook-config.json')
if config_file.exists():
    with open(config_file) as f:
        config = json.load(f)
        blocklist = config.get('blocked_files', [])
else:
    blocklist = []

# Check if file is blocked
file_path = data['tool_input'].get('file_path', '')
if file_path in blocklist:
    print(f"❌ Access to {file_path} is blocked", file=sys.stderr)
    sys.exit(2)
```

---

## Troubleshooting Reference

### Problem: Hook Not Executing

**Symptoms**: Hook doesn't run, expected behavior not occurring

**Diagnostic Steps**:

1. **Verify hook configured correctly**:
```bash
# Run /hooks command in Claude Code
# Check if hook appears in the list
```

2. **Check hook script exists**:
```bash
# For user global hooks
ls -la ~/.claude/hooks/my-hook.py

# For project hooks
ls -la .claude/hooks/my-hook.py
```

3. **Verify hook is executable**:
```bash
chmod +x ~/.claude/hooks/my-hook.py
```

4. **Test hook directly**:
```bash
echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | \
  python3 ~/.claude/hooks/my-hook.py
```

5. **Check for syntax errors**:
```bash
python3 -m py_compile ~/.claude/hooks/my-hook.py
```

6. **Verify matcher is correct**:
```json
// ❌ Wrong - lowercase
{"matcher": "bash"}

// ✅ Correct - case-sensitive
{"matcher": "Bash"}
```

---

### Problem: Hook Blocking Legitimate Commands

**Symptoms**: Hook blocks commands that should be allowed

**Solutions**:

1. **Add to whitelist**:
```python
# Expand whitelist
SAFE_COMMANDS = ['ls', 'cd', 'cat', 'git', 'npm', 'node', 'pip']
```

2. **Use escape hatch**:
```bash
SKIP_MY_HOOK=1 command
```

3. **Check matcher too broad**:
```json
// ❌ Too broad - matches everything
{"matcher": "*"}

// ✅ Specific - matches only Bash
{"matcher": "Bash"}
```

4. **Add logging to debug**:
```python
with open('/tmp/hook_debug.log', 'a') as f:
    f.write(f"Command: {command}\n")
    f.write(f"Blocked: {should_block}\n")
```

---

### Problem: Hook Performance Issues

**Symptoms**: Claude feels slow, delayed responses

**Solutions**:

1. **Add early exit**:
```python
# Exit before expensive operations
if command.startswith(('ls', 'cd', 'git')):
    sys.exit(0)
```

2. **Profile hook execution**:
```bash
time echo '{}' | python3 hook.py
```

3. **Optimize imports** (lazy loading):
```python
# Only import when needed
if needs_validation:
    import expensive_module
```

4. **Cache expensive operations**:
```python
import shelve
with shelve.open('/tmp/cache') as cache:
    if key in cache:
        return cache[key]
```

---

## Official Claude Code Documentation

**Primary References**:

1. **Hooks Guide**: https://docs.claude.com/en/docs/claude-code/hooks-guide
   - Hook events (PreToolUse, PostToolUse, SessionStart, etc.)
   - Exit codes (0, 1, 2)
   - Configuration syntax
   - Environment variables

2. **Settings Reference**: https://docs.claude.com/en/docs/claude-code/settings
   - Settings hierarchy (Enterprise → CLI → Project local → Project shared → User global)
   - Matcher patterns
   - Tool input format

3. **Plugin Reference** (includes hooks): https://docs.claude.com/en/docs/claude-code/plugins-reference
   - Plugin structure with hooks directory
   - Hook bundling in plugins
   - Distribution patterns

---

**Last Updated**: 2025-11-03
**Maintained By**: dev-setup template library
**Evidence**: Extracted from implementing global query validation hook + Claude Code official documentation
