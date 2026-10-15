# Skill: Long-Horizon Execution & Multi-Session Governance

Use this skill for engineering tasks that span multiple execution sessions, subagent handoffs, complex subtask graphs, or context compaction boundaries.

## Core Directives

1. **Durable Snapshot Invariant**: Active trajectory context in memory is volatile. Before any session transition or major state mutation, write a durable checkpoint snapshot following `.ai/templates/long-horizon-task.md`.
2. **Subtask Graph Management**: Maintain a directed subtask dependency graph. Never execute dependent subtasks until upstream dependencies reach `SUCCESS_VERIFIED` state.
3. **Compaction vs Handoff**:
   - Use **compaction** (`/compact` or trajectory pruning) to shrink context within the *same* session while preserving hot state and decision points.
   - Use a **durable handoff** when session context approaches limits, work transfers across subagents, or a failure/interruption requires session restart.
4. **Research-to-Code Protocol**: When transitioning from research/analysis to coding, enforce `.ai/contracts/long-horizon-task.contract.md` by producing a structured `RESEARCH_TO_CODE_HANDOFF` artifact before generating or modifying code.
5. **Idempotent Failure Recovery**: On session recovery, always verify repository state against the last checkpoint using `git status` and `git diff` before attempting to re-execute subtasks.

---

## Operating Loop for Long-Horizon Execution

```text
INIT TASK → BUILD SUBTASK GRAPH → CHECKPOINT STATE → EXECUTE BATCH → VERIFY BATCH → COMPACT/HANDOFF → RESUME
```

### 1. Initialization & Graph Construction
- Assign a unique `task_id` (e.g., `lht-YYYY-MMDD-<feature>`).
- Decompose task into atomic subtasks with explicit role assignments (`researcher`, `coder`, `analyst`).
- Set budget controls (`max_total_tokens`, `max_sessions`, `max_cost_usd`).

### 2. Execution & Batch Verification
- Execute subtasks in topological order.
- Collect verified evidence for each completed subtask node (`FACT`, `OBSERVED`, `VERIFIED`).
- Cross-agent artifacts must be serialized and checksummed per `.ai/contracts/long-horizon-task.contract.md`.

### 3. Checkpointing & State Recovery
- Checkpoint after every completed subtask or prior to risky system mutations:
  Save state snapshot to `.ai/tasks/<task_id>/checkpoint-<counter>.json`.
- When recovering from an unexpected exit or failure:
  1. Inspect `.ai/tasks/<task_id>/` for the latest checkpoint.
  2. Inspect workspace file diffs with `git status` and `git diff`.
  3. Reconcile workspace state with checkpoint subtask graph status.
  4. Resume execution from the first unverified node in `IN_PROGRESS` or `PENDING` status.

### 4. Context Compaction & Session Handoff
- Monitor token usage. When active context exceeds 75% capacity:
  1. Summarize verified facts, decisions, and open questions into the checkpoint snapshot.
  2. Prune raw execution logs and raw tool outputs from active context.
  3. If starting a fresh session, execute handoff transfer per `.ai/skills/context-management/SKILL.md`.

---

## Cost & Budget Controls

- **Hard Token Caps**: Set maximum cumulative token caps at dispatch. Stop execution with `MAX_BUDGET_REACHED` if cumulative spend reaches 90% without complete verification.
- **Session Limits**: Enforce maximum session count (default: 10).
- **Proactive Pruning**: Never retain unchanged file bodies or full build logs in HOT context. Convert them to concise references or summaries.

---

## Reference & Related Contracts
- Contract: `.ai/contracts/long-horizon-task.contract.md`
- Template: `.ai/templates/long-horizon-task.md`
- Context Management: `.ai/skills/context-management/SKILL.md`
- Token Economy: `.ai/skills/token-economics/SKILL.md`
