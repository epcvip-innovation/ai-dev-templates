# CLAUDE.md

<!-- AUDIT: Run /audit-claude-md quarterly. Last audit: 2026-01-15. Next: 2026-04-15 -->

This file provides guidance to Claude Code when working with this repository.

## Repository Purpose

This is an **AI workflow template library**, built from 6+ months of real-world AI-assisted development experience.

**Primary Purpose**: 66+ template files across 12 categories for AI-assisted development
- Evidence-based approach: 239+ commits analyzed across 4 production repositories
- 12 template categories: skill templates (command format), CLAUDE.md structures, anti-slop standards, hooks, project organization, features backlog, permissions, security, testing, CI/CD, skills, plugins
- Ready for personal use, team adoption, and community sharing

## Template Library

The core value of this repository. **Browse before using** - these are patterns to adapt, not rules to follow.

### 12 Template Categories

**1. Skill Templates — Command Format** (`templates/slash-commands/`)
- 21 active flat-file skill templates (16 general + 5 audit lenses)
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

**5. Project & Task Management** (`templates/project-management/`)
- Unified guide: native Tasks, `.projects/` cross-session pattern, single-file and folder-based backlogs
- YAML frontmatter for tracking status, priority, effort calibration
- Python utilities for indexing, validation, duplicate detection
- Optional backlog skills (experimental auto-trigger)
- **See**: [templates/project-management/README.md](./templates/project-management/README.md)

**6. Permissions** (`templates/permissions/`)
- Environment-based tool access configuration
- Reduces approval prompts
- **See**: [templates/permissions/README.md](./templates/permissions/README.md)

**7. Security** (`templates/security/`)
- Tiered AI agent security (baseline → team → strict)
- Deny lists, bypass prevention, hooks, settings isolation
- Industry-sourced (NVIDIA AI Red Team, Backslash Security)
- **See**: [templates/security/README.md](./templates/security/README.md)

**8. Testing** (`templates/testing/`)
- Playwright E2E testing patterns for Claude Code projects
- Two modes: scripted tests (CI/regression) vs MCP (Claude-driven exploration)
- Page Object Model and multi-user fixture patterns
- **See**: [templates/testing/PLAYWRIGHT_CLAUDE_GUIDE.md](./templates/testing/PLAYWRIGHT_CLAUDE_GUIDE.md)

**9. CI/CD** (`templates/ci/`)
- GitHub Actions workflows for AI-assisted development
- Claude QA: Automated PR verification with Claude + Playwright MCP
- QA persona prompting for consistent, thorough reviews
- Risk-gated CI: classify PRs by tier, gate security + QA on sensitive paths (optional advanced pattern)
- **See**: [templates/ci/README.md](./templates/ci/README.md)

**10. Skills** (`templates/skills/`)
- Claude Code skills for common workflows (code-review, tdd, skill-creator)
- Unified code review: 5-phase pipeline (agents → evaluation → root-cause), `--quick` for 3-agent mode
- TDD enforcement: RED-GREEN-REFACTOR cycle, test-first discipline during development (complements `/local-review` and `pr-test-analyzer` which review tests after the fact)
- Guided skill scaffolding: discovery interview → archetype → scaffold → quality validation
- Community skills: curated third-party skills with provenance tracking
- Includes [SKILL-TEMPLATE.md](./templates/skills/SKILL-TEMPLATE.md) for creating new skills
- **See**: [templates/skills/README.md](./templates/skills/README.md)
- **See**: [templates/skills/community/README.md](./templates/skills/community/README.md)

**11. Custom Agents** (`templates/agents/`)
- Subagent definitions with frontmatter: model, tools, memory, isolation, permissions
- Agent teams (experimental), background agents, worktree isolation
- **See**: [templates/agents/README.md](./templates/agents/README.md)

**12. Plugins** (`templates/plugins/`)
- Distributable bundles of commands, agents, hooks, and references
- Working example: doc-review (4 agents, multi-model, consolidated reports)
- Includes [PLUGIN-TEMPLATE.md](./templates/plugins/PLUGIN-TEMPLATE.md) for creating new plugins
- Team marketplace pattern for internal distribution
- **See**: [templates/plugins/README.md](./templates/plugins/README.md)

## Research & Evidence

### Evidence-Based Approach

All templates extracted from real production usage, not theoretical best practices.

**Methodology**:
1. **Pattern Discovery**: 4 repositories audited (production FastAPI services, data processors, template projects)
2. **Validation**: 239+ commits analyzed for recurring patterns
3. **Refinement**: Tested in new projects, iterated based on feedback

**Note**: 239+ commits analyzed across production repositories. Templates are production-validated and ready for use.

## Using This Repository

**Philosophy**: "Evidence-based patterns you can copy and adapt, not rules you must follow."

**Getting Started**:
1. **Browse** [templates/README.md](./templates/README.md) for overview
2. **Read** category READMEs to understand when/how to use each template
3. **Adapt** templates to your project structure and needs
4. **Validate** patterns work for your specific context

**For Context & Learning**:
- See [README.md](./README.md) for complete navigation

**Key References**:
- [New Project Setup](./docs/getting-started/NEW-PROJECT-SETUP.md) - Complete project setup guide
- [Built-in vs Custom](./docs/decisions/BUILTIN_VS_CUSTOM.md) - When to use built-in vs custom
- [Advanced Workflows](./docs/reference/ADVANCED-WORKFLOWS.md) - Power-user guide: context, planning, agents, extensions

**Don't**:
- Don't copy templates blindly without understanding context
- Don't treat these as rigid requirements
- Don't skip adaptation for your specific project

## Development Environment

**Secondary Purpose**: Development environment setup (platform-agnostic guides + optional WSL2 power setup for Windows).

**Quick Start**:
- **[docs/setup-guides/DAILY-WORKFLOW.md](./docs/setup-guides/DAILY-WORKFLOW.md)** - ⭐ Daily workflow guide
- **[docs/decisions/why-wsl.md](./docs/decisions/why-wsl.md)** - Why we use WSL (architectural decision)

**Setup Guides**:
- **[docs/getting-started/SETUP-GUIDE-2026.md](./docs/getting-started/SETUP-GUIDE-2026.md)** - Platform-agnostic setup (Mac, Windows, Linux)
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

## Important Notes

1. **This is a template library** - Not an environment setup guide (that's secondary)
2. **Evidence-based** - All patterns validated across 239+ commits in production repos
3. **Adapt, don't copy** - Templates are starting points, not rigid requirements
4. **Team resource** - Intended for team use and public community contribution
5. **Living documentation** - Continuously updated based on real-world usage
