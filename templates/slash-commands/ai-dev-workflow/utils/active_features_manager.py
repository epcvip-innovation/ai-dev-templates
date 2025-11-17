#!/usr/bin/env python3
"""
Active Features Manager

Manages .active-features index file (add, remove, list, is-active operations).
Returns JSON for machine parsing.

Usage:
    python3 .claude/utils/active_features_manager.py add "feature-name"
    python3 .claude/utils/active_features_manager.py remove "feature-name"
    python3 .claude/utils/active_features_manager.py list
    python3 .claude/utils/active_features_manager.py is-active "feature-name"

Output: JSON to stdout
    {"success": true, "message": "...", "features": [...]}
    {"success": false, "error": "..."}
"""

import json
import sys
from pathlib import Path


def find_project_root():
    """Find the project root directory (where .active-features should exist)."""
    current = Path.cwd()

    # Try current directory first
    if (current / '.active-features').exists() or (current / '.claude').exists():
        return current

    # Walk up to find .claude directory
    for parent in current.parents:
        if (parent / '.claude').exists():
            return parent

    # Fallback: assume we're in project root
    return current


def get_active_features_path():
    """Get path to .active-features file."""
    return find_project_root() / '.active-features'


def get_features_dir():
    """Get path to features directory."""
    return find_project_root() / 'docs' / 'planning' / 'features'


def read_active_features():
    """
    Read current active features from .active-features file.

    Returns:
        list: Feature names (empty list if file doesn't exist)
    """
    path = get_active_features_path()

    if not path.exists():
        return []

    features = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                features.append(line)

    return features


def write_active_features(features):
    """
    Write active features to .active-features file.

    Args:
        features: List of feature names
    """
    path = get_active_features_path()

    with open(path, 'w') as f:
        f.write("# Active Features Index\n")
        f.write("# Auto-maintained by slash commands - DO NOT EDIT MANUALLY\n")
        f.write("# Format: feature-name (one per line, must match directory name in docs/planning/features/)\n")
        f.write("\n")

        for feature in sorted(features):
            f.write(f"{feature}\n")


def feature_exists(feature_name):
    """
    Check if feature directory exists.

    Args:
        feature_name: Name of feature

    Returns:
        bool: True if feature directory exists
    """
    features_dir = get_features_dir()
    feature_path = features_dir / feature_name

    return feature_path.exists() and feature_path.is_dir()


def add_feature(feature_name):
    """
    Add feature to .active-features file.

    Args:
        feature_name: Name of feature to add

    Returns:
        dict: JSON result with success/error
    """
    # Validate feature exists
    if not feature_exists(feature_name):
        return {
            "success": False,
            "error": f"Feature directory does not exist: docs/planning/features/{feature_name}/"
        }

    features = read_active_features()

    # Check if already active
    if feature_name in features:
        return {
            "success": True,
            "message": f"Feature '{feature_name}' already active (no change)",
            "features": features
        }

    # Add feature
    features.append(feature_name)
    write_active_features(features)

    return {
        "success": True,
        "message": f"Added '{feature_name}' to active features",
        "features": sorted(features)
    }


def remove_feature(feature_name):
    """
    Remove feature from .active-features file.

    Args:
        feature_name: Name of feature to remove

    Returns:
        dict: JSON result with success/error
    """
    features = read_active_features()

    # Check if feature is active
    if feature_name not in features:
        return {
            "success": True,
            "message": f"Feature '{feature_name}' not in active features (no change)",
            "features": features
        }

    # Remove feature
    features.remove(feature_name)
    write_active_features(features)

    return {
        "success": True,
        "message": f"Removed '{feature_name}' from active features",
        "features": sorted(features)
    }


def list_features():
    """
    List all active features.

    Returns:
        dict: JSON result with feature list
    """
    features = read_active_features()

    return {
        "success": True,
        "count": len(features),
        "features": sorted(features)
    }


def is_active(feature_name):
    """
    Check if feature is active.

    Args:
        feature_name: Name of feature to check

    Returns:
        dict: JSON result with active status
    """
    features = read_active_features()
    active = feature_name in features

    return {
        "success": True,
        "feature": feature_name,
        "is_active": active
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        result = {
            "success": False,
            "error": "Usage: active_features_manager.py {add|remove|list|is-active} [feature-name]"
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            result = {"success": False, "error": "Missing feature name for 'add' command"}
            print(json.dumps(result, indent=2))
            sys.exit(1)
        result = add_feature(sys.argv[2])

    elif command == "remove":
        if len(sys.argv) < 3:
            result = {"success": False, "error": "Missing feature name for 'remove' command"}
            print(json.dumps(result, indent=2))
            sys.exit(1)
        result = remove_feature(sys.argv[2])

    elif command == "list":
        result = list_features()

    elif command == "is-active":
        if len(sys.argv) < 3:
            result = {"success": False, "error": "Missing feature name for 'is-active' command"}
            print(json.dumps(result, indent=2))
            sys.exit(1)
        result = is_active(sys.argv[2])

    else:
        result = {
            "success": False,
            "error": f"Unknown command '{command}'. Valid: add, remove, list, is-active"
        }

    # Output JSON
    print(json.dumps(result, indent=2))

    # Exit code based on success
    sys.exit(0 if result.get("success", False) else 1)


if __name__ == '__main__':
    main()

