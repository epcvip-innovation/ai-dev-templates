#!/usr/bin/env python3
"""
Backlog Index Generator

Scans backlog/*/plan.md files, parses YAML frontmatter, and generates
_INDEX.md with categorized views. Can also output JSON for skill consumption.

Usage:
    python3 .claude/utils/backlog_index.py           # Preview markdown
    python3 .claude/utils/backlog_index.py --json    # Output JSON only
    python3 .claude/utils/backlog_index.py --write   # Write _INDEX.md to disk
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def find_project_root():
    """Find the project root directory (where backlog/ exists)."""
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
            return {}

        end_match = re.search(r'\n---\s*\n', content[3:])
        if not end_match:
            return {}

        yaml_content = content[3:end_match.start() + 3]

        frontmatter = {}
        for line in yaml_content.strip().split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Remove inline comments
                if '#' in value and not value.startswith('['):
                    value = value.split('#')[0].strip()

                # Remove quotes
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                # Handle null
                if value.lower() in ('null', 'none', '~', ''):
                    value = None
                # Handle arrays
                elif value.startswith('[') and value.endswith(']'):
                    value = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]

                frontmatter[key] = value

        return frontmatter

    except Exception as e:
        return {"_error": str(e), "_path": str(file_path)}


def scan_backlog(project_root):
    """Scan all backlog items and return structured data."""
    backlog_dir = project_root / 'backlog'

    if not backlog_dir.exists():
        return {"error": f"backlog/ not found in {project_root}", "items": []}

    items = []
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
                continue

            frontmatter = parse_yaml_frontmatter(plan_path)
            if frontmatter.get('_error'):
                items.append({
                    "id": item_dir.name,
                    "type": type_dir,
                    "_error": frontmatter['_error'],
                    "path": str(plan_path.relative_to(project_root))
                })
                continue

            items.append({
                "id": frontmatter.get('id', item_dir.name),
                "title": frontmatter.get('title', item_dir.name),
                "type": frontmatter.get('type', type_dir),
                "status": frontmatter.get('status', 'planned'),
                "priority": frontmatter.get('priority', 'P3'),
                "effort_estimate": frontmatter.get('effort_estimate'),
                "effort_actual": frontmatter.get('effort_actual'),
                "created": frontmatter.get('created'),
                "started": frontmatter.get('started'),
                "completed": frontmatter.get('completed'),
                "blocked_by": frontmatter.get('blocked_by', []),
                "related": frontmatter.get('related', []),
                "tags": frontmatter.get('tags', []),
                "path": str(plan_path.relative_to(project_root))
            })

    return {"items": items}


def categorize_items(items):
    """Categorize items by status and priority."""
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}

    in_progress = []
    blocked = []
    ready_high = []  # P0-P1
    backlog = []     # P2-P3

    for item in items:
        if item.get('_error'):
            continue

        status = item.get('status', 'planned').lower()
        priority = item.get('priority', 'P3')

        if status == 'in_progress':
            in_progress.append(item)
        elif status == 'blocked':
            blocked.append(item)
        elif status == 'planned':
            if priority in ('P0', 'P1'):
                ready_high.append(item)
            else:
                backlog.append(item)

    # Sort each category by priority
    for lst in [in_progress, blocked, ready_high, backlog]:
        lst.sort(key=lambda x: priority_order.get(x.get('priority', 'P3'), 9))

    return {
        "in_progress": in_progress,
        "blocked": blocked,
        "ready": ready_high,
        "backlog": backlog
    }


def generate_markdown(categories, items):
    """Generate _INDEX.md content."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Backlog Index",
        f"**Generated:** {now} (do not edit manually)",
        "",
    ]

    # In Progress
    lines.append(f"## In Progress ({len(categories['in_progress'])})")
    if categories['in_progress']:
        lines.append("| ID | Title | Priority | Type | Effort |")
        lines.append("|----|-------|----------|------|--------|")
        for item in categories['in_progress']:
            lines.append(f"| [{item['id']}]({item['path']}) | {item['title']} | {item['priority']} | {item['type']} | {item.get('effort_estimate', '-')} |")
    else:
        lines.append("*None*")
    lines.append("")

    # Blocked
    lines.append(f"## Blocked ({len(categories['blocked'])})")
    if categories['blocked']:
        lines.append("| ID | Title | Blocked By |")
        lines.append("|----|-------|------------|")
        for item in categories['blocked']:
            blocked_by = ', '.join(item.get('blocked_by', [])) or '-'
            lines.append(f"| [{item['id']}]({item['path']}) | {item['title']} | {blocked_by} |")
    else:
        lines.append("*None*")
    lines.append("")

    # Ready (P0-P1)
    lines.append(f"## Ready (P0-P1) ({len(categories['ready'])})")
    if categories['ready']:
        lines.append("| ID | Title | Priority | Type | Effort |")
        lines.append("|----|-------|----------|------|--------|")
        for item in categories['ready']:
            lines.append(f"| [{item['id']}]({item['path']}) | {item['title']} | {item['priority']} | {item['type']} | {item.get('effort_estimate', '-')} |")
    else:
        lines.append("*None*")
    lines.append("")

    # Backlog (P2-P3)
    lines.append(f"## Backlog (P2-P3) ({len(categories['backlog'])})")
    if categories['backlog']:
        lines.append("| ID | Title | Priority | Type | Effort |")
        lines.append("|----|-------|----------|------|--------|")
        for item in categories['backlog']:
            lines.append(f"| [{item['id']}]({item['path']}) | {item['title']} | {item['priority']} | {item['type']} | {item.get('effort_estimate', '-')} |")
    else:
        lines.append("*None*")
    lines.append("")

    # Stats
    total = len(items)
    in_progress_count = len(categories['in_progress'])
    blocked_count = len(categories['blocked'])

    lines.extend([
        "---",
        "",
        "## Stats",
        f"- **Total:** {total} items",
        f"- **In Progress:** {in_progress_count}",
        f"- **Blocked:** {blocked_count}",
        f"- **Ready (P0-P1):** {len(categories['ready'])}",
        f"- **Backlog (P2-P3):** {len(categories['backlog'])}",
        ""
    ])

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate backlog index')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of markdown')
    parser.add_argument('--write', action='store_true', help='Write _INDEX.md to disk')
    args = parser.parse_args()

    project_root = find_project_root()
    result = scan_backlog(project_root)

    if result.get('error'):
        print(json.dumps({"error": result['error']}, indent=2))
        sys.exit(1)

    items = result['items']
    categories = categorize_items(items)

    if args.json:
        output = {
            "generated": datetime.now().isoformat(),
            "summary": {
                "total": len(items),
                "in_progress": len(categories['in_progress']),
                "blocked": len(categories['blocked']),
                "ready": len(categories['ready']),
                "backlog": len(categories['backlog'])
            },
            "categories": categories
        }
        print(json.dumps(output, indent=2))
    else:
        markdown = generate_markdown(categories, items)

        if args.write:
            index_path = project_root / 'backlog' / '_INDEX.md'
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"Written to {index_path}")
        else:
            print(markdown)


if __name__ == '__main__':
    main()
