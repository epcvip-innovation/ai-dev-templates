# Playwright + Claude Code Testing Guide

A comprehensive guide for automated E2E testing using Playwright, with patterns for Claude Code integration.

> **2026 Insight**: "2026 is the year testers move from 'writing scripts' to orchestrating AI-powered automation workflows." — [TestLeaf](https://www.testleaf.com/blog/playwright-mcp-ai-test-automation-2026/)

## The 5 Approaches to Playwright (February 2026)

| Approach | Command / Setup | Who Sees Page | Best For |
|----------|----------------|---------------|----------|
| **Headless** | `npx playwright test` | Nobody | CI/CD, fast regression |
| **Headed** | `npx playwright test --headed` | Human watches | Demos, stakeholder presentations |
| **UI Mode** | `npx playwright test --ui` | Human interacts | Debugging, writing tests |
| **MCP** | Claude + Playwright MCP | Claude AI | Exploration, visual bugs, competitor analysis |
| **Chrome** | Claude Code Chrome (beta) | Claude AI | Quick browser tasks (macOS/Linux only, **NOT WSL2**) |

> **New in 2026:** Playwright CLI (`@playwright/cli`) offers ~3x token savings vs MCP (verified) — see [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) and [evaluation results](./PLAYWRIGHT_CLI_EVALUATION.md).

## Three Fundamental Approaches

### Approach 1: Scripted Tests (CI/Regression)

```
Code runs → Assertions check → Pass/Fail
```

- **Who sees the page**: Nobody — just code assertions
- **Speed**: Fast (milliseconds per action)
- **Repeatability**: 100% deterministic
- **Best for**: CI/CD, regression testing, automated checks

### Approach 2: MCP Browser Control (Claude-Driven)

```
Claude navigates → Takes snapshot → Claude SEES the page → Decides action
```

- **Who sees the page**: Claude AI sees accessibility tree and DOM
- **Speed**: Slower (AI thinking time + MCP protocol overhead)
- **Best for**: Exploration, debugging, one-off tasks, visual verification
- **Current version**: v0.0.64 (in-memory profiles by default)

### Approach 3: Claude Code Chrome (Beta)

```
Claude uses built-in browser → No MCP setup needed
```

- **Who sees the page**: Claude AI directly
- **Speed**: Fast (no MCP protocol overhead)
- **Platform**: macOS, native Linux only — **does NOT work on WSL2**
- **Best for**: Quick browser tasks when MCP isn't configured

> **WSL2 users:** Claude Code Chrome is not available in WSL2. Use Playwright MCP instead.

## When to Use Which

| Scenario | Use Scripted Tests | Use MCP |
|----------|-------------------|---------|
| CI/CD pipeline | ✅ | ❌ |
| Regression testing | ✅ | ❌ |
| Visual bug hunting | ❌ | ✅ |
| Exploring new features | ❌ | ✅ |
| Debugging failures | ❌ | ✅ |
| Writing new tests | ❌ → ✅ | ✅ (explore first) |

**Ideal workflow**:
1. Claude MCP explores app → finds issues → writes test
2. Scripted test runs in CI → catches regressions
3. On failure → Claude MCP investigates with screenshots

## Project Setup

### 1. Install Playwright

```bash
npm init playwright@latest
# Or add to existing project:
npm install -D @playwright/test
npx playwright install
```

### 2. Configure `playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './test/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',      // Capture trace on failure
    video: 'on-first-retry',      // Record video on failure
    screenshot: 'only-on-failure', // Screenshot on failure
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 13'] },
    },
  ],

  // Auto-start your dev server
  webServer: {
    command: 'npm start',
    url: 'http://localhost:3000/health',
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
});
```

### 3. Directory Structure

```
project/
├── test/
│   └── e2e/
│       ├── fixtures.ts        # Custom test fixtures
│       ├── helpers/
│       │   └── PageObject.ts  # Page Object Models
│       ├── auth.spec.ts       # Test files
│       └── checkout.spec.ts
├── playwright.config.ts
└── package.json
```

## Page Object Model Pattern

Encapsulate page interactions for cleaner, reusable tests.

### `helpers/LoginPage.ts`

```typescript
import { Page, BrowserContext, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly context: BrowserContext;

  constructor(page: Page, context: BrowserContext) {
    this.page = page;
    this.context = context;
  }

  // Navigation
  async goto() {
    await this.page.goto('/login');
    await this.page.waitForSelector('[data-testid="login-form"]');
  }

  // Actions
  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
    await this.page.waitForURL('/dashboard');
  }

  // State inspection
  async getErrorMessage() {
    return this.page.textContent('[data-testid="error"]');
  }

  // Cleanup
  async close() {
    await this.context.close();
  }
}
```

## Custom Fixtures for Multi-User Testing

Essential for multiplayer or multi-session scenarios.

### `fixtures.ts`

```typescript
import { test as base, Browser } from '@playwright/test';
import { LoginPage } from './helpers/LoginPage';

type CustomFixtures = {
  // Factory for creating isolated user contexts
  createUserContext: (name: string) => Promise<LoginPage>;

  // Pre-configured two-user setup
  twoUsers: { userA: LoginPage; userB: LoginPage };
};

export const test = base.extend<CustomFixtures>({
  // Factory fixture: creates isolated contexts on demand
  createUserContext: async ({ browser }, use) => {
    const users: LoginPage[] = [];

    const factory = async (name: string) => {
      const context = await browser.newContext();
      const page = await context.newPage();
      const user = new LoginPage(page, context);
      users.push(user);
      return user;
    };

    await use(factory);

    // Cleanup all created users
    for (const user of users) {
      await user.close();
    }
  },

  // Two users ready to interact
  twoUsers: async ({ browser }, use) => {
    const ctxA = await browser.newContext();
    const ctxB = await browser.newContext();

    const pageA = await ctxA.newPage();
    const pageB = await ctxB.newPage();

    const userA = new LoginPage(pageA, ctxA);
    const userB = new LoginPage(pageB, ctxB);

    await use({ userA, userB });

    await userA.close();
    await userB.close();
  },
});

export { expect } from '@playwright/test';
```

### Using Fixtures in Tests

```typescript
import { test, expect } from './fixtures';

test('two users can chat', async ({ twoUsers }) => {
  const { userA, userB } = twoUsers;

  await userA.goto();
  await userA.login('alice@test.com', 'password');

  await userB.goto();
  await userB.login('bob@test.com', 'password');

  // Now both users are logged in with isolated sessions
});
```

## What Scripted Tests Actually Check

Tests only verify what you explicitly assert — they won't catch CSS issues, broken images, or console errors unless you add assertions for them.

**Extend coverage** with: `page.on('console', ...)` for console errors, `toHaveScreenshot()` for visual regression, and `@axe-core/playwright` for accessibility. See [Playwright docs](https://playwright.dev/docs/test-assertions) for full assertion reference.

## Debugging & Artifacts

### Run Modes

```bash
# Headless (default, for CI)
npx playwright test

# Headed (see browsers)
npx playwright test --headed

# UI mode (interactive debugging)
npx playwright test --ui

# Debug mode (step through)
npx playwright test --debug
```

### Traces & Reports

```bash
# Record traces
npx playwright test --trace on

# View HTML report
npx playwright show-report

# View specific trace
npx playwright show-trace test-results/*/trace.zip
```

### What Traces Capture

- Screenshots at every action
- DOM snapshots (inspectable)
- Network requests/responses
- Console logs
- Step-by-step timeline

## UI Mode Deep Dive

UI Mode (`--ui`) opens an interactive IDE for test development and debugging.

### Launching UI Mode

```bash
npx playwright test --ui
```

### UI Mode Features

```
┌─────────────────────────────────────────────────────────────────┐
│  PLAYWRIGHT                        Timeline (2.0s - 30.0s)      │
├──────────────┬──────────────────────────────────────────────────┤
│  TESTS       │  Actions │ Metadata    │ Action │ Before │ After │
│  ○ auth.spec │                        ├────────────────────────┤
│    ○ login   │                        │  Browser Preview       │
│    ○ logout  │                        │  (Live or snapshot)    │
│  ○ cart.spec │                        │                        │
├──────────────┴──────────────────────────────────────────────────┤
│  Locator │ Source │ Call │ Log │ Errors │ Console │ Network    │
└─────────────────────────────────────────────────────────────────┘
```

### Key Panels

| Panel | Purpose |
|-------|---------|
| **Tests Sidebar** | List of all tests, click to select |
| **Timeline** | Scrub through test execution |
| **Browser Preview** | Live browser or DOM snapshot at each step |
| **Locator** | Test and refine element selectors |
| **Source** | View test code at current step |
| **Call** | See Playwright API call details |
| **Network** | Inspect API requests/responses |
| **Console** | Browser console output |
| **Errors** | Test failures and stack traces |

### When to Use UI Mode

- **Writing new tests** — See DOM as you build selectors
- **Debugging failures** — Step through timeline to find issue
- **Understanding flows** — Watch how pages transition
- **Refining locators** — Test selectors in real-time

### UI Mode Workflow

1. Launch: `npx playwright test --ui`
2. Click test in sidebar to load it
3. Click play button to run test
4. Scrub timeline to see each step
5. Click on step to see DOM snapshot
6. Use Locator tab to refine selectors
7. View Network tab to debug API issues

## CI Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: npm ci
      - run: npx playwright install --with-deps

      - run: npx playwright test

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

## MCP Integration with Claude Code

The Model Context Protocol (MCP) lets Claude control a real browser, observe results, and make intelligent decisions.

> **Key Insight**: "MCP lets the AI interact with a real browser, observe the page state, and execute actions directly instead of guessing." — [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)

### Setup

```bash
# Add Playwright MCP to Claude Code (one-time setup)
claude mcp add playwright npx '@playwright/mcp@latest'
```

Or configure manually in `.mcp.json` (project-level, recommended):

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest", "--no-sandbox"]
    }
  }
}
```

> **WSL2/Linux:** Always include `--no-sandbox`. See [mcp.json.template](../../docs/mcp/playwright/examples/mcp.json.template) for platform-specific configs.

> **v0.0.64 note:** In-memory profiles are now the default (`--isolated` behavior). Use `--user-data-dir` for persistent profiles.

### Available MCP Tools

Claude can use 28+ browser control tools:

| Category | Tools |
|----------|-------|
| **Navigation** | `browser_navigate`, `browser_navigate_back` |
| **Observation** | `browser_snapshot`, `browser_take_screenshot`, `browser_console_messages` |
| **Interaction** | `browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`, `browser_hover`, `browser_drag` |
| **Input** | `browser_press_key`, `browser_file_upload`, `browser_handle_dialog` |
| **State** | `browser_network_requests`, `browser_tabs`, `browser_evaluate` |
| **Automation** | `browser_run_code` — run Playwright code snippets directly |
| **Control** | `browser_wait_for`, `browser_resize`, `browser_close`, `browser_install` |

### How MCP Works

```typescript
// 1. Navigate to page
mcp__playwright__browser_navigate({ url: 'http://localhost:3000' })

// 2. Take snapshot - Claude SEES the page
mcp__playwright__browser_snapshot()
// Returns accessibility tree + reference IDs for elements

// 3. Interact using element references
mcp__playwright__browser_click({ element: 'Submit button', ref: 'e15' })
mcp__playwright__browser_type({ element: 'Email field', ref: 'e10', text: 'test@example.com' })

// 4. Verify with another snapshot
mcp__playwright__browser_snapshot()
```

### MCP Workflow Patterns

**Pattern 1: Visual Bug Hunting**
```
Claude navigates → Takes snapshot → Spots visual issues → Reports with screenshot
```

**Pattern 2: Test Generation**
```
Claude explores feature → Observes behavior → Writes Playwright test code
```

**Pattern 3: Failure Investigation**
```
CI fails → Claude navigates to failing page → Investigates live → Reports findings
```

**Pattern 4: Competitor Analysis**
```
Claude navigates to competitor → Captures features → Extracts data → Compares
```

### What MCP Can Catch That Scripts Miss

| Scripts Miss | MCP Catches |
|--------------|-------------|
| CSS styling issues | ✅ Claude sees layout |
| Typos in text | ✅ Claude reads content |
| Broken images | ✅ Claude notices missing visuals |
| Confusing UX | ✅ Claude evaluates flow |
| Console errors | ✅ `browser_console_messages` |

### Best Practices for MCP

1. **Be specific in prompts**
   ```
   Navigate to /checkout and verify the cart shows 3 items with correct prices
   ```

2. **Request screenshots as evidence**
   ```
   Take a screenshot of any issues you find
   ```

3. **Use for exploration, not regression**
   - MCP is slower than scripted tests
   - Best for visual verification and debugging

4. **Authenticate manually when needed**
   - Browser window is visible
   - Log in yourself, then let Claude explore

## Best Practices

### 1. Use `data-testid` Attributes

```html
<button data-testid="submit-order">Place Order</button>
```

```typescript
await page.click('[data-testid="submit-order"]');
```

### 2. Wait for State, Not Time

```typescript
// Bad
await page.waitForTimeout(2000);

// Good
await page.waitForSelector('[data-testid="results"]');
await page.waitForURL('/success');
await expect(page.locator('.loading')).toBeHidden();
```

### 3. Isolate Test Data

```typescript
// Each test gets fresh context
test('user can checkout', async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();
  // This session is completely isolated
});
```

### 4. Make Tests Independent

Each test should:
- Set up its own state
- Not depend on other tests
- Clean up after itself

### 5. Use Descriptive Test Names

```typescript
test('guest user sees login prompt when adding to cart', async ({ page }) => {
  // Clear what's being tested
});
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npx playwright test` | Run all tests |
| `npx playwright test --headed` | See browser windows |
| `npx playwright test --ui` | Interactive UI mode |
| `npx playwright test --debug` | Step-through debugging |
| `npx playwright test --trace on` | Record traces |
| `npx playwright show-report` | View HTML report |
| `npx playwright codegen` | Generate tests by recording |

## Platform Compatibility

| Approach | macOS | Linux | WSL2 | CI (Ubuntu) |
|----------|:-----:|:-----:|:----:|:-----------:|
| Playwright MCP | Yes | Yes | Yes* | Yes** |
| Playwright CLI | Yes | Yes | Yes* | Yes |
| Claude Code Chrome | Yes | Yes | **NO** | No |
| Scripted Tests | Yes | Yes | Yes* | Yes |

*\*Requires `--no-sandbox` flag*
*\*\*Requires `--headless` flag*

## See Also

- [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) — Full landscape analysis, model selection guide
- [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md) — Model pricing and cost optimization
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Page Object Model](https://playwright.dev/docs/pom)
- [Fixtures](https://playwright.dev/docs/test-fixtures)
- [Visual Comparisons](https://playwright.dev/docs/test-snapshots)
