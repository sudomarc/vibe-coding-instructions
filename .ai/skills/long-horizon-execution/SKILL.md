---
name: long-horizon-execution
description: Skill for governing long-horizon, multi-session engineering agent tasks spanning research-to-code transitions, checkpointing, compaction, and failure recovery.
---

# Long-Horizon Task Execution Skill

## Purpose
Guide engineering agents through multi-session, multi-step tasks while maintaining strict state continuity, budget enforcement, evidence protocol compliance, and deterministic recovery.

## Long-Horizon Operating Loop

```text
INIT
 │
 ▼
RESEARCH & SPECIFICATION
 │ (Research-to-Code Handoff Artifact)
 ▼
CHECKPOINT (Multi-Session Task State)
 │
 ▼
IMPLEMENTATION BATCHES
 │ (Context Compaction Trigger)
 ▼
VERIFICATION & TEST PROBE
 │
 ├─► Success ──► FINAL HANDOFF & COMPLETED
 │
 └─► Failure ──► FAILURE-RESUME RECOVERY ──► RESUME AT CHECKPOINT
```

---

## 1. Multi-Session Epoch & Checkpoint Protocol

1. **Epoch Initialization**:
   - Every session restoration increments `session_epoch` by 1.
   - Read the latest checkpoint file (`.ai/state/task_<id>_checkpoint.json`).
   - Re-inspect repository state (`git status`, `git diff`) before executing any tools. Repository evidence always outranks stale context summaries.

2. **Checkpoint Creation Criteria**:
   - Create a new checkpoint snapshot whenever:
     a) Research phase completes and transitions to implementation.
     b) A coherent implementation batch completes verification.
     c) The active context approaches 75% capacity and compaction is required.
     d) The task is paused or handed off to another agent session.

---

## 2. Research-to-Code Transition Rules

1. **Structured Handoff**:
   - Research agents MUST NOT write production application code directly.
   - Research agents produce a `RESEARCH_TO_CODE_HANDOFF` artifact listing key findings, architectural constraints, acceptance criteria, and verified source locations.

2. **Handshake Verification**:
   - The implementing Coder agent validates the handoff artifact, verifying that cited file locations exist and constraints are actionable before making edits.

---

## 3. Failure-Resume & Recovery Procedure

When a task fails mid-execution due to model errors, tool execution crashes, or session interrupts:

1. **Locate Last Valid Checkpoint**: Inspect `.ai/state/` or the latest handoff document.
2. **Re-establish Baseline Evidence**:
   - Run `git status` to identify modified, added, or untracked files.
   - Execute test probes on modified modules to establish what is working and what is broken.
3. **Compare State with Checkpoint**:
   - If code changes match the checkpoint state, resume from the next pending subtask.
   - If code changes are inconsistent or unverified, revert unverified edits and resume from the last passing checkpoint.
4. **Circuit Breaker Check**:
   - If the same subtask fails 3 times, trip status to `GOAL_BLOCKED` and escalate to the Orchestrator or human reviewer.

---

## 4. Token & Cost Budget Discipline

1. **Phase Token Caps**:
   - Research & Discovery: ≤ 30% of total token allocation.
   - Batch Implementation: ≤ 50% of total token allocation.
   - Verification & Documentation: ≤ 20% of total token allocation.

2. **Compaction Rules**:
   - Compact context before running expensive test suites or multi-file inspections.
   - Preserve only HOT context: goal statement, latest checkpoint metadata, verified diff summary, failing test logs, and next action.
