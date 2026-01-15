# AI Slash Command Workflow: Design Rationale

**Purpose:** This document captures the "why" behind the AI-assisted development workflow. It serves as a historical and philosophical guide to the system, intended for the maintainer of the template (you) rather than for end-users of the commands.

---

## Core Philosophy: Structured Collaboration

The fundamental goal of this workflow is to transform the interaction with an AI assistant from a simple, conversational back-and-forth into a structured, predictable, and robust collaboration.

**Core Principles:**
- **Explicit over Implicit:** We favor manual triggers (`/slash-commands`) over automatic behaviors (like Claude Skills). This ensures the developer is always in control.
- **Process over Prompts:** Instead of relying on one-off prompts, we define reusable, battle-tested "Standard Operating Procedures" (SOPs) for the AI to follow for every key development task.
- **Full Lifecycle Integration:** The AI is leveraged across the entire development lifecycle—from planning and architecture to debugging and completion—not just for code generation.
- **Active Context Management:** We explicitly manage the AI's limited context window using a `session-handoff` and `resume-feature` cycle, solving the problem of state loss between sessions.
- **Built-in Quality Gates:** Quality is not an afterthought. Commands like `/validate-plan`, `/check-drift`, and `/ai-review` embed quality assurance directly into the workflow.

---

## Evolution of the Workflow

This workflow has evolved through several iterations, incorporating lessons learned from real-world projects.

### V1: Fragmented Commands
- The initial template consisted of ~6 core commands, organized into a complex, multi-level folder structure (`analysis/`, `quality/`, etc.).
- **Lesson:** This structure was too complicated and didn't map to how Claude Code discovers commands. The documentation was scattered across multiple `README.md` files, making it hard to get a holistic view.

### V2: Centralized & Polished (The `data-query-tool` version)
- **Key Change:** We consolidated all commands into a single `.claude/commands/` directory.
- **Subfolder Discovery:** Through experimentation (our conversation on Nov 16, 2025), we discovered that Claude Code supports a `folder:command` syntax, allowing for a much cleaner organization (e.g., `query/build-query.md` becomes `/query:build-query`). This is the superior organizational model.
- **New Capabilities:** We added several critical commands:
    - `/help`: A dynamic command to improve discoverability.
    - `/debug-failure`: A sophisticated, Socratic method for debugging that prevents the AI from taking lazy shortcuts.
- **Reliability Fixes:** We added `pwd` pre-flight checks to filesystem-heavy commands after an "after-action review" revealed the AI could get confused about its current working directory.

### V3: Template/Design Separation
- **Key Change:** We recognized the need to separate the "deployable" template from the "design" documentation.
- **`template/` folder:** Contains the clean, copy-paste-ready commands for bootstrapping a new project.
- **`design/` folder:** Contains this document—the history, philosophy, and rationale that is essential for the template's maintainer but is unnecessary clutter for a project using the template.

### V4: Streamlined Commands (January 2026)
- **Key Change:** After 6+ months of real-world usage (esp. fwaptile-wordle project), we identified which commands provide genuine value vs. those superseded by Claude Code built-in features.

**Deprecation decisions:**
| Command | Real-world finding | Action |
|---------|-------------------|--------|
| `start-feature` | Claude's built-in `/plan` mode does this better | Deprecated |
| `resume-feature` | Built-in plan files + session management | Deprecated |
| `session-handoff` | Auto-compact improvements reduce need | Deprecated |
| `add-task` | TodoWrite tool is more flexible | Deprecated |
| `check-drift` | Not used in practice | Deprecated |
| `audit/*` sub-commands | Better as plugin agents with sub-tasks | Deprecated |

**New insight: Plugins > Slash Commands**
- Plugins support auto-triggers based on natural language
- Plugin sub-tasks can't be ignored (unlike optional slash commands)
- Plugin hooks provide lifecycle control

**Commands retained:**
- `/audit-feature` - Still valuable for comprehensive quality checks
- `/push` - Critical for safe commit workflows (added in V4)
- `/debug-failure` - Unique Socratic debugging approach
- `/plan-approaches` - Useful for early design exploration

---

## Key Design Decisions & Rationale

### `session-handoff` vs. `/compact`
- **Problem:** Claude Code's native `/compact` command is a black box. It's unclear what context is preserved, and community consensus is that it's unreliable.
- **Solution:** We created `/session-handoff`. This is an explicit, transparent process where we decide what to archive (verbose implementation details) and what to keep (summaries and next steps). The output is a structured `HANDOFF.md` file.
- **Benefit:** This "Document & Clear" method provides 100% reliable context restoration, enabling effective multi-session work. The cost is negligible (~$0.03 per cycle) for a massive gain in reliability.

### `/debug-failure`: The Socratic Debugger
- **Problem:** When faced with a failing test, AI assistants often take shortcuts. They might hack the test to make it pass or fix the symptom without understanding the root cause.
- **Solution:** The `/debug-failure` command forbids the AI from immediately proposing a fix. It *must* first analyze the failure, present a ranked list of hypotheses with supporting evidence, and propose a minimal, non-invasive "verification step" (e.g., adding a log). Only after the user confirms the hypothesis does the AI proceed with a targeted fix.
- **Benefit:** This forces a robust, first-principles approach to debugging, leading to more reliable fixes.

### Naming Convention (`/query:build`) vs. Prefixes (`/query-build`)
- **Initial Hypothesis:** We initially believed subfolders were not supported and planned to use a prefix-based naming convention for organization.
- **Discovery:** Your screenshot on Nov 16, 2025, provided definitive proof that the `folder:command` syntax works.
- **Decision:** The folder-based organization is superior as it's cleaner and more scalable. We updated the `/help` command to correctly parse this structure.
