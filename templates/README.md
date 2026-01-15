# Template Library

Production-validated patterns for AI-assisted development.

**Updated**: January 2026

---

## Quick Start

| Need | Go To |
|------|-------|
| **New project setup** | [Getting Started Guide](../docs/getting-started/NEW-PROJECT-SETUP.md) |
| **Built-in vs custom?** | [Decision Guide](../docs/decisions/BUILTIN_VS_CUSTOM.md) |
| **Backlog management** | [Features Backlog](./features-backlog/README.md) |
| **Code review** | [Plugins](./plugins/README.md) |

---

## 10 Template Categories

| Category | Purpose | Entry Point |
|----------|---------|-------------|
| **slash-commands** | CLI command templates (9 active) | [README](./slash-commands/README.md) |
| **claude-md** | CLAUDE.md structure patterns | [README](./claude-md/README.md) |
| **plugins** | Claude Code skills (code-review, backlog) | [README](./plugins/README.md) |
| **features-backlog** | Simple & folder-based backlog systems | [README](./features-backlog/README.md) |
| **standards** | Anti-slop quality standards | [ANTI_SLOP_STANDARDS.md](./standards/ANTI_SLOP_STANDARDS.md) |
| **hooks** | Workflow automation hooks | [README](./hooks/README.md) |
| **projects** | Project organization patterns | [README](./projects/README.md) |
| **permissions** | Tool access configuration | [README](./permissions/README.md) |
| **testing** | Playwright + Claude Code patterns | [PLAYWRIGHT_CLAUDE_GUIDE.md](./testing/PLAYWRIGHT_CLAUDE_GUIDE.md) |
| **ci** | GitHub Actions workflows | [README](./ci/README.md) |

---

## Key Insight: Plugins > Slash Commands

Based on real-world usage:

- **Plugins** auto-trigger, support hooks, and sub-tasks can't be ignored
- **Slash commands** are good for utilities (`/push`, `/audit`)
- **Python utilities** are valuable for data operations (backlog indexing)

See [BUILTIN_VS_CUSTOM.md](../docs/decisions/BUILTIN_VS_CUSTOM.md) for detailed guidance.

---

## Template Counts

- **66 template files** across 10 categories
- **9 active slash commands** (7 deprecated, moved to `_deprecated/`)
- **5 plugin skills** (code-review agents, backlog management)
- **3 Python utilities** for backlog enforcement

---

## Philosophy

> "Evidence-based patterns you can copy and adapt, not rules you must follow."

These templates were extracted from real production usage across 239+ commits in 4 repositories, not theoretical best practices.

---

**Last Updated**: 2026-01-15
