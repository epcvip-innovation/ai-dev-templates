# Claude Code Utility Scripts

This directory contains Python utility scripts that enforce consistent behavior for Claude Code slash commands.

**Why utilities?** Claude can sometimes ignore markdown instructions (e.g., "use grep only" but reads full file anyway). Python scripts programmatically enforce the correct behavior, making workflows predictable and testable.

---

## Available Utilities

### 1. `feature_discovery.py` - Discover Active Features

**Purpose:** Find active features from .active-features file (primary) or FEATURES_BACKLOG.md using grep (fallback). Validates HANDOFF.md status.

**Usage:**
```bash
python3 .claude/utils/feature_discovery.py
```

**Output Format:**
```json
{
  "count": 2,
  "active_features": [
    {
      "name": "session-based-auth",
      "remaining_hours": 12,
      "blocked": true,
      "status_summary": "Railway deployment issue"
    },
    {
      "name": "query-reorganization",
      "remaining_hours": 3,
      "blocked": false,
      "status_summary": "Ready for Phase 3"
    }
  ]
}
```

**Key Features:**
- ✅ Uses .active-features file (primary) for fast discovery (50-300 tokens)
- ✅ Falls back to grep on FEATURES_BACKLOG.md if .active-features missing
- ✅ Enforces grep-only discovery (can't accidentally read full FEATURES_BACKLOG.md)
- ✅ Parses grep output into structured JSON
- ✅ Returns feature count for smart prompting logic
- ✅ Validates HANDOFF.md Status line format

**Used by:**
- `/resume-feature` - Step 2 (feature discovery)
- `/session-handoff` - To identify current feature
- `/feature-complete` - To find features to mark complete

**Error Handling:**
- Returns `{"count": 0, "active_features": []}` if no features found
- Returns `{"count": 0, "error": "..."}` if FEATURES_BACKLOG.md missing

---

### 2. `handoff_loader.py` - Load Selected Feature Context

**Purpose:** Load ONLY the selected feature's HANDOFF.md and plan.md (prevents loading all features).

**Usage:**
```bash
python3 .claude/utils/handoff_loader.py <feature-name>
```

**Example:**
```bash
python3 .claude/utils/handoff_loader.py session-based-auth
```

**Output Format:**
```json
{
  "feature_name": "session-based-auth",
  "handoff_content": "...",
  "plan_content": "...",
  "files_loaded": [
    "docs/planning/features/session-based-auth/HANDOFF.md",
    "docs/planning/features/session-based-auth/plan.md"
  ],
  "lines_loaded": 911,
  "status_valid": true,
  "status_warning": null
}
```

**Key Features:**
- ✅ Loads only selected feature (not all active features)
- ✅ Prefers plan.md, falls back to README.md
- ✅ Returns line count for context awareness
- ✅ Validates HANDOFF.md Status line format
- ✅ Context savings: ~50% reduction (1 feature vs all features)

**Used by:**
- `/resume-feature` - Step 4 (after user selects feature)
- `/check-drift` - To load current state
- `/session-handoff` - To load feature for handoff update

**Error Handling:**
- Returns `{"error": "Feature directory not found"}` if feature doesn't exist
- Returns `{"error": "No HANDOFF.md or plan.md found"}` if files missing
- Still returns partial data if one file exists

---

### 3. `plan_validator.py` - Validate Plan Without Rubric

**Purpose:** Run the 3 boolean validation checks without loading PLAN_QUALITY_RUBRIC.md.

**Usage:**
```bash
python3 .claude/utils/plan_validator.py <feature-name>
```

**Example:**
```bash
python3 .claude/utils/plan_validator.py session-based-auth
```

**Output Format:**
```json
{
  "feature_name": "session-based-auth",
  "category": "valid",
  "checks": {
    "goal_unchanged": true,
    "dependencies_met": true,
    "approach_sound": true
  },
  "issues": [],
  "recommendation": "Continue with current plan"
}
```

**Categories:**
- `"valid"` - All checks pass, continue with plan
- `"update"` - 1 check fails, update plan.md to reflect changes
- `"invalid"` - Multiple checks fail, run /replan-feature

**Key Features:**
- ✅ Lightweight boolean checks (not full rubric analysis)
- ✅ Never loads PLAN_QUALITY_RUBRIC.md (saves ~50 lines)
- ✅ Compares plan.md vs HANDOFF.md for drift
- ✅ Returns actionable recommendations

**Used by:**
- `/resume-feature` - Step 4.5 (plan validation)
- `/check-drift` - Quick validation before detailed analysis
- `/feature-complete` - Verify plan was followed

**Error Handling:**
- Returns `{"category": "invalid", "error": "..."}` if feature not found
- Assumes "valid" if no HANDOFF.md exists (early in feature)

---

### 4. `active_features_manager.py` - Manage Active Features Index

**Purpose:** Manages .active-features index file (add, remove, list, is-active operations).

**Usage:**
```bash
python3 .claude/utils/active_features_manager.py add "feature-name"
python3 .claude/utils/active_features_manager.py remove "feature-name"
python3 .claude/utils/active_features_manager.py list
python3 .claude/utils/active_features_manager.py is-active "feature-name"
```

**Output Format:**
```json
{
  "success": true,
  "message": "Added 'feature-name' to active features",
  "features": ["feature-name"]
}
```

**Key Features:**
- ✅ Auto-maintains .active-features index file
- ✅ Validates feature directory exists before adding
- ✅ Returns JSON for machine parsing
- ✅ Used by `/start-feature` and `/feature-complete`

**Used by:**
- `/start-feature` - Adds feature to index when starting
- `/feature-complete` - Removes feature from index when completing

---

## Testing Utilities

**Test discovery:**
```bash
cd /path/to/project
python3 .claude/utils/feature_discovery.py
```

**Test loader:**
```bash
# Replace with actual feature name from your project
python3 .claude/utils/handoff_loader.py query-reorganization
```

**Test validator:**
```bash
python3 .claude/utils/plan_validator.py query-reorganization
```

**Test manager:**
```bash
python3 .claude/utils/active_features_manager.py list
```

**Expected output:** Well-formed JSON with expected fields

---

## Integration with Slash Commands

### Before (Markdown-only instructions)
```markdown
## Step 2: Find active features

Use grep to find features:
```bash
grep -A 2 "🚧 In Progress" docs/planning/FEATURES_BACKLOG.md
```

Parse the output and identify features...
```

**Problem:** Claude might ignore instructions and read full file instead.

### After (Python utility enforcement)
```markdown
## Step 2: Discover Active Features

**Run discovery script:**
```bash
python3 .claude/utils/feature_discovery.py
```

**Parse JSON output** - feature count and details provided in structured format.
```

**Benefit:** Claude MUST run the script, which enforces grep-only behavior programmatically.

---

## Design Principles

1. **Enforcement over suggestions** - Python scripts enforce correct behavior (can't be ignored)
2. **Structured output** - JSON for reliable parsing by Claude
3. **Error handling** - Scripts return errors as JSON (no exceptions to stderr)
4. **Minimal dependencies** - Only stdlib (subprocess, json, pathlib, re)
5. **Testable** - Can run scripts standalone for debugging
6. **Reusable** - Multiple commands use same utilities
7. **Backward compatible** - Graceful fallbacks when files missing

---

## File Locations

**Utilities location:**
```
.claude/utils/
├── feature_discovery.py    (~300 lines)
├── handoff_loader.py        (~180 lines)
├── plan_validator.py        (~310 lines)
├── active_features_manager.py (~265 lines)
└── README.md                (this file)
```

**Project root detection:**
All scripts automatically find project root by looking for `.claude/` directory, so they work from any subdirectory.

---

## Active Features Index

The `.active-features` file at the project root serves as a lightweight index of features currently in progress:

```
.active-features                 # Auto-maintained index (DO NOT EDIT MANUALLY)
.claude/utils/
└── active_features_manager.py   # CLI tool for managing the index
```

**Purpose:** Minimize context usage during feature discovery (50-300 tokens vs 1000+ with grep).

**How it works:**
1. `/start-feature` automatically adds features to the index
2. `/feature-complete` automatically removes them
3. Feature discovery reads this file first (fallback to FEATURES_BACKLOG.md grep if missing)

**Manual management (if needed):**
```bash
# List active features
python3 .claude/utils/active_features_manager.py list

# Check if a feature is active
python3 .claude/utils/active_features_manager.py is-active "feature-name"

# Manually add (rarely needed)
python3 .claude/utils/active_features_manager.py add "feature-name"

# Manually remove (rarely needed)
python3 .claude/utils/active_features_manager.py remove "feature-name"
```

---

## HANDOFF.md Status Requirement

For feature discovery to work correctly, **HANDOFF.md files MUST include a Status line in the first 10 lines:**

```markdown
# Handoff: [Feature Name]

**Last Updated**: [Date/Time]
**Session**: [Session number or description]
**Status**: [Brief status - e.g., "Phase 2 in progress", "Ready to start Phase 3"]

## Quick Resume (Read This First)
...
```

The `**Status:**` line is validated by `.claude/utils/feature_discovery.py` and `.claude/utils/handoff_loader.py`. If missing or malformed, you'll receive a warning (not an error - validation only, no auto-fixing).

---

## Future Enhancements

**Potential additions:**
- `task_estimator.py` - Estimate effort for new tasks (for /add-task)
- `drift_analyzer.py` - Detailed drift analysis (for /check-drift)
- `test_utilities.py` - Unit tests for all utilities
- `backlog_manager.py` - Add/update features in FEATURES_BACKLOG.md

**Extension to other workflows:**
- Query validation utilities
- Documentation generation utilities
- Git commit message formatters

---

## Troubleshooting

### Script not found
```bash
# Error: No such file or directory: .claude/utils/feature_discovery.py
```

**Solution:** Scripts must be run from project root or a subdirectory. Check that `.claude/utils/` exists.

### Permission denied
```bash
# Error: Permission denied
```

**Solution:** Make scripts executable:
```bash
chmod +x .claude/utils/*.py
```

Or run with `python3` explicitly:
```bash
python3 .claude/utils/feature_discovery.py
```

### JSON parsing errors in Claude
```bash
# Claude says "Failed to parse JSON output"
```

**Solution:** 
1. Run script manually to check output format
2. Check for print statements that pollute JSON output
3. Ensure script only prints JSON to stdout

### Feature not found
```bash
# Output: {"error": "Feature directory not found: ..."}
```

**Solution:** Check feature name spelling and that feature exists in `docs/planning/features/`

---

## Contributing

When adding new utilities:
1. Follow the same structure (find_project_root, main function, JSON output)
2. Add error handling (return errors as JSON, not exceptions)
3. Document in this README with usage examples
4. Update "Used by" sections for relevant commands
5. Test standalone before integrating into commands

---

**Last Updated:** 2025-01-16
**Related:** See `.claude/commands/ai-dev-workflow/` for slash commands that use these utilities

