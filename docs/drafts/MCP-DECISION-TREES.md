# MCP Server Decision Trees (DRAFT)

**Status**: In Progress
**Source**: Patterns from [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery)
**Target**: `docs/reference/MCP-GUIDE.md` or `templates/mcp/`

---

## Overview

Decision trees for choosing the right MCP server for different use cases.

---

## Browser Automation Decision Tree

```
Need browser automation?
│
├─ Public/test scenarios (no login required)
│  └─ Use: Playwright MCP
│     - Official Anthropic support
│     - Reliable, uses accessibility trees
│     - Fresh browser context each time
│     - Best for: Testing, scraping public sites
│
├─ Your authenticated sessions (need your logins)
│  └─ Use: Browser MCP
│     - Uses your actual Chrome profile
│     - Accesses Gmail, GitHub with your sessions
│     - Bypasses bot detection (real browser)
│     - Best for: Tasks needing your accounts
│
└─ Complex AI-driven workflows
   └─ Use: Browser Use
      - Cloud-based profiles
      - Natural language task description
      - 85.8% benchmark score (WebVoyager)
      - Best for: Complex multi-step automation
```

### Quick Reference

| Scenario | MCP Server | Why |
|----------|------------|-----|
| E2E testing | Playwright | Fresh context, accessibility tree |
| Scrape public site | Playwright | Reliable, no auth needed |
| Check your Gmail | Browser MCP | Uses your Chrome session |
| Book appointment | Browser Use | Complex multi-step flow |
| Fill authenticated form | Browser MCP | Your logged-in session |
| Screenshot comparison | Playwright | Consistent environments |

---

## Database Access Decision Tree

```
Need database access?
│
├─ Read-only queries (analytics, exploration)
│  └─ Use: Read-only connection string
│     - Separate read replica if available
│     - Query validation hooks recommended
│
├─ Write operations needed
│  └─ Use: Full connection with safeguards
│     - Transaction wrappers
│     - Dangerous command hooks
│     - Audit logging
│
└─ Schema changes needed
   └─ Use: Migration tool MCP (if available)
      - Or manual review process
      - Never auto-apply DDL
```

---

## Documentation/Context Decision Tree

```
Need up-to-date library docs?
│
├─ Common libraries (React, Next.js, etc.)
│  └─ Use: Context7 MCP
│     - Live documentation
│     - Version-aware
│     - Replaces outdated training data
│
├─ Internal documentation
│  └─ Use: File-based context
│     - CLAUDE.md hub-and-spoke
│     - Project-specific docs
│
└─ API documentation
   └─ Use: OpenAPI/Swagger MCP (if available)
      - Or WebFetch with API docs URL
```

---

## TODO: Validate These Patterns

- [ ] Test Playwright MCP vs Browser MCP for real scenarios
- [ ] Evaluate Context7 token usage
- [ ] Document Browser Use setup complexity
- [ ] Add cost considerations (cloud vs local)

---

## Sources

- TheDecipherist guide: Browser automation decision tree
- Internal experience: Database access patterns
- Anthropic docs: Playwright MCP official guide

---

**Last Updated**: 2026-01-15
**Status**: Draft - needs validation before promotion
