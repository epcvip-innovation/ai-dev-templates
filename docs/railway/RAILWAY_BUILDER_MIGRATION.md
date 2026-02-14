# Railway Builder Migration: NIXPACKS to RAILPACK

Guide for migrating from NIXPACKS (deprecated) to RAILPACK (current).

## Current Status

EPCVIP operates 11 Railway services. Most have migrated to **RAILPACK**; a few remain on **NIXPACKS** (still works, maintenance-only mode).

| Service | Current Builder | Status |
|---------|----------------|--------|
| Experiments Dashboard | RAILPACK | Migrated |
| Reports Dashboard | RAILPACK | Migrated |
| Athena Monitor | RAILPACK | Migrated |
| Documentation Hub | RAILPACK | Migrated |
| Tools Hub | RAILPACK | Migrated |
| Admin Dashboard | RAILPACK | Migrated |
| Funnel Step Lab | RAILPACK | Migrated |
| Competitor Analyzer | RAILPACK | Migrated (Next.js) |
| Fwaptile Wordle | RAILPACK | Migrated |
| Ping Tree Compare | NIXPACKS | Pending — verify volume mount |
| Uptime Kuma | Docker | Self-hosted, N/A |

## Why Migrate to RAILPACK?

RAILPACK is Railway's next-generation builder, offering substantial improvements:

### Image Size Reduction
- **Node.js**: 38% smaller images
- **Python**: 77% smaller images
- **Benefits**: Faster deployments, lower storage costs, quicker cold starts

### Better Caching
- Direct BuildKit integration for superior layer caching
- More cache hits across deployments
- Sharable caches between environments
- **Result**: Faster builds, cheaper costs

### Granular Version Control
- Support for exact `major.minor.patch` versions
- NIXPACKS used Nix's approximate versioning
- **Example**: Specify Python 3.11.5 instead of ~3.11

### Active Development
- RAILPACK under active development
- NIXPACKS in maintenance-only mode
- New features only coming to RAILPACK

### Supported Languages (as of February 2026)

RAILPACK currently supports:
- Node.js
- Python (your primary language)
- Go
- PHP
- Static HTML (Vite, Astro, CRA, Angular)

## Migration Decision

### When to Migrate

✅ **Good times to migrate**:
- Starting a new project
- Major refactoring or updates
- Experiencing slow build times
- Want smaller image sizes for cost savings
- Need specific version pinning

❌ **When to wait**:
- Production app working perfectly
- About to launch critical update
- No current performance issues
- Team unfamiliar with RAILPACK

### Migration Risk Assessment

**Low Risk**:
- Simple Python/Node.js apps
- Standard dependencies
- Well-tested applications
- Have staging environment

**Medium Risk**:
- Complex build processes
- Custom build commands
- Specific version requirements
- Multiple microservices

**High Risk**:
- Mission-critical production app
- Unusual dependencies
- No staging environment
- Tight deadlines

## Migration Process

### Option 1: Via Railway Dashboard (Easiest)

1. **Open Railway Dashboard**
   - Go to https://railway.com/dashboard
   - Select your project

2. **Navigate to Service Settings**
   - Click on your service
   - Go to "Settings" tab
   - Find "Builder" section

3. **Change Builder**
   - Select "RAILPACK" from dropdown
   - Click "Save"

4. **Trigger Deployment**
   - Make a small change to your repo
   - Push to main branch
   - Railway will rebuild with RAILPACK

### Option 2: Via railway.toml (Recommended)

**Before (NIXPACKS)**:
```toml
[build]
builder = "nixpacks"

[build.nixpacks]
nixpacksVersion = "1.30.0"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "on_failure"
```

**After (RAILPACK)**:
```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"
```

**Changes**:
1. Change `builder = "nixpacks"` to `builder = "RAILPACK"`
2. Remove `[build.nixpacks]` section
3. Update `restartPolicyType` values to uppercase (RAILPACK convention)

### Step-by-Step Migration

#### 1. Prepare

```bash
# Ensure you're on main branch
git checkout main
git pull origin main

# Verify current deployment works
curl https://your-app-production.up.railway.app/health
```

#### 2. Create Migration Branch (Recommended)

```bash
git checkout -b migrate-to-railpack
```

#### 3. Update railway.toml

```bash
# Edit railway.toml
# Change builder from nixpacks to RAILPACK
```

Example for your projects:

**tiller-bridge**:
```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"
healthcheckPath = "/health"
healthcheckTimeout = 60
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

**ping-tree-compare**:
```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"
healthcheckPath = "/health"
healthcheckTimeout = 120
restartPolicyType = "ON_FAILURE"

[[deploy.mounts]]
name = "airy-volume"
mountPath = "/app/data"
```

#### 4. Test Deployment

```bash
# Commit changes
git add railway.toml
git commit -m "chore: migrate to RAILPACK builder"

# Push to test branch (Railway might auto-deploy PR preview)
git push origin migrate-to-railpack
```

#### 5. Monitor Build

```bash
# Watch build logs
railway logs --build --follow

# Check for errors
railway logs --build | grep -i error
```

#### 6. Verify Deployment

```bash
# Check health
curl https://your-app-staging.up.railway.app/health

# Test API endpoints
curl https://your-app-staging.up.railway.app/api/status

# Check logs for issues
railway logs --limit 100 | grep -i "error\|warning"
```

#### 7. Merge to Production

```bash
# If everything works, merge to main
git checkout main
git merge migrate-to-railpack
git push origin main

# Monitor production deployment
railway logs --follow
```

#### 8. Post-Migration Verification

```bash
# Verify production health
curl https://your-app-production.up.railway.app/health

# Check image size (in Railway dashboard)
# Should be 38-77% smaller

# Monitor for 24 hours
railway logs --follow
```

## Configuration Differences

### Build Configuration

**NIXPACKS** (old):
```toml
[build]
builder = "nixpacks"

[build.nixpacks]
nixpacksVersion = "1.30.0"
```

**RAILPACK** (new):
```toml
[build]
builder = "RAILPACK"

# Optional: specify RAILPACK version
[build]
railpackVersion = "0.7.0"
```

### Python Version Specification

**NIXPACKS**:
```toml
[build.nixpacks]
nixpacksVersion = "1.30.0"

# Set via environment variable
# NIXPACKS_PYTHON_VERSION=3.11
```

**RAILPACK**:
```toml
[build]
builder = "RAILPACK"

# Python version detected from:
# - runtime.txt
# - pyproject.toml
# - .python-version
```

### Restart Policy Naming

**NIXPACKS** (lowercase):
```toml
restartPolicyType = "on_failure"
```

**RAILPACK** (uppercase):
```toml
restartPolicyType = "ON_FAILURE"
```

Options: `ON_FAILURE`, `ALWAYS`, `NEVER`

## Project-Specific Migration Notes

### tiller-bridge

**Current**: Python FastAPI with SQLite, cron service
**Considerations**:
- Main service: straightforward migration
- Cron service: update railway.cron.toml separately
- Database: No changes needed (volume mounts work the same)
- Estimated benefit: 77% smaller image, faster builds

**Migration steps**:
1. Update main railway.toml
2. Update railway.cron.toml
3. Test cron schedule still works (every 30 minutes)

### ping-tree-compare

**Current**: Python FastAPI with persistent volume
**Considerations**:
- Volume mount syntax identical
- Single worker for SQLite: keep `--workers 1`
- Health check timeout: 120s (keep the same)
- Estimated benefit: 77% smaller image

**Migration steps**:
1. Update railway.toml
2. Verify volume mount after migration: `railway ssh` → check `/app/data`
3. Test database operations

### anki-clone & japanese-flashcard-app

**Current**: Node.js applications
**Considerations**:
- Node.js support in RAILPACK
- Build commands preserved
- Estimated benefit: 38% smaller image

## Rollback Plan

If migration causes issues:

### Immediate Rollback

```bash
# Revert railway.toml
git revert HEAD
git push origin main

# Or manually change builder back
# Edit railway.toml: builder = "nixpacks"
git add railway.toml
git commit -m "rollback: revert to nixpacks"
git push origin main
```

### Dashboard Rollback

1. Go to Railway dashboard
2. Find previous successful deployment
3. Click "Redeploy"
4. System uses previous configuration

### Verify Rollback

```bash
# Check health
curl https://your-app-production.up.railway.app/health

# Monitor logs
railway logs --follow
```

## Gradual Migration Strategy

For multiple projects, migrate one at a time:

### Phase 1: Testing Project
- Migrate least critical project first
- Example: japanese-flashcard-app (low traffic)
- Monitor for 1 week

### Phase 2: Medium Complexity
- Migrate anki-clone
- Monitor for 1 week

### Phase 3: Production Projects
- Migrate ping-tree-compare
- Monitor for 1 week
- Migrate tiller-bridge last (most critical)

## Post-Migration Monitoring

### Week 1: Daily Checks

```bash
# Check health daily
curl https://your-app-production.up.railway.app/health

# Review logs for errors
railway logs --json | jq 'select(.level=="error")'

# Monitor build times (should be faster)
railway logs --build
```

### Week 2-4: Weekly Checks

```bash
# Weekly health verification
curl https://your-app-production.up.railway.app/health

# Check Railway dashboard for:
# - Image size reduction
# - Build time improvements
# - Deployment success rate
```

## Benefits Realization

After migration, you should see:

### Immediate
- ✅ Smaller Docker images (38-77% reduction)
- ✅ Faster builds (better caching)
- ✅ Future-proof configuration

### Medium-term (1-3 months)
- ✅ Lower storage costs
- ✅ Faster deployment times
- ✅ Improved CI/CD performance

### Long-term (3+ months)
- ✅ Access to new RAILPACK features
- ✅ Better developer experience
- ✅ Reduced technical debt

## FAQ

### Q: Do I have to migrate?
**A**: No! NIXPACKS continues to work in maintenance mode. Migrate when convenient.

### Q: Will my environment variables change?
**A**: No, environment variables are unaffected by builder choice.

### Q: Will migration cause downtime?
**A**: Minimal. Railway does rolling deploys. Expect <2 minutes typical downtime.

### Q: Can I test without affecting production?
**A**: Yes! Use a PR branch or staging environment to test first.

### Q: What if RAILPACK doesn't support my language?
**A**: Continue using NIXPACKS or switch to Dockerfile-based builds.

### Q: Will volumes/databases be affected?
**A**: No, persistent volumes and databases work identically with both builders.

## Next Steps

1. ✅ Review this guide
2. ✅ Choose migration timeline
3. ✅ Test on non-critical project first
4. ✅ Monitor results
5. ✅ Gradually migrate remaining projects

## Resources

- **Railway RAILPACK Announcement**: https://blog.railway.com/p/introducing-railpack
- **Railway Build Configuration**: https://docs.railway.com/guides/build-configuration
- **NIXPACKS Reference**: https://docs.railway.com/reference/nixpacks
- **Your Templates**: See `templates/railway/` for NIXPACKS and RAILPACK examples

---

**Migration Status Tracker**:

| Service | Current Builder | Target | Status | Notes |
|---------|----------------|--------|--------|-------|
| Experiments Dashboard | RAILPACK | — | Complete | |
| Reports Dashboard | RAILPACK | — | Complete | |
| Athena Monitor | RAILPACK | — | Complete | |
| Documentation Hub | RAILPACK | — | Complete | |
| Tools Hub | RAILPACK | — | Complete | |
| Admin Dashboard | RAILPACK | — | Complete | |
| Funnel Step Lab | RAILPACK | — | Complete | |
| Competitor Analyzer | RAILPACK | — | Complete | Next.js |
| Fwaptile Wordle | RAILPACK | — | Complete | |
| Ping Tree Compare | NIXPACKS | RAILPACK | Pending | Verify volume mount post-migration |
| Uptime Kuma | Docker | — | N/A | Self-hosted image |

Legend: Complete | Pending | N/A

**Last Updated**: February 2026
