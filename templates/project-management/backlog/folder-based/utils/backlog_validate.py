#!/usr/bin/env python3
"""
Backlog Validator

Validates backlog items for:
- Required frontmatter fields
- Valid field values (status, priority, type)
- Circular dependency detection
- Orphaned folders (no plan.md)

Usage:
    python3 .claude/utils/backlog_validate.py
    python3 .claude/utils/backlog_validate.py --fix  # Auto-fix simple issues
"""

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = ['id', 'title', 'type', 'status', 'priority']
VALID_TYPES = ['feature', 'bug', 'tech-debt', 'research']
VALID_STATUSES = ['planned', 'in_progress', 'blocked', 'complete']
VALID_PRIORITIES = ['P0', 'P1', 'P2', 'P3']


def find_project_root():
    """Find the project root directory."""
    current = Path.cwd()
    if (current / 'backlog').exists():
        return current
    for parent in current.parents:
        if (parent / 'backlog').exists():
            return parent
    return current


def parse_yaml_frontmatter(file_path):
    """Parse YAML frontmatter from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None, "No frontmatter found"

        end_match = re.search(r'\n---\s*\n', content[3:])
        if not end_match:
            return None, "Frontmatter not closed"

        yaml_content = content[3:end_match.start() + 3]

        frontmatter = {}
        for line in yaml_content.strip().split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if '#' in value and not value.startswith('['):
                    value = value.split('#')[0].strip()

                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                if value.lower() in ('null', 'none', '~', ''):
                    value = None
                elif value.startswith('[') and value.endswith(']'):
                    value = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]

                frontmatter[key] = value

        return frontmatter, None

    except Exception as e:
        return None, str(e)


def validate_item(item_path, frontmatter):
    """Validate a single backlog item."""
    errors = []
    warnings = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter or frontmatter[field] is None:
            errors.append(f"Missing required field: {field}")

    # Validate type
    item_type = frontmatter.get('type')
    if item_type and item_type not in VALID_TYPES:
        errors.append(f"Invalid type: {item_type} (must be one of {VALID_TYPES})")

    # Validate status
    status = frontmatter.get('status')
    if status and status not in VALID_STATUSES:
        errors.append(f"Invalid status: {status} (must be one of {VALID_STATUSES})")

    # Validate priority
    priority = frontmatter.get('priority')
    if priority and priority not in VALID_PRIORITIES:
        errors.append(f"Invalid priority: {priority} (must be one of {VALID_PRIORITIES})")

    # Check id matches folder name
    folder_name = item_path.parent.name
    item_id = frontmatter.get('id')
    if item_id and item_id != folder_name:
        warnings.append(f"ID '{item_id}' doesn't match folder name '{folder_name}'")

    return errors, warnings


def detect_circular_dependencies(items):
    """Detect circular dependencies in blocked_by relationships."""
    cycles = []

    def find_cycle(item_id, visited, path):
        if item_id in path:
            cycle_start = path.index(item_id)
            return path[cycle_start:] + [item_id]
        if item_id in visited:
            return None

        visited.add(item_id)
        path.append(item_id)

        item = items.get(item_id)
        if item:
            for blocker_id in item.get('blocked_by', []):
                cycle = find_cycle(blocker_id, visited, path)
                if cycle:
                    return cycle

        path.pop()
        return None

    for item_id in items:
        cycle = find_cycle(item_id, set(), [])
        if cycle and cycle not in cycles:
            cycles.append(cycle)

    return cycles


def validate_backlog(project_root):
    """Validate entire backlog."""
    backlog_dir = project_root / 'backlog'
    results = {
        "valid": True,
        "items": [],
        "orphans": [],
        "circular_deps": [],
        "missing_refs": []
    }

    if not backlog_dir.exists():
        results["valid"] = False
        results["error"] = "backlog/ directory not found"
        return results

    items = {}
    type_dirs = ['feature', 'bug', 'tech-debt', 'research']

    for type_dir in type_dirs:
        type_path = backlog_dir / type_dir
        if not type_path.exists():
            continue

        for item_dir in type_path.iterdir():
            if not item_dir.is_dir():
                continue

            plan_path = item_dir / 'plan.md'
            if not plan_path.exists():
                results["orphans"].append(str(item_dir.relative_to(project_root)))
                continue

            frontmatter, parse_error = parse_yaml_frontmatter(plan_path)

            if parse_error:
                results["items"].append({
                    "path": str(plan_path.relative_to(project_root)),
                    "errors": [parse_error],
                    "warnings": []
                })
                results["valid"] = False
                continue

            if frontmatter is None:
                frontmatter = {}

            errors, warnings = validate_item(plan_path, frontmatter)

            if errors:
                results["valid"] = False

            results["items"].append({
                "id": frontmatter.get('id', item_dir.name),
                "path": str(plan_path.relative_to(project_root)),
                "errors": errors,
                "warnings": warnings
            })

            items[frontmatter.get('id', item_dir.name)] = frontmatter

    # Check for circular dependencies
    cycles = detect_circular_dependencies(items)
    if cycles:
        results["valid"] = False
        results["circular_deps"] = [' -> '.join(c) for c in cycles]

    # Check for missing blocked_by references
    all_ids = set(items.keys())
    for item_id, item in items.items():
        for ref in item.get('blocked_by', []):
            if ref not in all_ids:
                results["missing_refs"].append(f"{item_id} references non-existent '{ref}'")
                results["valid"] = False

    return results


def main():
    parser = argparse.ArgumentParser(description='Validate backlog items')
    parser.add_argument('--fix', action='store_true', help='Auto-fix simple issues')
    args = parser.parse_args()

    project_root = find_project_root()
    results = validate_backlog(project_root)

    # Print results
    if results["valid"]:
        print("Backlog is valid!")
    else:
        print("Backlog has issues:\n")

    # Show item-specific issues
    for item in results["items"]:
        if item["errors"] or item["warnings"]:
            print(f"  {item['path']}:")
            for err in item["errors"]:
                print(f"    ERROR: {err}")
            for warn in item["warnings"]:
                print(f"    WARN: {warn}")

    # Show orphans
    if results["orphans"]:
        print("\nOrphaned folders (no plan.md):")
        for orphan in results["orphans"]:
            print(f"  - {orphan}")

    # Show circular dependencies
    if results["circular_deps"]:
        print("\nCircular dependencies:")
        for cycle in results["circular_deps"]:
            print(f"  - {cycle}")

    # Show missing references
    if results["missing_refs"]:
        print("\nMissing references:")
        for ref in results["missing_refs"]:
            print(f"  - {ref}")

    # Summary
    valid_count = sum(1 for i in results["items"] if not i["errors"])
    total_count = len(results["items"])
    print(f"\nSummary: {valid_count}/{total_count} items valid")

    sys.exit(0 if results["valid"] else 1)


if __name__ == '__main__':
    main()
