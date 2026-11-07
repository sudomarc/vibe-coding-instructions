# Reversibility Classification & State Compensation Patterns

This reference provides operational guidelines and concrete patterns for managing state reversibility, transaction journaling, and saga-style compensation workflows in autonomous agent execution loops.

---

## 1. Reversibility Decision Tree

Before invoking any mutating tool or executing a state-changing shell command, evaluate the reversibility tier:

```text
Does an automated inverse operation exist?
  ├─ YES: Can it restore the exact bitwise pre-state?
  │    ├─ YES ──> PURE_REVERSIBLE (Log pre-hash and inverse snapshot)
  │    └─ NO  ──> COMPENSABLE (Log semantic counter-action)
  └─ NO: Can an equivalent balancing action be executed?
       ├─ YES ──> COMPENSABLE (Define idempotent compensation handler)
       └─ NO: Does the action affect external systems or shared history?
            ├─ YES ──> FORWARD_FIX_ONLY (Require explicit remediation plan)
            └─ NO  ──> IRREVERSIBLE (Strict human approval checkpoint required)
```

---

## 2. Common Action Archetypes & Inverses

| Operation Type | Reversibility Tier | Forward Action | Idempotent Compensation Handler | Verification Check |
|---|---|---|---|---|
| Workspace File Edit | `PURE_REVERSIBLE` | `replace_with_git_merge_diff` / `write_file` | Restore file from pre-execution snapshot or reverse diff patch | SHA-256 match on restored file |
| New File Creation | `PURE_REVERSIBLE` | `write_file` (new file) | `delete_file(filepath)` | Verify file does not exist |
| Dependency Addition | `COMPENSABLE` | `npm install <pkg>` / `pip install <pkg>` | `git checkout HEAD package.json package-lock.json && npm install` | Clean `git status --porcelain` |
| Database Migration | `COMPENSABLE` | `prisma migrate dev` / `alembic upgrade` | `prisma migrate resolve --rolled-back` / `alembic downgrade -1` | Target DB schema version inspection |
| Background Service | `COMPENSABLE` | `npm run dev &` (spawns PID on :3000) | `kill $(lsof -t -i :3000) 2>/dev/null \|\| true` | Confirm port is unallocated (`lsof -i :3000` empty) |
| Git Commit (Local) | `PURE_REVERSIBLE` | `git commit -m "..."` | `git reset --soft HEAD~1` | Git reflog inspection |
| External API Mutation | `FORWARD_FIX_ONLY` | Post webhook / deploy artifact | Issue cancellation API call or forward fix deployment | Verification via remote status probe |
| Remote Force Push | `IRREVERSIBLE` | `git push --force` | Forbidden without Level 4 human checkpoint | N/A (Blocked pre-execution) |

---

## 3. Append-Only Transaction Journal Protocol

Before executing any mutative step:
1. Capture `pre_state_hash` of all target files or system metrics.
2. Formulate the exact inverse command or handler specification.
3. Append entry to `journal.jsonl` with status `APPLIED`.
4. Execute tool. If successful, transition status to `COMMITTED`.
5. If step fails or an unexpected error/signal occurs, initiate unwinding.

---

## 4. Saga Compensation Unwinding Loop

```text
[EXECUTION FAILURE TRIGGERED]
  │
  ├─> Read journal.jsonl in reverse order (LIFO)
  │
  ├─> For each transaction in COMPENSATING queue:
  │     ├─ Execute compensation_action
  │     ├─ Verify restored state (hash / port / process)
  │     ├─ If PASS: Mark entry COMPENSATED
  │     └─ If FAIL:
  │          ├─ Mark entry COMPENSATION_FAILED
  │          ├─ Halt further automated unwinds
  │          └─ Emit QUARANTINE_MANUAL_HOLD & Escalation Report
  │
  └─> Confirm overall pristine status & emit VERIFIED evidence
```

---

## 5. Handling Partial Failures and Quarantines

When a compensation handler fails:
- **Do not blindly retry destructive commands**: If a file restore fails due to unexpected file locks or disk write errors, repeating without diagnosing risks further corruption.
- **Isolate the workspace**: Ensure no other concurrent subagents write to the affected workspace directory.
- **Generate escalation report**: Follow `.ai/templates/escalation-report.md` including exact diverging hashes and the journal transaction trail.
