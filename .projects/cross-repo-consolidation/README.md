# Cross-Repo Consolidation

> **Part of**: [Project Organization Templates](../../templates/projects/README.md)

**Status**: COMPLETE
**Started**: 2024-09
**Completed**: 2025-12-08
**Owner**: Personal project

---

## Migration Complete

**December 2025**: Full reorganization completed using revised plan.

**Final Structure**:
```
~/epcvip/              # Production codebases (unchanged)
~/repos-epcvip/        # EPCVIP innovation repos (NEW)
├── tools/             # data-platform-assistant, experimentation-toolkit
├── docs/              # epcvip-docs, epcvip-docs-obsidian, innovation-data-docs, offer-hub
├── projects/          # lead-value-segmentation, dynamic-rla, analysis projects
├── utilities/         # ping-tree-compare, dois-test-capacity-planner
└── templates/         # ai-dev-templates, claude-dev-template
~/repos/               # Personal projects only
```

**Key Changes**:
- `~/repos-epcvip/` at home level (avoids CLAUDE.md inheritance pollution)
- Category-based organization (tools, docs, projects, utilities, templates)
- CLAUDE.md navigation hierarchy (master hub → category → project)
- Git subtree replaced with manual team sharing

**See**: `~/repos-epcvip/MIGRATION_COMPLETE.md` for full details.

---

## Historical Documents (Archived)

These documents capture the original planning process:
1. **integration-strategy.md** - OfferHub implementation pattern (superseded)
2. **reorganization-plan.md** - Original comprehensive plan (superseded by Claude plan)
3. **cross-references.md** - Pre-migration reference tracking
4. **manual-rename-required.md** - Manual steps documentation

---

## Document Guide

| Document | Purpose | Audience | Update Frequency |
|----------|---------|----------|------------------|
| **README.md** (this file) | Navigation & project status | Everyone | As needed |
| **integration-strategy.md** | Current implementation pattern (OfferHub) | Engineers + PMs | When pattern evolves |
| **reorganization-plan.md** | Original comprehensive reorganization plan | Reference | Historical |
| **cross-references.md** | Pre-migration reference tracking | Migration team | During migration |
| **manual-rename-required.md** | Manual migration steps | Migration team | During migration |

---

## For Claude (AI Context)

### Current Focus
**Working On**: Consolidating workflow between dev-setup, docs, and datalake-assistant repos
**Current Session Goal**: Organize planning documents and prepare for team sharing

### Scope Boundaries

**ONLY work on**:
- Cross-repo integration patterns
- Documentation organization
- Workflow consolidation between repos

**DO NOT** (explicitly out of scope):
- [ ] Don't implement full reorganization yet (still exploring patterns)
- [ ] Don't modify other repos without explicit request
- [ ] Don't create new consolidation docs without reviewing existing ones

### Next Checkpoint

**Stop after**: Documents organized and root cleaned
**Validate with**: Check that all references are updated
**Then**: Ask user before proceeding

---

## Project Overview

This project explores patterns for consolidating workflows and documentation across three repositories:
- **dev-setup**: Template library and development environment setup
- **docs**: Documentation repositories (epcvip-docs, epcvip-docs-obsidian, innovation-data-docs)
- **datalake-assistant**: Data platform query and analysis tooling

**Problem**: 30-40% content duplication, broken cross-links, unclear ownership, maintenance burden across repos.

**Approach**: Started with OfferHub as "guinea pig" to test project-specific monorepo pattern before applying to DOIS/SCS.

---

## Quick Links

- **Current Strategy**: [integration-strategy.md](./integration-strategy.md) - OfferHub implementation pattern
- **Original Plan**: [reorganization-plan.md](./reorganization-plan.md) - Comprehensive team-based approach
- **System Architecture**: [system-architecture.md](./system-architecture.md) - Multi-repo documentation structure
- **Reference Tracking**: [cross-references.md](./cross-references.md) - Pre-migration scan results
- **Manual Steps**: [manual-rename-required.md](./manual-rename-required.md) - Migration instructions

---

## Key Decisions

- **Project-specific monorepos** (not one giant monorepo) - Better for independent teams and 30-40% duplication
- **Workflow-based structure** (1-5 pattern) - Better for self-contained projects than team-based folders
- **Manual extraction** (not automated) - Simple, visible, intentional sync to company docs
- **GitHub permalinks** - Stable cross-repo references instead of relative paths

See integration-strategy.md for full decision rationale.

---

## Progress Summary

- [x] Phase 1: Problem identification and approach exploration (completed 2024-09)
- [x] Phase 2: OfferHub implementation (completed 2025-11) - Pattern proven
- [x] Phase 3: Full reorganization (completed 2025-12-08) - All repos migrated to ~/repos-epcvip/
- [x] Phase 4: CLAUDE.md hierarchy (completed 2025-12-08) - Navigation hub created
- [x] Phase 5: Git subtree removal (completed 2025-12-08) - Simplified to manual sync

**Completion**: 100% - Migration complete

---

## Notes

- Project COMPLETE as of December 2025
- Original reorganization-plan.md superseded by Claude-assisted plan (see ~/.claude/plans/)
- Full migration documented in ~/repos-epcvip/MIGRATION_COMPLETE.md
- Historical documents preserved for reference

---

**Last Updated**: 2025-12-08 by Adams (Migration Complete)

