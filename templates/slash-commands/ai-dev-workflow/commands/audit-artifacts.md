---
description: Evaluate and archive temporary markdown files - thorough cleanup when context allows
allowed-tools: read_file, write_file, edit_file, run_terminal_cmd, grep, glob_file_search
argument-hint: (optional: directory to audit, defaults to project root)
---

## Purpose

Deep analysis and cleanup of markdown files created during development.

**Use this when**:
- Context is comfortable (<100K tokens, plenty of headroom)
- After running `/session-handoff` (freed up context)
- Want thorough cleanup of exploratory documents
- Before starting new major phase

**This command will**:
1. 🔍 Scan all markdown files in project
2. 📋 Evaluate each against your documentation structure
3. 💬 Show recommendations with reasoning
4. ✅ Archive approved candidates
5. 📊 Report context savings

**Note**: Requires moderate context (40-60K tokens) for thorough evaluation. If context is tight, run `/session-handoff` first.

---

## Evaluation Framework

### Core Documents (NEVER Archive)

These are intentional, permanent documentation:

```bash
# Core project docs
CLAUDE.md
README.md
TASKS.md
tasks.md
TODO.md
HANDOFF.md
FEATURES_BACKLOG.md
CHANGELOG.md
CONTRIBUTING.md

# Package/project metadata
package.json
requirements.txt
go.mod
Cargo.toml
pyproject.toml
```

### Organized Documentation (NEVER Archive)

Files in structured locations are intentional:

```bash
docs/                      # Documentation folder
.projects/                 # Project organization system
features/                  # Feature specifications
architecture/              # Architecture docs
decisions/                 # ADR (Architecture Decision Records)
```

### Candidates for Evaluation

Files that MAY be temporary/exploratory:

```bash
# Root directory markdown (unorganized)
ANALYSIS_*.md
APPROACH_*.md
PLAN_*.md
SESSION_NOTES_*.md
debug-*.md
exploration-*.md
research-*.md
notes-*.md
scratch-*.md
temp-*.md

# Generic names (often temporary)
test.md
draft.md
ideas.md
brainstorm.md
```

---

## Step 1: Scan Project for Markdown Files

Find all markdown files and categorize:

```bash
echo "🔍 SCANNING FOR MARKDOWN FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Find all markdown files
ALL_MD=$(find . -name "*.md" -type f ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/venv/*" ! -path "*/dist/*" ! -path "*/build/*" 2>/dev/null)

# Count total
TOTAL_MD=$(echo "$ALL_MD" | wc -l)
echo "Total markdown files found: $TOTAL_MD"
echo ""

# Categorize files
echo "📂 CATEGORIZATION:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

### 1.1 Identify Core Documents

```bash
# Core files (never archive)
CORE_FILES=("CLAUDE.md" "README.md" "TASKS.md" "tasks.md" "TODO.md" "HANDOFF.md" "FEATURES_BACKLOG.md" "CHANGELOG.md" "CONTRIBUTING.md")

echo "✅ Core Documents (NEVER Archive):"
for file in "${CORE_FILES[@]}"; do
  if [ -f "$file" ]; then
    LINES=$(wc -l < "$file")
    echo "   $file ($LINES lines)"
  fi
done
echo ""
```

### 1.2 Identify Organized Documentation

```bash
# Files in structured locations
ORGANIZED=$(echo "$ALL_MD" | grep -E "^\./(docs|\.projects|features|architecture|decisions)/" 2>/dev/null)

if [ -n "$ORGANIZED" ]; then
  ORGANIZED_COUNT=$(echo "$ORGANIZED" | wc -l)
  echo "✅ Organized Documentation (Keep):"
  echo "   $ORGANIZED_COUNT files in structured folders"
  echo "$ORGANIZED" | head -10 | sed 's/^/   /'
  if [ "$ORGANIZED_COUNT" -gt 10 ]; then
    echo "   ... and $(($ORGANIZED_COUNT - 10)) more"
  fi
  echo ""
fi
```

### 1.3 Identify Archive Candidates

```bash
# Root directory markdown (potential candidates)
ROOT_MD=$(echo "$ALL_MD" | grep -E "^\./[A-Z_-]+\.md$" | grep -v -E "(CLAUDE|README|TASKS|TODO|HANDOFF|FEATURES_BACKLOG|CHANGELOG|CONTRIBUTING)\.md")

if [ -n "$ROOT_MD" ]; then
  CANDIDATE_COUNT=$(echo "$ROOT_MD" | wc -l)
  echo "⚠️  Archive Candidates Found:"
  echo "   $CANDIDATE_COUNT files to evaluate"
  echo ""
fi
```

---

## Step 2: Evaluate Each Candidate

For each candidate file, apply the evaluation framework:

### Evaluation Criteria

**Question 1: Is it referenced in core docs?**
```bash
# Check if file is linked from CLAUDE.md, README.md, TASKS.md, HANDOFF.md
grep -l "[FILENAME]" CLAUDE.md README.md TASKS.md HANDOFF.md 2>/dev/null
```
- ✅ **Referenced** → Keep (part of active system)
- ❌ **Not referenced** → Continue evaluation

**Question 2: How recent is it?**
```bash
# Check last modification time
find [FILENAME] -mmin -120  # Modified in last 2 hours?
```
- ✅ **Recent (< 2 hours)** → Keep (active work)
- ⚠️ **Older (2-24 hours)** → Possible candidate
- ❌ **Old (> 24 hours)** → Strong candidate

**Question 3: Does it duplicate existing docs?**
- Manual review: Does content overlap with plan.md, ARCHITECTURE.md, etc.?
- ✅ **Unique** → Keep
- ❌ **Duplicates** → Archive candidate

**Question 4: Is it exploratory/temporary?**
- Filename patterns: ANALYSIS_*, APPROACH_*, debug-*, research-*
- Content patterns: Multiple approaches compared, brainstorming, scratch notes
- ✅ **Final/reference** → Keep
- ❌ **Exploratory** → Archive candidate

### Evaluation Output Format

For each candidate, show:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANDIDATE: [filename]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Location: [path]
📏 Size: [X lines]
🕐 Last modified: [timestamp] ([X hours/days ago])
🔗 Referenced by: [files that link to it, or "None"]

📝 Content Preview (first 10 lines):
[show first 10 lines]

🔍 Analysis:
├─ Reference check: [✅ Referenced / ❌ Not referenced]
├─ Recency: [✅ Recent / ⚠️ Moderate / ❌ Old]
├─ Pattern: [ANALYSIS_* / APPROACH_* / debug-* / generic]
└─ Duplication: [Would require manual review to confirm]

❓ Assessment Questions:
1. Is this information still needed?
2. Has the decision/exploration been completed?
3. Is the content duplicated elsewhere?
4. Does this serve a current purpose?

💡 Recommendation: [Archive / Keep / Review Manually]

Reason: [1-2 sentence explanation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 3: Present Recommendations

After analyzing all candidates, present summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 AUDIT SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total markdown files: [X]
├─ Core documents: [X] (never archive)
├─ Organized docs: [X] (keep)
└─ Candidates evaluated: [X]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🗑️  ARCHIVE (Strong recommendation):
1. [filename1] ([X] lines) - [Reason]
2. [filename2] ([X] lines) - [Reason]
3. [filename3] ([X] lines) - [Reason]

Total lines to archive: [Y]
Estimated token reduction: ~[Z] tokens

⚠️  REVIEW MANUALLY (Uncertain):
1. [filename4] ([X] lines) - [Why uncertain]
2. [filename5] ([X] lines) - [Why uncertain]

✅ KEEP (Referenced or active):
1. [filename6] - [Referenced in TASKS.md]
2. [filename7] - [Modified <2 hours ago]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to do?

[1] Archive all recommended files (safe, reversible)
[2] Review each recommendation individually
[3] Archive only [specific files] (enter numbers)
[4] Skip archiving, just show report
[Q] Quit without changes

Your choice: _
```

---

## Step 4: Archive Approved Files

Based on user selection:

### Option 1: Archive All Recommended

```bash
# Create archive directory
ARCHIVE_DIR="./archive/audit-$(date +%Y%m%d-%H%M)"
mkdir -p "$ARCHIVE_DIR"

# Archive each recommended file
for file in [RECOMMENDED_FILES]; do
  echo "Archiving: $file"
  mv "$file" "$ARCHIVE_DIR/"
done

# Create index
cat > "$ARCHIVE_DIR/README.md" <<'EOF'
# Archived Markdown Files

**Archive Date**: [Timestamp]
**Reason**: Routine artifact audit
**Command**: /audit-artifacts

## Files Archived

[List each file with reason]

## How to Restore

If you need any of these files back:
```bash
cp archive/audit-[TIMESTAMP]/[filename] ./
```

## Archive Criteria

Files were archived if:
- Not referenced in core docs (CLAUDE.md, README.md, TASKS.md, HANDOFF.md)
- Older than 24 hours
- Exploratory/temporary nature (ANALYSIS_*, APPROACH_*, debug-*)
- Duplicated information from other docs

EOF
```

### Option 2: Review Each Individually

```bash
# For each recommended file, ask:
for file in [RECOMMENDED_FILES]; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "FILE: $file"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Show details again
  echo "Size: $(wc -l < $file) lines"
  echo "Modified: $(stat -c %y $file)"
  echo "Preview:"
  head -10 "$file"
  echo "..."

  echo ""
  echo "Archive this file?"
  echo "[Y]es / [N]o / [V]iew full content / [Q]uit: "

  # User responds for each file
done
```

### Option 3: Archive Specific Files

```bash
# User enters: 1,3,5 (archive files 1, 3, and 5 from list)
# Archive only those files
```

---

## Step 5: Report Results

After archiving:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AUDIT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Archive Location:
└─ archive/audit-[TIMESTAMP]/

🗑️  Files Archived: [X]
├─ [filename1] ([Y] lines)
├─ [filename2] ([Y] lines)
└─ [filename3] ([Y] lines)

📊 Context Optimization:
├─ Total lines removed: [Z]
├─ Estimated token reduction: ~[N] tokens
└─ Reduction percentage: ~[X]%

✅ Remaining Active Files:
├─ Core documents: [X]
├─ Organized docs: [X]
└─ Active work files: [X]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Archive Index:
All archived files documented in:
└─ archive/audit-[TIMESTAMP]/README.md

🔄 To Restore Files:
If you need any archived file:
```bash
cp archive/audit-[TIMESTAMP]/[filename] ./
```

💡 Next Steps:
- Continue working (context optimized)
- Run /session-handoff when ready to end session
- Archived files preserved if needed later

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Common Patterns to Recognize

### Exploratory Documents (Often Archive)

**ANALYSIS_*.md**:
- Created during exploration phase
- Compare multiple approaches
- Decision already made and documented elsewhere
- **Archive if**: Decision documented in plan.md or TASKS.md

**APPROACH_*.md**:
- Evaluate different implementation strategies
- Pros/cons comparison
- Final decision recorded
- **Archive if**: Implementation begun, approach chosen

**debug-*.md**:
- Debugging session notes
- Error traces
- Investigation steps
- **Archive if**: Bug fixed, issue resolved

**research-*.md**:
- Library/API research
- Feature investigation
- Learning notes
- **Archive if**: Research complete, decision made

### Legitimate Active Documents (Keep)

**plan.md** (in .projects/ or docs/):
- Current project plan
- Architecture decisions
- Active reference
- **Keep**: Core project doc

**ARCHITECTURE.md**:
- System design
- Component relationships
- Technical decisions
- **Keep**: Core reference

**api-spec.md** (if referenced):
- API contract
- Endpoint definitions
- Used by multiple tasks
- **Keep**: Active reference

---

## Anti-Patterns to Watch For

### False Positives (Don't Archive)

**Recent work documents**:
- Modified in last 2 hours
- Actively being worked on
- May have temporary names but serving current purpose

**Referenced documents**:
- Linked from TASKS.md or HANDOFF.md
- Part of current workflow
- Even if name suggests "temporary"

**Unique information**:
- Contains decisions not documented elsewhere
- Has implementation details needed later
- Source of truth for specific area

### False Negatives (Should Archive)

**Stale exploration**:
- Created days/weeks ago
- Decision made and documented elsewhere
- Never referenced

**Duplicate content**:
- Information available in plan.md or other docs
- Created "just in case" but never needed
- Redundant with organized documentation

---

## Safety Features

### Reversible

All archiving is reversible:
- Files moved to timestamped archive folder
- Original structure preserved
- Easy to restore if needed

### Non-Destructive

No files deleted:
- Archives kept indefinitely
- Can reference later if needed
- Index documents what was archived and why

### Conservative Defaults

When uncertain:
- Recommend "Review Manually"
- Don't auto-archive edge cases
- User makes final decision

---

## Integration with Session Workflow

### Typical Workflow

```bash
# Context getting full (140K tokens)
/session-handoff
# → Archives completed work, simplifies TASKS.md
# → Creates HANDOFF.md
# → Result: ~100K tokens

# Now have context headroom for thorough cleanup
/audit-artifacts
# → Deep analysis of markdown files
# → Archive exploratory documents
# → Result: ~80K tokens

# Continue working with optimized context
```

### Standalone Usage

Can also run independently:
```bash
# Just want to clean up artifacts
/audit-artifacts

# No handoff needed, just removing clutter
```

---

## Quality Checklist

Before completing, verify:
- [ ] All markdown files scanned
- [ ] Core documents identified (never archived)
- [ ] Organized docs identified (kept)
- [ ] Candidates evaluated with framework
- [ ] Recommendations shown with reasoning
- [ ] User confirmed each archive decision
- [ ] Files moved to timestamped archive
- [ ] Archive index created (README.md)
- [ ] Results reported with token savings

---

Markdown artifacts audited! 🎉

