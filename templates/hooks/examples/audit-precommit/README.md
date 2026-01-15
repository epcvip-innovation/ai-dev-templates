# Pre-Commit Audit Hook

Lightweight anti-slop and security checks that run before every commit.

## What It Does

- **Blocks** on Critical issues (SQL injection, hardcoded secrets, empty exceptions)
- **Warns** on High issues (console.log, print statements, incomplete TODOs)
- **Informs** on Medium issues (magic numbers, long lines)

## Installation

### Option 1: Git Pre-Commit Hook (Recommended)

```bash
# Copy to your project
cp audit-precommit.py /path/to/your-project/.git/hooks/pre-commit
chmod +x /path/to/your-project/.git/hooks/pre-commit
```

### Option 2: Claude Code Hook (Global)

```bash
# Copy to Claude Code hooks directory
cp audit-precommit.py ~/.claude/hooks/audit-precommit.py
chmod +x ~/.claude/hooks/audit-precommit.py
```

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/audit-precommit.py"
          }
        ]
      }
    ]
  }
}
```

### Option 3: Pre-Commit Framework

If using [pre-commit](https://pre-commit.com/):

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: audit-precommit
        name: Audit Pre-Commit
        entry: python3 .hooks/audit-precommit.py
        language: system
        always_run: true
```

## Bypass

For emergencies (use sparingly):

```bash
SKIP_AUDIT=1 git commit -m "emergency fix"
```

## What It Checks

### Critical (Blocks Commit)

| Check | Pattern | Why |
|-------|---------|-----|
| SQL Injection | `execute` with f-strings or concatenation | Security vulnerability |
| Hardcoded Secrets | `password/api_key/secret/token = "..."` | Credential exposure |
| Empty Exception | `except: pass` | Silent failures |

### High (Warns)

| Check | Pattern | Why |
|-------|---------|-----|
| Console Log | `console.log(` | Debug code in production |
| Print Statement | `print(` | Use proper logging |
| TODO Without Context | `# TODO` with no description | Incomplete work |

### Medium (Informational)

| Check | Pattern | Why |
|-------|---------|-----|
| Magic Number | Common values like 60, 3600, 86400 | Use named constants |
| Long Line | Lines over 120 chars | Readability |

## Customization

Edit the `*_PATTERNS` dictionaries in `audit-precommit.py` to:

- Add project-specific patterns
- Adjust severity levels
- Change file type filters
- Modify messages

### Example: Add Custom Pattern

```python
CRITICAL_PATTERNS = {
    # ... existing patterns ...
    
    'Banned Function': {
        'pattern': r'deprecated_function\(',
        'file_types': ['.py'],
        'message': 'deprecated_function is banned: use new_function instead',
    },
}
```

### Example: Skip Additional Files

```python
SKIP_PATTERNS = [
    # ... existing patterns ...
    r'migrations/',      # Django migrations
    r'generated/',       # Generated code
    r'vendor/',          # Vendored dependencies
]
```

## Output Example

```
🔍 Running pre-commit audit...

📊 Found 4 issues:

============================================================
🚨 CRITICAL ISSUES (blocking commit)
============================================================
🚨 CRITICAL: SQL Injection
   File: api/users.py:45
   Potential SQL injection: use parameterized queries
   > cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

============================================================
⚠️  HIGH ISSUES (should fix)
============================================================
⚠️ HIGH: Console Log in Production
   File: static/js/app.js:120
   console.log found: remove before production
   > console.log("Debug:", data)

============================================================
💡 MEDIUM ISSUES: 2 found (informational)
============================================================
   - Magic Number: 2 instances

============================================================
❌ COMMIT BLOCKED
============================================================
Fix critical issues before committing.

To bypass (emergency only):
  SKIP_AUDIT=1 git commit -m 'message'
```

## Integration with /audit-feature

This hook provides **fast, deterministic checks** as a pre-commit gate.

For comprehensive audits, use `/audit-feature` which provides:
- Multi-lens review (business logic, security, regression)
- Bounded severity with stop conditions
- EPCVIP-specific lenses (experiment integrity, data contracts)

**Workflow:**
1. Pre-commit hook catches obvious issues automatically
2. `/audit-feature` provides deep review before completing features
3. CI provides final verification (security-review.yml)

## Performance

- Early exit for non-code files: <1ms
- Per-file check: ~5-10ms
- Typical commit with 10 files: <100ms

## Related Templates

- [/audit-feature](../../slash-commands/ai-dev-workflow/commands/audit-feature.md) - Comprehensive feature audit
- [Query Validation Hook](../query-validation/) - Database query validation
- [Hooks README](../../README.md) - Full hooks documentation
