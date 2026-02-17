# Railway Automation & Advanced Patterns

Advanced automation patterns, CI/CD integration, and scripts for Railway deployments.

## Non-Interactive CLI Usage

For automation and Claude Code workflows.

### Project Token Authentication

Railway supports project tokens for non-interactive automation:

#### Create Project Token

1. Go to Railway Dashboard → Project Settings → Tokens
2. Click "Create Token"
3. Select "Project Token"
4. Copy token (shown only once!)
5. Store securely

#### Use Project Token

```bash
# Set token in environment
export RAILWAY_TOKEN=your-project-token-here

# Commands now use token instead of browser auth
railway status
railway logs
railway variables
```

**For CI/CD**: Store token as secret (e.g., GitHub Secrets: `RAILWAY_TOKEN`).

### Auto-Detected CI Mode

Railway automatically detects CI environments:

```bash
# CI environment auto-detected when CI=true
# Only build logs streamed, exits with appropriate code

railway up --ci  # Explicit CI mode
```

---

## Git Push Deployment Pattern

Your primary automation pattern (requires no Railway CLI).

### Setup

**One-time**:
1. Connect GitHub repo to Railway (via dashboard)
2. Select branch (typically `main`)
3. Railway automatically deploys on push

### Usage

```bash
# Make changes
vim main.py

# Commit and push
git add .
git commit -m "feat: add new feature"
git push origin main

# Railway automatically:
# 1. Detects push
# 2. Starts build (~1-2 minutes)
# 3. Runs health check
# 4. Deploys if successful
```

### Monitoring Automated Deployment

```bash
# Watch logs (Claude Code)
railway logs --follow

# Check status
railway status

# Verify health
curl https://your-app-production.up.railway.app/health
```

---

## Automated Deployment Scripts

### Complete Deployment Script

```bash
#!/bin/bash
# deploy.sh - Automated deployment with verification

set -e  # Exit on error

PROJECT_URL="https://your-app-production.up.railway.app"
TIMEOUT=180  # 3 minutes

echo "=== Railway Deployment Script ==="

# 1. Run tests
echo "Running tests..."
if ! pytest tests/ -v; then
  echo "❌ Tests failed! Aborting deployment."
  exit 1
fi

# 2. Commit changes
echo "Committing changes..."
if [[ -z $(git status -s) ]]; then
  echo "No changes to commit."
  exit 0
fi

read -p "Commit message: " msg
git add .
git commit -m "$msg"

# 3. Push to trigger deployment
echo "Pushing to GitHub..."
git push origin main

# 4. Monitor deployment
echo "Monitoring deployment..."
railway logs --follow &
LOG_PID=$!

# 5. Wait for deployment
echo "Waiting for deployment to complete..."
sleep $TIMEOUT

# 6. Verify health
echo "Verifying deployment..."
health=$(curl -s $PROJECT_URL/health | jq -r '.status // "unknown"')

if [ "$health" = "healthy" ]; then
  echo "✅ Deployment successful!"
  kill $LOG_PID 2>/dev/null || true
  exit 0
else
  echo "❌ Deployment failed! Health check returned: $health"
  echo "Check logs: railway logs --limit 100"
  kill $LOG_PID 2>/dev/null || true
  exit 1
fi
```

**Usage**:
```bash
chmod +x deploy.sh
./deploy.sh
```

### Quick Deploy Script

```bash
#!/bin/bash
# quick-deploy.sh - Fast commit and deploy

set -e

if [[ -z "$1" ]]; then
  echo "Usage: ./quick-deploy.sh \"commit message\""
  exit 1
fi

git add .
git commit -m "$1"
git push origin main

echo "Deployment triggered. Monitor with: railway logs --follow"
```

**Usage**:
```bash
./quick-deploy.sh "fix: resolve database locking issue"
```

---

## Health Check Automation

### Health Check Script

```bash
#!/bin/bash
# health-check.sh - Verify deployment health

PROJECT_URL="${1:-https://your-app-production.up.railway.app}"

echo "Checking health for: $PROJECT_URL"

# Health check
health=$(curl -s $PROJECT_URL/health | jq -r '.status // "unknown"')

if [ "$health" = "healthy" ]; then
  echo "✅ Health: $health"
else
  echo "❌ Health: $health"
  exit 1
fi

# Check for recent errors
error_count=$(railway logs --json --limit 100 | jq 'select(.level=="error")' | wc -l)
echo "Recent errors: $error_count"

if [ "$error_count" -gt 10 ]; then
  echo "⚠️  High error count!"
  exit 1
fi

echo "✅ All checks passed"
```

**Usage**:
```bash
chmod +x health-check.sh
./health-check.sh
# Or specify URL:
./health-check.sh https://staging-app.up.railway.app
```

### Continuous Health Monitoring

```bash
#!/bin/bash
# monitor.sh - Continuous health monitoring

PROJECT_URL="${1:-https://your-app-production.up.railway.app}"
INTERVAL=60  # Check every 60 seconds

while true; do
  clear
  echo "=== Railway Health Monitor ==="
  echo "Time: $(date)"
  echo "URL: $PROJECT_URL"
  echo ""

  # Health check
  health=$(curl -s $PROJECT_URL/health 2>/dev/null | jq -r '.status // "unknown"')
  echo "Health: $health"

  # Railway status
  echo ""
  echo "=== Railway Status ==="
  railway status

  # Recent errors
  echo ""
  echo "=== Recent Errors ==="
  error_count=$(railway logs --json --limit 100 | jq 'select(.level=="error")' 2>/dev/null | wc -l)
  echo "Errors in last 100 logs: $error_count"

  sleep $INTERVAL
done
```

**Usage**:
```bash
chmod +x monitor.sh
./monitor.sh
```

---

## Environment Variable Management

### Bulk Variable Setting

```bash
#!/bin/bash
# set-variables.sh - Set multiple variables from file

set -e

if [[ ! -f ".env.production" ]]; then
  echo "Error: .env.production file not found"
  exit 1
fi

echo "Setting variables from .env.production..."

while IFS='=' read -r key value; do
  # Skip comments and empty lines
  [[ "$key" =~ ^#.*  ]] && continue
  [[ -z "$key" ]] && continue

  echo "Setting: $key"
  railway variables set "$key=$value"
done < .env.production

echo "✅ All variables set"
echo "Note: This triggered redeployment. Monitor with: railway logs --follow"
```

**.env.production** format:
```
DATABASE_PATH=/app/data/db.sqlite
JWT_SECRET_KEY=your-secret-here
ENVIRONMENT=production
LOG_LEVEL=INFO
```

**Usage**:
```bash
chmod +x set-variables.sh
./set-variables.sh
```

**⚠️ Warning**: This triggers one redeployment per variable! For many variables, use Railway dashboard instead.

### Variable Audit Script

```bash
#!/bin/bash
# audit-variables.sh - Check required variables are set

REQUIRED_VARS=(
  "DATABASE_PATH"
  "JWT_SECRET_KEY"
  "ENVIRONMENT"
)

echo "=== Railway Variable Audit ==="

missing=0

for var in "${REQUIRED_VARS[@]}"; do
  if railway variables | grep -q "^$var="; then
    echo "✅ $var"
  else
    echo "❌ $var (MISSING)"
    missing=$((missing + 1))
  fi
done

if [ $missing -gt 0 ]; then
  echo ""
  echo "❌ $missing required variables missing"
  exit 1
else
  echo ""
  echo "✅ All required variables set"
fi
```

**Usage**:
```bash
chmod +x audit-variables.sh
./audit-variables.sh
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          railway up --service=${{ secrets.SERVICE_ID }} --ci

      - name: Verify Deployment
        run: |
          sleep 60
          curl -f https://your-app-production.up.railway.app/health
```

**Setup**:
1. Create project token in Railway dashboard
2. Add to GitHub Secrets as `RAILWAY_TOKEN`
3. Add service ID as `SERVICE_ID`

### GitLab CI

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  image: node:18
  only:
    - main
  script:
    - npm install -g @railway/cli
    - railway up --service=$SERVICE_ID --ci
  variables:
    RAILWAY_TOKEN: $RAILWAY_TOKEN
```

### Simple Git Hook (Pre-Push)

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "Running pre-push checks..."

# Run tests
if ! pytest tests/ -v; then
  echo "❌ Tests failed! Push aborted."
  exit 1
fi

# Check for secrets
if grep -r "API_KEY.*=" --include="*.py" --include="*.js" .; then
  echo "⚠️  Warning: Potential hardcoded API keys found"
  read -p "Continue anyway? (y/N): " confirm
  [[ "$confirm" != "y" ]] && exit 1
fi

echo "✅ Pre-push checks passed"
```

**Setup**:
```bash
chmod +x .git/hooks/pre-push
```

---

## Automated Testing Scripts

### Pre-Deployment Test Script

```bash
#!/bin/bash
# test-before-deploy.sh - Run all checks before deployment

set -e

echo "=== Pre-Deployment Tests ==="

# Unit tests
echo "Running unit tests..."
pytest tests/ -v

# Lint checks
echo "Running linter..."
ruff check . || echo "⚠️  Linting issues found"

# Security scan (if installed)
if command -v safety &> /dev/null; then
  echo "Running security scan..."
  safety check
fi

# Check for secrets
echo "Checking for hardcoded secrets..."
if grep -rE "(API_KEY|SECRET|PASSWORD).*=" --include="*.py" --include="*.js" . | grep -v ".env"; then
  echo "⚠️  Potential secrets found in code"
  exit 1
fi

# Local health check
echo "Testing local health endpoint..."
if curl -f http://localhost:8000/health 2>/dev/null; then
  echo "✅ Local health check passed"
else
  echo "⚠️  Local server not running (skipping)"
fi

echo ""
echo "✅ All pre-deployment tests passed"
```

**Usage**:
```bash
# Run before deploy
./test-before-deploy.sh && git push origin main
```

### Post-Deployment Verification

```bash
#!/bin/bash
# verify-deployment.sh - Post-deployment checks

PROJECT_URL="${1:-https://your-app-production.up.railway.app}"

echo "=== Post-Deployment Verification ==="

# Wait for deployment
echo "Waiting for deployment to stabilize..."
sleep 30

# Health check
echo "Checking health..."
health=$(curl -s $PROJECT_URL/health | jq -r '.status')
[[ "$health" != "healthy" ]] && echo "❌ Health check failed" && exit 1
echo "✅ Health check passed"

# Test key endpoints
echo "Testing key endpoints..."
endpoints=(
  "/health"
  "/api/status"
)

for endpoint in "${endpoints[@]}"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" $PROJECT_URL$endpoint)
  if [ "$status" = "200" ]; then
    echo "✅ $endpoint: $status"
  else
    echo "❌ $endpoint: $status"
    exit 1
  fi
done

# Check logs for errors
echo "Checking logs for errors..."
error_count=$(railway logs --json --limit 100 | jq 'select(.level=="error")' | wc -l)
if [ "$error_count" -gt 5 ]; then
  echo "⚠️  High error count: $error_count"
  exit 1
fi
echo "✅ Error count acceptable: $error_count"

echo ""
echo "✅ All verification checks passed"
```

**Usage**:
```bash
# After git push
./verify-deployment.sh
```

---

## Automated Rollback

### Rollback Script

```bash
#!/bin/bash
# rollback.sh - Emergency rollback to previous deployment

set -e

echo "=== Emergency Rollback ==="

# Confirm
read -p "Are you sure you want to rollback? (yes/NO): " confirm
[[ "$confirm" != "yes" ]] && echo "Aborted" && exit 0

echo "Rolling back to previous commit..."
git revert HEAD --no-edit
git push origin main

echo "Monitoring rollback deployment..."
railway logs --follow &
LOG_PID=$!

sleep 120  # Wait for deployment

# Verify rollback
echo "Verifying rollback..."
health=$(curl -s https://your-app.up.railway.app/health | jq -r '.status')

if [ "$health" = "healthy" ]; then
  echo "✅ Rollback successful"
  kill $LOG_PID 2>/dev/null || true
else
  echo "❌ Rollback verification failed"
  echo "Manual intervention required!"
  kill $LOG_PID 2>/dev/null || true
  exit 1
fi
```

**Usage**:
```bash
./rollback.sh
```

---

## Cron Service Automation

### Cron Service Deployment Script

```bash
#!/bin/bash
# deploy-cron.sh - Deploy cron service separately

set -e

echo "=== Deploying Cron Service ==="

# Ensure we're on cron service
railway service your-app-cron

# Sync environment variables from main service
echo "Syncing environment variables..."
# (Variables must be set manually or via script)

# Trigger deployment
git push origin main

echo "Monitoring cron service deployment..."
railway logs --follow
```

### Cron Health Check Script

```bash
#!/bin/bash
# check-cron.sh - Verify cron service is running

echo "=== Cron Service Health Check ==="

# Switch to cron service
railway service your-app-cron

# Check recent executions
echo "Recent executions:"
railway logs --limit 20 | grep -i "running\|complete\|error"

# Count recent runs
run_count=$(railway logs --limit 100 | grep -c "Running sync" || echo "0")
echo ""
echo "Executions in last 100 logs: $run_count"

# Check for errors
error_count=$(railway logs --json --limit 100 | jq 'select(.level=="error")' | wc -l)
echo "Errors in last 100 logs: $error_count"

if [ "$error_count" -gt 10 ]; then
  echo "⚠️  High error rate in cron service"
  exit 1
fi

echo "✅ Cron service appears healthy"
```

---

## Database Automation

### Automated Backup Script

```bash
#!/bin/bash
# backup-database.sh - Backup production database

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sqlite"

mkdir -p $BACKUP_DIR

echo "=== Database Backup ==="

# Create backup endpoint in your app:
echo "Downloading database backup..."
curl -s https://your-app.up.railway.app/api/admin/backup \
  -H "Authorization: Bearer $ADMIN_SECRET" \
  -o $BACKUP_FILE

if [ -f "$BACKUP_FILE" ] && [ -s "$BACKUP_FILE" ]; then
  echo "✅ Backup saved: $BACKUP_FILE"

  # Keep only last 7 days
  find $BACKUP_DIR -name "backup_*.sqlite" -mtime +7 -delete
  echo "Old backups cleaned up"
else
  echo "❌ Backup failed"
  exit 1
fi
```

**Requires backup endpoint**:
```python
@app.get("/api/admin/backup")
async def backup_database(authorization: str = Header(None)):
    if not verify_admin_token(authorization):
        raise HTTPException(401)

    return FileResponse(
        DATABASE_PATH,
        media_type="application/x-sqlite3",
        filename=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite"
    )
```

---

## Monitoring Automation

### Automated Status Report

```bash
#!/bin/bash
# status-report.sh - Generate status report

echo "=== Railway Status Report ==="
echo "Generated: $(date)"
echo ""

# Railway status
echo "--- Service Status ---"
railway status

# Health check
echo ""
echo "--- Health Check ---"
curl -s https://your-app-production.up.railway.app/health | jq

# Environment variables
echo ""
echo "--- Environment Variables ---"
railway variables | grep -E "DATABASE|ENVIRONMENT" | wc -l
echo "variables configured"

# Recent deployments
echo ""
echo "--- Recent Activity ---"
railway logs --limit 10 | grep -i "deployed\|started"

# Error summary
echo ""
echo "--- Error Summary (last 24 hours) ---"
error_count=$(railway logs --json --limit 1000 | jq 'select(.level=="error")' | wc -l)
echo "Total errors: $error_count"

# Performance
echo ""
echo "--- Performance ---"
response_time=$(time curl -s https://your-app-production.up.railway.app/health 2>&1 | grep real | awk '{print $2}')
echo "Health endpoint response: $response_time"
```

---

## Next Steps

- **Templates**: See `templates/railway/scripts/` for ready-to-use scripts
- **Workflows**: [RAILWAY_WORKFLOWS.md](./RAILWAY_WORKFLOWS.md)
- **Troubleshooting**: [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)

---

**Remember**: Automation is about reliability, not complexity. Start simple, automate incrementally.
