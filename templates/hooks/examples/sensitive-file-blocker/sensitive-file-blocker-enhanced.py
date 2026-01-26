#!/usr/bin/env python3
"""
Enhanced Sensitive File Blocker Hook

PreToolUse hook that blocks access to sensitive files using multiple detection strategies:
1. Exact filename matching (common secrets files)
2. Extension-based detection (certificates, keys)
3. Keyword pattern matching (paths containing 'secrets', 'credentials', etc.)

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
# CONFIGURATION - Edit these lists for your needs
# =============================================================================

# Exact filenames to block (case-sensitive)
BLOCKED_FILENAMES = {
    # Environment files
    '.env',
    '.env.local',
    '.env.production',
    '.env.staging',
    '.env.development',

    # Credentials and secrets
    'secrets.json',
    'secrets.yaml',
    'secrets.yml',
    'credentials.json',
    'credentials.yaml',
    'credentials.yml',
    'config/production.json',

    # Cloud credentials
    '.aws/credentials',
    '.aws/config',
    '.gcloud/credentials.json',
    '.azure/credentials',

    # SSH keys
    'id_rsa',
    'id_rsa.pub',
    'id_ed25519',
    'id_ed25519.pub',
    'id_ecdsa',
    'id_ecdsa.pub',
    'known_hosts',
    'authorized_keys',

    # Package manager auth
    '.npmrc',
    '.pypirc',
    '.netrc',

    # Database
    '.pgpass',
    '.my.cnf',

    # Docker secrets
    'docker-compose.secrets.yml',
    'docker-compose.secrets.yaml',
}

# File extensions to block
BLOCKED_EXTENSIONS = {
    '.pem',      # Certificates/keys
    '.key',      # Private keys
    '.p12',      # PKCS#12 bundles
    '.pfx',      # PKCS#12 (Windows)
    '.jks',      # Java keystores
    '.keystore', # Keystores
    '.crt',      # Certificates (block writes, allow reads for verification)
    '.cer',      # Certificates
}

# Patterns to match anywhere in the path (case-insensitive)
BLOCKED_PATH_PATTERNS = [
    r'/secrets/',           # secrets directories
    r'/credentials/',       # credentials directories
    r'/private[_-]?keys?/', # private key directories
    r'\.secrets\.',         # .secrets. in filename
    r'secret[_-]?key',      # secret_key, secretkey, secret-key
    r'private[_-]?key',     # private_key, privatekey, private-key
    r'api[_-]?key',         # api_key files (not in code, just dedicated files)
    r'master[_-]?key',      # Rails master.key etc
    r'/\.ssh/',             # SSH directory
]

# Tools to check (Read can be optionally included)
# Set to True to also block Read operations on sensitive files
BLOCK_READ_OPERATIONS = False

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


def get_filename(path):
    """Extract just the filename from a path."""
    return os.path.basename(path)


def get_extension(path):
    """Extract the file extension (including the dot)."""
    _, ext = os.path.splitext(path)
    return ext.lower()


def normalize_path(path):
    """Normalize path for consistent matching."""
    # Remove leading ./ and normalize separators
    path = path.lstrip('./')
    path = path.replace('\\', '/')
    return path


def is_sensitive_file(file_path):
    """
    Check if file is sensitive using three strategies:
    1. Exact filename match
    2. Extension match
    3. Path pattern match

    Returns: (is_sensitive: bool, reason: str)
    """
    normalized = normalize_path(file_path)
    filename = get_filename(normalized)
    extension = get_extension(normalized)

    # Strategy 1: Exact filename match
    if filename in BLOCKED_FILENAMES:
        return True, f"Blocked filename: {filename}"

    # Also check if full relative path matches (for nested paths like .aws/credentials)
    if normalized in BLOCKED_FILENAMES:
        return True, f"Blocked path: {normalized}"

    # Strategy 2: Extension match
    if extension in BLOCKED_EXTENSIONS:
        return True, f"Blocked extension: {extension}"

    # Strategy 3: Path pattern match
    for pattern in BLOCKED_PATH_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True, f"Blocked pattern: {pattern}"

    return False, ""


def main():
    # Check for escape hatch
    if os.environ.get('ALLOW_SENSITIVE_ACCESS') == '1':
        allow_execution()

    tool_name, tool_input = read_hook_input()

    # Determine which tools to check
    tools_to_check = ['Edit', 'Write']
    if BLOCK_READ_OPERATIONS:
        tools_to_check.append('Read')

    if tool_name not in tools_to_check:
        allow_execution()

    # Get file path from tool input
    file_path = tool_input.get('file_path', '')
    if not file_path:
        allow_execution()

    # Check if file is sensitive
    is_sensitive, reason = is_sensitive_file(file_path)

    if is_sensitive:
        action = "read from" if tool_name == 'Read' else "write to"
        error_message = f"""
BLOCKED: Sensitive file access prevented!

Tool: {tool_name}
File: {file_path}
Reason: {reason}

This file is classified as sensitive and cannot be {action} directly.

Detection method:
- Exact filename matching (common secrets files)
- Extension detection (certificates, keys)
- Path pattern matching (secrets/, credentials/, etc.)

To proceed anyway (use extreme caution):
  ALLOW_SENSITIVE_ACCESS=1 claude

To modify the blocklist:
  Edit ~/.claude/hooks/sensitive-file-blocker-enhanced.py

Alternative approaches:
- Use .env.example with placeholder values
- Store secrets in environment variables
- Use a secrets manager (AWS Secrets Manager, HashiCorp Vault)
"""
        block_execution(error_message)

    allow_execution()


if __name__ == '__main__':
    main()
