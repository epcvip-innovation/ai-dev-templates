#!/usr/bin/env python3
"""
Plan Validator Utility

Runs the 3 boolean validation checks without loading PLAN_QUALITY_RUBRIC.md.
Compares original plan against current HANDOFF state.

Usage:
    python3 .claude/utils/plan_validator.py <feature-name>

Output:
    JSON with validation category (valid/update/invalid)
"""

import json
import sys
import re
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


def extract_goal(content):
    """Extract goal statement from markdown content."""
    if not content:
        return None
    
    # Look for "## Goal" or "## Problem" or "## Purpose" section
    goal_patterns = [
        r'##\s+Goal\s*\n+(.*?)(?=\n##|\Z)',
        r'##\s+Problem\s*\n+(.*?)(?=\n##|\Z)',
        r'##\s+Purpose\s*\n+(.*?)(?=\n##|\Z)',
        r'\*\*Goal:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)',
    ]
    
    for pattern in goal_patterns:
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        if match:
            goal = match.group(1).strip()
            # Take first paragraph only
            goal = goal.split('\n\n')[0]
            return goal[:500]  # Limit length
    
    return None


def extract_approach(content):
    """Extract technical approach from markdown content."""
    if not content:
        return None
    
    # Look for "## Approach" or "## Technical Approach" section
    approach_patterns = [
        r'##\s+(?:Technical\s+)?Approach\s*\n+(.*?)(?=\n##|\Z)',
        r'##\s+Solution\s*\n+(.*?)(?=\n##|\Z)',
        r'\*\*Approach:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)',
    ]
    
    for pattern in approach_patterns:
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        if match:
            approach = match.group(1).strip()
            # Take first 2 paragraphs
            paragraphs = approach.split('\n\n')[:2]
            return '\n\n'.join(paragraphs)[:800]  # Limit length
    
    return None


def check_goal_unchanged(original_goal, handoff_content):
    """
    Check if goal is unchanged between plan and current state.
    
    Returns:
        bool: True if goal is unchanged or only clarified
    """
    if not original_goal:
        # Can't verify if no original goal
        return True
    
    if not handoff_content:
        # No handoff means early in feature, assume unchanged
        return True
    
    # Look for goal changes mentioned in handoff
    change_indicators = [
        r'goal\s+changed',
        r'scope\s+changed',
        r'pivot',
        r'different\s+outcome',
        r'requirements\s+changed'
    ]
    
    for pattern in change_indicators:
        if re.search(pattern, handoff_content, re.IGNORECASE):
            return False
    
    # No explicit change mentioned - assume unchanged
    return True


def check_dependencies_met(handoff_content):
    """
    Check if dependencies are still met (no blockers discovered).
    
    Returns:
        str: "yes" | "workaround" | "no"
    """
    if not handoff_content:
        # No handoff - assume dependencies met
        return "yes"
    
    # Look for blocker mentions
    blocker_patterns = [
        r'\*\*Blockers?:\*\*\s*None',
        r'No blockers',
        r'🚫.*block',
        r'❌.*block',
    ]
    
    # Check for explicit "no blockers"
    for pattern in blocker_patterns:
        if re.search(pattern, handoff_content, re.IGNORECASE):
            if 'None' in pattern or 'No block' in pattern:
                return "yes"
            else:
                # Found blocker indicators
                return "no"
    
    # Look for workaround mentions
    if re.search(r'workaround|temporary\s+solution', handoff_content, re.IGNORECASE):
        return "workaround"
    
    # No explicit blockers mentioned - assume met
    return "yes"


def check_approach_sound(original_approach, handoff_content):
    """
    Check if approach is unchanged or only refined.
    
    Returns:
        str: "same" | "minor" | "major"
    """
    if not original_approach:
        # Can't verify if no original approach
        return "same"
    
    if not handoff_content:
        # No handoff - assume unchanged
        return "same"
    
    # Look for major approach changes
    major_change_indicators = [
        r'complete\s+redesign',
        r'changed\s+architecture',
        r'switching\s+to',
        r'abandoned.*approach',
        r'pivoting\s+to',
    ]
    
    for pattern in major_change_indicators:
        if re.search(pattern, handoff_content, re.IGNORECASE):
            return "major"
    
    # Look for minor refinements
    minor_change_indicators = [
        r'refined\s+approach',
        r'adjusted',
        r'tweaked',
        r'optimization',
        r'simplified',
    ]
    
    for pattern in minor_change_indicators:
        if re.search(pattern, handoff_content, re.IGNORECASE):
            return "minor"
    
    # No changes mentioned - assume same
    return "same"


def validate_plan(feature_name):
    """
    Run the 3 boolean validation checks.
    
    Returns:
        dict: JSON structure with validation results
    """
    project_root = find_project_root()
    feature_dir = project_root / 'backlog' / feature_name
    
    if not feature_dir.exists():
        return {
            "feature_name": feature_name,
            "category": "invalid",
            "error": f"Feature directory not found: {feature_dir}",
            "checks": {},
            "issues": ["Feature not found"],
            "recommendation": "Check feature name and try again"
        }
    
    # Load plan
    plan_path = feature_dir / 'plan.md'
    readme_path = feature_dir / 'README.md'
    plan_content = None
    
    if plan_path.exists():
        plan_content = plan_path.read_text(encoding='utf-8')
    elif readme_path.exists():
        plan_content = readme_path.read_text(encoding='utf-8')
    
    # Load handoff
    handoff_path = feature_dir / 'HANDOFF.md'
    handoff_content = None
    if handoff_path.exists():
        handoff_content = handoff_path.read_text(encoding='utf-8')
    
    # Extract key information from plan
    original_goal = extract_goal(plan_content) if plan_content else None
    original_approach = extract_approach(plan_content) if plan_content else None
    
    # Run the 3 boolean checks
    goal_unchanged = check_goal_unchanged(original_goal, handoff_content)
    dependencies = check_dependencies_met(handoff_content)
    approach = check_approach_sound(original_approach, handoff_content)
    
    checks = {
        "goal_unchanged": goal_unchanged,
        "dependencies_met": dependencies == "yes",
        "approach_sound": approach in ["same", "minor"]
    }
    
    # Determine category based on checks
    issues = []
    
    if not checks["goal_unchanged"]:
        issues.append("Goal has changed from original plan")
    
    if dependencies == "no":
        issues.append("Critical dependencies/blockers discovered")
    elif dependencies == "workaround":
        issues.append("Working around dependency issues (temporary)")
    
    if approach == "major":
        issues.append("Major approach change (complete redesign)")
    
    # Categorize: valid / update / invalid
    if len(issues) == 0:
        category = "valid"
        recommendation = "Continue with current plan"
    elif len(issues) == 1 and approach == "minor":
        category = "update"
        recommendation = "Update plan.md to reflect minor refinements, then continue"
    elif len(issues) >= 2:
        category = "invalid"
        recommendation = "Run /replan-feature or /check-drift for detailed analysis"
    else:
        category = "update"
        recommendation = "Document changes in plan.md, consider if replanning needed"
    
    return {
        "feature_name": feature_name,
        "category": category,
        "checks": checks,
        "issues": issues,
        "recommendation": recommendation
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: plan_validator.py <feature-name>",
            "example": "python3 plan_validator.py session-based-auth"
        }, indent=2), file=sys.stderr)
        sys.exit(1)
    
    feature_name = sys.argv[1]
    result = validate_plan(feature_name)
    
    # Pretty print JSON
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    if 'error' in result or result['category'] == 'invalid':
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

