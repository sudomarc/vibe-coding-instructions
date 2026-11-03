# Transactional Rollback & State Compensation Contract

This contract defines the governance specification for tracking side-effect mutations, managing state snapshots, and executing deterministic rollback and compensation workflows (Saga unwinding) across autonomous agent runs in the CHAD + LapisLLM ecosystem.

---

## 1. Governance Purpose & Invariants

Autonomous agents frequently execute multi-step plans involving filesystem edits, build artifacts, process executions, database operations, or external network transactions. When an agent run halts unexpectedly due to:
- Stop conditions (`MAX_BUDGET_REACHED`, `GOAL_BLOCKED`, `SAFETY_TRIGGERED`),
- Unhandled tool exceptions (`TOOL_EXEC_ERR`),
- Plan defects or verification failure (`VERIF_FALSE_POS`), or
- Circuit breaker trip or human checkpoint rejection,

the execution environment risks remaining in a corrupted, inconsistent, or dirty state.

### Core Invariants
1. **No Silent State Poisoning**: Every mutating action MUST be registered in an active Side-Effect Journal before or immediately upon execution.
2. **Deterministic Unwinding (LIFO)**: Rollback operations MUST compensate mutations in reverse chronological order (Last-In, First-Out) to respect dependency hierarchies.
3. **Explicit Verification of Compensation**: A rollback is not considered complete until compensating actions are verified against repository evidence.
4. **Safety Over Complete Unwind**: If a compensating action is itself high-risk (`PRIVILEGED_MUTATION`) or ambiguous, the runtime MUST pause and request human intervention rather than guess.

---

## 2. Reversibility Tiers Taxonomy

Every mutation registered by a tool or agent is categorized into one of four reversibility tiers:

| Tier | Name | Description | Compensation Mechanism |
|---|---|---|---|
| **R0** | `PURE_REVERSIBLE` | Bit-for-bit restorable local mutations (e.g., modifying tracked workspace files, creating temp files). | Git checkout/restore, deleting created temp files, restoring clean file snapshot. Fully automated. |
| **R1** | `COMPENSABLE` | Semantic inverse actions exist (e.g., inserting a database record with a known ID -> DELETE record; reserving a resource -> release lease; creating branch -> delete branch). | Execute registered inverse compensating action. Automated or supervised. |
| **R2** | `FORWARD_FIX_ONLY` | Actions where inverse is impossible or destructive, but a corrective forward mutation restores operational stability (e.g., running forward database migrations, applying patch commit). | Generate forward-fix plan; requires human or orchestrator approval. |
| **R3** | `IRREVERSIBLE` | Operations with permanent external or physical side-effects (e.g., sending emails/webhooks, third-party payment transactions, public package publishing). | Cannot be mechanically rolled back. Must trigger `QUARANTINE_MANUAL_HOLD` and emit incident telemetry. |

---

## 3. Side-Effect Journal Schema

During an agent task or multi-agent orchestration session, the runtime maintains an append-only JSONL Side-Effect Journal (`journal.jsonl`):

```json
{
  "journal_version": "1.0.0",
  "entry_id": "jnl_7f8e9d0a1b2c",
  "trace_id": "trc_9a8b7c6d5e4f",
  "span_id": "spn_12345678",
  "agent_id": "coder-subagent-01",
  "step_id": 4,
  "timestamp": "2026-03-31T12:05:00Z",
  "mutation_type": "FILE_MODIFICATION | FILE_CREATION | FILE_DELETION | PROCESS_SPAWN | DB_TRANSACTION | RESOURCE_ACQUISITION | EXTERNAL_CALL",
  "reversibility_tier": "PURE_REVERSIBLE | COMPENSABLE | FORWARD_FIX_ONLY | IRREVERSIBLE",
  "target_resource": "src/api/auth.py",
  "forward_action": {
    "tool_name": "write_file",
    "params_hash": "sha256:abc123...",
    "summary": "Updated token expiry validation logic"
  },
  "compensating_action": {
    "strategy": "RESTORE_SNAPSHOT | EXECUTE_TOOL | HUMAN_INTERVENTION",
    "tool_name": "write_file",
    "compensation_payload": {
      "filepath": "src/api/auth.py",
      "restore_from_ref": "snapshot:snap_init_auth_hash"
    }
  },
  "state_snapshot_ref": "snap_9876543210",
  "status": "APPLIED | COMPENSATED | FAILED_COMPENSATION | ABANDONED"
}
```

### Schema Requirements:
- `trace_id` & `agent_id`: Correlate mutations across parent orchestrators and subagents.
- `compensating_action`: Explicit definition of the inverse operation. If tier is `IRREVERSIBLE`, strategy must be `HUMAN_INTERVENTION`.
- `state_snapshot_ref`: Pointer to a pre-mutation hash, Git blob SHA, or diff snapshot stored in `.ai/state/snapshots/`.

---

## 4. Rollback Execution Strategies

When a task aborts, fails verification, or exceeds budget thresholds, the runtime selects a rollback execution strategy based on the highest reversibility tier present in the journal:

```text
Task Aborted / Circuit Breaker / Failure
                    │
   Evaluate Highest Tier in Journal
                    ├─ All R0 (PURE_REVERSIBLE) ────> AUTOMATED_SAGA_UNWIND
                    ├─ Contains R1 (COMPENSABLE) ───> SUPERVISED_ROLLBACK_CHECKPOINT
                    └─ Contains R2 / R3 ────────────> QUARANTINE_MANUAL_HOLD
```

### 4.1 AUTOMATED_SAGA_UNWIND
- **Applicability**: All uncommitted mutations are Tier R0 (`PURE_REVERSIBLE`) or pre-authorized deterministic R1 (`COMPENSABLE`).
- **Behavior**: Runtime iterates backwards through the journal in LIFO order, applying each `compensating_action`.
- **Completion Gate**: Git working tree status is verified clean (`git status --porcelain` empty) and temporary files are purged.

### 4.2 SUPERVISED_ROLLBACK_CHECKPOINT
- **Applicability**: Journal contains Tier R1 (`COMPENSABLE`) actions with semantic consequences, or partial multi-agent branch state.
- **Behavior**: Orchestrator presents an unwinding sequence to the human operator or primary evaluation agent before triggering execution.
- **Verification**: Each compensating step emits an audit verification event.

### 4.3 QUARANTINE_MANUAL_HOLD
- **Applicability**: Journal contains Tier R2 (`FORWARD_FIX_ONLY`), Tier R3 (`IRREVERSIBLE`), or a failed compensation attempt (`FAILED_COMPENSATION`).
- **Behavior**: Execution immediately freezes. Locks acquired under `.ai/contracts/concurrency-lock.contract.md` are marked `QUARANTINED` to prevent other agents from operating on the tainted resource. An escalation report is generated.

---

## 5. Compensation Failure & Deadlock Avoidance

### 5.1 Failure in Compensation
If a compensating action itself raises an error:
1. DO NOT retry blindly (respect Retry & Token Economy limits).
2. Mark entry status as `FAILED_COMPENSATION`.
3. Transition execution strategy immediately to `QUARANTINE_MANUAL_HOLD`.
4. Emit an alert with the tainted resource identifier, current actual state, and intended state.

### 5.2 Concurrency Lock Release on Rollback
- Resources locked via `.ai/contracts/concurrency-lock.contract.md` MUST NOT be released until either:
  1. All corresponding mutations on that resource are successfully compensated (`COMPENSATED`), OR
  2. The resource is quarantined under human supervision.

---

## 6. Rollback Telemetry & Audit Schema

Every rollback invocation emits a structured telemetry event conforming to `.ai/contracts/tool-audit.contract.md`:

```json
{
  "event_type": "transactional_rollback_event",
  "timestamp": "2026-03-31T12:10:00Z",
  "trace_id": "trc_9a8b7c6d5e4f",
  "agent_id": "orchestrator",
  "trigger": "CIRCUIT_BREAKER_ACTIVATED",
  "strategy": "AUTOMATED_SAGA_UNWIND",
  "total_entries": 4,
  "compensated_entries": 4,
  "failed_entries": 0,
  "duration_ms": 420,
  "verification_status": "VERIFIED_CLEAN",
  "post_rollback_evidence": "git status clean, 0 orphaned processes"
}
```

---

## 7. Ecosystem Alignment (CHAD & LapisLLM)

### CHAD Runtime Responsibility
- CHAD maintains the runtime Side-Effect Journal in the session context.
- CHAD captures pre-execution snapshots (file state, git index state, process handles) before dispatching modifying tools.
- CHAD automatically executes `AUTOMATED_SAGA_UNWIND` on task cancellation or catastrophic failure before reporting to the user interface.

### LapisLLM Model Responsibility
- LapisLLM receives the active rollback strategy and reversibility tiers in system context.
- When generating recovery plans, LapisLLM is constrained to produce strictly valid inverse or forward-fix compensation schemas matching this contract.
