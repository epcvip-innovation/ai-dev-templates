# Access Control Patterns

Control who can access your apps beyond basic authentication.

## Per-App User Allowlist (Recommended)

The most flexible approach: each app maintains its own list of allowed users.

### How It Works

```
User authenticates (Google OAuth, email/password)
         │
         ▼
   Token validated ✓
         │
         ▼
Check ALLOWED_USERS env var
         │
    ┌────┴────┐
    │         │
 In list   Not in list
    │         │
    ▼         ▼
  Allow    "Access Denied"
           (with logout button)
```

### Environment Variable

```bash
# Comma-separated list of allowed emails
ALLOWED_USERS=alice@company.com,bob@company.com,carol@company.com
```

### Implementation (Python)

```python
import os

ALLOWED_USERS = [
    u.strip().lower() 
    for u in os.getenv("ALLOWED_USERS", "").split(",") 
    if u.strip()
]
ALLOWED_DOMAIN = os.getenv("ALLOWED_DOMAIN", "")


def is_user_allowed(email: str) -> bool:
    """Check if user email is allowed to access this app."""
    email_lower = email.lower().strip()
    
    # Check explicit allowlist first
    if ALLOWED_USERS:
        return email_lower in ALLOWED_USERS
    
    # Fall back to domain check
    if ALLOWED_DOMAIN:
        return email_lower.endswith(f"@{ALLOWED_DOMAIN.lower()}")
    
    # No restrictions if neither is configured
    return True
```

### Implementation (TypeScript)

```typescript
const ALLOWED_USERS = (process.env.ALLOWED_USERS || '')
  .split(',')
  .map(u => u.trim().toLowerCase())
  .filter(Boolean);

const ALLOWED_DOMAIN = process.env.ALLOWED_DOMAIN || '';

function isUserAllowed(email: string): boolean {
  const emailLower = email.toLowerCase().trim();
  
  // Check explicit allowlist first
  if (ALLOWED_USERS.length > 0) {
    return ALLOWED_USERS.includes(emailLower);
  }
  
  // Fall back to domain check
  if (ALLOWED_DOMAIN) {
    return emailLower.endsWith(`@${ALLOWED_DOMAIN.toLowerCase()}`);
  }
  
  return true;
}
```

---

## Domain Restriction (Fallback)

Restrict access to a specific email domain.

```bash
# Only allow @yourcompany.com emails
ALLOWED_DOMAIN=yourcompany.com
```

This is typically used as a fallback when `ALLOWED_USERS` is empty.

---

## Access Denied Page

When a user authenticates but isn't in the allowlist, show a friendly message:

### Streamlit

```python
def check_access(email: str) -> bool:
    if not is_user_allowed(email):
        st.error("⛔ Access Denied")
        st.write(f"Your account ({email}) doesn't have access to this app.")
        st.write("Contact your administrator to request access.")
        if st.button("Sign Out"):
            logout()
        st.stop()
        return False
    return True
```

### React/Next.js

```tsx
function AccessDenied({ email, onLogout }: { email: string; onLogout: () => void }) {
  return (
    <div className="access-denied">
      <h1>Access Denied</h1>
      <p>Your account ({email}) doesn't have access to this app.</p>
      <p>Contact your administrator to request access.</p>
      <button onClick={onLogout}>Sign Out</button>
    </div>
  );
}
```

---

## Role-Based Access Control (RBAC)

For more complex permissions, use roles stored in your database.

### Database Schema

```sql
CREATE TABLE user_roles (
  user_id UUID REFERENCES auth.users(id),
  role TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, role)
);

-- Example roles: 'admin', 'editor', 'viewer'
```

### Check Role

```python
async def require_role(request: Request, required_role: str) -> str:
    email = await require_auth(request)
    
    # Query user role from database
    role = await db.get_user_role(email)
    
    if role != required_role and role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires {required_role} role"
        )
    
    return email
```

---

## Comparison

| Approach | Complexity | Best For |
|----------|------------|----------|
| **ALLOWED_USERS** | Simple | Small teams, invite-only apps |
| **ALLOWED_DOMAIN** | Simple | Company-wide internal tools |
| **RBAC** | Medium | Multiple permission levels |
| **Custom policies** | Complex | Enterprise, compliance needs |

---

## Security Tips

1. **Always validate on the server** — client-side checks are bypassable
2. **Log access attempts** — audit trail for denied access
3. **Fail closed** — if unsure, deny access
4. **Separate admin routes** — don't mix admin/user endpoints
5. **Review allowlists regularly** — remove departed users promptly
