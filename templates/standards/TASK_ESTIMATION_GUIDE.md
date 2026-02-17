# Task Estimation Guide v1.0

**Purpose:** Calibrated benchmarks for estimating feature effort in AI-driven development workflows.

**Last Updated:** 2025-11-15  
**Project:** data-query-tool (primary calibration source)  
**Methodology:** Track estimated vs actual hours, adjust benchmarks based on patterns

---

## Quick Reference: Size Tiers

| Tier | Hours | Session Count | Characteristics | Use Case |
|------|-------|---------------|-----------------|----------|
| **Tier 1: Simple** | 1-6h | 1 session | Single file/component, config, straightforward logic | 80% of features |
| **Tier 2: Moderate** | 7-15h | 2-3 sessions | Multi-file, integration, new subsystem | 15% of features |
| **Tier 3: Complex** | >15h | 3+ sessions | **Must split into Tier 1/2 features** | Avoid (split first) |

**Target:** Plan most features as Tier 1 (≤6 hours, single session)

---

## Tier 1: Simple Features (1-6 hours)

### Characteristics
- Single file or component
- Configuration changes
- UI updates (buttons, forms, styling)
- Simple integrations (1-2 API calls)
- No architectural decisions
- Self-contained changes

### Examples from This Project

**Example 1: Schema Caching (Actual: 0.25 hours)**
```markdown
Feature: Cache schemas for 5 MTX tables
Original estimate: 2 hours
Actual time: 15 minutes (-87% drift)
Learning: Simple caching tasks overestimated
```

**Tasks:**
- Run discovery script for 5 tables (10 min)
- Verify schemas cached correctly (5 min)

**Why faster than estimated:**
- Script already existed (just needed table names)
- No edge cases discovered
- Caching mechanism well-established

**Calibrated estimate for similar tasks:** 1 hour

---

**Example 2: OAuth Credentials Setup (Actual: ~2 hours)**
```markdown
Feature: Configure Google OAuth in Google Cloud Console
Original estimate: 2 hours
Actual time: ~2 hours (accurate)
```

**Tasks:**
- Create Google Cloud project (15 min)
- Configure OAuth consent screen (30 min)
- Create credentials (15 min)
- Test auth flow (30 min)
- Save to Railway sealed variables (15 min)
- Troubleshoot redirect URI (15 min)

**Calibrated estimate for similar tasks:** 2 hours (accurate)

---

**Example 3: Add Copy-to-Clipboard Button (Hypothetical: 1 hour)**
```markdown
Feature: Add copy button to query output
Estimated: 1 hour
```

**Tasks:**
- Create CopyButton component (20 min)
- Add to query output section (10 min)
- Add toast notification (20 min)
- Test with long queries (10 min)

**Calibrated estimate:** 1 hour

---

### Estimation Guidelines (Tier 1)

**Single file changes:** 0.5-2 hours
- Add function: 0.5-1 hour
- Add component: 1-2 hours
- Refactor existing: 1-2 hours

**Configuration changes:** 0.5-1 hour
- Update config file: 0.5 hour
- Add environment variable: 0.5 hour
- Railway/deployment config: 1 hour

**UI updates:** 1-3 hours
- Add button/form: 1 hour
- Style updates: 0.5-1 hour
- New page/section: 2-3 hours

**Simple API endpoint:** 1-2 hours
- GET endpoint (read-only): 1 hour
- POST endpoint (with validation): 2 hours
- Add to existing router: 1 hour

**Testing:** Add 25% to base estimate
- Manual testing: +0.5 hour
- Write unit tests: +1 hour

---

## Tier 2: Moderate Features (7-15 hours)

### Characteristics
- Multi-file changes
- New endpoint with business logic
- Integration work (2+ systems)
- Requires design decisions
- May span multiple components
- Needs checkpoints every 6 hours

### Examples from This Project

**Example 1: OAuth Phase 1 (Actual: 2.5 hours)**
```markdown
Feature: Implement FastAPI OAuth + JWT endpoints
Original estimate: 2 hours
Actual time: 2.5 hours (+25% drift)
Learning: Auth tasks consistently take longer
```

**Tasks:**
- Create FastAPI app structure (30 min)
- Add OAuth routes (30 min - longer: debugging redirect)
- Implement JWT utilities (30 min)
- Add authentication dependency (20 min)
- Test OAuth flow (30 min - longer: OIDC token issues)
- Create .env.example (10 min)

**Why longer than estimated:**
- OAuth redirect URI troubleshooting (15 min unexpected)
- OIDC token validation research (10 min unexpected)

**Calibrated estimate for similar tasks:** 2.5 hours (add 25% buffer for auth)

---

**Example 2: Streamlit OAuth Integration (Estimate: 4 hours)**
```markdown
Feature: Dual authentication (Streamlit + API)
Estimated: 4 hours (not yet completed)
```

**Phases:**
- Phase 1: Streamlit built-in OAuth (2 hours)
- Phase 2: Dual token support in API (2 hours)

**Calibrated estimate:** 4 hours (will update after completion)

---

**Example 3: ValidationEngine Migration (Actual: 10 hours)**
```markdown
Feature: Migrate from RuleEngine to ValidationEngine
Original estimate: 8 hours
Actual time: 10 hours (+25% drift)
```

**Tasks completed:**
- Update QueryValidator imports (1 hour)
- Fix partition filter false positives (2 hours - longer than expected)
- Update documentation (1 hour)
- Test edge cases (2 hours)
- Validate 70 production queries (2 hours)
- Create git commits (1 hour)
- Fix campaign_payout_rule special case (1 hour - unplanned)

**Why longer than estimated:**
- Partition detection required schema-based logic (1 hour unplanned)
- Edge case with non-partitioned tables (1 hour unplanned)

**Calibrated estimate for similar migrations:** 10 hours (add 25% buffer)

---

### Estimation Guidelines (Tier 2)

**Multi-file features:** 4-8 hours
- 2-3 files: 4 hours
- 4-6 files: 6 hours
- 7+ files: 8 hours (consider splitting)

**Integration work:** 4-6 hours
- Single service integration: 4 hours
- Multi-service: 6 hours
- With error handling + retry: +2 hours

**New subsystem:** 6-12 hours
- Simple subsystem (1 component): 6 hours
- Moderate (2-3 components): 8-10 hours
- Complex (4+ components): 12 hours (consider Tier 3)

**Architecture changes:** 8-12 hours
- Refactor major component: 8 hours
- Migrate between systems: 10 hours
- Database schema changes: 12 hours

**Checkpoints:** Add checkpoint tasks every 6 hours
- Checkpoint = drift check + deploy/test + review

---

## Tier 3: Complex Features (>15 hours)

### Rule: DO NOT PLAN AS SINGLE FEATURE

**Instead:**
1. **Break down** into Tier 1/2 features
2. **Identify MVP** (6-hour version)
3. **Create phases** (each ≤6 hours, independently shippable)
4. **Use `/start-feature`** which will auto-break down large ideas

### Example Breakdown

**Original idea:** "Complete audit logging system with dashboard" (25 hours)

**Broken down:**
- **Feature A:** Basic audit logging (SQLite + log function) - 6 hours ⭐ START HERE
- **Feature B:** Log dashboard (Streamlit table view) - 4 hours
- **Feature C:** Advanced dashboard (filters, search, export) - 6 hours
- **Feature D:** Alerts + retention policy - 5 hours
- **Feature E:** S3 backup integration - 4 hours

**Benefits:**
- Each shippable independently
- Can defer B-E if A solves problem
- Easier to estimate small pieces
- Less drift risk

---

## Calibration Log

**Purpose:** Track estimated vs actual to improve future estimates

**Update after:** Each feature completion (run `/check-drift`)

### 2025-11 Sprint

| Feature | Estimated | Actual | Drift | Category | Learning |
|---------|-----------|--------|-------|----------|----------|
| Schema cache (5 MTX tables) | 2h | 0.25h | -87% | Tier 1 | Caching: reduce to 1h default |
| OAuth credentials setup | 2h | 2h | 0% | Tier 1 | Auth setup: accurate |
| OAuth Phase 1 (FastAPI) | 2h | 2.5h | +25% | Tier 2 | Auth implementation: add 25% buffer |
| ValidationEngine migration | 8h | 10h | +25% | Tier 2 | Migrations: add 25% buffer |
| Query reorganization | TBD | TBD | TBD | Tier 2 | (In progress) |
| Streamlit OAuth integration | 4h | TBD | TBD | Tier 2 | (Planned) |

### Patterns Identified

**Authentication tasks:** +25% buffer needed
- Reason: OAuth flows have unexpected edge cases (redirect URIs, token formats)
- Recommendation: Multiply auth estimates by 1.25x

**Caching tasks:** -50% from initial intuition
- Reason: Caching mechanisms well-established in project
- Recommendation: Use 1 hour for simple caching tasks

**Migrations:** +25% buffer needed
- Reason: Edge cases discovered during testing
- Recommendation: Add "edge case buffer" task (+2 hours)

**First-time features:** +50% buffer
- Reason: Learning curve for new patterns
- Recommendation: Research task at beginning (1-2 hours)

---

## Estimation Process

### Step 1: Identify Feature Type

**Ask:**
- Single file or multiple?
- New concept or established pattern?
- Integration required?
- How many systems involved?

**Output:** Tier 1, 2, or 3 (if Tier 3, stop and break down)

---

### Step 2: Use Benchmarks

**Look for similar completed features:**
- Check Calibration Log for analogous tasks
- Apply identified patterns (+25% for auth, etc.)

**If no similar features:**
- Use guidelines (e.g., "multi-file feature: 4-8h")
- Add +50% buffer for first-time (learning curve)

---

### Step 3: Break Into Tasks

**For Tier 1:**
- List 3-8 concrete tasks
- Estimate each task (15 min to 2 hours)
- Sum total
- Add 25% for testing/debugging

**For Tier 2:**
- Group into 2-4 phases
- Each phase: 2-6 hours
- Add checkpoint tasks (every 6h)
- Ensure phases are independently shippable

---

### Step 4: Sanity Check

**Red flags:**
- Single task >4 hours → Break down further
- Feature >15 hours → Must split
- Estimate is "it depends" → Unknowns exist, research needed
- No testing time allocated → Add 25%

**Adjustments:**
- First time doing X: +50%
- Authentication involved: +25%
- Integration with external system: +2 hours for error handling
- Database changes: +2 hours for migration + rollback

---

### Step 5: Document Estimate

**In plan.md:**
```markdown
## Effort Estimation

**Total:** 6 hours (Tier 1)

**Breakdown:**
- Task 1.1: Configure OAuth (2h)
- Task 1.2: Add endpoint (2h)
- Task 1.3: Testing (1h)
- Task 1.4: Documentation (1h)

**Basis:**
- Similar to OAuth Phase 1 (actual: 2.5h)
- Used 1.25x multiplier for auth tasks
- Added 1h for testing (25% of base)

**Confidence:** Medium (first time with st.login, but well-documented)
```

---

## Tips for Accurate Estimation

### Do's ✅

✅ **Break down into concrete tasks** - "Add OAuth" → "Create credentials, configure, test"  
✅ **Use past actuals** - Check Calibration Log for similar features  
✅ **Add buffers** - Auth +25%, first-time +50%, testing +25%  
✅ **Include testing time** - Manual testing counts as work  
✅ **Document assumptions** - "Assumes API already deployed"  
✅ **Round up** - 3.7 hours → 4 hours (easier to track)

### Don'ts ❌

❌ **Don't estimate >15h as single feature** - Split first  
❌ **Don't forget testing** - Always add 25%  
❌ **Don't ignore learning curve** - First time? Add 50%  
❌ **Don't use "it depends"** - Research first, then estimate  
❌ **Don't overconfident** - Even "simple" tasks have surprises  
❌ **Don't copy estimates blindly** - Context matters (is infrastructure ready?)

---

## When Estimates Are Wrong

### Acceptable Drift

**±25% is normal** - Implementation always has surprises
- 6-hour estimate → 4.5-7.5 hours actual: ✅ Good
- 6-hour estimate → 8 hours actual: ⚠️ Update calibration
- 6-hour estimate → 12 hours actual: 🚫 Major drift, replan

### Learning from Drift

**If faster than estimated:**
- What shortcuts were available?
- Was infrastructure better than thought?
- Update calibration: reduce similar estimates

**If slower than estimated:**
- What was unexpected?
- Was research needed?
- Were edge cases discovered?
- Update calibration: add buffer for similar tasks

**Document in Calibration Log:**
```markdown
| Feature | Est | Actual | Drift | Learning |
|---------|-----|--------|-------|----------|
| OAuth Setup | 2h | 3h | +50% | Add 1h buffer for OAuth redirect debugging |
```

---

## Calibration Maintenance

### After Each Feature

1. Run `/check-drift` to capture actual time
2. Update Calibration Log (add row)
3. Note any patterns (auth took longer again?)

### Monthly Review

1. Analyze last 5-10 features
2. Calculate average drift by category
3. Update benchmarks if systematic bias found
4. Share learnings with team (if applicable)

### Quarterly Deep Dive

1. Review all features from quarter
2. Identify chronic overestimation/underestimation
3. Update estimation guidelines
4. Bump version number of this guide

---

## Integration with Commands

### `/start-feature`
- Uses Tier 1/2/3 definitions to determine complexity
- Auto-breaks down Tier 3 (>15h) into smaller features
- Adds checkpoints for Tier 2 (every 6 hours)

### `/check-drift`
- Compares plan estimate vs actual progress
- Prompts to update Calibration Log
- Suggests estimate adjustments for future

### `/validate-plan`
- Checks if estimate is realistic (uses benchmarks)
- Flags estimates >15h (must split)
- Warns if no testing time allocated

---

## Version History

**v1.0** (2025-11-15)
- Initial guide with Tier 1/2/3 definitions
- Calibration log initialized with 4 features
- Patterns identified: Auth +25%, Caching -50%
- Based on data-query-tool project

---

**Next Review:** 2026-05-16 (or after 10 features completed)

