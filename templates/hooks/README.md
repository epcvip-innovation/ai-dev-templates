# Claude Code Hooks Templates

[← Back to Main README](../../README.md)

**Purpose**: Automate workflow enforcement, validation, and logging with Claude Code hooks

**Location**: Hooks can be configured at multiple levels (see Settings Hierarchy below)

---

## Quick Start

### Understanding Hooks

Claude Code hooks are shell commands that execute at specific workflow events:
- **PreToolUse** - Before tool calls (can block them) ⭐ Most common
- **PostToolUse** - After tool calls complete
- **UserPromptSubmit** - When users submit prompts
- **SessionStart** - On new or resumed sessions
- **Stop** - When Claude finishes responding

**Key Benefit**: Deterministic control over Claude's actions (vs hoping the LLM does it)

**Example Use Cases**:
- Block database query execution without validation
- Auto-format code after edits
- Log all commands for compliance
- Validate file sizes before writes
- Enforce security policies

---

## Hook Examples in This Template

### 1. Query Validation Hook (Production-Ready) ⭐
**Path**: [`query-validation/`](./query-validation/)
**Use case**: Enforce Athena query validation before execution
**Features**:
- Blocks query execution without prior validation
- Whitelist-based early exit for common commands (git, ls, etc.)
- One-time validation markers
- Emergency bypass mechanism

**When to use**: Any project with database queries (Athena, BigQuery, Snowflake, Postgres)

**Installation**: Copy to `~/.claude/hooks/` and configure in `~/.claude/settings.json`

---

### 2. Pre-Commit Format Hook (Example)
**Path**: [`examples/pre-commit-format/`](./examples/pre-commit-format/)
**Use case**: Auto-format code before git commits
**Features**:
- Runs prettier/black on staged files
- Only formats changed files (fast)
- Shows formatting diff to Claude

**When to use**: Projects requiring consistent code formatting

---

### 3. Sensitive File Blocker (Example)
**Path**: [`examples/sensitive-file-blocker/`](./examples/sensitive-file-blocker/)
**Use case**: Prevent edits to production config files
**Features**:
- Blocks Edit/Write tools for specified paths
- Configurable blocklist
- Clear error messages

**When to use**: Projects with sensitive configuration files

---

### 3b. Enhanced Sensitive File Blocker (Example) - NEW
**Path**: [`examples/sensitive-file-blocker/sensitive-file-blocker-enhanced.py`](./examples/sensitive-file-blocker/sensitive-file-blocker-enhanced.py)
**Use case**: Comprehensive secrets/credentials protection
**Features**:
- Multi-strategy detection: exact filenames, extensions, path patterns
- 30+ blocked filenames (vs 4 in basic version)
- Extension blocking (.pem, .key, .p12, .jks, .crt)
- Regex path patterns (/secrets/, /credentials/, etc.)
- SSH key protection (id_rsa, id_ed25519, known_hosts)
- Cloud credentials (.aws/credentials, .gcloud/, .azure/)
- Optional Read blocking

**When to use**: Any project handling credentials or sensitive data

**Attribution**: Based on [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery)

---

### 5. Dangerous Commands Blocker (Example) - NEW
**Path**: [`examples/dangerous-commands-blocker/`](./examples/dangerous-commands-blocker/)
**Use case**: Prevent destructive Bash commands
**Features**:
- Blocks: `rm -rf /`, curl-to-shell, force push to main, DROP DATABASE
- Warns: recursive delete, chmod 777, force push (general)
- Early exit for safe commands (performance)
- Regex-based pattern matching

**When to use**: Any project where Claude executes Bash commands

**Attribution**: Based on [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery)

---

### 4. Command Logger (Example)
**Path**: [`examples/command-logger/`](./examples/command-logger/)
**Use case**: Audit trail of all Bash commands
**Features**:
- Logs all Bash commands to file
- Never blocks execution
- Timestamped entries

**When to use**: Compliance requirements, debugging, learning patterns

---

## Hook Categories

### Validation Hooks (PreToolUse)
**Purpose**: Enforce requirements before allowing operations

**Pattern**: Check conditions → Block if invalid → Provide recovery instructions

**Examples**:
- Query validation (Athena, SQL)
- File size limits
- Permissions checking
- Security scanning
- Syntax validation

**Exit code**: 2 (block execution with error message)

**Best for**:
- Preventing expensive mistakes (full table scans)
- Enforcing team standards
- Security policies

---

### Automation Hooks (PostToolUse)
**Purpose**: Automatically run follow-up actions after tool execution

**Pattern**: Tool completes → Run automation → Never block

**Examples**:
- Auto-formatting after edits
- Updating documentation
- Syncing related files
- Generating types
- Running tests

**Exit code**: 0 (always allow)

**Best for**:
- Reducing manual work
- Maintaining consistency
- Keeping derived files in sync

---

### Logging Hooks (Any event)
**Purpose**: Track Claude's actions for compliance/debugging

**Pattern**: Observe → Log → Never block

**Examples**:
- Command execution logging
- User prompt tracking
- Tool usage metrics
- Security audit trail
- Session analytics

**Exit code**: 0 (always allow)

**Best for**:
- Compliance requirements
- Understanding Claude's patterns
- Debugging issues
- Learning workflow optimization

---

## Settings Hierarchy

Hooks follow Claude Code's settings priority (higher overrides lower):

1. **Enterprise settings** (managed by organization)
2. **CLI arguments** (`--config` flag)
3. **Project local** (`.claude/settings.local.json`) ← Gitignored, personal
4. **Project shared** (`.claude/settings.json`) ← Checked in, team
5. **User global** (`~/.claude/settings.json`) ← Applies to all projects ⭐

**Query validation hook** is configured at level 5 (user global), so it works across all repos.

---

## Configuration Syntax

### Basic Hook Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/my-hook.py"
          }
        ]
      }
    ]
  }
}
```

### Multiple Hooks for Same Event

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/validate-query.py"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/log-commands.py"
          }
        ]
      }
    ]
  }
}
```

### Multiple Matchers

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "bash-hook.sh"}]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "file-hook.py"}]
      }
    ]
  }
}
```

### Matcher Patterns

- `"Bash"` - Only Bash tool
- `"Edit|Write"` - Multiple tools (pipe syntax)
- `"*"` - All tools

**Note**: Matchers are tool names, not command content. To filter by command content, do it in your hook script.

### Exit Codes

- **0** = Allow operation
- **2** = Block operation (stderr shown to Claude)
- **1** = Error (logged, doesn't block)

---

## Installation Patterns

### Pattern A: User Global Hook (Cross-repo) ⭐ Recommended

**Use case**: Query validation, logging, global standards

**Applies to**: All repositories on your machine

**Location**: `~/.claude/settings.json`

**Steps**:
```bash
# 1. Copy hook script to user hooks directory
cp query-validation/validate-query-execution.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/validate-query-execution.py

# 2. Add hook configuration to global settings
# Edit ~/.claude/settings.json and add:
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

# 3. Reload configuration
# Run /hooks in Claude Code, or restart Claude Code

# 4. Test in any repository
git status  # Should work without errors
```

**Pros**:
- Works everywhere automatically
- Single source of truth
- Easy to maintain

**Cons**:
- Affects all projects (use early exit to skip irrelevant repos)

---

### Pattern B: Project Shared Hook (Team standard)

**Use case**: Project-specific validation, team standards

**Applies to**: All team members in this project

**Location**: `.claude/settings.json` (checked into git)

**Steps**:
```bash
# 1. Copy hook script to project hooks directory
mkdir -p .claude/hooks
cp path/to/hook.py .claude/hooks/
chmod +x .claude/hooks/hook.py

# 2. Add hook configuration to project settings
# Edit .claude/settings.json:
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/hook.py"
          }
        ]
      }
    ]
  }
}

# 3. Commit both files
git add .claude/hooks/hook.py .claude/settings.json
git commit -m "Add project hook for X"

# 4. Team members inherit hook automatically
```

**Pros**:
- Team-wide enforcement
- Project-specific logic
- Version controlled

**Cons**:
- Requires team buy-in
- Hook runs for everyone

---

### Pattern C: Project Local Hook (Personal workflow)

**Use case**: Personal automation, experiments

**Applies to**: Only you in this project

**Location**: `.claude/settings.local.json` (gitignored)

**Steps**:
```bash
# 1. Use global hook path or local
# Can reference ~/.claude/hooks/ or .claude/hooks/

# 2. Add hook configuration to local settings
# Edit .claude/settings.local.json:
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/personal-hook.py"
          }
        ]
      }
    ]
  }
}

# 3. Hook only applies to you
# Not checked into git
```

**Pros**:
- Personal customization
- Doesn't affect team
- Can experiment safely

**Cons**:
- Not shared with team
- Per-project configuration

---

## Security Considerations

⚠️ **IMPORTANT**: Hooks execute with your full user permissions

### Safe Practices ✅

- **Review hook code before installation** - Hooks can access any file your user can
- **Use absolute paths** for user global hooks (`~/.claude/hooks/`)
- **Use relative paths** for project hooks (`.claude/hooks/`)
- **Add escape hatches** - Environment variable bypass for emergencies
- **Log hook failures** - Debug issues without breaking workflow
- **Test hooks in safe environment** first
- **Never hardcode secrets** in hook scripts

### Unsafe Practices ❌

- Running unreviewed hook code from unknown sources
- Hardcoding credentials or secrets
- Blocking all operations with no escape hatch
- Hooks that call external services without review
- Hooks that modify files without validation

### Security Example: Escape Hatch

```python
#!/usr/bin/env python3
import os
import sys

# Emergency bypass
if os.environ.get('SKIP_MY_HOOK') == '1':
    sys.exit(0)

# ... hook logic ...
```

**Usage**:
```bash
# Normal: Hook runs
python run_query.py query.sql

# Emergency: Hook skipped
SKIP_MY_HOOK=1 python run_query.py query.sql
```

---

## Hook Development Best Practices

### 1. Early Exit for Common Cases ⭐ Most Important

```python
#!/usr/bin/env python3
import sys
import json

data = json.load(sys.stdin)
tool_name = data.get('tool_name')
command = data.get('tool_input', {}).get('command', '')

# Early exit for whitelisted commands
if command.startswith(('ls', 'cd', 'cat', 'git', 'grep', 'find')):
    sys.exit(0)  # Allow immediately

# ... actual validation logic ...
```

**Why**: Performance - hook runs before EVERY tool use. Early exit saves 90%+ of overhead.

**Impact**: <1ms for whitelisted commands, ~5ms for validation logic

---

### 2. Provide Escape Hatch

```python
# Emergency bypass via environment variable
if os.environ.get('SKIP_VALIDATION') == '1':
    sys.exit(0)
```

**Why**: Don't break workflow when hook malfunctions or needs temporary override

**Usage**: `SKIP_VALIDATION=1 <command>`

---

### 3. Clear Error Messages

```python
if validation_failed:
    error_message = """
❌ Query execution blocked - validation required!

Query: {query_path}

You must validate this query before executing it:

  1. Run validation command:
     /validate-query {query_path}

  2. Fix any errors or warnings

  3. Try executing again

To bypass this check (emergency only):
  SKIP_VALIDATION=1 {command}

Why validation is required:
• Ensures partition filters are present
• Catches timezone handling issues
• Validates Trino/Athena function compatibility
"""
    print(error_message, file=sys.stderr)
    sys.exit(2)
```

**Why**: Claude needs specific recovery instructions to proceed

---

### 4. Handle Errors Gracefully

```python
try:
    # Hook validation logic
    validate_query(query_path)
except Exception as e:
    # Log error but don't block workflow
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(1)  # Error code 1 = log but continue
```

**Why**: Hook bugs shouldn't break Claude's workflow

**Exit code 1**: Logged but doesn't block execution

---

### 5. Read Hook Input Correctly

```python
import json
import sys

def read_hook_input():
    """Read JSON input from stdin."""
    try:
        data = json.load(sys.stdin)
        return data.get('tool_name'), data.get('tool_input', {})
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Hook error: Failed to parse input: {e}", file=sys.stderr)
        sys.exit(1)

tool_name, tool_input = read_hook_input()
```

**Why**: Hooks receive JSON via stdin, must parse correctly

---

## Integration with Other Templates

### Works With Slash Commands

**Example**: `/validate-query` creates marker, hook checks marker

**Pattern**:
1. Slash command runs validation → Creates `/tmp/query_validated_<hash>.marker`
2. User tries to execute query → PreToolUse hook checks for marker
3. If marker exists → Delete marker, allow execution
4. If no marker → Block execution, tell Claude to run `/validate-query`

**Benefit**: Deterministic enforcement (hook guarantees validation ran)

**See also**: [`slash-commands/`](../slash-commands/)

---

### Works With Permissions

**Example**: Hook validates after permission check passes

**Order of execution**:
1. **Permissions system** checks allow/deny list (coarse filtering)
2. If allowed → **Hook runs** (fine-grained validation)
3. Hook can still block if validation fails

**Pattern**: Permissions = "Can this tool run?" → Hooks = "Should this specific operation run?"

**See also**: [`permissions/`](../permissions/)

---

### Works With Anti-Slop Standards

**Example**: Hook enforces CLAUDE.md size limit

**Pattern**:
```python
# PreToolUse hook for Write tool
if file_path == 'CLAUDE.md':
    line_count = len(content.split('\n'))
    if line_count > 200:
        print("❌ CLAUDE.md too long (>200 lines)", file=sys.stderr)
        sys.exit(2)  # Block
```

**Benefit**: Automated enforcement of standards (vs hoping Claude follows them)

**See also**: [`standards/`](../standards/)

---

## Managing Hooks

### Interactive Configuration

```bash
# Run /hooks command in Claude Code
/hooks

# Follow prompts to:
# - Add new hooks
# - Edit existing hooks
# - Delete hooks
# - View current configuration
```

### Manual Configuration

```bash
# User global hooks
nano ~/.claude/settings.json

# Project shared hooks
nano .claude/settings.json

# Project local hooks
nano .claude/settings.local.json
```

### Viewing Active Hooks

```bash
# Run /hooks command and navigate through UI
# Shows all active hooks with their:
# - Event type (PreToolUse, PostToolUse, etc.)
# - Matcher pattern
# - Command
# - Source (User Settings, Local Settings, etc.)
```

---

## Troubleshooting

### Hook Not Running

**Symptoms**: Expected hook behavior not occurring

**Check list**:
1. Is hook configured in correct settings.json? (check hierarchy)
2. Is hook script executable? (`chmod +x hook.py`)
3. Is matcher correct? (tool name case-sensitive: "Bash" not "bash")
4. Is script path correct? (absolute for ~/, relative for .claude/)
5. Check Claude logs for errors
6. Run `/hooks` to view active hooks

**Debug**:
```bash
# Test hook directly
echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | python3 ~/.claude/hooks/my-hook.py
```

---

### Hook Blocking Too Much

**Symptoms**: Hook blocks legitimate operations

**Solutions**:
1. **Add escape hatch**: `SKIP_MY_HOOK=1 <command>`
2. **Refine early exit** - Add more whitelisted commands
3. **Check matcher** - Too broad? (using "*" instead of "Bash")
4. **Add logging** to understand what's being blocked
5. **Temporarily disable** - Remove from settings.json

**Example fix** - Add to whitelist:
```python
# Before
if command.startswith(('ls', 'cd', 'cat')):
    sys.exit(0)

# After (added 'git', 'npm', 'node')
if command.startswith(('ls', 'cd', 'cat', 'git', 'npm', 'node')):
    sys.exit(0)
```

---

### Hook Performance Issues

**Symptoms**: Claude feels slow, tool calls delayed

**Solutions**:
1. **Add early exit** for common commands (90%+ speedup)
2. **Cache expensive checks** (database lookups, API calls)
3. **Optimize regex patterns** (compile once, not per call)
4. **Profile hook execution**: `time echo '{}' | python3 hook.py`

**Performance targets**:
- Early exit: <1ms
- Simple validation: <10ms
- Complex validation: <50ms
- If >100ms: Consider optimization or async pattern

---

### Hook Script Not Found

**Symptoms**: Error like "python3: can't open file '.claude/hooks/hook.py'"

**Causes**:
1. Using `$CLAUDE_PROJECT_DIR` in wrong context
2. Relative path in user global settings (use `~/`)
3. Absolute path in project settings (use relative)
4. Hook script not copied to expected location

**Solutions**:
1. **User global hooks**: Use absolute path `~/.claude/hooks/hook.py`
2. **Project hooks**: Use relative path `.claude/hooks/hook.py`
3. **Verify file exists**: `ls -la ~/.claude/hooks/` or `ls -la .claude/hooks/`
4. **Run `/hooks`** to reload configuration

---

## FAQ

### Q: Can I have multiple hooks for the same event?
**A**: Yes! Configure multiple hooks in the array:
```json
"hooks": [
  {"type": "command", "command": "hook1.py"},
  {"type": "command", "command": "hook2.py"}
]
```
They execute in order. If any hook blocks (exit 2), subsequent hooks don't run.

### Q: Do hooks work in background bash sessions?
**A**: Yes, PreToolUse hooks apply to all tool uses, including background sessions.

### Q: Can hooks modify tool input before execution?
**A**: Yes - read `$CLAUDE_TOOL_INPUT`, modify the JSON, output to stdout with exit 0.

### Q: What's the performance impact?
**A**: Minimal with early exit patterns. Typical: <5ms per hook. With early exit for whitelisted commands: <1ms.

### Q: Can I disable hooks temporarily?
**A**: Yes - three methods:
1. Use escape hatch: `SKIP_HOOK=1 <command>`
2. Remove from settings.json temporarily
3. Comment out in settings.json (JSON doesn't support comments, so remove the hook object)

### Q: Do hooks work for subagents (Task tool)?
**A**: Yes, hooks apply to all tool uses including subagents.

### Q: Can I use hooks in plugins?
**A**: Yes! Plugins can bundle hooks in their `.claude/hooks/` directory. See [official plugin reference](https://docs.claude.com/en/docs/claude-code/plugins-reference).

### Q: Are hooks secure?
**A**: Hooks execute with your user permissions. Review hook code before installation. Use official sources or write your own.

---

## Related Templates

- [**Slash Commands**](../slash-commands/) - `/validate-query` integrates with query validation hook
- [**Permissions**](../permissions/) - Coarse filtering, hooks for fine validation
- [**Anti-Slop Standards**](../standards/) - Hooks can enforce standards automatically
- [**Project Organization**](../projects/) - Hooks can validate .projects/ structure

---

## Complete Technical Reference

For comprehensive hook documentation including:
- All hook events (PreToolUse, PostToolUse, SessionStart, etc.)
- Exit code reference
- Hook input format (Python, Bash, Node.js)
- Environment variables
- Advanced patterns
- Security best practices

**See**: [HOOKS_REFERENCE.md](./HOOKS_REFERENCE.md)

---

## Official Claude Code Documentation

**Primary References**:
- **Hooks Guide**: https://docs.claude.com/en/docs/claude-code/hooks-guide
- **Settings Reference**: https://docs.claude.com/en/docs/claude-code/settings
- **Plugin Reference** (includes hooks): https://docs.claude.com/en/docs/claude-code/plugins-reference

---

**Last Updated**: 2025-11-03
**Maintained By**: dev-setup template library
**Evidence**: Extracted from implementing global query validation hook across 4 repositories
