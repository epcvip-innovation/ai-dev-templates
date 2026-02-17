#!/usr/bin/env python3
"""
Query Validation Enforcement Hook

This PreToolUse hook enforces that queries are validated before execution.
It blocks query execution commands unless a validation marker exists.

Exit codes:
  0 = Allow execution
  2 = Block execution (stderr shown to Claude)
  1 = Error (logged, doesn't block)
"""

import sys
import json
import re
import os
import hashlib
from pathlib import Path


def read_hook_input():
    """Read JSON input from stdin."""
    try:
        data = json.load(sys.stdin)
        return data.get('tool_name'), data.get('tool_input', {})
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Hook error: Failed to parse input: {e}", file=sys.stderr)
        sys.exit(1)


def is_query_execution(command):
    """
    Check if command is a query execution (not a normal bash command).

    Returns True if command matches query execution patterns.
    """
    # Early exit for common non-query commands
    command_stripped = command.strip()
    if command_stripped.startswith(('ls', 'cd', 'cat', 'grep', 'find', 'echo',
                                    'pwd', 'mkdir', 'rm', 'cp', 'mv', 'touch',
                                    'head', 'tail', 'wc', 'sort', 'uniq', 'git')):
        return False

    # Query execution patterns (refined to avoid false positives)
    patterns = [
        r'python3?\s+run_validation_query\.py',  # Our validation query runner
        r'python3?\s+run_query\.py',             # Generic query runner
        r'python3?\s+.*athena_client\.py',       # Direct athena client usage
        r'python3?\s+-m\s+core\.athena_client',  # Module-based execution
    ]

    return any(re.search(pattern, command) for pattern in patterns)


def extract_query_path_from_command(command):
    """
    Extract query file path from command.

    Looks for .sql file paths in the command.
    Returns None if no SQL file found.
    """
    # Look for .sql file in command
    sql_match = re.search(r'([^\s]+\.sql)', command)
    if sql_match:
        return sql_match.group(1)
    return None


def check_validation_marker(query_path):
    """
    Check if validation marker exists for the given query path.

    Returns (exists: bool, marker_path: Path)
    """
    try:
        # Resolve to absolute path
        query_abs_path = Path(query_path).resolve()

        # Generate same hash as validation command
        path_hash = hashlib.sha256(str(query_abs_path).encode()).hexdigest()[:16]
        marker_path = Path(f'/tmp/query_validated_{path_hash}.marker')

        return marker_path.exists(), marker_path
    except Exception as e:
        print(f"Hook error: Failed to check marker: {e}", file=sys.stderr)
        return False, None


def allow_execution():
    """Allow the command to execute."""
    sys.exit(0)


def block_execution(message):
    """Block the command and show error message to Claude."""
    print(message, file=sys.stderr)
    sys.exit(2)


def main():
    # Check for escape hatch (emergency bypass)
    if os.environ.get('SKIP_QUERY_VALIDATION') == '1':
        allow_execution()

    # Read hook input
    tool_name, tool_input = read_hook_input()

    # Only intercept Bash commands
    if tool_name != 'Bash':
        allow_execution()

    # Get command from tool_input
    command = tool_input.get('command', '')
    if not command:
        allow_execution()

    # Check if this is a query execution command
    if not is_query_execution(command):
        allow_execution()

    # Extract query path from command
    query_path = extract_query_path_from_command(command)
    if not query_path:
        # Query execution command but no .sql file found
        # This might be a different kind of query execution, allow for now
        allow_execution()

    # Check for validation marker
    marker_exists, marker_path = check_validation_marker(query_path)

    if marker_exists:
        # Marker found - delete it (one-time use) and allow execution
        try:
            marker_path.unlink()
        except Exception as e:
            print(f"Hook warning: Failed to delete marker: {e}", file=sys.stderr)

        allow_execution()
    else:
        # No marker - block execution
        error_message = f"""
❌ Query execution blocked - validation required!

Query: {query_path}

You must validate this query before executing it:

  1. Run validation command:
     /validate-query {query_path}

  2. Fix any errors or warnings

  3. Try executing again

To bypass this check (emergency only):
  SKIP_QUERY_VALIDATION=1 {command}

Why validation is required:
• Ensures partition filters are present (avoids expensive full table scans)
• Catches timezone handling issues
• Validates Trino/Athena function compatibility
• Prevents queries with syntax errors

See CLAUDE.md and QUERY_WORKFLOW.md for details.
"""
        block_execution(error_message)


if __name__ == '__main__':
    main()
