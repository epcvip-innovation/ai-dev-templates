#!/usr/bin/env python3
"""
Feature Discovery Utility

Discovers active features by scanning backlog/*/plan.md files and reading
YAML frontmatter. Features with status: in_progress are considered active.

Usage:
    python3 .claude/utils/feature_discovery.py

Output:
    JSON with feature count and structured feature data
"""

import json
import re
import sys
from pathlib import Path


def find_project_root():
    """Find the project root directory (where backlog/ or .claude/ exists)."""
    current = Path.cwd()
    
    # Try current directory first
    if (current / 'backlog').exists() or (current / '.claude').exists():
        return current
    
    # Walk up to find backlog or .claude directory
    for parent in current.parents:
        if (parent / 'backlog').exists() or (parent / '.claude').exists():
            return parent
    
    # Fallback: assume we're in project root
    return current


def parse_yaml_frontmatter(file_path):
    """
    Parse YAML frontmatter from a markdown file.
    
    Args:
        file_path: Path to markdown file
        
    Returns:
        dict: Parsed frontmatter fields (empty dict if no frontmatter)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for YAML frontmatter (starts with ---)
        if not content.startswith('---'):
            return {}
        
        # Find the closing ---
        end_match = re.search(r'\n---\s*\n', content[3:])
        if not end_match:
            return {}
        
        yaml_content = content[3:end_match.start() + 3]
        
        # Simple YAML parsing (key: value pairs)
        frontmatter = {}
        for line in yaml_content.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                # Handle null values
                if value.lower() in ('null', 'none', '~', ''):
                    value = None
                # Handle arrays (simple format: [a, b, c])
                elif value.startswith('[') and value.endswith(']'):
                    value = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]
                
                frontmatter[key] = value
        
        return frontmatter
        
    except Exception as e:
        return {"_error": str(e)}


def validate_handoff_status(feature_dir):
    """
    Validate HANDOFF.md has proper Status line in first 10 lines.
    
    Args:
        feature_dir: Path to feature directory
        
    Returns:
        dict: {"valid": bool, "error": str (if invalid), "status": str (if found)}
    """
    handoff_path = feature_dir / 'HANDOFF.md'
    
    if not handoff_path.exists():
        return {
            "valid": True,  # HANDOFF.md is optional
            "has_handoff": False
        }
    
    try:
        with open(handoff_path, 'r', encoding='utf-8') as f:
            lines = [f.readline() for _ in range(10)]
        
        status_pattern = re.compile(r'\*\*Status\*\*:\s*(.+)')
        
        for line in lines:
            match = status_pattern.search(line)
            if match:
                return {
                    "valid": True,
                    "has_handoff": True,
                    "status": match.group(1).strip()
                }
        
        return {
            "valid": False,
            "has_handoff": True,
            "error": "Missing **Status:** line in first 10 lines of HANDOFF.md"
        }
        
    except Exception as e:
        return {
            "valid": False,
            "has_handoff": True,
            "error": f"Failed to read HANDOFF.md: {str(e)}"
        }


def discover_features():
    """
    Discover active features by scanning backlog/*/plan.md frontmatter.
    
    Returns:
        dict: JSON structure with count and active_features list
    """
    project_root = find_project_root()
    backlog_dir = project_root / 'backlog'
    
    if not backlog_dir.exists():
        return {
            "count": 0,
            "active_features": [],
            "error": f"backlog/ directory not found in {project_root}"
        }
    
    features = []
    
    # Scan all directories in backlog (excluding _ prefixed files)
    for item in backlog_dir.iterdir():
        if item.is_dir() and not item.name.startswith('_'):
            plan_path = item / 'plan.md'
            
            if plan_path.exists():
                frontmatter = parse_yaml_frontmatter(plan_path)
                
                if frontmatter.get('_error'):
                    continue
                
                status = frontmatter.get('status', '').lower()
                
                # Only include in_progress features
                if status == 'in_progress':
                    # Calculate remaining hours if we have estimate and actual
                    remaining_hours = None
                    effort_estimate = frontmatter.get('effort_estimate')
                    effort_actual = frontmatter.get('effort_actual')
                    
                    if effort_estimate:
                        # Parse "Xh" format
                        est_match = re.search(r'(\d+)', str(effort_estimate))
                        if est_match:
                            total = int(est_match.group(1))
                            if effort_actual:
                                act_match = re.search(r'(\d+)', str(effort_actual))
                                if act_match:
                                    done = int(act_match.group(1))
                                    remaining_hours = max(0, total - done)
                            else:
                                remaining_hours = total
                    
                    # Check HANDOFF.md
                    handoff_check = validate_handoff_status(item)
                    
                    feature_data = {
                        "id": frontmatter.get('id', item.name),
                        "name": item.name,
                        "title": frontmatter.get('title', item.name),
                        "status": status,
                        "priority": frontmatter.get('priority'),
                        "effort_estimate": effort_estimate,
                        "effort_actual": effort_actual,
                        "remaining_hours": remaining_hours,
                        "blocked": frontmatter.get('blocked', False),
                        "started": frontmatter.get('started'),
                        "component": frontmatter.get('component'),
                        "plan_path": str(plan_path.relative_to(project_root))
                    }
                    
                    # Add handoff status
                    if handoff_check.get('status'):
                        feature_data["status_summary"] = handoff_check['status']
                    if handoff_check.get('error'):
                        feature_data["status_warning"] = handoff_check['error']
                    
                    features.append(feature_data)
    
    # Sort by priority (P0 > P1 > P2 > P3)
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3, None: 9}
    features.sort(key=lambda f: priority_order.get(f.get('priority'), 9))
    
    return {
        "count": len(features),
        "active_features": features
    }


def main():
    """Main entry point."""
    result = discover_features()
    
    # Pretty print JSON
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    if 'error' in result:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
