# Standard Transactional Rollback & State Compensation Contract

## Metadata
- **contract_id**: `rollback_compensation_governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Define a provider-neutral, evidence-based governance contract for tracking side effects, classifying reversibility, executing saga-style compensations, and deterministically restoring pristine state when AI agent task execution fails, is interrupted, or triggers a safety stop condition.

---

## 1. Architecture & Execution Lifecycle

When an AI agent (such as `coder` or `orchestrator`) executes state-changing actions across the workspace, environment, or external dependencies, side effects must be registered in an append-only transaction journal prior to or concurrently with execution.

```text
       Agent Execution Loop (Coder / Orchestrator)
                          │
         [Pre-action: Snapshot / Inverse Handler]
                          ▼
            CHAD Transaction Journal (journal.jsonl)
                          │
                 [Tool Execution RPC]
                          ▼
             Workspace / Environment Mutation
                          │
          ┌───────────────┴───────────────┐
          │                               │
       Success                         Failure
          │                    (Budget / Safety / Error)
          ▼                               ▼
    Commit Step /                Rollback Coordinator
 Release Temp Checkpoint                  │
                               ┌──────────┴──────────┐
                               ▼                     ▼
                       Automated Saga         Quarantine Hold
                       LIFO Unwind           (Manual Supervised)
```

---

## 2. Reversibility Taxonomy

Every mutative tool execution and side effect is classified into one of four reversibility tiers:

| Reversibility Tier | Definition | Compensation Mechanism | Fallback Policy |
|---|---|---|---|
| `PURE_REVERSIBLE` | Direct, lossless inverse operation exists (e.g. file edit with reverse patch, newly created untracked file deletion). | Automated inverse tool call (e.g. `restore_file`, delete created file). | Revert to base snapshot hash. |
| `COMPENSABLE` | State cannot be directly undone, but an equivalent counter-action restores equilibrium (e.g. rollback DB migration, cancel reserved port, kill child process). | Execute defined compensation handler script/command. | Escalate to human checkpoint if compensation fails. |
| `FORWARD_FIX_ONLY` | Action cannot be unwound automatically without risk of corruption (e.g. external distributed API call with side effects, published package). | Generate remedial forward patch or notify external system webhook. | Quarantine execution; prompt human operator. |
| `IRREVERSIBLE` | Destructive action with permanent state destruction (e.g. drop database without backup, git push --force on remote main). | Strictly forbidden without prior checkpoint authorization (`PRIVILEGED_MUTATION`). | Abort immediately if unapproved; record safety violation. |

---

## 3. Transaction Journal Schema (`journal.jsonl`)

The host runtime (CHAD) maintains an append-only transaction log per agent execution session (`trace_id`). Every state-mutating operation records a transaction step:

```json
{
  "transaction_id": "tx-20250401-0001",
  "step_index": 3,
  "trace_id": "tr-20250401-eng-042",
  "agent_id": "coder-alpha",
  "tool_name": "replace_with_git_merge_diff",
  "target_resource": "src/auth/session.ts",
  "reversibility_tier": "PURE_REVERSIBLE",
  "forward_action": {
    "command": "replace_with_git_merge_diff",
    "params_hash": "sha256:4a8b...",
    "pre_state_hash": "sha256:d89e...",
    "post_state_hash": "sha256:7c11..."
  },
  "compensation_action": {
    "handler": "restore_file_snapshot",
    "params": {
      "filepath": "src/auth/session.ts",
      "restore_snapshot_ref": "snapshots/src/auth/session.ts.bak"
    },
    "idempotent": true,
    "timeout_sec": 15
  },
  "status": "APPLIED | COMMITTED | COMPENSATING | COMPENSATED | COMPENSATION_FAILED",
  "timestamp": "2025-04-01T10:15:30Z"
}
```

---

## 4. Saga Compensation Unwinding Protocol

When execution terminates under `MAX_BUDGET_REACHED`, `GOAL_BLOCKED`, `SAFETY_TRIGGERED`, or an unhandled tool exception:

1. **LIFO Compensation Ordering**:
   - Compensations are executed in reverse chronological order (Last-In-First-Out) of applied transactions.
2. **Idempotence Invariant**:
   - Every compensation handler must be idempotent. Re-executing a compensation step in case of transient timeout must not produce compounding errors.
3. **Execution Unwind Strategies**:
   - `AUTOMATED_SAGA_UNWIND`: Default for all `PURE_REVERSIBLE` actions. Evaluated without human intervention.
   - `SUPERVISED_ROLLBACK_CHECKPOINT`: Triggered when encountering `COMPENSABLE` actions requiring external side-effect adjustments.
   - `QUARANTINE_MANUAL_HOLD`: Triggered if any compensation handler returns a non-zero exit code or fails hash verification.

---

## 5. Rollback Failure Escalation & Quarantining

If a compensation step fails:
1. **Stop Further Compensations**:
   - Do not continue automated unwinding on dependent steps to avoid corrupting state.
2. **State Freezing (Quarantine)**:
   - Mark the transaction state as `COMPENSATION_FAILED`.
   - Prevent the workspace from executing further automated tasks or merging into base branches.
3. **Escalation Report Generation**:
   - Emit an escalation incident report using `.ai/templates/escalation-report.md` specifying:
     - The exact failed compensation step and error log.
     - Divergent resource hashes (`pre_state_hash` vs. `actual_state_hash`).
     - Manual remediation instructions for the human operator.

---

## 6. Compensation Verification Gates

A rollback is not considered complete until verified with real evidence:
1. **Pristine Hash Check**:
   - Files modified during the transaction session must match their pre-execution SHA-256 hashes or Git clean status (`git status --porcelain` returns empty).
2. **Environment Resource Sweep**:
   - Spawned preview servers or background worker PIDs recorded in the journal must be confirmed terminated.
   - Temporary test databases or schemas created for the batch must be confirmed dropped.
3. **Evidence Assertion**:
   - The rollback coordinator emits a verification block with label `VERIFIED`:
     ```json
     {
       "evidence": [
         {
           "label": "VERIFIED",
           "statement": "All 4 mutated files restored to base commit hashes; no orphaned processes on port 3000.",
           "source": "rollback_coordinator:hash_audit",
           "timestamp": "2025-04-01T10:16:00Z"
         }
       ]
     }
     ```

---

## 7. CHAD & LapisLLM Runtime Layer Responsibilities

### CHAD Runtime Layer
- Maintains the append-only `journal.jsonl` during agent execution.
- Intercepts mutating tool execution and captures pre-mutation snapshots or diff inverses before executing mutations.
- Enforces LIFO compensation when stop conditions `SAFETY_TRIGGERED` or unrecoverable exceptions occur.
- Manages the quarantine hold state when automated compensation fails.

### LapisLLM Model Layer
- When planning multi-step changes, classifies proposed actions according to the reversibility taxonomy.
- Prefers `PURE_REVERSIBLE` and `COMPENSABLE` action sequences over irreversible side effects.
- In recovery and failure analysis, reads the transaction journal to construct minimal corrective batches rather than re-running the entire task from scratch.
