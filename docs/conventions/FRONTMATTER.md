---
id: frontmatter-conventions
title: "Document Frontmatter Conventions"
description: "Schema for YAML frontmatter in ai-dev-templates documentation"
audience: intermediate
tags: ["conventions", "metadata", "frontmatter"]
---

# Document Frontmatter Conventions

[← Back to Main README](../../README.md)

YAML frontmatter schema for documentation in this repository. Compatible with the [docs-site publishing pipeline](../../../utilities/docs-site/PUBLISHING.md).

---

## Schema

```yaml
---
id: my-doc-id                    # Required. Unique, kebab-case (a-z0-9- only)
title: "Document Title"          # Required. Matches the H1 heading
description: "One-line summary"  # Recommended. Used in search and listings
audience: intermediate           # Recommended. beginner | intermediate | power-user
tags: ["tag1", "tag2"]           # Optional. List of strings for discoverability
---
```

### Field Reference

| Field | Required | Type | Values |
|-------|----------|------|--------|
| `id` | Yes | string | Unique kebab-case (`^[a-z0-9-]+$`) |
| `title` | Yes | string | Should match the document's H1 heading |
| `description` | Recommended | string | One-line summary for search and listings |
| `audience` | Recommended | string | `beginner`, `intermediate`, `power-user` |
| `tags` | Optional | list[string] | Lowercase, hyphenated terms |

### Audience Values

| Value | Means |
|-------|-------|
| `beginner` | New to Claude Code or AI-assisted development |
| `intermediate` | Comfortable with basics, learning advanced patterns |
| `power-user` | Optimizing workflows, managing context at scale |

---

## Publishing to docs-site

When a document is ready to publish to `docs.epcvip.vip`, add a `publish_to` block:

```yaml
---
id: my-doc-id
title: "Document Title"
description: "One-line summary"
audience: intermediate
tags: ["tag1", "tag2"]
publish_to:
  docs_site: true
  category: ai-templates
  status: published         # published | draft | internal | in-review
  sensitivity: public       # public | internal | restricted
  parent: ai-templates-root # Folder ID in docs-site hierarchy
  order: 1                  # Position within parent folder
---
```

Files without `publish_to.docs_site: true` are silently skipped by the build pipeline.

See [docs-site PUBLISHING.md](../../../utilities/docs-site/PUBLISHING.md) for the full publishing guide.

---

## What We Don't Store

| Field | Why Not |
|-------|---------|
| `last-updated` | Git tracks modification dates more accurately. Manual dates go stale. |
| `author` | Git blame handles this. AI-assisted authorship is fuzzy. |
| `related_docs` | See Also sections in content already handle cross-linking. |
| `scope` / `type` | Directory structure communicates this (`docs/reference/`, `templates/`, `docs/setup-guides/`). |

**Exception**: `last-verified` (for external source freshness) stays inline where relevant — it records when a human confirmed external links/claims are still accurate, which git can't infer.

---

## Rollout

Frontmatter is added **gradually** — when you create or modify a file, add frontmatter. Don't bulk-update existing files.
