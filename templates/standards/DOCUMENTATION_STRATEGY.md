# Documentation Strategy Guide

[← Back to Main README](../../README.md)

**Purpose**: Decision framework for when to split vs consolidate documentation to prevent "documentation mess"

**Last Updated**: 2025-11-02

---

## What This Is

A focused guide answering one core question: **"Should I split this documentation or keep it together?"**

This isn't comprehensive documentation theory. It's a practical decision tree based on real-world experience maintaining docs across multiple AI-assisted development projects.

### Why This Matters

Documentation becomes a mess without deliberate patterns:

- **The bloat problem**: Files start at 150 lines, grow to 500+, become unscannable
- **The fragmentation problem**: 20 tiny files scattered across repo, impossible to navigate
- **The inconsistency problem**: No clear rules = everyone makes different decisions

**This guide prevents all three** with measurable criteria and automated enforcement.

---

## Core Principles

### Principle 1: The 30-Line Rule

**Rule**: If a section exceeds 30 lines, consider extracting it to a separate document.

**Why 30 lines?**
- Human attention span: ~1 screen of text without scrolling
- Scan test: Can user find info in <30 seconds?
- AI context efficiency: Smaller, focused docs are easier to reference

**Example from this repo**:
```
README.md had "Commands & Shortcuts" section at 73 lines
→ Extracted to COMMAND-REFERENCE.md
→ README kept 6-line essential commands table + link
```

**When to ignore**: Tables, code blocks, structured lists (inherently scannable even if long)

---

### Principle 2: Progressive Disclosure (Max 2 Levels)

**Rule**: Information architecture should have maximum 2 levels: **Quick Start → Deep Dive**

**Why 2 levels?**
- 1 level = Mega-doc (500+ lines, unscannable)
- 2 levels = Hub-and-spoke (README → detailed guides)
- 3+ levels = Lost in navigation hell

**Example from this repo**:
```
Level 1 (Hub): README.md
  - Quick Navigation section
  - Links to 6 template categories

Level 2 (Spoke): templates/slash-commands/README.md
  - Category overview
  - Links to 13 individual commands
```

**Anti-pattern**: README → Category README → Sub-category README → Individual doc (too deep!)

---

### Principle 3: Reference vs Embed

**Rule**: Decide whether to include content inline or reference externally based on **reuse frequency** and **context switching cost**.

**Embed inline when**:
- Content is <10 lines
- User needs it immediately (no context switching)
- Content is unique to this doc

**Reference externally when**:
- Content is reused across 2+ docs
- Content is >30 lines
- Content is independently useful

**Example from this repo**:
```
✅ EMBED: Essential commands table in README (6 lines, needed immediately)
✅ REFERENCE: Full command docs in COMMAND-REFERENCE.md (reusable, >100 lines)

Anti-pattern: Copying same 50-line troubleshooting section into 3 different READMEs
→ Extract to TROUBLESHOOTING.md, reference from all 3
```

---

### Principle 4: One Job Per Document

**Rule**: Each document should have a single, clear purpose. If you can't explain its job in <10 words, it's doing too much.

**Good examples**:
- `README.md` → "Navigate to environment setup or templates" (6 words)
- `COMMAND-REFERENCE.md` → "Complete list of all CLI commands" (6 words)
- `ANTI_SLOP_STANDARDS.md` → "Prevent AI-generated code bloat" (4 words)

**Bad examples**:
- "Development guide and troubleshooting and commands and architecture" (too many jobs)
- "Miscellaneous notes" (no clear job)

**Test**: If someone asks "Where should I document X?", can you give a clear answer in <5 seconds?

---

### Principle 5: Evidence Over Opinions

**Rule**: Documentation decisions should be based on measurable criteria, not preferences.

**Measurable criteria**:
- ✅ Line count (objective)
- ✅ Scan test (<30s to find info)
- ✅ Reuse count (used in 2+ places?)
- ✅ Section count (>5 sections = consider splitting)

**Preference-based (avoid)**:
- ❌ "This feels too long"
- ❌ "I prefer separate files"
- ❌ "This looks better to me"

**Example from this repo**:
```
Decision: Should we split audit-claude-md.md (457 lines)?

✅ Measurable analysis:
- Line count: 457 (over 400-line guideline for templates)
- Section test: Has command logic + interpretation guide (2 jobs)
- Reuse test: Interpretation guide referenced by other commands

→ Decision: SPLIT (command <250 lines, reference doc separate)

❌ Preference-based:
- "It just feels too long" → Not actionable
```

---

**Summary of Core Principles**:

1. **30-line rule** - Extract sections >30 lines (unless tables/lists)
2. **Progressive disclosure** - Max 2 levels (hub → spoke)
3. **Reference vs embed** - Inline <10 lines, external >30 lines
4. **One job per doc** - Single purpose in <10 words
5. **Evidence over opinions** - Measurable criteria only

These 5 principles form the foundation for all split/consolidate decisions.

---

## When to Split vs Consolidate (Decision Tree)

This is the core value of this guide. Use these 4 pragmatic tests to decide whether to split or consolidate documentation.

---

### The 4 Pragmatic Tests

Run your documentation through these 4 tests in order:

#### Test 1: Scan Test (30-Second Rule)

**Question**: Can a user find any piece of information in this document in <30 seconds?

**How to test**:
1. Pick 3 random topics the doc covers
2. Time yourself scanning for each
3. If any take >30 seconds → **SPLIT**

**Example from this repo**:
```
Before: README.md (352 lines)
Test: "How do I check performance?" → 45 seconds (failed)
Test: "Where are command references?" → 60 seconds (failed)
→ Decision: SPLIT (extracted COMMAND-REFERENCE.md)

After: README.md (232 lines)
Test: "How do I check performance?" → 8 seconds (passed)
→ Decision: KEEP CONSOLIDATED
```

**When scan test fails**: Extract the hardest-to-find sections to separate docs.

---

#### Test 2: Purpose Test (One Job Rule)

**Question**: Can you describe this document's purpose in <10 words?

**How to test**:
1. Write a one-sentence purpose statement
2. Count words (exclude articles like "a", "the")
3. If >10 words OR you need "and" → **SPLIT**

**Example from this repo**:
```
Before split:
"Commands reference and troubleshooting and performance monitoring and architecture"
→ 8 words, but has 3 "and"s (multiple jobs) → SPLIT

After split:
- COMMAND-REFERENCE.md: "Complete list of all CLI commands" (6 words) ✅
- README.md: "Navigate to environment setup or templates" (6 words) ✅
```

**When purpose test fails**: Each "and" becomes a separate document.

---

#### Test 3: Section Test (30-Line Section Rule)

**Question**: Does any single section exceed 30 lines?

**How to test**:
1. Count lines in each H2/H3 section
2. Ignore tables, code blocks, lists (inherently scannable)
3. If any section >30 lines → **EXTRACT THAT SECTION**

**Example from this repo**:
```
README.md "Commands & Shortcuts" section:
- Tmux commands: 28 lines
- Claude Code commands: 12 lines
- Codex commands: 14 lines
- Performance monitoring: 8 lines
→ Total: 62 lines (way over 30) → EXTRACT to COMMAND-REFERENCE.md
```

**When section test fails**: Extract the long section, leave a 3-5 line summary + link in original doc.

---

#### Test 4: Audience Test (Multiple Audiences)

**Question**: Does this document serve multiple distinct audiences with different needs?

**How to test**:
1. List the audiences (new users, experts, contributors, etc.)
2. If >2 distinct audiences → **SPLIT BY AUDIENCE**

**Example from this repo**:
```
Original README served 4 audiences:
1. Environment setup users (need setup steps)
2. Template browsers (need to find templates)
3. Researchers (need evidence/methodology)
4. Contributors (need architecture details)

→ Decision: Keep audiences 1-3 in README (related), extract detailed architecture to DEVELOPMENT-ENVIRONMENT.md
```

**When audience test fails**: Create audience-specific documents (GETTING-STARTED.md, CONTRIBUTING.md, ARCHITECTURE.md).

---

### Decision Tree Flowchart

```
Start: "Should I split this document?"
│
├─→ Run Test 1 (Scan Test)
│   ├─ Can find info in <30s? → Continue to Test 2
│   └─ Takes >30s? → SPLIT (extract hard-to-find sections)
│
├─→ Run Test 2 (Purpose Test)
│   ├─ Purpose in <10 words, no "and"s? → Continue to Test 3
│   └─ >10 words OR multiple "and"s? → SPLIT (each job = separate doc)
│
├─→ Run Test 3 (Section Test)
│   ├─ All sections <30 lines? → Continue to Test 4
│   └─ Any section >30 lines? → EXTRACT SECTION (keep summary + link)
│
├─→ Run Test 4 (Audience Test)
│   ├─ Serves ≤2 audiences? → KEEP CONSOLIDATED
│   └─ Serves 3+ audiences? → SPLIT BY AUDIENCE
│
└─→ All tests passed? → KEEP CONSOLIDATED (document is well-structured)
```

---

### Common Scenarios & Decisions

| Scenario | Tests That Fail | Decision | Action |
|----------|----------------|----------|--------|
| **README is 600 lines** | Scan test (can't find info quickly) | SPLIT | Extract detailed sections to separate docs |
| **Section is 50 lines** | Section test (>30 lines) | EXTRACT | Move section to own doc, leave summary + link |
| **Doc covers 5 topics** | Purpose test (too many jobs) | SPLIT | Create 5 focused docs |
| **Doc has 3 audiences** | Audience test (>2 audiences) | SPLIT | Create audience-specific docs |
| **README is 200 lines, scannable** | All tests pass | KEEP | Document is well-structured |

---

### When NOT to Split (Anti-Patterns)

**Don't split prematurely**. Splitting has costs:
- More files to maintain
- Navigation overhead (users click multiple links)
- Risk of fragmentation (can't find anything)

**Red flags for premature splitting**:

❌ **"This file is getting long"** (opinion, not measurable)
- Run the 4 tests first. If all pass, keep consolidated.

❌ **"I want to organize by topic"** (arbitrary categorization)
- Only split if scan test or purpose test fails.

❌ **"Each function should have its own doc"** (over-fragmentation)
- Documentation isn't code. Keep related info together.

❌ **"Let's split into 10 files just in case"** (premature optimization)
- Start with 1-2 docs, split only when tests fail.

**Good reasons to split**:
- ✅ Scan test fails (can't find info in <30s)
- ✅ Purpose test fails (multiple jobs, uses "and")
- ✅ Section test fails (sections >30 lines)
- ✅ Audience test fails (serves 3+ distinct groups)

---

### Real Examples from This Repo

**Example 1: README.md Split**
```
Original: 352 lines
Tests:
- Scan test: FAIL (60s to find command references)
- Purpose test: FAIL ("Environment AND templates AND commands AND troubleshooting")
- Section test: FAIL ("Commands & Shortcuts" section = 73 lines)
- Audience test: PASS (2 audiences: setup users, template browsers)

Decision: SPLIT
Actions:
1. Extracted COMMAND-REFERENCE.md (detailed commands)
2. Condensed README to 232 lines
3. Kept essential commands table (6 lines) in README
4. Added link to full reference

Result: All tests now pass ✅
```

**Example 2: audit-claude-md.md Split (Planned)**
```
Original: 457 lines
Tests:
- Scan test: BORDERLINE (command logic mixed with reference material)
- Purpose test: FAIL ("Audit command AND interpretation guide")
- Section test: FAIL (interpretation section = 120 lines)
- Audience test: PASS (1 audience: developers)

Decision: SPLIT
Actions:
1. Keep command logic in audit-claude-md.md (<250 lines)
2. Extract AUDIT_REFERENCE.md (interpretation guide, examples)
3. Add link from command to reference

Rationale: Follows "reference vs embed" anti-slop principle
```

**Example 3: ANTI_SLOP_STANDARDS.md (Keep Consolidated)**
```
Current: 789 lines
Tests:
- Scan test: PASS (table of contents, clear sections, <30s to find any standard)
- Purpose test: PASS ("Prevent AI-generated code bloat" = 4 words)
- Section test: PASS (longest section = 28 lines, mostly tables/lists)
- Audience test: PASS (1 audience: developers)

Decision: KEEP CONSOLIDATED
Rationale: Reference doc (no hard limit), all tests pass, tables are scannable
```

---

### Quick Decision Prompts

Ask yourself these 5 questions:

1. **Can I find any info in this doc in <30 seconds?** (Scan test)
   - No → Split

2. **Can I describe this doc's purpose in <10 words without "and"?** (Purpose test)
   - No → Split

3. **Are all sections <30 lines (excluding tables/lists)?** (Section test)
   - No → Extract long sections

4. **Does this serve ≤2 audiences?** (Audience test)
   - No → Split by audience

5. **Am I splitting because tests failed, not because "it feels long"?** (Evidence test)
   - Feelings → Don't split
   - Failed tests → Split

**If all 5 answers are "yes" → Keep consolidated**

---

## Length Guidelines by Document Type

These limits are based on empirical analysis of 4 repos (239+ commits) and specifically prevent AI-generated documentation bloat.

### File Size Limits

| Document Type | Recommended Limit | Why This Limit? |
|---------------|-------------------|-----------------|
| **CLAUDE.md** | 150-200 lines | AI context efficiency - smaller files load faster, easier to reference |
| **README.md** | 200-400 lines | Scan test - users find info in <30s, prevents mega-doc syndrome |
| **Slash commands** | <250 lines | Single responsibility - command logic only, extract reference material |
| **Category READMEs** | 200-400 lines | Hub function - overview + navigation, not comprehensive guide |
| **Standards/Reference** | <600 lines | No hard limit if scannable (tables, clear sections, TOC) |
| **Project specs** | 300-500 lines | AI resume efficiency - Claude can load entire context in one read |

**Key insight**: These limits aren't arbitrary. They're based on:
1. **AI context windows** - Smaller docs = faster loading, better referencing
2. **Scan test** - All limits correlate with <30s information retrieval
3. **AI over-generation patterns** - AI assistants tend to add without removing, limits force discipline

---

### Why AI Generates Bloat (And How Limits Help)

**AI bloat pattern observed**:
```
Session 1: Claude generates 150-line CLAUDE.md ✅
Session 2: Adds 50 lines (new features) → 200 lines ⚠️
Session 3: Adds 80 lines (edge cases) → 280 lines ❌
Session 4: Adds 120 lines ("just in case" docs) → 400 lines ❌❌
```

**Without limits**: Files grow indefinitely (AI never removes, only adds)

**With limits**: Forces extraction decisions
```
Session 2: Hits 200-line limit
→ Run 4 tests
→ Extract detailed examples to separate doc
→ CLAUDE.md stays at 180 lines ✅
```

**AI-specific bloat triggers**:
- "Add comprehensive documentation" → AI generates 200 lines when 30 would suffice
- "Document edge cases" → AI lists every possible scenario
- "Improve clarity" → AI adds examples without removing redundant text

**Limits prevent this** by forcing split decisions when files grow.

---

### Automated Detection (Grep Patterns)

Use these patterns to detect documentation bloat automatically:

**Check file sizes**:
```bash
# Find docs over recommended limits
find . -name "CLAUDE.md" -exec wc -l {} \; | awk '$1 > 200 {print "⚠️  CLAUDE.md too long:", $1, "lines"}'
find . -name "README.md" -exec wc -l {} \; | awk '$1 > 400 {print "⚠️  README.md too long:", $1, "lines"}'
find . -path "*/slash-commands/*.md" -exec wc -l {} \; | awk '$1 > 250 {print "⚠️  Slash command too long:", $1, "lines -", $2}'
```

**Check for AI bloat indicators**:
```bash
# Find docs with excessive examples (AI over-generation)
grep -r "Example [4-9]:" . --include="*.md"  # More than 3 examples = bloat
grep -r "Note:" . --include="*.md" | wc -l   # Excessive notes = AI hedging

# Find docs with multiple audiences (needs splitting)
grep -r "For beginners\|For advanced\|For contributors" . --include="*.md"
```

**AI-generated fluff patterns**:
```bash
# Detect verbose AI writing
grep -r "It is important to note that\|It should be noted that\|Please be aware" . --include="*.md"
grep -r "In order to\|For the purpose of\|With regards to" . --include="*.md"
```

**Run these checks periodically** (monthly) to catch bloat before it becomes unmanageable.

---

## Quick Reference

### Common Scenarios Cheat Sheet

| Your Situation | What to Do | Link to Details |
|----------------|-----------|-----------------|
| **"My README is 450 lines"** | Run 4 tests. Likely needs split (scan test will fail) | [Decision Tree](#when-to-split-vs-consolidate-decision-tree) |
| **"Section is 60 lines"** | Extract to separate doc, leave summary + link | [Section Test](#test-3-section-test-30-line-section-rule) |
| **"AI added 150 lines of docs"** | Check for fluff patterns, remove verbose phrases | [AI Bloat Detection](#automated-detection-grep-patterns) |
| **"CLAUDE.md is 350 lines"** | Over 200-line limit. Extract details to category docs | [Length Guidelines](#file-size-limits) |
| **"Should I split by topic?"** | Only if tests fail. Don't split on opinion | [When NOT to Split](#when-not-to-split-anti-patterns) |
| **"Doc serves 4 audiences"** | Split by audience (GETTING-STARTED, CONTRIBUTING, etc.) | [Audience Test](#test-4-audience-test-multiple-audiences) |

---

### Quick Decision Framework

When in doubt, ask these 5 questions in order:

1. **Line count >400?** → Run all 4 tests
2. **Any section >30 lines?** → Extract section
3. **Can't find info in <30s?** → Split
4. **Purpose has "and"?** → Split
5. **Serves 3+ audiences?** → Split by audience

If none apply → **Keep consolidated**

---

### Real Files from This Repo (Examples)

Use these as reference points:

**Well-structured (keep consolidated)**:
- [README.md](../../README.md) - 232 lines, all tests pass
- [ANTI_SLOP_STANDARDS.md](./ANTI_SLOP_STANDARDS.md) - 789 lines, scannable (tables/TOC)
- [COMMAND-REFERENCE.md](../../COMMAND-REFERENCE.md) - Focused purpose, extracted from README

**Needs splitting (planned)**:
- `templates/slash-commands/audit-claude-md.md` - 457 lines, multiple jobs (command + guide)

**Good split examples**:
- README.md → COMMAND-REFERENCE.md (extracted detailed commands)
- Category READMEs → Individual templates (2-level hub-and-spoke)

---

### When to Use This Guide

**Use when**:
- ✅ Deciding whether to split documentation
- ✅ AI session added significant content (>50 lines)
- ✅ Monthly doc maintenance/cleanup
- ✅ Onboarding new team member (share standards)

**Don't use for**:
- ❌ Code organization (this is docs-specific)
- ❌ One-time notes/scratch files
- ❌ External docs you don't control

---

**That's it.** The guide is intentionally focused on the core question: **"Split or consolidate?"**

For comprehensive documentation theory, see established resources (Google Style Guide, Plain Language Act). This guide is specifically for preventing AI-generated documentation bloat in AI-assisted development.

---

**Created**: 2025-11-02
**Based on**: 4 repo audits, 239+ commits analyzed, 6+ months AI-assisted development

