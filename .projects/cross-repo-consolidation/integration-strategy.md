# Cross-Repo Integration Strategy - OfferHub Implementation (Nov 2025)

## Executive Summary

**What we did**: Created docs-offer-hub as a self-contained monorepo with workflow-based organization (1-5 structure), instead of implementing the full multi-repo team-aligned reorganization from [reorganization-plan.md](./reorganization-plan.md).

**Why it's different**: Started with OfferHub as a "guinea pig" to test the pattern before applying to DOIS/SCS.

**Key insight**: Project-specific monorepos work better than one giant monorepo when 30-40% content duplication exists and teams work independently.

---

## The Problem We Were Solving

### Initial Pain Points (From Conversation)

**User quote**: "I also have this folder \\wsl.localhost\Ubuntu\home\adams\repos\docs\epcvip-docs-obsidian\Projects\Offer Hub... I feel like the project specific docs in my epcvip-docs-obsidian one needs to be better combined with the ab testing repo probably?"

**Specific issues identified**:
1. **30-40% duplication** across 3 repos:
   - `epcvip-docs` - Company-wide reference docs
   - `epcvip-docs-obsidian/Projects/Offer Hub` - Project planning docs
   - `ping-tree-ab-analysis/framework/guides/offerhub` - Testing framework docs
   - `ping-tree-ab-analysis/tests/offerhub` - Test results

2. **Broken cross-links** - Relative paths break when files move between repos

3. **Maintenance burden** - Same content updated in multiple places, gets out of sync

4. **Unclear ownership** - Which repo is "source of truth"?

5. **Different audiences** - Some docs for company onboarding, others for active development

---

## Decision Journey: What We Considered

### Option 1: Full Multi-Repo Reorganization (Original Plan)

**From [reorganization-plan.md](./reorganization-plan.md)**:
- Rename `ping-tree-ab-analysis` → `experimentation-framework`
- Organize Projects by team (dois/Olga, scs/Bruno, offer-hub/George)
- Use experiments/ subfolders with frontmatter tags
- Cross-repo CLAUDE.md navigation

**Why we didn't do this**:
- ✅ Good for team alignment
- ✅ Good for Notion sync
- ❌ **Too ambitious** - 20+ hours, 9 checkpoints, affects all teams
- ❌ **Risky** - Changes everything at once
- ❌ **Unclear ROI** - Needed to prove value first

---

### Option 2: Monorepo (Everything in One Repo)

**User consideration**: "Is there a scenario where this all lives in a single repo? Or a repo with sub repos?"

**Why we didn't do this**:
- ❌ **Too coupled** - DOIS, SCS, OfferHub have different cadences
- ❌ **Team friction** - Olga/Bruno/George all committing to same repo
- ❌ **Overwhelming** - Combining 3 testing frameworks + company docs = chaos

---

### Option 3: Git Submodules/Subtrees

**Explored**: Parent repo with linked sub-repos

**Why we didn't do this**:
- ❌ **Complex maintenance** - Git subtree commands are error-prone
- ❌ **Confusing history** - Commits from multiple repos interleaved
- ✅ **Already partially implemented** - docs-offer-hub WAS a subtree of epcvip-docs-obsidian
- 💡 **Key insight**: Subtree worked to create the repo, but NOT for ongoing sync

---

### Option 4: Project-Specific Monorepos (What We Chose) ✅

**Pattern**:
- One repo per project (docs-offer-hub, future docs-dois, docs-scs)
- Workflow-based organization (1-5 structure)
- Company-docs extraction mechanism for cross-repo sync
- GitHub permalinks for cross-references

**Why this won**:
- ✅ **Start small** - Prove pattern with OfferHub, then replicate
- ✅ **Clear ownership** - OfferHub team owns docs-offer-hub
- ✅ **Self-contained** - Everything in one place, grep works
- ✅ **Flexible extraction** - Can pull out company docs when needed
- ✅ **Low risk** - Doesn't affect DOIS or SCS workflows

---

## What We Implemented: The OfferHub Pattern

### 1. Repository Structure (1-5 Workflow)

**Chose workflow-based over content-type or audience-based**

```
docs-offer-hub/
├── 1-foundation/          # WHEN: Learning the system (onboarding)
├── 2-strategy/            # WHEN: Planning what to build
├── 3-methodology/         # WHEN: Designing tests
├── 4-implementation/      # WHEN: Running analysis
├── 5-tests/              # WHEN: Reviewing past results
├── reference/            # Supporting materials
└── company-docs/         # Extraction for epcvip-docs
```

**Why 1-5 structure**:

**User quote**: "Let's use offer hub as our guinea pig since it's relatively simple"

**Rationale**:
- **Progressive disclosure** - Numbers indicate reading order
- **Task-oriented** - "I need to..." → go to relevant number
- **Scales** - Same pattern for DOIS, SCS (consistency)
- **Future-proof** - Not tied to specific tools/teams

**What we rejected**:
- ❌ By content type (docs/, code/, data/) - Doesn't match mental model
- ❌ By audience (pm/, data-scientist/, engineer/) - Creates silos
- ❌ Flat structure - Doesn't scale beyond 10-15 files

---

### 2. Cross-Repo Integration: Extraction Pattern

**Problem**: Company docs (epcvip-docs) need OfferHub overview, but full project docs are too detailed

**Solution**: company-docs/ extraction directory

**How it works**:
1. **Source of truth**: docs-offer-hub (project repo)
2. **Extraction**: Manual copy from `1-foundation/` → `company-docs/`
3. **Sync to epcvip-docs**: `cp company-docs/system-overview.md ../epcvip-docs/docs/Lead-Monetization/`
4. **Documentation**: company-docs/README.md explains what/when to extract

**Key decision**: Manual sync (not automated)

**Why**:
- ✅ **Simple** - Copy command, not git hooks/CI/CD
- ✅ **Intentional** - Think before syncing (avoid noise)
- ✅ **Visible** - Clear commit history in both repos
- ⏳ **Future**: Can automate later with GitHub Actions if needed

**What to extract** (documented in company-docs/README.md):
- ✅ Core system architecture (1-foundation/)
- ✅ Stable, general-purpose docs
- ❌ Strategic planning (2-strategy/) - project-specific
- ❌ Test results (5-tests/) - historical record
- ❌ Methodology (3-methodology/) - specialized knowledge

---

### 3. Cross-References: GitHub Permalinks

**Problem**: Relative paths break when files move

**Example**:
```markdown
❌ BAD: [Guide](../../../framework/guides/offerhub/overview.md)
✅ GOOD: [Guide](https://github.com/ahhhdum/docs-offer-hub/blob/main/3-methodology/positional-bias/offerhub/overview.md)
```

**Why permalinks**:
- ✅ **Stable** - URL doesn't break if local structure changes
- ✅ **Clickable** - Works in GitHub UI, VS Code, any markdown viewer
- ✅ **Explicit** - Clear which repo/branch/file
- ⏳ **Future**: Can use commit SHAs for truly permanent links

**Trade-off accepted**: URLs are longer, but stability worth it

---

### 4. Content Migration Strategy

**What we migrated to docs-offer-hub**:

| Content Type | Source | Destination | Why |
|--------------|--------|-------------|-----|
| **System specs** | epcvip-docs-obsidian | 1-foundation/, 2-strategy/ | Already existed as subtree |
| **Testing methodology** | ping-tree-ab-analysis/framework/guides/offerhub/ | 3-methodology/positional-bias/ | OfferHub-specific |
| **Analysis scripts** | ping-tree-ab-analysis/framework/scripts/offerhub/ | 4-implementation/analysis-scripts/ | OfferHub-specific |
| **Data templates** | ping-tree-ab-analysis/framework/templates/offerhub/ | 4-implementation/data-templates/ | OfferHub-specific |
| **Test results** | ping-tree-ab-analysis/tests/offerhub/ | 5-tests/completed/ | OfferHub-specific |

**What we deleted**:
- ✅ Obsidian OfferHub folder (replaced with redirect README)
- ✅ ping-tree-ab-analysis OfferHub framework (kept archived test for reference)

**What we kept in original repos**:
- ✅ epcvip-docs company reference (synced from company-docs/)
- ✅ ping-tree-ab-analysis archived test (links updated to GitHub URLs)

**Key principle**: "Migrate if project-specific, extract if company-wide"

---

## Key Decisions & Rationale

### Decision 1: Don't Rename ping-tree-ab-analysis

**Original plan**: Rename to `experimentation-framework`

**What we did**: Keep the name

**Why**:
- ✅ **Separate concerns** - DOIS testing ≠ OfferHub testing (different methods)
- ✅ **Avoid breaking changes** - Other repos/scripts may reference it
- ✅ **Defer decision** - Can still rename later if needed

**User quote**: "don't rename the repo. continue with other tasks"

**Implication**: Each project gets its own repo (docs-offer-hub, future docs-dois)

---

### Decision 2: Use 1-5 Workflow Structure (Not Team-Based)

**Original plan**: Organize by team (dois/Olga, scs/Bruno, offer-hub/George)

**What we did**: Organize by workflow stage (1-foundation → 5-tests)

**Why**:
- ✅ **Task-oriented** - "I need to design a test" → go to 3-methodology
- ✅ **Reusable pattern** - Works for any project type
- ✅ **Clear progression** - Numbers show natural order
- ❌ **Team alignment** - Less important for OfferHub (one team owns it)

**When team-based is better**: Original [reorganization-plan.md](./reorganization-plan.md) is better for:
- Multi-team shared repos (Projects/ folder in Obsidian)
- Experiments folder synced to Notion
- PM-specific views (Olga's experiments, Bruno's experiments)

**When workflow-based is better**: Our approach is better for:
- Self-contained project repos
- Documentation consumed linearly
- Onboarding new team members

---

### Decision 3: Manual Extraction (Not Automated)

**Considered**: Git hooks, GitHub Actions, symlinks

**What we did**: Manual `cp` command documented in README

**Why**:
- ✅ **Simple** - No CI/CD setup needed
- ✅ **Intentional** - Review changes before syncing
- ✅ **Visible** - Clear commits in both repos
- ⏳ **Upgradeable** - Can automate later if sync frequency increases

**When to automate**: If syncing >1x per week, consider GitHub Actions

---

### Decision 4: Keep Archived Test Data in Source Repos

**What we did**:
- Migrated framework to docs-offer-hub
- Kept `ping-tree-ab-analysis/tests/offerhub/` with updated links

**Why**:
- ✅ **Historical reference** - Old repo still has test data
- ✅ **No duplication** - Data file in S3, not git
- ✅ **Clear migration path** - Links point to new docs
- ✅ **Safe fallback** - If docs-offer-hub has issues, archived version exists

---

## The Methodology We Settled On

### Pattern: Project-Specific Monorepos with Extraction

**For each major project** (OfferHub, DOIS, SCS):

1. **Create dedicated repo** - `docs-{project-name}`
2. **Use 1-5 structure** - foundation → strategy → methodology → implementation → tests
3. **Extract to company docs** - Foundation docs → epcvip-docs
4. **Update source repos** - Cross-references point to new location
5. **Document extraction** - company-docs/README.md explains what/when

---

### Repository Roles

| Repository | Purpose | Audience | Update Frequency |
|------------|---------|----------|------------------|
| **docs-offer-hub** | OfferHub project docs (source of truth) | OfferHub team | Weekly/sprint |
| **docs-dois** (future) | DOIS testing framework | DOIS team | Weekly/sprint |
| **docs-scs** (future) | SCS testing framework | SCS team | Monthly |
| **epcvip-docs** | Company-wide onboarding | All teams | Quarterly (extracted) |
| **epcvip-docs-obsidian** | Active project planning | PM/Data Science | Daily |
| **ping-tree-ab-analysis** | DOIS statistical framework | Data Science | As needed |

---

### Cross-Repo Reference Strategy

**Stable references** (use GitHub permalinks):
```markdown
[OfferHub Overview](https://github.com/ahhhdum/docs-offer-hub/blob/main/1-foundation/system-overview.md)
```

**Internal references** (use relative paths):
```markdown
[Testing Methodology](../3-methodology/positional-bias/)
```

**Extracted references** (document in company-docs/):
```markdown
Source: docs-offer-hub/1-foundation/system-overview.md
Destination: epcvip-docs/docs/Lead-Monetization/Decline Path/offerhub-system-overview.md
```

---

## Why This Approach Works

### 1. Scales Gradually

- ✅ Start with one project (OfferHub) - 4 commits, 1 week
- ✅ Learn lessons, refine pattern
- ✅ Apply to DOIS next (similar complexity)
- ✅ Eventually cover all projects

**Alternative (rejected)**: Big bang reorganization (20 hours, 9 checkpoints, all teams)

---

### 2. Single Source of Truth

**Before**:
- epcvip-docs-obsidian: Planning docs (outdated)
- ping-tree-ab-analysis: Framework docs (incomplete)
- epcvip-docs: Company docs (scattered)

**After**:
- docs-offer-hub: **Source of truth** (everything in one place)
- epcvip-docs: Extracted summaries (synced from docs-offer-hub)
- ping-tree-ab-analysis: Links to docs-offer-hub

**User quote**: "I feel like the project specific docs... needs to be better combined"

**Solution**: Combine in docs-offer-hub, extract to epcvip-docs

---

### 3. Grep Works

**Key benefit of monorepo**:
```bash
cd docs-offer-hub
grep "position bias" .  # Finds everything
```

**Before** (split across repos):
```bash
grep "position bias" ~/repos/  # Finds 30+ files across 5 repos
```

**User insight**: "Grep works: `grep 'position' .`" was a PRO in the decision matrix

---

### 4. Clear Ownership

| Repository | Owner | Commit Frequency |
|------------|-------|------------------|
| docs-offer-hub | OfferHub team | High |
| docs-dois | DOIS team | High |
| docs-scs | SCS team | Medium |
| epcvip-docs | All teams | Low (extracted) |

**Avoids**: Merge conflicts, unclear who reviews PRs, outdated docs

---

### 5. Future-Proof

**Can evolve to**:
- Automated extraction (GitHub Actions on main branch merge)
- Notion sync (frontmatter in test docs → Notion database)
- Search API (query across all docs-* repos)
- CI/CD validation (broken links, missing images, style checks)

**Doesn't lock us in to**:
- Specific tool (Obsidian, Notion, GitHub)
- Specific team structure (Olga/Bruno/George)
- Specific product (EPCVIP)

---

## Implementation Checklist

**Phase 1: OfferHub (COMPLETED ✅)**
- [x] Clone docs-offer-hub
- [x] Create 1-5 directory structure
- [x] Migrate content from 3 source repos
- [x] Setup company-docs extraction
- [x] Update cross-references in source repos
- [x] Delete duplicated content
- [x] Document methodology (this file)

**Phase 2: DOIS (FUTURE)**
- [ ] Create docs-dois repo
- [ ] Apply same 1-5 structure
- [ ] Migrate ping-tree-ab-analysis framework/guides/dois → docs-dois/3-methodology
- [ ] Setup company-docs extraction for ping tree overview
- [ ] Update CLAUDE.md to point to docs-dois

**Phase 3: SCS (FUTURE)**
- [ ] Create docs-scs repo when SCS testing framework exists
- [ ] Apply same pattern

---

## Lessons Learned

### What Worked ✅

1. **Start small** - OfferHub as guinea pig (user's suggestion)
2. **Use existing subtree** - docs-offer-hub already existed, just needed restructuring
3. **Document as we go** - CLAUDE.md, README.md, company-docs/README.md
4. **GitHub permalinks** - Stable cross-repo references
5. **Manual sync** - Simple, visible, intentional

### What We'd Do Differently 🔄

1. **Plan extraction first** - We figured out company-docs pattern mid-migration
2. **Version control extraction** - Track what's extracted in a manifest file
3. **Automate link checking** - Prevent broken references earlier

### What We Avoided ⛔

1. **Over-engineering** - Didn't build CI/CD, Notion sync, etc. upfront
2. **Big bang migration** - Didn't touch DOIS/SCS yet
3. **Renaming everything** - Kept ping-tree-ab-analysis name
4. **Git subtree ongoing** - Used it to create repo, not for sync

---

## When to Use This Pattern

### Good fit ✅

- **Self-contained projects** - Clear boundaries (OfferHub, DOIS, SCS)
- **Single team ownership** - One PM/team maintains the repo
- **Active development** - Frequent updates, experiments
- **Need company extraction** - Foundation docs useful for onboarding

### Poor fit ❌

- **Cross-cutting concerns** - Shared infrastructure (use original team-based plan)
- **Infrequent updates** - Monthly or less (overhead not worth it)
- **Tiny projects** - <10 docs (just use a folder)
- **Highly coupled** - Components can't be separated

---

## Decision Framework for Future Projects

**When creating docs for a new project, ask:**

1. **Is it project-specific or cross-cutting?**
   - Project-specific (OfferHub, DOIS) → Create `docs-{project}` repo
   - Cross-cutting (VIP20, shared infrastructure) → Use Projects/_shared/

2. **Does it need company extraction?**
   - Yes (system architecture) → Setup company-docs/
   - No (tactical experiments) → Skip extraction

3. **How many teams work on it?**
   - Single team → Workflow-based structure (1-5)
   - Multiple teams → Consider team-based folders (dois/, scs/)

4. **Update frequency?**
   - High (weekly+) → Dedicated repo
   - Low (monthly) → Folder in existing repo

---

## References

- **Original Plan**: [reorganization-plan.md](./reorganization-plan.md) - Team-based multi-repo approach
- **Implemented Example**: [docs-offer-hub](https://github.com/ahhhdum/docs-offer-hub) - Workflow-based monorepo
- **Extraction Pattern**: [company-docs/README.md](https://github.com/ahhhdum/docs-offer-hub/blob/main/company-docs/README.md)

---

## Summary: The Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ Project-Specific Monorepo Pattern                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Create docs-{project} repo                             │
│  2. Use 1-5 workflow structure                             │
│  3. Migrate project-specific content                       │
│  4. Setup company-docs extraction                          │
│  5. Update source repos with GitHub permalinks             │
│  6. Delete duplicates                                       │
│  7. Document in CLAUDE.md + README.md                      │
│                                                             │
│  Benefits:                                                  │
│  ✅ Single source of truth                                  │
│  ✅ Grep works                                              │
│  ✅ Clear ownership                                         │
│  ✅ Scales gradually                                        │
│  ✅ Future-proof                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Last Updated**: November 12, 2025
**Status**: OfferHub implemented, pattern proven
**Next**: Apply to DOIS when ready
