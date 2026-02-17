# Railway CLI Command Reference

Comprehensive Railway CLI command reference with Claude Code compatibility notes.

## CLI Version

Check your installed version:

```bash
railway --version
```

## Authentication Commands

### `railway login`

Authenticate with Railway via browser OAuth.

**Claude Code**: ❌ **Requires external terminal** (interactive browser flow)

```bash
# Must run in external terminal
railway login
```

**Process**:
1. Opens default browser
2. Redirects to Railway OAuth
3. Stores credentials in `~/.railway/config.json`

**Alternative**: Use `RAILWAY_TOKEN` environment variable for non-interactive auth.

### `railway logout`

Remove authentication credentials.

**Claude Code**: ✅ Works

```bash
railway logout
```

### `railway whoami`

Display currently authenticated user.

**Claude Code**: ✅ Works

```bash
railway whoami
# Output: Logged in as your-email@example.com
```

---

## Project Management

### `railway init`

Create a new Railway project.

**Claude Code**: ⚠️ May require external terminal (interactive prompts)

```bash
railway init
```

**Interactive prompts**:
- Project name
- Team selection (if applicable)

### `railway link`

Link current directory to existing Railway project.

**Claude Code**: ⚠️ May require external terminal (interactive project selection)

```bash
railway link
```

**Shows list of projects** to select from.

**After linking**: Creates `.railway/` directory with project info.

### `railway unlink`

Disconnect directory from Railway project.

**Claude Code**: ✅ Works

```bash
railway unlink
```

### `railway list`

Display all projects in your account.

**Claude Code**: ✅ Works

```bash
railway list
```

### `railway open`

Open project dashboard in browser.

**Claude Code**: ✅ Works (opens external browser)

```bash
railway open
```

---

## Environment Management

### `railway environment`

Manage project environments.

**Claude Code**: ⚠️ Interactive mode may require external terminal

```bash
# List environments
railway environment

# Switch environment (may be interactive)
railway environment staging
```

**Common environments**:
- `production` - Main deployment
- `staging` - Testing environment
- `pr-123` - Pull request preview environments

---

## Variables Management

### `railway variables`

List all environment variables.

**Claude Code**: ✅ Works

```bash
# List all variables
railway variables

# Pipe to grep for filtering
railway variables | grep JWT
railway variables | grep -E "^(DATABASE|AWS|JWT)"
```

### `railway variables set`

Set an environment variable.

**Claude Code**: ✅ Works

```bash
# Single variable
railway variables set KEY=value

# With generated value
railway variables set JWT_SECRET=$(openssl rand -hex 32)

# Multiple variables (run sequentially)
railway variables set DATABASE_PATH=/app/data/db.sqlite
railway variables set ENVIRONMENT=production
railway variables set LOG_LEVEL=INFO
```

**⚠️ Important**: Setting variables triggers automatic redeployment!

### `railway variables unset`

Remove an environment variable.

**Claude Code**: ✅ Works

```bash
railway variables unset OLD_VAR
```

**Also triggers redeployment**.

---

## Deployment Commands

### `railway up`

Deploy current directory to Railway.

**Claude Code**: ✅ Works

```bash
railway up
```

**Note**: Automatic git push deployment is usually preferred over `railway up`.

**Options**:
```bash
# Deploy specific service
railway up --service=your-service-id

# Non-interactive mode (for CI/CD)
railway up --ci
```

### `railway down`

Remove most recent deployment.

**Claude Code**: ✅ Works

```bash
railway down
```

### `railway redeploy`

Redeploy existing service version.

**Claude Code**: ✅ Works

```bash
railway redeploy

# With confirmation flag
railway redeploy --yes
```

---

## Logging Commands

### `railway logs`

View deployment and application logs.

**Claude Code**: ✅ Works

```bash
# Recent logs (default: last 100 lines)
railway logs

# Specify number of lines
railway logs --limit 50
railway logs --limit 200

# Follow logs in real-time
railway logs --follow

# Build logs only
railway logs --build

# Deployment logs only
railway logs --deployment

# JSON format (for parsing)
railway logs --json

# JSON with filtering
railway logs --json | jq 'select(.level=="error")'
```

**Common patterns**:
```bash
# Recent errors
railway logs --json | jq 'select(.level=="error")' | head -20

# Search for specific text
railway logs --limit 500 | grep -i "database\|connection"

# Count errors
railway logs --json --limit 100 | jq 'select(.level=="error")' | wc -l
```

---

## Service Commands

### `railway add`

Add database or service to project.

**Claude Code**: ⚠️ Interactive prompts may require external terminal

```bash
# Add PostgreSQL
railway add postgres

# Add Redis
railway add redis

# Add MySQL
railway add mysql

# Add MongoDB
railway add mongo
```

### `railway service`

Link specific service to current directory.

**Claude Code**: ⚠️ May require external terminal

```bash
# List services
railway service

# Select specific service
railway service your-service-name
```

---

## Domain Commands

### `railway domain`

Manage custom domains.

**Claude Code**: ✅ Works (but domain configuration better done in dashboard)

```bash
# Generate Railway domain
railway domain

# Add custom domain (interactive)
railway domain add yourdomain.com
```

---

## Database Commands

### `railway connect`

Connect to database shell (psql, mongo, redis, mysql).

**Claude Code**: ❌ **Requires external terminal** (interactive shell)

```bash
# Must run in external terminal
railway connect postgres
railway connect redis
railway connect mysql
railway connect mongo
```

---

## SSH Commands

### `railway ssh`

Connect to service via SSH.

**Claude Code**: ❌ **Requires external terminal** (interactive shell)

```bash
# Must run in external terminal
railway ssh

# Execute specific command
railway ssh --service=your-service-id
```

**Common usage** (in external terminal):
```bash
railway ssh

# Inside container:
python manage.py migrate
python -c "import sqlite3; print(sqlite3.version)"
ls -la /app/data
exit
```

---

## Status Commands

### `railway status`

Display project and service information.

**Claude Code**: ✅ Works

```bash
railway status
```

**Output includes**:
- Project name and ID
- Environment
- Service status
- Latest deployment
- Domain URL

---

## Volume Commands

### `railway volume`

Manage persistent volumes.

**Claude Code**: ⚠️ Some subcommands may be interactive

```bash
# List volumes
railway volume list

# Add volume (interactive)
railway volume add -m /data

# Delete volume (interactive)
railway volume delete volume-id

# Attach volume to service
railway volume attach volume-id service-id

# Detach volume
railway volume detach volume-id
```

**Recommendation**: Configure volumes in `railway.toml` instead.

---

## Utility Commands

### `railway docs`

Open Railway documentation in browser.

**Claude Code**: ✅ Works (opens external browser)

```bash
railway docs
```

### `railway run`

Run local command with Railway environment variables injected.

**Claude Code**: ✅ Works

```bash
# Run command with Railway env vars
railway run python script.py
railway run npm test

# Start local dev server with Railway vars
railway run uvicorn main:app --reload
```

### `railway shell`

Launch subshell with Railway environment variables.

**Claude Code**: ⚠️ May not work well (subshell interaction)

```bash
# Better to run in external terminal
railway shell
```

---

## Command Compatibility Summary

| Command | Claude Code | Notes |
|---------|-------------|-------|
| `railway login` | ❌ No | Use external terminal |
| `railway logout` | ✅ Yes | |
| `railway whoami` | ✅ Yes | |
| `railway init` | ⚠️ Maybe | May need external terminal |
| `railway link` | ⚠️ Maybe | May need external terminal |
| `railway unlink` | ✅ Yes | |
| `railway list` | ✅ Yes | |
| `railway open` | ✅ Yes | Opens browser |
| `railway environment` | ⚠️ Maybe | Interactive prompts |
| `railway variables` | ✅ Yes | |
| `railway variables set` | ✅ Yes | |
| `railway up` | ✅ Yes | |
| `railway down` | ✅ Yes | |
| `railway redeploy` | ✅ Yes | |
| `railway logs` | ✅ Yes | Excellent for monitoring |
| `railway logs --json` | ✅ Yes | Perfect with jq |
| `railway add` | ⚠️ Maybe | Interactive prompts |
| `railway service` | ⚠️ Maybe | Service selection |
| `railway domain` | ⚠️ Maybe | Better via dashboard |
| `railway connect` | ❌ No | Interactive database shell |
| `railway ssh` | ❌ No | Interactive SSH session |
| `railway status` | ✅ Yes | |
| `railway volume` | ⚠️ Maybe | Some ops interactive |
| `railway docs` | ✅ Yes | Opens browser |
| `railway run` | ✅ Yes | |
| `railway shell` | ⚠️ Maybe | Subshell interaction |

**Legend**:
- ✅ Yes: Works perfectly in Claude Code terminal
- ❌ No: Requires external terminal
- ⚠️ Maybe: May work, but interactive parts need external terminal

---

## Claude Code Best Practices

### ✅ Recommended Commands

These work great in Claude Code and should be used frequently:

```bash
# Monitoring
railway logs --follow
railway logs --json | jq
railway status

# Variables
railway variables
railway variables set KEY=value

# Quick checks
railway whoami
railway list
```

### ❌ Use External Terminal For

These require external terminal (not Claude Code):

```bash
# Authentication
railway login

# Interactive shells
railway ssh
railway connect postgres

# Interactive setup
railway link  # sometimes
railway init  # sometimes
```

### 💡 Better Alternatives

Instead of these Railway commands, use these alternatives in Claude Code:

| Instead of | Use in Claude Code |
|------------|-------------------|
| `railway ssh` + database queries | `curl https://app.up.railway.app/api/stats` |
| `railway connect postgres` | Create admin API endpoints |
| `railway login` | Authenticate once externally, then reopen Claude Code |

---

## Common Command Patterns

### Deployment Verification

```bash
# Push and verify
git push origin main
railway logs --follow  # Watch deployment
curl -s https://app.up.railway.app/health | jq  # Verify health
```

### Error Investigation

```bash
# Check for errors
railway logs --json | jq 'select(.level=="error")' | head -20

# Search logs
railway logs --limit 500 | grep -i "error"

# Get error count
railway logs --json --limit 100 | jq 'select(.level=="error")' | wc -l
```

### Environment Variable Audit

```bash
# List all vars
railway variables

# Check required vars
railway variables | grep -E "^(DATABASE|JWT|AWS)"

# Verify specific var
railway variables | grep JWT_SECRET_KEY
```

### Status Dashboard (One-Liner)

```bash
# Quick status check
railway status && echo "" && curl -s https://app.up.railway.app/health | jq
```

---

## CI/CD Usage

For GitHub Actions or automated deployment:

```bash
# Set token
export RAILWAY_TOKEN=your-project-token

# Deploy non-interactively
railway up --service=service-id --ci

# Or redeploy
railway redeploy --yes
```

**Environment variables**:
- `RAILWAY_TOKEN` - Project token (preferred for CI/CD)
- `RAILWAY_API_TOKEN` - Account/team token
- `CI=true` - Auto-detected for CI environments

---

## Global Options

```bash
# Help for any command
railway help
railway logs --help

# Specify service
railway --service=my-service logs

# Version
railway --version
```

---

## Next Steps

- **Quick Reference**: [RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md)
- **Workflows**: [RAILWAY_WORKFLOWS.md](./RAILWAY_WORKFLOWS.md)
- **Troubleshooting**: [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)
- **Automation**: [RAILWAY_AUTOMATION.md](./RAILWAY_AUTOMATION.md)

---

## Resources

- Railway CLI GitHub: https://github.com/railwayapp/cli
- Railway Docs: https://docs.railway.com/guides/cli
- Your CLI Location: `~/.npm-global/bin/railway`
- Check version: `railway --version`
