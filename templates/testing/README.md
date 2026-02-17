# Testing Templates

[← Back to Main README](../../README.md)

E2E testing patterns for Claude Code projects using Playwright.

> **2026 Insight**: "2026 is the year testers move from 'writing scripts' to orchestrating AI-powered automation workflows."

## Start Here

**New to Playwright + Claude Code?** Start with [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) — it covers all 5 approaches, setup, and patterns.

**Already using Playwright?** Jump to what you need:

| Goal | Read |
|------|------|
| Reduce token costs / pick the right model | [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md) |
| Use MCP for browser exploration | [Playwright MCP Guide](../../docs/mcp/playwright/README.md) |
| CLI vs MCP vs Chrome — full comparison | [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) |

**Want the full picture?** [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) covers every approach, model benchmark, and platform compatibility matrix.

## Contents

| File | Type | Purpose |
|------|------|---------|
| [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) | Guide | Comprehensive guide: 5 approaches, setup, patterns |
| [Playwright MCP Guide](../../docs/mcp/playwright/README.md) | Guide | Claude-driven browser control (moved to docs/mcp/) |
| [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md) | Reference | Cost analysis, model pricing, optimization strategies |
| [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) | Reference | Full landscape: 5 approaches, model selection, platform compatibility |
| [PLAYWRIGHT_CLI_EVALUATION.md](./PLAYWRIGHT_CLI_EVALUATION.md) | Reference | CLI vs MCP token measurements and comparison |
| [COMPETITOR_ANALYSIS.md](./COMPETITOR_ANALYSIS.md) | Guide | Using MCP for competitor research |
| [RESEARCH_ARCHIVE.md](./RESEARCH_ARCHIVE.md) | Archive | Curated 2026 research findings and sources |
| [examples/](./examples/) | Templates | Copy-paste starter files (configs, Page Objects, fixtures) |

## The 5 Approaches to Playwright

| Approach | Command / Setup | Best For |
|----------|----------------|----------|
| **Headless** | `npx playwright test` | CI/CD, fast regression |
| **Headed** | `npx playwright test --headed` | Demos, stakeholder presentations |
| **UI Mode** | `npx playwright test --ui` | Debugging, writing tests |
| **MCP** | Claude + Playwright MCP | Exploration, visual bugs, competitor analysis |
| **Chrome** | Claude Code Chrome (beta) | Quick browser tasks (macOS/Linux, **NOT WSL2**) |

> **New:** Playwright CLI (`@playwright/cli`) offers ~3x token savings vs MCP (verified) — see [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) and [evaluation results](./PLAYWRIGHT_CLI_EVALUATION.md).

## Quick Start

### Scripted Tests
```bash
npm init playwright@latest              # Install
npx playwright test                     # Run tests
npx playwright test --headed            # See browsers
npx playwright test --ui                # Interactive debugger
```

### Claude MCP Setup
```bash
claude mcp add playwright npx '@playwright/mcp@latest'
```

Then in Claude Code:
```
Navigate to http://localhost:3000 and explore the checkout flow
```

## What Each Approach Catches

| Approach | Catches | Misses |
|----------|---------|--------|
| **Scripted Tests** | Workflow breaks, regressions | Visual bugs, typos, UX issues |
| **Claude MCP** | Visual issues, layout, confusing UX | Nothing (but slower) |

**Key insight**: Scripted tests only verify what you explicitly assert. Claude MCP visually inspects everything.

## Use Cases

### 1. Automated Regression (Scripted)
```
Commit → CI runs tests → Pass/Fail → Screenshots on failure
```

### 2. Visual Bug Hunting (MCP)
```
Claude navigates → Takes snapshot → Spots issues → Reports with screenshots
```

### 3. Competitor Analysis (MCP)
```
Claude navigates to competitor → Extracts pricing/features → Compares to ours
```

### 4. Test Generation (MCP → Scripted)
```
Claude explores feature → Writes test code → Human reviews → Commits to CI
```

### 5. Failure Investigation (UI Mode + MCP)
```
CI fails → Open trace in UI Mode → Claude MCP explores live → Fix identified
```

## Key Patterns

### Page Object Model
Encapsulate page interactions:
```typescript
class CheckoutPage {
  async addToCart(product: string) {
    await this.page.click(`[data-testid="add-${product}"]`);
    await this.page.waitForSelector('[data-testid="cart-updated"]');
  }
}
```

### Multi-User Fixtures
For multiplayer/multi-session testing:
```typescript
export const test = base.extend({
  twoUsers: async ({ browser }, use) => {
    const userA = await createIsolatedContext(browser);
    const userB = await createIsolatedContext(browser);
    await use({ userA, userB });
  },
});
```

## Template Files

### `examples/playwright.config.ts.template`
Ready-to-use configuration with:
- `BASE_URL` env var support (test localhost or production)
- Conditional `webServer` (only starts when targeting localhost)
- Auto-start dev server, trace/video on failure
- Chrome + Firefox + mobile projects

### [`mcp.json.template`](../../docs/mcp/playwright/examples/mcp.json.template)
Standardized MCP configs (moved to `docs/mcp/playwright/examples/`):
- WSL2/Linux (with `--no-sandbox`)
- macOS (minimal flags)
- CI/Headless (with `--headless`)
- Video recording (competitor analysis)

### `examples/fixtures.ts.template`
Custom fixtures for:
- Factory to create isolated contexts
- Pre-configured two-user setup
- Authenticated user setup

### `examples/PageObject.ts.template`
Page Object Model with:
- Navigation helpers
- Action methods
- State inspection
- Cleanup

## Reading Order

```
PLAYWRIGHT_CLAUDE_GUIDE          ← start here
    │           │           │
    ▼           ▼           ▼
PLAYWRIGHT   COST_OPT   BROWSER_LANDSCAPE
MCP GUIDE*                     │
    │                          ▼
    ▼                    CLI_EVALUATION
COMPETITOR
ANALYSIS

* docs/mcp/playwright/
```

**Background reading**: [RESEARCH_ARCHIVE](./RESEARCH_ARCHIVE.md)

## External Links

- [Playwright Docs](https://playwright.dev/docs/intro)
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Playwright Agents](https://playwright.dev/docs/test-agents) — AI-powered test generation (v1.56+, experimental)

---

## See Also

- [CI/CD Templates](../ci/README.md) — GitHub Actions with Playwright
- [Playwright MCP Guide](../../docs/mcp/playwright/README.md) — Claude-driven browser control
- [All Templates](../README.md)
