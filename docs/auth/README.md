# Authentication Documentation

## Templates (Recommended)

For reusable auth patterns, see the template library:

| Template | Description |
|----------|-------------|
| [templates/auth/README.md](../../templates/auth/README.md) | Overview and decision guide |
| [templates/auth/SUPABASE_AUTH.md](../../templates/auth/SUPABASE_AUTH.md) | Supabase setup and code patterns |
| [templates/auth/ACCESS_CONTROL.md](../../templates/auth/ACCESS_CONTROL.md) | Per-app allowlists and RBAC |

## Project-Specific Setup

These docs contain setup guides specific to your environment:

| Guide | Description |
|-------|-------------|
| [SUPABASE-SETUP-GUIDE.md](SUPABASE-SETUP-GUIDE.md) | How to set up a new Supabase project |
| [AUTH-TROUBLESHOOTING.md](AUTH-TROUBLESHOOTING.md) | Common issues and solutions |

## Quick Start Checklist

### New Project Setup
- [ ] Get Supabase credentials (create project or reuse existing)
- [ ] Add env vars: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_JWT_SECRET`
- [ ] Copy code pattern from [templates/auth/](../../templates/auth/)
- [ ] Add production URL to Supabase Redirect URLs
- [ ] Configure `ALLOWED_USERS` or `ALLOWED_DOMAIN`
- [ ] Deploy

## Environment Variables

```bash
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJ...

# Server-side (FastAPI, Next.js API routes)
SUPABASE_JWT_SECRET=your-jwt-secret

# Access control
ALLOWED_USERS=user1@domain.com,user2@domain.com
ALLOWED_DOMAIN=yourdomain.com
```

## See Also

- [Railway Deployment](../railway/README.md) — Deploying with env vars
- [Testing](../../templates/testing/README.md) — Testing auth flows with Playwright
