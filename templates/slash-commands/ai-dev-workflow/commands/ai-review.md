---
description: Holistic AI code review against standards and best practices
allowed-tools: read_file, run_terminal_cmd, grep
---

## Command

Review recent code changes against project standards and common anti-patterns.

### 1. Load Project Standards

Read your project's coding standards:
- CLAUDE.md (if exists)
- CODING_STANDARDS.md (if exists)
- Any language-specific standards docs

### 2. Check Recent Changes

```bash
echo "=== Git Status ==="
git status --porcelain || true

echo ""
echo "=== Recent Diff ==="
git diff HEAD~1..HEAD || git diff || true
```

### 3. Review Against Anti-Patterns

Check for common issues:

**Code Quality:**
- Kitchen-sink parameters (functions accepting too many args)
- Over-abstraction (unnecessary wrappers, premature generalization)
- Blind exception handling (empty catch blocks, generic error handling)
- Premature optimization (complex solutions to simple problems)

**Code Structure:**
- Functions >50 lines (check if they should be split)
- Nesting depth >3 levels (check for early returns)
- Single responsibility violations (functions doing too much)

**Code Hygiene:**
- Unused imports
- Commented-out code blocks
- Debug statements (console.log, print, etc.)
- TODO comments without tickets

**Type Safety:**
- Use of `any` type (TypeScript)
- Missing type annotations (Python)
- Unchecked null/undefined access

**Security & Best Practices:**
- SQL injection risks (string concatenation in queries)
- Hardcoded secrets or credentials
- Missing input validation
- Authentication/authorization checks

**Testing & Documentation:**
- New code has corresponding tests
- Public APIs have documentation
- Complex logic has explanatory comments

### 4. UI-Specific Checks (if applicable)

If UI code changed:
- Mobile responsiveness (test at 375px width)
- Browser console errors
- Loading/error states handled
- Accessibility (keyboard navigation, ARIA labels)

### 5. Provide Recommendations

For each issue found:
- File path and line number
- Specific problem
- Suggested fix
- Why it matters

Format recommendations as actionable edits, not vague suggestions.

---

## Customization Notes

**For your project:**
1. Replace generic checks with your project-specific standards
2. Add framework-specific patterns (e.g., FastAPI auth, React hooks)
3. Reference your project's specific standards documents
4. Add automated grep checks for project-specific anti-patterns

**Example project-specific additions:**
```bash
# Check for project-specific patterns
rg "banned_function_name" src/
rg "@deprecated" --type ts
rg "FIXME|XXX" --type py
```

