# Standard Long-Horizon Task & Multi-Session Governance Contract

## Metadata
- **contract_id**: `long_horizon_task_governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Establish a provider-neutral governance contract standardizing multi-session task state schemas, research-to-code handoff artifact specs, cross-agent artifact exchange protocols, failure-resume recovery semantics, and long-running cost & budget controls across the CHAD + LapisLLM ecosystem.

---

## 1. Multi-Session Task State Schema

Tasks spanning multiple agent sessions, compaction cycles, or agent boundaries MUST persist a deterministic task state snapshot conforming to the `multi_session_task_state` schema.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MultiSessionTaskState",
  "type": "object",
  "properties": {
    "task_id": { "type": "string", "description": "Unique durable task identifier" },
    "checkpoint_id": { "type": "string", "description": "Monotonically increasing checkpoint ID (e.g. chk-0042)" },
    "session_epoch": { "type": "integer", "minimum": 1, "description": "Sequential session epoch count" },
    "phase": {
      "type": "string",
      "enum": ["INIT", "RESEARCH", "SPECIFICATION", "IMPLEMENTATION", "VERIFICATION", "HANDOFF", "COMPLETED"]
    },
    "status": {
      "type": "string",
      "enum": ["ACTIVE", "PAUSED", "COMPLETED", "BLOCKED", "FAILED_RESUMABLE"]
    },
    "progress_metrics": {
      "type": "object",
      "properties": {
        "completed_subtasks": { "type": "integer" },
        "total_subtasks": { "type": "integer" },
        "percent_complete": { "type": "number", "minimum": 0, "maximum": 100 },
        "accumulated_tokens": { "type": "integer" },
        "accumulated_cost_usd": { "type": "number" }
      },
      "required": ["completed_subtasks", "total_subtasks", "percent_complete"]
    },
    "active_context_summary": { "type": "string", "description": "Concise HOT context summary for session restoration" },
    "verified_evidence_refs": {
      "type": "array",
      "items": { "type": "string" },
      "description": "References to verified tool/test evidence items"
    }
  },
  "required": ["task_id", "checkpoint_id", "session_epoch", "phase", "status", "progress_metrics", "verified_evidence_refs"]
}
```

---

## 2. Research-to-Code Handoff Artifact Contract

When a research agent or research phase transfers findings to a coding agent or implementation phase, the transfer MUST be executed via a structured `research_to_code_artifact`:

```json
{
  "artifact_type": "RESEARCH_TO_CODE_HANDOFF",
  "task_id": "task-feat-auth-001",
  "research_artifact": {
    "key_findings": [
      "OAuth2 PKCE flow required for mobile client compatibility",
      "Existing user table requires `mfa_secret` column added in migration"
    ],
    "architectural_constraints": [
      "Token expiration must not exceed 900 seconds",
      "Must remain compatible with LapisLLM model gateway auth headers"
    ],
    "acceptance_criteria": [
      "Unit test coverage for PKCE challenge validation > 95%",
      "Database migration must be reversible"
    ],
    "verified_code_locations": [
      {
        "filepath": "src/auth/provider.py",
        "description": "Primary auth handler requiring PKCE addition"
      }
    ],
    "unresolved_risks": [
      "Downstream session store cache invalidation latency under peak load"
    ]
  }
}
```

### Invariants:
1. **Zero Unverified Syntheses**: Research findings MUST reference actual inspected source paths or authoritative documentation.
2. **Explicit Constraints**: Technical constraints and non-goals MUST be explicitly enumerated before implementation starts.

---

## 3. Cross-Agent Artifact Exchange Contract

Artifacts passed between independent subagents (e.g. Orchestrator -> Coder, Coder -> Analyst) MUST follow the standard `cross_agent_artifact` exchange envelope:

```json
{
  "exchange_id": "ex-20260330-01",
  "task_id": "task-feat-auth-001",
  "producer_agent_id": "researcher-01",
  "consumer_agent_id": "coder-01",
  "artifact_type": "SPECIFICATION | CODE_DIFF | TEST_SUITE | BENCHMARK_REPORT",
  "validation_status": "UNVERIFIED | VALIDATED | REJECTED",
  "payload": {},
  "signature_hash": "sha256-abcdef1234567890..."
}
```

---

## 4. Failure-Resume Recovery Semantics

When execution aborts due to rate limits, transient infrastructure errors, or session crashes, agents MUST recover using deterministic `failure_resume_semantics`:

1. **Checkpoint Strategy**: CHAD runtime MUST serialize state snapshots after every successful phase transition or batch verification.
2. **Deterministic State Serialization**: State files (`.ai/state/task_<id>_checkpoint.json`) contain exact subtask progress, changed files list, and verified evidence references.
3. **Idempotency Bounds**: On resume, the agent MUST re-inspect repository state (`git status`, `git diff`) and assert that previously reported changes actually exist in code before proceeding.
4. **Stale Context Invalidation**: Trajectory context prior to the last verified checkpoint is discarded. The new session loads only the latest HOT checkpoint state and re-verifies repository evidence.

---

## 5. Long-Running Cost & Budget Controls

To prevent context inflation and budget blowouts in multi-day or multi-session workflows:

1. **Context Compaction Triggers**:
   - Compaction MUST trigger when active context reaches 75% of context window capacity or 10 trajectory steps without checkpoint.
   - Compaction retains only HOT context (objective, latest verified diffs, failing test logs, exact next actions) and prunes COLD trajectory.
2. **Phase Context Budgets**:
   - Research Phase: max 30% of total task token budget.
   - Implementation Phase: max 50% of total task token budget.
   - Verification Phase: max 20% of total task token budget.
3. **Retry & Idle Circuit Breakers**:
   - Maximum 3 retries per failed step.
   - Circuit breaker trips to `GOAL_BLOCKED` state after 3 consecutive unhandled step failures or zero progress in 2 consecutive epochs.

---

## 6. Ecosystem Compatibility

- **CHAD Runtime**: CHAD implements state snapshotting to local workspace storage and enforces phase token budgets via the Model Gateway.
- **LapisLLM Model Server**: LapisLLM receives serialized compact state in prompt headers and respects `max_tokens` limits across long-horizon sessions.
