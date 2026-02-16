# AI-Assisted Development Slash Command Templates

**Purpose:** Reusable, battle-tested slash command templates to bootstrap structured AI workflows.

**Updated:** February 2026 - Un-deprecated custom commands; documented tradeoffs vs built-in features.

---

## Command Reference (21 total)

All commands live in `ai-dev-workflow/commands/` and are organized by workflow phase:

| Phase | Command | Purpose |
|-------|---------|---------|
| **Lifecycle** | `/start-feature` | Create project structure with backlog integration + YAML frontmatter |
| | `/resume-feature` | Resume work using HANDOFF.md structured context |
| | `/feature-complete` | Archive completed feature with summary |
| | `/session-handoff` | Explicit, reviewable context preservation |
| **Planning** | `/plan-approaches` | Score architectural options (1-10 anti-slop scale) |
| | `/validate-plan` | Validate plan against PLAN_QUALITY_RUBRIC |
| | `/add-task` | Add task to plan.md with frontmatter metadata |
| | `/check-drift` | Automated plan-vs-implementation comparison |
| **Quality** | `/ai-review` | Quick code quality check |
| | `/debug-failure` | Socratic debugging workflow (no lazy shortcuts) |
| | `/audit-feature` | Comprehensive feature/code quality audit |
| | `/audit-artifacts` | Audit project artifacts and deliverables |
| | `/audit-claude-md` | Check CLAUDE.md for bloat |
| **Audit Lenses** | `/audit:business` | Business impact analysis |
| | `/audit:security` | Security vulnerability scan |
| | `/audit:regression` | Regression risk assessment |
| | `/audit:experiment` | A/B test design review |
| | `/audit:data-contract` | Data contract validation |
| **Git** | `/push` | Safe commit workflow with quality gates |
| | `/align-project-docs` | Sync documentation across project |
| **Utility** | `/help` | List available commands |

---

## Custom Commands vs Built-in Features

This repo demonstrates **both** custom slash commands and built-in Claude Code features. Each has strengths:

| Task | Custom Command | Built-in Alternative | When Custom Wins |
|------|---------------|---------------------|------------------|
| Start a feature | `/start-feature` | `/plan` mode | Backlog integration + YAML frontmatter + `.projects/` scaffolding |
| Resume work | `/resume-feature` | Session restore | HANDOFF.md structured context with explicit scope boundaries |
| Session handoff | `/session-handoff` | Auto-compact | Explicit, reviewable context preservation (100% reliable restoration) |
| Validate plan | `/validate-plan` | `/plan` mode | Enforces a PLAN_QUALITY_RUBRIC with scored criteria |
| Add task | `/add-task` | Native Tasks (TaskCreate) | Persists in plan.md with frontmatter metadata (cross-session) |
| Check drift | `/check-drift` | Manual review | Automated plan-vs-implementation diff comparison |
| Code review | `/audit-feature` | code-review plugin | Slash command for one-off audits; plugin for auto-triggered reviews |

**Guidance:**
- **Built-in features** are simpler to set up and maintained by Anthropic — use them when they cover your needs
- **Custom commands** shine when you need structured output formats, project-specific rubrics, or integration with your backlog/documentation system
- **Plugins** (see `../plugins/`) are best for workflows that should auto-trigger — they support hooks, sub-tasks, and natural language matchers

---

## Available Workflow Templates

### 1. AI Development Workflow (Core)
Quality gates and structured development patterns.

- **[View AI Dev Workflow Guide](./ai-dev-workflow/WORKFLOW_GUIDE.md)**
- **Copy to:** `.claude/commands/` in your project

### 2. Query Building Workflow (Domain-Specific)
Specialized commands for SQL query generation and validation.

- **Location:** `./query-building-workflow/commands/`
- **Copy to:** `.claude/commands/query/` in your project

**Contains:**
- `/query:build-query` - Build new queries from natural language
- `/query:enhance-query` - Enhance existing queries
- `/query:generate-query` - Template-based query generation

---

## Design Rationale and Philosophy

The design documentation explains the "why" behind these workflows.

- **[Read the Design Rationale](./DESIGN_RATIONALE.md)**

---

## Quick Start

1. Copy commands from `ai-dev-workflow/commands/` to `.claude/commands/`
2. Optionally copy audit lenses from `commands/audit/` to `.claude/commands/audit/`
3. Consider using plugins from `../plugins/` for auto-triggered workflows
4. Start with `/help` to see available commands

**For query-focused projects:**
- Use query-building-workflow as your starting point
- Add specific ai-dev-workflow commands as needed
