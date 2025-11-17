#!/usr/bin/env python3
"""
Sensitive File Blocker Hook (Example)

PreToolUse hook that blocks edits to production config files.
Demonstrates validation pattern.
"""

import sys
import json
import os

# Configure blocked files (relative to project root)
BLOCKED_FILES = [
    '.env.production',
    'config/production.json',
    'secrets.yaml',
    'credentials.json',
]

def read_hook_input():
    try:
        data = json.load(sys.stdin)
        return data.get('tool_name'), data.get('tool_input', {})
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(1)

def allow_execution():
    sys.exit(0)

def block_execution(message):
    print(message, file=sys.stderr)
    sys.exit(2)

def main():
    # Check for escape hatch
    if os.environ.get('ALLOW_SENSITIVE_EDIT') == '1':
        allow_execution()

    tool_name, tool_input = read_hook_input()

    # Only check Edit and Write tools
    if tool_name not in ['Edit', 'Write']:
        allow_execution()

    # Get file path
    file_path = tool_input.get('file_path', '')
    if not file_path:
        allow_execution()

    # Normalize path (remove leading ./)
    file_path = file_path.lstrip('./')

    # Check if file is blocked
    if file_path in BLOCKED_FILES:
        error_message = f"""
❌ Edit blocked - sensitive file!

File: {file_path}

This file is marked as sensitive and cannot be edited.

Reason: Production configuration or credentials

To edit anyway (use caution):
  ALLOW_SENSITIVE_EDIT=1 <your edit command>

To modify blocklist:
  Edit ~/.claude/hooks/sensitive-file-blocker.py
"""
        block_execution(error_message)

    allow_execution()

if __name__ == '__main__':
    main()
