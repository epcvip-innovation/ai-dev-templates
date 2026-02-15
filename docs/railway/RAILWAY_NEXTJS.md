# Railway + Next.js Deployment Guide

Complete guide for deploying Next.js applications to Railway, based on production experience with Next.js 15+ and React 19.

## Quick Start

Next.js apps deploy to Railway with minimal configuration:

```bash
# 1. Push to GitHub (Railway auto-deploys from main branch)
git push origin main

# 2. Verify deployment
curl https://your-app-production.up.railway.app/api/health
```

## Minimal Configuration

### package.json

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start -H 0.0.0.0 -p ${PORT:-3000}",
    "lint": "next lint"
  }
}
```

**Key points:**
- `-H 0.0.0.0` binds to all interfaces (required for containers)
- `-p ${PORT:-3000}` uses Railway's injected PORT with fallback

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // Smaller images, better for containers
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
}

module.exports = nextConfig
```

### railway.toml

```toml
[build]
builder = "RAILPACK"

[deploy]
healthcheckPath = "/api/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

## Standalone Mode + Railpack (Recommended)

When using `output: "standalone"` with Railpack builder, you need **two config files** because Railpack ignores `startCommand` in railway.toml.

### The Problem

Railpack auto-detects Next.js and defaults to `npm run start`, which fails with standalone:
```
⚠ "next start" does not work with "output: standalone" configuration.
Use "node .next/standalone/server.js" instead.
```

### The Solution

**1. `railway.toml`** - Railway platform settings only:
```toml
[build]
builder = "RAILPACK"

[deploy]
healthcheckPath = "/api/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

**2. `railpack.json`** - Railpack builder settings (same directory):
```json
{
  "$schema": "https://schema.railpack.com",
  "deploy": {
    "startCommand": "node .next/standalone/server.js",
    "variables": {
      "HOSTNAME": "0.0.0.0"
    }
  }
}
```

### Why HOSTNAME=0.0.0.0?

Next.js standalone binds to the container hostname by default. Without this, the server listens on an internal hostname and Railway's health checks can't reach it:
```
# Without HOSTNAME - fails health checks
- Network: http://d812d860f458:8080

# With HOSTNAME=0.0.0.0 - works
- Network: http://0.0.0.0:8080
```

### Performance Impact

This pattern significantly improves build times:
- Before (npm run start): ~347 seconds
- After (standalone): ~38 seconds (89% faster)

## BasePath Configuration (Multi-App Deployments)

When deploying multiple apps under one domain (e.g., `your-app.example.com/funnels/`, `your-app.example.com/compare/`), use Next.js basePath.

### next.config.ts

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  basePath: "/funnels",  // Your app's path prefix
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "*.supabase.co",
        pathname: "/storage/v1/object/public/**",
      },
    ],
  },
};

export default nextConfig;
```

### Health Check Path

**Critical**: Include basePath in health check configuration:

```toml
# railway.toml
[deploy]
healthcheckPath = "/funnels/api/health"  # basePath + /api/health
```

### Asset Paths

Static assets automatically use basePath, but dynamic paths need handling:

```typescript
// lib/utils.ts
const ASSET_BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || "/funnels";

// Use in image paths, etc.
const screenshotUrl = `${ASSET_BASE_PATH}/reports/${date}/screenshots/${filename}`;
```

### Environment Variable

Set in Railway for runtime access:

```
NEXT_PUBLIC_BASE_PATH=/funnels
```

### Common Issues

**404 on static assets**: Verify paths include basePath prefix.

**Health check fails**: Ensure `healthcheckPath` includes basePath.

**Links broken**: Use Next.js `<Link>` component (handles basePath automatically) instead of `<a>` tags.

## Health Check Endpoint

Create `/app/api/health/route.ts`:

```typescript
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    port: process.env.PORT || 'unknown'
  });
}
```

**Or** handle in middleware for faster response:

```typescript
// middleware.ts
export async function middleware(request: NextRequest) {
  if (request.nextUrl.pathname === '/api/health') {
    return NextResponse.json({
      status: 'ok',
      timestamp: new Date().toISOString()
    });
  }
  // ... rest of middleware
}
```

## Common Issues & Solutions

### 502 Error: "Application failed to respond"

**Most Common Cause: Port Mismatch**

Railway has two port concepts:
1. **PORT env var** - What Railway injects for your app to listen on
2. **Public Networking port** - What Railway's proxy routes traffic to

If these don't match, you get 502 even when health checks pass internally.

**Solution:**
1. Go to **Service Settings → Networking → Public Networking**
2. Click on your domain
3. Look for "A port was detected by Railway magic ✨"
4. **Select the auto-detected port** instead of custom port
5. Click "Update"

**Prevention:**
- Always let Railway auto-detect ports
- Include port in health response for debugging:
  ```typescript
  return { status: 'ok', port: process.env.PORT }
  ```

### Container Keeps Getting SIGTERM

**Cause:** Standalone output not configured properly.

**Solution:**
1. Add `output: 'standalone'` to next.config.js
2. Railway will use the standalone server automatically

### Supabase Auth Not Working

**Cause:** `NEXT_PUBLIC_*` environment variables not available at build time.

**Solution:** Set these variables in Railway dashboard BEFORE deploying. RAILPACK will pick them up during build.

Required variables:
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
```

## Standalone vs Standard Mode

| Aspect | Standalone (`output: 'standalone'`) | Standard |
|--------|-------------------------------------|----------|
| Image size | ~38% smaller | Larger |
| Build output | `.next/standalone/server.js` | Uses `next start` |
| Dependencies | Self-contained | Full node_modules |
| Railway detection | Auto-detected | Auto-detected |

**Recommendation:** Use standalone for production deployments.

## Monorepo Setup

If your Next.js app is in a subdirectory:

**Railway Dashboard:**
- Root Directory: `/web` (your app's folder)
- Config File Path: `/railway.toml` (relative to root directory)

**railway.toml stays in the app folder:**
```
your-repo/
├── web/
│   ├── railway.toml
│   ├── package.json
│   └── ...
└── other-folders/
```

## Environment Variables

### Build-time vs Runtime

| Variable Pattern | When Available | Use Case |
|-----------------|----------------|----------|
| `NEXT_PUBLIC_*` | Build time | Client-side code |
| Other vars | Runtime only | Server-side code |

### Setting Variables

```bash
# Via Railway CLI (triggers redeploy)
railway variables set NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co

# View current variables
railway variables
```

## Deployment Checklist

- [ ] `output: 'standalone'` in next.config.js
- [ ] Health check endpoint at `/api/health`
- [ ] `NEXT_PUBLIC_*` vars set in Railway dashboard
- [ ] Port set to auto-detect in Public Networking
- [ ] railway.toml with RAILPACK builder

## Example Configurations

### Basic Next.js 15 App

```toml
# railway.toml
[build]
builder = "RAILPACK"

[deploy]
healthcheckPath = "/api/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### Next.js with Database

```toml
# railway.toml
[build]
builder = "RAILPACK"

[deploy]
healthcheckPath = "/api/health"
healthcheckTimeout = 180  # Longer for DB connection
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### Next.js with Persistent Storage

```toml
# railway.toml
[build]
builder = "RAILPACK"

[deploy]
healthcheckPath = "/api/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"

[[deploy.volumeMounts]]
mountPath = "/app/data"
```

## Debugging

### Check Deployment Logs

```bash
# Build logs
railway logs --build

# Runtime logs
railway logs --follow

# Filter for errors
railway logs --json | jq 'select(.level=="error")'
```

### Verify Health Check

```bash
# Test health endpoint
curl -s https://your-app.up.railway.app/api/health | jq

# Check response time
time curl -s https://your-app.up.railway.app/api/health
```

### Common Log Patterns

**Good:**
```
▲ Next.js 15.x.x
- Local:   http://0.0.0.0:8080
✓ Ready in xxxms
```

**Bad - Wrong hostname:**
```
- Local:   http://container-id:8080
```
Fix: Ensure `-H 0.0.0.0` in start command.

## Resources

- [Next.js Deployment Docs](https://nextjs.org/docs/app/getting-started/deploying)
- [Railway Next.js Template](https://github.com/nextjs/deploy-railway)
- [Railway Config Reference](https://docs.railway.com/reference/config-as-code)
