# Supabase Authentication Patterns

Generic Supabase authentication patterns for various frameworks. These are **framework patterns** - for organization-specific RBAC tables, redirect URLs, and user management, see your organization's internal documentation.

---

## Setup Checklist

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com) → New Project
2. Note these values from Settings > API:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **Anon Key**: `eyJ...` (safe for client-side)
   - **JWT Secret**: For server-side token validation

### 2. Configure Auth Providers

1. Authentication > Providers
2. Enable desired providers:
   - ✅ Email/Password (default)
   - ✅ Google (recommended for internal tools)
   - ✅ GitHub (optional)

### 3. Set Redirect URLs

1. Authentication > URL Configuration
2. Add your URLs:
   ```
   https://your-app.com
   https://your-app.com/auth/callback
   http://localhost:3000  (for dev)
   ```

---

## Streamlit Pattern

Uses `streamlit-supabase-auth` library.

### Installation

```bash
pip install streamlit-supabase-auth supabase
```

### Code

```python
import os
import streamlit as st
from streamlit_supabase_auth import login_form, logout_button

st.set_page_config(page_title="My App", layout="wide")

# Auth gate
session = login_form(
    url=os.getenv("SUPABASE_URL"),
    apiKey=os.getenv("SUPABASE_ANON_KEY"),
    providers=["google"],
)

if not session:
    st.stop()

# User is authenticated
user_email = session["user"]["email"]

# Sidebar with user info and logout
with st.sidebar:
    st.write(f"**{user_email}**")
    logout_button()
    st.divider()

# Your app code here
st.title("Welcome!")
```

---

## FastAPI Pattern

Local JWT validation (~1ms vs ~600ms remote call).

### Installation

```bash
pip install PyJWT fastapi
```

### auth.py

```python
"""Supabase JWT validation for FastAPI"""
import os
import jwt
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")
ALLOWED_USERS = os.getenv("ALLOWED_USERS", "").split(",")
ALLOWED_DOMAIN = os.getenv("ALLOWED_DOMAIN", "")
JWT_ALGORITHM = "HS256"


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Validate Supabase JWT and return user info."""
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience="authenticated",
        )

        # Check expiration
        exp = payload.get("exp", 0)
        if datetime.now(timezone.utc).timestamp() > exp:
            return None

        email = payload.get("email", "")
        
        # Check access control
        if not is_allowed(email):
            return None

        return {
            "user_id": payload.get("sub"),
            "email": email,
            "role": payload.get("role", "authenticated"),
        }
    except jwt.InvalidTokenError:
        return None


def is_allowed(email: str) -> bool:
    """Check if email is in allowlist or matches allowed domain."""
    email_lower = email.lower()
    
    # Check explicit allowlist first
    if ALLOWED_USERS and ALLOWED_USERS[0]:
        return email_lower in [u.lower().strip() for u in ALLOWED_USERS]
    
    # Fall back to domain check
    if ALLOWED_DOMAIN:
        return email_lower.endswith(f"@{ALLOWED_DOMAIN.lower()}")
    
    return True  # No restrictions if neither is set


def get_token(request: Request) -> Optional[str]:
    """Extract token from cookie or Authorization header."""
    # Try cookie first (browser)
    token = request.cookies.get("sb-access-token")
    if token:
        return token

    # Try Authorization header (API clients)
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]

    return None


async def require_auth(request: Request) -> str:
    """FastAPI dependency for protected endpoints."""
    token = get_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return user["email"]
```

### Usage

```python
from fastapi import APIRouter, Depends
from auth import require_auth

router = APIRouter()

@router.get("/api/protected")
async def protected(user_email: str = Depends(require_auth)):
    return {"message": f"Hello, {user_email}"}
```

---

## Next.js / React Pattern

Using `@supabase/ssr` for App Router.

### Installation

```bash
npm install @supabase/supabase-js @supabase/ssr
```

### lib/supabase/server.ts

```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options)
          })
        },
      },
    }
  )
}
```

### lib/supabase/client.ts

```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### middleware.ts

```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          response = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Redirect to login if not authenticated
  if (!user && !request.nextUrl.pathname.startsWith('/login')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return response
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|api/health).*)'],
}
```

---

## Vanilla JavaScript Pattern

For static sites or simple frontends.

### login.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <button id="google-btn">Sign in with Google</button>
    <button id="email-btn">Sign in with Email</button>

    <script>
        const SUPABASE_URL = 'YOUR_SUPABASE_URL';
        const SUPABASE_ANON_KEY = 'YOUR_ANON_KEY';

        // Handle logout redirect
        const params = new URLSearchParams(window.location.search);
        if (params.get('logout') === '1') {
            const ref = SUPABASE_URL.replace('https://', '').split('.')[0];
            localStorage.removeItem(`sb-${ref}-auth-token`);
            document.cookie = 'sb-access-token=; path=/; max-age=0';
            window.history.replaceState({}, '', '/login');
        }

        const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

        // Auth state listener
        sb.auth.onAuthStateChange((event, session) => {
            if (event === 'SIGNED_IN' && session) {
                document.cookie = `sb-access-token=${session.access_token}; path=/; SameSite=Lax`;
                window.location.href = '/';
            }
        });

        // Check existing session
        sb.auth.getSession().then(({ data: { session } }) => {
            if (session) {
                document.cookie = `sb-access-token=${session.access_token}; path=/; SameSite=Lax`;
                window.location.href = '/';
            }
        });

        // Sign in handlers
        document.getElementById('google-btn').onclick = () => {
            sb.auth.signInWithOAuth({
                provider: 'google',
                options: { redirectTo: window.location.origin }
            });
        };
    </script>
</body>
</html>
```

---

## Development Bypass

Optional: Skip auth in development for faster iteration.

```python
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
DEV_USER = os.getenv("DEV_USER", "dev@localhost")

async def require_auth(request: Request) -> str:
    # Dev bypass
    if ENVIRONMENT == "development":
        return DEV_USER

    # Normal auth flow...
```

**Warning**: Never deploy with `ENVIRONMENT=development` in production.
