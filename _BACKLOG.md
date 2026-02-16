# ai-dev-templates Backlog

**Last Updated:** 2026-02-16
**Purpose**: Track improvements to the template library itself

---

## In Progress

*(None currently)*

---

## P1 - High Priority

### Pass 15: Dev Server Skill Genericization
**Priority:** P1
**Added:** 2026-02-15
**Source:** Pass 11 skills audit — flagship skill #3

**Problem:** The dev-server skill currently has hardcoded repo-specific startup sequences (epcvip repos). Needs genericization to work as a template pattern.

**Action:** Extract the pattern (auto-detect framework, apply correct startup) from the org-specific implementation. Create a template version in `templates/plugins/`.

---

## P2 - Medium Priority

### MCP Consolidation Guide
**Priority:** P2
**Added:** 2026-02-15
**Source:** Gap analysis during content audit

**Problem:** MCP guidance is scattered across CLAUDE-CODE-CONFIG, PLAYWRIGHT-MCP, RAILWAY_MCP_GUIDE, and MCP-DECISION-TREES (draft). No single reference explains MCP types, cost implications, and when to use which server.

**Blocked by:** MCP-DECISION-TREES.md still has unvalidated TODOs. Needs real usage data before consolidation.

**Action:** Create a single "MCP Patterns" reference in `docs/reference/` that consolidates the scattered content.

---

### Codex Comparison Depth
**Priority:** P2
**Added:** 2026-02-15
**Source:** Gap analysis during content audit
**Partially addressed:** Pass 14 added strategic comparison to ADVANCED-WORKFLOWS.md Section 6

**Problem:** CODEX-SETUP.md covers installation but lacks detailed capability comparison and integration patterns beyond what's in ADVANCED-WORKFLOWS.

**Blocked by:** Needs more real dual-tool usage data to be evidence-based (not speculative).

**Action:** After accumulating more dual-tool workflow experience, add detailed capability comparison and quality benchmarks to CODEX-SETUP.md.

---

### Research Citations for Context Management
**Priority:** P2
**Added:** 2026-01-15
**Source:** TheDecipherist/claude-code-mastery comparative analysis

**Problem:** Internal templates rely on evidence from production commits but lack external research citations that could strengthen rationale.

**Research to explore:**
- "39% performance drop when mixing topics in multi-turn conversations" - Find original source
- "Lost-in-the-middle effect" - LLMs recall beginning/end better than middle
- "Context drift" studies - Gradual degradation of conversational state
- "2% early misalignment → 40% failure rates" - Cascading error research

**Action:** Research these claims, validate sources, and if credible, add citations to:
- `templates/slash-commands/session-handoff/` (context management rationale)
- `templates/claude-md/CLAUDE-MD-GUIDELINES.md` (size limit rationale)

**Acceptance criteria:**
- Each citation has verifiable source (arXiv, blog with methodology, official docs)
- Citations add value (not just "studies show")
- Integrated naturally, not bolted-on

---

### MCP Server Decision Trees
**Priority:** P2
**Added:** 2026-01-15
**Source:** TheDecipherist/claude-code-mastery

**Status:** Draft in progress at `docs/drafts/MCP-DECISION-TREES.md`

**Problem:** Current testing guide covers Playwright but lacks broader MCP guidance.

**Scope:**
- Browser automation decision tree (Playwright vs Browser MCP vs Browser Use)
- Database access patterns
- Documentation/context servers

**Next steps:**
1. Validate draft against real usage
2. Test recommended MCP servers
3. When validated, promote to `docs/reference/`

---

## P3 - Low Priority

### Context Management Research Citations
**Priority:** P3 (promoted from P2 research item)
**Added:** 2026-02-15
**Source:** ADVANCED-WORKFLOWS.md creation

**Action:** Validate and add citations to ADVANCED-WORKFLOWS.md Section 1:
- "39% performance drop" when mixing topics — find original source
- "Lost-in-the-middle" effect — LLMs recall beginning/end better than middle
- Attention diffusion past ~120k tokens — quantify with research

**Blocked by:** Citations need verified sources (arXiv, official docs, blog with methodology)

---

### Agent Orchestration Patterns
**Priority:** P3
**Added:** 2026-02-15
**Source:** ADVANCED-WORKFLOWS.md creation

**Problem:** ADVANCED-WORKFLOWS.md covers basic agent patterns but doesn't document failure modes, context sharing workarounds, or cost projections for multi-agent workflows.

**Blocked by:** Needs more production usage data to be evidence-based.

**Action:** Document failure modes, cost projections, and context sharing patterns after accumulating real multi-agent usage.

---

### Global CLAUDE.md Pattern
**Priority:** P3
**Added:** 2026-01-15
**Source:** TheDecipherist/claude-code-mastery

**Idea:** Document three-tier CLAUDE.md inheritance (enterprise → user global → project)

**Current state:** Each project has its own CLAUDE.md, no global pattern documented

**Consideration:** If implemented, enforce STRICT 100-line limit for global (vs 150-200 for project)

**Blocked by:** Need to validate if global CLAUDE.md is actually useful or just adds complexity

---

### New Project Scaffolding Script
**Priority:** P3
**Added:** 2026-01-15
**Source:** TheDecipherist/claude-code-mastery comparison

**Idea:** Single command/script to bootstrap new projects with:
- Standard directory structure
- Pre-configured CLAUDE.md
- .gitignore with common patterns
- Optional hooks installation

**Current state:** Manual setup or copy from claude-dev-template

---

## P4 - On Hold / Blocked

*(None currently)*

---

## Completed

### 2026-02-16: Pass 14 — Expand ADVANCED-WORKFLOWS to 7-Section Power-User Guide
- Expanded from 4 sections (272 lines) to 7 sections (386 lines)
- Section 1 (Context): Added MCP context costs, skill description budget, avoid list, compact-by-work-type, official 95% compaction trigger
- Section 2 (Planning): NEW — temporary vs durable plans, good plan elements, mandatory cleanup phases. Links to PLAN_QUALITY_RUBRIC
- Section 3 (Agents): Added sub-agent nesting limitation, cost awareness subsection with model selection guidance
- Section 4 (Extension Points): NEW — conceptual overview of skills, hooks, MCP (hidden context costs), plugins. Links to implementation READMEs
- Section 5 (Predictability): Added scoped diffs, structured output expectations to reproducibility techniques
- Section 6 (Claude Code vs Codex): Expanded from 3 bullets to proper strategic comparison with current data
- Section 7 (Meta-Level Principles): NEW — 5 crystallized takeaways distilled from the guide
- Updated cross-references in CLAUDE.md, README.md

### 2026-02-16: Pass 13 — Backlog Management Consolidation
- Consolidated 3 overlapping categories (features-backlog, projects, plugins/backlog-management) into `templates/project-management/`
- Created unified README with decision table and honest comparison to native Tasks
- Updated 3 backlog skills: rich descriptions, troubleshooting sections, native Tasks notes
- Overhauled BUILTIN_VS_CUSTOM.md (TodoWrite → native Tasks, Session Memory added)
- Updated 10 files with cross-reference fixes, removed 423 lines of overlap
- See AUDIT_LOG.md Pass 13 for full details

### Enhanced Security Hooks
**Completed:** 2026-01-15

Added from TheDecipherist/claude-code-mastery:
- `sensitive-file-blocker-enhanced.py` - Multi-strategy secrets detection
- `dangerous-commands-blocker.py` - Destructive command prevention

### 2026-02-15: Content Audit & Conceptual Guide
- Created `docs/reference/ADVANCED-WORKFLOWS.md` (context management, agents, predictability, model strategy)
- Rewrote `templates/plugins/README.md` with proper taxonomy (skills vs commands vs hooks vs plugins)
- Trimmed redundancy in CLAUDE-MD-GUIDELINES, hooks/README, PLAYWRIGHT_CLAUDE_GUIDE, NEW-PROJECT-SETUP
- Added cross-links between related docs

### 2026-02-15: Pass 12 — Unified Code Review Skill
- Merged 3 sequential skills (local-code-review + evaluate-code-review + root-cause-analysis) into unified `code-review` skill
- 5-phase pipeline: gather → agents → evaluate → root-cause → output
- Added guardrails (NEVER/ALWAYS), agent self-evaluation (confidence >= 70), false-positive filtering
- Created `references/false-positive-patterns.md` and `references/bug-categories.md`
- Installed to `~/.claude/skills/code-review/`, deprecated 4 old skills
- See AUDIT_LOG.md Pass 12 for full details

### 2026-01-15: Security Hooks from TheDecipherist
- Added `sensitive-file-blocker-enhanced.py`
- Added `dangerous-commands-blocker.py`
- Updated hooks README with new examples

---

## Sources & References

External guides evaluated:
- [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery) - Security hooks, MCP decision trees, research citations

Comparative analysis: See `_private/research/` for methodology and findings
