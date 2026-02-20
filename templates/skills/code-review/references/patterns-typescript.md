# TypeScript-Specific Review Patterns

Patterns and rules specific to TypeScript codebases to reduce false positives and catch real issues.

---

## Type Safety Patterns

### Real Issues (High Severity)

| Pattern | Severity | Why It Matters |
|---------|----------|----------------|
| `as any` | 70 | Bypasses type safety |
| `@ts-ignore` without comment | 80 | Hides potential bugs |
| `!` non-null assertion on user input | 85 | Trusts untrusted data |
| Missing return type on public API | 50 | API contract unclear |

### Acceptable Patterns (Reduce Severity)

| Pattern | When OK | Score Adjustment |
|---------|---------|------------------|
| `as const` assertions | Type narrowing | 0 |
| `satisfies` operator | Type checking without widening | 0 |
| Generic constraints | Proper type bounds | 0 |
| `unknown` instead of `any` | Proper handling | 0 |

---

## Common False Positives

### 1. Express Route Handlers

```typescript
// This looks like untyped callback but is actually typed
app.get('/api/users', async (req, res) => { ... });
```
**Adjustment**: If using Express/Fastify, don't flag untyped req/res if framework types are installed.

### 2. Type Assertions in Tests

```typescript
// Test files often need assertions for mocks
const mockFn = jest.fn() as jest.Mock<ReturnType>;
```
**Adjustment**: In `*.test.ts` or `*.spec.ts`, reduce `as` assertion severity by 50%.

### 3. Third-Party Library Types

```typescript
// Sometimes library types are wrong
const result = externalLib.method() as CorrectType;
```
**Adjustment**: If in same line as external library call, add note "verify library types".

---

## Node.js/Express Specifics

### Environment Variables

```typescript
// This is fine if validated at startup
const PORT = process.env.PORT || 3000;

// This is risky - could be undefined at runtime
const API_KEY = process.env.API_KEY!;
```

**Rule**: Flag `process.env.X!` (non-null assertion) as 60 severity unless validated elsewhere.

### Database Query Types

```typescript
// Supabase/Prisma return types are often `any`
const { data } = await supabase.from('users').select('*');
```

**Adjustment**: Known ORMs with proper types - reduce severity if using official client.

---

## React/JSX Specifics

### Event Handlers

```typescript
// This is typed correctly via React types
const handleClick = (e: React.MouseEvent) => { ... };

// This is also fine - inferred from JSX
<button onClick={(e) => handleClick(e)} />
```

### Props Typing

| Pattern | Severity | Notes |
|---------|----------|-------|
| Missing `children` type | 30 | Often inferred |
| `any` in props | 70 | Should be typed |
| Generic component without constraints | 50 | Consider adding |

---

## Severity Scoring for TypeScript

| Category | Base Score | Notes |
|----------|------------|-------|
| Type assertion to `any` | 70 | -20 if in test file |
| Missing explicit return type | 40 | -20 if private function |
| `@ts-ignore` | 80 | 0 if has comment explaining why |
| Non-null assertion `!` | 60 | 0 if after validation check |
| Implicit `any` parameter | 50 | Flag for public functions |

---

## Quick Reference

**Always Flag:**
- `as any` in production code
- `@ts-ignore` without explanation
- `!` on user input without validation
- `eval()` or `Function()` constructor

**Usually OK:**
- `as const` for literal types
- Type assertions in test files
- `satisfies` operator usage
- Explicit `unknown` handling
