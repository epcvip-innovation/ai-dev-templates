---
id: first-feature
title: "Your First Feature with Claude Code"
description: "Guided walkthrough of building a feature end-to-end — from prompt to commit"
audience: beginner
---

# Your First Feature with Claude Code

[← Back to Main README](../../README.md)

A step-by-step walkthrough of building one feature with Claude Code. By the end, you'll understand the core loop you'll use every day.

> **Prerequisites**: Claude Code installed ([Quickstart](./CLAUDE-CODE-QUICKSTART.md)) and a project with a CLAUDE.md file ([New Project Setup](./NEW-PROJECT-SETUP.md)).

---

## The Loop

Every feature follows the same cycle:

```
Describe  →  Implement  →  Review  →  Commit
   ↑                                    │
   └────────────────────────────────────┘
```

This guide walks through one pass of this loop.

---

## Step 1: Start a Session

Navigate to your project and start Claude Code:

```bash
cd ~/your-project
claude
```

Claude automatically reads your `CLAUDE.md` file. This gives it your project's purpose, tech stack, critical warnings, and navigation — before you say anything.

**Verify it has context**: Ask something about your project.

```
> What does this project do?
```

Claude should answer based on your CLAUDE.md. If it doesn't know, your CLAUDE.md may need a Purpose section (see [New Project Setup](./NEW-PROJECT-SETUP.md)).

---

## Step 2: Describe What You Want

Tell Claude what to build in plain language:

```
> Add a function that validates email addresses. Include tests.
```

Claude will:
1. Read relevant files in your project to understand the existing structure
2. Propose an approach (which files to create/edit, what pattern to follow)
3. Wait for your approval before making changes

### Writing good prompts

| Approach | Example |
|----------|---------|
| **Specific** (better) | "Add an email validation function to src/utils/ with unit tests" |
| **Vague** (still works) | "Add email validation" |
| **Too vague** (likely to miss) | "Improve the code" |

You don't need to be precise about implementation details — Claude reads your codebase and figures out where things go. But be specific about *what* you want built.

---

## Step 3: Let Claude Work

Claude creates and edits files. For each change, you'll see:

- **File diffs**: What Claude wants to add, remove, or change
- **Permission prompts**: Claude asks before running commands or editing files

### Permissions

When Claude asks to run a command or edit a file, you choose:

| Response | When to use |
|----------|-------------|
| **Allow** | You understand what it's doing and it looks right |
| **Allow always** | Common safe operations (reading files, running tests) |
| **Deny** | Something looks wrong or you want to redirect |

You can also interrupt at any point. Say "wait" or "stop" to pause, then redirect:

```
> Actually, put that in src/lib/ instead of src/utils/
```

---

## Step 4: Review

After Claude finishes implementing, review the work:

```
> /local-review --quick
```

This runs 3 parallel review agents that check for bugs, security issues, and code quality problems. You'll see a findings report with severity levels.

If issues are found, Claude will fix them:

```
> Fix the issues found in the review
```

You can also review manually — read the diffs, run your test suite, try the feature.

---

## Step 5: Commit

When you're satisfied with the changes:

```
> commit this
```

Claude examines all changes, writes a descriptive commit message, and creates the commit. Review the message before confirming.

If your project has a `/push` skill configured ([see skills](../../templates/slash-commands/README.md)), you can use that instead for additional quality checks before pushing.

---

## What You Just Learned

- **The daily loop**: Describe → Implement → Review → Commit. This is the core workflow for everything from bug fixes to features.
- **Natural language works**: You describe intent, Claude figures out implementation. Be specific about *what*, flexible about *how*.
- **CLAUDE.md is your project's memory**: It loads automatically and gives Claude the context to make good decisions. Invest in keeping it accurate.
- **Review is not optional**: `/local-review` catches issues that are easy to miss. Build the habit of reviewing before committing.

---

## Common Beginner Mistakes

**Starting without CLAUDE.md**: Claude has no project context and will make generic decisions. Even a 20-line CLAUDE.md with your tech stack and key commands makes a significant difference.

**Overloading a session**: Trying to fix a bug, add a feature, and refactor in one session leads to confused context. One concern per session — use `/clear` between unrelated tasks.

**Not reviewing AI output**: Always read diffs before approving. Claude is good but not perfect. Understanding what changed is part of the development process.

**Fighting the tool**: If Claude suggests an approach you don't like, redirect it instead of manually editing and then confusing the session. Say "instead, do it this way..." and let Claude handle it.

---

## Next Steps

| Ready for... | Go to |
|-------------|-------|
| The daily development rhythm | [Daily Workflow](../setup-guides/DAILY-WORKFLOW.md) |
| Setting up your own project | [New Project Setup](./NEW-PROJECT-SETUP.md) |
| Browsing reusable patterns | [Template Library](../../templates/README.md) |
| Power-user techniques | [Advanced Workflows](../reference/ADVANCED-WORKFLOWS.md) |
| Understanding context management | [Context Engineering](../reference/CONTEXT-ENGINEERING.md) |

---

## See Also

- [Quickstart](./CLAUDE-CODE-QUICKSTART.md) — 5-minute Claude Code install
- [Getting Started](./SETUP-GUIDE-2026.md) — Full platform setup (Mac, Windows, Linux)
- [New Project Setup](./NEW-PROJECT-SETUP.md) — Configure CLAUDE.md, permissions, skills
- [Daily Workflow](../setup-guides/DAILY-WORKFLOW.md) — Everyday usage patterns
- [Advanced Workflows](../reference/ADVANCED-WORKFLOWS.md) — Context, planning, agents, predictability

---
