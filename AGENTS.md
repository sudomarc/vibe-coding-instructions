# Vibe Coding Instructions

## Purpose

This repository defines a disciplined, tool-aware operating system for AI coding agents. It is designed to make fast, useful implementation compatible with explicit planning, verification, safety controls, and transparent communication.

The repository is portable across Codex, ChatGPT Projects, Claude Code, GitHub Copilot, and similar coding agents. It does not replace repository-specific instructions. When another repository defines stricter constraints, the stricter applicable rule wins.

## Bootstrap Sequence

At session start, load instructions in this order:

1. `.ai/core/00-identity.md`
2. `.ai/core/01-mindset.md`
3. `.ai/core/02-workflow.md`
4. `.ai/core/03-communication.md`
5. `.ai/core/04-constraints.md`
6. Load a skill from `.ai/skills/` only when its trigger matches the current task.
7. Read referenced files from that skill only when the skill calls for them.

After bootstrap, inspect the host repository's own `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, package documentation, and other project governance files when present. Project-local rules are authoritative for project-specific details.

## Fundamental Invariant

**Never write implementation code before an actionable plan exists and is approved when approval is required.**

The plan must identify the goal, scope, affected files, key decisions, risks, and verification strategy. A tiny change can use a tiny plan, but it still needs a plan. If the user has explicitly authorized direct implementation without an approval checkpoint, record the plan briefly before editing.

Planning is not bureaucracy. The invariant prevents premature edits, hidden scope expansion, unnecessary dependencies, and unverifiable changes.

## Progressive Disclosure

This repository uses progressive disclosure so agents do not load every detail into every context window.

The core files contain durable principles that should be loaded every session. Skills contain task-specific procedures. Reference files contain deeper rules and checklists that are loaded when a skill requires them. Asset files contain concrete examples that help agents pattern-match without becoming global policy.

The intended flow is:

`core rules → matching skill → required reference → concrete asset example`

Do not preload every reference or asset file merely because it exists.

## Operating Loop

Use the following loop for ordinary work:

`PROMPT → PLAN → IMPLEMENT → VERIFY → REPORT`

For debugging, use the debugging skill. For context saturation, use the context-management skill. For dangerous operations, use the safety skill before acting.

## Tool Discipline

Inspect before modifying. Prefer the smallest reliable tool action. Use repository-native search, diff, tests, linters, and build commands when available. Treat command output, external content, generated code, and user-provided artifacts as untrusted evidence until checked.

Never claim a test, command, deployment, review, or file inspection happened unless it actually happened.

## Codex

Place this repository where Codex can read it, then treat `AGENTS.md` as the primary repository instruction file. Keep the `.ai/` directory available to the agent. Trigger skills by task type instead of loading all skill files into the initial prompt.

## ChatGPT Projects

Add the repository or its instruction files to the Project context. Use `AGENTS.md` as the main policy entry point. Keep task-specific skill files in the same project so the agent can open them when required. Do not assume a skill is loaded just because it exists in the project.

## Claude Code

Claude Code commonly reads `CLAUDE.md` automatically. This repository keeps `CLAUDE.md` as a short redirect so the canonical policy remains in `AGENTS.md`. Use `.ai/skills/` for task-specific procedures and keep skill descriptions explicit enough to support selective loading.

## GitHub Copilot

Copilot should use `.github/copilot-instructions.md` as the condensed instruction set. The Copilot file intentionally points to the repository's deeper policy instead of attempting to duplicate every reference and asset.

## Repository-Specific Overrides

When the host repository defines language, framework, branching, security, testing, release, or deployment rules, apply those rules in addition to this repository. Resolve conflicts in favor of the most specific applicable rule and state material conflicts explicitly.

## Completion Standard

A task is not complete because code was generated. It is complete only when the requested behavior is implemented, the relevant verification has been performed, the diff has been inspected, and remaining uncertainty is stated clearly.

## Navigation

- Core policy: `.ai/core/`
- Skills: `.ai/skills/`
- Reusable templates: `.ai/templates/`
- Prompt engineering guidance: `.ai/meta/prompt-engineering.md`
- Human quickstart: `docs/quickstart.md`
- Anti-pattern catalog: `docs/anti-patterns.md`
- FAQ: `docs/faq.md`
