# CLAUDE.md

<!-- AUDIT: Run /audit-claude-md quarterly. Last audit: 2026-01-15. Next: 2026-04-15 -->

This file provides guidance to Claude Code when working with this repository.

## Repository Purpose

This is an **AI workflow template library**, built from 6+ months of real-world AI-assisted development experience.

**Primary Purpose**: 66 template files across 10 categories for AI-assisted development
- Evidence-based approach: 239+ commits analyzed across 4 production repositories
- 10 template categories: slash commands, CLAUDE.md structures, anti-slop standards, hooks, project organization, features backlog, permissions, testing, CI/CD, plugins
- Ready for personal use, team adoption, and future public sharing

**Target Audience**: Team (primary), public community (future)

## Template Library

The core value of this repository. **Browse before using** - these are patterns to adapt, not rules to follow.

### 10 Template Categories

**1. Slash Commands** (`templates/slash-commands/`)
- 21 active commands (16 general + 5 audit lenses)
- Categories: quality (`/audit-feature`, `/ai-review`), design (`/plan-approaches`), git (`/push`), debugging (`/debug-failure`)
- Examples: `/audit-feature`, `/push`, `/plan-approaches`, `/ai-review`, `/debug-failure`
- **See**: [templates/slash-commands/README.md](./templates/slash-commands/README.md)

**2. CLAUDE.md Structures** (`templates/claude-md/`)
- Lightweight project context templates (hub-and-spoke pattern)
- 150-200 line target (vs 500+ line bloat)
- Progressive disclosure: hub → spokes
- **See**: [templates/claude-md/CLAUDE-MD-GUIDELINES.md](./templates/claude-md/CLAUDE-MD-GUIDELINES.md)

**3. Anti-Slop Standards** (`templates/standards/`)
- 7 universal standards: functions <50 lines, nesting <3, no premature optimization
- Automated enforcement with grep patterns and pre-commit hooks
- 789 lines of detailed standards with recognition patterns
- **See**: [templates/standards/ANTI_SLOP_STANDARDS.md](./templates/standards/ANTI_SLOP_STANDARDS.md)

**3b. Frontend Standards** (`templates/standards/`)
- CSS/JS interaction patterns for vanilla JavaScript projects
- Prevents display type mismatches (block vs flex vs grid)
- Class-based visibility toggling, state management patterns
- **See**: [templates/standards/FRONTEND_STANDARDS.md](./templates/standards/FRONTEND_STANDARDS.md)

**4. Hooks System** (`templates/hooks/`)
- Workflow automation: query validation, pre-commit formatting, logging
- Event-driven patterns for AI workflows
- Latest addition (Nov 2025)
- **See**: [templates/hooks/README.md](./templates/hooks/README.md)

**5. Project Organization** (`templates/projects/`)
- `.projects/` 3-tier backlog system (active, backlog, icebox)
- Prevents "forgotten feature" syndrome
- Integrates with slash commands
- **See**: [templates/projects/README.md](./templates/projects/README.md)

**6. Features Backlog** (`templates/features-backlog/`)
- Two approaches: Simple (single-file) or Folder-based (with Python utilities)
- YAML frontmatter for tracking status, priority, effort
- **See**: [templates/features-backlog/README.md](./templates/features-backlog/README.md)

**7. Permissions** (`templates/permissions/`)
- Environment-based tool access configuration
- Reduces approval prompts
- **See**: [templates/permissions/README.md](./templates/permissions/README.md)

**8. Testing** (`templates/testing/`)
- Playwright E2E testing patterns for Claude Code projects
- Two modes: scripted tests (CI/regression) vs MCP (Claude-driven exploration)
- Page Object Model and multi-user fixture patterns
- **See**: [templates/testing/PLAYWRIGHT_CLAUDE_GUIDE.md](./templates/testing/PLAYWRIGHT_CLAUDE_GUIDE.md)

**9. CI/CD** (`templates/ci/`)
- GitHub Actions workflows for AI-assisted development
- Claude QA: Automated PR verification with Claude + Playwright MCP
- QA persona prompting for consistent, thorough reviews
- **See**: [templates/ci/README.md](./templates/ci/README.md)

**10. Plugins** (`templates/plugins/`)
- Claude Code skills for common workflows
- Multi-agent adversarial code review (5-agent and 3-agent lite versions)
- Severity scoring, technology-specific patterns
- **See**: [templates/plugins/README.md](./templates/plugins/README.md)

## Repository Layers

This repo has three layers of content:

| Layer | Location | Visibility | Purpose |
|-------|----------|-----------|---------|
| Private | `_private/` | Gitignored (own repo) | Personal configs, research intake, workflow preferences |
| Templates | `templates/` | Public | Reusable AI dev patterns (10 categories) |
| Docs | `docs/` | Public | Setup guides, reference, decisions |

`_private/` is a nested git repo — it's version-controlled separately and structurally invisible to this repo's git. See `_private/README.md` for setup instructions.

**Safety**: `.gitignore` excludes `_private/`, and a pre-commit hook (`scripts/hooks/pre-commit`) blocks accidental staging. Install with: `cp scripts/hooks/pre-commit .git/hooks/pre-commit`

## Research & Evidence

### Evidence-Based Approach

All templates extracted from real production usage, not theoretical best practices.

**Methodology**:
1. **Pattern Discovery**: 4 repositories audited (ping-tree-compare, dois-processor, claude-dev-template, and others)
2. **Validation**: 239+ commits analyzed for recurring patterns
3. **Refinement**: Tested in new projects, iterated based on feedback

**Note**: Research methodology and audit findings live in `_private/research/` (separate repo). Templates are production-validated and ready for use.

## Using This Repository

**Philosophy**: "Evidence-based patterns you can copy and adapt, not rules you must follow."

**Getting Started**:
1. **Browse** [templates/README.md](./templates/README.md) for overview
2. **Read** category READMEs to understand when/how to use each template
3. **Adapt** templates to your project structure and needs
4. **Validate** patterns work for your specific context

**For Context & Learning**:
- See [README.md](./README.md) for complete navigation

**Don't**:
- Don't copy templates blindly without understanding context
- Don't treat these as rigid requirements
- Don't skip adaptation for your specific project

## Development Environment

**Secondary Purpose**: WSL2-based development environment setup and utilities.

**Quick Start**:
- **[docs/setup-guides/DAILY-WORKFLOW.md](./docs/setup-guides/DAILY-WORKFLOW.md)** - ⭐ Daily workflow guide
- **[docs/decisions/why-wsl.md](./docs/decisions/why-wsl.md)** - Why we use WSL (architectural decision)

**Setup Guides**:
- **[docs/getting-started/SETUP-GUIDE-2026.md](./docs/getting-started/SETUP-GUIDE-2026.md)** - Platform-agnostic setup (Mac, Windows, Linux)
- **[docs/setup-guides/NEW-PC-SETUP.md](./docs/setup-guides/NEW-PC-SETUP.md)** - 90-minute WSL2 new machine setup
- **[docs/setup-guides/CLAUDE-CODE-SETUP.md](./docs/setup-guides/CLAUDE-CODE-SETUP.md)** - Claude Code deep-dive
- **[docs/setup-guides/CODEX-SETUP.md](./docs/setup-guides/CODEX-SETUP.md)** - Codex CLI + dual-tool workflow
- **[docs/setup-guides/CURSOR-WSL-SETUP.md](./docs/setup-guides/CURSOR-WSL-SETUP.md)** - Cursor + WSL integration
- **[docs/setup-guides/LOCAL-NETWORK-SHARING.md](./docs/setup-guides/LOCAL-NETWORK-SHARING.md)** - Share dev servers across devices

**Reference**:
- **[docs/reference/WSL-PATHS.md](./docs/reference/WSL-PATHS.md)** - Understanding Windows ↔ WSL paths
- **[docs/reference/CLAUDE-CODE-CONFIG.md](./docs/reference/CLAUDE-CODE-CONFIG.md)** - MCP configuration
- **[docs/reference/COMMANDS.md](./docs/reference/COMMANDS.md)** - Command reference

**Utility Scripts**:
- `scripts/dev` - Launch projects with AI assistants
- `scripts/perf` - WSL2 performance monitoring

## Key Workflows

**Daily development**:
```bash
cd ~/repos/your-project
claude              # Start Claude Code
cursor .            # Open Cursor (Remote-WSL)
```

**Common tasks**:
- Browse templates: `ls templates/`
- Check performance: `perf`

## Documentation Map

**Getting Started** (New Projects):
- [docs/getting-started/NEW-PROJECT-SETUP.md](./docs/getting-started/NEW-PROJECT-SETUP.md) - Complete project setup guide
- [docs/decisions/BUILTIN_VS_CUSTOM.md](./docs/decisions/BUILTIN_VS_CUSTOM.md) - When to use built-in vs custom

**Template Library** (Primary):
- [templates/README.md](./templates/README.md) - Complete template library overview
- [templates/slash-commands/](./templates/slash-commands/) - 21 workflow commands
- [templates/plugins/](./templates/plugins/) - Claude Code skills (code-review, backlog)
- [templates/features-backlog/](./templates/features-backlog/) - Simple & folder-based backlog systems
- [templates/claude-md/](./templates/claude-md/) - CLAUDE.md structure templates
- [templates/standards/](./templates/standards/) - Anti-slop standards & documentation strategy
- [templates/testing/](./templates/testing/) - Playwright + Claude Code testing patterns

**Research & Evidence**:
- Research methodology and audit findings in `_private/research/` (separate repo)

**Reference**:
- [docs/reference/ADVANCED-WORKFLOWS.md](./docs/reference/ADVANCED-WORKFLOWS.md) - Context management, agents, predictability, model strategy

**Environment Setup** (Secondary):
- [README.md](./README.md) - Main hub for all documentation
- [docs/setup-guides/DAILY-WORKFLOW.md](./docs/setup-guides/DAILY-WORKFLOW.md) - Daily workflow guide
- [docs/decisions/why-wsl.md](./docs/decisions/why-wsl.md) - Architectural decisions
- [docs/setup-guides/](./docs/setup-guides/) - Setup and architecture guides
- [docs/reference/](./docs/reference/) - Commands, paths, and configuration reference

## Important Notes

1. **This is a template library** - Not an environment setup guide (that's secondary)
2. **Evidence-based** - All patterns validated across 239+ commits in production repos
3. **Adapt, don't copy** - Templates are starting points, not rigid requirements
4. **Team resource** - Intended for team use and public community contribution
5. **Living documentation** - Continuously updated based on real-world usage
