---
description: EPCVIP data contract and compliance audit - payload drift, PII handling, fallback behavior
allowed-tools: read_file, grep, codebase_search, run_terminal_cmd
argument-hint: [service-or-file] [--pii-focus] [--api-changes]
---

## Command

**EPCVIP-Specific Lens**: Audit data contracts, compliance requirements, and PII handling to prevent silent data drift and compliance violations.

**When to use:**
- API contract changes (new endpoints, modified schemas)
- Database schema modifications
- New data fields being captured
- Integration with external services
- Anything touching PII (personally identifiable information)

---

## Stop Rule

```
STOP AFTER:
- 3 Critical/High issues (compliance or data integrity)
- 5 Medium issues

Critical for data = PII leak, compliance violation, data corruption
High = Contract break, silent failure masking
Medium = Schema drift, missing documentation
```

---

## Severity for Data Contract Issues

| Severity | Definition | Example |
|----------|------------|---------|
| 🚨 **Critical** | PII leak, compliance violation, data loss | SSN logged without redaction |
| ⚠️ **High** | Breaking API change, silent upstream failure masked | Field removed without deprecation |
| 💡 **Medium** | Schema drift, documentation mismatch | New field undocumented |
| 📝 **Low** | Minor inconsistency, style issue | Field naming convention |

---

## Step 1: Identify Data Flow

### 1.1 Find Data Models

```bash
# Python models (Pydantic, dataclasses, SQLAlchemy)
rg "class.*\(BaseModel\)|@dataclass|class.*\(Base\)" --type py 2>/dev/null || true

# TypeScript interfaces/types
rg "interface |type .*=" --type ts 2>/dev/null || true

# Database schemas
rg "CREATE TABLE|ALTER TABLE" --glob "*.sql" 2>/dev/null || true
```

### 1.2 Map Data Paths

Trace data from entry to storage:
1. **Ingress**: API endpoints, form submissions, webhooks
2. **Transform**: Validation, enrichment, normalization
3. **Storage**: Database, cache, external services
4. **Egress**: API responses, exports, logs

---

## Step 2: Payload Shape Audit

### 2.1 Schema Changes

**Question**: Are we changing payload shape or semantics?

**Check for:**
- Added fields (backward compatible?)
- Removed fields (breaking change!)
- Type changes (int → string)
- Semantic changes (field means different thing)

```bash
# Find recent model/schema changes
git diff HEAD~1..HEAD --name-only | xargs -I {} sh -c 'echo "=== {} ===" && git diff HEAD~1..HEAD -- "{}" | grep -E "^\+.*:|^\-.*:"' 2>/dev/null || true
```

### 2.2 Default Values

**Question**: Are default values appropriate?

**Check for:**
- Missing defaults on new optional fields
- Defaults that mask upstream failures
- Defaults that could cause data quality issues

**Anti-patterns:**
```python
# ❌ BAD: Default masks upstream failure
def get_affiliate(lead) -> str:
    return lead.get("affiliate_id", "unknown")  # Silent failure!

# ✅ GOOD: Explicit handling
def get_affiliate(lead) -> Optional[str]:
    affiliate_id = lead.get("affiliate_id")
    if not affiliate_id:
        logger.warning("⚠️ Missing affiliate_id", extra={"lead_id": lead["id"]})
    return affiliate_id
```

### 2.3 Validation Changes

**Question**: Are validation rules changing?

- Relaxed validation (allows more) - Generally safe
- Stricter validation (allows less) - Could reject valid data
- Different validation (changed rules) - Semantic change

---

## Step 3: PII Handling Audit

### 3.1 PII Field Identification

**Question**: What PII exists in this change?

Common PII fields:
- Email, phone, SSN, DOB
- IP address, device ID
- Name, address, financial data
- Any user-linkable identifier

```bash
# Find PII-related fields
rg "(email|phone|ssn|dob|address|credit_card|social_security|ip_address)" --type py 2>/dev/null || true
rg "(first_name|last_name|full_name|street|city|zip|postal)" --type py 2>/dev/null || true
```

### 3.2 PII Protection

**For each PII field, verify:**

1. **Storage**: Is it encrypted at rest?
2. **Transit**: Is it encrypted in transit (HTTPS)?
3. **Logging**: Is it redacted in logs?
4. **Access**: Is access properly restricted?
5. **Retention**: Is there a retention policy?

```bash
# Check for PII in logging
rg "logger\.(info|debug|error|warning).*email|ssn|phone" --type py 2>/dev/null || true
```

### 3.3 Consent Propagation

**Question**: Are consent fields being propagated correctly?

- TCPA consent for phone
- Email opt-in/opt-out
- SMS consent
- Marketing consent

---

## Step 4: Fallback Behavior Audit

### 4.1 Error Handling

**Question**: Could fallback/default behavior mask upstream failures?

**Check for:**
- Silently returning empty data on error
- Using stale cache without indication
- Defaulting to "safe" values without logging

**Anti-patterns:**
```python
# ❌ BAD: Silent fallback masks failure
try:
    data = fetch_from_api()
except Exception:
    data = {}  # No one knows the API is failing!

# ✅ GOOD: Explicit fallback with visibility
try:
    data = fetch_from_api()
except Exception as e:
    logger.error(f"❌ API failure, using fallback: {e}")
    metrics.increment("api_fallback_used")
    data = get_cached_fallback()
```

### 4.2 Degradation Visibility

**Question**: When degraded, is it visible?

- Metrics for fallback usage
- Alerts for high fallback rates
- Customer-visible indicators (if appropriate)

---

## Step 5: API Contract Audit

### 5.1 Breaking Changes

**Question**: Is this a breaking change for consumers?

Breaking changes (require coordination):
- Removing fields from response
- Changing field types
- Changing error formats
- Removing endpoints

Non-breaking changes (generally safe):
- Adding optional fields
- Adding new endpoints
- Expanding enum values (carefully)

### 5.2 Versioning

**Question**: Is versioning handled correctly?

- API version in URL or header
- Deprecation notices for old versions
- Migration path documented

### 5.3 Documentation

**Question**: Is the contract documented?

- OpenAPI/Swagger spec updated
- README reflects changes
- Changelog entry added

---

## Step 6: Generate Report

```
📋 DATA CONTRACT AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 DATA FLOW
├─ Ingress: [API endpoints, sources]
├─ Transform: [Validation, enrichment]
├─ Storage: [Database, cache]
└─ Egress: [API responses, exports]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 CRITICAL ISSUES

1. [Issue]
   ├─ Location: `file:line`
   ├─ Type: [PII Leak / Compliance / Data Loss]
   ├─ Impact: [What could go wrong]
   └─ Fix: [Specific remediation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ HIGH (Contract/Integrity Issues)

1. [Issue]
   ├─ Location: `file:line`
   ├─ Type: [Breaking Change / Silent Failure]
   └─ Fix: [Remediation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SCHEMA CHANGES

| Field | Before | After | Breaking? |
|-------|--------|-------|-----------|
| `user.email` | required | optional | ⚠️ Yes |
| `user.phone` | - | new field | ✅ No |
| `order.status` | string | enum | ⚠️ Possible |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔒 PII HANDLING CHECKLIST

| PII Field | Encrypted | Logged? | Redacted? | Retention |
|-----------|-----------|---------|-----------|-----------|
| email | ✅ | ✅ Logged | ✅ Masked | 2 years |
| phone | ✅ | ⚠️ Logged | ❌ NOT masked | - |
| ssn | ✅ | ❌ Not logged | N/A | 7 years |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 FALLBACK BEHAVIOR

| Scenario | Fallback | Visibility | Risk |
|----------|----------|------------|------|
| API timeout | Empty list | ❌ No metrics | ⚠️ High |
| Cache miss | DB query | ✅ Logged | Low |
| Validation fail | Reject | ✅ Error response | Low |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ COMPLIANCE CHECKLIST

- [ ] No PII in logs without redaction
- [ ] Consent fields propagated correctly
- [ ] Retention policies documented
- [ ] Access controls in place
- [ ] Encryption at rest and in transit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 RECOMMENDATION

[COMPLIANT / NEEDS FIXES / REQUIRES REVIEW]

[Summary and next steps]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## PII Focus Mode (`--pii-focus`)

If `--pii-focus` flag, deep-dive on PII only:

1. Complete PII inventory
2. Data flow diagram for each PII field
3. Compliance checklist (GDPR, CCPA, etc.)
4. Redaction verification in all log paths

---

## API Changes Mode (`--api-changes`)

If `--api-changes` flag, focus on contract:

1. Before/after schema comparison
2. Breaking change analysis
3. Consumer impact assessment
4. Migration guide draft

---

## Integration

**Works with:**
- `/audit-feature` - This is the data-contract lens (EPCVIP-specific)
- Schema validation tools
- API documentation generators

**References:**
- Data classification policies
- PII handling guidelines
- API versioning standards
