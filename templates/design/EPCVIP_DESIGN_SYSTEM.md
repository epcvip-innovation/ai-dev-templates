# EPCVIP Design System

Shared design guidelines for all epcvip.vip applications. Not a library to import - a reference document for consistent styling.

**Last Updated:** 2026-01-21
**Applies To:** All *.epcvip.vip apps (except special-theme apps like Tools Hub)

---

## Quick Start

Copy these CSS variables to your app's stylesheet:

```css
:root {
    /* Background Layers (darkest to lightest) */
    --bg-primary: #1a1a1a;      /* Body background */
    --bg-secondary: #2a2a2a;    /* Cards, headers, modals */
    --bg-tertiary: #333333;     /* Form inputs, alternating rows */
    --bg-elevated: #404040;     /* Hover states, highest elevation */

    /* Text Hierarchy */
    --text-primary: #ffffff;    /* Headlines, important text */
    --text-secondary: #e5e5e5;  /* Body text */
    --text-muted: #a0a0a0;      /* Secondary info, placeholders */
    --text-disabled: #666666;   /* Disabled states */

    /* Brand Accent (EPCVIP Gold) */
    --accent-primary: #ffd700;       /* Primary actions, links */
    --accent-primary-hover: #ffed4e; /* Hover states */

    /* Borders */
    --border-primary: #404040;
    --border-secondary: #4a4a4a;
    --border-subtle: #333333;

    /* Semantic Colors */
    --success: #10b981;
    --success-bg: rgba(16, 185, 129, 0.1);
    --warning: #f59e0b;
    --warning-bg: rgba(245, 158, 11, 0.1);
    --error: #ef4444;
    --error-bg: rgba(239, 68, 68, 0.1);
    --info: #3b82f6;
    --info-bg: rgba(59, 130, 246, 0.1);

    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
}
```

---

## Design Principles

### 1. Dark Theme First
All apps use dark backgrounds for DOIS Hub alignment and reduced eye strain.

### 2. Gold Accent for Brand
EPCVIP gold (`#ffd700`) is the primary accent color across all professional apps. This creates visual continuity when users navigate between tools.

### 3. Semantic Colors for Status
Use the same success/warning/error/info colors everywhere. Never invent new status colors.

### 4. Progressive Elevation
Background layers indicate depth:
- `--bg-primary` → page background
- `--bg-secondary` → cards, modals
- `--bg-tertiary` → inputs, nested elements
- `--bg-elevated` → hover states, highest elements

---

## Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### Text Hierarchy
| Level | Color | Weight | Use Case |
|-------|-------|--------|----------|
| Primary | `--text-primary` (#fff) | 600-700 | Headlines, labels |
| Secondary | `--text-secondary` (#e5e5e5) | 400-500 | Body text |
| Muted | `--text-muted` (#a0a0a0) | 400 | Help text, timestamps |
| Disabled | `--text-disabled` (#666) | 400 | Disabled inputs |

### Monospace (Code/Data)
```css
font-family: "SF Mono", Monaco, Consolas, "Ubuntu Mono", monospace;
```

---

## Spacing & Layout

### Border Radius
| Element | Radius |
|---------|--------|
| Buttons, inputs | `6px` |
| Cards, modals | `12px` |
| Pills, badges | `9999px` (full round) |

### Standard Spacing
| Use | Value |
|-----|-------|
| Card padding | `2rem` |
| Section gap | `2rem` |
| Form group margin | `1.5rem` |
| List item gap | `1rem` |
| Input padding | `0.75rem` |

### Container
```css
.container {
    max-width: 1400px;  /* or 1760px for data-heavy apps */
    margin: 0 auto;
    padding: 2rem;
}
```

---

## Components

### Buttons

#### Primary (Gold Accent)
```css
.btn-primary {
    background: var(--accent-primary);
    color: var(--bg-primary);  /* Dark text on gold */
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-primary:hover {
    background: var(--accent-primary-hover);
    box-shadow: var(--shadow-sm);
}
```

#### Secondary
```css
.btn-secondary {
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    border: 1px solid var(--border-primary);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-secondary:hover {
    background: var(--bg-elevated);
    border-color: var(--border-secondary);
}
```

### Form Inputs
```css
input, textarea, select {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border: 1px solid var(--border-primary);
    border-radius: 6px;
    padding: 0.75rem;
    transition: border-color 0.2s ease, background-color 0.2s ease;
}

input:focus, textarea:focus, select:focus {
    outline: none;
    border-color: var(--accent-primary);
    background: var(--bg-elevated);
    box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}
```

### Cards
```css
.card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-primary);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: var(--shadow-md);
}
```

### Badges

#### Base Badge
```css
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}
```

#### Status Badges
```css
.badge-success {
    background: var(--success-bg);
    color: var(--success);
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-warning {
    background: var(--warning-bg);
    color: var(--warning);
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-error {
    background: var(--error-bg);
    color: var(--error);
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.badge-info {
    background: var(--info-bg);
    color: var(--info);
    border: 1px solid rgba(59, 130, 246, 0.3);
}
```

### Tables
```css
.data-table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-secondary);
    border: 1px solid var(--border-primary);
    border-radius: 8px;
    overflow: hidden;
}

.data-table th {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    font-weight: 600;
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border-primary);
}

.data-table td {
    padding: 1rem;
    border-bottom: 1px solid var(--border-subtle);
}

.data-table tbody tr:hover {
    background: var(--bg-tertiary);
}
```

### Modals
```css
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: var(--bg-secondary);
    border: 1px solid var(--border-primary);
    border-radius: 12px;
    box-shadow: var(--shadow-lg);
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow: auto;
}

.modal-header {
    background: var(--bg-tertiary);
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--border-primary);
}
```

---

## Interactive States

### Hover
```css
/* Cards/containers - subtle */
.card:hover {
    background: var(--bg-tertiary);
    border-color: var(--border-secondary);
}

/* Buttons - more prominent */
.btn:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Table rows */
tr:hover {
    background: var(--bg-tertiary);
}
```

### Focus
```css
/* Gold focus ring for all focusable elements */
:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
    border-color: var(--accent-primary);
}
```

### Transitions
```css
/* Standard transition for all interactive elements */
transition: all 0.2s ease;
```

---

## Responsive Breakpoints

```css
/* Desktop (default) */
/* No media query needed */

/* Tablet */
@media (max-width: 1024px) {
    .container { padding: 1.5rem; }
}

/* Mobile */
@media (max-width: 768px) {
    .container { padding: 1rem; }
    .card { padding: 1.5rem; }
}
```

---

## Accessibility

### Contrast Ratios
- All text meets WCAG AA (4.5:1 minimum)
- `--text-primary` on `--bg-primary`: 13.1:1
- `--text-secondary` on `--bg-primary`: 11.9:1
- `--accent-primary` on `--bg-primary`: 10.1:1

### Focus Visibility
- Gold focus ring (`rgba(255, 215, 0, 0.2)`) visible on all backgrounds
- Never remove focus indicators

### Color Independence
- Don't convey information by color alone
- Always include text labels with status badges

---

## App-Specific Variations

### Experiments Dashboard (xp.epcvip.vip)
Currently uses blue accent (`#3b82f6`). Should migrate to gold for consistency.

### Tools Hub (epcvip.vip)
**Exception**: Uses retro GameBoy theme (`#f0c000` gold, green screen colors). This is intentional for the gaming aesthetic and should NOT follow this design system.

### Reports Dashboard (reports.epcvip.vip)
Streamlit app - limited CSS control. Use Streamlit theming to approximate these colors.

---

## Implementation Checklist

When creating a new app or updating an existing one:

- [ ] Copy CSS variables to `:root`
- [ ] Use gold accent (`#ffd700`) for primary actions
- [ ] Use semantic colors for status (success/warning/error/info)
- [ ] Apply standard border-radius (6px buttons, 12px cards)
- [ ] Add focus states with gold ring
- [ ] Test on mobile (768px breakpoint)
- [ ] Verify contrast ratios

---

## Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Ping Tree Compare Design System | `utilities/ping-tree-compare/DESIGN_SYSTEM.md` | Full component reference |
| EPCVIP Services | `EPCVIP_SERVICES.md` | Service architecture, auth |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-21 | Initial version extracted from ping-tree-compare |
