#!/usr/bin/env bash
# classify-pr.sh — Reads a risk-policy.json and a list of changed files,
# outputs the highest-severity tier and its required checks.
#
# Usage:
#   classify-pr.sh <policy-file> <changed-files...>
#   echo "src/auth/login.ts src/utils/format.ts" | classify-pr.sh <policy-file>
#
# Output (JSON):
#   { "tier": "critical", "checks": ["security-review", "qa-review"], "evidence_required": true }
#
# Environment:
#   SKIP_RISK_GATE=1  — Override to return "low" tier (escape hatch for urgent hotfixes)
#
# Requires: jq, bash 4+

set -euo pipefail

# --- Escape hatch ---
if [[ "${SKIP_RISK_GATE:-0}" == "1" ]]; then
  echo '{"tier":"low","checks":[],"evidence_required":false,"skipped":true}'
  exit 0
fi

# --- Args ---
POLICY_FILE="${1:?Usage: classify-pr.sh <policy-file> [changed-files...]}"
shift

if [[ ! -f "$POLICY_FILE" ]]; then
  echo "Error: Policy file not found: $POLICY_FILE" >&2
  exit 1
fi

if ! command -v jq &>/dev/null; then
  echo "Error: jq is required but not installed" >&2
  exit 1
fi

# Collect changed files from args or stdin
CHANGED_FILES=()
if [[ $# -gt 0 ]]; then
  CHANGED_FILES=("$@")
else
  while IFS= read -r line; do
    for f in $line; do
      CHANGED_FILES+=("$f")
    done
  done
fi

if [[ ${#CHANGED_FILES[@]} -eq 0 ]]; then
  # No changed files → default tier
  DEFAULT_TIER=$(jq -r '.default_tier // "standard"' "$POLICY_FILE")
  CHECKS=$(jq -c --arg t "$DEFAULT_TIER" '.tiers[$t].required_checks // []' "$POLICY_FILE")
  EVIDENCE=$(jq -r --arg t "$DEFAULT_TIER" '.tiers[$t].evidence_required // false' "$POLICY_FILE")
  echo "{\"tier\":\"$DEFAULT_TIER\",\"checks\":$CHECKS,\"evidence_required\":$EVIDENCE}"
  exit 0
fi

# --- Tier ranking (higher number = higher severity) ---
tier_rank() {
  case "$1" in
    critical) echo 4 ;;
    high)     echo 3 ;;
    standard) echo 2 ;;
    low)      echo 1 ;;
    *)        echo 0 ;;
  esac
}

# --- Glob matching (bash built-in, no external deps) ---
# Converts simple glob patterns to extended globs for matching.
# Supports: *, **, ?
glob_match() {
  local pattern="$1"
  local filepath="$2"

  # Convert glob to regex:
  #   **  → match any path segment(s)
  #   *   → match within a single segment
  #   ?   → match single char
  local regex="$pattern"
  # Escape dots
  regex="${regex//./\\.}"
  # ** → any path
  regex="${regex//\*\*/DOUBLESTAR}"
  # * → within segment
  regex="${regex//\*/[^/]*}"
  # Restore **
  regex="${regex//DOUBLESTAR/.*}"
  # ? → single char
  regex="${regex//\?/.}"
  # Anchor
  regex="^${regex}$"

  [[ "$filepath" =~ $regex ]]
}

# --- Classify each file, track highest tier ---
HIGHEST_RANK=0
HIGHEST_TIER=""
DEFAULT_TIER=$(jq -r '.default_tier // "standard"' "$POLICY_FILE")
NUM_RULES=$(jq '.path_rules | length' "$POLICY_FILE")

for file in "${CHANGED_FILES[@]}"; do
  FILE_TIER="$DEFAULT_TIER"

  # Check each rule (first match wins — rules are ordered by priority)
  for ((i = 0; i < NUM_RULES; i++)); do
    PATTERN=$(jq -r ".path_rules[$i].pattern" "$POLICY_FILE")
    RULE_TIER=$(jq -r ".path_rules[$i].tier" "$POLICY_FILE")

    if glob_match "$PATTERN" "$file"; then
      FILE_TIER="$RULE_TIER"
      break
    fi
  done

  RANK=$(tier_rank "$FILE_TIER")
  if [[ $RANK -gt $HIGHEST_RANK ]]; then
    HIGHEST_RANK=$RANK
    HIGHEST_TIER=$FILE_TIER
  fi

  # Short-circuit: can't go higher than critical
  [[ "$HIGHEST_TIER" == "critical" ]] && break
done

# Fallback if nothing matched
if [[ -z "$HIGHEST_TIER" ]]; then
  HIGHEST_TIER="$DEFAULT_TIER"
fi

# --- Output ---
CHECKS=$(jq -c --arg t "$HIGHEST_TIER" '.tiers[$t].required_checks // []' "$POLICY_FILE")
EVIDENCE=$(jq -r --arg t "$HIGHEST_TIER" '.tiers[$t].evidence_required // false' "$POLICY_FILE")

echo "{\"tier\":\"$HIGHEST_TIER\",\"checks\":$CHECKS,\"evidence_required\":$EVIDENCE}"
