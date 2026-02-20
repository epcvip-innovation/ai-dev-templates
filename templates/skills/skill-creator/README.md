# Skill Creator

[← Back to Skills](../README.md)

Guided skill scaffolding — from discovery interview to installable skill package.

---

## Quick Start

```bash
# In any Claude Code session:
/skill-creator

# Or use natural language:
"Create a skill for reviewing database migrations"
"Build a new skill"
"Design a skill that generates API docs"
```

---

## What It Does

The skill-creator walks you through 4 phases:

1. **Discovery Interview** — 4 core questions (purpose, triggers, tools, output) + 2-3 adaptive follow-ups
2. **Scaffold Generation** — Produces SKILL.md with archetype-appropriate structure, plus references/ and assets/ as needed
3. **Quality Validation** — 8-criteria rubric check + security validation
4. **Installation Guidance** — Copy commands + customized testing checklist

---

## Three Archetypes

The skill-creator recommends one of three archetypes based on your answers:

| Archetype | When | Examples |
|-----------|------|---------|
| **Workflow Automation** | Multi-step process, consistent methodology | Code review, deployment pipeline, migration audit |
| **Document & Asset Creation** | Produces files or structured content | API docs generator, report builder, skill scaffolding |
| **MCP Enhancement** | Wraps MCP server capabilities | Accessibility audit (Playwright), DB workflow (Supabase) |

---

## Example Output

For "create a skill for database migration review":

```
db-migration-review/
├── SKILL.md                              # Main skill (Workflow Automation archetype)
│   ├── Phase 1: Gather Migrations
│   ├── Phase 2: Analyze Schema
│   ├── Phase 3: Check Patterns
│   └── Phase 4: Report
└── references/
    └── sql-anti-patterns.md              # Common SQL anti-patterns checklist
```

---

## Testing the Skill-Creator Itself

After installing:

1. **Trigger test**: Say "create a skill", "build a new skill", "design a skill", "/skill-creator" — all should load
2. **False positive test**: Say "review my code" — should NOT load (code-review skill should)
3. **Full workflow test**: Create a simple skill end-to-end and install it
4. **Consistency test**: Run twice with same inputs — similar quality output

---

## Installation

```bash
# Global (all projects)
cp -r templates/skills/skill-creator ~/.claude/skills/skill-creator

# Per-project
cp -r templates/skills/skill-creator .claude/skills/skill-creator
```

Do not copy this README.md into the skills directory — it's for browsing the template library.

---

## See Also

- [SKILL-TEMPLATE.md](../SKILL-TEMPLATE.md) — Annotated skill template with all frontmatter fields
- [code-review/](../code-review/) — Example of a complex Workflow Automation skill
- [Extend Claude with skills](https://code.claude.com/docs/en/skills) — Official Anthropic reference for skill architecture, frontmatter fields, and best practices
