# Railway MCP Guide

[← Back to Railway Docs](./README.md) | [Railway Overview →](./RAILWAY_OVERVIEW.md) | [CLI Reference →](./RAILWAY_CLI_REFERENCE.md)

**Last Updated**: February 2026

---

## What is Railway MCP?

Railway MCP is an official Model Context Protocol server (`@railway/mcp-server`) that gives Claude Code direct access to Railway operations. Instead of copy-pasting CLI commands and output, Claude can check statuses, read logs, set variables, and deploy — all within the conversation.

**Official Package**: [@railway/mcp-server](https://www.npmjs.com/package/@railway/mcp-server)

**Key advantages over CLI**:
- No interactive prompts — MCP tools return structured data
- Claude can chain operations (check logs → diagnose → set variable → redeploy)
- No terminal context switching
- Results stay in conversation context for analysis

---

## MCP vs CLI vs Dashboard

| Capability | MCP | CLI | Dashboard |
|------------|:---:|:---:|:---------:|
| **Check status/health** | Yes | Yes | Yes |
| **View deployment logs** | Yes (with filters) | Yes | Yes |
| **Set environment variables** | Yes | Yes | Yes |
| **Deploy from directory** | Yes | Yes | — |
| **Deploy templates** | Yes | — | Yes |
| **List services/projects** | Yes | Yes | Yes |
| **Generate domains** | Yes | Yes | Yes |
| **Create environments** | Yes | Yes | Yes |
| **Link service/environment** | Yes | Yes (interactive) | — |
| **SSH into container** | — | Yes | — |
| **Delete resources** | — | — | Yes |
| **Manage billing** | — | — | Yes |
| **Change builder** | — | — | Yes |
| **Initial authentication** | — | Yes | — |

**Rule of thumb**:
- **In a Claude Code session?** → Use MCP
- **Need auth, SSH, or interactive commands?** → Use CLI in external terminal
- **Need to delete or manage billing?** → Use Dashboard

---

## Setup

### Prerequisites

1. **Railway CLI installed and authenticated**
   ```bash
   # Check if CLI is installed
   railway version

   # If not installed
   npm install -g @railway/cli

   # Authenticate (requires external terminal)
   railway login
   ```

2. **MCP server configured in Claude Code**

### Current Configuration

The Railway MCP server is configured globally in `~/.claude.json`:

```json
{
  "mcpServers": {
    "railway": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@railway/mcp-server"],
      "env": {}
    }
  }
}
```

### Verification

Use the `check-railway-status` tool to verify everything is working:

```
Check if Railway CLI is installed and I'm logged in
```

This confirms:
- CLI is installed and on PATH
- You're authenticated
- The MCP server can communicate with Railway

---

## Complete Tool Reference

Railway MCP exposes 16 tools organized by function.

### Status & Discovery

| Tool | Description |
|------|-------------|
| `check-railway-status` | Verify CLI installation and authentication |
| `list-projects` | List all Railway projects for your account |

**Example — verify setup**:
```
Check my Railway status and list all projects
```

### Service Management

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `list-services` | List services in linked project | `workspacePath` |
| `link-service` | Link to a specific service | `workspacePath`, `serviceName` |
| `list-deployments` | List deployments with status/metadata | `workspacePath`, `service`, `environment`, `limit`, `json` |

**Example — check a project's services**:
```
List all services in /path/to/my-project
```

### Deployment

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `deploy` | Upload and deploy from directory | `workspacePath`, `service`, `environment`, `ci` |
| `deploy-template` | Search and deploy Railway templates | `workspacePath`, `searchQuery`, `templateIndex` |

**Example — deploy a service**:
```
Deploy the my-api service from /path/to/my-project
```

**Example — deploy with build log streaming**:
```
Deploy my-api with ci mode enabled so I can see build logs
```

### Environment Management

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `create-environment` | Create new environment | `workspacePath`, `environmentName`, `duplicateEnvironment` |
| `link-environment` | Link to a specific environment | `workspacePath`, `environmentName` |

**Example — create staging from production**:
```
Create a "staging" environment duplicating "production" for my-api
```

### Variables

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `list-variables` | Show variables for active environment | `workspacePath`, `service`, `environment`, `json` |
| `set-variables` | Set environment variables | `workspacePath`, `variables[]`, `service`, `environment`, `skipDeploys` |

**Example — check and set variables**:
```
Show me all environment variables for the my-api service
```

```
Set ENVIRONMENT=production and LOG_LEVEL=info for my-api, skip triggering a deploy
```

> **Note**: Setting variables triggers a redeploy by default. Use `skipDeploys` to batch changes, then deploy once.

### Networking

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `generate-domain` | Generate or retrieve a Railway domain | `workspacePath`, `service` |

**Example**:
```
Generate a domain for the my-api service
```

### Logs

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get-logs` | Get build or deployment logs | `workspacePath`, `logType`, `service`, `environment`, `deploymentId`, `lines`, `filter`, `json` |

**Log types**:
- `build` — build/compile output
- `deploy` — runtime application logs

**Filter syntax** (requires CLI v4.9.0+):
| Filter | Example |
|--------|---------|
| By level | `@level:error` |
| By text | `user login` |
| Compound | `@level:warn AND rate limit` |
| By status | `@status:500` |

**Example — check for errors**:
```
Get the last 50 deployment logs for my-api, filtered to errors only
```

**Example — investigate specific deployment**:
```
Get build logs for deployment ID abc123 in my-api
```

### Project Creation

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `create-project-and-link` | Create new project and link it | `workspacePath`, `projectName` |

**Example**:
```
Create a new Railway project called "my-new-service" and link it to the current directory
```

---

## Workflow Recipes

### Recipe 1: Debug a Failing Deployment

When a service is broken and you need to figure out why:

```
1. Check Railway status to make sure I'm authenticated
2. List deployments for my-api to find the failing one
3. Get the build logs for the latest deployment
4. If the build succeeded, get the deploy logs filtered to errors
5. Summarize what went wrong and suggest a fix
```

**What Claude does**:
1. `check-railway-status` — verifies connectivity
2. `list-deployments` with `json: true` — finds the failed deployment ID
3. `get-logs` with `logType: "build"` — checks for build errors
4. `get-logs` with `logType: "deploy"`, `filter: "@level:error"` — finds runtime errors
5. Analyzes the logs and suggests the fix

### Recipe 2: Deploy and Verify

Deploy code changes and confirm the deployment succeeds:

```
Deploy my-api, then check the deployment logs to confirm it's healthy
```

**What Claude does**:
1. `deploy` with `ci: true` — deploys and streams build logs
2. `get-logs` with `logType: "deploy"`, `lines: 20` — checks runtime output
3. Reports success or failure

### Recipe 3: Fleet Health Check

Check the status of all your services at once:

```
List all my Railway projects, then for each one list the services and their latest deployment status
```

**What Claude does**:
1. `list-projects` — gets all projects
2. For each project, `list-services` — enumerates services
3. For each service, `list-deployments` with `limit: 1`, `json: true` — gets latest status
4. Presents a summary table

### Recipe 4: Set Up a New Service from Scratch

Bootstrap a new Railway service for a FastAPI app:

```
1. Create a new Railway project called "my-new-tool" linked to /path/to/my-new-tool
2. Set these environment variables: ENVIRONMENT=production, APP_ID=my-new-tool
3. Generate a Railway domain for it
4. Deploy it
```

**What Claude does**:
1. `create-project-and-link` — creates and links
2. `set-variables` with `skipDeploys: true` — sets all vars without triggering multiple deploys
3. `generate-domain` — gets the public URL
4. `deploy` — builds and deploys

### Recipe 5: Investigate a Production Issue

A user reports that your app is slow:

```
Check the latest deployment logs for the my-api service, filtered to warnings and errors.
Also list the current environment variables to check for misconfigurations.
```

**What Claude does**:
1. `get-logs` with `filter: "@level:warn"`, `lines: 100` — looks for warnings
2. `get-logs` with `filter: "@level:error"`, `lines: 50` — looks for errors
3. `list-variables` — checks configuration
4. Analyzes patterns (memory issues, timeout errors, missing env vars)

---

## MCP vs CLI Decision Tree

```
Need to interact with Railway?
│
├─ Inside Claude Code session?
│  │
│  ├─ Yes → Use MCP tools
│  │   - Status, logs, variables, deploy, domains
│  │   - Claude chains operations automatically
│  │   - Structured data stays in context
│  │
│  └─ Need auth or SSH?
│     └─ Use CLI in external terminal
│        - railway login (browser OAuth)
│        - railway ssh (interactive shell)
│        - railway connect (database shell)
│
├─ Outside Claude Code?
│  └─ Use CLI
│     - railway up, railway logs, railway variables
│     - All non-interactive commands work
│
└─ Need destructive operations or billing?
   └─ Use Dashboard (railway.com)
      - Delete projects/services
      - Manage billing and plans
      - Change builder (NIXPACKS → RAILPACK)
      - View deployment history visually
```

---

## Safety Model

### What MCP Can Do

- Read: project/service/deployment status, logs, variables, domains
- Write: set variables, deploy, create environments, generate domains, create projects
- Link: connect to services and environments

### What MCP Cannot Do

MCP has intentional limitations for safety:

| Operation | Where to Do It | Why Not MCP |
|-----------|----------------|-------------|
| Delete projects/services | Dashboard | Destructive, irreversible |
| Manage billing | Dashboard | Financial impact |
| SSH into containers | CLI (external terminal) | Interactive session |
| Change builder | Dashboard | Configuration change |
| Manage team members | Dashboard | Access control |
| Configure custom domains | Dashboard | DNS changes |

### Shared Project Safety

Some Railway projects contain multiple services (e.g., a frontend and backend in the same project). When using MCP:

- Always specify the `service` parameter when operating on shared projects
- Use `list-services` first to confirm which services exist
- The `link-service` tool ensures subsequent operations target the correct service

---

## Troubleshooting

### CLI Not Found

**Symptom**: MCP tools fail with "railway: command not found"

**Fix**:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Verify
railway version
```

### Not Authenticated

**Symptom**: `check-railway-status` reports not logged in

**Fix**: Authenticate in an external terminal (requires browser):
```bash
railway login
```

Then return to Claude Code — the MCP server picks up the auth automatically.

### No Project Linked

**Symptom**: Tools fail with "no project linked"

**Fix**: Either:
1. Use `link-service` via MCP to link to a specific service
2. Or in an external terminal: `cd /path/to/repo && railway link`

### Empty Logs

**Symptom**: `get-logs` returns nothing

**Causes**:
- Service hasn't been deployed yet
- Wrong `logType` (use `build` for build output, `deploy` for runtime)
- Deployment is still in progress — wait and retry
- `filter` is too restrictive — try without filter first

### Variables Not Taking Effect

**Symptom**: `set-variables` succeeds but the service doesn't reflect changes

**Causes**:
- Used `skipDeploys: true` — you need to trigger a deploy afterward
- The app caches environment variables at startup — needs a full redeploy
- Wrong service targeted in a shared project — check with `list-services`

### Filter Syntax Not Working

**Symptom**: `get-logs` with `filter` returns all logs or errors

**Fix**: Requires Railway CLI v4.9.0+. Check version:
```bash
railway version
```

If below v4.9.0, upgrade: `npm update -g @railway/cli`

### MCP Server Won't Start

**Symptom**: Railway tools don't appear in Claude Code

**Checks**:
1. Verify config: `claude mcp list` should show `railway`
2. Verify npx works: `npx -y @railway/mcp-server --help`
3. Check `~/.claude.json` for correct MCP server entry

---

## Configuration Reference

### Current MCP Config

Location: `~/.claude.json` (global)

```json
{
  "mcpServers": {
    "railway": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@railway/mcp-server"],
      "env": {}
    }
  }
}
```

### Alternative: Project-Level Config

Create `.mcp.json` in your project root to enable Railway MCP only for specific projects:

```json
{
  "mcpServers": {
    "railway": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@railway/mcp-server"]
    }
  }
}
```

---

## See Also

- [RAILWAY_OVERVIEW.md](./RAILWAY_OVERVIEW.md) — What Railway is and why to use it
- [RAILWAY_CLI_REFERENCE.md](./RAILWAY_CLI_REFERENCE.md) — CLI command reference for external terminal
- [RAILWAY_SETUP_GUIDE.md](./RAILWAY_SETUP_GUIDE.md) — First-time setup and authentication
- [RAILWAY_WORKFLOWS.md](./RAILWAY_WORKFLOWS.md) — Step-by-step deployment workflows
- [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md) — General troubleshooting (beyond MCP)
- [Playwright MCP Guide](../mcp/playwright/README.md) — Similar MCP guide for browser automation

## External Resources

- [Railway MCP Server (npm)](https://www.npmjs.com/package/@railway/mcp-server)
- [Railway Documentation](https://docs.railway.com)
- [Railway CLI GitHub](https://github.com/railwayapp/cli)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)

---

**Last Updated**: February 2026
