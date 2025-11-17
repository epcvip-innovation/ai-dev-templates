# AI-Assisted Development Slash Command Templates

**Purpose:** Reusable, battle-tested slash command templates to bootstrap structured AI workflows.

This repository contains multiple workflow templates and separates deployable commands from design documentation.

---

## 📦 Available Workflow Templates

### 1. AI Development Workflow (Core)
Complete feature development lifecycle with planning, execution, and quality gates.

- **[View AI Dev Workflow Guide](./ai-dev-workflow/WORKFLOW_GUIDE.md)**
- **Copy to:** `.claude/commands/` in your project

**Contains:**
- Feature lifecycle commands (start, resume, complete)
- Planning & design commands (plan-approaches, validate-plan)
- Quality & debugging commands (ai-review, debug-failure)
- Context management commands (session-handoff, audit-artifacts)

### 2. Query Building Workflow (Domain-Specific)
Specialized commands for SQL query generation and validation.

- **Location:** `./query-building-workflow/commands/`
- **Copy to:** `.claude/commands/query/` in your project

**Contains:**
- `/query:build-query` - Build new queries from natural language
- `/query:enhance-query` - Enhance existing queries
- `/query:generate-query` - Template-based query generation

---

## 🧠 Design Rationale and Philosophy

The design documentation explains the "why" behind these workflows - their evolution, core principles, and key design decisions.

- **[Read the Design Rationale](./DESIGN_RATIONALE.md)**

This is intended for developers who want to understand, maintain, or contribute to the templates themselves.

---

## 🚀 Quick Start

**For most projects:**
1. Copy `ai-dev-workflow/` contents to `.claude/commands/`
2. Optionally add `query-building-workflow/commands/` to `.claude/commands/query/`
3. Start with `/help` to see available commands

**For query-focused projects:**
- Use query-building-workflow as your starting point
- Add specific ai-dev-workflow commands as needed
