# Review Patterns by Technology

## TypeScript / Node.js

### Critical Patterns (80+)
- `any` type usage hiding real type errors
- Missing `await` on async functions
- Unchecked `.json()` parsing without try/catch
- `req.body` or `req.query` used without validation
- Environment variables accessed without fallback
- `process.exit()` in library code

### High Patterns (60-79)
- Non-null assertion `!` without justification
- `as` type casting instead of type guards
- Floating promises (async call without await or .catch)
- Empty catch blocks swallowing errors
- `console.log` left in production code
- Hardcoded timeouts/retries without config

### Examples

**Bad: Floating promise**
```typescript
// Missing await - error silently ignored
saveToDatabase(data);
```

**Good:**
```typescript
await saveToDatabase(data);
// or if intentionally fire-and-forget:
saveToDatabase(data).catch(err => logger.error('Save failed', err));
```

## Express / HTTP APIs

### Critical Patterns (80+)
- Route handlers without error middleware
- `res.send(userInput)` without sanitization
- Missing rate limiting on auth endpoints
- Synchronous operations blocking event loop
- Secrets in query strings (logged by default)

### High Patterns (60-79)
- No request validation (missing zod/joi/etc)
- Missing CORS configuration
- No request ID for tracing
- Large payloads without size limits
- Missing compression for large responses

### Examples

**Bad: No validation**
```typescript
app.post('/users', (req, res) => {
  db.createUser(req.body); // Trusting client blindly
});
```

**Good:**
```typescript
app.post('/users', (req, res) => {
  const result = UserSchema.safeParse(req.body);
  if (!result.success) return res.status(400).json(result.error);
  db.createUser(result.data);
});
```

## PostgreSQL / Supabase

### Critical Patterns (80+)
- String interpolation in SQL queries
- Missing RLS policies on sensitive tables
- `SELECT *` in production queries
- No index on frequently filtered columns
- Credentials in connection strings in code

### High Patterns (60-79)
- N+1 query patterns (loop with queries inside)
- Missing transactions for multi-step operations
- No connection pooling configuration
- Unbounded queries without LIMIT
- Missing ON DELETE/UPDATE cascade consideration

### Examples

**Bad: SQL injection**
```typescript
const query = `SELECT * FROM users WHERE id = '${userId}'`;
```

**Good:**
```typescript
const { data } = await supabase
  .from('users')
  .select('id, name, email')
  .eq('id', userId)
  .single();
```

## WebSocket (ws library)

### Critical Patterns (80+)
- No authentication on connection
- Unbounded message handlers (memory exhaustion)
- Missing origin validation
- Broadcast without recipient filtering
- No heartbeat/ping-pong for stale connections

### High Patterns (60-79)
- No reconnection logic on client
- Missing message queue for offline clients
- No rate limiting per connection
- Large messages without chunking
- Missing close handler cleanup

### Examples

**Bad: No auth**
```typescript
wss.on('connection', (ws) => {
  ws.on('message', handleMessage); // Anyone can connect
});
```

**Good:**
```typescript
wss.on('connection', (ws, req) => {
  const token = new URL(req.url, 'http://localhost').searchParams.get('token');
  if (!validateToken(token)) {
    ws.close(4001, 'Unauthorized');
    return;
  }
  ws.on('message', handleMessage);
});
```

## Frontend / Vanilla JS

### Critical Patterns (80+)
- `innerHTML` with user content (XSS)
- `eval()` or `Function()` with dynamic input
- Storing auth tokens in localStorage (XSS accessible)
- Missing CSRF tokens on state-changing requests
- Credentials in client-side code

### High Patterns (60-79)
- No input sanitization before display
- Missing error boundaries/handlers
- Unbounded DOM manipulation (memory leaks)
- No debouncing on frequent events
- Missing loading/error states

### Examples

**Bad: XSS vulnerability**
```javascript
element.innerHTML = userComment;
```

**Good:**
```javascript
element.textContent = userComment;
// Or if HTML needed:
element.innerHTML = DOMPurify.sanitize(userComment);
```

## Jest / Testing

### Patterns to Flag (60+)
- `expect(true).toBe(true)` - meaningless assertion
- Mocking the thing being tested
- No assertions in test (silent pass)
- `setTimeout` in tests (flaky)
- Shared mutable state between tests
- Missing `afterEach` cleanup

### Examples

**Bad: Testing mocks**
```typescript
jest.mock('./userService');
test('creates user', async () => {
  await createUser(data);
  expect(mockUserService.create).toHaveBeenCalled(); // Only testing mock
});
```

**Good:**
```typescript
test('creates user', async () => {
  const result = await createUser(data);
  expect(result.id).toBeDefined();
  expect(result.email).toBe(data.email);
  // Verify actual behavior, not just that something was called
});
```

## Playwright / E2E

### Patterns to Flag (60+)
- Hardcoded waits (`page.waitForTimeout`)
- Missing test isolation (shared state)
- No retry configuration for flaky selectors
- Screenshot-only assertions (brittle)
- Missing accessibility checks

### Examples

**Bad: Hardcoded wait**
```typescript
await page.click('#submit');
await page.waitForTimeout(2000);
expect(await page.locator('.success').isVisible()).toBe(true);
```

**Good:**
```typescript
await page.click('#submit');
await expect(page.locator('.success')).toBeVisible({ timeout: 5000 });
```
