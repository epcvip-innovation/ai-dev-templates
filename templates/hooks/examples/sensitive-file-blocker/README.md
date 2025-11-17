# Sensitive File Blocker Hook (Example)

**Type**: PreToolUse hook (blocking)
**Use case**: Prevent edits to production config files
**Pattern**: Validation hook (blocks unsafe operations)

## What It Does

Blocks Edit/Write operations on sensitive files:
- `.env.production`
- `config/production.json`
- `secrets.yaml`
- `credentials.json`

## Installation

```bash
# Copy to user hooks directory
cp sensitive-file-blocker.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/sensitive-file-blocker.py

# Edit to configure your blocked files
nano ~/.claude/hooks/sensitive-file-blocker.py

# Add to ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/sensitive-file-blocker.py"
          }
        ]
      }
    ]
  }
}
```

## Customization

Edit `BLOCKED_FILES` list:

```python
BLOCKED_FILES = [
    '.env.production',
    'config/production.json',
    'aws-credentials.json',     # Add your files
    'database-passwords.txt',
]
```

## Emergency Bypass

```bash
# Allow edit to blocked file
ALLOW_SENSITIVE_EDIT=1 <edit command>
```

## Example Usage

```
Claude tries to edit .env.production

❌ Edit blocked - sensitive file!

File: .env.production

This file is marked as sensitive and cannot be edited.
```
