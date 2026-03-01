---
id: ai-dev-templates
title: "AI-Assisted Development — Templates, Guides & Setup"
description: "Battle-tested templates for AI-assisted development with Claude Code"
audience: beginner
tags: ["templates", "setup", "claude-code"]
---

## AI-Assisted Development — Templates, Guides & Setup

Battle-tested templates for AI-assisted development with Claude Code, extracted from 6+ months of production usage across 4 repositories.

---

### Start Here

| You Are... | Go To |
|------------|-------|
| **Experienced — here for templates** | **[Template Library](./templates/README.md)** |
| **Starting a new project** | [New Project Setup](./docs/getting-started/NEW-PROJECT-SETUP.md) |
| **New to Claude Code** | [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) |

---

## Template Library

10 categories of production-validated patterns. Also: [Auth patterns](./templates/auth/README.md) | [Railway configs](./templates/railway/README.md)

| Category | Purpose | Entry Point |
|----------|---------|-------------|
| **Skill Templates (Command Format)** | 21 flat-file skill templates (quality, design, git) | [README](./templates/slash-commands/README.md) |
| **CLAUDE.md Structures** | Lightweight project context (hub-and-spoke) | [README](./templates/claude-md/README.md) |
| **Skills** | Claude Code skills (code-review, skill-creator) | [README](./templates/skills/README.md) |
| **Project Management** | Tasks, backlogs, `.projects/` cross-session | [README](./templates/project-management/README.md) |
| **Anti-Slop Standards** | 7 universal quality gates with grep patterns | [ANTI_SLOP_STANDARDS.md](./templates/standards/ANTI_SLOP_STANDARDS.md) |
| **Frontend Standards** | CSS/JS interaction patterns, class-based visibility | [FRONTEND_STANDARDS.md](./templates/standards/FRONTEND_STANDARDS.md) |
| **Hooks** | Workflow automation and validation hooks | [README](./templates/hooks/README.md) |
| **Permissions** | Tool access configuration | [README](./templates/permissions/README.md) |
| **Testing** | Playwright + Claude Code E2E patterns | [README](./templates/testing/README.md) |
| **CI/CD** | Security review, QA workflows, risk-based gating | [README](./templates/ci/README.md) |

---

## Guides & Reference

| Document | Purpose |
|----------|---------|
| [Context Engineering](./docs/reference/CONTEXT-ENGINEERING.md) | .claudeignore, token optimization, isolation strategies, session management |
| [Consistency at Scale](./docs/reference/CONSISTENCY-AT-SCALE.md) | Tiered context, routing tables, ADRs, refactoring coordination for large repos |
| [Advanced Workflows](./docs/reference/ADVANCED-WORKFLOWS.md) | 7-section power-user guide: context, planning, agents, extensions, predictability |
| [MCP Patterns](./docs/mcp/README.md) | Context efficiency, version pinning, decision trees |
| [Playwright MCP](./docs/mcp/playwright/README.md) | Claude-driven browser automation |
| [Railway Docs](./docs/railway/README.md) | Deployment guides and configuration |
| [Daily Workflow](./docs/setup-guides/DAILY-WORKFLOW.md) | Everyday usage patterns |
| [Claude Code Config](./docs/reference/CLAUDE-CODE-CONFIG.md) | MCP and settings configuration |
| [Built-in vs Custom](./docs/decisions/BUILTIN_VS_CUSTOM.md) | When to use built-in features vs custom templates |

---

## Environment Setup

Platform-agnostic guides for Mac, Windows, and Linux. WSL2 is optional for Windows power users — see [Why WSL?](./docs/decisions/why-wsl.md).

| Guide | Purpose |
|-------|---------|
| [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) | Platform-agnostic Claude Code + Codex setup |
| [Quickstart](./docs/getting-started/CLAUDE-CODE-QUICKSTART.md) | 5-minute Claude Code install |
| [Claude Code Setup](./docs/setup-guides/CLAUDE-CODE-SETUP.md) | Full installation and configuration |
| [Codex Setup](./docs/setup-guides/CODEX-SETUP.md) | Dual-tool workflow with Codex CLI |
| [Multi-Device Workspace](./docs/setup-guides/MULTI-DEVICE-WORKSPACE.md) | Access Claude Code from iPad/phone/laptop |
| [Cursor + WSL](./docs/setup-guides/CURSOR-WSL-SETUP.md) | IDE with WSL integration (Windows) |
| [Commands Reference](./docs/reference/COMMANDS.md) | Full command reference |

> **Note**: This repository contains templates and examples. Replace paths, usernames, and repository URLs with your own before use.

---

## Evidence

All templates extracted from real production usage — 4 repositories audited, 239+ commits analyzed, 13 patterns validated across multiple projects before extraction. Not theoretical best practices.

---
