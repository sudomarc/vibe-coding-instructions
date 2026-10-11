# Contract: Long-Horizon Engineering Task Governance

## Metadata
- **contract_id**: `multi_session_task_governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions
- **scope**: Multi-session engineering tasks, cross-session context persistence, research-to-code state transfer, cross-agent artifact exchange, failure recovery, and long-running cost controls.

---

## 1. Multi-Session Task State Schema

Complex engineering tasks extending across multiple sessions or agent lifecycles must maintain a durable state record conforming to this schema:

```json
{
  "task_id": "string (UUID or persistent slug)",
  "session_id": "string (current session identifier)",
  "parent_task_id": "string | null",
  "status": "NOT_STARTED | IN_PROGRESS | SUSPENDED | COMPLETED | FAILED | BLOCKED",
  "phase": "RESEARCH | SPECIFICATION | PROTOTYPE | IMPLEMENTATION | VERIFICATION | DEPLOYMENT",
  "accumulated_cost_usd": 0.00,
  "budget_cap_usd": 10.00,
  "total_tokens_consumed": {
    "input_tokens": 0,
    "output_tokens": 0,
    "reasoning_tokens": 0
  },
  "checkpoints": [
    {
      "checkpoint_id": "chk_001",
      "timestamp": "ISO-8601 UTC",
      "phase": "RESEARCH",
      "state_snapshot_hash": "sha256",
      "verified_artifacts": ["docs/arch-spec.md"],
      "open_dependencies": []
    }
  ],
  "active_agent_assignments": {
    "orchestrator_id": "orch_123",
    "active_delegates": ["coder_456", "researcher_789"]
  }
}
```

---

## 2. Research-to-Code Handoff Artifact Contract

When a research phase transitions to implementation, the research agent must produce a structured artifact ensuring no assumptions or unverified specs pass to coding agents.

```json
{
  "artifact_type": "RESEARCH_TO_CODE_HANDOFF",
  "task_id": "string",
  "research_summary": "Concise summary of validated technical approach",
  "architecture_decisions": [
    {
      "adr_id": "ADR-001",
      "decision": "Use PostgreSQL JSONB for event store",
      "rationale": "High throughput and query flexibility without extra infra dependency",
      "rejected_alternatives": ["MongoDB", "Redis"]
    }
  ],
  "verified_technical_facts": [
    {
      "statement": "API endpoint /v1/infer supports max 4096 tokens",
      "verification_source": "Tested against local mock server"
    }
  ],
  "implementation_constraints": [
    "Must preserve backward compatibility for API v1",
    "Zero additional external runtime dependencies"
  ],
  "target_file_locations": [
    "src/gateway/inference.py",
    "tests/test_inference.py"
  ]
}
```

---

## 3. Cross-Agent Artifact Exchange Schema (`cross_agent_artifact_exchange`)

Subagents operating in parallel or in sequence must exchange work through explicit, immutable artifact contracts rather than unstructured prompt text.

```json
{
  "artifact_id": "art_2026_001",
  "producer_agent_id": "researcher_01",
  "consumer_agent_id": "coder_01",
  "task_id": "task_lh_001",
  "artifact_kind": "CODE_SPEC | TEST_SUITE | BENCHMARK_RESULT | SECURITY_AUDIT",
  "payload": {},
  "verification_status": "VERIFIED_LOCAL | UNVERIFIED | FAILED",
  "created_at": "ISO-8601 UTC"
}
```

---

## 4. Failure-Resume Recovery Semantics (`failure_resume_recovery`)

When a multi-session task encounters an unexpected failure (e.g., crash, timeout, API disruption, rate limit):

1. **Failure State Isolation**: The runtime must freeze active workspace modifications and log a `FAILURE_SNAPSHOT`.
2. **Resume Checkpoint Lookup**: Upon resumption, the agent inspects the last valid `checkpoint_id` in `.ai/tasks/<task_id>/state.json`.
3. **Diff Reconciliation**: The agent computes a diff between the checkpoint `state_snapshot_hash` and the current workspace git status to identify uncommitted or partial edits.
4. **Recovery Actions**:
   - If uncommitted edits are corrupted or invalid: revert workspace to `checkpoint_id` clean state.
   - If partial edits are valid and passing tests: complete remaining batch and create a new checkpoint.

---

## 5. Context Compaction Conventions (`context_compaction`)

To prevent context window saturation during long-horizon tasks:

1. **Threshold Trigger**: Compact active context when input context exceeds 75% of the model's window or after every 10 execution steps.
2. **Preservation Policy**:
   - **MUST PRESERVE**: Objective, task_id, active phase, non-negotiable constraints, failing test logs, verified facts.
   - **MUST PRUNE**: Intermediate search outputs, redundant file reads, succeeded verbose tool outputs, stale trajectory narration.
3. **Compaction Output**: Write a structured handoff snapshot conforming to `.ai/templates/handoff.md` and clear transient conversation history.

---

## 6. Long-Running Cost & Budget Controls

1. **Hard Budget Cap**: Every multi-session task must specify `budget_cap_usd`. Exceeding this cap immediately triggers `HUMAN_CHECKPOINT_REQUIRED`.
2. **Token Burn Rate Monitoring**: Compute cost per verified milestone. If `accumulated_cost_usd` exceeds 50% without reaching the `PROTOTYPE` phase, trigger an execution efficiency review.
3. **Model Tiering for Long Tasks**:
   - Use fast/cheaper models for exploratory search and initial research filtering.
   - Escalate to high-reasoning models (e.g., Claude Sonnet / Fable) for core implementation and complex refactoring.

---

## 7. CHAD & LapisLLM Runtime Compatibility

- **CHAD Runtime**: CHAD manages persistent task state in `.ai/tasks/<task_id>/state.json` and enforces budget caps at the execution boundary.
- **LapisLLM Runtime**: LapisLLM provides stateful session token caching and structured output parsing for multi-session handoffs and recovery schemas.
