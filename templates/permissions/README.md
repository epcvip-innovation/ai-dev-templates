# Claude Code Permission Templates

[← Back to Main README](../../README.md)

**Purpose**: Auto-approve common, safe operations to reduce approval prompts during development sessions.

**Location**: `.claude/settings.local.json` in your project root

---

## Quick Start

### For New Projects

```bash
# Copy template to your project
cp templates/permissions/settings.local.json.template your-project/.claude/settings.local.json

# Edit to match your project type
cd your-project/.claude/
nano settings.local.json

# Uncomment sections you need:
# - Python project: Uncomment Python permissions
# - TypeScript/Node: Uncomment npm/node permissions
# - Web service: Uncomment server permissions
```

### For Existing Projects

If you already have `.claude/settings.local.json`, merge permissions from template:
1. Keep your existing permissions
2. Add any missing common permissions from template
3. Remove duplicates

---

## Permission System Overview

### Three Permission Lists

**1. `allow` (auto-approve)**:
- Commands/tools that are safe to run without prompting
- Example: `git add`, `npm run build`, `Read(/home/user/**)`
- Claude will execute these automatically

**2. `deny` (always block)**:
- Commands that should NEVER be auto-approved
- Example: `rm -rf`, `git push --force`, `sudo`
- Claude will be prevented from running these

**3. `ask` (explicit approval)**:
- Commands that need user confirmation
- Example: `git push origin main`, database modifications
- Claude will prompt before executing

### Permission Syntax

**Bash commands**:
```json
"Bash(command:*)"           // Any arguments
"Bash(command)"             // Exact match only
"Bash(command:arg1:arg2)"   // Specific arguments
```

**Read permissions**:
```json
"Read(///**)"               // Read everything (permissive)
"Read(/home/user/**)"       // Read user directory
"Read(/home/user/.claude/**)"  // Read Claude config only
```

**Web permissions**:
```json
"WebSearch"                 // Allow web search
"WebFetch(domain:github.com)"  // Specific domain
"WebFetch(domain:*)"        // All domains (not recommended)
```

---

## Common Permission Categories

### 1. File Read Permissions

**Option A: Permissive** (personal projects, solo developer):
```json
"Read(///**)"
```

**Option B: Restricted** (team projects, shared machines):
```json
"Read(/home/[username]/**)",
"Read(/home/[username]/.claude/**)",
"Read(/home/[username]/.screenshots/**)"
```

**When to use**:
- Permissive: Personal projects, full control over machine
- Restricted: Team projects, need to prevent accidental reads of sensitive dirs

### 2. Git Commands (Essential)

**Always safe to auto-approve**:
```json
"Bash(git add:*)",
"Bash(git commit:*)",
"Bash(git push:*)",
"Bash(git branch:*)",
"Bash(git checkout:*)",
"Bash(git log:*)"
```

**Why**: These are non-destructive, reversible operations.

**Consider denying** (ask for approval):
```json
// In "ask" list:
"Bash(git push origin main)"  // Production branch
"Bash(git push --force:*)"    // Force push (destructive)
```

### 3. Python Project Permissions

**Common Python commands**:
```json
"Bash(python:*)",
"Bash(python3:*)",
"Bash(pip install:*)",
"Bash(pytest:*)",
"Bash(source:*)",
"Bash(black:*)",
"Bash(ruff check:*)",
"Bash(uvicorn:*)"
```

**When to use**: Any Python project

**Security note**: `pip install:*` is permissive - if concerned, remove and approve manually

### 4. TypeScript/Node Project Permissions

**Common npm/node commands**:
```json
"Bash(npm run build:*)",
"Bash(npm run lint:*)",
"Bash(npm run test:*)",
"Bash(npm install:*)",
"Bash(npx tsc:*)",
"Bash(npx tsx:*)"
```

**When to use**: TypeScript, React, Node.js projects

**Security note**: `npm install:*` can install packages - consider restricting if concerned

### 5. Project Management Commands

**Always useful**:
```json
"Bash(mkdir:*)",
"Bash(mv:*)",
"Bash(touch:*)",
"Bash(find:*)",
"Bash(grep:*)",
"Bash(cat:*)",
"Bash(wc:*)",
"Bash(ls:*)",
"Bash(echo:*)"
```

**Why**: These are read-only or create/move operations (not destructive)

### 6. Development Server Commands

**For local development**:
```json
"Bash(curl:*)",
"Bash(pkill:*)",
"Bash(kill:*)",
"Bash(lsof:*)"
```

**When to use**: Running local servers (Flask, Express, etc.)

**Security note**: `pkill` and `kill` can terminate processes - ensure you trust Claude's decisions

### 7. Web Search & Fetch

**Recommended permissions**:
```json
"WebSearch",
"WebFetch(domain:github.com)",
"WebFetch(domain:www.anthropic.com)",
"WebFetch(domain:docs.yourframework.com)"
```

**When to use**:
- WebSearch: Always useful for research
- WebFetch: Add domains Claude frequently needs (docs, APIs, your services)

**Security note**: Don't use `WebFetch(domain:*)` - restrict to specific domains

---

## Security Considerations

### What to Always Auto-Approve

✅ **Read-only operations**:
- File reads (`Read(/path/**)`)
- Git status, log, diff
- Grep, find, cat, ls

✅ **Non-destructive writes**:
- Git add, commit, push (to feature branches)
- File creation (mkdir, touch, echo)
- File moves (mv)

✅ **Build/test commands**:
- npm run build, npm test
- pytest, black, ruff
- tsc, tsx

### What to NEVER Auto-Approve

❌ **Destructive operations**:
- `rm -rf` (file deletion)
- `git reset --hard` (history rewrite)
- `git push --force` (force push)

❌ **System-level operations**:
- `sudo` (elevated permissions)
- `chmod 777` (permission changes)
- System package managers

❌ **Production deployments**:
- `git push origin main` (protect main branch)
- Deployment scripts (railway, vercel, aws)
- Database migrations in production

### What to Ask Before Approving

⚠️ **Context-dependent operations**:
- Main branch pushes (`git push origin main`)
- Package installations (`pip install`, `npm install`)
- Database operations (`psql`, `sqlite3`)
- File deletion (`rm`)
- Server restarts
- Environment variable changes with secrets

---

## Permission Strategies by Project Type

### Solo Personal Project (Permissive)

```json
{
  "permissions": {
    "allow": [
      "Read(///**)",
      "Bash(git:*)",
      "Bash(python:*)",
      "Bash(npm:*)",
      "Bash(mkdir:*)",
      "Bash(mv:*)",
      "Bash(find:*)",
      "Bash(grep:*)",
      "WebSearch"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)"
    ]
  }
}
```

**Philosophy**: Trust Claude with most operations, block only catastrophic commands

### Team Project (Restrictive)

```json
{
  "permissions": {
    "allow": [
      "Read(/home/[user]/project/**)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git log:*)",
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "WebSearch"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(npm install:*)",
      "Bash(pip install:*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(git push --force:*)"
    ]
  }
}
```

**Philosophy**: Require approval for operations that affect others or install dependencies

### Production Service (Very Restrictive)

```json
{
  "permissions": {
    "allow": [
      "Read(/home/[user]/service/**)",
      "Bash(git status)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "WebSearch"
    ],
    "ask": [
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(pytest:*)",
      "Bash(npm test:*)"
    ],
    "deny": [
      "Bash(git push:*)",
      "Bash(rm:*)",
      "Bash(railway:*)",
      "Bash(sudo:*)"
    ]
  }
}
```

**Philosophy**: Minimal auto-approval, ask for everything that modifies state

---

## Common Patterns from Your Repos

### Pattern 1: Python Backend Service (FastAPI)

```json
"Bash(python:*)",
"Bash(pip install:*)",
"Bash(pytest:*)",
"Bash(black:*)",
"Bash(uvicorn:*)",
"Bash(sqlite3:*)",
"Bash(railway:*)",
"WebFetch(domain:docs.railway.app)"
```

**Use case**: Flask/FastAPI service deployed to Railway

### Pattern 2: TypeScript Frontend (dois-test-capacity-planner)

```json
"Bash(npm run build:*)",
"Bash(npm run lint:*)",
"Bash(npx tsc:*)",
"Bash(npx tsx:*)",
"Read(/~/.screenshots/**)"
```

**Use case**: React/Vite frontend with TypeScript

### Pattern 3: Analysis/Research Project (ping-tree-compare)

```json
"Read(///**)",
"Bash(python:*)",
"Bash(python3:*)",
"Bash(find:*)",
"Bash(grep:*)",
"Bash(curl:*)",
"WebSearch"
```

**Use case**: Data analysis, research, exploration

---

## Troubleshooting

### Claude Keeps Asking for Permission

**Problem**: You're constantly approving the same command

**Solution**: Add to `allow` list:
```bash
# 1. Note the exact permission request
# Example: "Bash(npm run test)"

# 2. Add to .claude/settings.local.json
"Bash(npm run test:*)"

# 3. Reload Claude Code or restart session
```

### Permission Denied When It Should Work

**Problem**: Command is in `allow` list but still blocked

**Possible causes**:
1. **Syntax error** in JSON (missing comma, quote)
2. **Pattern doesn't match**: `Bash(npm test)` vs `Bash(npm run test)`
3. **File not in right location**: Should be `.claude/settings.local.json` (not `.claude/settings.json`)

**Debug**:
```bash
# Check JSON syntax
cat .claude/settings.local.json | python -m json.tool

# Check file location
ls -la .claude/

# Check exact command Claude tried to run (in error message)
```

### Too Permissive - Want to Restrict

**Problem**: Auto-approved something you didn't want

**Solution**: Move from `allow` to `ask` or `deny`:
```json
{
  "permissions": {
    "allow": [
      "// Removed: Bash(npm install:*)"
    ],
    "ask": [
      "Bash(npm install:*)"  // Now requires approval
    ]
  }
}
```

---

## Best Practices

### 1. Start Restrictive, Loosen as Needed

Begin with minimal permissions, add to `allow` list as you encounter prompts.

### 2. Use Wildcards Appropriately

✅ **Good**: `Bash(npm run:*)` (any npm script)
❌ **Too broad**: `Bash(*)` (any bash command)

### 3. Separate by Environment

**Development machine** (permissive):
```json
"Bash(git push:*)"  // Auto-approve
```

**Shared/production machine** (restrictive):
```json
// In "ask" list:
"Bash(git push origin main)"  // Require approval
```

### 4. Document Why

Add comments for non-obvious permissions:
```json
"Bash(export PUBLIC_API_SECRET_KEY=\"...\")",  // Required for local dev
"WebFetch(domain:community.tiller.com)",  // Fetch support docs
```

### 5. Review Quarterly

Set reminder to audit `.claude/settings.local.json`:
- Remove unused permissions
- Tighten overly permissive rules
- Add new common commands

---

## Integration with Slash Commands

### Commands That Need Permissions

| Slash Command | Required Permissions |
|---------------|----------------------|
| /start-feature | `Bash(mkdir:*)`, `Bash(touch:*)` |
| /resume-feature | `Read(//path/to/project/**)` |
| /ai-review | `Bash(git diff:*)`, `Bash(git log:*)` |
| /feature-complete | `Bash(find:*)`, `Bash(grep:*)`, `Bash(pytest:*)` or `Bash(npm test:*)` |
| /align-project-docs | `Bash(mkdir:*)`, `Bash(mv:*)` |
| /plan-approaches | `Bash(find:*)`, `Bash(grep:*)` |

**Recommendation**: If using slash commands, ensure you have these base permissions in `allow` list.

---

## Examples by Language/Framework

### Python (Flask/FastAPI)

```json
{
  "permissions": {
    "allow": [
      "Read(/home/user/project/**)",
      "Bash(git:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(pip install:*)",
      "Bash(pytest:*)",
      "Bash(black:*)",
      "Bash(ruff:*)",
      "Bash(uvicorn:*)",
      "Bash(source venv/bin/activate)",
      "WebSearch"
    ]
  }
}
```

### TypeScript (React/Next.js)

```json
{
  "permissions": {
    "allow": [
      "Read(/home/user/project/**)",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(node:*)",
      "WebSearch",
      "WebFetch(domain:nodejs.org)",
      "WebFetch(domain:npmjs.com)"
    ]
  }
}
```

### Go

```json
{
  "permissions": {
    "allow": [
      "Read(/home/user/project/**)",
      "Bash(git:*)",
      "Bash(go build:*)",
      "Bash(go test:*)",
      "Bash(go run:*)",
      "Bash(go mod:*)",
      "WebSearch",
      "WebFetch(domain:golang.org)"
    ]
  }
}
```

### Rust

```json
{
  "permissions": {
    "allow": [
      "Read(/home/user/project/**)",
      "Bash(git:*)",
      "Bash(cargo build:*)",
      "Bash(cargo test:*)",
      "Bash(cargo run:*)",
      "Bash(cargo clippy:*)",
      "Bash(cargo fmt:*)",
      "WebSearch",
      "WebFetch(domain:rust-lang.org)"
    ]
  }
}
```

---

## Template Customization Workflow

### Step 1: Copy Template

```bash
cp templates/permissions/settings.local.json.template .claude/settings.local.json
```

### Step 2: Identify Project Type

**Questions**:
- What language? (Python, TypeScript, Go, Rust, etc.)
- What framework? (Flask, React, Next.js, etc.)
- Running local servers? (Yes → add server commands)
- Team project? (Yes → more restrictive)

### Step 3: Uncomment Relevant Sections

In `.claude/settings.local.json`:
- Uncomment Python section if Python project
- Uncomment Node section if TypeScript/Node
- Uncomment server commands if running local servers
- Add project-specific domains to WebFetch

### Step 4: Remove Comments

```bash
# Optional: Remove all comment lines for cleaner file
sed -i '/\/\//d' .claude/settings.local.json
```

### Step 5: Test

Start Claude Code session, trigger commands:
- Should auto-execute without prompts
- If prompted, add to allow list

---

## FAQ

### Q: Where does .claude/settings.local.json live?

**A**: Project root, alongside CLAUDE.md and .git/

```
your-project/
├── .claude/
│   ├── settings.local.json  ← Here
│   └── commands/
├── .git/
├── CLAUDE.md
└── src/
```

### Q: What's the difference between settings.json and settings.local.json?

**A**:
- `settings.json`: Checked into git, shared with team
- `settings.local.json`: Gitignored, personal overrides

Use `settings.local.json` for personal permissions.

### Q: Can I have different permissions per subdirectory?

**A**: No. Permissions are per-project (where .claude/ folder lives).

**Workaround**: Use nested .claude/ folders in subdirectories for different permission scopes.

### Q: Do I need to restart Claude after changing permissions?

**A**: Not usually. Claude Code reloads settings automatically. If not working, restart session.

### Q: How do I see what permissions Claude is using?

**A**: Check `.claude/settings.local.json` file. There's no CLI command to list active permissions.

### Q: Can I use environment variables in permissions?

**A**: No. Permissions use literal strings, not variable expansion.

**Workaround**: Use wildcards: `Bash(export DATABASE_PATH:*)`

---

## Security Checklist

Before finalizing `.claude/settings.local.json`:

- [ ] No `Bash(rm -rf:*)` in allow list
- [ ] No `Bash(sudo:*)` in allow list
- [ ] No `Bash(git push --force:*)` in allow list
- [ ] Production deployments in `ask` or `deny` list
- [ ] API keys/secrets not hardcoded in allow list
- [ ] Read permissions don't include `/etc/`, `/root/`, other system dirs
- [ ] WebFetch restricted to specific domains (not `domain:*`)
- [ ] File deletion (`rm`) in `ask` or `deny` list
- [ ] Main branch pushes in `ask` list if team project

---

## Related Templates

**Slash commands that need permissions**:
- [start-feature](../slash-commands/feature-workflow/start-feature.md) - Needs `Bash(mkdir:*)`, `Bash(touch:*)`
- [feature-complete](../slash-commands/completion/feature-complete.md) - Needs `Bash(git:*)`, test commands
- [align-project-docs](../slash-commands/context-management/align-project-docs.md) - Needs `Bash(find:*)`, `Bash(grep:*)`

**Other templates**:
- [CLAUDE.md Guidelines](../claude-md/CLAUDE-MD-GUIDELINES.md) - File length enforcement
- [Anti-Slop Standards](../standards/) - Pre-commit quality gates

---

**Last Updated**: 2025-11-02
**Maintained By**: dev-setup template library
