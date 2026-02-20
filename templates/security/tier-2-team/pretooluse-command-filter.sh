#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# ──────────────────────────────────────────────────────────────
# PreToolUse hook — enforces Bash command permissions via
# externalized deny/allow conf files.
#
# Returns allow / deny / passthrough decisions via JSON on stdout.
# Applies to all sessions including subagents spawned via Task tool.
#
# Pattern: bash case glob matching with Bash() wrapper format.
#
# Configured in .claude/settings.json under hooks.PreToolUse.
# ──────────────────────────────────────────────────────────────

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DENY_FILE="${DIR}/denied-commands.conf"
ALLOW_FILE="${DIR}/allowed-commands.conf"

# Read tool input from stdin (JSON from Claude Code)
INPUT="$(cat)"
COMMAND="$(echo "${INPUT}" | jq -r '.tool_input.command // ""')"

# Empty command — passthrough
if [[ -z "${COMMAND}" ]]; then
  exit 0
fi

# Load patterns from a conf file.
# Strips comments, blank lines, and Bash() wrapper.
load_patterns() {
  local conf_file="$1"
  [[ ! -f "${conf_file}" ]] && return

  local line
  while IFS= read -r line; do
    # Strip inline comments
    line="${line%%#*}"
    # Strip leading whitespace
    while [[ "${line}" == " "* || "${line}" == "	"* ]]; do line="${line#?}"; done
    # Strip trailing whitespace
    while [[ "${line}" == *" " || "${line}" == *"	" ]]; do line="${line%?}"; done
    [[ -z "${line}" ]] && continue

    # Extract pattern from Bash(...)
    if [[ "${line}" == Bash\(*\) ]]; then
      local pattern="${line#Bash(}"
      pattern="${pattern%)}"
      printf '%s\n' "${pattern}"
    fi
  done < "${conf_file}"
}

# Check deny list first (deny takes precedence)
while IFS= read -r pattern; do
  # shellcheck disable=SC2254
  case "${COMMAND}" in
    ${pattern})
      printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked by denied-commands.conf"}}\n'
      exit 0
      ;;
  esac
done < <(load_patterns "${DENY_FILE}")

# Check allow list
while IFS= read -r pattern; do
  # shellcheck disable=SC2254
  case "${COMMAND}" in
    ${pattern})
      printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}\n'
      exit 0
      ;;
  esac
done < <(load_patterns "${ALLOW_FILE}")

# No match — passthrough to Claude's normal permission prompt
exit 0
