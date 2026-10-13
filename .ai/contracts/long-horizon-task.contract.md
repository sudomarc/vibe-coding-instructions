# Standard Long-Horizon Task Governance Contract

## Metadata
- **contract_id**: `long_horizon_task_governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Establish a provider-neutral governance contract standardizing multi-session task state, research-to-code handoff artifacts, cross-agent exchange protocols, failure-resume recovery semantics, context compaction conventions, and long-running cost/budget controls for long-horizon engineering tasks.

---

## 1. Multi-Session Task Lifecycle Architecture

Long-horizon tasks span multiple agent execution sessions, model contexts, or agent boundaries. Execution is structured as a phase state machine where task state is checkpointed and persisted independently of the ephemeral conversation context.

```text
               ┌────────────────────────┐
               │    RESEARCH / PLAN     │
               └───────────┬────────────┘
                           │
             Research-to-Code Handoff Artifact
                           │
                           ▼
               ┌────────────────────────┐
               │     IMPLEMENTATION     │ ◄───────┐
               └───────────┬────────────┘         │
                           │                      │ Failure / Resume
             Checkpoint / State Transition        │ Recovery Protocol
                           │                      │
                           ▼                      │
               ┌────────────────────────┐         │
               │   VERIFY / INTEGRATE   ├─────────┘
               └───────────┬────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │  COMPLETED / HANDOFF   │
               └────────────────────────┘
```

---

## 2. Multi-Session Task State Schema

All multi-session long-horizon tasks MUST maintain a persistent task state manifest conforming to the `multi_session_task_state` schema.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "task_id": "lh-task-20250330-001",
  "title": "Migrate Database ORM to Async SQLAlchemy 2.0",
  "status": "IN_PROGRESS",
  "current_phase": "IMPLEMENTATION",
  "current_session_id": "sess-003",
  "created_at": "2025-03-30T10:00:00Z",
  "updated_at": "2025-03-30T12:15:00Z",
  "budget": {
    "max_sessions": 10,
    "current_session": 3,
    "max_cumulative_tokens": 1000000,
    "cumulative_tokens_used": 245000,
    "max_estimated_cost_usd": 15.0,
    "cumulative_cost_usd": 3.68
  },
  "phases": [
    {
      "phase_id": "phase-01-research",
      "name": "Research & Architectural Mapping",
      "status": "COMPLETED",
      "assigned_agent": "researcher-01",
      "started_at": "2025-03-30T10:00:00Z",
      "completed_at": "2025-03-30T10:45:00Z",
      "artifact_ref": ".ai/artifacts/lh-task-20250330-001/research-handoff.json"
    },
    {
      "phase_id": "phase-02-implementation",
      "name": "Async ORM Code Migration",
      "status": "IN_PROGRESS",
      "assigned_agent": "coder-01",
      "started_at": "2025-03-30T10:45:00Z",
      "completed_at": null,
      "artifact_ref": null
    }
  ],
  "checkpoints": [
    {
      "checkpoint_id": "chk-002",
      "session_id": "sess-002",
      "timestamp": "2025-03-30T11:30:00Z",
      "git_commit_sha": "a1b2c3d4e5f6",
      "verification_evidence_ref": "ev-sess-002-tests",
      "compacted_context_summary": "Migrated models/user.py and models/order.py to async definitions. 12/12 unit tests passing."
    }
  ],
  "resume_state": {
    "pending_subtasks": [
      "Migrate models/payment.py to async SQLAlchemy",
      "Update database session middleware in API routes"
    ],
    "known_blockers": [],
    "last_failed_attempt": null
  }
}
```

---

## 3. Research-to-Code Handoff Schema

When transitioning from research/investigation to code implementation, the Researcher or Analyst agent MUST produce a structured `research_to_code_handoff` artifact before coding begins.

### 3.1 Research-to-Code Handoff Schema (`research-handoff.json`)

```json
{
  "handoff_version": "1.0",
  "task_id": "lh-task-20250330-001",
  "source_agent": "researcher-01",
  "target_agent": "coder-01",
  "timestamp": "2025-03-30T10:45:00Z",
  "architectural_decisions": [
    {
      "decision_id": "adr-001",
      "title": "Use AsyncSession with asyncpg backend",
      "rationale": "Matches high-concurrency requirements and PostgreSQL database driver capabilities.",
      "alternatives_rejected": ["databases library (lacks ORM 2.0 mapping features)"]
    }
  ],
  "target_files": [
    {
      "path": "src/database/session.py",
      "action": "MODIFY",
      "description": "Replace SyncEngine with create_async_engine and async_sessionmaker"
    },
    {
      "path": "src/models/user.py",
      "action": "MODIFY",
      "description": "Convert Column declarations to Mapped[] and mapped_column()"
    }
  ],
  "verification_plan": {
    "test_commands": ["pytest tests/unit/test_database.py"],
    "acceptance_criteria": [
      "All ORM operations use await session.execute()",
      "No synchronous I/O calls remain in API event loops"
    ]
  },
  "evidence": [
    {
      "label": "VERIFIED",
      "statement": "SQLAlchemy 2.0.28 is present in requirements.txt",
      "source": "requirements.txt",
      "timestamp": "2025-03-30T10:15:00Z"
    }
  ]
}
```

---

## 4. Cross-Agent Artifact Exchange Protocol

Artifacts exchanged between agents across sessions or phases follow strict exchange protocols (`cross_agent_artifact_exchange`):

1. **Immutable Storage**: Artifacts are written to `.ai/artifacts/<task_id>/` and MUST NOT be edited in-place once finalized.
2. **Provenance Traceability**: Every artifact references `task_id`, `source_agent`, `target_agent`, and `trace_id`.
3. **Repository Truth Precedence**: Code and git commit state in the workspace outrank stale claims in artifacts. A receiving agent MUST re-verify codebase state before execution.

---

## 5. Failure-Resume Recovery Semantics

When a session terminates abruptly (e.g. timeout, context limit, model API error, or unexpected failure), the recovery protocol (`failure_resume_recovery`) executes upon session start:

```text
Session Resume Sequence:
1. Load task state manifest (.ai/artifacts/<task_id>/state.json)
2. Read latest valid checkpoint (chk-N) and verify git_commit_sha against workspace
3. Inspect resume_state.last_failed_attempt (if non-null, isolate failure root cause)
4. Verify workspace state with focused test/inspection pass before attempting new code changes
5. Resume execution on resume_state.pending_subtasks[0]
```

### 5.1 Failure State Recording
If execution fails, the state manifest MUST record:
- `error_category`: Conforming to `.ai/self-improvement/references/failure-taxonomy.md` (e.g., `PLAN_DEFECT`, `TOOL_EXEC_ERR`, `CONTEXT_EXCEEDED`).
- `failure_context`: Last tool call, exact error message, and hypothesis for recovery.
- `rollback_point`: Git commit SHA or checkpoint ID to revert to if current state is corrupted.

---

## 6. Context Compaction & Token Economics Controls

To keep token costs manageable during long-running tasks, agents execute context compaction (`context_compaction_conventions`):

1. **Compaction Trigger**: Compaction MUST occur when context utilization exceeds 75% of context window or prior to initiating a new major task phase.
2. **Preserved Invariants**: Context compaction MUST preserve:
   - Primary Task Objective & Current Phase Goal;
   - Confirmed Facts (`FACT`, `VERIFIED`);
   - Rejection decisions and root causes of failed attempts;
   - Exact remaining pending subtasks and acceptance criteria.
3. **Pruned Elements**: Raw tool stdout/stderr, unchanged code reads, duplicate research outputs, and superseded intermediate thoughts MUST be pruned.

---

## 7. Budget & Stop Conditions for Long-Running Execution

Execution MUST halt and report to Orchestrator or human checkpoint under the following stop conditions:

- `MAX_SESSIONS_EXCEEDED`: Cumulative sessions exceed `budget.max_sessions`.
- `BUDGET_CAP_REACHED`: Token or USD cost exceeds configured budget.
- `REPEATED_PHASE_FAILURE`: Same subtask fails across 3 consecutive session attempts.
- `HUMAN_CHECKPOINT_REQUIRED`: High-risk or breaking migration step requiring manual confirmation.
