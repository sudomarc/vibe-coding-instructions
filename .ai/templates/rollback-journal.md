# Rollback & Transaction Journal Template

Use this template to document transaction sequences, reversibility classifications, compensation actions, and post-unwind verification audits when an agent execution fails or requires manual quarantine inspection.

---

## 1. Execution Context

- **trace_id**: `tr-YYYYMMDD-agent-000`
- **orchestrator_id**: `orchestrator-main`
- **agent_id**: `coder-alpha`
- **termination_stop_condition**: `MAX_BUDGET_REACHED | GOAL_BLOCKED | SAFETY_TRIGGERED | UNHANDLED_EXCEPTION`
- **rollback_trigger_timestamp**: `YYYY-MM-DDTHH:MM:SSZ`
- **rollback_coordinator**: `automated | human_supervised`

---

## 2. Transaction Log Summary (`journal.jsonl`)

| Step # | Resource Path / Target | Action Type | Reversibility Tier | Compensation Handler | Forward State Hash | Unwind Status |
|---|---|---|---|---|---|---|
| 1 | `src/config/env.ts` | Edit | `PURE_REVERSIBLE` | Restore file snapshot | `sha256:...` | `COMPENSATED` |
| 2 | `prisma/schema.prisma` | Edit | `PURE_REVERSIBLE` | Restore file snapshot | `sha256:...` | `COMPENSATED` |
| 3 | `dev_database_pg` | DB Migration | `COMPENSABLE` | `prisma migrate resolve --rolled-back` | `migration_v4` | `COMPENSATED` |
| 4 | `src/auth/oauth.ts` | Edit | `PURE_REVERSIBLE` | Restore file snapshot | `sha256:...` | `COMPENSATION_FAILED` |

---

## 3. Saga Compensation Unwind Sequence

### Step 4: `src/auth/oauth.ts` (Failed Step)
- **Forward Action**: `replace_with_git_merge_diff`
- **Compensation Action**: Restore from snapshot `snapshots/src/auth/oauth.ts.bak`
- **Result**: `COMPENSATION_FAILED`
- **Diagnostic Error**: Target file locked by background process PID 4190.
- **Action Taken**: Rollback coordinator halted automated unwinding; initiated `QUARANTINE_MANUAL_HOLD`.

### Step 3: `dev_database_pg`
- **Forward Action**: Migration run `20250401_add_auth_tokens`
- **Compensation Action**: Downgrade migration script
- **Result**: `COMPENSATED` (Verified database schema reverted to `20250328_baseline`).

### Step 2 & 1: `src/config/env.ts`, `prisma/schema.prisma`
- **Forward Action**: File edits
- **Compensation Action**: Restore from snapshots
- **Result**: `COMPENSATED` (Verified matching git index hash).

---

## 4. Post-Rollback State Audit & Verification

```json
{
  "rollback_status": "QUARANTINE_MANUAL_HOLD",
  "total_transactions": 4,
  "compensated_transactions": 3,
  "failed_transactions": 1,
  "evidence": [
    {
      "label": "VERIFIED",
      "statement": "Step 1, 2, and 3 successfully compensated to baseline state.",
      "source": "rollback_coordinator:hash_audit",
      "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "label": "CONFLICT",
      "statement": "Step 4 divergent from pre-state hash; PID 4190 held file lock.",
      "source": "rollback_coordinator:quarantine_check",
      "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ]
}
```

---

## 5. Human Intervention & Remediation Steps

- [ ] Inspect and kill lingering process PID 4190 (`kill -9 4190`).
- [ ] Run `git checkout HEAD src/auth/oauth.ts` to restore clean working tree.
- [ ] Validate workspace cleanliness via `git status --porcelain`.
- [ ] Release quarantine hold in runtime lock registry.
