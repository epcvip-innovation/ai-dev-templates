# Static Asset Caching & CDN (FastAPI + Cloudflare)

**Last Updated:** 2026-01-21

## The Problem

Static JS/CSS files get cached by Cloudflare CDN (4-hour default). After deploying updates, users see stale files until cache expires or they hard-refresh.

**Symptoms:**
- New features don't appear after deploy
- JavaScript errors from version mismatches
- `cf-cache-status: HIT` with old `last-modified` date

## Root Cause

- Cloudflare caches static files based on URL path
- FastAPI's `StaticFiles` doesn't set cache-control headers by default
- Manual `?v=2` version params require remembering to bump on every change

---

## Solution: Git Commit Hash Versioning (Recommended)

Three files provide automatic cache-busting on every deploy:

### 1. version.py - Capture commit hash

```python
"""
Application version management for cache-busting.

Captures git commit hash at startup for consistent versioning
across all requests and asset references.
"""

import subprocess
import os
from functools import lru_cache


@lru_cache(maxsize=1)
def get_app_version() -> str:
    """
    Get application version string for cache-busting.

    Returns short git commit hash if available, otherwise falls back to:
    1. RAILWAY_GIT_COMMIT_SHA environment variable (Railway provides this)
    2. Local git rev-parse (for development)
    3. "dev" as last resort

    Cached at module level - only computed once per process.
    """
    # First, try Railway's environment variable (most reliable in production)
    railway_sha = os.getenv("RAILWAY_GIT_COMMIT_SHA")
    if railway_sha:
        return railway_sha[:7]

    # Try git command (works in local development)
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=7", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=os.path.dirname(__file__) or "."
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    # Fallback for environments without git
    return "dev"


# Pre-compute at import time
APP_VERSION = get_app_version()
```

### 2. CachedStaticFiles - Set proper headers

```python
from starlette.staticfiles import StaticFiles

class CachedStaticFiles(StaticFiles):
    """StaticFiles with cache-control headers for versioned assets."""

    async def get_response(self, path: str, scope) -> "Response":
        response = await super().get_response(path, scope)
        query_string = scope.get("query_string", b"").decode()

        if "v=" in query_string:
            # Versioned request: cache for 1 year (immutable)
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            # Unversioned fallback: short cache
            response.headers["Cache-Control"] = "public, max-age=3600"

        return response

# Mount with custom class
app.mount("/static", CachedStaticFiles(directory="static"), name="static")
```

### 3. inject_asset_versions() - Auto-inject versions

```python
import re

def inject_asset_versions(html: str, version: str) -> str:
    """
    Add ?v=VERSION to /static/ CSS and JS references.

    Transforms:
        href="/static/css/styles.css"  -> href="/static/css/styles.css?v=abc1234"
        src="/static/js/app.js"        -> src="/static/js/app.js?v=abc1234"
    """
    pattern = r'((?:href|src)=["\'])(/static/[^"\']+\.(?:css|js))(["\'])'

    def replacer(match):
        attr_start, path, quote = match.groups()
        if '?v=' in path:
            return match.group(0)  # Already versioned
        return f'{attr_start}{path}?v={version}{quote}'

    return re.sub(pattern, replacer, html)
```

---

## How It Works

```
1. Deploy pushes to Railway
2. Railway sets RAILWAY_GIT_COMMIT_SHA env var
3. version.py reads commit hash on startup (e.g., "abc1234")
4. HTML template renders with /static/js/app.js
5. inject_asset_versions() transforms to /static/js/app.js?v=abc1234
6. Cloudflare treats ?v=abc1234 as unique URL, fetches fresh
7. CachedStaticFiles returns "immutable, max-age=1yr" header
8. Cloudflare caches forever (but URL changes on next deploy)
```

**Result:** Every deploy automatically busts cache without manual version bumps.

---

## Projects Using This Pattern

| Project | Location |
|---------|----------|
| athena-usage-monitor-fastapi | `utilities/athena-usage-monitor-fastapi/` |
| experiments-dashboard | `utilities/experiments-dashboard/` |

---

## Alternative: Manual Version Params (Not Recommended)

```html
<link rel="stylesheet" href="/static/css/styles.css?v=2">
```

**Problems:**
- Must remember to bump version on every change
- Easy to forget, leading to stale cache bugs
- No automated enforcement

---

## Official Documentation

**FastAPI:**
- [FastAPI Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)
- [Custom StaticFiles Cache Headers (GitHub Discussion)](https://github.com/fastapi/fastapi/discussions/7618)

**Cloudflare:**
- [Cloudflare Caching Levels](https://developers.cloudflare.com/cache/how-to/set-caching-levels/) - "Standard" mode treats each query string as unique
- [Cache-Control Best Practices](https://developers.cloudflare.com/cache/concepts/cache-control/)

---

## See Also

- [TECH_STACK_DEFAULTS.md](../getting-started/TECH_STACK_DEFAULTS.md) - FastAPI + Vanilla JS recommendation
- [Railway Quickstart](../railway/RAILWAY_QUICKSTART.md) - Deployment workflow
