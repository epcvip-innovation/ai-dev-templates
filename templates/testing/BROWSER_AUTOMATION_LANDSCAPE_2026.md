# Browser Automation Landscape — February 2026

**Date:** 2026-02-13
**Purpose:** Comprehensive reference for browser automation approaches, model selection, and platform compatibility in the Claude Code ecosystem.

---

## 1. The 5 Browser Automation Approaches

### Overview

| Approach | Speed | Cost | Platform | Status |
|----------|-------|------|----------|--------|
| **Playwright MCP** | Medium | Low (tool overhead) | All | Production |
| **Playwright CLI** | Fast (2.4-3.7x less tokens) | Lowest | All (shell access) | Tested — adopt for CI |
| **Claude Code Chrome** | Fast (no MCP overhead) | Low | macOS, Linux (**NOT WSL2**) | Beta |
| **Scripted Playwright Tests** | Fastest | Free | All | Production |
| **Playwright Agents** | Slow (AI reasoning) | Medium | All | Experimental |

---

### Approach 1: Playwright MCP (Production)

**What it is:** Microsoft's official MCP server (`@playwright/mcp`) that gives Claude 28+ browser control tools via the Model Context Protocol.

**Setup:**
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

**Capabilities:**
- Navigate, click, type, screenshot, evaluate JS
- Accessibility snapshot (semantic understanding of pages)
- Network request inspection, console message capture
- Tab management, file upload, dialog handling
- Video recording (`--save-video`)

**Limitations:**
- Tool definitions add ~5K tokens to context per session
- Each tool call adds overhead (protocol marshaling)
- ~114K tokens per typical automation task
- Requires npx (Node.js) installed

**When to use:**
- Interactive exploration and debugging
- Visual bug hunting
- Competitor analysis
- Test generation (explore → write tests)

**Current version:** v0.0.64
- In-memory profiles by default (`--isolated` is now the default behavior)
- New tools: `browser_run_code`, `browser_handle_dialog`, `browser_fill_form`, `browser_install`

---

### Approach 2: Playwright CLI (Tested)

**What it is:** `@playwright/cli` — a command-line interface for Playwright that Claude invokes via shell commands instead of MCP tools. Reduces token usage by saving output to files instead of inline.

**Setup:**
```bash
npm install -g @playwright/cli@latest
playwright-cli install    # Initialize workspace, detect browser
```

**Capabilities:**
- Same underlying Playwright engine
- All browser automation features (navigate, click, type, screenshot, console, network)
- Snapshots saved to `.playwright-cli/` directory as YAML files
- Storage management (cookies, localStorage, sessionStorage)
- Network route mocking via CLI
- Tracing and video recording
- `keyboard.type()` for non-form-input typing (games, rich editors)

**Limitations:**
- Requires shell access (Bash tool)
- No snapshot diffing (MCP marks `<changed>`/`[unchanged]`)
- `.playwright-cli/` directory accumulates files (no auto-cleanup)
- Extra Read tool call needed to inspect snapshots
- No `--no-sandbox` flag (not needed — handles WSL2 sandboxing internally)

**Token comparison (verified 2026-02-13 against fwaptile-wordle):**

| Metric | MCP | CLI |
|--------|-----|-----|
| Tokens per navigate+click+type+console flow | ~3,330 | ~890 |
| Reduction (lazy reads) | — | **3.7x fewer tokens** |
| Reduction (all files read) | — | **2.4x fewer tokens** |
| Architecture | MCP protocol + 28 tools | Shell commands via Bash |
| Console output (chatty app) | 92 lines inline (~1,200 tokens) | File ref (3 lines, ~12 tokens) |

**When to use:**
- CI/CD pipelines where token cost scales with volume
- Chatty apps (WebSocket timers, frequent console output)
- Typing into non-form elements (games, custom inputs)
- Batch automation workflows

**When NOT to use (prefer MCP):**
- Interactive exploration and debugging (snapshot diffs help)
- Form-heavy apps (`browser_fill_form` is convenient)
- First-time investigation where you need to see every page state

**Status:** Tested. Adopt for CI and chatty-app workflows. MCP remains the default for interactive exploration.

**Evaluation details:** See [PLAYWRIGHT_CLI_EVALUATION.md](PLAYWRIGHT_CLI_EVALUATION.md).

---

### Approach 3: Claude Code Chrome (Beta)

**What it is:** Native browser integration built into Claude Code — no MCP server needed. Claude controls a browser directly.

**Setup:** Built into Claude Code (no additional config).

**Capabilities:**
- Direct browser control without MCP overhead
- Same automation capabilities as MCP
- Potentially faster (no protocol marshaling)

**Limitations:**
- **Does NOT work on WSL2** — this is our primary dev environment
- macOS and native Linux only
- Beta — may have stability issues
- No video recording or trace capture

**When to use:**
- macOS or native Linux development
- Quick browser tasks without MCP setup
- When MCP overhead isn't desired

**Platform compatibility:**

| Platform | Supported |
|----------|-----------|
| macOS | Yes |
| Native Linux | Yes |
| **WSL2** | **NO** |
| CI (Ubuntu) | No |

**Status:** Beta. Document capabilities but **do not adopt** until WSL2 support lands. Monitor for updates.

---

### Approach 4: Scripted Playwright Tests (Production)

**What it is:** Traditional Playwright test scripts (`@playwright/test`) that run deterministically without AI involvement.

**Setup:**
```bash
npm init playwright@latest
npx playwright test
```

**Capabilities:**
- Deterministic assertions
- Visual regression (screenshot comparison)
- Parallel execution across browsers
- CI/CD integration
- Traces, videos, reports

**Limitations:**
- Only catches what you explicitly assert
- Requires human-written test code
- Can't discover unknown issues

**When to use:**
- CI/CD pipelines (always)
- Regression testing
- Visual regression baselines
- Performance benchmarks

**Status:** Production. This is the foundation — every repo should have scripted tests.

---

### Approach 5: Playwright Agents (Experimental)

**What it is:** AI-powered agents built into Playwright (v1.56+) that can plan, generate, and heal tests automatically.

**Three agents:**

| Agent | Purpose |
|-------|---------|
| **Planner** | Explores app, produces test plan markdown |
| **Generator** | Converts plan to executable Playwright tests |
| **Healer** | Fixes broken selectors when UI changes |

**Setup:**
```bash
npx playwright init-agents --loop=vscode
```

**Limitations:**
- Experimental — not production-ready
- Unpredictable test quality
- Slow (AI reasoning at each step)
- 6-12 months from stable release

**When to use:** Don't — yet. Track progress, revisit when stable.

**Status:** Experimental. Document for awareness, do not adopt. Revisit Q3 2026.

---

## 2. Model Selection Guide for Browser Automation

### Verified Benchmarks (February 2026)

| Model | Speed (t/s) | OSWorld | Cost/MTok (in/out) | Best For | API |
|-------|:-----------:|:-------:|:-------------------:|----------|:---:|
| **Haiku 4.5** | 105 | 61% | $1 / $5 | CI QA, high-volume automation | Yes |
| **Sonnet 4.5** | 70 | 61% | $3 / $15 | Balanced default | Yes |
| **Opus 4.6** | 72 | — | $5 / $25 | Complex reasoning tasks | Yes |
| **Opus 4.6 Fast** | 178 | Same as Opus | $30 / $150 | Speed-critical, interactive | Yes |
| **Codex Spark** | 1000+ (claimed) | 58.4%* | TBA | N/A yet | No |

*\*Codex Spark's 58.4% is Terminal-Bench, not OSWorld — not directly comparable to Claude's OSWorld scores.*

### Key Findings

**Haiku 4.5 is the sleeper pick for browser automation:**
- Same OSWorld accuracy as Sonnet 4.5 (61%)
- 1.5x faster (105 vs 70 t/s)
- 3x cheaper ($1/$5 vs $3/$15)
- Best value for CI QA, smoke tests, and high-volume automation

**Opus 4.6 Fast Mode analysis:**
- 2.5x faster than standard Opus (178 vs 72 t/s)
- **6x more expensive** ($30/$150 vs $5/$25)
- Same accuracy (same model, faster inference)
- Only worth it for: interactive debugging, time-sensitive workflows, demos

**Codex Spark (GPT 5.3) — do not recommend yet:**
- Claims 1000+ t/s but unverified independently
- No API access (ChatGPT Pro only)
- Terminal-Bench 58.4% — lower than Claude's OSWorld numbers and not comparable
- Reported Playwright MCP issues (tool calling reliability)
- 25% accuracy drop from GPT-5 base → Codex Spark (speed optimized)
- Monitor, do not adopt

### Recommended Model by Use Case

| Use Case | Model | Rationale |
|----------|-------|-----------|
| **CI QA automation** | Haiku 4.5 | Same accuracy, 3x cheaper |
| **Interactive debugging** | Opus 4.6 or Sonnet 4.5 | Better reasoning for complex issues |
| **Speed-critical demos** | Opus 4.6 Fast | 2.5x speed, cost justified by time saved |
| **Competitor analysis** | Sonnet 4.5 | Good balance of reasoning + cost |
| **Bulk smoke tests** | Haiku 4.5 | Volume × cost optimization |
| **Complex multi-step flows** | Opus 4.6 | Fewer turns = potentially cost-competitive |

### Cost Comparison: Real Scenario

**Scenario:** 50 UI PRs/month, AI QA on each

| Model | Per-Run Cost | Monthly (50 PRs) | Notes |
|-------|:-----------:|:----------------:|-------|
| Haiku 4.5 | ~$0.20 | **$10** | Best value |
| Sonnet 4.5 | ~$0.60 | $30 | Current baseline |
| Opus 4.6 | ~$0.80 | $40 | Fewer turns may reduce this |
| Opus 4.6 Fast | ~$4.80 | $240 | Only for speed-critical |

---

## 3. Playwright CLI vs MCP Comparison

*Verified 2026-02-13 against fwaptile-wordle. See [PLAYWRIGHT_CLI_EVALUATION.md](PLAYWRIGHT_CLI_EVALUATION.md) for full methodology.*

| Aspect | MCP | CLI |
|--------|-----|-----|
| **Tokens per task** | ~3,330 (measured) | ~890 (measured, lazy reads) |
| **Token savings** | Baseline | **2.4x-3.7x fewer** (depends on file reads) |
| **Architecture** | MCP protocol, 28+ tool definitions | Shell commands via Bash |
| **Setup** | `.mcp.json` config | `npm i -g @playwright/cli` + `playwright-cli install` |
| **Snapshot delivery** | Inline (always in context) | File on disk (read on demand) |
| **Snapshot diffing** | Yes (`<changed>`, `[unchanged]`) | No (full snapshot each time) |
| **Console output** | All messages inline | File reference (read if needed) |
| **Type into non-inputs** | Fails (`fill()` requires input/textarea) | Works (`keyboard.type()`) |
| **WSL2 sandbox** | Requires `--no-sandbox` flag | Automatic (no flag needed) |
| **Best for** | Interactive exploration, debugging | CI, chatty apps, cost-sensitive |
| **Learning curve** | Low (tool names are intuitive) | Low-medium (CLI syntax is readable) |
| **Maturity** | Production (v0.0.64) | Tested (works, adopt for targeted use) |

### When to Choose Which

**Choose MCP when:**
- Doing interactive exploration or debugging
- Need snapshot diffs to spot changes
- Working with form-heavy apps (`browser_fill_form`)
- Working on competitor analysis
- Generating tests from observation

**Choose CLI when:**
- Token cost is a primary concern (CI/CD)
- App has chatty console output (timers, WebSocket messages)
- Need to type into non-form elements (games, rich editors)
- Running batch automation
- Want simpler WSL2 setup (no `--no-sandbox` needed)

**Current recommendation:** MCP remains the default for interactive work. Adopt CLI for CI pipelines and chatty-app workflows where token savings are significant.

---

## 4. Platform Compatibility Matrix

| Tool | macOS | Native Linux | WSL2 | CI (Ubuntu) | Notes |
|------|:-----:|:------------:|:----:|:-----------:|-------|
| **Playwright MCP** | Yes | Yes | Yes* | Yes** | *`--no-sandbox` required, **`--headless` required |
| **Playwright CLI** | Yes | Yes | Yes | Yes | Auto-handles sandboxing (no flags needed) |
| **Claude Code Chrome** | Yes | Yes | **NO** | No | WSL2 has no display server access |
| **Scripted Tests** | Yes | Yes | Yes* | Yes | *`--no-sandbox` for headed mode |
| **Playwright Agents** | Yes | Yes | Yes* | TBD | *Experimental |

### WSL2-Specific Requirements

All Playwright browser automation in WSL2 requires:
1. `--no-sandbox` flag (Chromium sandbox doesn't work in WSL2)
2. Browser dependencies: `npx playwright install-deps chromium`
3. For headed mode: WSLg must be working (Windows 11 22H2+)

### CI-Specific Requirements

For GitHub Actions / CI environments:
1. `--headless` flag (no display server)
2. `npx playwright install --with-deps` in setup step
3. Upload artifacts on failure for debugging

---

## 5. What's Coming (Track, Don't Adopt)

### Playwright Agents (v1.56+)
- **Status:** Experimental, 6-12 months from production
- **What:** Planner, Generator, Healer agents for automated test creation
- **Track:** Playwright release notes, `playwright.dev/docs/test-agents`
- **Revisit:** Q3 2026

### Stagehand v3
- **What:** AI-native browser automation framework
- **Status:** Active development, growing adoption
- **Differentiator:** Built for AI from the ground up (vs Playwright adding AI later)
- **Track:** GitHub repo and releases

### Chrome DevTools MCP Servers
- **What:** Multiple implementations connecting Chrome DevTools Protocol to MCP
- **Status:** Various maturity levels
- **Note:** Playwright MCP is the recommended approach; DevTools MCP is an alternative

### Playwright CLI Maturity
- **What:** `@playwright/cli` reaching production stability
- **Evaluated:** 2026-02-13 against fwaptile-wordle
- **Result:** Works well. 2.4-3.7x token savings vs MCP. Adopted for CI and chatty-app use cases.
- **Details:** [PLAYWRIGHT_CLI_EVALUATION.md](PLAYWRIGHT_CLI_EVALUATION.md)

---

## Sources

- [Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing) — Model costs
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) — Official MCP server
- [Playwright Documentation](https://playwright.dev/docs/intro) — Core Playwright
- [Playwright Agents](https://playwright.dev/docs/test-agents) — Experimental agents
- [OSWorld Benchmark](https://os-world.github.io/) — Browser automation benchmarks
- [MCP Hidden Costs](https://mariogiancini.com/the-hidden-cost-of-mcp-servers-and-when-theyre-worth-it) — Token overhead analysis

---

## See Also

- [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) — Get started with the 5 approaches covered here
- [MCP_WORKFLOW_GUIDE.md](./MCP_WORKFLOW_GUIDE.md) — Deep dive into MCP patterns and workflows
- [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md) — Cost projections and optimization strategies
- [PLAYWRIGHT_CLI_EVALUATION.md](./PLAYWRIGHT_CLI_EVALUATION.md) — Hands-on CLI vs MCP token measurements

---

*Last Updated: 2026-02-13*
