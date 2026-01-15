#!/usr/bin/env python3
"""
Pre-Commit Audit Hook

Runs lightweight anti-slop and security checks before allowing commits.
Blocks on Critical issues only, warns on High/Medium.

Installation:
1. Copy to ~/.claude/hooks/ or .git/hooks/pre-commit
2. Configure in Claude Code settings or git hooks
3. Make executable: chmod +x audit-precommit.py

Bypass: SKIP_AUDIT=1 git commit -m "message"
"""

import os
import sys
import subprocess
import re
from pathlib import Path


# ============================================================================
# CONFIGURATION
# ============================================================================

# Exit early for these file patterns (not worth auditing)
SKIP_PATTERNS = [
    r'\.md$',           # Markdown files
    r'\.json$',         # JSON configs
    r'\.yml$',          # YAML configs
    r'\.yaml$',
    r'\.lock$',         # Lock files
    r'\.txt$',          # Text files
    r'test.*\.py$',     # Test files (skip for speed)
    r'__pycache__',     # Cache directories
    r'node_modules',    # Dependencies
    r'\.git/',          # Git internals
]

# Patterns that indicate CRITICAL issues (block commit)
CRITICAL_PATTERNS = {
    'SQL Injection': {
        'pattern': r'execute.*f["\']|execute.*\+\s*["\']|execute.*format\(',
        'file_types': ['.py'],
        'message': 'Potential SQL injection: use parameterized queries',
    },
    'Hardcoded Secret': {
        'pattern': r'(password|api_key|secret|token)\s*=\s*["\'][^"\']{8,}["\']',
        'file_types': ['.py', '.js', '.ts'],
        'message': 'Hardcoded secret detected: use environment variables',
    },
    'Empty Exception Handler': {
        'pattern': r'except.*:\s*pass\s*$',
        'file_types': ['.py'],
        'message': 'Empty exception handler: always log or handle errors',
    },
}

# Patterns that indicate HIGH issues (warn but don't block)
HIGH_PATTERNS = {
    'Console Log in Production': {
        'pattern': r'console\.log\(',
        'file_types': ['.js', '.ts', '.jsx', '.tsx'],
        'message': 'console.log found: remove before production',
    },
    'Print Statement': {
        'pattern': r'^\s*print\(',
        'file_types': ['.py'],
        'message': 'print() found: use logger instead',
    },
    'TODO Without Context': {
        'pattern': r'#\s*TODO\s*$|#\s*TODO\s*:?\s*$',
        'file_types': ['.py', '.js', '.ts'],
        'message': 'TODO without description: add context',
    },
}

# Patterns that indicate MEDIUM issues (informational only)
MEDIUM_PATTERNS = {
    'Magic Number': {
        'pattern': r'(?<![\w.])(?:60|3600|86400|1000|1024)(?![\w.])',
        'file_types': ['.py', '.js', '.ts'],
        'message': 'Magic number: consider named constant',
    },
    'Long Line': {
        'pattern': r'^.{120,}$',
        'file_types': ['.py'],
        'message': 'Line over 120 chars: consider breaking up',
    },
}


# ============================================================================
# HOOK LOGIC
# ============================================================================

def should_skip_file(filepath: str) -> bool:
    """Check if file should be skipped based on patterns."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, filepath):
            return True
    return False


def get_staged_files() -> list:
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True
        )
        return [f for f in result.stdout.strip().split('\n') if f]
    except Exception:
        return []


def get_staged_diff() -> str:
    """Get the staged diff content."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception:
        return ""


def check_file(filepath: str, patterns: dict, severity: str) -> list:
    """Check a file against patterns, return list of issues."""
    issues = []
    
    if not os.path.exists(filepath):
        return issues
    
    file_ext = Path(filepath).suffix
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception:
        return issues
    
    for name, config in patterns.items():
        # Check if pattern applies to this file type
        if file_ext not in config['file_types']:
            continue
        
        pattern = config['pattern']
        message = config['message']
        
        for line_num, line in enumerate(lines, 1):
            if re.search(pattern, line):
                issues.append({
                    'severity': severity,
                    'name': name,
                    'file': filepath,
                    'line': line_num,
                    'message': message,
                    'content': line.strip()[:80],
                })
    
    return issues


def format_issue(issue: dict) -> str:
    """Format an issue for display."""
    severity_icons = {
        'CRITICAL': '🚨',
        'HIGH': '⚠️',
        'MEDIUM': '💡',
    }
    icon = severity_icons.get(issue['severity'], '📝')
    return (
        f"{icon} {issue['severity']}: {issue['name']}\n"
        f"   File: {issue['file']}:{issue['line']}\n"
        f"   {issue['message']}\n"
        f"   > {issue['content']}\n"
    )


def main():
    """Main hook entry point."""
    
    # Check for bypass
    if os.environ.get('SKIP_AUDIT') == '1':
        print("⏭️  Audit hook bypassed (SKIP_AUDIT=1)")
        sys.exit(0)
    
    # Get staged files
    staged_files = get_staged_files()
    
    if not staged_files:
        sys.exit(0)
    
    # Filter files to check
    files_to_check = [f for f in staged_files if not should_skip_file(f)]
    
    if not files_to_check:
        sys.exit(0)
    
    print("🔍 Running pre-commit audit...")
    
    # Collect issues
    critical_issues = []
    high_issues = []
    medium_issues = []
    
    for filepath in files_to_check:
        critical_issues.extend(check_file(filepath, CRITICAL_PATTERNS, 'CRITICAL'))
        high_issues.extend(check_file(filepath, HIGH_PATTERNS, 'HIGH'))
        medium_issues.extend(check_file(filepath, MEDIUM_PATTERNS, 'MEDIUM'))
    
    # Report findings
    total_issues = len(critical_issues) + len(high_issues) + len(medium_issues)
    
    if total_issues == 0:
        print("✅ No issues found")
        sys.exit(0)
    
    print(f"\n📊 Found {total_issues} issues:\n")
    
    # Print critical issues (these block)
    if critical_issues:
        print("=" * 60)
        print("🚨 CRITICAL ISSUES (blocking commit)")
        print("=" * 60)
        for issue in critical_issues[:3]:  # Max 3 critical
            print(format_issue(issue))
        if len(critical_issues) > 3:
            print(f"   ... and {len(critical_issues) - 3} more critical issues\n")
    
    # Print high issues (warn only)
    if high_issues:
        print("=" * 60)
        print("⚠️  HIGH ISSUES (should fix)")
        print("=" * 60)
        for issue in high_issues[:5]:  # Max 5 high
            print(format_issue(issue))
        if len(high_issues) > 5:
            print(f"   ... and {len(high_issues) - 5} more high issues\n")
    
    # Print medium issues summary (informational)
    if medium_issues:
        print("=" * 60)
        print(f"💡 MEDIUM ISSUES: {len(medium_issues)} found (informational)")
        print("=" * 60)
        # Just summarize, don't enumerate
        medium_types = {}
        for issue in medium_issues:
            medium_types[issue['name']] = medium_types.get(issue['name'], 0) + 1
        for name, count in medium_types.items():
            print(f"   - {name}: {count} instances")
        print()
    
    # Decision: block or warn
    if critical_issues:
        print("=" * 60)
        print("❌ COMMIT BLOCKED")
        print("=" * 60)
        print("Fix critical issues before committing.")
        print("")
        print("To bypass (emergency only):")
        print("  SKIP_AUDIT=1 git commit -m 'message'")
        print("")
        sys.exit(1)
    else:
        print("=" * 60)
        print("✅ COMMIT ALLOWED (with warnings)")
        print("=" * 60)
        print("Consider fixing high/medium issues when possible.")
        print("")
        sys.exit(0)


if __name__ == '__main__':
    main()
