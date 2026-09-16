---
name: context-management
description: >
  Use when the working context is becoming saturated, the task must move to a
  new session, or the agent needs to hand off work without losing state.
---

# Context Management Skill

## When to Use

Use when the available context is no longer sufficient for reliable reasoning, when the user requests a fresh session, or when a long task needs a deliberate handoff.

## Workflow

1. Freeze implementation at a safe boundary.
2. Inspect current repository status and diff.
3. Record completed work, verification, open issues, and exact next steps.
4. Write a handoff using `references/handoff-protocol.md`.
5. In the next session, reload `AGENTS.md`, core files, and the handoff.
6. Re-verify repository state before continuing.

## Handoff quality

A handoff must be sufficient for another agent to resume without reconstructing hidden reasoning from chat history.

Include facts, not vague memory statements.

## Checklists

- [ ] Current commit/ref or working state identified.
- [ ] Changed files listed.
- [ ] Tests and commands recorded.
- [ ] Known failures recorded.
- [ ] Decisions recorded.
- [ ] Next action is concrete.
- [ ] Dangerous or pending operations are explicit.

## Stop conditions

Do not hand off while a destructive operation is partially executed or while the repository is in an unexplained state. Restore or clearly document the safe state first.

## Reference Files

- `references/handoff-protocol.md`
