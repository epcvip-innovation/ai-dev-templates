# .projects/ Folder Structure Templates

[← Back to Main README](../../README.md)

**Purpose**: Preserve context from complex brainstorming sessions and multi-session projects for future work when ready to execute.

**Mental Model**: Think of `.projects/` as your JIRA backlog, but designed for AI (Claude) to resume work effectively.

---

## The Problem This Solves

**Challenge**: AI has limited context windows. You can only work on tasks of limited complexity at a time. Anything more complex needs to be stored in a standardized format for later.

**Use Cases**:
1. **Future Ideas**: Long, data-filled, business-context conversations that aren't ready to implement yet
2. **Backlog Management**: Like JIRA tickets - ideas waiting in queue until ready
3. **Multi-phase Projects**: Some features are complex enough to span weeks/months
4. **Branch Management**: Work on multiple features in parallel, each in its own branch
5. **Session Continuity**: Resume work after context clears (next day, next week, next month)

**Key Insight**: **AI is like a team of junior engineers who will easily go off track and get distracted.** The `.projects/` structure keeps them (and you) focused with clear scope boundaries, checkpoints, and pre-answered questions.

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

**Decision Tree**:

```
Is this a simple feature (<1 week, <5 files)?
├── YES → Add to backlog/_BACKLOG.md (simple entry)
└── NO → Continue...
    │
    Is this a medium feature (1-2 weeks, 5-10 files)?
    ├── YES → Create .projects/[name]/ with essential 3 files (plan, tasks, HANDOFF)
    └── NO → Continue...
        │
        Is this a complex feature (>2 weeks, major refactoring)?
        └── YES → Create .projects/[name]/ with essential files + optional files as needed

Does this project span multiple phases or need architectural decisions?
└── YES → Add optional files: integration-notes.md, testing-strategy.md, decisions/
```

### Threshold Examples

| Feature | Complexity | Recommended Approach |
|---------|------------|----------------------|
| Add export button to table | Simple (<1 week) | backlog/_BACKLOG.md entry |
| Implement user authentication | Medium (1-2 weeks) | .projects/auth/ with 3 essential files |
| Backend refactor (2,162 lines → modular) | Complex (>2 weeks) | .projects/backend-refactor/ with full structure |
| Multi-tenant architecture migration | Very Complex (months) | Consider own repo or .projects/ with extensive docs |

---

## Where to Store Project Documentation

Your repo can use different locations for the same pattern. Choose based on team preference and project style:

### Option A: .projects/ (Recommended for Solo/Small Teams)

```
your-project/
├── .projects/
│   ├── [feature-name]/
│   │   ├── README.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── HANDOFF.md
│   └── archive/
├── CLAUDE.md
└── src/
```

**Pros**:
- Hidden from main file tree (cleaner, less clutter)
- Established pattern (ping-tree-compare, backend-refactor)
- Works seamlessly with /start-feature, /resume-feature commands
- Can gitignore for WIP features (keep planning private)

**Cons**:
- Less discoverable for team members (hidden folder)
- Not traditional documentation location
- May confuse new contributors

**Best for**: Solo developers, personal projects, exploratory work

---

### Option B: backlog/ (Recommended - Standard Structure)

```
your-project/
├── backlog/
│   ├── _BACKLOG.md              # Main backlog (underscore sorts first)
│   ├── _TEMPLATE.md             # Feature plan template
│   └── [feature-name]/
│       ├── plan.md              # Feature plan with YAML frontmatter
│       └── HANDOFF.md           # Session notes (optional)
├── CLAUDE.md
└── src/
```

**Pros**:
- Clear purpose (it's a backlog!)
- YAML frontmatter enables tooling
- Underscore prefix sorts root files first
- Feature discovery via `feature_discovery.py`
- Standard across all projects

**Cons**:
- More visible (can't hide WIP planning)

**Best for**: All projects - this is the recommended standard

---

### Option C: Hybrid (backlog + private WIP)

```
your-project/
├── backlog/
│   ├── _BACKLOG.md              # Main backlog
│   └── [feature-name]/          # Feature plans
│       └── plan.md
│
├── .projects/                   (private WIP, gitignored)
│   └── [wip-feature]/
│       ├── plan.md
│       └── HANDOFF.md
│
└── src/
```

**Pros**:
- Public planning (backlog/) + private experimentation (.projects/)
- Best of both approaches
- Flexible: share what's ready, hide what's not
- Good for open-source with private R&D

**Cons**:
- More complex to maintain
- Requires discipline to keep in sync
- Two places to check for planning docs
- Need clear rules for what goes where

**Best for**: Open-source projects with private features, mixed public/private development

---

### Key Insight: Same Pattern, Different Location

**The pattern is identical across all options**:
- Main specification document (plan.md or [feature].md)
- Task breakdown (tasks.md or in same file)
- Session continuity (HANDOFF.md or handoffs/[date].md)
- Archive strategy (archive/ folder)

**Only the LOCATION differs.** Choose based on:
- Team size (solo → .projects/, team → docs/)
- Visibility needs (private → .projects/, public → docs/)
- Existing conventions (follow what repo already uses)

**Slash commands support all three options** - they check multiple locations automatically.

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

**Why these 4 are essential**:
- **README.md**: Helps Claude (and humans) know where to start when entering project
- **plan.md**: Business context, architecture, decisions - stable reference
- **tasks.md**: Granular execution plan - updated frequently
- **HANDOFF.md**: Critical for AI session continuity (Claude forgets after context clears)

### Optional Files (Create When Needed)

```
.projects/[feature-name]/
├── [Essential files above]
├── integration-notes.md       # When dependencies are complex
├── testing-strategy.md        # When testing needs separate planning
├── decisions/                 # When architectural decisions are many
│   ├── 001-event-driven.md    # ADR (Architecture Decision Record) format
│   └── 002-sqlite-choice.md
├── [custom].md                # Whatever makes sense for your project
└── archive/                   # Completed session notes (optional)
    └── session-2025-09-17.md
```

**When to create optional files**:
- **integration-notes.md**: >3 external dependencies, complex data flows, or critical path analysis needed
- **testing-strategy.md**: Non-standard testing approach, performance benchmarks, or test complexity >30 lines in plan.md
- **decisions/**: >3 major architectural decisions that need separate justification (use ADR format)
- **Custom files**: As needed organically (migration-strategy.md, api-spec.md, data-model.md, etc.)

**Don't create files "just in case"** - only create when actual need arises.

---

## Document Purposes & Lengths

Based on your actual usage patterns and industry best practices from Google, Stripe, and Amazon:

| Document | Purpose | Typical Length | Max Length | When to Split |
|----------|---------|----------------|------------|---------------|
| README.md | Navigation & status | 200-400 words | 500 words | Never (must stay concise) |
| plan.md | Architecture & approach | 2,000-4,000 words | 5,000 words (~10 pages) | Section >30 lines → extract to separate file |
| tasks.md | Task breakdown | As needed | No limit | Group by phase, use archive/ for completed |
| HANDOFF.md | Session state | 500-1,500 words | 2,000 words | Move old handoffs to archive/ |
| integration-notes.md | Dependencies & flows | 1,000-3,000 words | 5,000 words | Multiple subsystems → separate docs |
| testing-strategy.md | Test plan | 1,000-2,000 words | 4,000 words | Split by test type (unit/integration/e2e) |

### Length Guidance Philosophy

**Don't use arbitrary line limits** (like "500 lines max"). Instead, use **pragmatic tests**:

1. **Scan Test**: Can you find what you need in <30 seconds of scrolling?
   - If NO → File is too large or poorly organized

2. **Purpose Test**: Is this file doing one job, or mixing concerns?
   - If mixing → Split into separate files

3. **Section Test**: Does any section exceed 30 lines?
   - If YES → Extract that section to separate file, link from main doc

4. **Audience Test**: Does this file serve multiple audiences with different needs?
   - If YES → Split (e.g., business context vs technical implementation)

**Industry Standard** (from research):
- Google/Stripe/Amazon: Main design docs are 5-10 pages max (~2,000-5,000 words)
- Reason: "Reviewers may not read documents longer than 5,000 words"
- Solution: Hub-and-spoke pattern (main doc links to appendices/sub-docs)

---

## The Hub-and-Spoke Pattern

**Your backend-refactor project already uses this industry-standard pattern!**

### How It Works

**Main Document** (plan.md):
- High-level architecture (2-3 pages)
- Links to detailed sub-documents for deep-dives
- Stays readable and scannable

**Linked Sub-Documents**:
- Technical deep-dives (EVENT-SQLITE-PLAN.md)
- Integration analysis (integration-notes.md)
- Test strategy (testing-strategy.md)
- Migration procedures (MIGRATION_GUIDE.md)

### Example (Your backend-refactor)

```markdown
# Backend Refactor - Plan

## Architecture Overview
[2-3 paragraphs of high-level approach]

For detailed technical design, see [EVENT-SQLITE-PLAN.md](./EVENT-SQLITE-PLAN.md)

## Testing
See [testing-strategy.md](./testing-strategy.md) for complete test plan
```

**Result**: Main doc stays 6 pages, total documentation is 22 pages across 6 files.

**This matches patterns from**:
- Google (design doc + linked appendices)
- Stripe (main proposal + impact analysis + specs)
- Amazon (PR/FAQ + technical appendix)

---

## AI-Specific Patterns (Claude as Junior Engineer)

**Key Difference**: Junior humans get tired after 4 hours. Claude's context window fills after 3-5 tasks.

### 1. Explicit Scope Boundaries

**In plan.md, add "Non-Goals" section**:
```markdown
## Non-Goals (Out of Scope for THIS Phase)
- ❌ NOT refactoring auth.py (already well-structured)
- ❌ NOT adding new features (only restructuring existing)
- ❌ NOT changing API contracts
```

**In README.md "For Claude" section**:
```markdown
### Scope Boundaries
**ONLY work on**: Extract auth routes to separate file
**DO NOT**:
- [ ] Don't refactor code that's already working
- [ ] Don't add features not in tasks.md
- [ ] Don't fix unrelated bugs (document in BUGS.md)
```

**Why this works**: Prevents scope drift - Claude won't wander off to "improve" things.

### 2. Checkpoint Frequency

**For human developers**: Checkpoints every 4-6 tasks
**For Claude**: Checkpoints every 1-2 tasks (context fills faster)

**In tasks.md**:
```markdown
- [x] Task 2.1: Extract auth routes
- [x] Task 2.2: Add auth tests

**🔍 CHECKPOINT 2.1**: Run these EXACT commands
\`\`\`bash
npm run test
curl http://localhost:3000/api/auth/login -X POST
# Expected: Tests pass, endpoint returns 200
\`\`\`

**If pass**: Proceed to Task 2.3
**If fail**: STOP, revert, debug
```

### 3. Pre-Answered FAQs

**In plan.md, add "FAQ: For Claude" section**:
```markdown
## FAQ: For Claude (AI Guidance)

**Q**: This code could be improved while I'm here, should I?
**A**: NO - Extract as-is, improvements in Phase 4

**Q**: I found a better pattern, should I use it?
**A**: Only if explicitly called out in tasks.md

**Q**: Should I add type hints while extracting?
**A**: NO - Separate improvement phase

**Q**: There's a bug in this code, should I fix it?
**A**: Document in BUGS.md, fix in dedicated session
```

**Why this works**: Claude WILL ask these questions. Pre-answer them to prevent detours.

### 4. Mandatory Validation Steps

**In tasks.md checkpoints, be SPECIFIC**:

❌ **Bad**: "Test that it works"
✅ **Good**:
```markdown
**🔍 CHECKPOINT 2.1**: Run these EXACT tests
\`\`\`bash
curl http://localhost:3000/api/auth/login -X POST -d "email=test@test.com&password=test"
# Expected: 200 OK with JWT cookie

curl http://localhost:3000/api/auth/me
# Expected: 401 Unauthorized (no cookie)
\`\`\`
```

### 5. File Change Scope Limits

**In HANDOFF.md "Next Steps" section**:
```markdown
**Files to Modify**:
- `src/main.py` (lines 50-120 ONLY)
- `api/auth_routes.py` (create new file)

**Files You Will NOT Touch**:
- `auth.py` (already perfect, out of scope)
- `database.py` (separate task)
```

**Why this works**: Explicit permission boundaries prevent over-engineering.

---

## Integration with Slash Commands

Your existing slash commands already support .projects/ pattern:

### /start-feature

**Creates .projects/ structure**:
- Simple features (≤3hrs): Add to TASKS.md, skip .projects/
- Complex features (>3hrs): Create .projects/[name]/ with template files

### /resume-feature

**Checks multiple patterns**:
```bash
.projects/[feature-name]/HANDOFF.md
backlog/[feature]/HANDOFF.md
features/[feature]/README.md
```

**Reads and summarizes** for Claude to resume work.

### /feature-complete

**Archives completed work**:
```bash
# Moves to:
.projects/archive/[feature-name]/
# OR summarizes in:
archive/session-${timestamp}.md
```

### TodoWrite Tool vs tasks.md

**Different purposes, both valid**:
- **TodoWrite**: Ephemeral in-session task list (stored in `.claude/todos.json`)
  - Used for: Current session focus
  - Lifetime: Cleared after session or when stale
  - Audience: Current AI session

- **tasks.md**: Persistent cross-session documentation
  - Used for: Full project scope, progress tracking
  - Lifetime: Lives with project until completion
  - Audience: Any session (human or AI)

**No conflict**: They complement each other.

---

## Document Hierarchy: Product → Technical → Implementation

Professional teams use a three-layer hierarchy. Your pattern already matches this!

### Layer 1: Product Spec (PRD)

**Document**: plan.md (partial)
**Owner**: Product Manager (or you as tech PM)
**Audience**: Entire team + stakeholders
**Lifecycle**: Changes rarely after approval
**Content**:
- Problem statement (with evidence!)
- Goals & success metrics
- User scenarios
- High-level requirements
- **Non-goals** (scope boundaries)

### Layer 2: Technical Design (TDD/RFC)

**Document**: plan.md + separate design docs (EVENT-SQLITE-PLAN.md, etc.)
**Owner**: Tech Lead / Senior Engineer
**Audience**: Engineering team
**Lifecycle**: Stable after review, may evolve during implementation
**Content**:
- Architecture overview
- Options considered (WHY we chose this approach)
- Data models & API contracts
- Dependencies & risks
- Migration strategy

### Layer 3: Implementation (Tasks/Stories)

**Document**: tasks.md
**Owner**: Individual engineers (or AI)
**Audience**: Person doing the work
**Lifecycle**: Changes daily
**Content**:
- Testable tasks with checkpoints
- Step-by-step instructions
- Code locations
- Testing requirements
- Definition of done

**Your backend-refactor structure**:
- ✅ Has problem statement, goals, success metrics (PRD)
- ✅ Has architecture, options considered, dependencies (TDD)
- ✅ Has granular tasks with checkpoints (Implementation)

You're already following industry best practices!

---

## Real-World Examples

### Example 1: Your backend-refactor (Complex Feature)

**Structure**:
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

**Total**: ~22 pages across 7 files
**Why it works**:
- Main plan.md stays readable (6 pages)
- Technical deep-dives separated (EVENT-SQLITE-PLAN.md)
- Different concerns have different lifecycles
- Hub-and-spoke linking keeps it navigable

**Matches**: Stripe API changes, Google design docs (same scale!)

### Example 2: Simple Feature (Add Export Button)

**Structure**:
```
.projects/
└── add-export-button.md (single file, 200 words)
```

**Content**:
```markdown
# Feature: Add Export Button

## Goal
Users want to export partner data to CSV

## Tasks
- [ ] Add button to PartnerTable.tsx
- [ ] Add /api/export/partners endpoint
- [ ] Generate CSV from database query
- [ ] Test: Button appears, click downloads CSV

**Estimated Time**: 2 hours
```

**Why single file**: Feature is simple, doesn't need separate planning/architecture docs.

### Example 3: Medium Feature (User Authentication)

**Structure**:
```
.projects/user-auth/
├── README.md (navigation)
├── plan.md (approach, security considerations)
├── tasks.md (implementation steps)
└── HANDOFF.md (session notes)
```

**When to add optional files**:
- If OAuth integration is complex → Create `integration-notes.md`
- If security testing needs separate plan → Create `testing-strategy.md`
- But START with just the 4 essential files, add as needed

---

## Archive Strategy

### When to Archive

**Archive completed projects when**:
- Feature is fully deployed to production
- All tasks marked complete
- No further work planned

### How to Archive

**Option A: Move entire folder** (recommended for complex projects)
```bash
mv .projects/backend-refactor .projects/archive/backend-refactor
```

**Option B: Summarize in main TASKS.md** (for simple features)
```markdown
## Archive: Completed Features

### Backend Refactor (Completed 2025-09-17)
- Extracted 33 endpoints to modular routes
- Reduced main.py from 2,162 to 385 lines
- All tests passing, deployed to production
- Archive: See [archive/backend-refactor/](./archive/backend-refactor/)
```

### What NOT to Do

❌ **Don't create completed/ subfolders within each project**
- Adds unnecessary depth
- Not standard development practice
- Better: Archive entire project when done

✅ **Do use git history as your archive**
- Commit messages document decisions
- Git log shows progression
- Tags mark milestones

---

## Growth Pattern: When to Graduate to Own Repo

**Start with** `.projects/[name]/`

**Graduate to own repo when**:
1. Project has 5+ substantial files (each >2,000 words)
2. Multiple developers working simultaneously
3. Needs its own CI/CD pipeline
4. Becomes a product vs a feature
5. Outgrows "feature" scope

**Example pattern**: Has actual Python code in `.projects/` - this suggests it was prototyping phase before becoming own repo.

**Pattern**:
```
.projects/prototype/ → Full codebase in .projects/ → Extract to own repo → .projects/ becomes planning archive
```

---

## Comparison to Other Patterns

### vs. ROADMAP.md (Ben Newton Pattern)

**ROADMAP.md**:
- Single file with checkbox statuses
- Works great for solo developer, many small features
- Doesn't scale to complex multi-week projects

**When to use ROADMAP.md instead**:
- Project has 20+ small features (<1 week each)
- All context fits in one file (<5,000 words)
- No complex architecture or integrations

**When to use .projects/**:
- Features span multiple weeks
- Need session continuity (AI handoffs)
- Complex with architectural decisions
- Multiple related documents needed

### vs. GitHub Issues/Linear

**GitHub Issues**:
- Great for team collaboration
- Built-in tracking and assignments
- Requires `gh` CLI for Claude to access
- Less suitable for complex planning docs

**Hybrid Approach** (recommended):
- Use GitHub Issues for team tracking
- Use .projects/ for AI context and detailed planning
- Link between them: Issue #123 → .projects/feature-x/

---

## FAQ

### Q: Should all repos use .projects/?

**A**: No. Use based on project complexity:
- Simple tools (single feature): ROADMAP.md or backlog/_BACKLOG.md
- Complex projects with multi-week features: backlog/[feature]/plan.md
- Mix: Both (backlog for ideas, .projects/ for private WIP)

### Q: How do I decide what goes in plan.md vs separate docs?

**A**: Use the 30-line rule:
- If section in plan.md exceeds 30 lines → Extract to separate doc
- Link from plan.md: "For detailed X, see [doc-name.md]"

### Q: Should I create all optional files upfront?

**A**: No! Only create files when actual need arises. Don't create "just in case."

Start with 4 essential files. Add integration-notes.md only when dependencies become complex.

### Q: How often should I update HANDOFF.md?

**A**: Every session. At end of work session:
1. Update "What Was Accomplished"
2. Update "What's Next"
3. Document any blockers or decisions

This is critical for AI continuity.

### Q: Can I use different structure for different repos?

**A**: The template is flexible. But standardizing helps:
- Slash commands work consistently
- Easier to switch between projects
- Team members know what to expect

### Q: What if my plan.md exceeds 5,000 words?

**A**: Split it:
1. Keep high-level overview in plan.md
2. Extract detailed sections to separate docs
3. Use hub-and-spoke linking

**Red flag**: If plan.md is >10,000 words, you're probably documenting implementation details that belong in code/comments.

### Q: Should tasks.md duplicate GitHub Issues?

**A**: Different purposes:
- GitHub Issues: Team tracking, assignments, public discussion
- tasks.md: Granular breakdown for execution, AI checkpoints

Link between them: "Task 2.3 implements Issue #45"

---

## Summary: Best Practices

### ✅ Do

- Create .projects/[name]/ for features >3hrs complexity
- Start with 4 essential files (README, plan, tasks, HANDOFF)
- Add optional files organically when needed
- Update HANDOFF.md every session
- Use hub-and-spoke linking (main doc → sub-docs)
- Add AI-specific guidance (scope boundaries, checkpoints, FAQs)
- Archive completed projects
- Keep files scannable (scan test, purpose test)

### ❌ Don't

- Don't create files "just in case"
- Don't use arbitrary line limits without purpose
- Don't create completed/ subfolders within projects
- Don't duplicate what git history already captures
- Don't mix multiple features in one .projects/ folder
- Don't let plan.md become implementation documentation
- Don't skip HANDOFF.md (critical for AI continuity)

---

## Templates Location

- **Essential Templates**: `templates/projects/_TEMPLATE/`
  - README.md
  - plan.md
  - tasks.md
  - HANDOFF.md

**Quick Copy Command**:
```bash
cp -r templates/projects/_TEMPLATE .projects/[your-feature-name]
cd .projects/[your-feature-name]
# Edit README.md, plan.md, tasks.md, HANDOFF.md with your details
```

---

**Last Updated**: 2025-11-02
**Maintained By**: dev-setup template library
**Next Review**: 2026-02-02 (quarterly)
