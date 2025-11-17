# Anti-Slop Standards Template

[← Back to Main README](../../README.md)

**Purpose**: Prevent AI-generated code bloat by applying measurable, automatable quality standards

**Template**: `ANTI_SLOP_STANDARDS.md`

---

## Quick Start

### For New Projects

```bash
# Copy template to project root
cp templates/standards/ANTI_SLOP_STANDARDS.md your-project/

# Optional: Create language-specific standards
cp templates/standards/ANTI_SLOP_STANDARDS.md your-project/CODING_STANDARDS.md

# Customize for your project:
# 1. Adjust function line limits (default: 50, can use 30-75)
# 2. Add language-specific grep patterns
# 3. Remove irrelevant anti-patterns
# 4. Add project-specific conventions
```

### For Existing Projects

If you already have `CODING_STANDARDS.md`:
- **Option A**: Replace with ANTI_SLOP_STANDARDS.md (if current file is generic)
- **Option B**: Extract anti-slop section, keep language-specific rules separate
- **Option C**: Reference ANTI_SLOP_STANDARDS.md from existing CODING_STANDARDS.md

---

## The Problem This Solves

### Before Anti-Slop Standards

**Scattered quality practices**:
- "Write clean code" (generic, unmeasurable)
- Code reviews catch issues too late
- AI generates verbose code, humans accept it
- No objective criteria for simplicity
- Technical debt accumulates invisibly

**Result**: Bloated codebases, 155-line functions, over-engineered abstractions

### After Anti-Slop Standards

**Measurable quality gates**:
- 7 universal standards with grep patterns
- Automated pre-commit checks
- Objective architectural scoring (1-10)
- Recognition patterns for AI slop
- Refactoring before merging, not after shipping

**Result**: 90% code reductions, simpler architecture, faster iteration

---

## Where It Fits in Workflow

```
┌─────────────────────────────────────────────────────────┐
│ PLANNING PHASE                                          │
│                                                         │
│ /plan-approaches                                        │
│   ├─ Evaluates 3 architectural options                │
│   ├─ Scores each on anti-slop compliance (1-10)       │
│   └─ Selects simplest viable approach                 │
│       (10/10 direct implementation > 6/10 framework)   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ IMPLEMENTATION                                          │
│                                                         │
│ AI generates code                                       │
│   ├─ Developer applies anti-slop filters:             │
│   │   - Delete 50% of verbose output                  │
│   │   - Check 7 universal standards                   │
│   │   - Recognize 8 AI anti-patterns                  │
│   └─ Refactor before committing                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ PRE-COMMIT                                              │
│                                                         │
│ Automated Quality Gates                                │
│   ├─ Grep: SQL injection risk?                        │
│   ├─ Grep: console.log in production?                 │
│   ├─ Grep: Empty exception handlers?                  │
│   ├─ AWK: Functions >50 lines?                        │
│   └─ PASS ✅ / FAIL ❌                                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ CODE REVIEW                                             │
│                                                         │
│ Manual Anti-Slop Checks                                │
│   ├─ Nesting <3 levels?                               │
│   ├─ No kitchen-sink parameters?                      │
│   ├─ No unnecessary abstractions?                     │
│   └─ Approve if all checks pass                       │
└─────────────────────────────────────────────────────────┘
```

**Key insight**: Anti-slop standards operate at **three intervention points**:
1. **Planning** - Choose simple architectures via scoring
2. **Implementation** - Refactor AI output before committing
3. **Automation** - Block common issues at pre-commit

---

## Template Structure Explained

### Section 1: Overview (Lines 1-50)

**What it is**: Introduction, rationale, industry alignment

**Key sections**:
- **Why It's Needed** - Explains AI tendency to over-engineer
- **Industry Alignment** - Connects to YAGNI, KISS, Plain Language, Hamel Husain
- **What It Provides** - Recognition patterns, automation, scoring

**Customization**: None needed - use as-is

---

### Section 2: Top 7 Universal Standards (Lines 51-300)

**What it is**: Measurable, automatable quality gates with grep patterns

**Standards**:
1. Functions <50 lines (Single Responsibility Principle)
2. Nesting <3 levels (Cyclomatic Complexity)
3. SQL parameterization (Security)
4. No console.log in production (Data leakage)
5. Emoji logging (Readability convention)
6. Return None on error (Graceful degradation)
7. No empty exception handlers (Error visibility)

**Customization**:
- **Adjust line limits**: Change 50 → 30 (stricter) or 75 (looser) based on team
- **Add language-specific patterns**: Include Go, Rust, Java equivalents
- **Remove irrelevant standards**: If no SQL, skip #3
- **Add project conventions**: Include project-specific patterns

**Example customization** (stricter Python project):
```markdown
### 1. Functions Under 30 Lines (Stricter)

**Rule**: Keep functions focused and under 30 lines of code

**Automated Check**:
```bash
# Find functions over 30 lines (Python)
awk '/^def / {start=NR} /^def |^class / && NR>start {if(NR-start>30) print FILENAME":"start" Function is "NR-start" lines"; start=NR}' **/*.py
```
```

---

### Section 3: 8 AI Over-Engineering Anti-Patterns (Lines 301-500)

**What it is**: Recognition training for AI-generated bloat

**Patterns**:
1. Kitchen-sink parameters (5+ args)
2. Over-abstraction (managers for single-use)
3. Blind exception handling (except: pass)
4. Type confusion (mixing str/int)
5. Copy-paste code (3+ occurrences)
6. Premature optimization (caching before profiling)
7. Framework addiction (libraries for simple tasks)
8. Comment novels (explaining obvious code)

**Customization**:
- **Add project-specific anti-patterns**: If AI generates specific bloat, document it
- **Include before/after examples**: Use real refactorings from your codebase
- **Remove irrelevant patterns**: If you use Redux legitimately, skip #7

**Example addition** (project-specific):
```markdown
### Pattern 9: Over-Typing (Project Anti-Pattern)

**Symptom**: Type hints for every internal function

**AI Behavior**: Adds type hints everywhere, even private helpers

**Example**:
```python
# ❌ AI SLOP: Over-typed private helper
def _format_date(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d")

# ✅ PROJECT-APPROPRIATE: Type hints on public API only
def get_report(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    def _format_date(date):  # Private helper, no types needed
        return date.strftime("%Y-%m-%d")
```
```

---

### Section 4: Architectural Simplicity Scoring (Lines 501-600)

**What it is**: 1-10 scoring system for `/plan-approaches` workflow

**Scoring criteria**:
- **10/10**: Direct, <30 lines, zero deps, no abstraction
- **7-9/10**: Minimal abstraction, <50 lines, stdlib only
- **4-6/10**: Moderate complexity, <100 lines, 1-2 deps
- **1-3/10**: Over-engineered (reject)

**Customization**:
- **Adjust thresholds**: Stricter projects can reject 4-6/10 approaches
- **Add domain-specific criteria**: Include performance, security, maintainability weights
- **Include scoring examples**: Add real architectural decisions from your project

**Example addition** (security-critical project):
```markdown
### Scoring Adjustments for Security-Critical Code

**Modified Criteria**:
- **10/10**: All of standard + security audit passed
- **7-9/10**: All of standard + no new attack surface
- **4-6/10**: Moderate complexity + security review required
- **1-3/10**: Reject if introduces security risk
```

---

### Section 5: Automation & Enforcement (Lines 601-700)

**What it is**: Pre-commit hooks and grep patterns for automated checks

**Includes**:
- Pre-commit hook script
- Grep pattern reference card
- Manual check guidelines

**Customization**:
- **Add language-specific checks**: Include Go, Rust, Java patterns
- **Adjust CLAUDE.md limit**: Change 250 → 200 (stricter) or 300 (looser)
- **Add project tools**: Include linters, formatters, static analyzers

**Example addition** (Go project):
```bash
# Check for SQL injection risk (Go)
rg 'db\.Exec.*fmt\.Sprintf' --type go

# Check for error shadowing (Go)
rg 'if err :=' --type go  # Manual review needed

# Check for goroutine leaks (Go)
rg 'go func\(' --type go  # Ensure proper cleanup
```

---

### Section 6: Integration with Workflows (Lines 701-800)

**What it is**: How anti-slop standards integrate with slash commands and code review

**Sections**:
1. `/plan-approaches` integration (scoring)
2. `/audit-claude-md` integration (CLAUDE.md bloat)
3. Code review checklist

**Customization**:
- **Add project-specific workflows**: Include deployment checks, testing requirements
- **Reference other commands**: Link to `/ai-review`, `/feature-complete`, etc.
- **Include team agreements**: Document code review expectations

---

### Section 7: Evidence & Validation (Lines 801-900)

**What it is**: Real refactoring examples proving standards work

**Includes**:
- Refactoring case studies (155 → 15 lines, 512 → 178 lines)
- Measurable impact table
- Validation across projects

**Customization**:
- **Replace with your examples**: Use real refactorings from your codebase
- **Add metrics**: Track function length, dependency count, CLAUDE.md size over time
- **Include team feedback**: Quote developers on impact

**Example addition** (your project):
```markdown
### Real Refactoring: Feature X Simplification

**Before (AI-generated)**:
- 8 files, 450 lines total
- 3 abstractions (Manager, Factory, Strategy)
- 2 new dependencies (lodash, moment)

**After (anti-slop refactor)**:
- 3 files, 120 lines total
- 1 direct implementation
- 0 new dependencies (used Date API, simple utilities)

**Impact**:
- 73% code reduction
- 50% faster onboarding for new devs
- Zero bugs introduced (simpler = fewer edge cases)
```

---

### Section 8: FAQ (Lines 901-1000)

**What it is**: Addresses skepticism and common questions

**Questions**:
1. Isn't this just YAGNI/KISS rebranded?
2. Why new terminology ("anti-slop")?
3. Won't AI improve and make this obsolete?
4. Isn't 50 lines per function too permissive?

**Customization**:
- **Add team-specific FAQs**: Answer questions your team will ask
- **Include adoption stories**: How other teams successfully used anti-slop
- **Address resistance**: Tackle "this is overkill" or "we don't have time" objections

**Example addition**:
```markdown
### Q: We already have linters. Why do we need anti-slop standards?

**A**: Linters catch **syntax and style** (formatting, naming). Anti-slop catches **architecture and design** (over-abstraction, unnecessary complexity).

**Linter** catches: Unused imports, inconsistent spacing, missing semicolons
**Anti-slop** catches: 155-line manager classes, 5-parameter kitchen-sink functions, premature abstractions

**Both are needed** - linters for code style, anti-slop for code design.
```

---

## Adoption Strategies

### Strategy A: Full Adoption (Recommended for New Projects)

**Steps**:
1. Copy `ANTI_SLOP_STANDARDS.md` to project root
2. Set up pre-commit hooks (automation section)
3. Update `/plan-approaches` to include scoring
4. Add to code review checklist
5. Run `/audit-claude-md` quarterly

**Timeline**: 1 hour setup, ongoing enforcement

**Best for**: New projects, greenfield development, solo developers

---

### Strategy B: Gradual Adoption (Recommended for Existing Projects)

**Phase 1: Documentation (Week 1)**
- Copy template to project
- Customize for your stack (Python/JS/Go)
- Add to project documentation

**Phase 2: Planning Integration (Week 2)**
- Update `/plan-approaches` with scoring
- Use scoring for new features only
- Don't refactor existing code yet

**Phase 3: Automated Checks (Week 3-4)**
- Add 1-2 grep patterns to pre-commit
- Start with critical checks (SQL injection, empty catches)
- Gradually add more checks

**Phase 4: Code Review (Week 5+)**
- Add anti-slop checklist to reviews
- Apply to new code only
- Refactor existing code opportunistically

**Timeline**: 5 weeks to full adoption

**Best for**: Existing codebases, team projects, need buy-in

---

### Strategy C: Minimal Adoption (Low-Overhead)

**What to adopt**:
1. ✅ Keep template as reference (don't customize)
2. ✅ Use 1-10 scoring in `/plan-approaches` (evaluate options)
3. ✅ Run 3 critical grep checks manually before merging:
   - SQL injection (`rg 'execute.*f"'`)
   - Empty catches (`rg "except.*:\s*pass"`)
   - Production logging (`rg "console\.log"`)
4. ⏭️ Skip pre-commit hooks (manual checks only)
5. ⏭️ Skip code review checklist (use judgment)

**Timeline**: 10 minutes setup, 5 minutes per review

**Best for**: Solo projects, prototypes, time-constrained teams

---

## Language-Specific Customization

### Python Projects

**Add to template**:
```markdown
### Python-Specific Standards

**9. Use Type Hints on Public APIs**
- Required for all public functions/classes
- Optional for private helpers (underscore prefix)
- Use `mypy --strict` for validation

**10. Avoid Mutable Default Arguments**
```python
# ❌ BAD: Mutable default
def add_item(item, items=[]):
    items.append(item)

# ✅ GOOD: None default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
```

**Automated Checks**:
```bash
# Check for mutable defaults
rg "def .*\(.*=\[\]" --type py
rg "def .*\(.*=\{\}" --type py
```
```

---

### TypeScript Projects

**Add to template**:
```markdown
### TypeScript-Specific Standards

**9. Use `unknown` Over `any`**
- `any` bypasses type checking (dangerous)
- `unknown` forces type checking before use

**10. No Non-Null Assertions (!)**
```typescript
// ❌ BAD: Non-null assertion
const user = users.find(u => u.id === id)!;

// ✅ GOOD: Explicit check
const user = users.find(u => u.id === id);
if (!user) return;
```

**Automated Checks**:
```bash
# Detect any usage
rg ": any" --type ts --glob "!**/*.test.ts"

# Detect non-null assertions
rg "!" --type ts | rg -v "!=="
```
```

---

### Go Projects

**Add to template**:
```markdown
### Go-Specific Standards

**9. Always Check Errors**
- Never ignore `err` return values
- Use explicit error handling

**10. No Goroutine Leaks**
```go
// ❌ BAD: Goroutine leak (no way to stop)
go func() {
    for {
        doWork()
    }
}()

// ✅ GOOD: Cancellable goroutine
ctx, cancel := context.WithCancel(context.Background())
defer cancel()
go func() {
    for {
        select {
        case <-ctx.Done():
            return
        default:
            doWork()
        }
    }
}()
```

**Automated Checks**:
```bash
# Detect ignored errors
rg "_, _ = " --type go  # Double ignore
rg "_ = .*Error" --type go  # Ignored error

# Detect potential goroutine leaks
rg "go func\(" --type go  # Manual review needed
```
```

---

## Integration with Existing Standards

### Scenario 1: You Have `CODING_STANDARDS.md` (Language-Specific)

**Recommendation**: Keep both, reference anti-slop

**In `CODING_STANDARDS.md`**, add:
```markdown
## Anti-Slop Principles

We follow universal anti-slop standards to prevent AI-generated code bloat.

**Reference**: See [ANTI_SLOP_STANDARDS.md](./ANTI_SLOP_STANDARDS.md) for:
- 7 universal standards with grep patterns
- 8 AI over-engineering anti-patterns
- Architectural simplicity scoring (1-10)

This file (`CODING_STANDARDS.md`) contains Python-specific style rules (formatting, naming, imports).
```

**Separation**:
- **ANTI_SLOP_STANDARDS.md**: Universal, language-agnostic, AI-specific
- **CODING_STANDARDS.md**: Language-specific style (linting, formatting, naming)

---

### Scenario 2: You Have General "Best Practices" Doc

**Recommendation**: Replace with ANTI_SLOP_STANDARDS.md

**Why**:
- Generic "best practices" are unmeasurable ("write clean code")
- ANTI_SLOP provides concrete, automatable standards
- Better fit for AI-assisted development

**Migration**:
1. Copy any project-specific rules from old doc
2. Add to ANTI_SLOP_STANDARDS.md as Pattern #9, #10, etc.
3. Delete old "best practices" doc

---

### Scenario 3: You Have Nothing (New Project)

**Recommendation**: Start with ANTI_SLOP_STANDARDS.md only

**Why**:
- Covers 90% of quality issues
- Automated enforcement
- Language-agnostic (works for Python, JS, Go, Rust)

**Add language-specific standards later** when patterns emerge (after 3-6 months).

---

## Maintenance Best Practices

### Quarterly Review (Every 3 Months)

**Actions**:
1. **Run automated checks on entire codebase**:
   ```bash
   # Check compliance with all 7 standards
   ./scripts/run-anti-slop-checks.sh
   ```

2. **Review new AI anti-patterns**:
   - Has AI generated new slop not covered by existing patterns?
   - Add as Pattern #9, #10, etc.

3. **Update thresholds if needed**:
   - Are functions consistently >50 lines? (Maybe 50 → 40)
   - Are standards too strict? (Maybe 30 → 50)

4. **Check adoption**:
   - Are pre-commit hooks still running?
   - Is `/plan-approaches` scoring still used?
   - Any team pushback? Address concerns.

---

### When to Update Template

**Triggers**:
- ✅ New language added to project (add language-specific standards)
- ✅ New AI anti-pattern observed 3+ times (add to pattern list)
- ✅ Team feedback suggests threshold adjustment (change line limits)
- ✅ New automation available (add to pre-commit hooks)
- ❌ Don't update for one-off issues (wait for patterns)

---

### Keeping It Lean

**Anti-pattern**: ANTI_SLOP_STANDARDS.md itself becomes bloated (500+ lines)

**Prevention**:
1. **Keep core template under 400 lines**
2. **Extract language-specific standards** to separate files:
   - `ANTI_SLOP_STANDARDS_PYTHON.md`
   - `ANTI_SLOP_STANDARDS_TYPESCRIPT.md`
3. **Reference, don't embed** - link to external resources (Hamel Husain, Google Style Guide)
4. **Delete stale content** - remove anti-patterns that no longer occur

---

## Troubleshooting

### Issue 1: Pre-Commit Hooks Failing on Legacy Code

**Problem**: Existing codebase violates anti-slop standards, blocking all commits

**Solutions**:

**Option A: Grandfather Existing Code** (Recommended)
```bash
# Only check changed files, not entire codebase
git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | xargs rg 'execute.*f"'
```

**Option B: Temporarily Disable Checks**
```bash
# Skip hooks for legacy refactor commits
git commit --no-verify -m "Refactor: legacy code"
```

**Option C: Incremental Adoption**
- Add only 1-2 critical checks (SQL injection, empty catches)
- Gradually add more checks as codebase improves

---

### Issue 2: Team Pushback ("This is Overkill")

**Problem**: Developers feel anti-slop standards slow them down

**Responses**:

**A. Show Evidence**
- Share refactoring examples (155 → 15 lines)
- Calculate time saved (simpler code = faster debugging)
- Demonstrate automation (pre-commit catches issues in seconds vs hours in review)

**B. Simplify Adoption**
- Start with Strategy C (minimal adoption)
- Focus on 3 critical checks only
- Skip pre-commit hooks, use manual checks

**C. Address Specific Concerns**
- "Too many standards" → Focus on Top 3 (functions <50, SQL parameterization, no empty catches)
- "Slows me down" → Automate with pre-commit hooks (catches in 2 seconds)
- "My code is already good" → Show AI-generated bloat examples from codebase

---

### Issue 3: Standards Don't Match Project Needs

**Problem**: Function limit (50 lines) too strict/loose for your project

**Solutions**:

**Adjust Thresholds**:
- **Stricter** (30 lines): Microservices, critical code, high-churn codebases
- **Standard** (50 lines): Most projects, balanced approach
- **Looser** (75 lines): Legacy refactors, complex algorithms, tolerance for larger functions

**Update Template**:
```markdown
### 1. Functions Under 30 Lines (Strict)

**Rule**: Keep functions focused and under 30 lines (stricter than standard 50)

**Rationale**: This is a high-churn microservice with 10+ contributors. Smaller functions reduce merge conflicts and improve testability.
```

---

## Examples by Project Type

### Example 1: Solo Developer, Greenfield Project

**Adoption**:
- ✅ Copy ANTI_SLOP_STANDARDS.md to root
- ✅ Set up pre-commit hooks (all 7 checks)
- ✅ Use `/plan-approaches` scoring
- ⏭️ Skip code review checklist (solo developer)

**Customization**:
- None needed - use template as-is

**Timeline**: 30 minutes setup

---

### Example 2: Team of 5, Existing Codebase

**Adoption**:
- ✅ Copy template, customize for Python
- ⚠️ Gradual adoption (Strategy B)
  - Week 1: Documentation only
  - Week 2: `/plan-approaches` scoring
  - Week 3: Add 3 critical grep checks
  - Week 4: Add to code review checklist
  - Week 5+: Refactor existing code opportunistically
- ✅ Add to team standards doc

**Customization**:
- Add Python-specific standards (type hints, mutable defaults)
- Adjust function limit to 30 lines (strict)
- Add team-specific anti-patterns

**Timeline**: 5 weeks to full adoption

---

### Example 3: Large Team (10+), Enterprise Codebase

**Adoption**:
- ✅ Copy template, customize for Go + Python
- ✅ Minimal adoption (Strategy C) for first quarter
- ⚠️ Full automation after validation
- ✅ Include in onboarding docs

**Customization**:
- Extract language-specific standards to separate files
- Add security-critical scoring adjustments
- Include compliance requirements (SOC2, PCI)

**Timeline**: 3 months to full adoption

---

## Success Metrics

**How to measure anti-slop standard effectiveness**:

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Average Function Length | `tokei --files` or custom script | <50 lines |
| CLAUDE.md Size | `wc -l CLAUDE.md` | 150-200 lines |
| Dependency Count | `package.json`, `requirements.txt` | Trend downward |
| Code Review Time | Track PR review duration | 20% reduction |
| Bugs in New Code | Track bug reports per feature | 30% reduction |
| Onboarding Time | New dev productivity | 15% faster |

**Quarterly Report Template**:
```markdown
## Q1 2025 Anti-Slop Impact Report

**Metrics**:
- Average function length: 45 lines (target: <50) ✅
- CLAUDE.md size: 178 lines (target: 150-200) ✅
- New dependencies added: 0 (trend: downward) ✅
- Code review time: 2.3hrs avg (down from 2.8hrs) ✅

**Refactoring Examples**:
- Feature X: 450 → 120 lines (73% reduction)
- Module Y: 8 files → 3 files (63% reduction)

**Team Feedback**:
- "Pre-commit hooks catch issues before code review" - Dev A
- "Scoring helps justify simple architectures to stakeholders" - Dev B
```

---

## FAQ: Template Usage

### Q: Do I need both ANTI_SLOP_STANDARDS.md and CODING_STANDARDS.md?

**A**: Depends on project:

| If You Have... | Recommendation |
|----------------|----------------|
| Nothing | Start with ANTI_SLOP_STANDARDS.md only |
| Generic "best practices" | Replace with ANTI_SLOP_STANDARDS.md |
| Language-specific style guide | Keep both, reference anti-slop from style guide |
| Multiple languages | ANTI_SLOP (universal) + CODING_STANDARDS_PYTHON.md, CODING_STANDARDS_GO.md |

---

### Q: Should anti-slop standards go in CLAUDE.md?

**A**: **NO** - Keep CLAUDE.md lightweight (150-200 lines).

**Instead**:
```markdown
<!-- In CLAUDE.md -->
## Code Quality Standards

We follow anti-slop principles: functions <50 lines, nesting <3, no premature optimization.

**Reference**: See [ANTI_SLOP_STANDARDS.md](./ANTI_SLOP_STANDARDS.md) for complete guidelines with grep patterns
```

**Why**:
- ANTI_SLOP_STANDARDS.md is 400+ lines (too long for CLAUDE.md)
- CLAUDE.md is prepended to every prompt (wasted context)
- Claude can read both files, no need to embed

---

### Q: How do I convince my team to adopt this?

**A**: Three approaches:

**1. Show Evidence** (Most Effective)
- Share refactoring examples from template (155 → 15 lines)
- Run grep checks on codebase, show violations
- Calculate ROI (time saved, bugs prevented)

**2. Start Small** (Low Resistance)
- Adopt only 3 critical checks (SQL, empty catches, console.log)
- Skip pre-commit hooks, use manual checks
- Add more after team sees value

**3. Make It Optional** (Compromise)
- Use for new features only (don't refactor existing code)
- Apply to high-risk code only (security, performance critical)
- Let team opt-in as they see value

---

### Q: What if AI models improve and stop generating slop?

**A**: The underlying principles remain valuable:

- **YAGNI** has been relevant since 1999 (25+ years)
- **KISS** has been relevant since Unix Philosophy (50+ years)
- **Plain Language** has been federal law since 2010

Even if AI improves:
- Human tendency to accept AI output uncritically won't change
- Documentation bloat is a human problem (CLAUDE.md grows from 178 → 512 over time)
- Simplicity is timeless (over-engineering predates AI)

**Anti-slop standards adapt timeless principles for AI collaboration**. They won't become obsolete.

---

**Last Updated**: 2025-11-02
**Maintained By**: dev-setup template library
