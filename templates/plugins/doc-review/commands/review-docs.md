---
description: "Review markdown documentation for quality, accuracy, links, and consistency"
argument-hint: "[file-or-directory] [--quick] [--fix]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Edit", "Task", "AskUserQuestion"]
---

# Documentation Review

Run a multi-agent review of markdown files for link correctness, content quality, AI writing patterns, and cross-file consistency.

**Review Target:** "$ARGUMENTS"

## Review Workflow

1. **Determine Scope**
   - If a file path is given, review that file
   - If a directory is given, review all `.md` files in it
   - If no argument, review uncommitted `.md` changes via `git diff --name-only HEAD -- '*.md'`
   - `--quick`: run link-checker and content-quality only (skip AI patterns and cross-file)
   - `--fix`: after review, offer to apply fixes interactively

2. **Gather File List**
   - Run `git diff --name-only HEAD -- '*.md'` or Glob for the target
   - Read each file to get: headings, links, frontmatter, word count
   - Build a shared context summary for agents

3. **Identify Applicable Reviews**
   Based on scope:
   - **Always**: link-checker, content-quality
   - **Unless `--quick`**: ai-pattern-detector
   - **If 2+ files and not `--quick`**: cross-file-analyzer
   - **If `--fix` and issues found**: apply fixes after review

4. **Launch Review Agents**

   Launch applicable agents in **parallel** using the Task tool. Pass each agent:
   - The list of files to review
   - The file contents or paths
   - Any relevant context (frontmatter, publish status)

   ```
   Task(subagent_type: "doc-review:link-checker", prompt: "Review these files: ...")
   Task(subagent_type: "doc-review:content-quality", prompt: "Review these files: ...")
   Task(subagent_type: "doc-review:ai-pattern-detector", prompt: "Review these files: ...")
   Task(subagent_type: "doc-review:cross-file-analyzer", prompt: "Review these files: ...")
   ```

5. **Aggregate Results**

   After agents complete, produce a consolidated report:

   ```markdown
   # Doc Review: {scope}

   ## Summary
   - **Files Reviewed**: {count} | **Total Words**: {word_count}
   - **Links**: {total} checked, {broken} broken, {suspect} suspect
   - **Content Issues**: {bloat} brevity, {structural} structural
   - **AI Patterns**: {count} detected
   - **Cross-File**: {duplicates} duplications, {conflicts} conflicts

   ## Critical Issues
   [Issues that must be fixed — broken links, factual errors, conflicts]

   ## Important Issues
   [Issues that should be fixed — bloat, stale refs, AI patterns]

   ## Suggestions
   [Nice-to-have improvements — structural, style, maintenance notes]
   ```

6. **Fix Mode** (if `--fix` passed)
   - For each fixable issue (broken links with known targets, bloat, AI patterns):
     - Show before/after
     - Ask user to confirm
     - Apply with Edit tool
   - Skip non-fixable issues (conflicts, structural, cross-file duplications)

## Usage Examples

**Full review of uncommitted docs:**
```
/doc-review:review-docs
```

**Review a specific file:**
```
/doc-review:review-docs tools/experimentation-toolkit/docs/ONBOARDING.md
```

**Review a directory:**
```
/doc-review:review-docs docs/epcvip-docs-obsidian/AI Infrastructure/
```

**Quick check (links + content only):**
```
/doc-review:review-docs --quick
```

**Review and fix:**
```
/doc-review:review-docs path/to/file.md --fix
```

## Agent Descriptions

**link-checker**:
- Validates all relative file links exist on filesystem
- Checks anchor links resolve to actual headings
- Flags cross-repo links that break on docs.epcvip.vip
- Detects missing .md extensions and orphaned reference definitions

**content-quality**:
- Flags filler phrases, redundant qualifiers, padding sentences
- Checks heading hierarchy, code block language tags, table formatting
- Verifies factual claims against other files in scope
- Reports word count per section, flags sections over 500 words

**ai-pattern-detector**:
- Scans for significance inflation, copula avoidance, superficial -ing phrases
- Detects rule-of-three overuse, negative parallelisms, em dash overuse
- Flags boldface overuse, sycophantic tone, generic positive conclusions
- Reports pattern name and location — does not rewrite (use /humanizer for that)

**cross-file-analyzer**:
- Identifies substantially similar content across files
- Detects conflicting information (same topic, different facts)
- Finds stale cross-references (links to headings that moved or were renamed)
- Notes maintenance risk for intentional duplication

## Tips

- Run before committing documentation changes
- Use `--quick` for pre-commit sanity checks
- Use full review for directory-wide audits
- Pair with `/humanizer` to fix detected AI patterns
- Address broken links first — they affect readers immediately
