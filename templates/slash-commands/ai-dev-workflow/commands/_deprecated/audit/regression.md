---
description: Regression surface analysis - what else could break from this change
allowed-tools: read_file, grep, codebase_search, run_terminal_cmd, list_dir
argument-hint: [file-or-feature] [--blast-radius]
---

## Command

Analyze the regression surface of a change. Identify what else could break, backwards compatibility concerns, and detection mechanisms.

**When to use:**
- Refactoring shared code/utilities
- Changing function signatures
- Database schema changes
- API contract modifications
- Touching high-traffic code paths

---

## Stop Rule

```
STOP AFTER:
- 5 potential regression scenarios
- For each scenario, provide ONE detection mechanism

Do NOT enumerate every possible failure.
Focus on MOST LIKELY causal mechanisms.
```

---

## Step 1: Identify Change Scope

### 1.1 Files Changed

```bash
# What files were modified?
git diff --name-only HEAD~1..HEAD 2>/dev/null || git diff --name-only 2>/dev/null || true

# What functions/classes were touched?
git diff HEAD~1..HEAD 2>/dev/null | grep "^@@" || true
```

### 1.2 Dependency Analysis

For each modified file, find what depends on it:

```bash
# Find imports of changed file (Python)
CHANGED_FILES=$(git diff --name-only HEAD~1..HEAD 2>/dev/null | grep "\.py$" | sed 's/\.py$//' | sed 's/\//./g')
for module in $CHANGED_FILES; do
  echo "=== Dependents of $module ==="
  rg "from $module import|import $module" --type py 2>/dev/null || true
done

# Find imports (JavaScript/TypeScript)
rg "from ['\"].*$(git diff --name-only HEAD~1..HEAD | head -1 | sed 's/\.[jt]sx\?$//')" 2>/dev/null || true
```

---

## Step 2: Blast Radius Assessment

### 2.1 Direct Impacts

**Question**: What code directly calls the modified code?

- List all callers
- Identify changed interfaces (parameters, return types)
- Check for implicit contracts (expected side effects)

### 2.2 Indirect Impacts

**Question**: What could break downstream?

- Database queries depending on changed schema
- Caches depending on changed data format
- External services depending on changed API
- Background jobs depending on changed state

### 2.3 Cross-Cutting Concerns

**Question**: Does this affect shared infrastructure?

- Logging (format changes)
- Metrics (label changes)
- Error handling (exception types)
- Configuration (new/removed settings)

---

## Step 3: Backwards Compatibility Check

### 3.1 API Contract Changes

Check if any of these changed:
- Function signatures (added/removed parameters)
- Return types or shapes
- Exception/error types
- Side effects

```bash
# Find signature changes
git diff HEAD~1..HEAD 2>/dev/null | grep -E "^[-+].*(def |async def |function |const.*=.*=>)" || true
```

### 3.2 Data Contract Changes

Check if any of these changed:
- Database column types/names
- JSON payload shapes
- Event schemas
- Configuration keys

### 3.3 Behavioral Changes

Check if any of these changed:
- Default values
- Validation rules
- Error messages
- Timing behavior

---

## Step 4: Regression Scenarios

**Frame as**: "Assume this ships and conversion drops 5%. What went wrong?"

For each scenario:

1. **Mechanism**: What specifically fails?
2. **Trigger**: What conditions cause it?
3. **Impact**: What's the user/business effect?
4. **Detection**: How would we know?
5. **Mitigation**: Feature flag, rollback, fix?

**Format:**
```
🎯 REGRESSION SCENARIO 1: Stale cache after schema change

├─ Mechanism: Cache TTL (3h) means old format served after deploy
├─ Trigger: Any request within 3h of deploy using cached data
├─ Impact: TypeError when parsing old format, lead routing fails
├─ Detection:
│   - Error rate spike in routing service
│   - Monitor: error_count{service="router", type="TypeError"}
└─ Mitigation:
   - Deploy with cache invalidation
   - Or: Feature flag to handle both formats
```

---

## Step 5: Feature Flag Coverage

**Question**: Is this change behind a feature flag?

If yes:
- Flag name and default state
- Rollout plan (% users)
- Rollback procedure

If no:
- Should it be? (Consider risk level)
- What's the rollback plan?

---

## Step 6: Generate Report

```
📊 REGRESSION ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 BLAST RADIUS

Files Changed: [N]
Direct Dependents: [N] files
Indirect Impact: [Scope description]

Changed Interfaces:
├─ `function_name(old_sig)` → `function_name(new_sig)`
└─ `ReturnType` changed from X to Y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ REGRESSION SCENARIOS (Top 5)

1. [Scenario Name]
   ├─ Mechanism: [What breaks]
   ├─ Trigger: [When it happens]
   ├─ Impact: [Business effect]
   ├─ Detection: [Metric/log to watch]
   └─ Mitigation: [Rollback/fix plan]

2. [Scenario Name]
   ├─ ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 BACKWARDS COMPATIBILITY

| Change | Compatible? | Migration |
|--------|-------------|-----------|
| API signature | ⚠️ No | Add default param |
| Data format | ✅ Yes | N/A |
| Behavior | ⚠️ No | Feature flag |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚩 FEATURE FLAG STATUS

Flag: `enable_new_routing_logic`
Default: OFF
Rollout: 10% → 50% → 100% over 3 days
Rollback: Toggle flag OFF, no deploy needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 MONITORING CHECKLIST

Before deploy:
- [ ] Baseline metrics captured
- [ ] Alert thresholds set

After deploy:
- [ ] Error rate: [metric name]
- [ ] Latency: [metric name]
- [ ] Business KPI: [metric name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Blast Radius Mode (`--blast-radius`)

If `--blast-radius` flag, focus only on dependency analysis:

1. Map all files that import changed code
2. Generate dependency graph
3. Highlight high-risk dependents (high traffic, critical path)

---

## Integration

**Works with:**
- `/audit-feature` - This is the regression lens
- `/check-drift` - Verify changes match original plan
- `/feature-complete` - Verify rollout plan before marking done

**Pairs well with:**
- Feature flag infrastructure
- Canary deployment systems
- Metric dashboards
