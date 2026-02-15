# Railway Setup Guide

Complete guide for initial Railway CLI installation, authentication, and project setup.

## Prerequisites

- Git installed and configured
- GitHub account with repository access
- Node.js/npm installed (for CLI installation)
- Railway account (sign up at https://railway.app)

## CLI Installation

### Method 1: npm Global Install (Your Current Method)

```bash
npm install -g @railway/cli
```

This installs Railway CLI globally, making it available system-wide. Your current installation:
- Location: `~/.npm-global/bin/railway`
- Version: Run `railway --version` to check

### Method 2: Homebrew (Alternative)

```bash
brew install railway
```

### Verify Installation

```bash
railway --version
# Should output: railway 4.5.5 (or current version)

which railway
# Should show installation path
```

## Authentication Setup

### Important: Claude Code Limitation

**Railway authentication requires interactive browser login, which does NOT work in Claude Code's terminal.**

**Workflow**:
1. Open an **external bash terminal** (not Claude Code)
2. Run `railway login`
3. Complete browser authentication
4. Close and reopen Claude Code
5. Verify authentication in Claude Code with `railway whoami`

### Step-by-Step Authentication

#### 1. Login (In External Terminal)

```bash
railway login
```

This command:
- Opens your default web browser
- Redirects to Railway OAuth page
- Prompts you to authorize the CLI
- Stores credentials in `~/.railway/config.json`

#### 2. Verify Authentication (In Claude Code or any terminal)

```bash
railway whoami
```

Expected output:
```
Logged in as your-email@example.com
```

If you see your email, authentication is successful!

#### 3. View Your Projects

```bash
railway list
```

This shows all Railway projects in your account.

### Alternative: API Token Authentication (Advanced)

For CI/CD or automation, you can use Railway API tokens:

1. Generate a token in Railway dashboard:
   - Go to project settings
   - Create a "Project Token"
   - Copy the token

2. Set environment variable:
   ```bash
   export RAILWAY_TOKEN=your-project-token-here
   ```

3. Commands will now use the token instead of browser auth

**Note**: Project tokens are recommended for CI/CD. For local development, browser login is simpler.

## Adding Railway to Existing Repository

This is your primary use case - deploying an existing GitHub repo to Railway.

### Prerequisites

- Repository must be on GitHub
- Repository should be in a deployable state
- You have access to the repository

### Step 1: Navigate to Project Directory

```bash
cd ~/repos/your-project-name
```

### Step 2: Link to Railway Project

Two options:

#### Option A: Create New Railway Project

```bash
railway init
```

This:
- Creates a new Railway project
- Links your local directory to it
- Prompts for project name

#### Option B: Link to Existing Railway Project

```bash
railway link
```

This:
- Shows list of your Railway projects
- Links current directory to selected project
- Stores project ID in `.railway/` directory

**Note**: This is interactive and may not work perfectly in Claude Code. Run in external terminal if needed.

### Step 3: Connect GitHub Repository

In Railway dashboard (web):
1. Go to your project
2. Click "Add Service"
3. Select "GitHub Repo"
4. Authorize Railway to access your GitHub
5. Select your repository
6. Choose branch (typically `main`)

Railway will automatically:
- Detect your app type (Python, Node.js, etc.)
- Configure build settings
- Trigger initial deployment

### Step 4: Configure Service

Create `railway.toml` in your repository root:

```toml
[build]
builder = "RAILPACK"  # or "nixpacks" for legacy

[deploy]
startCommand = "your-start-command-here"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
```

See [RAILWAY_CONFIG_REFERENCE.md](./RAILWAY_CONFIG_REFERENCE.md) for detailed configuration options.

### Step 5: Set Environment Variables

```bash
# Set required environment variables
railway variables set DATABASE_PATH=/app/data/db.sqlite
railway variables set JWT_SECRET_KEY=your-secret-key
railway variables set ENVIRONMENT=production
```

Or use the Railway web dashboard:
1. Go to project → Variables tab
2. Add variables manually
3. Click "Deploy" to apply changes

### Step 6: Deploy

#### Automatic Deployment (Recommended)

Once GitHub is connected, Railway automatically deploys on every push to your main branch:

```bash
git add .
git commit -m "Initial Railway deployment"
git push origin main
```

Railway will:
1. Detect the push
2. Start build process (~1-2 minutes)
3. Run health checks
4. Deploy if successful

#### Manual Deployment (Alternative)

```bash
railway up
```

This deploys your current local directory directly.

### Step 7: Monitor Deployment

```bash
# Watch deployment logs
railway logs --follow

# Check status
railway status

# Verify health
curl https://your-project-production.up.railway.app/health
```

## Project Structure After Setup

After linking, your project will have:

```
your-project/
├── .railway/
│   └── (internal Railway files)
├── railway.toml          # Railway configuration
├── .gitignore           # Should include .railway/
└── (your project files)
```

Add to `.gitignore`:
```
.railway/
```

## Verifying Setup

Run these commands to confirm everything is configured:

```bash
# 1. Check authentication
railway whoami
# Expected: Your email address

# 2. Check project linking
railway status
# Expected: Project and environment info

# 3. Check environment variables
railway variables
# Expected: List of configured variables

# 4. Check recent deployments
railway logs --limit 10
# Expected: Recent log entries
```

## Multiple Projects

If you work with multiple Railway projects (like ping-tree-compare, docs-site, experiments-dashboard):

### Each repository should have:
1. Its own `.railway/` directory
2. Its own `railway.toml` config
3. Its own Railway project (in Railway dashboard)

### Switching between projects:
```bash
# Navigate to project directory
cd ~/repos-epcvip/utilities/ping-tree-compare
railway status  # Shows ping-tree-compare project

cd ~/repos-epcvip/utilities/docs-site
railway status  # Shows docs-site project
```

Railway CLI automatically uses the correct project based on the `.railway/` directory in your current working directory.

## Environments

Railway supports multiple environments (production, staging, PR previews).

### View environments:
```bash
railway environment
```

### Switch environment:
```bash
railway environment staging
```

### Common environments:
- **production**: Main deployment
- **staging**: Testing environment
- **pr-X**: Automatic PR preview environments

## Project Token Setup (CI/CD)

For automated deployments (GitHub Actions, etc.):

### 1. Create Project Token

In Railway dashboard:
1. Go to project settings
2. Navigate to "Tokens"
3. Create a "Project Token"
4. Copy the token (shown only once!)

### 2. Store Token Securely

For GitHub Actions, add as repository secret:
1. GitHub repo → Settings → Secrets
2. Add new secret: `RAILWAY_TOKEN`
3. Paste your project token

### 3. Use in CI/CD

```yaml
# .github/workflows/deploy.yml
- name: Deploy to Railway
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
  run: |
    npm install -g @railway/cli
    railway up --service=${{ env.SERVICE_ID }} --ci
```

## Next Steps

Now that Railway is set up:

1. **Configure your service**: See [RAILWAY_CONFIG_REFERENCE.md](./RAILWAY_CONFIG_REFERENCE.md)
2. **Set up deployment workflows**: See [RAILWAY_WORKFLOWS.md](./RAILWAY_WORKFLOWS.md)
3. **Learn Railway CLI commands**: See [RAILWAY_CLI_REFERENCE.md](./RAILWAY_CLI_REFERENCE.md)
4. **Understand troubleshooting**: See [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| Install CLI | `npm install -g @railway/cli` | Your method |
| Login | `railway login` | Use external terminal |
| Check auth | `railway whoami` | Works in Claude Code |
| Create project | `railway init` | Interactive |
| Link project | `railway link` | Interactive |
| View projects | `railway list` | Shows all projects |
| Check status | `railway status` | Project info |
| Set variables | `railway variables set KEY=val` | Triggers redeploy |
| Deploy | `git push origin main` | Automatic (recommended) |
| Manual deploy | `railway up` | Alternative method |

## Troubleshooting Setup Issues

### Authentication fails

**Problem**: `railway login` doesn't work
**Solution**: Must run in external terminal (not Claude Code)

### Project not linking

**Problem**: `railway link` fails or shows empty list
**Solution**:
1. Verify authentication: `railway whoami`
2. Check you have projects in Railway dashboard
3. Try creating new project: `railway init`

### Commands not found

**Problem**: `railway: command not found`
**Solution**:
```bash
# Check installation
which railway
npm list -g @railway/cli

# Reinstall if needed
npm install -g @railway/cli
```

### Deployments not triggering

**Problem**: Git push doesn't trigger deployment
**Solution**:
1. Verify GitHub connection in Railway dashboard
2. Check branch is correct (usually `main`)
3. Ensure repository has valid `railway.toml`
4. Check deployment logs in Railway dashboard

---

**Verify your setup**:
```bash
railway version    # Check CLI is installed
railway status     # Check you're linked to a project
```

You're all set up! See [RAILWAY_MCP_GUIDE.md](./RAILWAY_MCP_GUIDE.md) for using Railway through Claude Code, or [RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md) for CLI day-to-day usage.
