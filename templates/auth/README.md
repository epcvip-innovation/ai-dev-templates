# Authentication Templates

Reusable authentication patterns for internal tools.

## Two Recommended Options

### Supabase Auth (Default for Python + Multi-Tool)

Best when you need Python support or shared auth across multiple tools.

| Strength | Details |
|----------|---------|
| Python SDKs | Streamlit, FastAPI, Flask |
| Database included | PostgreSQL with auth |
| Shared auth | One project, many apps |
| Free tier | 50K MAU |

### Clerk (Default for React/Next.js + Great UI)

Best when you want polished built-in UI components or are JavaScript-only.

| Strength | Details |
|----------|---------|
| Built-in UI | Sign-in/up modals, user buttons |
| React/Next.js | First-class support |
| Theming API | Easy dark mode, custom styles |
| Free tier | 10K MAU |

## Template Files

| File | Description |
|------|-------------|
| [SUPABASE_AUTH.md](SUPABASE_AUTH.md) | Supabase setup and code patterns |
| [CLERK_AUTH.md](CLERK_AUTH.md) | Clerk setup and code patterns |
| [ACCESS_CONTROL.md](ACCESS_CONTROL.md) | Per-app user allowlists |

## Quick Decision Guide

```
What kind of app are you building?
│
├─ Python dashboard (Streamlit/Gradio)
│   └─ Use: Supabase + streamlit-supabase-auth
│
├─ Python API (FastAPI/Flask)
│   └─ Use: Supabase + local JWT validation
│
├─ Next.js/React (want built-in UI)
│   └─ Use: Clerk + @clerk/nextjs
│
├─ Next.js/React (need database too)
│   └─ Use: Supabase + @supabase/ssr
│
├─ Vanilla JS game/app
│   └─ Use: Clerk CDN (great modals)
│
├─ Multiple tools, shared login
│   └─ Use: Supabase (shared project)
│
└─ Enterprise/compliance needs
    └─ Consider: Auth0, Okta
```

## Environment Variables (Standard)

All auth implementations should use these standard variable names:

```bash
# Supabase (recommended)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJ...               # Public, safe for client
SUPABASE_JWT_SECRET=your-jwt-secret    # Server-side only

# Access Control
ALLOWED_USERS=user1@domain.com,user2@domain.com
ALLOWED_DOMAIN=yourdomain.com          # Fallback if ALLOWED_USERS empty

# Development
ENVIRONMENT=development                 # or "production"
```

## Architecture Patterns

### Option A: Supabase (Auth + Database)

```
┌─────────────────────────────────────────────────────┐
│                    Supabase                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │    Auth     │  │  Database   │  │   Storage   │ │
│  │  (GoTrue)   │  │ (PostgreSQL)│  │    (S3)     │ │
│  └──────┬──────┘  └─────────────┘  └─────────────┘ │
└─────────┼───────────────────────────────────────────┘
          │
    ┌─────┴─────┐
    │ JWT Token │
    └─────┬─────┘
          │
    ┌─────┴─────────────────────────────────┐
    │                                        │
┌───┴────┐  ┌─────────┐  ┌─────────┐  ┌─────┴────┐
│Streamlit│  │ FastAPI │  │ Next.js │  │ Express  │
│   App   │  │   API   │  │   App   │  │   API    │
└─────────┘  └─────────┘  └─────────┘  └──────────┘
```

### Option B: Clerk (Auth Only) + Separate DB

```
┌──────────────┐          ┌──────────────┐
│    Clerk     │          │ Database     │
│  (Auth)      │          │ (Neon, etc.) │
└──────┬───────┘          └──────┬───────┘
       │                         │
       │    ┌────────────┐       │
       └───►│  Your App  │◄──────┘
            │  (Next.js, │
            │  Express)  │
            └────────────┘
```

## Shared vs Separate Projects

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Shared Supabase** | Single sign-on, one user DB | Shared rate limits | Internal tools, same team |
| **Separate projects** | Isolated, independent | Multiple logins | Different teams/clients |
| **Clerk + Neon** | Great UI, serverless DB | Two services to manage | JS-only apps, games |

For internal tools with Python, **shared Supabase is usually better**.
For React/JS apps with great UX needs, **Clerk is excellent**.

## Security Checklist

- [ ] JWT secret is 32+ characters
- [ ] Production uses HTTPS only
- [ ] Cookies have `Secure` and `SameSite` flags
- [ ] Access control validates on every request
- [ ] No secrets in client-side code
- [ ] OAuth redirect URLs are explicit (no wildcards)
- [ ] Dev bypass uses TCP peer IP (`request.client.host`), not forwarded headers
- [ ] Dev bypass requires BOTH `ENVIRONMENT=development` AND localhost/private IP
