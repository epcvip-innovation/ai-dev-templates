---
id: custom-agents
title: "Custom Agents (Subagents)"
description: "Define reusable agents with isolated context windows, custom tools, permissions, and memory"
audience: intermediate
tags: ["agents", "subagents", "isolation", "worktrees"]
---

# Custom Agents (Subagents)

[← Back to Template Library](../README.md)

**Purpose**: Define reusable, task-specific agents that run in isolated context windows with custom system prompts, tools, and permissions.

**Location**: `.claude/agents/` (project-scoped) or `~/.claude/agents/` (global)

---

## What Agents Are

Agents are Markdown files with YAML frontmatter that define isolated Claude instances. Unlike skills (which run in the main conversation), agents get their own context window and can run in the background or in isolated worktrees.

### Quick Decision Tree

| Need | Use |
|------|-----|
| Multi-step workflow in main context | **Skill** (`.claude/skills/`) |
| Isolated task with independent context | **Agent** (`.claude/agents/`) |
| Deterministic validation/formatting | **Hook** (`settings.json`) |
| Explicit utility command | **Flat-file skill** (`.claude/commands/`) |

See [BUILTIN_VS_CUSTOM.md](../../docs/decisions/BUILTIN_VS_CUSTOM.md) for detailed guidance.

---

## Quick Start

### Option 1: Interactive (`/agents` command)

```
/agents
# → Create, edit, delete agents interactively
```

### Option 2: Manual file creation

```bash
mkdir -p .claude/agents
cat > .claude/agents/reviewer.md << 'EOF'
---
name: reviewer
description: Reviews code changes for bugs, security issues, and style violations.
model: sonnet
tools: Read, Grep, Glob, Bash(git diff *)
permissionMode: dontAsk
---

# Code Reviewer

Review the code changes and report issues organized by severity (critical, warning, info).

Focus on:
- Logic errors and edge cases
- Security vulnerabilities
- Violations of project conventions in CLAUDE.md

Do NOT report: formatting, minor style preferences, missing comments.
EOF
```

### Option 3: Ephemeral (CLI flag)

```bash
claude --agents '[{"name":"scanner","tools":["Read","Grep"],"model":"haiku"}]'
```

### Scope & Priority

Agents resolve in this order (first match wins):

| Source | Location | Scope |
|--------|----------|-------|
| `--agents` flag | CLI argument | Session only |
| Project agents | `.claude/agents/` | This project |
| Global agents | `~/.claude/agents/` | All projects |
| Plugin agents | Plugin-provided | Per plugin |

---

## Frontmatter Reference

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | filename | Agent identifier (used in `Task(agent_type)`) |
| `description` | string | required | What the agent does (shown in agent picker) |
| `tools` | list | all | Allowed tools: `Read`, `Grep`, `Bash(git *)`, `MCP(server:github)` |
| `disallowedTools` | list | none | Explicitly blocked tools (overrides `tools`) |
| `model` | string | inherits | `haiku`, `sonnet`, or `opus` |
| `permissionMode` | string | `default` | See Permission Modes below |
| `maxTurns` | number | unlimited | Max agentic turns before stopping |
| `skills` | list | none | Skills to preload into agent context at startup |
| `mcpServers` | list | none | MCP servers available to this agent |
| `hooks` | object | none | Lifecycle hooks scoped to this agent |
| `memory` | string | none | Persistent memory: `user`, `project`, or `local` |
| `background` | boolean | `false` | Always run as a background task |
| `isolation` | string | none | Set to `worktree` for git worktree isolation |

---

## Permission Modes

Control how the agent handles permission prompts:

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Standard prompts | Normal interactive agents |
| `acceptEdits` | Auto-approve file edits, prompt for rest | Trusted refactoring agents |
| `dontAsk` | Auto-deny all prompts (allowed tools still work) | Read-only analysis |
| `bypassPermissions` | Skip all checks | Fully trusted automation (use with caution) |
| `plan` | Read-only exploration | Planning and research |

**Note**: If the parent session uses `bypassPermissions`, it propagates to all subagents.

---

## Common Patterns

### Explorer (read-only, fast)

```yaml
---
name: explorer
description: Fast codebase exploration and pattern discovery.
model: haiku
tools: Read, Grep, Glob, LS
permissionMode: dontAsk
---
```

### Reviewer (focused analysis)

```yaml
---
name: reviewer
description: Reviews code for bugs, security issues, and convention violations.
model: sonnet
tools: Read, Grep, Glob, Bash(git diff *)
permissionMode: dontAsk
maxTurns: 15
---
```

### Implementer (scoped changes, isolated)

```yaml
---
name: implementer
description: Makes focused code changes in an isolated worktree.
model: sonnet
isolation: worktree
permissionMode: acceptEdits
maxTurns: 25
---
```

### Background Researcher

```yaml
---
name: researcher
description: Investigates questions in the background while you keep working.
model: haiku
tools: Read, Grep, Glob, WebSearch, WebFetch
background: true
permissionMode: dontAsk
---
```

### Coordinator (restricts which agents it can spawn)

```yaml
---
name: coordinator
description: Orchestrates worker and researcher agents for complex tasks.
model: opus
tools: Read, Grep, Glob, Task(worker, researcher)
maxTurns: 30
---
```

The `Task(worker, researcher)` syntax restricts which agent types this agent can spawn.

---

## Agent Memory

Agents can maintain persistent state across sessions using `MEMORY.md`:

| Scope | Path | Shared Across |
|-------|------|---------------|
| `user` | `~/.claude/agent-memory/<agent>/MEMORY.md` | All projects, this user |
| `project` | `.claude/agent-memory/<agent>/MEMORY.md` | This project, all users |
| `local` | `.claude/agent-memory-local/<agent>/MEMORY.md` | This project, this user |

The first 200 lines of `MEMORY.md` are automatically included in the agent's system prompt. The agent can read and write to this file during execution.

**Use cases**: Learned project conventions, investigation history, accumulated context about the codebase.

---

## Worktree Isolation

Agents with `isolation: "worktree"` run in a temporary git worktree:

- Changes happen on a separate branch, not in your working tree
- If the agent makes no changes, the worktree is auto-cleaned up
- Useful for experimental changes, parallel implementation attempts, or risky refactors
- Parent `.claude/` directory is still discovered — custom agents, skills, and config work in worktrees
- Subagent transcripts go to `agent-{hash}.jsonl` in the parent project's session directory
- Worktree isolation does not nest — subagents of a worktree-isolated agent share the parent's worktree

**Session-level**: Start the entire session in a worktree with `claude --worktree` or `claude -w`. Add `--tmux` to run in a detached tmux session (fire-and-forget).

**Non-git SCM**: `WorktreeCreate` and `WorktreeRemove` hook events allow worktree-style isolation with Mercurial, Perforce, SVN, or jj (Jujutsu). Define hooks that create/remove workspaces in your SCM when Claude spawns worktree-isolated agents.

See [GIT-WORKTREES.md](../../docs/reference/GIT-WORKTREES.md) for more on worktree workflows.

---

## Agent Teams (Experimental)

Multi-agent collaboration where a lead coordinates independent teammates:

```bash
# Enable
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
# Or in settings: "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }
```

**Architecture**: One session is the lead. Teammates run in independent context windows with a shared task list and inter-agent mailbox. Teammates self-claim tasks; the system manages dependencies.

**Display modes**:
- In-process: all teammates in your terminal (cycle with Shift+Down)
- Split-pane: each teammate in a tmux/iTerm2 pane

**Quality gate hooks**:
- `TeammateIdle`: fires when a teammate is about to idle (exit 2 = keep working)
- `TaskCompleted`: fires when a task is marked complete (exit 2 = reject completion)

**When to use**: Parallel research, competing implementation approaches, cross-layer feature development. **When NOT to use**: Sequential tasks, small changes, when coordination overhead exceeds the work.

**Context management angle**: Because tasks persist on disk (independently of conversation history), each teammate can `/compact` and `/clear` aggressively without losing the project roadmap. The task list is the coordination source of truth, not any teammate's context window. This enables "aggressive context management" — preserving reasoning capacity by clearing noise, while the shared task list maintains continuity.

**Limitations**: ~3-4x token cost, no session resumption for teams, one team per session, no nested teams.

---

## Background Agents

Agents with `background: true` (or any agent backgrounded with Ctrl+B) run while you continue working:

- **Ctrl+B**: Background a running foreground agent
- **Ctrl+F**: Kill all background agents (two-press confirmation)
- Permissions must be pre-approved before launch; unapproved permissions auto-deny
- MCP tools are not available in background mode

---

## See Also

- [Skills](../skills/README.md) — Extensions that run in main context
- [Hooks](../hooks/README.md) — Deterministic lifecycle automation
- [Permissions](../permissions/README.md) — Permission modes and tool access
- [Security Guide](../security/AI-AGENT-SECURITY-GUIDE.md) — Tiered security for agent workflows
- [Advanced Workflows](../../docs/reference/ADVANCED-WORKFLOWS.md) — Context management, planning, agent patterns
- [Context Engineering](../../docs/reference/CONTEXT-ENGINEERING.md) — Five pillars, .claudeignore, isolation as context strategy

---
