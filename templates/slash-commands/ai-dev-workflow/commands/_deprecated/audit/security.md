---
description: Security audit - threat modeling, abuse cases, and vulnerability detection
allowed-tools: read_file, grep, codebase_search, run_terminal_cmd
argument-hint: [file-or-feature] [--owasp] [--quick]
---

## Command

Threat model this change and identify security vulnerabilities. Focus on plausible attack paths, not theoretical concerns.

**When to use:**
- Authentication/authorization changes
- Payment or financial code
- PII handling
- External API integrations
- Any user input processing

---

## Stop Rule

```
STOP AFTER:
- 3 Critical/High severity issues
- 5 Medium severity issues (combined)

For security issues:
- Only flag issues with a PLAUSIBLE ATTACKER PATH
- No hypotheticals without concrete exploitation scenario
- If multiple instances of same vulnerability, report ONE with count
```

---

## Severity for Security Issues

| Severity | Definition | Example |
|----------|------------|---------|
| 🚨 **Critical** | Exploitable remotely, no auth required, high impact | SQL injection in public endpoint |
| ⚠️ **High** | Exploitable with low-privilege access, significant impact | Auth bypass, privilege escalation |
| 💡 **Medium** | Requires specific conditions, moderate impact | CSRF, information disclosure |
| 📝 **Low** | Defense in depth, unlikely exploitation | Missing security header |

---

## Step 1: Identify Attack Surface

### 1.1 Entry Points

Find all places where external data enters the system:

```bash
# HTTP endpoints
rg "(@app\.(get|post|put|delete|patch)|@router\.(get|post|put|delete|patch))" --type py 2>/dev/null || true

# Form inputs
rg "request\.(form|args|json|data|files)" --type py 2>/dev/null || true

# URL parameters
rg "request\.args\.get|request\.query" 2>/dev/null || true
```

### 1.2 Trust Boundaries

Map where trusted meets untrusted:
- User input → Application logic
- Application → Database
- Application → External APIs
- Internal service → Internal service (authz)

---

## Step 2: Vulnerability Scan

### 2.1 Injection Attacks

**SQL Injection:**
```bash
# String interpolation in SQL
rg "execute.*f\"" --type py 2>/dev/null || true
rg "execute.*\+" --type py 2>/dev/null || true
rg "execute.*format\(" --type py 2>/dev/null || true
rg "\.query\(.*\+|\.query\(.*\$\{" 2>/dev/null || true
```

**Command Injection:**
```bash
# Shell execution with user input
rg "(subprocess|os\.system|os\.popen|eval|exec)\(" --type py 2>/dev/null || true
```

**XSS:**
```bash
# Unescaped output
rg "innerHTML|dangerouslySetInnerHTML|v-html" 2>/dev/null || true
rg "\|safe" --glob "*.html" 2>/dev/null || true
```

### 2.2 Authentication & Authorization

**Check for:**
- Missing auth decorators on sensitive endpoints
- Broken access control (IDOR)
- Session fixation
- Weak password requirements
- Token exposure in logs/URLs

```bash
# Endpoints without auth decorator
rg "@app\.(get|post)" --type py -A 3 2>/dev/null | grep -v "require_auth\|login_required\|Depends" || true

# Hardcoded credentials
rg "(password|secret|api_key|token)\s*=\s*['\"]" --type py 2>/dev/null || true
```

### 2.3 Data Exposure

**Check for:**
- PII in logs
- Secrets in code
- Error messages with stack traces
- Sensitive data in URLs

```bash
# Logging sensitive data
rg "logger\.(info|debug|error).*password|email|ssn|credit" --type py 2>/dev/null || true

# Secrets patterns
rg "(aws_secret|api_key|private_key|password)\s*=\s*['\"][^'\"]+['\"]" 2>/dev/null || true
```

### 2.4 Input Validation

**Check for:**
- Missing validation on user input
- Type confusion
- Buffer overflows (if applicable)
- Path traversal

```bash
# File operations with user input
rg "open\(.*request\.|read\(.*request\." --type py 2>/dev/null || true
rg "os\.path\.join.*request" --type py 2>/dev/null || true
```

---

## Step 3: Threat Model

For each entry point identified, answer:

1. **What can an attacker control?**
   - Input values
   - Request headers
   - File uploads
   - Timing

2. **What's the worst outcome?**
   - Data theft
   - Privilege escalation
   - Service disruption
   - Financial loss

3. **What's the attack path?**
   - Step-by-step exploitation
   - Required preconditions
   - Detection/logging gaps

**Format:**
```
🎯 THREAT MODEL

Entry Point: POST /api/users/update
├─ Attacker Controls: request.json["role"], request.json["permissions"]
├─ Worst Outcome: Privilege escalation to admin
├─ Attack Path:
│   1. Attacker creates normal user account
│   2. Sends POST with {"role": "admin"} in body
│   3. Backend doesn't validate role field
│   4. User gains admin privileges
└─ Severity: 🚨 CRITICAL
```

---

## Step 4: Generate Report

```
🔒 SECURITY AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 ATTACK SURFACE
├─ Entry Points: [N] endpoints analyzed
├─ Trust Boundaries: [list]
└─ User Input Paths: [list]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 CRITICAL VULNERABILITIES

1. [Vulnerability Name]
   ├─ Location: `file:line`
   ├─ Type: [SQL Injection / XSS / Auth Bypass / etc.]
   ├─ Attack Path: [Step-by-step]
   ├─ Impact: [What attacker gains]
   └─ Fix: [Specific remediation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ HIGH SEVERITY

1. [Vulnerability]
   ├─ Location: `file:line`
   ├─ Type: [Category]
   └─ Fix: [Remediation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 MEDIUM SEVERITY

1. [Issue] - `file:line` - [Fix]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NOT VULNERABLE (verified)

- [x] No SQL injection in database queries
- [x] Authentication required on all sensitive endpoints
- [x] No hardcoded secrets found
- [x] Input validation present on user inputs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## OWASP Quick Reference

If `--owasp` flag provided, check against OWASP Top 10 (2021):

1. **A01:2021 - Broken Access Control**
2. **A02:2021 - Cryptographic Failures**
3. **A03:2021 - Injection**
4. **A04:2021 - Insecure Design**
5. **A05:2021 - Security Misconfiguration**
6. **A06:2021 - Vulnerable Components**
7. **A07:2021 - Auth Failures**
8. **A08:2021 - Data Integrity Failures**
9. **A09:2021 - Logging Failures**
10. **A10:2021 - SSRF**

---

## Quick Mode (`--quick`)

If `--quick` flag, run only automated checks:

```bash
# Run all grep patterns
# Skip manual threat modeling
# Report findings without deep analysis
```

---

## Integration

**Works with:**
- `/audit-feature` - This is the security lens
- CI: `security-review.yml` - Automated PR security scanning
- Pre-commit hooks for blocking critical issues

**References:**
- OWASP Top 10: https://owasp.org/Top10/
- ANTI_SLOP_STANDARDS.md - SQL parameterization rules
