# MCP Context Window & Efficiency

[← Back to MCP Hub](./README.md) | [← Back to Main README](../../README.md)

How MCP servers interact with the context window, and why Claude Code's
lazy loading makes it more efficient than eager-loading alternatives.

## The Problem: Eager Loading

Before Tool Search, all MCP tool definitions loaded at session start. Each
MCP server's complete tool schemas (names, descriptions, parameter definitions)
were injected before any user message. Teams with 5+ MCPs reported losing
50,000-66,000 tokens of their 200k context window before typing anything.

## Tool Search: Lazy Loading (Claude Code)

Claude Code now builds a lightweight search index of tool names and descriptions,
then loads full schemas **on-demand** when Claude determines they're relevant.
Once loaded, tools remain available for the rest of the session.

### Configuration

| `ENABLE_TOOL_SEARCH` | Behavior |
|----------------------|----------|
| `auto` (default) | Activates when MCP tools exceed 10% of context |
| `auto:<N>` | Custom threshold (e.g., `auto:5` for 5%) |
| `true` | Always enabled |
| `false` | Disabled; all tools loaded upfront |

### Impact

Anthropic internal benchmarks:
- **Without Tool Search**: ~77k tokens consumed before work begins (50+ tools)
- **With Tool Search**: ~8.7k tokens (~89% reduction)
- **Accuracy improvement**: Opus 4 went from 49% to 74% on MCP evaluations

**Requirements**: Sonnet 4+ or Opus 4+. Haiku does not support Tool Search.

### Making Tool Search Work Well

Tool Search matches against tool names, descriptions, and parameter names.
To ensure your MCP tools are discoverable:

- Write clear, specific tool names (`create-branch` not `do-thing`)
- Add descriptive descriptions explaining what category of tasks the tool handles
- Add server instructions to your MCP server explaining its purpose

## Context Budget

| Source | Typical Cost | Notes |
|--------|-------------|-------|
| MCP tool definitions (with Tool Search) | 0.5-2k per server | On-demand loading |
| MCP tool definitions (without Tool Search) | 5-30k per server | Full schemas upfront |
| MCP tool output | Warn at 10k, cap at 25k | Configurable: `MAX_MCP_OUTPUT_TOKENS` |
| Full stack (4 MCPs, Tool Search on) | 5-10% of context | Before any conversation |

### Practical Advice

- Rely on Tool Search (enabled by default) — don't disable it
- Only enable MCP servers you need for the current project
- Use project-level `.mcp.json` instead of global config for project-specific MCPs
- Use plugins to toggle expensive MCPs on/off mid-session
- Monitor with `/cost` or context percentage in status line

## Claude Code vs Codex: MCP Efficiency

| Feature | Claude Code | Codex CLI |
|---------|------------|-----------|
| Config format | JSON (`.mcp.json`, `~/.claude.json`) | TOML (`~/.codex/config.toml`) |
| **Tool Search (lazy loading)** | **Yes — default, auto at 10%** | **Not documented** |
| Output token cap | 25k (configurable) | Not documented |
| MCP management CLI | `claude mcp add/remove/list/get` | `codex mcp add/list` |
| OAuth for MCP | Built-in (`/mcp` command) | Built-in (`codex mcp login`) |
| Network default | Approval required | **Off by default** locally |
| Sandboxing | OS-level, approval-gated | macOS Seatbelt, Linux Landlock+seccomp |
| Team allowlisting | `managed-mcp.json`, `allowedMcpServers` | `requirements.toml` |

**Key efficiency difference**: Claude Code's Tool Search is a significant advantage
for MCP-heavy workflows. Where Codex loads all tool schemas upfront, Claude Code
loads them on-demand, preserving ~89% of the context that would otherwise be consumed
by tool definitions. This matters most when using 3+ MCP servers simultaneously.

**Key sandboxing difference**: Codex defaults to no network access locally, while
Claude Code allows network requests upon approval. For MCP servers that need external
access (Railway, Supabase), Codex requires explicit network configuration.

Sources:
- code.claude.com/docs/en/mcp (Tool Search section)
- developers.openai.com/codex/mcp
- developers.openai.com/codex/security

## See Also

- [MCP Safety](./MCP-SAFETY.md) — Security, version pinning, prompt injection
- [MCP Hub](./README.md) — All MCP documentation
- [ADVANCED-WORKFLOWS.md](../reference/ADVANCED-WORKFLOWS.md) — Context management at scale
- [CLAUDE-CODE-CONFIG.md](../reference/CLAUDE-CODE-CONFIG.md) — MCP commands, plugin toggling
