# Reversibility & State Compensation Patterns

## Purpose
Provide engineering agents and runtime supervisors with operational guidance, action-to-compensation mappings, and recovery patterns across common development mutations in the CHAD + LapisLLM ecosystem.

---

## 1. Action-to-Compensation Mapping Matrix

| Mutating Action | Tool / Command | Reversibility Tier | Compensating Action | Verification Gate |
|---|---|---|---|---|
| Overwrite file | `write_file`, `replace_with_git_merge_diff` | `PURE_REVERSIBLE` | Restore file from pre-mutation snapshot or `git checkout -- <file>` | SHA-256 hash match against snapshot |
| Create new file | `write_file` (new path) | `PURE_REVERSIBLE` | Delete created file (`delete_file` or `rm`) | File path does not exist on disk |
| Rename / move file | `rename_file` | `PURE_REVERSIBLE` | Move file back to source path (`rename_file(dst, src)`) | Source path exists, destination path absent |
| Git stage | `git add <file>` | `PURE_REVERSIBLE` | Unstage changes (`git restore --staged <file>` or `git reset HEAD <file>`) | `git status --porcelain` indicates untracked/unstaged |
| Local commit | `git commit -m "..."` | `COMPENSABLE` | Soft reset commit (`git reset --soft HEAD~1`) | Previous commit hash restored to HEAD |
| Background server | `run_in_bash_session: cmd &` | `COMPENSABLE` | Terminate PID / port listener (`kill <pid>` or `kill $(lsof -t -i :<port>)`) | Port is free and process exited |
| Resource lock acquisition | Concurrency Lock Manager | `COMPENSABLE` | Explicit lock release RPC or lease termination | Lock status in registry is `RELEASED` |
| Database migration (additive) | `alembic upgrade`, `prisma migrate` | `COMPENSABLE` | Run downgrade migration (`alembic downgrade -1`) | Migration history table and schema match previous revision |
| Database migration (destructive) | Drop column / table | `FORWARD_FIX_ONLY` | Automated rollback blocked; prompt for human backup restore | Human checkpoint required |
| Remote push / deployment | `git push`, webhook dispatch | `IRREVERSIBLE` | Automated rollback blocked; flag incident and escalate | Operator manual intervention |

---

## 2. Operational Compensation Protocols

### 2.1 Filesystem & Workspace Rollback Protocol
1. **Pre-mutation Capture**:
   - Before modifying any file, agents or runtime interceptors record whether the file existed and its pre-mutation SHA-256 hash.
2. **Failure Trigger**:
   - Upon encountering a build, lint, or test failure that cannot be resolved within the retry budget:
     - Enumerate journaled file modifications in reverse chronological order.
     - For each touched file:
       - If `existed_prior == false`: delete the file.
       - If `existed_prior == true`: restore file content from snapshot.
3. **Verification**:
   - Execute `git status --porcelain` to confirm that the working tree contains no lingering uncommitted artifacts from the failed attempt.

### 2.2 Process & Port Compensation Protocol
1. **Process Tracking**:
   - Any background process dispatched by an agent (e.g. `npm run dev &`, preview servers, mock APIs) must log its PID and bound port to the side-effect journal.
2. **Termination Sequence**:
   - Send `SIGTERM` to the tracked PID.
   - Wait up to 5 seconds for graceful process termination.
   - If the process or port remains bound, issue `SIGKILL` (`kill -9 <PID>`).
   - Validate port availability via `lsof -i :<port>` or test socket binding.

### 2.3 Distributed Lock Compensation Protocol
1. **Context Abort Integration**:
   - When an agent encounters `SAFETY_TRIGGERED`, `GOAL_BLOCKED`, or `MAX_BUDGET_REACHED`:
     - Inspect active locks recorded in `.ai/contracts/concurrency-lock.contract.md`.
     - Dispatch `RELEASE_LOCK` calls for all held `FILE_LOCK`, `DIRECTORY_LOCK`, and `SHARED_RESOURCE_LOCK` entities.
     - Verify that the wait-for dependency graph clears the agent node.

---

## 3. Recovery Strategy Decision Tree

```text
[Failure or Stop Condition Triggered]
                  │
                  ▼
   Does the journal contain any IRREVERSIBLE steps?
      ├─ YES ──► [QUARANTINE_MANUAL_HOLD]
      │           - Freeze state
      │           - Emit incident report to operator
      │           - Do not attempt automatic inverse
      │
      └─ NO
           ▼
   Does the journal contain FORWARD_FIX_ONLY steps?
      ├─ YES ──► [SUPERVISED_ROLLBACK_CHECKPOINT]
      │           - Unwind PURE_REVERSIBLE steps back to boundary
      │           - Pause and request human checkpoint for forward fix
      │
      └─ NO
           ▼
         [AUTOMATED_SAGA_UNWIND]
           - LIFO execution of compensating actions
           - Run compensation verification gates
           - Report clean rollback telemetry
```

---

## 4. Best Practices for Coding Agents

1. **Keep Mutations Fine-Grained**: Group changes into cohesive, independently compensable batches.
2. **Validate Idempotence**: Ensure compensating actions can be executed multiple times without throwing errors or causing state drift.
3. **Never Mask Rollback Failures**: If a compensating action fails, immediately halt the automated unwind and escalate with `COMPENSATION_FAILED`.
4. **Preserve Diagnostic Artifacts**: When unwinding workspace state, archive failure logs and diffs into an ephemeral diagnostic folder so post-mortem analysis remains possible without polluting the source tree.
