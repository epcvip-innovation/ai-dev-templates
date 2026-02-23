# Community Skills

[← Back to Skills](../README.md)

Curated third-party skills snapshotted for immediate use. Each skill includes a local copy of the runtime files (SKILL.md, prompts, references, templates) plus a MANIFEST.yaml tracking provenance and upstream version.

**Model**: snapshot + link. Files are copied locally so they work immediately; MANIFEST.yaml links to the upstream repo for updates.

---

## Available Skills

| Skill | Category | Author | Version | Upstream |
|-------|----------|--------|---------|----------|
| [visual-explainer](./visual-explainer/) | Visualization | nicobailon | v0.1.1 | [GitHub](https://github.com/nicobailon/visual-explainer) |

---

## Tags Index

Tags for discoverability — when Claude Code searches for these terms, the relevant skill should surface.

| Tag | Skills |
|-----|--------|
| `visualization` | visual-explainer |
| `diagrams` | visual-explainer |
| `html` | visual-explainer |
| `charts` | visual-explainer |
| `mermaid` | visual-explainer |
| `tables` | visual-explainer |
| `data-tables` | visual-explainer |
| `architecture` | visual-explainer |
| `flowcharts` | visual-explainer |
| `interactive` | visual-explainer |
| `ascii-art-replacement` | visual-explainer |
| `styled-output` | visual-explainer |

---

## Quick Install

```bash
# Copy to global skills (available in all projects)
cp -r templates/skills/community/visual-explainer ~/.claude/skills/visual-explainer
```

The skill auto-triggers when you ask for diagrams, architecture overviews, diff reviews, plan reviews, or comparison tables. It also activates proactively when Claude is about to render a complex ASCII table (4+ rows or 3+ columns).

---

## Curation Criteria

Skills are included when they meet all of:

1. **Permissive license** (MIT, Apache 2.0, ISC)
2. **SKILL.md format** compatible with Claude Code's skill system
3. **Manually tested** in at least one real project
4. **Fills a gap** not covered by existing skills in this repo
5. **Active maintenance** or stable release

---

## Checking for Updates

Each skill's MANIFEST.yaml records the upstream commit SHA and version. To check for updates:

```bash
# Check if upstream has new releases
gh release list -R nicobailon/visual-explainer --limit 3

# Compare current snapshot version against latest
grep 'version:' templates/skills/community/visual-explainer/MANIFEST.yaml
```

When updating a snapshot, update the MANIFEST.yaml fields (`version`, `commit_sha`, `snapshot_date`) and copy the new runtime files.

---

**Last Updated**: 2026-02-22
