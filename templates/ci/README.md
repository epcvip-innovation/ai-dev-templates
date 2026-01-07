# CI Templates

GitHub Actions workflows for AI-assisted development using official Anthropic actions.

## Contents

| File | Purpose |
|------|---------|
| [claude-qa-workflow.yml.template](./claude-qa-workflow.yml.template) | Browser-based QA with Claude + Playwright MCP |
| [security-review.yml.template](./security-review.yml.template) | Automated security scanning on all PRs |
| [qa-persona.md.template](./qa-persona.md.template) | QA engineer persona prompt |

## Official Actions

These templates use Anthropic's official GitHub Actions:

| Action | Purpose | Speed |
|--------|---------|-------|
| [claude-code-action@v1](https://github.com/anthropics/claude-code-action) | General PR automation, browser testing | ~7 min |
| [claude-code-security-review](https://github.com/anthropics/claude-code-security-review) | Security vulnerability scanning | ~2 min |

## Quick Start

### Option 1: Security Review Only (Recommended Start)

Lightweight security scanning on every PR:

```bash
cp security-review.yml.template .github/workflows/security.yml
```

Add `ANTHROPIC_API_KEY` secret to your repository.

### Option 2: Full QA with Browser

Browser-based testing triggered by file changes or label:

```bash
cp claude-qa-workflow.yml.template .github/workflows/qa.yml
```

Customize:
1. File paths to trigger on
2. Server start command
3. Test instructions in the prompt

## How It Works

### Security Review
```
PR opened → Action runs → Scans diff → Posts findings as line comments
```

### QA Review
```
Files changed → Server starts → Claude navigates app → Posts report as PR comment
```

## Path-Specific Triggering

Run QA only when relevant files change:

```yaml
on:
  pull_request:
    paths:
      - 'src/checkout/**'
      - 'server/api/payments/**'
```

This pattern is useful for:
- Large monorepos
- Specific feature areas
- Cost control (API usage)

## Configuration

### MCP for Browser Automation

The QA workflow uses Playwright MCP for browser control:

```yaml
claude_args: |
  --mcp-config '{"mcpServers":{"playwright":{"command":"npx","args":["@playwright/mcp@latest","--headless"]}}}'
  --allowedTools "mcp__playwright__browser_navigate,mcp__playwright__browser_click,..."
```

Key points:
- `--headless` required for CI (no display)
- `--allowedTools` restricts Claude to browser-only (black-box testing)

### Available Browser Tools

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_click` | Click elements |
| `browser_type` | Type text |
| `browser_snapshot` | Get page state (accessibility tree) |
| `browser_take_screenshot` | Capture visual evidence |
| `browser_resize` | Test responsive layouts |
| `browser_console_messages` | Check for errors |

## Example Output

### Security Review
```
## Security Review

⚠️ **1 issue found**

### server/api/auth.ts:45
**Potential SQL Injection** (High)
User input passed directly to query without sanitization.
```

### QA Review
```
## QA Verification Report

**Verdict**: PASS WITH NOTES

### Tested
- [x] Login flow works
- [x] Dashboard loads
- [ ] Mobile menu - overlapping elements

### Issues Found
**Mobile nav overlap** (Medium)
On 375x667 viewport, hamburger menu overlaps logo.
[Screenshot attached]
```

## Cost Considerations

| Workflow | Triggers | Typical Cost |
|----------|----------|--------------|
| Security Review | Every PR | ~$0.10-0.30 |
| QA Review | Path-specific | ~$0.50-1.50 |
| QA Review | Label-triggered | On-demand |

Tips:
- Use path-specific triggers for QA
- Use labels for manual trigger
- Security review is cheap enough to run always

## Security Notes

From [Anthropic's security guidance](https://www.stepsecurity.io/blog/anthropics-claude-code-action-security-how-to-secure-claude-code-in-github-actions-with-harden-runner):

1. **Trusted PRs only**: Actions are not hardened against prompt injection
2. **External contributors**: Enable "Require approval for all external contributors"
3. **Secrets**: Never expose API keys in logs
4. **Permissions**: Use least-privilege (`contents: read`, `pull-requests: write`)

## Based On

- [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) - Official action
- [anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review) - Security action
- [Alex Op: AI QA Engineer](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/) - Implementation pattern
- [Claude Code GitHub Actions Docs](https://code.claude.com/docs/en/github-actions) - Official documentation

## See Also

- [Testing Templates](../testing/README.md) - E2E testing patterns
- [MCP Workflow Guide](../testing/MCP_WORKFLOW_GUIDE.md) - Claude + browser automation
- [Research Archive](../testing/RESEARCH_ARCHIVE.md) - 2026 research findings
