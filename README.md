# Vibe Coding Instructions

A portable instruction repository for disciplined AI-assisted software development.

## Why this exists

AI coding agents are fast at producing plausible code. The failure mode is often not syntax; it is acting before the problem is understood, expanding scope, trusting assumptions, skipping verification, or making irreversible changes too casually.

This repository provides a small operating system around the model:

`PROMPT → PLAN → IMPLEMENT → VERIFY → REPORT`

The goal is not to make agents slower. The goal is to spend compute and human attention on the decisions that have the highest failure cost.

## Design principles

The repository separates durable rules from task-specific procedures. Core rules are loaded every session. Skills are loaded on demand. Reference files carry deeper checklists. Assets carry examples.

This is progressive disclosure: enough policy to start safely, more detail only when the task needs it.

## Quick use

1. Copy or link `AGENTS.md` into the project root.
2. Keep `.ai/core/` available to the coding agent.
3. Keep `.ai/skills/` available for on-demand loading.
4. For Claude Code, retain `CLAUDE.md` as the automatic entry point.
5. For Copilot, retain `.github/copilot-instructions.md`.
6. Read `docs/quickstart.md` for a five-minute installation path.

## Core invariant

**Never write implementation code before an actionable plan exists and is approved when approval is required.**

The invariant applies to application code, configuration, migrations, scripts, CI changes, and infrastructure. A tiny change may use a tiny plan; it may not skip planning entirely.

## What this project does not do

It does not replace project-specific security policy, framework guidance, compliance requirements, code ownership rules, or human review. It does not grant an agent permission to perform destructive operations. It does not make uncertain output trustworthy merely by formatting it.

## Tree

```text
vibe-coding-instructions/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── .ai/
│   ├── core/                 # Always-loaded operating principles
│   ├── skills/               # Task-triggered procedures
│   ├── templates/            # Reusable work artifacts
│   └── meta/                 # Prompt-engineering guidance
├── .github/
│   └── copilot-instructions.md
└── docs/
    ├── quickstart.md
    ├── anti-patterns.md
    └── faq.md
```

## The core layer

`00-identity.md` defines the agent's role and boundaries.
`01-mindset.md` defines five principles.
`02-workflow.md` defines PLAN → IMPLEMENT → VERIFY.
`03-communication.md` standardizes status and uncertainty.
`04-constraints.md` defines absolute and soft constraints.

## The skills layer

Each skill uses Anthropic-style YAML frontmatter and a predictable body:

- When to Use
- Workflow
- Checklists
- Reference Files

This keeps triggering explicit and discovery shallow.

## Contribution model

Changes should preserve stable terminology and internal links. Update the most specific document rather than duplicating a rule in multiple places. Examples may evolve without changing the governing principle.

Before changing the instruction system itself, run a structural review: check file presence, frontmatter, path references, internal terminology, and accidental contradictions.

## License and reuse

The repository is intentionally plain Markdown so teams can adapt it to their own agent stack. Add a repository license appropriate to the project before distributing it under a formal open-source license.
