# Cross-References Scan Results - Pre-Migration

Date: 2025-11-05
Purpose: Document all cross-references before repository renaming

## Summary

- **ping-tree-ab-analysis references**: 19 lines across 13 files
- **epcvip-datalake-assistant references**: 14 lines across 9 files
- **Git remotes**: Could not check (terminal issue), assume no remotes

## Files to Update After Renaming

### In ping-tree-ab-analysis (→ experimentation-framework)

1. **CLAUDE.md** (2 references)
   - Line 228: cd /home/adams/repos/ping-tree-ab-analysis
   - Line 274: cd /home/adams/repos/ping-tree-ab-analysis

2. **framework/templates/offerhub/positional-bias/README.md** (1 reference)
   - Line 107: cd /home/adams/repos/ping-tree-ab-analysis

3. **framework/scripts/offerhub/README.md** (1 reference)
   - Line 119: cd /home/adams/repos/ping-tree-ab-analysis

4. **tests/ping-tree/2025_10_network_priority_leap_theory/README.md** (1 reference)
   - Line 320: cd /home/adams/repos/ping-tree-ab-analysis

5. **tests/ping-tree/2025_10_network_priority_leap_theory/scripts/network_analysis.py** (1 reference)
   - Line 337: file_path = '/home/adams/repos/ping-tree-ab-analysis/tests/2025_10_network_priority_leap_theory/data/...'

6. **tests/ping-tree/2025_10_network_priority_leap_theory/data/DATA_QUALITY_NOTES.md** (1 reference)
   - Line 306: Analysis framework: `/home/adams/repos/ping-tree-ab-analysis/framework/`

7. **tests/ping-tree/2025_10_network_priority_leap_theory/scripts/comprehensive_analysis_v3_row_per_conversion.py** (1 reference)
   - Line 917: base_dir = '/home/adams/repos/ping-tree-ab-analysis/tests/2025_10_network_priority_leap_theory'

8. **framework/templates/multi-conversion/README.md** (1 reference)
   - Line 42: cd /home/adams/repos/ping-tree-ab-analysis

9. **tests/ping-tree/2025_10_network_priority_leap_theory/scripts/archive/v2_array_based/comprehensive_analysis_v2_array_based.py** (1 reference)
   - Line 738: base_dir = '/home/adams/repos/ping-tree-ab-analysis/tests/2025_10_network_priority_leap_theory'

10. **framework/templates/aggregate/README.md** (1 reference)
    - Line 41: cd /home/adams/repos/ping-tree-ab-analysis

11. **tests/ping-tree/2025_10_network_priority_leap_theory/results/comprehensive_analysis_output.txt** (1 reference)
    - Line 7: Loading data from /home/adams/repos/ping-tree-ab-analysis/tests/2025_10_network_priority_leap_theory/data/...

12. **SESSION_SUMMARY_2025_10_27.md** (1 reference)
    - Line 295: cd /home/adams/repos/ping-tree-ab-analysis

13. **tests/ping-tree/2025_10_truepath/NEXT_STEPS_2025_10_28.md** (2 references)
    - Line 21: cd /home/adams/repos/ping-tree-ab-analysis
    - Line 353: cd /home/adams/repos/ping-tree-ab-analysis

14. **tests/ping-tree/2025_10_truepath/reports/questions_answered.md** (1 reference)
    - Line 407: cd /home/adams/repos/ping-tree-ab-analysis

15. **tests/ping-tree/2025_10_truepath/reports/analyst_deep_dive.md** (1 reference)
    - Line 527: cd /home/adams/repos/ping-tree-ab-analysis

16. **tests/ping-tree/2025_10_truepath/reports/stakeholder_summary.md** (1 reference)
    - Line 138: **Full analysis:** See `/home/adams/repos/ping-tree-ab-analysis/output/`

17. **tests/ping-tree/2025_10_truepath/reports/testing_landscape.md** (1 reference)
    - Line 326: Related analyses in `/home/adams/repos/ping-tree-ab-analysis/output/`:

### In epcvip-datalake-assistant (→ data-platform-assistant)

1. **CLAUDE.md** (5 references)
   - Line 226: Tool repo (here): `/home/adams/repos/epcvip-datalake-assistant/`
   - Line 235: /home/adams/repos/epcvip-datalake-assistant/
   - Line 285: Always work from datalake-assistant repo: `/home/adams/repos/epcvip-datalake-assistant/`
   - Line 310: cd /home/adams/repos/epcvip-datalake-assistant/
   - Line 337: TOOL_PROJECTS="/home/adams/repos/epcvip-datalake-assistant/.projects"

2. **investigations/partition-filtering-2025-11-03/compare_partition_patterns.py** (2 references)
   - Line 14: EFFICIENT_PATH = Path('/home/adams/repos/epcvip-datalake-assistant/queries/tests/efficient_pattern_results.csv')
   - Line 15: STANDARD_PATH = Path('/home/adams/repos/epcvip-datalake-assistant/queries/tests/standard_pattern_results.csv')

3. **ENVIRONMENT_SETUP.md** (1 reference)
   - Line 8: /home/adams/repos/epcvip-datalake-assistant/venv/

4. **SCHEMA_CATALOG_GUIDE.md** (1 reference)
   - Line 17: cd /home/adams/repos/epcvip-datalake-assistant

### In Projects/ping-tree-processors (epcvip-docs-obsidian)

1. **TASKS.md** (1 reference)
   - Line 369: Analysis Scripts: [.projects/ping-tree-processors/analysis/](../../../../epcvip-datalake-assistant/.projects/ping-tree-processors/analysis/)

2. **data/campaign-metrics/README.md** (2 references)
   - Line 28: cd /home/adams/repos/epcvip-datalake-assistant
   - Line 353: Datalake Assistant: `/home/adams/repos/epcvip-datalake-assistant/CLAUDE.md`

3. **data/campaign-metrics/docs/data-requirements.md** (1 reference)
   - Line 747: Analysis: [threshold_collision_analysis_2025-11-03.md](../../epcvip-datalake-assistant/.projects/ping-tree-processors/analysis/threshold_collision_analysis_2025-11-03.md)

4. **data/campaign-metrics/archive/investigation_docs/CURRENT_STATUS.md** (1 reference)
   - Line 331: cd /home/adams/repos/epcvip-datalake-assistant

5. **data/campaign-metrics/archive/phase1/phase1_2025-11-01_analysis.md** (1 reference)
   - Line 176: Analysis Script: `/home/adams/repos/epcvip-datalake-assistant/.projects/ping-tree-processors/analysis/analyze_phase1_results.py`

## Git Remotes Status

Could not check git remotes due to terminal issues. Will assume:
- Both repos are local only (no remotes to update)
- If remotes exist, they will be checked manually during Step 1

## Action Plan

### Step 1: Update ping-tree-ab-analysis → experimentation-framework
- Use find/replace: `/home/adams/repos/ping-tree-ab-analysis` → `/home/adams/repos/experimentation-framework`
- Update 17 files listed above

### Step 2: Update epcvip-datalake-assistant → data-platform-assistant
- Use find/replace: `/home/adams/repos/epcvip-datalake-assistant` → `/home/adams/repos/data-platform-assistant`
- Update 4 files in datalake-assistant repo
- Update 5 files in Projects/ping-tree-processors

## Notes

- No references found in workspace settings (assuming Cursor will handle folder rename gracefully)
- All references are path-based (no import statements to worry about)
- Most references are in documentation (markdown files)
- A few Python scripts have hardcoded paths that need updating

