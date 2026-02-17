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

### Pass 8 — Content Audit (see _private/research/)
**Date**: February 15, 2026
**Scope**: Research and content quality review
**What**: Deep content audit of template quality, accuracy, and completeness. Findings documented in `_private/research/audit-findings/`.

### Pass 9 — File Inventory + Quality Audit
**Date**: February 15, 2026
**Scope**: All 135 public .md files (repo-wide)

**What**: Created an auto-generated file inventory tool, then used it to surface and fix staleness, orphan, and bloat issues.

**Tooling created**:
- `scripts/generate-inventory.sh` — Scans all public `.md` files and generates `_FILE_INVENTORY.md` with per-file metadata (path, lines, title, git date, commit message), per-directory tables, summary stats, and audit flags (large/stale/no-heading)
- `_FILE_INVENTORY.md` — Auto-generated output (gitignored, local audit tool)

**Inventory stats**: 135 files, 41,961 total lines across 28 directories

| Category | Findings | Action |
|----------|----------|--------|
| **Staleness** | Railway CLI version hardcoded as "4.5.5" (2 locations) | Replaced with `railway --version` instruction |
| **Orphans fixed** | 5 files not linked from any navigation surface | Added links to appropriate READMEs/CLAUDE.md |
| **Orphans relocated** | 1 operational file (BACKLOG_MIGRATION_PLAN.md, 611 lines) | Moved to `_private/workflow/` (org-specific migration plan) |

**Orphan links added**:
- `docs/auth/SUPABASE-CODE-PATTERNS.md` → added to `docs/auth/README.md`
- `docs/setup-guides/LOCAL-NETWORK-SHARING.md` → added to root `CLAUDE.md`
- `templates/ci/DECISION_FRAMEWORK.md` → added to `templates/ci/README.md`
- `templates/ci/STATUS.md` → added to `templates/ci/README.md`
- `templates/features-backlog/FEATURES_BACKLOG.md` → added to `templates/features-backlog/README.md`

**Bloat assessment** (35 files >400 lines):
- 4 files appropriately long (reference docs): HOOKS_REFERENCE.md (1,240), RAILWAY_AUTOMATION.md (776), RAILWAY_WORKFLOWS.md (735), RAILWAY_CONFIG_REFERENCE.md (676)
- 5 files flagged for future trimming: standards/README.md (867), hooks/README.md (832), projects/README.md (775), permissions/README.md (702), RAILWAY_TROUBLESHOOTING.md (879)
- Remaining 26 are deprecated commands, setup guides, or config references where length is justified

**Files modified**: RAILWAY_CLI_REFERENCE.md, docs/auth/README.md, templates/ci/README.md, templates/features-backlog/README.md, CLAUDE.md, .gitignore

**Files created**: scripts/generate-inventory.sh, _FILE_INVENTORY.md (gitignored)

**Files relocated**: BACKLOG_MIGRATION_PLAN.md → `_private/workflow/`

### Pass 10 — Un-deprecate Slash Commands + Bloat Trimming
**Date**: February 15, 2026
**Scope**: 12 file moves, 7 files modified, 2 minor fixes

**What**: Reversed incorrect deprecation of 12 slash commands (7 general + 5 audit lenses) and condensed 5 bloated README files. The repo's purpose is to demonstrate BOTH custom commands and built-in alternatives with tradeoff documentation.

**Phase 1: Un-deprecate slash commands**:

| Action | Details |
|--------|---------|
| **Moved** | 7 files from `commands/_deprecated/` → `commands/` |
| **Moved** | 5 files from `commands/_deprecated/audit/` → `commands/audit/` (new directory) |
| **Deleted** | Empty `_deprecated/` and `_deprecated/audit/` directories |
| **Rewrote** | `templates/slash-commands/README.md` — unified 21-command listing by workflow phase, added Custom Commands vs Built-in Features comparison table, removed "Plugins > Slash Commands" framing |
| **Reframed** | `templates/slash-commands/DESIGN_RATIONALE.md` V4 section — changed from "deprecation decisions" to "alternatives identified" with tradeoffs |

**Phase 2: Trim 5 bloated files** (verbose multi-option explanations → comparison tables):

| File | Before | After | Savings | Key Changes |
|------|-------:|------:|--------:|-------------|
| templates/standards/README.md | 867 | 183 | 684 | Template walkthrough → table reference, 3 language examples → table + 1, troubleshooting → table |
| templates/hooks/README.md | 832 | 248 | 584 | Hook examples → table, 3 installation patterns → table + 1 example, 5 practices → table + 1 canonical example, troubleshooting → table |
| docs/railway/RAILWAY_TROUBLESHOOTING.md | 879 | 249 | 630 | Merged health check + port mismatch, deployment/database/cron issues → tables + 1 example each |
| templates/projects/README.md | 775 | 206 | 569 | 3 storage options → comparison table, AI patterns → table + 1 example, 3 real-world examples → 1 detailed |
| templates/permissions/README.md | 702 | 168 | 534 | 7 categories → table, 3 strategies → table + 1 example, 4 language examples → table |
| **Total** | **4,055** | **1,054** | **3,001** | |

**Phase 3: Minor fixes**:
- Moved "Enhanced Security Hooks" from "In Progress" to "Completed" in `_BACKLOG.md`
- Updated CLAUDE.md: fixed slash command count (9 → 21), removed deprecated framing

**Verification**: `ls commands/_deprecated/` fails (gone). `commands/` has 16 files + `audit/` directory with 5 files. Zero "deprecated" references in slash-commands README. ~3,001 lines trimmed across 5 files (4,055 → 1,054).

---

### Pass 11 — Skills Audit + Research
**Date**: February 15, 2026
**Scope**: All 34 SKILL.md files across repos (22 unique skills), article research on Skills open standard

**What**: Comprehensive audit of all Claude Code skills against the new Skills open standard (Anthropic Oct 2025). Stored article research, built complete inventory, interviewed user on workflow and priorities, audited each skill against 8 criteria, applied fixes, and documented a major redesign brief.

**Phase 1: Research stored** (3 files in `_private/research/`):

| File | Purpose |
|------|---------|
| `intake/2026-02-15-skills-standard-article.md` | Article intake log (key takeaways, verdict: Adopt) |
| `audit-research/skills-standard-best-practices.md` | Deep-dive reference: skill anatomy, progressive disclosure, description best practices, advanced patterns, gap analysis |
| `SOURCES.md` | Added skills.sh CLI + vercel-labs/agent-skills to source registry |

**Phase 2: User interview** — classified all 22 skills into priority tiers:

| Tier | Skills | Decision |
|------|--------|----------|
| **Flagship** | code-review pipeline, backlog-management, dev-server | Ship to coworkers as templates |
| **Active personal** | A/B testing suite (8 skills), image, porting-artifacts, sync-team-docs | Improve later, domain-specific |
| **Stale** | data-platform-assistant-fix-init-crash copies | Ignore |

**Phase 3: Inventory** — `_private/research/audit-findings/skills-inventory-2026-02.md`:
- 34 SKILL.md files across 4 layers (global, per-repo, template library, stale)
- 22 unique skills (12 global, 10 per-repo)
- Backlog skills duplicated across 4 repos (potential drift)

**Phase 4: Audit** — `_private/research/audit-findings/skills-audit-2026-02.md`:

8 criteria from the article (frontmatter, trigger phrases, outcome, instructions, examples, troubleshooting, progressive disclosure, no org-specific):

| Finding | Count | Action |
|---------|-------|--------|
| Missing YAML frontmatter | 4 skills | Fixed |
| No troubleshooting section | 22/22 skills | Noted, add to flagships in future pass |
| Thin descriptions (no triggers) | ~8 skills | Fixed for 4 missing-frontmatter skills |
| Progressive disclosure underused | 17/22 skills | Noted for future improvement |

**Phase 5: Fixes applied**:

| Action | Details |
|--------|---------|
| **Frontmatter added** | 4 skills: `database-review`, `mockup` (global), `format-test-readme`, `check-readme-standards` — all now have name + rich description with trigger phrases |
| **Template created** | `templates/plugins/SKILL-TEMPLATE.md` — canonical template with description checklist, progressive disclosure guide, testing instructions |
| **README updated** | `templates/plugins/README.md` — added backlog-management to available plugins, rewrote "Creating New Plugins" to reference SKILL-TEMPLATE.md |

**Phase 6: Code review redesign brief** — `_private/research/audit-findings/code-review-redesign-brief.md`:

Detailed brief for merging 3 skills (local-code-review + evaluate-code-review + root-cause-analysis) into a unified skill. Captures user's pain points (90% false positive rate, 3-skill sequential workflow, shallow analysis), proposed architecture, artifacts to preserve, and success criteria. Deferred to dedicated session.

---

### Pass 12 — Unified Code Review Skill
**Date**: February 15, 2026
**Scope**: 8 template files (2 created, 4 rewritten, 2 updated), 4 global skills modified, 1 global skill created

**What**: Merged 3 sequential skills (local-code-review + evaluate-code-review + root-cause-analysis) into a single unified `code-review` skill with a 5-phase pipeline: gather changes → run agents → evaluate findings → root-cause analysis → output.

**Problem**: The old 3-skill pipeline required running `/local-review` → `/evaluate-review` → `/root-cause` manually in sequence, with a ~90% false positive rate from the agent phase because agents reported findings without reading source files or tracing execution paths.

**Solution**: Unified skill with guardrails (NEVER/ALWAYS rules), agent self-evaluation (confidence >= 70 to report), built-in false-positive filtering (Phase 3), and automatic root-cause categorization (Phase 4).

**Phase 1: New reference files created**:

| File | Source | Purpose |
|------|--------|---------|
| `references/false-positive-patterns.md` | Extracted from `evaluate-code-review` SKILL.md | 3-question evaluation framework, common false positives by category, verdict definitions |
| `references/bug-categories.md` | Extracted from `root-cause-analysis` SKILL.md | 6 bug categories, root-cause heuristics, simple vs complex output templates, don't-over-engineer guardrails |

**Phase 2: Template files rewritten/updated**:

| File | Action | Key Changes |
|------|--------|-------------|
| `SKILL.md` | **Rewritten** | 5-phase pipeline, guardrails section, `--quick`/`--full` modes, evaluation + root-cause built in |
| `references/agent-personas.md` | **Updated** | Added self-evaluation protocol (all agents), per-agent pre-reporting checklist, confidence scoring, updated merging to include evaluation phase |
| `README.md` | **Rewritten** | Pipeline diagram, unified agent table, updated docs table |
| `METHODOLOGY.md` | **Rewritten** | Added self-evaluation protocol, built-in evaluation phase, root-cause integration, quick vs full comparison |
| `SKILL-INSTALLATION.md` | **Rewritten** | Migration guide from old 3-skill pipeline, before/after comparison, removal instructions |
| `plugins/README.md` | **Updated** | Unified plugin entry, updated install command, replaced `/local-review-lite` with `--quick` |

**Phase 3: Global skills**:

| Action | Location | Details |
|--------|----------|---------|
| **Created** | `~/.claude/skills/code-review/` | Full unified skill with all references |
| **Deprecated** | `~/.claude/skills/local-code-review/` | Deprecation notice pointing to unified skill |
| **Deprecated** | `~/.claude/skills/local-code-review-lite/` | Deprecation notice pointing to `--quick` flag |
| **Deprecated** | `~/.claude/skills/evaluate-code-review/` | Deprecation notice pointing to Phase 3 |
| **Deprecated** | `~/.claude/skills/root-cause-analysis/` | Deprecation notice pointing to Phase 4 |

**Key design decisions**:
- Kept `/local-review` as trigger name (avoids conflict with `pr-review-toolkit` plugin)
- Guardrails pattern from skillmaxxer-3000 (NEVER/ALWAYS rules) over hooks — enforces depth without build-time tooling
- `--quick` replaces `--lite` for consistency with `--full`
- Did not add `model: opus` to frontmatter (not a supported field) — guardrails force deeper analysis regardless
- Deprecated old skills with pointers rather than deleting — allows gradual migration

**Verification**: Unified `code-review` skill visible in Claude Code skills list. Old skills show "DEPRECATED" in description. All reference files present in both template and global locations.

---

### Pass 13 — Backlog Management Consolidation
**Date**: February 16, 2026
**Scope**: 17 files moved/created, 10 files updated, 3 directories removed, 2 files retired

**What**: Evaluated the backlog management ecosystem (~3,300 lines across 3 overlapping categories) against Claude Code's native Tasks (v2.1, Jan 2025) and Session Memory (v2.1.30+, Feb 2026). Consolidated three separate template categories into one unified `project-management/` directory with an honest comparison to built-in features.

**Key finding**: Native Tasks (TaskCreate/TaskList/TaskGet/TaskUpdate) replaces basic task tracking. Custom system's unique value is effort calibration, YAML frontmatter schema, `.projects/` cross-session pattern, and Python utilities for duplicate detection and indexing. The 3 backlog skills are the weakest component — they duplicate functionality native Tasks now handles and have auto-trigger reliability issues.

**Phase 1: Directory consolidation**:

| Old Location | New Location | Action |
|-------------|-------------|--------|
| `templates/features-backlog/` | `templates/project-management/backlog/` | Moved |
| `templates/projects/` | `templates/project-management/projects/` | Moved |
| `templates/plugins/backlog-management/` | `templates/project-management/skills/` | Moved |

**Phase 2: Files retired**:

| File | Lines | Reason |
|------|-------|--------|
| `FEATURES_BACKLOG.md` | 247 | Overlapped with `_BACKLOG.md` — tier definitions merged in |
| `folder-based/WORKFLOW.md` | 176 | Content duplicated across 3 other files |

**Phase 3: New content created**:

| File | Lines | Purpose |
|------|-------|---------|
| `templates/project-management/README.md` | ~200 | Unified entry point with decision table, 4 patterns, migration paths |

**Phase 4: Skills updated per Skills open standard**:
- All 3 backlog skills: rich multi-line `description` with trigger phrases, `## Troubleshooting` sections (2-3 entries each), native Tasks comparison note
- Skills README: rewritten with honest positioning ("Do you need these?"), auto-trigger reliability note, unique-value framing

**Phase 5: BUILTIN_VS_CUSTOM.md overhauled**:
- Replaced all `TodoWrite` references with native Tasks (TaskCreate/TaskList/TaskGet/TaskUpdate)
- Added "Native Tasks vs Custom Backlog" comparison table
- Added Session Memory (v2.1.30+) for cross-session context
- Reframed "Plugins > Slash Commands" to "Skills vs Slash Commands" (each has strengths)
- Updated date from January to February 2026

**Phase 6: Cross-references updated** (10 files):
- `CLAUDE.md` — consolidated categories 5+6 → "5. Project & Task Management", renumbered 7-9, count 10→9
- `templates/README.md` — rewritten category table (11→9), updated Quick Start links
- `templates/plugins/README.md` — removed backlog-management entry, added redirect note
- `README.md` (root) — updated Browse Templates and Common Tasks sections
- `docs/getting-started/NEW-PROJECT-SETUP.md` — updated copy paths and See Also
- `docs/decisions/BUILTIN_VS_CUSTOM.md` — updated all See Also links
- `docs/reference/CLAUDE-CODE-STORAGE.md` — TodoWrite → Task
- `templates/slash-commands/README.md` — TodoWrite → Native Tasks
- `templates/slash-commands/DESIGN_RATIONALE.md` — TodoWrite → Native Tasks

**Verification**: `templates/features-backlog/`, `templates/projects/`, `templates/plugins/backlog-management/` no longer exist. All cross-references point to new `templates/project-management/` locations. Zero TodoWrite references in decision/template docs.

---

### Pass 14 — ADVANCED-WORKFLOWS Expansion
**Date**: February 16, 2026
**Scope**: 3 files (ADVANCED-WORKFLOWS.md, CLAUDE.md, README.md)

**What**: Expanded the power-user conceptual guide from 4 sections (272 lines) to 7 sections (386 lines), then removed volatile specifics in a follow-up sub-pass.

**Phase 1: Content expansion** (ADVANCED-WORKFLOWS.md):

| Section | Status | Key Additions |
|---------|--------|---------------|
| 1. Context Management | Expanded | MCP context costs, skill description budget, avoid list, compact-by-work-type, official 95% compaction trigger |
| 2. Planning | **NEW** | Temporary vs durable plans, good plan elements, mandatory cleanup phases |
| 3. Agents | Expanded | Sub-agent nesting limitation, cost awareness, model selection guidance |
| 4. Extension Points | **NEW** | Conceptual overview of skills, hooks, MCP (hidden context costs), plugins |
| 5. Predictability | Expanded | Scoped diffs, structured output expectations |
| 6. Claude Code vs Codex | Expanded | Strategic comparison with current data (was 3 bullets) |
| 7. Meta-Level Principles | **NEW** | 5 crystallized takeaways distilled from guide |

**Phase 2: Volatile specifics removal** (Pass 14b):

| Removed | Reason |
|---------|--------|
| Model versions (GPT-5.3-Codex) | Outdated within months |
| Dollar pricing ($20-200/mo) | Changes frequently |
| SWE-bench scores | Benchmark-specific, changes per release |

Reframed model selection from cost-first ("default to cheapest") to stakes-based ("match model to stakes"). Kept durable tier names (haiku/sonnet/opus).

**Files modified**: ADVANCED-WORKFLOWS.md, CLAUDE.md, README.md

---

### Pass 15 — README Orientation & Platform Framing
**Date**: February 16, 2026
**Scope**: 2 files (README.md, CLAUDE.md)

**What**: Improved first-impression clarity for new readers and reduced platform-specific assumptions.

| Change | Details |
|--------|---------|
| **Value prop opening** | README.md now opens with what the repo is and why it matters |
| **Slash command counts** | Fixed 3 conflicting counts (9, 13 → all now 21) |
| **WSL framing** | Renamed architecture header to "Windows Power Setup: WSL2 (Optional)" |
| **Platform annotations** | Common Issues table rows labeled with (Windows/WSL) where applicable |
| **Utility scripts** | Platform-annotated (perf, obs labeled as Windows-only) |
| **CLAUDE.md** | Clarified secondary purpose: platform-agnostic first, WSL optional |

**Files modified**: README.md, CLAUDE.md

---

### Pass 16 — Shareability Cleanup
**Date**: February 16, 2026
**Scope**: 12 files (1 relocated, 11 modified)

**What**: Final pass addressing personal content, prescriptive framing, and broken links that would confuse team readers or external users.

| Category | Count | Details |
|----------|-------|---------|
| **Personal content relocated** | 1 | NEW-PC-SETUP.md → `_private/personal/` (Dell Precision specs, personal RAM allocation) |
| **`_private/` references removed** | 5 | Repository Layers section, 2× `_private/research/` refs, README note — all from CLAUDE.md and README.md |
| **Org-specific names generalized** | 1 | "ping-tree-compare, dois-processor" → "production FastAPI services, data processors" in CLAUDE.md |
| **Personal → team language** | 3 | why-wsl.md: "my workflow" → "when WSL makes sense", "my specific use case" → "teams that need Linux-speed file I/O" |
| **Prescriptive framing softened** | 2 | DAILY-WORKFLOW.md: added platform-agnostic intro. MULTI-DEVICE-WORKSPACE.md: added alternatives note, simplified architecture diagram |
| **Broken links fixed** | 2 | COMMANDS.md → DEVELOPMENT-ENVIRONMENT.md (removed). MULTI-DEVICE-WORKSPACE.md → JOURNAL.md (replaced with generic text) |
| **Incoming links updated** | 12 | All references to removed NEW-PC-SETUP.md redirected to SETUP-GUIDE-2026.md or Microsoft WSL docs |

**Files modified**: CLAUDE.md, README.md, _BACKLOG.md, why-wsl.md, CLAUDE-CODE-QUICKSTART.md, SETUP-GUIDE-2026.md, COMMANDS.md, CURSOR-WSL-SETUP.md, DAILY-WORKFLOW.md, MULTI-DEVICE-WORKSPACE.md, _FILE_INVENTORY.md (gitignored)

**File relocated**: docs/setup-guides/NEW-PC-SETUP.md → `_private/personal/`

**Verification**: Zero `NEW-PC-SETUP` references in public docs (outside AUDIT_LOG.md). Zero `_private/` references in CLAUDE.md. Zero "my workflow"/"my specific" in why-wsl.md. Zero broken links to DEVELOPMENT-ENVIRONMENT.md or JOURNAL.md.

---

### Pass 17 — Trim Bloated Hub READMEs
**Date**: February 16, 2026
**Scope**: 4 files modified, 1 file created

**What**: Trimmed two hub documents that exceeded the repo's own 150-200 line recommendation. The CLAUDE.md guidelines README was 2.4x the target; the query validation README was 3.2x.

**Phase 1: claude-md/README.md** (488 → ~130 lines):

| Section | Action | Savings |
|---------|--------|--------:|
| Files in Template Library | 89-line descriptions → 4-row table | ~74 |
| The Bloat Problem | 23 lines → 3-line summary + link | ~18 |
| Lightweight Philosophy | 20 lines → 2-line summary + link | ~16 |
| What Belongs vs What Doesn't | Removed (duplicates GUIDELINES) | ~27 |
| Code Quality + Examples | 54 lines → hub-and-spoke pattern | ~40 |
| Refactoring Workflow | 46 lines → 5-line overview + link | ~40 |
| Enforcement & Maintenance | 24 lines → 5 lines + link | ~17 |
| Common Questions | 63 lines → 1-line link to GUIDELINES FAQ | ~60 |
| Evidence & Sources | 18 lines → 5 lines | ~13 |

**Phase 2: CLAUDE-MD-GUIDELINES.md** (appended ~50 lines):
- Added `## Maintenance` section: team agreement template, quarterly checklist, pre-commit hook
- Added `## FAQ` section: 4 condensed Q&As (line limits, complex projects, separate docs, cross-tool)

**Phase 3: hooks/query-validation/README.md** (632 → ~290 lines):

| Section | Action | Savings |
|---------|--------|--------:|
| Installation Steps 3-5 | Condensed to single "Reload and Verify" section | ~40 |
| Customization | Extracted to CUSTOMIZATION.md | ~89 |
| FAQ (92 lines) | Merged relevant items into Troubleshooting, removed rest | ~80 |
| Integration with Other Tools | Condensed | ~15 |

**New file**: `templates/hooks/query-validation/CUSTOMIZATION.md` (~100 lines) — per-database patterns, custom runners, whitelist commands, marker location, content-based validation

**Files modified**: `templates/claude-md/README.md`, `templates/claude-md/CLAUDE-MD-GUIDELINES.md`, `templates/hooks/query-validation/README.md`, `_BACKLOG.md`, `AUDIT_LOG.md`
**Files created**: `templates/hooks/query-validation/CUSTOMIZATION.md`

**Verification**: `wc -l` shows README targets met. All internal links valid. No content lost — everything condensed in place or linked to new location.

---

## Remaining Work

### Dev Server Skill Genericization

Genericize the dev-server skill for the template library. Currently has hardcoded repo-specific startup sequences. See `_BACKLOG.md` P1 item.

### Future improvements (lower priority)

- Add `## Troubleshooting` sections to remaining non-flagship skills
- Add `backlog-start` to template library (exists in fwaptile-wordle only)
- Enhance descriptions on remaining non-flagship skills
- Evaluate `allowed-tools` frontmatter for sensitive skills
- Remaining `ping-tree-compare` references in template case studies (4 files) — acceptable as concrete examples but could be genericized in a future pass

Run `bash scripts/generate-inventory.sh` to refresh the full file inventory.

### What stays org-specific (intentionally)

- `AUDIT_LOG.md` — historical record of the audit process

---

## Principles

1. **Config patterns are generic** — railway.toml examples, CLI references, automation scripts stay as-is
2. **Org context is not generic** — service inventories, production URLs, team-specific framing gets removed
3. **Relocate, don't delete** — content that's useful but org-specific moves to the right repo (e.g., Obsidian guide → epcvip-docs-obsidian)
4. **A reader with no org context should be able to follow every guide** — the litmus test for "done"
