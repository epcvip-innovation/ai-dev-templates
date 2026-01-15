#!/usr/bin/env python3
"""
Active Features Manager (Frontmatter-based)

Manages feature status via plan.md YAML frontmatter.
Replaces the old .active-features index file approach.

Usage:
    python3 .claude/utils/active_features_manager.py list
    python3 .claude/utils/active_features_manager.py is-active "feature-name"
    python3 .claude/utils/active_features_manager.py set-status "feature-name" "in_progress"
    python3 .claude/utils/active_features_manager.py set-status "feature-name" "complete"

Output: JSON to stdout
    {"success": true, "message": "...", "features": [...]}
    {"success": false, "error": "..."}
"""

import json
import re
import sys
from pathlib import Path


def find_project_root():
    """Find the project root directory (where backlog/ should exist)."""
    current = Path.cwd()

    # Try current directory first
    if (current / 'backlog').exists() or (current / '.claude').exists():
        return current

    # Walk up to find backlog directory
    for parent in current.parents:
        if (parent / 'backlog').exists() or (parent / '.claude').exists():
            return parent

    # Fallback: assume we're in project root
    return current


def get_backlog_dir():
    """Get path to backlog directory."""
    return find_project_root() / 'backlog'


def parse_yaml_frontmatter(file_path):
    """
    Parse YAML frontmatter from a markdown file.
    
    Returns:
        tuple: (frontmatter_dict, full_content, frontmatter_end_pos)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            return {}, content, 0
        
        end_match = re.search(r'\n---\s*\n', content[3:])
        if not end_match:
            return {}, content, 0
        
        yaml_content = content[3:end_match.start() + 3]
        frontmatter_end = end_match.end() + 3
        
        frontmatter = {}
        for line in yaml_content.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                if value.lower() in ('null', 'none', '~', ''):
                    value = None
                elif value.startswith('[') and value.endswith(']'):
                    value = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]
                
                frontmatter[key] = value
        
        return frontmatter, content, frontmatter_end
        
    except Exception as e:
        return {"_error": str(e)}, "", 0


def update_frontmatter_field(file_path, field, value):
    """
    Update a field in the YAML frontmatter.
    
    Args:
        file_path: Path to markdown file
        field: Field name to update
        value: New value
        
    Returns:
        bool: True if successful
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            return False
        
        end_match = re.search(r'\n---\s*\n', content[3:])
        if not end_match:
            return False
        
        yaml_end = end_match.start() + 3
        yaml_content = content[3:yaml_end]
        rest_of_file = content[end_match.end() + 3:]
        
        # Format value for YAML
        if value is None:
            yaml_value = 'null'
        elif isinstance(value, list):
            yaml_value = '[' + ', '.join(value) + ']'
        elif isinstance(value, bool):
            yaml_value = 'true' if value else 'false'
        else:
            yaml_value = str(value)
        
        # Check if field exists
        field_pattern = re.compile(rf'^{re.escape(field)}:\s*.*$', re.MULTILINE)
        
        if field_pattern.search(yaml_content):
            # Update existing field
            new_yaml = field_pattern.sub(f'{field}: {yaml_value}', yaml_content)
        else:
            # Add new field before closing ---
            new_yaml = yaml_content.rstrip() + f'\n{field}: {yaml_value}\n'
        
        # Reconstruct file
        new_content = '---' + new_yaml + '---\n' + rest_of_file
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception:
        return False


def feature_exists(feature_name):
    """Check if feature directory exists."""
    backlog_dir = get_backlog_dir()
    feature_path = backlog_dir / feature_name
    return feature_path.exists() and feature_path.is_dir()


def list_features():
    """
    List all active features (status: in_progress).
    
    Returns:
        dict: JSON result with feature list
    """
    backlog_dir = get_backlog_dir()
    
    if not backlog_dir.exists():
        return {
            "success": False,
            "error": f"backlog/ directory not found"
        }
    
    features = []
    
    for item in backlog_dir.iterdir():
        if item.is_dir() and not item.name.startswith('_'):
            plan_path = item / 'plan.md'
            if plan_path.exists():
                frontmatter, _, _ = parse_yaml_frontmatter(plan_path)
                status = frontmatter.get('status', '').lower()
                
                if status == 'in_progress':
                    features.append({
                        "name": item.name,
                        "id": frontmatter.get('id', item.name),
                        "title": frontmatter.get('title'),
                        "priority": frontmatter.get('priority'),
                        "effort_estimate": frontmatter.get('effort_estimate')
                    })
    
    # Sort by priority
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3, None: 9}
    features.sort(key=lambda f: priority_order.get(f.get('priority'), 9))
    
    return {
        "success": True,
        "count": len(features),
        "features": features
    }


def is_active(feature_name):
    """
    Check if feature is active (status: in_progress).
    
    Returns:
        dict: JSON result with active status
    """
    backlog_dir = get_backlog_dir()
    plan_path = backlog_dir / feature_name / 'plan.md'
    
    if not plan_path.exists():
        return {
            "success": False,
            "error": f"Feature not found: {feature_name}"
        }
    
    frontmatter, _, _ = parse_yaml_frontmatter(plan_path)
    status = frontmatter.get('status', '').lower()
    
    return {
        "success": True,
        "feature": feature_name,
        "is_active": status == 'in_progress',
        "status": status
    }


def set_status(feature_name, new_status):
    """
    Set feature status in frontmatter.
    
    Valid statuses: planned, in_progress, complete, on_hold
    
    Returns:
        dict: JSON result
    """
    valid_statuses = ['planned', 'in_progress', 'complete', 'on_hold']
    
    if new_status.lower() not in valid_statuses:
        return {
            "success": False,
            "error": f"Invalid status '{new_status}'. Valid: {', '.join(valid_statuses)}"
        }
    
    backlog_dir = get_backlog_dir()
    plan_path = backlog_dir / feature_name / 'plan.md'
    
    if not plan_path.exists():
        return {
            "success": False,
            "error": f"Feature not found: {feature_name}"
        }
    
    if update_frontmatter_field(plan_path, 'status', new_status.lower()):
        # Also update timestamps
        from datetime import date
        today = date.today().isoformat()
        
        if new_status.lower() == 'in_progress':
            update_frontmatter_field(plan_path, 'started', today)
        elif new_status.lower() == 'complete':
            update_frontmatter_field(plan_path, 'completed', today)
        
        return {
            "success": True,
            "message": f"Set '{feature_name}' status to '{new_status}'",
            "feature": feature_name,
            "status": new_status.lower()
        }
    else:
        return {
            "success": False,
            "error": f"Failed to update frontmatter in {plan_path}"
        }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        result = {
            "success": False,
            "error": "Usage: active_features_manager.py {list|is-active|set-status} [feature-name] [status]"
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list":
        result = list_features()

    elif command == "is-active":
        if len(sys.argv) < 3:
            result = {"success": False, "error": "Missing feature name for 'is-active' command"}
            print(json.dumps(result, indent=2))
            sys.exit(1)
        result = is_active(sys.argv[2])

    elif command == "set-status":
        if len(sys.argv) < 4:
            result = {"success": False, "error": "Usage: set-status <feature-name> <status>"}
            print(json.dumps(result, indent=2))
            sys.exit(1)
        result = set_status(sys.argv[2], sys.argv[3])

    # Legacy commands - show deprecation notice
    elif command in ("add", "remove"):
        result = {
            "success": False,
            "error": f"Command '{command}' is deprecated. Use 'set-status <feature> in_progress' or 'set-status <feature> complete' instead."
        }

    else:
        result = {
            "success": False,
            "error": f"Unknown command '{command}'. Valid: list, is-active, set-status"
        }

    # Output JSON
    print(json.dumps(result, indent=2))

    # Exit code based on success
    sys.exit(0 if result.get("success", False) else 1)


if __name__ == '__main__':
    main()
