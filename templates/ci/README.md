# CI Templates

GitHub Actions workflows for AI-assisted development.

## Contents

| File | Purpose |
|------|---------|
| [claude-qa-workflow.yml.template](./claude-qa-workflow.yml.template) | PR verification with Claude + Playwright |
| [qa-persona.md.template](./qa-persona.md.template) | QA engineer persona prompt |

## Claude QA Review

Automated PR verification using Claude Code with Playwright MCP.

### How It Works

```
PR opened → Label added → GitHub Action triggers → Claude explores app → Reports findings as PR comment
```

### Setup

1. **Copy templates** to your project:
   ```bash
   cp claude-qa-workflow.yml.template .github/workflows/claude-qa.yml
   cp qa-persona.md.template prompts/qa-persona.md
   ```

2. **Add secrets** to GitHub repository:
   - `ANTHROPIC_API_KEY` - Your Anthropic API key

3. **Customize** the persona prompt for your app's features

4. **Use** by adding the `qa-verify` label to any PR

### Trigger Methods

The workflow is triggered by adding a label:

```yaml
on:
  pull_request:
    types: [labeled]

jobs:
  qa-review:
    if: github.event.label.name == 'qa-verify'
```

To re-run: remove the label and re-add it.

### Customization Points

#### 1. Server Start Command
```yaml
- name: Start dev server
  run: |
    npm start &  # Change to your start command
    sleep 10
```

#### 2. Health Check URL
```yaml
- name: Wait for server health
  run: |
    curl -s http://localhost:3000/health  # Change to your health endpoint
```

#### 3. Test Focus Areas
Edit `qa-persona.md` to include your app's specific features and edge cases.

### Output

The workflow produces:
- **PR Comment**: Verification report with findings
- **Artifacts**: QA report and screenshots

### Example Report

```markdown
## QA Verification Report

### Verified Working
- [x] Login flow - Valid credentials succeed
- [x] Dashboard - Data loads correctly
- [x] Settings - Changes persist

### Issues Found
#### Issue 1: Button overlap on mobile
- **Severity**: Medium
- **Steps**: Open app on mobile viewport
- **Expected**: Buttons properly spaced
- **Actual**: Submit button overlaps cancel button

### Overall Assessment
PASS WITH NOTES
```

## Best Practices

1. **Persona Prompting**: Detailed personas improve Claude's testing approach
2. **Black-Box Testing**: Focus on user-visible behavior, not implementation
3. **Evidence**: Always request screenshots for issues
4. **Structured Output**: Use consistent report format for easy parsing

## Based On

- [Alex Op: Building AI QA Engineer](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/)
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)

## See Also

- [Testing Templates](../testing/README.md) - E2E testing patterns
- [MCP Workflow Guide](../testing/MCP_WORKFLOW_GUIDE.md) - Claude + browser automation
