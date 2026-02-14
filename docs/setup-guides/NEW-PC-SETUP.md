# New PC Setup - Simple Guide

**Updated:** February 2026
**Time:** ~90 minutes

---

## Prerequisites

- Windows 11 PC
- Administrator access
- Your GitHub credentials
- Anthropic API key or Claude subscription

---

## 1. Check What's Already Installed (5 mins)

PowerShell as Admin:
```powershell
# Check WSL
wsl --list --verbose

# Check Git
git --version

# Check Node.js
node --version

# Check if Ubuntu is installed
wsl -l -v
```

Note what's already installed - we'll skip those steps.

---

## 2. Install WSL2 + Ubuntu (10 mins)

**If WSL not installed:**
```powershell
wsl --install
wsl --update
```

Restart computer. Launch Ubuntu from Start menu, create username/password.

**Update Ubuntu:**
```bash
sudo apt update && sudo apt upgrade -y
```

**Configure WSL Resources:**

Create `C:\Users\<YourUsername>\.wslconfig`:

```ini
[wsl2]
# For Dell Precision 5680 (64GB RAM, i9-13900H with 20 threads)
memory=40GB        # Leave ~24GB for Windows
processors=16      # Leave ~4 threads for Windows
swap=8GB

[experimental]
sparseVhd=true
autoMemoryReclaim=gradual
```

**Notes:**
- i9-13900H has 14 cores (6 P-cores + 8 E-cores) = 20 threads total
- Allocate 60-70% of RAM to WSL, leave rest for Windows
- Adjust based on your workload

Apply: `wsl --shutdown` in PowerShell, then restart WSL.

**✅ Standard Practice?** Yes! Explicit resource allocation prevents WSL from consuming too much and is recommended for development workloads.

---

## 3. Install Development Tools (15 mins)

**Check what's already installed:**
```bash
# Check installed tools
git --version 2>/dev/null || echo "Git not installed"
node --version 2>/dev/null || echo "Node.js not installed"
```

**Install only what's missing:**

```bash
# Git (if not installed)
if ! command -v git &> /dev/null; then
    sudo apt install -y git
    echo "✅ Git installed"
else
    echo "✅ Git already installed: $(git --version)"
fi

# Node.js 18+ (if not installed or old version)
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    echo "✅ Node.js installed"
else
    echo "✅ Node.js already installed: $(node --version)"
fi

# Other essentials
sudo apt install -y build-essential
```

**Configure Git (if needed):**
```bash
# Check if already configured
if [ -z "$(git config --global user.name)" ]; then
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    git config --global init.defaultBranch main
    echo "✅ Git configured"
else
    echo "✅ Git already configured for: $(git config --global user.name)"
fi
```

---

## 4. Install Claude Code (5 mins)

**Check if already installed:**
```bash
if command -v claude &> /dev/null; then
    echo "✅ Claude Code already installed: $(claude --version)"
else
    echo "Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code
    echo "✅ Claude Code installed"
fi
```

**Authenticate:**
```bash
claude
# Follow OAuth prompts in browser
# Choose: Anthropic Console, Claude Pro/Max, or Enterprise
```

**Test for freezing:** Type continuously for 30 seconds. If Claude freezes every ~10 seconds, see "Troubleshooting" section.

---

## 5. Set Up Directories & Clone Repos (15 mins)

```bash
# Create structure
mkdir -p ~/repos/code ~/repos-epcvip/docs ~/bin

# Clone dev-setup repo (replace with your username/fork)
cd ~/repos
git clone https://github.com/<your-username>/dev-setup.git

# Clone your documentation repos to WSL (IMPORTANT: not to /mnt/c/!)
# cd ~/repos-epcvip/docs

# Example: Clone your repos (customize for your setup)
# git clone https://github.com/<your-org>/your-docs.git
# git clone https://github.com/<your-org>/your-project.git
```

**Why WSL?** Linux FS is ~10x faster than accessing Windows FS via `/mnt/c/`.

**Note**: If you have a personal/ folder with clone-repos.sh script, use that for your actual repositories.

---

## 6. Install Custom Scripts (5 mins)

```bash
# Copy scripts
cp ~/repos/dev-setup/scripts/* ~/bin/
chmod +x ~/bin/*

# Add to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Test
dev     # Should show usage
perf    # Should show system stats
```

---

## 7. Install Obsidian in WSL (10 mins)

**Why WSL?** Prevents EISDIR errors when editing WSL-based docs.

```bash
cd ~/Downloads
wget https://github.com/obsidianmd/obsidian-releases/releases/download/v1.9.12/obsidian_1.9.12_amd64.deb
sudo apt install -y libasound2t64 ffmpeg
sudo apt install -y ./obsidian_1.9.12_amd64.deb
```

**Create launcher:**
```bash
cat > ~/bin/obs << 'EOF'
#!/bin/bash
obsidian > /dev/null 2>&1 &
EOF
chmod +x ~/bin/obs
```

Test: `obs` (GUI should appear)

---

## 8. Set Up Knowledge Base (5 mins)

```bash
mkdir -p ~/knowledge-base

# Create symlinks to your doc repos (customize for your setup)
# Example:
# ln -s ~/repos-epcvip/docs/your-docs ~/knowledge-base/docs
# ln -s ~/repos-epcvip/docs/your-project ~/knowledge-base/project

# Or use personal/setup/setup-knowledge-base.sh if you have it
```

---

## 9. Install Cursor IDE (5 mins)

Download from https://cursor.sh/ and install on Windows (not WSL).

Access WSL files in Cursor via: `\\wsl.localhost\Ubuntu\home\<your-username>\repos`

---

## 10. Configure Claude Skills & MCPs (15 mins)

### What Are Skills?

**New in October 2025:** Anthropic released "Skills" - modular task knowledge packs that make Claude faster and more consistent for specialized tasks.

**Skills vs MCPs:**
- **Skills** = Instructions + resources Claude loads dynamically (no token cost until used)
- **MCPs** = External tool connections (cost tokens when active)

### Set Up Skills

**1. Enable Skills (if you have Pro/Max/Team/Enterprise):**

In Claude:
```
/settings
# Toggle "Skills" on
```

**2. Use Pre-built Skills:**

Anthropic provides skills for:
- Excel generation (formulas, formatting)
- PowerPoint presentations
- Word documents
- PDF creation
- Brand guidelines

**3. Create Custom Skills (Optional):**

```bash
# Create skills directory
mkdir -p ~/.claude/skills

# Example: Create a project-specific skill
mkdir -p ~/.claude/skills/my-project
cat > ~/.claude/skills/my-project/instructions.md << 'EOF'
# My Project Coding Standards

- Use TypeScript strict mode
- Follow ESLint rules
- Write tests for all functions
EOF
```

In Claude: `/skill load ~/.claude/skills/my-project`

### Configure MCPs (Optional)

**Best Practice 2025:** Only enable MCPs you actively need (saves tokens).

**For Notion MCP:**
```bash
mkdir -p ~/.claude/marketplaces/local/notion-mode/.claude-plugin

cat > ~/.claude/marketplaces/local/notion-mode/.claude-plugin/plugin.json << 'EOF'
{
  "name": "notion-mode",
  "version": "1.0.0",
  "description": "Notion MCP (30k tokens)",
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
EOF
```

In Claude: `/plugin marketplace add ~/.claude/marketplaces/local`

**Enable/disable as needed:**
- Enable: `/plugin install notion-mode@local`
- Disable: `/plugin uninstall notion-mode`

### MCP Best Practices 2025

1. **Use HTTP MCPs when available** (hosted, auto-updated)
2. **Only load MCPs you need** (each costs tokens)
3. **Prefer Skills over MCPs** for static knowledge (no token cost)
4. **Test connections:** `claude mcp list` to verify

---

## 11. Test Everything (10 mins)

```bash
# Performance check
perf

# Launch Obsidian
obs

# Test project launcher
cd ~/repos-epcvip/docs
dev personal-docs claude
# Should start Claude Code
```

---

## Troubleshooting

### Claude Freezing Every ~10 Seconds

**Note:** Modern WSL (2025) typically doesn't have this issue. But if you experience it:

```bash
# Fix DNS resolution
sudo rm /etc/resolv.conf
echo -e "nameserver 8.8.8.8\nnameserver 1.1.1.1" | sudo tee /etc/resolv.conf
sudo chattr +i /etc/resolv.conf
echo -e "[network]\ngenerateResolvConf = false" | sudo tee -a /etc/wsl.conf

# Restart WSL (in PowerShell)
wsl --shutdown
wsl
```

**Verify issue first:** Check `dmesg | tail -20` for DNS errors like "CheckConnection: getaddrinfo() failed"

### Cursor Remote-WSL Setup (Recommended)

**For native WSL development with Cursor:**

1. Install "Cursor Remote WSL" extension in Cursor
2. Use `cursor .` command from WSL terminal (auto-connects via Remote-WSL)
3. Or manually: `Ctrl+Shift+P` → `Remote-WSL: New Window`
4. Verify `[WSL: Ubuntu]` indicator in bottom-left corner

**Benefits:**
- AI agent runs commands natively in WSL (no wrapper)
- Faster file operations
- Consistent environment with Claude Code
- Proper Linux path handling

**First connection:** Takes 1-2 minutes to install VS Code Server in WSL (one-time)

### Cursor Won't Open from WSL (Legacy Method)

**If Remote-WSL isn't working:**

```bash
cd ~/repos/project
explorer.exe .  # Opens Explorer, then right-click "Open with Cursor"
```

**Note:** This opens Cursor in Windows context, requiring AI agent to use `wsl` wrapper for commands.

### Cursor Terminal Shows No Output (WSL)

**Symptoms:** Commands execute in Cursor's integrated terminal but produce zero output

**Root Cause:** Cursor is using PowerShell as the terminal instead of WSL bash, causing the Windows-WSL bridge to fail

**Solution A - Change Terminal Profile (Quickest):**

1. In Cursor: Open Command Palette (`Ctrl+Shift+P`)
2. Type: `Terminal: Select Default Profile`
3. Select: **"WSL Bash"** or **"Ubuntu (WSL)"**
4. Open new terminal (`` Ctrl+` ``) and test: `echo "test"`

**Solution B - Use Remote-WSL Connection (Most Reliable):**

1. In Cursor: `Ctrl+Shift+P` → `Remote-WSL: New Window`
2. Select your Ubuntu distribution
3. Navigate to project: File → Open Folder → `~/repos/your-project` or `/home/YOUR_USERNAME/repos/your-project`
4. Terminal will automatically use WSL bash

**Solution C - Use SSH Connection (Alternative):**

SSH is already running in your WSL (started Nov 12). To connect:

1. In Cursor: Install "Remote - SSH" extension (if needed)
2. `Ctrl+Shift+P` → `Remote-SSH: Connect to Host`
3. Enter: `adams@localhost`
4. Enter WSL password when prompted

**Verification:**

```bash
# In Cursor's terminal - should show output
echo "test"
whoami
pwd
```

**Note:** The issue is NOT about opening Cursor (that's handled by the `cursor()` function). It's about Cursor using the correct terminal shell after it's opened.

### Slow File Performance

Make sure your repos are in `~/repos/`, NOT `/mnt/c/`. Check with:
```bash
pwd  # Should show ~/repos/...
```

---

## Quick Commands Reference

```bash
# Daily workflow
dev project-name claude         # Start Claude Code
dev project-name codex          # Start Codex
dev project-name cursor         # Open Cursor IDE
dev project-name claude +kb     # Claude with knowledge base

# System monitoring
perf                            # Quick check
perf --disk                     # With disk test

# Claude Code
claude                          # Start
/plugin install notion-mode     # Enable Notion
/plugin uninstall notion-mode   # Disable Notion (saves 30k tokens)
```

---

## What's Different from Your Old Setup?

✅ **Nothing major!** Your September 2024 setup is still current.

**New in 2025:**
- Permission modes: Try `/permission-mode acceptEdits` for auto-accepting file edits
- DNS fix may not be needed (test first!)
- New auth options: Claude Pro/Max subscription

---

## Next Steps

1. Clone your code projects to `~/repos/code`
2. Set up language-specific tools (Python, etc.)
3. Commit this setup to your dev-setup repo

---

## Your Laptop Specs Summary

**Dell Precision 5680:**
- CPU: i9-13900H (14 cores: 6 P-cores + 8 E-cores = 20 threads)
- RAM: 64GB
- GPU: RTX 3500 Ada (8GB VRAM)

**Recommended WSL Allocation:**
- Memory: 40GB (leaves 24GB for Windows)
- Processors: 16 (leaves 4 threads for Windows)

**Why these numbers?**
- 60-70% RAM allocation is standard for dev workloads
- Leave enough threads for Windows responsiveness
- GPU passthrough to WSL not needed (Claude Code doesn't use GPU)

---

## Skills vs MCPs vs Plugins - Quick Reference

| Feature | What It Is | Token Cost | When to Use |
|---------|-----------|------------|-------------|
| **Skills** | Modular instruction packs | None (until loaded) | Task-specific guidelines, workflows |
| **MCPs** | External tool connections | Yes (~30k each) | Notion, GitHub, databases |
| **Plugins** | Bundles that toggle MCPs | Varies | Managing MCP token costs |

**Strategy:**
1. Use **Skills** for static knowledge (coding standards, brand guidelines)
2. Use **MCPs** for live data access (Notion, databases)
3. Use **Plugins** to toggle MCPs on/off (save tokens)

---

That's it! Simple, practical, and modern. 🚀

