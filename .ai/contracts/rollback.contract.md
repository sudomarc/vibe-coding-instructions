# Transactional Rollback & State Compensation Governance Contract

## Metadata
- **contract_id**: `rollback_governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions
- **status**: `ACTIVE`
- **scope**: Provider-neutral transactional rollback, side-effect compensation semantics, reversibility classification, append-only mutation journaling, and automated Saga recovery protocols across AI agent task executions.

---

## 1. Purpose & Core Principles

When autonomous AI agents (`coder`, `orchestrator`, `analyst`, or domain specialists) execute multi-step engineering tasks, individual actions mutate state across workspaces, VCS branches, environment configurations, dependencies, databases, and external network services.

If a task halts unexpectedly—due to unexpected verification failures, execution exceptions, safety triggers (`SAFETY_TRIGGERED`), concurrency contention (`CONCURRENCY_CONTENTION_BLOCKED`), or resource exhaustion (`MAX_BUDGET_REACHED`)—leaving partial side-effects leads to corrupt environments, broken builds, dangling locks, and inconsistent states.

This contract defines the provider-neutral governance policy for:
1. **Reversibility Classification**: Categorizing tool mutations by rollback feasibility prior to execution.
2. **Append-Only Side-Effect Journaling**: Tracking fine-grained pre-mutation states and compensating inverses.
3. **LIFO Saga Unwinding**: Deterministically compensating mutations in reverse chronological order.
4. **Compensation Verification Gates**: Validating that post-rollback state strictly matches baseline state.
5. **Rollback Telemetry**: Emitting traceable records for auditability and incident recovery.

---

## 2. Reversibility Taxonomy (`reversibility_tiers`)

Every mutating tool invocation (`.ai/contracts/tool.contract.md`) must be evaluated against the standard reversibility taxonomy before execution:

| Reversibility Tier | Description | Recovery Strategy | Examples | Autonomy Tier Permitted |
|---|---|---|---|---|
| `PURE_REVERSIBLE` | Invertible without loss of external information or state mutation side-effects. | Automated inverse operation executed immediately on failure. | Workspace file edits (restored via git checkout or buffer cache), newly created scratch files (deleted). | L0 - L4 |
| `COMPENSABLE` | State change cannot be strictly undone, but a deterministic semantic inverse restores equivalence. | Compensating transaction executed via compensating action handler. | Database record insertions (soft delete/tombstone), acquired distributed resource locks (explicit release), temporary preview server processes (process termination). | L1 - L4 |
| `FORWARD_FIX_ONLY` | Mutation has created non-deterministic downstream side-effects; inverse does not restore parity. | Halts execution, blocks automated rollback, and requires forward remediation plan. | Data schema migrations with column drops or irreversible data backfills, merged Git commits on shared branches. | L2 - L4 (with human checkpoint) |
| `IRREVERSIBLE` | Action cannot be compensated, reversed, or restored by software automation. | Pre-execution human approval checkpoint required; automated rollback prohibited. | Production deployments, credential rotations, third-party webhook dispatches, permanent data purges (`PURGE_HARD_DELETE`). | L0 only (requires explicit human approval) |

---

## 3. Append-Only Side-Effect Journal Schema (`side_effect_journal`)

Runtimes (CHAD) supervising autonomous agents MUST maintain an append-only side-effect journal (`journal.jsonl` or in-memory ring buffer) during task execution.

### Journal Entry Schema
```json
{
  "journal_id": "jrn-20250415-001",
  "trace_id": "tr-20250415-agent-abc",
  "step_index": 3,
  "agent_id": "coder-alpha",
  "tool_id": "write_file",
  "permission_tier": "WORKSPACE_WRITE",
  "reversibility_tier": "PURE_REVERSIBLE | COMPENSABLE | FORWARD_FIX_ONLY | IRREVERSIBLE",
  "target_resource": "src/auth/jwt.py",
  "pre_mutation_state": {
    "type": "FILE_SNAPSHOT",
    "content_hash": "sha256:4a3b8...",
    "existed_prior": true,
    "snapshot_ref": ".ai/state/snapshots/jwt.py.bak"
  },
  "compensating_action": {
    "tool_id": "restore_file",
    "parameters": {
      "filepath": "src/auth/jwt.py",
      "target_hash": "sha256:4a3b8..."
    },
    "idempotent": true
  },
  "status": "APPLIED | COMPENSATED | FAILED_TO_COMPENSATE",
  "timestamp": "2025-04-15T10:15:30Z"
}
```

### Pre-Mutation Snapshot Requirements
1. **File Overwrites**: Pre-mutation content must be captured (via hash or copy in ephemeral snapshot storage) before calling `write_file` or `replace_with_git_merge_diff`.
2. **File Creations**: Recorded as `existed_prior: false`; compensating action is `delete_file`.
3. **Environment/Processes**: Recorded process PID and bound ports; compensating action is `kill_process` and lock release.
4. **Git Operations**: Base commit hash (`HEAD`) recorded before staging/committing.

---

## 4. LIFO Saga Unwinding Workflow (`saga_unwinding`)

When a task encounters an unrecoverable error or stop condition, the runtime triggers the Saga Unwinding workflow:

```text
[Task Active: Steps 1 -> 2 -> 3]
               │
               ▼ (Execution Aborted / Stop Condition)
[Evaluate Rollback Policy]
   ├─ If all steps are PURE_REVERSIBLE or COMPENSABLE:
   │    │
   │    ▼
   │  [AUTOMATED_SAGA_UNWIND (LIFO)]
   │    ├─ Step 3: Execute Compensating Action 3 ──► Verified OK
   │    ├─ Step 2: Execute Compensating Action 2 ──► Verified OK
   │    └─ Step 1: Execute Compensating Action 1 ──► Verified OK
   │
   ├─ If any step is FORWARD_FIX_ONLY:
   │    ▼
   │  [SUPERVISED_ROLLBACK_CHECKPOINT] (LIFO rollback up to non-reversible boundary, then prompt human)
   │
   └─ If any step is IRREVERSIBLE:
        ▼
      [QUARANTINE_MANUAL_HOLD] (Preserve state, freeze environment, request human takeover)
```

### Unwinding Execution Rules
1. **Reverse Chronological Order (LIFO)**: Step $N$ must be compensated and verified before Step $N-1$ compensation begins.
2. **Idempotence Constraint**: All compensating actions MUST be idempotent. If a compensating action is re-run, it must succeed without producing cumulative side-effects.
3. **Timeout & Budgeting**: Compensation actions operate under a dedicated recovery timeout budget (maximum 60 seconds per step).
4. **Lock Reclamation Integration**: Rollback of acquired resource locks (`.ai/contracts/concurrency-lock.contract.md`) is guaranteed upon completion or termination of the rollback phase.

---

## 5. Compensation Verification Gates (`verification_gates`)

Automated rollback is not considered complete until verifiable evidence proves the baseline state is restored:

1. **Workspace Diff Verification**:
   - `git status --porcelain` must show clean state for tracked files touched during the task.
   - Ephemeral scratch files created during the failed task must be confirmed deleted via filesystem check.
2. **Process & Lock Hygiene**:
   - Background processes started by the failed task must be confirmed terminated (`lsof` / `pgrep`).
   - Concurrency locks registered in the CHAD lock manager must be transitioned to `RELEASED`.
3. **Artifact Integrity**:
   - If build caches or lockfiles were touched, verify lockfile syntax and dependency integrity (`validate_instructions.py` or package manager check).

---

## 6. Rollback Telemetry & Incident Schema

All rollback operations emit structured audit telemetry conforming to `.ai/contracts/tool-audit.contract.md`:

```json
{
  "event_type": "ROLLBACK_INITIATED | STEP_COMPENSATED | ROLLBACK_COMPLETED | COMPENSATION_FAILED",
  "trace_id": "tr-20250415-agent-abc",
  "task_id": "task-impl-auth-tokens",
  "orchestrator_id": "orchestrator-main",
  "total_steps_journaled": 4,
  "steps_compensated": 4,
  "reversibility_profile": "PURE_REVERSIBLE",
  "unwind_strategy": "AUTOMATED_SAGA_UNWIND",
  "verification_gate_passed": true,
  "duration_ms": 340,
  "error_cause": {
    "stop_condition": "GOAL_BLOCKED",
    "message": "Type checking failed with 3 errors in unresolvable third-party import"
  },
  "timestamp": "2025-04-15T10:16:05Z"
}
```

---

## 7. CHAD & LapisLLM Runtime Compatibility

### CHAD Agent Runtime Layer
- Maintains the append-only side-effect journal in memory or ephemeral storage.
- Automatically captures pre-mutation snapshots before invoking mutating tools.
- Executes LIFO Saga unwinding upon unhandled task errors or stop conditions (`SAFETY_TRIGGERED`, `GOAL_BLOCKED`, `MAX_BUDGET_REACHED`).
- Runs compensation verification gates before re-dispatching tasks or surfacing results to the user.

### LapisLLM Model Runtime Layer
- Evaluates reversibility tiers during task planning and decomposes complex workflows into compensable batches.
- Avoids interleaving `IRREVERSIBLE` or `FORWARD_FIX_ONLY` operations with routine code edits without explicit checkpoints.
- Generates idempotent compensating instructions in plan schemas.
