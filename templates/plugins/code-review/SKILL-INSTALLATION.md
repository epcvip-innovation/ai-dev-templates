# Skill Installation Guide

How to install, configure, and customize code review skills.

## Skill File Structure

A Claude Code skill is a folder containing:

```
skill-name/
├── SKILL.md              # Required: Main skill definition
├── references/           # Optional: Supporting documentation
│   ├── patterns.md       # Domain-specific patterns
│   └── agent-prompts.md  # Agent persona definitions
└── scripts/              # Optional: Helper scripts
    └── gather-context.sh
```

### SKILL.md Format

```yaml
---
name: skill-name
description: What it does and trigger phrases
---

# Skill Title

Markdown documentation describing the workflow.
```

The `description` field tells Claude when to activate this skill.

## Installation Options

### Option 1: Global Install (Recommended)

Available in all projects:

```bash
# Create skills directory if needed
mkdir -p ~/.claude/skills

# Copy the skill
cp -r local-code-review ~/.claude/skills/
cp -r local-code-review-lite ~/.claude/skills/
```

### Option 2: Per-Project Install

Available only in one project:

```bash
# In your project root
mkdir -p .claude/skills
cp -r local-code-review .claude/skills/
```

### Option 3: From This Template Repo

```bash
# Clone and copy
git clone <ai-dev-templates-repo>
cp -r templates/plugins/code-review ~/.claude/skills/local-code-review
```

## Verification

After installation, verify with:

```bash
ls ~/.claude/skills/
# Should show: local-code-review, local-code-review-lite, etc.
```

Then in Claude Code:
```
/local-review
```

## Customization

### Adding Project-Specific Patterns

Edit `references/patterns.md` to add patterns for your codebase:

```markdown
## Your Framework

### Critical Patterns (80+)
- Your ORM-specific anti-patterns
- Your auth library gotchas
- Your API convention violations

### Examples
**Bad:**
\`\`\`typescript
// Your specific anti-pattern
\`\`\`

**Good:**
\`\`\`typescript
// Correct pattern for your codebase
\`\`\`
```

### Adjusting Severity Scoring

Edit `references/agent-prompts.md` to adjust what scores high/low:

```markdown
## Scoring Guidelines (Modified for Your Risk Tolerance)

| Scenario | Score |
|----------|-------|
| Any auth issue | 95+ |  # Stricter for your org
| Missing tests | 70 |    # Higher priority for you
```

### Adding/Removing Agents

Edit `SKILL.md` to modify the agent list:

```markdown
### Step 3: Run N Parallel Review Agents

#### Agent 1: Security Auditor
...

#### Agent 2: Your Custom Agent
**Mindset**: "Your domain-specific paranoia"

Reviews for:
- Your specific concerns
- Your compliance requirements
```

### Creating a Specialized Version

1. Copy the skill folder:
   ```bash
   cp -r ~/.claude/skills/local-code-review ~/.claude/skills/my-review
   ```

2. Edit `SKILL.md`:
   ```yaml
   ---
   name: my-review
   description: My team's specialized code review
   ---
   ```

3. Customize agents and patterns for your needs

## Troubleshooting

### Skill Not Triggering

1. Check skill is in correct location:
   ```bash
   ls ~/.claude/skills/local-code-review/SKILL.md
   ```

2. Verify YAML frontmatter is valid:
   ```yaml
   ---
   name: local-code-review
   description: ...
   ---
   ```

3. Try explicit command: `/local-review`

### Wrong Patterns Being Applied

Skills are matched by description keywords. If wrong skill triggers:
1. Make descriptions more specific
2. Use explicit `/skill-name` commands

### Token Usage Too High

1. Use lite version: `/local-review-lite`
2. Use `--agents security,bugs` to run fewer agents
3. Use `--min-score 80` to reduce output
4. Use `--scope staged` to review smaller diffs

## Uninstalling

```bash
# Remove global skill
rm -rf ~/.claude/skills/local-code-review

# Remove per-project skill
rm -rf .claude/skills/local-code-review
```
