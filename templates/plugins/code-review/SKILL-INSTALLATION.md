# Skill Installation Guide

How to install, configure, and customize the unified code review skill.

## Skill File Structure

```
code-review/
├── SKILL.md                          # Main skill definition (unified pipeline)
├── review-context.md.template        # Project context template
├── references/
│   ├── agent-personas.md             # Agent definitions with self-evaluation
│   ├── severity-scoring.md           # Scoring guidelines
│   ├── technology-patterns.md        # Language-specific patterns
│   ├── patterns-typescript.md        # TypeScript patterns
│   ├── patterns-react.md             # React patterns
│   ├── patterns-python.md            # Python patterns
│   ├── false-positive-patterns.md    # Evaluation framework
│   └── bug-categories.md             # Root-cause categorization
├── scripts/
│   └── gather-context.sh             # Context gathering helper
├── README.md
├── METHODOLOGY.md
└── SKILL-INSTALLATION.md             # This file
```

## Installation Options

### Option 1: Global Install (Recommended)

Available in all projects:

```bash
mkdir -p ~/.claude/skills
cp -r templates/plugins/code-review ~/.claude/skills/code-review
```

### Option 2: Per-Project Install

Available only in one project:

```bash
mkdir -p .claude/skills
cp -r templates/plugins/code-review .claude/skills/code-review
```

### Option 3: From This Template Repo

```bash
git clone <ai-dev-templates-repo>
cp -r templates/plugins/code-review ~/.claude/skills/code-review
```

## Verification

After installation:

```bash
ls ~/.claude/skills/code-review/SKILL.md
# Should exist
```

Then in Claude Code:
```
/local-review
```

---

## Migration from Old 3-Skill Pipeline

The unified skill replaces three separate skills that were run sequentially:

| Old Skill | Old Command | Now Handled By |
|-----------|-------------|----------------|
| `local-code-review` | `/local-review` | Phase 2 (agents) of unified skill |
| `evaluate-code-review` | `/evaluate-review` | Phase 3 (evaluation) of unified skill |
| `root-cause-analysis` | `/root-cause` | Phase 4 (root-cause) of unified skill |

### Migration steps

1. **Install the unified skill** (see above)
2. **Use `/local-review`** — it now runs all three phases automatically
3. **Old skills are deprecated** — they still work but point to the unified skill
4. **Remove old skills when ready**:
   ```bash
   rm -rf ~/.claude/skills/local-code-review
   rm -rf ~/.claude/skills/local-code-review-lite
   rm -rf ~/.claude/skills/evaluate-code-review
   rm -rf ~/.claude/skills/root-cause-analysis
   ```

### What changed

| Before (3 skills) | After (unified) |
|-------------------|-----------------|
| Run `/local-review`, copy findings, run `/evaluate-review`, copy valid findings, run `/root-cause` | Run `/local-review` — all phases run automatically |
| ~90% false positive rate from agents | Agents self-evaluate (confidence >= 70), then evaluation phase filters further |
| No root-cause unless you remember to run it | Root-cause built in for all surviving findings (skip with `--quick`) |
| `--lite` flag for 3 agents | `--quick` flag for 3 agents + no root-cause |

---

## Customization

### Adding Project-Specific Patterns

Edit `references/technology-patterns.md` or create new `references/patterns-*.md` files:

```markdown
## Your Framework

### Critical Patterns (80+)
- Your ORM-specific anti-patterns
- Your auth library gotchas
```

### Adjusting Severity Scoring

Edit `references/severity-scoring.md`:

```markdown
| Scenario | Score |
|----------|-------|
| Any auth issue | 95+ |  # Stricter for your org
| Missing tests | 70 |    # Higher priority
```

### Adding/Removing Agents

Edit `SKILL.md` Phase 2 and `references/agent-personas.md` to add custom agents.

### Project Context

Copy `review-context.md.template` to `.claude/review-context.md` in your project. Document:
- Known exceptions (vendor requirements, intentional designs)
- Trusted data sources
- Completed work paths
- App scale context

---

## Troubleshooting

### Skill Not Triggering

1. Check skill location: `ls ~/.claude/skills/code-review/SKILL.md`
2. Verify YAML frontmatter is valid
3. Try explicit: `/local-review`

### Both Old and New Skills Triggering

Remove the old skills:
```bash
rm -rf ~/.claude/skills/local-code-review
rm -rf ~/.claude/skills/local-code-review-lite
```

### Token Usage Too High

1. Use quick mode: `/local-review --quick`
2. Use `--min-score 80` to reduce output
3. Use `--scope staged` to review smaller diffs
