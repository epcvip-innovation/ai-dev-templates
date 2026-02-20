# Frontmatter Reference

Complete YAML frontmatter field specification for Claude Code skills.

---

## Core Fields

### `name`

The skill identifier. Used as the `/name` command trigger. If omitted, defaults to the directory name.

| Rule | Detail |
|------|--------|
| Format | Lowercase letters, numbers, and hyphens only. Max 64 characters. (e.g., `code-review`, `api-docs`) |
| Reserved | Must NOT start with `claude` or `anthropic` |
| Unique | Must not conflict with built-in commands or other installed skills |
| Required | No — defaults to directory name, but always include it for clarity |

> Source: [Official skills docs](https://code.claude.com/docs/en/skills#frontmatter-reference)

### `description`

Controls when Claude auto-triggers the skill. This is the most critical field.

| Rule | Detail |
|------|--------|
| Keep concise | Descriptions share ~2% of context window across all installed skills. Run `/context` to check budget. |
| Structure | `[Action + outcome]` + `[When to use]` + `[Trigger phrases]` + `[Negative triggers]` |
| Recommended | Yes — if omitted, Claude uses the first paragraph of the markdown body |

> Source: [Official skills docs](https://code.claude.com/docs/en/skills#frontmatter-reference)

**Template:**

```yaml
description: |
  [Action verb] [what it does] [outcome]. Use when [context: user asks X,
  uploads Y, needs Z]. Triggers on "/name", "[phrase 1]", "[phrase 2]",
  "[phrase 3]".
  Do NOT use for [negative trigger 1] or [negative trigger 2].
```

**Checklist:**
- [ ] Starts with a verb
- [ ] 2-4 sentences
- [ ] As concise as possible (descriptions share a limited context budget across all skills)
- [ ] 3+ trigger phrases users would actually say
- [ ] Mentions relevant file types or contexts
- [ ] States the outcome / deliverable
- [ ] Includes negative triggers

---

## Optional Fields

Include only when justified by the skill's requirements. Unnecessary fields add noise.

### Invocation Control

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `user-invocable` | boolean | `true` | Set to `false` if the skill should ONLY auto-trigger and never be called via `/name` |
| `disable-model-invocation` | boolean | `false` | Set to `true` to prevent auto-triggering (manual `/name` only) |
| `argument-hint` | string | none | Hint shown in autocomplete: `/name <hint>` (e.g., `"<file-path>"`, `"<url>"`, `"--quick"`) |

**When to use:**
- `user-invocable: false` — rare; for skills that should only trigger on natural language patterns
- `disable-model-invocation: true` — for skills with destructive actions or expensive operations
- `argument-hint` — whenever the skill accepts arguments

### Tool Restriction

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `allowed-tools` | string | none | Tools Claude can use without asking permission when this skill is active |

**Format:** Comma-separated tool names with optional glob syntax.

```yaml
# Examples
allowed-tools: Read, Grep, Glob                    # Read-only skill
allowed-tools: Bash(python:*), Bash(npm:*), Read   # Script execution only
allowed-tools: Read, Write, Grep, Glob, Bash(git:*)  # Standard dev tools
```

**When to use:** When the skill should NOT have access to all tools (e.g., a read-only analysis skill shouldn't use Write or Bash).

### Execution Context

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `model` | string | inherited | Force a specific model: `sonnet`, `opus`, `haiku` |
| `context` | string | none | Set to `fork` to run in an isolated subagent context |
| `agent` | string | `general-purpose` | Which subagent type to use when `context: fork` (`Explore`, `Plan`, `general-purpose`, or custom agent name) |

```yaml
# Force opus for complex reasoning
model: opus

# Run in isolation (doesn't pollute main conversation context)
context: fork
agent: Explore
```

> Source: [Official skills docs — run skills in a subagent](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent)

**When to use:**
- `model` — when the skill requires specific model capabilities (opus for complex analysis, haiku for fast simple tasks)
- `context: fork` — when the skill produces large intermediate output that shouldn't fill the main context
- `agent` — to specify which subagent type runs the forked skill (only relevant with `context: fork`)

### Lifecycle Hooks

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `hooks` | object | none | Shell hooks scoped to this skill's lifecycle |

```yaml
hooks:
  PreToolUse:
    - matcher: Write
      hooks:
        - command: "echo 'Skill writing file: $FILE_PATH'"
  PostToolUse:
    - matcher: Bash
      hooks:
        - command: "./scripts/log-execution.sh"
```

**When to use:** When the skill needs deterministic enforcement (validation, logging, formatting) beyond advisory instructions. Most skills don't need hooks.

### Advanced Fields (Subagent Mode)

These fields apply only when a skill uses `context: fork` to run in a subagent. For the full subagent frontmatter reference, see [Custom Agents](../../agents/README.md).

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `memory` | string | none | Persistent memory scope: `user` (global), `project` (shared), or `local` (personal). Agent's `MEMORY.md` (first 200 lines) auto-loaded into system prompt. |
| `background` | boolean | `false` | Always run the forked agent as a background task. MCP tools unavailable; permissions must be pre-approved. |
| `isolation` | string | none | Set to `worktree` for git worktree isolation. Auto-cleaned if no changes made. |
| `skills` | list | none | Skills to preload into the subagent's context at startup (by name). |
| `mcpServers` | list | none | MCP servers available to this subagent (by server name from config). |

**When to use:**

| Situation | Fields to Add |
|-----------|--------------|
| Skill needs cross-session learning | `memory: user` or `memory: project` |
| Skill should run without blocking | `background: true` (requires `context: fork`) |
| Skill modifies many files safely | `isolation: worktree` (requires `context: fork`) |
| Skill needs domain knowledge from other skills | `skills` list (requires `context: fork`) |
| Skill needs external service access | `mcpServers` list (requires `context: fork`) |

---

## String Substitutions

These placeholders are replaced at runtime when used anywhere in SKILL.md:

| Substitution | Expands To | Example |
|--------------|-----------|---------|
| `$ARGUMENTS` | Full argument string after `/name` | `/review src/` → `$ARGUMENTS` = `"src/"` |
| `$ARGUMENTS[0]` | First argument | `/deploy staging fast` → `$ARGUMENTS[0]` = `"staging"` |
| `$ARGUMENTS[1]` | Second argument | `/deploy staging fast` → `$ARGUMENTS[1]` = `"fast"` |
| `$0`, `$1`, `$2` | Shorthand for `$ARGUMENTS[0]`, `$ARGUMENTS[1]`, `$ARGUMENTS[2]` (0-based) | `/deploy staging fast` → `$0` = `"staging"`, `$1` = `"fast"` |
| `` !`command` `` | Output of shell command at load time | `` !`git branch --show-current` `` → `"main"` |
| `${CLAUDE_SESSION_ID}` | Unique session identifier | For logging or temp file naming |

**Dynamic injection example:**
```yaml
description: |
  Reviews code on the current branch (!`git branch --show-current`).
  Triggers on "/review", "review my changes".
```

---

## Security Rules

| Rule | Consequence |
|------|------------|
| Name starts with `claude` or `anthropic` | Skill rejected at load time |
| XML angle brackets in frontmatter | Skill rejected at load time |
| Description too verbose | Wastes shared context budget; skill may be excluded |
| Body over 500 lines | Works but wastes context; split into references/ |

---

## Decision Matrix: Which Optional Fields?

| Situation | Fields to Add |
|-----------|--------------|
| Skill accepts arguments (e.g., `/name <path>`) | `argument-hint` |
| Read-only analysis skill | `allowed-tools` (restrict to Read, Grep, Glob) |
| Expensive or destructive operation | `disable-model-invocation: true` |
| Needs complex reasoning | `model: opus` |
| Produces large intermediate output | `context: fork` |
| Needs deterministic validation | `hooks` |
| Needs cross-session learning | `memory: user` or `memory: project` (with `context: fork`) |
| Should run without blocking | `background: true` (with `context: fork`) |
| Modifies many files safely | `isolation: worktree` (with `context: fork`) |
| Most skills | **None** — only `name` and `description` |
