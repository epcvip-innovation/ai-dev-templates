# Railway Troubleshooting Guide

Common issues and solutions for Railway deployments and Claude Code workflows.

## Authentication Issues

### `railway login` Doesn't Work in Claude Code

**Problem**: Interactive browser authentication fails in Claude Code terminal

**Solution**: **Must use external terminal**
```bash
# In external terminal (not Claude Code):
railway login

# After authentication completes, reopen Claude Code
# Verify in Claude Code:
railway whoami
```

**Why**: Claude Code cannot handle interactive browser OAuth flows.

### `railway: command not found`

**Problem**: Railway CLI not in PATH

**Solution**:
```bash
# Check installation
which railway
npm list -g @railway/cli

# Reinstall if needed
npm install -g @railway/cli

# Verify
railway --version
```

### Authentication Expires

**Problem**: `railway whoami` shows "Not authenticated"

**Solution**:
```bash
# Re-authenticate in external terminal
railway login

# Or use project token for long-term access
export RAILWAY_TOKEN=your-project-token
```

---

## Health Check & Port Issues

### Health Check Fails

**Problem**: Deployment fails with "Health check timeout"

**Solutions**:

1. **Increase timeout**:
   ```toml
   [deploy]
   healthcheckTimeout = 180
   ```

2. **Verify health endpoint** (locally first):
   ```bash
   curl http://localhost:8000/health  # Should return 200 OK
   ```

3. **Ensure app listens on `$PORT`** (Railway's dynamic port):
   ```toml
   [deploy]
   startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
   ```

4. **Check logs for startup errors**:
   ```bash
   railway logs --limit 100 | grep -i "error\|exception\|failed"
   ```

### Health Check Passes But 502 Error

**Problem**: Health check succeeds internally, but external requests return 502.

**Root Cause**: Port mismatch — Railway's Public Networking port (manually set, e.g., 8000) differs from the app's actual `$PORT` (e.g., 8080). Health checks use the internal port; external traffic routes to the configured port.

**Fix**:
1. Go to **Service Settings → Networking → Public Networking**
2. Click the domain to edit
3. Change from "Custom port" to the auto-detected port ("Railway magic" option, e.g., "8080 (python)")
4. Click "Update"

**Prevention**:
- Always let Railway auto-detect ports
- Include port in health response for debugging: `return {"status": "healthy", "port": os.getenv("PORT")}`
- Log PORT at startup: `logger.info(f"PORT: {os.getenv('PORT')}")`

---

## Deployment Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Build fails** | Build process errors | Check `railway logs --build`. Common: missing `requirements.txt`, wrong Python version, bad build command. Test locally first. |
| **App crashes after deploy** | Starts then enters restart loop | Check `railway logs --limit 200`. Verify env vars: `railway variables`. Set `restartPolicyMaxRetries = 3` to prevent infinite loops. |
| **Deployment hangs** | Stuck in "Building"/"Deploying" | Check `railway logs --build --follow`. Cancel in dashboard and push new commit to retrigger. Check https://railway.app/status |

**Common build fixes**:
```toml
# Specify Python version
[environment]
NIXPACKS_PYTHON_VERSION = "3.11"

# Use RAILPACK builder
[build]
builder = "RAILPACK"

# Set restart policy
[deploy]
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

---

## Database Issues

| Issue | Cause | Solution |
|-------|-------|---------|
| **SQLite "database is locked"** | Multiple workers | Use `--workers 1` in startCommand |
| **Data lost after redeploy** | No persistent volume | Add `[[deploy.volumeMounts]]` with `mountPath = "/app/data"` and set `DATABASE_PATH=/app/data/db.sqlite` |
| **Migrations fail** | No pre-deploy command | Use `preDeployCommand = ["python", "manage.py", "migrate"]` or create a migration HTTP endpoint |
| **Can't SSH to database** | SSH is interactive | Create HTTP admin endpoints instead (see example below) |

**Admin endpoint example** (for database access without SSH):
```python
@app.get("/api/admin/stats")
async def get_stats(secret: str):
    if secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(401)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    conn.close()
    return {"users": user_count}
```

---

## Environment Variable Issues

| Issue | Solution |
|-------|----------|
| **Variable not updating** | Variables trigger automatic redeploy (~2-3 min). Verify with `curl .../api/config` after redeploy completes. |
| **Can't set multiline variables** | Use Railway Dashboard (not CLI) for JSON/multiline values. |
| **Missing required variables** | Check with `railway variables`. Common required: `DATABASE_PATH`, `JWT_SECRET_KEY`, `ENVIRONMENT=production`. |

---

## Volume / Storage Issues

### Volume Not Mounting

**Checklist**:
1. **Config**: `[[deploy.volumeMounts]]` with `mountPath = "/app/data"` in railway.toml
2. **Dashboard**: Volume created and attached to service
3. **Env var**: `DATABASE_PATH=/app/data/db.sqlite` matches mount path
4. **Test**: Create a `/api/admin/volume-check` endpoint that verifies `os.path.exists(volume_path)`

### Volume Full

Check volume size in Railway dashboard (default: 10GB). Clean up via admin endpoint or request size increase.

---

## Network / Connectivity Issues

| Issue | Solution |
|-------|----------|
| **App URL doesn't respond** | `railway status` → check deployment. `curl .../health` → check endpoint. `railway logs` → check errors. |
| **Timeouts / slow responses** | Profile: `time curl .../health`. Check logs for slow queries. Consider adding indexes, caching, or increasing `healthcheckTimeout`. |

---

## Cron Service Issues

| Issue | Cause | Solution |
|-------|-------|---------|
| **Config file not found** | Path format wrong | Must use leading slash: `/railway.cron.toml` (not `railway.cron.toml`) |
| **Can't import modules** | Monorepo path issue | Deploy from repo root, use `cd api &&` in startCommand. Set Root Directory empty, Config File Path `/railway.cron.toml` |
| **Cron not running** | Schedule/config issue | Verify syntax at crontab.guru. Check logs: `railway service cron-name && railway logs --follow`. Verify env vars match main service. |
| **Cron runs but does nothing** | Logic/timezone issue | Check time-based logic. Railway uses UTC. Add logging to show why sync was skipped. |

**Example cron config** (repo root deployment with monorepo imports):
```toml
# railway.cron.toml at repo root
[build]
builder = "RAILPACK"

[deploy]
cronSchedule = "0 15 * * *"
startCommand = "cd api && python -m cron.task_runner"
restartPolicyType = "NEVER"
```

---

## Claude Code Specific Issues

**Interactive commands** (must use external terminal): `railway login`, `railway ssh`, `railway link`, `railway connect`

**Workarounds**: Authenticate once externally. Create HTTP endpoints for database access. Link projects once externally. Use `curl` for all production interactions.

---

## Error Messages & Solutions

| Error | Solution |
|-------|----------|
| "Project Token not found" | `export RAILWAY_TOKEN=your-project-token` |
| "Service not found" | `railway service` to re-link, or `railway --service=id logs` |
| "Invalid configuration" | Check TOML syntax: quotes, field names, indentation |
| "Build exceeded timeout" | Optimize deps, use `.railwayignore`, consider pre-built Docker image |

---

## Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| Health check fails | Increase `healthcheckTimeout` |
| Health check passes but 502 | Check Public Networking port matches app's PORT |
| Database locked | Add `--workers 1` |
| Data lost | Add volume mount |
| Build fails | Check `railway logs --build` |
| Auth fails | Use external terminal for `railway login` |
| Cron not running | Check logs with `railway service cron-service` |
| Variables not updating | Wait for redeploy (~2-3 min) |
| SSH doesn't work | Create HTTP endpoints instead |
| Deployment hangs | Cancel and push new commit |

---

**Remember**: Most issues can be diagnosed via `railway logs` and `railway status`. When in doubt, check logs first!
