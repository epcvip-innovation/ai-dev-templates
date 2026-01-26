# Clerk Authentication Patterns

Clerk is a modern auth provider with excellent developer experience and built-in UI components.

## When to Use Clerk

| Use Case | Clerk | Supabase |
|----------|-------|----------|
| Need built-in UI (modals, forms) | ✅ Best | ⚠️ Manual |
| Full-stack Next.js/React | ✅ Excellent | ✅ Good |
| Python backend (FastAPI, Streamlit) | ⚠️ Limited | ✅ Better |
| Shared auth across many tools | ⚠️ Separate | ✅ Better |
| Free tier | 10K MAU | 50K MAU |
| Custom styling | ✅ Theme API | ⚠️ Manual |

## Setup Checklist

### 1. Create Clerk Application

1. Go to [clerk.com](https://clerk.com) → Create Application
2. Configure sign-in options (email, Google, GitHub)
3. Get your keys from Dashboard > API Keys:
   - **Publishable Key**: `pk_test_...` or `pk_live_...`
   - **Secret Key**: `sk_test_...` or `sk_live_...`

### 2. Environment Variables

```bash
# Required
CLERK_PUBLISHABLE_KEY=pk_live_xxxxx
CLERK_SECRET_KEY=sk_live_xxxxx

# Optional
CLERK_SIGN_IN_URL=/sign-in
CLERK_SIGN_UP_URL=/sign-up
CLERK_AFTER_SIGN_IN_URL=/
CLERK_AFTER_SIGN_UP_URL=/
```

---

## Frontend Pattern: Vanilla JavaScript (CDN)

For static sites or vanilla JS apps without a build step.

### HTML Setup

```html
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
</head>
<body>
    <div id="app">
        <button id="login-btn">Sign In</button>
        <button id="signup-btn">Sign Up</button>
        <button id="logout-btn" style="display:none">Sign Out</button>
        <div id="user-info"></div>
    </div>

    <!-- Clerk SDK - key injected by server or hardcoded -->
    <script
        async
        crossorigin="anonymous"
        data-clerk-publishable-key="__CLERK_PUBLISHABLE_KEY__"
        src="https://cdn.jsdelivr.net/npm/@clerk/clerk-js@5/dist/clerk.browser.js"
    ></script>

    <script type="module" src="/app.js"></script>
</body>
</html>
```

### JavaScript (app.js)

```javascript
let clerk = null;

// Initialize Clerk
async function initClerk() {
    await new Promise((resolve) => {
        const check = () => {
            if (window.Clerk?.loaded) {
                resolve();
            } else if (window.Clerk) {
                window.Clerk.load().then(resolve).catch(resolve);
            } else {
                setTimeout(check, 100);
            }
        };
        check();
    });

    clerk = window.Clerk;
    setupAuthListener();
    return clerk;
}

// Listen for auth changes
function setupAuthListener() {
    clerk.addListener(({ user }) => {
        if (user) {
            document.getElementById('login-btn').style.display = 'none';
            document.getElementById('signup-btn').style.display = 'none';
            document.getElementById('logout-btn').style.display = 'block';
            document.getElementById('user-info').textContent = 
                `Welcome, ${user.firstName || user.primaryEmailAddress?.emailAddress}`;
        } else {
            document.getElementById('login-btn').style.display = 'block';
            document.getElementById('signup-btn').style.display = 'block';
            document.getElementById('logout-btn').style.display = 'none';
            document.getElementById('user-info').textContent = '';
        }
    });
}

// Dark theme for Clerk modals
const clerkAppearance = {
    variables: {
        colorPrimary: '#6366f1',
        colorBackground: '#1a1a2e',
        colorInputBackground: '#16162a',
        colorText: '#ffffff',
    },
};

// Auth actions
function openLogin() {
    clerk?.openSignIn({ appearance: clerkAppearance });
}

function openSignup() {
    clerk?.openSignUp({ appearance: clerkAppearance });
}

async function logout() {
    await clerk?.signOut();
}

// Event listeners
document.getElementById('login-btn').addEventListener('click', openLogin);
document.getElementById('signup-btn').addEventListener('click', openSignup);
document.getElementById('logout-btn').addEventListener('click', logout);

// Initialize on load
initClerk();
```

---

## Backend Pattern: Express + Node.js

Server-side validation with `@clerk/clerk-sdk-node`.

### Installation

```bash
npm install @clerk/clerk-sdk-node express
```

### Server Setup (index.ts)

```typescript
import express from 'express';
import { ClerkExpressRequireAuth, clerkClient } from '@clerk/clerk-sdk-node';

const app = express();

// Clerk publishable key for client-side
const CLERK_PUBLISHABLE_KEY = process.env.CLERK_PUBLISHABLE_KEY || '';

// Inject key into HTML
app.get('/', (req, res) => {
    const html = fs.readFileSync('public/index.html', 'utf-8')
        .replace('__CLERK_PUBLISHABLE_KEY__', CLERK_PUBLISHABLE_KEY);
    res.type('html').send(html);
});

// Config endpoint for client
app.get('/api/config', (req, res) => {
    res.json({
        clerk: { publishableKey: CLERK_PUBLISHABLE_KEY }
    });
});

// Protected endpoint using Clerk middleware
app.get('/api/protected', 
    ClerkExpressRequireAuth(),
    (req, res) => {
        const userId = req.auth.userId;
        res.json({ message: `Hello user ${userId}` });
    }
);

// Get user details
app.get('/api/user/:userId', 
    ClerkExpressRequireAuth(),
    async (req, res) => {
        try {
            const user = await clerkClient.users.getUser(req.params.userId);
            res.json({
                id: user.id,
                email: user.primaryEmailAddress?.emailAddress,
                name: user.firstName,
            });
        } catch (error) {
            res.status(404).json({ error: 'User not found' });
        }
    }
);

app.listen(3000);
```

---

## Frontend Pattern: Next.js (App Router)

Using `@clerk/nextjs` for full integration.

### Installation

```bash
npm install @clerk/nextjs
```

### middleware.ts

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isPublicRoute = createRouteMatcher([
    '/',
    '/sign-in(.*)',
    '/sign-up(.*)',
    '/api/health',
]);

export default clerkMiddleware(async (auth, request) => {
    if (!isPublicRoute(request)) {
        await auth.protect();
    }
});

export const config = {
    matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'],
};
```

### app/layout.tsx

```tsx
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <ClerkProvider>
            <html lang="en">
                <body>{children}</body>
            </html>
        </ClerkProvider>
    );
}
```

### Components

```tsx
import { SignInButton, SignUpButton, UserButton, SignedIn, SignedOut } from '@clerk/nextjs';

export function Header() {
    return (
        <header>
            <SignedOut>
                <SignInButton />
                <SignUpButton />
            </SignedOut>
            <SignedIn>
                <UserButton />
            </SignedIn>
        </header>
    );
}
```

### Server Component (get current user)

```tsx
import { currentUser } from '@clerk/nextjs/server';

export default async function DashboardPage() {
    const user = await currentUser();
    
    if (!user) {
        return <div>Not signed in</div>;
    }

    return <div>Hello, {user.firstName}</div>;
}
```

---

## Programmatic Auth (No Hosted UI)

For custom login forms instead of Clerk's modals.

```javascript
async function login(email, password) {
    const signIn = await clerk.client.signIn.create({
        identifier: email,
        password,
    });

    if (signIn.status !== 'complete') {
        throw new Error('Sign in failed');
    }

    await clerk.setActive({ session: signIn.createdSessionId });
    return clerk.user;
}

async function signup(email, password, firstName) {
    const signUp = await clerk.client.signUp.create({
        emailAddress: email,
        password,
        firstName,
    });

    // Handle email verification if required
    if (signUp.status === 'missing_requirements') {
        await signUp.prepareEmailAddressVerification();
        // Show verification code input...
    }

    if (signUp.status === 'complete') {
        await clerk.setActive({ session: signUp.createdSessionId });
    }

    return clerk.user;
}
```

---

## Password Management

```javascript
// Request password reset (via email)
async function requestPasswordReset(email) {
    const signIn = await clerk.client.signIn.create({
        identifier: email,
        strategy: 'reset_password_email_code',
    });
    // User receives email with code
}

// Update password (when logged in)
async function updatePassword(currentPassword, newPassword) {
    await clerk.user.updatePassword({
        currentPassword,
        newPassword,
    });
}
```

---

## Comparison: Clerk vs Supabase

| Feature | Clerk | Supabase Auth |
|---------|-------|---------------|
| **Hosted UI components** | ✅ Built-in modals | ❌ Build your own |
| **React/Next.js support** | ✅ Excellent | ✅ Good |
| **Python SDK** | ❌ None | ✅ Full support |
| **Database included** | ❌ Separate (Neon, etc.) | ✅ PostgreSQL included |
| **Pricing** | 10K MAU free | 50K MAU free |
| **Self-host option** | ❌ No | ✅ Yes |
| **Multi-tenancy** | ✅ Organizations | ⚠️ Manual |

---

## Tips

1. **Server-side key injection**: Never expose `CLERK_SECRET_KEY` to the client
2. **Use middleware**: Protect routes at the edge, not in individual handlers
3. **Session tokens**: Clerk handles cookies/tokens automatically
4. **Theming**: Use `appearance` prop to match your app's style
5. **Webhooks**: Use Clerk webhooks for user lifecycle events (create, delete)
