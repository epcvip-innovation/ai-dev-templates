# Quality Rubric

8-criteria validation rubric for generated skills. Score each criterion as **Pass** or **Needs Work**.

---

## Criteria

### 1. Fit to Purpose

Does the skill solve the problem stated in Q1?

| Pass | Needs Work |
|------|------------|
| Instructions directly address the stated purpose | Instructions are generic or miss the core task |
| Output format matches what the user described in Q4 | Output doesn't match the expected deliverable |

### 2. Element Justification

Is every section justified by discovery answers?

| Pass | Needs Work |
|------|------------|
| Every section traces back to a specific discovery answer | Sections included "just in case" or by habit |
| Optional frontmatter fields are only present when justified | Unnecessary fields like `model` or `agent` added without reason |

**Common failure**: Including `allowed-tools` restriction when the skill genuinely needs broad tool access, or adding `context: fork` when there's no context isolation need.

### 3. Complexity Appropriateness

Is the structure as simple as possible for the task?

| Pass | Needs Work |
|------|------------|
| Simple task → steps only, no phases | Simple task with phase structure and arguments table |
| Complex task → phases with sub-steps | Complex task with only vague high-level steps |
| Reference files used only for >50-line content | Short lists moved to references/ unnecessarily |

**Common failure**: Using the Workflow Automation phase structure for a task that's really just 3 sequential steps.

### 4. Usability

Can a user trigger and use the skill without reading external docs?

| Pass | Needs Work |
|------|------------|
| Description includes 3+ natural trigger phrases | Only the /name trigger works |
| Negative triggers prevent false positives | Triggers on adjacent but wrong queries |
| Examples show realistic usage | Examples are abstract or trivial |

### 5. Completeness

Are all required sections present?

| Pass | Needs Work |
|------|------------|
| Has: frontmatter, guardrails, instructions, examples, troubleshooting | Missing guardrails or troubleshooting |
| References exist for any >50-line content | Long inline sections that should be extracted |
| Troubleshooting covers the 3 most likely failure modes | Only 1 generic troubleshooting entry |

**Required sections** (every skill): frontmatter, one-line summary, guardrails (NEVER/ALWAYS), instructions, examples (2+), troubleshooting (2+ entries).

### 6. Spec Adherence

Does it follow security restrictions and frontmatter rules?

| Pass | Needs Work |
|------|------------|
| Name: no reserved prefixes | Name starts with "claude-" or "anthropic-" |
| Description: concise, within context budget | Description too verbose, wastes shared budget |
| Body: under 500 lines | Body exceeds limit without references/ |
| No XML in frontmatter | Angle brackets in YAML values |

This criterion is binary — any spec violation is a hard fail.

### 7. Actionability

Are instructions concrete enough for Claude to follow without interpretation?

| Pass | Needs Work |
|------|------------|
| Steps specify exact actions: "Read file X", "Run command Y" | Steps say "analyze the code" without specifying how |
| Guardrails are specific: "Never report confidence <70" | Guardrails are vague: "Be careful" |
| Output format is precisely defined | Output format is "a summary" |

**Test**: Could a different Claude session follow these instructions and produce substantially the same output? If not, the instructions need more specificity.

### 8. Trigger Quality

Will the description achieve 90%+ trigger accuracy?

| Pass | Needs Work |
|------|------------|
| 3+ natural language trigger phrases included | Only 1-2 phrases |
| Phrases match how users actually talk | Phrases are formal or technical jargon |
| Negative triggers exclude adjacent skills | No negative triggers; will conflict with similar skills |
| File types or contexts mentioned where relevant | Generic description that could match too broadly |

**Test**: Read the description and imagine 10 different users asking for this task. Would 9+ of their phrasings match the trigger patterns?

---

## Scoring Summary

```
Criteria                      Score
─────────────────────────────────────
1. Fit to Purpose             [Pass / Needs Work]
2. Element Justification      [Pass / Needs Work]
3. Complexity Appropriateness [Pass / Needs Work]
4. Usability                  [Pass / Needs Work]
5. Completeness               [Pass / Needs Work]
6. Spec Adherence             [Pass / Needs Work]
7. Actionability              [Pass / Needs Work]
8. Trigger Quality            [Pass / Needs Work]

Result: N/8 Pass
```

**Threshold**: 7/8 Pass to ship. 6/8 is acceptable with a plan to fix. Below 6/8, iterate before installing.

**Spec Adherence (criterion 6) is a hard gate** — if it fails, the skill must be fixed regardless of other scores.

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| Over-engineering | Simple task has 4 phases, 3 reference files, arguments table | Strip back to steps; remove unjustified structure |
| Vague instructions | "Analyze the code and report findings" | Specify: "Read each changed file, check for X, Y, Z patterns" |
| Description too narrow | Only triggers on exact /name command | Add 3+ natural language phrases users would say |
| Description too broad | Triggers on every code-related query | Add negative triggers; narrow the context |
| Missing guardrails | Skill produces inconsistent output | Add NEVER/ALWAYS rules for the most important behaviors |
| Unnecessary references/ | 20-line checklist in a separate file | Inline short content; only extract >50 lines |
