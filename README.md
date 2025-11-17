## WSL2 + Claude Code + Codex + Cursor Development Setup

**Multi-AI Development Environment + Template Library**

**Quick Start**: See [Daily Workflow Guide](./docs/setup-guides/DAILY-WORKFLOW.md) for everyday usage, or [New PC Setup](./docs/setup-guides/NEW-PC-SETUP.md) for initial setup.

> **Note**: This repository contains templates and personal examples. Replace paths, usernames, and repository URLs with your own before use. If you're setting up a new machine with your personal config, check the `personal/` folder (git-ignored) for your actual setup details.

## What This Repo Provides

1. **Development Environment** - WSL2 + Claude Code + Codex CLI + Cursor IDE
   - High-performance Linux filesystem (~2.4 GB/s vs 200 MB/s Windows)
   - Parallel AI workflows with Claude Code and Codex
   - 32-core system optimized for AI-assisted development

2. **Template Library** - 27 validated patterns for AI-assisted development
   - **13 slash commands** across 7 workflow categories (development, analysis, documentation)
   - **CLAUDE.md structures** - Lightweight, evidence-based project context templates
   - **Project organization** - `.projects/` 3-tier backlog system
   - **Anti-slop standards** - Automated quality gates preventing AI-generated bloat
   - **Features backlog** - Tier-based prioritization framework
   - **Permission environments** - Tool access configuration patterns
   - **Workflow hooks** - Automated validation and enforcement (query validation, formatting)

3. **Research & Evidence** - Extracted from real-world usage, not arbitrary
   - 4 repository audits (ping-tree-compare, tiller-bridge, dois-processor, template projects)
   - 239+ commits analyzed for pattern validation
   - 13 patterns tested across multiple projects before extraction

---

## Quick Navigation

### 🎯 Daily Workflow
- **[Daily Workflow Guide](./docs/setup-guides/DAILY-WORKFLOW.md)** - ⭐ Start here for everyday usage
- [Claude Code Setup](./docs/setup-guides/CLAUDE-CODE-SETUP.md) - Installing and using Claude Code CLI
- [Codex Setup](./docs/setup-guides/CODEX-SETUP.md) - Alternative AI assistant setup
- [Cursor + WSL Setup](./docs/setup-guides/CURSOR-WSL-SETUP.md) - IDE with WSL integration
- [Why WSL?](./docs/decisions/why-wsl.md) - Architecture decision: why we use WSL (it's a choice, not a requirement)

### 🚀 Setting Up Environment
- **[New PC Setup](./docs/setup-guides/NEW-PC-SETUP.md)** - 90-minute guided setup for Windows 11
- [Global CLI Commands](./docs/reference/GLOBAL-CLI-SETUP.md) - Make repo scripts globally available
- [WSL Paths Reference](./docs/reference/WSL-PATHS.md) - Understanding Windows ↔ WSL paths
- [Claude Code Config](./docs/reference/CLAUDE-CODE-CONFIG.md) - MCPs, plugins, and configuration
- [Obsidian WSL Setup](./docs/setup-guides/OBSIDIAN-WSL-SETUP.md) - Running Obsidian in WSL

### 📚 Browse Templates
- [**Slash Commands**](./templates/slash-commands/) - 13 commands across 7 categories
  - ⭐ **[Context Management](./templates/slash-commands/context-management/)** - Replace `/compact` with explicit control
- [**CLAUDE.md Structures**](./templates/claude-md/) - Lightweight project context templates
- [**Project Organization**](./templates/projects/) - `.projects/` 3-tier backlog system
- [**Anti-Slop Standards**](./templates/standards/) - Automated quality enforcement
- [**Features Backlog**](./templates/features-backlog/) - Tier-based prioritization
- [**Permissions**](./templates/permissions/) - Tool access configuration
- [**Hooks**](./templates/hooks/) - 🆕 Workflow automation and validation hooks
- [**All Templates →**](./templates/)

### 🔍 Research & Validation
- Research methodology and audit findings excluded from this repository for brevity. Templates are production-validated from 239+ commits across 4 repositories.
- [Journal](./JOURNAL.md) - Personal AI-driven development journey

### 🎯 Common Tasks
- **Replace `/compact`** → [Context Management Commands](./templates/slash-commands/context-management/)
- **Enforce query validation** → [Query Validation Hook](./templates/hooks/query-validation/)
- **Copy a slash command** → [templates/slash-commands/](./templates/slash-commands/)
- **Set up new project** → [templates/projects/](./templates/projects/)
- **Learn anti-slop principles** → [templates/standards/ANTI_SLOP_STANDARDS.md](./templates/standards/ANTI_SLOP_STANDARDS.md)
- **Browse documentation patterns** → [templates/standards/DOCUMENTATION_STRATEGY.md](./templates/standards/DOCUMENTATION_STRATEGY.md)
- **See the journey** → [JOURNAL.md](./JOURNAL.md)

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
| Launch Obsidian | `obs` |
| Check performance | `perf` or `perf --disk` |

**Full command reference**: [docs/reference/COMMANDS.md](./docs/reference/COMMANDS.md)

---

## System Overview

### Performance Baseline

| Component | Spec | Notes |
|-----------|------|-------|
| **CPU** | i9-14900K (32 threads) | 24-26 allocated to WSL |
| **Memory** | 64GB total, 24GB to WSL | Typical usage: 1-2GB |
| **Linux FS** | ~2.4 GB/s | Use `~/repos/` for all code |
| **Windows FS** | ~200 MB/s | 10x slower, avoid for dev |
| **GPU** | RTX 4080 SUPER | Available to WSL via WSLg |

### Directory Structure
```
~/repos/              # All projects (Linux FS - FAST)
  ├── code/           # Development projects
  ├── docs/           # Documentation (Obsidian vaults)
  │   ├── personal-docs/            # Personal docs
  │   ├── company-shared-docs/      # Company docs
  │   └── query-docs/               # Query docs
  └── ai-dev-templates/  # This repo
~/bin/                # Custom scripts (dev, perf, etc.)
~/knowledge-base/     # Symlinks to doc repos
```

### Architecture
```text
Windows 11 Pro (Host)
├── Cursor IDE (Windows) → Remote-WSL → WSL2
└── WSL2 Ubuntu (24GB RAM, 26 processors)
    ├── ~/repos/ (all projects - FAST: 2.4 GB/s)
    ├── Claude Code (AI pair programming)
    ├── Codex CLI (Alternative AI)
    └── Obsidian (via WSLg)
```

**Why WSL?**: Linux filesystem is 10x faster than Windows FS. See [Why WSL?](./docs/decisions/why-wsl.md) for full rationale.

---

## Common Issues

| Issue | Solution |
|-------|----------|
| **Cursor won't open from WSL** | Use `cursor .` command or see [Cursor WSL Setup](./docs/setup-guides/CURSOR-WSL-SETUP.md) |
| **Memory growing** | Check with `perf`, restart: `wsl --shutdown` (PowerShell) |
| **Slow performance** | Ensure code is in `~/repos/`, not `/mnt/c/` |
| **Claude/Codex not found** | See setup guides: [Claude Code](./docs/setup-guides/CLAUDE-CODE-SETUP.md) \| [Codex](./docs/setup-guides/CODEX-SETUP.md) |

---

## Configuration Files

This repo includes sample configuration files and scripts:

- `scripts/dev` - Project launcher with AI assistant integration
- `scripts/perf` - WSL2 performance monitoring
- `scripts/obs` - Obsidian launcher for WSL
- `templates/` - Reusable templates for projects, slash commands, hooks
- `docs/` - Setup guides and reference documentation
  - `docs/railway/` - [Railway deployment guides](./docs/railway/README.md) for cloud-hosted projects

**Note**: System-specific configs (like `.bashrc`, actual project paths) live in `personal/` (git-ignored).

**WSL Configuration**: `C:\Users\<YourUsername>\.wslconfig` (24GB RAM, 26 processors, mirrored networking)

---

## Template Library

### How These Templates Were Built

**Evidence-Based, Not Arbitrary**

These aren't theoretical best practices. They were extracted from real usage:

1. **Pattern Discovery** (4 repositories audited)
   - ping-tree-compare (6 months, 80+ commits)
   - tiller-bridge (4 months, 50+ commits)
   - dois-processor (3 months, 60+ commits)
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

**📝 Slash Commands** (13 commands, 7 categories)
- Development workflow: `/start-feature`, `/resume`, `/feature-complete`
- Analysis: `/plan-approaches`, `/performance-analysis`
- Documentation: `/audit-claude-md`, `/sync-team-docs`
- [Browse all commands →](./templates/slash-commands/)

**📋 CLAUDE.md Structures**
- Lightweight project context (150-200 lines recommended)
- Hub-and-spoke pattern (main CLAUDE.md → category docs)
- Evidence from 4 repo audits
- [See templates →](./templates/claude-md/)

**📂 Project Organization**
- `.projects/` 3-tier backlog system (active, backlog, icebox)
- Prevents "forgotten feature" syndrome
- Integrates with slash commands
- [Learn more →](./templates/projects/)

**✨ Anti-Slop Standards**
- 7 universal standards (functions <50 lines, nesting <3, etc.)
- Automated enforcement (grep patterns, pre-commit hooks)
- Recognition patterns for AI-generated bloat
- [Full standards →](./templates/standards/)

**🎯 Features Backlog**
- Tier-based prioritization (Tier 1: critical, Tier 2: important, Tier 3: nice-to-have)
- Prevents over-engineering ("Tier 1 only" mindset)
- Works with .projects/ system
- [See template →](./templates/features-backlog/)

**🔐 Permissions**
- Environment-based tool access (home repo, work repo, demo mode)
- Security patterns for AI tools
- Pre-configured permission sets
- [See patterns →](./templates/permissions/)

---

### The Journey (Personal Context)

This template library documents my evolution with AI-assisted development over 6+ months:

- **Early mistakes**: Over-engineered solutions, AI-generated bloat, forgotten features
- **Pattern recognition**: What worked across multiple projects? What didn't?
- **Systematic extraction**: Auditing commits to find recurring patterns
- **Sharing**: Making these patterns reusable for others

**See the full story**: [JOURNAL.md](./JOURNAL.md) - Learnings, insights, and evolution over time.

---

Created: September 2024
Last Updated: November 2025