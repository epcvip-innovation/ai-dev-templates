---
description: Add discovered task to current feature with systematic scope evaluation
argument-hint: task-description
allowed-tools: read_file, search_replace, grep, list_dir
---

## Command

Capture tasks discovered during implementation, evaluate scope impact, and integrate systematically into the plan.

**When to use:**
- Discover edge case that needs handling during implementation
- Realize error handling is needed
- Find performance issue requiring optimization
- User suggests enhancement mid-implementation
- Blocker discovered that must be resolved

**When NOT to use:**
- Task was already in the plan (just implement it)
- Trivial change (<15 min) - just do it and note in handoff
- Unrelated to current feature (add to backlog separately)

## Step 1: Capture Task Details

**Ask user for details:**
```
📋 NEW TASK DISCOVERY

What task did you discover?
Name: [User input]

Why is this needed?
- [ ] Blocker (current work can't proceed without it)
- [ ] Edge case (discovered during testing)
- [ ] Enhancement (nice-to-have improvement)
- [ ] Technical debt (shortcut needs cleanup)
- [ ] Security/performance issue

Estimated effort: [User input or estimate]
Should it block current work? [Y/N]
```

---

## Step 2: Evaluate Scope Impact

**Load current feature context:**
1. Read `backlog/[name]/plan.md`
2. Read `HANDOFF.md` (if exists)
3. Check task tracking for current progress

**Calculate impact:**
```
📊 SCOPE IMPACT ANALYSIS

🆕 New Task: [Name]
├─ Type: [Blocker / Edge Case / Enhancement / Debt / Security]
├─ Effort: +[X] hours
├─ Current feature progress: [Y% complete or "Phase N of M"]
├─ Original estimate: [Z hours]
├─ New total if added: [Z + X hours]
└─ Drift: +[N%] from original

🎯 CATEGORIZATION: [✅ Necessary Evolution / ⚠️ Nice-to-Have / 🚫 Scope Creep]
```

### ✅ Necessary Evolution
**Indicators:**
- Blocker preventing current work
- Edge case discovered during testing
- Security/correctness issue found
- Required for feature to work

**Action:** Add to current feature, document as discovery

### ⚠️ Nice-to-Have Enhancement
**Indicators:**
- Improves UX but not required
- Performance optimization (not critical)
- Additional feature request
- "While we're at it" additions

**Decision point:** Add now (extend timeline) or defer to backlog?

### 🚫 Scope Creep
**Indicators:**
- Unrelated to original feature goal
- Changes core requirements
- Adds new capabilities beyond plan
- Significantly larger than described (>3 hours)

**Action:** Defer to backlog, create separate feature

---

## Step 3: Placement Decision

**Present options to user:**

```
📍 PLACEMENT OPTIONS

### Option A: Add to Current Feature (Extend Timeline)
**Impact:** Feature effort increases [Z]h → [Z+X]h
**Timeline:** +[X] hours (now Tier [1/2])
**Choose if:** Task is blocker or necessary for correctness

### Option B: Defer to Backlog (Separate Feature)
**Impact:** No change to current feature
**Timeline:** Current feature stays on track
**Choose if:** Enhancement or can ship without it

### Option C: Create Sub-Project (Large Discovery)
**Impact:** Current feature stays focused, new project created
**Choose if:** Task is >3h and substantial

Which option? [A/B/C]
```

---

## Step 4: Execute Chosen Option

### If Option A (Add to Current Feature)

**1. Update plan.md:**
```markdown
### Phase [N]: [Current Phase]

**Tasks:**
- [ ] Original task 1
- [ ] Original task 2
- [ ] 🆕 [New task name] - ADDED [date]
      **Reason:** [Why added - blocker/discovery/refinement]
      **Effort:** +[X hours]
      **Type:** [Necessary evolution / Enhancement]
```

**2. Update plan header:**
```markdown
## Effort Estimation

**Original:** [Z] hours
**Current:** [Z+X] hours (+[X]h for [reason])

**Status:** [Tier 1 / Tier 2] ([Note if tier changed])
```

**3. Add Plan Revision entry:**
```markdown
## Plan Revisions

### [Date] - Added: [Task name]
**Reason:** [Why added - blocker/discovery/edge case/enhancement]
**Impact:** +[X] hours (now [Total]h total)
**Type:** [Necessary evolution / Deferred enhancement / Scope creep]
**Decision:** [Why added now vs deferred]
```

**4. Update HANDOFF.md:**
```markdown
## Changes This Session

**Task Added:** [Name] (+[X]h)
- **Why:** [Reason]
- **Impact:** Timeline extended [Z]h → [Z+X]h
- **Status:** [Pending / In Progress]
```

---

### If Option B (Defer to Backlog)

**1. Add to _BACKLOG.md:**
```markdown
### Feature: [Task name]
**Effort:** [X hours]
**Priority:** [High/Medium/Low]
**Value:** [What problem it solves]

**Context:** Discovered during [Current feature]
**Dependency:** [Current feature] should complete first
```

**2. Note in current plan.md:**
```markdown
## Out of Scope (Deferred)

- **[Task name]:** Deferred to backlog (Feature #N)
  - **Why deferred:** [Reason - not blocking, enhancement, etc.]
  - **When to revisit:** [After current feature / When priority increases]
```

---

### If Option C (Create Sub-Project)

**1. Run `/start-feature`** for new task

**2. Link features in documentation:**
```markdown
## Related Features

- **[New feature name]:** Created as separate project
  - **Why separate:** [Reason - substantial scope, different focus]
  - **Link:** `backlog/[new-feature-name]/`
```

---

## Step 5: Confirm and Continue

```
✅ TASK INTEGRATED

📋 Task: [Name]
├─ Added to: [Current feature / Backlog / New sub-project]
├─ Impact: [Timeline change or "No impact"]
├─ Documents updated: [List]
└─ Next action: [What to do next]

Current feature status:
- Original: [Z]h
- Current: [Z+X]h (if changed)
- Progress: [Y% complete]

Ready to continue? [Y/n]
```

---

## Key Principles

1. **Systematic evaluation** - Not subjective "feels like scope creep"
2. **Clear categorization** - Necessary vs Nice-to-have vs Creep
3. **User decision** - Present options, user chooses
4. **Document rationale** - Why added/deferred for future reference
5. **Preserve visibility** - All changes tracked in plan revisions

---

## Integration with Other Commands

**Triggered by:**
- User manually runs `/add-task [description]`
- User mentions "we should also add..." during implementation
- Claude proactively asks: "Should we add X as a task?"

**Feeds into:**
- `plan.md` updates (if Option A)
- `_BACKLOG.md` (if Option B)
- `/start-feature` (if Option C)
- `HANDOFF.md` (notes discoveries)

**Works with:**
- `/check-drift` - Tracks unplanned tasks as drift metric
- `/session-handoff` - Documents task additions
- `/validate-plan` - Checks if new total still reasonable

