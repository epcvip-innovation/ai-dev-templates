# Railway Deployment Documentation

Complete guide to deploying projects to Railway, optimized for Claude Code workflows.

## Overview

This documentation covers EPCVIP's Railway deployment ecosystem as of February 2026.

**Current Setup**:
- Railway CLI installed via npm
- 11 services across multiple Railway projects (all in production)
- MCP server configured for Claude Code integration
- Custom domains on Cloudflare (`*.epcvip.vip`)

## Quick Start

**New to Railway?** Start here:

1. **[Railway Overview](./RAILWAY_OVERVIEW.md)** - What Railway is and why we use it
2. **[MCP Guide](./RAILWAY_MCP_GUIDE.md)** - Using Railway through Claude Code (recommended)
3. **[Setup Guide](./RAILWAY_SETUP_GUIDE.md)** - Initial setup and authentication
4. **[Quickstart Guide](./RAILWAY_QUICKSTART.md)** - Fast reference for day-to-day usage

**Already familiar?** Jump to:
- [CLI Reference](./RAILWAY_CLI_REFERENCE.md) - Command reference
- [Troubleshooting](./RAILWAY_TROUBLESHOOTING.md) - Common issues and solutions

## Documentation Structure

### Overview & MCP

- **[RAILWAY_OVERVIEW.md](./RAILWAY_OVERVIEW.md)** - What Railway is and why we use it
  - Platform overview and competitive positioning
  - Why EPCVIP chose Railway
  - Ecosystem summary (11 services)
  - Three interaction methods: MCP, CLI, Dashboard
  - Key concepts and pricing

- **[RAILWAY_MCP_GUIDE.md](./RAILWAY_MCP_GUIDE.md)** - Railway MCP for Claude Code
  - MCP vs CLI vs Dashboard comparison
  - Complete tool reference (16 tools)
  - 5 workflow recipes
  - Decision tree for choosing interaction method
  - Safety model and troubleshooting

### Getting Started

- **[RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md)** - Quick reference
  - Your current setup confirmation
  - Claude Code compatibility guide
  - Common commands and patterns
  - Primary deployment workflow
  - Best practices summary

- **[RAILWAY_SETUP_GUIDE.md](./RAILWAY_SETUP_GUIDE.md)** - Complete setup process
  - CLI installation methods
  - Authentication flow (with Claude Code limitations)
  - Adding Railway to existing repositories
  - Project linking and initial deployment
  - Environment variables setup

### Framework-Specific Guides

- **[RAILWAY_NEXTJS.md](./RAILWAY_NEXTJS.md)** - Next.js deployment (NEW)
  - Next.js 15 + React 19 configuration
  - Standalone output setup
  - Port mismatch troubleshooting
  - Health check endpoints
  - Supabase integration

### Core Guides

- **[RAILWAY_WORKFLOWS.md](./RAILWAY_WORKFLOWS.md)** - Deployment workflows
  - Initial deployment process
  - Day-to-day development workflow
  - Environment variables management
  - Monitoring and debugging
  - Database operations
  - Cron service setup
  - Emergency procedures

- **[RAILWAY_CONFIG_REFERENCE.md](./RAILWAY_CONFIG_REFERENCE.md)** - Configuration guide
  - railway.toml complete reference
  - Your working configurations (docs-site, ping-tree-compare)
  - NIXPACKS vs RAILPACK comparison
  - Build and deploy configuration options
  - Volume mounts and persistence
  - Environment-specific overrides

### Reference Documentation

- **[RAILWAY_CLI_REFERENCE.md](./RAILWAY_CLI_REFERENCE.md)** - Command reference
  - Complete CLI command list
  - Claude Code compatibility for each command
  - Common command patterns
  - Non-interactive usage
  - CI/CD integration

- **[RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)** - Common issues
  - Authentication issues
  - Deployment failures
  - Database problems (SQLite locking, persistence)
  - Environment variable issues
  - Claude Code specific problems
  - Quick reference table

### Advanced Topics

- **[RAILWAY_AUTOMATION.md](./RAILWAY_AUTOMATION.md)** - Automation patterns
  - Non-interactive CLI usage
  - Project token authentication
  - Automated deployment scripts
  - Health check automation
  - CI/CD integration (GitHub Actions, GitLab CI)
  - Database automation
  - Monitoring automation

- **[RAILWAY_BUILDER_MIGRATION.md](./RAILWAY_BUILDER_MIGRATION.md)** - NIXPACKS to RAILPACK
  - Why migrate (77% smaller Python images, 38% smaller Node images)
  - Migration decision framework
  - Step-by-step migration process
  - Project-specific migration notes for your repos
  - Rollback procedures

## Templates & Scripts

### Configuration Templates

Location: `../../templates/railway/`

**NIXPACKS Templates** (Legacy, still used by ping-tree-compare):
- `nixpacks.python-basic.toml` - Basic Python FastAPI
- `nixpacks.python-volume.toml` - Python with SQLite
- `nixpacks.cron.toml` - Cron service

**RAILPACK Templates** (Modern, recommended):
- `railpack.python-basic.toml` - Basic Python with 77% smaller images
- `railpack.python-volume.toml` - Python with SQLite and volumes
- `railpack.python-migrations.toml` - Python with auto-migrations
- `railpack.node-basic.toml` - Node.js with 38% smaller images

**See**: [templates/railway/README.md](../../templates/railway/README.md)

### Automation Scripts

Location: `../../templates/railway/scripts/`

- `deploy.sh` - Complete deployment with testing and verification
- `health-check.sh` - Quick health verification
- `monitor.sh` - Continuous health monitoring
- `audit-variables.sh` - Environment variable checker

**See**: [templates/railway/scripts/README.md](../../templates/railway/scripts/README.md)

## Claude Code Integration

### What Works in Claude Code ✅

These commands work perfectly:
```bash
railway logs --follow         # Monitor deployments
railway status               # Check project status
railway variables            # Manage environment variables
git push origin main         # Trigger automatic deployment
curl https://app.up.railway.app/health  # Health checks
```

### What Requires External Terminal ❌

These require external bash terminal:
```bash
railway login    # Interactive browser authentication
railway ssh      # Interactive shell into container
```

**Workflow**: Authenticate externally → Reopen Claude Code → Continue with deployment

### Claude Code Best Practices

1. **Use git push for deployments** - Automatic, no CLI interaction needed
2. **Use HTTP endpoints for database queries** - Instead of `railway ssh`
3. **Use `railway logs --json | jq`** - For programmatic log analysis
4. **Create admin API endpoints** - For operations that would normally need SSH

**See**: [RAILWAY_QUICKSTART.md#claude-code-compatibility](./RAILWAY_QUICKSTART.md#claude-code-compatibility)

## Your Production Deployments

### Active Production Services

- **docs-site**: https://docs.epcvip.vip
  - Python FastAPI
  - RAILPACK builder

- **ping-tree-compare**: https://compare.epcvip.vip
  - Python FastAPI + SQLite with persistent volume
  - Single worker for SQLite
  - NIXPACKS builder (pending RAILPACK migration)

### Configuration Status

| Project | Builder | Volume | Framework | Status |
|---------|---------|--------|-----------|--------|
| docs-site | RAILPACK | No | Python | Production |
| ping-tree-compare | NIXPACKS | Yes (/app/data) | Python | Production |

**Recommendation**: Consider migrating Python/Node.js apps to RAILPACK for smaller images and better caching.

## Common Tasks

### Deploy a New Project

```bash
# 1. Navigate to project
cd ~/repos/your-project

# 2. Copy railway.toml template
cp ~/repos/ai-dev-templates/templates/railway/railpack.python-basic.toml ./railway.toml

# 3. Set environment variables
railway variables set DATABASE_PATH=/app/data/db.sqlite
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)

# 4. Deploy
git add railway.toml
git commit -m "feat: add Railway configuration"
git push origin main

# 5. Monitor
railway logs --follow
```

**Full guide**: [RAILWAY_WORKFLOWS.md#initial-deployment](./RAILWAY_WORKFLOWS.md#initial-deployment)

### Update Existing Deployment

```bash
# 1. Make changes
vim main.py

# 2. Test locally
pytest tests/

# 3. Deploy
git add .
git commit -m "fix: resolve issue"
git push origin main

# 4. Verify
railway logs --follow
curl https://your-app.up.railway.app/health
```

**Full guide**: [RAILWAY_WORKFLOWS.md#day-to-day-development](./RAILWAY_WORKFLOWS.md#day-to-day-development)

### Troubleshoot Issues

```bash
# Check status
railway status

# View logs
railway logs --limit 100

# Check for errors
railway logs --json | jq 'select(.level=="error")'

# Verify health
curl https://your-app.up.railway.app/health
```

**Full guide**: [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)

## Migration Path: NIXPACKS → RAILPACK

Your projects currently use NIXPACKS (deprecated). RAILPACK offers:
- **77% smaller Python images** (faster deploys, lower costs)
- **38% smaller Node.js images**
- Better caching and build times
- Active development and new features

**Migration is optional** - NIXPACKS continues to work in maintenance mode.

**See**: [RAILWAY_BUILDER_MIGRATION.md](./RAILWAY_BUILDER_MIGRATION.md)

## Key Concepts

### Automatic Git Push Deployment

Your primary deployment method:
1. Connect GitHub repo to Railway (one-time)
2. Push to main branch
3. Railway automatically builds and deploys
4. No Railway CLI commands needed!

### Health Checks

Railway pings your `/health` endpoint to verify deployment success:
```python
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

Configure timeout in `railway.toml`:
```toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 120  # seconds
```

### Environment Variables

Set via CLI (triggers automatic redeploy):
```bash
railway variables set KEY=value
```

Or via Railway dashboard for multiline values (JSON credentials, etc.).

### Persistent Volumes

For SQLite or file uploads that must persist:
```toml
[[deploy.volumeMounts]]
mountPath = "/app/data"
```

Then set database path:
```bash
railway variables set DATABASE_PATH=/app/data/db.sqlite
```

### SQLite Single Worker Requirement

SQLite doesn't support multiple concurrent writes:
```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"
```

**Critical**: Always use `--workers 1` with SQLite.

## External Resources

- **Railway Documentation**: https://docs.railway.com
- **Railway Status**: https://railway.app/status
- **Railway CLI GitHub**: https://github.com/railwayapp/cli
- **Cron Schedule Helper**: https://crontab.guru/

## File Organization

```
dev-setup/
├── docs/
│   └── railway/
│       ├── README.md                          # This file
│       ├── RAILWAY_OVERVIEW.md                # What Railway is, why we use it
│       ├── RAILWAY_MCP_GUIDE.md               # MCP server for Claude Code
│       ├── RAILWAY_QUICKSTART.md              # Quick reference
│       ├── RAILWAY_SETUP_GUIDE.md             # Initial setup
│       ├── RAILWAY_NEXTJS.md                  # Next.js deployment
│       ├── RAILWAY_WORKFLOWS.md               # Deployment workflows
│       ├── RAILWAY_CLI_REFERENCE.md           # CLI commands
│       ├── RAILWAY_CONFIG_REFERENCE.md        # Configuration
│       ├── RAILWAY_TROUBLESHOOTING.md         # Common issues
│       ├── RAILWAY_AUTOMATION.md              # Automation patterns
│       └── RAILWAY_BUILDER_MIGRATION.md       # NIXPACKS → RAILPACK
└── templates/
    └── railway/
        ├── README.md                          # Template guide
        ├── nixpacks.python-basic.toml        # Basic Python
        ├── nixpacks.python-volume.toml       # Python + SQLite
        ├── nixpacks.cron.toml                 # Cron service
        ├── railpack.python-basic.toml        # Modern Python
        ├── railpack.python-volume.toml       # Modern + SQLite
        ├── railpack.python-migrations.toml   # With migrations
        ├── railpack.node-basic.toml          # Node.js
        └── scripts/
            ├── README.md                      # Script guide
            ├── deploy.sh                      # Deployment automation
            ├── health-check.sh                # Health verification
            ├── monitor.sh                     # Continuous monitoring
            └── audit-variables.sh             # Variable checker
```

## Quick Navigation

**By Task**:
- What is Railway? → [Overview](./RAILWAY_OVERVIEW.md)
- Using Railway from Claude Code → [MCP Guide](./RAILWAY_MCP_GUIDE.md)
- First-time Railway setup → [Setup Guide](./RAILWAY_SETUP_GUIDE.md)
- Deploy Next.js app → [Next.js Guide](./RAILWAY_NEXTJS.md)
- Deploy new project → [Workflows: Initial Deployment](./RAILWAY_WORKFLOWS.md#initial-deployment)
- Update existing project → [Workflows: Day-to-Day](./RAILWAY_WORKFLOWS.md#day-to-day-development)
- Something's broken → [Troubleshooting](./RAILWAY_TROUBLESHOOTING.md)
- Need a command → [CLI Reference](./RAILWAY_CLI_REFERENCE.md)
- Configure railway.toml → [Config Reference](./RAILWAY_CONFIG_REFERENCE.md)

**By Experience Level**:
- **Beginner**: Start with [Overview](./RAILWAY_OVERVIEW.md), then [Setup Guide](./RAILWAY_SETUP_GUIDE.md)
- **Intermediate**: Focus on [MCP Guide](./RAILWAY_MCP_GUIDE.md) and [Workflows](./RAILWAY_WORKFLOWS.md)
- **Advanced**: Explore [Automation](./RAILWAY_AUTOMATION.md) and [Builder Migration](./RAILWAY_BUILDER_MIGRATION.md)

---

**Documentation Version**: 2.0
**Last Updated**: February 2026
**Based On**: 11 production EPCVIP services + Railway best practices as of February 2026
**Optimized For**: Claude Code workflows (MCP-first)

---

**Questions or Issues?**
- Check [Troubleshooting Guide](./RAILWAY_TROUBLESHOOTING.md)
- Railway Status: https://railway.app/status
- Railway Docs: https://docs.railway.com
