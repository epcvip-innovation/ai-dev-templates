# GitHub Actions Decision Framework

How to choose the right CI templates based on project complexity, team size, and language.

---

## Quick Decision Tree

```
Is this a personal/hobby project?
├── Yes → Security Review Only
└── No → Continue...
    │
    Does it have auth/payments/sensitive data paths?
    ├── Yes → Add Risk Preflight (risk-gated CI)
    │         └── Does it have a web UI?
    │             ├── Yes → Risk Preflight + QA (evidence-gated)
    │             └── No → Risk Preflight (security only on critical paths)
    └── No → Continue...
        │
        Does it have a web UI?
        ├── Yes → Add QA Review (path-triggered)
        └── No → Security Review Only
            │
            Is it an enterprise/team project?
            ├── Yes → Full Suite + Label-Based QA
            └── No → Security Review + Selective QA
```

---

## Template Selection Matrix

| Project Type | Recommended Templates | Cost/PR |
|-------------|----------------------|---------|
| Static site, docs | None (GitHub Pages handles) | $0 |
| Personal CLI/utility | `security-review.yml` | $0.10-0.30 |
| Personal web app | `security-review.yml` + `claude-qa-workflow.yml` (path-triggered) | $0.30-0.80 |
| Team web app | Full suite with path triggers | $0.50-1.50 |
| Team app with sensitive paths | `risk-preflight.yml` + path-gated security + evidence-gated QA | $0-1.50 (tier-dependent) |
| Enterprise | Full suite + label-based QA + manual triggers | Variable |

---

## Available Templates

### 0. Risk Preflight (`risk-preflight.yml.template`)

**Purpose:** Classify PR risk by changed files, then gate security and QA checks by tier

**When to use:**
- Team projects with distinct sensitive code areas (auth, payments, PII)
- When you want docs-only PRs to skip expensive reviews
- When critical paths need QA evidence artifacts, not just PR comments

**Requires:**
- `risk-policy.json` — path → tier mapping (customize from template)
- `scripts/classify-pr.sh` — standalone classifier

**Cost:** $0 for low-tier PRs, up to ~$1.50 for critical-tier (security + QA + evidence)

**See:** [RISK-GATING.md](./RISK-GATING.md) for full setup guide

---

### 1. Security Review (`security-review.yml.template`)

**Purpose:** Scan for security vulnerabilities on every PR

**When to use:**
- Every project with code (default)
- Runs on all PRs, cheap and fast

**Triggers:**
```yaml
on:
  pull_request:
    types: [opened, synchronize]
```

**Cost:** ~$0.10-0.30 per PR

**What it checks:**
- OWASP top 10 vulnerabilities
- Hardcoded secrets
- Dependency vulnerabilities
- Authentication/authorization issues

---

### 2. QA Review (`claude-qa-workflow.yml.template`)

**Purpose:** Browser-based QA using Claude + Playwright MCP

**When to use:**
- Projects with web UI
- When visual/UX bugs matter
- Path-triggered to avoid running on every PR

**Triggers (recommended):**
```yaml
on:
  pull_request:
    paths:
      - 'src/components/**'
      - 'src/pages/**'
      - 'public/**'
      - '*.css'
      - '*.html'
```

**Cost:** ~$0.50-1.50 per PR (higher due to browser interaction)

**What it checks:**
- Visual rendering
- User flows
- Accessibility basics
- Responsive behavior

---

## Path-Specific Triggers

For larger projects, use path filters to run expensive workflows only when relevant:

```yaml
# Only run QA when frontend changes
on:
  pull_request:
    paths:
      - 'src/components/**'
      - 'src/pages/**'
      - 'src/styles/**'
      - 'public/**'

# Only run API tests when backend changes
on:
  pull_request:
    paths:
      - 'src/api/**'
      - 'src/services/**'
      - 'prisma/**'
```

---

## Label-Based Triggers

For manual control over expensive workflows:

```yaml
# Only run when labeled
on:
  pull_request:
    types: [labeled]

jobs:
  qa-review:
    if: contains(github.event.pull_request.labels.*.name, 'needs-qa')
    # ...
```

**Use case:** Enterprise projects where you want human decision on when to run QA.

---

## Cost Optimization

### Strategies

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| Path triggers | 50-70% | May miss cross-cutting changes |
| Label triggers | 80-90% | Requires manual intervention |
| Draft PR skip | 20-30% | None - drafts shouldn't run CI |
| Cache dependencies | 10-20% | Slightly more complex setup |

### Skip on Draft PRs

```yaml
jobs:
  qa-review:
    if: github.event.pull_request.draft == false
    # ...
```

---

## By Language/Framework

### TypeScript/JavaScript

```yaml
# Recommended
- security-review.yml    # Always
- qa-review.yml          # If web UI, path-triggered

# Quality checks (in workflow)
- npm run lint
- npm run typecheck
- npm run test
```

### Python

```yaml
# Recommended
- security-review.yml    # Always
- qa-review.yml          # If web UI (Django/Flask)

# Quality checks (in workflow)
- ruff check .
- mypy .
- pytest
```

### Go

```yaml
# Recommended
- security-review.yml    # Always

# Quality checks (in workflow)
- go vet ./...
- go test ./...
- golangci-lint run
```

---

## Team Size Considerations

### Solo Developer

```
├── security-review.yml (always)
└── qa-review.yml (optional, path-triggered)
```

- Keep it simple
- Path triggers to save costs
- No label-based workflows needed

### Small Team (2-5)

```
├── security-review.yml (always)
├── qa-review.yml (path-triggered)
└── CODEOWNERS (for review assignments)
```

- Add CODEOWNERS for automatic review assignments
- Consider branch protection rules

### Large Team / Enterprise

```
├── security-review.yml (always)
├── qa-review.yml (label-triggered)
├── CODEOWNERS (complex ownership)
├── Branch protection (required reviews)
└── Environment approvals (for deploy)
```

- Label-based QA for cost control
- Required reviews before merge
- Environment-specific approvals

---

## Integration with Claude Code Plugins

### Local Review Before PR

Run `/local-review` before creating PR:

```bash
# Review changes locally (free, faster)
/local-review --scope staged

# If clean, create PR
gh pr create
```

### CI as Safety Net

CI catches what local review might miss:
- Cross-browser issues (Playwright)
- Dependency vulnerabilities (npm audit)
- Issues introduced by merge conflicts

---

## Example Configurations

### Minimal (Personal Project)

```yaml
# .github/workflows/security.yml
name: Security Review
on: [pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-security-review@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Standard (Team Project)

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-security-review@v1

  qa:
    if: |
      contains(github.event.pull_request.labels.*.name, 'needs-qa') ||
      contains(github.event.pull_request.changed_files, 'src/components')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          prompt_file: .github/prompts/qa-persona.md
          mcp_config: .github/mcp-config.json
```

---

## Security Notes

From Anthropic documentation:

- **Trusted PRs only** - Not hardened against prompt injection
- **Require approval** for external contributors
- **Never expose API keys** in logs
- **Use least-privilege** permissions

```yaml
permissions:
  contents: read
  pull-requests: write  # For comments
```

---

## See Also

- [claude-qa-workflow.yml.template](./claude-qa-workflow.yml.template)
- [security-review.yml.template](./security-review.yml.template)
- [qa-persona.md.template](./qa-persona.md.template)
- [risk-preflight.yml.template](./risk-preflight.yml.template) — Risk-gated CI workflow
- [RISK-GATING.md](./RISK-GATING.md) — Risk-based CI guide
- [INCIDENT-MEMORY.md](./INCIDENT-MEMORY.md) — Post-mortem and harness-gap templates
- [../plugins/code-review/](../plugins/code-review/README.md) - Local review before PR
