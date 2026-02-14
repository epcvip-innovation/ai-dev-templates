# Local Network Sharing Guide

[← Back to Main README](../../README.md) | [Multi-Device Workspace →](./MULTI-DEVICE-WORKSPACE.md)

**Last Updated**: February 2026 | **Time Required**: 5-10 minutes

Share your local dev server, mockups, or prototypes with teammates on the same network (or VPN).

---

## Quick Reference

| Stack | Config Location | Key Setting | Command |
|-------|-----------------|-------------|---------|
| **Vite** | `vite.config.ts` | `host: '0.0.0.0'` | `npm run dev` |
| **Streamlit** | CLI flag | `--server.address 0.0.0.0` | `streamlit run app.py --server.address 0.0.0.0` |
| **FastAPI** | CLI flag | `--host 0.0.0.0` | `uvicorn main:app --host 0.0.0.0` |
| **Static HTML** | CLI flag | `--bind 0.0.0.0` | `python3 -m http.server 8000 --bind 0.0.0.0` |

**Get your IP (share this with teammates):**
```bash
hostname -I | awk '{print $1}'
```

---

## Vite (React, Vue, Vanilla JS)

Vite is the recommended approach for any frontend work - mockups, prototypes, or full apps.

### Option A: Configure in vite.config.ts (Recommended)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Makes dev server accessible on network
    port: 5173,       // Default Vite port
  },
})
```

Then run normally:
```bash
npm run dev
```

### Option B: CLI Flag (One-off)

If you don't want to modify config:
```bash
npm run dev -- --host 0.0.0.0
```

### Team Access

```
http://YOUR-IP:5173
```

Example: `http://192.168.1.100:5173`

---

## Streamlit (Python Data Apps)

For quick data dashboards, validators, or interactive tools.

### Start Server

```bash
streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.headless true
```

### Deploy Script Pattern

Create `deploy.sh` for easy startup:

```bash
#!/bin/bash
set -e

# Get IP for sharing
IP=$(hostname -I | awk '{print $1}')
echo "Share with team: http://$IP:8501"

source venv/bin/activate
streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.headless true
```

### Team Access

```
http://YOUR-IP:8501
```

---

## FastAPI / Uvicorn (Python APIs)

For backend services, APIs, or full-stack apps.

### Start Server

```bash
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### With Environment Variables

```bash
DEVELOPER_HOME_IP=$(hostname -I | awk '{print $1}') \
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Team Access

```
http://YOUR-IP:8000
```

---

## Static HTML Mockups

For sharing plain HTML/CSS/JS mockups without any build step.

### Start Server

```bash
cd path/to/mockups
python3 -m http.server 8000 --bind 0.0.0.0
```

### Team Access

```
http://YOUR-IP:8000/mockup.html
```

---

## WSL-Specific Notes

If you're running on WSL (Windows Subsystem for Linux), there are extra considerations.

### Get Your WSL IP

```bash
hostname -I
# Example output: 172.17.194.224
```

This IP is different from your Windows IP. Teammates need the WSL IP.

### Windows Browser Access

Standard `localhost` won't work from Windows browsers to WSL servers. Use the WSL IP directly:

```
http://172.17.194.224:5173
```

### Port Forwarding (Alternative)

From **Windows PowerShell (Admin)**:

```powershell
# Forward Windows localhost to WSL
netsh interface portproxy add v4tov4 listenport=5173 listenaddress=0.0.0.0 connectport=5173 connectaddress=172.17.194.224

# Now http://localhost:5173 works from Windows
```

To remove:
```powershell
netsh interface portproxy delete v4tov4 listenport=5173 listenaddress=0.0.0.0
```

---

## Troubleshooting

### "Connection refused" or "Site can't be reached"

1. **Check server is running**: Look for "listening on" message in terminal
2. **Check correct IP**: Run `hostname -I` and use that IP
3. **Check firewall**: 
   ```bash
   # Ubuntu/WSL
   sudo ufw allow 5173  # or your port
   ```
4. **Check same network**: Both devices must be on same network or VPN

### "Port already in use"

```bash
# Find what's using the port
lsof -i :5173

# Kill it (replace PID)
kill -9 <PID>
```

### Teammates Can't Connect

- Verify they're on the same network (office network, VPN)
- Corporate firewalls may block non-standard ports
- Try a common port like 3000 or 8080

---

## When to Use Each Stack

| Use Case | Recommended Stack |
|----------|-------------------|
| React/Vue/Svelte app | Vite |
| Plain HTML mockup | Vite or Python http.server |
| Python data dashboard | Streamlit |
| Backend API | FastAPI + Uvicorn |
| Full-stack with auth | FastAPI + Vite (separate ports) |

---

## Next Steps

- **Deploy permanently**: See [Railway Deployment Guide](../railway/README.md)
- **Access from anywhere**: See [Multi-Device Workspace](./MULTI-DEVICE-WORKSPACE.md) (Tailscale VPN)
- **Add authentication**: See existing patterns in `utilities/ping-tree-compare/`

