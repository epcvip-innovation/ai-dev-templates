# Railway Configuration Templates

Ready-to-use `railway.toml` templates for common project types.

## Template Files

### NIXPACKS (Your Current Working Configs)

Based on your production deployments:

- **`nixpacks.python-basic.toml`** - Basic Python FastAPI service
  - Source: tiller-bridge configuration
  - Use for: Simple API services without persistence

- **`nixpacks.python-volume.toml`** - Python FastAPI with SQLite
  - Source: ping-tree-compare configuration
  - Use for: Apps with SQLite database needing persistence
  - Includes: Volume mount, single worker for SQLite

- **`nixpacks.cron.toml`** - Scheduled cron service
  - Source: tiller-bridge cron service
  - Use for: Scheduled background tasks
  - Separate Railway service required

### RAILPACK (Modern, Recommended)

Updated versions with RAILPACK builder:

- **`railpack.python-basic.toml`** - Basic Python FastAPI (RAILPACK)
  - 77% smaller images vs NIXPACKS
  - Better caching and build times

- **`railpack.python-volume.toml`** - Python with SQLite (RAILPACK)
  - Includes volume mount configuration
  - Single worker for SQLite

- **`railpack.python-migrations.toml`** - Python with auto-migrations
  - Runs migrations before deployment
  - Examples for Alembic, Flask-Migrate, custom scripts

- **`railpack.node-basic.toml`** - Node.js application
  - 38% smaller images vs NIXPACKS
  - Auto-detects Node version

## Usage

### 1. Choose a Template

Select based on your project type:

| Project Type | Template |
|-------------|----------|
| Python API (simple) | `nixpacks.python-basic.toml` or `railpack.python-basic.toml` |
| Python + SQLite | `nixpacks.python-volume.toml` or `railpack.python-volume.toml` |
| Python + Migrations | `railpack.python-migrations.toml` |
| Scheduled tasks | `nixpacks.cron.toml` |
| Node.js | `railpack.node-basic.toml` |

### 2. Copy to Your Project

```bash
# Navigate to your project
cd ~/repos/your-project

# Copy template
cp ~/repos/ai-dev-templates/templates/railway/railpack.python-basic.toml ./railway.toml

# Edit as needed
vim railway.toml
```

### 3. Customize

Update these fields in `railway.toml`:

```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"  # Match your app
healthcheckPath = "/health"  # Verify endpoint exists
healthcheckTimeout = 60      # Adjust based on startup time
```

### 4. Set Environment Variables

```bash
# Required for volume-based configs
railway variables set DATABASE_PATH=/app/data/your_db.sqlite

# Other common variables
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)
railway variables set ENVIRONMENT=production
```

### 5. Deploy

```bash
git add railway.toml
git commit -m "feat: add Railway configuration"
git push origin main
```

## Template Comparison

### NIXPACKS vs RAILPACK

| Feature | NIXPACKS | RAILPACK |
|---------|----------|----------|
| Status | Deprecated but works | Current, recommended |
| Image Size (Python) | Baseline | 77% smaller |
| Image Size (Node) | Baseline | 38% smaller |
| Caching | Good | Better (BuildKit integration) |
| Version Control | Approximate | Exact (major.minor.patch) |
| Configuration | Via environment vars | Auto-detected |
| Active Development | Maintenance only | Yes |

**Recommendation**: Use RAILPACK for new projects. Existing NIXPACKS configs continue working.

## Common Patterns

### SQLite Database

Always use:
- Single worker: `--workers 1`
- Volume mount: `[[deploy.volumeMounts]]`
- Environment variable: `DATABASE_PATH=/app/data/db.sqlite`

### Health Checks

Recommended timeouts:
- Simple apps: 60 seconds
- With database: 120 seconds
- Heavy startup: 180-300 seconds

### Restart Policies

- **ON_FAILURE** (recommended): Restart only on crashes
- **ALWAYS**: Always restart (use for services that must stay running)
- **NEVER**: Don't restart (use for one-time jobs)

## Helper Scripts

See `scripts/` directory for automation scripts:

- `deploy.sh` - Automated deployment with verification
- `health-check.sh` - Verify deployment health
- `monitor.sh` - Continuous health monitoring
- `audit-variables.sh` - Check required environment variables

## Next Steps

- **Setup Guide**: [../docs/railway/RAILWAY_SETUP_GUIDE.md](../docs/railway/RAILWAY_SETUP_GUIDE.md)
- **Configuration Reference**: [../docs/railway/RAILWAY_CONFIG_REFERENCE.md](../docs/railway/RAILWAY_CONFIG_REFERENCE.md)
- **Workflows**: [../docs/railway/RAILWAY_WORKFLOWS.md](../docs/railway/RAILWAY_WORKFLOWS.md)

---

**Note**: All templates are based on your working production deployments (tiller-bridge, ping-tree-compare).
