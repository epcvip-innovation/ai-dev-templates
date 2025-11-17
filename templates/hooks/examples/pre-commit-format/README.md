# Pre-Commit Format Hook (Example)

**Type**: PostToolUse hook
**Use case**: Auto-format code after git adds files
**Pattern**: Automation hook (never blocks)

## What It Does

Automatically formats code files when added to git:
- Python files → black formatter
- JavaScript/TypeScript files → prettier

## Installation

```bash
# Copy to user hooks directory
cp pre-commit-format.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/pre-commit-format.py

# Add to ~/.claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/pre-commit-format.py"
          }
        ]
      }
    ]
  }
}
```

## Requirements

- `black` for Python formatting: `pip install black`
- `prettier` for JS/TS formatting: `npm install -g prettier`

## Example Usage

```bash
# Claude adds files to git
git add my_script.py utils.js

# Hook automatically formats both files
✅ Formatted 1 Python file(s)
✅ Formatted 1 JS/TS file(s)
```

## Customization

Add more formatters:

```python
# Format Rust files
rust_files = [f for f in files if f.endswith('.rs')]
if rust_files:
    subprocess.run(['rustfmt'] + rust_files)
```
