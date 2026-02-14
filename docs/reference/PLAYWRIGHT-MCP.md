# Playwright MCP Setup Guide

[← Back to Main README](../../README.md) | [Claude Code Config →](./CLAUDE-CODE-CONFIG.md)

**Last Updated**: February 2026 | **MCP Version**: v0.0.64

Comprehensive guide to setting up Playwright MCP for browser automation with Claude Code.

> **February 2026:** MCP v0.0.64 uses in-memory profiles by default. New tools: `browser_run_code`, `browser_handle_dialog`, `browser_fill_form`. See [BROWSER_AUTOMATION_LANDSCAPE_2026.md](../../templates/testing/BROWSER_AUTOMATION_LANDSCAPE_2026.md) for alternatives (CLI, Chrome beta).

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

### Connection issues

Verify MCP is configured:

```bash
claude mcp list
claude mcp get playwright
```

---

## Security Considerations

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
- Consider a plugin to toggle on/off (see [Claude Code Config](./CLAUDE-CODE-CONFIG.md#plugins))

---

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

- [BROWSER_AUTOMATION_LANDSCAPE_2026.md](../../templates/testing/BROWSER_AUTOMATION_LANDSCAPE_2026.md) — Full landscape analysis, CLI vs MCP, model selection
- [AUDIT_2026-02.md](../../templates/testing/AUDIT_2026-02.md) — Cross-repo Playwright audit
- [Claude Code Config Reference](./CLAUDE-CODE-CONFIG.md) — MCP management, plugins, hooks
- [Claude Code Setup Guide](../setup-guides/CLAUDE-CODE-SETUP.md) — Basic Claude Code setup
- [Daily Workflow](../setup-guides/DAILY-WORKFLOW.md) — Development workflow patterns

## External Resources

- [Microsoft Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Simon Willison's Playwright MCP Guide](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)

---

Last Updated: February 2026
