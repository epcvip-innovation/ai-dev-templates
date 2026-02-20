# Skill Template

Use this as a starting point when creating new Claude Code skills. Copy the template below into your skill's `SKILL.md` file and fill in each section.

## Template

```yaml
---
name: your-skill-name
description: |
  [What it does — action + outcome, 1-2 sentences]. Use when [context: user
  asks to do X, uploads Y file type, needs Z]. Triggers on "/your-skill",
  "[natural language phrase 1]", "[natural language phrase 2]".
  Do NOT use for [negative trigger — what this should NOT handle].

# --- Optional fields (include only when relevant) ---
# user-invocable: true              # false = auto-trigger only, never via /name
# allowed-tools: Read, Grep          # Tools auto-approved when skill is active
# model: sonnet                     # Force a specific model (sonnet, opus, haiku)
# context: fork                     # Run as a sub-agent with isolated context
# agent: Explore                    # Subagent type (Explore, Plan, general-purpose)
# argument-hint: "<file-path>"      # Hint shown in autocomplete for /name
# hooks:                            # Shell hooks scoped to this skill
#   PreToolUse:
#     - matcher: Write
#       hooks:
#         - command: "echo 'Writing file'"
# memory: user                       # Persistent memory: user, project, or local (with context: fork)
# background: true                   # Always run as background task (with context: fork)
# isolation: worktree                # Run in isolated git worktree (with context: fork)
# skills:                            # Preload skills into subagent (with context: fork)
#   - api-conventions
# mcpServers:                        # MCP servers for the subagent (with context: fork)
#   - slack
---

# Skill Name

[One-line summary of what this skill does.]

## Guardrails

**NEVER:**
- [Actions or behaviors to avoid]

**ALWAYS:**
- [Required behaviors for consistent output]

## Instructions

### Step 1: [First Major Step]
[Clear explanation of what to do and how.]

### Step 2: [Second Major Step]
[Continue with numbered steps.]

### Step 3: [Output / Deliver Results]
[Describe the expected output format.]

## Examples

### Example 1: [Common Scenario]
**User says**: "[natural language trigger]"
**Actions**:
1. [What the skill does]
2. [Next action]
**Result**: [What the user gets]

### Example 2: [Edge Case or Variation]
**User says**: "[different trigger]"
**Result**: [How the skill handles it differently]

## Troubleshooting

**Problem**: [Common error or unexpected behavior]
**Cause**: [Why it happens]
**Solution**: [How to fix it]

**Problem**: [Another common issue]
**Cause**: [Root cause]
**Solution**: [Fix or workaround]
```

## Directory Structure

```
your-skill-name/
├── SKILL.md              # Required — main skill file (this template)
├── references/           # Optional — supporting docs loaded on demand
│   ├── patterns.md       # Domain-specific patterns or checklists
│   └── examples.md       # Extended examples
├── scripts/              # Optional — executable helpers
│   └── validate.sh       # Validation or data gathering scripts
└── assets/               # Optional — templates used in OUTPUT generation
    └── output-template.md  # NOT loaded into context; used as copy targets
```

> **Note on `assets/`**: Files in `assets/` are templates that the skill copies or adapts when generating output. They are NOT automatically loaded into context — they are read on demand during execution. Use this for scaffolds, boilerplate, and output templates.

## Skill Categories

Choose the category that best fits your skill:

| Category | When to Use | Examples |
|----------|-------------|---------|
| **Workflow Automation** | Multi-step processes with consistent methodology | Code review, deployment pipelines, backlog management |
| **Document & Asset Creation** | Producing consistent, high-quality outputs | Report generation, mockups, documentation |
| **MCP Enhancement** | Guidance on top of MCP server integrations | Database workflows, API orchestration |

## Constraints

| Rule | Detail | Source |
|------|--------|--------|
| **Name format** | Lowercase letters, numbers, hyphens only. Max 64 characters. | [Official docs](https://code.claude.com/docs/en/skills#frontmatter-reference) |
| **No reserved prefixes** | `name` must not start with `claude` or `anthropic` | [Official docs](https://code.claude.com/docs/en/skills#frontmatter-reference) |
| **Body length** | Keep SKILL.md under 500 lines. Move detailed reference material to separate files. | [Official docs](https://code.claude.com/docs/en/skills#add-supporting-files) |
| **Description budget** | Descriptions share ~2% of context window across all skills (fallback: 16,000 chars total). Run `/context` to check. | [Official docs](https://code.claude.com/docs/en/skills#claude-doesnt-see-all-my-skills) |

## String Substitutions

These placeholders are replaced at runtime when used in SKILL.md:

| Substitution | Expands To | Example Use |
|--------------|-----------|-------------|
| `$ARGUMENTS` | Full argument string after `/name` | `Review the following: $ARGUMENTS` |
| `$ARGUMENTS[0]`, `$ARGUMENTS[1]` | Individual space-separated args | `File: $ARGUMENTS[0]` |
| `$0`, `$1`, ... `$N` | Shorthand for `$ARGUMENTS[N]` (0-based) | `Focus on: $0` |
| `` !`command` `` | Output of a shell command at load time | `` Current branch: !`git branch --show-current` `` |

## Context Budget

Skill descriptions are loaded into **every** conversation so Claude knows what's available. The budget scales at 2% of the context window, with a fallback of 16,000 characters total across all skills.

- Check for excluded skills: `/context`
- If skills get excluded, consolidate descriptions or remove unused skills
- Override the limit: set `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var
- The SKILL.md body is only loaded when the skill triggers — body size doesn't affect idle cost

> Source: [Official docs — Claude doesn't see all my skills](https://code.claude.com/docs/en/skills#claude-doesnt-see-all-my-skills)

## Description Field Checklist

The description is the most critical field — it controls when Claude auto-triggers the skill.

- [ ] Starts with a verb (action-oriented)
- [ ] 2-4 sentences (not a one-liner)
- [ ] As concise as possible (descriptions share a limited context budget across all skills)
- [ ] Includes 3+ trigger phrases users would actually say
- [ ] Mentions relevant file types or contexts
- [ ] States the outcome / deliverable
- [ ] Includes negative triggers ("Do NOT use for...")

## Progressive Disclosure

Skills use 3-level progressive disclosure to manage token usage:

| Level | What | When Loaded |
|-------|------|-------------|
| **1** | YAML frontmatter (name + description) | Always — in every conversation |
| **2** | SKILL.md body (instructions, examples) | When Claude determines skill is relevant |
| **3** | references/, scripts/, assets/ | Only when specifically needed during execution |

**Rule of thumb**: If a section is >50 lines of reference material, move it to `references/`.

## Testing Your Skill

1. **Trigger test**: Try 5 natural language variations — does the skill load? Target 90%+ trigger rate.
2. **Functionality test**: Run the full workflow — does it produce correct output?
3. **False positive test**: Try unrelated queries — does it avoid loading when it shouldn't?
4. **Consistency test**: Run the same task 3 times — similar quality each time?
5. **Context budget check**: Run `/context` — are total skill descriptions within budget?

## Installing a Skill

When installing from this template library, copy only the runtime files:

```bash
# Copy skill + references + scripts + assets (runtime files)
cp -r templates/skills/your-skill ~/.claude/skills/your-skill

# Do NOT copy README.md or other human docs into the skills directory
# README.md is for browsing the template library, not for Claude's context
```

For global install (available in all projects): copy to `~/.claude/skills/`
For per-project install: copy to `.claude/skills/` in the project root
