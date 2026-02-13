# MCP Workflow Guide

A practical guide for using Claude Code with Playwright MCP for browser automation, debugging, and exploration.

> **February 2026 Update:** MCP is now at v0.0.64 with 28+ tools. For a comparison of MCP vs the new Playwright CLI (2-4x fewer tokens, verified), see [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md).

## What is MCP?

**Model Context Protocol (MCP)** is a standard that allows AI tools to communicate with local systems. Playwright MCP exposes browser automation as tools that Claude can call directly.

> "MCP lets the AI interact with a real browser, observe the page state, and execute actions directly instead of guessing." — [Microsoft](https://github.com/microsoft/playwright-mcp)

## Setup

### One-Time Installation

```bash
# Add Playwright MCP to Claude Code
claude mcp add playwright npx '@playwright/mcp@latest'
```

### Manual Configuration (Recommended)

Add to project `.mcp.json`:

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

> **Required flags:** `-y` (auto-confirm npx), `--no-sandbox` (WSL2/Linux). See [examples/mcp.json.template](./examples/mcp.json.template) for platform variants.

### Verify Installation

In Claude Code, say:
```
Navigate to https://example.com and describe what you see
```

Claude should open a browser, navigate, and describe the page.

## How MCP Works

### The Cycle

```
┌─────────────────────────────────────────────────────────┐
│  1. NAVIGATE                                             │
│     browser_navigate({ url: '...' })                    │
│                    ↓                                     │
│  2. OBSERVE                                              │
│     browser_snapshot() → Returns accessibility tree      │
│     + screenshot that Claude SEES                        │
│                    ↓                                     │
│  3. DECIDE                                               │
│     Claude analyzes page, plans next action              │
│                    ↓                                     │
│  4. ACT                                                  │
│     browser_click(), browser_type(), etc.               │
│                    ↓                                     │
│  5. REPEAT                                               │
│     Back to step 2 for verification                      │
└─────────────────────────────────────────────────────────┘
```

### Key Difference from Scripted Tests

| Scripted Tests | MCP |
|----------------|-----|
| Pre-written assertions | Claude decides what to check |
| Fast, deterministic | Slower, intelligent |
| Catches what you specify | Catches what Claude notices |
| Runs in CI | Interactive exploration |

## Available Tools

### Navigation
| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_navigate_back` | Go back |
| `browser_navigate_forward` | Go forward |
| `browser_tabs` | List, create, switch tabs |

### Observation
| Tool | Purpose |
|------|---------|
| `browser_snapshot` | Get accessibility tree + screenshot |
| `browser_take_screenshot` | Save screenshot to file |
| `browser_console_messages` | Get console output |
| `browser_network_requests` | Get network activity |

### Interaction
| Tool | Purpose |
|------|---------|
| `browser_click` | Click element |
| `browser_type` | Type text (character by character) |
| `browser_fill_form` | Fill multiple fields |
| `browser_select_option` | Select dropdown option |
| `browser_press_key` | Press keyboard key |
| `browser_hover` | Hover over element |
| `browser_drag` | Drag and drop |

### Automation
| Tool | Purpose |
|------|---------|
| `browser_run_code` | Run Playwright code snippets directly |

### Utility
| Tool | Purpose |
|------|---------|
| `browser_wait_for` | Wait for text/element |
| `browser_evaluate` | Run JavaScript on page |
| `browser_handle_dialog` | Accept/dismiss browser dialogs |
| `browser_close` | Close browser |
| `browser_resize` | Resize viewport |
| `browser_install` | Install browser (first-time setup) |

## Workflow Patterns

### Pattern 1: Exploratory Testing

**Prompt:**
```
Navigate to http://localhost:3000 and explore the checkout flow.
Try to find bugs, edge cases, or confusing UX.
Take screenshots of any issues you find.
```

**Claude will:**
1. Navigate to the app
2. Explore like a real user
3. Try edge cases (empty cart, invalid input)
4. Report issues with evidence

### Pattern 2: Visual Verification

**Prompt:**
```
Navigate to http://localhost:3000/dashboard and verify:
1. The header shows the user's name
2. The stats cards show numbers (not loading spinners)
3. The sidebar has 5 menu items
4. No console errors
```

**Claude will:**
1. Navigate and snapshot
2. Verify each item
3. Report pass/fail with details

### Pattern 3: Test Generation

**Prompt:**
```
Navigate to http://localhost:3000/login and understand the login flow.
Then write a Playwright test that verifies:
- Valid login succeeds
- Invalid password shows error
- Empty fields show validation
```

**Claude will:**
1. Explore the login page
2. Test different scenarios
3. Generate test code based on observations

### Pattern 4: Failure Investigation

**Prompt:**
```
A test is failing with "element not found: [data-testid='submit']".
Navigate to http://localhost:3000/checkout and investigate.
Find where the submit button is and why the selector might fail.
```

**Claude will:**
1. Navigate to the page
2. Search for submit-related elements
3. Compare actual DOM to expected selector
4. Suggest fixes

### Pattern 5: Competitor Analysis

**Prompt:**
```
Navigate to https://competitor.com/pricing and extract:
1. Pricing tiers and costs
2. Feature list for each tier
3. Any promotional offers
Take screenshots for reference.
```

**Claude will:**
1. Navigate to competitor
2. Extract structured data
3. Save screenshots
4. Summarize findings

## Authentication Handling

Since the browser is visible, handle auth manually:

1. **Ask Claude to navigate to login:**
   ```
   Navigate to http://localhost:3000/login and wait for me to log in
   ```

2. **Log in yourself** in the visible browser

3. **Continue with Claude:**
   ```
   I've logged in. Now explore the dashboard and check for issues.
   ```

### Persisting Auth State

For repeated testing, save auth state:

```typescript
// In a setup test
await page.context().storageState({ path: 'playwright/.auth/user.json' });
```

Then tell Claude:
```
Use the saved auth state from playwright/.auth/user.json
```

## Screenshot-Driven Debugging

### Taking Screenshots

```
Navigate to /checkout and take a screenshot of the cart
```

Screenshots are saved to `.playwright-mcp/` directory.

### Using Screenshots as Evidence

```
Take screenshots of each step in the checkout flow:
1. Cart view
2. Shipping form
3. Payment form
4. Confirmation page
```

### Screenshot Comparison

```
Navigate to /dashboard.
Compare what you see to this screenshot: [reference.png]
Report any differences.
```

## Best Practices

### 1. Be Specific in Prompts

**Bad:**
```
Test the app
```

**Good:**
```
Navigate to http://localhost:3000/settings.
Verify that:
1. The user can update their display name
2. Changes persist after page refresh
3. Invalid names show an error message
```

### 2. Request Evidence

Always ask for screenshots or specific observations:
```
Take a screenshot of any errors you encounter
```

### 3. Use for What Scripts Can't Do

**Good uses for MCP:**
- Visual verification
- Exploratory testing
- Competitor analysis
- Understanding unfamiliar UIs
- Debugging failures

**Use scripted tests instead for:**
- Regression testing
- CI/CD pipelines
- Repetitive checks

### 4. Combine with Scripted Tests

```
Explore the new feature using MCP, then:
1. Identify key scenarios
2. Write Playwright tests for each
3. Run tests in CI
```

## Troubleshooting

### Browser Won't Open

```bash
# Reinstall browser
npx playwright install chromium
```

### MCP Not Recognized

```bash
# Verify MCP is configured
cat ~/.claude.json | grep playwright
```

### Slow Performance

**Option 1: Playwright CLI (recommended for token savings)**

The new Playwright CLI uses 2-4x fewer tokens than MCP. See [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md#3-playwright-cli-vs-mcp-comparison) for setup and comparison.

**Option 2: `@tontoko/fast-playwright-mcp` fork**

Third-party fork that optimizes MCP tokens. The official CLI is now the better alternative, but this exists:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@tontoko/fast-playwright-mcp"]
    }
  }
}
```

### Model Selection for MCP Workflows

Use **Haiku 4.5** for MCP-driven QA to reduce costs — same browser automation accuracy as Sonnet (61% OSWorld) at 3x lower cost. See [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md#model-selection-for-browser-automation) for full analysis.

## Integration with CI

While MCP is primarily for interactive use, you can trigger Claude-driven testing in CI:

```yaml
# GitHub Actions example (experimental)
- name: Claude QA Check
  uses: anthropic/claude-code-action@v1
  with:
    prompt: |
      Navigate to ${{ env.PREVIEW_URL }}
      Verify the deployment is working correctly
      Report any issues found
```

See [Alex Op's AI QA Engineer](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/) for a full implementation.

## Playwright CLI Alternative

For workflows where token cost matters (CI, batch automation), consider the **Playwright CLI** — uses shell commands instead of MCP tools, achieving 2-4x token reduction (~890 vs ~3,330 tokens measured per flow).

| Aspect | MCP | CLI |
|--------|-----|-----|
| Tokens per flow | ~3,330 | ~890 |
| Setup | `.mcp.json` config | `npm i -g @anthropic-ai/playwright-cli` + `playwright-cli install` |
| Best for | Interactive exploration | Scripted automation, CI |

See [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md#3-playwright-cli-vs-mcp-comparison) for full comparison.

## Further Reading

- [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) — Full landscape analysis
- [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md) — Model pricing and optimization
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Simon Willison's TIL](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)
- [TestLeaf 2026 Guide](https://www.testleaf.com/blog/playwright-mcp-ai-test-automation-2026/)
- [Building AI QA Engineer](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/)
