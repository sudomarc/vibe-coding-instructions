# Operational Reference: Reversibility & State Compensation

This reference provides operational guidelines for autonomous agents, specialists, and orchestrators executing mutable operations within the CHAD + LapisLLM ecosystem, following `.ai/contracts/rollback.contract.md`.

---

## 1. Pre-Mutation Invariants

Before any tool call classified as `WORKSPACE_WRITE`, `ISOLATED_EXECUTE`, `NETWORK_ACCESS`, or `PRIVILEGED_MUTATION` is dispatched:

1. **Reversibility Classification**: The agent or tool runner must classify the intended action into `PURE_REVERSIBLE` (R0), `COMPENSABLE` (R1), `FORWARD_FIX_ONLY` (R2), or `IRREVERSIBLE` (R3).
2. **Snapshot Capture**:
   - For file modifications or deletions: A clean snapshot ref (`state_snapshot_ref`) or Git hash must be recorded.
   - For process spawns: The PID or lifecycle handle must be tracked with a termination command.
   - For database records: The primary keys or identifiers must be retained with a deletion/undo statement.
3. **Journal Pre-Registration**: Register the planned entry in the active Side-Effect Journal.

---

## 2. Multi-Agent Saga Pattern (LIFO Unwinding)

When a subagent reaches an abortive stop condition (`MAX_BUDGET_REACHED`, `GOAL_BLOCKED`, `SAFETY_TRIGGERED`), the Orchestrator initiates unwinding:

```text
Step 1: Write File A       ───► Compensate Step 4: Kill Process D
Step 2: Modify Config B    ───► Compensate Step 3: Delete DB Record C
Step 3: Insert DB Record C ───► Compensate Step 2: Restore Config B
Step 4: Spawn Process D    ───► Compensate Step 1: Restore File A
```

### Unwinding Protocol:
- **Order**: Strict reverse chronological order (LIFO).
- **Isolation**: Each compensation action runs in an isolated execution sandbox.
- **Evidence Verification**: After executing a compensating action, probe the target resource to confirm restoration (e.g. `read_file` to verify original content, `lsof` / `pgrep` to confirm process termination).
- **Status Update**: Mark the journal entry as `COMPENSATED` only upon verified confirmation.

---

## 3. Handling Compensation Failures

A failure during rollback is a high-severity event because the environment is in an indeterminate state.

### Rules of Engagement:
1. **Never Cascade Retries**: Do not execute recursive retries of a failing compensating action. Maximum retry = 1 with verified parameter adjustment.
2. **Immediate Freeze**: If a compensation action fails, halt automated unwinding immediately.
3. **Quarantine Resource**: Tag the resource in `.ai/contracts/concurrency-lock.contract.md` as `QUARANTINED` so other agents cannot claim or modify it.
4. **Human Escalation**: Generate a structured escalation report using `.ai/templates/escalation-report.md` detailing:
   - Tainted resource path / ID.
   - Intended state vs observed state.
   - Last executed forward action and failed compensating action.

---

## 4. Partial Rollback Mitigation

When a multi-agent plan fails partially:
- If a subagent completed an isolated sub-branch that is fully verified and decoupled from the failing subtask, the Orchestrator may elect to preserve that sub-branch while rolling back only the tainted subtask's journal entries.
- Uncommitted, unverified, or intermediate dirty state MUST ALWAYS be unwound.
