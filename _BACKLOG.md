# ai-dev-templates Backlog

**Last Updated:** 2026-01-15
**Purpose**: Track improvements to the template library itself

---

## In Progress

### Enhanced Security Hooks
**Status:** Completed
**Added:** 2026-01-15

Added from TheDecipherist/claude-code-mastery:
- `sensitive-file-blocker-enhanced.py` - Multi-strategy secrets detection
- `dangerous-commands-blocker.py` - Destructive command prevention

---

## P1 - High Priority

*(None currently)*

---

## P2 - Medium Priority

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

### 2026-01-15: Security Hooks from TheDecipherist
- Added `sensitive-file-blocker-enhanced.py`
- Added `dangerous-commands-blocker.py`
- Updated hooks README with new examples

---

## Sources & References

External guides evaluated:
- [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery) - Security hooks, MCP decision trees, research citations

Comparative analysis: See `_private/research/` for methodology and findings
