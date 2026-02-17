# Command Logger Hook (Example)

**Type**: PreToolUse hook (non-blocking)
**Use case**: Audit trail of all Bash commands
**Pattern**: Logging hook (never blocks)

## What It Does

Logs all Bash commands executed by Claude to `~/.claude/command-log.txt`:

```
[2025-11-03 14:20:15] git status
[2025-11-03 14:20:22] python run_analysis.py
[2025-11-03 14:20:45] git add .
```

## Installation

```bash
# Copy to user hooks directory
cp command-logger.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/command-logger.py

# Add to ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/command-logger.py"
          }
        ]
      }
    ]
  }
}
```

## View Logs

```bash
# View all logged commands
cat ~/.claude/command-log.txt

# View recent commands
tail -n 20 ~/.claude/command-log.txt

# Search for specific command
grep "python" ~/.claude/command-log.txt
```

## Customization

Change log location:

```python
# Default
LOG_FILE = Path.home() / '.claude' / 'command-log.txt'

# Custom
LOG_FILE = Path('/var/log/claude/commands.log')
```

Add more details:

```python
# Log command + project directory
import os
project_dir = os.environ.get('CLAUDE_PROJECT_DIR', 'unknown')
log_entry = f"[{timestamp}] [{project_dir}] {command}\n"
```

## Use Cases

- Compliance requirements
- Understanding Claude's command patterns
- Debugging workflow issues
- Learning command usage
