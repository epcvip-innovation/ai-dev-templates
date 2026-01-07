# Testing Templates

E2E testing patterns for Claude Code projects using Playwright.

> **Status:** See [STATUS.md](./STATUS.md) for what's verified vs. untested.

> **2026 Insight**: "2026 is the year testers move from 'writing scripts' to orchestrating AI-powered automation workflows."

## Contents

| File | Purpose |
|------|---------|
| [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) | Comprehensive guide: all 4 modes, setup, patterns |
| [MCP_WORKFLOW_GUIDE.md](./MCP_WORKFLOW_GUIDE.md) | Claude-driven browser control workflows |
| [COMPETITOR_ANALYSIS.md](./COMPETITOR_ANALYSIS.md) | Using MCP for competitor research |
| [RESEARCH_ARCHIVE.md](./RESEARCH_ARCHIVE.md) | Curated 2026 research findings and sources |
| [examples/](./examples/) | Copy-paste starter files |

## The 4 Modes of Playwright

| Mode | Command | Best For |
|------|---------|----------|
| **Headless** | `npx playwright test` | CI/CD, fast regression |
| **Headed** | `npx playwright test --headed` | Demos, stakeholder presentations |
| **UI Mode** | `npx playwright test --ui` | Debugging, writing tests |
| **MCP** | Claude + Playwright MCP | Exploration, visual bugs, competitor analysis |

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
- Auto-start dev server
- Trace/video on failure
- Chrome + mobile projects

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

- [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) - Full guide
- [MCP_WORKFLOW_GUIDE.md](./MCP_WORKFLOW_GUIDE.md) - MCP-specific patterns
- [COMPETITOR_ANALYSIS.md](./COMPETITOR_ANALYSIS.md) - Market research automation
- [Playwright Docs](https://playwright.dev/docs/intro)
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)
