# Cross-Repo Consolidation

> **Part of**: [Project Organization Templates](../../templates/projects/README.md)

**Status**: On Hold
**Started**: 2024-09
**Last Updated**: 2025-11
**Owner**: Personal project

---

## Quick Start

**New to this project?** Read in this order:
1. **integration-strategy.md** - Current approach (OfferHub implementation pattern)
2. **reorganization-plan.md** - Original comprehensive plan (team-based approach)
3. **cross-references.md** - Pre-migration reference tracking
4. **manual-rename-required.md** - Manual steps documentation

**Resuming work?** Start with integration-strategy.md for current state.

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
- [ ] Phase 3: Apply pattern to DOIS (future)
- [ ] Phase 4: Apply pattern to SCS (future)

**Completion**: ~40% (OfferHub done, DOIS/SCS pending)

---

## Notes

- This is an active project that has been started and stopped multiple times
- OfferHub implementation validated the pattern successfully
- Documents moved here from root to clean up repository for team sharing
- Pattern is ready to replicate for DOIS/SCS when needed

---

**Last Updated**: 2025-11 by Adams

