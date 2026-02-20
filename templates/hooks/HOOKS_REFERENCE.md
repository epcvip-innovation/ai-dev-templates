# Claude Code Hooks: Technical Reference

[← Back to Hooks README](README.md) | [← Back to Main README](../../README.md)

**Purpose**: Technical reference for implementing Claude Code hooks

**Source**: Official docs at [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) + production experience

---

## Table of Contents

1. [Hook Events](#hook-events)
2. [Exit Codes](#exit-codes)
3. [Configuration](#configuration)
4. [Input Format](#input-format)
5. [Output Format](#output-format)
6. [Matchers](#matchers)
7. [Environment Variables](#environment-variables)
8. [Handler Types](#handler-types)
9. [Performance](#performance)
10. [Testing](#testing)
11. [Advanced Patterns](#advanced-patterns)
12. [Troubleshooting](#troubleshooting)

---

## Hook Events

Claude Code has **15 hook events**. For detailed per-event input fields and decision control schemas, see the [official hooks reference](https://code.claude.com/docs/en/hooks).

| Event | When | Blocks? | Matcher |
|-------|------|---------|---------|
| **SessionStart** | Session begins/resumes | No | `startup`, `resume`, `clear`, `compact` |
| **UserPromptSubmit** | User submits prompt | Yes | None |
| **PreToolUse** | Before tool executes | Yes | Tool name regex |
| **PermissionRequest** | Permission dialog appears | Yes | Tool name regex |
| **PostToolUse** | After tool succeeds | No | Tool name regex |
| **PostToolUseFailure** | After tool fails | No | Tool name regex |
| **Notification** | Notification sent | No | `permission_prompt`, `idle_prompt`, etc. |
| **SubagentStart** | Subagent spawns | No | Agent type |
| **SubagentStop** | Subagent finishes | Yes | Agent type |
| **Stop** | Claude finishes responding | Yes | None |
| **TeammateIdle** | Teammate going idle | Yes | None |
| **TaskCompleted** | Task marked complete | Yes | None |
| **ConfigChange** | Config file changes mid-session | Yes | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| **PreCompact** | Before compaction | No | `manual`, `auto` |
| **SessionEnd** | Session terminates | No | Exit reason |

**Can block (exit 2)**: PreToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, TeammateIdle, TaskCompleted, ConfigChange

**Cannot block**: PostToolUse, PostToolUseFailure, Notification, SubagentStart, SessionStart, SessionEnd, PreCompact

---

## Exit Codes

| Code | Effect | When |
|------|--------|------|
| **0** | Success — continue. Stdout parsed for JSON | Validation passed |
| **2** | Block — stop execution. Stderr fed to Claude | Policy violation |
| **Other** | Non-blocking error — continue. Stderr in verbose mode | Hook malfunction |

**Important**: JSON output is only processed on exit 0. Exit 2 ignores stdout — use stderr for the block reason.

```
Can this event block? (see table above)
├─ YES → Should it proceed?
│  ├─ YES → exit 0 (optionally with JSON output)
│  └─ NO → print reason to stderr, exit 2
└─ NO (PostToolUse, etc.)
   └─ exit 0 (exit 2 shows stderr but does not block)
```

---

## Configuration

### Hook Locations

| Location | Scope | Shareable |
|----------|-------|-----------|
| `~/.claude/settings.json` | All your projects | No |
| `.claude/settings.json` | Single project | Yes (commit to repo) |
| `.claude/settings.local.json` | Single project | No (gitignored) |
| Managed policy settings | Organization-wide | Yes (admin-controlled) |
| Plugin `hooks/hooks.json` | When plugin enabled | Yes |
| Skill/agent frontmatter | While component active | Yes |

### Priority

Hooks from multiple levels are **combined** (all run). For conflicts, higher-priority sources win:

1. **Managed policy** — highest
2. **Project local** (`.claude/settings.local.json`)
3. **Project shared** (`.claude/settings.json`)
4. **User global** (`~/.claude/settings.json`) — lowest

Enterprise: `allowManagedHooksOnly` blocks user/project/plugin hooks.

### Snapshot Behavior

Hooks are **snapshotted at startup**. Mid-session edits require review in the `/hooks` menu before they take effect.

### Disabling Hooks

- **All**: `"disableAllHooks": true` in settings, or toggle in `/hooks` menu
- **Individual**: Remove from settings or delete via `/hooks` menu

### Basic Config

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/my-hook.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Path Resolution

- `$CLAUDE_PROJECT_DIR` — Project root (quote for spaces)
- `$CLAUDE_PLUGIN_ROOT` — Plugin root (for plugin hooks)
- Use absolute paths for global hooks, relative for project hooks

---

## Input Format

### Common Fields (all events, via stdin JSON)

| Field | Description |
|-------|-------------|
| `session_id` | Current session identifier |
| `transcript_path` | Path to conversation JSON |
| `cwd` | Current working directory |
| `permission_mode` | `default`, `plan`, `acceptEdits`, `dontAsk`, or `bypassPermissions` |
| `hook_event_name` | Name of the event |

### Example (PreToolUse)

```json
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "npm test" }
}
```

### Reading Input

**Python**:
```python
import sys, json
data = json.load(sys.stdin)
tool_name = data.get('tool_name')
command = data.get('tool_input', {}).get('command', '')
```

**Bash**:
```bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
```

---

## Output Format

On exit 0, Claude Code parses stdout for JSON.

### Universal Fields

| Field | Default | Description |
|-------|---------|-------------|
| `continue` | `true` | If `false`, Claude stops entirely |
| `stopReason` | — | Message when `continue` is false |
| `suppressOutput` | `false` | Hide stdout from verbose mode |
| `systemMessage` | — | Warning shown to user |

### Decision Control (by event)

| Events | Pattern | Key Fields |
|--------|---------|------------|
| PreToolUse | `hookSpecificOutput` | `permissionDecision` (allow/deny/ask), `permissionDecisionReason`, `updatedInput`, `additionalContext` |
| PermissionRequest | `hookSpecificOutput` | `decision.behavior` (allow/deny), `updatedInput` |
| UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChange | Top-level | `decision: "block"`, `reason` |
| TeammateIdle, TaskCompleted | Exit code only | Exit 2 blocks, stderr is feedback |

### PreToolUse Decision Example

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked"
  }
}
```

Use `updatedInput` to modify tool parameters before execution. Combine with `"allow"` to auto-approve or `"ask"` to show modified input to user.

---

## Matchers

Matchers are **regex strings**. Use `"*"`, `""`, or omit `matcher` to match everything.

### Tool Name Matchers (PreToolUse, PostToolUse, PermissionRequest)

| Pattern | Matches |
|---------|---------|
| `"Bash"` | Bash tool only |
| `"Edit\|Write"` | Edit OR Write |
| `"mcp__.*"` | All MCP tools |
| `"mcp__github__.*"` | GitHub MCP tools |
| `"Notebook.*"` | Notebook tools |

### Other Event Matchers

| Event | Values |
|-------|--------|
| SessionStart | `startup`, `resume`, `clear`, `compact` |
| SessionEnd | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| Notification | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| SubagentStart/Stop | `Bash`, `Explore`, `Plan`, custom names |
| ConfigChange | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| PreCompact | `manual`, `auto` |

**Matchers are case-sensitive**: `"Bash"` works, `"bash"` does not.

---

## Environment Variables

### All Hooks

| Variable | Description |
|----------|-------------|
| `$CLAUDE_PROJECT_DIR` | Project directory (absolute path) |
| `$CLAUDE_CODE_REMOTE` | `"true"` in remote web environments |
| `$CLAUDE_PLUGIN_ROOT` | Plugin root (plugin hooks only) |

### SessionStart Only

| Variable | Description |
|----------|-------------|
| `$CLAUDE_ENV_FILE` | File path to write `export` statements for persisting env vars |

---

## Handler Types

### Command (`type: "command"`)

Shell command. JSON on stdin, communicates via exit codes + stdout/stderr.

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | `"command"` |
| `command` | Yes | Shell command to execute |
| `timeout` | No | Seconds (default: 600) |
| `statusMessage` | No | Custom spinner message |
| `once` | No | Run once per session (skills only) |
| `async` | No | Run in background without blocking |

### Prompt (`type: "prompt"`)

Single-turn LLM evaluation. Returns `{ "ok": true/false, "reason": "..." }`.

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | `"prompt"` |
| `prompt` | Yes | Prompt text (`$ARGUMENTS` = hook input JSON) |
| `model` | No | Model to use (default: fast model) |
| `timeout` | No | Seconds (default: 30) |

### Agent (`type: "agent"`)

Multi-turn subagent with tool access (Read, Grep, Glob). Same response format as prompt hooks.

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | `"agent"` |
| `prompt` | Yes | What to verify (`$ARGUMENTS` = hook input) |
| `model` | No | Model (default: fast model) |
| `timeout` | No | Seconds (default: 60, up to 50 tool-use turns) |

### Async Hooks

Add `"async": true` to command hooks to run in background. Cannot block or return decisions. Output delivered on next conversation turn.

---

## Performance

### Early Exit Pattern

The single most impactful optimization — <1ms for 95% of tool uses:

```python
import sys, json
data = json.load(sys.stdin)

if data.get('tool_name') != 'Bash':
    sys.exit(0)

command = data.get('tool_input', {}).get('command', '')
SAFE = ('ls', 'cd', 'pwd', 'git status', 'git log', 'git diff', 'echo')
if command.startswith(SAFE):
    sys.exit(0)

# Expensive validation only for non-safe commands
import re  # Lazy import
```

### Targets

| Scenario | Target |
|----------|--------|
| Early exit (safe commands) | <1ms |
| Simple validation | <10ms |
| Complex validation | <50ms |
| If >100ms | Needs optimization |

---

## Testing

```bash
# Test allow (should exit 0)
echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' | python3 hook.py
echo "Exit: $?"

# Test deny (exit depends on implementation — exit 2 or exit 0 with deny JSON)
echo '{"tool_name":"Bash","tool_input":{"command":"eval rm -rf /"}}' | python3 hook.py
echo "Exit: $?"

# Test non-Bash passthrough (should exit 0)
echo '{"tool_name":"Read","tool_input":{"file_path":"test.txt"}}' | python3 hook.py
echo "Exit: $?"

# Performance
time echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 hook.py

# Debug mode
claude --debug  # See hook execution details
```

---

## Advanced Patterns

### Externalized Configuration

Load deny/allow patterns from `.conf` files using `Bash()` wrapper format (same syntax as settings.json). Uses bash `case` glob matching — `Bash(env *)` matches "env VAR=x cmd" but NOT "printenv":

```bash
# Conf file format (one pattern per line):
#   Bash(eval)       — exact match
#   Bash(eval *)     — prefix + args
#   Bash(*/deploy.sh *) — CWD-independent glob

# load_patterns() strips the Bash() wrapper for case matching:
load_patterns() {
  local conf_file="$1"
  [[ ! -f "${conf_file}" ]] && return
  while IFS= read -r line; do
    line="${line%%#*}"  # strip comments
    # strip whitespace...
    [[ -z "${line}" ]] && continue
    if [[ "${line}" == Bash\(*\) ]]; then
      local pattern="${line#Bash(}"
      pattern="${pattern%)}"
      printf '%s\n' "${pattern}"
    fi
  done < "${conf_file}"
}

# Match using bash case (glob, not regex/substring):
while IFS= read -r pattern; do
  case "${COMMAND}" in
    ${pattern})  # unquoted = glob expansion
      printf '{"hookSpecificOutput":{"permissionDecision":"deny",...}}\n'
      exit 0
      ;;
  esac
done < <(load_patterns "denied-commands.conf")
```

More auditable (changes visible in PR diffs) and maintainable than hardcoded lists. See [security templates](../security/) for complete examples.

### Escape Hatch

```python
import os
if os.environ.get('SKIP_VALIDATION') == '1':
    sys.exit(0)  # Emergency bypass
```

### CWD-Independent Patterns

```
# In allowed-commands.conf — works regardless of working directory
*/scripts/deploy.sh *
*/scripts/validate.sh *
```

### Stop Hook Loop Prevention

```bash
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
    exit 0  # Prevent infinite loop
fi
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Hook not executing | Run `/hooks` to confirm it's registered. Check case-sensitive matcher (`"Bash"` not `"bash"`). Verify script is executable. Remember: hooks snapshotted at startup. |
| Hook blocking too much | Add escape hatch env var. Expand safe-command early exit. Narrow matcher. |
| Performance issues | Add early exit for safe commands. Use lazy imports. Profile with `time`. |
| Stop hook runs forever | Check `stop_hook_active` field — exit 0 if true. |
| JSON validation failed | Shell profile `echo` statements prepend text to hook output. Guard with `if [[ $- == *i* ]]`. |

---

## Official Documentation

- **Hooks reference**: https://code.claude.com/docs/en/hooks
- **Hooks guide (examples)**: https://code.claude.com/docs/en/hooks-guide
- **Settings**: https://code.claude.com/docs/en/settings
- **Bash validator (reference impl)**: https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py

---

**Last Updated**: 2026-02-19
**Maintained By**: dev-setup template library
