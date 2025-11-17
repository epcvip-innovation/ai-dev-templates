# Railway Deployment Workflows

Claude Code-optimized workflows for deploying and managing Railway applications.

## Table of Contents

1. [Initial Deployment](#initial-deployment)
2. [Day-to-Day Development](#day-to-day-development)
3. [Environment Variables Management](#environment-variables-management)
4. [Monitoring & Debugging](#monitoring--debugging)
5. [Database Operations](#database-operations)
6. [Cron Service Setup](#cron-service-setup)
7. [Emergency Procedures](#emergency-procedures)

## Initial Deployment

### Deploying an Existing Repository to Railway

**Prerequisites**:
- Railway CLI installed and authenticated
- GitHub repository with your code
- Basic `railway.toml` configuration

#### Step 1: Prepare Your Application

```bash
# Navigate to your project
cd ~/repos/your-project

# Ensure your app has required files
ls -la  # Check for railway.toml, requirements.txt/package.json, etc.

# Test locally
# Python:
source venv/bin/activate && python main.py
# Node:
npm install && npm start

# Verify health endpoint works
curl http://localhost:8000/health  # or your local port
```

#### Step 2: Create Railway Configuration

Create `railway.toml` in your project root:

```toml
[build]
builder = "RAILPACK"  # or "nixpacks" for existing projects

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

See [RAILWAY_CONFIG_REFERENCE.md](./RAILWAY_CONFIG_REFERENCE.md) for language-specific configs.

#### Step 3: Link to Railway (One-Time Setup)

**⚠️ Note**: May require external terminal if interactive prompts appear.

```bash
# Option A: Create new Railway project
railway init

# Option B: Link to existing project
railway link
```

#### Step 4: Connect GitHub Repository

In Railway Dashboard (web):
1. Go to https://railway.app/dashboard
2. Select your project
3. Click "Add Service" → "GitHub Repo"
4. Authorize and select your repository
5. Choose branch (typically `main`)

Railway will automatically detect your app and configure build settings.

#### Step 5: Configure Environment Variables

```bash
# Set required environment variables (Claude Code friendly)
railway variables set DATABASE_PATH=/app/data/db.sqlite
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)
railway variables set ENVIRONMENT=production

# For complex/multiline variables, use Railway dashboard
# Dashboard → Project → Variables tab
```

**Note**: Setting variables triggers automatic redeployment (~2-3 minutes).

#### Step 6: Initial Deploy

**Automatic method** (recommended):
```bash
# Commit your railway.toml
git add railway.toml
git commit -m "feat: add Railway configuration"
git push origin main

# Railway automatically detects push and deploys
```

**Manual method** (alternative):
```bash
railway up
```

#### Step 7: Monitor Deployment

```bash
# Watch deployment logs in real-time (Claude Code)
railway logs --follow

# In another terminal/tab, check status
railway status

# Wait for health check to pass (~2-3 minutes)
```

#### Step 8: Verify Deployment

```bash
# Get your Railway URL from dashboard or:
railway status  # Look for "Domain" field

# Test health endpoint
curl -s https://your-app-production.up.railway.app/health | jq

# Test other endpoints
curl -s https://your-app-production.up.railway.app/api/status
curl -s https://your-app-production.up.railway.app/docs  # FastAPI docs
```

#### Step 9: Post-Deployment Checklist

```bash
# ✅ Health check passes
curl https://your-app.up.railway.app/health

# ✅ No errors in logs
railway logs --limit 100 | grep -i error

# ✅ Environment variables set
railway variables | grep -E "DATABASE|JWT|ENVIRONMENT"

# ✅ Database/volumes mounted (if applicable)
curl https://your-app.up.railway.app/api/stats

# ✅ API endpoints working
curl https://your-app.up.railway.app/api/auth/me
```

---

## Day-to-Day Development

### Standard Development Workflow

```bash
# 1. Make changes to your code
vim main.py  # or your preferred editor

# 2. Test locally
pytest tests/ -v
curl http://localhost:8000/health

# 3. Commit changes
git add .
git commit -m "feat: add new feature"

# 4. Push to trigger automatic deployment
git push origin main

# 5. Monitor deployment (Claude Code)
railway logs --follow

# 6. Verify deployment
curl https://your-app-production.up.railway.app/health

# 7. Check for errors
railway logs --json | jq 'select(.level=="error")' | head -20
```

### Quick Feature Deploy

```bash
# One-liner for quick deploys
git add . && git commit -m "fix: quick bug fix" && git push origin main

# Monitor in background
railway logs --follow &

# Or watch logs with error filtering
railway logs --follow | grep -i "error\|warning\|started"
```

### Testing Before Deploy

```bash
# Run full test suite
pytest tests/ -v --cov

# Check for common issues
python -c "import main; print('Imports OK')"

# Test health endpoint locally
curl http://localhost:8000/health | jq '.status'

# Only push if tests pass
pytest tests/ && git push origin main
```

---

## Environment Variables Management

### Viewing Variables

```bash
# List all variables
railway variables

# Filter specific variables
railway variables | grep JWT
railway variables | grep AWS
railway variables | grep -E "^(DATABASE|JWT|AWS|DOIS)"

# Check if required variables are set
required_vars=("DATABASE_PATH" "JWT_SECRET_KEY" "ENVIRONMENT")
for var in "${required_vars[@]}"; do
  railway variables | grep "^$var" || echo "❌ Missing: $var"
done
```

### Setting Variables (Claude Code)

```bash
# Single variable
railway variables set DATABASE_PATH=/app/data/db.sqlite

# Multiple variables (sequential)
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)
railway variables set ENVIRONMENT=production
railway variables set LOG_LEVEL=INFO

# Generate secure secrets
railway variables set API_SECRET=$(openssl rand -base64 32)
```

**⚠️ Important**: Setting any variable triggers automatic redeployment!

### Complex/Multiline Variables (Use Dashboard)

For JSON credentials or multiline values:

1. Go to Railway Dashboard → Project → Variables
2. Click "Add Variable"
3. Paste multiline JSON (e.g., `GOOGLE_CREDENTIALS_JSON`)
4. Click "Save"

Example values that need dashboard:
- `GOOGLE_CREDENTIALS_JSON` (JSON object)
- SSH private keys
- Multi-line configuration files

### Updating Variables Without Downtime

```bash
# 1. Check current value
railway variables | grep MY_VAR

# 2. Update variable
railway variables set MY_VAR=new_value

# 3. Monitor deployment (triggered automatically)
railway logs --follow

# 4. Verify new value is being used
curl https://your-app.up.railway.app/api/config | jq '.MY_VAR'
```

### Removing Variables

```bash
# Remove a variable
railway variables unset OLD_VAR

# This also triggers redeployment
railway logs --follow
```

---

## Monitoring & Debugging

### Real-Time Log Monitoring

```bash
# Follow logs in real-time
railway logs --follow

# Filter for specific patterns
railway logs --follow | grep -i "error\|warning"

# JSON format for parsing
railway logs --json --follow | jq '.message'
```

### Log Analysis

```bash
# Recent errors only
railway logs --json | jq 'select(.level=="error")' | head -20

# Specific time range (last 100 lines)
railway logs --limit 100

# Build logs specifically
railway logs --build

# Deployment logs
railway logs --deployment
```

### Health Check Patterns

```bash
# Simple health check
curl -s https://your-app.up.railway.app/health

# Health check with JSON parsing
curl -s https://your-app.up.railway.app/health | jq '.status'

# Automated health verification
health_status=$(curl -s https://your-app.up.railway.app/health | jq -r '.status')
if [ "$health_status" = "healthy" ]; then
  echo "✅ Application healthy"
else
  echo "❌ Application unhealthy: $health_status"
  exit 1
fi
```

### Status Monitoring

```bash
# Quick status check
railway status

# Check for recent deployments
railway logs --limit 10 | grep -i "started\|deployed"

# Comprehensive status script
echo "=== Railway Status ==="
railway status
echo ""
echo "=== Health Check ==="
curl -s https://your-app.up.railway.app/health | jq
echo ""
echo "=== Recent Errors ==="
railway logs --json --limit 100 | jq 'select(.level=="error")' | wc -l
```

### Error Investigation Workflow

```bash
# 1. Check recent errors
railway logs --json | jq 'select(.level=="error")' | head -20

# 2. Search for specific error patterns
railway logs --limit 500 | grep -i "database error\|connection refused"

# 3. Check environment variables
railway variables | grep DATABASE

# 4. Verify health endpoint
curl -s https://your-app.up.railway.app/health | jq

# 5. Check application-specific status
curl -s https://your-app.up.railway.app/api/status
```

---

## Database Operations

### SQLite with Persistent Volume (Your Pattern)

**Setup** (in railway.toml):
```toml
[[deploy.mounts]]
name = "your-volume-name"
mountPath = "/app/data"
```

**Environment variable**:
```bash
railway variables set DATABASE_PATH=/app/data/your_db.sqlite
```

### Checking Database via HTTP (Claude Code Friendly)

Instead of SSH, create API endpoints:

```python
# In your FastAPI app
@app.get("/api/stats")
async def get_stats():
    """Database statistics endpoint"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transaction_count = cursor.fetchone()[0]

    conn.close()

    return {
        "users": user_count,
        "transactions": transaction_count,
        "database_path": DATABASE_PATH
    }
```

Then query via HTTP:
```bash
curl -s https://your-app.up.railway.app/api/stats | jq
```

### Database Operations via SSH (Requires External Terminal)

**⚠️ Cannot run in Claude Code - use external terminal**

```bash
# SSH into container (external terminal)
railway ssh

# Once inside container:
python3
>>> import sqlite3
>>> conn = sqlite3.connect('/app/data/your_db.sqlite')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT COUNT(*) FROM users")
>>> print(cursor.fetchone())
>>> exit()

# Exit SSH
exit
```

### Database Migrations

**Option 1: Pre-deploy Command** (in railway.toml):
```toml
[deploy]
preDeployCommand = ["python", "manage.py", "migrate"]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

**Option 2: Manual Migration via SSH** (external terminal):
```bash
railway ssh
python manage.py migrate
exit
```

**Option 3: HTTP Endpoint** (Claude Code friendly):
```python
@app.post("/api/admin/migrate")
async def run_migration(secret: str):
    if secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(401)

    # Run migration logic
    run_migrations()
    return {"status": "migrations complete"}
```

Then trigger:
```bash
curl -X POST https://your-app.up.railway.app/api/admin/migrate \
  -H "Content-Type: application/json" \
  -d '{"secret": "your-admin-secret"}'
```

---

## Cron Service Setup

Based on tiller-bridge's working pattern.

### Step 1: Create railway.cron.toml

```toml
[build]
builder = "RAILPACK"

[deploy]
# Run every 30 minutes
cronSchedule = "*/30 * * * *"
startCommand = "python utils/sync_runner.py"

# No health check for cron jobs
# Railway will run and exit
```

### Step 2: Create Cron Script

```python
# utils/sync_runner.py
import os
import time
from datetime import datetime

def should_sync_now():
    """Determine if sync should run based on time"""
    hour = datetime.now().hour
    # Run at market hours and overnight
    return hour in [9, 13, 16, 2]  # 9:30 AM, 1 PM, 4:30 PM, 2 AM

def main():
    if should_sync_now():
        print(f"Running sync at {datetime.now()}")
        # Your sync logic here
        run_sync()
    else:
        print(f"Skipping sync at {datetime.now()}")

if __name__ == "__main__":
    main()
```

### Step 3: Add as Separate Service

In Railway Dashboard:
1. Go to project
2. Click "Add Service" → "Empty Service"
3. Name it `your-app-cron`
4. Connect to same GitHub repo
5. Set custom config path to `railway.cron.toml`

### Step 4: Set Environment Variables

```bash
# Switch to cron service
railway service your-app-cron

# Set same variables as main service
railway variables set DATABASE_PATH=/app/data/db.sqlite
railway variables set API_KEY=your-api-key
```

### Step 5: Verify Cron Execution

```bash
# Watch cron logs
railway service your-app-cron
railway logs --follow

# You should see execution every 30 minutes (or your schedule)
```

---

## Emergency Procedures

### Rollback to Previous Deployment

#### Via Railway Dashboard (Fastest)

1. Go to Railway Dashboard
2. Select project → Deployments
3. Find last working deployment
4. Click "Redeploy"
5. Monitor: `railway logs --follow`

#### Via Git Revert

```bash
# Revert last commit
git revert HEAD
git push origin main

# Monitor redeploy
railway logs --follow
```

### Emergency Variable Change

```bash
# Quickly update variable
railway variables set EMERGENCY_MODE=true

# Monitor restart
railway logs --follow

# Verify change took effect
curl https://your-app.up.railway.app/api/config | jq '.EMERGENCY_MODE'
```

### Taking Service Offline Temporarily

```bash
# Set health check to fail
railway variables set HEALTH_CHECK_DISABLED=true

# Or update railway.toml to remove health check temporarily
# Then git push
```

### Quick Log Search for Issues

```bash
# Find when error started
railway logs --limit 1000 | grep -i "error" | head -1

# Check for specific error pattern
railway logs --limit 500 | grep -i "database\|connection\|timeout"

# Get error count
railway logs --json --limit 500 | jq 'select(.level=="error")' | wc -l
```

### Emergency Contact Points

```bash
# Check health
curl https://your-app.up.railway.app/health

# Check status endpoint
curl https://your-app.up.railway.app/api/status

# Check Railway status
railway status

# Get deployment info
railway logs --limit 5 | grep -i "deployed\|started"
```

---

## Workflow Scripts

### Complete Deployment Script

```bash
#!/bin/bash
# deploy.sh - Complete deployment workflow

set -e  # Exit on error

echo "=== Railway Deployment Workflow ==="

# 1. Run tests
echo "Running tests..."
pytest tests/ -v

# 2. Commit changes
echo "Committing changes..."
git add .
read -p "Commit message: " msg
git commit -m "$msg"

# 3. Push to trigger deployment
echo "Pushing to GitHub..."
git push origin main

# 4. Monitor deployment
echo "Monitoring deployment..."
railway logs --follow &
LOG_PID=$!

# 5. Wait for health check (30 seconds)
echo "Waiting for deployment..."
sleep 30

# 6. Verify deployment
echo "Verifying deployment..."
health=$(curl -s https://your-app-production.up.railway.app/health | jq -r '.status')

if [ "$health" = "healthy" ]; then
  echo "✅ Deployment successful!"
  kill $LOG_PID
else
  echo "❌ Deployment failed! Health check returned: $health"
  exit 1
fi
```

### Monitoring Script

```bash
#!/bin/bash
# monitor.sh - Continuous monitoring

while true; do
  clear
  echo "=== Railway Monitoring Dashboard ==="
  echo "Time: $(date)"
  echo ""

  echo "=== Status ==="
  railway status
  echo ""

  echo "=== Health ==="
  curl -s https://your-app.up.railway.app/health | jq
  echo ""

  echo "=== Recent Errors ==="
  error_count=$(railway logs --json --limit 100 | jq 'select(.level=="error")' | wc -l)
  echo "Errors in last 100 logs: $error_count"

  sleep 60  # Refresh every minute
done
```

---

## Next Steps

- **CLI Reference**: See [RAILWAY_CLI_REFERENCE.md](./RAILWAY_CLI_REFERENCE.md)
- **Configuration**: See [RAILWAY_CONFIG_REFERENCE.md](./RAILWAY_CONFIG_REFERENCE.md)
- **Troubleshooting**: See [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)
- **Automation**: See [RAILWAY_AUTOMATION.md](./RAILWAY_AUTOMATION.md)
