#!/usr/bin/env python3
"""
Feature Discovery Utility

Discovers active features from .active-features file (primary) or
FEATURES_BACKLOG.md using grep (fallback). Validates HANDOFF.md status.

Usage:
    python3 .claude/utils/feature_discovery.py

Output:
    JSON with feature count and structured feature data
"""

import subprocess
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


def read_active_features_file():
    """
    Read active features from .active-features file.

    Returns:
        list: Feature names (empty if file doesn't exist)
    """
    project_root = find_project_root()
    active_features_path = project_root / '.active-features'

    if not active_features_path.exists():
        return None  # Signal to use fallback

    features = []
    with open(active_features_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                features.append(line)

    return features


def validate_handoff_status(feature_name):
    """
    Validate HANDOFF.md has proper Status line in first 10 lines.

    Args:
        feature_name: Name of feature

    Returns:
        dict: {"valid": bool, "error": str (if invalid)}
    """
    project_root = find_project_root()
    handoff_path = project_root / 'docs' / 'planning' / 'features' / feature_name / 'HANDOFF.md'

    if not handoff_path.exists():
        return {
            "valid": False,
            "error": f"HANDOFF.md not found for feature '{feature_name}'"
        }

    try:
        # Read only first 10 lines (minimal context)
        with open(handoff_path, 'r') as f:
            lines = [f.readline() for _ in range(10)]

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
            "error": f"Missing **Status:** line in first 10 lines of HANDOFF.md"
        }

    except Exception as e:
        return {
            "valid": False,
            "error": f"Failed to read HANDOFF.md: {str(e)}"
        }


def discover_features():
    """
    Find active features from .active-features file (primary) or
    FEATURES_BACKLOG.md grep (fallback). Validates HANDOFF.md status.

    Returns:
        dict: JSON structure with count and active_features list
    """
    # Try primary method: .active-features file
    feature_names = read_active_features_file()

    if feature_names is None:
        # Fallback to grep method
        return discover_features_grep()

    # Build feature data with validation
    features = []
    for name in feature_names:
        feature_data = {
            "name": name,
            "remaining_hours": None,
            "blocked": False,
            "status_summary": "In Progress"
        }

        # Validate HANDOFF.md status
        status_check = validate_handoff_status(name)
        if not status_check["valid"]:
            feature_data["status_warning"] = status_check["error"]

        features.append(feature_data)

    return {
        "count": len(features),
        "active_features": features
    }


def discover_features_grep():
    """
    Fallback: Find active features using grep on FEATURES_BACKLOG.md.

    Returns:
        dict: JSON structure with count and active_features list
    """
    project_root = find_project_root()
    backlog_path = project_root / 'docs' / 'planning' / 'FEATURES_BACKLOG.md'

    if not backlog_path.exists():
        return {
            "count": 0,
            "active_features": [],
            "error": f"FEATURES_BACKLOG.md not found at {backlog_path}"
        }

    try:
        # Use grep to extract only "In Progress" section (minimal context)
        # -A 100 allows for multiple features (~30-40 lines each)
        result = subprocess.run(
            ['grep', '-A', '100', '🚧 In Progress', str(backlog_path)],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0 or not result.stdout.strip():
            # No features in progress
            return {
                "count": 0,
                "active_features": []
            }

        features = parse_grep_output(result.stdout)

        return {
            "count": len(features),
            "active_features": features
        }

    except Exception as e:
        return {
            "count": 0,
            "active_features": [],
            "error": f"Failed to discover features: {str(e)}"
        }


def parse_grep_output(grep_output):
    """
    Parse grep output into structured feature list.
    
    Expected format from FEATURES_BACKLOG.md:
        ### Feature Name ⭐
        **Status:** In Progress (Phase X)
        **Started:** 2025-11-15
        **Effort:** 12h total, 8h done (67%)
        ...
        **Blockers:** None / [blocker description]
    
    Args:
        grep_output: Raw output from grep command
        
    Returns:
        list: Structured feature data
    """
    features = []
    lines = grep_output.strip().split('\n')
    
    current_feature = None
    
    for line in lines:
        line = line.strip()
        
        # Feature name line (starts with ###)
        if line.startswith('###'):
            # Save previous feature if exists
            if current_feature and current_feature.get('name'):
                features.append(current_feature)
            
            # Start new feature
            name_match = re.search(r'###\s+(.+?)(?:\s+⭐)?$', line)
            if name_match:
                current_feature = {
                    "name": name_match.group(1).strip(),
                    "remaining_hours": None,
                    "blocked": False,
                    "status_summary": "In Progress"
                }
        
        elif current_feature:
            # Extract effort/remaining hours
            if '**Effort:**' in line:
                # Try to extract remaining hours
                remaining_match = re.search(r'(\d+)h\s+remaining', line, re.IGNORECASE)
                if remaining_match:
                    current_feature['remaining_hours'] = int(remaining_match.group(1))
                else:
                    # Try to calculate from "Xh total, Yh done"
                    total_match = re.search(r'(\d+)h\s+total.*?(\d+)h\s+done', line)
                    if total_match:
                        total = int(total_match.group(1))
                        done = int(total_match.group(2))
                        current_feature['remaining_hours'] = total - done
            
            # Extract blocker status
            elif '**Blockers:**' in line:
                current_feature['blocked'] = 'None' not in line and line.strip() != '**Blockers:**'
                if current_feature['blocked']:
                    # Extract blocker description
                    blocker_match = re.search(r'\*\*Blockers:\*\*\s+(.+)', line)
                    if blocker_match:
                        current_feature['status_summary'] = blocker_match.group(1).strip()
            
            # Extract status summary
            elif '**Status:**' in line:
                status_match = re.search(r'\*\*Status:\*\*\s+(.+)', line)
                if status_match:
                    status_text = status_match.group(1).strip()
                    # Remove "In Progress" since that's redundant
                    status_text = re.sub(r'^In Progress\s*\(?\s*', '', status_text)
                    status_text = re.sub(r'\)?$', '', status_text)
                    if status_text:
                        current_feature['status_summary'] = status_text
            
            # Stop parsing this feature at separator
            elif line.startswith('---') or line.startswith('##'):
                if current_feature.get('name'):
                    features.append(current_feature)
                    current_feature = None
    
    # Add last feature if exists
    if current_feature and current_feature.get('name'):
        features.append(current_feature)
    
    return features


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

