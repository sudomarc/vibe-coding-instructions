# Standard Transactional Rollback & State Compensation Contract

## Metadata
- **contract_id**: `transactional_rollback_governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Define a provider-neutral, evidence-based governance contract for transactional rollback, state compensation workflows, reversibility classifications, append-only side-effect journaling, and saga unwinding across multi-step and multi-agent executions.

---

## 1. Reversibility Taxonomy

Every mutating tool invocation or environment alteration executed by an agent is classified into one of four reversibility tiers:

| Reversibility Tier | Description | Recovery Strategy | Human Gate Required for Rollback |
|---|---|---|---|
| `PURE_REVERSIBLE` | Direct, atomic inverse operation exists (e.g. workspace file creation/edit/deletion backed by snapshot/git). | Automated inverse execution or git revert | No |
| `COMPENSABLE` | Exact state restoration impossible, but semantical counter-action mitigates impact (e.g. deleting created cloud resource, dropping staged DB table). | Automated or supervised compensating transaction | Conditionally if impact is HIGH |
| `FORWARD_FIX_ONLY` | Action cannot be reversed or cancelled; system must advance forward with remediation patches (e.g. sent webhook, public API commit). | Forward repair batch or incident response escalation | Yes |
| `IRREVERSIBLE` | Destructive action causing permanent loss or external mutation with severe side-effects (e.g. hard purge of production DB, permanent credential revocation). | Strictly gated at invocation; manual human intervention on failure | Mandatory |

---

## 2. Append-Only Side-Effect Journaling Schema

Any mutating action executed by an agent (`WORKSPACE_WRITE`, `ISOLATED_EXECUTE`, `PRIVILEGED_MUTATION`) must be recorded in an append-only JSONL transaction journal (`journal.jsonl`) managed by the runtime:

```json
{
  "transaction_id": "tx-20250330-001",
  "step_index": 3,
  "agent_id": "coder-alpha",
  "trace_id": "tr-20250330-saga-001",
  "action_name": "write_file",
  "reversibility_tier": "PURE_REVERSIBLE | COMPENSABLE | FORWARD_FIX_ONLY | IRREVERSIBLE",
  "target_resource": "src/services/billing.ts",
  "pre_state_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "post_state_hash": "sha256:7d793037a0760186574b0282f2f435e70d18583fed6ff63f9dec3032f3161a60",
  "compensation_action": {
    "tool_name": "restore_file",
    "parameters": {
      "filepath": "src/services/billing.ts",
      "target_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  },
  "status": "COMMITTED | COMPENSATED | COMPENSATION_FAILED | UNCOMPENSABLE",
  "timestamp": "2025-03-30T12:00:00Z"
}
```

---

## 3. Saga Unwinding & Rollback Strategies

When an execution halts due to `GOAL_BLOCKED`, `SAFETY_TRIGGERED`, test failures, or uncaught execution exceptions, the runtime initiates a rollback protocol according to the registered strategy:

1. **AUTOMATED_SAGA_UNWIND**
   - **Mechanism**: The runtime iterates backwards through `journal.jsonl` in strict LIFO (Last-In, First-Out) order.
   - **Applicability**: All actions in the saga are `PURE_REVERSIBLE` or low-risk `COMPENSABLE`.
   - **Action**: Executes each `compensation_action` sequentially, validating pre-state conditions before each step.

2. **SUPERVISED_ROLLBACK_CHECKPOINT**
   - **Mechanism**: Rollback pauses when reaching a `COMPENSABLE` action with medium/high risk or a `FORWARD_FIX_ONLY` step.
   - **Action**: Presents the compensation plan, affected resources, and remaining side-effects to human supervisor (`HUMAN_CHECKPOINT_REQUIRED`).

3. **QUARANTINE_MANUAL_HOLD**
   - **Mechanism**: Triggered if a compensation action itself fails (`COMPENSATION_FAILED`) or an `IRREVERSIBLE` action was attempted.
   - **Action**: Halts all subagents, locks workspace state, preserves the transaction journal and environment state, and escalates to an incident report.

---

## 4. Compensation Verification Gates

A rollback is not considered complete merely because compensation actions were dispatched. Every compensation step requires explicit verification:

1. **State Hash Verification**:
   - For file and artifact mutations, the post-compensation hash MUST match the initial `pre_state_hash`.
2. **Environment Invariant Checks**:
   - Verification commands (e.g. `git status --porcelain`, test runner sanity, process port check) must confirm clean restoration.
3. **Evidence Record**:
   - The final rollback report must record `VERIFIED` compensation evidence for each journaled transaction.

---

## 5. Ecosystem Compatibility (CHAD & LapisLLM)

### CHAD Runtime Layer
- CHAD maintains the append-only `journal.jsonl` buffer per agent session or subtask batch.
- CHAD intercepts tool execution to capture `pre_state_hash` (or file content snapshots) before mutation occurs.
- On abort, CHAD manages LIFO saga unwinding and compensation dispatching.

### LapisLLM Model Layer
- When planning multi-step operations, LapisLLM evaluates action reversibility and includes appropriate `compensation_action` metadata in task proposals.
- When generating repair or rollback plans, LapisLLM generates compensatory actions in reverse chronological sequence to respect dependency chains.
