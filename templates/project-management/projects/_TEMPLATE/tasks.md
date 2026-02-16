# [Project Name] - Tasks

<!--
This is your granular implementation checklist.

PURPOSE: Track what's done, what's next, what's blocked
AUDIENCE: Developer doing the work
UPDATE FREQUENCY: Daily (or every session)

CHECKPOINT FREQUENCY:
- For human developers: Every 4-6 tasks
- For Claude AI: Every 1-2 tasks (context fills faster)

TASK FORMAT:
- [ ] Task description - Location | Expected outcome | Validation

Keep tasks testable and granular (1-3 hours each max)
-->

**Last Updated**: YYYY-MM-DD
**Current Phase**: [Phase number/name]
**Overall Progress**: XX% (based on completed tasks)

---

## Phase 1: [Phase Name] - Planning & Setup

**Goal**: [What this phase accomplishes]
**Status**: ✅ Complete | 🏗️ In Progress | ⏳ Pending

### Tasks

- [x] Define project scope and goals → plan.md | Clear acceptance criteria | Review approved
- [x] Create initial architecture design → plan.md | Architecture diagram complete | Tech lead reviewed
- [x] Set up project structure → `.projects/[name]/` | All template files created | README.md populated
- [x] Identify dependencies and risks → plan.md | Risk matrix complete | Stakeholders notified

**🔍 CHECKPOINT 1.1**: Planning complete
- [x] plan.md reviewed and approved
- [x] Stakeholders aligned on approach
- [x] All open questions resolved

**Completed**: YYYY-MM-DD

---

## Phase 2: [Phase Name] - Core Implementation

**Goal**: [What this phase accomplishes]
**Status**: 🏗️ In Progress | ⏳ Pending

### Tasks

- [x] Task 2.1: [Description] → `src/file.ts:123` | Expected outcome | Validation command
- [x] Task 2.2: [Description] → `src/another.ts` | Expected outcome | Tests pass
- [ ] Task 2.3: [Description] → `src/component.tsx` | Expected outcome | Visual check
- [ ] Task 2.4: [Description] → `src/utils.ts` | Expected outcome | Unit tests pass

**🔍 CHECKPOINT 2.1**: After Task 2.2
**Run these EXACT validation steps**:
```bash
npm run test
npm run build
curl http://localhost:3000/health
# Expected: All pass, server starts, health returns 200
```

**✅ If all pass**: Proceed to Task 2.3
**❌ If any fail**: STOP, revert changes, debug before continuing

**Current Task**: Task 2.3 (started YYYY-MM-DD)

---

### Tasks (continued)

- [ ] Task 2.5: [Description] → `src/api.ts` | Expected outcome | Integration test passes
- [ ] Task 2.6: [Description] → `src/database.ts` | Expected outcome | Migration runs successfully

**🔍 CHECKPOINT 2.2**: After Task 2.6
**Validation**:
```bash
npm run test:integration
npm run db:migrate
# Expected: All integration tests pass, migrations applied without errors
```

**STOP HERE**: Ask user before proceeding to Phase 3

---

## Phase 3: [Phase Name] - Testing & Integration

**Goal**: [What this phase accomplishes]
**Status**: ⏳ Pending

### Tasks

- [ ] Task 3.1: [Description] → `tests/unit/` | Expected outcome | All unit tests pass
- [ ] Task 3.2: [Description] → `tests/integration/` | Expected outcome | All integration tests pass
- [ ] Task 3.3: [Description] → Manual testing | Expected outcome | User flows validated
- [ ] Task 3.4: [Description] → Performance testing | Expected outcome | Metrics within targets

**🔍 CHECKPOINT 3.1**: After all tests
**Validation**:
- [ ] All unit tests pass (coverage >80%)
- [ ] All integration tests pass
- [ ] Manual test scenarios validated
- [ ] Performance benchmarks met
- [ ] No regressions in existing functionality

**Phase Completion**: YYYY-MM-DD (estimated)

---

## Phase 4: [Phase Name] - Deployment & Monitoring

**Goal**: [What this phase accomplishes]
**Status**: ⏳ Pending

### Tasks

- [ ] Task 4.1: Deploy to staging → Staging environment | Deployed successfully | Health check passes
- [ ] Task 4.2: Staging validation → Test all features | No issues found | Sign-off received
- [ ] Task 4.3: Production deployment (canary) → 10% traffic | Metrics stable | No errors
- [ ] Task 4.4: Gradual rollout → 50% traffic | Metrics improving | User feedback positive
- [ ] Task 4.5: Full rollout → 100% traffic | Full deployment | Success metrics achieved

**🔍 CHECKPOINT 4.1**: After each rollout phase
**Validation**:
- [ ] Error rate < baseline
- [ ] Response time within SLA
- [ ] No user complaints
- [ ] Metrics showing improvement

**Rollback Plan**: If any metric fails, execute rollback in [migration-guide.md](./migration-guide.md)

---

## Archive: Completed Phases

<!--
Move completed phases here to keep active work visible.
Keep summary for historical context.
-->

### Phase 0: Discovery (Completed YYYY-MM-DD)
**Summary**: Researched options, validated approach with stakeholders
**Outcome**: Plan approved, ready for implementation
**Archive**: See [archive/phase-0-discovery.md](./archive/phase-0-discovery.md)

---

## Blocked Tasks

<!--
Track tasks that can't proceed until blocker is resolved.
-->

| Task | Blocked By | Owner | Target Resolution |
|------|------------|-------|-------------------|
| Task X.Y | [Reason/dependency] | [Name] | YYYY-MM-DD |

---

## Bugs Discovered During Implementation

<!--
Don't fix unrelated bugs during feature work - document them here.
-->

| Bug | Severity | Location | Reported | Status |
|-----|----------|----------|----------|--------|
| [Description] | High/Med/Low | `file.ts:123` | YYYY-MM-DD | Open |

---

## Task Breakdown Guidelines

<!--
Reference for writing good tasks.
-->

### Good Task Format
```
- [ ] Extract auth routes to separate file → `main.py:50-120` to `api/auth_routes.py` |
      Endpoints: POST /login, POST /logout, GET /me |
      Validation: curl localhost:3000/api/auth/me (expect 401)
```

**Why good**:
- Specific location (file and line numbers)
- Clear outcome (what endpoints)
- Testable validation (exact command)

### Bad Task Format
```
- [ ] Refactor authentication
```

**Why bad**:
- Vague scope (what exactly?)
- No location (where in codebase?)
- No validation (how do we know it's done?)

---

## Notes

<!--
Implementation notes that don't fit elsewhere.
Keep brief - detail goes in HANDOFF.md or plan.md.
-->

- [Important note about implementation]
- [Gotcha or learning from previous task]

---

## Progress Tracking

**Total Tasks**: [Count]
**Completed**: [Count] ([X]%)
**In Progress**: [Count]
**Blocked**: [Count]

**Current Velocity**: ~[X] tasks per day
**Estimated Completion**: YYYY-MM-DD

---

**Last Updated**: YYYY-MM-DD by [Name]
**Next Review**: YYYY-MM-DD
