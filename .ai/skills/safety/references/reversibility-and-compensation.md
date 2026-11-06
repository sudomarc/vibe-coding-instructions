# Reversibility & State Compensation Guidance

This reference provides operational guidelines and execution protocols for AI agents performing mutations in the CHAD + LapisLLM ecosystem, ensuring all actions adhere to `.ai/contracts/rollback.contract.md`.

---

## 1. Core Operating Principle: Zero Uncompensated State

Every mutation performed by an agent introduces potential instability. If a batch fails midway through execution, leaves broken syntax, or triggers a security barrier, an agent must never abandon the workspace in a dirty state.

**The Golden Invariant**:
> No mutating tool call (`write_file`, `replace_with_git_merge_diff`, shell state modification) may execute without first recording a valid compensation strategy and pre-state snapshot in the side-effect journal.

---

## 2. Reversibility Classification at Plan Time

Before invoking any tool that modifies files, environment, dependencies, or external resources, the agent must evaluate its reversibility tier:

### 2.1 PURE_REVERSIBLE
- **Examples**: Modifying an existing file, adding a new source file, deleting a temporary cache.
- **Requirements**:
  - Existing files: Record current SHA-256 hash and snapshot path.
  - New files: Inverse tool is `delete_file`.
  - Deleted files: Store pre-deletion contents in snapshot; inverse tool is `write_file`.

### 2.2 COMPENSABLE
- **Examples**: Running a database schema migration (`npm run migrate:up`), creating a mock OAuth client, installing a package via npm/pip.
- **Requirements**:
  - Must provide explicit inverse command (e.g. `npm run migrate:down`, `npm uninstall <pkg>`).
  - Pre-flight dry run must be executed whenever available.

### 2.3 FORWARD_FIX_ONLY
- **Examples**: Non-reversible data backfill, asynchronous schema compaction, non-idempotent data conversion.
- **Requirements**:
  - Must NOT be grouped into an automated saga batch.
  - Requires pre-computation of forward-fix patches and human review.

### 2.4 IRREVERSIBLE
- **Examples**: `rm -rf` on root/unbounded paths, `git push --force` to upstream, dropping a database table without backups, revoking root certificates.
- **Requirements**:
  - **HARD STOP**: Requires explicit human checkpoint (`HUMAN_CHECKPOINT_REQUIRED`). Never execute autonomously.

---

## 3. Side-Effect Journaling Flow

When executing a batch of mutations, the agent coordinates with the CHAD runtime journal manager:

1. **Pre-Mutation Snapshotting**:
   ```bash
   # Conceptual runtime hook before write_file('src/config.ts')
   sha256sum src/config.ts > .ai/state/snapshots/src/config.ts.sha256
   cp src/config.ts .ai/state/snapshots/src/config.ts.bak
   ```
2. **Journal Declaration**:
   - Register the pending entry in `.ai/state/journal.jsonl` with status `COMMITTED` once write succeeds.
3. **Batch Boundary**:
   - Once all mutations in a plan batch succeed and pass verification, the journal batch is marked `RESOLVED`.

---

## 4. Saga Unwind Execution Protocol

When a test fails, syntax errors persist across allowed retries, or `SAFETY_TRIGGERED` occurs:

1. **Cease Further Mutations**: Immediately stop pending forward operations.
2. **Read Journal in LIFO Order**: Load entries from `.ai/state/journal.jsonl` for the current batch from last committed to first committed.
3. **Execute Inverses Sequentially**:
   - For file writes: Restore from `.bak` or delete newly created files.
   - For database/environment: Run defined inverse compensation commands.
4. **Run Verification Probes**:
   - Verify file hashes against recorded `pre_state.sha256`.
   - Run `git status --porcelain` to confirm clean working directory.
   - Run quick syntax check (`tsc --noEmit`, `python3 -m py_compile`, etc.).
5. **Report Outcome**: Emit a Rollback Manifest conforming to `.ai/templates/rollback-journal.md`.

---

## 5. Handling Compensation Failures (Quarantine Protocol)

If any inverse operation fails during saga unwinding:
- **Do not guess or try speculative shell commands.**
- Immediately transition status to `QUARANTINE_MANUAL_HOLD`.
- Isolate the divergence: Record the exact file, expected hash vs observed hash, and failed compensation command.
- Escalate to the human supervisor with evidence labels `CONFLICT` and `FACT`.
