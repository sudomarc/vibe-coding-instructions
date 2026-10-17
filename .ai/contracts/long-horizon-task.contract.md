# Long-Horizon Engineering Task Contract

This contract defines the governance schema and operational rules for long-running, multi-session engineering agent tasks in the CHAD + LapisLLM ecosystem.

Long-horizon tasks span across session boundaries, agent role shifts (e.g., Research → Implementation → Verification), context compactions, and potential runtime interruptions.

---

## 1. Multi-Session Task State Schema

All long-running tasks must maintain a durable state record (`task_id`) persisted across session restarts, store compactions, and subagent handoffs.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LongHorizonTaskState",
  "type": "object",
  "required": [
    "task_id",
    "title",
    "status",
    "phase",
    "created_at",
    "updated_at",
    "session_count",
    "token_budget",
    "checkpoints",
    "active_artifacts",
    "blocked_reasons"
  ],
  "properties": {
    "task_id": {
      "type": "string",
      "pattern": "^LHT-[0-9]{4}-[0-9]{3,}$",
      "description": "Unique durable task identifier (e.g. LHT-2026-001)"
    },
    "title": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["IN_PROGRESS", "PAUSED", "COMPLETED", "FAILED", "BLOCKED", "ROLLED_BACK"]
    },
    "phase": {
      "type": "string",
      "enum": [
        "DISCOVERY_RESEARCH",
        "ARCHITECTURAL_SPECIFICATION",
        "BATCHED_IMPLEMENTATION",
        "INTEGRATION_VERIFICATION",
        "FINAL_DIFF_REVIEW"
      ]
    },
    "session_count": { "type": "integer", "minimum": 1 },
    "token_budget": {
      "type": "object",
      "required": ["allocated_tokens", "consumed_tokens", "max_cost_usd", "consumed_cost_usd"],
      "properties": {
        "allocated_tokens": { "type": "integer" },
        "consumed_tokens": { "type": "integer" },
        "max_cost_usd": { "type": "number" },
        "consumed_cost_usd": { "type": "number" }
      }
    },
    "checkpoints": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["checkpoint_id", "session_id", "timestamp", "phase", "git_sha", "verified"],
        "properties": {
          "checkpoint_id": { "type": "string" },
          "session_id": { "type": "string" },
          "timestamp": { "type": "string", "format": "date-time" },
          "phase": { "type": "string" },
          "git_sha": { "type": "string" },
          "verified": { "type": "boolean" },
          "evidence_ref": { "type": "string" }
        }
      }
    },
    "active_artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["artifact_id", "artifact_type", "path", "checksum", "producer_agent"],
        "properties": {
          "artifact_id": { "type": "string" },
          "artifact_type": {
            "type": "string",
            "enum": ["RESEARCH_DOSSIER", "ARCHITECTURE_SPEC", "IMPLEMENTATION_DIFF", "VERIFICATION_LOG"]
          },
          "path": { "type": "string" },
          "checksum": { "type": "string" },
          "producer_agent": { "type": "string" }
        }
      }
    },
    "blocked_reasons": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

---

## 2. Cross-Agent Artifact & Research-to-Code Handoff Schema

When handoff occurs across phases (specifically from Research to Implementation), raw conversational context MUST NOT be passed. Instead, a verified **Research Dossier Artifact** conforming to this contract must be produced.

### Research-to-Code Handoff Invariants
1. **Objective Evidence Requirement**: Claims in the dossier must bear explicit `FACT`, `OBSERVED`, or `VERIFIED` labels.
2. **Architecture Decoupling**: Specification artifacts must detail target files, modified interfaces, test strategies, and explicit non-goals.
3. **No Conversational Noise**: Conversational trajectory, rejected prompts, and duplicate tool logs are stripped.
4. **Immutability & Hash Verification**: Artifacts generated in phase $N$ must have an MD5/SHA256 checksum recorded in the task state before phase $N+1$ begins.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ResearchToCodeHandoffArtifact",
  "type": "object",
  "required": [
    "artifact_id",
    "task_id",
    "target_architecture",
    "verified_findings",
    "technical_constraints",
    "implementation_roadmap",
    "risk_analysis"
  ],
  "properties": {
    "artifact_id": { "type": "string" },
    "task_id": { "type": "string" },
    "target_architecture": {
      "type": "object",
      "required": ["affected_files", "new_components", "breaking_changes"],
      "properties": {
        "affected_files": { "type": "array", "items": { "type": "string" } },
        "new_components": { "type": "array", "items": { "type": "string" } },
        "breaking_changes": { "type": "boolean" }
      }
    },
    "verified_findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["label", "statement", "source"],
        "properties": {
          "label": { "type": "string", "enum": ["FACT", "OBSERVED", "VERIFIED"] },
          "statement": { "type": "string" },
          "source": { "type": "string" }
        }
      }
    },
    "technical_constraints": { "type": "array", "items": { "type": "string" } },
    "implementation_roadmap": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step", "goal", "verification_command"],
        "properties": {
          "step": { "type": "integer" },
          "goal": { "type": "string" },
          "verification_command": { "type": "string" }
        }
      }
    },
    "risk_analysis": { "type": "array", "items": { "type": "string" } }
  }
}
```

---

## 3. Failure-Resume Recovery Semantics

When a long-running session crashes, times out, or reaches budget limits, recovery must follow deterministic resumption protocols:

```text
[Crash / Disruption / Timeout]
         │
         ▼
 1. Read Task State Record (`task_id`)
         │
         ▼
 2. Verify Integrity of Last Verified Checkpoint (Git SHA + Checksum)
         │
 ┌───────┴────────────────────────┐
 │ Valid                          │ Invalid / Corrupted
 ▼                                ▼
 3a. Roll back repository to     3b. Fall back to previous checkpoint
     last verified Checkpoint Git SHA   Re-inspect workspace state
         │                                │
         └────────────────┬───────────────┘
                          │
                          ▼
                 4. Load HOT Context Only
                 (Dossier + Active Plan + Last Verified Log)
                          │
                          ▼
                 5. Resume Execution at Next Action
```

### Recovery Rules
- **Never continue from unverified state**: If a session died mid-implementation, inspect Git status. Unverified dirty changes must be stashed or reverted to the last clean checkpoint Git SHA before resumption.
- **Durable Failure Log**: Record failure taxonomy classification (`PLAN_DEFECT`, `CONTEXT_EXCEEDED`, `INFRA_FAIL`, etc.) in the task state before restarting.
- **Max Retry Threshold**: If a specific checkpoint fails to advance after 3 resumption attempts, escalate to `GOAL_BLOCKED` and trigger a human checkpoint.

---

## 4. Long-Running Cost & Token Budget Controls

Long-horizon tasks can consume extensive token budgets. Runtimes MUST enforce strict cost and token governance:

1. **Hard Token Budget Cap**: Every task declares a total budget (e.g. 5,000,000 tokens / $50 USD). Upon reaching 80% budget consumption, the system enforces **Aggressive Compaction Mode**.
2. **Phase Token Caps**: Each phase receives an allocated quota (e.g. Research: 15%, Specs: 10%, Implementation: 50%, Verification: 25%).
3. **Automatic Circuit Breaker**: If 3 consecutive implementation batches fail verification without advancing the goal, execution halts immediately with `CIRCUIT_BREAKER_TRIPPED` to preserve token budget.
4. **Context Compaction Thresholds**: Active context window MUST be compacted or transitioned into a durable handoff whenever context utilization exceeds 70% of model context capacity.
