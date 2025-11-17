# AI-Assisted Experimentation System - Reorganization Plan (REVISED)

## Executive Summary

Transform three disconnected repositories into a cohesive AI-assisted experimentation management system aligned with team structure (SCS/Bruno, DOIS/Olga, Offer Hub/George). 

**THE PROBLEM WE'RE SOLVING**:
- **Disconnected workflows**: Manual handoffs between hypothesis → data extraction → analysis → decision
- **Lost context**: Experiments scattered across repos with no clear connections
- **No team alignment**: Flat folder structure doesn't reflect who owns what (Bruno/SCS, Olga/DOIS, George/Offer Hub)
- **Manual tracking**: Can't query experiments by status, PM, or KPI without manually searching
- **AI can't help**: Claude Code can't understand relationships between Projects docs, queries, and analysis results
- **Inconsistent naming**: Repo names too specific (ping-tree) or product-specific (epcvip)

**THE SOLUTION**:
- **Nested experiments structure**: Features contain experiments/ folders (mirrors Notion board)
- **Frontmatter tags**: Structured metadata enables querying and future Notion sync
- **Team-aligned domains**: dois/Olga, scs/Bruno, offer-hub/George
- **Cross-repo navigation**: CLAUDE.md files link all three repos
- **Generic names**: Reusable beyond current products
- **AI-friendly**: Claude Code can read structure, understand context, automate workflows

**SCOPE**: Repository renaming and folder reorganization ONLY. Slash commands/hooks in future phases.

**KEY CORRECTIONS APPLIED**:
1. TruePath → network-priority feature (separate from ping-tree-processors)
2. HOHA → offer-hub (NOT ping-tree-processors)
3. type_in_trees → separate DOIS feature
4. ad_chain_break_detection → _infrastructure (not a testable feature)
5. Scan for cross-references BEFORE renaming
6. Checkpoints for review after each major step

## Complete Before/After Structure (All 3 Repos)

### Repo 1: Projects Folder (Documentation & Domain Knowledge)
**Location**: `\\wsl.localhost\Ubuntu\home\adams\repos\docs\epcvip-docs-obsidian\Projects`

**BEFORE** (Flat, mixed):
```
Projects/
├── ping-tree-processors/          # DOIS feature
├── Marketplace/                    # DOIS feature
├── Fraud/                          # DOIS feature
├── RTB/                            # DOIS feature
├── HOHA/                           # Offer Hub feature (misplaced)
├── Ad-Chain Break Detection/       # SCS infrastructure
├── Offer Hub/                      # Offer Hub features
├── dois-unified-processor/         # DOIS infrastructure
├── dois-experiments/               # DOIS infrastructure
├── experimentation-process/        # Mixed infrastructure
├── vip-20-rework/                  # Cross-cutting
└── _shared/                        # Cross-cutting
```

**AFTER** (Domain-organized, features with experiments/):
```
Projects/
├── CLAUDE.md                              # NEW: Master navigation hub
├── dois/                                  # Olga's domain
│   ├── README.md                          # NEW: Domain overview
│   ├── ping-tree-processors/              # FEATURE
│   │   ├── README.md
│   │   ├── ping-tree-processor-overview.md
│   │   ├── experiments/                   # NEW: Contains tests
│   │   │   ├── 2025_10_parallel_processing/
│   │   │   └── 2025_11_soft_timeout/
│   │   ├── Background/
│   │   └── data/
│   ├── network-priority/                  # NEW FEATURE (was scattered)
│   │   └── experiments/
│   │       ├── 2025_10_truepath/          # MOVED from ping-tree-processors
│   │       └── 2025_10_leaptheory/
│   ├── type-in-trees/                     # NEW FEATURE (was in ping-tree-processors)
│   │   └── experiments/
│   ├── marketplace/                       # MOVED from Marketplace/
│   │   └── experiments/
│   ├── fraud/                             # MOVED from Fraud/
│   │   └── experiments/
│   ├── rtb/                               # MOVED from RTB/
│   │   └── experiments/
│   └── _infrastructure/                   # NEW: Non-testable projects
│       ├── experimentation-process/
│       ├── dois-unified-processor/
│       └── dois-experiments/
├── scs/                                   # Bruno's domain
│   ├── README.md                          # NEW: Domain overview
│   ├── funnel-optimization/               # NEW FEATURE
│   │   └── experiments/
│   └── _infrastructure/                   # NEW: Non-testable projects
│       ├── ad-chain-break-detection/      # MOVED + RENAMED
│       └── experimentation-process/
├── offer-hub/                             # George's domain
│   ├── README.md                          # NEW: Domain overview
│   ├── hoha/                              # MOVED from HOHA/ (top level)
│   │   └── experiments/
│   ├── bidding-algorithm/                 # MOVED from Offer Hub/
│   │   └── experiments/
│   ├── position-bias/                     # MOVED from Offer Hub/
│   │   └── experiments/
│   └── offerwall-architecture/            # MOVED from Offer Hub/
│       └── experiments/
└── _shared/                               # UNCHANGED: Cross-cutting
    ├── DOIS/
    └── VIP20/
```

**WHY THIS HELPS**:
- ✅ Clear ownership (Bruno sees scs/, Olga sees dois/, George sees offer-hub/)
- ✅ Features vs infrastructure distinction (experiments/ folder = testable)
- ✅ Mirrors Notion board (each experiment folder = Notion card)
- ✅ Claude Code can auto-navigate to correct experiment based on domain/feature

---

### Repo 2: Data Platform Assistant (Query & Extraction)
**Location**: `\\wsl.localhost\Ubuntu\home\adams\repos\epcvip-datalake-assistant` → `data-platform-assistant`

**BEFORE**:
```
epcvip-datalake-assistant/
├── CLAUDE.md                              # Generic, no cross-repo refs
├── core/                                  # Query validation, execution
├── knowledge/                             # Rules, patterns
├── queries/                               # Templates
└── .claude/commands/                      # 4 commands (query-focused)
```

**AFTER**:
```
data-platform-assistant/                   # RENAMED: Generic, reusable
├── CLAUDE.md                              # UPDATED: Cross-repo navigation
├── core/                                  # UNCHANGED
├── knowledge/                             # UNCHANGED
├── queries/                               # UNCHANGED
└── .claude/commands/                      # UNCHANGED (future: add experiment commands)
```

**CHANGES IN THIS PHASE**:
- ✅ Rename repository folder
- ✅ Update CLAUDE.md with Projects structure references
- ✅ Update internal path references (9 files)

**FUTURE PHASES** (not in this plan):
- Add /extract-experiment-data command
- Add /validate-experiment-data command
- Add hooks for data quality checks

**WHY THIS HELPS**:
- ✅ Generic name (not tied to EPCVIP product)
- ✅ CLAUDE.md links to Projects experiments
- ✅ Future: Can auto-detect which domain/feature to query based on context

---

### Repo 3: Experimentation Framework (Statistical Analysis)
**Location**: `\\wsl.localhost\Ubuntu\home\adams\repos\ping-tree-ab-analysis` → `experimentation-framework`

**BEFORE** (DOIS-centric):
```
ping-tree-ab-analysis/
├── CLAUDE.md                              # Ping tree focused
├── framework/
│   ├── scripts/                           # DOIS scripts at root
│   │   ├── 01_aggregate_analysis.py
│   │   ├── 02_partner_attribution.py
│   │   └── offerhub/                      # Only subfolder
│   ├── guides/                            # DOIS guides at root
│   │   ├── attribution-and-cannibalization.md
│   │   └── offerhub/                      # Only subfolder
│   └── templates/                         # DOIS templates at root
│       ├── aggregate/
│       ├── multi-conversion/
│       └── offerhub/                      # Only subfolder
└── tests/                                 # Flat structure
    ├── ping-tree/                         # DOIS tests
    │   ├── 2025_10_truepath/
    │   └── 2025_10_network_priority_leap_theory/
    └── offerhub/                          # Offer Hub tests
        └── 2025_11_position_bias_wallet_shark/
```

**AFTER** (Multi-domain):
```
experimentation-framework/                 # RENAMED: Generic
├── CLAUDE.md                              # UPDATED: Cross-repo, multi-domain
├── framework/
│   ├── scripts/                           # REORGANIZED by domain
│   │   ├── dois/                          # DOIS-specific
│   │   │   ├── 01_aggregate_analysis.py
│   │   │   ├── 02_partner_attribution.py
│   │   │   ├── 03_attribution_validation.py
│   │   │   ├── 04_price_tier_cascade.py
│   │   │   └── 05_campaign_attribution.py
│   │   ├── scs/                           # SCS-specific (new scaffold)
│   │   │   └── README.md
│   │   └── offer-hub/                     # RENAMED from offerhub/
│   │       ├── positional_bias_analysis.py
│   │       └── analyze_aggregated_position_data.py
│   ├── guides/                            # REORGANIZED by domain
│   │   ├── dois/                          # DOIS guides
│   │   │   ├── attribution-and-cannibalization.md
│   │   │   ├── baseline-selection-and-test-setup.md
│   │   │   ├── data-characteristics.md
│   │   │   ├── multiple-comparisons-problem.md
│   │   │   ├── sequential-vs-parallel-testing.md
│   │   │   ├── test-extension-and-false-positive-control.md
│   │   │   └── weight-allocation-and-revenue-optimization.md
│   │   ├── scs/                           # SCS guides (new scaffold)
│   │   │   └── README.md
│   │   └── offer-hub/                     # RENAMED from offerhub/
│   │       ├── offerhub-overview.md
│   │       └── positional-bias-analysis.md
│   └── templates/                         # REORGANIZED by domain
│       ├── dois/                          # DOIS templates
│       │   ├── aggregate/
│       │   └── multi-conversion/
│       ├── scs/                           # SCS templates (new scaffold)
│       │   └── README.md
│       └── offer-hub/                     # RENAMED from offerhub/
│           └── positional-bias/
└── tests/                                 # REORGANIZED by domain
    ├── dois/                              # DOIS test archive
    │   ├── 2025_10_truepath/              # MOVED to dois/
    │   └── 2025_10_network_priority_leap_theory/
    ├── scs/                               # SCS test archive (new, empty)
    │   └── README.md
    └── offer-hub/                         # RENAMED from offerhub/
        └── 2025_11_position_bias_wallet_shark/
```

**CHANGES IN THIS PHASE**:
- ✅ Rename repository folder
- ✅ Update CLAUDE.md with Projects structure references
- ✅ Reorganize framework/ by domain (dois/scs/offer-hub)
- ✅ Reorganize tests/ by domain
- ✅ Create SCS scaffolds (empty but ready)
- ✅ Update internal path references (17 files)

**WHY THIS HELPS**:
- ✅ Generic name (works for all experiment types, not just ping tree)
- ✅ Domain-organized (easy to find DOIS vs SCS vs Offer Hub methods)
- ✅ Scalable (SCS experiments can use scs/ framework when built)
- ✅ Claude Code can auto-select correct framework based on domain/feature
- ✅ Team-aligned (Bruno's SCS tests will use scs/ framework, Olga's use dois/, George's use offer-hub/)

## Migration Steps with Checkpoints

### CHECKPOINT 0: Pre-Migration Scan (30 min)

**Purpose**: Find all cross-references before breaking them

**Actions**:
1. Scan for repo name references:
   - `grep -r "ping-tree-ab-analysis" ~/repos/`
   - `grep -r "epcvip-datalake-assistant" ~/repos/`

2. Document findings in [cross-references.md](./cross-references.md):
   - File paths
   - Line numbers
   - What needs updating

3. Check git remotes:
   ```bash
   cd ~/repos/ping-tree-ab-analysis && git remote -v
   cd ~/repos/epcvip-datalake-assistant && git remote -v
   ```

4. Check Cursor workspace references:
   - Workspace settings file
   - Launch configurations
   - Task definitions

**Deliverable**: [cross-references.md](./cross-references.md) with complete list of files to update

**STOP FOR REVIEW**: Share findings before proceeding

---

### Step 1: Repository Renaming (1 hour)

**Actions**:
1. Rename folders:
   ```powershell
   cd \\wsl.localhost\Ubuntu\home\adams\repos
   mv ping-tree-ab-analysis experimentation-framework
   mv epcvip-datalake-assistant data-platform-assistant
   ```

2. Update git remotes (if they exist):
   ```bash
   cd experimentation-framework
   git remote set-url origin <new-url>
   ```

3. Update Cursor workspace:
   - Edit workspace file
   - Update folder paths
   - Save and reload

4. Update all files from [cross-references.md](./cross-references.md):
   - Find/replace old → new names
   - Test affected functionality

**Deliverable**: Both repos renamed, remotes updated, workspace functional

**CHECKPOINT 1**: Test that both repos still work
- [ ] Can open repos in Cursor
- [ ] Python environments still work
- [ ] Git commands work
- [ ] No broken imports

**STOP FOR REVIEW**: Verify renaming complete before moving forward

---

### Step 2: Create Domain Structure in Projects (30 min)

**Actions**:
```bash
cd Projects/
mkdir -p dois/_infrastructure
mkdir -p scs/_infrastructure
mkdir -p offer-hub
```

Create domain README.md files:

**dois/README.md**:
```markdown
# DOIS Experiments & Features

PM: Olga

## Features (Testable)
- ping-tree-processors
- network-priority (TruePath, LeapTheory tests)
- type-in-trees
- marketplace
- fraud
- rtb

## Infrastructure (Not Testable)
- experimentation-process
- dois-unified-processor
- dois-experiments
```

**scs/README.md**:
```markdown
# SCS Experiments & Features

PM: Bruno

## Features (Testable)
- funnel-optimization

## Infrastructure (Not Testable)
- ad-chain-break-detection
- experimentation-process
```

**offer-hub/README.md**:
```markdown
# Offer Hub Experiments & Features

Lead: George

## Features (Testable)
- hoha (Hybrid Offer Hub Algorithm)
- bidding-algorithm
- position-bias
- offerwall-architecture
```

**Deliverable**: Domain folders + README stubs

**CHECKPOINT 2**: Review structure before moving files
- [ ] Domain folders created
- [ ] README stubs accurate
- [ ] Team assignments correct (Olga/Bruno/George)

**STOP FOR REVIEW**: Confirm structure matches expectations

---

### Step 3: Move Projects to Domains (2-3 hours)

**DOIS Moves** (use `git mv`):
```bash
cd Projects/
git mv ping-tree-processors dois/
git mv Marketplace dois/marketplace
git mv Fraud dois/fraud
git mv RTB dois/rtb
git mv HOHA offer-hub/hoha  # CORRECTED: Goes to offer-hub
git mv dois-unified-processor dois/_infrastructure/
git mv dois-experiments dois/_infrastructure/
```

**Create new DOIS features**:
```bash
mkdir -p dois/network-priority  # NEW: For TruePath, LeapTheory
mkdir -p dois/type-in-trees     # NEW: Separate feature
```

**SCS Moves**:
```bash
git mv "Ad-Chain Break Detection" scs/_infrastructure/ad-chain-break-detection
```

**Offer Hub Moves**:
```bash
# Offer Hub/ → offer-hub/ (flatten)
mv "Offer Hub"/* offer-hub/
rmdir "Offer Hub"
```

**Update internal references**:
- Search for broken [[wikilinks]] in Obsidian
- Update path references in markdown files
- Fix any relative links

**Deliverable**: All projects in correct domains, git history preserved

**CHECKPOINT 3**: Verify moves completed correctly
- [ ] All projects in correct domains
- [ ] Git history preserved (check `git log --follow`)
- [ ] Obsidian links work
- [ ] No broken references

**STOP FOR REVIEW**: Check that nothing broken

---

### Step 4: Create experiments/ Subfolders (1-2 hours)

**For each FEATURE** (not _infrastructure):

**DOIS features**:
```bash
cd Projects/dois/

# ping-tree-processors (processor optimization tests)
mkdir -p ping-tree-processors/experiments/2025_10_parallel_processing
mkdir -p ping-tree-processors/experiments/2025_11_soft_timeout

# network-priority (TruePath, LeapTheory, etc.)
mkdir -p network-priority/experiments/2025_10_truepath
mkdir -p network-priority/experiments/2025_10_leaptheory

# type-in-trees
mkdir -p type-in-trees/experiments/2025_11_type_in_optimization

# marketplace
mkdir -p marketplace/experiments/2025_11_lead_prediction

# fraud (empty for now)
mkdir -p fraud/experiments/

# rtb (empty for now)
mkdir -p rtb/experiments/
```

**SCS features**:
```bash
cd Projects/scs/
mkdir -p funnel-optimization/experiments/
```

**Offer Hub features**:
```bash
cd Projects/offer-hub/

# HOHA - CORRECTED: Lives in offer-hub
mkdir -p hoha/experiments/2025_11_hoha_sorting

# bidding-algorithm
mkdir -p bidding-algorithm/experiments/

# position-bias
mkdir -p position-bias/experiments/2025_11_wallet_shark_position

# offerwall-architecture
mkdir -p offerwall-architecture/experiments/
```

**Deliverable**: experiments/ folders created for all features

**CHECKPOINT 4**: Verify experiments structure
- [ ] All features have experiments/ folders
- [ ] Infrastructure projects have NO experiments/ folders
- [ ] Experiment folders named correctly (YYYY_MM_name)

**STOP FOR REVIEW**: Confirm structure before adding content

---

### Step 5: Add Frontmatter to Experiments (2-3 hours)

**Standard Template**:
```yaml
---
type: experiment
experiment_id: 2025_10_truepath
feature: network-priority
domain: dois
pm: olga
status: testing  # upcoming | testing | scaling | analysis | completed
primary_kpi: EPL
secondary_kpis: [decision_latency, conversion_rate]
notion_link: https://notion.so/...
started: 2025-10-01
expected_end: 2025-11-25
---
```

**For each experiment**:
1. Create or update HYPOTHESIS.md
2. Add frontmatter from Notion board
3. Map Notion columns:
   - Upcoming → status: upcoming
   - Testing/In Progress → status: testing
   - Scaling/Optimizing → status: scaling
   - Analysis/Follow Up → status: analysis
   - Completed → status: completed

**Example for TruePath**:
```yaml
---
type: experiment
experiment_id: 2025_10_truepath
feature: network-priority
domain: dois
pm: olga
status: analysis  # Currently in Analysis/Follow Up column
primary_kpi: EPL
secondary_kpis: [win_rate, collision_rate]
notion_link: https://notion.so/...
started: 2025-10-01
expected_end: 2025-11-25
---

# TruePath Test - Network Priority Optimization

## Hypothesis
Moving TruePath to static section (top of ping tree) will increase EPL...
```

**Deliverable**: All experiments have frontmatter matching Notion

**CHECKPOINT 5**: Verify frontmatter consistency
- [ ] All experiments have frontmatter
- [ ] Status maps to Notion columns
- [ ] PMs assigned correctly (olga/bruno/george)
- [ ] experiment_id matches folder name

**STOP FOR REVIEW**: Check frontmatter before reorganizing framework

---

### Step 6: Reorganize Experimentation Framework (2-3 hours)

**Create domain structure**:
```bash
cd experimentation-framework/framework/

# Scripts
mkdir -p scripts/{dois,scs,offer-hub}
mv scripts/01_aggregate_analysis.py scripts/dois/
mv scripts/02_partner_attribution.py scripts/dois/
mv scripts/03_attribution_validation.py scripts/dois/
mv scripts/04_price_tier_cascade.py scripts/dois/
mv scripts/05_campaign_attribution.py scripts/dois/
mv scripts/offerhub/ scripts/offer-hub/
echo "# SCS Scripts - Coming Soon" > scripts/scs/README.md

# Guides
mkdir -p guides/{dois,scs,offer-hub}
mv guides/*.md guides/dois/
mv guides/offerhub/ guides/offer-hub/
echo "# SCS Guides - Coming Soon" > guides/scs/README.md

# Templates
mkdir -p templates/{dois,scs,offer-hub}
mv templates/aggregate/ templates/dois/
mv templates/multi-conversion/ templates/dois/
mv templates/offerhub/ templates/offer-hub/
echo "# SCS Templates - Coming Soon" > templates/scs/README.md

# Tests
mkdir -p tests/{dois,scs,offer-hub}
mv tests/ping-tree/ tests/dois/
mv tests/offerhub/ tests/offer-hub/
echo "# SCS Tests - Coming Soon" > tests/scs/README.md
```

**Update imports** in Python scripts (if needed)

**Deliverable**: Framework reorganized by domain

**CHECKPOINT 6**: Verify framework restructure
- [ ] Scripts organized by domain
- [ ] Guides organized by domain
- [ ] Templates organized by domain
- [ ] Tests organized by domain
- [ ] Python scripts still run

**STOP FOR REVIEW**: Test that analysis scripts still work

---

### Step 7: Create Master CLAUDE.md Files (1-2 hours)

**Projects/CLAUDE.md** (Master Hub):

```markdown
# Experimentation Projects - Master Hub

## Purpose
This is the FIRST stop for all experimentation work. All hypothesis development, domain knowledge, and results documentation starts here.

## Repository Ecosystem

### 1. Projects (HERE)
- **Path**: \\wsl.localhost\Ubuntu\home\adams\repos\docs\epcvip-docs-obsidian\Projects
- **Purpose**: Hypothesis, domain knowledge, queries, results
- **Structure**: dois/ | scs/ | offer-hub/ | _shared/

### 2. Data Platform Assistant
- **Path**: \\wsl.localhost\Ubuntu\home\adams\repos\data-platform-assistant
- **Purpose**: Query generation, validation, data extraction
- **Commands**: /validate-query, /build-query, /validate-and-execute-query

### 3. Experimentation Framework
- **Path**: \\wsl.localhost\Ubuntu\home\adams\repos\experimentation-framework
- **Purpose**: Statistical analysis, A/B testing, decision memos
- **Structure**: framework/scripts/{dois,scs,offer-hub}/, tests/{dois,scs,offer-hub}/

## Team Organization

| Domain | PM | Features |
|--------|----|---------| 
| **DOIS** | Olga | Ping Tree Processors, Network Priority, Type-in-Trees, Marketplace, Fraud, RTB |
| **SCS** | Bruno | Funnel Optimization |
| **Offer Hub** | George | HOHA, Bidding Algorithm, Position Bias, Offerwall |

## How to Use This System

### Starting a New Experiment
1. **Define hypothesis**: Create folder in Projects/{domain}/{feature}/experiments/
2. **Add frontmatter**: Use standard template (type, experiment_id, status, pm, kpis)
3. **Extract data**: Use data-platform-assistant to query datalake
4. **Analyze**: Use experimentation-framework for statistical tests
5. **Document**: Save results back to Projects experiment folder

### Finding Existing Experiments
- Browse by domain: dois/ | scs/ | offer-hub/
- Browse by feature: ping-tree-processors/, marketplace/, etc.
- Query by tag: `grep -r "status: testing"` or `grep -r "pm: olga"`
- Check Notion board (synced via frontmatter)

## Standard Frontmatter

All experiments must include:
```yaml
---
type: experiment
experiment_id: YYYY_MM_name
feature: feature-name
domain: dois | scs | offer-hub
pm: olga | bruno | george
status: upcoming | testing | scaling | analysis | completed
primary_kpi: EPL | CTR | Fund Rate | etc.
notion_link: https://notion.so/...
started: YYYY-MM-DD
expected_end: YYYY-MM-DD
---
```

## Infrastructure vs Features

**Features** (have experiments/ subfolder):
- Testable systems (ping-tree-processors, marketplace, bidding-algorithm)
- Can run A/B tests or experiments
- Have associated hypothesis and KPIs

**Infrastructure** (_infrastructure/ prefix):
- Process documentation (experimentation-process)
- System specs (dois-unified-processor)
- No experiments (informational only)
```

**Update CLAUDE.md in each repo** with cross-references

**Deliverable**: Master navigation established

**CHECKPOINT 7**: Verify CLAUDE.md accuracy
- [ ] All paths correct
- [ ] Cross-repo references accurate
- [ ] Team organization matches reality
- [ ] Workflow instructions clear

**STOP FOR REVIEW**: Read through CLAUDE.md for accuracy

---

### Step 8: Update Cross-References (2-3 hours)

**From [cross-references.md](./cross-references.md)** (created in Checkpoint 0):
1. Update each identified file
2. Replace old paths with new paths
3. Test affected functionality

**Additional updates**:
- Feature overview docs (ping-tree-processor-overview.md)
- README files
- Script paths
- Documentation links

**Scan for missed references**:
```bash
grep -r "ping-tree-ab-analysis" ~/repos/
grep -r "epcvip-datalake-assistant" ~/repos/
# Should return no results
```

**Deliverable**: All cross-references updated

**CHECKPOINT 8**: Verify no broken references
- [ ] All files from [cross-references.md](./cross-references.md) updated
- [ ] No grep results for old names
- [ ] All markdown links work
- [ ] Scripts run without path errors

**STOP FOR REVIEW**: Final check before documentation

---

### Step 9: Create Migration Documentation (1-2 hours)

**Create MIGRATION_GUIDE.md**:
```markdown
# Migration Complete - What Changed

## Repository Names
- ping-tree-ab-analysis → experimentation-framework
- epcvip-datalake-assistant → data-platform-assistant

## Projects Structure (Key Corrections)
- TruePath → dois/network-priority/ (NOT ping-tree-processors)
- HOHA → offer-hub/hoha/ (NOT dois/ping-tree-processors)
- type_in_trees → dois/type-in-trees/ (separate feature)
- ad_chain_break_detection → scs/_infrastructure/ (infrastructure, not feature)

## How to Navigate

### Find experiments by domain:
```bash
ls Projects/dois/*/experiments/
ls Projects/scs/*/experiments/
ls Projects/offer-hub/*/experiments/
```

### Query experiments by status:
```bash
grep -r "status: testing" Projects/
```

### Query by PM:
```bash
grep -r "pm: olga" Projects/dois/
grep -r "pm: bruno" Projects/scs/
grep -r "pm: george" Projects/offer-hub/
```

## What Changed for You

### If you have bookmarks:
- Update to new repo names
- Update Projects paths (now domain-based)

### If you have scripts:
- Update repo paths
- Update import statements (framework now has dois/scs/offer-hub)

### If you reference experiments:
- Check new locations (especially TruePath, HOHA)
- Use frontmatter experiment_id for cross-references
```

**Create CHECKPOINT_RESULTS.md**:
Document results from all 9 checkpoints

**Deliverable**: Complete migration documentation

**FINAL CHECKPOINT**: Full system validation
- [ ] Both repos renamed and functional
- [ ] All projects in correct domains
- [ ] All experiments have frontmatter
- [ ] Framework reorganized by domain
- [ ] CLAUDE.md files accurate
- [ ] No broken cross-references
- [ ] Documentation complete
- [ ] Ready for team rollout

**STOP FOR FINAL REVIEW**: Complete walkthrough before declaring done

---

## Timeline

- Checkpoint 0: Pre-scan (30 min) ✅ COMPLETED
- Step 1: Rename repos + Checkpoint 1 (1.5 hours) 🔄 IN PROGRESS (BLOCKED - needs manual rename)
- Step 2: Domain structure + Checkpoint 2 (1 hour)
- Step 3: Move projects + Checkpoint 3 (3 hours)
- Step 4: Create experiments/ + Checkpoint 4 (2 hours)
- Step 5: Add frontmatter + Checkpoint 5 (3 hours)
- Step 6: Reorganize framework + Checkpoint 6 (3 hours)
- Step 7: CLAUDE.md files + Checkpoint 7 (2 hours)
- Step 8: Cross-references + Checkpoint 8 (3 hours)
- Step 9: Documentation + Final Checkpoint (2 hours)

**Total: 20 hours over 4-5 days with review pauses**

## Benefits of This Reorganization

### For Team Members (Bruno/Olga/George)
- ✅ **Clear ownership**: Each PM has their own domain folder
- ✅ **Easy navigation**: Browse experiments by feature, not scattered across repos
- ✅ **Notion alignment**: Frontmatter maps directly to Notion board columns
- ✅ **Query experiments**: `grep -r "status: testing" Projects/dois/` to find all active tests

### For AI (Claude Code)
- ✅ **Context understanding**: Can read CLAUDE.md and understand full workflow
- ✅ **Auto-navigation**: Can jump from hypothesis → query → analysis → results
- ✅ **Domain detection**: Knows which framework to use based on domain/feature
- ✅ **Future automation**: Structure enables slash commands like /analyze-experiment

### For System Quality
- ✅ **Traceability**: Every experiment has clear lineage (Projects → data-platform-assistant → experimentation-framework)
- ✅ **Reproducibility**: Frontmatter captures all experiment metadata
- ✅ **Scalability**: Adding new domains/features follows same pattern
- ✅ **Reusability**: Generic names and structure work beyond EPCVIP

### Success Metrics
**Efficiency**:
- Before: 30-60 min manual handoffs (find data, copy files, remember commands)
- After: 5-10 min with AI assistance (Claude reads context, suggests next steps)

**Context Preservation**:
- Before: Lose context between extraction → analysis (days/weeks later)
- After: CLAUDE.md maintains full context, experiments self-document

**Team Adoption**:
- Target: Bruno/Olga/George can run complete workflow in one session
- Measure: Number of experiments run end-to-end in system

## What's NOT Included (Future Phases)

### Phase 2: Automation
- Auto-generate README indices from frontmatter
- Slash commands for experiment workflows (/extract-experiment-data, /analyze-experiment)
- Hooks for data quality checks
- Integration scripts between repos

### Phase 3: Notion Sync
- Bi-directional sync between frontmatter and Notion
- Automated status updates
- KPI tracking integration

### Phase 4: Advanced Features
- Query experiments by tags via web UI
- Experiment dashboards
- Team-specific views (Bruno/Olga/George)
- Automated report generation

## Key Corrections Applied

1. ✅ TruePath → network-priority (separate from ping-tree-processors)
2. ✅ HOHA → offer-hub (not DOIS)
3. ✅ type_in_trees → separate DOIS feature
4. ✅ ad_chain_break_detection → _infrastructure
5. ✅ Pre-scan for cross-references (Checkpoint 0) - COMPLETED
6. ✅ Review checkpoints after each step
7. ✅ Update remotes and workspace
8. ✅ Scan for broken references before completing

## Files Created During Migration

- ✅ [cross-references.md](./cross-references.md) - Complete list of files to update (31 files identified)
- ✅ [manual-rename-required.md](./manual-rename-required.md) - Instructions for manual folder renaming
- ✅ [reorganization-plan.md](./reorganization-plan.md) - This file (complete plan reference)
- 🔜 `CHECKPOINT_RESULTS.md` - Results from all checkpoints
- 🔜 `MIGRATION_GUIDE.md` - Final migration summary for team

