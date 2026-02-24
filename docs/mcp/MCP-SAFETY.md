# MCP Safety & Version Management

[← Back to MCP Hub](./README.md) | [← Back to Main README](../../README.md)

## Why This Matters

The MCP specification calls MCP tools "arbitrary code execution." MCP servers
run with your user permissions, can read/write files, make network requests,
and their outputs flow directly into the LLM's context. Three risk categories:

## 1. Supply Chain Attacks

### The Problem

- `npx -y @some-mcp@latest` re-downloads on every invocation
- A compromised maintainer account can ship malicious code to trusted packages

### Real Incidents

- **postmark-mcp** (npm): Legitimate through ~15 versions, then v1.0.16
  added a BCC backdoor exfiltrating all emails to an external address
  (Source: snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails)
- **mcp-server-git** (Anthropic's own): 3 vulnerabilities found Dec 2025 —
  code execution, file deletion, context loading via prompt injection in
  repository content
  (Source: thehackernews.com/2026/01/three-flaws-in-anthropic-mcp-git-server)

### Version Pinning

| Strategy | Example | Risk |
|----------|---------|------|
| **Pin exact** (recommended) | `@playwright/mcp@0.0.64` | Lowest — requires manual updates |
| **Periodic review** | Pin, check `npm view <pkg> version` monthly | Best balance |
| **@latest** (avoid) | `@playwright/mcp@latest` | Highest — auto-updates, no audit trail |

```bash
# Check latest available version
npm view @playwright/mcp version

# Pin in your config (not @latest)
claude mcp add playwright -- npx -y @playwright/mcp@0.0.64
```

Team configs (`.mcp.json`): Always pin exact versions.

## 2. Prompt Injection via MCP

### Attack Vectors

- **Indirect injection**: Malicious instructions in content returned by MCP tools
  (e.g., a GitHub issue containing "ignore previous instructions and...")
- **Tool poisoning**: Malicious MCP server embeds instructions in tool descriptions
  or response metadata
- **Context poisoning**: Untrusted tool responses inject content that causes
  misuse of legitimate tools

### Claude Code Mitigations

- **Permission system**: Explicit approval for sensitive operations
- **Isolated context**: Web fetch uses a separate context window (MCP responses don't)
- **Command blocklist**: Risky commands blocked by default
- **Injection detection**: Forces manual approval even for allowlisted commands
  when injection patterns detected

### Your Responsibility

- Treat all MCP tool output as untrusted
- Don't blindly follow instructions in MCP responses
- Use hooks to validate MCP outputs before acting on them

Source: modelcontextprotocol.io/specification/draft/basic/security_best_practices

## 3. Write-Capable MCP Risks

Write operations through MCPs are privilege escalation surfaces:

| MCP | Write Capability | Risk |
|-----|-----------------|------|
| Supabase `execute_sql` | Arbitrary SQL including DROP TABLE | Data loss |
| Railway `set-variables` | Change production env vars | Service disruption |
| Filesystem MCP | Read/write any file you can access | Data exfiltration |
| GitHub MCP | Create issues, PRs, comments | Reputation risk |

**Principle**: Least privilege. Use read-only MCPs when write isn't needed.
Prefer MCPs with safety models (Railway blocks delete/billing, Supabase
tracks migrations separately from raw SQL).

## 4. Permission Model

### Claude Code

- Per-tool approval on first use
- "Allow and remember" for repeat operations
- `managed-mcp.json` for team-enforced MCP configs (exclusive control)
- `allowedMcpServers` / `deniedMcpServers` in settings for policy control
- Project-scoped MCPs in `.mcp.json` require trust verification

### Codex CLI

- Three tiers: `on-request`, `untrusted`, `never`
- `requirements.toml` with `mcp_servers` allowlists
- Network off by default locally (macOS Seatbelt, Linux Landlock+seccomp)

## 5. Uninstalling MCPs Safely

`claude mcp remove <name>` only clears the **global scope** config.

### Residual state to clean up:

- [ ] Project-scoped entries in `~/.claude.json` under `projects.<path>.mcpServers`
- [ ] OAuth tokens in system keychain
- [ ] Lock files in `~/.local/state/claude/locks/`
- [ ] Any files the MCP server created on disk

### Cleanup commands:

```bash
# Remove from specific scope
claude mcp remove <name> -s local
claude mcp remove <name> -s global

# Verify removal
claude mcp list

# Check for residual project-scoped entries
grep -A5 "mcpServers" ~/.claude.json
```

(Source: GitHub issues #7936, #405, #513)

## Sources

| Topic | Source |
|-------|--------|
| MCP security spec | modelcontextprotocol.io/specification/draft/basic/security_best_practices |
| Supply chain (postmark-mcp) | snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails |
| mcp-server-git CVEs | thehackernews.com/2026/01/three-flaws-in-anthropic-mcp-git-server |
| Claude Code security | code.claude.com/docs/en/security |
| Claude Code MCP docs | code.claude.com/docs/en/mcp |
| Uninstall residual state | github.com/anthropics/claude-code issues #7936, #405, #513 |
| Codex security model | developers.openai.com/codex/security |
| MCP attack surface research | unit42.paloaltonetworks.com/model-context-protocol-attack-vectors |

## See Also

- [MCP Trust Tiers](./MCP-TRUST-TIERS.md) — Build vs adapt vs install decision framework
- [MCP Context & Efficiency](./MCP-CONTEXT.md) — Tool Search, context budgets
- [MCP Hub](./README.md) — All MCP documentation
- [CLAUDE-CODE-CONFIG.md](../reference/CLAUDE-CODE-CONFIG.md) — MCP management commands
