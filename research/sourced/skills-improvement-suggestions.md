# Suggested Improvements to Our Skills Guides

**Based on**: [Anthropic Skills Guide Analysis](./anthropic-skills-guide-analysis.md)
**Created**: 2026-02-14
**Priority**: Ordered by impact (highest first)

---

## Priority 1: High Impact, Low Effort

### 1.1 Add Invocation Control to Existing Skills

Our code-review skill auto-triggers on "review my changes" which could fire unexpectedly. Add `disable-model-invocation: true` to side-effect or heavyweight skills.

**Files to update**:
- `templates/skills/code-review/SKILL.md` - Add `disable-model-invocation: true`
- `templates/skills/backlog-management/backlog-complete/SKILL.md` - Add `disable-model-invocation: true` (archives items, has side effects)

**Example**:
```yaml
---
name: local-code-review
description: Multi-agent adversarial code review for local git changes...
disable-model-invocation: true
---
```

### 1.2 Add `allowed-tools` to Review Skills

The code-review skill should be read-only during analysis phases. Adding `allowed-tools` prevents accidental file modifications.

```yaml
---
name: local-code-review
description: ...
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git diff*), Bash(git show*), Bash(git log*)
---
```

### 1.3 Add 500-Line Limit Guidance to Plugin README

Update `templates/skills/README.md` "Creating New Plugins" section to include:
- SKILL.md should stay under 500 lines
- Move detailed content to `references/`
- Challenge every paragraph: "Does this justify its token cost?"

### 1.4 Move "When to Use" from Body to Description

Our code-review SKILL.md has "Trigger Phrases" section in the body. Per Anthropic: all trigger/usage context must be in the `description` field since the body only loads AFTER triggering.

**Current** (body):
```markdown
## Trigger Phrases
- "/local-review", "/local-code-review"
- "review my changes", "review my code"
```

**Should be** (all in description):
```yaml
description: >
  Multi-agent adversarial code review for local git changes.
  Use when asked to "/local-review", "review my changes",
  "review my code", "code review", "review recent work",
  "what did I break", or "check my changes".
  Runs 5 parallel review perspectives, scores findings by severity,
  and outputs actionable fixes.
```

---

## Priority 2: Medium Impact, Medium Effort

### 2.1 Document All Frontmatter Fields

Update `templates/skills/README.md` and `SKILL-INSTALLATION.md` to cover all available frontmatter fields:

```yaml
---
name: skill-name                    # Required. Becomes /slash-command
description: What + when to use     # Required. Primary trigger mechanism
disable-model-invocation: true      # Optional. User-only invocation
user-invocable: false               # Optional. Claude-only (background knowledge)
allowed-tools: Read, Grep, Glob     # Optional. Restrict tool access
context: fork                       # Optional. Run in isolated subagent
agent: Explore                      # Optional. Subagent type (with context: fork)
argument-hint: "[scope] [flags]"    # Optional. Autocomplete hint
model: sonnet                       # Optional. Override model
hooks: ...                          # Optional. Lifecycle hooks
---
```

### 2.2 Document the Three Resource Types

Update plugin structure docs to distinguish:

```
skill-name/
├── SKILL.md              # Required: instructions (<500 lines)
├── scripts/              # Executed by Claude, NOT loaded into context
│   └── validate.py       # Deterministic operations
├── references/           # Loaded into context ON DEMAND
│   └── patterns.md       # Domain knowledge, schemas, API docs
└── assets/               # Used in output, NOT loaded or executed
    └── template.html     # Templates, images, boilerplate
```

### 2.3 Add `$ARGUMENTS` Substitution to Templates

Replace our manual argument parsing with official substitution patterns:

```yaml
---
name: local-code-review
description: ...
argument-hint: "[--scope <type>] [--min-score <n>] [--lite]"
---

Review changes with scope: $ARGUMENTS
```

### 2.4 Add Skill Testing Section

New section in `templates/skills/README.md`:

```markdown
## Testing Skills

### Manual Testing
1. Ask Claude something that should trigger the skill
2. Ask paraphrased versions of the trigger
3. Ask unrelated questions - verify skill does NOT trigger
4. Invoke directly with `/skill-name`

### Validation Checklist
- [ ] Triggers on obvious requests (90%+ target)
- [ ] Does NOT trigger on unrelated topics
- [ ] Handles missing arguments gracefully
- [ ] Output format is consistent across runs
- [ ] Token usage is reasonable (compare with/without skill)

### Check Context Budget
Run `/context` to verify skills aren't exceeding the description budget
(2% of context window, ~16k chars fallback).
```

---

## Priority 3: Medium Impact, Higher Effort

### 3.1 Document `context: fork` Subagent Pattern

Add a new section or reference doc showing how to use native subagent execution:

```yaml
---
name: deep-research
description: Research a topic thoroughly in the codebase
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

This is relevant for our code-review skill - each review agent could potentially run as a native subagent rather than simulated sequential agents.

### 3.2 Document Dynamic Context Injection

Add examples of the `` !`command` `` preprocessing pattern:

```yaml
---
name: pr-review
description: Review a pull request
context: fork
agent: Explore
---

## PR Context
- Diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
- PR description: !`gh pr view`

## Review Instructions
Analyze the above PR context...
```

### 3.3 Add Content Type Classification

Classify skills as reference or task content:

| Type | Purpose | Invocation | Example |
|------|---------|------------|---------|
| **Reference** | Conventions, patterns, domain knowledge | Auto (Claude decides) | API conventions, coding standards |
| **Task** | Step-by-step actions | Manual (`disable-model-invocation: true`) | Deploy, review, commit |

### 3.4 Clarify Template vs Installed Skill Distinction

Our plugin folders contain both template/documentation files (README.md, SKILL-INSTALLATION.md, METHODOLOGY.md) and the actual skill files (SKILL.md, references/). Per Anthropic, installed skills should NOT contain README.md or other extraneous docs.

**Suggested approach**: Add a note to the README clarifying that when installing a skill, only copy:
- `SKILL.md`
- `references/`
- `scripts/`
- `assets/`

Do NOT copy README.md, METHODOLOGY.md, or SKILL-INSTALLATION.md into the installed skill directory.

---

## Priority 4: Lower Priority / Future Consideration

### 4.1 Add Visual Output Pattern Example

Anthropic highlights skills that generate interactive HTML output (codebase visualizers, dependency graphs). We could create a template skill demonstrating this pattern with a bundled Python script.

### 4.2 Add Permission Control Documentation

Document how to allow/deny specific skills:
```
# In /permissions
Skill(local-code-review)     # Allow this specific skill
Skill(deploy *)              # Deny deploy with any args
```

### 4.3 Consider Agent Skills Open Standard

Anthropic published skills as an open standard at [agentskills.io](https://agentskills.io). Our templates could reference this standard and note compatibility with non-Claude tools.

### 4.4 Add Plugin Distribution via GitHub

Anthropic recommends hosting skills on GitHub with:
- Clear README with example usage and screenshots
- Link from MCP documentation
- Installation instructions for Claude Code (`/plugin marketplace add`)

### 4.5 Explore Monorepo Skill Discovery

Claude Code auto-discovers `.claude/skills/` in nested directories (e.g., `packages/frontend/.claude/skills/`). Document this for teams using monorepo structures.
