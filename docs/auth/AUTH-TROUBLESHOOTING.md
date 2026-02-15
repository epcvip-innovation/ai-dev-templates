# Auth Troubleshooting

Common authentication issues and their solutions.

---

## OAuth Redirects to Wrong App

### Symptom
Google OAuth redirects to a different app (e.g., athena-usage-monitor) instead of your app.

### Cause
Supabase's **Site URL** setting determines the default OAuth redirect destination. When multiple apps share a Supabase project, localhost OAuth often redirects to the Site URL app.

### Solutions

**Solution 1: Test in Production (Recommended)**
- Deploy your app to Railway first
- Add production URL to Supabase Redirect URLs
- OAuth works reliably in production-to-production flow

**Solution 2: Use Email/Password for Local Testing**
- Email/password login doesn't use OAuth redirect
- Works locally without Site URL conflicts
- OAuth can be tested after production deployment

**Solution 3: Temporarily Change Site URL**
- Change Supabase Site URL to your app's URL
- Test OAuth
- Change back (may break other apps temporarily)

### Prevention
For multi-app setups, accept that localhost OAuth may not work perfectly. Design your testing workflow around:
1. Email/password for local auth testing
2. OAuth testing in production environment

---

## OAuth Callback Fails (PKCE "missing code" or Silent Redirect)

### Symptom
After Google login, the callback fails with "missing code" error, fails silently, or redirects back to login page.

### Cause
**Server-side code exchange without `code_verifier`**. PKCE (Proof Key for Code Exchange) requires:
1. Client generates `code_verifier` and stores it in localStorage
2. Client sends `code_challenge` (hash of verifier) to auth server
3. After redirect, the **same client** must exchange `code` + `code_verifier`

If the server tries to exchange the authorization code directly with Supabase's `/auth/v1/token` endpoint, it doesn't have access to the `code_verifier` stored in the browser, causing the exchange to fail.

### Wrong Pattern (Server-Side Exchange)
```typescript
// ❌ BROKEN - Server can't access client's code_verifier
app.get('/auth/callback', async (req, res) => {
  const { code } = req.query;
  const response = await fetch(`${SUPABASE_URL}/auth/v1/token?grant_type=authorization_code`, {
    body: JSON.stringify({ code }),  // Missing code_verifier!
  });
});
```

### Correct Pattern (Recommended)

```javascript
// ✅ Let Supabase handle PKCE exchange automatically
const { data: { session }, error } = await sb.auth.getSession();

if (error) {
  console.error('[Auth] Session error:', error);
  window.location.href = '/login?error=oauth_failed';
  return;
}

if (session) {
  // User is authenticated - proceed with app logic
}
```

**Why `getSession()` is preferred:**
- Handles PKCE state management internally
- Works gracefully when users switch accounts mid-flow (no stale code_verifier issues)
- Simpler code - no need to parse URL params manually
- Matches OAuth 2.1 best practices (2026)
- Recommended as the standard pattern across all repos

**Alternative: Explicit exchange (legacy)**
```javascript
// ⚠️ Only use if you need fine-grained control over the exchange
const code = new URLSearchParams(window.location.search).get('code');
if (code) {
  const { data, error } = await sb.auth.exchangeCodeForSession(code);
}
```
This approach is more prone to PKCE state misalignment when users switch Google accounts during the OAuth flow.

### Solution
1. Serve an HTML page at `/auth/callback` (don't handle exchange server-side)
2. Load Supabase JS SDK in that HTML page
3. Use `getSession()` - SDK handles PKCE automatically
4. Never exchange the authorization code server-side without the code_verifier

---

## Logout Doesn't Work (Redirects Back to Dashboard)

### Symptom
Clicking logout briefly shows login page, then redirects back to dashboard.

### Cause
**Race condition**: Supabase client auto-restores session from localStorage when created. The `onAuthStateChange` listener fires with `SIGNED_IN` before your logout code can execute `signOut()`.

### Solution
Clear localStorage BEFORE creating the Supabase client:

```javascript
// Check for logout FIRST, BEFORE creating Supabase client
const urlParams = new URLSearchParams(window.location.search);
const isLoggingOut = urlParams.get('logout') === '1';

if (isLoggingOut) {
    // Clear localStorage BEFORE client can restore session
    const projectRef = SUPABASE_URL.replace('https://', '').split('.')[0];
    localStorage.removeItem(`sb-${projectRef}-auth-token`);
    document.cookie = 'sb-access-token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    window.history.replaceState({}, document.title, '/login');
}

// NOW create client (no session to restore)
const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Only register auth listener if NOT logging out
if (!isLoggingOut) {
    sb.auth.onAuthStateChange((event, session) => {
        // ... handle auth state
    });
}
```

And update logout to pass the flag:
```javascript
window.location.href = '/login?logout=1';
```

---

## JWT Validation Errors

### "Invalid signature" Error

**Cause**: Wrong JWT secret or using wrong key type.

**Solution**:
1. Go to Supabase Dashboard > Settings > API
2. Find "JWT Settings" section
3. Click "Legacy JWT Secret" tab
4. Copy the full secret (not the public key)

### "Token expired" Error

**Cause**: Supabase tokens expire after 1 hour by default.

**Solution**:
- Frontend: Supabase client handles refresh automatically
- Backend: Check for expired tokens and return 401

### "Invalid audience" Error

**Cause**: Token was issued for different audience.

**Solution**: Ensure JWT decode includes correct audience:
```python
jwt.decode(token, secret, algorithms=["HS256"], audience="authenticated")
```

---

## Cookie Not Being Set

### Symptom
Login succeeds but subsequent requests fail with 401.

### Causes & Solutions

**Cause 1: SameSite attribute**
```javascript
// Wrong
document.cookie = `sb-access-token=${token}; path=/`;

// Correct
document.cookie = `sb-access-token=${token}; path=/; SameSite=Lax`;
```

**Cause 2: Secure flag on HTTP**
Don't use `Secure` flag for localhost:
```javascript
// For production (HTTPS)
document.cookie = `token=${token}; path=/; SameSite=Lax; Secure`;

// For localhost (HTTP)
document.cookie = `token=${token}; path=/; SameSite=Lax`;
```

**Cause 3: Missing credentials in fetch**
```javascript
// Wrong
fetch('/api/endpoint');

// Correct
fetch('/api/endpoint', { credentials: 'include' });
```

---

## JavaScript Variable Naming Conflict

### Symptom
```
SyntaxError: Identifier 'supabase' has already been declared
```

### Cause
Naming your Supabase client `supabase` conflicts with `window.supabase`:
```javascript
// This causes error
const supabase = window.supabase.createClient(...);
```

### Solution
Use a different variable name:
```javascript
// Correct
const sb = window.supabase.createClient(...);
```

---

## Railway Deployment Fails

### "Missing SUPABASE_JWT_SECRET" Error

**Solution**: Add environment variable in Railway dashboard:
1. Go to your service > Variables
2. Add `SUPABASE_JWT_SECRET` with value from Supabase dashboard

### Health Check Fails After Auth Migration

**Cause**: Health endpoint now requires authentication.

**Solution**: Exclude health endpoint from auth:
```python
@app.get("/health")
async def health():  # No auth dependency
    return {"status": "healthy"}
```

---

## Local Development Not Working

### Can't Access App from Browser

**WSL Issue**: Use WSL IP, not localhost:
```bash
# Get your WSL IP
hostname -I

# Start server on that IP
DEVELOPER_HOME_IP=172.17.x.x uvicorn main:app --host 0.0.0.0 --port 8000
```

Access via: `http://172.17.x.x:8000`

### Dev Bypass Not Working

Check all conditions:
1. `ENVIRONMENT=development` is set
2. `DEVELOPER_HOME_IP` matches your actual IP
3. Server is bound to `0.0.0.0`, not `127.0.0.1`

---

## Supabase Dashboard Issues

### Can't Find JWT Secret

1. Go to Settings > API
2. Look for "JWT Settings" section
3. Click "Legacy JWT Secret" tab (not the default view)

### Can't Add Redirect URL

Ensure URL format is correct:
- Include protocol: `https://` or `http://`
- No trailing slash
- Exact match required

---

## Quick Diagnostic Checklist

When auth isn't working, check:

- [ ] Environment variables set correctly?
- [ ] JWT secret is the legacy secret (not public key)?
- [ ] Production URL in Supabase Redirect URLs?
- [ ] Cookie being set with correct attributes?
- [ ] Using `credentials: 'include'` in fetch calls?
- [ ] Health endpoint excluded from auth?
- [ ] For WSL: Using WSL IP, not localhost?
