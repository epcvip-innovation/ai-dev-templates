# Playwright MCP Guide

[← Back to MCP Hub](../README.md) | [← Back to Main README](../../../README.md)

**Last Updated**: February 2026 | **MCP Version**: v0.0.64

Comprehensive guide to setting up Playwright MCP for browser automation with Claude Code.

> **February 2026:** MCP v0.0.64 uses in-memory profiles by default. New tools: `browser_run_code`, `browser_handle_dialog`, `browser_fill_form`. See [BROWSER_AUTOMATION_LANDSCAPE_2026.md](../../../templates/testing/BROWSER_AUTOMATION_LANDSCAPE_2026.md) for alternatives (CLI, Chrome beta).

---

## What is Playwright MCP?

Playwright MCP is a Model Context Protocol server that gives Claude browser automation capabilities using Microsoft's Playwright framework. Unlike screenshot-based automation, it uses **accessibility snapshots** - a semantic understanding of web pages that makes automation more reliable and faster.

**Key Benefits:**
- Claude can interact with web pages directly
- Authentication is simple (use visible browser, login manually)
- Accessibility-based selectors are more stable than visual detection
- Session cookies persist throughout the interaction

**Official Package:** [@playwright/mcp](https://www.npmjs.com/package/@playwright/mcp)
**GitHub:** [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)

---

## The MCP Cycle

When Claude uses Playwright MCP, it follows a navigate-observe-decide-act loop:

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

---

## Quick Setup

### Method 1: Claude Code CLI (Recommended)

```bash
# Add Playwright MCP to current project
claude mcp add playwright -- npx @playwright/mcp@latest
```

This persists configuration to `~/.claude.json` for the current directory.

### Method 2: Project-Level Config

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

### Method 3: Global User Config

Add to `~/.claude/settings.json` for all projects:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

---

## Browser Installation

**Important:** Install browsers manually before first use. Claude cannot handle browser installation due to permission requirements.

```bash
# Install Chromium (default browser)
npx playwright install chromium

# Install system dependencies (Linux/WSL)
npx playwright install-deps chromium
```

---

## Configuration Options

### Browser Selection

```json
{
  "args": ["@playwright/mcp@latest", "--browser", "chromium"]
}
```

| Browser | Flag | Notes |
|---------|------|-------|
| Chromium | `--browser chromium` | Default, recommended |
| Chrome | `--browser chrome` | Uses installed Chrome |
| Firefox | `--browser firefox` | Alternative engine |
| WebKit | `--browser webkit` | Safari-like engine |
| Edge | `--browser msedge` | Microsoft Edge |

### Display Modes

```json
// Headed mode (default) - visible browser window
{
  "args": ["@playwright/mcp@latest"]
}

// Headless mode - no GUI, for CI/server
{
  "args": ["@playwright/mcp@latest", "--headless"]
}
```

### Viewport & Device Emulation

```json
// Custom viewport size
{
  "args": ["@playwright/mcp@latest", "--viewport-size", "1280x720"]
}

// Device emulation (iPhone, iPad, etc.)
{
  "args": ["@playwright/mcp@latest", "--device", "iPhone 15"]
}
```

### Session Persistence

> **v0.0.64 change:** In-memory profiles are now the default behavior. The `--isolated` flag is no longer needed — it's the default. Use `--user-data-dir` to opt into persistent profiles.

```json
// Default behavior (v0.0.64+): in-memory, no disk persistence
{
  "args": ["@playwright/mcp@latest"]
}

// Use persistent profile (keeps cookies, localStorage)
{
  "args": ["@playwright/mcp@latest", "--user-data-dir", "/path/to/profile"]
}

// Load saved session state
{
  "args": ["@playwright/mcp@latest", "--storage-state", "/path/to/state.json"]
}
```

### Network & Security

```json
// Block specific origins
{
  "args": ["@playwright/mcp@latest", "--blocked-origins", "ads.example.com;tracking.example.com"]
}

// Allow only specific origins
{
  "args": ["@playwright/mcp@latest", "--allowed-origins", "api.mysite.com;cdn.mysite.com"]
}

// Use proxy
{
  "args": ["@playwright/mcp@latest", "--proxy-server", "http://proxy.example.com:8080"]
}

// Ignore HTTPS errors (self-signed certs)
{
  "args": ["@playwright/mcp@latest", "--ignore-https-errors"]
}
```

### Linux/WSL Specific

```json
// Disable sandbox (required for many Linux/WSL environments)
{
  "args": ["@playwright/mcp@latest", "--no-sandbox"]
}
```

### Debugging & Tracing

```json
// Save trace for debugging
{
  "args": ["@playwright/mcp@latest", "--save-trace"]
}

// Record video
{
  "args": ["@playwright/mcp@latest", "--save-video", "800x600"]
}

// Output directory for artifacts
{
  "args": ["@playwright/mcp@latest", "--output-dir", "./playwright-output"]
}
```

### Timeouts

```json
// Action timeout (default: 5000ms)
{
  "args": ["@playwright/mcp@latest", "--timeout-action", "10000"]
}

// Navigation timeout (default: 60000ms)
{
  "args": ["@playwright/mcp@latest", "--timeout-navigation", "30000"]
}
```

---

## Complete CLI Reference

| Flag | Description |
|------|-------------|
| `--browser <browser>` | Browser: chromium, chrome, firefox, webkit, msedge |
| `--headless` | Run without visible window |
| `--no-sandbox` | Disable process sandboxing (Linux/WSL) |
| `--device <device>` | Device emulation (e.g., "iPhone 15") |
| `--viewport-size <WxH>` | Resolution (e.g., "1280x720") |
| `--user-agent <ua>` | Custom User-Agent string |
| `--user-data-dir <path>` | Persistent browser profile |
| `--storage-state <path>` | Load cookies/localStorage from file |
| `--isolated` | In-memory profile (no disk) |
| `--proxy-server <proxy>` | HTTP/SOCKS proxy |
| `--proxy-bypass <domains>` | Domains to skip proxy |
| `--allowed-origins <origins>` | Semicolon-separated allowlist |
| `--blocked-origins <origins>` | Semicolon-separated blocklist |
| `--ignore-https-errors` | Skip certificate validation |
| `--block-service-workers` | Disable service workers |
| `--timeout-action <ms>` | Action timeout (default: 5000) |
| `--timeout-navigation <ms>` | Navigation timeout (default: 60000) |
| `--output-dir <path>` | Directory for generated files |
| `--save-trace` | Record Playwright trace |
| `--save-video <WxH>` | Record video at resolution |
| `--caps <caps>` | Capabilities: vision, pdf, testing, tracing |
| `--init-script <path>` | JavaScript files to inject |
| `--init-page <path>` | TypeScript files for page setup |
| `--executable-path <path>` | Custom browser executable |
| `--cdp-endpoint <url>` | Connect to existing browser via CDP |

---

## Available Tools

When Playwright MCP is active, Claude has access to these browser automation tools:

### Navigation
| Tool | Description |
|------|-------------|
| `browser_navigate` | Go to a URL |
| `browser_navigate_back` | Go back in history |
| `browser_navigate_forward` | Go forward in history |

### Interaction
| Tool | Description |
|------|-------------|
| `browser_click` | Click an element |
| `browser_type` | Type text into an input |
| `browser_fill_form` | Fill multiple form fields |
| `browser_select_option` | Select dropdown option |
| `browser_drag` | Drag and drop |
| `browser_hover` | Hover over element |
| `browser_press_key` | Press keyboard key |
| `browser_file_upload` | Upload files |

### Inspection
| Tool | Description |
|------|-------------|
| `browser_snapshot` | Get accessibility tree (preferred) |
| `browser_take_screenshot` | Capture visual screenshot |
| `browser_console_messages` | Get console logs |
| `browser_network_requests` | View network activity |
| `browser_evaluate` | Run JavaScript on page |

### Tab Management
| Tool | Description |
|------|-------------|
| `browser_tabs` | List, create, close, select tabs |

### Automation
| Tool | Description |
|------|-------------|
| `browser_run_code` | Run Playwright code snippets — execute arbitrary Playwright JavaScript |

### Control
| Tool | Description |
|------|-------------|
| `browser_wait_for` | Wait for text/element/time |
| `browser_resize` | Change browser size |
| `browser_close` | Close the browser |
| `browser_install` | Install browser (first-time setup) |
| `browser_handle_dialog` | Accept/dismiss browser dialogs (alerts, confirms, prompts) |

---

## Usage Patterns

### Basic Web Interaction

```
Navigate to example.com and take a screenshot
```

```
Use playwright mcp to open https://localhost:3000
```

**Tip:** Say "playwright mcp" explicitly the first time to ensure Claude uses the MCP tools instead of bash commands.

### Authentication Workflow

Since Playwright runs a visible browser:

1. Ask Claude: "Open the login page at example.com/login"
2. Manually enter your credentials in the visible browser window
3. Tell Claude: "I've logged in, now navigate to the dashboard"
4. Session cookies persist for the remainder of the session

#### Persisting Auth State

For repeated testing, save auth state:

```typescript
// In a setup test
await page.context().storageState({ path: 'playwright/.auth/user.json' });
```

Then tell Claude:
```
Use the saved auth state from playwright/.auth/user.json
```

### Form Testing

```
Fill out the contact form with:
- Name: Test User
- Email: test@example.com
- Message: Hello world
Then submit and check for success message
```

### Mobile Testing

```
Resize the browser to mobile width (375px) and take a screenshot of the homepage
```

### Debugging Web Apps

```
Navigate to localhost:3000, check the console for errors, and show me any network request failures
```

### Workflow Pattern: Exploratory Testing

**Prompt:**
```
Navigate to http://localhost:3000 and explore the checkout flow.
Try to find bugs, edge cases, or confusing UX.
Take screenshots of any issues you find.
```

Claude will navigate to the app, explore like a real user, try edge cases (empty cart, invalid input), and report issues with evidence.

### Workflow Pattern: Visual Verification

**Prompt:**
```
Navigate to http://localhost:3000/dashboard and verify:
1. The header shows the user's name
2. The stats cards show numbers (not loading spinners)
3. The sidebar has 5 menu items
4. No console errors
```

Claude will navigate, snapshot, verify each item, and report pass/fail with details.

### Workflow Pattern: Test Generation

**Prompt:**
```
Navigate to http://localhost:3000/login and understand the login flow.
Then write a Playwright test that verifies:
- Valid login succeeds
- Invalid password shows error
- Empty fields show validation
```

Claude will explore the login page, test different scenarios, and generate test code based on observations.

### Workflow Pattern: Failure Investigation

**Prompt:**
```
A test is failing with "element not found: [data-testid='submit']".
Navigate to http://localhost:3000/checkout and investigate.
Find where the submit button is and why the selector might fail.
```

Claude will navigate, search for submit-related elements, compare actual DOM to expected selector, and suggest fixes.

### Workflow Pattern: Competitor Analysis

**Prompt:**
```
Navigate to https://competitor.com/pricing and extract:
1. Pricing tiers and costs
2. Feature list for each tier
3. Any promotional offers
Take screenshots for reference.
```

Claude will navigate, extract structured data, save screenshots, and summarize findings.

---

## Example Configurations

### Development (Headed + Persistent Profile)

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y", "@playwright/mcp@latest",
        "--user-data-dir", "~/.playwright-profile"
      ]
    }
  }
}
```

### CI/Headless Testing

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y", "@playwright/mcp@latest",
        "--headless",
        "--no-sandbox",
        "--save-trace",
        "--output-dir", "./test-artifacts"
      ]
    }
  }
}
```

### WSL2 (Linux) Setup

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y", "@playwright/mcp@latest",
        "--no-sandbox"
      ]
    }
  }
}
```

### Secure Testing (Restricted Network)

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y", "@playwright/mcp@latest",
        "--blocked-origins", "analytics.google.com;facebook.com",
        "--block-service-workers"
      ]
    }
  }
}
```

See [examples/mcp.json.template](./examples/mcp.json.template) for platform-specific variants.

---

## Frontend Development Workflow

Playwright MCP enables a powerful frontend development and testing workflow:

### 1. Visual Verification

```
Navigate to localhost:3000/dashboard and describe what you see on the page
```

Claude uses accessibility snapshots to understand the page semantically.

### 2. Interactive Debugging

```
Click the "Add Item" button and check if the modal appears correctly
```

### 3. Responsive Testing

```
Take screenshots at mobile (375px), tablet (768px), and desktop (1280px) widths
```

### 4. Form Validation Testing

```
Try submitting the form with an invalid email and capture the error message
```

### 5. State Verification

```
After clicking submit, wait for the success message and verify the item appears in the list
```

### 6. Console Error Monitoring

```
Navigate through the app and report any console errors or warnings
```

---

## When to Use MCP vs Alternatives

| Aspect | MCP | CLI | Scripted Tests |
|--------|-----|-----|---------------|
| **Best for** | Interactive exploration, visual bugs, competitor analysis | Scripted automation, CI, batch jobs | Regression, CI/CD pipelines |
| **Tokens per flow** | ~3,330 | ~890 | N/A (no AI tokens) |
| **Setup** | `.mcp.json` config | `npm i -g @anthropic-ai/playwright-cli` + `playwright-cli install` | `npm init playwright@latest` |
| **Deterministic** | No (AI-driven) | Partially (AI interprets shell output) | Yes |
| **Catches** | What Claude notices | What Claude notices | Only what you assert |

**Good uses for MCP:**
- Visual verification and exploratory testing
- Competitor analysis and data extraction
- Understanding unfamiliar UIs
- Debugging test failures interactively
- Generating test code from observations

**Use scripted tests instead for:**
- Regression testing in CI/CD
- Repetitive checks that run every commit
- Deterministic pass/fail assertions

**Use Playwright CLI instead for:**
- Token-sensitive CI workflows (2-4x fewer tokens)
- Batch automation scripts

See [BROWSER_AUTOMATION_LANDSCAPE_2026.md](../../../templates/testing/BROWSER_AUTOMATION_LANDSCAPE_2026.md) for full comparison.

---

## Troubleshooting

### Browser not installed

```bash
# Install browser manually
npx playwright install chromium
npx playwright install-deps chromium  # Linux only
```

Or use the MCP tool:
```
Use browser_install to install the required browser
```

### Sandbox errors (Linux/WSL)

Add `--no-sandbox` to your configuration:

```json
{
  "args": ["-y", "@playwright/mcp@latest", "--no-sandbox"]
}
```

### Claude uses bash instead of Playwright

Explicitly mention "playwright mcp" in your first request:

```
Use playwright mcp to navigate to example.com
```

### Slow npx startup

The `npx -y` approach checks npm registry each time. For faster startup:

```bash
# Install globally (one time)
npm install -g @playwright/mcp

# Use in config
{
  "command": "playwright-mcp",
  "args": []
}
```

### Slow performance / high token usage

**Option 1: Playwright CLI (recommended for token savings)**

The new Playwright CLI uses 2-4x fewer tokens than MCP. See [BROWSER_AUTOMATION_LANDSCAPE_2026.md](../../../templates/testing/BROWSER_AUTOMATION_LANDSCAPE_2026.md#3-playwright-cli-vs-mcp-comparison) for setup and comparison.

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

### Model selection for MCP workflows

Use **Haiku 4.5** for MCP-driven QA to reduce costs — same browser automation accuracy as Sonnet (61% OSWorld) at 3x lower cost. See [COST_OPTIMIZATION_GUIDE.md](../../../templates/testing/COST_OPTIMIZATION_GUIDE.md#model-selection-for-browser-automation) for full analysis.

### Connection issues

Verify MCP is configured:

```bash
claude mcp list
claude mcp get playwright
```

---

## CI Integration

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

See [Alex Op's AI QA Engineer](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/) for a full implementation. For CI workflow templates, see [templates/ci/](../../../templates/ci/README.md).

---

## Security Considerations

**See also**: [MCP Safety Guide](../MCP-SAFETY.md) for general MCP security (version pinning, supply chain, prompt injection).

- **MCP servers run with your user permissions** - they can access anything you can
- **Use `--blocked-origins`** to prevent requests to sensitive domains
- **Use `--isolated` mode** for testing to avoid persisting credentials
- **Playwright MCP is more secure than direct bash access** because you define the scope
- **Version control `.mcp.json`** for reproducible, auditable configurations

---

## Token Cost

Playwright MCP adds tool definitions to Claude's context. This is generally smaller than other MCPs (like Notion's ~30k tokens) but still adds overhead.

**Strategy:**
- Only enable in projects that need browser automation
- Use project-level `.mcp.json` instead of global config
- Consider a plugin to toggle on/off (see [Claude Code Config](../../reference/CLAUDE-CODE-CONFIG.md#plugins))

---

## Claude Code Chrome (Beta)

Claude Code now includes a built-in browser (Claude Code Chrome) that provides browser automation without MCP setup.

**Capabilities:**
- Direct browser control without MCP overhead
- No `.mcp.json` configuration needed
- Same automation capabilities

**Critical limitation:**
- **Does NOT work on WSL2** — our primary development environment
- macOS and native Linux only

**Recommendation:** Continue using Playwright MCP for WSL2 development. Monitor Claude Code Chrome for WSL2 support updates.

---

## See Also

- [BROWSER_AUTOMATION_LANDSCAPE_2026.md](../../../templates/testing/BROWSER_AUTOMATION_LANDSCAPE_2026.md) — Full landscape analysis, CLI vs MCP, model selection
- [COST_OPTIMIZATION_GUIDE.md](../../../templates/testing/COST_OPTIMIZATION_GUIDE.md) — Model pricing and optimization
- [PLAYWRIGHT_CLAUDE_GUIDE.md](../../../templates/testing/PLAYWRIGHT_CLAUDE_GUIDE.md) — Testing patterns (scripted + MCP)
- [Claude Code Config Reference](../../reference/CLAUDE-CODE-CONFIG.md) — MCP management, plugins, hooks
- [Claude Code Setup Guide](../../setup-guides/CLAUDE-CODE-SETUP.md) — Basic Claude Code setup
- [Daily Workflow](../../setup-guides/DAILY-WORKFLOW.md) — Development workflow patterns

## External Resources

- [Microsoft Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Simon Willison's Playwright MCP Guide](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [TestLeaf 2026 Guide](https://www.testleaf.com/blog/playwright-mcp-ai-test-automation-2026/)
- [Building AI QA Engineer](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/)

---

Last Updated: February 2026
