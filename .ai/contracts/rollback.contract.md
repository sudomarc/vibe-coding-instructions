# Standard Transactional Rollback & State Compensation Contract

## Metadata
- **contract_id**: `rollback_governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Define a provider-neutral, evidence-based governance contract for transaction boundaries, side-effect recording, automated LIFO saga unwinding, compensating operations, and failure recovery across autonomous AI agent executions.

---

## 1. Architectural Model & Scope

When an AI agent (such as an Orchestrator, Coder, or Specialist) performs a multi-step task, individual operations introduce state mutations into the workspace, git working tree, system processes, build artifacts, or external systems.

If the task fails due to an unexpected error, a test regression, a security violation (`SAFETY_TRIGGERED`), or a human abort, the runtime must not leave the environment in a corrupt or indeterminate state.

```text
       Agent Execution Step [i]
                  │
                  ▼
   Evaluate Reversibility Tier
   (PURE_REVERSIBLE | COMPENSABLE | FORWARD_FIX_ONLY | IRREVERSIBLE)
                  │
                  ├─ If IRREVERSIBLE ──> Block for Human Checkpoint Approval
                  │
                  ▼
   Append Mutation & Inverse to Journal (journal.jsonl)
                  │
                  ▼
         Execute Mutation Step
                  │
     ┌────────────┴────────────┐
   Success                   Failure / Abort
     │                         │
     ▼                         ▼
 Proceed to Step [i+1]    Initiate LIFO Saga Rollback
                               │
                               ├─ Inverse Action Execution (Step n..1)
                               ├─ Verification Probe per Step
                               └─ Emit Rollback Telemetry & Update State
```

---

## 2. Reversibility Taxonomy

Every mutating operation planned or dispatched by an agent must be classified into one of four reversibility tiers:

| Reversibility Tier | Description | Recovery Strategy | Permission & Checkpoint Rules |
|---|---|---|---|
| `PURE_REVERSIBLE` | Complete, deterministic restoration is guaranteed without side-effects (e.g. creating/editing clean git-tracked files, isolated scratch dirs). | Automated rollback via direct inverse action (e.g. `git checkout -- <file>`, file deletion). | Standard execution permitted without user prompt. |
| `COMPENSABLE` | The exact prior state cannot be restored natively, but a compensating transaction neutralizes the side-effect (e.g. killing a spawned preview daemon, uninstalling a sandboxed package, dropping a temporary test database). | Automated compensation sequence defined explicitly before execution. | Allowed within bounded sandbox; audit-logged. |
| `FORWARD_FIX_ONLY` | Reversal is impractical or introduces further corruption (e.g. partial data migration across shared tables, complex multi-branch git merge conflicts). | System halts mutation, flags state as `FORWARD_FIX_REQUIRED`, and generates a compensatory migration plan. | Requires explicit human checkpoint if risk is elevated. |
| `IRREVERSIBLE` | Mutation cannot be undone and has permanent external consequences (e.g. remote API mutations, credit charges, email dispatch, `git push --force` to shared remotes). | Cannot be rolled back automatically. | **Mandatory human checkpoint** before invocation. |

---

## 3. Append-Only Side-Effect Journaling (`journal.jsonl`)

The runtime environment (CHAD) maintains a tamper-resistant, append-only journal of all mutating side-effects for the active task session.

### Schema Specification
Each entry in `journal.jsonl` adheres to the following JSON structure:

```json
{
  "entry_id": "jrn-20250330-001",
  "trace_id": "tr-20250330-agent-01",
  "step_index": 3,
  "agent_id": "coder-alpha",
  "tool_id": "write_file",
  "reversibility_tier": "PURE_REVERSIBLE",
  "idempotency_key": "write_src_auth_ts_v2",
  "target_resource": "src/auth.ts",
  "forward_action": {
    "command": "write_file",
    "parameters_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "prior_state_checksum": "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  },
  "compensating_action": {
    "action_type": "RESTORE_CONTENT | DELETE_FILE | EXECUTE_SHELL | API_CALL",
    "command": "restore_file",
    "payload": {
      "filepath": "src/auth.ts",
      "snapshot_path": ".ai/snapshots/src_auth.ts.bak"
    },
    "timeout_seconds": 15
  },
  "verification_probe": {
    "probe_type": "FILE_CHECKSUM | COMMAND_EXIT_CODE | PORT_CHECK",
    "expected_value": "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  },
  "status": "RECORDED | COMMITTED | COMPENSATED | COMPENSATION_FAILED",
  "timestamp": "2025-03-30T14:22:00Z"
}
```

### Invariants:
1. **Pre-mutation Logging**: The journal record MUST be flushed to disk before the mutating tool executes.
2. **Deterministic Inverse**: The `compensating_action` must be fully formulated and self-contained; it must not depend on future agent inference.
3. **Snapshot Isolation**: When mutating files, prior file contents or git blob SHAs must be captured before writing changes.

---

## 4. LIFO Saga Unwinding Strategies

When an execution failure occurs, the rollback supervisor selects one of three strategies:

1. `AUTOMATED_SAGA_UNWIND`
   - **Condition**: All executed steps in the journal are `PURE_REVERSIBLE` or `COMPENSABLE`, and no manual intervention was requested.
   - **Procedure**:
     - Traverse the journal in strict **Last-In, First-Out (LIFO)** order.
     - For each entry, execute `compensating_action`.
     - Run `verification_probe` immediately following each step.
     - If all probes pass, transition task state to `ROLLBACK_COMPLETED` and yield `GOAL_BLOCKED` or `FAILURE_ESCALATED`.

2. `SUPERVISED_ROLLBACK_CHECKPOINT`
   - **Condition**: A step marked `FORWARD_FIX_ONLY` failed, or a compensating action failed its verification probe.
   - **Procedure**:
     - Halt automatic unwinding.
     - Freeze the workspace state.
     - Emit a structured incident report detailing remaining uncompensated mutations.
     - Require human operator approval to either attempt manual compensation or accept current state.

3. `QUARANTINE_MANUAL_HOLD`
   - **Condition**: An unexpected filesystem permission error, hardware error, or security boundary violation (`SAFETY_TRIGGERED`) occurs during rollback.
   - **Procedure**:
     - Immediately isolate the container/workspace.
     - Mark task status as `QUARANTINE_HOLD`.
     - Do not execute further automated commands.

---

## 5. Compensation Verification Gates & Telemetry

A rollback is not considered complete merely because compensating commands exited with returncode 0. Every rollback must satisfy strict verification gates.

### Verification Gates:
1. **Repository Cleanliness Check**: `git status --porcelain` matches baseline state prior to task initiation.
2. **Process Integrity Probe**: Any daemons, background test servers, or headless browser instances spawned during the task are verified killed (`lsof`, `pgrep`).
3. **Artifact Cleanup Check**: Ephemeral build directories, lock files, or temporary output files are removed.

### Telemetry Schema (`rollback_telemetry`):
```json
{
  "event_type": "ROLLBACK_EXECUTION",
  "trace_id": "tr-20250330-agent-01",
  "task_id": "task-883",
  "strategy": "AUTOMATED_SAGA_UNWIND",
  "total_mutations_recorded": 5,
  "mutations_compensated": 5,
  "uncompensated_count": 0,
  "duration_ms": 1240,
  "status": "SUCCESS | PARTIAL_FAILURE | QUARANTINED",
  "verification_gate_results": {
    "git_cleanliness": true,
    "process_cleanup": true,
    "artifact_cleanup": true
  },
  "timestamp": "2025-03-30T14:22:15Z"
}
```

---

## 6. Ecosystem Boundary & Runtime Responsibilities

### CHAD Runtime Layer
- CHAD maintains the runtime state machine for transaction lifecycles (`ACTIVE`, `COMMITTED`, `ROLLING_BACK`, `ROLLED_BACK`, `QUARANTINE_HOLD`).
- CHAD enforces pre-mutation logging to `journal.jsonl` before calling tool execution wrappers.
- CHAD coordinates LIFO unwinding and runs verification probes upon receiving failure signals or step budget exhaustion.

### LapisLLM Model Layer
- LapisLLM classifies intended operations by `reversibility_tier` during plan generation.
- LapisLLM constructs explicit `compensating_action` specifications whenever generating plans involving `COMPENSABLE` tool invocations.
- If LapisLLM detects an `IRREVERSIBLE` step, it flags the step with a mandatory human checkpoint requirement before emitting tool call requests.
