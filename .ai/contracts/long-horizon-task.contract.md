# Governance Contract: Long-Horizon Task Execution

## Metadata
- **contract_id**: `long-horizon-task-governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Define formal schemas, handoff interfaces, state recovery rules, and budget boundaries for long-horizon engineering tasks that span multiple sessions, subagent handoffs, or context compaction boundaries.

---

## 1. Multi-Session Task State Schema (`multi_session_state`)

Long-horizon tasks require persistent state representation across session boundaries and context truncations. All multi-session state records MUST conform to the following schema:

```json
{
  "task_id": "lht-2026-0412-auth-overhaul",
  "version": "1.0.0",
  "session_id": "sess-8921-b",
  "checkpoint_counter": 4,
  "status": "IN_PROGRESS | COMPLETED | BLOCKED | FAILED | RECOVERING",
  "created_at": "2026-04-12T10:00:00Z",
  "updated_at": "2026-04-12T14:30:00Z",
  "objective": "Replace legacy session cookies with JWT bearer tokens across backend and frontend",
  "subtask_graph": {
    "nodes": [
      {
        "subtask_id": "st-001",
        "title": "Research OAuth/JWT patterns",
        "assigned_role": "researcher",
        "status": "COMPLETED",
        "dependencies": [],
        "artifact_id": "art-res-001"
      },
      {
        "subtask_id": "st-002",
        "title": "Implement auth middleware",
        "assigned_role": "coder",
        "status": "IN_PROGRESS",
        "dependencies": ["st-001"],
        "artifact_id": "art-code-002"
      }
    ]
  },
  "active_context_window": {
    "hot_files": ["src/auth/middleware.ts", "src/auth/jwt.ts"],
    "verified_facts": ["Existing cookie handler is in src/legacy/session.ts"],
    "open_questions": ["Token refresh TTL requirement"]
  },
  "budget_controls": {
    "max_total_tokens": 5000000,
    "consumed_tokens": 1250000,
    "max_sessions": 10,
    "consumed_sessions": 2,
    "max_cost_usd": 15.00,
    "consumed_cost_usd": 3.75
  }
}
```

---

## 2. Research-to-Code Handoff Contract (`research_to_code_handoff`)

When a research or analyst agent completes exploration and handoffs to a coding agent, the research artifact MUST adhere to this contract:

```json
{
  "artifact_type": "RESEARCH_TO_CODE_HANDOFF",
  "artifact_id": "art-res-001",
  "task_id": "lht-2026-0412-auth-overhaul",
  "producer_role": "researcher",
  "consumer_role": "coder",
  "architectural_constraints": [
    "Must preserve backward compatibility with /api/v1/session endpoint for 30 days",
    "Must use Web Crypto API for signing in Edge runtime"
  ],
  "target_components": [
    {
      "filepath": "src/auth/jwt.ts",
      "action": "CREATE",
      "specification": "Export verifyToken(token: string) and signToken(payload: object)"
    }
  ],
  "test_expectations": [
    "Unit test for expired token rejection",
    "Integration test verifying 401 Unauthorized header on invalid bearer token"
  ],
  "verified_evidence": [
    {
      "label": "OBSERVED",
      "statement": "Current auth uses express-session in src/server.ts",
      "source": "src/server.ts:42"
    }
  ]
}
```

---

## 3. Cross-Agent Artifact Exchange Contract (`cross_agent_artifact`)

Artifacts passed between orchestrator, researcher, coder, and analyst subagents MUST maintain provenance and integrity tracking:

```json
{
  "artifact_id": "art-code-002",
  "task_id": "lht-2026-0412-auth-overhaul",
  "producer_agent_id": "coder-agent-4",
  "consumer_agent_id": "orchestrator-main",
  "schema_version": "1.0.0",
  "checksum_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "payload_type": "CODE_DIFF_AND_VERIFICATION",
  "payload": {
    "modified_files": ["src/auth/middleware.ts"],
    "verification_status": "VERIFIED_PASSING",
    "test_command": "npm test tests/auth.test.ts",
    "test_output_summary": "12 tests passed, 0 failed"
  }
}
```

---

## 4. Failure-Resume & Recovery Semantics (`failure_resume_semantics`)

Long-horizon tasks MUST handle session drops, tool execution failures, or rate-limit interruptions without duplicating work or leaving repository state corrupted:

1. **Checkpoint Invariant**: Prior to any state mutation (file write, build execution, database modification), the agent MUST write a durable checkpoint snapshot to `.ai/tasks/<task_id>/checkpoint-<counter>.json`.
2. **Idempotent Restart**: Upon resumption after failure or session disconnect, the agent MUST inspect current git status and compare against the last verified checkpoint before resuming execution.
3. **Rollback Points**: If a subtask fails verification after 3 retry attempts, the agent MUST revert uncommitted workspace changes back to the last known healthy checkpoint.
4. **State Recovery Loop**:
   `READ CHECKPOINT → INSPECT REPOSITORY STATE → RECONCILE DIFF → RESUME SUBTASK GRAPH`

---

## 5. Long-Running Budget Controls (`budget_controls`)

Long-horizon tasks MUST enforce explicit token, session, and cost boundaries:

- **Token Thresholds**: Mandatory compaction when session active context window exceeds 75% of model max context window.
- **Session Limits**: Maximum session ceiling configured per task ID (default: 10 sessions).
- **Cost Ceilings**: Maximum USD or token expenditure limit hard-capped at orchestrator dispatch boundary.
- **Breach Protocol**: When budget limits reach 90%, the agent MUST halt subtask expansion, perform context compaction, and yield a `MAX_BUDGET_REACHED` stop condition to the user or orchestrator.

---

## 6. CHAD & LapisLLM Runtime Compatibility

### CHAD Runtime Layer
- CHAD persists long-horizon state schemas into task store directory (`.ai/tasks/` or CHAD runtime storage).
- CHAD enforces subtask graph transitions, managing subagent lifecycles and enforcing hard budget caps.
- CHAD's resume handler automatically invokes state recovery loops upon session reconnects.

### LapisLLM Model Layer
- LapisLLM's inference gateway receives context compaction directives during multi-session transitions.
- LapisLLM enforces structured output generation for artifact exchange and research-to-code handoffs.
