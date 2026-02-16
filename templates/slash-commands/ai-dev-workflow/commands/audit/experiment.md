---
description: Domain-specific experiment integrity audit - bucketing, logging, attribution, sample ratio
allowed-tools: read_file, grep, codebase_search, run_terminal_cmd
argument-hint: [experiment-name] [--comprehensive]
---

## Command

**Domain-specific-Specific Lens**: Audit experiment implementation for integrity issues that could corrupt test results or bias outcomes.

**When to use:**
- New A/B test implementation
- Changes to bucketing logic
- Modifications to event logging
- Experiment framework updates
- Before launching to traffic

---

## Stop Rule

```
STOP AFTER:
- 3 Critical/High issues (experiment integrity)
- 5 Medium issues

Critical for experiments = Could invalidate results entirely
High = Could bias results
Medium = Could reduce confidence
```

---

## Severity for Experiment Issues

| Severity | Definition | Example |
|----------|------------|---------|
| 🚨 **Critical** | Experiment results invalid, cannot trust data | Exposure logged multiple times |
| ⚠️ **High** | Results biased, directionally incorrect conclusions | Sample ratio mismatch |
| 💡 **Medium** | Reduced statistical power, longer test needed | Missing segment logging |
| 📝 **Low** | Minor tracking gaps, doesn't affect conclusions | Missing debug metadata |

---

## Step 1: Identify Experiment Code

```bash
# Find experiment-related code
rg "(experiment|variant|bucket|treatment|control|ab_test|feature_flag)" --type py 2>/dev/null || true
rg "(exposure|conversion|impression|event_log)" --type py 2>/dev/null || true
```

---

## Step 2: Exposure Event Audit

### 2.1 Logging Exactly Once

**Critical Question**: Is the exposure event logged exactly once per user-experiment combination?

**Check for:**
- Multiple code paths that log exposure
- Exposure in loops without deduplication
- Race conditions in async exposure logging

```bash
# Find exposure logging calls
rg "log_exposure|track_exposure|record_exposure|exposure_event" --type py -C 3 2>/dev/null || true
```

**Anti-patterns:**
```python
# ❌ BAD: Exposure logged on every page view
def render_page():
    variant = get_variant(user_id, experiment_id)
    log_exposure(user_id, experiment_id, variant)  # Called every time!
    return render(variant)

# ✅ GOOD: Exposure logged once with deduplication
def render_page():
    variant = get_variant(user_id, experiment_id)
    log_exposure_once(user_id, experiment_id, variant)  # Checks if already logged
    return render(variant)
```

### 2.2 Exposure Timing

**Question**: Is exposure logged at the right moment?

- **Too early**: Logged before user actually sees variant (intent-to-treat issues)
- **Too late**: Logged after user interacts (selection bias)
- **Correct**: Logged when variant is rendered/applied

---

## Step 3: Conversion Event Audit

### 3.1 Attribution Correctness

**Question**: Are conversions correctly attributed to the right experiment variant?

**Check for:**
- Conversion logged without checking exposure
- Attribution to wrong experiment
- Cross-session attribution issues

```bash
# Find conversion logging
rg "log_conversion|track_conversion|conversion_event" --type py -C 3 2>/dev/null || true
```

### 3.2 Conversion Window

**Question**: Is the conversion window handled correctly?

- Time-bound conversions (7-day window, 30-day window)
- Session vs user-level attribution
- Multi-touch vs last-touch attribution

---

## Step 4: Sample Ratio Mismatch (SRM) Risk

### 4.1 Bucketing Consistency

**Critical Question**: Is the same user always assigned to the same variant?

**Check for:**
- Bucketing based on volatile IDs (session ID, request ID)
- Bucketing that changes on code deploy
- Bucketing affected by user state changes

```bash
# Find bucketing logic
rg "(hash|bucket|variant|get_experiment_group)" --type py -C 5 2>/dev/null || true
```

**Anti-patterns:**
```python
# ❌ BAD: Bucketing on session (user sees different variant each session)
def get_variant(session_id, experiment_id):
    return hash(session_id + experiment_id) % 2

# ✅ GOOD: Bucketing on stable user ID
def get_variant(user_id, experiment_id):
    return hash(user_id + experiment_id) % 2
```

### 4.2 Traffic Allocation

**Question**: Is traffic split correctly?

- 50/50 split actually 50/50?
- Ramp-up logic correct (10% → 50% → 100%)
- Holdout groups respected

### 4.3 Segment Leakage

**Question**: Could users move between segments during the test?

- Geo-based bucketing with VPN users
- Device-based bucketing with multi-device users
- New users vs returning users overlap

---

## Step 5: Bias Detection

### 5.1 Selection Bias

**Question**: Does this change bias WHO gets exposed?

- Different error rates per variant
- Performance differences affecting page load
- Feature availability differences

### 5.2 Novelty/Primacy Effects

**Question**: Are there confounds from test timing?

- Novelty effect (new = exciting, but temporary)
- Learning curve effects
- Day-of-week effects

### 5.3 Interaction Effects

**Question**: Does this experiment interact with other experiments?

- Multiple experiments on same page
- Shared user populations
- Conflicting treatments

---

## Step 6: Generate Report

```
🧪 EXPERIMENT INTEGRITY AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 EXPERIMENT: [name]
├─ Variants: [control, treatment_a, treatment_b]
├─ Traffic Split: [50/50 or other]
├─ Bucketing Key: [user_id, session_id, etc.]
└─ Conversion Goal: [primary metric]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 CRITICAL ISSUES (Could Invalidate Results)

1. [Issue]
   ├─ Location: `file:line`
   ├─ Problem: [What's wrong]
   ├─ Impact: [How it corrupts results]
   └─ Fix: [Specific remediation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ HIGH (Could Bias Results)

1. [Issue]
   ├─ Location: `file:line`
   ├─ Bias Type: [Selection / SRM / Attribution]
   └─ Fix: [Remediation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ INTEGRITY CHECKLIST

Exposure Events:
- [ ] Logged exactly once per user-experiment
- [ ] Logged at correct timing (render, not intent)
- [ ] Deduplication mechanism in place

Conversion Events:
- [ ] Correctly attributed to variant
- [ ] Conversion window respected
- [ ] Only logged for exposed users

Bucketing:
- [ ] Deterministic (same input = same output)
- [ ] Based on stable ID (user_id, not session_id)
- [ ] Traffic split matches intended allocation

Bias:
- [ ] No selection bias in exposure
- [ ] No interaction with other experiments
- [ ] Holdout groups respected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 RECOMMENDATION

[SAFE TO LAUNCH / FIX BEFORE LAUNCH / NEEDS INVESTIGATION]

[Summary and next steps]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Comprehensive Mode (`--comprehensive`)

If `--comprehensive` flag, also check:

1. **Pre-experiment validation**: Is there a pre-analysis plan?
2. **Power analysis**: Is sample size sufficient?
3. **Stopping rules**: Are early stopping criteria defined?
4. **Segmentation**: Are all relevant segments being tracked?

---

## Integration

**Works with:**
- `/audit-feature` - This is the experiment lens (Domain-specific-specific)
- `experimentation-toolkit` - Analysis framework
- A/B test documentation templates

**References:**
- Experiment integrity best practices
- Sample ratio mismatch detection
- Exposure logging standards
