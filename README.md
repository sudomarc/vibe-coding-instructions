# Vibe Coding Instructions

A repository-native instruction system for disciplined AI coding agents.

## Why this exists

AI coding agents are capable of producing large changes quickly. The failure mode is not only bad code. It is also premature coding, misunderstood architecture, silent scope expansion, unverifiable claims, dependency drift, accidental destructive actions, and loss of context across sessions.

This repository turns those concerns into a layered operating system:

- always-on core policy for identity, mindset, workflow, communication, and constraints;
- task-specific skills for planning, implementation, debugging, review, security, testing, and engineering domains;
- references for detailed procedures and edge cases;
- examples and assets for pattern matching without polluting every context window;
- templates for plans, tasks, handoffs, and commits;
- compatibility guides for Codex, Claude Code, ChatGPT Projects, and GitHub Copilot;
- a master prompt for environments that cannot load a repository of instructions automatically.

## Design basis

The design deliberately borrows architectural ideas from public agent ecosystems rather than copying their text. Anthropic's published skill-development material emphasizes a required `SKILL.md`, YAML metadata, explicit triggering, progressive disclosure, and optional bundled resources. Anthropic's public Claude Code repository also demonstrates specialized review agents and task-focused skills. OpenAI's Codex repository documents scoped `AGENTS.md` instructions, while the OpenAI Cookbook demonstrates persistent plans and iterative development workflows. GitHub documents repository-wide, path-specific, and agent instruction mechanisms for Copilot.

See `docs/sources.md` for the source list and the boundaries between source facts and this repository's original synthesis.

## Core philosophy

### Plan before code

Every implementation begins with an observable goal, bounded scope, known constraints, and a verification strategy. Tiny changes use tiny plans; complex changes use living plans.

### Decompose ruthlessly

Break large work into independently verifiable batches. Each batch should have a clear purpose and a stop condition.

### Verify, do not assume

Use repository tools, tests, type checks, linters, builds, diffs, and runtime checks as evidence. Do not replace evidence with confidence.

### Surface uncertainty

State unknowns, assumptions, conflicting evidence, unverified behavior, and environment limitations explicitly.

### Simplicity over cleverness

Prefer the smallest architecture that correctly satisfies the requirement and fits existing project patterns.

## Full workflow

`PROMPT → INSPECT → PLAN → IMPLEMENT → VERIFY → REVIEW → REPORT`

The workflow changes for debugging and incident response, but the same evidence standard remains.

## Directory map

```text
.
├── AGENTS.md
├── CLAUDE.md
├── MASTER-PROMPT.md
├── .ai/
│   ├── core/
│   ├── skills/
│   ├── templates/
│   └── meta/
├── .github/
│   ├── copilot-instructions.md
│   ├── instructions/
│   └── prompts/
└── docs/
```

## Using it in another repository

Copy the policy entry files and the `.ai/` directory into the target repository. Preserve the same paths so cross-references remain valid. Then adapt only project-specific sections: runtime, framework, commands, architecture, branching, test commands, deployment procedures, and ownership rules.

Do not blindly copy project-specific rules from this repository into another project. This repository defines a general operating system, not application-specific truth.

## What this repository does not do

It does not guarantee perfect agent behavior. Instruction-following is probabilistic, tools vary, repositories contain ambiguous requirements, and verification can have blind spots. The purpose is to create a repeatable decision framework that makes those failure modes visible and easier to detect.

## Further reading

Start with `docs/quickstart.md`, then inspect `MASTER-PROMPT.md` and the relevant skill. For source attribution, read `docs/sources.md`.
