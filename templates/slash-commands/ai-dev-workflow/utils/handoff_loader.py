#!/usr/bin/env python3
"""
Handoff Loader Utility

Loads ONLY the selected feature's context (HANDOFF.md and plan.md).
Validates HANDOFF.md status line format. Prevents loading all features.

Usage:
    python3 .claude/utils/handoff_loader.py <feature-name>

Output:
    JSON with feature context and metadata
"""

import json
import re
import sys
from pathlib import Path


def find_project_root():
    """Find the project root directory (where .claude/ exists)."""
    current = Path.cwd()

    # Try current directory first
    if (current / '.claude').exists():
        return current

    # Walk up to find .claude directory
    for parent in current.parents:
        if (parent / '.claude').exists():
            return parent

    # Fallback: assume we're in project root
    return current


def validate_handoff_status(handoff_content):
    """
    Validate HANDOFF.md has proper Status line in first 10 lines.

    Args:
        handoff_content: Full HANDOFF.md content string

    Returns:
        dict: {"valid": bool, "error": str (if invalid)}
    """
    if not handoff_content:
        return {
            "valid": False,
            "error": "HANDOFF.md is empty"
        }

    # Read only first 10 lines (minimal context)
    lines = handoff_content.splitlines()[:10]

    # Look for **Status:** line
    status_pattern = re.compile(r'\*\*Status\*\*:\s*(.+)')

    for line in lines:
        match = status_pattern.search(line)
        if match:
            # Found status line - valid
            return {"valid": True}

    # No status line found in first 10 lines
    return {
        "valid": False,
        "error": "Missing **Status:** line in first 10 lines of HANDOFF.md"
    }


def load_feature_context(feature_name):
    """
    Load ONLY the selected feature's context files.
    
    Args:
        feature_name: Name of the feature (e.g., "session-based-auth")
        
    Returns:
        dict: JSON structure with feature context
    """
    project_root = find_project_root()
    feature_dir = project_root / 'docs' / 'planning' / 'features' / feature_name
    
    if not feature_dir.exists():
        return {
            "feature_name": feature_name,
            "error": f"Feature directory not found: {feature_dir}",
            "handoff_content": None,
            "plan_content": None,
            "files_loaded": [],
            "lines_loaded": 0
        }
    
    result = {
        "feature_name": feature_name,
        "handoff_content": None,
        "plan_content": None,
        "files_loaded": [],
        "lines_loaded": 0,
        "status_valid": False,
        "status_warning": None
    }

    # Load HANDOFF.md if exists
    handoff_path = feature_dir / 'HANDOFF.md'
    if handoff_path.exists():
        try:
            content = handoff_path.read_text(encoding='utf-8')
            result['handoff_content'] = content
            result['files_loaded'].append(str(handoff_path.relative_to(project_root)))
            result['lines_loaded'] += len(content.splitlines())

            # Validate status line
            status_check = validate_handoff_status(content)
            result['status_valid'] = status_check['valid']
            if not status_check['valid']:
                result['status_warning'] = status_check['error']

        except Exception as e:
            result['error'] = f"Failed to read HANDOFF.md: {str(e)}"
    
    # Load plan.md or README.md (prefer plan.md)
    plan_path = feature_dir / 'plan.md'
    readme_path = feature_dir / 'README.md'
    
    if plan_path.exists():
        try:
            content = plan_path.read_text(encoding='utf-8')
            result['plan_content'] = content
            result['files_loaded'].append(str(plan_path.relative_to(project_root)))
            result['lines_loaded'] += len(content.splitlines())
        except Exception as e:
            if 'error' in result:
                result['error'] += f"; Failed to read plan.md: {str(e)}"
            else:
                result['error'] = f"Failed to read plan.md: {str(e)}"
    
    elif readme_path.exists():
        try:
            content = readme_path.read_text(encoding='utf-8')
            result['plan_content'] = content
            result['files_loaded'].append(str(readme_path.relative_to(project_root)))
            result['lines_loaded'] += len(content.splitlines())
        except Exception as e:
            if 'error' in result:
                result['error'] += f"; Failed to read README.md: {str(e)}"
            else:
                result['error'] = f"Failed to read README.md: {str(e)}"
    
    # If no plan or handoff found, note it
    if not result['handoff_content'] and not result['plan_content']:
        result['error'] = f"No HANDOFF.md or plan.md/README.md found in {feature_dir}"
    
    return result


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: handoff_loader.py <feature-name>",
            "example": "python3 handoff_loader.py session-based-auth"
        }, indent=2), file=sys.stderr)
        sys.exit(1)
    
    feature_name = sys.argv[1]
    result = load_feature_context(feature_name)
    
    # Pretty print JSON
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    if 'error' in result:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

