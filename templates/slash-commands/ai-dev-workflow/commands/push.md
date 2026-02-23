# Push Changes

Safely stage, commit, and push all changes with quality checks.

## Step 1: Analyze Changes

Run in parallel to understand what's being committed:

- `git status` - see all changes
- `git diff --stat` - summary of modifications
- `git log -1 --oneline` - last commit for context

## Step 2: Safety Checks

Before proceeding, check for:

- **Secrets**: .env files, *_key, *_secret, credentials, API tokens with real values
- **Large files**: Files >5MB that should use Git LFS
- **Merge conflicts**: Look for `<<<<<<<` markers
- **Debug code**: `debugger` statements, `console.log` with TODO comments

If any issues found, warn the user and ask for confirmation before continuing.

## Step 3: Quality Checks

<!-- CUSTOMIZE: Replace with your project's quality gates -->
Run these checks - all must pass:

```bash
# Tests - run project test suite
npm test          # or: pytest, go test ./..., cargo test

# Lint
npm run lint      # or: ruff check ., golangci-lint run

# Type check
npm run typecheck # or: mypy ., go vet ./...
```

**If any check fails:**
1. Report which check failed
2. Suggest fix commands (e.g., `npm run lint:fix`, `npm run format`)
3. Stop and let user fix before retrying

**Customization guidance:**
- Python projects: `pytest`, `ruff check .`, `mypy .`
- Go projects: `go test ./...`, `go vet ./...`
- Minimal projects: Skip this step or just run `npm test`

## Step 4: Stage & Commit

1. Stage all changes: `git add .`
2. Show staged changes: `git status`
3. Generate a conventional commit message based on the changes:
   - Format: `type: brief description`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`
   - Include bullet points for significant changes
4. Create the commit

**Commit message examples:**
```
feat: add user authentication flow

- Add login/logout endpoints
- Integrate JWT token generation
- Add auth middleware
```

```
fix: resolve race condition in WebSocket handler

- Add mutex lock for room state updates
- Clear intervals on disconnect
```

## Step 5: Push & Verify

1. Push to remote: `git push`
2. Verify success: `git log -1`
3. Report:
   - Commit hash
   - Commit message
   - Number of files changed
   - Branch name

---

## Variants

### `/push --dry-run`
Run all checks without actually committing or pushing. Useful to verify everything is ready.

### `/push --skip-checks`
Skip quality checks (Step 3). Use only when you've already run checks manually or need to push urgently.

### `/push --amend`
Amend the previous commit instead of creating a new one. Only use if the previous commit hasn't been pushed yet.

---

## Template Customization

When copying this to your project, customize:

1. **Step 3 quality checks** - Replace with your project's actual lint/format/test commands
2. **Commit message style** - Adjust format if your team uses different conventions
3. **Additional safety checks** - Add project-specific patterns to check for

**Minimal version** (for simple projects):
Remove Step 3 entirely if you don't have quality tooling set up.
