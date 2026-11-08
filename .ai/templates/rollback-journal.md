# Rollback & Compensation Journal Template

This template records mutating side-effects, reversibility classifications, compensating operations, and verification evidence during agent task execution.

---

## 1. Task Execution & Transaction Context

- **Task ID**: `[e.g., task-892]`
- **Trace ID**: `[e.g., tr-20250330-agent-01]`
- **Orchestrator ID**: `[e.g., orchestrator-main]`
- **Active Agent**: `[e.g., coder-alpha]`
- **Transaction Strategy**: `[AUTOMATED_SAGA_UNWIND | SUPERVISED_ROLLBACK_CHECKPOINT | QUARANTINE_MANUAL_HOLD]`
- **Transaction Status**: `[ACTIVE | COMMITTED | ROLLING_BACK | ROLLED_BACK | QUARANTINE_HOLD]`

---

## 2. Mutating Operations Log (`journal.jsonl` entries)

| Step | Tool / Command | Target Resource | Reversibility Tier | Compensating Action | Verification Probe | Status |
|---|---|---|---|---|---|---|
| 1 | `write_file` | `src/auth.ts` | `PURE_REVERSIBLE` | `restore_file` (from snapshot) | `FILE_CHECKSUM` | `COMMITTED` |
| 2 | `run_in_bash_session` | `PORT 3000` | `COMPENSABLE` | `kill $(lsof -t -i :3000)` | `PORT_CHECK` | `COMMITTED` |
| 3 | `run_in_bash_session` | `npm install pkg-x` | `COMPENSABLE` | `npm uninstall pkg-x && git checkout package*.json` | `COMMAND_EXIT_CODE` | `COMMITTED` |
| 4 | `run_in_bash_session` | `db/migrate.py` | `FORWARD_FIX_ONLY` | `python3 db/rollback.py` | `COMMAND_EXIT_CODE` | `FAILED` |

---

## 3. Rollback & Compensation Execution (if triggered)

- **Trigger Cause**: `[TEST_REGRESSION | SAFETY_TRIGGERED | GOAL_BLOCKED | HUMAN_ABORT]`
- **Trigger Details**: `[Description of failure or error event]`
- **Unwind Direction**: LIFO (Last-In, First-Out: Step 4 → 3 → 2 → 1)

### Rollback Step Log
- [ ] **Step 4**: `db/migrate.py`
  - Action taken: `python3 db/rollback.py`
  - Probe result: `FAILED` (Schema altered, requires manual intervention)
  - Result: Escalated to `SUPERVISED_ROLLBACK_CHECKPOINT`
- [ ] **Step 3**: `npm install pkg-x`
  - Action taken: `npm uninstall pkg-x && git checkout package*.json`
  - Probe result: `PASS`
- [ ] **Step 2**: Background test server `:3000`
  - Action taken: `kill $(lsof -t -i :3000)`
  - Probe result: `PASS` (Port released)
- [ ] **Step 1**: `src/auth.ts`
  - Action taken: `restore_file`
  - Probe result: `PASS` (Checksum verified)

---

## 4. Verification Gates Post-Rollback

- [ ] **Git Working Tree Cleanliness**: `git status --porcelain` is empty / matches pre-task state.
- [ ] **Process Cleanup Verification**: No lingering orphaned PIDs or open listening ports.
- [ ] **Build Artifact Cleanup**: Designated temporary build files / directories removed.

---

## 5. Escalation & Incident Summary (for incomplete rollbacks)

- **Uncompensated Resources**: `[List any resources that could not be restored automatically]`
- **Observed Workspace State**: `[Current git status, diff, or error message]`
- **Recommended Human Intervention**: `[Exact commands for operator to restore baseline]`
