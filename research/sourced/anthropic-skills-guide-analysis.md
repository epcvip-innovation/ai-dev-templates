# Anthropic: Complete Guide to Building Skills for Claude

**Source**: [The Complete Guide to Building Skills for Claude](https://claude.com/blog/complete-guide-to-building-skills-for-claude) (Anthropic, January 29, 2026)
**Additional sources**: [Official Claude Code Skills Docs](https://code.claude.com/docs/en/skills), [anthropics/skills GitHub repo](https://github.com/anthropics/skills), [Skill Creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
**Researched**: 2026-02-14

---

## Summary

Anthropic published a 30+ page guide positioning skills as the knowledge layer on top of MCP. Key analogy: "MCP gives Claude the kitchen, Skills give it the recipe." Skills are now an open standard ([agentskills.io](https://agentskills.io)) and work across Claude.ai, Claude Code, and the API.

---

## Key Concepts from the Guide

### 1. Skill Architecture

A skill is a folder with a required `SKILL.md` and optional resources:

```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + markdown instructions
└── Bundled Resources      # Optional
    ├── scripts/           # Executable code (Python/Bash)
    ├── references/        # Docs loaded into context on demand
    └── assets/            # Files used in output (templates, icons, fonts)
```

**Key distinction between resource types**:
- `scripts/` - Executed, not loaded into context. For deterministic, repeatable operations.
- `references/` - Loaded into context on demand. For domain knowledge, schemas, API docs.
- `assets/` - Neither loaded nor executed. Used in output (templates, images, boilerplate).

### 2. Progressive Disclosure (Three Levels)

This is the central design principle:

| Level | What | When Loaded | Size Target |
|-------|------|-------------|-------------|
| 1. Metadata | `name` + `description` from frontmatter | Always in context | ~100 words |
| 2. SKILL.md body | Full instructions | When skill triggers | <500 lines / <5k words |
| 3. Bundled resources | References, scripts, assets | On demand by Claude | Unlimited |

The description field is the **primary triggering mechanism**. All "when to use" information must be in the description, NOT in the body. The body is only loaded after triggering.

### 3. YAML Frontmatter (Official Specification)

Required fields:
- `name` - Lowercase letters, numbers, hyphens (max 64 chars). Becomes the `/slash-command`.
- `description` - What it does AND when to use it. Include specific trigger phrases.

Claude Code additional fields:
- `disable-model-invocation: true` - Only user can invoke (for side-effect skills like `/deploy`)
- `user-invocable: false` - Only Claude can invoke (for background knowledge)
- `allowed-tools` - Restrict which tools Claude can use when skill is active
- `context: fork` - Run in isolated subagent
- `agent` - Which subagent type (`Explore`, `Plan`, `general-purpose`, or custom)
- `argument-hint` - Autocomplete hint (e.g., `[issue-number]`)
- `model` - Override model for this skill
- `hooks` - Lifecycle hooks scoped to this skill

Security restrictions: No XML angle brackets, no reserved terms like "claude" or "anthropic" in frontmatter.

### 4. Invocation Control Matrix

| Frontmatter | User Invokes | Claude Invokes | Context Loading |
|-------------|-------------|----------------|-----------------|
| (default) | Yes | Yes | Description always, body on invoke |
| `disable-model-invocation: true` | Yes | No | Description NOT in context |
| `user-invocable: false` | No | Yes | Description always, body on invoke |

### 5. Three Major Skill Patterns

1. **Document & asset creation** - Reports, presentations, designs using bundled templates/assets
2. **Workflow automation** - Multi-step processes with consistent methodology
3. **MCP enhancement** - Workflow guidance layer on top of MCP tool integrations

### 6. Advanced Features (Claude Code)

**String substitutions**:
- `$ARGUMENTS` - All arguments passed when invoking
- `$ARGUMENTS[N]` or `$N` - Specific argument by index
- `${CLAUDE_SESSION_ID}` - Current session ID

**Dynamic context injection**:
- `` !`command` `` syntax runs shell commands before skill content is sent to Claude
- Output replaces the placeholder (preprocessing, not Claude execution)

**Subagent execution** (`context: fork`):
- Skill runs in isolated context without conversation history
- Skill content becomes the subagent's task prompt
- `agent` field selects execution environment

**Permission control**:
- `Skill(name)` / `Skill(name *)` permission rules
- `allowed-tools` field for per-skill tool restrictions

### 7. Skill Creation Best Practices

From the skill-creator reference:

- **Default assumption: Claude is already very smart.** Only add context Claude doesn't already have.
- **Challenge each piece of information**: "Does Claude really need this explanation?" / "Does this paragraph justify its token cost?"
- **Prefer concise examples over verbose explanations.**
- **Match specificity to task fragility**: High freedom for text-based guidance, medium for pseudocode, low for fragile/deterministic operations.
- **Do NOT include**: README.md, INSTALLATION_GUIDE.md, CHANGELOG.md in the skill itself. Only include what an AI agent needs.
- **Keep SKILL.md under 500 lines.** Split to references when approaching this limit.
- **Avoid deeply nested references** - Keep references one level deep from SKILL.md.
- **Use imperative/infinitive form** in writing.
- **Test scripts by actually running them** before including.

### 8. Progressive Disclosure Patterns

**Pattern 1: High-level guide with references**
```markdown
# PDF Processing
## Quick start
[core instructions]
## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```
Claude only reads the relevant reference file.

**Pattern 3: Conditional details**
Load specialized references only when the user needs those features.

### 9. Testing Framework

Three levels of testing rigor:
1. **Manual** - Fast iteration in Claude.ai
2. **Scripted** - Repeatable validation
3. **Programmatic** - API-based for production

Test coverage should verify:
- Triggers on obvious AND paraphrased requests
- Does NOT trigger on unrelated topics
- Functional correctness, error handling, edge cases
- Baseline comparison (with vs without skill)

Quantitative targets:
- 90%+ trigger rate on relevant queries
- Consistent tool call counts
- Zero failed API calls per workflow

### 10. Distribution Model

| Scope | Location | Audience |
|-------|----------|----------|
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |
| Enterprise | Managed settings | All org users |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled |

Priority: enterprise > personal > project. Plugin skills use namespace (`plugin:skill`).

**Monorepo support**: Nested `.claude/skills/` directories in subdirectories are auto-discovered.

### 11. Visual Output Pattern

Skills can bundle scripts that generate interactive HTML files (e.g., codebase visualizers, dependency graphs, test coverage reports). Claude orchestrates while scripts do heavy lifting.

---

## Gap Analysis: Our Templates vs Anthropic Guide

### What We Do Well

1. **Folder structure** - Our `templates/skills/` follows the recommended `SKILL.md` + `references/` pattern
2. **Progressive disclosure** - Our code-review skill uses `references/` for agent-personas, severity-scoring, technology-patterns
3. **Trigger phrases in description** - Our SKILL.md descriptions include explicit trigger phrases
4. **Multi-agent patterns** - Our code-review is a sophisticated multi-agent workflow
5. **Customization guidance** - SKILL-INSTALLATION.md covers per-project and global install

### Gaps and Opportunities

#### Gap 1: Missing `assets/` Directory Pattern
**Anthropic says**: Skills have three resource types: `scripts/`, `references/`, `assets/` (for templates, icons, fonts used in output).
**We have**: Only `references/` in our examples. No `assets/` usage demonstrated.
**Action**: Document the `assets/` pattern and add examples.

#### Gap 2: No Frontmatter Field Coverage Beyond `name`/`description`
**Anthropic says**: Skills support `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context`, `agent`, `argument-hint`, `model`, `hooks`.
**We have**: Only `name` and `description` in our examples.
**Action**: Document all frontmatter fields with use cases. Several of our skills (e.g., `/push`) should use `disable-model-invocation: true`.

#### Gap 3: No `$ARGUMENTS` Substitution Usage
**Anthropic says**: Skills support `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, `${CLAUDE_SESSION_ID}`.
**We have**: Custom argument parsing documented in SKILL.md body (e.g., `--scope`, `--min-score`).
**Action**: Migrate to official `$ARGUMENTS` substitution pattern where appropriate.

#### Gap 4: Missing Invocation Control
**Anthropic says**: Three invocation modes - both (default), user-only, Claude-only.
**We have**: All skills use default (both). Some skills like code-review should probably be user-only.
**Action**: Add `disable-model-invocation: true` to side-effect skills. Consider `user-invocable: false` for background knowledge skills.

#### Gap 5: No Subagent / Fork Pattern
**Anthropic says**: `context: fork` runs skills in isolated subagents. Can use `agent: Explore` etc.
**We have**: Multi-agent approach in code-review, but uses manual agent simulation, not native subagent execution.
**Action**: Document `context: fork` pattern. Consider whether code-review agents could use native subagent execution.

#### Gap 6: No Dynamic Context Injection (`` !`command` ``)
**Anthropic says**: `` !`gh pr diff` `` syntax runs shell commands before skill content reaches Claude.
**We have**: Shell commands documented as instructions for Claude to execute (Step 2 in code-review).
**Action**: Document `` !`command` `` preprocessing pattern. Evaluate whether code-review could use this for git diff preprocessing.

#### Gap 7: SKILL.md Length Not Tracked
**Anthropic says**: Keep SKILL.md under 500 lines. Challenge every paragraph: "Does this justify its token cost?"
**We have**: Code-review SKILL.md is 175 lines (good), but no guidance on length limits in our templates.
**Action**: Add 500-line limit guidance to plugin creation docs.

#### Gap 8: No `allowed-tools` Usage
**Anthropic says**: Restrict tool access per-skill for safety (e.g., read-only skills).
**We have**: No tool restrictions on any skills.
**Action**: Document `allowed-tools` pattern. Consider adding to review skills (read-only during analysis).

#### Gap 9: No Testing Framework for Skills
**Anthropic says**: Three-level testing (manual, scripted, programmatic). 90%+ trigger rate target.
**We have**: No testing guidance for skills.
**Action**: Add testing section to plugin creation guide.

#### Gap 10: No Permission Control Documentation
**Anthropic says**: `Skill(name)` / `Skill(name *)` permission rules to allow/deny specific skills.
**We have**: No permission control documented for skills.
**Action**: Add permission control section to installation guide.

#### Gap 11: Extraneous Files in Skills
**Anthropic says**: Do NOT include README.md, INSTALLATION_GUIDE.md, CHANGELOG.md inside skills. Only what an AI agent needs.
**We have**: README.md and SKILL-INSTALLATION.md alongside SKILL.md in the same plugin folder.
**Action**: These files are templates for humans, not part of the deployed skill. Clarify this distinction - installed skills should only contain SKILL.md + references/ + scripts/ + assets/.

#### Gap 12: No "Content Type" Guidance (Reference vs Task)
**Anthropic says**: Skills are either "reference content" (conventions, patterns) or "task content" (step-by-step actions). This affects invocation design.
**Action**: Classify our existing skills by content type and document the pattern.

#### Gap 13: Context Budget Awareness
**Anthropic says**: Skill descriptions share a 2% of context window budget (~16k chars fallback). Too many skills may exceed this. Check with `/context`.
**We have**: No mention of context budget concerns.
**Action**: Add context budget awareness to plugin creation docs.

---

## Key Takeaways

1. **Skills are now an open standard** - Not Claude-specific. Design for portability.
2. **Description is everything** - It's the primary trigger mechanism. "When to use" goes in description, not body.
3. **Three resource types** - `scripts/` (execute), `references/` (read into context), `assets/` (use in output). Each has distinct semantics.
4. **Progressive disclosure is the design philosophy** - Three levels: metadata (always), body (on trigger), resources (on demand).
5. **Invocation control matters** - Side-effect skills should be user-only. Background knowledge should be Claude-only.
6. **Token economy is a first-class concern** - Challenge every piece of content. Keep SKILL.md under 500 lines.
7. **Native features we're not using** - `$ARGUMENTS`, `` !`command` ``, `context: fork`, `allowed-tools`, `hooks`.
8. **Testing is recommended** - Three tiers with quantitative targets.
