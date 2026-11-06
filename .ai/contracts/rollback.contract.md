# Standard Transactional Rollback & State Compensation Contract

## Metadata
- **contract_id**: `rollback_and_state_compensation`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Define a provider-neutral, evidence-based governance contract for transactional rollback, side-effect recording, automated saga unwinding, and state compensation across autonomous AI agent executions.

---

## 1. Rollback & State Compensation Architecture

When an agent (`coder`, `orchestrator`, or specialist) executes state-mutating actions (file writes, directory mutations, database migrations, package installations, or external service calls), execution may fail abruptly due to `SAFETY_TRIGGERED`, test failures, syntax errors, or environmental conflicts.

To guarantee that the workspace and external dependencies are never left in a corrupted or half-modified intermediate state, the runtime coordinates rollback via an append-only **Side-Effect Journal**:

```text
Agent (Coder / Orchestrator)
  │
  ├── [Dispatches Mutating Tool Call]
  │     ├── 1. Register Pending Side-Effect & Compensation Spec
  │     ├── 2. Capture Pre-State Snapshot / Inverse Command
  │     └── 3. Execute Mutation
  │
  ▼
CHAD Runtime Side-Effect Journal Manager (`journal.jsonl`)
  ├─ Appends Committed Mutation Record
  ├─ Monitors Task Termination (Normal vs Abnormal Stop Condition)
  └─ Evaluates Unwinding Policy on Failure
        │
        ▼ (On Failure / Abort)
  Saga Unwinding Arbiter (LIFO Rollback Engine)
        ├─ Executes Inverse Operations in Reverse Order
        └─ Verifies Workspace Post-State via Evidence Probes
```

---

## 2. Reversibility Tiers Taxonomy

Every side-effecting action dispatched by an agent must be categorized into one of four standard reversibility tiers:

| Reversibility Tier | Description | Recovery Mechanism | Execution Boundary |
|---|---|---|---|
| `PURE_REVERSIBLE` | Action can be completely undone to the exact prior byte/content state with zero side effects. | Direct restoration from snapshot or patch inverse (`restore_file`, git checkout). | Automated LIFO saga unwinding without human intervention. |
| `COMPENSABLE` | Action cannot be simply "undone" byte-for-byte, but an inverse semantic operation restores equivalent system state. | Compensating transaction (e.g. running down-migration, uninstalling added package, revoking created API token). | Automated compensation permitted if pre-verified in dry-run; otherwise prompts supervised checkpoint. |
| `FORWARD_FIX_ONLY` | Action cannot be safely rolled back or compensated without risk of data loss; resolution requires forward patch. | Forward repair workflow: freeze system, isolate diff, generate corrective patch. | Orchestrator halts execution, records `GOAL_BLOCKED`, alerts user. |
| `IRREVERSIBLE` | Action permanently mutates unrecoverable state (e.g. dropping production table, purging remote repository history, permanent external API billing charge). | Disaster recovery protocol; manual human recovery required. | Requires explicit human checkpoint (`HUMAN_CHECKPOINT_REQUIRED`) prior to initial execution. |

---

## 3. Side-Effect Journal Schema

All state-modifying tool executions must record an entry in the append-only journal (`.ai/state/journal.jsonl` or runtime equivalent) prior to committing state changes.

```json
{
  "journal_id": "jrn-20250330-0042",
  "trace_id": "tr-20250330-exec-101",
  "step_index": 3,
  "agent_id": "coder-unit-1",
  "tool_name": "write_file",
  "target_resource": "src/auth/jwt.service.ts",
  "reversibility_tier": "PURE_REVERSIBLE",
  "pre_state": {
    "existed": true,
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "backup_artifact_path": ".ai/state/snapshots/src/auth/jwt.service.ts.bak"
  },
  "mutation_spec": {
    "action": "OVERWRITE",
    "bytes_written": 1420
  },
  "compensation_spec": {
    "strategy": "RESTORE_SNAPSHOT",
    "inverse_tool": "restore_file",
    "inverse_params": {
      "filepath": "src/auth/jwt.service.ts",
      "source_snapshot": ".ai/state/snapshots/src/auth/jwt.service.ts.bak"
    },
    "verification_probe": {
      "type": "SHA256_HASH_MATCH",
      "expected_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  },
  "status": "COMMITTED | COMPENSATED | COMPENSATION_FAILED",
  "timestamp": "2025-03-30T14:32:00Z"
}
```

---

## 4. Saga Unwinding Strategies

When an execution batch fails, aborts, or is terminated by `SAFETY_TRIGGERED` or unhandled exceptions, the runtime selects one of three unwinding strategies based on the highest-risk reversibility tier in the journal:

1. `AUTOMATED_SAGA_UNWIND`
   - **Condition**: All journaled actions in the batch are `PURE_REVERSIBLE` or pre-approved `COMPENSABLE`.
   - **Procedure**: The runtime processes the batch journal entries in strict **Last-In, First-Out (LIFO)** order. Each inverse tool is executed sequentially.
   - **Validation**: Post-compensation verification probes are run after each step.
2. `SUPERVISED_ROLLBACK_CHECKPOINT`
   - **Condition**: One or more entries are `COMPENSABLE` with external side effects or `FORWARD_FIX_ONLY`.
   - **Procedure**: Execution halts; the journal manager presents a structured rollback plan detailing each proposed inverse operation and risk assessment to the human supervisor.
   - **Validation**: Requires explicit human approval before executing compensation commands.
3. `QUARANTINE_MANUAL_HOLD`
   - **Condition**: Any compensation step fails (`COMPENSATION_FAILED`) or unexpected divergence is detected.
   - **Procedure**: The workspace is locked; all further mutating operations are blocked. A diagnostic report is generated from the journal to isolate partial mutations.

---

## 5. Post-Compensation Verification Gates

A rollback is not considered complete merely because inverse commands were dispatched. The runtime must verify the restored state against objective evidence:

1. **Hash Verification**: For `PURE_REVERSIBLE` files, the SHA-256 of the restored file must match `pre_state.sha256`.
2. **Git Working Tree Cleanliness**: `git status --porcelain` on affected paths must confirm removal of newly created untracked artifacts and clean revert of modified paths.
3. **Environment Sanity Probe**: The test suite or syntax checker that was operational prior to the batch must execute to confirm the workspace compiles cleanly.
4. **Evidence Labeling**: The compensation report must output verified evidence using the ecosystem labels (`VERIFIED`, `FACT`, `CONFLICT`).

---

## 6. Compensation Telemetry & Incident Schema

Failed rollbacks or critical unwinds emit structured event telemetry to `.ai/state/rollback-events.jsonl`:

```json
{
  "event_type": "SAGA_UNWIND_COMPLETED | SAGA_UNWIND_FAILED",
  "trace_id": "tr-20250330-exec-101",
  "batch_id": "batch-884",
  "total_mutations": 4,
  "compensated_mutations": 4,
  "failed_mutations": 0,
  "unwind_strategy": "AUTOMATED_SAGA_UNWIND",
  "verification_status": "ALL_PROBES_PASSED",
  "duration_ms": 340,
  "timestamp": "2025-03-30T14:32:05Z"
}
```

---

## 7. Ecosystem Compatibility (CHAD & LapisLLM)

### CHAD Runtime Layer
- CHAD implements the Side-Effect Journal Manager, intercepting file system mutation tools (`write_file`, `replace_with_git_merge_diff`, shell executions) to capture pre-state snapshots in `.ai/state/snapshots/`.
- CHAD executes the LIFO saga unwinder automatically upon agent crash, stop-condition abort, or explicit rollback request.

### LapisLLM Model Layer
- LapisLLM generates explicit compensation specifications (`compensation_spec`) when planning complex multi-step refactorings or database operations.
- LapisLLM identifies `FORWARD_FIX_ONLY` and `IRREVERSIBLE` actions during decomposition and marks them for human checkpoints before dispatching.
