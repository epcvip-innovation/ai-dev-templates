# Frontend Standards (HTML/CSS/JS)

**Purpose**: Prevent CSS/JS interaction bugs by establishing patterns for vanilla JavaScript frontend development.

**Core Problem**: When JavaScript manipulates element visibility or state directly via `style.display`, it can conflict with CSS's intended display type (block vs flex vs grid), causing layout bugs.

---

## The Golden Rule

> **CSS controls display types. JavaScript controls visibility states.**

---

## Top 3 Universal Frontend Standards

### 1. Never Use `style.display` Directly - Use Classes

**Rule**: Toggle visibility via CSS classes, not inline `style.display` manipulation.

**Why**: CSS defines the element's display type. JS overriding with a different type breaks layouts.

```css
/* CSS defines display type AND hidden state */
.stat-item { display: flex; flex-direction: column; }
.hidden { display: none !important; }
```

```javascript
// BAD: JS sets display type, may conflict with CSS
element.style.display = 'block';  // Overwrites flex with block

// GOOD: JS toggles visibility class, CSS controls display type
element.classList.add('hidden');     // Hide
element.classList.remove('hidden');  // Show (CSS flex takes over)
```

**Automated Check**:
```bash
# Find direct display manipulation (potential bug)
rg "\.style\.display\s*=" --type js --type ts
```

**Exceptions**:
- Third-party library integration that requires inline styles
- Dynamic layouts where display type is computed (document with rationale)

---

### 2. If You Must Use `style.display`, Match CSS's Display Type

**Rule**: When inline display is unavoidable, use the same value CSS expects.

```css
/* CSS expects flex */
.admin-controls { display: flex; }
```

```javascript
// BAD: JS uses block when CSS expects flex
adminControls.style.display = 'block';  // Breaks flex layout

// ACCEPTABLE: JS uses same display type as CSS
adminControls.style.display = 'flex';   // Matches CSS expectation

// BEST: Use class toggle instead
adminControls.classList.remove('hidden');
```

**Code Review Pattern**:
1. Find JS display manipulation: `element.style.display = 'value'`
2. Find element's CSS class definition
3. Verify values match

---

### 3. Use Utility Classes for Visibility States

**Standard utility classes** (add to your CSS):

```css
/* Visibility utilities - add to every project */
.hidden { display: none !important; }
.visible { visibility: visible; }
.invisible { visibility: hidden; }

/* Fade transitions */
.fade-out { opacity: 0; transition: opacity 0.2s; }
.fade-in { opacity: 1; transition: opacity 0.2s; }
```

**JavaScript usage**:
```javascript
// Toggle visibility
element.classList.toggle('hidden');

// Show/hide helpers
function show(el) { el.classList.remove('hidden'); }
function hide(el) { el.classList.add('hidden'); }

// Check visibility
const isHidden = element.classList.contains('hidden');
```

---

## State Management Patterns

### Use Data Attributes for UI State

```html
<!-- State stored in data attribute -->
<div class="modal" data-state="closed">
```

```css
/* CSS responds to state */
.modal[data-state="closed"] { display: none; }
.modal[data-state="open"] { display: flex; }
```

```javascript
// JS changes state, not display
modal.dataset.state = 'open';
modal.dataset.state = 'closed';
```

### Use Class-Based States for Simpler Cases

```html
<button class="dropdown-toggle">Menu</button>
<div class="dropdown-menu">...</div>
```

```css
.dropdown-menu { display: none; }
.dropdown-toggle.is-open + .dropdown-menu { display: block; }
```

```javascript
// Toggle state class, not display property
toggleBtn.classList.toggle('is-open');
```

---

## Naming Conventions

### State Classes

| Class | Meaning |
|-------|---------|
| `.hidden` | Completely hidden (`display: none`) |
| `.is-active` | Active/selected state |
| `.is-open` | Expanded/visible state |
| `.is-loading` | Loading in progress |
| `.is-disabled` | Disabled state |
| `.is-error` | Error state |

### CSS Patterns

```css
/* State classes modify appearance */
.button { background: blue; }
.button.is-loading { background: gray; pointer-events: none; }
.button.is-disabled { opacity: 0.5; cursor: not-allowed; }

/* Hidden state always uses !important to override display */
.hidden { display: none !important; }
```

---

## Common Anti-Patterns

### Anti-Pattern 1: Display Type Mismatch

```javascript
// CSS: .card { display: flex; flex-direction: column; }

// BAD: Sets display:block, breaks flex layout
card.style.display = 'block';

// GOOD: Use class toggle
card.classList.remove('hidden');
```

### Anti-Pattern 2: Mixing Inline and Class Styles

```javascript
// BAD: Sets inline style, then CSS class can't override
element.style.display = 'none';
element.classList.remove('hidden');  // Won't work! Inline wins

// GOOD: Consistent class-based approach
element.classList.add('hidden');
element.classList.remove('hidden');  // Works correctly
```

### Anti-Pattern 3: Hardcoded Values

```javascript
// BAD: Hardcoded colors/sizes
element.style.backgroundColor = '#ff0000';
element.style.padding = '16px';

// GOOD: Use CSS classes or variables
element.classList.add('error-state');
// CSS: .error-state { background: var(--error-bg); padding: var(--spacing-md); }
```

---

## Code Review Checklist

When reviewing frontend code, check for:

- [ ] **No `style.display =`** in JavaScript (use class toggling)
- [ ] **CSS defines display types**, JS only toggles visibility classes
- [ ] **State managed via classes** (`.is-*`) or data attributes
- [ ] **No hardcoded colors/sizes** in JS (use CSS variables)
- [ ] **Utility classes exist** (`.hidden`, `.is-active`, etc.)
- [ ] **If `style.display` used**, display type matches CSS expectation

---

## Quick Migration Guide

### Converting `style.display` to Class-Based

**Before** (bug-prone):
```javascript
function showAdminPanel() {
    adminPanel.style.display = 'block';  // May break flex/grid layout
}

function hideAdminPanel() {
    adminPanel.style.display = 'none';
}
```

**After** (robust):
```css
/* Add to CSS */
.hidden { display: none !important; }
```

```javascript
function showAdminPanel() {
    adminPanel.classList.remove('hidden');  // CSS display type preserved
}

function hideAdminPanel() {
    adminPanel.classList.add('hidden');
}
```

---

## Integration with Existing Standards

This document complements:
- **ANTI_SLOP_STANDARDS.md** - General code quality (functions <50 lines, etc.)
- **Project CODING_STANDARDS.md** - Language-specific style

**Scope**:
- **FRONTEND_STANDARDS.md**: HTML/CSS/JS interaction patterns
- **ANTI_SLOP_STANDARDS.md**: Universal code quality, AI slop prevention
- **CODING_STANDARDS.md**: Language-specific conventions (TypeScript, Python)

---

## Automated Checks

### Pre-Commit Hook (Optional)

```bash
#!/bin/bash
# .git/hooks/pre-commit (add to existing)

# Check for direct display manipulation
if rg "\.style\.display\s*=" --type js --type ts -q; then
    echo "WARNING: Found style.display manipulation"
    echo "Consider using class toggling instead. See FRONTEND_STANDARDS.md"
    rg "\.style\.display\s*=" --type js --type ts -n
fi
```

### grep Patterns

```bash
# Find direct display manipulation
rg "\.style\.display\s*=" --type js --type ts

# Find inline style assignments (potential smell)
rg "\.style\.\w+\s*=" --type js --type ts

# Find hardcoded colors in JS
rg "style\.(background|color)\s*=\s*['\"]#" --type js --type ts
```

---

## FAQ

### Q: Why not just use `style.display = ''` to reset?

**A**: Setting `style.display = ''` removes the inline style, but:
1. Requires knowing there's an inline style to remove
2. Creates inconsistent patterns (add vs remove)
3. Class-based approach is clearer and more consistent

### Q: What about CSS-in-JS libraries (styled-components, etc.)?

**A**: These standards apply to **vanilla JS**. CSS-in-JS libraries handle display types internally and are generally safe.

### Q: Is `!important` on `.hidden` too aggressive?

**A**: No. The `.hidden` class is a **utility** that should always win. If an element has `.hidden`, it should be hidden regardless of other styles. This is intentional.

---

**Last Updated**: 2026-01-23
**Applies To**: Vanilla JavaScript frontend projects (non-framework)
