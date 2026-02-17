[← Back to Main README](../README.md)

# Template Library

Production-validated patterns for AI-assisted development.

**Updated**: February 2026

---

## Quick Start

| Need | Go To |
|------|-------|
| **New project setup** | [Getting Started Guide](../docs/getting-started/NEW-PROJECT-SETUP.md) |
| **Built-in vs custom?** | [Decision Guide](../docs/decisions/BUILTIN_VS_CUSTOM.md) |
| **Task/backlog management** | [Project Management](./project-management/README.md) |
| **Code review** | [Plugins](./plugins/README.md) |

---

## 10 Template Categories

| Category | Purpose | Entry Point |
|----------|---------|-------------|
| **slash-commands** | CLI command templates (21 active) | [README](./slash-commands/README.md) |
| **claude-md** | CLAUDE.md structure patterns | [README](./claude-md/README.md) |
| **plugins** | Claude Code skills (code-review) | [README](./plugins/README.md) |
| **project-management** | Tasks, backlogs, .projects/ cross-session | [README](./project-management/README.md) |
| **standards** | Anti-slop quality standards | [ANTI_SLOP_STANDARDS.md](./standards/ANTI_SLOP_STANDARDS.md) |
| **standards** | Frontend CSS/JS interaction patterns | [FRONTEND_STANDARDS.md](./standards/FRONTEND_STANDARDS.md) |
| **hooks** | Workflow automation hooks | [README](./hooks/README.md) |
| **permissions** | Tool access configuration | [README](./permissions/README.md) |
| **testing** | Playwright + Claude Code patterns | [README](./testing/README.md) |
| **ci** (flat) | Security review + Claude QA on every PR | [README](./ci/README.md) |
| **ci** (risk-gated) | Classify PRs by risk tier, skip reviews for docs-only | [README](./ci/README.md) |

---

## Extension Mechanisms

Claude Code has four extension mechanisms — each serves a different purpose:

- **Skills** auto-trigger on natural language, best for complex multi-step workflows
- **Slash commands** are explicit and reliable, best for utilities (`/push`, `/audit`)
- **Hooks** are deterministic (shell scripts), best for validation and formatting
- **Python utilities** are best for data operations (backlog indexing, search)

See [BUILTIN_VS_CUSTOM.md](../docs/decisions/BUILTIN_VS_CUSTOM.md) for detailed guidance.

---

## Philosophy

> "Evidence-based patterns you can copy and adapt, not rules you must follow."

These templates were extracted from real production usage across 239+ commits in 4 repositories, not theoretical best practices.

---

## See Also

- [Advanced Workflows](../docs/reference/ADVANCED-WORKFLOWS.md) — Power-user guide: context, planning, agents, extensions
- [MCP Patterns](../docs/mcp/README.md) — Context efficiency, version pinning, decision trees
- [New Project Setup](../docs/getting-started/NEW-PROJECT-SETUP.md) — Complete project setup guide

---

**Last Updated**: 2026-02-16
