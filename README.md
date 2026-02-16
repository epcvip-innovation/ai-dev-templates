## AI-Assisted Development — Templates, Guides & Setup

Evidence-based templates and setup guides for Claude Code, Codex, and AI-assisted development workflows.

---

### Where Should I Start?

| You Are... | Start Here | Time |
|------------|-----------|------|
| **New (Mac or Linux)** | [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) | 10 min |
| **New (Windows)** | [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) — see the Windows setup path inside | 10 min |
| **Windows + want full Linux dev environment** | [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) → then [New PC Setup](./docs/setup-guides/NEW-PC-SETUP.md) | 10 + 90 min |
| **Setting up Claude Code quickly** | [Quickstart](./docs/getting-started/CLAUDE-CODE-QUICKSTART.md) | 5 min |
| **Starting a new project** | [New Project Setup](./docs/getting-started/NEW-PROJECT-SETUP.md) | 30 min |
| **Experienced — here for templates** | [Templates](./templates/) | Browse |

> **What is Claude Code?** An AI coding assistant that runs in your terminal (or VS Code). It reads your codebase, writes code, runs commands, and helps you build software faster. We also recommend **Codex CLI** as a secondary tool — one writes code, the other reviews it.

---

**Daily users**: See [Daily Workflow Guide](./docs/setup-guides/DAILY-WORKFLOW.md) for everyday usage.

> **Note**: This repository contains templates and examples. Replace paths, usernames, and repository URLs with your own before use.

## What This Repo Provides

1. **Template Library** — 66 template files across 10 categories
   - **9 active slash commands** (quality, design, git workflow)
   - **CLAUDE.md structures** — Lightweight, evidence-based project context templates
   - **Project organization** — `.projects/` 3-tier backlog system
   - **Anti-slop standards** — Automated quality gates preventing AI-generated bloat
   - **Hooks, permissions, testing, CI/CD, plugins** — Full workflow automation

2. **Setup Guides** — Get running on Mac, Windows, or Linux
   - [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) — Platform-agnostic setup for Claude Code + Codex
   - [Quickstart](./docs/getting-started/CLAUDE-CODE-QUICKSTART.md) — 5-minute Claude Code install
   - [Claude Code deep-dive](./docs/setup-guides/CLAUDE-CODE-SETUP.md) — Configuration, troubleshooting, best practices
   - [Codex CLI](./docs/setup-guides/CODEX-SETUP.md) — Dual-tool workflow setup

3. **WSL2 Power Setup** (optional, Windows only) — Full Linux dev environment
   - [New PC Setup](./docs/setup-guides/NEW-PC-SETUP.md) — 90-minute guided Windows 11 + WSL2 setup
   - [Why WSL?](./docs/decisions/why-wsl.md) — Architecture decision (it's a choice, not a requirement)
   - The [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) guide explains when to choose WSL vs native Windows

4. **Research & Evidence** — Extracted from real-world usage, not arbitrary
   - 4 repository audits (production FastAPI services, data processors, template projects)
   - 239+ commits analyzed for pattern validation
   - 13 patterns tested across multiple projects before extraction

---

## Quick Navigation

### Setup Guides
- **[Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md)** — Platform-agnostic Claude Code + Codex setup (Mac, Windows, Linux)
- [Quickstart](./docs/getting-started/CLAUDE-CODE-QUICKSTART.md) — 5-minute Claude Code install
- [Claude Code Setup](./docs/setup-guides/CLAUDE-CODE-SETUP.md) — Full installation and configuration
- [Codex Setup](./docs/setup-guides/CODEX-SETUP.md) — Dual-tool workflow with Codex CLI
- [Daily Workflow Guide](./docs/setup-guides/DAILY-WORKFLOW.md) — Everyday usage patterns
- [Multi-Device Workspace](./docs/setup-guides/MULTI-DEVICE-WORKSPACE.md) — Access Claude Code from iPad/phone/laptop
- [Cursor + WSL Setup](./docs/setup-guides/CURSOR-WSL-SETUP.md) — IDE with WSL integration (Windows)
- [Why WSL?](./docs/decisions/why-wsl.md) — Architecture decision: why we use WSL (it's a choice, not a requirement)

### Browse Templates
- [**Slash Commands**](./templates/slash-commands/) — 13 commands across 7 categories
  - [Context Management](./templates/slash-commands/context-management/) — Replace `/compact` with explicit control
- [**CLAUDE.md Structures**](./templates/claude-md/) — Lightweight project context templates
- [**Project Organization**](./templates/projects/) — `.projects/` 3-tier backlog system
- [**Anti-Slop Standards**](./templates/standards/) — Automated quality enforcement
- [**Features Backlog**](./templates/features-backlog/) — Tier-based prioritization
- [**Permissions**](./templates/permissions/) — Tool access configuration
- [**Hooks**](./templates/hooks/) — Workflow automation and validation hooks
- [**Testing**](./templates/testing/) — Playwright + Claude Code testing patterns
- [**CI/CD**](./templates/ci/) — GitHub Actions for AI-assisted development
- [**Plugins**](./templates/plugins/) — Claude Code skills (code review, backlog)
- [**All Templates →**](./templates/)

### Common Tasks
- **Set up new project** → [**New Project Setup Guide**](./docs/getting-started/NEW-PROJECT-SETUP.md)
- **Work from iPad/phone** → [Multi-Device Workspace](./docs/setup-guides/MULTI-DEVICE-WORKSPACE.md)
- **Browser automation/testing** → [Playwright MCP](./docs/reference/PLAYWRIGHT-MCP.md)
- **Replace `/compact`** → [Context Management Commands](./templates/slash-commands/context-management/)
- **Enforce query validation** → [Query Validation Hook](./templates/hooks/query-validation/)
- **Copy a slash command** → [templates/slash-commands/](./templates/slash-commands/)
- **Set up backlog system** → [templates/features-backlog/](./templates/features-backlog/)
- **Learn anti-slop principles** → [templates/standards/ANTI_SLOP_STANDARDS.md](./templates/standards/ANTI_SLOP_STANDARDS.md)
- **Browse documentation patterns** → [templates/standards/DOCUMENTATION_STRATEGY.md](./templates/standards/DOCUMENTATION_STRATEGY.md)

---

## Environment Quick Start

### Launch a Project
```bash
dev <project-name> [mode]    # Launch AI tools or IDE
```

**Common modes**: `claude`, `codex`, `cursor`

**Examples**:
```bash
dev my-project claude         # Start Claude Code
dev my-project codex          # Start Codex
dev my-project cursor         # Open in Cursor IDE
```

### Essential Commands

| Task | Command |
|------|---------|
| Start Claude | `claude` |
| Start Codex | `codex` |
| Open Cursor | `cursor .` |
| Check performance | `perf` or `perf --disk` |

**Full command reference**: [docs/reference/COMMANDS.md](./docs/reference/COMMANDS.md)

---

## Architecture: Our WSL2 Setup (Windows)

```text
Windows 11 Pro (Host)
├── Cursor IDE (Windows) → Remote-WSL → WSL2
└── WSL2 Ubuntu
    ├── ~/repos/ (all projects - Linux FS, fast I/O)
    ├── Claude Code (AI pair programming)
    ├── Codex CLI (secondary AI, cross-review)
    └── VS Code / Cursor (via Remote-WSL)
```

This is our team's power-user setup on Windows. **Not required** — Claude Code and Codex work natively on Mac, Windows, and Linux without WSL. See [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) for platform-agnostic installation.

**Why WSL?**: Linux filesystem is 10x faster than Windows FS for development. See [Why WSL?](./docs/decisions/why-wsl.md) for full rationale.

---

## Common Issues

| Issue | Solution |
|-------|----------|
| **Claude/Codex not found** | See [Getting Started](./docs/getting-started/SETUP-GUIDE-2026.md) for install instructions |
| **Cursor won't open from WSL** | Use `cursor .` command or see [Cursor WSL Setup](./docs/setup-guides/CURSOR-WSL-SETUP.md) |
| **Memory growing (WSL)** | Check with `perf`, restart: `wsl --shutdown` (PowerShell) |
| **Slow performance (WSL)** | Ensure code is in `~/repos/`, not `/mnt/c/` |

---

## Configuration Files

This repo includes sample configuration files and scripts:

- `scripts/dev` — Project launcher with AI assistant integration
- `scripts/perf` — WSL2 performance monitoring
- `scripts/obs` — Obsidian launcher for WSL
- `templates/` — Reusable templates for projects, slash commands, hooks
- `docs/` — Setup guides and reference documentation
  - `docs/railway/` — [Railway deployment guides](./docs/railway/README.md) for cloud-hosted projects

**Note**: System-specific configs (like `.bashrc`, actual project paths) live in `_private/personal/` (nested git repo, git-ignored).

---

## Template Library

### How These Templates Were Built

**Evidence-Based, Not Arbitrary**

These aren't theoretical best practices. They were extracted from real usage:

1. **Pattern Discovery** (4 repositories audited)
   - Production FastAPI services (6+ months, 130+ commits)
   - Data processing pipelines (3 months, 60+ commits)
   - Template projects (2 months, 49+ commits)

2. **Validation** (239+ commits analyzed)
   - Which patterns appeared in 3+ projects?
   - Which solved recurring problems?
   - Which were abandoned? (those were excluded)

3. **Refinement** (Tested in new projects)
   - Applied templates to new codebases
   - Measured effectiveness (time saved, bugs prevented)
   - Iterated based on real-world feedback

**Result**: 13 Tier 1 patterns validated for extraction, organized into 27 template files.

---

### Template Categories

**Slash Commands** (13 commands, 7 categories)
- Development workflow: `/start-feature`, `/resume`, `/feature-complete`
- Analysis: `/plan-approaches`, `/performance-analysis`
- Documentation: `/audit-claude-md`, `/sync-team-docs`
- [Browse all commands →](./templates/slash-commands/)

**CLAUDE.md Structures**
- Lightweight project context (150-200 lines recommended)
- Hub-and-spoke pattern (main CLAUDE.md → category docs)
- Evidence from 4 repo audits
- [See templates →](./templates/claude-md/)

**Project Organization**
- `.projects/` 3-tier backlog system (active, backlog, icebox)
- Prevents "forgotten feature" syndrome
- Integrates with slash commands
- [Learn more →](./templates/projects/)

**Anti-Slop Standards**
- 7 universal standards (functions <50 lines, nesting <3, etc.)
- Automated enforcement (grep patterns, pre-commit hooks)
- Recognition patterns for AI-generated bloat
- [Full standards →](./templates/standards/)

**Features Backlog**
- Tier-based prioritization (Tier 1: critical, Tier 2: important, Tier 3: nice-to-have)
- Prevents over-engineering ("Tier 1 only" mindset)
- Works with .projects/ system
- [See template →](./templates/features-backlog/)

**Permissions**
- Environment-based tool access (home repo, work repo, demo mode)
- Security patterns for AI tools
- Pre-configured permission sets
- [See patterns →](./templates/permissions/)

---

Created: September 2024
Last Updated: February 13, 2026
