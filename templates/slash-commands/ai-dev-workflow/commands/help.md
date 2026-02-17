---
description: Display a list of all available slash commands
allowed-tools: run_terminal_cmd
---

## Command

I will display a list of all available slash commands by scanning this directory and extracting the description from each command file.

```bash
echo "✅ Available Slash Commands"
echo "───────────────────────────────"

# Recursively find all command files and parse them to handle subdirectories
COMMANDS_DIR="./.claude/commands"
find "$COMMANDS_DIR" -name "*.md" -type f | while read -r file; do
    # Get the relative path from the commands dir, remove .md extension
    REL_PATH=$(realpath --relative-to="$COMMANDS_DIR" "$file" | sed 's/\.md$//')

    # Don't process the README file
    if [ "$REL_PATH" = "README" ]; then
        continue
    fi

    # Replace slashes with colons for the command name
    COMMAND_NAME=$(echo "$REL_PATH" | sed 's/\//:/g')

    # Get the description
    DESCRIPTION=$(awk -F': ' '/^description:/ {for (i=2; i<=NF; i++) printf "%s ", $i; print ""; exit}' "$file" | sed 's/ $//')

    printf "  /%-25s - %s\n" "$COMMAND_NAME" "$DESCRIPTION"
 done

echo ""
echo "───────────────────────────────"
echo "For a detailed guide to the workflow, see .claude/commands/WORKFLOW_GUIDE.md"
```

