# Git Worktrees: Parallel Development Guide

[← Back to Main README](../../README.md)

How to use Git worktrees for parallel development — especially with AI coding agents (Claude Code, Codex).

**Audience**: Developers using AI coding assistants who want to work on multiple features simultaneously.

---

## 1. Worktrees vs Branches

### Branch = Pointer, Worktree = Directory

```
my-repo/          ← one directory
├── .git/HEAD     ← points to ONE branch
├── .git/index    ← ONE staging area
└── src/          ← ONE set of files
```

A worktree adds **independent working directories** backed by the **same Git object database**:

```
my-repo/              ← main worktree (original checkout)
├── .git/             ← shared object database
└── src/

../my-repo-feature-a/ ← linked worktree (independent checkout)
├── .git              ← file pointing back to main .git/
└── src/              ← different branch, different files

../my-repo-bugfix/    ← another linked worktree
├── .git
└── src/
```

All worktrees share commit history, refs, and remote configuration. A `git fetch` in one updates branches for all.

### Comparison

| Aspect | Branches | Worktrees |
|--------|----------|-----------|
| **Simultaneous checkouts** | No — single HEAD per directory | Yes — each worktree has its own HEAD |
| **Context switching** | `git stash` → `git switch` → `git stash pop` | `cd ../other-worktree` |
| **Disk overhead** | None (just a 41-byte ref) | ~1 MB per worktree (shared object DB) |
| **Dependencies (venv, node_modules)** | Shared — one set on disk | Separate per worktree (must install each) |
| **Build artifacts** | Shared — can collide | Isolated per worktree |
| **Best for** | Feature isolation, PRs, release tracks | Parallel work, code review, AI agents |

---

## 2. Why Branches Fail for Parallel Work

### The Stash/Switch/Unstash Cycle

```
1. Working on feature-A...
2. Urgent bug report comes in
3. git stash                    ← save incomplete work
4. git switch hotfix-branch     ← rewrite all files on disk
5. Fix the bug, commit, push
6. git switch feature-a         ← rewrite files again
7. git stash pop                ← restore incomplete work
8. Try to remember where you left off
```

This is disruptive for humans. For AI agents, it's a non-starter.

### Why Two Agents Cannot Share One Checkout

| Resource | Conflict |
|----------|----------|
| **Working directory files** | Agent A edits `app.py` while Agent B reads stale version |
| **Git index (staging area)** | `git add` from both agents interleaves staged changes |
| **Lock files** | `package-lock.json`, `.pnpm-lock.yaml` written by concurrent installs |
| **Build artifacts** | `dist/`, `.next/`, `__pycache__/` rebuilt by overlapping processes |
| **Dev server ports** | Both agents try to start server on same port |
| **Git HEAD** | One agent commits while other has uncommitted changes |

With worktrees, each agent operates in a **completely isolated directory** — no stashing, no lock contention, no port conflicts.

---

## 3. Git Worktree Essentials

### Core Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `git worktree add <path> -b <branch>` | Create worktree with new branch | `git worktree add ../my-app-auth -b feature/auth` |
| `git worktree add <path> <existing-branch>` | Create worktree from existing branch | `git worktree add ../my-app-hotfix hotfix/bug-123` |
| `git worktree add -d <path>` | Create with detached HEAD (throwaway) | `git worktree add -d ../experiment` |
| `git worktree list` | Show all worktrees | Lists path, commit, branch for each |
| `git worktree remove <path>` | Delete worktree properly | `git worktree remove ../my-app-auth` |
| `git worktree prune` | Clean stale worktree references | Run after manual `rm -rf` (avoid this) |

### Directory Organization

```
~/repos/
├── my-app/                 ← main worktree (usually main/master)
├── my-app-feature-auth/    ← linked worktree for auth feature
├── my-app-bugfix-123/      ← linked worktree for bug fix
└── my-app-review/          ← linked worktree for code review
```

**Naming convention**: `{repo}-{purpose}` or `{repo}-{branch-short-name}`

### Key Constraint: No Duplicate Branch Checkouts

Git prevents checking out the same branch in two worktrees:

```bash
$ git worktree add ../second-main main
fatal: 'main' is already checked out at '/home/user/repos/my-app'
```

**Workaround**: Create a new branch pointing to the same commit:

```bash
git worktree add ../my-app-review -b review/main HEAD
```

### Cleanup: Always Use `git worktree remove`

```bash
# Wrong — leaves stale references
rm -rf ../my-app-feature-auth

# Right — clean removal
git worktree remove ../my-app-feature-auth

# If you already used rm -rf:
git worktree prune
```

---

## 4. Claude Code + Worktrees

### Built-in Support: EnterWorktree

Claude Code has a native `EnterWorktree` tool that creates worktrees in `.claude/worktrees/` and switches the session into the new directory. Trigger it by saying "start a worktree" or "work in a worktree."

For more control, create worktrees manually (Section 3) for explicit naming and placement.

### CLI Flags for Worktrees

| Flag | Purpose |
|------|---------|
| `--worktree` / `-w` | Start session in a new isolated worktree (branches from HEAD) |
| `--tmux` | Auto-create a detached tmux session for the worktree (requires `--worktree`). Uses iTerm2 native panes when available; `--tmux=classic` forces traditional tmux |
| `--append-system-prompt` | Inject additional system prompt text — useful for giving each parallel worker different instructions |
| `--fork-session` | When combined with `--resume` or `--continue`, creates a new session ID instead of reusing the original — branch a conversation without losing the parent |

### Manual Worktree Setup for Claude Code Sessions

```bash
# Terminal 1: Create worktree and start Claude
git worktree add ../my-app-auth -b feature/auth
cd ../my-app-auth
claude                    # Session A — isolated to auth feature

# Terminal 2: Create another worktree and start Claude
git worktree add ../my-app-api -b feature/api-endpoints
cd ../my-app-api
claude                    # Session B — isolated to API work
```

Each Claude Code instance gets its own working directory, Git HEAD/index, session storage, build artifacts, and dev server ports.

### Autonomous Worktree Recipes

Combine `--worktree` with `--tmux` for fire-and-forget parallel work. Each session runs in a detached tmux window — no terminal babysitting required.

**Single autonomous task**:
```bash
claude -w --tmux -p "implement user authentication with JWT, write tests, create a PR"
```

**Multiple parallel workers with specialized instructions**:
```bash
# Worker 1: Backend API
claude -w --tmux --append-system-prompt "Focus on the backend API layer. Implement REST endpoints for user management."

# Worker 2: Frontend components
claude -w --tmux --append-system-prompt "Focus on the frontend. Build React components for the user profile page."

# Worker 3: Test suite
claude -w --tmux --append-system-prompt "Write comprehensive tests for the auth module. Cover edge cases."
```

**Monitor or reconnect**:
```bash
tmux ls                   # List active sessions
tmux attach -t <name>     # Watch a worker in progress
```

**Fork a conversation to explore an alternative**:
```bash
claude --resume <session-id> --fork-session   # Branch from an existing session
```

### Session Isolation

Claude Code stores sessions based on the project directory path. Each worktree gets a distinct entry:

```
~/.claude/projects/
├── home-user-repos-my-app/                 ← main worktree sessions
├── home-user-repos-my-app-auth/            ← auth worktree sessions
└── home-user-repos-my-app-api/             ← api worktree sessions
```

Use `/resume` to switch between sessions. Named sessions (`/rename auth-refactor`) make this easier.

### Multi-Agent Patterns

| Pattern | Isolation Level | Best For |
|---------|-----------------|----------|
| **Subagents** (Task tool) | Shared context window | Quick parallel tasks within a single feature |
| **Worktrees + Sessions** | Full filesystem isolation | Independent features, long-running parallel work |

**Decision**: Need two things done quickly in one session? → Subagents. Building separate features? → Worktrees.

---

## 5. Virtual Environments in Worktrees

### The Core Problem

Python virtual environments store **absolute paths** in their scripts. A venv created in `/home/user/repos/my-app/.venv/` won't work from a worktree at `/home/user/repos/my-app-auth/`. You need a separate environment per worktree.

### Python: uv (Recommended) or venv

| Strategy | Speed | Disk Use | Best For |
|----------|-------|----------|----------|
| **uv** | Fastest (80x faster) | Minimal (hard-link cache) | All projects |
| **Separate venv** | Moderate | Full copy per worktree | No extra tools needed |

#### uv (Recommended)

[uv](https://docs.astral.sh/uv/) creates venvs in <1 second and uses hard links from a global cache, minimizing disk usage across worktrees.

```bash
# In each worktree:
cd ../my-app-auth
uv venv                              # Creates .venv in <1 second
uv pip install -r requirements.txt   # Installs from cache instantly

# Or if using pyproject.toml:
uv sync                              # Creates venv + installs everything
```

#### venv (Fallback)

```bash
cd ../my-app-auth
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Node.js

[pnpm](https://pnpm.io/) uses a global content-addressable store and creates `node_modules` via symlinks — packages aren't duplicated across worktrees:

```bash
pnpm install              # Links from global store — fast, small footprint
```

Fallback: `npm install` (full install per worktree).

### .gitignore

Ensure `.venv/`, `venv/`, `node_modules/`, `.env`, and build dirs (`dist/`, `.next/`) are in your `.gitignore`.

---

## 6. Automation

### The /worktree Skill

If you're using the epcvip AI Dev Templates, the `/worktree` skill automates the entire setup:

```
/worktree feature/auth          # Creates worktree + venv + installs deps + copies .env
/worktree list                  # Shows active worktrees
/worktree remove feature/auth   # Clean teardown
```

See `~/.claude/skills/worktree/SKILL.md` for details.

### Post-Checkout Hook (Auto-Setup)

Git's `post-checkout` hook fires when creating a worktree. Use it to auto-install dependencies:

```bash
#!/bin/bash
# .git/hooks/post-checkout (or via core.hooksPath)

PREV_HEAD=$1
NEW_HEAD=$2

# Detect new worktree: previous HEAD is all zeros
if [[ "$PREV_HEAD" == "0000000000000000000000000000000000000000" ]]; then
    echo "New worktree detected — setting up environment..."

    # Python
    if [ -f requirements.txt ] || [ -f pyproject.toml ]; then
        if command -v uv &> /dev/null; then
            uv venv && uv pip install -r requirements.txt 2>/dev/null || uv sync 2>/dev/null
        else
            python -m venv .venv && .venv/bin/pip install -r requirements.txt 2>/dev/null
        fi
    fi

    # Node.js
    if [ -f package.json ]; then
        if command -v pnpm &> /dev/null; then
            pnpm install
        else
            npm install
        fi
    fi

    # Copy .env from main worktree if available
    MAIN_WORKTREE=$(git worktree list --porcelain | head -1 | sed 's/worktree //')
    if [ -f "$MAIN_WORKTREE/.env" ] && [ ! -f .env ]; then
        cp "$MAIN_WORKTREE/.env" .env
        echo "Copied .env from main worktree."
    fi
fi
```

---

## 7. Best Practices & Pitfalls

- **Limit active worktrees to 3-4** — more creates cognitive overhead
- **Commit frequently** within each worktree — small commits prevent data loss and ease rebasing
- **Rebase from main regularly** — the longer a worktree diverges, the harder the merge
- **Name descriptively** — `my-app-feature-auth` not `my-app-wt1`
- **Clean up immediately** when a feature is merged — stale worktrees accumulate fast
- **Use `git worktree remove`**, not `rm -rf` — proper cleanup avoids stale references
- **Run `/init`** in each new worktree when using Claude Code
- **Never share venvs across worktrees** — absolute paths break
- **Never manually move worktree directories** — use `git worktree move` or recreate

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Deleted worktree with `rm -rf` — stale entries in `git worktree list` | `git worktree prune` |
| `fatal: '<branch>' is already checked out` | Create a new branch: `git worktree add -b new-name <path> <commit>` |
| Editing in wrong worktree — changes on wrong branch | Check `pwd` before committing |
| 5 worktrees x 1GB `node_modules` = 5GB | Use `pnpm` (shared store) or clean up unused worktrees |
| `claude -w` branches from HEAD (often main), not your feature branch | Use manual `git worktree add` from the branch you want, then `cd` + `claude` |

---

## 8. Quick Reference

### Command Cheat Sheet

```bash
git worktree add ../my-app-auth -b feature/auth   # New branch
git worktree add ../my-app-hotfix hotfix/bug-123   # Existing branch
git worktree add -d ../experiment                   # Detached HEAD
git worktree list                                   # List all
git worktree remove ../my-app-auth                  # Remove
git worktree prune                                  # Clean stale refs
```

### Decision Guide

```
Do you need to work on two things at the same time?
├── No → Use a branch. Switch with `git switch`.
└── Yes
    ├── Both tasks in the same Claude session? → Use subagents (Task tool)
    └── Tasks need separate sessions?
        ├── Yes → Create a worktree per task
        └── Unsure → Default to worktrees (minimal overhead, prevents surprises)
```

---

## References

| Resource | Link |
|----------|------|
| Git worktree docs | https://git-scm.com/docs/git-worktree |
| Git hooks docs | https://git-scm.com/docs/githooks |
| Python venv docs | https://docs.python.org/3/library/venv.html |
| uv docs | https://docs.astral.sh/uv/ |
| pnpm docs | https://pnpm.io/ |
| Claude Code docs | https://docs.anthropic.com/en/docs/claude-code |
| zen (worktree orchestrator) | https://github.com/mgreau/zen — Automates worktree lifecycle for PR reviews: polls GitHub, creates worktrees per PR, injects context via `CLAUDE.local.md`, auto-cleans merged PRs |
| Context Engineering guide | [CONTEXT-ENGINEERING.md](./CONTEXT-ENGINEERING.md) — Worktrees as context isolation strategy, .claudeignore, token optimization |
