# Governance Contract: Long-Horizon Task Execution

## Metadata
- **contract_id**: `long_horizon_task`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Overview
This contract defines the governance rules, schemas, and operational boundaries for executing long-horizon, multi-session engineering tasks across CHAD and LapisLLM. It standardizes multi-session task state, durable handoffs, context compaction, research-to-code artifact exchange, failure-resume recovery semantics, and budget controls across agent boundaries.

---

## 1. Multi-Session Task State Schema

Long-horizon engineering tasks span multiple agent execution sessions. Task state must be persisted in a structured, verifiable format (`.ai/state/task-state.json` or runtime equivalent) conforming to the schema below:

```json
{
  "task_id": "lh-task-2025-0501-001",
  "version": "1.0.0",
  "objective": "High-level goal description",
  "status": "IN_PROGRESS | COMPLETED | BLOCKED | FAILED | RECOVERING",
  "created_at": "2025-05-01T10:00:00Z",
  "updated_at": "2025-05-01T12:30:00Z",
  "session_sequence": 3,
  "active_agent_id": "coder-agent-01",
  "checkpoint_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "budget": {
    "max_sessions": 10,
    "max_tokens_total": 500000,
    "tokens_consumed": 125000,
    "max_cost_usd": 15.00,
    "cost_consumed_usd": 3.75,
    "max_wall_clock_seconds": 86400
  },
  "milestone_tree": [
    {
      "milestone_id": "m1-research",
      "title": "Architecture Research & Interface Discovery",
      "status": "COMPLETED",
      "completed_in_session": 1,
      "artifacts": ["docs/architecture-proposal.md"]
    },
    {
      "milestone_id": "m2-implementation-pass-1",
      "title": "Core Module Implementation",
      "status": "IN_PROGRESS",
      "completed_in_session": null,
      "artifacts": []
    }
  ],
  "durable_state": {
    "architecture_decisions": ["ADR-001: Use provider-neutral RPC"],
    "files_modified": ["src/core/adapter.ts"],
    "verified_test_suites": ["npm test unit"],
    "failed_attempts": [
      {
        "session": 2,
        "approach": "Direct API mutation",
        "failure_reason": "Permission escalation blocked",
        "lessons": "Use sandboxed dispatcher"
      }
    ]
  }
}
```

---

## 2. Durable Task Handoff Protocol

When a session concludes, reaches context limits, or transfers execution ownership, a **Durable Task Handoff** must be created following `.ai/templates/handoff.md`.

### Mandatory Handoff Rules
1. **Durable Evidence Persistence**: All verification evidence, build logs, and test outputs must be referenced by relative file paths or stored in the task state artifact.
2. **Preservation of Failure History**: Failed attempts and lessons learned must NEVER be pruned or omitted during session handoffs.
3. **Repository Re-inspection Rule**: A resuming session MUST read the handoff artifact, but MUST re-inspect repository state before executing state-changing tools. Repository technical evidence overrides stale handoff claims.

---

## 3. Context Compaction & Pruning Conventions

Long-horizon execution requires proactive context compaction to avoid context degradation, token limits, and high costs.

### Compaction Rules
- **HOT Context**: Objective, active milestone, current file diffs, failing test output, and exact next step. Must remain in active context.
- **WARM Context**: Prior milestone outcomes, design decisions, completed file paths. Compact into structured summaries.
- **COLD Context**: Raw tool call payloads, succeeded test logs, full file contents of unmodified modules. Offload to persistent disk artifacts (`.ai/logs/` or `.ai/state/`).

### Compaction Triggers
1. **Token Utilization Threshold**: Compaction MUST occur when prompt token consumption exceeds 70% of the active context window.
2. **Milestone Completion**: Compaction MUST occur immediately after completing a milestone before commencing the next milestone.
3. **Session Boundary**: Compaction MUST precede any handoff writing.

---

## 4. Research-to-Code Handoff Protocol

When a `researcher` or `analyst` agent completes research and hands off execution to a `coder` or `orchestrator`, a structured **Research-to-Code Artifact** must be produced:

```json
{
  "artifact_type": "RESEARCH_TO_CODE_HANDOFF",
  "task_id": "lh-task-2025-0501-001",
  "research_summary": "Synthesized architectural plan and codebase analysis",
  "technical_constraints": [
    "Must maintain SemVer backwards compatibility",
    "Zero external dependency additions"
  ],
  "proposed_file_changes": [
    {
      "path": "src/adapter.ts",
      "action": "MODIFY",
      "rationale": "Implement new interface contract"
    }
  ],
  "verification_plan": [
    "Run `npm test`",
    "Execute `python3 scripts/validate_instructions.py`"
  ],
  "identified_risks": [
    "Potential breaking change if legacy parameter missing"
  ]
}
```

---

## 5. Cross-Agent Artifact Exchange Schemas

Agents operating in long-horizon workflows exchange state using standardized JSON artifact contracts saved in workspace storage (`.ai/artifacts/`):

- `RESEARCH_REPORT` — Findings, codebase topology, and dependency graphs.
- `CODE_PLAN` — Proposed diffs, component breakdown, and step-by-step implementation order.
- `VERIFICATION_REPORT` — Observed test results, coverage deltas, and performance benchmarks.
- `POSTMORTEM_INCIDENT` — Failure cascade analysis for interrupted or crashed long-horizon tasks.

---

## 6. Failure-Resume Recovery Semantics

When a long-horizon task is interrupted by session disconnect, max token exhaustion, system crash, or tool failure, execution resumes according to the **Failure-Resume Protocol**:

1. **State Integrity Validation**: Check `checkpoint_hash` against `.ai/state/task-state.json`. If hash mismatch or corrupted state is detected, roll back to the last valid milestone checkpoint.
2. **Reconciliation Pass**: Resuming agent compares persisted `durable_state.files_modified` with current Git diff/status to verify physical workspace alignment.
3. **Resume Execution Loop**:
   - Status set to `RECOVERING`.
   - Read last recorded failure or next action.
   - Execute minimal verification to confirm environment health.
   - Update status to `IN_PROGRESS` and resume active milestone.

---

## 7. Long-Running Cost & Budget Controls

To prevent runaway token burn and unbounded cost growth during multi-session execution, runtimes MUST enforce strict budget ceilings:

| Control Domain | Hard Ceiling Default | Enforcement Action |
|---|---|---|
| **Max Sessions per Task** | 10 sessions | Escalates to human checkpoint on exhaustion |
| **Max Tokens per Session** | 100,000 tokens | Triggers mandatory handoff & context compaction |
| **Max Total Task Budget** | $15.00 USD | Halts execution under `MAX_BUDGET_REACHED` |
| **Wall-Clock Timeout** | 24 hours | Marks task state as `BLOCKED` |
| **Failed Attempt Quota** | 3 consecutive failures | Triggers `GOAL_BLOCKED` and escalation report |

---

## 8. CHAD & LapisLLM Runtime Compatibility

- **CHAD Runtime**: Manages persistent state files in `.ai/state/`, executes checkpoint validation, enforces token/financial budget ceilings, and handles multi-agent session handoffs.
- **LapisLLM Model Layer**: Receives compacted task state as HOT context, respects output-token caps per session step, and enforces structured JSON generation for cross-agent artifacts.
