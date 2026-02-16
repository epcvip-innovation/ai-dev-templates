# [Project Name]

> **Part of**: [Project Organization Templates](../README.md)

<!--
This README serves as the navigation hub for this project.
Replace all bracketed placeholders with your actual content.
Delete sections that don't apply to your project.
-->

**Status**: Planning | In Progress | Complete | On Hold
**Started**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD
**Owner**: [Team/Person]

---

## Quick Start

**New to this project?** Read in this order:
1. **plan.md** - Architecture overview, goals, approach
2. **tasks.md** - Current progress and implementation breakdown
3. **HANDOFF.md** - Most recent session notes

**Resuming work?** Go straight to HANDOFF.md

---

## Document Guide

| Document | Purpose | Audience | Update Frequency |
|----------|---------|----------|------------------|
| **README.md** (this file) | Navigation & project status | Everyone | Weekly |
| **plan.md** | Architecture, goals, approach | Engineers + PMs | Rarely (stable after approval) |
| **tasks.md** | Implementation checklist | Developer | Daily |
| **HANDOFF.md** | Session continuity | Next session (AI/human) | Every session |
| **integration-notes.md** | Dependencies, data flows | Engineers | As discovered |
| **testing-strategy.md** | Test plan & validation | QA + Engineers | Weekly |
| **decisions/** | Architecture Decision Records | Engineers | Per decision |

**Note**: Only create optional files (integration-notes, testing-strategy, decisions/) if actually needed. Don't create files "just in case."

---

## For Claude (AI Context)

<!--
This section helps Claude Code stay focused and on-track.
Update this at the start of each session.
-->

### Current Focus
**Working On**: [Link to specific task in tasks.md, e.g., "Phase 2, Task 2.3"]
**Current Session Goal**: [One sentence: what should be accomplished this session]

### Scope Boundaries

**ONLY work on**:
- [Specific files or features for this session]
- [Clear permission boundaries]

**DO NOT** (explicitly out of scope):
- [ ] Don't refactor code that's already working (unless specifically tasked)
- [ ] Don't add new features not in tasks.md
- [ ] Don't fix unrelated bugs (document in BUGS.md instead)
- [ ] Don't deviate from patterns established in plan.md

### Next Checkpoint

**Stop after**: [Specific task or milestone]
**Validate with**: [Specific commands to run or tests to check]
**Then**: Ask user before proceeding

---

## Project Overview

<!--
One-paragraph summary for quick context.
Detail goes in plan.md, not here.
-->

[2-3 sentences: What is this project? Why does it exist? What problem does it solve?]

---

## Quick Links

- **Main Spec**: [plan.md](./plan.md)
- **Task Breakdown**: [tasks.md](./tasks.md)
- **Session Continuity**: [HANDOFF.md](./HANDOFF.md)
- **Related Projects**: [Link to related .projects/ folders or repos]
- **JIRA/Linear**: [Link to external tracker if applicable]

---

## Key Decisions

<!--
Quick reference to major architectural decisions.
Detail in decisions/ folder or plan.md.
-->

- **[Decision 1]**: [One sentence rationale]
- **[Decision 2]**: [One sentence rationale]

See `decisions/` folder for full ADRs.

---

## Progress Summary

<!--
High-level milestones. Detail in tasks.md.
-->

- [x] Phase 1: Planning & Design (completed YYYY-MM-DD)
- [ ] Phase 2: Core Implementation (in progress)
- [ ] Phase 3: Testing & Integration
- [ ] Phase 4: Deployment

**Completion**: ~XX% (based on tasks.md)

---

## Notes

<!--
Any critical context that doesn't fit elsewhere.
Keep brief - detail goes in appropriate doc.
-->

- [Important note 1]
- [Important note 2]

---

**Last Updated**: YYYY-MM-DD by [Name]
