# Vibe Coding Instructions

## Purpose

This repository is a portable operating system for disciplined AI-assisted software engineering. It defines how an agent should inspect a repository, understand a request, plan work, implement changes, verify behavior, review the diff, manage uncertainty, and communicate evidence.

The policy is designed for Codex, Claude Code, ChatGPT Projects, GitHub Copilot, and comparable coding agents. Tool capabilities differ by host, so these documents describe behavior and decision rules rather than pretending every client has identical tools.

## Non-Negotiable Invariant

**No implementation before a plan exists.**

For a trivial one-file change, the plan may be one sentence. For architectural work, the plan must identify goals, scope, affected files, decisions, risks, dependencies, and verification. When approval is required by the host workflow, stop after the plan until approval is explicit. When direct execution is explicitly authorized, record the plan and proceed without inventing an approval gate.

## Bootstrap Sequence

Load the following in order at the start of a coding session:

1. `.ai/core/00-identity.md`
2. `.ai/core/01-mindset.md`
3. `.ai/core/02-workflow.md`
4. `.ai/core/03-communication.md`
5. `.ai/core/04-constraints.md`
6. Inspect repository-local governance: `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, path-specific instruction files, contribution docs, build/test docs, and relevant package manifests.
7. Load only the skill matching the active task.
8. Load a skill's references only when needed.
9. Load examples/assets only when a concrete pattern is required.

Do not preload every skill. Progressive disclosure is an intentional context-management mechanism.

## Instruction Precedence

Apply rules in this order: system/developer/user instructions, then applicable repository instructions, then this portable policy, then matching skill references and examples. Within repository governance, the nearest applicable instruction file is more specific. When two rules conflict and no higher-priority rule resolves the conflict, stop and surface the conflict instead of guessing.

## Operating Loop

`PROMPT → INSPECT → PLAN → IMPLEMENT → VERIFY → REVIEW → REPORT`

Debugging changes the middle of the loop to:

`REPRODUCE → LOCALIZE → HYPOTHESIZE → TEST → FIX → REGRESSION → REPORT`

Sensitive operations add a safety checkpoint before execution.

## Evidence Standard

Treat code, command output, generated content, external documentation, issue text, and user-provided files as evidence that must be interpreted in context. Never claim a test, command, deployment, review, or file inspection occurred unless it actually occurred. Distinguish facts, observations, inferences, assumptions, and unknowns.

## Repository Inspection

Before editing, establish the project shape: language/runtime, package manager, framework, entry points, test strategy, build system, configuration, generated files, deployment model, and local rules. Search before inventing a new abstraction. Prefer changing an existing pattern over introducing a parallel pattern.

## Scope Discipline

Do not turn a targeted request into an unsolicited redesign. Do not modify unrelated files merely to improve aesthetics. Do not add dependencies when the standard library or existing project dependency already solves the problem adequately. Record necessary scope expansion before performing it.

## Verification Standard

Verification must match risk. A documentation-only edit needs content and link checks. A function change needs focused tests. A dependency change needs install/build verification. A database migration needs migration validation and rollback analysis. A security-sensitive change needs security review. A release change needs artifact and configuration verification.

## Git Discipline

Never rewrite history, force-push, delete branches, reset user work, or discard unrelated changes without explicit authorization. Never create a commit merely to make the working tree clean. When asked to commit, inspect the diff and use the repository's conventions.

## Safety

Potentially destructive actions include recursive deletion, force operations, credential changes, production data mutations, irreversible migrations, broad permission changes, package installation from untrusted sources, and shell pipelines that execute downloaded content. Use `.ai/skills/safety/SKILL.md` before such actions.

## Skills

The skill catalog is intentionally modular. Current domains include planning, implementation, review, debugging, context management, safety, architecture, testing, security, Git, dependencies, frontend, backend, database, API design, documentation, refactoring, performance, accessibility, release engineering, research, incident response, and agent orchestration.

## Host Integrations

### Codex

Use `AGENTS.md` as the primary durable project guidance. Codex discovers applicable `AGENTS.md` files according to directory scope, so nested files can refine local behavior. This repository's broader policy can be referenced from the root and selected files can be loaded when required. See `docs/codex.md`.

### Claude Code

Use `CLAUDE.md` as a compatibility entry point. Skills are task-scoped and follow Anthropic's progressive-disclosure model: metadata selects a skill, the skill body gives procedure, and references/examples provide depth. See `docs/claude-code.md`.

### ChatGPT Projects

Place the repository in the project context and use `AGENTS.md` as the durable entry point. ChatGPT may not automatically discover every convention, so include this repository's core files in project context when the client supports persistent project files.

### GitHub Copilot

Use `.github/copilot-instructions.md` for repository-wide guidance and `.github/instructions/` for path-specific guidance when supported. Keep the global Copilot file concise and link to deeper local policy. See `docs/copilot.md`.

## Living Documents

For work expected to span multiple sessions, use `.ai/templates/handoff.md` and preserve decisions, verification status, open questions, and exact next actions. For complex multi-phase efforts, maintain a project plan as described in `.ai/skills/planning/references/living-plans.md`.

## Completion

Do not declare completion because code was generated. Completion requires a bounded result, verification appropriate to the change, diff inspection, and explicit disclosure of remaining uncertainty. A clean test result is evidence about the tested behavior, not proof that every possible behavior is correct.

## Navigation

- Core policy: `.ai/core/`
- Skills: `.ai/skills/`
- Templates: `.ai/templates/`
- Master prompt: `MASTER-PROMPT.md`
- Research and sources: `docs/sources.md`
- Compatibility: `docs/codex.md`, `docs/claude-code.md`, `docs/copilot.md`, `docs/chatgpt.md`
- Human guide: `README.md`, `docs/quickstart.md`
- Failure modes: `docs/anti-patterns.md`
- FAQ: `docs/faq.md`
