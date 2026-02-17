#!/usr/bin/env python3
"""
Backlog Search Utility

Searches backlog items by title, tags, type, or status.
Used by add-backlog skill to detect duplicates before creating new items.

Usage:
    python3 .claude/utils/backlog_search.py "search query"
    python3 .claude/utils/backlog_search.py --type feature "query"
    python3 .claude/utils/backlog_search.py --status planned "query"
    python3 .claude/utils/backlog_search.py --check-duplicate "exact title"
"""

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path


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

        return frontmatter

    except Exception:
        return {}


def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def scan_all_items(project_root):
    """Scan all backlog items."""
    backlog_dir = project_root / 'backlog'
    items = []

    if not backlog_dir.exists():
        return items

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
            if not frontmatter:
                continue

            items.append({
                "id": frontmatter.get('id', item_dir.name),
                "title": frontmatter.get('title', item_dir.name),
                "type": frontmatter.get('type', type_dir),
                "status": frontmatter.get('status', 'planned'),
                "priority": frontmatter.get('priority', 'P3'),
                "tags": frontmatter.get('tags', []),
                "path": str(plan_path.relative_to(project_root))
            })

    return items


def search_items(items, query, type_filter=None, status_filter=None):
    """Search items by query with optional filters."""
    results = []
    query_lower = query.lower()

    for item in items:
        # Apply filters
        if type_filter and item['type'] != type_filter:
            continue
        if status_filter and item['status'] != status_filter:
            continue

        # Calculate relevance score
        title_lower = item['title'].lower()
        id_lower = item['id'].lower()
        tags_text = ' '.join(item.get('tags', [])).lower()

        score = 0

        # Exact match in title
        if query_lower in title_lower:
            score += 100

        # Exact match in id
        if query_lower in id_lower:
            score += 80

        # Exact match in tags
        if query_lower in tags_text:
            score += 60

        # Fuzzy match
        title_sim = similarity(query, item['title'])
        if title_sim > 0.6:
            score += int(title_sim * 50)

        # Word match
        query_words = set(query_lower.split())
        title_words = set(title_lower.split())
        common_words = query_words & title_words
        if common_words:
            score += len(common_words) * 20

        if score > 0:
            results.append({**item, "_score": score})

    # Sort by score descending
    results.sort(key=lambda x: x['_score'], reverse=True)

    return results


def check_duplicate(items, title, threshold=0.85):
    """Check if a title is too similar to existing items."""
    duplicates = []

    for item in items:
        sim = similarity(title, item['title'])
        if sim >= threshold:
            duplicates.append({
                **item,
                "_similarity": round(sim, 2)
            })

    duplicates.sort(key=lambda x: x['_similarity'], reverse=True)
    return duplicates


def main():
    parser = argparse.ArgumentParser(description='Search backlog items')
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--type', choices=['feature', 'bug', 'tech-debt', 'research'],
                        help='Filter by type')
    parser.add_argument('--status', choices=['planned', 'in_progress', 'blocked', 'complete'],
                        help='Filter by status')
    parser.add_argument('--check-duplicate', metavar='TITLE',
                        help='Check if title is a duplicate')
    parser.add_argument('--threshold', type=float, default=0.85,
                        help='Similarity threshold for duplicate detection (default: 0.85)')
    args = parser.parse_args()

    project_root = find_project_root()
    items = scan_all_items(project_root)

    if args.check_duplicate:
        duplicates = check_duplicate(items, args.check_duplicate, args.threshold)
        if duplicates:
            print(json.dumps({
                "is_duplicate": True,
                "similar_items": duplicates
            }, indent=2))
            sys.exit(1)
        else:
            print(json.dumps({
                "is_duplicate": False,
                "similar_items": []
            }, indent=2))
            sys.exit(0)

    if not args.query:
        # List all items
        print(json.dumps({"items": items}, indent=2))
        sys.exit(0)

    results = search_items(items, args.query, args.type, args.status)

    print(json.dumps({
        "query": args.query,
        "filters": {
            "type": args.type,
            "status": args.status
        },
        "count": len(results),
        "results": results
    }, indent=2))

    sys.exit(0)


if __name__ == '__main__':
    main()
