# Railway Deployment Documentation

## Quick Reference

| Task | File |
|------|------|
| What is Railway? | [RAILWAY_OVERVIEW.md](RAILWAY_OVERVIEW.md) |
| Railway MCP (Claude Code) | [RAILWAY_MCP_GUIDE.md](RAILWAY_MCP_GUIDE.md) |
| First time setup | [RAILWAY_SETUP_GUIDE.md](RAILWAY_SETUP_GUIDE.md) |
| Daily reference | [RAILWAY_QUICKSTART.md](RAILWAY_QUICKSTART.md) |
| Deploy a project | [RAILWAY_WORKFLOWS.md](RAILWAY_WORKFLOWS.md) |
| Configure railway.toml | [RAILWAY_CONFIG_REFERENCE.md](RAILWAY_CONFIG_REFERENCE.md) |
| CLI command help | [RAILWAY_CLI_REFERENCE.md](RAILWAY_CLI_REFERENCE.md) |
| Something broken | [RAILWAY_TROUBLESHOOTING.md](RAILWAY_TROUBLESHOOTING.md) |
| Automate deployments | [RAILWAY_AUTOMATION.md](RAILWAY_AUTOMATION.md) |
| Migrate to RAILPACK | [RAILWAY_BUILDER_MIGRATION.md](RAILWAY_BUILDER_MIGRATION.md) |
| Deploy Next.js | [RAILWAY_NEXTJS.md](RAILWAY_NEXTJS.md) |

## Templates

Located in: `/templates/railway/`

| Template | Use Case |
|----------|----------|
| `railpack.python-basic.toml` | Python FastAPI (recommended) |
| `railpack.python-volume.toml` | Python + SQLite with persistence |
| `railpack.python-migrations.toml` | Python with database migrations |
| `railpack.node-basic.toml` | Node.js applications |
| `nixpacks.*.toml` | Legacy (deprecated but working) |

## Claude Code Constraints

### Interactive Commands (Require External Terminal)
```bash
railway login      # Browser OAuth
railway ssh        # Interactive shell
railway link       # Project selection
railway connect    # Database shell
```

### Non-Interactive Commands (Work in Claude Code)
```bash
railway status     # Check project status
railway logs       # View logs
railway variables  # List/set env vars
railway up         # Deploy from CLI
railway redeploy   # Trigger redeploy
```

### Preferred Pattern
Use **git push** for deployments instead of CLI:
```bash
git add . && git commit -m "Deploy" && git push origin main
```

## Key Configuration Patterns

### Minimal railway.toml (Python FastAPI)
```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "python -m uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### With SQLite (Add Volume + Single Worker)
```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"

[[deploy.volumeMounts]]
mountPath = "/app/data"
```

### Health Endpoint Pattern
```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "port": os.getenv("PORT", "unknown")
    }
```

Including `port` in response helps debug port mismatch issues.

## Common Issues

### Health Check Passes But 502 Error
**Cause**: Port mismatch between Public Networking config and app's PORT.

**Fix**: In Railway dashboard → Networking → Select auto-detected port (e.g., "8080 (python)") instead of custom port.

**See**: [RAILWAY_TROUBLESHOOTING.md](RAILWAY_TROUBLESHOOTING.md#port-mismatch-health-check-passes-but-external-requests-fail)

### Config-as-Code Not Working
**Cause**: `railway.toml` not linked in Railway dashboard.

**Fix**: Settings → Config-as-code → Add File Path → Enter `railway.toml`

### NIXPACKS Deprecated Warning
**Cause**: Using legacy builder.

**Fix**: Change `builder = "nixpacks"` to `builder = "RAILPACK"` in railway.toml.

**See**: [RAILWAY_BUILDER_MIGRATION.md](RAILWAY_BUILDER_MIGRATION.md)

## Production Deployments (Reference)

| Project | Stack | Features |
|---------|-------|----------|
| ping-tree-compare | Python + SQLite | Volume persistence, auth |
| tiller-bridge | Python FastAPI | Cron service, automation |
| athena-usage-monitor | Python FastAPI | Supabase auth, Athena |

## Python Version

RAILPACK auto-detects from (in order):
1. `runtime.txt` (e.g., `python-3.11`)
2. `pyproject.toml`
3. `.python-version`

## Environment Variables

Set via CLI or dashboard:
```bash
railway variables set KEY=value
```

Common variables:
- `DATABASE_PATH=/app/data/db.sqlite` (SQLite with volume)
- `JWT_SECRET_KEY` (authentication)
- `ENVIRONMENT=production`

## Scripts

Located in: `/templates/railway/scripts/`

- `deploy.sh` - Full deployment with verification
- `health-check.sh` - Verify health endpoint
- `monitor.sh` - Continuous monitoring
- `audit-variables.sh` - Check env vars
