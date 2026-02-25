# What's New

Team-facing updates log. Tracks template changes and the Claude Code platform changes they reflect. Reverse chronological — entries older than 6 months are removed.

---

## February 2026 — Custom Agents, Agent Teams, Plugins, Worktree Isolation

### Template Changes

- **UPDATED**: Unified skills/commands terminology across ~20 docs (Feb 25):
  - Skills and commands are **unified** — both produce `/name`, both work identically
  - `.claude/commands/` is the **flat-file format** (legacy, still works)
  - `.claude/skills/name/SKILL.md` is the **directory format** (recommended for complex workflows)
  - Three extension mechanisms (Skills, Hooks, Plugins) — not four
  - Updated taxonomy tables, hierarchy of customization, cross-references
- **UPDATED**: Plugin & skill docs synced with official sources (Feb 24):
  - **Plugin structure**: `skills/` recommended over `commands/` (legacy), `hooks/hooks.json` JSON config, `.mcp.json`, `.lsp.json`, `settings.json`, `outputStyles/` components
  - **Manifest**: now optional (auto-discovery), new fields (`homepage`, `repository`, `license`, `keywords`, component paths), `${CLAUDE_PLUGIN_ROOT}` env var
  - **CLI/marketplace**: `--plugin-dir` testing, `claude plugin validate`/`update`, `--scope` flag, official marketplace (`claude-plugins-official`), GitHub shorthand, `extraKnownMarketplaces`/`enabledPlugins`/`strictKnownMarketplaces` team settings
  - **Skills**: `disable-model-invocation` frontmatter, `${CLAUDE_SESSION_ID}` substitution, Agent Skills open standard (agentskills.io)
- **NEW**: Plugin ecosystem (`templates/plugins/`) — README with decision tree (skill vs plugin), PLUGIN-TEMPLATE.md for scaffolding new plugins, team marketplace distribution pattern
- **NEW**: doc-review plugin (`templates/plugins/doc-review/`) — 4-agent documentation review (link validation, content quality, AI patterns, cross-file consistency) with `--quick` and `--fix` flags
- **NEW**: MCP Trust Tiers (`docs/mcp/MCP-TRUST-TIERS.md`) — Build vs adapt vs install decision framework with vetting checklist for third-party MCPs
- **NEW**: TDD skill (`templates/skills/tdd/`) — RED-GREEN-REFACTOR enforcement during development; complements `/local-review` (post-dev review) and `pr-test-analyzer` (PR-time coverage). Adapted from Superpowers by Jesse Vincent (@obra)
- **NEW**: Community skills section (`templates/skills/community/`) — curated third-party skills with MANIFEST.yaml provenance
- **NEW**: visual-explainer community skill — styled HTML visualizations (diagrams, tables, charts) by nicobailon
- **NEW**: Custom agents template (`templates/agents/README.md`) — full frontmatter reference, common patterns, memory, worktree isolation, agent teams
- **UPDATED**: Skills frontmatter — added `memory`, `background`, `isolation`, `skills`, `mcpServers` fields (SKILL-TEMPLATE.md + frontmatter-reference.md)
- **UPDATED**: Permissions README — added permission modes section (acceptEdits, dontAsk, bypassPermissions, plan), expanded sandbox documentation
- **UPDATED**: Security guide — heredoc smuggling prevention, ConfigChange hook for security auditing, sandbox skill injection note
- **UPDATED**: Config/security docs clarified managed settings delivery paths (macOS plist, Windows Registry) while preserving precedence model
- **UPDATED**: Advanced Workflows — background agents, worktree isolation, agent teams (experimental), session customization sections added
- **UPDATED**: Git Worktrees guide — autonomous workflow recipes (`--tmux` + `--append-system-prompt`), CLI flags table, branch base pitfall, zen orchestrator reference
- **UPDATED**: Template categories now 12 (agents, plugins added)
- **NEW**: This file (WHATS-NEW.md)

### Claude Code Platform Changes (v2.1.34–v2.1.49)

- **Custom agents**: `.claude/agents/` with full YAML frontmatter, `/agents` management command
- **Agent teams**: Experimental multi-session coordination (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
- **`--worktree` / `-w` flag**: Start sessions in isolated git worktrees
- **`--tmux` flag**: Run worktree sessions in detached tmux windows (requires `--worktree`); `--tmux=classic` forces traditional tmux over iTerm2 panes
- **`--append-system-prompt`**: Inject additional system prompt text at launch — worker specialization for parallel sessions
- **`--fork-session`**: Branch a conversation into a new session ID (use with `--resume` or `--continue`)
- **`isolation: "worktree"`**: Run agents in temporary worktrees with auto-cleanup
- **`background: true`**: Always-background agents; Ctrl+B to background running tasks, Ctrl+F to kill
- **`memory: user|project|local`**: Persistent agent memory across sessions (MEMORY.md auto-loaded)
- **Permission modes**: `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` for agents and sessions
- **ConfigChange hook**: Monitor/block mid-session config modifications
- **TeammateIdle / TaskCompleted hooks**: Quality gates for agent teams
- **Heredoc smuggling prevention**: Improved delimiter parsing (v2.1.38+)
- **Sandbox hardening**: `.claude/skills` write blocking, `autoAllowBashIfSandboxed` security fix
- **Sonnet 4.6**: Replaced Sonnet 4.5 with 1M context
- **Opus 4.6**: Adaptive thinking, effort controls (low/medium/high/max), 1M context beta
- **`claude auth login/status/logout`**: CLI auth management subcommands
- **50+ stability fixes**: Memory management, WSL2, Unicode handling, concurrent agents

---

## January 2026 — Initial Release

### Template Changes

- 11 template categories: skill templates (flat-file format), CLAUDE.md structures, skills, project management, standards, security, hooks, permissions, testing, CI/CD, frontend standards
- 21 flat-file skill templates
- 3-tier AI agent security (baseline → team → strict)
- Unified code review skill (5-phase pipeline)
- Skill creator skill (guided scaffolding)
- Hooks system with 15 events and 5 working examples
- Playwright E2E testing patterns
- CI/CD workflows (security review, Claude QA, risk-gated)

### Claude Code Platform Changes (v2.1.x baseline)

- Skills system with YAML frontmatter
- Hooks with command/prompt/agent handler types
- Native Tasks (TaskCreate, TaskList, TaskGet, TaskUpdate)
- MCP tool integration
- Plan mode
- Context compaction

---

**Maintained by**: Innovation team
**Last updated**: 2026-02-24
