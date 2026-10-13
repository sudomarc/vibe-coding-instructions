# Long-Horizon Task State Manifest

> Persistent state manifest for long-horizon engineering tasks spanning multiple sessions, phases, or agents.
> Stored at `.ai/artifacts/<task_id>/state.json` (or `.md` summary). Conforms to `.ai/contracts/long-horizon-task.contract.md`.

## Task Metadata
- **task_id**: `lh-task-YYYYMMDD-001`
- **title**: Brief descriptive title of long-horizon goal
- **status**: `IN_PROGRESS | COMPLETED | BLOCKED | FAILED`
- **current_phase**: `RESEARCH | PLANNING | IMPLEMENTATION | VERIFICATION`
- **current_session_id**: `sess-001`
- **created_at**: ISO-8601 UTC timestamp
- **updated_at**: ISO-8601 UTC timestamp

## Budget & Cost Tracking
- **max_sessions**: `10`
- **current_session**: `1`
- **max_cumulative_tokens**: `1000000`
- **cumulative_tokens_used**: `0`
- **max_estimated_cost_usd**: `15.00`
- **cumulative_cost_usd**: `0.00`

## Phase Lifecycle
| Phase ID | Name | Assigned Agent | Status | Artifact Ref |
|---|---|---|---|---|
| `phase-01` | Research & Architecture | `researcher-01` | `COMPLETED` | `.ai/artifacts/<task_id>/research-handoff.json` |
| `phase-02` | Core Implementation | `coder-01` | `IN_PROGRESS` | - |
| `phase-03` | Integration Verification | `coder-01` | `PENDING` | - |

## Checkpoints History
### Checkpoint `chk-001`
- **session_id**: `sess-001`
- **timestamp**: ISO-8601 UTC
- **git_commit_sha**: `abc1234`
- **verification_evidence_ref**: `ev-sess-001-tests`
- **compacted_context_summary**: Concise summary of progress, decisions, and verified state.

## Resume State (For Next Session)
- **pending_subtasks**:
  1. Subtask item 1
  2. Subtask item 2
- **known_blockers**: None
- **last_failed_attempt**:
  - **error_category**: `TOOL_EXEC_ERR`
  - **description**: What failed
  - **recovery_hypothesis**: Plan to fix

## Verification & Acceptance Criteria
- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
- [ ] All unit and integration tests passing
