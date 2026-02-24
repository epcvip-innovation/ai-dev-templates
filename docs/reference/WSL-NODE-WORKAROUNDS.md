# WSL2 + Node.js Network Issues

**Last Updated:** 2026-02-24

## The Problem

Node.js v20+ tools (including Claude Code) experience timeouts and hangs in WSL2 while `curl` works fine. Symptoms include:
- Claude Code startup hangs (120+ seconds)
- `fetch()` calls timing out intermittently
- Git HTTPS operations hanging
- External API calls failing

## Root Causes

There are **two separate issues** that often appear together:

### 1. WindowsPowerShell in WSL PATH (Claude Code hangs)

Windows appends its own PATH entries to WSL, including `WindowsPowerShell`. When Claude Code starts, it resolves executables and gets stuck on Windows paths that don't respond correctly from the Linux side.

- **Canonical issue:** [claude-code#619](https://github.com/anthropics/claude-code/issues/619) (still open)
- **Confirmed fix:** Filter PowerShell from PATH (see Fix 1 below)

### 2. IPv6 Happy Eyeballs timeout (Node.js fetch timeouts)

Node.js uses the "Happy Eyeballs" algorithm ([RFC 8305](https://datatracker.ietf.org/doc/html/rfc8305)) to race IPv6 and IPv4 connections. The default fallback timeout is 250ms, which is too short for WSL2's NAT networking where IPv6 attempts hang longer.

- **Original issue:** [nodejs/undici#2990](https://github.com/nodejs/undici/issues/2990) (closed March 2024 — root cause identified)
- **Node.js fix available since:** Node 20.13.0 / Node 22.1.0 (configurable timeout via `NODE_OPTIONS`)

> **Note on `UNDICI_NO_HTTP2=1`:** This was previously recommended as the primary fix. However, Node.js `fetch()` does not use HTTP/2 by default (it's opt-in via `allowH2`). The `UNDICI_NO_HTTP2` flag is harmless but likely not addressing the actual root cause for most users. The fixes below target the real issues.

---

## Fix 1: Remove WindowsPowerShell from PATH (Essential)

Add to `~/.bashrc`:

```bash
# Fix: Remove WindowsPowerShell from PATH (causes Claude Code hangs in WSL2)
# See: https://github.com/anthropics/claude-code/issues/619
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v 'WindowsPowerShell' | tr '\n' ':' | sed 's/:$//')
```

**Verify:**

```bash
echo "$PATH" | tr ':' '\n' | grep -i powershell
# Should return nothing
```

---

## Fix 2: Increase Happy Eyeballs Timeout (Essential)

Add to `~/.bashrc`:

```bash
# Fix: Increase Happy Eyeballs timeout for WSL2 NAT networking
# See: https://github.com/nodejs/undici/issues/2990
export NODE_OPTIONS="--network-family-autoselection-attempt-timeout=1000"
```

This increases the IPv6-to-IPv4 fallback timeout from 250ms to 1000ms, giving WSL2's NAT networking enough time to respond.

**Requires:** Node.js 20.13.0+ or Node.js 22.1.0+

**Verify:**

```bash
echo $NODE_OPTIONS
# Should show: --network-family-autoselection-attempt-timeout=1000
```

Or per-project in `package.json`:

```json
"scripts": {
  "dev": "NODE_OPTIONS='--network-family-autoselection-attempt-timeout=1000' vite"
}
```

---

## Fix 3: Prefer IPv4 Over IPv6 (If Fix 2 is insufficient)

If you're still seeing timeouts after applying Fix 2, force IPv4 preference system-wide:

```bash
sudo bash -c 'echo "precedence ::ffff:0:0/96  100" >> /etc/gai.conf'
```

**Why:** Skips IPv6 connection attempts entirely, avoiding the timeout altogether.

---

## Fix 4: Enable Mirrored Networking (Optional — for VPN users)

> **Warning:** Mirrored mode can cause Windows DNS resolution failures on some setups. Only use this if you need VPN compatibility (e.g., Cisco AnyConnect).

Edit `C:\Users\<username>\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
dnsTunneling=true
```

Then restart WSL:

```powershell
wsl --shutdown
```

**Trade-offs:**
- May help with VPN issues
- Can break Windows DNS on some machines
- Adds more configuration complexity

**Sources:**
- [Microsoft WSL Networking Docs](https://learn.microsoft.com/en-us/windows/wsl/networking)

---

## Fix 5: Keep UNDICI_NO_HTTP2 (Defense-in-depth)

This flag is harmless and may help with edge cases where third-party libraries enable HTTP/2 explicitly:

```bash
export UNDICI_NO_HTTP2=1
```

It does **not** affect standard `fetch()` calls (which use HTTP/1.1 by default). Keep it if you already have it, but it is not the primary fix.

---

## When You'll Hit This

- Claude Code startup hangs (120+ seconds) — Fix 1
- `fetch()` timeouts in Node.js — Fix 2
- Supabase/external API calls timing out — Fix 2
- Git HTTPS push/pull hanging — Fix 2 or Fix 3
- Any server-side fetch in Next.js/Node.js — Fix 2

---

## Quick Setup (Copy-Paste)

Apply all recommended fixes at once:

```bash
cat >> ~/.bashrc << 'FIXES'

# === WSL2 networking fixes ===
# Fix 1: Remove WindowsPowerShell from PATH (causes Claude Code hangs)
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v 'WindowsPowerShell' | tr '\n' ':' | sed 's/:$//')

# Fix 2: Increase IPv6 fallback timeout (prevents Node.js fetch timeouts)
export NODE_OPTIONS="--network-family-autoselection-attempt-timeout=1000"

# Fix 3: Disable HTTP/2 in Node.js undici (defense-in-depth fallback)
export UNDICI_NO_HTTP2=1
FIXES

source ~/.bashrc
```

---

## Related Issues

- [claude-code#619](https://github.com/anthropics/claude-code/issues/619) — Canonical Claude Code WSL hang issue (open)
- [nodejs/undici#2990](https://github.com/nodejs/undici/issues/2990) — IPv6 Happy Eyeballs timeout (closed, root cause confirmed)
- [nodejs/undici#2750](https://github.com/nodejs/undici/issues/2750) — HTTP/2 default support (open — confirms HTTP/2 is still opt-in)
- [Claude Code WSL2 #4474](https://github.com/anthropics/claude-code/issues/4474) — API timeouts (closed)
- [Claude Code WSL2 #9114](https://github.com/anthropics/claude-code/issues/9114) — Startup hangs (closed, dup of #619)
- [microsoft/WSL#4285](https://github.com/microsoft/WSL/issues/4285) — DNS stops working

---

## See Also

- [Microsoft .wslconfig Reference](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) — Official WSL2 configuration docs
- [WSL Paths Reference](./WSL-PATHS.md) — Filesystem path guide
- [Cursor WSL Setup](../setup-guides/CURSOR-WSL-SETUP.md) — IDE integration
