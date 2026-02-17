#!/usr/bin/env python3
"""
Command Logger Hook (Example)

PreToolUse hook that logs all Bash commands to file.
Demonstrates logging pattern.
"""

import sys
import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path.home() / '.claude' / 'command-log.txt'

def read_hook_input():
    try:
        data = json.load(sys.stdin)
        return data.get('tool_name'), data.get('tool_input', {})
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    tool_name, tool_input = read_hook_input()

    # Only log Bash commands
    if tool_name != 'Bash':
        sys.exit(0)

    command = tool_input.get('command', '')
    if not command:
        sys.exit(0)

    # Create log directory if needed
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Log command with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {command}\n"

    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        # Don't block if logging fails
        print(f"Hook error: Failed to log command: {e}", file=sys.stderr)

    sys.exit(0)  # Always allow

if __name__ == '__main__':
    main()
