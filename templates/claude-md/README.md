# CLAUDE.md Templates & Guidelines

[← Back to Main README](../../README.md)

**Purpose**: Keep CLAUDE.md lightweight (150-200 lines) as project complexity grows

**The Problem**: CLAUDE.md files bloat over time — what starts as 150 lines grows to 500+ as developers add information without removing anything.

**The Solution**: Clear criteria for what belongs, automated bloat detection, modular documentation strategy. See [CLAUDE-MD-GUIDELINES.md](./CLAUDE-MD-GUIDELINES.md) for the complete reference.

---

## Quick Start

### For New Projects

1. **Copy template**: `cp CLAUDE.md.template your-project/CLAUDE.md`
2. **Fill in placeholders**: Replace bracketed sections with your project details
3. **Follow guidance comments**: Each section has inline notes on what belongs
4. **Stay under 200 lines**: If you need more, create separate docs + references

### For Existing Projects (Bloated CLAUDE.md)

1. **Run audit**: Copy `../slash-commands/ai-dev-workflow/commands/audit-claude-md.md` to `.claude/commands/`, run `/audit-claude-md`
2. **Review violations**: Check length, embedded standards, missing references
3. **Follow refactoring guide**: See [example-refactored.md](./example-refactored.md) for step-by-step
4. **Verify**: Run `/audit-claude-md` again (should show 0-2 warnings)

---

## Files in This Template Library

| File | Purpose | Lines |
|------|---------|------:|
| [CLAUDE.md.template](./CLAUDE.md.template) | Lightweight template with placeholders and inline guidance | ~180 |
| [CLAUDE-MD-GUIDELINES.md](./CLAUDE-MD-GUIDELINES.md) | Complete reference: decision tree, inclusion criteria, bloat warning signs | ~410 |
| [example-refactored.md](./example-refactored.md) | Case study: 512 → 178 lines (65% reduction) with step-by-step | ~150 |
| [audit-claude-md](../slash-commands/ai-dev-workflow/commands/audit-claude-md.md) | Skill for automated bloat detection | ~50 |

---

## The Bloat Problem

CLAUDE.md files grow from 150 → 500+ lines through "just add it here" accumulation. Only 1 of 4 audited repos met the 100-200 line guidance — the rest had 45-156% bloat.

**See**: [CLAUDE-MD-GUIDELINES.md](./CLAUDE-MD-GUIDELINES.md) for the decision tree, inclusion criteria, and seven bloat warning signs.

---

## Official Guidance (Updated Jan 2026)

**From Claude Code best practices (v2.1.x)**:
- Target: **100-200 lines maximum**
- Philosophy: **"Always lightweight"** — files prepended to every prompt
- Warning: **"Long CLAUDE.md files are a code smell"**
- Strategy: **"Reference separate docs instead of embedding detail"**

**New in 2026:**
- Use `#` key during sessions to have Claude auto-update CLAUDE.md
- Use "think", "think hard", or "ultrathink" for extended reasoning
- Hub-and-spoke pattern is now industry standard

**Sources**: [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices), community patterns, industry guidance

---

## The Lightweight Philosophy

CLAUDE.md is a quick-reference card, not a user manual. Before adding content, ask: (1) used in 80%+ of sessions? (2) Claude gets it wrong without it? (3) fits in <10 lines? If any answer is "no", create a separate doc.

**See**: [CLAUDE-MD-GUIDELINES.md](./CLAUDE-MD-GUIDELINES.md) for the full decision tree and inclusion criteria.

---

## Modular Documentation Strategy

### The Core Pattern: Reference, Don't Embed

**Bad**: 89 lines of coding standards embedded in CLAUDE.md.
**Good**: 3-line summary + link to CODING_STANDARDS.md — 100% information preserved.

### Hub-and-Spoke Pattern

```
CLAUDE.md (hub — 150-200 lines, always loaded)
├── CODING_STANDARDS.md (spoke — loaded when needed)
├── docs/ARCHITECTURE.md (spoke)
├── .claude/review-context.md (spoke)
└── backlog/_INDEX.md (spoke)
```

Hub = things Claude needs ALWAYS. Spokes = things Claude needs SOMETIMES.

---

## Refactoring Workflow

1. **Audit** (5 min): Run `/audit-claude-md` to get violations report
2. **Plan** (10 min): Decide which separate docs to create based on violations
3. **Extract** (30 min): Move content to separate docs, replace with 3-line summary + link
4. **Verify** (10 min): Run `/audit-claude-md` again — should show 0-2 warnings, 150-220 lines

**See**: [example-refactored.md](./example-refactored.md) for a full walkthrough (512 → 178 lines).

---

## Enforcement & Maintenance

**Quarterly audits**: Run `/audit-claude-md` every 3 months, after major features, or when exceeding 200 lines.

**Pre-commit hook** (optional): Block commits when CLAUDE.md exceeds 250 lines. See [CLAUDE-MD-GUIDELINES.md § Maintenance](./CLAUDE-MD-GUIDELINES.md#maintenance) for the hook snippet and team agreement template.

**Common questions**: See [CLAUDE-MD-GUIDELINES.md § FAQ](./CLAUDE-MD-GUIDELINES.md#faq) for answers on line limits, complex projects, separate doc discovery, and cross-tool applicability.

---

## See Also

- [Skill Templates](../slash-commands/README.md) — 21 flat-file skill templates including `/audit-claude-md`
- [Anti-Slop Standards](../standards/ANTI_SLOP_STANDARDS.md) — Code quality with grep patterns
- [Project Management](../project-management/README.md) — Task tracking and backlogs

---

## Evidence & Sources

- **Official**: Anthropic Claude Code docs, community best practices
- **Validation**: 4 repos audited — 75% violated guidance, proving templates needed
- **Case study**: [example-refactored.md](./example-refactored.md) — 512 → 178 lines without information loss

---

## Getting Help

1. Read [CLAUDE-MD-GUIDELINES.md](./CLAUDE-MD-GUIDELINES.md) (decision tree + inclusion criteria)
2. See [example-refactored.md](./example-refactored.md) (step-by-step case study)
3. Run `/audit-claude-md` (automated detection)

When in doubt, extract to a separate doc — it's always safer than leaving content in CLAUDE.md.

---

**Last Updated**: 2026-02-16
**Next Review**: 2026-05-16 (quarterly)
**Maintained By**: ai-dev-templates library
