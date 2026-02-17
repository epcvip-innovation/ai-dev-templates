# Plan Quality Rubric v1.0

**Purpose:** Systematic evaluation of feature plans using boolean checks (AI-friendly, deterministic).

**Last Updated:** 2025-11-15  
**Review Schedule:** Quarterly or after 5+ replanned features

---

## How to Use This Rubric

**For Claude Code:**
- Run this checklist in `/validate-plan`, `/start-feature`, `/resume-feature`
- Each check is boolean (Pass/Fail) - no subjective percentages
- Quote evidence from plan for each check
- Clear recommendations for failures

**For Developers:**
- Reference when creating plans manually
- Use as pre-implementation checklist
- Update "Calibration" section based on real outcomes

---

## ✅ Ready to Implement

Plan passes **all** checks in sections 1-5.

### 1. Scope Clarity (5 checks)

- [ ] **Goal is specific and measurable**
  - ❌ BAD: "Improve authentication"
  - ✅ GOOD: "Add Google OAuth restricted to @company.com domain"
  - **Evidence needed:** Clear goal statement with measurable outcome

- [ ] **Success criteria are testable**
  - ❌ BAD: "Make it fast"
  - ✅ GOOD: "Query validation completes in <5 seconds"
  - **Evidence needed:** List of acceptance criteria with numbers/behaviors

- [ ] **Out-of-scope is explicitly documented**
  - ❌ BAD: No mention of what's NOT included
  - ✅ GOOD: "This does NOT include query generation API (see Feature #4)"
  - **Evidence needed:** "Out of scope" or "Not included" section

- [ ] **No vague language in goal description**
  - ❌ BAD: "Generally improve", "Better", "More robust"
  - ✅ GOOD: "Add error handling for X", "Reduce latency from Y to Z"
  - **Evidence needed:** Concrete verbs (add, reduce, implement, migrate)

- [ ] **Dependencies are identified and available**
  - ❌ BAD: "Use authentication library" (which one?)
  - ✅ GOOD: "Use Authlib 1.2+ (already in requirements.txt)"
  - **Evidence needed:** Explicit library/service names with availability confirmation

### 2. Feasibility (4 checks)

- [ ] **All required resources exist or are obtainable**
  - Check: API keys, credentials, libraries, infrastructure
  - ❌ FAIL: Needs SMTP but no provider configured
  - ✅ PASS: Google OAuth credentials secured in Railway (sealed variables)

- [ ] **No unknowns flagged without resolution plan**
  - ❌ BAD: "TBD: Decide approach during implementation"
  - ✅ GOOD: "Approach A selected (see decision rationale)" OR "Research task: Evaluate JWT vs Session (1 hour)"
  - **Evidence needed:** No "TBD" markers OR research task scheduled

- [ ] **Technical approach is justified**
  - ❌ BAD: "Use FastAPI" (no explanation why)
  - ✅ GOOD: "Use FastAPI (industry standard, matches OAuth patterns, team experience)"
  - **Evidence needed:** "Why this approach" section with rationale

- [ ] **No blockers exist that prevent implementation**
  - Check: Infrastructure ready, permissions granted, dependencies met
  - ❌ FAIL: Needs database but database not deployed
  - ✅ PASS: All prerequisites complete (validator-api exists, OAuth configured)

### 3. Implementability (4 checks)

- [ ] **Tasks are concrete, not abstract**
  - ❌ BAD: "Implement authentication"
  - ✅ GOOD: "Create OAuth 2.0 credentials in Google Cloud Console"
  - **Evidence needed:** Tasks with specific actions (create, update, deploy, test)

- [ ] **Each task has acceptance criteria**
  - ❌ BAD: "Task 2.1: Add endpoint"
  - ✅ GOOD: "Task 2.1: Add /api/validate endpoint (accepts JSON, returns ValidationResponse, requires JWT)"
  - **Evidence needed:** Each task lists "what done looks like"

- [ ] **Test/verification strategy exists**
  - ❌ BAD: No mention of how to verify it works
  - ✅ GOOD: "Test: curl POST with valid query → returns 200, Test: curl without JWT → returns 401"
  - **Evidence needed:** Testing section OR acceptance criteria include verification

- [ ] **Files/components to modify are identified**
  - ❌ BAD: "Update the code"
  - ✅ GOOD: "Modify: streamlit_app.py (add st.login), secrets.toml (add OAuth config)"
  - **Evidence needed:** Specific file paths in task descriptions

### 4. Size Appropriateness (3 checks)

- [ ] **Total effort is ≤15 hours** (or explicitly approved as multi-feature epic)
  - ❌ FAIL: 25 hours (must split)
  - ⚠️ WARNING: 12 hours (Tier 2 - requires milestones)
  - ✅ PASS: 4 hours (Tier 1 - single session)

- [ ] **Checkpoints exist every 6 hours for Tier 2 features** (7-15h)
  - ❌ FAIL: 12-hour plan with no checkpoints
  - ✅ PASS: Checkpoint after Phase 1 (3h), Phase 2 (6h), Phase 3 (10h)
  - **Evidence needed:** "Checkpoint" tasks with drift check + review

- [ ] **Shippable milestones exist for multi-session features**
  - ❌ BAD: "Phase 1-4 must all complete before deployment"
  - ✅ GOOD: "Phase 1 deployable independently (OAuth working, validation pending)"
  - **Evidence needed:** Each phase marked as "🟢 Safe pause" or "🟡 Risky"

### 5. Technical Soundness (3 checks)

- [ ] **Follows CLAUDE.md standards and anti-patterns**
  - Check: Anti-slop (no over-abstraction, functions <50 lines, direct implementation)
  - ❌ FAIL: Creates factory pattern for single use case
  - ✅ PASS: Direct implementation, minimal abstraction, follows project patterns

- [ ] **Architectural decisions are documented**
  - If multiple valid approaches exist, decision rationale is provided
  - ❌ BAD: "We'll use approach B" (no explanation)
  - ✅ GOOD: "Approach B selected: Separate services (pros: API access, cons: $5 more/month)"

- [ ] **Technical debt or shortcuts are documented with payback plan**
  - ❌ BAD: Takes shortcut silently
  - ✅ GOOD: "Shortcut: Skip email verification for MVP (add in Phase 4 before public launch)"
  - **Evidence needed:** "Technical debt" section OR inline notes about deferred work

---

## ⚠️ Needs Refinement

Plan has **1-2 checks** that fail. Fixable in 10-30 minutes.

### Warning Signs

🚩 **Vague tasks:** "Implement feature X" without concrete steps  
🚩 **TBD markers:** "Decide during implementation" (unknowns not resolved)  
🚩 **No testing:** Plan doesn't mention verification strategy  
🚩 **Scope creep indicators:** "Also add", "While we're at it", "Might as well"  
🚩 **Unclear dependencies:** "Use library X" (which version? already installed?)  
🚩 **Missing checkpoints:** Multi-session plan with no review points  

### Action Required

1. **Run `/plan-approaches`** if multiple valid approaches exist (design decision needed)
2. **Break down vague tasks** into concrete steps with acceptance criteria
3. **Remove scope creep** - defer nice-to-haves to backlog
4. **Add missing checkpoints** - every 6 hours for Tier 2
5. **Document test strategy** - how will you verify each task?

**Time to fix:** 10-30 minutes (update plan document)

---

## 🚫 Not Ready (Stop and Address)

Plan has **red flags** - attempting implementation will likely fail.

### Red Flags

❌ **Missing prerequisites:** "Integrate with API X" but API X doesn't exist yet  
❌ **Unsolved design questions:** Multiple valid approaches, no decision made  
❌ **Effort >20 hours:** Epic-sized, needs splitting into smaller features  
❌ **No clear value:** "Might be useful" vs "solves problem Y" (unclear why)  
❌ **Technical impossibility:** Requires capabilities that don't exist  
❌ **Circular dependencies:** Task A needs B, but B needs A completed first  
❌ **Goal mismatch:** Plan doesn't actually achieve stated goal  

### Action Required

1. **Run `/validate-scope`** - Identify blockers preventing implementation
2. **Split feature** - Use `/split-feature` or manual breakdown (>15h → multiple features)
3. **Resolve design questions** - Run `/plan-approaches`, make decision, document rationale
4. **Defer to backlog** - If not ready, add to backlog for future grooming
5. **Rewrite goal** - Ensure plan actually achieves what's stated

**Do not proceed** until red flags resolved.

---

## 🔄 Session Resume Evaluation

When resuming a feature in a new session (via `/resume-feature`), evaluate drift:

### Has Plan Diverged? (Boolean Checks)

- [ ] **Goal unchanged?** (Compare original plan vs HANDOFF.md)
  - YES → Continue
  - NO → Major drift, run `/replan-feature`

- [ ] **Approach unchanged or only refined?**
  - Same approach → Continue
  - Minor refinement → Document in plan, continue
  - Major change → Major drift, run `/replan-feature`

- [ ] **Task count drift ≤2?** (Count: added tasks - removed tasks)
  - ≤2 → Healthy evolution
  - 3-5 → Moderate drift, update plan
  - >5 → Major drift, run `/replan-feature`

- [ ] **No major blockers discovered?**
  - No blockers → Continue
  - Workaround exists → Document, continue
  - Fundamental blocker → Stop, resolve before continuing

- [ ] **Time drift <2x estimate?** (Ask user: "Did this take 2x longer than planned?")
  - No → Healthy
  - Yes, but explainable → Update estimates, continue
  - Yes, and unclear why → Major drift, reassess plan

### Drift Categories

**✅ Healthy Evolution** (All checks pass)
- Estimates within ±25%
- Discovered 1-2 edge cases (unplanned tasks)
- Minor approach refinements
- **Action:** Document in HANDOFF.md, continue

**⚠️ Moderate Drift** (1-2 checks fail)
- Estimates off by 25-50%
- Added 3-5 unplanned tasks
- Approach modified but goal unchanged
- **Action:** Update plan.md with revised estimates, document why, continue

**🚫 Major Drift** (Red flag present)
- Goal changed from original
- Estimates off by >50% OR >2x time
- Complete approach overhaul
- Added >5 unplanned tasks
- **Action:** Stop, run `/replan-feature`, get user approval before continuing

---

## Decision Matrix

| Situation | Assessment | Action | Time |
|-----------|------------|--------|------|
| All checks pass | ✅ Ready | Proceed with confidence | 0 min |
| 1-2 checks fail | ⚠️ Refine | Fix issues, then proceed | 10-30 min |
| Red flags present | 🚫 Not Ready | Stop, run validation/split commands | 1+ hour |
| Resume: No drift | ✅ Continue | Load context and continue | 5 min |
| Resume: 1-2 checks fail | ⚠️ Update | Update plan, document drift | 10 min |
| Resume: Red flag | 🚫 Replan | Run `/replan-feature` | 30-60 min |

---

## Real Examples (Calibration)

### Example 1: OAuth Authentication Feature (PASS with Refinement)

**Original plan assessment:**

**Scope Clarity:** ✅ PASS (5/5)
- Goal specific: "Add Google OAuth restricted to @company.com"
- Success criteria: "Only @company.com users can access"
- Out-of-scope: "Does NOT include query generation API"
- No vague language
- Dependencies clear: Google OAuth credentials, Railway deployment

**Feasibility:** ✅ PASS (4/4)
- Resources available: Google OAuth configured, Railway sealed variables
- No unknowns: Approach decided (dual authentication strategy)
- Approach justified: FastAPI + Streamlit st.login (fast MVP + API ready)
- No blockers: Infrastructure exists

**Implementability:** ✅ PASS (4/4)
- Tasks concrete: "Upgrade Streamlit 1.28 → 1.42", "Configure secrets.toml"
- Acceptance criteria: "st.login() works", "JWT validation accepts both tokens"
- Test strategy: Manual testing with @company.com account + non-domain rejection
- Files identified: streamlit_app.py, secrets.toml, validator-api/main.py

**Size:** ⚠️ WARNING (2/3)
- Effort: 20 hours (Tier 2 - multi-session)
- ❌ Missing: Checkpoints every 6 hours
- ✅ Has: Shippable milestones (Phase 1, Phase 2 deploy independently)

**Technical Soundness:** ✅ PASS (3/3)
- Follows standards: Direct implementation, no over-abstraction
- Decisions documented: "Approach B: Separate services (rationale provided)"
- Debt documented: None (clean implementation)

**Overall:** ⚠️ Needs Refinement (missing checkpoints)  
**Action:** Add checkpoint tasks after Phase 1, 2, 4  
**Time to fix:** 10 minutes  
**After fix:** ✅ Ready to implement

---

### Example 2: Streamlit OAuth Integration (PASS)

**Scope Clarity:** ✅ PASS (5/5)
- Goal: "Dual authentication: Streamlit st.login + validator-api JWT"
- Success: "Both paths authenticate @company.com, validator-api accepts both tokens"
- Out-of-scope: Explicit (browser access only, not CLI scripts)
- Concrete language: "Upgrade", "Configure", "Update", "Deploy"
- Dependencies: Google OAuth (exists), Streamlit 1.42+ (available)

**Feasibility:** ✅ PASS (4/4)
- Resources: OAuth credentials secured, Railway services exist
- No unknowns: Approach validated via web research (Nov 2025 docs)
- Justified: Built-in OAuth (official Streamlit feature, maintained)
- No blockers: Can upgrade Streamlit without breaking changes

**Implementability:** ✅ PASS (4/4)
- Concrete tasks: "Upgrade Streamlit", "Install google-auth", "Update get_current_user()"
- Acceptance: "st.login() works", "OIDC tokens validated", "Both auth paths tested"
- Test strategy: Manual testing both paths (Streamlit UI + API call with JWT)
- Files: requirements.txt, secrets.toml, streamlit_app.py, validator-api/main.py

**Size:** ✅ PASS (3/3)
- Effort: 4 hours (Tier 1 - single session)
- No checkpoints needed (≤6 hours)
- Single milestone: Deploy both services

**Technical Soundness:** ✅ PASS (3/3)
- Standards: Direct implementation, official library usage
- Decision: Dual token approach justified (fast + future-proof)
- No debt: Clean implementation

**Overall:** ✅ Ready to Implement  
**Action:** Proceed immediately

---

### Example 3: Hypothetical Bad Plan (FAIL - Not Ready)

**Goal:** "Improve query performance" (vague)

**Issues found:**
- ❌ Scope Clarity: Goal not measurable (improve by how much?)
- ❌ Scope Clarity: No out-of-scope defined
- ❌ Feasibility: No approach selected (caching? indexing? query optimization?)
- ❌ Implementability: Tasks vague ("optimize queries")
- ❌ Size: Effort "TBD" (no estimate)

**Overall:** 🚫 Not Ready (5+ failures)  
**Action:** Stop, rewrite plan with:
1. Specific goal: "Reduce validation time from 30s to <5s"
2. Out-of-scope: "Not including Athena query optimization (AWS side)"
3. Selected approach: "Cache ValidationEngine results for 1 hour"
4. Concrete tasks: "Add Redis dependency", "Implement cache layer", "Add cache TTL config"
5. Effort estimate: 6 hours (based on similar caching tasks)

---

## Calibration & Updates

### Update Process

**After each feature:**
1. Run `/check-drift` to compare plan vs actual
2. Note which estimates were accurate vs inaccurate
3. Update this section with learnings

**Quarterly review:**
1. Analyze last 10+ features
2. Identify systematic biases (always underestimate auth tasks?)
3. Update benchmarks in TASK_ESTIMATION_GUIDE.md

### Current Calibration (2025-11-15)

| Feature Type | Typical Estimate | Actual Average | Adjustment Needed |
|--------------|------------------|----------------|-------------------|
| OAuth/Auth tasks | 2-4 hours | 2.5-5 hours | +25% buffer |
| Schema caching | 2 hours | 0.25 hours | Reduce to 1 hour |
| API endpoint (simple) | 1-2 hours | 1.5 hours | Accurate |
| API endpoint (complex) | 3-4 hours | TBD | Monitor |
| Streamlit UI updates | 1-2 hours | TBD | Monitor |

**Patterns identified:**
- Authentication tasks consistently take 25% longer than estimated (OAuth complexity)
- Caching tasks significantly overestimated (simple implementation)
- First feature in new domain: Add 50% buffer (learning curve)

**Next review:** 2026-05-16 (or after 5 more features completed)

---

## Version History

**v1.0** (2025-11-15)
- Initial rubric with boolean checks
- Based on OAuth feature analysis
- Calibration section initialized
- Examples from data-query-tool project

---

**This rubric is referenced by:**
- `/validate-plan` command
- `/start-feature` command (Step 4.5)
- `/resume-feature` command (Step 4.5)
- `/check-drift` command (drift categorization)

