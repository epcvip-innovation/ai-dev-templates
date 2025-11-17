# Features Backlog

**Purpose**: Track long-term improvements and enhancements for [Project Name]

**Status Key**:
- 🎯 **Planned** - Accepted, prioritized, not started
- 🚀 **In Progress** - Currently being developed
- ✅ **Complete** - Shipped to production
- ⏸️ **On Hold** - Deferred pending user feedback or dependencies

---

## Tier 1: Do Now (High Value, Low Risk)

<!--
CRITERIA FOR TIER 1:
- High user/business impact
- Low technical risk
- Can be completed in 1-4 hours
- Addresses immediate pain points
- Clear acceptance criteria
-->

### 🎯 Feature #1: [Feature Name]
**Status**: Planned
**Priority**: High
**Effort**: [X hours]
**Value**: [One sentence: impact if we build this]

**Problem**: [1-2 sentences describing user pain point]

**Solution**: [2-4 sentences describing proposed approach]
```
[Optional: Example output, mockup, or data structure]
```

**Implementation Notes**:
- [Key technical consideration 1]
- [Key technical consideration 2]

---

### 🎯 Feature #2: [Feature Name]
**Status**: Planned
**Priority**: High
**Effort**: [X hours]
**Value**: [One sentence: impact]

**Problem**: [User pain point]

**Solution**: [Proposed approach]

**Implementation Notes**:
- [Technical note]

---

## Tier 2: Do Next (High Value, Manage Risk)

<!--
CRITERIA FOR TIER 2:
- High impact but moderate complexity (4-8 hours)
- Requires more planning or architectural decisions
- May have dependencies on other features
- Good "next sprint" candidates
-->

### 🎯 Feature #3: [Feature Name]
**Status**: Planned
**Priority**: Medium-High
**Effort**: [X hours]
**Value**: [One sentence]

**Problem**: [Description]

**Solution**: [Approach with options if applicable]

**Risk**: [What could go wrong, how to mitigate]

**Implementation Notes**:
- [Technical consideration]
- [Alternative approach if primary doesn't work]

---

## Tier 3: Polish (Nice-to-Have)

<!--
CRITERIA FOR TIER 3:
- Improves user experience but not critical
- "Quality of life" improvements
- Can be done in 1-3 hours
- Good for filling gaps between major features
-->

### 🎯 Feature #4: [Feature Name]
**Status**: Planned
**Priority**: Medium
**Effort**: [X hours]
**Value**: [One sentence]

**Problem**: [Minor pain point]

**Solution**: [Simple improvement]

**Implementation Notes**:
- [Keep it simple - avoid scope creep]

---

## Tier 4: Defer (Needs More Information)

<!--
CRITERIA FOR TIER 4:
- Good ideas but blockers exist
- Need user feedback before committing
- Require external dependencies
- High effort with uncertain value
-->

### ⏸️ Feature #5: [Feature Name]
**Status**: On Hold
**Priority**: Low
**Effort**: [X hours]
**Value**: [Potential value if built]

**Problem**: [Problem description]

**Solution**: [Proposed approach]

**Blockers**:
- [Dependency 1: what's needed before we can proceed]
- [Dependency 2: data, user feedback, or technical requirement]

**Decision**: [Why deferred and what would trigger reconsideration]

---

## Future Considerations (Not Yet Prioritized)

<!--
IDEAS PARKING LOT:
- Brainstorming ideas
- User requests that need validation
- "Wouldn't it be cool if..." suggestions
- Keep brief - just enough to remember the idea
-->

### Unprioritized Ideas:
- [Idea 1]: [One sentence description]
- [Idea 2]: [One sentence]
- [Idea 3]: [One sentence]

**Note**: These require user feedback or business validation before moving to tiers.

---

## Sprint Planning Reference

<!--
RECOMMENDED SPRINT BREAKDOWN:
Organize features into achievable sprint goals
-->

**Sprint 1**: Quick Wins (~4-6 hours)
- Feature #1: [Name]
- Feature #2: [Name]

**Sprint 2**: Medium Features (~6-8 hours)
- Feature #3: [Name]

**Sprint 3**: Polish (~3-4 hours)
- Feature #4: [Name]

**Future Sprints**: (pending user feedback)
- Feature #5: [Name] (blocked until [dependency])

---

## Integration with .projects/

<!--
HOW THIS BACKLOG FEEDS INTO ACTIVE WORK:
-->

**Workflow**:
1. **Ideas live here** (FEATURES_BACKLOG.md)
2. **When ready to start**: Run `/start-feature [feature-name]`
3. **Creates**:
   - `.projects/[feature-name]/plan.md` (detailed spec)
   - `.projects/[feature-name]/tasks.md` (implementation breakdown)
4. **During development**: Update feature status in backlog (🚀 In Progress)
5. **When complete**: Mark as ✅ Complete, archive notes in .projects/

**Status sync**:
- FEATURES_BACKLOG.md = high-level status
- .projects/[feature]/ = detailed implementation notes

---

## Tier Definitions

### Tier 1: Do Now
- **Impact**: High
- **Effort**: 1-4 hours
- **Risk**: Low
- **Decision**: Just do it - no analysis paralysis

### Tier 2: Do Next
- **Impact**: High
- **Effort**: 4-8 hours
- **Risk**: Medium (needs planning)
- **Decision**: Plan first (run `/plan-approaches` if complex)

### Tier 3: Polish
- **Impact**: Medium
- **Effort**: 1-3 hours
- **Risk**: Low
- **Decision**: Fill gaps between major features

### Tier 4: Defer
- **Impact**: Uncertain
- **Effort**: High (6+ hours)
- **Risk**: High (blockers exist)
- **Decision**: Wait for user feedback or dependency resolution

---

## Maintenance

**Review Frequency**: Weekly (during sprint planning)

**Questions to Ask**:
- Have any Tier 2-3 features been validated? (promote to Tier 1)
- Have any Tier 4 blockers been resolved? (promote to Tier 2)
- Have any new user requests come in? (add to appropriate tier)
- Are any "Future Considerations" now validated? (promote to tiers)

**Cleanup**:
- Archive completed features (move to separate COMPLETED.md or delete)
- Remove stale ideas (not pursued in 3+ months)
- Consolidate similar ideas

---

**Last Updated**: YYYY-MM-DD
**Maintainer**: [Team/Person]
