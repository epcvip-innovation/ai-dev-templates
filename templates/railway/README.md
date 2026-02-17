# Railway Configuration Templates

[← Back to Main README](../../README.md)

Ready-to-use `railway.toml` templates for common project types.

**Quick Reference**: See [../docs/railway/CLAUDE.md](../docs/railway/CLAUDE.md) for Claude Code integration guide.

## Template Files

### RAILPACK (Recommended)

Modern builder with smaller images and better caching:

- **`railpack.python-basic.toml`** - Python FastAPI
  - 77% smaller images, better caching
  - Use case: any Python API service

- **`railpack.python-volume.toml`** - Python + SQLite with persistence
  - Volume mount for database persistence
  - Single worker for SQLite concurrency
  - Use case: any app with local SQLite persistence

- **`railpack.python-migrations.toml`** - Python with database migrations
  - Pre-deploy command for Alembic/Flask-Migrate
  - Runs migrations before starting app

- **`railpack.node-basic.toml`** - Node.js applications
  - 38% smaller images vs NIXPACKS
  - Auto-detects Node version

### NIXPACKS (Legacy)

Deprecated but still functional. Use RAILPACK for new projects.

- **`nixpacks.python-basic.toml`** - Basic Python FastAPI
- **`nixpacks.python-volume.toml`** - Python + SQLite
- **`nixpacks.cron.toml`** - Scheduled cron service

## Usage

### 1. Choose a Template

| Project Type | Template |
|-------------|----------|
| Python API | `railpack.python-basic.toml` |
| Python + SQLite | `railpack.python-volume.toml` |
| Python + Migrations | `railpack.python-migrations.toml` |
| Node.js | `railpack.node-basic.toml` |
| Scheduled tasks | `nixpacks.cron.toml` |

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
startCommand = "python -m uvicorn main:app --host 0.0.0.0 --port $PORT"  # Use python -m for PATH reliability
healthcheckPath = "/health"  # Verify endpoint exists
healthcheckTimeout = 120     # 60s for simple apps, 120s with database
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

**Note**: All templates are based on working production deployments.

## See Also

- [Railway Documentation](../../docs/railway/README.md) — Setup, configuration, and workflow guides
- [CI/CD Templates](../ci/README.md) — GitHub Actions for deployment
- [All Templates](../README.md)
