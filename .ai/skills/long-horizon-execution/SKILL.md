---
name: long-horizon-execution
description: Use when managing complex engineering agent tasks that span multiple execution sessions, subagent handoffs, research-to-code transitions, or require durable task state recovery.
---

# Long-Horizon Execution Skill

This skill governs the execution lifecycle of multi-session, long-horizon tasks, enforcing structured handoffs, context compaction protocols, research-to-code transitions, and crash-recovery procedures.

## Core Rules

1. **Durable Task State Manifest**:
   - Every long-horizon task MUST establish and update a durable state file (`.ai/templates/long-horizon-task.md` or `.ai/tasks/<task-id>/state.json`).
   - Never rely exclusively on session trajectory context; session context can be pruned or reset at any time.

2. **Research-to-Code Gate**:
   - Before editing code files in a complex feature/refactoring task, complete a research phase and record a Research-to-Code Handoff artifact.
   - Code execution MUST NOT begin without verified target outcomes, exact file change boundaries, and concrete verification steps.

3. **Context Compaction & Session Handoff**:
   - When context length exceeds 75% of model limits or when switching session boundaries, run a compaction pass.
   - Compacted context MUST retain: invariant objective, current phase, verified repository state, open risks, and exact next steps.

4. **Failure-Resume Protocol**:
   - When resuming a interrupted or failed session, DO NOT assume context in prompt memory matches repository disk state.
   - Re-inspect `git status`, `git diff`, and execute test suites to reconcile local disk state against the state manifest before performing edits.

5. **Cost & Token Burn Rate Guardrails**:
   - Track cumulative cost and token expenditure across sessions against budgeted caps (`max_total_cost_usd`, `max_sessions`).
   - Halt execution and request user approval (`L2_CHECKPOINT`) when cumulative expenditure reaches budget limits or after 3 consecutive failed retry loops.

## Execution Workflow

```text
INIT TASK -> RESEARCH PHASE -> HANDOFF ARTIFACT -> EXECUTE IN BATCHES -> VERIFY BATCH -> COMPACT/CHECKPOINT -> RESUME/COMPLETE
```

### 1. Task Initialization
- Assign unique `task_id` (e.g., `lh-20250512-refactor`).
- Initialize task state manifest with phase breakdown, token budget, and verification criteria.

### 2. Research & Exploration Pass
- Gather evidence using read-only inspection tools (`read_file`, `list_files`, `grep`).
- Formulate architectural hypotheses and verify them against codebase realities.
- Write Research-to-Code Handoff artifact.

### 3. Implementation Batches
- Execute changes in bounded batches (max 3-5 files per batch).
- Run narrow unit/integration tests after each batch.
- Update checkpoint state in state manifest.

### 4. Compaction & Cross-Session Resume
- Produce structured handoff snapshot prior to session end or context reset.
- Upon session resume: Read manifest -> Run `git status` / `git diff` -> Reconcile state -> Continue next subtask batch.

---

## Compatibility

- **CHAD Execution Runtime**: Orchestrates subagents across long-horizon phases and persists task manifests.
- **LapisLLM Inference Runtime**: Benefits from structured, compacted prompt inputs, maximizing prompt cache hit rates across multi-session trajectories.
