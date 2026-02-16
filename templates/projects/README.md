# .projects/ Folder Structure Templates

[← Back to Main README](../../README.md)

**Purpose**: Preserve context from complex brainstorming sessions and multi-session projects for future work when ready to execute.

**Mental Model**: Think of `.projects/` as your JIRA backlog, but designed for AI (Claude) to resume work effectively.

---

## The Problem This Solves

**Challenge**: AI has limited context windows. Complex work needs to be stored in a standardized format for later.

**Use Cases**:
1. **Future Ideas**: Long, data-filled conversations not ready to implement yet
2. **Backlog Management**: Ideas waiting in queue until ready
3. **Multi-phase Projects**: Features spanning weeks/months
4. **Session Continuity**: Resume work after context clears

**Key Insight**: AI is like a team of junior engineers who easily go off track. The `.projects/` structure keeps them focused with clear scope boundaries, checkpoints, and pre-answered questions.

---

## Quick Start

### For New Projects

1. **Copy template**: `cp -r templates/projects/_TEMPLATE .projects/[feature-name]`
2. **Fill in README.md**: Update status, document map, current focus
3. **Create plan.md**: Problem statement, goals, non-goals, architecture
4. **Create tasks.md**: Break down into granular, testable tasks
5. **Keep HANDOFF.md current**: Update at end of every session

### For Existing Projects

If you have an existing .projects/ folder without this structure:
1. **Add README.md**: Navigation hub (helps Claude know where to start)
2. **Ensure plan.md exists**: Main specification (if missing, extract from code/commits)
3. **Ensure HANDOFF.md exists**: Current session state (critical for AI continuity)
4. **Update tasks.md**: Current progress and next steps

---

## When to Use .projects/

| Feature Complexity | Recommended Approach |
|-------------------|---------------------|
| Simple (<1 week, <5 files) | `backlog/_BACKLOG.md` entry |
| Medium (1-2 weeks, 5-10 files) | `.projects/[name]/` with 3 essential files |
| Complex (>2 weeks, major refactoring) | `.projects/[name]/` with essential + optional files |
| Very Complex (months) | Consider own repo, or `.projects/` with extensive docs |

---

## Where to Store Project Documentation

| Option | Location | Best For | Tradeoff |
|--------|----------|----------|----------|
| **A: .projects/** | `.projects/[feature]/` (hidden) | Solo devs, private WIP | Less discoverable for team |
| **B: backlog/** (recommended) | `backlog/[feature]/` (visible) | All projects | Can't hide WIP planning |
| **C: Hybrid** | backlog/ (public) + .projects/ (private WIP) | Open-source with private R&D | More complex to maintain |

**The pattern is identical across all options** — same files (plan.md, tasks.md, HANDOFF.md), different location. Choose based on team size and visibility needs. Slash commands support all three options automatically.

---

## File Structure

### Essential Files (Always Create)

```
.projects/[feature-name]/
├── README.md          # Navigation hub - where to start
├── plan.md            # Main specification - WHY + WHAT + HOW
├── tasks.md           # Task breakdown - granular implementation steps
└── HANDOFF.md         # Session continuity - current state + what's next
```

### Optional Files (Create When Needed)

| File | Create When... |
|------|---------------|
| `integration-notes.md` | >3 external dependencies or complex data flows |
| `testing-strategy.md` | Non-standard testing approach or test complexity >30 lines in plan.md |
| `decisions/001-*.md` | >3 major architectural decisions needing separate justification (ADR format) |
| Custom files | As needed organically (migration-strategy.md, api-spec.md, etc.) |

**Don't create files "just in case"** — only when actual need arises.

---

## Document Purposes & Lengths

| Document | Purpose | Max Length | When to Split |
|----------|---------|------------|---------------|
| README.md | Navigation & status | 500 words | Never (must stay concise) |
| plan.md | Architecture & approach | ~5,000 words (~10 pages) | Any section >30 lines → extract to separate file |
| tasks.md | Task breakdown | No limit | Group by phase, archive completed |
| HANDOFF.md | Session state | ~2,000 words | Move old handoffs to archive/ |

**Industry standard** (Google/Stripe/Amazon): Main design docs are 5-10 pages max. Use hub-and-spoke pattern (main doc links to appendices).

---

## AI-Specific Patterns (Claude as Junior Engineer)

Claude's context window fills after 3-5 tasks. These patterns prevent scope drift:

| Pattern | What to Add | Why It Works |
|---------|------------|--------------|
| **Scope boundaries** | "Non-Goals" in plan.md, "DO NOT" list in README.md | Prevents Claude from wandering off to "improve" things |
| **Frequent checkpoints** | Every 1-2 tasks in tasks.md with exact test commands | Catches drift early (humans checkpoint every 4-6 tasks) |
| **Pre-answered FAQs** | "FAQ: For Claude" in plan.md | Claude WILL ask these questions — pre-answer to prevent detours |
| **Mandatory validation** | Exact `curl` / test commands in checkpoints (not "test that it works") | Eliminates ambiguity in verification |
| **File change limits** | "Files to Modify" and "Files You Will NOT Touch" in HANDOFF.md | Explicit permission boundaries prevent over-engineering |

**Example checkpoint** (be this specific):
```markdown
**CHECKPOINT 2.1**: Run these EXACT commands
```bash
curl http://localhost:3000/api/auth/login -X POST -d "email=test@test.com&password=test"
# Expected: 200 OK with JWT cookie
```
**If pass**: Proceed to Task 2.3
**If fail**: STOP, revert, debug
```

---

## Integration with Slash Commands

| Command | .projects/ Integration |
|---------|----------------------|
| `/start-feature` | Creates `.projects/[name]/` structure for complex features (>3hrs) |
| `/resume-feature` | Checks `.projects/`, `backlog/`, `features/` for HANDOFF.md |
| `/feature-complete` | Archives to `.projects/archive/[name]/` |
| **TodoWrite vs tasks.md** | TodoWrite = ephemeral in-session list. tasks.md = persistent cross-session. Both valid, complementary. |

---

## Real-World Example: Complex Feature

```
.projects/backend-refactor/
├── plan.md (2,500 words ≈ 6 pages)
├── tasks.md (1,000 words ≈ 2 pages)
├── integration-notes.md (2,000 words ≈ 5 pages)
├── testing-strategy.md (2,500 words ≈ 6 pages)
├── EVENT-SQLITE-PLAN.md (800 words ≈ 2 pages)
├── MIGRATION_GUIDE.md (500 words ≈ 1 page)
└── HANDOFF.md (current session state)
```

**Total**: ~22 pages across 7 files. Main plan.md stays readable (6 pages), technical deep-dives separated, hub-and-spoke linking keeps it navigable. Matches Stripe API changes and Google design doc scale.

---

## Archive Strategy

**When**: Feature fully deployed, all tasks complete, no further work planned.

**How**: `mv .projects/backend-refactor .projects/archive/backend-refactor` (entire folder).

**Don't**: Create `completed/` subfolders within projects. Use git history as your primary archive — commit messages document decisions, tags mark milestones.

---

## Growth Pattern

**Start with** `.projects/[name]/`. **Graduate to own repo when**: 5+ substantial files (each >2,000 words), multiple developers, needs own CI/CD, becomes a product vs a feature.

---

## FAQ

| Question | Answer |
|----------|--------|
| Should all repos use .projects/? | No — simple tools use backlog/_BACKLOG.md. Complex multi-week features use .projects/. |
| What goes in plan.md vs separate docs? | 30-line rule: if a section exceeds 30 lines, extract to separate doc and link. |
| Create all optional files upfront? | No! Only create when actual need arises. Start with 4 essential files. |
| How often update HANDOFF.md? | Every session. Update "accomplished", "what's next", any blockers/decisions. Critical for AI continuity. |
| plan.md exceeds 5,000 words? | Split: keep overview in plan.md, extract details to sub-docs with hub-and-spoke linking. |

---

## Summary: Best Practices

**Do**: Create `.projects/` for features >3hrs. Start with 4 essential files. Add optional files organically. Update HANDOFF.md every session. Use hub-and-spoke linking. Add AI-specific guidance.

**Don't**: Create files "just in case". Mix multiple features in one folder. Let plan.md become implementation docs. Skip HANDOFF.md.

---

## Templates Location

**Essential Templates**: `templates/projects/_TEMPLATE/` (README.md, plan.md, tasks.md, HANDOFF.md)

```bash
cp -r templates/projects/_TEMPLATE .projects/[your-feature-name]
```

---

**Last Updated**: 2026-02-15
**Maintained By**: dev-setup template library
