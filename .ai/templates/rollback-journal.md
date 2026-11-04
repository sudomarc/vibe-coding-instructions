# Rollback Journal & State Compensation Templates

## 1. Append-Only Side-Effect Journal Entry Template (`journal.jsonl`)

Use this JSON schema template when recording mutating actions in the runtime side-effect journal:

```json
{
  "journal_id": "jrn-YYYYMMDD-UUID",
  "trace_id": "tr-agent-trace-id",
  "step_index": 1,
  "agent_id": "coder-agent-1",
  "tool_id": "write_file",
  "permission_tier": "WORKSPACE_WRITE",
  "reversibility_tier": "PURE_REVERSIBLE",
  "target_resource": "path/to/target/file",
  "pre_mutation_state": {
    "type": "FILE_SNAPSHOT",
    "content_hash": "sha256:...",
    "existed_prior": true,
    "snapshot_ref": ".ai/state/snapshots/file.bak"
  },
  "compensating_action": {
    "tool_id": "restore_file",
    "parameters": {
      "filepath": "path/to/target/file",
      "target_hash": "sha256:..."
    },
    "idempotent": true
  },
  "status": "APPLIED",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

---

## 2. Post-Rollback State Verification Report Template

Use this Markdown template when completing a rollback or Saga unwinding phase:

```markdown
# Agent Rollback & Compensation Report

## Task Context
- **task_id**: [Task Identifier]
- **trace_id**: [Trace Identifier]
- **triggering_event**: [SAFETY_TRIGGERED | GOAL_BLOCKED | CONCURRENCY_CONTENTION_BLOCKED | USER_ABORT]
- **triggering_reason**: [Detailed explanation of why task halted]
- **orchestrator_id**: [Orchestrator Identifier]
- **executing_agent_id**: [Agent Identifier]

## Journal Summary
- **total_journaled_steps**: [Count]
- **steps_unwound**: [Count]
- **unwind_strategy**: [AUTOMATED_SAGA_UNWIND | SUPERVISED_ROLLBACK_CHECKPOINT | QUARANTINE_MANUAL_HOLD]
- **overall_reversibility**: [PURE_REVERSIBLE | COMPENSABLE | FORWARD_FIX_ONLY | IRREVERSIBLE]

## Compensating Actions Executed (LIFO)
1. **Step [Index]**: `[tool_id]` on `[target_resource]`
   - **Compensating Action**: `[compensating tool / command]`
   - **Result**: [SUCCESS | FAILED]
   - **Verification**: [Hash verified / File removed / Process killed / Lock freed]
2. **Step [Index]**: `[tool_id]` on `[target_resource]`
   - **Compensating Action**: `[compensating tool / command]`
   - **Result**: [SUCCESS | FAILED]
   - **Verification**: [Verification outcome]

## Verification Gates
- [ ] Workspace clean check (`git status --porcelain` is clean): [PASS / FAIL]
- [ ] Scratch files purged: [PASS / FAIL]
- [ ] Background processes terminated (PIDs cleared): [PASS / FAIL]
- [ ] Concurrency locks released in lock manager: [PASS / FAIL]

## Residual State & Risks
- **uncompensated_side_effects**: [None / List residual effects]
- **forward_fix_required**: [YES / NO]
- **recommendations**: [Actionable next steps for operator or agent retry]
```
