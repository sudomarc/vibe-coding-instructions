# Side-Effect Journal & Rollback Record Template

Use this template to record mutations, state snapshots, and rollback or state compensation history conforming to `.ai/contracts/rollback.contract.md`.

---

## Task Metadata

- **Session / Task ID:** `<session-or-task-id>`
- **Trace ID:** `<trace-id>`
- **Primary Agent / Orchestrator:** `<orchestrator-id>`
- **Current Execution Status:** `ACTIVE | ABORTED | ROLLING_BACK | ROLLBACK_VERIFIED | QUARANTINED`
- **Highest Reversibility Tier:** `PURE_REVERSIBLE | COMPENSABLE | FORWARD_FIX_ONLY | IRREVERSIBLE`

---

## Side-Effect Journal Entries

| Step | Agent ID | Target Resource | Mutation Type | Reversibility Tier | Forward Tool & Summary | Snapshot Ref | Status |
|---|---|---|---|---|---|---|---|
| 1 | `coder-01` | `src/config.py` | `FILE_MODIFICATION` | `PURE_REVERSIBLE` | `replace_with_git_merge_diff` | `snap_001` | `APPLIED` |
| 2 | `coder-01` | `db/schema.sql` | `DB_TRANSACTION` | `COMPENSABLE` | `run_in_bash_session` (add table) | `snap_002` | `APPLIED` |
| 3 | `researcher-01` | `tmp/cache.json` | `FILE_CREATION` | `PURE_REVERSIBLE` | `write_file` (scrape cache) | `snap_003` | `APPLIED` |

---

## Rollback Execution Plan (If Triggered)

- **Rollback Trigger:** `MAX_BUDGET_REACHED | CIRCUIT_BREAKER | GOAL_BLOCKED | SAFETY_TRIGGERED | HUMAN_ABORT`
- **Execution Strategy:** `AUTOMATED_SAGA_UNWIND | SUPERVISED_ROLLBACK_CHECKPOINT | QUARANTINE_MANUAL_HOLD`

### Unwinding Sequence (LIFO)

1. **Step 3 Undo:** Delete `tmp/cache.json` via file deletion.
2. **Step 2 Undo:** Drop created table via database compensation command.
3. **Step 1 Undo:** Restore `src/config.py` using `snap_001`.

---

## Verification Evidence Post-Rollback

- **Repository Cleanliness Check:**
  - `git status --porcelain`: `[ ] Verified Clean`
  - Ephemeral files deleted: `[ ] Verified Purged`
  - Background processes killed: `[ ] Verified Inactive`
- **Quarantined Resources (if any):** `<list or None>`
- **Remaining Anomalies / Human Action Needed:** `<explicit statement or None>`
