# Documentation Audit Log

Tracking the ongoing effort to genericize `ai-dev-templates` for public sharing.

## Why

This repo is a **general-purpose template library** — reusable patterns for AI-assisted development that could be shared with anyone. It grew out of real production use at EPCVIP, which means the docs accumulated organizational specifics: internal service names, production URLs, team context, personal workflows. A reader outside the organization would hit references that don't help them and break the illusion of a portable template library.

**End state**: Every doc reads as "here's how to do X with Claude Code" — not "here's how our team does X."

---

## Completed Passes

### Pass 1 — Surface-Level Fixes
**Date**: January 2026
**Scope**: ~10 files (railway docs)
**What**: Fixed broken links, stale dates, outdated URLs. Pure housekeeping.

### Pass 2 — Retired Project Names
**Date**: January 2026
**Scope**: 7 railway doc files
**What**: Removed references to retired/renamed projects that no longer existed in railway docs.

### Pass 3 — Personal Projects + Domains/Versions
**Date**: February 2026
**Scope**: 17 files repo-wide
**What**: Removed personal project references, fixed domain references, updated stale version numbers across the repo (not just railway docs).

### Pass 4 — Genericize Railway Docs
**Date**: February 15, 2026
**Scope**: 10 railway doc files + railway CLAUDE.md + 1 file relocation

**What**: Stripped all organizational specifics from railway docs so they work as standalone deployment guides.

| Reference Type | Count Removed | Action |
|----------------|---------------|--------|
| "EPCVIP" org name | 45 | Removed or replaced with "your team" / generic |
| `.epcvip.vip` URLs | 25 | Replaced with `your-app.example.com` or placeholders |
| Specific service names | 59 | Replaced with generic names (`my-api`, descriptive labels) |
| Service inventory tables | 3 | Removed (operational content) |
| Migration status trackers | 2 | Removed (operational tracking) |

**Files modified**: RAILWAY_OVERVIEW.md, RAILWAY_MCP_GUIDE.md, RAILWAY_BUILDER_MIGRATION.md, README.md (railway), RAILWAY_QUICKSTART.md, RAILWAY_TROUBLESHOOTING.md, RAILWAY_CONFIG_REFERENCE.md, RAILWAY_NEXTJS.md, RAILWAY_SETUP_GUIDE.md, CLAUDE.md (railway)

**File relocated**: `docs/setup-guides/OBSIDIAN-WSL-SETUP.md` → `~/repos-epcvip/docs/epcvip-docs-obsidian/` (hardcoded personal vault paths, not template content)

**Verification**: 0 EPCVIP references, 0 `.epcvip.vip` URLs, 0 specific service names remaining in `docs/railway/`.

### Pass 5 — Repo-Wide Genericization + Secrets Scan
**Date**: February 15, 2026
**Scope**: ~20 files (8 relocated/deleted, 9 genericized, 3 reference updates)

**What**: Final pass to address remaining ~109 organizational references across ~18 files outside railway docs. Also documented a git history secrets scan.

**Git History Secrets Scan**: **CLEAN**. No real API keys, tokens, passwords, or private keys were ever committed. All key/token references in history are placeholders (`eyJ...`, `your-...-here`, `xxxxx`) or documentation examples.

| Action | Files | Details |
|--------|-------|---------|
| **Relocated** | 8 | EPCVIP_DESIGN_SYSTEM.md → epcvip-docs (org branding), cross-repo-consolidation/ (6 files) → epcvip-docs-obsidian (internal planning), CUSTOM-INSTRUCTIONS-README.md → epcvip-docs-obsidian (personal AI config) |
| **Deleted** | 2 | templates/testing/STATUS.md, templates/testing/AUDIT_2026-02.md (operational tracking, served their purpose) |
| **Genericized** | 9 | SUPABASE-SETUP-GUIDE.md, SUPABASE-CODE-PATTERNS.md, AUTH-TROUBLESHOOTING.md, NEW-PC-SETUP.md, CLAUDE-CODE-SETUP.md, MULTI-DEVICE-WORKSPACE.md, MCP-DECISION-TREES.md, CLAUDE-CODE-STORAGE.md, BACKLOG_MIGRATION_PLAN.md |
| **Reference cleanup** | 6 | Removed stale links to deleted files from testing README, CI README, PLAYWRIGHT_CLAUDE_GUIDE, PLAYWRIGHT_CLI_EVALUATION, COST_OPTIMIZATION_GUIDE, BROWSER_AUTOMATION_LANDSCAPE_2026, PLAYWRIGHT-MCP |

**Verification**: Near-zero EPCVIP references remaining in template content. Only AUDIT_LOG.md (this file) retains references for historical context.

### Pass 6 — Three-Layer Restructuring
**Date**: February 15, 2026
**Scope**: Entire repo structure

**What**: Separated the repo into three distinct layers — private (personal configs, research), templates (public patterns), and docs (public guides). Created a nested git repo (`_private/`) that's structurally invisible to the parent repo.

| Action | Details |
|--------|---------|
| **Created** | `_private/` as nested git repo (`ahhhdum/ai-dev-private`) |
| **Moved** | `personal/` (19 files) → `_private/personal/` |
| **Moved** | `research/` (11 files) → `_private/research/{methodology,audit-findings,audit-research}/` |
| **Created** | `_private/research/SOURCES.md` — master source registry |
| **Created** | `_private/research/intake/` — chronological research intake log |
| **Created** | `_private/workflow/` — personal AI workflow preferences (4 stubs) |
| **Updated** | `.gitignore` — replaced `personal/` + `research/` entries with `_private/` |
| **Added** | Pre-commit hook (`scripts/hooks/pre-commit`) blocking `_private/` staging |
| **Deleted** | `.projects/fresh-repo-deployment/` (empty) |
| **Updated** | `CLAUDE.md`, `README.md` — documented three-layer system |

**Verification**: `git status` shows no `_private/` files. `_private/` has independent git history with all 37 files committed and pushed to private remote.

### Pass 7 — Content Polish for Team Sharing
**Date**: February 15, 2026
**Scope**: 11 files (content quality, broken links, stale metadata, personal references)

**What**: Final content polish fixing ~25 issues that would confuse a first-time team reader.

| Category | Count | Details |
|----------|-------|---------|
| **Broken links** | 3 | Removed references to non-existent `context-management/` directory (README.md x2, permissions/README.md x1) |
| **Stale counts** | 2 | Fixed slash command count (13→9 active), deprecated count (7→8) |
| **Personal username** | 10 | Replaced `adams` with `YOUR_USERNAME` across 5 files (why-wsl, DAILY-WORKFLOW, NEW-PC-SETUP, WSL-PATHS, CLAUDE-CODE-STORAGE) |
| **Personal metadata** | 4 | Removed "Created: September 2024", "Your September 2024 setup", personal plan file path, "Personal development workflow" |
| **Org-specific refs** | 2 | Changed `DOIS` grep pattern to `APP`, replaced `utilities/ping-tree-compare/` reference with `templates/auth/` |

**Files modified**: README.md, CLAUDE.md, templates/permissions/README.md, docs/decisions/why-wsl.md, docs/setup-guides/DAILY-WORKFLOW.md, docs/setup-guides/NEW-PC-SETUP.md, docs/reference/WSL-PATHS.md, docs/reference/CLAUDE-CODE-STORAGE.md, docs/railway/RAILWAY_WORKFLOWS.md, docs/setup-guides/LOCAL-NETWORK-SHARING.md, _BACKLOG.md

**Verification**: `grep -ri "adams" docs/ templates/` returns zero results. `grep -r "context-management" .` returns zero results outside `_deprecated/`.

---

## Remaining Work

The genericization and content polish effort is complete. The repo is ready for team sharing.

Remaining organizational references are limited to:

- **AUDIT_LOG.md** (this file) — intentionally retains org name for historical context
- **Repo-root CLAUDE.md** — guides Claude Code within this specific repo (repo-specific by nature)

### What stays org-specific (intentionally)

- Repo-root `CLAUDE.md` — guides Claude Code within this specific repo
- `AUDIT_LOG.md` — historical record of the audit process

---

## Principles

1. **Config patterns are generic** — railway.toml examples, CLI references, automation scripts stay as-is
2. **Org context is not generic** — service inventories, production URLs, team-specific framing gets removed
3. **Relocate, don't delete** — content that's useful but org-specific moves to the right repo (e.g., Obsidian guide → epcvip-docs-obsidian)
4. **A reader with no org context should be able to follow every guide** — the litmus test for "done"
