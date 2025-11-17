# Development Environment Overview

## System Architecture

- **Host OS**: Windows 11 Professional
- **Development Environment**: WSL2 (Windows Subsystem for Linux)
- **Linux Distribution**: Ubuntu (via WSL2)
- **Primary Development Path**: `~/`

## Directory Structure

### WSL Home Directory (`~/`)
```
~/
├── repos/                    # Active development projects
├── knowledge-base/           # Multi-repo documentation system (symlinked)
├── bin/                      # Custom scripts and utilities
├── Desktop/                  # WSL desktop files
├── windows-projects/         # Symlink to Windows projects
├── windows-sync/            # Sync directory with Windows
└── windows-to-wsl2-screenshots/  # Screenshot transfer directory
```

### Windows Home Directory (`/mnt/c/Users/<YourUsername>/`)
- **repos/**: Windows-based repositories
- **scoop/**: Windows package manager installations
- **miniconda3/**: Python environment manager
- **aws/**: AWS CLI configuration
- **Documents/**, **Downloads/**: Standard Windows directories
- **OneDrive/**: Cloud storage sync

## Key Repositories

### Active Projects (`~/repos/`)
- `dev-setup`: This repository - development environment documentation
- `knowledge-base`: Symlinked multi-repo documentation system
- `epcvip-datalake-assistant`: Company data lake tooling
- `engagement-ab-analysis-pipeline`: A/B testing pipeline
- `ping-tree-compare`: Ping tree comparison tools
- Various other project repositories

## Knowledge Base System

The knowledge base is a critical part of the workflow, consisting of three symlinked repositories:

- **company-docs/**: Company knowledge, products, processes (90+ files)
- **internal-docs/**: Personal projects, notes, planning (80+ files)
- **query-docs/**: SQL queries, data analysis patterns (40+ files)

Key files:
- `CLAUDE.md`: AI context and search patterns
- `INDEX.md`: Quick reference and navigation
- `USAGE.md`: Daily workflow guide
- `search-all.sh`: Cross-repository search script

## Development Tools

### Package Managers
- **Windows**: Scoop
- **WSL/Linux**: apt, npm, pip
- **Python**: Miniconda3

### Cloud Services
- AWS CLI configured for cloud operations
- OneDrive for document synchronization

## Workflow Patterns

### Cross-Environment Access
- Windows files accessible via `/mnt/c/`
- WSL files accessible from Windows via `\\wsl$\Ubuntu\home\adams`
- Symlinks bridge Windows and WSL environments

### Version Control
- Git repositories in both Windows and WSL
- Primary development in WSL for better performance
- Windows repos accessed via `/mnt/c/` when needed

### Documentation Workflow
1. Navigate to `~/knowledge-base/`
2. Use specialized search patterns for each sub-repo
3. Cross-reference between company, internal, and query docs
4. Maintain consistency across all documentation repos

## Quick Commands

```bash
# Navigate to main repos
cd ~/repos

# Access knowledge base
cd ~/knowledge-base

# Access Windows home
cd /mnt/c/Users/<YourUsername>/

# Search all documentation
~/knowledge-base/search-all.sh "search term"
```

## Performance Considerations

- WSL2 provides near-native Linux performance
- File operations on `/mnt/c/` are slower than native WSL paths
- Use WSL paths (`~/`) for active development
- Cache frequently accessed Windows files in WSL filesystem