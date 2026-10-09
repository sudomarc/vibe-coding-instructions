# Long-Horizon Engineering Task Governance Contract

This contract establishes the provider-neutral policy, JSON schemas, state lifecycle, and verification invariants for AI agents executing multi-session, long-horizon engineering tasks within the CHAD + LapisLLM ecosystem.

---

## 1. Governance Overview & Scope

Long-horizon tasks span across multiple execution sessions, subagent delegations, context compactions, and potential session interruptions or failures. To prevent state degradation, loss of verification evidence, unconstrained token/dollar burn, and uncoordinated code mutations, all long-horizon execution loops MUST conform to this contract.

```text
Vibe Coding Instructions (.ai/contracts/long-horizon-task.contract.md)
  ├── 1. Multi-Session Task State Schema (multi_session_task_state)
  ├── 2. Research-to-Code Handoff Artifact Contract (research_to_code_handoff)
  ├── 3. Cross-Agent Artifact Exchange Schema (cross_agent_artifact)
  ├── 4. Failure-Resume Recovery Semantics (failure_resume_recovery)
  └── 5. Long-Horizon Cost & Budget Controls (cost_burn_usd)
```

---

## 2. Multi-Session Task State Schema (`multi_session_task_state`)

Every long-horizon task maintains a durable, machine-readable state checkpoint that persists across session boundaries.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MultiSessionTaskState",
  "type": "object",
  "required": [
    "task_id",
    "session_index",
    "lifecycle_stage",
    "checkpoints",
    "cumulative_metrics",
    "active_context_summary"
  ],
  "properties": {
    "task_id": {
      "type": "string",
      "description": "Unique UUID or slug identifying the overarching long-horizon task."
    },
    "session_index": {
      "type": "integer",
      "minimum": 0,
      "description": "Monotonically increasing index of the current execution session."
    },
    "lifecycle_stage": {
      "type": "string",
      "enum": [
        "RESEARCH",
        "PLANNING",
        "IMPLEMENTATION",
        "VERIFICATION",
        "COMPLETED",
        "FAILED",
        "BLOCKED"
      ]
    },
    "checkpoints": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["checkpoint_id", "timestamp", "session_index", "state_digest_hash"],
        "properties": {
          "checkpoint_id": { "type": "string" },
          "timestamp": { "type": "string", "format": "date-time" },
          "session_index": { "type": "integer" },
          "state_digest_hash": { "type": "string" },
          "git_commit_sha": { "type": ["string", "null"] },
          "handoff_ref": { "type": "string" }
        }
      }
    },
    "cumulative_metrics": {
      "type": "object",
      "required": ["total_input_tokens", "total_output_tokens", "cost_burn_usd", "tool_call_count"],
      "properties": {
        "total_input_tokens": { "type": "integer", "minimum": 0 },
        "total_output_tokens": { "type": "integer", "minimum": 0 },
        "cost_burn_usd": { "type": "number", "minimum": 0.0 },
        "tool_call_count": { "type": "integer", "minimum": 0 }
      }
    },
    "active_context_summary": {
      "type": "object",
      "required": ["objective", "verified_claims", "failed_hypotheses", "open_risks"],
      "properties": {
        "objective": { "type": "string" },
        "verified_claims": { "type": "array", "items": { "type": "string" } },
        "failed_hypotheses": { "type": "array", "items": { "type": "string" } },
        "open_risks": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

---

## 3. Research-to-Code Handoff Artifact Contract (`research_to_code_handoff`)

When a long-horizon task transitions from research/analysis to code implementation, the Researcher/Analyst agent MUST produce a validated `research_to_code_handoff` artifact before any `WORKSPACE_WRITE` tool call is authorized.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ResearchToCodeHandoff",
  "type": "object",
  "required": [
    "handoff_id",
    "task_id",
    "research_summary",
    "technical_decisions",
    "target_surfaces",
    "verification_gate_criteria"
  ],
  "properties": {
    "handoff_id": { "type": "string" },
    "task_id": { "type": "string" },
    "research_summary": { "type": "string" },
    "technical_decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["decision_id", "choice", "rationale", "rejected_alternatives"],
        "properties": {
          "decision_id": { "type": "string" },
          "choice": { "type": "string" },
          "rationale": { "type": "string" },
          "rejected_alternatives": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "target_surfaces": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["filepath", "change_type"],
        "properties": {
          "filepath": { "type": "string" },
          "change_type": { "type": "string", "enum": ["CREATE", "MODIFY", "DELETE"] }
        }
      }
    },
    "verification_gate_criteria": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["criterion_id", "verification_type", "expected_outcome"],
        "properties": {
          "criterion_id": { "type": "string" },
          "verification_type": { "type": "string", "enum": ["UNIT_TEST", "INTEGRATION_TEST", "LINT", "TYPECHECK", "BUILD", "BENCHMARK"] },
          "expected_outcome": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 4. Cross-Agent Artifact Exchange Schema (`cross_agent_artifact`)

Subagents operating in long-horizon tasks MUST exchange structured artifacts rather than raw, unparsed trajectory text.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CrossAgentArtifact",
  "type": "object",
  "required": [
    "artifact_id",
    "task_id",
    "producer_agent_id",
    "consumer_agent_id",
    "artifact_type",
    "payload_schema",
    "validation_status"
  ],
  "properties": {
    "artifact_id": { "type": "string" },
    "task_id": { "type": "string" },
    "producer_agent_id": { "type": "string" },
    "consumer_agent_id": { "type": "string" },
    "artifact_type": {
      "type": "string",
      "enum": ["RESEARCH_BRIEF", "CODE_DIFF_SPEC", "TEST_SUITE_SPEC", "POSTMORTEM_SUMMARY", "SECURITY_AUDIT_REPORT"]
    },
    "payload_schema": { "type": "object" },
    "validation_status": {
      "type": "string",
      "enum": ["PENDING_VALIDATION", "VALIDATED", "REJECTED_SCHEMA_MISMATCH", "REJECTED_UNTRUSTED"]
    }
  }
}
```

---

## 5. Failure-Resume Recovery Semantics (`failure_resume_recovery`)

When a long-horizon task encounters an unhandled exception, tool crash, or model rate limit, execution recovers gracefully using structured resumption state.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "FailureResumeRecovery",
  "type": "object",
  "required": [
    "recovery_id",
    "task_id",
    "failed_session_index",
    "checkpoint_id",
    "restoration_scope",
    "invalidated_assumptions",
    "recovery_step"
  ],
  "properties": {
    "recovery_id": { "type": "string" },
    "task_id": { "type": "string" },
    "failed_session_index": { "type": "integer" },
    "checkpoint_id": { "type": "string" },
    "restoration_scope": {
      "type": "string",
      "enum": ["LAST_STABLE_CHECKPOINT", "RESTART_CURRENT_STAGE", "ROLLBACK_TO_RESEARCH"]
    },
    "invalidated_assumptions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "recovery_step": {
      "type": "object",
      "required": ["action", "target_agent_id", "context_pruning_rule"],
      "properties": {
        "action": { "type": "string" },
        "target_agent_id": { "type": "string" },
        "context_pruning_rule": { "type": "string" }
      }
    }
  }
}
```

---

## 6. Long-Horizon Cost & Budget Controls (`cost_burn_usd`)

Long-horizon executions MUST establish strict dollar and token caps to prevent runaway context loops.

1. **Hard Cost Cap**: Every long-horizon task MUST specify `max_task_budget_usd`. When `cost_burn_usd >= max_task_budget_usd`, execution MUST pause with stop condition `MAX_BUDGET_REACHED`.
2. **Session Budget Bounds**: No single session index may consume more than 30% of `max_task_budget_usd` without an explicit Orchestrator re-authorization.
3. **Compaction Budget Threshold**: When active context window utilization reaches 80% capacity, mandatory compaction MUST occur before spawning new tool calls.
4. **L0-L4 Escalation Triggers**: Escalation to human checkpoints is required when cumulative `cost_burn_usd` exceeds 80% of budget without reaching `VERIFICATION` stage.

---

## 7. Verification Invariants

- **Invariant 1**: A new session in a long-horizon task MUST read the latest checkpoint and re-inspect repository state before executing state-changing tools.
- **Invariant 2**: Repository technical truth outranks any stale claim in a handoff artifact.
- **Invariant 3**: Failed hypotheses and failed attempts MUST NOT be purged during context compaction; they are durable state required to avoid infinite retry loops.
