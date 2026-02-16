# Multi-Device AI Workspace

[← Back to Main README](../../README.md) | [Daily Workflow →](./DAILY-WORKFLOW.md)

**Last Updated**: February 2026 | **Time Required**: 30-45 minutes

Access Claude Code from any device - continue sessions, edit files, and run agents from your phone, tablet, or laptop.

---

## Why This Matters

Web AI (ChatGPT, Claude.ai) can chat but can't:
- Edit your files directly
- Update spreadsheets or documents
- Run commands on your system
- Maintain persistent context across sessions

Claude Code can do all of this - but traditionally requires a terminal on your desktop.

**This guide breaks that constraint.** Access your full Claude Code environment from iPad, phone, laptop, or any device with a terminal app.

**Who This Is For:**
- Developers who want session continuity across devices
- Project managers managing docs, kanban boards, markdown files from mobile
- Anyone who needs AI to edit files, not just chat

---

## Overview

### Stack
- **Tailscale** - Mesh VPN (secure device-to-device connection, no port forwarding)
- **SSH with keepalive** - Stable terminal access that doesn't drop
- **tmux** - Persistent sessions that survive disconnects and device switches
- **Mosh** (optional) - For very unstable networks

> **Alternatives:** GitHub Codespaces or Gitpod provide browser-based dev environments without self-hosting. The stack below is for developers who prefer a self-hosted setup with full control.

### Result
Start a Claude session on your desktop, continue it from your iPad at a coffee shop, check in from your phone on the train.

### Connection Architecture
```
Your Device → Tailscale VPN → Dev Machine → Claude Code
```

---

## Part 1: Tailscale Setup

Tailscale creates an encrypted mesh network between your devices. No port forwarding, no exposed services.

### Windows Host (One-Time)

1. **Download**: https://tailscale.com/download/windows
2. **Install and sign in** with Google, Microsoft, or email
3. **Note your Windows IP** (e.g., `100.107.0.99`) - shown in Tailscale tray icon

### WSL2 Configuration (One-Time)

WSL2 needs its own Tailscale instance:

```bash
# In WSL terminal
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Note the WSL2 IP (e.g., 100.108.214.33) - this is your SSH target
tailscale ip -4
```

### Mobile Devices

**iOS/iPadOS:**
1. App Store → Tailscale → Install
2. Sign in with same account
3. Toggle VPN on when needed

**Android:**
- Play Store → Tailscale → same process

### Verify Connectivity

From your mobile device (with Tailscale connected):
```bash
ping 100.108.214.33  # Replace with your WSL2 IP
```

---

## Part 2: SSH Configuration (Critical for Stability)

### Key-Based Authentication (One-Time)

Generate SSH keys on your mobile device's terminal app, then copy to WSL:

```bash
# On WSL - ensure SSH server is running
sudo apt install openssh-server
sudo service ssh start

# Add your public key to authorized_keys
mkdir -p ~/.ssh
echo "your-public-key-here" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### SSH Config with Keepalive (IMPORTANT)

**Problem:** Default SSH times out on idle connections, causing frequent drops even on stable WiFi.

**Solution:** Add keepalive settings to your SSH config.

On your mobile device (or any client), edit `~/.ssh/config`:

```bash
Host wsl
    HostName 100.108.214.33    # Your WSL Tailscale IP
    User yourusername
    ServerAliveInterval 60     # Send keepalive every 60 seconds
    ServerAliveCountMax 3      # Disconnect after 3 missed keepalives
    TCPKeepAlive yes
```

Now connect with just:
```bash
ssh wsl
```

### Test Connection

```bash
ssh wsl
echo "Connected!"
exit
```

---

## Part 3: tmux for Persistent Sessions

### Why tmux?

tmux keeps your session alive when:
- WiFi drops or device sleeps
- You switch devices (iPad → iPhone → Desktop)
- Connection temporarily breaks

Without tmux, disconnection = lost work. With tmux, just reconnect.

### Essential Commands

```bash
# Session management
tmux new -s work           # Create new session named "work"
tmux attach -t work        # Reconnect to existing session
tmux ls                    # List all sessions
tmux kill-session -t work  # End session (only when done)

# Inside tmux (prefix is Ctrl+B)
Ctrl+B, D     # Detach (keeps session running)
Ctrl+B, C     # New window
Ctrl+B, N     # Next window
Ctrl+B, P     # Previous window
Ctrl+B, [     # Scroll mode (Q to exit)
```

### Session Handoff Between Devices

The magic of tmux: start on one device, continue on another.

**Example: iPad → iPhone**
```bash
# On iPad (at coffee shop):
ssh wsl
tmux attach -t work
# Work with Claude Code...
Ctrl+B, D    # Detach
exit

# On iPhone (in taxi):
ssh wsl
tmux attach -t work
# Exactly where you left off!
```

### Multiple Sessions (Project Isolation)

Keep different projects in different sessions:
```bash
tmux new -s personal
tmux new -s work-projectA
tmux new -s work-projectB

# Switch between them:
tmux ls                    # See all sessions
tmux attach -t personal    # Connect to specific one
```

---

## Part 4: Mobile Terminal Setup

### Blink Shell (iOS - Recommended)

Best iOS terminal app. Native feel, great keyboard support.

**Setup:**
```
Settings → Hosts → Add:
- Host: wsl
- HostName: 100.108.214.33  (your WSL IP)
- User: yourusername
- Key: (select your SSH key)
```

**Connect:** Type `ssh wsl` or just `wsl` in Blink.

### Prompt 3 (iOS Alternative)

Similar setup. Also supports Eternal Terminal (ET) for even more stable connections.

### Android Options

- **Termux** - Full Linux environment
- **JuiceSSH** - Simple SSH client
- **Termius** - Cross-platform

### Keyboard Shortcuts (iPad)

With external keyboard:
- **Cmd+T**: New tab
- **Cmd+W**: Close tab
- **Cmd+K**: Clear screen
- **Ctrl+C**: Cancel command
- **Ctrl+D**: Exit/logout

---

## Part 5: Image Upload Workflow (Optional but Powerful)

Send photos from your phone to Claude Code for analysis:
- Receipts → expense tracking
- Screenshots → extract information
- Signs/menus → translation
- Documents → data extraction

### Server Setup (One-Time on WSL)

Create a simple upload server:

```python
# ~/bin/image-upload-server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import os, json, cgi
from datetime import datetime

UPLOAD_DIR = "/tmp/claude-images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            fields = cgi.parse_multipart(self.rfile, pdict)
            file_data = fields.get('file')[0]
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(file_data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"path": filepath}).encode())

HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()
```

Run with: `python3 ~/bin/image-upload-server.py &`

### iOS Shortcut Configuration

Create a Shortcut called "Send to Claude":

1. **Repeat with Each** (input: Shortcut Input)
2. **Get Contents of URL**
   - URL: `http://YOUR_WSL_IP:8000`
   - Method: POST
   - Request Body: Form
   - Add field: Key=`file`, Value=`Repeat Item`
3. **Get Dictionary Value** (key: `path`)
4. **End Repeat**
5. **Combine Text** (separator: space)
6. **Text**: `Analyze [Combined Text]`
7. **Copy to Clipboard**
8. **Show Notification**: "Ready to paste"

**Usage:** Share images → "Send to Claude" → Paste in terminal.

---

## Part 6: Mosh for Unstable Networks (Optional)

Mosh (Mobile Shell) handles network changes better than SSH.

### When to Use Mosh vs SSH

| Situation | Use |
|-----------|-----|
| Stable WiFi | SSH with keepalive |
| Moving (train, walking) | Mosh |
| Switching networks | Mosh |
| Cellular data | Mosh |

### Installation

```bash
# On WSL
sudo apt install mosh

# In Blink Shell
# Edit host → Connection type → Mosh
```

### Usage

```bash
mosh wsl
```

### Tradeoffs

**Pros:**
- Auto-reconnects after disconnects
- Local echo (feels responsive on lag)
- Handles IP changes (WiFi → cellular)

**Cons:**
- Requires UDP ports 60000-61000 open
- Less compatible with some firewalls
- Slightly different terminal behavior

---

## Daily Workflows

### Start Remote Session (from any device)

```bash
ssh wsl                    # Connect
tmux attach -t work        # Reattach to session (or `tmux new -s work`)
cd ~/repos/your-project    # Navigate
claude                     # Start Claude Code
```

### Device Handoff (iPad → iPhone → Desktop)

1. On current device: `Ctrl+B, D` to detach tmux
2. `exit` to close SSH
3. On new device: `ssh wsl && tmux attach -t work`
4. Continue exactly where you left off

### End of Day

**Option A: Leave session running**
```bash
Ctrl+B, D     # Detach tmux
exit          # Close SSH
# Session stays running - reconnect tomorrow
```

**Option B: Clean close**
```bash
# In Claude: /exit
exit          # Close shell
tmux kill-session -t work
exit          # Close SSH
```

---

## For Different Users

### Developers

- **Session continuity** - Start debugging at desk, continue on laptop
- **Git operations** - Commit, push, review from mobile
- **Quick fixes** - Hot fix from phone without full desktop

### Project Managers / Document Managers

- **Update markdown files** - Edit project docs, meeting notes
- **Manage kanban boards** - Update task files, status docs
- **AI-assisted research** - Claude Code researches, synthesizes, writes

### Work vs Personal

Consider separate tmux sessions:
```bash
tmux new -s work-project
tmux new -s personal-projects
```

This isolates contexts and prevents accidental cross-contamination.

---

## Troubleshooting

### Connection Drops on Stable WiFi

**Cause:** SSH timeout (default settings don't send keepalives)

**Fix:** Add to `~/.ssh/config`:
```bash
ServerAliveInterval 60
ServerAliveCountMax 3
```

### "Connection Refused"

1. **Tailscale running?** - Check green status in Tailscale app
2. **Home PC on?** - `ping YOUR_WSL_IP` - no reply = PC sleeping
3. **WSL running?** - Open PowerShell on PC: `wsl --list --running`

### "Permission Denied (publickey)"

```bash
# Use password fallback
ssh -o PreferredAuthentications=password user@YOUR_WSL_IP

# Or check your key is in authorized_keys
cat ~/.ssh/authorized_keys
```

### tmux Session "Not Found"

```bash
tmux ls                # List sessions
tmux new -s work       # Create if none exist
```

### Home PC Asleep / Unreachable

**Backup: GitHub Codespaces**
1. github.com → your repo → Code → Codespaces
2. `npm install -g @anthropic-ai/claude-code`
3. Work in browser - not as good, but functional

---

## Pre-Setup Checklist

Before relying on this workflow:

- [ ] Tailscale installed on all devices (Windows, WSL, mobile)
- [ ] SSH key authentication working (`ssh wsl` connects)
- [ ] SSH config has `ServerAliveInterval 60`
- [ ] Terminal app configured with `wsl` host
- [ ] Windows power settings: Never sleep (when plugged in)
- [ ] Test full workflow: connect → tmux → claude → detach → reconnect from different device

---

## See Also

- [Daily Workflow](./DAILY-WORKFLOW.md) - General development workflow
- [Claude Code Setup](./CLAUDE-CODE-SETUP.md) - Installing Claude Code
- [WSL Paths Reference](../reference/WSL-PATHS.md) - Understanding file paths

---

_This workflow has been tested extensively on the go — trains, coffee shops, hotels — proof that Claude Code is more than a desktop coding tool._
