---
name: skill-creator
description: |
  Guided skill scaffolding with discovery interview, archetype selection, and
  quality validation. Creates complete skill packages (SKILL.md + references/ +
  assets/) ready for installation. Triggers on "/skill-creator", "create a skill",
  "build a new skill", "make a skill", "design a skill", "scaffold a skill".
  Do NOT use for slash commands (use .claude/commands/ directly), hooks
  (see hooks templates), or editing existing skills.
---

# Skill Creator

Guides you through building a Claude Code skill from discovery to installation. Produces a complete skill directory with SKILL.md, optional references/, and assets/.

## Guardrails

**NEVER:**
- Generate a skill without completing the Discovery Interview (Phase 1)
- Skip the quality validation rubric (Phase 3)
- Create skills with names starting with "claude" or "anthropic" (reserved prefixes)
- Put XML angle brackets (`<`, `>`) in YAML frontmatter values
- Write descriptions that waste the shared context budget (all skill descriptions share ~2% of context window)
- Force Complex archetype structure on a simple, linear task
- Include optional frontmatter fields that aren't relevant to the specific skill

**ALWAYS:**
- Ask all 4 core discovery questions before generating anything
- Classify the archetype before generating the scaffold
- Justify the archetype choice by referencing specific discovery answers
- Keep SKILL.md body under 500 lines — move reference material to `references/`
- Mark every user-customizable point with `[CUSTOMIZE: description]`
- Include negative triggers ("Do NOT use for...") in the description
- Validate the generated skill against the quality rubric
- Default to simplicity — upgrade structure only when discovery answers justify it
- Show the complete directory structure before writing files

---

## Phase 1: Discovery Interview

### 1a. Ask 4 Core Questions

Ask these questions one at a time or in a natural batch. Do not skip any.

**Q1 — Purpose**: "What should this skill do? Describe the action and the outcome in 1-2 sentences."

**Q2 — Triggers**: "When should this skill activate? List 3+ phrases a user would say, any relevant file types, and what should NOT trigger it."

**Q3 — Tools**: "What tools does this skill need? (Read, Write, Bash, Grep, Glob, specific MCP servers, external APIs). Will it need to execute scripts?"

**Q4 — Output**: "What does the user get when the skill finishes? (File created, report displayed, actions taken, side effects). Describe the format."

### 1b. Classify Archetype

Based on the answers, select one archetype from `references/archetype-patterns.md`:

| Archetype | Signal Pattern |
|-----------|---------------|
| **Workflow Automation** | Multi-step process, consistent methodology, tools orchestration |
| **Document & Asset Creation** | Produces files/content, high-quality output, format consistency |
| **MCP Enhancement** | Wraps MCP server capabilities, adds workflow guidance on top |

Present the recommendation with justification tied to specific answers:

> "Based on your answers, I recommend **[archetype]** because:
> - [Q1 answer] indicates [reasoning]
> - [Q4 answer] suggests [reasoning]
> - This archetype's structure handles [specific need] well"

If the user disagrees, accommodate their preference and note the trade-offs.

### 1c. Adaptive Follow-ups

Based on the archetype and answers, ask 2-3 follow-up questions. Select from:

| Condition | Follow-up Question |
|-----------|--------------------|
| Multi-phase workflow (Q1) | "How many phases? What are the approval gates between them?" |
| High output variation (Q4) | "Does quality need subjective scoring or is it pass/fail?" |
| MCP Enhancement (archetype) | "Which MCP servers? Do they need specific auth or config?" |
| Reference-heavy domain (Q1) | "Do you have reference docs, checklists, or examples to include?" |
| Repeat use expected (Q1/Q4) | "Will users run this repeatedly? Should it remember preferences?" |
| High-stakes output (Q4) | "Are there safety/compliance concerns? Need disclaimer guardrails?" |

---

## Phase 2: Generate Scaffold

### 2a. Generate Frontmatter

Build the YAML frontmatter using `references/frontmatter-reference.md`:

1. **Recommended**: `name` and `description` (always include; `name` defaults to directory name if omitted)
2. **Optional**: Only include fields justified by discovery answers:
   - `argument-hint` — if the skill accepts arguments
   - `allowed-tools` — if tools should be restricted
   - `model` — if a specific model is needed (e.g., opus for complex reasoning)
   - `context: fork` — if the skill should run in an isolated subagent
   - `context: [paths]` — if specific files should always be loaded
   - `user-invocable` — only if it should NOT be invocable via /name (rare)

### 2b. Generate Body

Start from `assets/skill-scaffold.md` as the base template, then apply archetype-specific patterns from `references/archetype-patterns.md`:

**All archetypes include:**
- Guardrails section (NEVER/ALWAYS rules)
- Step-by-step instructions
- Examples section (2+ scenarios)
- Troubleshooting table

**Archetype-specific additions:**

| Archetype | Additional Sections |
|-----------|-------------------|
| **Workflow Automation** | Phase structure with numbered phases, arguments table if applicable |
| **Document & Asset Creation** | Output format specification, quality criteria, template reference |
| **MCP Enhancement** | MCP server requirements, connection verification step, tool-specific patterns |

### 2c. Progressive Disclosure Decisions

Apply the >50-line rule:

- **Body >500 lines total?** — Must split. Move reference material to `references/`
- **Any single section >50 lines?** — Should split. Extract to a reference file
- **Domain patterns, checklists, rubrics?** — Move to `references/` for on-demand loading
- **Output templates or scaffolds?** — Move to `assets/` (not loaded into context)

### 2d. Present Directory Structure

Show the proposed structure before writing any files:

```
skill-name/
├── SKILL.md                          # Main skill file
├── references/                       # (if needed)
│   └── [domain-patterns.md]          # [purpose]
└── assets/                           # (if needed)
    └── [output-template.md]          # [purpose]
```

Confirm with the user before proceeding to write files.

---

## Phase 3: Quality Validation

### 3a. Apply Quality Rubric

Evaluate the generated skill against 8 criteria from `references/quality-rubric.md`. Score each as **Pass** or **Needs Work**:

1. **Fit to Purpose** — Does the skill solve the stated problem?
2. **Element Justification** — Is every section justified by discovery answers?
3. **Complexity Appropriateness** — Is the structure as simple as possible?
4. **Usability** — Can a user trigger and use it without reading docs?
5. **Completeness** — Are all required sections present?
6. **Spec Adherence** — Does it follow security restrictions and frontmatter rules?
7. **Actionability** — Are instructions concrete enough for Claude to follow?
8. **Trigger Quality** — Will the description achieve 90%+ trigger accuracy?

### 3b. Security Validation

Verify against the security checklist:

- [ ] Name does not start with "claude" or "anthropic"
- [ ] No XML angle brackets in frontmatter
- [ ] Description is concise (shares context budget with all other skills)
- [ ] Body under 500 lines
- [ ] No hardcoded secrets or credentials
- [ ] `allowed-tools` restricts access if the skill doesn't need full tool access

### 3c. Present Results

Show the rubric results in a summary table:

```
Quality Validation:
  Fit to Purpose:            Pass
  Element Justification:     Pass
  Complexity Appropriateness: Pass
  ...

Security Checks:             All passed

[CUSTOMIZE] markers remaining: N locations
```

If any criterion shows "Needs Work", explain what to fix and offer to regenerate that section.

---

## Phase 4: Installation Guidance

### 4a. Install Commands

Provide both options:

```bash
# Global install (available in all projects)
cp -r skill-name ~/.claude/skills/skill-name

# Per-project install
cp -r skill-name .claude/skills/skill-name
```

Remind: Do not copy README.md into the skills directory — it's for humans browsing the template library, not for Claude's context.

### 4b. Testing Checklist

Provide a customized checklist based on the skill's triggers:

```
Testing Checklist:
1. Trigger test: Try these 5 phrases:
   - "[primary trigger]"
   - "[natural language variation 1]"
   - "[natural language variation 2]"
   - "[/skill-name]"
   - "[/skill-name with-argument]"
   Target: 4/5 should load the skill

2. False positive test: Try these unrelated queries:
   - "[similar but different task]"
   - "[adjacent skill's trigger]"
   Target: 0/2 should load the skill

3. Functionality test: Run the full workflow once

4. Consistency test: Run the same task 3 times

5. Context budget: Run /context to check total skill description size
```

---

## Examples

### Example 1: Workflow Automation Skill

**User says**: "Create a skill for database migration review"

**Discovery answers**:
- Q1: Reviews SQL migrations for schema design and data integrity issues
- Q2: "review migration", "check my schema", "/db-review"; NOT for code review
- Q3: Read (SQL files), Grep (pattern matching), Bash (run linters)
- Q4: Markdown report with findings categorized by severity

**Archetype**: Workflow Automation (multi-step review process, consistent methodology)

**Result**: SKILL.md with phases (gather migrations → analyze schema → check patterns → report), references/sql-patterns.md for common anti-patterns, no assets needed.

### Example 2: Document Creation Skill

**User says**: "I want a skill that generates API documentation from code"

**Discovery answers**:
- Q1: Scans source code and generates OpenAPI-style API docs
- Q2: "generate API docs", "document this API", "/api-docs"; NOT for README files
- Q3: Read, Glob (find route files), Grep (extract decorators/annotations)
- Q4: Markdown file with endpoint table, request/response schemas, examples

**Archetype**: Document & Asset Creation (produces formatted documentation)

**Result**: SKILL.md with steps (scan routes → extract schemas → generate docs → validate), assets/api-doc-template.md for consistent output format.

### Example 3: MCP Enhancement Skill

**User says**: "Build a skill that uses Playwright MCP to run accessibility audits"

**Discovery answers**:
- Q1: Navigates to URLs and runs accessibility checks using Playwright
- Q2: "check accessibility", "a11y audit", "/a11y"; NOT for unit tests
- Q3: Playwright MCP (navigation, snapshots), Write (save report)
- Q4: Accessibility report with WCAG violations, severity, and fix suggestions

**Archetype**: MCP Enhancement (wraps Playwright MCP with accessibility workflow)

**Result**: SKILL.md with MCP verification step, audit phases, references/wcag-checklist.md for WCAG criteria.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Generated skill won't trigger | Description lacks specific trigger phrases | Add 3+ phrases users actually say; include /name trigger |
| Skill triggers on wrong queries | Missing negative triggers | Add "Do NOT use for..." to description |
| Skill too complex for the task | Archetype mismatch | Re-evaluate with discovery answers; consider Lightweight equivalent |
| Body exceeds 500 lines | Too much reference material inline | Move checklists/patterns to `references/` directory |
| Description too verbose | Wastes shared context budget | Shorten to action + context + triggers + negative trigger |
| Optional frontmatter confusion | Included fields that aren't needed | Remove optional fields unless discovery answers justify them |

---

## References

| Reference | Purpose |
|-----------|---------|
| [frontmatter-reference.md](./references/frontmatter-reference.md) | Complete YAML frontmatter field specification |
| [archetype-patterns.md](./references/archetype-patterns.md) | 3 skill archetypes with templates and decision matrix |
| [quality-rubric.md](./references/quality-rubric.md) | 8-criteria quality validation rubric |
| [skill-scaffold.md](./assets/skill-scaffold.md) | Base scaffold template with [CUSTOMIZE] markers |
| [SKILL-TEMPLATE.md](../SKILL-TEMPLATE.md) | Full annotated skill template (upstream reference) |
