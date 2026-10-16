---
name: long-horizon-execution
description: This skill must be used when an engineering task spans multiple sessions, involves subagent delegation, requires research-to-code synthesis, or consumes significant token budgets over time.
---

# Long-Horizon Execution Skill

## Purpose

Provide practical execution guidelines for engineering agents navigating long-horizon, multi-session tasks while maintaining strict decision quality, failure-resume integrity, token economy, and budget controls.

---

## Operational Loop for Long-Horizon Tasks

```text
STATE INIT -> RESEARCH & ADR -> BATCH IMPLEMENT -> INCREMENTAL VERIFY -> COMPACT / HANDOFF -> RESUME
```

---

## 1. Multi-Session Task Lifecycle

1. **Initialization (`INIT`)**:
   - Inspect `.ai/templates/long-horizon-task.md` or `.ai/contracts/long-horizon-task.contract.md`.
   - Establish explicit task boundaries, non-goals, and budget limits.

2. **Research-to-Code Synthesis (`RESEARCHING` -> `PLANNING`)**:
   - Synthesize research notes into architectural decisions (`ADR`) and interface contracts.
   - Validate trade-off choices against repository code before writing implementation plans.
   - Emit a formal `ResearchToCodeHandoff` artifact.

3. **Batched Execution & Incremental Verification (`EXECUTING` -> `VERIFYING`)**:
   - Divide code modifications into small, self-contained batches (1-3 files per batch).
   - Verify every batch immediately using narrow, targeted test/typecheck commands.
   - Update the living task plan after each verification pass.

4. **Compaction & Handoff (`SUSPENDED` / `HANDOFF READY`)**:
   - When context pressure rises or budget soft caps (80%) are reached, freeze execution.
   - Record durable state snapshot using `.ai/templates/long-horizon-task.md`.
   - Never purge failed attempts or verified architectural decisions.

5. **Resumption (`SUSPENDED` -> `EXECUTING`)**:
   - Read the task snapshot.
   - **Re-inspect Repository**: Run `git status`, `git diff`, and baseline build commands. Repository evidence ALWAYS outranks stale snapshot notes.
   - Resume execution from the first unfulfilled task in the resumption checklist.

---

## 2. Context Management & Compaction Rules

- **Hot vs. Cold Context**: Keep active task objective, active batch code, and recent test failure details in HOT context. Prune past full file dumps or raw tool execution outputs into COLD context.
- **Compaction Guard**: Compact only when facts, decisions, and failure trajectory entries are recorded in durable task state files.

---

## 3. Failure-Resume Protocol

For any failed attempt during long-horizon execution:
1. Log attempt details in the durable failure log (`.ai/templates/long-horizon-task.md`).
2. Record root cause and conditions under which the approach might be reconsidered.
3. Apply retry circuit breakers: if a step fails 3 times, pause and trigger escalation.

---

## 4. Cost & Budget Invariants

- **Token Soft Cap (80%)**: Initiate compaction/pruning pass.
- **Token Hard Cap (100%)**: Suspend execution, persist task snapshot, and escalate to human operator.
- **Cost Savings Invariant**: Cost controls must never compromise safety, verification completeness, or repository state integrity.
