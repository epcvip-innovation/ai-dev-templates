# Plugin Template

Use this as a starting point when creating a new Claude Code plugin. Copy the directory structure, fill in the templates, and adapt from the doc-review example.

## Directory Structure

```
your-plugin/
├── .claude-plugin/
│   └── plugin.json              # Optional — manifest (auto-discovery works without it)
├── README.md                    # Human docs (not loaded into context at runtime)
├── skills/                      # Recommended — skills as entry points
│   └── your-skill/
│       └── SKILL.md             #   Users invoke via /your-plugin:your-skill
├── commands/                    # Legacy — use skills/ for new plugins
│   └── your-command.md          #   Users invoke via /your-plugin:your-command
├── agents/                      # Optional — specialized agents launched by skills/commands
│   ├── fast-agent.md            #   Haiku: pattern matching, validation, linting
│   └── deep-agent.md            #   Sonnet: judgment, analysis, cross-references
├── hooks/
│   └── hooks.json               # Optional — lifecycle hooks (JSON config)
├── .mcp.json                    # Optional — MCP server configs for this plugin
├── .lsp.json                    # Optional — LSP server configs
├── settings.json                # Optional — default settings applied when enabled
├── outputStyles/                # Optional — custom output styles
└── references/                  # Optional — supporting docs loaded on demand
    └── patterns.md              #   Checklists, domain knowledge, examples
```

> **Minimum viable plugin**: One file in `skills/` or `commands/`. Everything else is optional — Claude Code auto-discovers components in default directories.

---

## Plugin Manifest Template

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin",
  "description": "One-line summary — shown in /plugin list and marketplace",
  "author": {
    "name": "Your Name or Team",
    "email": "you@example.com"
  },
  "version": "1.0.0",
  "homepage": "https://github.com/your-org/your-plugin",
  "repository": "https://github.com/your-org/your-plugin",
  "license": "MIT",
  "keywords": ["category1", "category2"]
}
```

**Naming**: Use lowercase with hyphens. The `name` field must match the directory name.

**Description**: Keep it short — this appears in `/plugin list`. Include the key capability and approximate token cost if significant (e.g., "Notion integration (30k tokens)").

**When to add a manifest**: If you need custom component paths, metadata for marketplace discovery (`homepage`, `keywords`), or bundled MCP/LSP configs. Otherwise skip it — auto-discovery handles defaults.

See [plugin reference](https://code.claude.com/docs/en/plugins-reference) for the full manifest schema.

---

## Skill Template (Recommended)

Create `skills/your-skill/SKILL.md`. This is the recommended entry point — users invoke via `/your-plugin:your-skill`.

```yaml
---
name: your-skill
description: |
  What this skill does — shown in autocomplete. Use when [context].
  Triggers on "/your-plugin:your-skill", "[natural language]".
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Edit", "Task", "AskUserQuestion"]
---
```

Below the frontmatter, write the orchestration instructions (same patterns as commands — determine scope, gather context, launch agents, aggregate results).

See [SKILL-TEMPLATE.md](../skills/SKILL-TEMPLATE.md) for the full skill template with all frontmatter fields.

---

## Hook Config Template

Create `hooks/hooks.json` (same format as the `hooks` key in `settings.json`):

```json
{
  "PreToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
        }
      ]
    }
  ]
}
```

> **`${CLAUDE_PLUGIN_ROOT}`** is replaced at runtime with the plugin's root directory. Use it in hook commands and MCP configs to reference plugin-relative paths.

---

## Command Template (Legacy)

Create `commands/your-command.md`. This is the legacy entry point — users invoke via `/your-plugin:your-command`. For new plugins, prefer `skills/` above.

```yaml
---
description: "What this command does — shown in autocomplete"
argument-hint: "[target] [--flags]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Edit", "Task", "AskUserQuestion"]
---
```

**Below the frontmatter**, write the orchestration instructions. A command typically:

1. **Determines scope** from `$ARGUMENTS` (file, directory, git diff, etc.)
2. **Gathers context** (reads files, builds a summary)
3. **Launches agents** in parallel via the Task tool
4. **Aggregates results** into a consolidated report

### Command body pattern (from doc-review)

```markdown
# Your Command Name

Run [description of what the command orchestrates].

**Target:** "$ARGUMENTS"

## Workflow

1. **Determine Scope**
   - If a file path is given, review that file
   - If a directory is given, find all relevant files
   - If no argument, default to uncommitted changes
   - Parse flags: `--quick`, `--fix`, etc.

2. **Gather Context**
   - Read files, extract metadata
   - Build a shared context summary for agents

3. **Launch Agents**

   Launch applicable agents in **parallel** using the Task tool:

   ` ` `
   Task(subagent_type: "your-plugin:fast-agent", prompt: "Check these files: ...")
   Task(subagent_type: "your-plugin:deep-agent", prompt: "Analyze these files: ...")
   ` ` `

4. **Aggregate Results**

   Produce a consolidated report with sections for each severity level.
```

> **`$ARGUMENTS`**: Replaced at runtime with everything after `/your-plugin:your-command`. Use `$ARGUMENTS[0]`, `$ARGUMENTS[1]`, or `$0`, `$1` for positional args.

> **`allowed-tools`**: Always include `Task` if the command launches agents. Include `AskUserQuestion` if you need interactive confirmation (e.g., `--fix` mode).

---

## Agent Template

Create `agents/your-agent.md`. Agents are launched by commands via the Task tool.

```yaml
---
name: your-agent
description: Use this agent to [action on what]. Launch when [context/trigger]. Pass it [what to include in the prompt — file paths, contents, metadata].
model: haiku
---
```

**Below the frontmatter**, write the agent's procedure. Good agents have:

1. **Role statement** — one sentence saying what the agent does
2. **Procedure** — numbered steps with explicit instructions
3. **Output format** — exact format the agent must produce
4. **Rules** — hard constraints and scope boundaries

### Agent body pattern (from doc-review's link-checker)

```markdown
You are a [role]. Your job is to [specific outcome].

## Procedure

Follow these steps in order for each [unit of work]:

### Step 1: [First action]
[Explicit instructions. Tell the agent exactly what to do, what tools to use.]

### Step 2: [Second action]
[Continue with numbered steps. Be specific about what to check, count, or verify.]

### Step 3: [Produce output]
[Instructions for formatting results.]

## Output Format

` ` `
## {identifier}

[CATEGORY] line {N} — {description}
> "{quoted evidence}"
Suggestion: {actionable fix}
` ` `

If no issues found:
` ` `
## {identifier}
{metric}: {count} — all clean
` ` `

## Rules

- **Verify everything.** Do not assume — use tools to check.
- **Include line numbers.** Vague findings are not actionable.
- **Stay in scope.** Do not flag things another agent handles.
- **Quote evidence.** Every finding must include the relevant text.
```

---

## Model Selection Guide

| Model | Cost | Speed | Use When |
|-------|------|-------|----------|
| **Haiku** | Low | Fast | Pattern matching, validation, linting, counting. The task has clear rules and doesn't need judgment. |
| **Sonnet** | Medium | Medium | Quality assessment, conflict detection, recommendations. The task requires weighing tradeoffs. |
| **Opus** | High | Slow | Complex multi-step reasoning, architectural analysis. Rarely needed for plugin agents. |

**Default to haiku.** Upgrade to sonnet only when haiku produces inconsistent or shallow results. Most plugin agents work well with haiku because they follow explicit procedures.

**doc-review example**: link-checker (haiku — rule-based checking), content-quality (sonnet — judgment about what's bloat vs legitimate), ai-pattern-detector (haiku — pattern matching), cross-file-analyzer (sonnet — judgment about conflicts vs intentional variation).

---

## Agent Design Checklist

- [ ] **Explicit procedure**: Numbered steps, not vague instructions. "Check every link with Glob" not "verify links are correct."
- [ ] **Output format**: Exact template the agent fills in. Include the "all clean" variant.
- [ ] **Rules section**: Hard constraints at the end. What to always do, what to never do.
- [ ] **Scope boundaries**: What this agent handles and what it explicitly doesn't (another agent's job).
- [ ] **Tool usage**: Tell the agent which tools to use for each step. "Use Glob to verify the file exists" not "check if the file exists."
- [ ] **Evidence requirement**: Every finding must include a line number and quoted text.
- [ ] **Graceful empty case**: What to output when there are no findings.

---

## Naming Conventions

| Thing | Convention | Example |
|-------|-----------|---------|
| Plugin directory | `lowercase-with-hyphens` | `doc-review` |
| plugin.json `name` | Must match directory name | `"name": "doc-review"` |
| Skill directories | `skills/<name>/SKILL.md` | `skills/review-docs/SKILL.md` |
| Command files (legacy) | `verb-noun.md` | `review-docs.md` |
| Agent files | `descriptive-role.md` | `link-checker.md`, `content-quality.md` |
| Invocation | `/plugin:skill` or `/plugin:command` | `/doc-review:review-docs` |
| Task subagent_type | `plugin:agent` | `"doc-review:link-checker"` |

---

## Testing Checklist

### Test during development with `--plugin-dir`

```bash
# Load your plugin without installing — fastest iteration loop
claude --plugin-dir /path/to/your-plugin
```

### Validate structure

```bash
# Check plugin structure, manifest, and component discovery
claude plugin validate
```

### Test agents individually

```text
Task(subagent_type: "general-purpose", prompt: "[paste agent instructions] Review this file: [path]")
```

### Full checklist

- [ ] **`claude plugin validate`**: Does the structure pass validation?
- [ ] **Each agent individually**: Does it follow the procedure? Does the output match the format?
- [ ] **Agent with edge cases**: Empty files, huge files, files with no issues, files with many issues
- [ ] **Skill/command orchestration**: Does it correctly determine scope from arguments?
- [ ] **With `--quick`** (if applicable): Does it skip the right agents?
- [ ] **Full end-to-end**: Install the plugin, run the command, verify the consolidated report
- [ ] **Model appropriateness**: Is haiku reliable for each haiku agent? Switch to sonnet if results are inconsistent.

---

## Full Example: doc-review

The [doc-review](./doc-review/) plugin in this directory is a complete working example. It demonstrates:

- **4 agents** with different models (2 haiku, 2 sonnet)
- **1 command** that orchestrates all agents with `--quick` and `--fix` flags
- **Agent scope boundaries** (content-quality explicitly defers cross-file work to cross-file-analyzer)
- **Consolidated report** with severity levels (Critical, Important, Suggestions)
- **plugin.json** with author and version metadata

Read its files in this order for the clearest understanding:
1. `.claude-plugin/plugin.json` — manifest
2. `commands/review-docs.md` — orchestration logic
3. `agents/link-checker.md` — simplest agent (haiku, rule-based)
4. `agents/content-quality.md` — more complex agent (sonnet, judgment-based)

---

## See Also

- [Plugins README](./README.md) — Overview, installation, distribution, marketplace
- [Skills README](../skills/README.md) — Single-workflow skill patterns
- [SKILL-TEMPLATE.md](../skills/SKILL-TEMPLATE.md) — Skill template (simpler alternative)
- [CLAUDE-CODE-CONFIG.md](../../docs/reference/CLAUDE-CODE-CONFIG.md#plugins) — Plugin mechanics and CLI commands

---

**Last Updated**: 2026-02-24
