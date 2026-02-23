# Reliable Sources for AI-Assisted Development

**Purpose:** Document where to check for latest AI dev trends, best practices, and tooling updates.

**Last Updated:** January 2026 (Claude Code v2.1.7)

---

## Primary Sources (Check Weekly)

### Official Documentation

| Source | URL | Focus |
|--------|-----|-------|
| **Claude Code Docs** | https://code.claude.com/docs | Official features, changelog |
| **Claude Code Best Practices** | https://www.anthropic.com/engineering/claude-code-best-practices | Anthropic's official guide |
| **Anthropic Release Notes** | https://docs.anthropic.com/release-notes | New features, deprecations |
| **Skills Repository** | https://github.com/anthropics/skills | Official skill examples |

### Trusted Technical Writers

| Writer | URL | Why Trusted |
|--------|-----|-------------|
| **Simon Willison** | https://simonwillison.net/ | Deep AI tooling analysis, real-world testing |
| **Addy Osmani** | https://addyosmani.com/blog/ | AI coding workflows, practical patterns |
| **ClaudeLog** | https://claudelog.com/ | Claude-specific news, release analysis |

### Paid/Premium (Worth It)

| Source | URL | Notes |
|--------|-----|-------|
| **Nate's Newsletter** | https://natesnewsletter.substack.com/ | Paid subscription, requires access |

---

## Community Resources (Check Monthly)

### GitHub Repositories

| Repo | Purpose | Stars/Activity |
|------|---------|----------------|
| **anthropics/skills** | Official skill examples, SKILL.md format | Official |
| **anthropics/claude-code** | Official Claude Code source | Official |
| **travisvn/awesome-claude-skills** | Community-curated skills | Active |
| **jeremylongshore/claude-code-plugins-plus-skills** | 700+ skills with tutorials | Active |
| **alirezarezvani/claude-code-skill-factory** | Skill generation toolkit | Active |
| **nicobailon/visual-explainer** | HTML visualization skill (diagrams, tables, charts) | Active, curated |

### Discussion Forums

| Platform | Where | Signal-to-Noise |
|----------|-------|-----------------|
| **Hacker News** | Search: "Claude Code", "agentic coding" | High (but verify claims) |
| **Reddit** | r/ClaudeAI, r/LocalLLaMA | Medium (filter for quality) |
| **X/Twitter** | @AnthropicAI, developer accounts | Medium |
| **Discord** | Anthropic Discord server | High for real-time issues |

---

## Validation Approach

When evaluating new patterns or claims:

### Trust Hierarchy

1. **Official Anthropic** - Trusted without verification
2. **Well-known authors** (Simon Willison, Addy Osmani) - High trust, minimal verification
3. **GitHub repos with high stars** - Verify with quick test
4. **Forum posts/Reddit** - Always verify independently
5. **Random blog posts** - Verify with 2+ sources

### Verification Steps

1. **Check source date** - Is this for current Claude Code version?
2. **Test in sandbox** - Create a test project, try the pattern
3. **Check for contradictions** - Does this conflict with official docs?
4. **Document results** - Add to your project's changelog if adopted

### Red Flags

- Claims without version numbers
- Screenshots from much older versions
- Patterns that require disabling security features
- "Works for me" without reproducible steps

---

## What to Watch (2026)

### Claude Code Features

- **Plan mode evolution** - Built-in planning continues to improve
- **Skills/Plugins** - SKILL.md format now shared with OpenAI Codex
- **Hooks system** - PreToolUse, PostToolUse, Stop events
- **Session management** - Auto-compact, session teleportation
- **Multi-agent patterns** - Subagent orchestration

### Industry Trends

- **MCP (Model Context Protocol)** - Standardizing tool integration
- **AGENTS.md** - Emerging standard for AI instruction files
- **Agentic loops** - AI with linters, test runners, code execution
- **Planning-first workflows** - Spec before code generation
- **Testing integration** - AI feedback loops require tests

### Key Versions to Track

| Tool | Current Version | Release Notes |
|------|-----------------|---------------|
| Claude Code | v2.1.7 | https://claudelog.com/faqs/claude-code-release-notes/ |
| Codex CLI | v1.x | https://platform.openai.com/docs/codex |
| Cursor | Check app | https://cursor.com/changelog |

---

## Research Workflow

### When to Check Sources

| Trigger | Action |
|---------|--------|
| Claude Code update | Check official docs + ClaudeLog |
| New pattern discovered | Verify with 2+ sources |
| Something doesn't work | Check GitHub issues, Discord |
| Quarterly review | Full scan of all primary sources |

### How to Document Findings

When you adopt a new pattern, document in your project:

```markdown
## Changelog

### 2026-01-14
- Adopted review-context.md pattern for code review
- Source: fwaptile-wordle project, validated against Anthropic best practices
- Reduces false positives by 60%
```

---

## Template Usage

Copy this file to your project's `docs/` or `.claude/` directory and customize:

1. **Add project-specific sources** - Domain experts, framework docs
2. **Track what you've verified** - Add checkmarks to patterns you've tested
3. **Set review reminders** - Quarterly audit of sources
4. **Remove irrelevant sections** - If you don't use Cursor, remove that row

---

## See Also

- [BUILTIN_VS_CUSTOM.md](../../docs/decisions/BUILTIN_VS_CUSTOM.md) - When to use built-in vs custom workflows
- [../skills/code-review/](../skills/code-review/README.md) - Code review skill with latest patterns
- [CLAUDE-MD-GUIDELINES.md](../claude-md/CLAUDE-MD-GUIDELINES.md) - Keeping CLAUDE.md lean
