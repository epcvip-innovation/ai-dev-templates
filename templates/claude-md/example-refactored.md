# Example: Refactoring Bloated CLAUDE.md

**Case Study**: capacity-planner (React + TypeScript)

**Problem**: CLAUDE.md grew from ~178 lines (template baseline) to 512 lines (186% bloat)

**Solution**: Extract 334 lines to 4 separate docs, reducing to 178 lines

**Result**: 65% size reduction while preserving all information through modular references

---

## Before Refactoring

**Status**: 512 lines, 156% over official guidance (100-200 lines)

**Bloat Analysis**:
- Embedded 89 lines of coding standards ❌
- Embedded 51 lines of statistical formulas ❌
- Embedded 95 lines of development guides ❌
- No modular references ❌
- Multiple sections >30 lines ❌

**Violations**:
1. 🔴 Length bloat: 512 lines (target: 150-200)
2. 🔴 Embedded coding standards: 164 lines should be separate
3. 🔴 Embedded domain knowledge: 67 lines should be separate
4. 🟡 Missing references: 0 "See [doc]" links found
5. 🟡 Long sections: 6 sections exceed 30-line limit

---

## Refactoring Strategy

### Step 1: Identify Extractable Content

Run `/audit-claude-md` to detect violations:

```
# CLAUDE.md Audit Report

## Summary
- Length: 512 lines 🔴 (156% over guidance)
- References: 0 found 🔴
- Bloat Score: 334 lines extractable (65% bloat)

## Violations

### 🔴 Embedded Coding Standards (164 lines)
- "Code Quality Standards" section: 89 lines
- "Component Guidelines" section: 30 lines
- "Error Handling Philosophy" section: 25 lines
- "Common Pitfalls" section: 20 lines

### 🔴 Embedded Domain Knowledge (67 lines)
- "Key Domain Concepts" section: 16 lines
- "Working with Statistical Calculations" section: 51 lines

### 🔴 Embedded Development Guides (95 lines)
- "Project Structure" section: 30 lines
- "Typical Workflow" section: 10 lines
- "Understanding Data Model" section: 25 lines
- "Resources and References" section: 30 lines
```

### Step 2: Create Target Documentation Files

```bash
# Create separate docs for extracted content
touch CODING_STANDARDS.md       # 164 lines from CLAUDE.md
touch STATISTICAL_REFERENCE.md  # 67 lines from CLAUDE.md
touch DEVELOPMENT_GUIDE.md      # 95 lines from CLAUDE.md

# Optional: Create docs/ subdirectory for organization
mkdir -p docs/
mv STATISTICAL_REFERENCE.md docs/
mv DEVELOPMENT_GUIDE.md docs/
```

### Step 3: Extract Content to Separate Docs

See detailed extraction below for each file.

### Step 4: Replace with References in CLAUDE.md

For each extracted section, replace with 3-line summary + reference link.

---

## Detailed Extraction: Before → After

### Example 1: Coding Standards (89 lines → 3 lines)

#### ❌ BEFORE (in CLAUDE.md):
```markdown
## Code Quality Standards

**Anti-Slop Principles**:

### What Good Code Looks Like
- **Functions <50 lines**: Break down larger functions
- **Nesting depth <3**: Use early returns
- **No premature optimization**: Start simple, profile first
- **Clear naming**: Descriptive variable/function names
- **Single responsibility**: Each function does one thing

### What Bad Code Looks Like
- Long functions (>50 lines)
- Deep nesting (>3 levels)
- Clever abstractions
- Magic numbers
- Copy-paste code

### Code Review Checklist
Before accepting ANY code:
- [ ] Functions are under 50 lines
- [ ] Nesting depth is under 3 levels
- [ ] No console.log statements
- [ ] TypeScript types are explicit (no `any`)
- [ ] Components follow single responsibility
- [ ] Error handling is explicit
- [ ] Loading states are handled
- [ ] Edge cases are considered

### Examples

**Good - Clear, Simple**:
```typescript
function calculateEPL(impressions: number, conversions: number): number {
  if (impressions === 0) return 0
  return (conversions / impressions) * 100
}
```

**Bad - Over-engineered**:
```typescript
const calculateMetric = (config: MetricConfig): number => {
  const strategy = MetricStrategyFactory.create(config.type)
  return strategy.calculate(config.params)
}
```

[... 60 more lines of examples and explanations ...]
```

#### ✅ AFTER (in CLAUDE.md):
```markdown
## Code Quality Standards

We follow anti-slop principles: functions <50 lines, nesting <3, no premature optimization, clear naming.

**Reference**: See [CODING_STANDARDS.md](./CODING_STANDARDS.md) for complete guidelines with examples and review checklist
```

**Savings**: 86 lines removed from CLAUDE.md, full detail preserved in CODING_STANDARDS.md

---

### Example 2: Statistical Domain Knowledge (51 lines → 3 lines)

#### ❌ BEFORE (in CLAUDE.md):
```markdown
## Working with Statistical Calculations

### EPL (Earnings Per Lead)
Formula: `(conversions / impressions) * 100`

**Interpretation**:
- Higher EPL = Better converting traffic
- Benchmark: 2-5% is typical for personal loans
- < 1% = Poor quality traffic
- > 10% = Exceptional (or data error)

**Edge cases**:
- If impressions = 0, return 0 (not error)
- If conversions > impressions, flag as data error

### Redirect Rate
Formula: `(redirects / impressions) * 100`

**Interpretation**:
- Shows what % of traffic is sent to affiliates
- 100% = All traffic redirected
- < 50% = Many rejections (quality filter working)

### Sample Size Calculations
Minimum sample size for statistical significance:

**Formula**:
```typescript
function minSampleSize(
  baselineRate: number,
  mde: number,  // minimum detectable effect (e.g., 0.10 for 10%)
  alpha: number = 0.05,  // significance level
  power: number = 0.80   // statistical power
): number {
  // Z-scores for alpha and power
  const zAlpha = 1.96  // for 95% confidence
  const zPower = 0.84  // for 80% power

  const p = baselineRate
  const pooledP = p * (1 + mde)

  return Math.ceil(
    2 * Math.pow(zAlpha + zPower, 2) *
    pooledP * (1 - pooledP) /
    Math.pow(mde * p, 2)
  )
}
```

[... 20 more lines of statistical formulas ...]
```

#### ✅ AFTER (in CLAUDE.md):
```markdown
## Domain Knowledge

**Key Statistical Concepts**: EPL (earnings per lead), Redirect Rate, Sample Size calculations

**Reference**: See [docs/STATISTICAL_REFERENCE.md](./docs/STATISTICAL_REFERENCE.md) for formulas, interpretations, and edge cases
```

**Savings**: 48 lines removed from CLAUDE.md, full formulas preserved in STATISTICAL_REFERENCE.md

---

### Example 3: Project Structure (30 lines → 5 lines)

#### ❌ BEFORE (in CLAUDE.md):
```markdown
## Project Structure

```
capacity-planner/
├── src/
│   ├── components/
│   │   ├── CapacityPlanner.tsx    # Main container component
│   │   ├── CapacityHeader.tsx     # Header with controls
│   │   ├── TreeTable.tsx          # Tree visualization table
│   │   ├── CapacityCard.tsx       # Tree capacity cards
│   │   ├── RecommendationPanel.tsx # Warnings/suggestions
│   │   └── TestSetupForm.tsx      # A/B test configuration
│   ├── utils/
│   │   ├── calculations.ts        # EPL, redirect rate, sample size
│   │   ├── trafficAllocation.ts   # Traffic split calculations
│   │   └── recommendations.ts     # Warning/suggestion engine
│   ├── types/
│   │   ├── index.ts               # Core TypeScript types
│   │   └── calculations.ts        # Calculation-specific types
│   ├── data/
│   │   └── mockData.ts            # FLA-Google mock dataset
│   └── App.tsx                    # Main app component
├── docs/
│   └── planning/
│       ├── PROJECT_OVERVIEW.md    # Problem statement, goals
│       ├── TASKS.md               # Task list with phases
│       ├── DATA_ASSUMPTIONS.md    # Statistical assumptions
│       └── FEATURES_BACKLOG.md    # Future features
└── public/                        # Static assets
```
```

#### ✅ AFTER (in CLAUDE.md):
```markdown
## File Organization

```
src/components/  # UI components (CapacityPlanner, TreeTable, etc.)
src/utils/       # Calculations (EPL, traffic allocation)
docs/planning/   # Planning docs (TASKS, FEATURES_BACKLOG)
```

**Reference**: See [docs/DEVELOPMENT_GUIDE.md](./docs/DEVELOPMENT_GUIDE.md) for complete file structure
```

**Savings**: 25 lines removed from CLAUDE.md, full tree preserved in DEVELOPMENT_GUIDE.md

---

### Example 4: Component Guidelines (30 lines → 5 lines)

#### ❌ BEFORE (in CLAUDE.md):
```markdown
## Component Guidelines

### Color Coding for Trees
We use consistent color coding for visual recognition:

```typescript
// Control groups
const controlColors = {
  bg: 'bg-blue-50',
  border: 'border-blue-200',
  text: 'text-blue-700'
}

// Variant groups
const variantColors = {
  bg: 'bg-purple-50',
  border: 'border-purple-200',
  text: 'text-purple-700'
}

// Warning states
const warningColors = {
  bg: 'bg-yellow-50',
  border: 'border-yellow-200',
  text: 'text-yellow-700'
}
```

### Icon Usage
- ⚠️ **AlertCircle** for warnings
- ✓ **Check** for valid states
- ℹ️ **Info** for informational messages

[... more lines ...]
```

#### ✅ AFTER (in CLAUDE.md):
```markdown
## Code Patterns

**Color coding**: Control (blue), Variant (purple), Warning (yellow)

**Reference**: See [CODING_STANDARDS.md](./CODING_STANDARDS.md) for component guidelines, icon usage, and examples
```

**Savings**: 25 lines removed from CLAUDE.md

---

## After Refactoring

### Final CLAUDE.md Structure (178 lines)

```markdown
# CLAUDE.md

## Project Purpose (15 lines)
Brief description of capacity planner tool

## Tech Stack (10 lines)
- React 19 + Vite + Tailwind v4
- TypeScript
- Recharts

## Critical Warnings (15 lines)
- Tailwind v4 syntax (not v3)
- No PostCSS config needed

## Development Status (20 lines)
Phase tracking with current progress

## Essential Commands (10 lines)
npm run dev, validate, build

## Code Patterns (15 lines)
Brief example + reference to CODING_STANDARDS.md

## Domain Knowledge (10 lines)
Brief summary + reference to STATISTICAL_REFERENCE.md

## Documentation Map (25 lines) ← KEY SECTION
- CODING_STANDARDS.md - Code quality, anti-slop principles
- docs/STATISTICAL_REFERENCE.md - Formulas, calculations
- docs/DEVELOPMENT_GUIDE.md - File structure, workflow
- docs/planning/TASKS.md - Current tasks and progress
- docs/planning/FEATURES_BACKLOG.md - Planned features

## Development Notes (15 lines)
Progressive documentation framework, session workflow

## Quick Reference (20 lines)
Core principles reminder
```

**Total**: 178 lines (exactly back to template baseline!)

---

## Created Documentation Files

### 1. CODING_STANDARDS.md (164 lines extracted)
**Contains**:
- Anti-slop principles (functions <50 lines, nesting <3)
- Code review checklist
- Component guidelines (color coding, icons)
- Error handling philosophy
- Common pitfalls to avoid
- Good vs bad code examples

**Usage**: Referenced during code review, before commits, when adding new patterns

---

### 2. docs/STATISTICAL_REFERENCE.md (67 lines extracted)
**Contains**:
- EPL formula, interpretation, edge cases
- Redirect rate calculations
- Sample size formulas with TypeScript implementation
- Statistical significance thresholds
- Benchmark values for personal loans domain

**Usage**: Referenced when implementing calculations, validating statistical logic

---

### 3. docs/DEVELOPMENT_GUIDE.md (95 lines extracted)
**Contains**:
- Complete project structure (full file tree)
- Typical development workflow
- Understanding core data model
- Component architecture
- Resources and references

**Usage**: Onboarding new developers, understanding project organization

---

## Verification

### Before vs After Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **CLAUDE.md length** | 512 lines | 178 lines | -65% ✅ |
| **Over guidance %** | 156% over | 11% under | Within target ✅ |
| **Longest section** | 89 lines | 25 lines | Within 30-line limit ✅ |
| **Reference links** | 0 | 5 | Modular strategy ✅ |
| **Embedded standards** | 164 lines | 0 lines | Extracted ✅ |
| **Embedded domain** | 67 lines | 0 lines | Extracted ✅ |

### Audit Results

#### Before Refactoring:
```
🔴 CRITICAL: Length Bloat (512 lines)
🔴 Embedded Coding Standards (164 lines)
🔴 Embedded Domain Knowledge (67 lines)
🟡 Missing References (0 links)
```

#### After Refactoring:
```
✅ Length: 178 lines (within target)
✅ Modular strategy: 5 reference links
✅ No embedded standards
✅ No sections exceed 30-line limit
```

---

## Lessons Learned

### What Caused the Bloat?

1. **"Just add it here" mentality**: Every piece of information added to CLAUDE.md without extracting anything
2. **No periodic audits**: File grew from 178 → 512 over time without intervention
3. **Confusion about purpose**: Treated CLAUDE.md as comprehensive manual vs quick reference
4. **Lack of criteria**: No decision framework for "does this belong?"

### What Prevented Bloat in claude-dev-template?

1. **Template awareness**: Knew it would be copied, kept intentionally lean
2. **Limited scope**: Only artifact-porting workflow, not full development
3. **Reference strategy**: Created 4 separate docs (README, QUICK_REF, SETUP, CLAUDE.md)
4. **Protective tone**: Heavy warnings prevented additions

### Key Takeaways

✅ **Do**:
- Create separate docs early (CODING_STANDARDS, DOMAIN_GUIDE, etc.)
- Use "Reference: See [doc]" pattern liberally
- Audit quarterly (run `/audit-claude-md`)
- Apply 30-line section limit strictly

❌ **Don't**:
- Add content without removing/extracting
- Embed long explanations or tutorials
- Skip the "does this belong?" decision tree
- Wait until 500+ lines to refactor

---

## Refactoring Checklist

Use this when refactoring your own bloated CLAUDE.md:

**Step 1: Audit** (5 min)
- [ ] Run `/audit-claude-md`
- [ ] Note violations (length, embedded content, missing references)
- [ ] Identify extractable sections

**Step 2: Plan Extraction** (10 min)
- [ ] Determine which separate docs to create
- [ ] Map content to target docs:
  - Coding standards → CODING_STANDARDS.md
  - Domain knowledge → DOMAIN_GUIDE.md
  - Development guides → DEVELOPMENT_GUIDE.md
  - Setup/installation → SETUP.md or README.md

**Step 3: Create Docs** (5 min)
- [ ] Create target doc files
- [ ] Add headers and structure

**Step 4: Extract Content** (30 min)
- [ ] Copy full content from CLAUDE.md to target doc
- [ ] Replace in CLAUDE.md with 3-line summary + reference
- [ ] Repeat for each violation

**Step 5: Verify** (10 min)
- [ ] Run `/audit-claude-md` again (should be clean)
- [ ] Check CLAUDE.md length (target: 150-200)
- [ ] Test in session: Can Claude find referenced docs?
- [ ] Verify all "Reference: See [doc]" links work

---

**Example completed**: 2025-11-01
**Result**: 512 → 178 lines (65% reduction, 0 information loss)
