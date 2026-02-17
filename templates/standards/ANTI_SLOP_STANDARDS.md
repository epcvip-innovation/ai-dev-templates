# AI-Assisted Code Quality Standards
## Preventing Common AI-Generated Anti-Patterns ("Anti-Slop")

**Purpose**: Measurable, automatable standards for AI-assisted development that operationalize established principles (YAGNI, KISS, Plain Language) with AI-specific patterns, thresholds, and enforcement.

**Last Updated**: 2025-11-02

---

## What This Is

This document provides **concrete, enforceable standards** to prevent common AI-generated code bloat ("slop") that creeps into projects when AI assistants over-engineer solutions.

### Why It's Needed

AI code assistants can generate high-quality code, but also tend to:
- **Over-abstract** - Creating managers for single-use functions
- **Add "kitchen-sink" parameters** - Features "just in case"
- **Produce verbose documentation** - 50% fluff, 50% value

These standards provide:
- ✅ Recognition patterns for AI-generated bloat
- ✅ Automated enforcement via grep/awk
- ✅ Scoring systems for architectural simplicity
- ✅ Proven workflows validated across 8+ projects

### Industry Alignment

This isn't trendy terminology or AI-hype. These standards operationalize proven principles:

- **Plain Language Act (2010)**: Clear, concise communication
- **YAGNI Principle (XP/Agile)**: "You Ain't Gonna Need It" - don't add unneeded features
- **KISS Philosophy (Unix)**: Keep It Simple, Stupid
- **Hamel Husain (2024)**: Anti-slop writing methodology for AI-assisted documentation
- **Google Style Guide**: "Cut unnecessary content, trim like a bonsai tree"

**Connection to Established Standards**:
- Functions <50 lines → **Single Responsibility Principle** (Clean Code, SOLID)
- Nesting <3 levels → **Cyclomatic Complexity** limits (IEEE standards)
- No premature abstraction → **YAGNI** (Extreme Programming, 1999)
- Direct implementation → **KISS** (Unix Philosophy)

---

## Top 7 Universal Standards

These 7 standards are **measurable, automatable, and language-agnostic**. Enforce across all projects:

### 1. Functions Under 50 Lines

**Rule**: Keep functions focused and under 50 lines of code

**Rationale**:
- Violates **Single Responsibility Principle** if longer
- Harder to test, harder to debug
- AI tends to generate 100+ line functions

**Automated Check**:
```bash
# Find functions over 50 lines (Python example)
awk '/^def / {start=NR} /^def |^class / && NR>start {if(NR-start>50) print FILENAME":"start" Function is "NR-start" lines"; start=NR}' **/*.py
```

**Example**:
```python
# ❌ BAD: AI-generated 155-line class
class PingTreeDataFetcherManager:
    def __init__(self, config_manager, cache_manager, logger_factory):
        self.config = config_manager.get_config()
        # ... 150 more lines of abstraction

# ✅ GOOD: 15-line direct implementation
async def fetch_ping_tree_from_athena(tree_id: int):
    """Fetch ping tree campaigns from Athena"""
    try:
        result = await execute_athena_query(query)
        logger.info(f"✅ Fetched {len(result)} campaigns")
        return result
    except Exception as e:
        logger.error(f"❌ Failed: {str(e)}")
        return None
```

---

### 2. Nesting Depth Under 3 Levels

**Rule**: Maximum nesting depth of 3 levels (for/if/while)

**Rationale**:
- Proxy for **cyclomatic complexity**
- Deep nesting = hard to reason about
- AI loves creating nested conditionals

**Automated Check**:
```bash
# Detect deep nesting (4+ levels of indentation)
grep -n "^[[:space:]]\{16,\}" **/*.py  # Python (4 spaces * 4 levels)
grep -n "^[[:space:]]\{8,\}" **/*.js   # JavaScript (2 spaces * 4 levels)
```

**Example**:
```javascript
// ❌ BAD: 4 levels deep
if (user) {
  if (user.isActive) {
    if (user.hasPerm) {
      if (data.valid) {
        // Too deep!
      }
    }
  }
}

// ✅ GOOD: Early returns, <3 levels
if (!user || !user.isActive) return;
if (!user.hasPerm) return;
if (!data.valid) return;
// Proceed with logic
```

---

### 3. SQL Parameterization (No String Interpolation)

**Rule**: Always parameterize SQL queries, never use f-strings or string concatenation

**Rationale**:
- **SQL injection** vulnerability
- AI often generates f-strings by default
- Critical security issue

**Automated Check**:
```bash
# Detect SQL injection risk (Python)
rg 'cursor\.execute.*f"' --type py
rg 'cursor\.execute.*\+' --type py
rg "cursor\.execute.*format\(" --type py
```

**Example**:
```python
# ❌ CRITICAL: SQL injection risk
tree_id = request.args.get('id')
query = f"SELECT * FROM trees WHERE id = {tree_id}"
cursor.execute(query)

# ✅ GOOD: Parameterized query
query = "SELECT * FROM trees WHERE id = ?"
cursor.execute(query, (tree_id,))
```

---

### 4. No Production Console Logging

**Rule**: Remove all `console.log`, `print()` debug statements before merging

**Rationale**:
- Leaks internal data to browser console
- AI adds debug logging everywhere
- Use proper logging libraries

**Automated Check**:
```bash
# Detect production logging
rg "console\.log" --type js --glob "!**/*.test.js"
rg "print\(" --type py --glob "!**/tests/**"
```

**Example**:
```javascript
// ❌ BAD: Debug logging in production
console.log("User data:", userData);  // Leaks PII

// ✅ GOOD: Use logger with levels
logger.debug("User loaded", { userId: userData.id });
```

---

### 5. Emoji Logging (Project Convention)

**Rule**: Use emoji prefixes for log clarity (✅ success, ❌ error, 🔍 search, 📊 data)

**Rationale**:
- Improves log scannability
- Consistent across projects
- AI can learn and replicate

**Not Automated** - Code review check

**Example**:
```python
# ❌ BAD: Generic logging
logger.info("Fetched campaigns for tree 123")
logger.error("Failed to fetch campaigns")

# ✅ GOOD: Emoji logging
logger.info(f"✅ Fetched {len(campaigns)} campaigns for tree {tree_id}")
logger.error(f"❌ Failed to fetch campaigns: {str(e)}")
```

---

### 6. Return None on Error (Graceful Degradation)

**Rule**: Return `None` on error instead of raising exceptions (for non-critical errors)

**Rationale**:
- **Graceful degradation** > crashing
- AI loves throwing exceptions
- Caller decides how to handle

**Not Fully Automated** - Code review check

**Example**:
```python
# ❌ BAD: Exceptions for expected failures
def fetch_data(id):
    if not id:
        raise ValueError("ID required")  # Expected case, not exceptional
    return data

# ✅ GOOD: None for expected failures
def fetch_data(id):
    if not id:
        logger.warning("⚠️ No ID provided")
        return None
    return data
```

---

### 7. No Empty Exception Handlers

**Rule**: Never use `except: pass` or `catch { }` - always log or handle

**Rationale**:
- **Silent failures** are impossible to debug
- AI defaults to blind exception handling when unsure
- Violates error visibility

**Automated Check**:
```bash
# Detect empty catches (Python)
rg "except.*:\s*pass" --type py

# Detect empty catches (JavaScript)
rg "catch.*\{\s*\}" --type js
```

**Example**:
```python
# ❌ CRITICAL: Silent failure
try:
    result = fetch_data(id)
except:
    pass  # What failed? Why? No idea.

# ✅ GOOD: Log and return sentinel
try:
    result = fetch_data(id)
except Exception as e:
    logger.error(f"❌ Failed to fetch: {str(e)}")
    return None
```

---

## 8 AI Over-Engineering Anti-Patterns

These are **recognition patterns** - learn to spot AI-generated bloat and refactor aggressively.

### Pattern 1: Kitchen-Sink Parameters

**Symptom**: Functions with 5+ parameters, many unused

**AI Behavior**: Adds parameters "just in case" for flexibility

**Example**:
```python
# ❌ AI SLOP: Too many options
async def fetch_data(tree_id, retry_count=3, timeout=30,
                     use_cache=True, validate=True,
                     transform=True, log_level="INFO"):
    # 90% of callers use defaults

# ✅ PROJECT-APPROPRIATE: Start simple
async def fetch_data(tree_id: str):
    # Add parameters only when actually needed
```

**Fix**: Start with minimum parameters, add only when 2+ callers need them

---

### Pattern 2: Over-Abstraction

**Symptom**: Classes/wrappers for single-use cases

**AI Behavior**: Creates managers, factories, strategies for simple tasks

**Example**:
```javascript
// ❌ AI SLOP: 50 lines for one button
class ButtonClickManager extends EventManager {
    constructor() {
        super();
        this.initializeHandlers();
    }
    // ... 45 more lines
}

// ✅ PROJECT-APPROPRIATE: Direct implementation
button.addEventListener('click', async () => {
    button.disabled = true;
    await loadData();
    button.disabled = false;
});
```

**Fix**: Use direct implementation first, abstract only when pattern appears 3+ times

---

### Pattern 3: Blind Exception Handling

**Symptom**: `except: pass`, `catch { }`, or generic catches

**AI Behavior**: Catches all exceptions to "be safe"

**Example**:
```python
# ❌ AI SLOP: Blind catch
try:
    process_data()
except:
    pass  # Silent failure

# ✅ PROJECT-APPROPRIATE: Specific + logging
try:
    process_data()
except ValueError as e:
    logger.error(f"❌ Invalid data: {str(e)}")
    return None
```

**Fix**: Catch specific exceptions, log all errors, never silence

---

### Pattern 4: Type Confusion

**Symptom**: Mixing string/int IDs, inconsistent types

**AI Behavior**: Doesn't maintain type consistency across codebase

**Example**:
```python
# ❌ AI SLOP: Inconsistent types
def fetch_tree(tree_id):  # Sometimes int, sometimes str
    query = f"SELECT * FROM trees WHERE id = {tree_id}"  # Breaks if str

# ✅ PROJECT-APPROPRIATE: Enforce types
def fetch_tree(tree_id: int) -> Optional[Dict]:
    """Fetch tree by ID (always int)"""
```

**Fix**: Use type hints, enforce consistency in function signatures

---

### Pattern 5: Copy-Paste Code

**Symptom**: Same logic appears 3+ times

**AI Behavior**: Generates similar code for each use case instead of reusing

**Example**:
```python
# ❌ AI SLOP: Same pattern 3 times
def fetch_campaigns(): ...logic...
def fetch_offers(): ...same logic...
def fetch_affiliates(): ...same logic...

# ✅ PROJECT-APPROPRIATE: Extract to reusable function
def fetch_from_athena(table: str) -> List[Dict]:
    """Generic Athena fetch"""

campaigns = fetch_from_athena("campaigns")
offers = fetch_from_athena("offers")
```

**Fix**: Extract after 2nd occurrence (DRY principle)

---

### Pattern 6: Premature Optimization

**Symptom**: Caching, memoization, complex data structures before measuring

**AI Behavior**: Adds optimization "best practices" without profiling

**Example**:
```python
# ❌ AI SLOP: Premature caching
@lru_cache(maxsize=1000)  # Is this even slow?
def calculate_simple_sum(a, b):
    return a + b

# ✅ PROJECT-APPROPRIATE: Measure first
def calculate_sum(a, b):
    return a + b
# Add caching ONLY if profiling shows bottleneck
```

**Fix**: Profile first, optimize second (don't guess)

---

### Pattern 7: Framework Addiction

**Symptom**: Adding libraries for simple tasks

**AI Behavior**: Suggests frameworks for everything

**Example**:
```javascript
// ❌ AI SLOP: Library for simple task
import { debounce } from 'lodash';  // 70KB for one function

// ✅ PROJECT-APPROPRIATE: Write 5 lines
const debounce = (fn, ms) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
};
```

**Fix**: Write simple utilities yourself, use libraries for complex tasks only

---

### Pattern 8: Comment Novels

**Symptom**: Excessive comments explaining obvious code

**AI Behavior**: Generates docstrings and comments for everything

**Example**:
```python
# ❌ AI SLOP: Comment explaining obvious code
def add_numbers(a, b):
    """
    Add two numbers together.

    Args:
        a (int): The first number to add
        b (int): The second number to add

    Returns:
        int: The sum of a and b

    Example:
        >>> add_numbers(2, 3)
        5
    """
    return a + b  # Return the sum of a and b

# ✅ PROJECT-APPROPRIATE: Comment only non-obvious
def retry_athena_query(query, max_retries=3):
    """Retry up to 3 times for transient Athena timeouts"""
    # Only document WHY, not WHAT
```

**Fix**: Comment the WHY, not the WHAT. Delete obvious comments.

---

## Architectural Simplicity Scoring (1-10)

Use this scoring system in `/plan-approaches` to evaluate architectural options objectively.

### Scoring Criteria

**10/10 - Perfect Simplicity**:
- ✅ Direct implementation (no abstractions)
- ✅ Functions <30 lines
- ✅ Zero dependencies added
- ✅ Single responsibility per function
- ✅ No nesting >2 levels

**7-9/10 - Good Simplicity**:
- ✅ Minimal abstraction (only where pattern repeats 3+ times)
- ✅ Functions <50 lines
- ✅ Standard library only (no new deps)
- ⚠️ Some nesting (3 levels max)

**4-6/10 - Acceptable Complexity**:
- ⚠️ Moderate abstraction (base classes, interfaces)
- ⚠️ Functions <100 lines
- ⚠️ 1-2 small dependencies added
- ⚠️ Some deep nesting (4 levels)

**1-3/10 - Over-Engineered (Reject)**:
- ❌ Heavy abstraction (managers, factories, strategies)
- ❌ Functions >100 lines
- ❌ 3+ new dependencies
- ❌ Deep nesting (5+ levels)
- ❌ Premature optimization

### Example Scoring (React State Management)

**Approach 1: Individual useState (10/10 anti-slop)**
- Direct implementation ✅
- No abstraction ✅
- Zero dependencies ✅
- 5 lines per state ✅

**Approach 2: useReducer (8/10 anti-slop)**
- Standard pattern ✅
- Some abstraction (action types) ⚠️
- No dependencies ✅
- 30 lines total ✅

**Approach 3: Zustand (6/10 anti-slop)**
- External library ⚠️
- Global state (may be overkill) ⚠️
- 1 dependency added ⚠️
- 50 lines total ⚠️

**Approach 4: Redux Toolkit (3/10 anti-slop - REJECT)**
- Heavy framework ❌
- 5 new dependencies ❌
- 200+ lines boilerplate ❌
- Over-engineered for simple app ❌

**Recommendation**: Select Approach 1 (10/10) for simple apps, Approach 2 (8/10) if state logic is complex.

---

## Automation & Enforcement

### Pre-Commit Quality Gates

Create `.git/hooks/pre-commit` for automated checks:

```bash
#!/bin/bash
# Anti-Slop Quality Gates

echo "🔍 Running anti-slop checks..."

# 1. Check for SQL injection risk
if rg 'cursor\.execute.*f"' --type py --quiet; then
  echo "❌ SQL injection risk detected (f-strings in execute)"
  exit 1
fi

# 2. Check for console.log in production
if rg "console\.log" --type js --glob "!**/*.test.js" --quiet; then
  echo "❌ console.log found in production code"
  exit 1
fi

# 3. Check for empty exception handlers
if rg "except.*:\s*pass" --type py --quiet; then
  echo "❌ Empty exception handler detected"
  exit 1
fi

# 4. Check CLAUDE.md length
if [ -f "CLAUDE.md" ]; then
  LINES=$(wc -l < CLAUDE.md)
  if [ $LINES -gt 250 ]; then
    echo "❌ CLAUDE.md is $LINES lines (max 250). Run /audit-claude-md"
    exit 1
  fi
fi

echo "✅ All anti-slop checks passed"
```

### Grep Pattern Reference

**Quick reference for manual checks**:

```bash
# SQL Injection
rg 'cursor\.execute.*f"' --type py
rg "execute.*format\(" --type py

# Production Logging
rg "console\.log" --glob "!**/*.test.js"
rg "print\(" --glob "!**/tests/**"

# Empty Catches
rg "except.*:\s*pass" --type py
rg "catch.*\{\s*\}" --type js

# Long Functions (Python, 50+ lines)
awk '/^def / {start=NR} /^def |^class / && NR>start {if(NR-start>50) print FILENAME":"start; start=NR}' **/*.py

# Deep Nesting (4+ levels)
grep -n "^[[:space:]]\{16,\}" **/*.py  # Python
grep -n "^[[:space:]]\{8,\}" **/*.js   # JavaScript
```

---

## Integration with Development Workflows

### 1. `/plan-approaches` Command

**When evaluating architectural options**, score each approach 1-10 on anti-slop compliance:

```markdown
## Approach 1: Individual useState
**Anti-Slop Score**: 10/10
- Direct implementation ✅
- Zero abstractions ✅
- Functions <30 lines ✅

## Approach 2: useReducer
**Anti-Slop Score**: 8/10
- Minimal abstraction ⚠️
- Standard pattern ✅
- Functions <50 lines ✅
```

**Selection rationale**: Choose highest anti-slop score unless complexity genuinely requires lower score.

### 2. `/audit-claude-md` Command

**CLAUDE.md bloat is a form of slop**. Run quarterly:

```bash
/audit-claude-md
```

Checks for:
- Length >250 lines (should be 150-200)
- Embedded standards (should be separate docs)
- Missing references (should link to detailed docs)

### 3. Code Review Checklist

**Before accepting ANY AI-generated code**:

- [ ] Functions <50 lines?
- [ ] Nesting <3 levels?
- [ ] SQL parameterized?
- [ ] No console.log in production?
- [ ] No empty exception handlers?
- [ ] No unnecessary abstractions?
- [ ] No "just in case" parameters?
- [ ] Comments explain WHY not WHAT?

---

## Evidence & Validation

These standards are **validated across real projects**, not theoretical:

### Real Refactoring Examples

**Example 1: ping-tree-compare CODING_STANDARDS.md**
- **Before**: AI generated 155-line `PingTreeDataFetcherManager` class
- **After**: Refactored to 15-line `fetch_ping_tree_from_athena()` function
- **Reduction**: 90% less code, same functionality

**Example 2: dois-test-capacity-planner CLAUDE.md**
- **Before**: 512 lines with embedded standards and domain knowledge
- **After**: 178 lines (extracted to separate docs)
- **Reduction**: 65% bloat removed

**Example 3: `/plan-approaches` scoring validation**
- **dois-test-capacity-planner**: Selected "Individual useState" (10/10 anti-slop) over Redux (3/10)
- **Result**: Simpler codebase, easier to maintain, no added dependencies

### Measurable Impact

| Metric | Before Anti-Slop | After Anti-Slop | Improvement |
|--------|-----------------|----------------|-------------|
| CLAUDE.md Length | 512 lines | 178 lines | 65% reduction |
| Function Length | 155 lines | 15 lines | 90% reduction |
| Dependencies Added | 5 (Redux) | 0 (useState) | 100% reduction |
| Abstraction Layers | 3 (Manager/Factory) | 1 (Direct) | 67% reduction |

---

## FAQ: Addressing Skepticism

### Q: Isn't this just YAGNI/KISS rebranded?

**A**: Yes and no. The **principles** are established (YAGNI, KISS, Plain Language), but:
- ✅ AI-specific recognition patterns (AI slop behaviors)
- ✅ Automated enforcement (grep patterns, scoring)
- ✅ Concrete thresholds tuned for AI collaboration (50 lines, not Clean Code's 20)
- ✅ Integration with workflows (`/plan-approaches` scoring)

Traditional standards say "be simple" - these standards provide **measurable criteria** and **automation**.

### Q: Why new terminology ("anti-slop") if it's established principles?

**A**: "Anti-slop" is emerging terminology (2024-2025, Hamel Husain) for AI-era development. We use it because:
- Recognizable in AI-assisted coding communities
- Captures AI-specific behaviors (kitchen-sink, over-abstraction)
- Bridges to established terms (YAGNI, KISS)

**Primary branding**: "AI-Assisted Code Quality Standards"
**Secondary label**: "Anti-slop (YAGNI/simplicity-first)"

### Q: Won't AI improve and make this obsolete?

**A**: The underlying principles (simplicity, clarity) are **timeless**. Even if AI improves:
- Human tendency to accept AI output uncritically won't change
- Documentation bloat is a human problem (CLAUDE.md grew from 178 → 512 over time)
- YAGNI and KISS have been relevant since 1999 - won't become obsolete

These standards **adapt** timeless principles for AI collaboration.

### Q: Isn't 50 lines per function too permissive?

**A**: It's a **practical threshold** for AI collaboration:
- Clean Code (Robert Martin) suggests <20 lines (ideal for human-written code)
- AI tends to generate 100+ line functions
- 50 lines is a **compromise** - tighter than AI default, looser than Clean Code ideal
- Enforces Single Responsibility without being dogmatic

**Adjust per project**: Stricter projects can use 30, looser projects can use 75.

---

## Summary: The Anti-Slop Philosophy

**Core Principle**: AI is a powerful tool, but it needs guardrails to prevent over-engineering.

**Mental Model**:
- AI generates code **quickly** ✅
- AI tends to generate code **verbosely** ❌
- Anti-slop standards **trim the excess** ✅

**Three Questions Before Accepting AI Code**:
1. **Simplicity**: Could this be 50% shorter with same functionality?
2. **Necessity**: Are all these abstractions/parameters actually needed?
3. **Measurability**: Does this pass the 7 universal standards?

**If any answer is "yes" to #1, "no" to #2, or "no" to #3**: Refactor before merging.

---

## Quick Reference Card

### 7 Universal Standards (Automated)

1. ✅ Functions <50 lines
2. ✅ Nesting <3 levels
3. ✅ SQL parameterized
4. ✅ No console.log in prod
5. ⚠️ Emoji logging (convention)
6. ⚠️ Return None on error
7. ✅ No empty catches

### 8 AI Anti-Patterns (Recognition)

1. Kitchen-sink parameters
2. Over-abstraction
3. Blind exception handling
4. Type confusion
5. Copy-paste code
6. Premature optimization
7. Framework addiction
8. Comment novels

### Scoring (1-10)

- **10/10**: Direct, <30 lines, zero deps, no abstraction
- **7-9/10**: Minimal abstraction, <50 lines, standard lib only
- **4-6/10**: Moderate complexity, <100 lines, 1-2 deps
- **1-3/10**: Over-engineered, >100 lines, heavy abstraction (REJECT)

---

**Maintained**: 2025-11-02
**Next Review**: 2026-05-16 (quarterly)
