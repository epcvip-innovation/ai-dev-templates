# AI Assistant Workflow Guide

**Purpose:** This guide provides a comprehensive overview of the AI-assisted development workflow, including the available commands, development cycle, and best practices.

---

## 🚀 The Development Cycle

This workflow is structured around a feature-centric development cycle that leverages AI at every stage.

### 1. Planning Phase
- **Goal:** Define and prioritize what to build.
- **Process:** Features are added to `docs/planning/FEATURES_BACKLOG.md`, prioritized, and estimated.
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

### Utility Commands
- **`/help`**: Display a list of all available slash commands and their descriptions.

---

## 📁 Planning File Structure

The core of this workflow resides in the `docs/planning/` directory.

```
docs/planning/
├── FEATURES_BACKLOG.md          # Single source of truth for all features
├── archive/                     # Historical sprint/feature archives
└── features/
    ├── _TEMPLATE.md             # Template for full feature plans
    └── [feature-name]/          # Directory for a specific feature
        ├── plan.md              # The detailed specification (for complex features)
        ├── README.md            # A lightweight plan (for simple features)
        ├── HANDOFF.md           # Session continuity document
        └── archive/             # Archive of past session notes for this feature
```

### Active Features Tracking

The `.active-features` file at the project root serves as a lightweight index of features currently in progress:

```
.active-features                 # Auto-maintained index (DO NOT EDIT MANUALLY)
.claude/utils/
└── active_features_manager.py   # CLI tool for managing the index
```

**Purpose:** Minimize context usage during feature discovery (50-300 tokens vs 1000+ with grep).

**How it works:**
1. `/start-feature` automatically adds features to the index
2. `/feature-complete` automatically removes them
3. Feature discovery reads this file first (fallback to FEATURES_BACKLOG.md grep if missing)

**Manual management (if needed):**
```bash
# List active features
python3 .claude/utils/active_features_manager.py list

# Check if a feature is active
python3 .claude/utils/active_features_manager.py is-active "feature-name"

# Manually add (rarely needed)
python3 .claude/utils/active_features_manager.py add "feature-name"

# Manually remove (rarely needed)
python3 .claude/utils/active_features_manager.py remove "feature-name"
```

---

## 🛠️ Python Utility Scripts

This workflow includes Python utility scripts in `.claude/utils/` that enforce consistent behavior for slash commands.

**Why utilities?** Claude can sometimes ignore markdown instructions (e.g., "use grep only" but reads full file anyway). Python scripts programmatically enforce the correct behavior, making workflows predictable and testable.

### Available Utilities

- **`feature_discovery.py`** - Discovers active features from `.active-features` file (primary) or FEATURES_BACKLOG.md using grep (fallback)
- **`handoff_loader.py`** - Loads only the selected feature's context (HANDOFF.md + plan.md)
- **`plan_validator.py`** - Validates plans without loading full PLAN_QUALITY_RUBRIC.md
- **`active_features_manager.py`** - Manages `.active-features` index file

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

