# Architectural Decision Record: WSL for Development

**Status**: Active
**Date**: 2024-09
**Deciders**: Personal development workflow
**Last Updated**: 2026-01-21

---

## Context and Problem Statement

When developing on Windows 11, there are multiple approaches for running Linux tooling:
1. **WSL2** (Windows Subsystem for Linux)
2. **Native Windows** with cross-platform tools
3. **Dual Boot** Linux/Windows
4. **Virtual Machine** (VirtualBox, VMware)
5. **Mixed Approach** (some tools in Windows, some in WSL)

**Key Question**: What's the best approach for my workflow with Claude Code, Codex, Cursor IDE, and data analysis projects?

**Important**: This is a **CHOICE, not a requirement**. All these tools work on Windows native. WSL is an optimization for my specific use case.

---

## Decision

**Primary development environment: WSL2 (Ubuntu)**

All code repositories, Claude Code, Codex, and most development tooling run in WSL2. Cursor IDE runs on Windows but connects to WSL via the Remote-WSL extension.

---

## Rationale

### Why WSL Over Windows Native

**File I/O Performance** (~10x faster):
- **WSL Linux FS**: ~2.4 GB/s (measured with `perf --disk`)
- **Windows FS**: ~200 MB/s
- **Windows FS via /mnt/c/**: ~200 MB/s
- **Impact**: Git operations, file searches, build times significantly faster

**Source**: [Microsoft WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/compare-versions#performance-across-os-file-systems)

**Tool Compatibility**:
- Claude Code CLI: Works on both, no difference
- Codex: Works on both, no difference
- Shell scripts: Bash native vs PowerShell/Git Bash wrappers
- Unix tools: Native vs Windows ports

**Development Experience**:
- Linux paths (`~/repos/`) vs Windows paths (`C:\Users\...`)
- Native SSH, git without wrappers
- Better Docker/container integration
- Consistent with production (Linux servers)

### Why Not Native Windows

**Cons of Windows Native**:
- 10x slower file I/O for repos on Windows filesystem
- Need PowerShell equivalents or Git Bash for shell scripts
- Path translation issues (backslashes, drive letters)
- Less consistent with Linux production environments

**When Windows Native Makes Sense**:
- Single-file editing (no performance impact)
- Windows-specific development (.NET, C#, Windows APIs)
- Team doesn't use Linux
- No shell scripts or Linux-specific tools

### Why Not Dual Boot

**Cons**:
- Reboot to switch environments
- Can't access both simultaneously
- Harder to use Windows-only tools (Outlook, Teams, some corporate software)

### Why Not VM

**Cons**:
- Resource overhead (RAM, CPU dedicated to VM)
- More complex setup than WSL
- Network configuration complexity
- WSL provides same Linux environment with better integration

---

## Consequences

### Positive

- **10x faster file operations** for repos in WSL
- **Native Linux environment** for CLI tools
- **Seamless Windows integration** (access Windows files, run Windows apps)
- **Cursor IDE** works via Remote-WSL extension (native Linux paths)
- **Single system resources** (no VM overhead)

### Negative

- **Learning curve** for WSL-specific concepts:
  - Windows paths: `\\wsl.localhost\Ubuntu\home\adams\repos`
  - WSL paths: `~/repos/` (Linux) vs `/mnt/c/` (Windows)
  - Which filesystem to use for what
- **Two worlds** to understand (Windows host + Linux guest)
- **Potential issues** with:
  - File permissions (Windows vs Linux)
  - Line endings (CRLF vs LF)
  - Path case sensitivity

### Neutral

- **Resource allocation**: Configure WSL based on your hardware (see `.wslconfig` example below)
- **Both environments available**: Can use Windows tools when needed

---

## Implementation Details

### Current Configuration

**WSL Version**: WSL2
**Distribution**: Ubuntu
**Config Location**: `C:\Users\<username>\.wslconfig`

**Recommended .wslconfig** (as of 2026-01):
```ini
[wsl2]
# Resource allocation (adjust to your hardware)
memory=48GB
processors=16
swap=8GB

# Networking - NAT mode (default, most compatible)
localhostForwarding=true   # Access WSL services from Windows
firewall=true
autoProxy=true

[experimental]
sparseVhd=true             # Auto-shrink disk
autoMemoryReclaim=gradual  # Return unused RAM to Windows
```

**Full reference:** See `~/WSL-CONFIG-REFERENCE.md` or [WSL-NODE-WORKAROUNDS.md](../reference/WSL-NODE-WORKAROUNDS.md)

**Why NAT mode (default):** Simpler and more compatible than mirrored mode. Node.js timeouts are resolved with `UNDICI_NO_HTTP2=1` (set globally in `~/.bashrc` or per-project in `package.json`). Mirrored mode can cause Windows DNS resolution failures on some setups.

**Directory Structure**:
```
WSL (Linux FS - FAST):
  ~/repos/          # All code (2.4 GB/s)
  ~/bin/            # Scripts
  ~/knowledge-base/ # Docs

Windows:
  \\wsl.localhost\Ubuntu\home\adams\repos  # Access from Windows
  C:\Users\adams\  # Windows-only files
```

**Tool Setup**:
- **Claude Code**: Installed in WSL (`npm install -g @anthropic-ai/claude-code`)
- **Codex**: Installed in WSL
- **Cursor**: Installed on Windows, connects via Remote-WSL extension
- **Git**: In WSL (faster) and Windows (for Windows-only repos)

### Cursor + WSL Integration

**How it works**:
1. Cursor (Windows) installs VS Code Server in WSL (one-time, automatic)
2. Remote-WSL extension handles connection
3. Terminal, AI agent, file operations run natively in WSL
4. UI renders on Windows

**Command**: `cursor .` from WSL automatically connects via Remote-WSL

**Benefits**:
- AI agent runs commands natively (no `wsl` wrapper)
- File paths are Linux paths (no translation)
- Fast file operations (Linux FS)
- Consistent with Claude Code environment

---

## Alternatives Considered

### Alternative 1: Windows Native

**Decision**: Rejected for primary workflow

**Reasoning**:
- 10x slower file operations
- Would need PowerShell equivalents for all scripts
- Less consistent with Linux production

**When to use**: Windows-specific development, single-file editing

### Alternative 2: Dual Boot

**Decision**: Rejected

**Reasoning**:
- Can't use Windows and Linux simultaneously
- Reboot friction
- WSL provides same Linux environment without dual boot complexity

### Alternative 3: Mixed Approach (some Windows, some WSL)

**Decision**: Partially adopted

**Implementation**:
- **Primary development**: WSL (repositories, tools)
- **Windows-only**: Cursor UI, Obsidian (can run in WSL but Windows version stable)
- **Shared**: Access Windows files from WSL when needed (`/mnt/c/`)

**Reasoning**: Best of both worlds - Linux development performance + Windows UI apps

---

## When to Use Each Approach

### Use WSL When:
- Working with code repositories (file I/O matters)
- Running shell scripts or Unix tools
- Need consistent Linux environment
- Working with containers/Docker
- Team uses Linux in production

### Use Windows Native When:
- Windows-specific development (.NET, Windows APIs)
- Single-file editing (no performance impact)
- Windows-only tools required
- Team is Windows-only
- Simpler mental model preferred

### Use Mixed Approach When:
- Need both environments (like this setup)
- Want Windows UI apps + Linux CLI tools
- Flexibility to choose per project

---

## Decision Review

**Review Date**: Quarterly
**Next Review**: 2026-04

**Criteria for Reconsidering**:
- WSL performance degrades
- Windows native performance improves significantly
- Tool compatibility issues emerge
- Team requirements change

---

## References

- [Microsoft WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [WSL Performance Best Practices](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)
- [Set up WSL development environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)
- Personal performance testing: `perf --disk` script results

---

**TL;DR**: WSL chosen for 10x faster file I/O, native Linux tooling, and better development experience. Windows native is viable alternative if you don't need the performance or Linux tools. Cursor + Remote-WSL gives best of both worlds.

