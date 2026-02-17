---
description: Unified feature audit with bounded multi-lens review and severity scoring
allowed-tools: read_file, run_terminal_cmd, grep, codebase_search, list_dir
argument-hint: [feature-name] [--deep] [--lens security|business|regression|experiment|data-contract]
---

## Command

Audit a recently completed feature against project standards, coding patterns, and business requirements. Uses a layered review funnel with bounded severity to prevent infinite review loops.

**Modes:**
- **Quick mode** (default): Single-pass review with all core lenses
- **Deep mode** (`--deep`): Multi-pass with fresh session prompt
- **Single lens** (`--lens <name>`): Focus on one specific area

---

## Step 1: Load Context

### 1.1 Load Project Standards

Read project-specific standards (if they exist):
```bash
# Find and read standards documents
cat CLAUDE.md 2>/dev/null || true
cat CODING_STANDARDS.md 2>/dev/null || true
cat .claude/CLAUDE.md 2>/dev/null || true
```

### 1.2 Identify Changes to Audit

```bash
echo "=== Git Status ==="
git status --porcelain || true

echo ""
echo "=== Recent Changes (last 5 commits) ==="
git log --oneline -5 || true

echo ""
echo "=== Diff Summary ==="
git diff --stat HEAD~1..HEAD 2>/dev/null || git diff --stat 2>/dev/null || true
```

If user specified files or a feature name, focus on those. Otherwise, audit the most recent diff.

---

## Step 2: Run Review Lenses

Apply each lens in sequence. **CRITICAL: Stop at severity limits.**

### Stop Rule (Apply to ALL Lenses)

```
STOP CONDITION: 
- Maximum 3 Critical/High issues per lens
- Maximum 5 Medium issues per lens (combined with High)
- If more issues found: Group into THEMES, report highest-leverage representative
- DO NOT enumerate every instance of the same pattern
```

### Severity Definitions

| Severity | Definition | Action |
|----------|------------|--------|
| 🚨 **Critical** | Data loss, security breach, compliance violation, prod crash | Must fix before merge |
| ⚠️ **High** | Feature broken, blocking workflow, wrong business outcome | Should fix |
| 💡 **Medium** | Partial breakage, workaround exists, edge case missed | Consider fixing |
| 📝 **Low** | Cosmetic, minor inconvenience, style preference | Nice to have |

---

### Lens 1: Anti-Slop & Code Quality

**Reference**: ANTI_SLOP_STANDARDS.md patterns

**Check for:**
- Functions >50 lines (should be split)
- Nesting depth >3 levels (use early returns)
- Kitchen-sink parameters (too many args)
- Over-abstraction (unnecessary wrappers)
- Blind exception handling (empty catches)
- Premature optimization
- Copy-paste code (same logic 3+ times)
- Comment novels (explaining obvious code)

**Automated checks:**
```bash
# Empty exception handlers
rg "except.*:\s*pass" --type py 2>/dev/null || true
rg "catch.*\{\s*\}" --type js 2>/dev/null || true

# Console/print statements
rg "console\.log" --type js --glob "!**/*.test.js" 2>/dev/null || true
rg "print\(" --type py --glob "!**/tests/**" 2>/dev/null || true

# SQL injection risk
rg 'execute.*f"' --type py 2>/dev/null || true
rg "execute.*\+" --type py 2>/dev/null || true
```

---

### Lens 2: Security & Abuse Cases

**Threat model this change:**
- Entry points - What new inputs does this accept?
- Trust boundaries - Where does trusted meet untrusted?
- Abuse cases - How could this be misused?

**Check for:**
- SQL injection (string concatenation in queries)
- Hardcoded secrets or credentials
- Missing input validation
- Authentication/authorization gaps
- Unsafe deserialization
- Path traversal risks
- CORS/CSRF vulnerabilities

**Only flag issues with a plausible attacker path** - no hypotheticals.

---

### Lens 3: Business Logic Walkthrough

**"Walk through the diff like you're debugging a prod incident."**

1. **List invariants** this code assumes
2. **Identify edge cases** that would cause:
   - Wrong lead routing
   - Wrong monetization outcome
   - Silent data corruption
   - Incorrect user experience

3. **Only include issues tied to a concrete path in the diff**

---

### Lens 4: Regression Surface

**"Assume this ships and conversion drops 5%."**

**Analyze:**
- What else could break from this change?
- Backwards compatibility concerns?
- Feature flag coverage?
- Shared code/utilities affected?
- Database migration risks?
- API contract changes?

**Output**: Top 5 most likely causal mechanisms and how to detect each.

---

### Lens 5: Documentation & Types

**Check:**
- New public APIs have documentation
- Complex logic has explanatory comments (WHY not WHAT)
- Type annotations present (Python/TypeScript)
- No `any` type abuse (TypeScript)
- Missing error messages for user-facing failures

---

## Step 3: Domain-Specific Lenses (If Applicable)

**Only run if `--data-contracts` flag or project has experiment/data-contract code.**

### Lens 6: Experiment Integrity

**See**: `/audit:experiment` for full command

**Quick check:**
- Exposure events logged exactly once?
- Conversion events properly attributed?
- Sample ratio mismatch risk?
- Bucketing deterministic and reproducible?
- Holdout groups respected?

### Lens 7: Data Contract & Compliance

**See**: `/audit:data-contract` for full command

**Quick check:**
- Payload shape or semantics changed?
- New fields that should be redacted/hashed?
- Fallback behavior that could mask upstream failure?
- PII handling correct?
- Consent fields propagated?

---

## Step 4: Generate Audit Report

Present findings in this format:

```
🔍 FEATURE AUDIT: [feature name or "Recent Changes"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY
├─ Critical: [N]
├─ High: [N]
├─ Medium: [N]
├─ Low: [N]
└─ Lenses Applied: [list]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 CRITICAL (must fix before merge)

1. [Issue Title]
   ├─ File: `path/to/file.py:42`
   ├─ Problem: [Description]
   ├─ Fix: [Specific remediation]
   └─ Lens: [Which lens found this]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ HIGH (should fix)

1. [Issue]
   ├─ File: `path/to/file.py:42`
   ├─ Problem: [Description]
   └─ Fix: [Remediation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 MEDIUM (consider fixing)

1. [Issue] - `file:line` - [Brief fix]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 THEMES (patterns to watch)

If multiple issues share a root cause, group them:

1. **[Theme Name]** - [N] instances
   └─ Representative: [One example with fix]
   └─ Pattern: [What to watch for]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PASSING (what looks good)

- [Positive observation 1]
- [Positive observation 2]
- [Positive observation 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 RECOMMENDATION

[PASS / PASS WITH FIXES / NEEDS WORK]

[Brief summary and next steps]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 5: Learnings Capture (Optional)

If a pattern appears that should become a rule:

**Ask the user:**
```
📝 LEARNINGS CAPTURE

This audit found recurring patterns that could become enforceable rules:

1. [Pattern] - Would you like to add this to CLAUDE.md/CODING_STANDARDS.md?

Add to project rules? [Y/n]
```

If yes, suggest specific text to add to project standards.

---

## Deep Mode (`--deep`)

If `--deep` flag is provided:

1. Run standard audit (Steps 1-4)
2. Present findings
3. **Fresh Session Prompt:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 FRESH SESSION REVIEW

For a second opinion, start a NEW Claude session and paste:

---
Review this diff against these acceptance criteria:

**Diff:**
[paste git diff output]

**Acceptance Criteria:**
[paste from feature spec/ticket]

**Known Constraints:**
- Performance: [any perf requirements]
- Data contracts: [any API contracts]
- Rollout plan: [feature flags, gradual rollout]

Look for issues the original developer might have missed.
Focus on: invariants, edge cases, implicit assumptions.
---

This breaks "same-context blindness" and catches different issue classes.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Single Lens Mode (`--lens <name>`)

If `--lens` flag is provided, run only that lens:

- `--lens security` → Run only Security & Abuse Cases lens
- `--lens business` → Run only Business Logic Walkthrough
- `--lens regression` → Run only Regression Surface analysis
- `--lens experiment` → Run only Experiment Integrity (domain-specific)
- `--lens data-contract` → Run only Data Contract Compliance (domain-specific)

For full lens documentation, see: `/audit:business`, `/audit:security`, etc.

---

## Integration Notes

**Works with:**
- `/feature-complete` - Run audit before marking complete
- `/check-drift` - Compare audit findings to original plan
- `/ai-review` - Lighter-weight code review (this is more comprehensive)

**References:**
- `ANTI_SLOP_STANDARDS.md` - Code quality patterns
- `CODING_STANDARDS.md` - Project-specific standards
- `CLAUDE.md` - Project context and rules

---

## Examples

```bash
# Quick audit of recent changes
/audit-feature

# Audit specific feature with deep mode
/audit-feature user-authentication --deep

# Security-focused audit only
/audit-feature --lens security

# Data contracts mode (includes experiment + data-contract lenses)
/audit-feature --data-contracts

# Audit specific commit range
/audit-feature --diff HEAD~5..HEAD
```

---

Feature audit complete! Review findings and address Critical/High issues before proceeding.
