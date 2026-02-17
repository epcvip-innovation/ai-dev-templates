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
---

# Skill Name

[One-line summary of what this skill does.]

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
└── assets/               # Optional — templates, icons, static files
    └── output-template.md
```

## Skill Categories

Choose the category that best fits your skill:

| Category | When to Use | Examples |
|----------|-------------|---------|
| **Workflow Automation** | Multi-step processes with consistent methodology | Code review, deployment pipelines, backlog management |
| **Document & Asset Creation** | Producing consistent, high-quality outputs | Report generation, mockups, documentation |
| **MCP Enhancement** | Guidance on top of MCP server integrations | Database workflows, API orchestration |

## Description Field Checklist

The description is the most critical field — it controls when Claude auto-triggers the skill.

- [ ] Starts with a verb (action-oriented)
- [ ] 2-4 sentences (not a one-liner)
- [ ] Includes 3+ trigger phrases users would actually say
- [ ] Mentions relevant file types or contexts
- [ ] States the outcome / deliverable
- [ ] Optionally includes negative triggers ("Do NOT use for...")

## Progressive Disclosure

Skills use 3-level progressive disclosure to manage token usage:

| Level | What | When Loaded |
|-------|------|-------------|
| **1** | YAML frontmatter (name + description) | Always — in every conversation |
| **2** | SKILL.md body (instructions, examples) | When Claude determines skill is relevant |
| **3** | references/, scripts/, assets/ | Only when specifically needed during execution |

**Rule of thumb**: If a section is >50 lines of reference material, move it to `references/`.

## Testing Your Skill

1. **Trigger test**: Try 5 natural language variations — does the skill load?
2. **Functionality test**: Run the full workflow — does it produce correct output?
3. **False positive test**: Try unrelated queries — does it avoid loading when it shouldn't?
4. **Consistency test**: Run the same task 3 times — similar quality each time?
