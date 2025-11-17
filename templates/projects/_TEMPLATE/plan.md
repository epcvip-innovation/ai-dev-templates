# [Project Name] - Plan

<!--
This is your main specification document. Keep it scannable.

TARGET LENGTH: 2,000-5,000 words (~5-10 pages)
AUDIENCE: Engineers, PMs, stakeholders
LIFECYCLE: Stable after approval (rarely changes)

IF ANY SECTION EXCEEDS 30 LINES: Extract to separate document and link here.
Example: "See [architectural-design.md](./architectural-design.md) for detailed architecture"
-->

**Status**: Draft | Under Review | Approved | Archived
**Author**: [Name]
**Last Updated**: YYYY-MM-DD

---

## Problem Statement

<!--
WHAT PROBLEM are we solving? Use evidence!
- User pain points (quotes, metrics)
- Business impact (revenue, cost, opportunity)
- Technical debt (performance issues, maintenance burden)

Keep to 3-5 paragraphs. This is WHY we're doing this project.
-->

[Describe the problem you're solving]

**Evidence**:
- [Metric or user feedback 1]
- [Metric or user feedback 2]
- [Business impact]

---

## Goals & Success Criteria

<!--
WHAT does success look like? Make it testable.
-->

### Primary Goals

1. **[Goal 1]**: [Measurable outcome]
2. **[Goal 2]**: [Measurable outcome]
3. **[Goal 3]**: [Measurable outcome]

### Success Metrics

- [ ] [Quantitative metric 1: e.g., "Reduce response time from 500ms to <100ms"]
- [ ] [Quantitative metric 2: e.g., "Zero breaking changes to existing API"]
- [ ] [Qualitative metric: e.g., "Code review approval from 2+ senior engineers"]

---

## Non-Goals (Critical for Scope Management!)

<!--
WHAT ARE WE EXPLICITLY NOT DOING?
This is the most important section for keeping AI (and humans) on track.
-->

**Out of Scope for THIS Phase**:
- ❌ NOT refactoring [unrelated system] (already well-structured)
- ❌ NOT adding [new feature X] (separate project)
- ❌ NOT optimizing [Y] for performance (future phase)
- ❌ NOT changing [Z] API contracts (backward compatibility required)

**Future Considerations** (not now):
- [ ] [Feature to consider in Phase 2]
- [ ] [Improvement to revisit later]

---

## Architecture Overview

<!--
HOW are we solving this technically?
Keep high-level here. Deep technical details go in separate docs.
-->

### Current State

[Brief description of how things work today]

**Problems with Current Approach**:
- [Problem 1]
- [Problem 2]

### Proposed Solution

[2-3 paragraphs describing the new approach]

**Key Components**:
1. **[Component 1]**: [Purpose and responsibilities]
2. **[Component 2]**: [Purpose and responsibilities]
3. **[Component 3]**: [Purpose and responsibilities]

**Architecture Diagram** (optional):
```
[ASCII diagram or link to diagram]
```

**For detailed technical design**: See [architectural-design.md](./architectural-design.md)

---

## Options Considered

<!--
WHAT ELSE did we evaluate? WHY did we choose this approach?
This is critical for future reference and avoiding repeated discussions.
-->

### Option A: [Approach Name]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Why rejected**: [One sentence reason]

### Option B: [Approach Name]

**Pros**:
- [Advantage 1]

**Cons**:
- [Disadvantage 1]

**Why rejected**: [One sentence reason]

### Option C: [Chosen Approach]

**Pros**:
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons**:
- [Acknowledged tradeoff 1]
- [Acknowledged tradeoff 2]

**Why chosen**: [Clear rationale]

---

## Integration Points & Dependencies

<!--
WHAT does this touch? WHO needs to be notified?
If this section exceeds 30 lines, extract to integration-notes.md
-->

### Internal Dependencies

- **[System A]**: [How we interact, what could break]
- **[System B]**: [How we interact, what could break]

### External Dependencies

- **[External Service C]**: [Version, SLA, fallback plan]
- **[Library D]**: [Version, migration notes]

### Teams to Notify

- [ ] [Team X] - [Why they care]
- [ ] [Team Y] - [Why they care]

**For detailed integration analysis**: See [integration-notes.md](./integration-notes.md)

---

## Data Model Changes

<!--
WHAT data structures change? Database schema? API contracts?
If complex, extract to separate data-model.md
-->

### Database Changes

[Describe schema changes, migrations needed]

### API Changes

**New Endpoints**:
- `[METHOD] /api/endpoint` - [Description]

**Modified Endpoints**:
- `[METHOD] /api/existing` - [What changed, backward compatibility]

**Deprecated** (if any):
- `[METHOD] /api/old` - [Sunset timeline]

---

## Testing Strategy

<!--
HOW will we validate this works?
If testing is complex, extract to testing-strategy.md
-->

### Unit Tests

- [ ] [Component A] - [Test coverage goal]
- [ ] [Component B] - [Test coverage goal]

### Integration Tests

- [ ] [Scenario 1] - [What we're validating]
- [ ] [Scenario 2] - [What we're validating]

### Manual Testing

- [ ] [User flow 1] - [Expected behavior]
- [ ] [User flow 2] - [Expected behavior]

**For detailed test plan**: See [testing-strategy.md](./testing-strategy.md)

---

## Migration & Rollout Strategy

<!--
HOW do we deploy this safely?
-->

### Phase 1: Development
- [x] Complete plan & design
- [ ] Implement core functionality
- [ ] Local testing

### Phase 2: Staging
- [ ] Deploy to staging environment
- [ ] Integration testing
- [ ] Performance validation

### Phase 3: Production Rollout
- [ ] Deploy behind feature flag (0% traffic)
- [ ] Gradual rollout (10% → 50% → 100%)
- [ ] Monitor metrics
- [ ] Full rollout or rollback

### Rollback Plan
**If issues detected**:
1. [Step to revert]
2. [Rollback command or process]
3. [Notification plan]

---

## Risks & Mitigation

<!--
WHAT could go wrong? How do we handle it?
-->

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [How we'll handle it] |
| [Risk 2] | High/Medium/Low | High/Medium/Low | [How we'll handle it] |
| [Risk 3] | High/Medium/Low | High/Medium/Low | [How we'll handle it] |

---

## Timeline & Milestones

<!--
WHEN will this be done? What are the key checkpoints?
Detailed tasks go in tasks.md, not here.
-->

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Design approval | YYYY-MM-DD | ✅ Complete |
| Core implementation | YYYY-MM-DD | 🏗️ In Progress |
| Integration complete | YYYY-MM-DD | ⏳ Pending |
| Testing complete | YYYY-MM-DD | ⏳ Pending |
| Production deployment | YYYY-MM-DD | ⏳ Pending |

**Total Estimated Effort**: [X weeks/months]

---

## FAQ: For Claude (AI Guidance)

<!--
Pre-answer common questions Claude might ask during implementation.
This prevents scope drift and keeps AI focused.
-->

### Common Questions & Answers

**Q: This code could be improved while I'm here, should I?**
**A**: NO - Extract as-is, improvements in [Phase X / separate project]

**Q: I found a better pattern than what's in the plan, should I use it?**
**A**: Only if explicitly called out in tasks.md. Otherwise, follow plan.md patterns.

**Q: Should I add type hints/docstrings while implementing?**
**A**: [YES - part of quality standards | NO - separate improvement phase]

**Q: There's a bug in existing code, should I fix it?**
**A**: Document in BUGS.md, fix in dedicated bug-fix session (not during feature work)

**Q: Should I add tests while implementing features?**
**A**: [YES - required for each task | NO - testing phase comes later]

**Q: This is taking longer than estimated, what should I do?**
**A**: Stop at next checkpoint, update HANDOFF.md, ask user for guidance

### Red Flags to Watch For

If you find yourself doing any of these, STOP and ask user:
- ⚠️ Functions growing over [50 lines / your standard]
- ⚠️ Adding "just in case" functionality not in tasks.md
- ⚠️ Solving problems that don't exist yet
- ⚠️ Deviating from established code patterns
- ⚠️ Refactoring code that's working fine
- ⚠️ Working on files not mentioned in current task

---

## Open Questions

<!--
WHAT do we still need to decide?
Remove items as they're resolved.
-->

- [ ] [Question 1] - **Owner**: [Name] - **Deadline**: YYYY-MM-DD
- [ ] [Question 2] - **Owner**: [Name] - **Deadline**: YYYY-MM-DD

---

## Related Documents

- **Task Breakdown**: [tasks.md](./tasks.md)
- **Session Notes**: [HANDOFF.md](./HANDOFF.md)
- **Architecture Deep-Dive**: [architectural-design.md](./architectural-design.md)
- **Integration Analysis**: [integration-notes.md](./integration-notes.md)
- **Testing Strategy**: [testing-strategy.md](./testing-strategy.md)
- **Decision Records**: [decisions/](./decisions/)

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Initial plan created | [Name] |
| YYYY-MM-DD | [Major change description] | [Name] |

---

**Document Status**: Draft | Under Review | Approved | Archived
**Last Review Date**: YYYY-MM-DD
**Next Review Date**: YYYY-MM-DD (review quarterly or after major changes)
