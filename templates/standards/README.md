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

# Customize for your project:
# 1. Adjust function line limits (default: 50, can use 30-75)
# 2. Add language-specific grep patterns
# 3. Remove irrelevant anti-patterns
# 4. Add project-specific conventions
```

### For Existing Projects

| If You Have... | Recommendation |
|----------------|----------------|
| Nothing | Start with ANTI_SLOP_STANDARDS.md only |
| Generic "best practices" | Replace with ANTI_SLOP_STANDARDS.md |
| Language-specific style guide | Keep both, reference anti-slop from style guide |
| Multiple languages | ANTI_SLOP (universal) + per-language CODING_STANDARDS |

---

## The Problem This Solves

**Before**: "Write clean code" (generic, unmeasurable). AI generates verbose code, humans accept it. Result: 155-line functions, over-engineered abstractions.

**After**: 7 universal standards with grep patterns, automated pre-commit checks, objective scoring (1-10). Result: 90% code reductions, simpler architecture, faster iteration.

---

## Where It Fits in Workflow

Anti-slop standards operate at **three intervention points**:

1. **Planning** — `/plan-approaches` scores architectural options on anti-slop compliance (1-10)
2. **Implementation** — Developer applies anti-slop filters: delete 50% of verbose AI output, check 7 standards, recognize 8 anti-patterns
3. **Automation** — Pre-commit hooks block common issues (SQL injection, empty catches, console.log)

---

## Template Contents

The template (`ANTI_SLOP_STANDARDS.md`) contains 8 sections. Read it directly for the full content — this README covers when and how to customize.

| Section | What It Contains | Customization |
|---------|-----------------|---------------|
| **1. Overview** | Rationale, industry alignment (YAGNI, KISS) | Use as-is |
| **2. Top 7 Standards** | Measurable quality gates with grep patterns | Adjust line limits (30-75), add language-specific patterns |
| **3. 8 Anti-Patterns** | Recognition training for AI-generated bloat | Add project-specific anti-patterns from real refactorings |
| **4. Scoring** | 1-10 scale for `/plan-approaches` | Adjust thresholds; add domain-specific criteria |
| **5. Automation** | Pre-commit hooks and grep patterns | Add language-specific checks |
| **6. Integration** | How standards connect to slash commands | Add project-specific workflows |
| **7. Evidence** | Real refactoring case studies | Replace with your own examples |
| **8. FAQ** | Addresses common skepticism | Add team-specific FAQs |

---

## Adoption Strategies

| Strategy | Best For | Setup Time | Approach |
|----------|----------|------------|----------|
| **A: Full** | New projects, solo devs | 1 hour | Copy template, set up pre-commit hooks, add scoring to `/plan-approaches` |
| **B: Gradual** | Existing codebases, teams | 5 weeks | Week 1: docs → Week 2: scoring → Week 3-4: automated checks → Week 5+: code review |
| **C: Minimal** | Prototypes, time-constrained | 10 min | Keep template as reference, use scoring, run 3 critical grep checks manually |

**Minimal (Strategy C) — the three critical grep checks:**
```bash
rg 'execute.*f"'          # SQL injection
rg "except.*:\s*pass"     # Empty catches
rg "console\.log"         # Production logging
```

---

## Language-Specific Customization

Add language-specific standards as Patterns #9, #10, etc. in your copy of the template.

| Language | Key Standards to Add | Key Automated Checks |
|----------|---------------------|---------------------|
| **Python** | Type hints on public APIs only; no mutable default args | `rg "def .*\(.*=\[\]" --type py` |
| **TypeScript** | Use `unknown` over `any`; no non-null assertions (`!`) | `rg ": any" --type ts --glob "!**/*.test.ts"` |
| **Go** | Always check errors; no goroutine leaks | `rg "_, _ = " --type go` |

**Example** (Python — mutable default args):
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

---

## Integration with Existing Standards

| Scenario | Recommendation |
|----------|---------------|
| You have a language-specific style guide | Keep both — style guide for formatting/naming, anti-slop for architecture/design |
| You have generic "best practices" | Replace with ANTI_SLOP_STANDARDS.md (concrete, automatable) |
| New project with nothing | Start with ANTI_SLOP_STANDARDS.md only, add language-specific later |

---

## Maintenance

### Quarterly Review

1. Run automated checks on entire codebase
2. Review new AI anti-patterns (add as Pattern #9, #10, etc.)
3. Update thresholds if needed
4. Check adoption (pre-commit hooks running? scoring still used?)

### Keeping It Lean

Keep core template under 400 lines. Extract language-specific standards to separate files. Delete stale content — remove anti-patterns that no longer occur.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Pre-commit hooks fail on legacy code** | Check only changed files: `git diff --cached --name-only --diff-filter=ACM \| grep '\.py$' \| xargs rg 'execute.*f"'` |
| **Team pushback ("overkill")** | Start with Strategy C (3 critical checks only). Show evidence: 155→15 line refactorings. |
| **Standards don't match project** | Adjust thresholds: 30 lines (strict/microservices), 50 (standard), 75 (legacy/algorithms) |

---

## Success Metrics

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Average Function Length | `tokei --files` or custom script | <50 lines |
| CLAUDE.md Size | `wc -l CLAUDE.md` | 150-200 lines |
| Dependency Count | `package.json`, `requirements.txt` | Trend downward |
| Code Review Time | Track PR review duration | 20% reduction |

---

## FAQ

### Q: Should anti-slop standards go in CLAUDE.md?

**NO** — Keep CLAUDE.md lightweight (150-200 lines). Add a 2-line summary with a link:

```markdown
## Code Quality Standards
We follow anti-slop principles: functions <50 lines, nesting <3, no premature optimization.
**Reference**: See [ANTI_SLOP_STANDARDS.md](./ANTI_SLOP_STANDARDS.md)
```

### Q: What if AI models improve and stop generating slop?

The underlying principles (YAGNI since 1999, KISS since Unix, Plain Language since 2010) are timeless. Human tendency to accept AI output uncritically won't change, and over-engineering predates AI.

### Q: Isn't this just YAGNI/KISS rebranded?

Anti-slop adds what YAGNI/KISS lack: **measurable standards** (grep patterns, line limits), **automated enforcement** (pre-commit hooks), and **AI-specific recognition patterns** (8 anti-patterns trained from real AI output).

---

## See Also

- [Hooks](../hooks/README.md) — Automated enforcement of standards
- [Slash Commands](../slash-commands/README.md) — `/plan-approaches` uses anti-slop scoring
- [All Templates](../README.md)

---

**Last Updated**: 2026-02-15
**Maintained By**: dev-setup template library
