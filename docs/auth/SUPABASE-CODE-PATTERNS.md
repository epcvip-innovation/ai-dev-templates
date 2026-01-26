# Supabase Code Patterns

Generic authentication code patterns for different frameworks. These are **copy-paste starting points** - customize for your project's access control requirements (RBAC tables, allowed domains, etc.).

---

Proven authentication patterns for different frameworks.

## Streamlit Pattern

Uses `streamlit_supabase_auth` library for simple OAuth integration.

### Installation
```bash
pip install streamlit-supabase-auth supabase
```

### Basic Usage
```python
import os
import streamlit as st
from streamlit_supabase_auth import login_form, logout_button

st.set_page_config(page_title="My App", layout="wide")

# Auth gate - blocks until authenticated
session = login_form(
    url=os.getenv("SUPABASE_URL"),
    apiKey=os.getenv("SUPABASE_ANON_KEY"),
    providers=["google"],  # OAuth providers
)

if not session:
    st.stop()

# User is authenticated
user_email = session["user"]["email"]

# Sidebar with logout
with st.sidebar:
    st.write(f"**{user_email}**")
    logout_button()
    st.divider()

# Your app code here
st.title("Welcome!")
```

---

## FastAPI Pattern

Uses local JWT validation with PyJWT for performance (~1ms vs ~600ms remote).

### Installation
```bash
pip install PyJWT fastapi
```

### auth_supabase.py
```python
"""
Supabase Auth for FastAPI
Validates JWTs locally using SUPABASE_JWT_SECRET
"""
import os
import jwt
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status

# Configuration
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")
ALLOWED_DOMAIN = os.getenv("ALLOWED_DOMAIN", "")
JWT_ALGORITHM = "HS256"

def verify_supabase_token(token: str) -> Optional[Dict[str, Any]]:
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

        # Validate email domain
        email = payload.get("email", "")
        if not email.lower().endswith(f"@{ALLOWED_DOMAIN}"):
            return None

        return {
            "user_id": payload.get("sub"),
            "email": email,
            "role": payload.get("role", "authenticated"),
        }
    except jwt.InvalidTokenError:
        return None

def get_token_from_request(request: Request) -> Optional[str]:
    """Extract token from cookie or Authorization header."""
    # Try cookie first
    token = request.cookies.get("sb-access-token")
    if token:
        return token

    # Try Authorization header
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]

    return None

async def require_authentication(request: Request) -> str:
    """FastAPI dependency for protected endpoints."""
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    user = verify_supabase_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return user["email"]
```

### Usage in Routes
```python
from fastapi import APIRouter, Depends
from auth_supabase import require_authentication

router = APIRouter()

@router.get("/api/protected")
async def protected_endpoint(user_email: str = Depends(require_authentication)):
    return {"message": f"Hello, {user_email}"}
```

---

## Frontend Login Page Pattern

Vanilla JavaScript with Supabase JS client.

### login.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <button onclick="signInWithGoogle()">Sign in with Google</button>

    <script>
        const SUPABASE_URL = '{{SUPABASE_URL}}';
        const SUPABASE_ANON_KEY = '{{SUPABASE_ANON_KEY}}';

        // IMPORTANT: Check for logout BEFORE creating client
        const urlParams = new URLSearchParams(window.location.search);
        const isLoggingOut = urlParams.get('logout') === '1';

        if (isLoggingOut) {
            // Clear localStorage BEFORE Supabase can restore session
            const projectRef = SUPABASE_URL.replace('https://', '').split('.')[0];
            localStorage.removeItem(`sb-${projectRef}-auth-token`);
            document.cookie = 'sb-access-token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
            window.history.replaceState({}, document.title, '/login');
        }

        // NOW create client
        const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

        // Only register auth listener if NOT logging out
        if (!isLoggingOut) {
            sb.auth.onAuthStateChange((event, session) => {
                if (event === 'SIGNED_IN' && session) {
                    document.cookie = `sb-access-token=${session.access_token}; path=/; SameSite=Lax`;
                    window.location.href = '/';
                }
            });

            // Check existing session
            (async () => {
                const { data: { session } } = await sb.auth.getSession();
                if (session) {
                    document.cookie = `sb-access-token=${session.access_token}; path=/; SameSite=Lax`;
                    window.location.href = '/';
                }
            })();
        }

        async function signInWithGoogle() {
            await sb.auth.signInWithOAuth({
                provider: 'google',
                options: { redirectTo: window.location.origin }
            });
        }
    </script>
</body>
</html>
```

### Logout Function (in main app)
```javascript
async function logout() {
    await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' });
    // Pass logout flag to clear Supabase session
    window.location.href = '/login?logout=1';
}
```

---

## Development Bypass Pattern

Allow localhost access without authentication during development.

```python
# In auth_supabase.py
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
DEVELOPER_HOME_IP = os.getenv("DEVELOPER_HOME_IP", "")

def should_bypass_auth(request: Request) -> bool:
    """Check if request should bypass authentication."""
    if ENVIRONMENT != "development":
        return False

    if not DEVELOPER_HOME_IP:
        return False

    client_ip = request.client.host if request.client else ""
    return client_ip == DEVELOPER_HOME_IP

async def require_authentication(request: Request) -> str:
    # Dev bypass
    if should_bypass_auth(request):
        return "dev@localhost"

    # Normal auth flow...
```

---

## Cookie vs Header Authentication

| Method | Use Case | Example |
|--------|----------|---------|
| Cookie | Browser-based apps, SSR | `sb-access-token` cookie |
| Header | API clients, mobile apps | `Authorization: Bearer <token>` |

The FastAPI pattern above supports both automatically.

---

## Railway Environment Variables

```bash
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=<anon-key>
SUPABASE_JWT_SECRET=<jwt-secret>

# Access control
ALLOWED_USERS=user1@domain.com,user2@domain.com

# Production mode
ENVIRONMENT=production
```

---

## Note

For comprehensive auth templates, see [templates/auth/](../../templates/auth/).
