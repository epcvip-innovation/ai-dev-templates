# Claude Code Permission Templates

[← Back to Main README](../../README.md)

**Purpose**: Auto-approve common, safe operations to reduce approval prompts during development sessions.

**Location**: `.claude/settings.local.json` in your project root

---

## Quick Start

```bash
# Copy template to your project
cp templates/permissions/settings.local.json.template your-project/.claude/settings.local.json

# Customize for your project type (uncomment relevant sections)
nano your-project/.claude/settings.local.json
```

For existing projects, merge permissions from template into your existing `.claude/settings.local.json`.

---

## Permission System Overview

### Three Permission Lists

| List | Behavior | Example |
|------|----------|---------|
| **`allow`** | Auto-approve (no prompt) | `Bash(git add *)`, `Read` |
| **`deny`** | Always block | `Bash(rm -rf *)`, `Bash(sudo *)` |
| **`ask`** | Prompt for approval | `Bash(git push origin main)` |

### Permission Syntax

```
"Bash(npm run *)"              // Matches commands starting with "npm run" (space-separated)
"Bash(git commit *)"           // Any git commit arguments
"Bash"                         // Matches ALL Bash commands
"Read"                         // Allow all reads
"WebSearch"                    // Allow web search
"WebFetch(domain:github.com)"  // Specific domain (colon only for domain specifiers)
"MCP"                          // All MCP tools
```

**Important**: Bash rules use **spaces** between the command prefix and `*`: `Bash(git add *)` not ~~`Bash(git add:*)`~~. The colon syntax is only for domain specifiers like `WebFetch(domain:example.com)`.

### Evaluation Order

Rules are evaluated: **deny first, then ask, then allow**. The first matching rule wins. Higher-priority settings sources (managed > local > project > user) take precedence for deny rules.

---

## Common Permission Categories

| Category | Permissions | Notes |
|----------|------------|-------|
| **File Read** | `Read` (permissive) or `Read(/home/[user]/**)` (restricted) | Permissive for solo; restricted for shared machines |
| **Git** | `Bash(git add *)`, `Bash(git commit *)`, `Bash(git push *)`, `Bash(git branch *)`, `Bash(git log *)` | Non-destructive, reversible. Consider `ask` for `git push origin main` and `deny` for `--force`. |
| **Python** | `Bash(python *)`, `Bash(pip install *)`, `Bash(pytest *)`, `Bash(black *)`, `Bash(uvicorn *)` | `pip install *` is permissive — remove if concerned |
| **TypeScript/Node** | `Bash(npm run build *)`, `Bash(npm run test *)`, `Bash(npm install *)`, `Bash(npx tsc *)` | `npm install *` can install packages — consider restricting |
| **File Management** | `Bash(mkdir *)`, `Bash(mv *)`, `Bash(touch *)`, `Bash(find *)`, `Bash(ls *)` | Read-only or create/move operations |
| **Dev Server** | `Bash(curl *)`, `Bash(pkill *)`, `Bash(lsof *)` | `pkill` can terminate processes — ensure trust |
| **Web** | `WebSearch`, `WebFetch(domain:github.com)` | Don't use `WebFetch` without domain specifier — restrict to specific domains |
| **MCP** | `MCP(server:github)`, `MCP(tool:github/search_issues)` | Explicitly approve only needed MCP servers |

---

## Security Guidelines

| Category | Always Auto-Approve | Never Auto-Approve | Ask First |
|----------|--------------------|--------------------|-----------|
| **File ops** | Read, mkdir, mv, touch | `rm -rf`, `chmod 777` | `rm` (single file) |
| **Git** | add, commit, log, diff, branch | `push --force`, `reset --hard` | `push origin main` |
| **Build/test** | npm test, pytest, tsc | — | — |
| **System** | — | `sudo`, system package managers | — |
| **Deploy** | — | Production deployment scripts | — |
| **Packages** | — | — | `pip install`, `npm install` |

---

## Permission Strategies by Project Type

| Strategy | Philosophy | Key Differences |
|----------|-----------|-----------------|
| **Solo Personal** | Trust Claude with most operations | `allow: [Bash(git *), Bash(python *), Bash(npm *)]`. Only deny catastrophic commands. |
| **Team Project** | Require approval for operations affecting others | `ask: [Bash(git push *), Bash(npm install *)]`. Deny `rm` and force push. |
| **Production Service** | Minimal auto-approval | `allow: [Read, Bash(git status *)]`. Ask for commits and tests. Deny push, rm, deploy. |

**Example** (Solo Personal — permissive):
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(git *)",
      "Bash(python *)",
      "Bash(npm *)",
      "Bash(mkdir *)",
      "Bash(mv *)",
      "Bash(find *)",
      "WebSearch"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  }
}
```

---

## Language/Framework Quick Reference

| Language | Key Permissions |
|----------|----------------|
| **Python (FastAPI)** | `Bash(python *)`, `Bash(pip install *)`, `Bash(pytest *)`, `Bash(black *)`, `Bash(ruff *)`, `Bash(uvicorn *)`, `Bash(source venv/bin/activate)` |
| **TypeScript (React)** | `Bash(npm *)`, `Bash(npx *)`, `Bash(node *)`, `WebFetch(domain:nodejs.org)` |
| **Go** | `Bash(go build *)`, `Bash(go test *)`, `Bash(go run *)`, `Bash(go mod *)`, `WebFetch(domain:golang.org)` |
| **Rust** | `Bash(cargo build *)`, `Bash(cargo test *)`, `Bash(cargo run *)`, `Bash(cargo clippy *)`, `Bash(cargo fmt *)` |

All should include: `Bash(git *)`, `Read`, `WebSearch`.

---

## Integration with Slash Commands

| Slash Command | Required Permissions |
|---------------|----------------------|
| /start-feature | `Bash(mkdir *)`, `Bash(touch *)` |
| /resume-feature | `Read(/path/to/project/**)` |
| /ai-review | `Bash(git diff *)`, `Bash(git log *)` |
| /feature-complete | `Bash(find *)`, `Bash(grep *)`, `Bash(pytest *)` or `Bash(npm test *)` |
| /align-project-docs | `Bash(mkdir *)`, `Bash(mv *)` |
| /plan-approaches | `Bash(find *)`, `Bash(grep *)` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Claude keeps asking for permission** | Add the exact permission string to `allow` list. Restart session if needed. |
| **Permission denied but it's in allow** | Check JSON syntax (`python -m json.tool`). Verify pattern matches exactly. Ensure correct file (`.local.json` not `.json`). |
| **Too permissive** | Move from `allow` to `ask` or `deny`. |

---

## FAQ

| Question | Answer |
|----------|--------|
| Where does settings.local.json live? | Project root: `your-project/.claude/settings.local.json` |
| Difference between settings.json and settings.local.json? | `settings.json` = checked into git (team). `settings.local.json` = gitignored (personal). |
| Different permissions per subdirectory? | No. Permissions are per-project. Workaround: nested `.claude/` folders. |
| Need to restart after changing? | Settings are snapshotted at startup. For hooks especially, mid-session changes require review in `/hooks` menu or restart. Use `/config` to reload settings. |
| Environment variables in permissions? | No. Use wildcards instead: `Bash(export DATABASE_PATH=*)` |
| Settings isolation for teams? | Use `claude --setting-sources project` to ensure personal settings can't override project controls. |
| Sandbox mode? | `"sandbox": { "enabled": true }` in settings restricts filesystem/network access for Bash commands. |

---

## Security Checklist

Before finalizing `.claude/settings.local.json`:

- [ ] No `rm -rf`, `sudo`, `git push --force` in allow list
- [ ] Production deployments in `ask` or `deny`
- [ ] No hardcoded secrets in allow list
- [ ] Read permissions don't include `/etc/`, `/root/`
- [ ] WebFetch restricted to specific domains
- [ ] Main branch pushes in `ask` list (if team project)

---

## See Also

- [Security Guide](../security/AI-AGENT-SECURITY-GUIDE.md) — Tiered security best practices using permissions + hooks
- [Hooks](../hooks/README.md) — Runtime enforcement (complements permissions)
- [Slash Commands](../slash-commands/README.md) — Commands that need specific permissions
- [All Templates](../README.md)

---

**Last Updated**: 2026-02-19
**Maintained By**: dev-setup template library
