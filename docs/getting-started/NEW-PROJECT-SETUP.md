# New Project Setup Guide

One-stop reference for setting up Claude Code workflows in a new project.

**Updated**: January 2026 (Claude Code v2.1.x)

> **Prerequisites**: Claude Code must be installed and authenticated.
> Run `claude --version` to verify. If not installed, see [Quickstart](./CLAUDE-CODE-QUICKSTART.md) first (5 min).

---

## Quick Start (30 minutes)

> **Starting fresh?** See [TECH_STACK_DEFAULTS.md](./TECH_STACK_DEFAULTS.md) for recommended tech choices.

### Step 1: CLAUDE.md (5 min)

Create a hub CLAUDE.md file (100-200 lines max):

```markdown
# Project Name

## Purpose
Brief description of what this project does.

## Tech Stack
- Framework: [Next.js/React/etc.]
- Language: [TypeScript/Python/etc.]
- Database: [Postgres/etc.]

## Critical Warnings
- Never commit .env files
- Always run tests before pushing

## Key Commands
- `npm run dev` - Start development server
- `npm run test` - Run tests
- `npm run build` - Production build

## Navigation
- [Architecture](docs/ARCHITECTURE.md)
- [Backlog](backlog/_INDEX.md)
```

**Template**: [templates/claude-md/](../../templates/claude-md/README.md)

---

### Step 2: Permissions & Security (5 min)

Create `.claude/settings.json` for auto-approvals and safety deny rules:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Read",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(git push --force *)",
      "Read(.env)",
      "Read(.env.*)"
    ]
  }
}
```

For team projects, consider adding hooks for runtime command validation and bypass prevention. See the [security templates](../../templates/security/README.md) for three tiers of protection.

**Templates**: [Permissions](../../templates/permissions/README.md) | [Security](../../templates/security/README.md)

---

### Step 3: MCP Servers (10 min)

Create `.mcp.json` for project-specific tools:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest", "--no-sandbox"]
    }
  }
}
```

Common MCP servers:
- **Playwright** - Browser automation, E2E testing
- **Fetch** - HTTP requests
- **Filesystem** - Extended file operations

**Reference**: [Playwright MCP Guide](../mcp/playwright/README.md)

---

### Step 4: Built-in Skills (10 min)

These are available immediately - no setup required. Just know they exist:

| Skill | Trigger | Purpose |
|--------|---------|---------|
| `/feature-dev:feature-dev` | `/feature-dev`, "implement X" | Guided feature development |
| `/local-review` | `/local-review`, "review changes" | 5-agent adversarial review (`--quick` for 3-agent fast mode) |
| `/code-review:code-review` | `/code-review [URL]` | PR code review |

**That's it for Quick Start!** Your project is now ready for AI-assisted development.

---

## Full Setup (2+ hours)

Continue with these steps for production projects or team workflows.

---

### Step 5: Custom Skills — Flat-File Format (30 min)

Copy essential skill templates to `.claude/commands/` (flat-file skill format):

```bash
mkdir -p .claude/commands
# Copy from templates
cp templates/slash-commands/ai-dev-workflow/commands/push.md .claude/commands/
cp templates/slash-commands/ai-dev-workflow/commands/audit.md .claude/commands/
```

**Essential skills:**
- `/push` - Safe commit with quality checks
- `/audit` - Project health check

**Template**: [templates/slash-commands/](../../templates/slash-commands/README.md)

---

### Step 6: Custom Skills (1 hour)

Skills auto-trigger on natural language. Copy to `.claude/skills/`:

```bash
mkdir -p .claude/skills
# Copy code review skill with project context
cp -r templates/skills/code-review .claude/skills/
```

**Essential skill:** Code review with `review-context.md`

Create `.claude/review-context.md` to reduce false positives:

```markdown
# Project Review Context

## App Scale
- Internal tool, <100 users, Production

## Data Trust Model
- **Database queries**: TRUSTED - ORM with parameterized queries
- **Environment variables**: TRUSTED - Developer-controlled
- **User input**: UNTRUSTED - Validate all request bodies

## Known Exceptions
- `lib/legacy/*.ts` - Legacy code, lower priority
```

**Template**: [templates/skills/](../../templates/skills/README.md)

---

### Step 7: Backlog System (30 min)

Choose your approach:

| Approach | Best For | Setup |
|----------|----------|-------|
| **Simple** | <10 items, solo | Single `_BACKLOG.md` file |
| **Folder-based** | 10+ items, team | Type directories + Python utilities |

**Simple (5 min):**
```bash
mkdir -p backlog
cp templates/project-management/backlog/_BACKLOG.md backlog/
cp templates/project-management/backlog/_TEMPLATE.md backlog/
```

**Folder-based (30 min):**
```bash
mkdir -p backlog/{feature,bug,tech-debt,research}
mkdir -p .claude/utils
cp -r templates/project-management/backlog/folder-based/* backlog/
cp templates/project-management/backlog/folder-based/utils/* .claude/utils/
```

**Template**: [templates/project-management/](../../templates/project-management/README.md)

---

### Step 8: CI/CD Integration (Optional)

Add GitHub Actions for automated reviews:

```bash
mkdir -p .github/workflows
cp templates/ci/security-review.yml .github/workflows/
```

| Template | Trigger | Est. Cost/PR |
|----------|---------|--------------|
| `security-review.yml` | Every PR | $0.10-0.30 |
| `claude-qa-workflow.yml` | Path-specific | $0.50-1.50 |
| `risk-preflight.yml` | PR risk tier | $0.10-1.50 (varies by tier) |

For team projects with sensitive code paths (auth, payments, PII), `risk-preflight.yml` classifies PRs by risk tier so docs-only changes skip expensive reviews. See [RISK-GATING.md](../../templates/ci/RISK-GATING.md).

**Framework**: [templates/ci/DECISION_FRAMEWORK.md](../../templates/ci/DECISION_FRAMEWORK.md)

---

## Built-in Skills Reference

| Skill | Trigger | Purpose |
|--------|---------|---------|
| `/feature-dev` | "implement X", `/feature-dev` | Guided feature development with architecture focus |
| `/local-review` | "review changes", `/local-review` | 5-agent adversarial code review (`--quick` for 3-agent fast mode) |
| `/code-review [URL]` | `/code-review 123` | Review existing pull requests |

All built-in — no setup required. For detailed agent descriptions, trigger patterns, and customization options, see [templates/skills/README.md](../../templates/skills/README.md).

---

## Setup Checklists

### Minimal (30 min) - Recommended Start

- [ ] Create CLAUDE.md with project purpose and tech stack
- [ ] Create `.claude/settings.json` with permissions + deny rules (Tier 1 security)
- [ ] Verify built-in skills work (`/local-review --quick`)

### Standard (1-2 hours) - Production Projects

- [ ] All minimal steps
- [ ] Configure `.mcp.json` for Playwright (if web project)
- [ ] Add `/push` command with project-specific quality gates
- [ ] Create `.claude/review-context.md` for code review tuning
- [ ] Create simple backlog (`_BACKLOG.md`)

### Full (4+ hours) - Long-term/Team Projects

- [ ] All standard steps
- [ ] Set up folder-based backlog with Python utilities
- [ ] Install custom skills (backlog-dashboard, add-backlog, backlog-complete)
- [ ] Configure CI/CD with GitHub Actions
- [ ] (Team) Add Tier 2 security: hooks + deny/allow conf files (see [security templates](../../templates/security/README.md))
- [ ] (Team) Configure risk-gated CI (see [RISK-GATING.md](../../templates/ci/RISK-GATING.md))
- [ ] Document architecture in spoke files

---

## Decision Guide

| Level | Setup Time | Best For |
|-------|------------|----------|
| Built-in only | 0 min | Quick prototypes, learning |
| Minimal | 30 min | Most projects |
| Standard | 1-2 hours | Production projects |
| Full | 4+ hours | Long-term, team projects |

**Detailed guidance**: [docs/decisions/BUILTIN_VS_CUSTOM.md](../decisions/BUILTIN_VS_CUSTOM.md)

---

## File Structure Reference

```
your-project/
├── CLAUDE.md                    # Hub (100-200 lines)
├── .mcp.json                    # MCP server config
├── .claude/
│   ├── settings.json            # Permissions
│   ├── commands/                # Skills (flat-file format)
│   │   ├── push.md
│   │   └── audit.md
│   ├── skills/                  # Custom skills
│   │   ├── code-review/
│   │   │   └── SKILL.md
│   │   └── backlog-dashboard/
│   │       └── SKILL.md
│   ├── utils/                   # Python utilities
│   │   ├── backlog_index.py
│   │   ├── backlog_validate.py
│   │   └── backlog_search.py
│   ├── hooks/                   # Security hooks (Tier 2+)
│   └── review-context.md        # Code review tuning
├── backlog/                     # If using folder-based backlog
│   ├── _INDEX.md                # Auto-generated
│   ├── _TEMPLATE.md
│   ├── _ARCHIVE.md
│   ├── feature/
│   │   └── my-feature/
│   │       └── plan.md
│   ├── bug/
│   ├── tech-debt/
│   └── research/
├── .github/
│   └── workflows/               # CI/CD
│       ├── security-review.yml
│       └── # risk-preflight.yml  (team projects — see RISK-GATING.md)
└── docs/
    └── ARCHITECTURE.md          # Spoke document
```

---

## Workflow After Setup

### Daily Development

```
1. Start session: claude
2. Check backlog: "show backlog" or /backlog
3. Start feature: /feature-dev or "help me implement X"
4. Code...
5. Review: /local-review --quick (quick) or /local-review (thorough)
6. Push: /push
7. Complete: "finished with [feature]"
```

### Backlog Workflow (Folder-based)

```
/backlog → /backlog start [id] → [code] → /push → /backlog complete [id]
```

---

## See Also

- [TECH_STACK_DEFAULTS.md](./TECH_STACK_DEFAULTS.md) - Preferred tech choices for new projects
- [templates/claude-md/](../../templates/claude-md/README.md) - CLAUDE.md templates
- [templates/slash-commands/](../../templates/slash-commands/README.md) - Command templates
- [templates/skills/](../../templates/skills/README.md) - Skill templates
- [templates/project-management/](../../templates/project-management/README.md) - Task & backlog management
- [templates/permissions/](../../templates/permissions/README.md) - Permission templates
- [templates/security/](../../templates/security/README.md) - AI agent security (3 tiers)
- [docs/decisions/BUILTIN_VS_CUSTOM.md](../decisions/BUILTIN_VS_CUSTOM.md) - When to customize

---

**Last Updated**: 2026-01-15
