# Archetype Patterns

Three skill archetypes aligned with the Anthropic skills guide. Use discovery answers to select the right one.

---

## Archetype 1: Workflow Automation

Multi-step processes with consistent methodology. The skill orchestrates a sequence of actions, enforcing order and quality at each step.

### Signal Pattern

Select this archetype when discovery answers show:
- **Q1 (Purpose)**: Involves multiple steps, phases, or stages
- **Q3 (Tools)**: Uses 2+ tools in sequence
- **Q4 (Output)**: Side effects matter as much as the final output (files changed, commands run)

### Examples
- Code review (gather → analyze → evaluate → report)
- Deployment pipeline (build → test → deploy → verify)
- Database migration review (parse → check patterns → validate → report)

### Body Template

```markdown
# [Skill Name]

[One-line summary.]

## Guardrails

**NEVER:**
- [Skip phases or reorder them]
- [Proceed without completing prerequisite steps]

**ALWAYS:**
- [Complete all phases in order]
- [Validate before moving to the next phase]

## Arguments

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--scope` | [options] | [default] | [What it controls] |
| `--quick` | flag | false | [Reduced version] |

## Phase 1: [Gather / Initialize]

### 1a. [First sub-step]
[Instructions]

### 1b. [Second sub-step]
[Instructions]

## Phase 2: [Process / Analyze]

### 2a. [First sub-step]
[Instructions]

## Phase 3: [Output / Report]

[Output format specification]

## Examples

### Example 1: [Standard usage]
[Trigger → Actions → Result]

### Example 2: [Quick mode or scope variation]
[Trigger → Actions → Result]

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| [Issue] | [Cause] | [Fix] |
```

### Key Patterns
- **Phase numbering**: `## Phase N:` with `### Na.` sub-steps
- **Arguments table**: When the skill accepts flags or options
- **Quick mode**: Reduced version that skips optional phases
- **Scope control**: What subset of work to operate on

---

## Archetype 2: Document & Asset Creation

Produces consistent, high-quality outputs. The skill follows a template or standard to generate files, reports, or structured content.

### Signal Pattern

Select this archetype when discovery answers show:
- **Q1 (Purpose)**: Creates or generates a file, document, or structured output
- **Q4 (Output)**: A specific deliverable (Markdown file, HTML page, config file)
- Consistency and format matter more than exploratory analysis

### Examples
- API documentation generator
- Report creation from data
- Skill scaffolding (this skill!)
- UI mockup generation

### Body Template

```markdown
# [Skill Name]

[One-line summary.]

## Guardrails

**NEVER:**
- [Produce output without required inputs]
- [Deviate from the output format]

**ALWAYS:**
- [Validate inputs before generating]
- [Follow the output template exactly]

## Instructions

### Step 1: [Gather Inputs]
[What information to collect and validate]

### Step 2: [Generate Content]
[How to produce the output, referencing templates in assets/ if applicable]

### Step 3: [Validate Output]
[Quality checks before delivering]

### Step 4: [Deliver]
[How to present or save the output]

## Output Format

[Exact specification of what the output looks like — structure, sections, formatting]

## Examples

### Example 1: [Standard generation]
[Trigger → Inputs gathered → Output produced]

### Example 2: [Variation or edge case]
[Different input → Different output adaptation]

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| [Issue] | [Cause] | [Fix] |
```

### Key Patterns
- **Output Format section**: Explicit specification of the deliverable
- **assets/ directory**: Templates for consistent output generation
- **Step-based** (not phase-based): Linear flow without approval gates
- **Validation step**: Quality check before delivery

---

## Archetype 3: MCP Enhancement

Adds workflow guidance on top of MCP server integrations. The skill teaches Claude how to use MCP tools effectively for a specific workflow.

### Signal Pattern

Select this archetype when discovery answers show:
- **Q3 (Tools)**: Relies on specific MCP servers (Playwright, Supabase, Slack, etc.)
- **Q1 (Purpose)**: The core task requires MCP capabilities (browser automation, database ops, API calls)
- Without the skill, Claude would use the MCP tools but without domain-specific methodology

### Examples
- Accessibility audit using Playwright MCP
- Database workflow using Supabase MCP
- Design-to-dev handoff using Figma MCP + Linear MCP

### Body Template

```markdown
# [Skill Name]

[One-line summary.]

## Prerequisites

- **Required MCP servers**: [list servers that must be connected]
- **Optional MCP servers**: [nice-to-have integrations]

## Guardrails

**NEVER:**
- [Proceed without verifying MCP connection]
- [Use MCP tools outside their intended scope]

**ALWAYS:**
- [Verify MCP server is connected before starting]
- [Handle MCP failures gracefully]

## Instructions

### Step 1: Verify MCP Connection
[Check that required MCP servers are available]

### Step 2: [Gather Context]
[Collect inputs needed for the MCP workflow]

### Step 3: [Execute MCP Workflow]
[Step-by-step MCP tool usage with error handling]

### Step 4: [Process Results]
[Transform MCP output into user-friendly format]

## MCP Tool Patterns

[Specific patterns for the MCP server — tool names, common parameters, error handling]

## Examples

### Example 1: [Happy path]
[Full workflow with MCP calls]

### Example 2: [MCP failure recovery]
[What happens when MCP connection fails or returns errors]

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| MCP connection failed | Server not configured | Check `.mcp.json` configuration |
| [Tool-specific issue] | [Cause] | [Fix] |
```

### Key Patterns
- **Prerequisites section**: Required MCP servers listed upfront
- **Connection verification**: Always check MCP availability first
- **MCP Tool Patterns section**: Domain-specific tool usage guidance
- **Failure recovery example**: MCP tools can fail; skill must handle it

---

## Decision Matrix

Use this to select the right archetype based on discovery answers:

```
Q1 (Purpose) describes a multi-step process?
├── Yes → Uses MCP servers as primary tools?
│   ├── Yes → MCP Enhancement
│   └── No  → Workflow Automation
└── No  → Document & Asset Creation
```

Shortcut signals:

| Signal | Archetype |
|--------|-----------|
| "review", "analyze", "audit", "pipeline" | Workflow Automation |
| "generate", "create", "scaffold", "produce" | Document & Asset Creation |
| "using Playwright", "using Supabase", "with MCP" | MCP Enhancement |

When ambiguous, prefer Workflow Automation — it's the most flexible and can always be simplified.

---

## Common Sub-Patterns

These patterns appear across archetypes. Include them when discovery answers justify it:

| Pattern | When to Include | How |
|---------|----------------|-----|
| **Sequential phases** | 3+ ordered steps that depend on prior results | Use `## Phase N:` structure |
| **Multi-MCP orchestration** | 2+ MCP servers coordinated | Add Prerequisites section, verification per server |
| **Iterative refinement** | Output quality varies, needs iteration | Add validation + refinement loop |
| **Context-aware branching** | Behavior changes based on input type | Add decision tree in instructions |
| **Domain-specific rules** | Specialized knowledge needed | Move to `references/` for on-demand loading |

---

## Complexity Calibration

Match structure to actual complexity:

| Complexity | Body Size | References | Assets | Structure |
|------------|-----------|------------|--------|-----------|
| **Simple** | <100 lines | None | None | Steps only, no phases |
| **Standard** | 100-300 lines | 1-2 files | 0-1 files | Phases or detailed steps |
| **Complex** | 300-500 lines | 3+ files | 1+ files | Phases with sub-steps, arguments table |

**Default to Simple.** Only escalate when discovery answers demand it.
