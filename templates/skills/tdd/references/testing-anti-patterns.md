# Testing Anti-Patterns

Extended reference for common testing anti-patterns. Loaded on demand when reviewing test quality.

## Anti-Pattern Catalog

### 1. Mocking Real Behavior

**Wrong**: Mocking the function under test, then asserting the mock returns what you told it to.

```python
# Bad — tests that the mock works, not the code
mock_auth.return_value = AuthResult(success=True)
result = mock_auth("alice", "secret")
assert result.success is True  # You're testing the mock
```

**Right**: Test the real function. Only mock external boundaries (network, filesystem, clock).

### 2. Test-Only Production Methods

**Wrong**: Adding methods to production code solely for test access.

```python
# Bad — production code polluted with test helpers
class UserService:
    def _test_get_internal_cache(self):  # Only called by tests
        return self._cache
```

**Right**: Test through the public API. If you can't, the design needs refactoring.

### 3. Assertion-Free Tests

**Wrong**: Tests that run code but never assert outcomes.

```python
# Bad — exercises code but proves nothing
def test_process_order():
    process_order(sample_order)
    # No assertions — "it didn't crash" is not a test
```

**Right**: Assert specific outcomes. Every test proves something.

### 4. Implementation-Coupled Tests

**Wrong**: Tests that break when you refactor without changing behavior.

```python
# Bad — tied to internal method names
def test_user_creation():
    user = User("alice")
    assert user._validate_name.called  # Testing internals
```

**Right**: Assert observable behavior (return values, side effects, state changes).

### 5. Shotgun Assertions

**Wrong**: Asserting everything to "make sure nothing changed."

```python
# Bad — fragile, obscures intent
assert user.name == "alice"
assert user.id == 42
assert user.created_at == datetime(2026, 1, 1)
assert user.updated_at == datetime(2026, 1, 1)
assert user.role == "member"
assert user.active is True
# What behavior is this actually testing?
```

**Right**: Assert only what this test is about. One behavior per test.

### 6. Flaky Time Dependencies

**Wrong**: Tests that depend on wall clock time.

```python
# Bad — fails at midnight, across timezones, on slow CI
def test_token_not_expired():
    token = create_token()
    assert token.expires_at > datetime.now()
```

**Right**: Inject a clock. Control time in tests.

### 7. Shared Mutable State

**Wrong**: Tests that depend on or modify global state.

```python
# Bad — test order matters, parallel execution breaks
_users = []  # Module-level shared state

def test_add_user():
    _users.append(User("alice"))
    assert len(_users) == 1  # Fails if another test ran first
```

**Right**: Each test creates its own state. Use fixtures for setup/teardown.

### 8. Testing Framework Behavior

**Wrong**: Tests that verify the testing framework or language features.

```python
# Bad — testing Python, not your code
def test_list_append():
    items = []
    items.append("x")
    assert len(items) == 1
```

**Right**: Test your code's behavior, not the tools it uses.

---

**See also**: [Anti-Slop Standards](../../standards/ANTI_SLOP_STANDARDS.md) for code quality patterns.
