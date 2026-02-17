---
description: Evaluate 3 distinct approaches before implementing a task
allowed-tools: read_file, codebase_search, grep
---

## Command

Before implementing, propose 3 architecturally distinct valid approaches evaluated against CLAUDE.md anti-slop standards.

**For each approach:**
1. High-level strategy (architecture, state management, validation)
2. Pros (why it's good for this use case)
3. Cons (trade-offs, risks, limitations)
4. Anti-slop score (1-10: follows simplicity, directness, and minimal abstraction principles)

**Anti-Slop Scoring Criteria (1-10)**:

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

**1-3/10 - Over-Engineered (Typically Reject)**:
- ❌ Heavy abstraction (managers, factories, strategies)
- ❌ Functions >100 lines
- ❌ 3+ new dependencies
- ❌ Deep nesting (5+ levels)
- ❌ Premature optimization

**See**: ANTI_SLOP_STANDARDS.md for detailed anti-patterns and recognition guidance

**Then:**
- Select the best approach with clear reasoning
- Explain why the others were rejected
- Adjust the plan if the best approach differs from original task
- Wait for user approval before proceeding

**Guidelines:**
- Check existing codebase patterns first (use read_file/codebase_search)
- Focus on meaningful architectural differences, not trivial variations
- All 3 approaches must be actually viable (no straw men)
- If task is premature/misdirected, say so ("Approach 0: Don't build this yet")

