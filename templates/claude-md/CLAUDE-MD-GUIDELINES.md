---
id: claude-md-guidelines
title: "CLAUDE.md Guidelines: Keeping It Lightweight"
description: "Reference guide for maintaining CLAUDE.md at 150-200 lines as project complexity grows"
audience: intermediate
tags: ["claude-md", "guidelines", "documentation"]
---

# CLAUDE.md Guidelines: Keeping It Lightweight

**Purpose**: Reference guide for maintaining CLAUDE.md at 150-200 lines as project complexity grows.

**The Problem**: CLAUDE.md files tend to accumulate bloat over time. What starts as 150 lines grows to 500+ as developers add "helpful" information without removing anything.

**The Solution**: Clear criteria for what belongs, quarterly audits, and modular documentation strategy.

---

## Official Guidance

**From Claude Code best practices (as of Nov 1, 2025)**:

- ✅ **Target length**: 100-200 lines maximum
- ✅ **Philosophy**: "Always lightweight" - files are prepended to every prompt
- ❌ **Warning**: "Long CLAUDE.md files are a code smell"
- ❌ **Anti-pattern**: "Bloated files introduce noise and reduce effectiveness"
- ✅ **Strategy**: "Reference separate docs instead of embedding detail"

**Source**: Anthropic official documentation, community best practices, industry guidance (Tyler Burnam, Shipyard)

---

## The Decision Tree

When considering adding content to CLAUDE.md, use this flowchart:

```
┌─────────────────────────────────────────────────────┐
│ Is this information needed for EVERY Claude Code    │
│ session? (80%+ of sessions)                         │
└─────────────────────────────────────────────────────┘
         │
         ├─ NO ──→ Put in separate doc, add 1-line reference in CLAUDE.md
         │
         └─ YES
             │
             ┌─────────────────────────────────────────┐
             │ Can it be explained in < 10 lines?      │
             └─────────────────────────────────────────┘
                  │
                  ├─ NO ──→ Summarize in 3 lines, link to full doc
                  │
                  └─ YES
                      │
                      ┌──────────────────────────────────────────────┐
                      │ Does Claude frequently get this wrong        │
                      │ without explicit guidance in CLAUDE.md?      │
                      └──────────────────────────────────────────────┘
                           │
                           ├─ NO ──→ Move to separate doc or delete
                           │
                           └─ YES ──→ ✅ KEEP IN CLAUDE.md
```

---

## Inclusion Criteria

Content must pass **ALL 3** criteria to belong in CLAUDE.md:

### 1. Frequency of Reference (80%+ sessions)
- ✅ **Include**: Used in 80%+ of sessions
- ❌ **Exclude**: Used occasionally or rarely

**Examples**:
- ✅ "Tailwind v4 uses `@import "tailwindcss"`, not v3's `@tailwind` directives" (used every time working with styles)
- ❌ "Deployment to Railway uses this command" (used once per deploy, not every session)

### 2. Impact on Model Confusion/Drift
- ✅ **Include**: Claude frequently gets this wrong without explicit guidance
- ✅ **Include**: Critical project-specific quirks or deprecated patterns
- ❌ **Exclude**: Standard practices Claude already knows

**Examples**:
- ✅ "DO NOT use `@tailwind base/components/utilities` (v3 syntax) - Claude trained on v3"
- ❌ "Functions should be under 50 lines" (general best practice, not project-specific)

### 3. Uniqueness to This Project
- ✅ **Include**: Project-specific patterns, conventions, workflows
- ❌ **Exclude**: General best practices (those go in CODING_STANDARDS.md)

**Examples**:
- ✅ "Ping tree nodes use `weight` property for distribution, not `probability`" (project-specific)
- ❌ "Use TypeScript strict mode" (general practice, belongs in CODING_STANDARDS.md)

### Corollary: Don't Duplicate Linter-Enforceable Rules

If a pre-commit hook, linter, or CI check already enforces a rule, don't spend CLAUDE.md tokens on it. Claude will see the failure and self-correct. Reserve CLAUDE.md for project-specific patterns that only Claude can know — domain conventions, deprecated API patterns, architectural choices.

If your linter does NOT run automatically (no hook, no CI), the CLAUDE.md entry has value because Claude won't get corrective feedback. For the full framework, see [Consistency at Scale](../../docs/reference/CONSISTENCY-AT-SCALE.md).

---

## Section Length Limits

**Hard rules** to prevent bloat:

| Section | Max Lines | If Over Limit | Example |
|---------|-----------|---------------|---------|
| Project Purpose | 15 | Create PROJECT_OVERVIEW.md | 2-3 sentence description |
| Tech Stack | 10 | Create TECH_STACK.md | Bullet list only |
| Critical Warnings | 30 | Create CONFIGURATION_GUIDE.md | Top 1-2 mistakes only |
| Commands | 10 | Create COMMANDS_REFERENCE.md | 5-10 essential commands |
| Code Patterns | 20 | Create CODING_STANDARDS.md | 1 example + link to full doc |
| Domain Knowledge | 15 | Create DOMAIN_GUIDE.md | Brief summary only |
| Environment | 15 | Create SETUP.md | Essential vars only |
| Documentation Map | 15 | N/A | Always include |

**Rule**: No section should exceed 30 lines. If it does, extract to separate doc.

---

## Reference vs Embed Principle

**The core strategy** for keeping CLAUDE.md lightweight:

### When to Embed (in CLAUDE.md)

✅ **Embed when**:
- Information is used in 80%+ of sessions
- Can be conveyed in <10 lines
- Claude frequently gets it wrong without explicit guidance
- It's project-specific (not general best practice)

**Examples to embed**:
```markdown
## Tech Stack
- React 19 - UI framework with TypeScript
- Tailwind v4 - Utility CSS (Vite plugin, not PostCSS)

## Critical Warnings
**DO NOT** use Tailwind v3 syntax:
- ❌ Don't create postcss.config.js
- ❌ Don't use @tailwind directives
✅ Use @import "tailwindcss" in index.css
```

### When to Reference (link to separate doc)

✅ **Reference when**:
- Would take >10 lines to explain
- Not needed in every session
- General best practices (not project-specific)
- Frequently changes
- Detailed procedures or tutorials

**Examples to reference**:
```markdown
## Code Patterns
We follow anti-slop principles: functions <50 lines, nesting <3, no premature optimization.

**Reference**: See [CODING_STANDARDS.md](./CODING_STANDARDS.md) for complete guidelines with examples

## Deployment
**Reference**: See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for Railway deployment procedures
```

---

## What Belongs in CLAUDE.md vs Separate Docs

### ✅ Keep in CLAUDE.md

| Content Type | Max Lines | Rationale |
|--------------|-----------|-----------|
| Project purpose | 15 | Every session needs context |
| Tech stack list | 10 | Quick reference, list only |
| Critical framework warnings | 30 | Claude gets these wrong (e.g., Tailwind v4 vs v3) |
| Essential commands | 10 | Used in 80%+ of sessions |
| Top 1-2 code patterns | 20 | Project-specific patterns with examples |
| Documentation map | 15 | Navigation to detailed docs |

### ❌ Extract to Separate Docs

| Content Type | Separate Doc | Rationale |
|--------------|--------------|-----------|
| Coding standards | CODING_STANDARDS.md | Not used in every session, can be long |
| Setup instructions | README.md or SETUP.md | One-time operation |
| Domain knowledge | DOMAIN_GUIDE.md | Detailed explanations, formulas |
| Deployment procedures | DEPLOYMENT.md | Infrequent operation |
| API documentation | API_REFERENCE.md | Detailed, reference-style |
| Environment setup | SETUP.md | One-time operation |
| Project planning | backlog/ | Not needed for coding sessions |
| Testing strategy | TESTING.md | Detailed procedures |
| Quality checklists | QUALITY_CHECKLIST.md | Use /ai-review skill instead |
| Architecture decisions | docs/ADR/ | Reference when needed |

---

## Seven Bloat Warning Signs

Run `/audit-claude-md` quarterly to detect these:

### 1. 🔴 Length Bloat (Most Common)
**Warning**: File exceeds 250 lines
**Severity**: Critical if >300 lines, Severe if >500 lines
**Fix**: Extract sections >30 lines to separate docs

### 2. 🔴 Embedded Coding Standards
**Warning**: Sections like "Code Quality", "Coding Standards", "Anti-Slop Rules" in CLAUDE.md
**Severity**: High (these sections often 50-100 lines)
**Fix**: Extract to CODING_STANDARDS.md, keep 3-line summary + link

### 3. 🔴 Embedded Domain Knowledge
**Warning**: Sections with formulas, definitions, tutorials in CLAUDE.md
**Severity**: High (often 30-50 lines)
**Fix**: Extract to DOMAIN_GUIDE.md, keep brief 3-line summary

### 4. 🟡 Long Command Lists
**Warning**: Commands section >20 lines
**Severity**: Medium
**Fix**: Keep 5-10 essential commands, extract rest to COMMANDS_REFERENCE.md

### 5. 🟡 Missing References
**Warning**: Zero "Reference:" or "See [doc]" links found
**Severity**: Medium (indicates everything is embedded)
**Fix**: Extract detailed content to separate docs, add reference links

### 6. 🟡 Duplicate Content
**Warning**: Same section headers/content in both CLAUDE.md and README.md
**Severity**: Low-Medium
**Fix**: Remove from CLAUDE.md, keep in README (user-facing)

### 7. 🟡 Stale Content
**Warning**: Sections added >3 months ago never referenced in sessions
**Severity**: Low
**Fix**: Delete or move to separate reference doc

---

## Good vs Bad Examples

**✅ GOOD** (178 lines): Sections 5-15 lines each, references 4 external docs, framework-specific warnings only, no embedded standards.

**❌ BAD** (512 lines): 89 lines of embedded coding standards, 51 lines of statistical formulas, no modular references. Fix: extract to CODING_STANDARDS.md + STATISTICAL_REFERENCE.md + DEVELOPMENT_GUIDE.md → 178 lines.

**See**: [example-refactored.md](./example-refactored.md) for detailed before/after with full extraction walkthrough.

---

## Quarterly Audit Process

### When to Audit

**Triggers**:
- Every 3 months (quarterly)
- After major feature additions
- When CLAUDE.md exceeds 200 lines
- When team reports "Claude seems confused lately"

### How to Audit

**Step 1: Run audit command**
```bash
/audit-claude-md
```

**Step 2: Review violations**
- Length bloat? (target: 150-200 lines)
- Embedded standards? (should be separate doc)
- Missing references? (should link to docs)
- Long sections? (max 30 lines per section)

**Step 3: Refactor**
- Extract violations to separate docs
- Add reference links
- Test that Claude can still find information

**Step 4: Verify**
- Run `/audit-claude-md` again
- Should show 0-2 warnings maximum
- Length should be 150-220 lines

---

## Migration Strategy (Refactoring Bloated CLAUDE.md)

If your CLAUDE.md is >250 lines, here's how to fix it:

### Step 1: Identify Bloat (10 minutes)
Run `/audit-claude-md` to get violations report

### Step 2: Create Target Docs (15 minutes)
Based on audit, create separate doc files:
```bash
touch CODING_STANDARDS.md    # For embedded code quality rules
touch DOMAIN_GUIDE.md         # For embedded domain knowledge
touch COMMANDS_REFERENCE.md   # If command list >20 lines
touch DEVELOPMENT_GUIDE.md    # For workflow, structure details
```

### Step 3: Extract & Reference (30 minutes)
For each violation:
1. Copy full content to appropriate doc
2. Replace in CLAUDE.md with 3-line summary + link
3. Verify Claude can still find the information

**Example**:
```markdown
<!-- BEFORE (in CLAUDE.md): 89 lines embedded -->
## Code Quality Standards

**Anti-Slop Principles**:
- Functions should be under 50 lines
- Nesting depth should be under 3 levels
- [... 85 more lines ...]

<!-- AFTER (in CLAUDE.md): 3 lines + reference -->
## Code Quality Standards

We follow anti-slop principles: functions <50 lines, nesting <3, no premature optimization.

**Reference**: See [CODING_STANDARDS.md](./CODING_STANDARDS.md) for complete guidelines with grep patterns
```

### Step 4: Verify & Test (10 minutes)
- Run `/audit-claude-md` again (should be clean)
- Check CLAUDE.md length (should be 150-220 lines)
- Test in actual session: Can Claude find the referenced docs?

---

## Enforcement Mechanisms

### 1. Pre-Commit Hook (Recommended)
```bash
# .git/hooks/pre-commit
if [ -f "CLAUDE.md" ]; then
  LINES=$(wc -l < CLAUDE.md)
  if [ $LINES -gt 250 ]; then
    echo "❌ CLAUDE.md is $LINES lines (max 250)"
    echo "Run: /audit-claude-md to fix"
    exit 1
  fi
fi
```

### 2. Quarterly Calendar Reminder
Set recurring calendar event: "Audit CLAUDE.md" every 3 months

### 3. Team Agreement
Add to CLAUDE.md itself:
```markdown
<!-- AUDIT: Run /audit-claude-md quarterly. Last audit: 2025-11-01 -->
```

### 4. Documentation in README
```markdown
## CLAUDE.md Maintenance

**Target**: 150-200 lines (enforced)
**Audit**: Run `/audit-claude-md` quarterly
**Guidelines**: See [templates/claude-md/CLAUDE-MD-GUIDELINES.md](./templates/claude-md/CLAUDE-MD-GUIDELINES.md)
```

---

## Summary: The Lightweight Philosophy

**Core Principle**: CLAUDE.md is a quick-reference card, not a user manual.

**Mental Model**:
- Think of CLAUDE.md as a "cheat sheet" (150-200 lines)
- Think of separate docs as "reference manuals" (unlimited length)
- Claude can read both, but CLAUDE.md is prepended to EVERY prompt

**Three Questions Before Adding Content**:
1. **Frequency**: Will this be used in 80%+ of sessions?
2. **Impact**: Does Claude frequently get this wrong?
3. **Brevity**: Can I explain this in <10 lines?

**If any answer is "no"**: Create separate doc, add 1-line reference.

**For broader context management strategy** (why size matters, `.claudeignore`, token optimization, how compaction works): see [CONTEXT-ENGINEERING.md](../../docs/reference/CONTEXT-ENGINEERING.md) and [ADVANCED-WORKFLOWS.md](../../docs/reference/ADVANCED-WORKFLOWS.md).

---

## Maintenance

### Team Agreement Template

Add to your project's README.md:

```markdown
## CLAUDE.md Maintenance

**Target**: 150-200 lines (enforced)
**Audit**: Run `/audit-claude-md` quarterly
**Guidelines**: See [templates/claude-md/CLAUDE-MD-GUIDELINES.md](./templates/claude-md/CLAUDE-MD-GUIDELINES.md)
```

And add an audit comment to the top of CLAUDE.md itself:

```markdown
<!-- AUDIT: Run /audit-claude-md quarterly. Last audit: YYYY-MM-DD. Next: YYYY-MM-DD -->
```

### Quarterly Review Checklist

Every 3 months (or after major features):
1. Run `/audit-claude-md` — check for length bloat, embedded standards, missing references
2. Extract any section >30 lines to a separate doc
3. Verify all reference links still work
4. Update the audit comment date

### Pre-Commit Hook (Optional)

```bash
# .git/hooks/pre-commit
if [ -f "CLAUDE.md" ]; then
  LINES=$(wc -l < CLAUDE.md)
  if [ $LINES -gt 250 ]; then
    echo "CLAUDE.md is $LINES lines (max 250). Run: /audit-claude-md"
    exit 1
  fi
fi
```

---

## FAQ

**Q: Why 100-200 lines? Seems arbitrary.**
CLAUDE.md is prepended to every prompt. Longer files consume context window, introduce noise, and reduce effectiveness. This target comes from Anthropic's official guidance and community consensus.

**Q: My project is complex. Can't I have 300+ lines?**
Complexity doesn't require a longer CLAUDE.md — it requires better modular docs. Our case study went from 512 → 178 lines without losing any information. The secret: reference separate docs instead of embedding detail.

**Q: Won't separate docs make it harder for Claude to find information?**
No. Claude reads referenced docs on demand. The advantage of a lean CLAUDE.md: every session starts with clear context instead of 500 lines of noise.

**Q: Can I use these principles for non-Claude Code tools?**
Yes. The core principle — keep high-frequency context lightweight, reference detailed docs — applies to Cursor, Copilot, or any LLM-based coding assistant.

---

## See Also

- [Consistency at Scale](../../docs/reference/CONSISTENCY-AT-SCALE.md) — Routing tables, tiered context, ADRs, and the full consistency strategy for large repos
- [CONTEXT-ENGINEERING.md](../../docs/reference/CONTEXT-ENGINEERING.md) — Five pillars, .claudeignore, token optimization
- [ADVANCED-WORKFLOWS.md](../../docs/reference/ADVANCED-WORKFLOWS.md) — Context budgets, planning, agents, predictability

---

**Maintained**: 2026-02-16
**Next Review**: 2026-05-16 (quarterly)
