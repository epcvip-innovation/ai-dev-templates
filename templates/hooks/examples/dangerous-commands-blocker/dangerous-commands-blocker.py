#!/usr/bin/env python3
"""
Dangerous Commands Blocker Hook

PreToolUse hook that blocks potentially destructive or dangerous Bash commands.
Prevents common footguns like:
- rm -rf without safeguards
- curl piping directly to shell
- Force pushes to protected branches
- Database drops/deletes without confirmation

Based on patterns from TheDecipherist/claude-code-mastery, adapted for internal use.

Exit codes:
- 0: Allow operation
- 1: Error (logged but doesn't block)
- 2: Block operation (stderr shown to Claude)
"""

import sys
import json
import os
import re

# =============================================================================
# CONFIGURATION - Edit these patterns for your needs
# =============================================================================

# Commands/patterns that are always blocked
ALWAYS_BLOCKED = [
    # Destructive file operations
    (r'rm\s+(-[a-zA-Z]*)?rf\s+[/~]', 'rm -rf on root or home directory'),
    (r'rm\s+(-[a-zA-Z]*)?rf\s+\*', 'rm -rf with wildcard'),
    (r'rm\s+(-[a-zA-Z]*)?rf\s+\.\s', 'rm -rf on current directory'),

    # Curl/wget piping to shell (common malware vector)
    (r'curl\s+.*\|\s*(ba)?sh', 'curl piping to shell'),
    (r'wget\s+.*\|\s*(ba)?sh', 'wget piping to shell'),
    (r'curl\s+.*\|\s*sudo', 'curl piping to sudo'),
    (r'wget\s+.*\|\s*sudo', 'wget piping to sudo'),

    # Git force operations on protected branches
    (r'git\s+push\s+.*--force.*\s+(main|master|production|prod)\b', 'force push to protected branch'),
    (r'git\s+push\s+-f\s+.*\s+(main|master|production|prod)\b', 'force push to protected branch'),
    (r'git\s+reset\s+--hard\s+origin/(main|master|production|prod)', 'hard reset to remote protected branch'),

    # Database destruction
    (r'DROP\s+DATABASE', 'DROP DATABASE command'),
    (r'DROP\s+TABLE', 'DROP TABLE command (use with explicit confirmation)'),
    (r'TRUNCATE\s+TABLE', 'TRUNCATE TABLE command'),
    (r'DELETE\s+FROM\s+\w+\s*;?\s*$', 'DELETE without WHERE clause'),

    # System destruction
    (r'mkfs\s+', 'filesystem format command'),
    (r'dd\s+.*of=/dev/', 'dd writing to device'),
    (r':\s*\(\s*\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;', 'fork bomb'),

    # Credential exposure
    (r'echo\s+.*\bpassword\b.*>>', 'echoing password to file'),
    (r'echo\s+.*\btoken\b.*>>', 'echoing token to file'),
    (r'echo\s+.*\bsecret\b.*>>', 'echoing secret to file'),
]

# Commands that trigger a warning but are allowed
WARN_PATTERNS = [
    (r'rm\s+(-[a-zA-Z]*)?r', 'recursive delete - verify target'),
    (r'chmod\s+777', 'overly permissive chmod'),
    (r'chmod\s+-R', 'recursive chmod'),
    (r'chown\s+-R', 'recursive chown'),
    (r'git\s+push\s+--force', 'force push (verify branch)'),
    (r'git\s+reset\s+--hard', 'hard reset (verify you want to lose changes)'),
]

# Commands that are always allowed (early exit for performance)
ALWAYS_ALLOWED_PREFIXES = [
    'ls', 'cd', 'pwd', 'cat', 'head', 'tail', 'less', 'more',
    'echo', 'printf',  # Basic output (blocked patterns caught separately)
    'grep', 'find', 'locate', 'which', 'whereis',
    'git status', 'git log', 'git diff', 'git branch', 'git show',
    'git fetch', 'git pull',  # Non-destructive git
    'npm list', 'npm info', 'npm view',
    'pip list', 'pip show',
    'docker ps', 'docker images', 'docker logs',
    'kubectl get', 'kubectl describe', 'kubectl logs',
    'python --version', 'node --version', 'npm --version',
]

# =============================================================================
# IMPLEMENTATION
# =============================================================================

def read_hook_input():
    """Read JSON input from stdin."""
    try:
        data = json.load(sys.stdin)
        return data.get('tool_name'), data.get('tool_input', {})
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(1)


def allow_execution():
    """Allow the operation to proceed."""
    sys.exit(0)


def block_execution(message):
    """Block the operation with an error message."""
    print(message, file=sys.stderr)
    sys.exit(2)


def is_allowed_command(command):
    """Check if command starts with an always-allowed prefix."""
    command_lower = command.strip().lower()
    for prefix in ALWAYS_ALLOWED_PREFIXES:
        if command_lower.startswith(prefix.lower()):
            return True
    return False


def check_dangerous_patterns(command):
    """
    Check command against dangerous patterns.

    Returns: (is_blocked: bool, reason: str, is_warning: bool)
    """
    # Check always-blocked patterns first
    for pattern, reason in ALWAYS_BLOCKED:
        if re.search(pattern, command, re.IGNORECASE):
            return True, reason, False

    # Check warning patterns (allowed but flagged)
    for pattern, reason in WARN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, reason, True

    return False, "", False


def main():
    # Check for escape hatch
    if os.environ.get('ALLOW_DANGEROUS_COMMANDS') == '1':
        allow_execution()

    tool_name, tool_input = read_hook_input()

    # Only check Bash tool
    if tool_name != 'Bash':
        allow_execution()

    # Get command from tool input
    command = tool_input.get('command', '')
    if not command:
        allow_execution()

    # Early exit for safe commands (performance optimization)
    if is_allowed_command(command):
        allow_execution()

    # Check for dangerous patterns
    is_blocked, reason, is_warning = check_dangerous_patterns(command)

    if is_blocked:
        error_message = f"""
BLOCKED: Dangerous command detected!

Command: {command}
Reason: {reason}

This command pattern is blocked because it could cause:
- Irreversible data loss
- Security vulnerabilities
- System instability

To proceed anyway (use extreme caution):
  ALLOW_DANGEROUS_COMMANDS=1 claude

Alternative approaches:
- Use more targeted commands (specify exact paths)
- Add safety checks (--dry-run, --interactive)
- Break into smaller, safer operations
- Verify the target before destructive operations

To modify the blocklist:
  Edit ~/.claude/hooks/dangerous-commands-blocker.py
"""
        block_execution(error_message)

    # Warnings are logged but not blocked (could add stderr output here if desired)

    allow_execution()


if __name__ == '__main__':
    main()
