# Preferred Tech Stack Defaults

When starting a new project, these are battle-tested choices based on real production experience.

---

## Internal Tools / Dashboards

**Backend**: FastAPI + Python
- Simple, fast, Railway-friendly
- Excellent for data-centric apps with AWS integrations
- Great DX with auto-generated OpenAPI docs

**Frontend**: Vanilla JS
- No build step, direct file serving
- Works great for internal tools where React would be overkill
- Easy to maintain without framework churn

**Auth**: Supabase
- Google OAuth with PKCE flow
- JWT-based, server-side validation
- RBAC via shared `epcvip_app_roles` table

**Database**:
- **Supabase PostgreSQL** - When you need user data, shared state
- **SQLite** - When you need persistent local storage (Railway volumes)

**Deployment**: Railway
- Auto-deploy on push to main
- Custom domains via Cloudflare
- Persistent volumes for SQLite
- **Static assets**: Git-hash versioning for CDN cache-busting. See [STATIC-ASSETS-CDN.md](../reference/STATIC-ASSETS-CDN.md)

---

## Public Web Apps

**Framework**: Next.js 14+ (App Router)
- Server components by default
- Built-in API routes
- Great SEO and performance

**Language**: TypeScript
- Type safety, better DX, easier refactoring

**Styling**: Tailwind CSS
- Utility-first, fast iteration
- Consistent design tokens

**Database**: Supabase or Neon PostgreSQL
- Managed Postgres with generous free tiers
- Real-time subscriptions if needed

---

## Games / Interactive

**Engine**: KaPlay (Kaboom.js fork)
- 2D canvas games with simple API
- Good for retro-style games

**Backend**: Express + TypeScript
- WebSocket support for multiplayer
- Supabase for player data

**Auth**: Clerk
- Easy setup, good DX
- Email + social auth out of the box

---

## Decision Framework

| Question | If Yes... | If No... |
|----------|-----------|----------|
| Internal tool for trusted users? | FastAPI + Vanilla JS | Consider React/Next.js |
| Need real-time features? | WebSocket + Supabase | REST API is fine |
| Complex state management? | React/Zustand | Vanilla JS |
| SEO important? | Next.js | SPA is fine |
| Data-heavy (analytics/reports)? | FastAPI + Streamlit | Standard web stack |

---

## Anti-Patterns (Avoid)

- **Don't use React for simple CRUD apps** - Vanilla JS with fetch() is enough
- **Don't roll your own auth** - Use Supabase/Clerk
- **Don't use microservices for internal tools** - Monolith is fine
- **Don't over-engineer database** - SQLite works for many use cases

---

## See Also

- [NEW-PROJECT-SETUP.md](./NEW-PROJECT-SETUP.md) - Claude Code setup for new projects
- [EPCVIP_SERVICES.md](../../../../EPCVIP_SERVICES.md) - EPCVIP service architecture and tech stacks
