# Railway Helper Scripts

Automation scripts for common Railway deployment tasks. Optimized for Claude Code workflows.

## Scripts

### `deploy.sh` - Complete Deployment Workflow

Automated deployment with testing and verification.

**What it does**:
1. Runs tests (pytest)
2. Commits changes (with your message)
3. Pushes to trigger Railway deployment
4. Monitors deployment logs
5. Verifies health check

**Usage**:
```bash
# Set your project URL (or edit script)
export PROJECT_URL=https://your-app-production.up.railway.app

# Run deployment
./deploy.sh
```

**Requirements**:
- Railway CLI authenticated
- Git repository configured
- pytest installed (optional, will skip if not found)

---

### `health-check.sh` - Verify Deployment Health

Quick health verification after deployment.

**What it does**:
1. Checks `/health` endpoint
2. Counts recent errors in logs
3. Measures response time

**Usage**:
```bash
# Check default URL
./health-check.sh

# Check specific URL
./health-check.sh https://staging-app.up.railway.app
```

**Requirements**:
- Railway CLI authenticated (optional, for log checking)
- `jq` installed (for JSON parsing)

---

### `monitor.sh` - Continuous Health Monitoring

Real-time monitoring dashboard for your Railway app.

**What it does**:
1. Checks health every 60 seconds
2. Shows Railway status
3. Counts recent errors
4. Auto-refreshes display

**Usage**:
```bash
# Monitor default URL
./monitor.sh

# Monitor specific URL
./monitor.sh https://your-app.up.railway.app
```

Press `Ctrl+C` to exit.

**Requirements**:
- Railway CLI authenticated
- `jq` installed

---

### `audit-variables.sh` - Environment Variable Audit

Check that all required environment variables are set.

**What it does**:
1. Checks for required variables
2. Reports missing variables
3. Provides command to set them

**Usage**:
```bash
./audit-variables.sh
```

**Customization**:
Edit the script to add your required variables:
```bash
REQUIRED_VARS=(
  "DATABASE_PATH"
  "JWT_SECRET_KEY"
  "ENVIRONMENT"
  "YOUR_VAR_HERE"  # Add your variables
)
```

**Requirements**:
- Railway CLI authenticated

---

## Installation

### Make Scripts Executable

```bash
chmod +x deploy.sh health-check.sh monitor.sh audit-variables.sh
```

### Install Dependencies

```bash
# jq (for JSON parsing)
# macOS:
brew install jq

# Ubuntu/Debian:
sudo apt-get install jq

# Fedora:
sudo dnf install jq
```

### Copy to Project

```bash
# Copy individual script
cp ~/repos/ai-dev-templates/templates/railway/scripts/deploy.sh .

# Or copy all scripts
cp ~/repos/ai-dev-templates/templates/railway/scripts/*.sh .
```

## Customization

### Set Project URL

**Option 1**: Environment variable
```bash
export PROJECT_URL=https://your-app-production.up.railway.app
./deploy.sh
```

**Option 2**: Edit script directly
```bash
# In deploy.sh, change:
PROJECT_URL="${PROJECT_URL:-https://your-app-production.up.railway.app}"
```

### Adjust Timeouts

In `deploy.sh`:
```bash
TIMEOUT=180  # Change to desired seconds
```

In `monitor.sh`:
```bash
INTERVAL=60  # Change refresh interval
```

### Add Custom Health Checks

Example addition to `health-check.sh`:
```bash
# Check specific API endpoint
echo "Checking API endpoint..."
if curl -s -f "$PROJECT_URL/api/status" > /dev/null; then
  echo "✅ API responding"
else
  echo "❌ API not responding"
  exit 1
fi
```

## Usage with Claude Code

All scripts work perfectly in Claude Code terminal:

```bash
# Deploy from Claude Code
./deploy.sh

# Quick health check
./health-check.sh

# Monitor in background
./monitor.sh &

# Verify variables
./audit-variables.sh
```

**Note**: Scripts that require `railway` CLI work in Claude Code. Only `railway login` requires external terminal.

## Integration with CI/CD

### GitHub Actions Example

```yaml
# .github/workflows/verify-deployment.yml
name: Verify Deployment

on:
  push:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Verify Deployment
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
          PROJECT_URL: ${{ secrets.PROJECT_URL }}
        run: |
          # Wait for deployment
          sleep 60
          # Run health check
          ./health-check.sh
```

## Troubleshooting

### "railway: command not found"

Install Railway CLI:
```bash
npm install -g @railway/cli
railway --version
```

### "jq: command not found"

Install jq:
```bash
# macOS:
brew install jq

# Linux:
sudo apt-get install jq  # Ubuntu/Debian
sudo dnf install jq      # Fedora
```

### Scripts don't have execute permission

```bash
chmod +x *.sh
```

### Health check fails but app works

1. Verify `/health` endpoint exists
2. Check endpoint returns 200 OK
3. Test manually: `curl https://your-app.up.railway.app/health`

## Next Steps

- **Workflows**: [../docs/railway/RAILWAY_WORKFLOWS.md](../../../docs/railway/RAILWAY_WORKFLOWS.md)
- **Automation Guide**: [../docs/railway/RAILWAY_AUTOMATION.md](../../../docs/railway/RAILWAY_AUTOMATION.md)
- **Troubleshooting**: [../docs/railway/RAILWAY_TROUBLESHOOTING.md](../../../docs/railway/RAILWAY_TROUBLESHOOTING.md)

---

**Remember**: These scripts are templates. Customize them for your specific needs!
