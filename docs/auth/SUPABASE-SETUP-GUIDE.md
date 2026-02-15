# Supabase Setup Guide

How to set up Supabase authentication for a new tool or join an existing project.

## Option A: Join Existing Project (Recommended)

If your team shares a single Supabase project for centralized user management, join the existing one.

### Get Credentials

1. Go to `https://supabase.com/dashboard/project/your-project-id`
2. Navigate to **Settings > API**
3. Copy:
   - **Project URL**: `https://your-project-id.supabase.co`
   - **Anon Key**: Under "Project API keys" (safe for client-side)
   - **JWT Secret**: Under "JWT Settings" > Legacy JWT Secret tab

### Add Your App's URLs

1. Go to **Authentication > URL Configuration**
2. Add your production URL to **Redirect URLs**:
   ```
   https://your-app-production.up.railway.app
   ```
3. For local dev, also add:
   ```
   http://localhost:8000
   http://localhost:8501
   ```

### Note on Site URL
The **Site URL** is shared across all apps. It determines the default OAuth redirect. For multi-app setups, production OAuth works reliably; localhost OAuth may redirect to the Site URL app.

---

## Option B: Create New Project

Only needed if you require isolated user management.

### 1. Create Account & Project

1. Go to [supabase.com](https://supabase.com) and sign up
2. Create new project with a descriptive name
3. Choose a region close to your users
4. Set a secure database password (save it)

### 2. Enable Auth Providers

**Authentication > Providers:**

- **Email**: Enable by default
- **Google OAuth** (recommended):
  1. Go to [Google Cloud Console](https://console.cloud.google.com)
  2. Create OAuth 2.0 credentials
  3. Add authorized redirect URI: `https://<project-ref>.supabase.co/auth/v1/callback`
  4. Copy Client ID and Secret to Supabase

### 3. Configure URLs

**Authentication > URL Configuration:**

- **Site URL**: Your primary production URL
- **Redirect URLs**: All environments that need OAuth
  ```
  https://your-app.up.railway.app
  http://localhost:8000
  http://localhost:8501
  ```

### 4. Domain Restriction (Optional)

To restrict to your company's email domain, handle in application code:

```python
# FastAPI example
if not email.endswith('@your-company.com'):
    raise HTTPException(403, "Only @your-company.com emails allowed")
```

```javascript
// Frontend example
if (!email.toLowerCase().endsWith('@your-company.com')) {
    showError('Only @your-company.com emails are allowed');
    return;
}
```

---

## Environment Variables

### For Railway Deployment

Add these in Railway dashboard > Variables:

```bash
# Required
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=<your-anon-key>

# For FastAPI with local JWT validation
SUPABASE_JWT_SECRET=<your-jwt-secret>

# Optional: Production mode (disables dev bypass)
ENVIRONMENT=production
```

### For Local Development

Create `.env.local` (gitignored):

```bash
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=<your-anon-key>
SUPABASE_JWT_SECRET=<your-jwt-secret>

# Enable localhost auth bypass
ENVIRONMENT=development
DEVELOPER_HOME_IP=<your-wsl-ip>  # Get with: hostname -I
```

---

## Verification Checklist

After setup, verify:

- [ ] Can access Supabase dashboard
- [ ] Environment variables set in Railway
- [ ] Production URL in Redirect URLs
- [ ] OAuth provider configured (if using Google)
- [ ] Test login works in production

---

## Finding Your Credentials

| Credential | Location in Dashboard |
|------------|----------------------|
| Project URL | Settings > API > Project URL |
| Anon Key | Settings > API > Project API keys > anon |
| JWT Secret | Settings > API > JWT Settings > Legacy JWT Secret |
| Service Role Key | Settings > API > Project API keys > service_role (server-side only!) |

**Security Notes:**
- Anon Key is safe for client-side (frontend, Streamlit)
- JWT Secret is for server-side validation only
- Service Role Key bypasses RLS - never expose to client
