# Python-Specific Review Patterns

Patterns and rules specific to Python codebases to reduce false positives and catch real issues.

---

## Type Hints

### Real Issues (High Severity)

| Pattern | Severity | Why It Matters |
|---------|----------|----------------|
| `Any` type in public API | 60 | API contract unclear |
| Missing return type annotation | 40 | Hard to maintain |
| `# type: ignore` without comment | 70 | Hides issues |
| Incorrect type narrowing | 50 | Runtime errors |

### Acceptable Patterns (Reduce Severity)

| Pattern | When OK | Score Adjustment |
|---------|---------|------------------|
| `Any` in generic wrappers | Proper forwarding | 0 |
| Missing types in tests | Test code | 0 |
| `cast()` with comment | Known limitation | 20 |

---

## Security

### SQL Injection

```python
# Bad: String formatting
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good: Parameterized
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```
**Severity**: f-string in SQL = 95

### Command Injection

```python
# Bad: Shell=True with user input
subprocess.run(f"ls {user_path}", shell=True)

# Good: List arguments
subprocess.run(["ls", user_path])
```
**Severity**: shell=True with variable = 90

### Path Traversal

```python
# Bad: Direct path join
file_path = os.path.join(base_dir, user_filename)

# Good: Validate within bounds
file_path = os.path.join(base_dir, user_filename)
if not file_path.startswith(os.path.abspath(base_dir)):
    raise ValueError("Path traversal detected")
```
**Severity**: Unvalidated path join = 80

---

## Error Handling

### Exception Patterns

| Pattern | Severity | Notes |
|---------|----------|-------|
| Bare `except:` | 80 | Catches SystemExit, KeyboardInterrupt |
| `except Exception:` | 50 | Usually OK, document if intentional |
| `except: pass` | 90 | Silent failure |
| No exception handling in I/O | 40 | Depends on context |

### Good Patterns

```python
# Specific exceptions
except (ValueError, TypeError) as e:
    logger.error(f"Invalid input: {e}")
    return None

# Re-raising with context
except HTTPError as e:
    raise APIError(f"Failed to fetch: {e}") from e
```

---

## Resource Management

### Context Managers

```python
# Bad: Manual resource handling
f = open("file.txt")
data = f.read()
f.close()  # May not run on exception

# Good: Context manager
with open("file.txt") as f:
    data = f.read()
```
**Severity**: File open without context manager = 60

### Connection Handling

```python
# Bad: Connection leak
conn = db.connect()
# ... code that might raise ...
conn.close()

# Good: Context manager or try/finally
with db.connect() as conn:
    # ... code ...
```
**Severity**: DB connection without context manager = 70

---

## Async Patterns

### Common Issues

| Pattern | Severity | Notes |
|---------|----------|-------|
| `asyncio.run()` in async context | 80 | Nested event loop |
| Missing `await` | 70 | Coroutine not executed |
| Sync I/O in async function | 60 | Blocks event loop |
| Unbounded `asyncio.gather()` | 50 | Resource exhaustion |

### Good Patterns

```python
# Bounded concurrency
semaphore = asyncio.Semaphore(10)
async with semaphore:
    await fetch_data()

# Proper cancellation handling
try:
    await some_operation()
except asyncio.CancelledError:
    # Cleanup
    raise
```

---

## Common False Positives

### 1. F-strings in Logging

```python
# This is fine - no SQL
logger.info(f"User {user_id} logged in")
```
**Adjustment**: F-strings in logger calls = 0 severity

### 2. Type Comments in Python 2 Compat

```python
# type: ignore for Python 2 compatibility
def func(x):  # type: (int) -> str
```
**Adjustment**: If project supports Python 2, don't flag type comments

### 3. Test Assertions

```python
# Tests often have broad exceptions
with pytest.raises(Exception):
    risky_function()
```
**Adjustment**: In test files, reduce exception severity by 80%

---

## Framework Specifics

### Django/Flask

| Pattern | Severity | Notes |
|---------|----------|-------|
| Raw SQL in views | 80 | Use ORM |
| Missing CSRF protection | 85 | Security issue |
| DEBUG=True in production | 90 | Information leak |
| Hardcoded SECRET_KEY | 95 | Credential exposure |

### FastAPI/Pydantic

| Pattern | Severity | Notes |
|---------|----------|-------|
| `Any` in Pydantic models | 60 | Skips validation |
| Missing `response_model` | 30 | Documentation issue |
| Sync DB calls in async route | 70 | Blocks event loop |

---

## Severity Scoring for Python

| Category | Base Score | Notes |
|----------|------------|-------|
| SQL injection | 95 | Always flag |
| Command injection | 90 | Always flag |
| Bare except | 80 | -30 if has logging |
| except: pass | 90 | Always flag |
| Missing type hints | 40 | 0 in test files |
| Resource leak | 60-70 | Check for try/finally |
| Any type | 60 | 0 in internal utils |

---

## Quick Reference

**Always Flag:**
- f-strings in SQL/subprocess
- Bare `except:` or `except: pass`
- `shell=True` with variables
- Hardcoded credentials

**Usually OK:**
- `except Exception:` with logging
- Missing types in test files
- F-strings in log messages
- `# type: ignore` with explanation
