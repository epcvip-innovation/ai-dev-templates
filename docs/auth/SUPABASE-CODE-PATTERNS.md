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

Allow localhost/private network access without authentication during development. Uses **TCP peer IP only** (`request.client.host`) for security decisions — never trust forwarded headers (`X-Forwarded-For`) for auth bypass, as they can be spoofed.

> **Security note**: `get_client_ip()` (which reads forwarded headers) is still useful for **audit logging** — worst case an attacker spoofs their own IP in logs. But auth bypass decisions must use the unforgeable TCP peer IP.

```python
# In auth_supabase.py
ENVIRONMENT = os.getenv("ENVIRONMENT", "production").lower()
DEVELOPER_HOME_IP = os.getenv("DEVELOPER_HOME_IP")


def is_development_environment() -> bool:
    """Check if running in development mode."""
    return ENVIRONMENT in ["development", "dev", "local"]


def get_dev_persona() -> tuple[str, str]:
    """Dev bypass persona from env vars. Returns (email, role).
    Role is normalized (strip + lowercase) to prevent casing/whitespace lockouts.
    """
    email = os.getenv("DEV_EMAIL", "").strip() or "dev@localhost"
    role = os.getenv("DEV_ROLE", "").strip().lower() or "admin"
    return email, role


def get_client_ip(request: Request) -> str:
    """Get real client IP, handling proxies (Railway, Cloudflare, etc.)

    NOTE: Only use for audit logging, NOT for auth decisions.
    Forwarded headers can be spoofed by attackers.
    """
    forwarded_for = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    if forwarded_for:
        return forwarded_for
    real_ip = request.headers.get("x-real-ip", "").strip()
    if real_ip:
        return real_ip
    return getattr(request.client, "host", "")


def should_bypass_auth(request: Request) -> bool:
    """
    Check if authentication should be bypassed for local development.

    Requires BOTH:
    - ENVIRONMENT=development (or dev/local)
    - Request from localhost, local network, or DEVELOPER_HOME_IP

    Uses TCP peer IP (request.client.host) — unforgeable.
    Does NOT trust X-Forwarded-For or X-Real-IP headers.
    """
    client_host = getattr(request.client, "host", "")
    # Use TCP peer IP only (unforgeable) — not forwarded headers which can be spoofed
    real_ip = getattr(request.client, "host", "")

    # Check for localhost variants
    is_localhost = (
        client_host in ["127.0.0.1", "::1", "localhost"]
        or client_host.startswith("127.")
        or real_ip in ["127.0.0.1", "::1", "localhost"]
        or real_ip.startswith("127.")
    )

    # Check for local network IPs (192.168.x.x, 172.16-31.x.x, 10.x.x.x)
    def is_private_ip(ip):
        if not ip or not ip[0].isdigit():
            return False
        if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("127."):
            return True
        if ip.startswith("172."):
            try:
                second_octet = int(ip.split(".")[1])
                return 16 <= second_octet <= 31
            except (ValueError, IndexError):
                return False
        return False

    is_local_network = is_private_ip(client_host) or is_private_ip(real_ip)

    if DEVELOPER_HOME_IP:
        is_authorized_ip = real_ip == DEVELOPER_HOME_IP or client_host == DEVELOPER_HOME_IP
    else:
        is_authorized_ip = False

    is_dev_env = is_development_environment()

    bypass_allowed = is_dev_env and (is_localhost or is_local_network or is_authorized_ip)

    if bypass_allowed:
        logger.info(f"Auth bypass: client={client_host}, real_ip={real_ip}, "
                     f"localhost={is_localhost}, local_net={is_local_network}, "
                     f"authorized={is_authorized_ip}")

    return bypass_allowed


async def require_authentication(request: Request) -> str:
    # Dev bypass
    if should_bypass_auth(request):
        dev_email, _ = get_dev_persona()
        return dev_email

    # Normal auth flow...
```

### Deployment Checklist

When deploying this pattern across your FastAPI services, verify each service has:

| Checkpoint | Description |
|------------|-------------|
| TCP Peer IP | Uses `request.client.host` (not forwarded headers) for auth bypass |
| Private IP Check | Validates localhost + private IP ranges |
| `get_dev_persona()` | Returns dev email/role from env vars |

Track your services in a table like:

| Service | Auth File | TCP Peer IP | Private IP Check | `get_dev_persona()` |
|---------|-----------|:-----------:|:----------------:|:-------------------:|
| my-api | `auth_supabase.py` | Yes | Yes | Yes |

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
