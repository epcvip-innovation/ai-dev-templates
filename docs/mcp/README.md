# MCP (Model Context Protocol)

[← Back to Main README](../../README.md)

Hub for MCP patterns, safety, and decision guidance. Individual MCP server
guides live in their domain directories — this hub covers what applies to
all MCPs.

## What MCPs Are

- External tool servers that give Claude access to databases, browsers, APIs,
  deployment platforms
- Run as local processes (stdio) or remote servers (HTTP)
- Execute with your user permissions — treat as arbitrary code execution

## Contents

| Guide | What It Covers |
|-------|---------------|
| [MCP-SAFETY.md](./MCP-SAFETY.md) | Supply chain, version pinning, prompt injection, uninstall hygiene |
| [MCP-TRUST-TIERS.md](./MCP-TRUST-TIERS.md) | Build vs adapt vs install decision framework, vetting checklist |
| [MCP-CONTEXT.md](./MCP-CONTEXT.md) | Tool Search (lazy loading), context budgets, Claude Code vs Codex |
| [MCP-DECISION-TREES.md](./MCP-DECISION-TREES.md) | When to use which MCP server (browser, database, deployment) |

## Individual MCP Guides

These cover specific MCP servers in depth (setup, tools, workflows):

| Guide | MCP Server |
|-------|-----------|
| [Playwright MCP](./playwright/README.md) | Browser automation (28 tools, config options, WSL setup) |
| [Railway MCP](../railway/RAILWAY_MCP_GUIDE.md) | Deployment, logs, variables (16 tools, 5 workflow recipes) |

## Quick Start

1. **New to MCPs?** Read this page, then [MCP-CONTEXT.md](./MCP-CONTEXT.md)
2. **Security review?** Read [MCP-SAFETY.md](./MCP-SAFETY.md)
3. **Choosing an MCP?** See [MCP-DECISION-TREES.md](./MCP-DECISION-TREES.md)
4. **Setting up a specific MCP?** Go to the individual guide above
5. **Managing MCPs in Claude Code?** See [CLAUDE-CODE-CONFIG.md](../reference/CLAUDE-CODE-CONFIG.md)

## See Also

- [CLAUDE-CODE-CONFIG.md](../reference/CLAUDE-CODE-CONFIG.md) — MCP management commands, plugin toggling, hooks
- [ADVANCED-WORKFLOWS.md](../reference/ADVANCED-WORKFLOWS.md) — MCP in the broader extension architecture
- [CODEX-SETUP.md](../setup-guides/CODEX-SETUP.md) — Codex CLI dual-tool workflow
