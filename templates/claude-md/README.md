# CLAUDE.md Templates & Guidelines

[← Back to Main README](../../README.md)

**Purpose**: Keep CLAUDE.md lightweight (150-200 lines) as project complexity grows

**The Problem**: CLAUDE.md files bloat over time - what starts as 150 lines grows to 500+ as developers add information without removing anything. Long files introduce noise, reduce Claude Code effectiveness, and are considered a **code smell**.

**The Solution**: Clear criteria for what belongs, automated bloat detection, modular documentation strategy.

---

## Quick Start

### For New Projects

1. **Copy template**: `cp CLAUDE.md.template your-project/CLAUDE.md`
2. **Fill in placeholders**: Replace bracketed sections with your project details
3. **Follow guidance comments**: Each section has inline notes on what belongs
4. **Stay under 200 lines**: If you need more, create separate docs + references

### For Existing Projects (Bloated CLAUDE.md)

1. **Run audit**: Copy `../slash-commands/documentation/audit-claude-md.md` to `.claude/commands/`, run `/audit-claude-md`
2. **Review violations**: Check length, embedded standards, missing references
3. **Follow refactoring guide**: See [example-refactored.md](./example-refactored.md) for step-by-step
4. **Verify**: Run `/audit-claude-md` again (should show 0-2 warnings)

---

## Files in This Template Library

### 1. CLAUDE.md.template (180 lines)
**What it is**: Lightweight template with placeholder sections and inline guidance

**Use when**: Starting a new project

**Key features**:
- Target: 150-180 lines (well under 200-line guidance)
- Inline comments explaining what belongs in each section
- Section length limits (no section >30 lines)
- Emphasis on "reference vs embed" principle
- Examples of good patterns

**How to use**:
1. Copy to your project root
2. Replace placeholders with your project details
3. Delete optional sections you don't need
4. Keep following the guidance comments

---

### 2. CLAUDE-MD-GUIDELINES.md (comprehensive reference)
**What it is**: Complete reference guide for maintaining lightweight CLAUDE.md

**Use when**:
- Deciding "does this belong in CLAUDE.md?"
- Auditing existing CLAUDE.md for bloat
- Teaching team about documentation principles
- As authoritative reference point

**Key sections**:
- **Decision tree**: "Does this belong?" flowchart
- **Inclusion criteria**: Frequency + Impact + Uniqueness (must pass all 3)
- **Section length limits**: Max lines for each section type
- **Reference vs Embed**: When to link vs include
- **Seven bloat warning signs**: What to watch for
- **Good vs Bad examples**: Real repos analyzed

**Critical principle**:
> Content must be used in 80%+ of sessions, have high impact on Claude confusion, AND be project-specific to belong in CLAUDE.md. Otherwise, extract to separate doc.

---

### 3. example-refactored.md (case study)
**What it is**: Real example showing bloat refactoring (512 → 178 lines, 65% reduction)

**Use when**:
- Your CLAUDE.md is bloated (>250 lines)
- Need to see practical refactoring steps
- Want proof that 500+ lines can be reduced without information loss

**Shows**:
- Before/after comparison (dois-test-capacity-planner case study)
- What was extracted to which separate docs
- How to replace embedded content with references
- Verification metrics

**Key lesson**:
> 334 lines extracted to 4 separate docs (CODING_STANDARDS.md, STATISTICAL_REFERENCE.md, DEVELOPMENT_GUIDE.md, archive), reducing from 512 → 178 lines while preserving 100% of information through modular references.

---

### 4. ../slash-commands/documentation/audit-claude-md.md
**What it is**: Automated bloat detection slash command

**Use when**:
- Quarterly (every 3 months)
- After major feature additions
- When CLAUDE.md exceeds 200 lines
- Before creating best practice examples

**Checks**:
1. ✅ Length (target: 100-200 lines, max 250)
2. ✅ Embedded coding standards (should be separate doc)
3. ✅ Embedded domain knowledge (should be separate doc)
4. ✅ Section lengths (max 30 lines per section)
5. ✅ Reference links (modular strategy indicator)
6. ✅ Duplication with README
7. ✅ Common bloat patterns (long command lists, file trees, code examples)

**Output**:
- Violations summary
- Bloat score (% of file that's extractable)
- Specific refactoring recommendations
- Projected final length

---

## The Bloat Problem

### What Causes Bloat?

**Common patterns**:
1. **"Just add it here" mentality**: Every piece of information added to CLAUDE.md without extracting
2. **No periodic audits**: File grows from 150 → 500 over months without intervention
3. **Confusion about purpose**: Treating CLAUDE.md as comprehensive manual vs quick reference
4. **Lack of criteria**: No decision framework for "does this belong?"

### Evidence from Our Repos

| Repo | Lines | Status | Bloat Analysis |
|------|-------|--------|----------------|
| claude-dev-template | 178 | ✅ Good | Appropriate detail for template protection |
| ping-tree-compare | 226 | ⚠️ Minor bloat | ~30 lines extractable (env vars, tech stack) |
| fastapi-service-b | 289 | ❌ Bloated | ~60 lines extractable (coding standards) |
| dois-test-capacity | 512 | ❌❌ Severe bloat | ~334 lines extractable (65% bloat!) |

**Conclusion**: Only 1 of 4 repos met official guidance (100-200 lines). Others demonstrate bloat accumulation over time.

---

## Official Guidance (Updated Jan 2026)

**From Claude Code best practices (v2.1.x)**:
- ✅ Target: **100-200 lines maximum**
- ✅ Philosophy: **"Always lightweight"** - files prepended to every prompt
- ❌ Warning: **"Long CLAUDE.md files are a code smell"**
- ❌ Anti-pattern: **"Bloated files introduce noise and reduce effectiveness"**
- ✅ Strategy: **"Reference separate docs instead of embedding detail"**

**New in 2026:**
- ✅ Use `#` key during sessions to have Claude auto-update CLAUDE.md
- ✅ Use "think", "think hard", or "ultrathink" for extended reasoning on complex problems
- ✅ Hub-and-spoke pattern is now industry standard (see below)

**Sources**: [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices), community patterns, industry guidance

---

## The Lightweight Philosophy

### Core Principle
**CLAUDE.md is a quick-reference card, not a user manual.**

**Mental model**:
- CLAUDE.md = "cheat sheet" (150-200 lines, every prompt)
- Separate docs = "reference manuals" (unlimited length, referenced when needed)

### Three Questions Before Adding Content

**Ask yourself**:
1. **Frequency**: Will this be used in 80%+ of sessions?
2. **Impact**: Does Claude frequently get this wrong without explicit guidance?
3. **Brevity**: Can I explain this in <10 lines?

**If any answer is "no"**: Create separate doc, add 1-line reference in CLAUDE.md.

---

## What Belongs vs What Doesn't

### ✅ Keep in CLAUDE.md (with length limits)

| Content | Max Lines | Example |
|---------|-----------|---------|
| Project purpose | 15 | "This is a [type] for [purpose]" |
| Tech stack | 10 | Bullet list only, no setup details |
| Critical warnings | 30 | Framework quirks Claude gets wrong (Tailwind v4 vs v3) |
| Essential commands | 10 | 5-10 commands used in 80%+ of sessions |
| Top code patterns | 20 | 1-2 project-specific examples + link to full doc |
| Documentation map | 15 | "See [CODING_STANDARDS.md] for quality guidelines" |

### ❌ Extract to Separate Docs

| Content | Separate Doc | Rationale |
|---------|--------------|-----------|
| Coding standards | CODING_STANDARDS.md | Not needed every session, can be long |
| Setup instructions | README.md or SETUP.md | One-time operation |
| Domain knowledge | DOMAIN_GUIDE.md | Detailed explanations, formulas |
| Deployment procedures | DEPLOYMENT.md | Infrequent operation |
| API documentation | API_REFERENCE.md | Reference-style, detailed |
| Quality checklists | Use `/ai-review` command | Automation > documentation |
| Architecture decisions | docs/ADR/ | Historical reference |

---

## Modular Documentation Strategy

### The Core Pattern: Reference, Don't Embed

**Bad (embedded)**:
```markdown
## Code Quality Standards

### Anti-Slop Principles
- Functions <50 lines
- Nesting <3 levels
- No premature optimization
- [... 85 more lines of standards, examples, checklists ...]
```

**Good (referenced)**:
```markdown
## Code Quality Standards

We follow anti-slop principles: functions <50 lines, nesting <3, no premature optimization.

**Reference**: See [CODING_STANDARDS.md](./CODING_STANDARDS.md) for complete guidelines with examples
```

**Result**: 89 lines → 3 lines in CLAUDE.md, 100% information preserved in separate doc

### Hub-and-Spoke Pattern

The recommended architecture for project documentation:

```
CLAUDE.md (hub - 150-200 lines)
├── CODING_STANDARDS.md (spoke)
├── docs/ARCHITECTURE.md (spoke)
├── .claude/review-context.md (spoke)
└── backlog/_INDEX.md (spoke)
```

**Hub contains** (always loaded):
- Project purpose (15 lines)
- Tech stack overview (10 lines)
- Critical warnings Claude gets wrong (30 lines)
- Navigation to spokes (15 lines)
- Essential commands (10 lines)

**Spokes contain** (loaded when needed):
- Detailed coding standards
- Architecture decisions
- Domain knowledge
- Review context
- Backlog/task lists

**Why it works:**
- Hub is always in context (every session)
- Spokes are loaded on-demand (when relevant)
- Total information: unlimited
- Context cost: minimal (150-200 lines vs 500+)

---

## Typical Refactoring Workflow

### Step 1: Audit (5 minutes)
```bash
# Copy audit command to your project
cp templates/slash-commands/documentation/audit-claude-md.md .claude/commands/

# Run audit
/audit-claude-md
```

**Output**:
```
📏 Length: 512 lines 🔴 CRITICAL
📚 References: 0 links 🔴
📊 Bloat Score: ~334 lines extractable (65%)

Violations:
🔴 Embedded coding standards (164 lines)
🔴 Embedded domain knowledge (67 lines)
🔴 No modular references
```

### Step 2: Plan Extraction (10 minutes)
Based on violations, decide which docs to create:
- CODING_STANDARDS.md (for embedded quality rules)
- DOMAIN_GUIDE.md (for embedded domain knowledge)
- DEVELOPMENT_GUIDE.md (for embedded workflow details)

### Step 3: Create Separate Docs (5 minutes)
```bash
touch CODING_STANDARDS.md
mkdir -p docs/
touch docs/DOMAIN_GUIDE.md
touch docs/DEVELOPMENT_GUIDE.md
```

### Step 4: Extract & Reference (30 minutes)
For each violation:
1. Copy full content to appropriate separate doc
2. Replace in CLAUDE.md with 3-line summary + reference link
3. Verify link works

**Example**:
```markdown
<!-- Embedded: 89 lines in CLAUDE.md -->
## Code Quality Standards
[... 89 lines of standards ...]

<!-- After extraction: 3 lines in CLAUDE.md -->
## Code Quality Standards
Anti-slop principles: functions <50 lines, nesting <3, no premature optimization.
**Reference**: See [CODING_STANDARDS.md](./CODING_STANDARDS.md)
```

### Step 5: Verify (10 minutes)
```bash
# Run audit again
/audit-claude-md

# Expected output:
✅ Length OK: 178 lines
✅ Good modular strategy: 5 references
✅ No embedded standards
```

**Total time**: ~60 minutes to refactor even severely bloated CLAUDE.md

---

## Enforcement & Maintenance

### Quarterly Audit Schedule
**Set calendar reminder**: "Audit CLAUDE.md" every 3 months

**When to audit**:
- Every quarter (scheduled)
- After major feature additions
- When CLAUDE.md exceeds 200 lines
- When team reports confusion

### Pre-Commit Hook (Optional)
```bash
# .git/hooks/pre-commit
if [ -f "CLAUDE.md" ]; then
  LINES=$(wc -l < CLAUDE.md)
  if [ $LINES -gt 250 ]; then
    echo "❌ CLAUDE.md is $LINES lines (max 250)"
    echo "Run: /audit-claude-md"
    exit 1
  fi
fi
```

### Team Agreement
Add to project README.md:
```markdown
## CLAUDE.md Maintenance

**Target**: 150-200 lines (enforced)
**Audit**: Run `/audit-claude-md` quarterly
**Guidelines**: [templates/claude-md/CLAUDE-MD-GUIDELINES.md]
```

---

## Common Questions

### Q: Why 100-200 lines? Seems arbitrary.

**A**: Official Claude Code guidance from Anthropic and community best practices. CLAUDE.md is prepended to every prompt - longer files:
- Consume context window unnecessarily
- Introduce noise that reduces effectiveness
- Are considered a "code smell" (industry consensus)

---

### Q: My project is complex. Can't I have 300 lines?

**A**: Complexity doesn't require longer CLAUDE.md - it requires better modular docs. Our dois repo went from 512 → 178 lines without losing ANY information. The secret: reference separate docs instead of embedding detail.

**Example**: Complex statistical project needs formulas → Create STATISTICAL_REFERENCE.md (67 lines), add 3-line reference in CLAUDE.md.

---

### Q: What if I need to explain a critical pattern?

**A**: Ask 3 questions:
1. Used in 80%+ of sessions? (If no → separate doc)
2. Claude gets it wrong without guidance? (If no → separate doc)
3. Can explain in <10 lines? (If no → summarize in 3 lines + link)

**Only if all 3 are YES**: Include full explanation in CLAUDE.md.

---

### Q: Won't separate docs make it harder for Claude to find information?

**A**: No. Claude can easily read referenced docs when needed. The advantage of keeping CLAUDE.md lean:
- Every session starts with clear context (not buried in 500 lines)
- Reduces noise in every prompt
- Claude can still access detailed docs via references

**Mental model**: CLAUDE.md = things Claude needs ALWAYS. Separate docs = things Claude needs SOMETIMES.

---

### Q: How often should I audit?

**A**: Quarterly (every 3 months) minimum. Also:
- After major features
- When exceeding 200 lines
- When noticing Claude confusion

**Takes ~5 minutes** to run `/audit-claude-md`. **Takes ~60 minutes** to refactor if bloated.

---

### Q: Can I use this for non-Claude Code projects?

**A**: These principles apply to any AI-assisted development:
- Cursor IDE
- GitHub Copilot with chat
- Any LLM-based coding assistant

**Core principle is universal**: Keep high-frequency context lightweight, reference detailed docs.

---

## Related Templates

**Also in this library**:
- [Slash Commands](../slash-commands/) - 6 proven commands for AI workflows
- [Project Structures](../projects/) - .projects/ 3-tier organization (coming)
- [Document Templates](../documents/) - tasks.md, HANDOFF.md, plan.md (coming)
- [Anti-Slop Standards](../standards/) - With grep patterns (coming)

**Note**: Research methodology (EXTRACTION-ROADMAP.md) excluded from repository for brevity. Templates are production-validated and ready for use.

---

## Evidence & Sources

### Official Guidance Sources
- Anthropic Claude Code documentation (docs.claude.com)
- Tyler Burnam, Medium: "Long CLAUDE.md files are a code smell"
- Shipyard best practices: "Reference files using @ref syntax"
- Community consensus: 100-200 line target

### Validation from Audited Repos
- **claude-dev-template** (178 lines): Only repo meeting guidance ✅
- **ping-tree-compare** (226 lines): 13% over, modular strategy partially applied
- **fastapi-service-b** (289 lines): 45% over, embedded standards
- **dois-test-capacity** (512 lines): 156% over, severe bloat

**Conclusion**: 75% of audited repos violated guidance → Templates needed to prevent bloat.

---

## Getting Help

**Found a bloated CLAUDE.md?**
1. Read [CLAUDE-MD-GUIDELINES.md](./CLAUDE-MD-GUIDELINES.md) (decision tree)
2. See [example-refactored.md](./example-refactored.md) (step-by-step)
3. Run `/audit-claude-md` (automated detection)

**Still unsure what to extract?**
- Use decision tree in guidelines
- Apply 3 questions (frequency, impact, brevity)
- When in doubt, extract to separate doc

**Need team buy-in?**
- Share official guidance quotes
- Show good vs bad examples (178 lines vs 512 lines)
- Run `/audit-claude-md` to demonstrate bloat objectively

---

**Last Updated**: 2026-01-14
**Next Review**: 2026-04-14 (quarterly)
**Maintained By**: ai-dev-templates library
