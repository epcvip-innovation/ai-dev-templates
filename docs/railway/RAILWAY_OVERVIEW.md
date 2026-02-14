# Railway Overview

[← Back to Railway Docs](./README.md) | [MCP Guide →](./RAILWAY_MCP_GUIDE.md) | [Setup Guide →](./RAILWAY_SETUP_GUIDE.md)

**Last Updated**: February 2026

---

## What is Railway?

Railway is a Platform-as-a-Service (PaaS) for deploying applications directly from Git repositories. It handles infrastructure, scaling, networking, and deployments so you can focus on code.

**Key stats** (as of early 2026):
- 2M+ developers
- 29M+ deployments per month
- Supports Node.js, Python, Go, PHP, Rust, Docker, and more

**Competitive positioning**:

| Platform | Strength | Weakness (for us) |
|----------|----------|-------------------|
| **Railway** | Git-push deploys, MCP integration, simple UX | Smaller ecosystem than AWS |
| Heroku | Mature, well-known | Expensive after free tier removal |
| Render | Similar to Railway | No MCP server, less flexible |
| Fly.io | Edge deployment, low latency | More DevOps complexity |
| Vercel | Best for Next.js frontends | Backend support is secondary |
| AWS (ECS/Lambda) | Enterprise-grade | Overkill for small team |

---

## Why EPCVIP Uses Railway

**Team context**: Small innovation team shipping internal tools fast. We need deploys in minutes, not hours of DevOps.

**What Railway gives us**:
- **Git-push deploys** — push to `main`, Railway builds and deploys automatically
- **Pro plan** — $20/seat + usage-based pricing (no idle charges on scale-to-zero)
- **Custom domains** on Cloudflare — all services at `*.epcvip.vip`
- **MCP integration** — Claude Code can manage Railway directly (our primary interaction method)
- **Multi-service projects** — group related services under one project
- **Persistent volumes** — SQLite databases survive redeploys
- **Health checks** — automatic rollback on failed deploys

**What we don't use Railway for**:
- Production customer-facing systems (those run on AWS via `~/epcvip/`)
- Data pipelines (AWS Glue/Athena)
- Authentication (Supabase)

---

## Our Ecosystem

All EPCVIP innovation services deploy on Railway with the architecture:

```
GitHub repo → Railway (build + deploy) → Cloudflare (CDN + SSL) → *.epcvip.vip
```

### Service Summary

| Service | Domain | Stack | Railway Project |
|---------|--------|-------|-----------------|
| Experiments Dashboard | xp.epcvip.vip | FastAPI + Vanilla JS | experiments-dashboard |
| Reports Dashboard | reports.epcvip.vip | FastAPI + Streamlit | EPCVIP Datalake Validator |
| Ping Tree Compare | compare.epcvip.vip | FastAPI + Vanilla JS | ping-tree-compare |
| Athena Monitor | athena.epcvip.vip | FastAPI + Vanilla JS | epcvip-pulse-automation |
| Documentation Hub | docs.epcvip.vip | FastAPI + React/Jinja2 | epcvip.vip \| Hub |
| Tools Hub | epcvip.vip | Express + Vanilla JS | epcvip.vip \| Hub |
| Competitor Analyzer | tools.epcvip.vip | Next.js + React | competitor-analyzer |
| Fwaptile Wordle | fwaptile.com | Express + Vanilla JS | fwaptile-wordle |
| Funnel Step Lab | lab.epcvip.vip | FastAPI + Vanilla JS | funnel-step-lab |
| Admin Dashboard | admin.epcvip.vip | FastAPI + Vanilla JS | epcvip-admin |
| Uptime Kuma | uptime.epcvip.vip | Node.js (self-hosted) | uptime-kuma |

> **Full details**: See [EPCVIP_SERVICES.md](../../../../EPCVIP_SERVICES.md) for auth providers, tech stacks, RBAC setup, and environment variables. This table is intentionally a summary — the services doc is the source of truth.

---

## Three Interaction Methods

Railway offers three ways to manage your services. We use all three depending on context.

### 1. MCP Server (Recommended for Claude Code)

The `@railway/mcp-server` gives Claude Code direct access to Railway operations — checking status, viewing logs, setting variables, deploying, and more. No copy-pasting CLI output.

**Best for**: Everything you do inside a Claude Code session.

**See**: [RAILWAY_MCP_GUIDE.md](./RAILWAY_MCP_GUIDE.md)

### 2. CLI (`railway`)

The Railway CLI works from any terminal. Some commands are interactive (login, SSH) and require an external terminal outside Claude Code.

**Best for**: Initial authentication, SSH into containers, operations Claude Code can't do.

**See**: [RAILWAY_CLI_REFERENCE.md](./RAILWAY_CLI_REFERENCE.md)

### 3. Dashboard (railway.com)

The web dashboard at [railway.com](https://railway.com) provides a visual UI for project management.

**Best for**: Deleting services/projects, billing management, visual project overview, builder configuration.

**See**: [Railway Dashboard](https://railway.com/dashboard)

### When to Use Each

| Task | MCP | CLI | Dashboard |
|------|:---:|:---:|:---------:|
| Check deployment status | **Yes** | Yes | Yes |
| View logs | **Yes** | Yes | Yes |
| Set environment variables | **Yes** | Yes | Yes |
| Deploy from code | **Yes** | Yes | — |
| Initial login/auth | — | **Yes** | — |
| SSH into container | — | **Yes** | — |
| Delete services/projects | — | — | **Yes** |
| Manage billing | — | — | **Yes** |
| Change builder (NIXPACKS/RAILPACK) | — | — | **Yes** |

---

## Key Concepts

### Project
A container for one or more services. Example: `epcvip.vip | Hub` contains both `epcvip-tools-hub` and `docs-site`.

### Service
A single deployable unit within a project. Each service has its own source repo, environment variables, and domain.

### Environment
Isolated configuration contexts (e.g., `production`, `staging`). Variables and domains are per-environment.

### Deployment
A specific build + release of a service. Railway keeps deployment history for rollback.

### Volume
Persistent storage that survives redeploys. Used for SQLite databases (`/app/data`).

### Builder
The system that turns your code into a container image:
- **RAILPACK** (current) — smaller images, better caching, actively developed
- **NIXPACKS** (legacy) — still works, maintenance-only mode

**See**: [RAILWAY_BUILDER_MIGRATION.md](./RAILWAY_BUILDER_MIGRATION.md)

---

## Pricing

| Plan | Cost | Best For |
|------|------|----------|
| **Hobby** | $5/month + usage | Personal projects, side projects |
| **Pro** | $20/seat/month + usage | Teams, production workloads |
| **Enterprise** | Custom | Large orgs, compliance needs |

**Usage-based components**: CPU, memory, network egress, build minutes. Pro plan includes a usage credit.

**EPCVIP uses Pro plan** — the per-seat cost is minimal for a small team, and usage-based pricing means we only pay for what we use.

---

## See Also

- [RAILWAY_MCP_GUIDE.md](./RAILWAY_MCP_GUIDE.md) — MCP server setup and complete tool reference
- [RAILWAY_CLI_REFERENCE.md](./RAILWAY_CLI_REFERENCE.md) — CLI command reference
- [RAILWAY_SETUP_GUIDE.md](./RAILWAY_SETUP_GUIDE.md) — First-time setup and authentication
- [RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md) — Daily reference card
- [RAILWAY_WORKFLOWS.md](./RAILWAY_WORKFLOWS.md) — Deployment workflows
- [RAILWAY_BUILDER_MIGRATION.md](./RAILWAY_BUILDER_MIGRATION.md) — NIXPACKS to RAILPACK migration
- [EPCVIP_SERVICES.md](../../../../EPCVIP_SERVICES.md) — Full service catalog with auth and architecture

## External Resources

- [Railway Documentation](https://docs.railway.com)
- [Railway Blog](https://blog.railway.com)
- [Railway Status](https://railway.app/status)
- [Railway MCP Server](https://github.com/nichochar/railway-mcp-server)

---

**Last Updated**: February 2026
