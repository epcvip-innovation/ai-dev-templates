# AI-Assisted Development Slash Command Templates

**Purpose:** Reusable, battle-tested slash command templates to bootstrap structured AI workflows.

**Updated:** January 2026 - Streamlined based on real-world usage patterns.

---

## Streamlined Command Set (Jan 2026)

After 6+ months of real-world usage, we've streamlined this template to focus on commands that provide genuine value vs. those superseded by Claude Code's built-in features.

### Active Commands (9 total)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/audit-feature` | Comprehensive feature/code quality audit | Before commits, before PRs |
| `/audit-claude-md` | Check CLAUDE.md for bloat | Quarterly maintenance |
| `/audit-artifacts` | Audit project artifacts and deliverables | Project milestones |
| `/ai-review` | Quick code quality check | During development |
| `/plan-approaches` | Score architectural options | Early design phase |
| `/debug-failure` | Structured debugging workflow | Test failures, bugs |
| `/align-project-docs` | Sync documentation across project | After major changes |
| `/help` | List available commands | Discovery |
| `/push` | Safe commit workflow | Every commit |

### Deprecated Commands (in `_deprecated/`)

These commands were useful but are now superseded by Claude Code built-in features:

| Command | Reason | Replacement |
|---------|--------|-------------|
| `start-feature` | Claude's built-in plan mode | `/plan` or `/feature-dev:feature-dev` plugin |
| `resume-feature` | Built-in plan restoration | Native session management |
| `session-handoff` | Auto-compact improvements | Built-in memory management |
| `feature-complete` | Superseded | Built-in plan mode |
| `validate-plan` | Superseded | `/plan` mode validation |
| `add-task` | Rarely used | TodoWrite tool |
| `check-drift` | Not used | Inline in /audit |
| `audit/*` | Better as plugin agents | code-review plugin agents |

**Note:** Deprecated commands remain available for reference or projects that prefer manual workflows.

---

## Available Workflow Templates

### 1. AI Development Workflow (Core)
Quality gates and structured development patterns.

- **[View AI Dev Workflow Guide](./ai-dev-workflow/WORKFLOW_GUIDE.md)**
- **Copy to:** `.claude/commands/` in your project

**Active commands (9 total):**
- Quality: `/audit-feature`, `/audit-claude-md`, `/audit-artifacts`, `/ai-review`
- Design: `/plan-approaches`
- Documentation: `/align-project-docs`
- Debugging: `/debug-failure`
- Git workflow: `/push`
- Discovery: `/help`

### 2. Query Building Workflow (Domain-Specific)
Specialized commands for SQL query generation and validation.

- **Location:** `./query-building-workflow/commands/`
- **Copy to:** `.claude/commands/query/` in your project

**Contains:**
- `/query:build-query` - Build new queries from natural language
- `/query:enhance-query` - Enhance existing queries
- `/query:generate-query` - Template-based query generation

---

## Key Insight: Plugins > Slash Commands

Based on real-world usage, we recommend:

1. **Use built-in features first** - Claude Code's `/plan` mode, TodoWrite, and session management
2. **Use plugins for workflows** - Plugins support auto-triggers, hooks, and sub-tasks that can't be ignored
3. **Use slash commands for utilities** - Quality gates (`/audit`), debugging (`/debug-failure`), git (`/push`)

See [`../plugins/`](../plugins/) for plugin templates including:
- `code-review` - Multi-agent adversarial code review
- `backlog-management` - Backlog dashboard and management skills

---

## 🧠 Design Rationale and Philosophy

The design documentation explains the "why" behind these workflows.

- **[Read the Design Rationale](./DESIGN_RATIONALE.md)**

---

## 🚀 Quick Start

**Recommended approach (Jan 2026):**
1. Copy active commands from `ai-dev-workflow/commands/` to `.claude/commands/`
2. Skip deprecated commands unless you have specific needs
3. Consider using plugins from `../plugins/` for workflow automation
4. Start with `/help` to see available commands

**For query-focused projects:**
- Use query-building-workflow as your starting point
- Add specific ai-dev-workflow commands as needed
