# Manual Repository Renaming Required

## Terminal Access Issue

The automated terminal commands are not working. Please execute these commands manually:

### Option 1: Using Windows File Explorer
1. Navigate to `\\wsl.localhost\Ubuntu\home\adams\repos\`
2. Rename `ping-tree-ab-analysis` to `experimentation-framework`
3. Rename `epcvip-datalake-assistant` to `data-platform-assistant`

### Option 2: Using WSL Terminal
```bash
cd /home/adams/repos
mv ping-tree-ab-analysis experimentation-framework
mv epcvip-datalake-assistant data-platform-assistant
```

### Option 3: Using PowerShell (from Windows side)
```powershell
cd \\wsl.localhost\Ubuntu\home\adams\repos
Rename-Item "ping-tree-ab-analysis" -NewName "experimentation-framework"
Rename-Item "epcvip-datalake-assistant" -NewName "data-platform-assistant"
```

## After Renaming

Once renamed, all file content updates will be applied automatically by the migration script.

## Status

- [ ] Rename ping-tree-ab-analysis → experimentation-framework
- [ ] Rename epcvip-datalake-assistant → data-platform-assistant
- [ ] Verify both folders exist with new names
- [ ] Continue with file content updates

