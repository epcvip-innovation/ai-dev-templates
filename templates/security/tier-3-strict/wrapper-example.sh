#!/bin/bash
# wrapper-example.sh — Secure agent launcher
#
# Standardizes Claude Code launch flags to enforce security controls.
# Prevents bypassing security via dangerous CLI flags.
#
# Usage:
#   Install:  cp wrapper-example.sh /usr/local/bin/claude-secure && chmod +x /usr/local/bin/claude-secure
#   Run:      claude-secure [regular claude args]
#   Example:  claude-secure "Fix the login bug"

set -euo pipefail

# --- Block dangerous flags ---
for arg in "$@"; do
    case "$arg" in
        --dangerously-skip-permissions)
            echo "ERROR: --dangerously-skip-permissions is blocked by security policy."
            echo "If you need to bypass permissions, contact your team lead."
            exit 1
            ;;
        --setting-sources=user|--setting-sources=cli)
            echo "ERROR: Only --setting-sources project is allowed by security policy."
            echo "This ensures all team members use the same security settings."
            exit 1
            ;;
    esac
done

# --- Enforce project-only settings ---
# This prevents personal ~/.claude/settings.json from weakening project controls
SETTING_SOURCES="project"

# --- Audit logging ---
LOG_FILE="/tmp/claude-audit-$(date +%Y%m%d).jsonl"
echo "{\"timestamp\":\"$(date -Iseconds)\",\"user\":\"$(whoami)\",\"cwd\":\"$(pwd)\",\"args\":$(printf '%s\n' "$@" | jq -R . | jq -s .)}" >> "$LOG_FILE"

# --- Launch Claude Code with enforced settings ---
exec claude --setting-sources "$SETTING_SOURCES" "$@"
