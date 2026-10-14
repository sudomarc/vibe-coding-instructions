# Long-Horizon Task State & Handoff Manifest

## Metadata
- **Task ID**: `lh-YYYYMMDD-task-name`
- **Task Title**: [Concise Task Title]
- **Status**: `[NOT_STARTED | IN_PROGRESS | BLOCKED | VERIFYING | COMPLETED]`
- **Current Phase**: `[Phase 1: Research | Phase 2: Architecture | Phase 3: Implementation | Phase 4: Verification]`
- **Active Session ID**: `session-001`
- **Session Count**: `1 / Max 10`
- **Created At**: `YYYY-MM-DD HH:MM UTC`
- **Last Updated**: `YYYY-MM-DD HH:MM UTC`

---

## Task Budget & Resource Limits
- **Max Cost Cap (USD)**: `$15.00`
- **Consumed Cost (USD)**: `$0.00`
- **Max Token Budget**: `5,000,000`
- **Consumed Tokens**: `0`
- **Autonomy Level**: `L1_BOUNDED_AUTONOMY`

---

## 1. Objective & Non-Goals
### Invariant Objective
[Clear description of the observable outcome that must be achieved]

### Non-Goals
- [Boundary 1: What this long-horizon task will NOT attempt]
- [Boundary 2: Out-of-scope refactoring]

---

## 2. Research-to-Code Handoff
*Must be completed and verified before entering implementation phase.*

### Verified Technical Hypotheses
- **Fact / Observed**: [Key codebase constraint discovered during inspection]
- **Evidence**: `path/to/file.ext:lines`
- **Architectural Decision**: [Chosen pattern/approach]

### Target File Plan
- [ ] `path/to/file1.ext` — [Created | Modified | Deleted] — [Purpose]
- [ ] `path/to/file2.ext` — [Created | Modified | Deleted] — [Purpose]

### Architectural Invariants
- [Invariant 1: e.g. Do not break public API compatibility in `v1/chat/completions`]
- [Invariant 2: e.g. Preserve token economy budget invariants]

---

## 3. Subtask Execution Ledger

| Subtask ID | Phase | Description | Status | Verification Evidence |
|---|---|---|---|---|
| `st-01` | Research | Inspect codebase architecture | COMPLETED | `logs/research.md` |
| `st-02` | Implementation | Implement interface adapters | IN_PROGRESS | — |
| `st-03` | Verification | Run full automated test suite | PENDING | — |

---

## 4. Checkpoint & Failure Recovery State

### Repository State Checkpoint
- **Git Branch**: `feature/long-horizon-task`
- **Last Verified Git Commit**: `abcdef123456`
- **Dirty / Uncommitted Files**:
  - `src/index.ts`
- **Open Risks & Blockers**:
  - [Risk 1: Potential dependency conflict in package updates]

### Failure Recovery Log
| Session ID | Timestamp | Incident / Crash Type | Reconciliation Action Taken |
|---|---|---|---|
| — | — | No incidents recorded | — |

---

## 5. Next Session Execution Plan
1. [Exact step 1 for resuming session]
2. [Exact step 2 for resuming session]
3. [Verification command to run after batch completion]
