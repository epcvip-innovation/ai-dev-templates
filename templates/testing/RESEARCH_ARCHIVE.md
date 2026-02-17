# Playwright + Claude Code Research Archive

Curated findings from January 2026 research on AI-driven browser automation, testing patterns, and competitor analysis.

## Key Sources

### AI-Driven Testing

#### TestLeaf: Playwright MCP AI Test Automation 2026
**URL:** https://www.testleaf.com/blog/playwright-mcp-ai-test-automation-2026/

**Key Insights:**
- "2026 is the year testers move from 'writing scripts' to orchestrating AI-powered automation workflows"
- Self-healing test suites that adapt to UI changes
- Multi-client browser sessions for complex scenarios
- AI can handle dynamic content better than static selectors

**Relevance:** Validates the shift from pure scripted tests to AI-assisted testing

---

### Claude Code + Playwright Integration

#### Alex Op: Building AI QA Engineer
**URL:** https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/

**Key Insights:**
- GitHub Action triggered by PR label (`qa-verify`)
- QA persona prompting improves Claude's testing approach
- Browser-only tool restriction for black-box testing
- Screenshots as evidence for findings
- Structured output format (Verified/Issues/Recommendations)

**Implementation Pattern:**
```yaml
# Triggered on label
on:
  pull_request:
    types: [labeled]

jobs:
  qa-review:
    if: github.event.label.name == 'qa-verify'
```

**Relevance:** Direct blueprint for CI Claude QA implementation

---

#### Simon Willison: Playwright MCP with Claude Code
**URL:** https://til.simonwillison.net/claude-code/playwright-mcp-claude-code

**Key Insights:**
- Setup command: `claude mcp add playwright npx '@playwright/mcp@latest'`
- Browser window is visible - enables manual authentication
- 25+ browser control tools available
- Accessibility tree + screenshot for each snapshot
- Element references (ref IDs) for precise interactions

**Tool Categories:**
| Category | Tools |
|----------|-------|
| Navigation | `browser_navigate`, `browser_navigate_back`, `browser_tabs` |
| Observation | `browser_snapshot`, `browser_take_screenshot`, `browser_console_messages` |
| Interaction | `browser_click`, `browser_type`, `browser_fill_form` |
| State | `browser_network_requests`, `browser_evaluate` |

**Relevance:** Practical setup guide and tool reference

---

### Competitor Analysis & Web Scraping

#### Browse AI
**URL:** https://www.browse.ai/

**Features:**
- No-code competitor monitoring
- Scheduled scraping (daily/weekly)
- Change detection and alerts
- Pricing: $39-249/month

**Use Case:** Ongoing automated monitoring at scale

---

#### Firecrawl
**URL:** https://www.firecrawl.dev/

**Features:**
- Web scraping optimized for AI/LLM consumption
- Structured data extraction
- Clean markdown output
- Usage-based pricing

**Use Case:** Converting web pages to AI-friendly formats

---

#### Apify: Best AI Web Scrapers
**URL:** https://blog.apify.com/best-ai-web-scrapers/

**Key Insights:**
- 30-40% time reduction vs traditional methods
- AI-powered anti-detection capabilities
- Natural language instructions for scraping
- Handles dynamic JavaScript-rendered content

**Relevance:** Benchmark for what's possible with AI scraping

---

### Official Anthropic GitHub Actions (January 2026)

#### anthropics/claude-code-action
**URL:** https://github.com/anthropics/claude-code-action

**Status:** Official, Production-Ready (launched September 29, 2025)
**Stars:** 4.9k+ | **Forks:** 1.4k+

**Key Features:**
- General-purpose PR automation and code changes
- MCP server support via `--mcp-config` in `claude_args`
- Playwright MCP works with `--headless` flag for CI
- Tool restrictions via `--allowedTools` for black-box testing
- Automatic PR commenting with findings
- Multiple auth providers (Anthropic, Bedrock, Vertex AI, Foundry)

**Configuration Example:**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Test the checkout flow"
    claude_args: |
      --mcp-config '{"mcpServers":{"playwright":{"command":"npx","args":["@playwright/mcp@latest","--headless"]}}}'
      --allowedTools "mcp__playwright__browser_navigate,mcp__playwright__browser_click,..."
```

**Relevance:** This is THE official way to run Claude QA in CI. Supersedes CLI-based approaches.

---

#### anthropics/claude-code-security-review
**URL:** https://github.com/anthropics/claude-code-security-review

**Status:** Official, Production-Ready

**Key Features:**
- Automatic security scanning on every PR
- Posts findings as line comments on specific code
- Language agnostic
- False positive filtering (excludes DoS, rate limiting noise)
- Diff-aware (only scans changed files)

**What It Checks:**
- Injection attacks (SQL, command, XSS, XXE, NoSQL)
- Authentication & authorization issues
- Hardcoded secrets and sensitive data
- Cryptographic weaknesses
- Business logic flaws (race conditions, TOCTOU)
- Input validation gaps

**Simple Setup:**
```yaml
- uses: anthropics/claude-code-security-review@main
  with:
    claude-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Relevance:** Zero-config security scanning. Should be on every repo.

---

#### Claude Code GitHub Actions Documentation
**URL:** https://code.claude.com/docs/en/github-actions

**Key Topics:**
- Setup via `/install-github-app` command
- Tag mode vs Agent mode
- Solutions guide with working examples
- Security best practices

---

### Additional Official Resources

#### Microsoft Playwright MCP
**URL:** https://github.com/microsoft/playwright-mcp

**Status:** Official Microsoft implementation
**Features:**
- Full browser control via MCP protocol
- Chromium, Firefox, WebKit support
- Accessibility tree snapshots

---

#### ExecuteAutomation MCP
**URL:** https://github.com/executeautomation/mcp-playwright

**Status:** Community alternative
**Features:**
- Additional automation helpers
- Extended tool set

---

#### Playwright Documentation
**URL:** https://playwright.dev/docs/intro

**Key Pages:**
- [Test Fixtures](https://playwright.dev/docs/test-fixtures) - Custom test setup
- [Page Object Model](https://playwright.dev/docs/pom) - Encapsulation pattern
- [Visual Comparisons](https://playwright.dev/docs/test-snapshots) - Screenshot regression
- [Trace Viewer](https://playwright.dev/docs/trace-viewer) - Debugging tool

---

## Key Insights Summary

### 1. Scripts vs MCP: Complementary, Not Competing

| Aspect | Scripted Tests | MCP-Driven |
|--------|---------------|------------|
| Speed | Fast (ms per action) | Slower (AI thinking) |
| Coverage | What you assert | Everything visible |
| Repeatability | 100% deterministic | Variable |
| Best For | CI/CD regression | Exploration, debugging |

**Principle:** Scripts check assertions; MCP sees everything. Use both.

### 2. Personas Improve AI Testing

QA persona prompting (e.g., "You are Quinn, a meticulous QA engineer") improves:
- Thoroughness of exploration
- Quality of issue reports
- Consistency of output format

### 3. Evidence Matters

Always capture screenshots for:
- Bug reports
- Visual verification
- Competitor analysis
- Documentation

### 4. Browser is the New OS

> "The browser is becoming the place where AI work gets done—not just a source of information."

AI is evolving from reading web content to operating within browsers:
- Form filling
- Multi-step workflows
- Visual inspection
- Data extraction

### 5. Hybrid Workflows Win

Best practice workflow:
```
Claude MCP explores → Identifies issues → Writes scripted test → CI runs forever
```

---

## Implementation Patterns

### CI Claude QA (from Alex Op)

**Trigger:** PR label `qa-verify`
**Process:**
1. Start dev server
2. Claude explores with MCP
3. Reports findings as PR comment
4. Screenshots attached as evidence

**Template:** See [`../ci/claude-qa-workflow.yml.template`](../ci/claude-qa-workflow.yml.template)

---

### Competitor Analysis (from research)

**One-time analysis:** Claude MCP + natural language prompts
**Ongoing monitoring:** Browse AI or similar SaaS
**Data extraction:** Firecrawl for AI-friendly output

**Template:** See `COMPETITOR_ANALYSIS.md`

---

### Visual Regression (from Playwright docs)

```typescript
// Baseline comparison
await expect(page).toHaveScreenshot('dashboard.png');

// With tolerance
await expect(page).toHaveScreenshot('chart.png', {
  maxDiffPixels: 100,
});
```

**Template:** See [`examples/visual.spec.ts.template`](./examples/visual.spec.ts.template)

---

## Tools Comparison

| Tool | Best For | Pricing | Notes |
|------|----------|---------|-------|
| **Claude MCP** | Ad-hoc analysis, intelligent exploration | Per-usage | Best for one-time, complex tasks |
| **Browse AI** | Scheduled monitoring | $39-249/mo | No-code, change alerts |
| **Firecrawl** | AI data extraction | Usage-based | Clean markdown output |
| **Bright Data** | Large-scale scraping | Enterprise | Proxy network, CAPTCHA handling |
| **Apify** | Custom scrapers | Usage-based | Actor marketplace |

---

## Research Date

**Compiled:** January 2026
**Last Updated:** January 7, 2026

---

## Further Reading

- [PLAYWRIGHT_CLAUDE_GUIDE.md](./PLAYWRIGHT_CLAUDE_GUIDE.md) - Comprehensive testing guide
- [Playwright MCP Guide](../../docs/mcp/playwright/README.md) - MCP-specific patterns
- [COMPETITOR_ANALYSIS.md](./COMPETITOR_ANALYSIS.md) - Market research automation
