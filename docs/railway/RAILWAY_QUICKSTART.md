# Railway Quickstart - Claude Code Optimized

Quick reference for deploying existing projects to Railway, optimized for Claude Code workflows.

## Your Current Setup

- **Railway CLI**: Installed via npm at `~/.npm-global/bin/railway`
- **Authentication**: your-email@example.com
- **Installation method**: `npm install -g @railway/cli`

Verify your setup:
```bash
railway --version
railway whoami
```

> **Prefer MCP?** If you use Claude Code, the Railway MCP server lets you manage deployments without the CLI. See [RAILWAY_MCP_GUIDE.md](./RAILWAY_MCP_GUIDE.md).

## Claude Code Compatibility

### ✅ Works in Claude Code Terminal

These commands work perfectly in Claude Code's integrated terminal:

```bash
railway status              # Check project/deployment status
railway logs               # Stream application logs
railway logs --follow      # Real-time log monitoring
railway logs --json        # Machine-readable JSON output
railway variables          # List environment variables
railway variables set KEY=value  # Set variables
```

### ❌ Requires External Terminal

These require an **external bash terminal** (cannot run in Claude Code):

```bash
railway login   # Interactive browser authentication
railway ssh     # Interactive shell into production container
```

**Workflow**: Authenticate in external terminal → Close and reopen Claude Code → Continue with deployment.

## Primary Deployment Workflow

Your main workflow uses **git push** for automatic deployment (no Railway CLI needed!):

```bash
# 1. Test locally
pytest tests/ -v
curl http://localhost:8000/health

# 2. Commit and push (triggers automatic Railway deployment)
git add .
git commit -m "Feature: description"
git push origin main

# 3. Monitor deployment in Claude Code
railway logs --follow

# 4. Verify deployment via HTTP
curl -s https://your-app-production.up.railway.app/health | jq '.status'
```

## Quick Commands

### Check Deployment Status
```bash
# Railway status
railway status

# Or use HTTP health check (Claude Code friendly)
curl -s https://your-app.up.railway.app/health | jq
```

### Monitor Logs
```bash
# Stream recent logs
railway logs --limit 100

# Follow in real-time
railway logs --follow

# Check for errors
railway logs --json | jq 'select(.level=="error")' | head -20

# Build logs specifically
railway logs --build
```

### Environment Variables
```bash
# List all variables
railway variables

# Filter for specific vars
railway variables | grep JWT
railway variables | grep -E "^(DATABASE|JWT|AWS)"

# Set a variable (triggers automatic redeploy)
railway variables set DATABASE_PATH=/app/data/db.sqlite
railway variables set JWT_SECRET_KEY=your-secret-here
```

### Health Checks (HTTP-based)
```bash
# Production health check
curl -s https://your-app-production.up.railway.app/health

# With JSON parsing
curl -s https://your-app-production.up.railway.app/health | jq '.status'

# Check multiple endpoints
curl -s https://your-app-production.up.railway.app/api/status
curl -s https://your-app-production.up.railway.app/api/auth/me
```

## Common Patterns

### Deploy and Verify
```bash
# Deploy
git push origin main

# Wait for deployment (~2-3 minutes)
railway logs --follow

# Verify (Ctrl+C to exit logs first)
curl -s https://your-app.up.railway.app/health | jq
railway logs --limit 50 | grep -i error
```

### Update Environment Variables
```bash
# Set variable
railway variables set NEW_VAR=value

# Verify it was set
railway variables | grep NEW_VAR

# Note: Setting variables triggers automatic redeploy
# Monitor the redeploy
railway logs --follow
```

### Error Investigation
```bash
# Recent errors
railway logs --json | jq 'select(.level=="error")' | head -20

# Search for specific patterns
railway logs --limit 200 | grep -i "database\|connection\|timeout"

# Check last 100 lines for errors
railway logs --limit 100 | grep -i error || echo "No errors found"
```

## Key Limitations

1. **Interactive authentication doesn't work in Claude Code**
   - Must run `railway login` in external terminal
   - After authentication, reopen Claude Code to continue

2. **SSH access requires external terminal**
   - `railway ssh` doesn't work in Claude Code
   - For database operations, use HTTP API endpoints instead
   - Or run `railway ssh` in external terminal when needed

3. **Environment variable changes trigger redeployment**
   - Setting any variable causes automatic redeploy (~2-3 minutes)
   - Plan variable updates accordingly

## Best Practices for Claude Code

1. **Use HTTP endpoints instead of SSH**
   ```bash
   # Instead of: railway ssh -> python script
   # Do this: Create API endpoint and use curl
   curl -s https://app.up.railway.app/api/admin/stats
   ```

2. **Use JSON output for parsing**
   ```bash
   # Parse logs programmatically
   railway logs --json | jq '.message' | grep "error"
   ```

3. **Leverage git push for deployment**
   ```bash
   # No need for: railway up
   # Just use: git push origin main
   ```

4. **Create status endpoints for monitoring**
   ```bash
   # Instead of SSH database queries
   # Create: /api/stats endpoint that returns DB summary
   curl https://app.up.railway.app/api/stats | jq
   ```

## Next Steps

- **Full setup guide**: See [RAILWAY_SETUP_GUIDE.md](./RAILWAY_SETUP_GUIDE.md)
- **Deployment workflows**: See [RAILWAY_WORKFLOWS.md](./RAILWAY_WORKFLOWS.md)
- **Configuration reference**: See [RAILWAY_CONFIG_REFERENCE.md](./RAILWAY_CONFIG_REFERENCE.md)
- **CLI command reference**: See [RAILWAY_CLI_REFERENCE.md](./RAILWAY_CLI_REFERENCE.md)
- **Troubleshooting**: See [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)

## Quick Reference Card

| Task | Command | Claude Code? |
|------|---------|--------------|
| Check status | `railway status` | ✅ Yes |
| View logs | `railway logs --follow` | ✅ Yes |
| Set variable | `railway variables set KEY=val` | ✅ Yes |
| Health check | `curl https://app.up.railway.app/health` | ✅ Yes |
| Deploy | `git push origin main` | ✅ Yes |
| Login | `railway login` | ❌ No - use external terminal |
| SSH access | `railway ssh` | ❌ No - use external terminal |
