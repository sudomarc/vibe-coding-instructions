# Long-Horizon Task & Multi-Session Governance Contract

This contract defines the governance principles, data schemas, and lifecycle constraints for AI engineering agents executing complex, multi-session, long-horizon tasks across session boundaries, subagent handoffs, and checkpoint resumes in the CHAD + LapisLLM ecosystem.

---

## 1. Governance Architecture

Long-horizon tasks span multiple context sessions, execution runs, or subagent handoffs. To maintain execution fidelity, state consistency, and budget controls, long-horizon execution adheres to this protocol:

```text
Orchestrator / Human Request
        │
        ▼
Multi-Session Task State Initialization
        │
        ├── Session N (Research / Planning) ──► Research-to-Code Handoff Artifact
        │                                             │
        ├── Session N+1 (Implementation) ◄───────────┘
        │      │
        │      ├── Context Compaction & Checkpoint State
        │      └── Cross-Agent Artifact Contracts
        │
        └── Failure / Interruption ──► Failure-Resume Recovery Semantics
```

---

## 2. Multi-Session Task State Schema

All long-horizon tasks maintain a durable state object serialized at session boundaries and saved in runtime persistent storage (`.ai/state/tasks/{task_id}.json`).

```json
{
  "$schema": "https://sudomarc.github.io/vibe-coding-instructions/schemas/long-horizon-task.v1.json",
  "task_id": "lht-2026-0331-8f9a",
  "title": "Implement Distributed Tracing Engine",
  "status": "IN_PROGRESS",
  "current_session_index": 3,
  "max_sessions": 10,
  "created_at": "2026-03-31T10:00:00Z",
  "updated_at": "2026-03-31T14:30:00Z",
  "budget_controls": {
    "max_accumulated_cost_usd": 15.00,
    "current_accumulated_cost_usd": 4.25,
    "max_total_tokens": 1500000,
    "current_total_tokens": 420000,
    "token_limit_action": "PAUSE_AND_CHECKPOINT"
  },
  "completed_milestones": [
    "M1: Architecture research and design brief",
    "M2: Core data model and storage schema"
  ],
  "active_milestone": "M3: API endpoints and middleware integration",
  "remaining_milestones": [
    "M4: End-to-end integration tests & benchmarking",
    "M5: Documentation and migration guide"
  ],
  "checkpoints": [
    {
      "checkpoint_id": "chk-002",
      "session_index": 2,
      "timestamp": "2026-03-31T12:15:00Z",
      "git_commit_sha": "a1b2c3d4e5f6",
      "state_snapshot_ref": ".ai/state/checkpoints/chk-002.json"
    }
  ]
}
```

---

## 3. Durable Task Handoffs & Context Compaction

When transitioning between sessions or reaching context thresholds during a long-horizon task:

1. **Context Compaction Conventions**:
   - Before writing a handoff or snapshot, active trajectory state MUST be compacted.
   - Raw tool outputs, redundant file reads, and intermediate conversation dialogue MUST be pruned.
   - Preserved state MUST include: objective, verified facts, active code decisions, git branch/diff references, test results, open risks, and next step instructions.

2. **Durable Handoff Snapshot**:
   - The agent MUST populate `.ai/templates/long-horizon-task.md` or append to the task state file.
   - Subsequent sessions MUST re-inspect repository state before executing code changes. Repository evidence outranks handoff claims when conflicts occur.

---

## 4. Research-to-Code Handoff Artifacts

When a research or analysis session precedes code implementation, the agent MUST produce a structured `Research-to-Code Handoff Artifact` conforming to this contract:

```json
{
  "artifact_type": "RESEARCH_TO_CODE_HANDOFF",
  "task_id": "lht-2026-0331-8f9a",
  "research_summary": "Evaluated OpenTelemetry vs custom trace buffer; selected custom lock-free ring buffer.",
  "architectural_decisions": [
    {
      "decision": "Use lock-free ring buffer for trace spans",
      "rationale": "Meets 50ns latency allocation without mutex lock contention under high concurrency.",
      "alternatives_rejected": ["Mutex-backed deque", "Channel per thread"]
    }
  ],
  "target_files": [
    "pkg/tracing/buffer.go",
    "pkg/tracing/span.go",
    "pkg/tracing/buffer_test.go"
  ],
  "verification_contract": [
    "go test -v -race ./pkg/tracing/...",
    "go test -bench=. ./pkg/tracing/..."
  ],
  "risk_assessment": "Potential memory overhead if span allocation rate exceeds flush consumer capacity."
}
```

---

## 5. Cross-Agent Artifact Contracts

When multiple specialized agents (e.g., Researcher, Coder, Analyst, Reviewer) collaborate on a long-horizon task, artifacts exchanged across boundaries MUST adhere to explicit schemas:

- **Immutable Artifact ID**: Every artifact receives a deterministic hash or unique ID.
- **Provenance Tracking**: Includes originating agent ID, trace ID, timestamp, and permission scope.
- **Trust Level**: Labeled as `VERIFIED_LOCAL`, `UNTRUSTED_REMOTE`, or `ISOLATED_SANDBOXED`.
- **Validation Constraint**: Receiver subagents MUST validate schema compliance before processing.

---

## 6. Failure-Resume Recovery Semantics

Long-horizon tasks must gracefully recover from crashes, context exhaustion, model errors, or rate limits using standardized `Failure-Resume Semantics`:

1. **Checkpoint Rollback & Recovery**:
   - On resumption after an abnormal termination, the Orchestrator inspects the latest verified checkpoint (`checkpoint_id`).
   - The workspace state is reconciled against `git_commit_sha` and `.ai/state/checkpoints/`.
2. **Re-Verification Pass**:
   - Before resuming implementation, the agent executes a lightweight verification pass on existing files to confirm workspace integrity.
3. **Failure Classification & Resume Strategy**:
   - `PERM_DENIED` / `SAFETY_BLOCKED`: Pause task, raise human checkpoint.
   - `CONTEXT_EXCEEDED`: Trigger forced compaction, reload minimal HOT context snapshot, resume from active milestone.
   - `TOOL_EXEC_ERR` / `PLAN_DEFECT`: Re-evaluate plan step, isolate failing file/test, apply minimal repair.

---

## 7. Long-Running Cost & Budget Controls

To prevent unbounded token consumption or runaway costs during long-horizon tasks:

1. **Hard Cost & Token Ceilings**:
   - Every long-horizon task MUST specify `max_accumulated_cost_usd` and `max_total_tokens`.
   - Exceeding 80% of budget triggers automatic compaction and advisory notification.
   - Exceeding 100% of budget triggers mandatory execution suspension and `HUMAN_CHECKPOINT_REQUIRED`.
2. **Per-Session Step Limits**:
   - Individual subagent sessions within a long-horizon task are capped at a maximum number of tool steps (default: 30 steps) before requiring a checkpoint handoff.
3. **Cost-per-Verified-Success Metrics**:
   - Runtime tracking calculates `Cost per Verified Milestone` to identify inefficient execution loops.

---

## 8. Ecosystem Compatibility (CHAD & LapisLLM)

### CHAD Runtime Layer
- CHAD serializes long-horizon task state in `.ai/state/tasks/` and handles multi-session context persistence.
- CHAD enforces budget limits and triggers checkpoint handoffs when session step limits or token caps are reached.
- CHAD automatically invokes failure-resume recovery routines on session crash or interruption.

### LapisLLM Model Layer
- LapisLLM provides high-efficiency prompt caching across session resume checkpoints to minimize re-ingestion cost.
- LapisLLM inference gateway exposes token usage headers enabling CHAD to track accumulated task cost accurately.
