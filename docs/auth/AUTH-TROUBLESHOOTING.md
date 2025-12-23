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
