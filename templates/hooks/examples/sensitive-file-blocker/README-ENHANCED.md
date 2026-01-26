# Enhanced Sensitive File Blocker Hook

**Type**: PreToolUse hook (blocking)
**Use case**: Comprehensive protection for secrets, credentials, and sensitive files
**Pattern**: Multi-strategy detection (filename, extension, path patterns)

## What It Does

Blocks Read/Edit/Write operations on sensitive files using three detection strategies:

### 1. Exact Filename Matching
- `.env`, `.env.production`, `.env.local`
- `secrets.json`, `credentials.yaml`
- SSH keys (`id_rsa`, `id_ed25519`, `known_hosts`)
- Cloud credentials (`.aws/credentials`, `.gcloud/credentials.json`)
- Package manager auth (`.npmrc`, `.pypirc`)

### 2. Extension-Based Detection
- `.pem`, `.key` - Private keys
- `.p12`, `.pfx`, `.jks` - Keystores
- `.crt`, `.cer` - Certificates

### 3. Path Pattern Matching
- `/secrets/` directories
- `/credentials/` directories
- Files containing `private_key`, `secret_key`, `api_key`
- `/.ssh/` directory

## Comparison to Basic Version

| Feature | Basic | Enhanced |
|---------|-------|----------|
| Exact filenames | 4 files | 30+ files |
| Extension matching | No | Yes (.pem, .key, etc.) |
| Path patterns | No | Yes (regex-based) |
| SSH key protection | No | Yes |
| Cloud credentials | No | Yes |
| Block Read operations | No | Optional |

## Installation

```bash
# Copy to user hooks directory
cp sensitive-file-blocker-enhanced.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/sensitive-file-blocker-enhanced.py

# Add to ~/.claude/settings.json
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
      }
    ]
  }
}
```

## Configuration

Edit the Python file to customize:

```python
# Add more blocked filenames
BLOCKED_FILENAMES = {
    '.env',
    'my-custom-secrets.json',  # Add your files
}

# Add more blocked extensions
BLOCKED_EXTENSIONS = {
    '.pem',
    '.mykey',  # Add custom extensions
}

# Add more path patterns
BLOCKED_PATH_PATTERNS = [
    r'/secrets/',
    r'/my-sensitive-dir/',  # Add custom patterns
]

# Enable Read blocking (disabled by default)
BLOCK_READ_OPERATIONS = True
```

## Emergency Bypass

```bash
# Allow access to blocked file (use extreme caution)
ALLOW_SENSITIVE_ACCESS=1 claude
```

## Example Output

```
BLOCKED: Sensitive file access prevented!

Tool: Edit
File: .env.production
Reason: Blocked filename: .env.production

This file is classified as sensitive and cannot be written to directly.

Alternative approaches:
- Use .env.example with placeholder values
- Store secrets in environment variables
- Use a secrets manager (AWS Secrets Manager, HashiCorp Vault)
```

## Attribution

Based on patterns from [TheDecipherist/claude-code-mastery](https://github.com/TheDecipherist/claude-code-mastery), adapted for internal use with additional patterns and documentation.
