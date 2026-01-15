# Testing Templates - Verification Status

**Last Updated:** 2026-01-07 11:35 PST
**Author:** Claude Code + Human

This document tracks what has been TESTED vs. UNTESTED in these templates.

> **Note:** "Deployed to" references are example deployments from the author's projects used to verify these templates work in production. Your deployments will use your own repository paths.

## Legend

| Status | Meaning |
|--------|---------|
| VERIFIED | Template used in real project, confirmed working |
| RESEARCH-BASED | Based on verified sources, template untested |
| SPECULATIVE | Theoretical, needs validation |

---

## CI Templates (`../ci/`)

### `claude-qa-workflow.yml.template`
**Status:** VERIFIED
**Created:** 2026-01-07
**Verified:** 2026-01-08
**Source:** [Alex Op article](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/), [Official docs](https://github.com/anthropics/claude-code-action)
**Deployed to:** `epcvip-tools-hub/.github/workflows/wordle-qa.yml`
**Tested:** YES - Run #20800668844
**Results:**
- Duration: 4m 36s (219s Claude processing)
- Turns: 39 browser interactions
- Cost: $0.62 (Sonnet 4.5)
- Status: SUCCESS
**Notes:**
- Uses official `anthropics/claude-code-action@v1`
- MCP config with `--headless` flag for CI
- `--allowedTools` for black-box testing
- **Required fix:** `id-token: write` permission for OIDC auth

### `security-review.yml.template`
**Status:** VERIFIED
**Created:** 2026-01-07
**Verified:** 2026-01-08
**Source:** [Official repo](https://github.com/anthropics/claude-code-security-review)
**Deployed to:** `epcvip-tools-hub/.github/workflows/security.yml`
**Tested:** YES - Run #20800666122
**Results:**
- Duration: 36s
- Findings: 0 vulnerabilities
- Status: SUCCESS
**Notes:**
- Uses official `anthropics/claude-code-security-review@main`
- Zero config setup, works out of the box

### `qa-persona.md.template`
**Status:** SPECULATIVE
**Notes:** Generic persona, not yet used in real QA run

---

## Testing Guides

### `PLAYWRIGHT_CLAUDE_GUIDE.md`
**Status:** PARTIALLY VERIFIED
**Verified sections:**
- Local MCP setup and usage
- Scripted test commands
- UI mode debugging
**Unverified sections:**
- CI integration patterns
- Visual regression CI setup

### `MCP_WORKFLOW_GUIDE.md`
**Status:** VERIFIED (local use)
**Notes:** Used extensively for local browser exploration

### `RESEARCH_ARCHIVE.md`
**Status:** SOURCES VERIFIED
**Last verified:** 2026-01-07
**All URLs checked:** Yes
**Notes:** Sources confirmed to exist. Implementation patterns from sources not all tested.

### `COMPETITOR_ANALYSIS.md`
**Status:** SPECULATIVE
**Notes:** Pattern documented but not used in real analysis

---

## Example Files (`examples/`)

### `playwright.config.ts.template`
**Status:** VERIFIED
**Used in:** `epcvip-tools-hub/playwright.config.ts`
**Notes:** Working, minor customizations made

### `fixtures.ts.template`
**Status:** VERIFIED
**Used in:** `epcvip-tools-hub/test/e2e/fixtures.ts`
**Notes:** Two-player fixture working

### `PageObject.ts.template`
**Status:** VERIFIED
**Used in:** `epcvip-tools-hub/test/e2e/pages/`
**Notes:** Pattern working, adapted for Wordle

### `visual.spec.ts.template`
**Status:** VERIFIED (local)
**Used in:** `epcvip-tools-hub/test/e2e/visual.spec.ts`
**Notes:** Screenshot comparison working locally

---

## What Needs Verification

| Template | How to Verify | Priority |
|----------|---------------|----------|
| `claude-qa-workflow.yml.template` | Deploy to repo, run on PR | High |
| `security-review.yml.template` | Deploy to repo, run on PR | High |
| `COMPETITOR_ANALYSIS.md` | Use for real competitor research | Low |
| `qa-persona.md.template` | Use in actual QA run | Medium |

---

## Sources Verification Log

| Source | URL | Status | Verified |
|--------|-----|--------|----------|
| claude-code-action | github.com/anthropics/claude-code-action | EXISTS | 2026-01-07 |
| claude-code-security-review | github.com/anthropics/claude-code-security-review | EXISTS | 2026-01-07 |
| Alex Op AI QA | alexop.dev/posts/... | EXISTS | 2026-01-07 |
| Simon Willison MCP | til.simonwillison.net/... | EXISTS | 2026-01-07 |
| TestLeaf 2026 | testleaf.com/blog/... | EXISTS | 2026-01-07 |
| Playwright MCP (MS) | github.com/microsoft/playwright-mcp | EXISTS | 2026-01-07 |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-08 | **VERIFIED** claude-qa-workflow.yml.template (Run #20800668844, $0.62, 39 turns) |
| 2026-01-08 | **VERIFIED** security-review.yml.template (Run #20800666122, 36s) |
| 2026-01-08 | Added `id-token: write` permission (required for OIDC) |
| 2026-01-08 | Added `workflow_dispatch` triggers for manual testing |
| 2026-01-07 | Created this STATUS.md |
| 2026-01-07 | Fixed CI templates to use official actions |
| 2026-01-07 | Updated RESEARCH_ARCHIVE with official sources |
| 2026-01-06 | Initial templates created |
