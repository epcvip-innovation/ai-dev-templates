# AI Agent Security Best Practices

[← Back to Security README](README.md) | [← Back to Main README](../../README.md)

**Purpose**: Tiered security for AI coding agents (Claude Code, Codex, Cursor, etc.)

**Source**: [NVIDIA AI Red Team](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/), [Backslash Security](https://www.backslash.security/blog/claude-code-security-best-practices), [official Claude Code docs](https://code.claude.com/docs/en/hooks)

---

## Why This Matters

AI agents run with your user-level permissions: file read/write/delete, shell commands, network access, and spawning subagents that **bypass the parent CLI's interactive controls**.

They can be manipulated via **indirect prompt injection** — malicious instructions in files, web pages, or tool outputs. They can also bypass deny lists by executing denied commands through approved ones (e.g., `eval "rm -rf /"`).

> "Attackers use indirection — calling restricted tools through approved ones — to bypass application controls."
> — NVIDIA AI Red Team (Jan 2026)

The right model: treat AI agents as **untrusted but powerful interns** (Backslash Security).

### Three Control Surfaces

| Surface | Controls | Mechanism |
|---------|----------|-----------|
| **Permissions** | What tools can run | `settings.json` allow/deny/ask lists |
| **Hooks** | Runtime validation | Shell scripts on events (PreToolUse, etc.) |
| **Settings isolation** | Consistent boundaries | `--setting-sources project`, managed settings |

---

## Tiered Security Levels

### Tier 1 — Baseline

**Every project should have this.** Version-controlled `.claude/settings.json` with:

- **Deny**: `rm -rf`, `sudo`, `git push --force`, `chmod 777`
- **Deny**: `.env` reads (`Read(.env)`, `Read(.env.*)`)
- **Allow**: File tools (Read, Edit, Write, Glob, Grep) for productivity
- **Allow**: `WebFetch(domain:github.com)` — specific domains only, never wildcard

**Setup**: Copy [tier-1-baseline/settings.json.example](tier-1-baseline/settings.json.example) → `.claude/settings.json`

---

### Tier 2 — Team Standard

**Recommended for shared projects.** Adds runtime validation on top of Tier 1:

- **PreToolUse hook** for Bash command filtering (deny/allow/passthrough)
- **Externalized deny/allow in `.conf` files** — auditable via PR diffs, not hardcoded in hooks
- **Bash glob pattern matching** via `case` statement — `Bash(env *)` matches "env VAR=x cmd" but NOT "printenv" (space enforces word boundary)
- **`Bash()` wrapper format** in conf files — same syntax as settings.json, self-documenting
- **Dual entries** for each denied command: `Bash(cmd)` (exact) + `Bash(cmd *)` (with args)
- **Bypass prevention**: Block `eval`, `exec`, `command`, `bash`, `sh`, `env`, `xargs`, `nohup`, `nice`, `time`, `timeout`, `watch` — these execute denied commands indirectly
- **`--setting-sources project`** — prevents personal settings from weakening controls

**How the hook decides**:
1. Deny list checked first → outputs `{"hookSpecificOutput":{"permissionDecision":"deny"}}` to stdout, exit 0
2. Allow list checked second → outputs `{"hookSpecificOutput":{"permissionDecision":"allow"}}` to stdout, exit 0
3. No match → silent exit 0 (passthrough to Claude's normal permission prompt)

**Setup**: Copy [tier-2-team/](tier-2-team/) files → `.claude/hooks/`, then test:
```bash
# Should deny (bypass attempt)
echo '{"tool_name":"Bash","tool_input":{"command":"eval cat /etc/passwd"}}' | \
  bash .claude/hooks/pretooluse-command-filter.sh

# Should allow
echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' | \
  bash .claude/hooks/pretooluse-command-filter.sh

# Should NOT false-positive (printenv is not "env")
echo '{"tool_name":"Bash","tool_input":{"command":"printenv HOME"}}' | \
  bash .claude/hooks/pretooluse-command-filter.sh
```

---

### Tier 3 — Strict

**Production/compliance environments.** Adds on top of Tier 2:

- **Wrapper script** blocking `--dangerously-skip-permissions`
- **Deny interpreters**: `node -e`, `perl -e`, `ruby -e`, `python3 -c`
- **Deny shell equivalents** of dedicated tools (`cat`, `grep`, `find`, `sed`, `awk`) — forces auditable built-in tools
- **Audit logging** (JSONL), **curl denied** (use WebFetch with domain restrictions)
- **CWD-independent patterns**: `*/scripts/deploy.sh *`
- **Managed settings** (`allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`) for enterprise lockdown

**Scoped denies**: Deny `python3 -c *` (arbitrary execution) while allowing `python3 -m compileall *` (specific safe subcommand).

**Setup**: Copy [tier-3-strict/](tier-3-strict/) files. See `wrapper-example.sh` for launch script.

---

### Comparison

| Control | Tier 1 | Tier 2 | Tier 3 |
|---------|--------|--------|--------|
| Settings in version control | Yes | Yes | Yes |
| Destructive command deny list | Yes | Yes | Yes |
| Domain-restricted WebFetch | Yes | Yes | Yes |
| Sensitive file deny rules | Yes | Yes | Yes |
| PreToolUse command filter hook | — | Yes | Yes |
| Externalized deny/allow conf files | — | Yes | Yes |
| Bypass prevention (eval/exec/etc.) | — | Yes | Yes |
| `--setting-sources project` | — | Yes | Yes |
| Wrapper script / interpreter deny | — | — | Yes |
| Audit logging / managed settings | — | — | Yes |

---

## Other Agents

The same principles apply to any AI coding tool:

- **Codex CLI**: Has sandbox modes (read-only, workspace-write, danger-full-access)
- **Cursor**: Uses VS Code sandbox + its own permission model
- **Universal**: Default deny, explicit allowlists, subagent coverage, bypass prevention, config as code, regular audits

---

## Reference

**Official Claude Code**: [Hooks](https://code.claude.com/docs/en/hooks) | [Settings](https://code.claude.com/docs/en/settings) | [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)

**Reference Implementation**: [Bash command validator](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)

**Industry**: [NVIDIA AI Agent Security](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/) | [Backslash Security](https://www.backslash.security/blog/claude-code-security-best-practices)

**Related templates**: [Hooks templates](../hooks/) | [Permissions templates](../permissions/)

---

**Last Updated**: 2026-02-19
**Maintained By**: dev-setup template library
