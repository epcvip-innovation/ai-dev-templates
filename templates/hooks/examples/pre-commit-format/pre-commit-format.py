#!/usr/bin/env python3
"""
Pre-Commit Format Hook (Example)

PostToolUse hook that auto-formats code after git adds files.
Demonstrates automation pattern.
"""

import sys
import json
import subprocess
from pathlib import Path

def read_hook_input():
    try:
        data = json.load(sys.stdin)
        return data.get('tool_name'), data.get('tool_input', {})
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    tool_name, tool_input = read_hook_input()

    # Only run for Bash commands
    if tool_name != 'Bash':
        sys.exit(0)

    command = tool_input.get('command', '')

    # Only format files added to git
    if not command.startswith('git add'):
        sys.exit(0)

    # Extract files from command
    # Example: "git add file1.py file2.py"
    parts = command.split()
    files = [f for f in parts[2:] if f.endswith(('.py', '.js', '.ts'))]

    if not files:
        sys.exit(0)

    # Format Python files with black
    python_files = [f for f in files if f.endswith('.py')]
    if python_files:
        try:
            subprocess.run(['black'] + python_files, check=True, capture_output=True)
            print(f"✅ Formatted {len(python_files)} Python file(s)", file=sys.stderr)
        except subprocess.CalledProcessError:
            pass  # Black not installed or failed, don't block
        except FileNotFoundError:
            pass  # Black not installed

    # Format JS/TS files with prettier
    js_files = [f for f in files if f.endswith(('.js', '.ts'))]
    if js_files:
        try:
            subprocess.run(['prettier', '--write'] + js_files, check=True, capture_output=True)
            print(f"✅ Formatted {len(js_files)} JS/TS file(s)", file=sys.stderr)
        except subprocess.CalledProcessError:
            pass
        except FileNotFoundError:
            pass

    sys.exit(0)  # Always allow for PostToolUse

if __name__ == '__main__':
    main()
