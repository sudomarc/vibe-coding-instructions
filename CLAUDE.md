# Claude Code Entry Point

This file is a compatibility entry point for Claude Code.

## Canonical policy

Read `AGENTS.md` first. It is the canonical repository policy and defines the bootstrap sequence, fundamental invariant, progressive-disclosure model, and completion standard.

## Claude Code behavior

Claude Code should treat this file as an automatic doorway into the repository instructions, not as a second policy source. Avoid maintaining contradictory rules here.

When a task matches one of the task-specific procedures, load the appropriate `.ai/skills/<skill>/SKILL.md` file. Then load only the references named by that skill that are needed for the current work.

Relevant skills include:

- planning for architectural planning and scope definition;
- implementation for controlled coding batches;
- review for self-audit and diff inspection;
- debugging for evidence-driven fault isolation;
- context-management for session handoffs;
- safety for destructive, privileged, irreversible, or high-impact actions.

Claude Code must inspect project-local instructions before changing files. Repository-specific rules override generic examples in this repository when they are more specific.

Do not claim that tests, tools, or inspections ran unless they actually ran. Do not silently broaden scope. Preserve user intent while making uncertainty explicit.
