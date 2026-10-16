# Long-Horizon Engineering Task Governance Contract

**Contract Name**: `long-horizon-task`
**Version**: `1.0.0`
**Status**: `ACTIVE`
**Repository**: `vibe-coding-instructions` (`.ai/contracts/long-horizon-task.contract.md`)
**Scope**: Provider-neutral governance for engineering tasks spanning multiple sessions, subagent boundaries, context resets, or multi-phase lifecycles within CHAD and LapisLLM.

---

## 1. Overview & Objectives

Long-horizon engineering tasks exceed single context windows, require session resets, involve asynchronous subagent handoffs, or progress through distinct engineering phases (research -> design -> implementation -> verification).

This contract establishes:
1. **Multi-Session Task State Schema**: Deterministic state transitions and durable persistence schemas.
2. **Context Compaction Conventions**: Rules for bounded compaction without loss of decision-bearing facts or failure history.
3. **Research-to-Code Handoff Artifacts**: Formalized contracts for transferring research insights into executable code plans.
4. **Cross-Agent Artifact Exchange Protocol**: Schema for exchanging intermediate deliverables across heterogeneous agents.
5. **Failure-Resume Recovery Semantics**: Re-entry protocols after session terminations, context degradation, or subagent failures.
6. **Long-Running Cost & Budget Controls**: Hard and soft cost caps, token budgets, and execution circuit breakers.

---

## 2. Multi-Session Task State Schema

Every long-horizon task MUST maintain a structured, durable state snapshot stored in the workspace (e.g., `.ai/tasks/<task_id>/state.json` or `.ai/templates/long-horizon-task.md`).

### 2.1 State Lifecycle & Transitions

```text
       ┌──────────┐
       │   INIT   │
       └────┬─────┘
            │
            v
   ┌─────────────────┐
   │   RESEARCHING   │
   └────────┬────────┘
            │
            v
    ┌───────────────┐
    │   PLANNING    │
    └───────┬───────┘
            │
            v
    ┌───────────────┐      Session Reset / Interrupt
    │   EXECUTING   ├─────────────────────────────────┐
    └───────┬───────┘                                 │
            │                                         v
            v                                 ┌───────────────┐
    ┌───────────────┐  Failure Threshold      │   SUSPENDED   │
    │   VERIFYING   ├────────────────────────>│  (Resumable)  │
    └───────┬───────┘                         └───────┬───────┘
            │                                         │ Resume
            ├─────────────────────────────────────────┘
            v
    ┌───────────────┐
    │   COMPLETED   │
    └───────────────┘
            OR
    ┌───────────────┐
    │    FAILED     │
    └───────────────┘
```

### 2.2 Allowed State Transitions

| Current State | Target State | Trigger / Condition |
| :--- | :--- | :--- |
| `INIT` | `RESEARCHING` | Task initialized, context loaded, problem statement bounded. |
| `RESEARCHING` | `PLANNING` | Research evidence verified, trade-offs analyzed, architecture selected. |
| `PLANNING` | `EXECUTING` | Implementation plan approved, task batches defined, dependencies checked. |
| `EXECUTING` | `VERIFYING` | Implementation batch completed, unit/integration code modified. |
| `EXECUTING` | `SUSPENDED` | Context pressure high, session reset required, or human checkpoint hit. |
| `VERIFYING` | `EXECUTING` | Verification failed with actionable error; returning to minimal fix loop. |
| `VERIFYING` | `SUSPENDED` | Verification requires session reset or external approval. |
| `VERIFYING` | `COMPLETED` | All verification gates pass, diff reviewed, evidence documented. |
| `SUSPENDED` | `EXECUTING` / `PLANNING` | Task resumed in new session; state re-inspected against repository evidence. |
| Any Active State | `FAILED` | Irrecoverable failure, budget limit reached, or circuit breaker tripped. |

---

## 3. Context Compaction Conventions

When long-horizon execution threatens context saturation, agents MUST perform context compaction or issue a formal handoff before resetting.

### 3.1 Compaction Invariants
1. **Fact Preservation**: Objective facts (`FACT`), confirmed constraints (`VERIFIED`), and explicit architecture decisions MUST be preserved in summary form.
2. **Failure Trajectory Integrity**: Material failed attempts MUST NEVER be purged during compaction. Every failure must retain: approach, root cause, and re-consideration criteria.
3. **Evidence Precedence**: Compacted summaries serve solely as orientation; actual repository files and git diffs remain the technical source of truth.
4. **Pruning Cold Context**: Raw tool outputs, intermediate file reads, verbose logs, and unreferenced search results MUST be pruned first.

---

## 4. Research-to-Code Handoff Artifact Contract

When a research or analyst phase precedes implementation, the output MUST produce structured, machine-parsable handoff artifacts before transitioning to `PLANNING` or `EXECUTING`.

### 4.1 Required Artifact Types

1. `RESEARCH_NOTE`: Findings, source evidence, evaluated options, and trade-off matrices.
2. `ARCH_DECISION` (ADR): Selected architectural approach, rationale, rejected alternatives, and invariants.
3. `INTERFACE_SPEC`: API definitions, schema constraints, function signatures, and type boundaries.

### 4.2 Research-to-Code Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ResearchToCodeHandoff",
  "type": "object",
  "required": [
    "task_id",
    "research_summary",
    "arch_decisions",
    "interface_specs",
    "verification_criteria"
  ],
  "properties": {
    "task_id": { "type": "string" },
    "research_summary": { "type": "string" },
    "arch_decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "decision", "rationale", "rejected_alternatives"],
        "properties": {
          "id": { "type": "string" },
          "title": { "type": "string" },
          "decision": { "type": "string" },
          "rationale": { "type": "string" },
          "rejected_alternatives": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "interface_specs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["component", "spec_format", "content_ref"],
        "properties": {
          "component": { "type": "string" },
          "spec_format": { "type": "string", "enum": ["OPENAPI", "TYPESCRIPT", "PROTOBUF", "JSON_SCHEMA"] },
          "content_ref": { "type": "string" }
        }
      }
    },
    "verification_criteria": { "type": "array", "items": { "type": "string" } }
  }
}
```

---

## 5. Cross-Agent Artifact Exchange Protocol

Heterogeneous agents (e.g., `researcher` -> `architect` -> `coder` -> `analyst`) MUST exchange deliverables via immutable, schema-validated artifacts.

### 5.1 Exchange Principles
- **Immutability**: Artifacts stored in workspace state are read-only once published by an agent.
- **Traceability**: Every artifact references the originating `agent_id`, `trace_id`, and `parent_artifact_id`.
- **Integrity Check**: The receiving agent MUST validate the artifact schema and verify repository facts before execution.

---

## 6. Failure-Resume Recovery Semantics

When resuming a `SUSPENDED` or interrupted long-horizon task:

1. **State Snapshot Read**: Read the last recorded multi-session task snapshot (`.ai/templates/long-horizon-task.md` or state JSON).
2. **Repository Re-Inspection**: Immediately re-verify `git status`, changed files, and build/test status. Repository state outranks stale state snapshots.
3. **Delta Reconcile**: Identify discrepancies between snapshot state and repository reality.
4. **Failed Attempt Inspection**: Review previous failed attempts to prevent repeating failed paths.
5. **Execution Resume**: Resume execution from the explicit next action listed in the snapshot.

---

## 7. Long-Running Cost & Budget Controls

Long-horizon tasks present elevated token consumption and execution costs. Agents MUST enforce strict budget boundaries.

### 7.1 Budget & Circuit Breaker Limits

- **Token Soft Cap**: At 80% of task token budget, trigger context compaction and emit a cost alert.
- **Token Hard Cap**: At 100% of task token budget, suspend task execution, persist state snapshot, and request authorization.
- **Retry Circuit Breaker**: If the same step or test fails 3 consecutive times, force transition to `SUSPENDED` and generate an escalation report.
- **Iteration Bound**: Maximum 15 implementation/verification iterations per session without human check-in.

---

## 8. Runtime & Model Compatibility

- **CHAD Compatibility**: CHAD's orchestrator uses this contract to manage multi-session task state, schedule subagents, and enforce budget circuit breakers.
- **LapisLLM Compatibility**: LapisLLM model gateway respects state compaction signals and token caps passed in request metadata.
