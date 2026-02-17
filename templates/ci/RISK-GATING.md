# Risk-Based CI Gating

[← Back to CI README](./README.md)

Route CI checks by the **risk level of changed files**, not the existence of a PR. Docs-only changes skip expensive reviews; auth changes get the full suite.

> **When this is worth the complexity**: Team projects with distinct sensitive code areas (auth, payments, PII). Solo projects or repos with uniform risk can skip this — use flat security review instead.

## How It Works

```
PR opened
  │
  ▼
┌─────────────┐    risk-policy.json     ┌──────────────┐
│ classify job │ ◄───────────────────── │ path → tier  │
└──────┬──────┘                         └──────────────┘
       │ outputs: tier, checks, evidence_required
       │
       ├── tier = low ──────────────► done (no CI spend)
       │
       ├── tier = standard ─────────► security-review only
       │
       └── tier = critical/high ────► security-review + qa-review
                                        │
                                        ▼
                                   evidence artifact
```

Three files work together:

| File | Role |
|------|------|
| [`risk-policy.json.template`](./risk-policy.json.template) | Contract: maps paths → tiers, defines required checks per tier |
| [`scripts/classify-pr.sh`](./scripts/classify-pr.sh) | Classifier: reads policy + changed files, outputs highest tier |
| [`risk-preflight.yml.template`](./risk-preflight.yml.template) | Workflow: runs classifier, gates downstream jobs on tier |

## Setup

1. **Copy and customize the policy**:
   ```bash
   cp risk-policy.json.template .github/risk-policy.json
   # Edit path_rules to match YOUR repo's directory structure
   ```

2. **Copy the classifier**:
   ```bash
   mkdir -p .github/scripts
   cp scripts/classify-pr.sh .github/scripts/classify-pr.sh
   chmod +x .github/scripts/classify-pr.sh
   ```

3. **Copy the workflow**:
   ```bash
   cp risk-preflight.yml.template .github/workflows/risk-preflight.yml
   # Customize: server start command, port, dependencies
   ```

4. **Copy QA assets** (needed for high/critical tier reviews):
   ```bash
   mkdir -p .github/prompts
   cp qa-persona.md.template .github/prompts/qa-persona.md
   cp evidence-manifest.json.template .github/evidence-manifest.json
   ```

5. **Add secrets**: `ANTHROPIC_API_KEY` in repo settings.

## Risk Policy Schema

The policy file defines **tiers** and **path rules**:

```json
{
  "tiers": {
    "critical": {
      "required_checks": ["security-review", "qa-review"],
      "evidence_required": true,
      "auto_merge_allowed": false
    }
  },
  "path_rules": [
    { "pattern": "src/auth/**", "tier": "critical" }
  ],
  "default_tier": "standard"
}
```

**Rules are first-match**: order them from most specific to most general. Files not matching any rule get `default_tier`.

### Simplifying for Smaller Projects

Two-tier variant for simpler repos:

```json
{
  "tiers": {
    "high": {
      "required_checks": ["security-review"],
      "evidence_required": false
    },
    "low": {
      "required_checks": [],
      "evidence_required": false
    }
  },
  "path_rules": [
    { "pattern": "src/**", "tier": "high" },
    { "pattern": "*.md",   "tier": "low" }
  ],
  "default_tier": "high"
}
```

## Classifier Usage

The classifier script is standalone and testable outside CI:

```bash
# From args
./scripts/classify-pr.sh .github/risk-policy.json src/auth/login.ts README.md

# From stdin (pipe from git diff)
git diff --name-only origin/main | ./scripts/classify-pr.sh .github/risk-policy.json

# Output:
# {"tier":"critical","checks":["security-review","qa-review"],"evidence_required":true}
```

### Escape Hatch

For urgent hotfixes, skip the gate:

```bash
SKIP_RISK_GATE=1 ./scripts/classify-pr.sh .github/risk-policy.json src/auth/login.ts
# {"tier":"low","checks":[],"evidence_required":false,"skipped":true}
```

In the workflow, set the `SKIP_RISK_GATE` repository variable to `1` to bypass classification. This is intended for urgent hotfixes — remove it after the emergency.

## SHA Discipline

The preflight workflow captures `github.event.pull_request.head.sha` in the classify job and passes it to all downstream jobs via `needs.classify.outputs.head_sha`. Every checkout uses this pinned SHA:

```yaml
- uses: actions/checkout@v4
  with:
    ref: ${{ needs.classify.outputs.head_sha }}
```

**Why this matters**: Between when the classify job reads the diff and when the security/QA jobs run, the PR head can advance if the author pushes. Without SHA pinning, the review runs against code that wasn't classified — a merge safety gap.

The `synchronize` trigger ensures a new classification run starts whenever the PR head changes.

## Tamper Resistance

The classify job fetches the policy file and classifier script from the **base branch**, not the PR branch. This prevents a PR from modifying the gate to downgrade its own classification.

If the base branch doesn't have these files yet (bootstrapping — first PR that adds risk gating), the workflow falls back to the PR's own copies.

The template policy also classifies `.github/workflows/**`, `.github/scripts/**`, and `.github/risk-policy.json` as `critical`, ensuring that any change to the gate itself gets full review.

## Rerun Deduplication

When using automated CI comments (security findings, QA reports), avoid flooding PRs with duplicate comments on re-runs. Two patterns:

1. **SHA-stamped markers**: Include the head SHA in a hidden HTML comment at the top of your PR comment. Before posting, search for an existing comment with the same SHA and update it instead of creating a new one.

2. **Single-comment writer**: Designate one bot user per workflow and always update their most recent comment.

Our [hooks system](../hooks/README.md) uses SHA-hashed markers for local deduplication — the same principle applies in CI.

## Remediation Loop Guardrails

If your team wants to add automated fix-and-resubmit (a coding agent that remediates security findings), these guardrails prevent runaway loops:

| Guardrail | Why |
|-----------|-----|
| **Pin the model version** | Prevent behavior changes mid-loop |
| **Max iteration cap** (2-3) | Stop infinite fix-break cycles |
| **Skip stale comments** | Don't remediate findings from old SHAs |
| **Never bypass gates** | The fix must pass the same risk preflight |
| **Human review on critical** | Auto-fix for standard tier only; critical always needs human eyes |
| **Commit audit trail** | Each auto-fix gets its own commit with `[auto-remediate]` prefix |

We deliberately don't provide a remediation workflow template — the coding agent invocation is irreducibly repo-specific. These guardrails are the transferable pattern.

## Cost Impact

| Scenario | Without gating | With gating | Savings |
|----------|---------------|-------------|---------|
| Docs-only PR | ~$0.40 | $0 | 100% |
| Config change | ~$0.40 | $0 | 100% |
| Standard code PR | ~$0.40 | ~$0.20 | 50% |
| Critical path PR | ~$0.40 | ~$0.80 | -100% (more thorough) |

The savings compound: in a typical repo, 30-50% of PRs touch only docs, tests, or config.

## Where to Start

Best suited for repos with distinct auth/permissions code AND a web UI: **epcvip-admin** (RBAC matrix), **docs-site** (per-doc access control), **experiments-dashboard** (role-based test visibility). These have the highest ratio of mixed-risk PRs — a single sprint typically includes both docs-only and auth-touching changes, so risk gating saves the most CI spend there.

## See Also

- [DECISION_FRAMEWORK.md](./DECISION_FRAMEWORK.md) — Choose the right CI template for your project
- [evidence-manifest.json.template](./evidence-manifest.json.template) — Structured QA evidence schema
- [INCIDENT-MEMORY.md](./INCIDENT-MEMORY.md) — Post-mortem and harness-gap templates
- [qa-persona.md.template](./qa-persona.md.template) — QA persona with evidence output
