# Reversibility & State Compensation Reference

## Metadata
- **reference_id**: `reversibility_and_compensation`
- **version**: `1.0.0`
- **contract**: `.ai/contracts/rollback.contract.md`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Provide operational guidelines for agent orchestrators, delegates, and subagents on designing reversible workflows, maintaining side-effect journals, unwinding multi-step operations using the Saga pattern, and verifying compensation integrity when recovering from execution failures.

---

## 1. Principles of Agentic Reversibility

Every state modification carries risk. Agents must operate under the **Reversibility-First Invariant**:

1. **Pre-Flight Snapshot**:
   - Before executing any mutating operation (`write_file`, `replace_with_git_merge_diff`, shell state change, database migration), capture the target pre-state hash and backup snapshot.
2. **Explicit Compensation Definition**:
   - Do not perform an action without registering its exact compensation action in the side-effect journal (`journal.jsonl`).
3. **Prefer Non-Destructive Mutation**:
   - Prefer renaming or staging files over hard deletions.
   - Prefer ephemeral test databases or isolated schemas over altering shared development databases.
4. **Quarantine on Partial Unwind Failure**:
   - If a rollback compensation action fails, halt immediately. Do not attempt blind retry without human supervisor review.

---

## 2. Reversibility Tier Decision Tree

When planning an action, classify it into the appropriate reversibility tier:

```text
Does an exact, automated inverse operation exist?
  ├─ YES: Can it restore the pre-state bit-for-bit without data loss?
  │         ├─ YES ──> PURE_REVERSIBLE (e.g. restore_file, git revert, delete new file)
  │         └─ NO  ──> COMPENSABLE (e.g. drop temporary table, kill launched background PID)
  │
  └─ NO: Can a forward patch mitigate the operational impact?
            ├─ YES ──> FORWARD_FIX_ONLY (e.g. send cancellation webhook, issue refund/credit)
            └─ NO  ──> IRREVERSIBLE (e.g. DROP DATABASE, hard delete production volume)
```

---

## 3. The Saga Unwinding Protocol

A **Saga** is a sequence of subtasks where each step modifies state and provides a corresponding compensating step.

### Forward Execution Phase
1. Subagent A modifies `src/config.py` (Transaction 1, `PURE_REVERSIBLE`).
2. Subagent A creates migration `migrations/0002_add_field.py` (Transaction 2, `PURE_REVERSIBLE`).
3. Subagent A runs migration against dev database (Transaction 3, `COMPENSABLE`, compensation: execute downgrade).
4. Subagent A runs integration tests -> **TESTS FAIL / STOP CONDITION: GOAL_BLOCKED**.

### Backward Compensation Phase (LIFO Order)
```text
Failure Detected at Step 4
  │
  ├── 1. Read journal.jsonl (reverse order)
  │
  ├── 2. Step 3 Compensation: Run downgrade migration
  │       └── Verification: Verify schema matches pre-migration hash -> PASS
  │
  ├── 3. Step 2 Compensation: Remove migrations/0002_add_field.py
  │       └── Verification: Verify file does not exist -> PASS
  │
  ├── 4. Step 1 Compensation: Restore src/config.py
  │       └── Verification: Verify file hash matches pre_state_hash -> PASS
  │
  ▼
State Restored: Emit ROLLBACK_SUCCESS to Orchestrator
```

---

## 4. Git Worktree & Snapshot Checkpoints

For complex multi-file engineering tasks:

1. **Ephemeral Branch Checkpointing**:
   - Create a checkpoint branch `agent/checkpoint-<trace_id>` before starting substantial implementation batches.
2. **Atomic Reset on Rollback**:
   - If the task is aborted before human checkpoint approval:
     ```bash
     git reset --hard checkpoint-<trace_id>
     git clean -fd
     ```
3. **Validation of Invariants**:
   - Check `git status --porcelain` to guarantee zero untracked debris or dirty worktree states remain after rollback.

---

## 5. Compensation Recipes by Domain

| Domain | Mutating Action | Compensation Action | Verification Method |
|---|---|---|---|
| **Filesystem** | `write_file` (new file) | `delete_file` | Check file non-existence |
| **Filesystem** | `replace_with_git_merge_diff` | `write_file` (pre-state content) | Match SHA-256 with `pre_state_hash` |
| **Processes** | `run_in_bash` (background server `npm start &`) | `kill $(lsof -t -i :<port>)` | Verify port free via `lsof -i :<port>` |
| **Package Dependencies** | `npm install <pkg>` | `npm uninstall <pkg>` && restore lockfile | Verify `package.json` and lockfile hash |
| **Database** | Apply DB migration | Run reverse/down migration | Query database schema version table |
| **External API** | Create cloud test resource | Issue DELETE request on created resource ID | Query resource endpoint expecting 404 |

---

## 6. Escalation on Rollback Failure

If any compensation step fails during LIFO unwinding:

1. **Immediate State Freeze**: Halt all active subagents and lock all acquired resources.
2. **Mark Transaction Status**: Update journal entry to `COMPENSATION_FAILED`.
3. **Generate Rollback Failure Report**:
   - Record exact failed step, expected state, observed error, and partially reverted components.
4. **Escalate to Human Supervisor**:
   - Transition agent stop condition to `HUMAN_CHECKPOINT_REQUIRED`.
   - Never attempt repeated unconstrained retries on failing compensation actions.
