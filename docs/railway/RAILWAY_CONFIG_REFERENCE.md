# Railway Configuration Reference

Complete guide to `railway.toml` configuration based on your working projects and latest Railway standards.

## Configuration File

Railway looks for `railway.toml` or `railway.json` in your repository root. Configuration defined in code overrides dashboard settings for that specific deployment only.

**Format**: This guide uses `railway.toml` (TOML format).

## Your Working Configurations

### tiller-bridge (Basic Python Service)

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info"
healthcheckPath = "/health"
healthcheckTimeout = 60
restartPolicyType = "on_failure"

[environment]
NIXPACKS_PYTHON_VERSION = "3.11"
```

### ping-tree-compare (Python with Persistent Volume)

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info --workers 1"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "on_failure"

[[deploy.volumeMounts]]
mountPath = "/app/data"

[environment]
NIXPACKS_PYTHON_VERSION = "3.11"
```

**Note**: `--workers 1` is critical for SQLite to prevent database locking.

### tiller-bridge-cron (Scheduled Service)

```toml
[build]
builder = "nixpacks"

[deploy]
cronSchedule = "0,30 * * * *"  # Every 30 minutes
startCommand = "python -m utils.sync_runner --type smart"

[environment]
NIXPACKS_PYTHON_VERSION = "3.11"
```

---

## Build Configuration

### Builder Selection

**NIXPACKS** (Your current - deprecated but still works):
```toml
[build]
builder = "nixpacks"
```

**RAILPACK** (Recommended for new projects):
```toml
[build]
builder = "RAILPACK"
```

**Dockerfile** (Custom builds):
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"  # Optional: default is "Dockerfile"
```

### Build Command

Override the default build command:

```toml
[build]
buildCommand = "npm run build"
```

### Watch Patterns

Conditionally trigger deploys based on file changes:

```toml
[build]
watchPatterns = ["src/**", "!tests/**"]
```

Only deploys when files in `src/` change, ignoring `tests/`.

### RAILPACK Version (Optional)

```toml
[build]
builder = "RAILPACK"
railpackVersion = "0.7.0"
```

---

## Deploy Configuration

### Start Command

**Python/FastAPI** (your pattern):
```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

**Python/Flask**:
```toml
[deploy]
startCommand = "gunicorn -w 4 -b 0.0.0.0:$PORT app:app"
```

**Node.js**:
```toml
[deploy]
startCommand = "node index.js"
```

**Note**: Always use `$PORT` - Railway provides this variable.

### Health Checks

Railway pings this endpoint to verify deployment success.

**Your patterns**:
```toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 60   # tiller-bridge: 60 seconds
healthcheckTimeout = 120  # ping-tree-compare: 120 seconds
```

**Recommendations**:
- **Simple apps**: 60 seconds
- **Database initialization**: 120 seconds
- **Heavy startup**: 180-300 seconds

**Health endpoint example** (FastAPI):
```python
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Restart Policies

**Your current** (NIXPACKS lowercase):
```toml
[deploy]
restartPolicyType = "on_failure"
```

**RAILPACK** (uppercase):
```toml
[deploy]
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

**Options**:
- `ON_FAILURE` - Restart only on failure (recommended)
- `ALWAYS` - Always restart (for services that should never stop)
- `NEVER` - Don't restart (for one-time jobs)

### Pre-Deploy Commands

Run commands before service starts (e.g., database migrations):

```toml
[deploy]
preDeployCommand = ["python", "manage.py", "migrate"]
```

**Multiple commands**:
```toml
[deploy]
preDeployCommand = ["npm", "run", "migrate"]
```

### Cron Schedule

For scheduled jobs (like tiller-bridge cron service):

```toml
[deploy]
cronSchedule = "0,30 * * * *"  # Every 30 minutes
cronSchedule = "0 */6 * * *"   # Every 6 hours
cronSchedule = "0 2 * * *"     # Daily at 2 AM
```

**Note**: Cron services don't need health checks.

### Zero-Downtime Deployments

Control deployment overlap and shutdown:

```toml
[deploy]
overlapSeconds = "60"      # New deploy overlaps old for 60s
drainingSeconds = "10"     # Wait 10s between SIGTERM and SIGKILL
```

---

## Volume Mounts

For persistent storage (databases, uploads, etc.).

**Your pattern** (ping-tree-compare):
```toml
[[deploy.volumeMounts]]
mountPath = "/app/data"
```

**Named volume**:
```toml
[[deploy.volumeMounts]]
name = "my-volume"
mountPath = "/app/data"
```

**Common mount paths**:
- `/app/data` - Application data
- `/data` - General data
- `/var/lib/postgresql/data` - PostgreSQL
- `/uploads` - User uploads

**Note**: Volumes persist across deployments. All containers in a service share the same volume.

---

## Environment Variables

Set environment-specific variables in configuration.

**Your pattern** (NIXPACKS Python version):
```toml
[environment]
NIXPACKS_PYTHON_VERSION = "3.11"
```

**RAILPACK Python version** (detected from files):
- `runtime.txt`
- `pyproject.toml`
- `.python-version`

**Node.js version**:
```toml
[environment]
NIXPACKS_NODE_VERSION = "18"
```

**Note**: Sensitive values (secrets, API keys) should be set in Railway dashboard or via `railway variables`, not in `railway.toml`.

---

## Environment-Specific Overrides

Apply different configurations per environment:

```toml
[environments.production]
[environments.production.deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4"

[environments.staging]
[environments.staging.deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"
healthcheckTimeout = 300
```

**Priority**: environment config → base config → dashboard settings

---

## Complete Configuration Examples

### Basic Python FastAPI Service

```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### Python with SQLite + Volume

```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"

[[deploy.volumeMounts]]
mountPath = "/app/data"
```

**Note**: Single worker required for SQLite to prevent locking.

### Python with Migrations

```toml
[build]
builder = "RAILPACK"

[deploy]
preDeployCommand = ["python", "manage.py", "migrate"]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
```

### Node.js Application

```toml
[build]
builder = "RAILPACK"
buildCommand = "npm run build"

[deploy]
startCommand = "node dist/index.js"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
```

### Cron Service

```toml
[build]
builder = "RAILPACK"

[deploy]
cronSchedule = "0 */6 * * *"  # Every 6 hours
startCommand = "python scripts/sync_data.py"
```

### Monorepo Service

```toml
[build]
builder = "RAILPACK"
watchPatterns = ["backend/**"]

[deploy]
startCommand = "node backend/dist/index.js"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
```

### Multi-Region Deployment

```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 120

[deploy.multiRegionConfig]
[deploy.multiRegionConfig.us-west2]
numReplicas = 2

[deploy.multiRegionConfig."europe-west4-drams3a"]
numReplicas = 2
```

---

## Configuration Best Practices

### 1. Always Include Health Checks

```toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 120
```

Without health checks, Railway can't verify successful deployment.

### 2. Use Appropriate Timeouts

- **Simple apps**: 60s
- **Database apps**: 120s
- **Heavy initialization**: 180-300s

### 3. Set Restart Policy

```toml
[deploy]
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

Prevents infinite restart loops.

### 4. SQLite Requires Single Worker

```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"
```

Multiple workers cause database locking.

### 5. Use Volumes for Persistence

```toml
[[deploy.volumeMounts]]
mountPath = "/app/data"
```

Without volumes, data is lost on redeploy.

### 6. Never Commit Secrets

Don't put secrets in `railway.toml`:
```toml
# ❌ BAD
[environment]
JWT_SECRET = "my-secret-key"

# ✅ GOOD - Set via Railway CLI or dashboard
[environment]
NODE_ENV = "production"  # Safe non-sensitive values only
```

### 7. Use Pre-Deploy Commands for Migrations

```toml
[deploy]
preDeployCommand = ["python", "manage.py", "migrate"]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

Ensures database is up-to-date before app starts.

### 8. Consider Zero-Downtime Deploys

```toml
[deploy]
overlapSeconds = "60"
drainingSeconds = "10"
```

For production services with active traffic.

---

## Migrating Your Existing Configs

### Update tiller-bridge to RAILPACK

**Current** (NIXPACKS):
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info"
healthcheckPath = "/health"
healthcheckTimeout = 60
restartPolicyType = "on_failure"

[environment]
NIXPACKS_PYTHON_VERSION = "3.11"
```

**Updated** (RAILPACK):
```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info"
healthcheckPath = "/health"
healthcheckTimeout = 60
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

Remove `[environment]` section - RAILPACK auto-detects Python version.

### Update ping-tree-compare to RAILPACK

**Current** (NIXPACKS):
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info --workers 1"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "on_failure"

[[deploy.volumeMounts]]
mountPath = "/app/data"

[environment]
NIXPACKS_PYTHON_VERSION = "3.11"
```

**Updated** (RAILPACK):
```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info --workers 1"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[[deploy.volumeMounts]]
mountPath = "/app/data"
```

Same changes: remove `[environment]`, update `restartPolicyType` to uppercase.

---

## Troubleshooting Configuration Issues

### Build Fails

**Problem**: Build errors
**Solution**:
1. Check `railway logs --build`
2. Verify builder is correct
3. Ensure dependencies are specified (requirements.txt, package.json)

### Health Check Fails

**Problem**: Deployment fails health check
**Solution**:
1. Increase `healthcheckTimeout`
2. Verify `/health` endpoint exists and returns 200
3. Check logs: `railway logs`

### App Crashes on Start

**Problem**: Service restarts repeatedly
**Solution**:
1. Check logs: `railway logs --limit 100`
2. Verify start command is correct
3. Check environment variables: `railway variables`
4. Set `restartPolicyMaxRetries = 3` to prevent infinite loops

### Volume Not Persisting

**Problem**: Data lost on redeploy
**Solution**:
1. Verify `[[deploy.volumeMounts]]` is configured
2. Check mount path matches your app's database path
3. Verify DATABASE_PATH env var points to mount path

### SQLite Database Locked

**Problem**: "database is locked" errors
**Solution**:
```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"
```
Must use single worker for SQLite.

---

## Next Steps

- **Templates**: See `templates/railway/` for copy-paste configurations
- **Workflows**: [RAILWAY_WORKFLOWS.md](./RAILWAY_WORKFLOWS.md)
- **Migration Guide**: [RAILWAY_BUILDER_MIGRATION.md](./RAILWAY_BUILDER_MIGRATION.md)
- **Troubleshooting**: [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)

---

## Resources

- **Railway Config Documentation**: https://docs.railway.com/reference/config-as-code
- **Your Working Configs**:
  - tiller-bridge/railway.toml
  - ping-tree-compare/railway.toml
  - tiller-bridge/railway.cron.toml
