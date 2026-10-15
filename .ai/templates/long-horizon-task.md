# Long-Horizon Task State & Handoff Template

Use this template to persist state snapshots for long-horizon engineering tasks across session boundaries, subagent handoffs, and context compactions.

---

```json
{
  "task_id": "lht-YYYY-MMDD-<short-description>",
  "session_id": "<current-session-id>",
  "checkpoint_counter": 1,
  "status": "IN_PROGRESS",
  "created_at": "<ISO-8601 UTC Timestamp>",
  "updated_at": "<ISO-8601 UTC Timestamp>",
  "objective": "<High-level target objective>",
  "subtask_graph": {
    "nodes": [
      {
        "subtask_id": "st-001",
        "title": "<Subtask description>",
        "assigned_role": "orchestrator | researcher | coder | analyst",
        "status": "PENDING | IN_PROGRESS | COMPLETED | BLOCKED | FAILED",
        "dependencies": [],
        "artifact_id": "art-001"
      }
    ]
  },
  "research_to_code_handoff": {
    "architectural_constraints": [
      "<Constraint 1>",
      "<Constraint 2>"
    ],
    "target_components": [
      {
        "filepath": "<relative/path/to/file>",
        "action": "CREATE | MODIFY | DELETE",
        "specification": "<Summary of intended changes>"
      }
    ],
    "test_expectations": [
      "<Test scenario 1>",
      "<Test scenario 2>"
    ]
  },
  "cross_agent_artifacts": [
    {
      "artifact_id": "art-001",
      "producer_role": "researcher",
      "consumer_role": "coder",
      "checksum_sha256": "<sha256>",
      "summary": "<Summary of artifact payload>"
    }
  ],
  "active_context_window": {
    "hot_files": [
      "<Path to file currently being edited>"
    ],
    "verified_facts": [
      "<Fact 1 verified by test or file inspection>"
    ],
    "open_questions": [
      "<Unresolved question>"
    ]
  },
  "budget_controls": {
    "max_total_tokens": 5000000,
    "consumed_tokens": 0,
    "max_sessions": 10,
    "consumed_sessions": 1,
    "max_cost_usd": 10.00,
    "consumed_cost_usd": 0.00
  },
  "verification_evidence": [
    {
      "label": "VERIFIED",
      "statement": "<Passing test or benchmark output>",
      "source": "<Command or test file>"
    }
  ],
  "failure_recovery": {
    "last_healthy_checkpoint": "checkpoint-0.json",
    "uncommitted_files": [],
    "retry_count": 0
  }
}
```
