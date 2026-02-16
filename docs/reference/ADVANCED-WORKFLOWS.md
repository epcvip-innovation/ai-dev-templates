# Advanced Workflows: Context, Agents, Predictability & Strategy

[← Back to Main README](../../README.md)

Power-user guide for working effectively with Claude Code at scale. Covers the conceptual foundations that setup guides don't: how context windows actually work, when to use sub-agents, how to engineer predictable outputs, and how to choose models strategically.

**Audience**: Developers already comfortable with Claude Code who want to work more effectively on complex, multi-session projects.

---

## 1. Context Management at Scale

### What Fills the Context Window

Claude Code's 200k token context window fills from multiple sources simultaneously:

| Source | Typical Size | Notes |
|--------|-------------|-------|
| CLAUDE.md (all levels) | 1-3k tokens | Loaded every session |
| Files read with Read tool | 1-10k per file | Accumulates fast during exploration |
| Tool output (Bash, Grep, etc.) | 0.5-5k per call | Large outputs get truncated |
| MCP server definitions | 0.5-2k per server | Fixed overhead per configured server |
| Sub-agent results | 1-5k per agent | Summarized, not raw |
| Conversation history | Grows continuously | The biggest consumer |

**Key insight**: Performance degrades *before* you hit the ceiling. Research suggests quality drops noticeably past ~120k tokens due to attention diffusion — the model has more to attend to, so each piece gets less focus.

### Treat Context as a Budget, Not a Container

The wrong mental model: "I have 200k tokens, so I can keep going until I run out."

The right mental model: "Context is scarce memory in a constrained system. Every token I spend on exploration is a token unavailable for implementation."

**Practical implications**:
- Read targeted sections of files, not entire files when you know what you need
- Use Grep/Glob to find what you need before reading
- Summarize investigation findings before moving to implementation
- Close investigation threads explicitly ("I've found the issue in X, moving on")

### Externalizing State

The most important context management technique: **write things down in files instead of relying on conversation memory**.

| What to Externalize | Where | Why |
|---------------------|-------|-----|
| Current plan + steps | `plan.md` or `.claude/plans/` | Survives compaction, restartable |
| Key decisions made | `decisions.md` or CLAUDE.md | Won't be re-debated |
| Modified files list | `HANDOFF.md` | Critical for session continuity |
| Open questions | `plan.md` TODO section | Prevents silent drops |

**Pattern**: At the start of complex work, create a plan file. Update it as you go. This file becomes the source of truth that survives context compaction and session restarts.

### Auto-Compact: What Survives and What Doesn't

When context fills, Claude Code automatically compacts the conversation. Understanding what survives helps you work with it:

**Survives well**:
- Recent messages and tool calls
- CLAUDE.md content (reloaded fresh)
- Files currently open / recently read
- The current task or question

**Gets lost or degraded**:
- Early investigation findings
- Nuanced decisions from 50+ messages ago
- The "why" behind rejected approaches
- Intermediate reasoning steps

**Compact instructions in CLAUDE.md**: You can add a section to CLAUDE.md telling Claude what to preserve during compaction:

```markdown
## On Context Compaction
When compacting, preserve:
- Current goal and active plan file path
- List of files modified this session
- Key decisions made and their rationale
- Open TODOs and blockers
```

### When to Compact Deliberately

Use `/compact` proactively at natural breakpoints:

- **After investigation, before implementation** — You've explored the codebase, found the issue, now clear the investigation debris before writing code
- **Before large test runs** — Test output can flood context; start clean
- **Between phases** — Finished the API? Compact before starting the UI
- **After resolving tangents** — Got sidetracked debugging a dependency? Compact to refocus

---

## 2. Agents and Sub-Agents

### Why Sub-Agents Exist

The Task tool spawns isolated Claude instances (sub-agents) that work independently and return summarized results. Three key benefits:

1. **Isolated context** — The sub-agent gets a clean context window, free from your conversation's accumulated state
2. **Parallel work** — Multiple agents can run simultaneously on independent tasks
3. **Summarized output** — Instead of dumping 500 lines of grep results into your context, an agent reads them and returns a 20-line summary

### Common Patterns

**Explorer** (read-only codebase mapping):
- "Find all API endpoints and their authentication requirements"
- "Map the data flow from user input to database write"
- Model: haiku (fast, cheap, sufficient for pattern matching)

**Reviewer** (edge-case hunting):
- "Review these changes for security issues, focusing on input validation"
- "Check if this refactor breaks any existing callers"
- Model: sonnet or opus (needs reasoning depth)

**Implementer** (scoped changes):
- "Update all test files to use the new fixture pattern"
- "Add error handling to these 5 API endpoints following the pattern in users.ts"
- Model: sonnet (balances speed and quality)

### The Task Tool: How It Works

```
Main conversation                    Sub-agent
┌──────────────┐                    ┌──────────────┐
│ Your context  │ ── Task call ──→  │ Fresh context │
│ (may be full) │                   │ (clean 200k)  │
│               │ ←── Summary ───   │ Does work...  │
│ Gets ~1-5k    │                   │ Returns result │
│ token summary │                   └──────────────┘
└──────────────┘
```

**When to use agents**:
- Exploration that would generate lots of output (searching across many files)
- Parallel independent tasks (review security AND check tests simultaneously)
- When your context is already heavy and you need focused work done

**When NOT to use agents**:
- Simple, targeted searches (just use Grep/Glob directly)
- Tasks that need your conversation's full context
- Sequential work where each step depends on the previous

### Model Selection for Agents

| Agent Task | Recommended Model | Cost (Input/MTok) | Rationale |
|-----------|-------------------|-------------------|-----------|
| File scanning, pattern finding | haiku | $1.00 | Speed and cost; accuracy sufficient for search |
| Code review, bug hunting | sonnet | $3.00 | Needs reasoning but not deep architecture insight |
| Architecture decisions, complex refactors | opus | $5.00 | Worth the cost for critical decisions |

### Downsides to Know

- **Cost multiplier** — Each agent is a separate API call chain. 5 parallel agents = 5x the token cost of that work
- **Divergent edits** — Two agents modifying the same file will conflict. Assign non-overlapping scopes
- **No shared context** — Agent A doesn't know what Agent B found. You're the coordinator
- **Overhead** — For a 3-second Grep, spawning an agent adds 10-30 seconds of startup overhead

---

## 3. Engineering Predictability

### The Core Problem

LLM outputs are probabilistic. Ask the same question twice, get different answers. This is a feature for creative work and a liability for engineering workflows.

**Predictability must be engineered** — it doesn't emerge naturally from prompting alone.

### The Predictability Stack

From weakest to strongest enforcement:

```
Human checkpoints    ← Strongest (manual review at key moments)
Test gates           ← Strong (automated pass/fail)
Hooks                ← Strong (exit codes guarantee behavior)
Compact rules        ← Medium (survives context, but advisory)
Plan files           ← Medium (Claude follows, but can drift)
CLAUDE.md guidance   ← Weak-Medium (read every session, but advisory)
Prompt instructions  ← Weakest (can be forgotten mid-session)
```

### Hooks as the Primary Determinism Lever

Hooks are shell commands that run at workflow events. Unlike prompt instructions (which Claude *might* follow), hooks enforce behavior through exit codes:

- **Exit 0**: Allow the operation
- **Exit 2**: Block the operation (Claude sees the error message)

**This is deterministic**. No amount of prompt drift can bypass an exit code 2.

**Example**: Query validation hook ensures every database query is validated before execution. Claude can't "forget" this step — the hook physically blocks unvalidated queries.

**See**: [templates/hooks/README.md](../../templates/hooks/README.md) for implementation patterns.

### Reproducibility Techniques

Beyond hooks, these patterns improve consistency:

1. **Limit scope** — "Fix the null check in `processOrder()`" beats "improve error handling across the app"
2. **Explicit success criteria** — "Done when all 3 tests pass and the type error on line 47 is resolved"
3. **Verify before proceeding** — "Run the tests, show me the output, then move to the next file"
4. **Plan files as contracts** — Write the plan, get approval, execute against it. Drift is visible because the plan is written down

### When NOT to Enforce Predictability

Strict determinism is counterproductive for:
- **Exploration** — "What's in this codebase?" needs freedom to wander
- **Prototyping** — Rapid iteration benefits from creative latitude
- **Creative work** — UI design, naming, documentation tone
- **Learning** — Understanding unfamiliar code requires open-ended investigation

Match enforcement level to the task. Investigation gets loose reins; production deployment gets tight ones.

---

## 4. Strategic Model and Tool Usage

### Not All Models for All Tasks

The instinct to always use the most powerful model wastes money and sometimes speed:

| Task Type | Best Model | Why |
|-----------|-----------|-----|
| File scanning, simple searches | Haiku ($1/MTok in) | Speed matters, reasoning depth doesn't |
| Standard implementation | Sonnet ($3/MTok in) | Good balance of speed, quality, cost |
| Architecture, complex debugging | Opus ($5/MTok in) | Worth the premium for critical decisions |
| Browser automation (CI) | Haiku ($1/MTok in) | Same accuracy as Sonnet for browser tasks (61% OSWorld) |

**See**: [COST_OPTIMIZATION_GUIDE.md](../../templates/testing/COST_OPTIMIZATION_GUIDE.md) for detailed pricing and benchmarks.

### Context is Your Scarcest Resource

More valuable than tokens or money: **attention quality**. A clean 50k-token context outperforms a cluttered 150k-token context.

**Practical rules**:
- Start complex tasks with a fresh session (or `/compact`)
- Read only what you need, not "everything that might be relevant"
- Close investigative threads before opening new ones
- Externalize findings to files as you go

### The Dual-Tool Pattern

Running Claude Code and a second AI tool (Codex CLI, Cursor) simultaneously:

1. **Write in one, review in the other** — Different models catch different issues
2. **Competing approaches** — Ask both the same architecture question, compare answers
3. **Verification** — One tool implements, the other verifies the approach

**See**: [CODEX-SETUP.md](../setup-guides/CODEX-SETUP.md) for dual-tool workflow setup.

### Human Checkpoints Still Matter

AI accelerates development; it doesn't replace judgment. Insert human review at:

- **Architecture boundaries** — Before committing to a pattern that will propagate
- **Security-sensitive changes** — Auth, permissions, data access
- **Irreversible operations** — Database migrations, deployments, data deletions
- **Cross-system integration** — Where your code meets external systems

The cost of pausing to review is minutes. The cost of an unreviewed mistake can be hours or days.

---

## See Also

- [CLAUDE-MD-GUIDELINES.md](../../templates/claude-md/CLAUDE-MD-GUIDELINES.md) — Keeping CLAUDE.md lightweight
- [Hooks README](../../templates/hooks/README.md) — Workflow automation and enforcement
- [COST_OPTIMIZATION_GUIDE.md](../../templates/testing/COST_OPTIMIZATION_GUIDE.md) — Model pricing and testing costs
- [BUILTIN_VS_CUSTOM.md](../decisions/BUILTIN_VS_CUSTOM.md) — When to use built-in vs custom tooling
- [Plugins README](../../templates/plugins/README.md) — Skills, commands, and plugin taxonomy

---

**Last Updated**: 2026-02-15
