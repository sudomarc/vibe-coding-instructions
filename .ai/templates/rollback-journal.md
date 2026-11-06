# Transactional Rollback Manifest & Verification Report

## Metadata
- **trace_id**: `[Trace ID correlating to orchestrator task]`
- **batch_id**: `[Execution batch identifier]`
- **agent_id**: `[Agent ID executing rollback]`
- **trigger_reason**: `[TEST_FAILURE | SAFETY_TRIGGERED | GOAL_BLOCKED | EXCEPTION]`
- **timestamp**: `[ISO-8601 UTC Timestamp]`

---

## 1. Batch Execution Summary

| Total Mutations | Compensated | Failed Compensation | Unwind Strategy | Final Status |
|---|---|---|---|---|
| `[Count]` | `[Count]` | `[Count]` | `AUTOMATED_SAGA_UNWIND | SUPERVISED_ROLLBACK_CHECKPOINT | QUARANTINE_MANUAL_HOLD` | `CLEAN_REVERTED | DIVERGENCE_DETECTED | QUARANTINED` |

---

## 2. Unwind Execution Journal (LIFO Order)

List the reversed mutations in the exact reverse order of original execution:

| Step | Resource | Original Action | Reversibility Tier | Compensation Action Executed | Verification Result |
|---|---|---|---|---|---|
| 1 (Last) | `[File / Table / Key]` | `[OVERWRITE | CREATE | DELETE | RUN_MIGRATION]` | `PURE_REVERSIBLE | COMPENSABLE` | `[restore_file | delete_file | migrate:down]` | `PASS (Hash match) | FAIL` |
| 2 | `[File / Table / Key]` | `[...]` | `[...]` | `[...]` | `[...]` |

---

## 3. Post-Rollback Verification Evidence

Provide concrete evidence verifying workspace integrity:

```markdown
- [VERIFIED] Pre-batch SHA-256 restored for all modified files.
- [VERIFIED] Git working directory status clean: `git status --porcelain` returns no uncommitted artifacts.
- [VERIFIED] Baseline test/compilation probe executed: clean compile.
```

---

## 4. Residual Risks & Next Actions

- **Quarantine State**: `[NONE | ISOLATED_CONFLICT]`
- **Forward Patch Required**: `[YES | NO]`
- **Next Action**: `[Re-serialize task with updated hypothesis | Escalate to human supervisor | Retry with alternative approach]`
