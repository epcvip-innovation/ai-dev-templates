---
id: contributing
title: "Contributing: Content Organization & Documentation Conventions"
description: "How content is organized, linked, maintained, and discovered in this repository"
audience: beginner
---

# Contributing: Content Organization & Documentation Conventions

[← Back to Main README](./README.md)

How content is organized, linked, and maintained in this repository — for both human contributors and AI assistants working with the codebase.

---

## Content Architecture

This repo uses a **hub-and-spoke model**:

- **Hub**: `CLAUDE.md` at repo root (~185 lines). Auto-loaded every Claude Code session. Contains routing — tells you *where* to find things, not the things themselves.
- **Spokes**: Everything in `docs/` and `templates/`. Loaded on demand when relevant.

The hub stays lightweight so every session starts with clear context. Detailed knowledge lives in spokes and gets read when needed. For the full three-tier context model, see [Consistency at Scale](./docs/reference/CONSISTENCY-AT-SCALE.md).

---

## Where New Content Goes

| Content Type | Directory | Examples |
|-------------|-----------|----------|
| Getting started, onboarding | `docs/getting-started/` | Quickstart, setup guide, first feature |
| Reference, advanced patterns | `docs/reference/` | Context engineering, advanced workflows |
| Architecture decisions | `docs/decisions/` | Why WSL, built-in vs custom |
| Conventions, standards | `docs/conventions/` | Frontmatter schema |
| Setup guides | `docs/setup-guides/` | Claude Code setup, Cursor + WSL |
| MCP documentation | `docs/mcp/` | Playwright MCP, context efficiency |
| Reusable templates | `templates/<category>/` | Skills, hooks, CLAUDE.md structures |
| Quality standards | `templates/standards/` | Anti-slop, frontend standards |

**Not sure?** Ask: "Is this something someone reads once to learn, or repeatedly to reference?" Learning goes in `docs/getting-started/`. Reference goes in `docs/reference/`. Patterns to copy go in `templates/`.

---

## Cross-Linking Conventions

Every document should be reachable from at least one other document. Orphaned docs are invisible to both humans and AI.

### Three link types (all used throughout this repo)

1. **Back-link at top**: Navigation breadcrumb to parent
   ```markdown
   [← Back to Main README](../../README.md)
   ```

2. **Inline contextual**: First mention of a related concept includes a cross-reference
   ```markdown
   For the full three-tier context model, see [Consistency at Scale](./docs/reference/CONSISTENCY-AT-SCALE.md).
   ```

3. **"See Also" at bottom**: Categorized by purpose
   ```markdown
   ## See Also
   - [Context Engineering](./CONTEXT-ENGINEERING.md) — Five pillars, token optimization
   - [Advanced Workflows](./ADVANCED-WORKFLOWS.md) — Planning, agents, predictability
   ```

### Discoverability

There are no metadata tags or databases to maintain. Discoverability comes from:

- **Cross-references in the document graph** — every doc links to related docs
- **README.md tables** — the main entry point for human navigation
- **CLAUDE.md routing** — the main entry point for AI navigation
- **`grep`** — to find all references to any file: `grep -r "FILENAME" docs/ templates/ README.md`

### When renaming or moving files

Search for the old name across the repo and update all references:

```bash
grep -r "OLD-FILENAME" docs/ templates/ README.md CLAUDE.md CONTRIBUTING.md
```

---

## Document Standards

### Frontmatter

All documentation files should include YAML frontmatter. See [docs/conventions/FRONTMATTER.md](./docs/conventions/FRONTMATTER.md) for the schema.

Required: `id`, `title`. Recommended: `description`, `audience`.

### Style

- **Evidence-based, not theoretical**: Patterns should come from real usage, not speculation
- **Guidelines, not hard rules**: Frame limits with context ("effectiveness tends to degrade around X") rather than absolute numbers — unless there's a technical reason for a hard limit
- **Verify before documenting**: Claude Code features change between versions. Check against [official docs](https://code.claude.com/docs) and [release notes](https://github.com/anthropics/claude-code/releases) before writing about specific features

### Quality checks

Run the doc-review plugin before committing documentation changes:

```
/doc-review:review-docs
```

This checks link validity, content quality, cross-file consistency, and AI-generated writing patterns.

---

## What to Avoid

- **Duplicating content across docs** — reference the source instead of copying. One source of truth per concept.
- **CLAUDE.md bloat** — keep it under ~200 lines. Route to spoke docs for detail. See [CLAUDE-MD-GUIDELINES](./templates/claude-md/CLAUDE-MD-GUIDELINES.md).
- **Documenting linter-enforceable rules in CLAUDE.md** — if a hook or CI check catches it, Claude will see the failure and self-correct. Reserve CLAUDE.md for things only Claude can know. See [Consistency at Scale](./docs/reference/CONSISTENCY-AT-SCALE.md).
- **Orphaned documents** — every doc should have at least one incoming link from another doc.
- **Fabricating features** — always verify Claude Code features against official sources before documenting them.

---

## Maintenance

### Quarterly audit

Run these checks every 3 months (or after major additions):

- [ ] CLAUDE.md under ~200 lines
- [ ] All cross-reference links resolve (run doc-review link checker)
- [ ] README.md tables reflect current content
- [ ] No duplicate content across docs
- [ ] Spoke docs still accurate and current

For the full audit process, see [CLAUDE-MD-GUIDELINES.md](./templates/claude-md/CLAUDE-MD-GUIDELINES.md) (quarterly audit section) and [Consistency at Scale](./docs/reference/CONSISTENCY-AT-SCALE.md) (Section 9).

---

## See Also

- [Consistency at Scale](./docs/reference/CONSISTENCY-AT-SCALE.md) — Three-tier context, routing tables, the consistency stack
- [CLAUDE-MD-GUIDELINES](./templates/claude-md/CLAUDE-MD-GUIDELINES.md) — Keeping CLAUDE.md lightweight, decision tree, quarterly audits
- [Frontmatter Conventions](./docs/conventions/FRONTMATTER.md) — YAML frontmatter schema
- [Context Engineering](./docs/reference/CONTEXT-ENGINEERING.md) — Five pillars, token optimization, isolation strategies

---
