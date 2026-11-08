# Operational Reference: Reversibility & State Compensation

## Metadata
- **skill**: `safety`
- **reference_id**: `reversibility_and_compensation`
- **contract**: `.ai/contracts/rollback.contract.md`

## Purpose
Provide practical operational procedures for evaluating reversibility, managing side-effects, generating compensating actions, and handling state recovery across multi-step agent workflows.

---

## 1. Operational Reversibility Assessment

Before executing any mutating command or tool, the agent must determine its reversibility tier:

```text
               Mutating Tool Request
                         │
                         ▼
           Does it modify only workspace files
           tracked by Git without committing?
                         │
           ┌─────────────┴─────────────┐
          Yes                          No
           │                           │
           ▼                           ▼
    PURE_REVERSIBLE        Does it spawn processes, install
    (Restore via git /      local packages, or create temp data?
     file snapshot)                    │
                                ┌──────┴──────┐
                               Yes            No
                                │             │
                                ▼             ▼
                           COMPENSABLE   Is it an external API call,
                           (Kill daemon,  credential rotation, or
                            uninstall,    remote push?
                            drop DB)          │
                                       ┌──────┴──────┐
                                      Yes            No
                                       │             │
                                       ▼             ▼
                                  IRREVERSIBLE  FORWARD_FIX_ONLY
                                  (Block for    (Complex migration,
                                   checkpoint)   synthesize forward fix)
```

---

## 2. Resource-Specific Compensation Procedures

### 2.1 Git Working Tree & Workspace Files
- **Forward Action**: `write_file`, `replace_with_git_merge_diff`, `delete_file`.
- **Pre-execution Snapshot**:
  - If target file exists: read prior content or capture blob hash (`git hash-object`).
  - If target file does not exist: record that it is a newly created path.
- **Compensating Action**:
  - Modified file: restore snapshot content or run `git checkout -- <filepath>`.
  - Created file: delete the file (`rm <filepath>` or tool equivalent).
  - Deleted file: write back cached snapshot.

### 2.2 Processes, Daemons & Port Bindings
- **Forward Action**: Spawning background servers (e.g. `npm run dev &`, test databases, mock servers).
- **Compensating Action**:
  - Record the PID or bound port immediately upon launch.
  - Inverse sequence:
    1. Send `SIGTERM` to the PID: `kill <PID> 2>/dev/null || true`.
    2. Fallback to port cleanup: `kill $(lsof -t -i :<PORT>) 2>/dev/null || true`.
    3. Verify process termination via `pgrep` or `lsof`.

### 2.3 Dependency & Environment Package Changes
- **Forward Action**: Installing packages via npm, pip, cargo, etc.
- **Pre-execution Snapshot**:
  - Snapshot `package.json`, `package-lock.json`, `requirements.txt`, or environment manifests.
- **Compensating Action**:
  - Restore lockfiles and manifest files.
  - Run package manager prune/clean (e.g. `npm prune`, `pip uninstall -y <package>`).

### 2.4 Temporary Directories and Scratch Artifacts
- **Forward Action**: Generating build artifacts in `./build`, `./dist`, or `/tmp/scratch-*`.
- **Compensating Action**:
  - Constrain scratch space to explicit subdirectories.
  - Inverse: delete the designated temporary directory cleanly.

---

## 3. Handling Rollback Failures (Saga Escalation)

When a compensating action fails or its verification probe detects lingering corruption:

1. **Do not retry blindly**: Repeated failed compensation attempts can aggravate corruption.
2. **Transition to SUPERVISED_ROLLBACK_CHECKPOINT**:
   - Halt automatic script execution.
   - Summarize the exact discrepancy in the escalation report:
     - Which steps were cleanly reversed.
     - Which step failed compensation.
     - Observed current environment state (`git status`, running processes, disk diff).
3. **Escalate to Human Supervisor**:
   - Present proposed manual remediation commands (e.g., manual git reset, process termination).
   - Await human instruction before resuming.
