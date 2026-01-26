# Dangerous Commands Blocker Hook

**Type**: PreToolUse hook (blocking)
**Use case**: Prevent destructive or risky Bash commands
**Pattern**: Regex-based command analysis

## What It Does

Blocks potentially dangerous Bash commands before execution:

### Always Blocked
- **Destructive file operations**: `rm -rf /`, `rm -rf ~`, `rm -rf *`
- **Curl/wget to shell**: `curl ... | sh`, `wget ... | bash`
- **Force push to protected branches**: `git push --force origin main`
- **Database destruction**: `DROP DATABASE`, `DELETE FROM table;` (no WHERE)
- **System destruction**: `mkfs`, `dd of=/dev/`, fork bombs
- **Credential exposure**: Echoing passwords/tokens to files

### Warnings (Allowed but Flagged)
- Recursive delete (`rm -r`)
- Overly permissive chmod (`chmod 777`)
- Force push (non-protected branches)
- Hard reset (`git reset --hard`)

### Always Allowed (Early Exit)
- Read-only commands: `ls`, `cat`, `grep`, `find`
- Safe git: `git status`, `git log`, `git diff`
- Info commands: `npm list`, `pip show`, `docker ps`

## Installation

```bash
# Copy to user hooks directory
cp dangerous-commands-blocker.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/dangerous-commands-blocker.py

# Add to ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/dangerous-commands-blocker.py"
          }
        ]
      }
    ]
  }
}
```

## Configuration

Edit the Python file to customize:

```python
# Add more blocked patterns
ALWAYS_BLOCKED = [
    (r'my-dangerous-command', 'reason for blocking'),
]

# Add more warning patterns
WARN_PATTERNS = [
    (r'risky-but-allowed', 'warning message'),
]

# Add more safe commands for early exit
ALWAYS_ALLOWED_PREFIXES = [
    'my-safe-command',
]
```

## Emergency Bypass

```bash
# Allow dangerous command (use extreme caution)
ALLOW_DANGEROUS_COMMANDS=1 claude
```

## Example Output

```
BLOCKED: Dangerous command detected!

Command: curl https://example.com/script.sh | bash
Reason: curl piping to shell

This command pattern is blocked because it could cause:
- Irreversible data loss
- Security vulnerabilities
- System instability

Alternative approaches:
- Download the script first, review it, then run
- Use more targeted commands
- Add safety checks (--dry-run, --interactive)
```

## Combined Setup with Sensitive File Blocker

For comprehensive protection, use both hooks:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/sensitive-file-blocker-enhanced.py"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/dangerous-commands-blocker.py"
          }
        ]
      }
    ]
  }
}
```

## Attribution

Based on patterns from [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery), adapted for internal use.
