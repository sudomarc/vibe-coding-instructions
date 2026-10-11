# Skill: Long-Horizon Execution & Multi-Session Governance

## Quick reference
- Contract: `.ai/contracts/long-horizon-task.contract.md`
- State File Location: `.ai/tasks/<task_id>/state.json`
- Handoff Template: `.ai/templates/handoff.md`

## Overview
Long-horizon engineering tasks span multiple execution sessions, high tool-call trajectories, multi-agent delegations, and large codebase refactorings. This skill provides operational procedures for maintaining state continuity, executing research-to-code transitions, recovering from unexpected runtime interruptions, and enforcing budget controls across sessions.

---

## Operating Loop for Long-Horizon Execution

```text
TASK INITIALIZE → CHECKPOINT RESTORE → PHASE EXECUTION → PROGRESS VERIFICATION → COMPACTION/HANDOFF
```

### Phase 1: Task Initialization & State Hydration
1. Read `.ai/tasks/<task_id>/state.json` if resuming, or initialize a new state file conforming to `.ai/contracts/long-horizon-task.contract.md`.
2. Re-inspect repository state and git status before executing any plan steps.
3. Verify budget limits (`budget_cap_usd`) and token usage metrics.

### Phase 2: Research-to-Code Handoff Workflow
1. Complete research and architecture exploration.
2. Produce a validated `RESEARCH_TO_CODE_HANDOFF` JSON artifact containing confirmed ADRs, verified technical facts, and target file boundaries.
3. Pass the research artifact to the `coder` agent. Coder agents MUST NOT proceed with implementation until research claims are explicitly verified.

### Phase 3: Failure-Resume Protocol
When resuming from an interruption, crash, or session timeout:
1. Load the last checkpoint from `checkpoints` array in `.ai/tasks/<task_id>/state.json`.
2. Execute `git diff` and compare workspace state against `state_snapshot_hash`.
3. Discard corrupted or half-written temporary files.
4. Resume execution from the last unverified step.

### Phase 4: Context Compaction & Cross-Session Handoff
1. Monitor context window consumption.
2. Trigger compaction when input tokens exceed 75% capacity or after 10 execution turns.
3. Export state snapshot to `.ai/templates/handoff.md`.
4. Preserve objective, verified facts, decisions, failed attempts, and exact next actions. Prune raw tool outputs and stale narration.

---

## CHAD & LapisLLM Integration Guidelines

- **CHAD Engine**: Persists multi-session states to `.ai/tasks/<task_id>/state.json` automatically at every phase transition and verifies execution budget limits before delegating subtasks.
- **LapisLLM Gateway**: Utilizes KV-cache state preservation across sessions and strictly validates structured handoff artifacts against JSON schemas.
