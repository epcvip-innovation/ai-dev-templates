# Railway Troubleshooting Guide

Common issues and solutions based on your production deployments and Claude Code workflows.

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

**Your Setup**: `~/.npm-global/bin/railway`

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

## Deployment Issues

### Health Check Fails

**Problem**: Deployment fails with "Health check timeout"

**Symptoms**:
- `railway logs` shows app starting
- Deployment marked as failed
- Health check endpoint not responding

**Solutions**:

#### 1. Increase Timeout
```toml
[deploy]
healthcheckTimeout = 180  # Increase from 60 or 120
```

#### 2. Verify Health Endpoint
```bash
# Check locally first
curl http://localhost:8000/health

# Should return 200 OK
```

**Example health endpoint** (FastAPI):
```python
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

#### 3. Check App is Listening on Correct Port
```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

**Critical**: Must use `--port $PORT` (Railway's dynamic port).

#### 4. Check Logs for Startup Errors
```bash
railway logs --limit 100 | grep -i "error\|exception\|failed"
```

### Port Mismatch: Health Check Passes But External Requests Fail

**Problem**: Health check passes (200 OK in deploy logs), but external requests return "Application failed to respond" (502 error).

**Symptoms**:
- Deploy logs show: `Healthcheck succeeded!`
- App logs show: `PORT environment variable: 8080`
- App logs show: `<<< RESPONSE: 200` for health check
- BUT: `curl https://your-app.up.railway.app/health` returns 502

**Root Cause**: Port mismatch between:
- **Public Networking port** (manually configured in Railway UI, e.g., 8000)
- **App's actual port** (Railway's injected `$PORT`, e.g., 8080)

Railway's edge proxy routes external traffic to the configured Public Networking port, but the app is listening on a different port.

**How This Happens**:
1. When you first set up a service, you might manually enter a port (e.g., 8000)
2. Later, Railway's "Railway magic ✨" auto-detects the correct port (e.g., 8080)
3. The manual override takes precedence, causing the mismatch
4. Health checks work because Railway checks internally on the correct port
5. External requests fail because edge routes to the wrong port

**Solution**:

#### 1. Check Public Networking Port
Go to **Service Settings → Networking → Public Networking**

Look for the port shown under your domain (e.g., "Port 8000 · Metal Edge")

#### 2. Switch to Auto-Detected Port
1. Click the domain to edit it
2. Click the dropdown that shows "Custom port"
3. Look for "A port was detected by Railway magic ✨" with a port like "8080 (python)"
4. **Select the auto-detected port** instead of custom port
5. Click "Update"

#### 3. Verify Fix
```bash
curl https://your-app.up.railway.app/health
# Should now return: {"status":"healthy","port":"8080",...}
```

**Prevention - Best Practices**:

1. **Always let Railway auto-detect ports** - Don't manually enter a port unless necessary
2. **Include port in health response** - Makes debugging easier:
   ```python
   @app.get("/health")
   async def health():
       return {
           "status": "healthy",
           "port": os.getenv("PORT", "unknown")
       }
   ```
3. **Log PORT at startup** - Helps identify mismatches:
   ```python
   logger.info(f"PORT environment variable: {os.getenv('PORT', 'NOT SET')}")
   ```
4. **Check after setting up new services** - Verify the auto-detected port is being used

**CLI Detection** (requires service linking):
```bash
# Link service first (interactive - use external terminal)
railway service

# Check domain configuration
railway domain --json
```

### Build Fails

**Problem**: Build process fails

**Solutions**:

#### 1. Check Build Logs
```bash
railway logs --build
```

#### 2. Common Build Issues

**Missing dependencies**:
```bash
# Python: Ensure requirements.txt exists and is up-to-date
pip freeze > requirements.txt

# Node.js: Ensure package.json exists
npm install
```

**Wrong Python version**:
```toml
[build]
builder = "RAILPACK"

# Or specify explicitly (NIXPACKS)
[environment]
NIXPACKS_PYTHON_VERSION = "3.11"
```

**Build command fails**:
```toml
[build]
buildCommand = "npm run build"  # Verify this command works locally
```

#### 3. Test Build Locally
```bash
# Python
python -m pip install -r requirements.txt
python -c "import main; print('OK')"

# Node.js
npm install
npm run build
```

### App Crashes Immediately After Deploy

**Problem**: Service starts then crashes

**Symptoms**:
- Deployment succeeds
- App crashes seconds/minutes later
- Constant restart loop

**Solutions**:

#### 1. Check Application Logs
```bash
railway logs --limit 200
```

Look for:
- Exception/error messages
- Import errors
- Database connection failures
- Missing environment variables

#### 2. Verify Environment Variables
```bash
# List all variables
railway variables

# Check for required vars
railway variables | grep -E "DATABASE|JWT|API_KEY"
```

#### 3. Set Restart Policy
```toml
[deploy]
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

Prevents infinite restart loops.

#### 4. Check Database Path
```bash
# For SQLite with volume
railway variables | grep DATABASE_PATH
# Should show: DATABASE_PATH=/app/data/db.sqlite

# Verify volume is mounted
```

**Your railway.toml** should have:
```toml
[[deploy.volumeMounts]]
mountPath = "/app/data"
```

### Deployment Hangs / Never Completes

**Problem**: Deployment stuck in "Building" or "Deploying" state

**Solutions**:

#### 1. Check for Long-Running Build
```bash
railway logs --build --follow
```

#### 2. Cancel and Retry
```bash
# Cancel current deployment (in Railway dashboard)
# Or push new commit to trigger fresh deploy
git commit --allow-empty -m "retrigger deploy"
git push origin main
```

#### 3. Check Railway Status
Visit https://railway.app/status

---

## Database Issues

### SQLite Database Locked

**Problem**: "database is locked" errors in logs

**Solution**: **Must use single worker**
```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"
```

**Why**: Multiple workers cause simultaneous write attempts to SQLite.

**Your Pattern**: ping-tree-compare uses `--workers 1` (correct).

### Database Data Lost After Redeploy

**Problem**: Data disappears after deployment

**Solution**: **Must use persistent volume**
```toml
[[deploy.volumeMounts]]
mountPath = "/app/data"
```

**And** set database path:
```bash
railway variables set DATABASE_PATH=/app/data/your_db.sqlite
```

**Without volume**: Data is stored in ephemeral container storage and lost on redeploy.

### Database Migrations Fail

**Problem**: Migration errors during deployment

**Solutions**:

#### 1. Use Pre-Deploy Command
```toml
[deploy]
preDeployCommand = ["python", "manage.py", "migrate"]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

#### 2. Or Run Manually via SSH (External Terminal)
```bash
# In external terminal:
railway ssh

# Inside container:
python manage.py migrate
exit
```

#### 3. Or Create Migration Endpoint (Claude Code Friendly)
```python
@app.post("/api/admin/migrate")
async def run_migration(secret: str):
    if secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(401)

    run_migrations()
    return {"status": "complete"}
```

Then trigger:
```bash
curl -X POST https://your-app.up.railway.app/api/admin/migrate \
  -H "Content-Type: application/json" \
  -d '{"secret": "your-admin-secret"}'
```

### Can't Access Database via SSH

**Problem**: `railway ssh` doesn't work in Claude Code

**Solution**: **Create HTTP endpoints for database queries**

Instead of:
```bash
# ❌ Doesn't work in Claude Code
railway ssh
sqlite3 /app/data/db.sqlite "SELECT COUNT(*) FROM users"
```

Do this:
```python
# ✅ Works in Claude Code
@app.get("/api/admin/stats")
async def get_stats():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    conn.close()
    return {"users": user_count}
```

Then:
```bash
curl https://your-app.up.railway.app/api/admin/stats | jq
```

---

## Environment Variable Issues

### Variable Not Updating

**Problem**: Changed variable but app still uses old value

**Solution**: **Variables trigger automatic redeploy**
```bash
# Set variable
railway variables set MY_VAR=new_value

# Watch redeploy
railway logs --follow

# Verify new value (wait for redeploy to complete)
curl https://your-app.up.railway.app/api/config | jq
```

**Note**: Redeploy takes ~2-3 minutes.

### Can't Set Multiline Variables via CLI

**Problem**: `railway variables set` doesn't handle JSON/multiline

**Solution**: **Use Railway Dashboard**
1. Go to Railway Dashboard → Project → Variables
2. Click "Add Variable"
3. Paste multiline value (e.g., JSON credentials)
4. Save (triggers redeploy)

**Example variables needing dashboard**:
- `GOOGLE_CREDENTIALS_JSON`
- SSH private keys
- Multi-line configuration files

### Missing Required Variables

**Problem**: App fails with "KeyError" or "environment variable not found"

**Solution**:
```bash
# Check what's set
railway variables

# Set missing variables
railway variables set DATABASE_PATH=/app/data/db.sqlite
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)
```

**Common required variables**:
- `DATABASE_PATH`
- `JWT_SECRET_KEY`
- `ENVIRONMENT=production`
- API keys and credentials

---

## Volume / Storage Issues

### Volume Not Mounting

**Problem**: Files not persisting or volume path doesn't exist

**Solution**:

#### 1. Verify Volume Configuration
```toml
[[deploy.volumeMounts]]
mountPath = "/app/data"
```

#### 2. Check Volume Exists (Railway Dashboard)
- Go to project → Volumes
- Verify volume is created and attached to service

#### 3. Verify App Uses Correct Path
```bash
# Environment variable should match mount path
railway variables | grep DATABASE_PATH
# Should show: DATABASE_PATH=/app/data/db.sqlite
```

#### 4. Test Volume Access (via HTTP endpoint)
```python
@app.get("/api/admin/volume-check")
async def check_volume():
    import os
    volume_path = "/app/data"

    exists = os.path.exists(volume_path)
    writable = os.access(volume_path, os.W_OK) if exists else False
    files = os.listdir(volume_path) if exists else []

    return {
        "path": volume_path,
        "exists": exists,
        "writable": writable,
        "files": files
    }
```

### Volume Full / Out of Space

**Problem**: "No space left on device" errors

**Solution**:
```bash
# Check volume size in Railway dashboard
# Default: 10GB

# Clean up unnecessary files via SSH or endpoint
# Or request volume size increase in Railway dashboard
```

---

## Network / Connectivity Issues

### Can't Access Production App

**Problem**: App URL doesn't respond

**Solutions**:

#### 1. Verify Deployment Status
```bash
railway status
```

#### 2. Check Health Endpoint
```bash
curl https://your-app-production.up.railway.app/health
```

#### 3. Check Logs for Errors
```bash
railway logs --limit 100 | grep -i error
```

#### 4. Verify Service is Running
```bash
railway status
# Look for: "Status: Running"
```

### Timeouts or Slow Responses

**Problem**: Requests take too long or timeout

**Solutions**:

#### 1. Check Application Performance
```bash
# Monitor response times
time curl https://your-app.up.railway.app/health

# Check logs for slow queries
railway logs | grep -i "slow\|timeout"
```

#### 2. Optimize Database Queries
- Add indexes
- Use query optimization
- Consider caching

#### 3. Check Health Check Timeout
```toml
[deploy]
healthcheckTimeout = 120  # Increase if needed
```

---

## Cron Service Issues

### Config File Not Found

**Problem**: `config file railway.cron.toml does not exist`

**Root Cause**: Railway config file path format is incorrect.

**Solutions**:

#### 1. Config File Path MUST Have Leading Slash
```
# ❌ Doesn't work
Config File Path: railway.cron.toml
Config File Path: validator-api/railway.cron.toml

# ✅ Works - leading slash required
Config File Path: /railway.cron.toml
Config File Path: /validator-api/railway.cron.toml
```

#### 2. Place Config at Repo Root for Simplicity
```
your-repo/
├── railway.cron.toml    # ✅ At root, reference as /railway.cron.toml
├── validator-api/
│   └── ...
└── core/
    └── ...
```

**Dashboard Settings**:
- Root Directory: *(leave empty)*
- Config File Path: `/railway.cron.toml`

### Cron Can't Import Modules from Other Directories

**Problem**: Cron needs modules outside its subdirectory (monorepo pattern)

**Example**: `validator-api/cron/` needs `core/pulse/` from repo root

**Solution**: Deploy from repo root, use `cd` in startCommand

```toml
# railway.cron.toml at repo root
[build]
builder = "RAILPACK"

[deploy]
cronSchedule = "0 15 * * *"
startCommand = "cd validator-api && python -m cron.pulse_poster"
restartPolicyType = "NEVER"
```

**Dashboard Settings**:
- Root Directory: *(empty - deploys from repo root)*
- Config File Path: `/railway.cron.toml`

This allows Python to import from both `core/` (repo root) and `validator-api/cron/`.

### Cron Not Running

**Problem**: Scheduled job doesn't execute

**Solutions**:

#### 1. Verify Cron Schedule
```toml
[deploy]
cronSchedule = "0,30 * * * *"  # Every 30 minutes
```

Test cron syntax: https://crontab.guru/

#### 2. Check Cron Service Logs
```bash
railway service your-app-cron
railway logs --follow
```

#### 3. Verify Environment Variables
```bash
# Switch to cron service
railway service your-app-cron
railway variables

# Should have same vars as main service
```

#### 4. Test Cron Script Locally
```bash
python -m utils.sync_runner --type smart
```

### Cron Runs But Does Nothing

**Problem**: Cron executes but no work is done

**Solution**: **Check smart sync logic**

Your tiller-bridge pattern:
```python
def should_sync_now():
    """Determine if sync should run based on time"""
    hour = datetime.now().hour
    # Run at market hours only
    return hour in [9, 13, 16, 2]
```

**Verify**:
1. Logic is correct
2. Timezone is correct (Railway uses UTC)
3. Logs show why sync was skipped

---

## Claude Code Specific Issues

### Command Works in Terminal But Not Claude Code

**Problem**: Command succeeds in external terminal but fails in Claude Code

**Solution**: **Likely an interactive command**

Commands requiring external terminal:
- `railway login` - Interactive browser auth
- `railway ssh` - Interactive shell
- `railway link` - Interactive project selection
- `railway connect` - Interactive database shell

**Use alternatives**:
- Authentication: Do once externally, reopen Claude Code
- Database queries: Create HTTP endpoints
- Project linking: Do once externally

### Can't Monitor SSH Session

**Problem**: Need to run commands in production

**Solution**: **Create admin API endpoints instead**

Example:
```python
@app.post("/api/admin/clear-cache")
async def clear_cache(secret: str):
    if secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(401)

    # Clear cache logic
    cache.clear()
    return {"status": "cache cleared"}
```

Then call via HTTP (Claude Code friendly):
```bash
curl -X POST https://your-app.up.railway.app/api/admin/clear-cache \
  -H "Content-Type: application/json" \
  -d '{"secret": "your-secret"}'
```

---

## Error Messages & Solutions

### "Project Token not found"

**Problem**: CI/CD failing with token error

**Solution**:
```bash
# Set project token
export RAILWAY_TOKEN=your-project-token

# Verify
railway whoami
```

### "Service not found"

**Problem**: Railway can't find service

**Solution**:
```bash
# Link to correct service
railway service

# Or specify service explicitly
railway --service=your-service-id logs
```

### "Invalid configuration"

**Problem**: railway.toml syntax error

**Solution**:
```bash
# Check TOML syntax
# Common issues:
# - Missing quotes around strings
# - Incorrect indentation
# - Typos in field names

# Verify against working config:
cat ~/repos/tiller-bridge/railway.toml
```

### "Build exceeded timeout"

**Problem**: Build takes too long

**Solution**:
1. Optimize dependencies (remove unused packages)
2. Use `.railwayignore` to exclude large files
3. Consider pre-built Docker image

---

## Debugging Workflows

### Quick Deployment Verification

```bash
# 1. Check deployment completed
railway status

# 2. Verify health
curl https://your-app.up.railway.app/health

# 3. Check for errors
railway logs --json --limit 100 | jq 'select(.level=="error")'

# 4. Test key endpoints
curl https://your-app.up.railway.app/api/status
```

### Systematic Error Investigation

```bash
# Step 1: When did error start?
railway logs --limit 1000 | grep -i "error" | head -1

# Step 2: What type of error?
railway logs --limit 500 | grep -i "error" | sort | uniq -c

# Step 3: Check related systems
railway variables | grep DATABASE
curl https://your-app.up.railway.app/health

# Step 4: Check Railway status
# Visit: https://railway.app/status
```

### Performance Debugging

```bash
# Response time check
time curl -s https://your-app.up.railway.app/health

# Log analysis for slow operations
railway logs | grep -i "slow\|took\|duration" | tail -20

# Error rate
error_count=$(railway logs --json --limit 500 | jq 'select(.level=="error")' | wc -l)
echo "Errors in last 500 logs: $error_count"
```

---

## Getting Help

### Check Railway Status

https://railway.app/status

### Your Working Examples

Reference your production deployments:
- **tiller-bridge**: https://tiller-bridge-production.up.railway.app
- **ping-tree-compare**: https://ping-tree-compare-production.up.railway.app

### Documentation

- **Railway Docs**: https://docs.railway.com
- **Your Guides**: See `dev-setup/docs/railway/`

---

## Quick Reference: Common Fixes

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
| Can't find command | Check `which railway` and reinstall if needed |

---

**Remember**: Most issues can be diagnosed via `railway logs` and `railway status`. When in doubt, check logs first!
