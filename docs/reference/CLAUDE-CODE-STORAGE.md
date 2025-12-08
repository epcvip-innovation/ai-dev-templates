# Claude Code Local Storage Reference

[← Back to Main README](../../README.md) | [Configuration Reference →](./CLAUDE-CODE-CONFIG.md)

**Last Updated**: December 7, 2025 | **Claude Code Version**: 2.0.x

Practical guide to Claude Code's local data storage, session history, and how to find old conversations.

> **Note**: This documents internal storage based on community observation (December 2025).
> Internal formats may change between versions. Official documentation is limited.

---

## Overview

Claude Code stores all application data in `~/.claude/` (not `~/.config/claude/`).

**What's stored:**
- Session transcripts (your conversations)
- File edit history (undo capability)
- Configuration and authentication
- Plugins, skills, and hooks

**Typical size:** 100-500MB, can grow larger with heavy use

**Not synced:** This is local storage only. Cloud sync requires manual backup.

---

## Directory Structure

```
~/.claude/                    # Main directory (NOT ~/.config/claude/)
├── projects/                # Session transcripts (largest)
├── file-history/            # File edit undo history
├── todos/                   # TodoWrite task state
├── plans/                   # Plan mode markdown files
├── debug/                   # Debug logs
├── hooks/                   # User hook scripts
├── skills/                  # Custom skills
├── plugins/                 # Installed plugins
├── marketplaces/            # Plugin sources
├── statsig/                 # Feature flags (internal)
├── session-env/             # Runtime state
├── shell-snapshots/         # Shell environment snapshots
├── settings.json            # User configuration
├── settings.local.json      # Permission overrides
├── .credentials.json        # OAuth tokens (mode 600)
└── history.jsonl            # Global command history index
```

### Size Breakdown

| Directory | Typical Size | Purpose | Safe to Clean? |
|-----------|-------------|---------|----------------|
| `projects/` | 100-300MB | Session transcripts | ⚠️ Lose history & resume |
| `file-history/` | 10-50MB | File edit undo | ⚠️ Lose undo ability |
| `todos/` | 1-5MB | TodoWrite state | ✅ Yes |
| `plans/` | <1MB | Plan mode files | ✅ Yes (if done) |
| `debug/` | 1-10MB | Debug logs | ✅ Yes |
| `hooks/` | <1MB | User hook scripts | ❌ Custom code |
| `skills/` | <1MB | Custom skills | ❌ Custom config |
| `plugins/` | <1MB | Installed plugins | ⚠️ Can reinstall |

---

## Session Storage (projects/)

Your conversations are stored per-project in `~/.claude/projects/`.

### Path Encoding

Project paths are encoded by replacing `/` with `-`:

| Actual Path | Encoded Folder Name |
|-------------|---------------------|
| `/home/adams/repos/myproject` | `-home-adams-repos-myproject` |
| `/mnt/c/Users/adam.s/Documents/Foo` | `-mnt-c-Users-adam-s-Documents-Foo` |

### File Types

| Pattern | Purpose |
|---------|---------|
| `{uuid}.jsonl` | Main session transcript |
| `agent-{hash}.jsonl` | Subagent (Task tool) transcripts - filter these out when searching for main conversations |

**Tip:** When searching, filter out agent files first to focus on main sessions:
```bash
ls *.jsonl | grep -v agent-
```

### JSONL Format (Simplified)

Each line is a JSON object. Key fields:

```json
{"type":"user","message":{"role":"user","content":"..."},"timestamp":"2025-12-07T..."}
{"type":"assistant","message":{"role":"assistant","content":"..."},"timestamp":"..."}
```

This is enough for grep searching. Full schema is undocumented and may change.

---

## Other Storage

### file-history/ - Edit Undo

Stores versions of files Claude has edited, enabling undo.

```
file-history/{session-uuid}/
├── {hash}@v1    # Version 1
├── {hash}@v2    # Version 2
└── {hash}@v3    # Version 3
```

### todos/ - Task State

One JSON file per session storing TodoWrite state:

```json
[{"content": "Fix bug", "status": "completed", "activeForm": "Fixing bug"}]
```

### plans/ - Plan Mode

Markdown files with whimsical names (e.g., `vectorized-questing-crane.md`).

### debug/ - Logs

Text files with timestamped debug messages per session.

### Configuration Files

| File | Purpose | Notes |
|------|---------|-------|
| `settings.json` | User config (hooks, statusLine, plugins) | Editable |
| `settings.local.json` | Permission overrides | Editable |
| `.credentials.json` | OAuth tokens | Mode 600, don't share |
| `history.jsonl` | Global command history | Index for --resume |

---

## Finding & Searching Conversations

### Using --resume (Built-in)

```bash
# Interactive session picker with timestamps
claude --resume

# Resume last session
claude -c
# or
claude --continue

# Resume specific session by ID
claude --resume 6294a501-76d7-46dd-8e5f-e28c04c7511f
```

### Finding Your Project's Sessions

```bash
# List sessions for current project (newest first)
ls -lt ~/.claude/projects/-$(pwd | tr '/' '-')/

# Count sessions
ls ~/.claude/projects/-$(pwd | tr '/' '-')/*.jsonl | wc -l
```

### Searching Conversation Content

```bash
# Find sessions containing a term
grep -rl "search term" ~/.claude/projects/

# Search with context (2 lines before/after)
grep -r -C 2 "error message" ~/.claude/projects/

# Search specific project only
grep -r "API key" ~/.claude/projects/-home-adams-repos-myproject/

# Search recent sessions only (last 7 days)
find ~/.claude/projects/ -name "*.jsonl" -mtime -7 -exec grep -l "search" {} \;
```

**Narrowing Strategy:** If your search returns too many results:
1. Add file paths or unique identifiers: `grep -l "myfile.py\|specific-error"`
2. Combine with time filter: `find ... -mtime -7 -exec grep -l "term" {} \;`
3. Exclude agent files: `grep -l "term" *.jsonl | grep -v agent-`
4. Search user messages only: `grep '"role":"user"' file.jsonl | grep "term"`

### Extract Conversation Summary

```bash
# Quick look at a session's topics (user messages only)
grep '"role":"user"' ~/.claude/projects/-path-to-project/session-id.jsonl | head -10
```

### Session Discovery Patterns

When searching for a specific past conversation, use this workflow:

**Step 1: List recent main sessions (exclude subagents)**
```bash
# Get project folder, list main sessions by date
PROJECT=~/.claude/projects/-home-adams-repos-myproject
ls -lt "$PROJECT"/*.jsonl | grep -v agent- | head -10
```

**Step 2: Get timestamps for candidate sessions**
```bash
stat -c '%y %n' "$PROJECT"/*.jsonl | grep -v agent | sort -r | head -10
```

**Step 3: Identify session topic from first user message**
```bash
# Extract first real user message (skip tool results and meta messages)
grep '"role":"user"' session.jsonl | grep -v 'tool_result\|isMeta\|command-message' | head -1
```

**Step 4: Search with specific terms first**
```bash
# Start narrow - unique identifiers work better than generic terms
grep -l "HANDOFF.md\|specific-filename" "$PROJECT"/*.jsonl

# If too many results, add more specific terms
grep -l "8-line.*frontmatter\|query-vetting/HANDOFF" "$PROJECT"/*.jsonl
```

**Common Pitfalls:**
- ❌ Generic terms (`frontmatter`, `error`) return too many sessions
- ❌ Forgetting to filter `agent-*.jsonl` files (subagent noise)
- ❌ Not checking timestamps (similar sessions from different dates)
- ✅ Start with unique file names, project names, or specific phrases
- ✅ Use `grep -l` first (file list), then `grep -C 2` for context

**Quick Reference - One-liner to find and identify sessions:**
```bash
# Find sessions matching term, show date and first user message
for f in $(grep -l "search-term" ~/.claude/projects/-your-project/*.jsonl | grep -v agent); do
  echo "=== $(stat -c %y "$f" | cut -d. -f1) ==="
  grep '"role":"user"' "$f" | grep -v tool_result | head -1 | cut -c1-200
done
```

---

## Storage Management

### Checking Disk Usage

```bash
# Total ~/.claude size
du -sh ~/.claude/

# Breakdown by folder
du -sh ~/.claude/*/ | sort -h

# Largest sessions
find ~/.claude/projects/ -name "*.jsonl" -size +10M -exec ls -lh {} \;
```

### What's Safe to Delete

| Item | Command | What You Lose |
|------|---------|---------------|
| Old debug logs | `find ~/.claude/debug/ -mtime +7 -delete` | Old debug info |
| Empty todos | `find ~/.claude/todos/ -size 2c -delete` | Nothing (empty files) |
| Specific project history | `rm -rf ~/.claude/projects/-path-to-project/` | That project's history |
| All todos | `rm -rf ~/.claude/todos/` | Task state |

### What NOT to Delete

| Item | Why |
|------|-----|
| `settings.json` | Your configuration |
| `.credentials.json` | Will need to re-authenticate |
| `hooks/` | Custom hook scripts you wrote |
| `skills/` | Custom skills you created |

### Known Issues

**Storage Bloat** ([GitHub #5024](https://github.com/anthropics/claude-code/issues/5024))

Sessions can grow to 50-100MB+ each. The `projects/` folder may reach multiple GB.

**Symptoms:**
- Slow Claude Code startup
- Large ~/.claude folder

**Workaround:**
```bash
# Find large old sessions
find ~/.claude/projects/ -name "*.jsonl" -size +10M -mtime +7 -exec ls -lh {} \;

# Delete after review (CAREFUL - loses history)
find ~/.claude/projects/ -name "*.jsonl" -size +10M -mtime +7 -delete
```

**Setting:** `cleanupPeriodDays` in settings.json (default 30 days)
```json
{"cleanupPeriodDays": 14}
```
Sessions inactive longer than this are deleted at startup.

---

## Third-Party Tools

Official tooling for browsing history is limited. Community tools fill the gap:

| Tool | Purpose | Link |
|------|---------|------|
| **claude-conversation-extractor** | Export conversations to readable format | [GitHub](https://github.com/ZeroSumQuant/claude-conversation-extractor) |
| **claude-code-log** | Convert JSONL to HTML | [GitHub](https://github.com/daaain/claude-code-log) |
| **claude-code-history-mcp** | MCP server for history access | [LobeHub](https://lobehub.com/mcp/yudppp-claude-code-history-mcp) |
| **Claude Code Assist** (VS Code) | Visual history browser | VS Code Marketplace |

---

## See Also

**Internal:**
- [Configuration Reference](./CLAUDE-CODE-CONFIG.md) - Settings, hooks, plugins
- [Claude Code Setup](../setup-guides/CLAUDE-CODE-SETUP.md) - Installation

**External:**
- [Official Memory Docs](https://code.claude.com/docs/en/memory) - CLAUDE.md hierarchy
- [Hidden Conversation History Guide](https://kentgigger.com/posts/claude-code-conversation-history) - Community guide
- [GitHub Issue #5024](https://github.com/anthropics/claude-code/issues/5024) - Storage bloat discussion

---

**Sources**: This guide is based on observation of Claude Code 2.0.61 (December 2025) and community research. Internal formats are not officially documented and may change.
