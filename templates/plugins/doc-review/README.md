# doc-review Plugin

[← Back to Plugins](../README.md)

Multi-agent documentation review — link validation, content quality, AI writing patterns, and cross-file consistency.

---

## Quick Start

```bash
# Install via local marketplace (see ../README.md for one-time setup)
cp -r templates/plugins/doc-review ~/.claude/marketplaces/local/doc-review
# Then in Claude Code: /plugin install doc-review@local

# Or use directly from this repo without installing
/doc-review:review-docs path/to/docs/
```

---

## What It Does

The plugin runs 4 specialized agents in parallel, each focused on one aspect of documentation quality:

| Agent | Focus | Model |
|-------|-------|-------|
| **link-checker** | Broken links, missing anchors, cross-repo link issues | Haiku |
| **content-quality** | Brevity, bloat, structural issues, word counts | Sonnet |
| **ai-pattern-detector** | AI writing tells from Wikipedia's "Signs of AI writing" | Haiku |
| **cross-file-analyzer** | Duplication, conflicts, stale cross-references | Sonnet |

The `review-docs` skill orchestrates these agents and produces a consolidated report.

---

## Usage

```
/doc-review:review-docs                              # Review uncommitted .md changes
/doc-review:review-docs path/to/file.md              # Review a specific file
/doc-review:review-docs path/to/directory/            # Review all .md files in directory
/doc-review:review-docs --quick                       # Links + content only (skip AI/cross-file)
/doc-review:review-docs path/to/file.md --fix         # Review and offer to apply fixes
```

---

## Plugin Structure

```
doc-review/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── README.md                    # This file (not loaded into context)
├── skills/
│   └── review-docs/
│       └── SKILL.md             # Main skill — orchestrates agents
└── agents/
    ├── link-checker.md           # Link validation specialist
    ├── content-quality.md        # Brevity, structure, accuracy
    ├── ai-pattern-detector.md    # AI writing pattern detection
    └── cross-file-analyzer.md    # Cross-file consistency
```

---

## Related Tools

| Tool | When to Use |
|------|-------------|
| `/humanizer` | Rewrite text to remove AI patterns (this plugin detects, humanizer fixes) |
| `/local-review` | Code review (not documentation) |
| `/check-readme-standards` | Validate A/B test READMEs against format spec |

---

## Design Decisions

- **Haiku for link-checker and ai-pattern-detector**: These are pattern-matching tasks that don't need deep reasoning. Haiku is fast and cheap.
- **Sonnet for content-quality and cross-file-analyzer**: These require judgment about what's bloat vs legitimate repetition, and what's a conflict vs intentional variation.
- **Agents over monolithic skill**: The original skill version didn't self-execute — it loaded instructions and waited. Agents run autonomously in isolated context.
- **No URL fetching**: External link validation is slow, may require auth, and produces false positives. We check patterns only.
