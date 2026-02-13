# Testing Templates - Verification Status

**Last Updated:** 2026-02-13
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
**Last Updated:** 2026-02-13
**Verified sections:**
- Local MCP setup and usage
- Scripted test commands
- UI mode debugging
- 5 approaches table (updated from 4 modes)
**Unverified sections:**
- CI integration patterns
- Visual regression CI setup
- Playwright CLI approach (verified — see PLAYWRIGHT_CLI_EVALUATION.md)
- Claude Code Chrome (documented, not available on WSL2)

### `MCP_WORKFLOW_GUIDE.md`
**Status:** VERIFIED (local use)
**Last Updated:** 2026-02-13
**Notes:** Used extensively for local browser exploration. Updated with 28+ tools, CLI alternative, model recommendations.

### `PLAYWRIGHT_CLI_EVALUATION.md`
**Status:** VERIFIED
**Created:** 2026-02-13
**Notes:** Hands-on evaluation of `@playwright/cli` against fwaptile-wordle (localhost:3011).
CLI vs MCP comparison with real token measurements. 6 CLI tests + equivalent MCP tests run.
Measured 2.4x-3.7x token savings (vs marketed 4x). CLI handles WSL2 sandboxing automatically.

### `BROWSER_AUTOMATION_LANDSCAPE_2026.md`
**Status:** PARTIALLY VERIFIED
**Created:** 2026-02-13
**Notes:** Comprehensive landscape analysis. CLI section updated from "needs testing" to verified findings based on PLAYWRIGHT_CLI_EVALUATION.md. Model benchmarks from official documentation. Approaches 1 (MCP), 2 (CLI), 4 (Scripted) verified. Approaches 3 (Chrome) and 5 (Agents) documented but untested (Chrome not available on WSL2, Agents experimental).

### `AUDIT_2026-02.md`
**Status:** VERIFIED
**Created:** 2026-02-13
**Notes:** Cross-repo audit based on direct file inspection of all 24 repos. Per-repo configs verified against actual `.mcp.json` and `playwright.config.ts` files. Production fixes applied and verified.

### `COST_OPTIMIZATION_GUIDE.md`
**Status:** RESEARCH-BASED
**Last Updated:** 2026-02-13
**Notes:** Pricing updated to Feb 2026. Model selection benchmarks from OSWorld. Opus 4.6 Fast Mode and Codex Spark sections added. CLI token comparison from published analysis.

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
**Last Updated:** 2026-02-13
**Used in:** `epcvip-tools-hub/playwright.config.ts`
**Notes:** Updated with BASE_URL env var pattern (from fwaptile-wordle best practice). Conditional webServer support.

### `mcp.json.template`
**Status:** VERIFIED
**Created:** 2026-02-13
**Used in:** Applied to fwaptile-wordle, competitor-analyzer, epcvip-tools-hub
**Notes:** Four platform variants (WSL2, macOS, CI, video recording). Standardized flags verified across production repos.

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
| 2026-02-13 | **NEW** PLAYWRIGHT_CLI_EVALUATION.md — hands-on CLI vs MCP evaluation (6 tests, token measurements, 2.4-3.7x savings) |
| 2026-02-13 | **UPDATED** BROWSER_AUTOMATION_LANDSCAPE_2026.md — CLI status from "needs testing" to verified, real token numbers |
| 2026-02-13 | **NEW** AUDIT_2026-02.md — cross-repo Playwright audit (4/24 repos, 19 test files, 3,467 lines) |
| 2026-02-13 | **NEW** BROWSER_AUTOMATION_LANDSCAPE_2026.md — 5 approaches, model selection, platform matrix |
| 2026-02-13 | **NEW** mcp.json.template — standardized MCP configs for WSL2/macOS/CI/video |
| 2026-02-13 | **UPDATED** COST_OPTIMIZATION_GUIDE.md — Opus 4.6 pricing, Fast Mode, Haiku 4.5 for QA, CLI tokens |
| 2026-02-13 | **UPDATED** PLAYWRIGHT_CLAUDE_GUIDE.md — 5 approaches (was 4 modes), Chrome beta, MCP v0.0.64 |
| 2026-02-13 | **UPDATED** MCP_WORKFLOW_GUIDE.md — 28+ tools, CLI alternative, model recommendations |
| 2026-02-13 | **UPDATED** docs/reference/PLAYWRIGHT-MCP.md — v0.0.64, browser_run_code, Chrome beta |
| 2026-02-13 | **UPDATED** playwright.config.ts.template — BASE_URL env var, conditional webServer |
| 2026-02-13 | **FIXED** fwaptile-wordle/.mcp.json — added -y, --no-sandbox |
| 2026-02-13 | **FIXED** competitor-analyzer/.mcp.json — added -y, --no-sandbox, type: stdio |
| 2026-02-13 | **FIXED** epcvip-tools-hub/playwright.config.ts — added BASE_URL env var support |
| 2026-01-08 | **VERIFIED** claude-qa-workflow.yml.template (Run #20800668844, $0.62, 39 turns) |
| 2026-01-08 | **VERIFIED** security-review.yml.template (Run #20800666122, 36s) |
| 2026-01-08 | Added `id-token: write` permission (required for OIDC) |
| 2026-01-08 | Added `workflow_dispatch` triggers for manual testing |
| 2026-01-07 | Created this STATUS.md |
| 2026-01-07 | Fixed CI templates to use official actions |
| 2026-01-07 | Updated RESEARCH_ARCHIVE with official sources |
| 2026-01-06 | Initial templates created |

---

## See Also

- [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) — Main guide (verification entries reference this)
- [examples/](./examples/) — Template files tracked in this status doc
- [AUDIT_2026-02.md](./AUDIT_2026-02.md) — Source of per-repo verification entries
- [README.md](./README.md) — Testing templates directory hub
