# Backlog Standardization Migration Plan

**Created:** 2026-01-08
**Purpose:** Migrate 6 repositories to a standardized backlog system
**Status:** PLANNING - Needs questions answered before execution

---

## Table of Contents

1. [Methodology](#methodology)
2. [Current State Audit](#current-state-audit)
3. [Target Standard](#target-standard)
4. [Migration Tasks by Repository](#migration-tasks-by-repository)
5. [Execution Order](#execution-order)
6. [Validation Checklist](#validation-checklist)
7. [Questions to Answer](#questions-to-answer-before-execution)
8. [Supporting Documentation](#supporting-documentation)

---

## Methodology

### Discovery Process

1. **File Discovery** - Used `glob_file_search` for `*BACKLOG*.md` and `**/planning/**` patterns
2. **Reference Analysis** - Used `grep` to find all files referencing backlog paths
3. **CLAUDE.md Analysis** - Read each repo's CLAUDE.md to understand documentation structure
4. **Slash Command Audit** - Examined `.claude/commands/` folders for feature workflow commands
5. **Python Utility Audit** - Checked `.claude/utils/` for hardcoded paths

### Migration Principles

1. **Consolidate duplicates** - Each repo should have ONE primary backlog
2. **Standardize location** - All backlogs at `docs/planning/FEATURES_BACKLOG.md`
3. **Update all references** - CLAUDE.md, slash commands, Python utilities
4. **Create redirects** - Old locations should point to new location
5. **Preserve history** - Don't lose backlog content during migration
6. **Template first** - Update the template repo before migrating others

---

## Current State Audit

### Summary Table

| Repo | Backlog Location(s) | Has Duplicates | Slash Commands | Python Utils | Complexity |
|------|---------------------|----------------|----------------|--------------|------------|
| data-platform-assistant | `docs/planning/BACKLOG.md` + `docs/planning/FEATURES_BACKLOG.md` | YES | 14+ commands | 4 utilities | HIGH |
| tools-hub | `BACKLOG.md` (root) + `tools/BACKLOG.md` | YES | 5 commands | None | HIGH |
| athena-usage-monitor-fastapi | `BACKLOG.md` (root) | No | None | None | LOW |
| engagement-analysis | `planning/BACKLOG.md` (wrong location) | No | None | None | MEDIUM |
| experimentation-toolkit | NONE | N/A | None | None | LOW |
| ai-dev-templates | `templates/features-backlog/FEATURES_BACKLOG.md` | No | 14+ template commands | None | LOW |

### Detailed Findings

#### 1. data-platform-assistant

**Files Found:**
- `docs/planning/BACKLOG.md` (330 lines) - Scheduled Reports System backlog
- `docs/planning/FEATURES_BACKLOG.md` (410 lines) - Main features backlog

**References Found (67 files total):**
- 14 slash commands in `.claude/commands/ai-dev-workflow/commands/`
- 4 Python utilities in `.claude/utils/`:
  - `feature_discovery.py` line 155: hardcoded to `docs/planning/FEATURES_BACKLOG.md`
  - `active_features_manager.py` line 86: hardcoded to `docs/planning/features/`
  - `handoff_loader.py`
  - `plan_validator.py`
- `CLAUDE.md` references `docs/planning/DOIS_MIGRATION.md`

**Key Slash Commands:**
- `start-feature.md` - Line 16-17: reads `docs/planning/FEATURES_BACKLOG.md`
- `resume-feature.md` - Uses `feature_discovery.py`
- `feature-complete.md` - Updates `FEATURES_BACKLOG.md`

#### 2. tools-hub

**Files Found:**
- `BACKLOG.md` (743 lines) - Main backlog with P0-P3 priority + T-shirt sizing
- `tools/BACKLOG.md` (161 lines) - Map editor specific backlog

**References Found (10 files):**
- `.claude/commands/start-feature.md` line 9: reads `BACKLOG.md`
- `CLAUDE.md` line 64: references `BACKLOG.md`
- `STANDARDS.md`, `TECH_DEBT.md`, various docs

**Slash Commands:**
- `audit.md`
- `lint.md`
- `push.md`
- `review-recent.md`
- `start-feature.md` - NEEDS UPDATE

#### 3. athena-usage-monitor-fastapi

**Files Found:**
- `BACKLOG.md` (41 lines) - Simple backlog with Priority/Effort text

**References Found (2 files):**
- `CLAUDE.md` line 144: "See `BACKLOG.md` for planned features"

**No .claude folder** - No slash commands to update

#### 4. engagement-analysis

**Files Found:**
- `planning/BACKLOG.md` (102 lines) - P2-P3 table format
- `planning/HEALTH_SCORECARD_DESIGN.md`
- `planning/archive/`

**References Found (2 files):**
- `CLAUDE.md` line 160: references `planning/HEALTH_SCORECARD_DESIGN.md`

**Note:** Uses `planning/` instead of standard `docs/planning/`

**No .claude folder** - No slash commands to update

#### 5. experimentation-toolkit

**Files Found:**
- NO BACKLOG FILE EXISTS
- Has `docs/planning/features/test-intake-slash-command/README.md`

**Structure Exists:**
- `docs/planning/features/` directory already exists
- Missing: `FEATURES_BACKLOG.md` and `_TEMPLATE.md`

**CLAUDE.md:**
- Comprehensive (513 lines)
- References test INDEX.md files
- No backlog reference

#### 6. ai-dev-templates (Template Repo)

**Files Found:**
- `templates/features-backlog/FEATURES_BACKLOG.md` (248 lines) - THE TEMPLATE
- `templates/features-backlog/README.md`

**Slash Command Templates (14 commands):**
All in `templates/slash-commands/ai-dev-workflow/commands/`:
- `start-feature.md` - References `docs/planning/FEATURES_BACKLOG.md` (CORRECT)
- `resume-feature.md`
- `feature-complete.md`
- `session-handoff.md`
- `validate-plan.md`
- `add-task.md`
- `check-drift.md`
- `plan-approaches.md`
- `ai-review.md`
- `debug-failure.md`
- `audit-artifacts.md`
- `align-project-docs.md`
- `audit-claude-md.md`
- `help.md`

**Key File:** `WORKFLOW_GUIDE.md` documents the standard structure

---

## Target Standard

### File Structure

```
repo/
├── docs/
│   └── planning/
│       ├── FEATURES_BACKLOG.md    # Single source of truth
│       ├── archive/               # Completed feature docs
│       └── features/
│           ├── _TEMPLATE.md       # Feature plan template
│           └── [feature-name]/    # One folder per major feature
│               ├── README.md      # Lightweight plan (Tier 1)
│               ├── plan.md        # Full spec (Tier 2+)
│               └── HANDOFF.md     # Session continuity
```

### Backlog Format

```markdown
# Features Backlog - [Project Name]

**Last Updated:** YYYY-MM-DD
**Active Features:** [count]
**Completed This Month:** [count]

---

## 🚧 In Progress

### Feature Name
**Status:** 🚀 In Progress (Phase X)
**Priority:** P1
**Effort:** Xh total, Yh done (Z%)
**Value:** [One sentence impact]

**Current Focus:** [What's being worked on]

**Blockers:** None OR [description]

---

## 🔴 P1 - High Priority (This Sprint)

### Feature Name
**Priority:** P1
**Effort:** X-Yh
**Value:** [Impact statement]

**Problem:** [What pain point]
**Solution:** [Proposed approach]

---

## 🟡 P2 - Medium Priority (Next 2-4 Weeks)

## 🟢 P3 - Low Priority (Backlog)

## ⏸️ P4 - On Hold / Blocked

---

## ✅ Recently Completed

### Feature Name (YYYY-MM-DD)
**Effort:** Xh actual (vs Yh estimated)
**Impact:** [Brief outcome]
```

### Priority System

| Priority | Meaning | Timeline | Emoji |
|----------|---------|----------|-------|
| P0 | Critical/Blocker | Immediate | 🔴 |
| P1 | High value, should do | This sprint | 🔴 |
| P2 | Important, plan for | 2-4 weeks | 🟡 |
| P3 | Nice to have | When time allows | 🟢 |
| P4 | On hold/Blocked | Needs resolution | ⏸️ |

---

## Migration Tasks by Repository

### 1. ai-dev-templates (DO FIRST)

**Goal:** Update the template that defines the standard

**Tasks:**
1. Update `templates/features-backlog/FEATURES_BACKLOG.md` with standardized format
2. Verify `WORKFLOW_GUIDE.md` reflects the standard
3. Create `templates/features-backlog/MIGRATION_GUIDE.md` for adoption

**Files to Modify:**
- `templates/features-backlog/FEATURES_BACKLOG.md`
- `templates/slash-commands/ai-dev-workflow/WORKFLOW_GUIDE.md`

**Files to Create:**
- `templates/features-backlog/MIGRATION_GUIDE.md`

---

### 2. data-platform-assistant

**Goal:** Consolidate duplicate backlogs

**Tasks:**
1. DECISION NEEDED: Merge or keep separate backlogs?
   - Option A: Merge `BACKLOG.md` content into `FEATURES_BACKLOG.md`
   - Option B: Rename `BACKLOG.md` to `SCHEDULED_REPORTS_BACKLOG.md`
2. Delete or redirect old file
3. Verify all 14 slash commands reference correct path (should already be correct)
4. Verify all 4 Python utilities reference correct path (should already be correct)

**Files to Modify:**
- `docs/planning/FEATURES_BACKLOG.md` (if merging)
- `docs/planning/BACKLOG.md` (delete or rename)

**Reference Check Commands:**
```bash
grep -r "BACKLOG.md" tools/data-platform-assistant/.claude/
grep -r "FEATURES_BACKLOG" tools/data-platform-assistant/.claude/
```

---

### 3. experimentation-toolkit

**Goal:** Create missing backlog file

**Tasks:**
1. Create `docs/planning/FEATURES_BACKLOG.md` with initial content
2. Create `docs/planning/features/_TEMPLATE.md`
3. Update `CLAUDE.md` to add backlog reference in "Repo Organization" section

**Initial Content Sources:**
- `tests/ping-tree/INDEX.md` - Test registry
- `tests/scs/INDEX.md`
- `CLAUDE.md` mentions of planned work
- `docs/planning/features/test-intake-slash-command/README.md`

**Files to Create:**
- `docs/planning/FEATURES_BACKLOG.md`
- `docs/planning/features/_TEMPLATE.md`

**Files to Modify:**
- `CLAUDE.md` (add backlog reference)

---

### 4. athena-usage-monitor-fastapi

**Goal:** Move backlog to standard location

**Tasks:**
1. Create `docs/planning/` directory structure
2. Move `BACKLOG.md` → `docs/planning/FEATURES_BACKLOG.md`
3. Reformat content to standard format
4. Update `CLAUDE.md` line 144
5. Create redirect at old location

**Files to Create:**
- `docs/planning/FEATURES_BACKLOG.md`
- `docs/planning/features/_TEMPLATE.md`

**Files to Modify:**
- `CLAUDE.md` line 144

**Files to Delete/Redirect:**
- `BACKLOG.md` (create redirect notice)

---

### 5. engagement-analysis

**Goal:** Restructure planning folder to standard location

**Tasks:**
1. Create `docs/` directory
2. Move entire `planning/` → `docs/planning/`
3. Rename `BACKLOG.md` → `FEATURES_BACKLOG.md`
4. Create `docs/planning/features/_TEMPLATE.md`
5. Update `CLAUDE.md` line 160 (planning path)
6. Add backlog reference to `CLAUDE.md`

**Files to Move:**
- `planning/BACKLOG.md` → `docs/planning/FEATURES_BACKLOG.md`
- `planning/HEALTH_SCORECARD_DESIGN.md` → `docs/planning/HEALTH_SCORECARD_DESIGN.md`
- `planning/archive/` → `docs/planning/archive/`

**Files to Create:**
- `docs/planning/features/_TEMPLATE.md`

**Files to Modify:**
- `CLAUDE.md` (update planning references)

---

### 6. tools-hub (MOST COMPLEX)

**Goal:** Consolidate duplicates and update all references

**Tasks:**
1. Create `docs/planning/` directory structure
2. DECISION NEEDED: How to handle `tools/BACKLOG.md`?
   - Option A: Merge into main backlog
   - Option B: Keep separate as `docs/planning/MAP_EDITOR_BACKLOG.md`
3. Move `BACKLOG.md` → `docs/planning/FEATURES_BACKLOG.md`
4. Move `tools/BACKLOG.md` → `docs/planning/MAP_EDITOR_BACKLOG.md` (if keeping separate)
5. Update `.claude/commands/start-feature.md` line 9
6. Update `CLAUDE.md` lines 64, 147-148
7. Create `docs/planning/features/_TEMPLATE.md`
8. Create redirect notices at old locations

**Files to Create:**
- `docs/planning/FEATURES_BACKLOG.md`
- `docs/planning/features/_TEMPLATE.md`
- `docs/planning/MAP_EDITOR_BACKLOG.md` (if keeping separate)

**Files to Modify:**
- `.claude/commands/start-feature.md` line 9: `BACKLOG.md` → `docs/planning/FEATURES_BACKLOG.md`
- `CLAUDE.md` line 64: Update backlog reference
- `CLAUDE.md` lines 147-148: Update documentation table

**Files to Delete/Redirect:**
- `BACKLOG.md` (create redirect notice)
- `tools/BACKLOG.md` (create redirect notice)

**Critical Update - start-feature.md:**
```markdown
# Current (line 9):
2. `BACKLOG.md` - Feature backlog

# Change to:
2. `docs/planning/FEATURES_BACKLOG.md` - Feature backlog
```

---

## Execution Order

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ai-dev-templates                                         │
│    Update template first - this DEFINES the standard        │
│    Complexity: LOW | Dependencies: None                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. data-platform-assistant                                  │
│    Consolidate duplicates (already has correct structure)   │
│    Complexity: HIGH | Dependencies: Template                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. experimentation-toolkit                                  │
│    Create new backlog (structure exists, file missing)      │
│    Complexity: LOW | Dependencies: Template                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. athena-usage-monitor-fastapi                             │
│    Simple move (no slash commands to update)                │
│    Complexity: LOW | Dependencies: Template                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. engagement-analysis                                      │
│    Restructure planning folder location                     │
│    Complexity: MEDIUM | Dependencies: Template              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. tools-hub                                         │
│    Most complex - duplicates + multiple references          │
│    Complexity: HIGH | Dependencies: Template                │
└─────────────────────────────────────────────────────────────┘
```

---

## Validation Checklist

Run after each repo migration:

### File Structure Check
```bash
# Required files exist
[ -f "docs/planning/FEATURES_BACKLOG.md" ] && echo "✅ Backlog exists" || echo "❌ Missing backlog"
[ -f "docs/planning/features/_TEMPLATE.md" ] && echo "✅ Template exists" || echo "❌ Missing template"
```

### Reference Check
```bash
# No old references remain
grep -r "BACKLOG.md" . --include="*.md" --include="*.py" | grep -v "FEATURES_BACKLOG" | grep -v "node_modules"

# CLAUDE.md points to correct location
grep -n "FEATURES_BACKLOG\|docs/planning" CLAUDE.md
```

### Slash Command Check (if applicable)
```bash
# All commands reference correct path
grep -r "FEATURES_BACKLOG\|docs/planning" .claude/commands/
```

### Full Validation Checklist

- [ ] `docs/planning/FEATURES_BACKLOG.md` exists
- [ ] `docs/planning/features/_TEMPLATE.md` exists
- [ ] CLAUDE.md references `docs/planning/FEATURES_BACKLOG.md`
- [ ] All slash commands reference correct path
- [ ] All Python utilities reference correct path (if applicable)
- [ ] Old files deleted OR have redirect notices
- [ ] No broken links in documentation
- [ ] `grep -r "BACKLOG.md" .` returns no incorrect references

---

## Questions to Answer Before Execution

### Critical Questions (Must Answer)

#### Q1: data-platform-assistant - Duplicate Backlogs
The repo has TWO backlog files:
- `docs/planning/BACKLOG.md` - Scheduled Reports System (330 lines)
- `docs/planning/FEATURES_BACKLOG.md` - Main features (410 lines)

**Options:**
- **A) MERGE** - Add Scheduled Reports as a section in FEATURES_BACKLOG.md
- **B) KEEP SEPARATE** - Rename to `SCHEDULED_REPORTS_BACKLOG.md` 

**Recommendation:** Option B (keep separate) - Scheduled Reports is a distinct subsystem

---

#### Q2: tools-hub - Duplicate Backlogs
The repo has TWO backlog files:
- `BACKLOG.md` (root) - Main backlog (743 lines, Wordle Battle + Overworld)
- `tools/BACKLOG.md` - Map Editor specific (161 lines)

**Options:**
- **A) MERGE** - Add Map Editor as a section in main backlog
- **B) KEEP SEPARATE** - Move to `docs/planning/MAP_EDITOR_BACKLOG.md`

**Recommendation:** Option B (keep separate) - Map Editor is a distinct tool

---

#### Q3: Effort Sizing Standardization
Currently different repos use different effort scales:
- **tools-hub:** T-shirt sizing (XS, S, M, L, XL)
- **Others:** Hours (4-6h, 8-12h, etc.)

**Options:**
- **A) STANDARDIZE TO HOURS** - Convert all to hour estimates
- **B) ALLOW FLEXIBILITY** - Each repo keeps its preferred scale

**Recommendation:** Option B (allow flexibility) - T-shirt sizing works well for tools-hub

---

### Nice-to-Have Questions

#### Q4: Redirect File Content
Should old backlog locations contain:
- **A) DELETE** - Just delete old files
- **B) REDIRECT NOTICE** - Keep file with pointer to new location

**Recommendation:** Option B - Helps anyone using old paths

**Example redirect notice:**
```markdown
# ⚠️ MOVED

This backlog has moved to: `docs/planning/FEATURES_BACKLOG.md`

Please update your bookmarks and references.
```

---

## Supporting Documentation

### Files Referenced in This Plan

| File | Purpose | Read During Audit |
|------|---------|-------------------|
| `tools/data-platform-assistant/CLAUDE.md` | Main repo context | ✅ Full |
| `tools/data-platform-assistant/docs/planning/BACKLOG.md` | Scheduled Reports backlog | ✅ Full |
| `tools/data-platform-assistant/docs/planning/FEATURES_BACKLOG.md` | Main features backlog | ✅ Full |
| `tools/data-platform-assistant/.claude/commands/ai-dev-workflow/commands/start-feature.md` | Feature workflow command | ✅ Full |
| `tools/data-platform-assistant/.claude/utils/feature_discovery.py` | Python utility | ✅ Full |
| `utilities/tools-hub/CLAUDE.md` | Repo context | ✅ Full |
| `utilities/tools-hub/BACKLOG.md` | Main backlog | ✅ Full |
| `utilities/tools-hub/tools/BACKLOG.md` | Map editor backlog | ✅ Full |
| `utilities/tools-hub/.claude/commands/start-feature.md` | Feature workflow command | ✅ Full |
| `utilities/athena-usage-monitor-fastapi/CLAUDE.md` | Repo context | ✅ Full |
| `utilities/athena-usage-monitor-fastapi/BACKLOG.md` | Backlog | ✅ Full |
| `engagement-analysis/CLAUDE.md` | Repo context | ✅ Full |
| `engagement-analysis/planning/BACKLOG.md` | Backlog | ✅ Full |
| `tools/experimentation-toolkit/CLAUDE.md` | Repo context | ✅ Full |
| `templates/ai-dev-templates/CLAUDE.md` | Template repo context | ✅ Full |
| `templates/ai-dev-templates/templates/features-backlog/FEATURES_BACKLOG.md` | Template | ✅ Full |
| `templates/ai-dev-templates/templates/slash-commands/ai-dev-workflow/WORKFLOW_GUIDE.md` | Workflow guide | ✅ Full |
| `templates/ai-dev-templates/templates/slash-commands/ai-dev-workflow/commands/start-feature.md` | Template command | ✅ Full |
| `tools/data-platform-assistant/docs/planning/features/_TEMPLATE.md` | Feature template | ✅ Full |
| `utilities/dois-test-capacity-planner/docs/planning/features/_TEMPLATE.md` | Feature template | ✅ Full |

### Search Commands Used

```bash
# Find all backlog files
glob_file_search "*BACKLOG*.md"

# Find all planning directories
glob_file_search "**/planning/**"

# Find references per repo
grep -r "BACKLOG|FEATURES_BACKLOG|docs/planning|planning/" <repo_path>
```

### Key Path Hardcodes Found

| File | Line | Hardcoded Path |
|------|------|----------------|
| `feature_discovery.py` | 155 | `docs/planning/FEATURES_BACKLOG.md` |
| `active_features_manager.py` | 86 | `docs/planning/features/` |
| `start-feature.md` (dpa) | 16-17 | `docs/planning/FEATURES_BACKLOG.md` |
| `start-feature.md` (hub) | 9 | `BACKLOG.md` |
| `CLAUDE.md` (hub) | 64 | `BACKLOG.md` |
| `CLAUDE.md` (athena) | 144 | `BACKLOG.md` |
| `CLAUDE.md` (engage) | 160 | `planning/HEALTH_SCORECARD_DESIGN.md` |

---

## Next Steps for Executor

1. **Read this entire document** to understand scope
2. **Answer the 3 critical questions** (Q1, Q2, Q3)
3. **Start with ai-dev-templates** (Step 1)
4. **Work through repos in order** (Steps 2-6)
5. **Run validation checklist** after each repo
6. **Commit after each repo** with message: `refactor: standardize backlog to docs/planning/FEATURES_BACKLOG.md`

---

*Last Updated: 2026-01-08*
*Author: Claude Code (Audit Session)*
