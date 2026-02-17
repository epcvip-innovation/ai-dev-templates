# React-Specific Review Patterns

Patterns and rules specific to React codebases to reduce false positives and catch real issues.

---

## Hook Rules

### Real Issues (High Severity)

| Pattern | Severity | Why It Matters |
|---------|----------|----------------|
| Hooks inside conditionals | 90 | Breaks hook rules |
| Hooks inside loops | 90 | Breaks hook rules |
| Missing dependency in useEffect | 70 | Stale closure bugs |
| `useEffect` without cleanup | 60 | Memory leaks |

### Acceptable Patterns (Reduce Severity)

| Pattern | When OK | Score Adjustment |
|---------|---------|------------------|
| Empty dependency array `[]` | One-time effects | 0 if intentional |
| Disabling eslint exhaustive-deps | With comment | 30 (document why) |
| Multiple useEffects | Separation of concerns | 0 |

---

## State Management

### useState Issues

```jsx
// Bad: Object mutation
const [user, setUser] = useState({ name: 'Alice' });
user.name = 'Bob'; // Mutation! Won't trigger re-render

// Good: Immutable update
setUser({ ...user, name: 'Bob' });
```
**Severity**: Direct state mutation = 80

### Context Performance

```jsx
// Bad: Large context re-renders everything
const AppContext = createContext({ user, settings, theme, data });

// Better: Split contexts
const UserContext = createContext(user);
const ThemeContext = createContext(theme);
```
**Severity**: Large context without memo = 50

---

## Component Patterns

### Props Spreading

```jsx
// Risky: Unknown props to DOM
<div {...props} />

// Safer: Explicit props
<div className={props.className} onClick={props.onClick} />
```
**Severity**: Props spread to DOM = 40 (potential XSS via event handlers)

### Key Prop Issues

```jsx
// Bad: Index as key in dynamic list
{items.map((item, i) => <Item key={i} />)}

// Good: Stable unique key
{items.map((item) => <Item key={item.id} />)}
```
**Severity**: Index as key = 60 (causes re-render bugs)

---

## Performance

### Re-render Prevention

| Pattern | Severity | Notes |
|---------|----------|-------|
| Missing `memo()` on list items | 40 | Depends on list size |
| Inline object/function in render | 50 | Creates new reference |
| Large component without useMemo | 30 | Profile first |

### useCallback/useMemo Overuse

```jsx
// Unnecessary: Simple value
const doubled = useMemo(() => value * 2, [value]);

// Appropriate: Expensive computation
const sorted = useMemo(() => items.sort(expensiveFn), [items]);
```
**Adjustment**: Don't flag missing useMemo for simple operations.

---

## Security

### XSS Vectors

| Pattern | Severity | Notes |
|---------|----------|-------|
| `dangerouslySetInnerHTML` | 85 | Must sanitize |
| `href={userInput}` | 80 | javascript: URLs |
| Inline event handlers from props | 60 | Check source |

### Safe Patterns

```jsx
// Safe: React escapes by default
<div>{userInput}</div>

// Risky: Direct HTML
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

---

## Common False Positives

### 1. Custom Hooks with Conditional Logic

```jsx
// This is fine - hook is always called
function useAuth() {
  const user = useUser();
  if (!user) return null; // Conditional RETURN is OK
  return user.profile;
}
```
**Adjustment**: Conditional returns after hooks = OK

### 2. Effect Cleanup Not Needed

```jsx
// No cleanup needed for simple state updates
useEffect(() => {
  setLoaded(true);
}, []);
```
**Adjustment**: If effect only sets state, no cleanup warning.

### 3. Memo in Test Files

```jsx
// Test files often skip optimization
const TestComponent = () => <div>Test</div>;
```
**Adjustment**: In test files, don't flag missing memo/callbacks.

---

## Next.js / Remix Specifics

### Server Components (Next.js 13+)

| Pattern | Server OK | Client OK |
|---------|-----------|-----------|
| `useState` | No | Yes |
| `useEffect` | No | Yes |
| `async` component | Yes | No |
| Database queries | Yes | No |

**Rule**: Don't flag missing hooks in files without `'use client'` directive.

### Data Fetching

```jsx
// Next.js: Server-side is preferred
// Don't flag useEffect for data fetching if using getServerSideProps
```

---

## Severity Scoring for React

| Category | Base Score | Notes |
|----------|------------|-------|
| Hook rules violation | 90 | Always flag |
| Direct state mutation | 80 | Always flag |
| dangerouslySetInnerHTML | 85 | 0 if sanitized |
| Missing key prop | 70 | 50 if static list |
| Index as key | 60 | 30 if list never reorders |
| Missing useCallback | 40 | 0 in test files |
| Missing memo | 30 | Profile before flagging |

---

## Quick Reference

**Always Flag:**
- Hooks in conditionals/loops
- Direct state mutation
- Unsanitized dangerouslySetInnerHTML
- javascript: URLs in href

**Usually OK:**
- Conditional returns after hooks
- Empty dependency arrays (if intentional)
- Missing memo on small components
- Missing useCallback in non-critical paths
