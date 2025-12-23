# Authentication with Supabase

Standard authentication pattern for EPCVIP internal tools using Supabase Auth.

## Why Supabase Auth

| Requirement | Supabase Delivers |
|-------------|-------------------|
| Works for Streamlit, FastAPI, custom UIs | SDKs for Python, JS, and more |
| Password reset, MFA, admin panel | All built-in |
| Learn once, use everywhere | Same patterns across all apps |
| Low/no cost | Free 100K MAU |
| SOC2 certified | Type 2 |

## Quick Start Checklist

### New Project Setup
- [ ] Get Supabase credentials from existing project (or create new)
- [ ] Add env vars: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_JWT_SECRET`
- [ ] Copy appropriate code pattern (Streamlit or FastAPI)
- [ ] Add production URL to Supabase Redirect URLs
- [ ] Deploy to Railway

### Existing Supabase Project
- **Project**: `epcvip-auth` (shared across tools)
- **Dashboard**: https://supabase.com/dashboard/project/yuithqxycicgokkgmpzg

## Documentation

| Guide | Description |
|-------|-------------|
| [SUPABASE-SETUP-GUIDE.md](SUPABASE-SETUP-GUIDE.md) | Project setup, providers, credentials |
| [SUPABASE-CODE-PATTERNS.md](SUPABASE-CODE-PATTERNS.md) | Streamlit, FastAPI, and frontend patterns |
| [AUTH-TROUBLESHOOTING.md](AUTH-TROUBLESHOOTING.md) | Common issues and solutions |

## Currently Deployed Tools

| Tool | Framework | Auth Status |
|------|-----------|-------------|
| athena-usage-monitor | Streamlit | Supabase (Google OAuth) |
| ping-tree-compare | FastAPI | Supabase (Google OAuth + Email) |

## Environment Variables

### Required for All Apps
```bash
SUPABASE_URL=https://yuithqxycicgokkgmpzg.supabase.co
SUPABASE_ANON_KEY=<get from dashboard>
```

### Additional for FastAPI Backend
```bash
SUPABASE_JWT_SECRET=<get from dashboard - Settings > API > JWT Secret>
```

### Optional Development
```bash
ENVIRONMENT=development
DEVELOPER_HOME_IP=<your WSL IP>  # Enables localhost auth bypass
```

## Related Resources

- **Templates**: `utilities/supabase-auth-templates/`
- **Tools Hub**: https://ahhhdum.github.io/epcvip-tools-hub/
- **Railway Docs**: `docs/railway/`
