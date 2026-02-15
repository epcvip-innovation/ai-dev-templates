# AI Assistant Workflow Guide

**Purpose:** This guide provides a comprehensive overview of the AI-assisted development workflow, including the available commands, development cycle, and best practices.

---

## 🚀 The Development Cycle

This workflow is structured around a feature-centric development cycle that leverages AI at every stage.

### 1. Planning Phase
- **Goal:** Define and prioritize what to build.
- **Process:** Features are added to `backlog/_BACKLOG.md`, prioritized, and estimated.
- **Key Command:** `/start-feature` initiates this process.

### 2. Preparation & Design Phase
- **Goal:** For complex features, create a detailed, high-quality plan before coding.
- **Process:** A feature-specific `plan.md` is created, architectural approaches are evaluated, and the plan is validated against a quality rubric.
- **Key Commands:** `/plan-approaches`, `/validate-plan`.

### 3. Active Development Phase
- **Goal:** Implement the feature, managing state and context across sessions.
- **Process:** Code is written, tasks are added or adjusted, and progress is tracked in a `HANDOFF.md` file to ensure continuity for the AI.
- **Key Commands:** `/add-task`, `/session-handoff`, `/check-drift`.

### 4. Quality & Debugging Phase
- **Goal:** Ensure code quality and robustly fix issues.
- **Process:** Code is reviewed against standards, and a structured, hypothesis-driven process is used to debug test failures.
- **Key Commands:** `/ai-review`, `/debug-failure`.

### 4.5. Feature Audit Phase (NEW)
- **Goal:** Comprehensive verification that the feature was implemented correctly.
- **Process:** Multi-lens review covering business logic, security, regression risk, and optionally domain-specific lenses (experiment integrity, data contracts).
- **Key Commands:** `/audit-feature`, `/audit:business`, `/audit:security`, `/audit:regression`.
- **Domain-specific (optional):** `/audit:experiment`, `/audit:data-contract`.
- **Stop Rule:** Max 3 High + 5 Medium findings per lens to prevent infinite review loops.

### 5. Completion Phase
- **Goal:** Finalize the feature with proper cleanup and documentation.
- **Process:** The feature is marked as complete, temporary files are archived, and the backlog is updated.
- **Key Commands:** `/feature-complete`, `/audit-artifacts`.

---

## 📞 Available Commands

All commands are stored as markdown files in this directory (`.claude/commands/`). Use `/help` for a quick, dynamically generated list.

### Feature Lifecycle Commands
- **`/start-feature [name]`**: Start a new feature from the backlog. Guides you through planning and setup.
- **`/resume-feature [name]`**: Resume work on an in-progress feature after a break by loading its context.
- **`/feature-complete`**: Run a checklist to complete a feature, including cleanup, archiving, and doc updates.
- **`/session-handoff`**: Create/update the `HANDOFF.md` file to ensure context continuity for the next session.

### Planning & Design Commands
- **`/plan-approaches`**: Evaluate 3 distinct architectural approaches for a task before implementation.
- **`/validate-plan`**: Validate a feature plan against the project's quality rubric to catch issues early.
- **`/add-task [description]`**: Add a newly discovered task to the current feature plan systematically.
- **`/check-drift`**: Detect drift between the original plan and the current implementation reality.

### Code & Query Commands
- **`/build-query`**: Build a new SQL query from a natural language description, following a strict validation workflow.
- **`/enhance-query [path]`**: Enhance an existing SQL query with new features.

### Quality & Maintenance Commands
- **`/ai-review`**: Perform a holistic AI code review against project standards and best practices.
- **`/debug-failure`**: Debug a test failure using a structured, hypothesis-driven process.
- **`/audit-artifacts`**: Perform a deep cleanup of temporary or exploratory markdown files to reduce clutter.

### Feature Audit Commands (NEW)
- **`/audit-feature`**: Unified feature audit with bounded multi-lens review. Quick mode (default) or `--deep` for comprehensive analysis.
- **`/audit:business`**: Business logic walkthrough - invariants, edge cases, intent verification.
- **`/audit:security`**: Security audit - threat modeling, abuse cases, vulnerability detection.
- **`/audit:regression`**: Regression surface analysis - what else could break from this change.
- **`/audit:experiment`**: (Domain-specific) Experiment integrity - bucketing, logging, attribution, sample ratio.
- **`/audit:data-contract`**: (Domain-specific) Data contract compliance - payload drift, PII handling, fallback behavior.

### Utility Commands
- **`/help`**: Display a list of all available slash commands and their descriptions.

---

## 📁 Backlog File Structure

The core of this workflow resides in the `backlog/` directory at project root.

```
backlog/
├── _BACKLOG.md                  # Main backlog (underscore sorts first)
├── _TEMPLATE.md                 # Template for feature plans (YAML frontmatter)
├── _SUBSYSTEM_BACKLOG.md        # Optional: subsystem-specific backlogs
└── [feature-name]/              # Directory for a specific feature
    ├── plan.md                  # Feature plan with YAML frontmatter
    └── HANDOFF.md               # Session continuity document
```

**Feature plans use YAML frontmatter:**
```yaml
---
id: feature-name
title: Human Readable Title
status: in_progress    # planned | in_progress | complete | on_hold
priority: P1           # P0 | P1 | P2 | P3
effort_estimate: 8h
effort_actual: 4h
started: 2026-01-09
completed: null
---
```

### Active Features Tracking

Active features are discovered by scanning `backlog/*/plan.md` files and reading YAML frontmatter.

**How it works:**
1. Scan `backlog/` for feature directories (folders not starting with `_`)
2. Read `plan.md` frontmatter in each directory
3. Features with `status: in_progress` are active

**Discovery script:**
```bash
python3 .claude/utils/feature_discovery.py
```

Returns JSON:
```json
{
  "count": 2,
  "active_features": [
    {"id": "session-auth", "status": "in_progress", "effort_estimate": "12h"},
    {"id": "query-reorg", "status": "in_progress", "effort_estimate": "3h"}
  ]
}
```

**No manual index file needed** - frontmatter is the source of truth.

---

## 🛠️ Python Utility Scripts

This workflow includes Python utility scripts in `.claude/utils/` that enforce consistent behavior for slash commands.

**Why utilities?** Claude can sometimes ignore markdown instructions (e.g., "use grep only" but reads full file anyway). Python scripts programmatically enforce the correct behavior, making workflows predictable and testable.

### Available Utilities

- **`feature_discovery.py`** - Discovers active features by scanning `backlog/*/plan.md` frontmatter
- **`handoff_loader.py`** - Loads only the selected feature's context (HANDOFF.md + plan.md)
- **`plan_validator.py`** - Validates plans without loading full PLAN_QUALITY_RUBRIC.md
- **`active_features_manager.py`** - (Deprecated) Previously managed `.active-features` index - now use frontmatter

**Key Benefits:**
- ✅ Enforces correct behavior (can't be ignored like markdown instructions)
- ✅ Structured JSON output for reliable parsing
- ✅ Context savings: 50-90% reduction in token usage
- ✅ Testable and debuggable

**See `.claude/utils/README.md` for detailed documentation.**

---

## 📋 HANDOFF.md Requirements

For feature discovery to work correctly, **HANDOFF.md files MUST include a Status line in the first 10 lines:**

```markdown
# Handoff: [Feature Name]

**Last Updated**: [Date/Time]
**Session**: [Session number or description]
**Status**: [Brief status - e.g., "Phase 2 in progress", "Ready to start Phase 3"]

## Quick Resume (Read This First)
...
```

The `**Status:**` line is validated by `.claude/utils/feature_discovery.py` and `.claude/utils/handoff_loader.py`. If missing or malformed, you'll receive a warning (not an error - validation only, no auto-fixing).

---

## 💡 Core Principles & Best Practices

- **Tier-Based Planning:** Features are sized into Tiers.
  - **Tier 1 (≤6 hours):** Use a lightweight `README.md` for planning. Fast and efficient.
  - **Tier 2 (7-15 hours):** Use a full `plan.md` and `HANDOFF.md`. Requires detailed planning.
  - **Tier 3 (>15 hours):** **Do not start.** Break it down into smaller Tier 1 or 2 features first.
- **Session Handoffs are Critical:** For any multi-session task, updating `HANDOFF.md` is the most important step before pausing work. It's the key to effective AI collaboration over time.
- **Parallel Work is Supported:** The per-feature directory structure allows multiple developers (or multiple AI instances) to work on different features simultaneously without merge conflicts in planning files.
- **Embrace the Commands:** Using the slash commands ensures that the structured, quality-driven processes are followed. They are the "guardrails" of this workflow.

---

## 🔍 Feature Audit Workflow

The `/audit-feature` command provides a layered review funnel to verify features are implemented correctly.

### Audit Philosophy

1. **Layered Review**: Different failure modes need different reviewers (security vs business logic vs regression)
2. **Bounded Severity**: Stop conditions prevent infinite adversarial review loops
3. **Learnings Capture**: Recurring issues become enforceable rules over time

### Stop Rules (Critical)

Every audit lens enforces:
- **Max 3 Critical/High** issues per lens
- **Max 5 Medium** issues (combined)
- **Theme Grouping**: If >5 similar issues, group into one theme with representative example

### Available Lenses

| Lens | Command | When to Use |
|------|---------|-------------|
| **Quick Audit** | `/audit-feature` | Default - runs all core lenses |
| **Business Logic** | `/audit:business` | Complex feature logic, monetization rules |
| **Security** | `/audit:security` | Auth, payments, PII, user input |
| **Regression** | `/audit:regression` | Refactors, shared code changes |
| **Experiment** | `/audit:experiment` | A/B tests, bucketing (domain-specific) |
| **Data Contract** | `/audit:data-contract` | API changes, PII handling (domain-specific) |

### Recommended Workflow

```
1. Complete feature implementation
2. Run /audit-feature for quick multi-lens review
3. Address Critical/High issues
4. Run /audit-feature --deep for fresh session review (optional)
5. Run /feature-complete to finalize
```

### Pre-Commit Hook (Optional)Install `audit-precommit.py` for automatic checks before every commit:
- Blocks on Critical issues (SQL injection, hardcoded secrets)
- Warns on High issues (console.log, print statements)
- See `templates/hooks/examples/audit-precommit/` for setup
