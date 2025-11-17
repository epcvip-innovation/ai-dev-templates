# Features Backlog Template

[← Back to Main README](../../README.md)

**Purpose**: Simple tier-based structure for managing feature ideas before they become active .projects/

**Mental Model**: Think of FEATURES_BACKLOG.md as your JIRA ticket backlog, but designed for AI-assisted development workflows.

---

## Quick Start

### For New Projects

```bash
# Copy template to project root
cp templates/features-backlog/FEATURES_BACKLOG.md your-project/

# Edit with your features
cd your-project/
nano FEATURES_BACKLOG.md

# Add features to appropriate tiers
# - Tier 1: High value, low risk (just do it)
# - Tier 2: High value, needs planning
# - Tier 3: Polish/nice-to-have
# - Tier 4: Defer until dependencies resolve
```

### For Existing Projects

If you already track features elsewhere (JIRA, Linear, GitHub Issues):
- Keep your existing system as source of truth
- Use FEATURES_BACKLOG.md as **local planning cache** for AI sessions
- Sync periodically (copy ticket descriptions to backlog format)

---

## The Problem This Solves

### Before FEATURES_BACKLOG.md

**Scattered ideas**:
- Feature requests in Slack threads
- TODOs in code comments
- "We should build..." conversations lost
- No prioritization framework
- AI can't see what's planned

**Result**: Forgotten ideas, duplicated work, unclear priorities

### After FEATURES_BACKLOG.md

**Centralized backlog**:
- All ideas in one place
- Tier-based prioritization (clear focus)
- AI can read and suggest from backlog
- Integration with `/start-feature` command
- Track status transitions (Planned → In Progress → Complete)

**Result**: Clear roadmap, AI-assisted feature selection, nothing forgotten

---

## Where It Fits in Workflow

```
┌─────────────────────────────────────────────────────────┐
│ IDEA COLLECTION                                         │
│                                                         │
│ User requests, team brainstorming, bug reports         │
│         ↓                                               │
│ Add to FEATURES_BACKLOG.md (appropriate tier)          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ PLANNING PHASE                                          │
│                                                         │
│ /start-feature                                          │
│   ├─ Reads FEATURES_BACKLOG.md                         │
│   ├─ Shows features by tier                            │
│   ├─ User selects feature                              │
│   └─ Assess: Simple (<3hrs) or Complex (>3hrs)?       │
│                                                         │
│ If Complex:                                             │
│   ├─ Trigger /plan-approaches                          │
│   ├─ Create .projects/[feature]/plan.md               │
│   └─ Update FEATURES_BACKLOG status → 🚀 In Progress  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ IMPLEMENTATION                                          │
│                                                         │
│ Work in .projects/[feature]/                           │
│ Reference FEATURES_BACKLOG.md for context              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ COMPLETION                                              │
│                                                         │
│ /feature-complete                                       │
│   └─ Update FEATURES_BACKLOG status → ✅ Complete     │
│                                                         │
│ Archive in .projects/[feature]/archive/               │
└─────────────────────────────────────────────────────────┘
```

**Key insight**: FEATURES_BACKLOG.md is the "before .projects/" phase. It stores ideas until you're ready to actively work on them.

---

## Tier System Explained

### Tier 1: Do Now (High Value, Low Risk)

**Criteria**:
- ✅ High user/business impact
- ✅ Low technical risk
- ✅ Can be completed in 1-4 hours
- ✅ Addresses immediate pain points
- ✅ Clear acceptance criteria

**Examples**:
- Fix broken link in navigation
- Add export button to report page
- Improve error message clarity
- Display additional column in table

**Decision rule**: If all criteria met, just do it. No analysis paralysis.

**Typical sprint velocity**: 3-4 Tier 1 features per week

---

### Tier 2: Do Next (High Value, Manage Risk)

**Criteria**:
- ✅ High impact BUT moderate complexity (4-8 hours)
- ✅ Requires planning or architectural decisions
- ✅ May have dependencies on other features
- ⚠️ Need to run `/plan-approaches` before starting

**Examples**:
- Add user authentication system
- Implement search functionality
- Integrate third-party API
- Refactor legacy module

**Decision rule**: Plan first, then execute. Good "next sprint" candidates.

**Typical sprint velocity**: 1-2 Tier 2 features per sprint

---

### Tier 3: Polish (Nice-to-Have)

**Criteria**:
- ✅ Improves UX but not critical
- ✅ "Quality of life" improvements
- ✅ Can be done in 1-3 hours
- ⚠️ Don't prioritize over Tier 1-2

**Examples**:
- Add loading spinners
- Improve button styling
- Add keyboard shortcuts
- Improve mobile responsive design

**Decision rule**: Fill gaps between major features. Don't interrupt flow for these.

**Typical sprint velocity**: 2-3 Tier 3 features in downtime

---

### Tier 4: Defer (Needs More Information)

**Criteria**:
- ⚠️ Good idea but blockers exist
- ⚠️ Need user feedback before committing
- ⚠️ Require external dependencies
- ⚠️ High effort (6+ hours) with uncertain value

**Examples**:
- Timeline Gantt chart (blocked: need real data first)
- Multi-tenant support (blocked: need customer validation)
- Advanced analytics (blocked: need data pipeline first)

**Decision rule**: Don't start until blockers resolved. Revisit quarterly.

**Promotion triggers**:
- User feedback validates value
- Dependency resolved
- New data available

---

## Feature Template Structure

### Minimum Required Fields

```markdown
### 🎯 Feature #X: [Name]
**Status**: Planned
**Priority**: High/Medium/Low
**Effort**: [X hours]
**Value**: [One sentence impact]

**Problem**: [User pain point]

**Solution**: [Proposed approach]
```

**Why these fields**:
- **Status**: Track lifecycle (🎯 Planned → 🚀 In Progress → ✅ Complete)
- **Priority**: Relative importance within tier
- **Effort**: Helps with sprint planning
- **Value**: Forces articulation of "why build this?"
- **Problem**: Grounds feature in real user need
- **Solution**: Clear approach prevents scope drift

### Optional Fields

Add these for complex features:

```markdown
**Implementation Notes**:
- [Technical consideration 1]
- [Alternative approach if primary fails]

**Risk**: [What could go wrong]

**Blockers**:
- [Dependency that must be resolved first]

**Decision**: [Why deferred, what triggers reconsideration]
```

---

## Integration with Slash Commands

### /start-feature

**How it uses FEATURES_BACKLOG.md**:

1. Reads FEATURES_BACKLOG.md
2. Parses features by tier
3. Shows list: "Available features: #1 (Tier 1), #2 (Tier 1), #3 (Tier 2)..."
4. User selects feature number
5. Assesses complexity based on effort estimate
6. Creates .projects/[feature]/ if complex
7. **Updates FEATURES_BACKLOG.md status** → 🚀 In Progress

**Example interaction**:
```
You: /start-feature

Claude: I found 8 features in FEATURES_BACKLOG.md:

Tier 1 (Do Now):
  #1: Export to CSV (1hr) - High priority
  #2: Fix broken pagination (2hrs) - High priority

Tier 2 (Do Next):
  #3: Add user authentication (6hrs) - Medium priority

Which feature would you like to start? (Enter number)

You: 3

Claude: Feature #3 is complex (6hrs). Running /plan-approaches to evaluate options...
```

### /feature-complete

**How it updates FEATURES_BACKLOG.md**:

1. Completes .projects/[feature]/ work
2. Archives session notes
3. **Updates FEATURES_BACKLOG.md**:
   - Changes status → ✅ Complete
   - Adds completion date
   - Optionally adds "What was actually built" summary

**Example**:
```markdown
### ✅ Feature #3: Add User Authentication
**Status**: Complete (Sprint 2)
**Priority**: High
**Effort**: 6 hours (actual: 7 hours)
**Value**: Enables personalized features
**Completed**: 2025-11-02

**Problem**: No way to identify users or save preferences

**Solution Implemented**: JWT-based auth with email/password
- Backend: FastAPI with bcrypt password hashing
- Frontend: React context for auth state
- Database: Users table with hashed passwords

**What Changed from Plan**:
- Added "remember me" functionality (not originally planned)
- Deferred OAuth integration to Phase 2
```

---

## Tier Promotion/Demotion

### When to Promote

**Tier 4 → Tier 2**:
- Blocker resolved (dependency shipped, user feedback received)
- Business priority increased

**Tier 3 → Tier 1**:
- User complaints indicate polish is actually critical
- Quick win that unblocks other work

**Tier 2 → Tier 1**:
- Risk mitigated (prototype validated approach)
- Simpler implementation discovered

### When to Demote

**Tier 1 → Tier 3**:
- Lower priority than anticipated
- Technical risk discovered

**Tier 2 → Tier 4**:
- Blocker discovered during planning
- User feedback suggests different approach needed

**Any Tier → Removed**:
- User feedback invalidates need
- Replaced by better approach
- Business priorities shifted

---

## Maintenance Best Practices

### Weekly Review (During Sprint Planning)

**Questions to ask**:
1. Have any Tier 2-3 features been validated? → Promote to Tier 1
2. Have any Tier 4 blockers been resolved? → Promote to Tier 2
3. Have new user requests come in? → Add to appropriate tier
4. Are any "Future Considerations" validated? → Promote to tiers
5. Are any features stale (3+ months, no movement)? → Remove or defer

### Quarterly Cleanup

**Actions**:
- Archive completed features (move to COMPLETED.md or delete)
- Remove abandoned ideas (not pursued in 3+ months)
- Consolidate similar ideas
- Re-validate Tier 4 blockers (still blocked or can promote?)

### Keep It Lean

**Anti-patterns** (avoid these):
- ❌ 50+ features in backlog (overwhelming)
- ❌ Detailed specs in FEATURES_BACKLOG.md (goes in .projects/)
- ❌ Features without clear problem statements
- ❌ Everything marked "High priority"

**Target**:
- ✅ 5-10 Tier 1 features (enough for 2-3 sprints)
- ✅ 3-5 Tier 2 features (next month's work)
- ✅ 3-5 Tier 3 polish items
- ✅ <5 Tier 4 deferred items

---

## Alternatives to FEATURES_BACKLOG.md

### When to Use FEATURES_BACKLOG.md

✅ **Use if**:
- Solo developer or small team (2-3 people)
- Working primarily with Claude Code
- Want simple, local, markdown-based tracking
- Need AI to see and suggest from backlog
- Prefer lightweight over feature-rich

### When to Use External Tools

✅ **Use JIRA/Linear/GitHub Issues if**:
- Team >5 people
- Need collaboration features (assignments, comments, approvals)
- Require integrations (Slack, email notifications)
- Need detailed reporting/analytics
- Multi-project tracking

**Hybrid approach**: Use both
- JIRA = source of truth for team
- FEATURES_BACKLOG.md = local cache for AI sessions (sync weekly)

---

## Location Flexibility

### Where to Store FEATURES_BACKLOG.md

**Option A: Project root** (recommended for most projects)
```
your-project/
├── FEATURES_BACKLOG.md  ← Here
├── CLAUDE.md
├── README.md
└── src/
```

**Pros**: Easy to find, top-level visibility
**Cons**: Clutters root directory

---

**Option B: docs/** (recommended for teams, public repos)
```
your-project/
├── docs/
│   ├── FEATURES_BACKLOG.md  ← Here
│   └── planning/
├── CLAUDE.md
└── src/
```

**Pros**: Organized with other docs, professional appearance
**Cons**: Slightly less discoverable

---

**Option C: docs/planning/** (used in dois-test-capacity-planner)
```
your-project/
├── docs/
│   └── planning/
│       ├── FEATURES_BACKLOG.md  ← Here
│       ├── TASKS.md
│       └── features/
└── src/
```

**Pros**: Co-located with planning docs, clear context
**Cons**: Deeper nesting, requires docs/planning/ structure

---

**Recommendation**: Start with Option A (project root). Move to Option B/C if repo has established docs/ structure.

---

## Example: Complete Feature Lifecycle

### Stage 1: Idea Collection

User says: "It would be nice to export our capacity report to share with the team."

**Action**: Add to FEATURES_BACKLOG.md
```markdown
### 🎯 Feature #6: Export Capacity Report
**Status**: Planned
**Priority**: Medium
**Effort**: 1 hour
**Value**: Enables team collaboration

**Problem**: No way to share capacity analysis. Users resort to screenshots.

**Solution**: Add "Copy to Clipboard" button that formats as markdown table
```

### Stage 2: Planning

Run `/start-feature`:
```
Claude: Feature #6 is simple (1hr). Creating task in TASKS.md...
```

No .projects/ needed (simple feature).

### Stage 3: Implementation

Work on feature, use TodoWrite to track progress.

### Stage 4: Completion

Run `/feature-complete`:
```
Claude: Feature #6 complete. Updating FEATURES_BACKLOG.md status...
```

**FEATURES_BACKLOG.md updated**:
```markdown
### ✅ Feature #6: Export Capacity Report
**Status**: Complete
**Completed**: 2025-11-02
**Effort**: 1 hour (actual: 45 minutes)

**What was built**: Copy to clipboard button with markdown formatting
```

---

## FAQ

### Q: Do I need both FEATURES_BACKLOG.md AND TASKS.md?

**A**: Yes, different purposes:
- **FEATURES_BACKLOG.md**: High-level feature descriptions (pre-planning)
- **TASKS.md**: Granular implementation steps (during execution)

**Relationship**: FEATURES_BACKLOG → (planning) → TASKS.md

### Q: Should I track bugs in FEATURES_BACKLOG.md?

**A**: No, create separate BUGS.md or use issue tracker.
- **Bugs**: Things that are broken and need fixing
- **Features**: New functionality that doesn't exist yet

### Q: How detailed should feature descriptions be?

**A**: 3-5 sentences max in FEATURES_BACKLOG.md
- Problem (1-2 sentences)
- Solution (2-3 sentences)
- Detailed specs go in .projects/[feature]/plan.md when you start work

### Q: What if a feature spans multiple sprints?

**A**: Break it down:
- Create parent feature in Tier 2
- Break into sub-features in Tier 1
- Example: "User Authentication" (Tier 2) → "Email/Password Login" (Tier 1), "OAuth Integration" (Tier 1), "Password Reset" (Tier 1)

### Q: Can I have multiple people working from the same backlog?

**A**: Yes, but:
- Add "Owner" field to features
- Use status emojis: 🚀 In Progress (Owner: Alice)
- Coordinate to avoid conflicts
- Consider JIRA for teams >5 people

---

## Templates for Common Feature Types

### Bug Fix That Became a Feature
```markdown
### 🎯 Feature #X: [Name]
**Status**: Planned
**Priority**: High
**Effort**: 2 hours
**Value**: Fixes critical user issue + improves UX

**Problem**: [Bug description + broader UX issue]

**Solution**: [Bug fix + enhancement]

**Note**: Originally reported as bug #123, expanded scope to improve overall flow
```

### User Request
```markdown
### 🎯 Feature #X: [Name]
**Status**: Planned
**Priority**: Medium
**Effort**: 3 hours
**Value**: Directly addresses user feedback

**Problem**: [User pain point from feedback]

**Solution**: [Proposed implementation]

**User Quote**: "[Direct quote from user request/feedback]"
```

### Technical Debt Paydown
```markdown
### 🎯 Feature #X: Refactor [Component]
**Status**: Planned
**Priority**: Medium
**Effort**: 4 hours
**Value**: Improves maintainability, enables future features

**Problem**: Current [component] is 500+ lines, hard to modify

**Solution**: Break into smaller modules with clear responsibilities

**Enables**: Feature #Y (blocked by current structure)
```

---

## Related Templates

**Slash commands**:
- [start-feature](../slash-commands/feature-workflow/start-feature.md) - Reads FEATURES_BACKLOG.md
- [feature-complete](../slash-commands/completion/feature-complete.md) - Updates status
- [plan-approaches](../slash-commands/analysis/plan-approaches.md) - Evaluates complexity

**Project organization**:
- [.projects/](../projects/) - Where features go after planning

---

**Last Updated**: 2025-11-02
**Maintained By**: dev-setup template library
