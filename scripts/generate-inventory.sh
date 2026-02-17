#!/usr/bin/env bash
# Generate _FILE_INVENTORY.md — a complete file inventory with metadata for audit use.
# Usage: bash scripts/generate-inventory.sh
# Output: _FILE_INVENTORY.md (gitignored)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

OUTPUT="_FILE_INVENTORY.md"
TODAY=$(date +%Y-%m-%d)
BLOAT_THRESHOLD=400
STALE_MONTHS=3
STALE_CUTOFF=$(date -d "$STALE_MONTHS months ago" +%Y-%m-%d 2>/dev/null || date -v-${STALE_MONTHS}m +%Y-%m-%d)

# Collect all public .md files
mapfile -t FILES < <(find . -name "*.md" \
  -not -path "./_private/*" \
  -not -path "./.git/*" \
  -not -path "./node_modules/*" \
  -not -name "_FILE_INVENTORY.md" \
  | sed 's|^\./||' \
  | sort)

TOTAL_FILES=${#FILES[@]}
TOTAL_LINES=0

# Arrays for audit flags
declare -a LARGE_FILES=()
declare -a STALE_FILES=()
declare -a NO_HEADING_FILES=()

# Collect per-file metadata
declare -A FILE_LINES
declare -A FILE_TITLE
declare -A FILE_DATE
declare -A FILE_MSG
declare -A FILE_DIR

for f in "${FILES[@]}"; do
  lines=$(wc -l < "$f")
  FILE_LINES["$f"]=$lines
  TOTAL_LINES=$((TOTAL_LINES + lines))

  # Extract title: first markdown heading (any level)
  title=$(grep -m1 '^#' "$f" | sed 's/^#\+ *//' | sed 's/ *$//')
  if [[ -z "$title" ]]; then
    title="(no heading)"
    NO_HEADING_FILES+=("$f")
  fi
  FILE_TITLE["$f"]=$title

  # Git metadata
  commit_date=$(git log --format="%cd" --date=short -1 -- "$f" 2>/dev/null || echo "unknown")
  commit_msg=$(git log --format="%s" -1 -- "$f" 2>/dev/null || echo "")
  # Truncate commit message to 60 chars
  if [[ ${#commit_msg} -gt 60 ]]; then
    commit_msg="${commit_msg:0:57}..."
  fi
  FILE_DATE["$f"]=$commit_date
  FILE_MSG["$f"]=$commit_msg

  # Directory grouping
  dir=$(dirname "$f")
  if [[ "$dir" == "." ]]; then
    dir="(root)"
  fi
  FILE_DIR["$f"]=$dir

  # Audit flags
  if [[ $lines -gt $BLOAT_THRESHOLD ]]; then
    LARGE_FILES+=("$f ($lines lines)")
  fi
  if [[ "$commit_date" != "unknown" && "$commit_date" < "$STALE_CUTOFF" ]]; then
    STALE_FILES+=("$f (last: $commit_date)")
  fi
done

# Get unique directories in sorted order
mapfile -t DIRS < <(for f in "${FILES[@]}"; do echo "${FILE_DIR[$f]}"; done | sort -u)

# Find top 5 largest files
mapfile -t TOP_LARGE < <(
  for f in "${FILES[@]}"; do
    echo "${FILE_LINES[$f]} $f"
  done | sort -rn | head -5
)

# Find top 5 oldest files
mapfile -t TOP_OLD < <(
  for f in "${FILES[@]}"; do
    [[ "${FILE_DATE[$f]}" != "unknown" ]] && echo "${FILE_DATE[$f]} $f"
  done | sort | head -5
)

# Format total lines with commas
format_number() {
  echo "$1" | sed ':a;s/\B[0-9]\{3\}\>/,&/;ta'
}

# --- Generate output ---

{
  echo "# File Inventory"
  echo ""
  echo "Auto-generated on $TODAY. Run \`bash scripts/generate-inventory.sh\` to refresh."
  echo ""
  echo "## Summary"
  echo ""
  echo "- **Total files**: $TOTAL_FILES"
  echo "- **Total lines**: $(format_number $TOTAL_LINES)"
  echo ""
  echo "### Largest Files"
  echo ""
  for entry in "${TOP_LARGE[@]}"; do
    lines=$(echo "$entry" | awk '{print $1}')
    file=$(echo "$entry" | awk '{print $2}')
    echo "- \`$file\` — $lines lines"
  done
  echo ""
  echo "### Oldest Files (by last git commit)"
  echo ""
  for entry in "${TOP_OLD[@]}"; do
    date_val=$(echo "$entry" | awk '{print $1}')
    file=$(echo "$entry" | awk '{print $2}')
    echo "- \`$file\` — $date_val"
  done
  echo ""
  echo "---"
  echo ""
  echo "## By Directory"
  echo ""

  for dir in "${DIRS[@]}"; do
    # Collect files in this directory
    dir_files=()
    dir_lines=0
    for f in "${FILES[@]}"; do
      if [[ "${FILE_DIR[$f]}" == "$dir" ]]; then
        dir_files+=("$f")
        dir_lines=$((dir_lines + FILE_LINES[$f]))
      fi
    done

    echo "### $dir (${#dir_files[@]} files, $(format_number $dir_lines) lines)"
    echo ""
    echo "| File | Lines | Last Modified | Commit | Title |"
    echo "|------|------:|:------------:|--------|-------|"

    for f in "${dir_files[@]}"; do
      basename=$(basename "$f")
      echo "| $basename | ${FILE_LINES[$f]} | ${FILE_DATE[$f]} | ${FILE_MSG[$f]} | ${FILE_TITLE[$f]} |"
    done
    echo ""
  done

  echo "---"
  echo ""
  echo "## Audit Flags"
  echo ""
  echo "### Large Files (>$BLOAT_THRESHOLD lines)"
  echo ""
  if [[ ${#LARGE_FILES[@]} -eq 0 ]]; then
    echo "None."
  else
    for entry in "${LARGE_FILES[@]}"; do
      echo "- \`$entry\`"
    done
  fi
  echo ""
  echo "### Stale Files (no edits since $STALE_CUTOFF)"
  echo ""
  if [[ ${#STALE_FILES[@]} -eq 0 ]]; then
    echo "None."
  else
    for entry in "${STALE_FILES[@]}"; do
      echo "- \`$entry\`"
    done
  fi
  echo ""
  echo "### No Heading"
  echo ""
  if [[ ${#NO_HEADING_FILES[@]} -eq 0 ]]; then
    echo "None."
  else
    for entry in "${NO_HEADING_FILES[@]}"; do
      echo "- \`$entry\`"
    done
  fi

} > "$OUTPUT"

echo "Generated $OUTPUT"
echo "  $TOTAL_FILES files, $(format_number $TOTAL_LINES) total lines"
echo "  ${#LARGE_FILES[@]} large, ${#STALE_FILES[@]} stale, ${#NO_HEADING_FILES[@]} no heading"
