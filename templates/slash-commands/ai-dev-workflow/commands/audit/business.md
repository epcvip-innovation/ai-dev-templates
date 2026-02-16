---
description: Business logic walkthrough - invariants, edge cases, and intent verification
allowed-tools: read_file, codebase_search, grep, run_terminal_cmd
argument-hint: [file-or-feature] [--context spec.md]
---

## Command

Deep-dive business logic review. Walk through the code like you're debugging a production incident.

**When to use:**
- Complex feature logic with multiple branches
- Business rules that affect monetization/routing
- After changes to core domain logic
- When something "feels off" but you can't pinpoint why

---

## Stop Rule

```
STOP AFTER:
- 3 High severity issues
- 5 Medium severity issues (combined with High)

If more issues found:
- Group into THEMES
- Pick highest-leverage representative per theme
- Do NOT enumerate every instance
```

---

## Step 1: Load Context

### 1.1 Read the Diff/Code

```bash
# Get recent changes
git diff HEAD~1..HEAD 2>/dev/null || git diff 2>/dev/null || true

# Or read specific files if provided
```

### 1.2 Load Acceptance Criteria (if available)

If `--context` flag provided, read the spec/requirements document.

Otherwise, ask:
```
📋 CONTEXT NEEDED

What should this code accomplish? Provide either:
- Link to ticket/spec
- Brief description of expected behavior
- Or I'll infer from the code (less accurate)
```

---

## Step 2: Identify Invariants

**"What assumptions does this code make that MUST be true?"**

For each function/module, identify:

1. **Input invariants** - What must be true about inputs?
   - Types, ranges, null handling
   - Required fields, optional fields
   - Format expectations (dates, IDs, enums)

2. **State invariants** - What must be true about system state?
   - Database records exist
   - External services available
   - Cache state consistent

3. **Output invariants** - What must be true about results?
   - Return type guarantees
   - Side effect guarantees
   - Error handling guarantees

**Format:**
```
📐 INVARIANTS IDENTIFIED

Function: `process_lead(lead_data)`

INPUT:
- lead_data.email must be valid email format
- lead_data.state must be 2-letter code
- lead_data.requested_amount must be > 0

STATE:
- Database connection must be active
- Affiliate lookup cache must be populated

OUTPUT:
- Returns Lead object or None (never raises)
- If successful, lead_id is guaranteed unique
- Side effect: always logs to analytics
```

---

## Step 3: Edge Case Analysis

**"What inputs would cause wrong lead routing or wrong monetization outcome?"**

Analyze systematically:

### 3.1 Boundary Conditions
- Empty collections ([], {}, "")
- Zero values
- Maximum/minimum values
- Off-by-one errors

### 3.2 Invalid State Transitions
- Operations in wrong order
- Concurrent modifications
- Partial failures mid-transaction

### 3.3 External Dependencies
- API timeouts
- Network failures
- Stale cache data
- Rate limiting

### 3.4 Business Logic Gaps
- Unhandled enum values
- Missing validation
- Implicit defaults that may change
- Time zone issues
- Currency/locale handling

**Output top 5 edge cases tied to concrete paths in the diff:**

```
🎯 EDGE CASES (Business Impact)

1. **Empty affiliate list handling**
   - Path: `router.py:45` → `get_affiliate_bids()` returns []
   - Impact: Lead falls through to default routing (low revenue)
   - Severity: ⚠️ HIGH
   - Fix: Add explicit fallback affiliate or queue for manual review

2. **Stale cache on affiliate disable**
   - Path: `cache.py:120` → Cache TTL is 3 hours
   - Impact: Leads routed to disabled affiliate for up to 3 hours
   - Severity: ⚠️ HIGH
   - Fix: Add cache invalidation on affiliate status change

3. ...
```

---

## Step 4: Intent Verification

**"Does the code do what it claims to do?"**

For each significant function:

1. **Read the docstring/comment** (what it claims)
2. **Trace the implementation** (what it does)
3. **Identify gaps** between claim and reality

**Common mismatches:**
- Docstring says "validates input" but validation is incomplete
- Comment says "handles error" but only handles one error type
- Function name implies idempotent but has side effects
- Return type says Optional but can actually return multiple error states

---

## Step 5: Generate Report

```
🔍 BUSINESS LOGIC AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📐 INVARIANTS
[List key invariants this code depends on]

🎯 EDGE CASES (by severity)

⚠️ HIGH
1. [Edge case] - `file:line`
   └─ Impact: [Business outcome]
   └─ Fix: [Specific remediation]

💡 MEDIUM
1. [Edge case] - `file:line`
   └─ Impact: [Business outcome]
   └─ Fix: [Specific remediation]

📋 THEMES
[If >5 similar issues, group into patterns]

🔄 INTENT MISMATCHES
[Where code doesn't match its claims]

✅ VERIFIED CORRECT
[What looks good and why]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Prompting Technique

Use this exact prompt internally when analyzing:

```
Walk through this diff like you're debugging a prod incident where 
conversion dropped 10%.

1. List every invariant this code assumes
2. For each invariant, identify what happens if it's violated
3. Find the top 5 edge cases that would cause:
   - Wrong lead routing
   - Wrong monetization outcome
   - Silent data corruption
4. Only include issues you can tie to a concrete path in the diff
5. Stop after 3 High + 5 Medium issues
```

---

## Integration

**Works with:**
- `/audit-feature` - This is the business logic lens
- `/debug-failure` - Use findings to form hypotheses
- `/check-drift` - Compare against original spec

**References:**
- Project-specific business rules in `CLAUDE.md`
- Domain-specific patterns in `CODING_STANDARDS.md`
