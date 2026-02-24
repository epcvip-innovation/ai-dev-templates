# MCP Trust Tiers

[← Back to MCP Hub](./README.md) | [← Back to Main README](../../README.md)

## Overview

Not all MCP servers carry the same risk. This framework classifies MCPs into
four trust tiers based on who controls the source code, how it was reviewed,
and what access it has. Use this to decide whether to build, adapt, or install.

## The Four Tiers

### Tier 1: First-Party (You Built It)

**Trust level:** Highest

- Source code lives in your repo or org
- You control every line, every dependency, every update
- No supply chain risk — you *are* the supply chain

**Examples:**
- Custom MCP wrapping your internal API
- A skill that orchestrates your deploy pipeline
- A data access layer tailored to your schema

**When to build:** The task is core to your workflow, touches sensitive data,
or needs to evolve with your system. The initial investment pays back on every
future session.

---

### Tier 2: Adapted (Forked & Reviewed)

**Trust level:** High

- Started from someone else's code (open source, community, vendor)
- You forked it, read the source, stripped what you don't need
- You own the result and control updates

**Examples:**
- Community MCP server forked to remove unused write tools
- Vendor MCP with custom validation hooks added
- Open-source MCP pinned to a specific commit hash

**When to adapt:** The capability exists but doesn't match your needs exactly.
Forking is faster than building from scratch, and you still get full control.

---

### Tier 3: Verified Third-Party (Official, Pinned)

**Trust level:** Moderate

- Published by the vendor or a known, reputable maintainer
- Pinned to an exact version (`@0.0.64`, not `@latest`)
- Permissions reviewed before first use

**Examples:**
- `@playwright/mcp@0.0.64` — Playwright's official MCP
- `@anthropic/supabase-mcp` — Supabase's official integration
- `@railway/mcp` — Railway's official deploy tooling

**Requirements before use:**
- Pin exact version in config
- Review tool list and permissions
- Understand what write capabilities it has
- Set up update review cadence (monthly check)

---

### Tier 4: Unverified Third-Party (Community, Unvetted)

**Trust level:** Low — requires full vetting

- Published by unknown or unverified authors
- No guarantee of code quality, security, or maintenance
- Highest supply chain risk

**Examples:**
- Random npm packages with MCP in the name
- GitHub repos with < 50 stars and no security audit
- Any MCP installed via copy-paste from a blog post

**Requirements before use:**
- Complete the vetting checklist below
- Consider adapting (Tier 2) instead of using as-is
- Never use with `@latest` — always pin exact version

## Decision Tree: Build, Adapt, or Install?

```
Does this MCP touch sensitive data or credentials?
├── Yes → Build your own (Tier 1)
└── No
    ├── Does an official vendor MCP exist?
    │   ├── Yes → Does it do exactly what you need?
    │   │   ├── Yes → Use it, pin version (Tier 3)
    │   │   └── No → Fork and adapt (Tier 2)
    │   └── No → Does a well-maintained community MCP exist?
    │       ├── Yes → Is this core to your workflow?
    │       │   ├── Yes → Fork, vet, and adapt (Tier 2)
    │       │   └── No → Vet and use as-is (Tier 4), pin version
    │       └── No → Build your own (Tier 1)
```

**After choosing a tier**, decide on distribution:

```
Will multiple team members use this MCP?
├── Yes → Add to managed-mcp.json, document review date
└── No → Add to personal config, still pin version
```

## Vetting Checklist (Tier 3-4)

Run through this before installing any third-party MCP:

### Source Review
- [ ] Read the main source file(s) — not just the README
- [ ] Check `package.json` dependencies for known-bad packages
- [ ] Look for obfuscated code, eval(), or dynamic imports from URLs
- [ ] Verify the published npm package matches the GitHub source

### Permissions Audit
- [ ] List all tools the MCP exposes (`claude mcp list-tools <name>`)
- [ ] Identify which tools have write capabilities
- [ ] Check for file system access, network requests, shell execution
- [ ] Confirm you actually need each exposed tool

### Version Pinning
- [ ] Pin to exact version in config (`@0.0.64`, not `@latest`)
- [ ] Record the version and date of review
- [ ] Set a calendar reminder for monthly version check
- [ ] Document what you reviewed in a comment or CHANGELOG

### License & Maintenance
- [ ] Check the license is compatible with your use
- [ ] Verify the package is actively maintained (last commit < 6 months)
- [ ] Check for open security issues or CVEs
- [ ] Note the maintainer — is it an individual or an organization?

## Team Distribution

Once an MCP passes vetting, distribute it safely:

**`managed-mcp.json`** (enforced across team members):
```json
{
  "playwright": {
    "command": "npx",
    "args": ["-y", "@playwright/mcp@0.0.64"]
  }
}
```

> Track tier, review date, and reviewer separately (spreadsheet, CHANGELOG, or comments above the config). These are not `managed-mcp.json` schema fields.

**`.mcp.json`** (committed to the repo):
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@anthropic/supabase-mcp@0.1.3", "--project-ref", "your-ref"]
    }
  }
}
```

## See Also

- [MCP Safety & Version Management](./MCP-SAFETY.md) — Supply chain attacks, real incidents, permission models
- [MCP Context & Efficiency](./MCP-CONTEXT.md) — Tool Search, context budgets
- [AI Agent Security Guide](../../templates/security/AI-AGENT-SECURITY-GUIDE.md) — 3-tier security model
- [Community Skills](../../templates/skills/community/README.md) — Provenance tracking, MANIFEST.yaml
- [MCP Hub](./README.md) — All MCP documentation
