# Agentic Transaction & Rollback Journal Template

Use this template to record mutating state operations, compensation handlers, and rollback verification evidence during multi-step or multi-agent workflows.

---

## Task Metadata

- **Session / Task ID**: `task-YYYYMMDD-XXXX`
- **Trace ID**: `tr-YYYYMMDD-XXXX`
- **Orchestrator ID**: `orchestrator-main`
- **Rollback Strategy**: `AUTOMATED_SAGA_UNWIND | SUPERVISED_ROLLBACK_CHECKPOINT | QUARANTINE_MANUAL_HOLD`
- **Final Status**: `COMMITTED | FULLY_COMPENSATED | PARTIALLY_COMPENSATED | QUARANTINED`

---

## Side-Effect Journal (`journal.jsonl`)

Each mutating tool execution appends an entry to this journal before or immediately upon execution:

```jsonl
{"transaction_id": "tx-001", "step_index": 1, "agent_id": "coder-1", "action_name": "write_file", "reversibility_tier": "PURE_REVERSIBLE", "target_resource": "src/config.ts", "pre_state_hash": "sha256:abc123...", "post_state_hash": "sha256:def456...", "compensation_action": {"tool_name": "restore_file", "parameters": {"filepath": "src/config.ts", "target_hash": "sha256:abc123..."}}, "status": "COMMITTED", "timestamp": "2025-03-30T10:00:00Z"}
{"transaction_id": "tx-002", "step_index": 2, "agent_id": "coder-1", "action_name": "run_in_bash", "reversibility_tier": "COMPENSABLE", "target_resource": "db:schema_migrations", "pre_state_hash": "v1.2", "post_state_hash": "v1.3", "compensation_action": {"tool_name": "run_in_bash", "parameters": {"command": "python manage.py migrate app 0001"}}, "status": "COMMITTED", "timestamp": "2025-03-30T10:01:00Z"}
```

---

## Rollback Execution Summary (When Triggered)

Fill out this section if a failure or cancellation triggered saga unwinding:

### 1. Trigger Context
- **Failure Trigger**: `TEST_FAILURE | GOAL_BLOCKED | SAFETY_TRIGGERED | USER_CANCELLED`
- **Failed Step**: Step 3 (Integration test execution)
- **Error Diagnostic**: `ConnectionRefusedError: database failed integrity check`

### 2. Compensation Execution Log (LIFO Order)

| Step # | Action Compensated | Compensation Tool | Verification Method | Outcome Status |
|---|---|---|---|---|
| tx-002 | Apply migration 0002 | `python manage.py migrate app 0001` | Query schema version table | `VERIFIED` |
| tx-001 | Modified `src/config.ts` | `restore_file` | SHA-256 match `sha256:abc123...` | `VERIFIED` |

### 3. Residual Side-Effects & Invariant Checks
- **Git Worktree Status**: Clean (`git status --porcelain` is empty).
- **Process Status**: No lingering background PID or port bindings.
- **Uncompensated Debris**: None.
- **Remaining Uncertainty**: None.

---

## Supervisor Sign-off (For Supervised or Quarantined States)

- **Reviewer**: `@human-supervisor`
- **Approval Timestamp**: `YYYY-MM-DDTHH:MM:SSZ`
- **Notes**: All files and database states verified restored to initial baseline.
