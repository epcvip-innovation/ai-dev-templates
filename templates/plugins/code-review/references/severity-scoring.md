# Severity Scoring

How to score findings consistently and prioritize fixes.

## Score Ranges

| Score | Severity | Action | Response Time |
|-------|----------|--------|---------------|
| 80-100 | **Critical** | Must fix before merge | Immediately |
| 60-79 | **High** | Should fix, real risk | Before PR approval |
| 40-59 | **Medium** | Consider fixing | Next sprint |
| 0-39 | **Low/Pedantic** | Ignore | Never (usually) |

## Scenario Scoring Guide

### Critical (80-100)

| Scenario | Score |
|----------|-------|
| Proven exploitable vulnerability | 95-100 |
| Authentication bypass possible | 90-100 |
| Data loss or corruption possible | 85-95 |
| Production crash likely | 80-90 |
| Secrets exposed in code | 85-95 |
| SQL/command injection | 90-100 |

### High (60-79)

| Scenario | Score |
|----------|-------|
| Security best practice violation | 65-80 |
| Bug under specific conditions | 60-75 |
| XSS vulnerability (reflected) | 70-80 |
| Missing input validation | 65-75 |
| Race condition in writes | 70-80 |
| Resource leak (connections, memory) | 65-75 |

### Medium (40-59)

| Scenario | Score |
|----------|-------|
| Code smell, works but fragile | 45-60 |
| Missing error handling | 50-60 |
| N+1 query (moderate scale) | 45-55 |
| Missing test coverage | 40-55 |
| Inconsistent pattern | 40-50 |

### Low (0-39)

| Scenario | Score |
|----------|-------|
| Style/preference issue | 20-40 |
| Minor code duplication | 25-35 |
| Could be more elegant | 15-30 |
| Nitpick | 0-20 |
| Naming suggestion | 10-25 |

## Adjusting for Context

### Higher Scores When:
- **Financial data** involved (+10-15)
- **User PII** exposed (+10-15)
- **High traffic** endpoint (+5-10)
- **No rollback** possible (+10)
- **Compliance** requirements (+10-15)

### Lower Scores When:
- **Internal tool** only (-10-15)
- **Behind auth** already (-5-10)
- **Low traffic** (-5)
- **Easy rollback** available (-5)
- **Temporary code** (feature flag) (-10)

## Example Scoring Walkthrough

### Example 1: SQL Injection
```typescript
const query = `SELECT * FROM users WHERE id = '${userId}'`;
```
- Base score: 90 (SQL injection)
- User input? Yes, +0
- Production? Yes, +0
- Contains PII? Yes, +5
- **Final Score: 95** (Critical)

### Example 2: Missing Null Check
```typescript
function getName(user) {
  return user.profile.name; // Could be undefined
}
```
- Base score: 50 (null reference)
- Crash likely? Maybe, +5
- User-facing? Yes, +5
- Easy fix? Yes, -5
- **Final Score: 55** (Medium)

### Example 3: Floating Promise
```typescript
saveToDatabase(data); // Missing await
```
- Base score: 60 (async issue)
- Error silently ignored? Yes, +10
- Data loss possible? Maybe, +5
- **Final Score: 75** (High)

## Using --min-score

```bash
# Show only critical (80+)
/local-review --min-score 80

# Show high and above (60+) - default
/local-review --min-score 60

# Show everything including nitpicks
/local-review --min-score 0
```

## When Multiple Agents Flag Same Issue

If Security Auditor (85) and Bug Hunter (70) both flag the same line:
- **Confidence**: High (multiple perspectives agree)
- **Score**: 85 (use highest)
- **Context**: Merged from both agents

Multiple agents agreeing is a strong signal to prioritize the fix.
