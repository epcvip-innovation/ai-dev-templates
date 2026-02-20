# AI Agent Security Templates

[← Back to Main README](../../README.md)

**Purpose**: Tiered security configurations for AI coding agents

**Start here**: [AI-AGENT-SECURITY-GUIDE.md](AI-AGENT-SECURITY-GUIDE.md)

---

## Quick Navigation

| Need | Go To |
|------|-------|
| **Why this matters** | [Security Guide — Threat Model](AI-AGENT-SECURITY-GUIDE.md#why-this-matters) |
| **Pick your security tier** | [Security Guide — Tiers](AI-AGENT-SECURITY-GUIDE.md#tiered-security-levels) |
| **Copy-paste settings** | Tier directories below (settings.json.example files) |

---

## Tier Overview

| Tier | For | Time | Key Addition |
|------|-----|------|-------------|
| **[Tier 1 — Baseline](tier-1-baseline/)** | Every project | 5 min | `settings.json` deny list |
| **[Tier 2 — Team Standard](tier-2-team/)** | Shared projects | 15 min | PreToolUse hook + externalized conf files |
| **[Tier 3 — Strict](tier-3-strict/)** | Production / compliance | 30 min | Wrapper scripts + audit logging + enterprise lockdown |

---

## Directory Structure

```
security/
├── AI-AGENT-SECURITY-GUIDE.md          # Main best practices guide
├── README.md                            # This file
├── tier-1-baseline/
│   └── settings.json.example           # Minimal deny list + file tool auto-allow
├── tier-2-team/
│   ├── settings.json.example           # Hook registration + permissions
│   ├── pretooluse-command-filter.sh     # Generic deny/allow hook
│   ├── denied-commands.conf            # Externalized deny patterns
│   └── allowed-commands.conf           # Externalized allow patterns
└── tier-3-strict/
    ├── settings.json.example           # Full lockdown config
    ├── denied-commands.conf            # Extended deny list (41+ entries)
    ├── allowed-commands.conf           # Minimal allow list
    └── wrapper-example.sh              # Agent wrapper script
```

---

## See Also

- [Hooks](../hooks/README.md) — Hook templates and reference documentation
- [Permissions](../permissions/README.md) — Permission configuration templates
- [HOOKS_REFERENCE.md](../hooks/HOOKS_REFERENCE.md) — Complete hooks technical reference

---

**Last Updated**: 2026-02-19
