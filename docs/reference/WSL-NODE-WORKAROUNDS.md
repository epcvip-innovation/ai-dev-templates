# WSL2 + Node.js Network Issues

**Last Updated:** 2026-01-21

## The Problem

Node.js v20+ fetch (Undici) times out in WSL2 while curl works fine. This also affects:
- Claude Code startup (plugin marketplace clones timing out)
- Git HTTPS operations
- Any external API calls

## Root Cause

Multiple compounding issues in WSL2's default NAT networking:
- Undici's HTTP/2 + connection pooling conflicts with WSL2 virtualized networking
- IPv6/IPv4 "Happy Eyeballs" algorithm hangs on IPv6 attempts
- DNS tunneling can add 5+ second delays
- Known issue: https://github.com/nodejs/undici/issues/2990

---

## Fix 1: Disable HTTP/2 in Node.js (Recommended)

**This is the simplest and most reliable fix.** Add to `~/.bashrc`:
```bash
export UNDICI_NO_HTTP2=1
```

Or per-project in `package.json`:
```json
"scripts": {
  "dev": "UNDICI_NO_HTTP2=1 vite"
}
```

**Why:** Disables HTTP/2 in Node.js undici, avoiding the protocol conflict with WSL2 networking. Works with NAT mode (the default) without additional configuration.

---

## Fix 2: Enable Mirrored Networking (Alternative)

> ⚠️ **Warning:** Mirrored mode can cause Windows DNS resolution failures on some setups. If Windows browsers can't resolve domains after enabling this, switch back to NAT mode.

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

**Why:** Mirrored mode eliminates NAT and can improve VPN compatibility (including Cisco AnyConnect).

**Trade-offs:**
- ✅ May help with VPN issues
- ❌ Can break Windows DNS on some machines
- ❌ More complex than disabling HTTP/2

**Sources:**
- [Microsoft WSL Networking Docs](https://learn.microsoft.com/en-us/windows/wsl/networking)
- [WSL Mirrored Mode Guide](https://windowsforum.com/threads/wsl-networking-in-windows-11-mirrored-mode-and-dns-tunneling-guide.386779/)

**Full .wslconfig reference:** See `~/WSL-CONFIG-REFERENCE.md` for all options with explanations.

---

## Fix 3: Prefer IPv4 Over IPv6

If still having issues after mirrored mode, add to `/etc/gai.conf`:
```
precedence ::ffff:0:0/96  100
```

**Why:** Forces IPv4 preference, avoiding IPv6 connection attempts that hang.

---

## When You'll Hit This

- Claude Code slow startup (140+ seconds)
- Plugin marketplace clone failures
- Supabase/external API calls timing out
- Git HTTPS push/pull hanging
- Any server-side fetch in Next.js/Node.js

---

## Projects with Fix Applied

- `utilities/competitor-analyzer/web/` - Has `UNDICI_NO_HTTP2` in dev script
- `~/.bashrc` - Global `UNDICI_NO_HTTP2=1` export

---

## Related Issues

- [nodejs/undici#2990](https://github.com/nodejs/undici/issues/2990) - Original Undici issue
- [Claude Code WSL2 #4474](https://github.com/anthropics/claude-code/issues/4474) - API timeouts
- [Claude Code WSL2 #9114](https://github.com/anthropics/claude-code/issues/9114) - Startup hangs
- [microsoft/WSL#4285](https://github.com/microsoft/WSL/issues/4285) - DNS stops working

---

## See Also

- `~/WSL-CONFIG-REFERENCE.md` - Complete .wslconfig reference with all options
- [WSL Paths Reference](./WSL-PATHS.md) - Filesystem path guide
- [Cursor WSL Setup](../setup-guides/CURSOR-WSL-SETUP.md) - IDE integration
