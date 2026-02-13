# Testing Templates

E2E testing patterns for Claude Code projects using Playwright.

> **Status:** See [STATUS.md](./STATUS.md) for what's verified vs. untested.

> **2026 Insight**: "2026 is the year testers move from 'writing scripts' to orchestrating AI-powered automation workflows."

## Contents

| File | Purpose |
|------|---------|
| [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) | Comprehensive guide: 5 approaches, setup, patterns |
| [MCP_WORKFLOW_GUIDE.md](./MCP_WORKFLOW_GUIDE.md) | Claude-driven browser control workflows |
| [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md) | Cost analysis, model pricing, optimization strategies |
| [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) | **NEW** Full landscape: 5 approaches, model selection, platform compatibility |
| [AUDIT_2026-02.md](./AUDIT_2026-02.md) | **NEW** Cross-repo Playwright audit with per-repo findings |
| [COMPETITOR_ANALYSIS.md](./COMPETITOR_ANALYSIS.md) | Using MCP for competitor research |
| [RESEARCH_ARCHIVE.md](./RESEARCH_ARCHIVE.md) | Curated 2026 research findings and sources |
| [examples/](./examples/) | Copy-paste starter files (configs, Page Objects, fixtures) |

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

### `examples/mcp.json.template`
Standardized MCP configs for:
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

## Further Reading

- [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) — Full guide with 5 approaches
- [MCP_WORKFLOW_GUIDE.md](./MCP_WORKFLOW_GUIDE.md) — MCP-specific patterns
- [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md) — Cost analysis, model selection
- [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) — Landscape analysis, CLI vs MCP
- [AUDIT_2026-02.md](./AUDIT_2026-02.md) — Cross-repo audit findings
- [COMPETITOR_ANALYSIS.md](./COMPETITOR_ANALYSIS.md) — Market research automation
- [Playwright Docs](https://playwright.dev/docs/intro)
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Playwright Agents](https://playwright.dev/docs/test-agents) — AI-powered test generation (v1.56+, experimental)
