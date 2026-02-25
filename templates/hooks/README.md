# Claude Code Hooks Templates

[← Back to Main README](../../README.md)

**Purpose**: Automate workflow enforcement, validation, and logging with Claude Code hooks

**Location**: Hooks can be configured at multiple levels (see Settings Hierarchy below)

---

## Quick Start

### Understanding Hooks

Claude Code hooks are shell commands (or LLM prompts) that execute at specific workflow events. There are **14 events** — the most common:
- **PreToolUse** - Before tool calls (can block them) — Most common
- **PostToolUse** / **PostToolUseFailure** - After tool calls succeed or fail
- **UserPromptSubmit** - When users submit prompts (can block)
- **PermissionRequest** - When a permission dialog appears (can auto-approve/deny)
- **SessionStart** / **SessionEnd** - Session lifecycle
- **Stop** - When Claude finishes responding (can force continuation)
- **SubagentStart** / **SubagentStop** - Subagent lifecycle
- **TeammateIdle** / **TaskCompleted** - Agent team quality gates
- **Notification** / **PreCompact** - Notifications and context compaction

**Key Benefit**: Deterministic control over Claude's actions (vs hoping the LLM does it)

---

## Hook Examples in This Template

| # | Hook | Path | Use Case | When to Use |
|---|------|------|----------|-------------|
| 1 | **Query Validation** | [`query-validation/`](./query-validation/) | Block query execution without validation | Any project with database queries (Athena, BigQuery, Postgres) |
| 2 | **Pre-Commit Format** | [`examples/pre-commit-format/`](./examples/pre-commit-format/) | Auto-format code before git commits | Projects requiring consistent formatting |
| 3 | **Sensitive File Blocker** | [`examples/sensitive-file-blocker/`](./examples/sensitive-file-blocker/) | Prevent edits to production config | Projects with sensitive config files |
| 3b | **Enhanced File Blocker** | [`examples/sensitive-file-blocker/sensitive-file-blocker-enhanced.py`](./examples/sensitive-file-blocker/sensitive-file-blocker-enhanced.py) | Multi-strategy secrets detection (30+ filenames, SSH/cloud creds) | Projects handling credentials. Based on [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery) |
| 4 | **Command Logger** | [`examples/command-logger/`](./examples/command-logger/) | Audit trail of all Bash commands | Compliance, debugging, learning patterns |
| 5 | **Dangerous Commands Blocker** | [`examples/dangerous-commands-blocker/`](./examples/dangerous-commands-blocker/) | Block `rm -rf /`, curl-to-shell, force push, DROP DATABASE | Any project where Claude executes Bash. Based on [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery) |

---

## Hook Categories

| Category | Event | Pattern | Exit Code | Best For |
|----------|-------|---------|-----------|----------|
| **Validation** | PreToolUse | Check → Block if invalid → Recovery instructions | 2 (block) | Preventing expensive mistakes, enforcing standards |
| **Automation** | PostToolUse | Tool completes → Run follow-up → Never block | 0 (allow) | Auto-formatting, syncing files, generating types |
| **Logging** | Any | Observe → Log → Never block | 0 (allow) | Compliance, debugging, understanding patterns |

---

## Settings Hierarchy

Hooks from multiple levels are **combined** (all run). For settings conflicts, higher-priority sources win:

1. **Managed policy** (organization; can be delivered via macOS plist / Windows Registry) — highest priority
2. **Project local** (`.claude/settings.local.json`) — Gitignored, personal
3. **Project shared** (`.claude/settings.json`) — Checked in, team
4. **User global** (`~/.claude/settings.json`) — Applies to all projects — lowest priority

Additional hook locations: plugin `hooks/hooks.json`, skill/agent frontmatter.

**Important**: Hooks are snapshotted at startup. Mid-session edits require review in `/hooks` menu. Set `"disableAllHooks": true` to temporarily disable all hooks.

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

### Matcher Patterns

Matchers are **regex strings** (not simple strings):

- `"Bash"` - Only Bash tool (exact match)
- `"Edit|Write"` - Multiple tools (regex alternation)
- `"mcp__.*"` - All MCP tools (regex wildcard)
- `"Notebook.*"` - Tools starting with Notebook
- `"*"` or `""` or omitted - All tools

**Note**: Matchers filter by tool name (or event-specific field), not command content. To filter by command content, do it in your hook script. Matchers are case-sensitive.

### Exit Codes

- **0** = Allow operation (stdout parsed for JSON output)
- **2** = Block operation (stderr fed to Claude as feedback). Only works for blocking events: PreToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, TeammateIdle, TaskCompleted
- **Any other** = Non-blocking error (stderr shown in verbose mode, execution continues)

### Hook Handler Types

Three types available:
- `"type": "command"` — Shell command (receives JSON on stdin). Supports `"async": true` for background execution
- `"type": "prompt"` — Single-turn LLM evaluation (returns `{ "ok": true/false }`)
- `"type": "agent"` — Multi-turn subagent with tool access (Read, Grep, Glob)

---

## Installation Patterns

| Pattern | Location | Applies To | Best For |
|---------|----------|------------|----------|
| **A: User Global** | `~/.claude/settings.json` | All repos on your machine | Query validation, logging, global standards |
| **B: Project Shared** | `.claude/settings.json` (in git) | All team members in this project | Project-specific validation, team standards |
| **C: Project Local** | `.claude/settings.local.json` (gitignored) | Only you in this project | Personal automation, experiments |

**Example installation** (Pattern A — recommended for cross-repo hooks):
```bash
# 1. Copy hook script
cp query-validation/validate-query-execution.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/validate-query-execution.py

# 2. Add to ~/.claude/settings.json (see Configuration Syntax above)

# 3. Reload: Run /hooks in Claude Code, or restart

# 4. Test in any repository
git status  # Should work without errors
```

---

## Security Considerations

Hooks execute with your full user permissions.

**Safe practices**: Review hook code before installation. Use absolute paths for global hooks. Add escape hatches. Log failures. Never hardcode secrets.

**Unsafe practices**: Running unreviewed hook code. Hardcoding credentials. Blocking all operations with no escape hatch. Hooks that call external services without review.

### Escape Hatch Pattern

```python
import os, sys
if os.environ.get('SKIP_MY_HOOK') == '1':
    sys.exit(0)
```

---

## Hook Development Best Practices

The five essential practices, with one canonical example:

| Practice | Why | Key Pattern |
|----------|-----|-------------|
| **1. Early exit for common cases** | Performance — hook runs before EVERY tool use | Whitelist safe commands (`ls`, `cd`, `git`) → `sys.exit(0)` |
| **2. Escape hatch** | Don't break workflow on hook malfunction | `SKIP_VALIDATION=1` env var check |
| **3. Clear error messages** | Claude needs specific recovery instructions | Include: what failed, how to fix, how to bypass |
| **4. Handle errors gracefully** | Hook bugs shouldn't break Claude | `except Exception: sys.exit(1)` (log but continue) |
| **5. Read input correctly** | Hooks receive JSON via stdin | `json.load(sys.stdin)` → `tool_name`, `tool_input` |

**Canonical example** (combining all five):
```python
#!/usr/bin/env python3
import sys, json, os

# Practice 2: Escape hatch
if os.environ.get('SKIP_VALIDATION') == '1':
    sys.exit(0)

try:
    # Practice 5: Read input correctly
    data = json.load(sys.stdin)
    command = data.get('tool_input', {}).get('command', '')

    # Practice 1: Early exit for common cases
    if command.startswith(('ls', 'cd', 'cat', 'git', 'grep', 'find')):
        sys.exit(0)

    # ... actual validation logic ...

    if validation_failed:
        # Practice 3: Clear error messages
        print("❌ Blocked: Run /validate-query first", file=sys.stderr)
        sys.exit(2)

except Exception as e:
    # Practice 4: Handle errors gracefully
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(1)
```

**Performance targets**: Early exit <1ms, simple validation <10ms, complex validation <50ms.

---

## Integration with Other Templates

| Template | Integration Pattern |
|----------|-------------------|
| **Skills** | `/validate-query` creates marker file → hook checks marker before allowing execution |
| **Permissions** | Permissions = "Can this tool run?" → Hooks = "Should this specific operation run?" |
| **Anti-Slop Standards** | Hook enforces CLAUDE.md size limit on Write tool (`line_count > 200` → block) |
| **CI Risk Gating** | SHA-marker pattern used for CI comment deduplication — see [RISK-GATING.md](../ci/RISK-GATING.md) Rerun Deduplication section |

---

## Troubleshooting

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Hook not running** | Expected behavior not occurring | Check: correct settings.json? Script executable? Matcher case-sensitive ("Bash" not "bash")? Path correct? |
| **Hook blocking too much** | Legitimate operations blocked | Add escape hatch. Refine early exit whitelist. Check matcher scope. |
| **Performance issues** | Claude feels slow | Add early exit for common commands. Cache expensive checks. Profile: `time echo '{}' \| python3 hook.py` |
| **Script not found** | "can't open file" error | Global hooks: use `~/` absolute path. Project hooks: use relative `.claude/hooks/` path. |

**Debug any hook**:
```bash
echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | python3 ~/.claude/hooks/my-hook.py
```

---

## FAQ

| Question | Answer |
|----------|--------|
| Multiple hooks for same event? | Yes — configure in array. Execute in order. If any blocks (exit 2), subsequent hooks don't run. |
| Hooks in background sessions? | Yes — PreToolUse applies to all tool uses including background sessions. |
| Can hooks modify tool input? | Yes — use `updatedInput` field in `hookSpecificOutput` JSON (exit 0 with JSON to stdout). |
| Performance impact? | Minimal with early exit. Typical: <5ms. With whitelist: <1ms. |
| Disable temporarily? | Escape hatch (`SKIP_HOOK=1`), remove from settings.json, or restart without hook. |
| Work for subagents? | Yes — hooks apply to all tool uses including Task tool subagents. |
| Hooks in plugins? | Yes — plugins can bundle hooks in `.claude/hooks/`. |

---

## Complete Technical Reference

For comprehensive documentation (all events, exit codes, input formats, environment variables, advanced patterns):

**See**: [HOOKS_REFERENCE.md](./HOOKS_REFERENCE.md)

## Official Claude Code Documentation

- **Hooks reference**: https://code.claude.com/docs/en/hooks
- **Hooks guide (examples)**: https://code.claude.com/docs/en/hooks-guide
- **Settings reference**: https://code.claude.com/docs/en/settings

---

**For the determinism philosophy behind hooks** (the predictability stack): see [ADVANCED-WORKFLOWS.md](../../docs/reference/ADVANCED-WORKFLOWS.md).

---

## See Also

- [Security Guide](../security/AI-AGENT-SECURITY-GUIDE.md) — Tiered security best practices using hooks + permissions
- [Skill Templates](../slash-commands/README.md) — Skills that integrate with hooks
- [Permissions](../permissions/README.md) — Coarse-grained access control (hooks add fine-grained)
- [Anti-Slop Standards](../standards/ANTI_SLOP_STANDARDS.md) — Quality standards hooks can enforce
- [All Templates](../README.md)

---

**Last Updated**: 2026-02-19
**Maintained By**: dev-setup template library
**Evidence**: Extracted from implementing global query validation hook across 4 repositories
