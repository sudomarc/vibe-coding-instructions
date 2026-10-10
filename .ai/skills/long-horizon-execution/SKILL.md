---
name: long-horizon-execution
description: Use this skill when executing complex, multi-session engineering tasks that require state persistence, research-to-code handoffs, failure recovery, context compaction, and cross-session budget governance.
---

# Long-Horizon Task Execution Skill

Use this skill when managing or executing engineering tasks that span multiple execution sessions, subagent delegates, or large multi-file code refactoring cycles.

---

## 1. Operating Loop for Long-Horizon Tasks

For any multi-session task, follow the 6-phase long-horizon execution loop:

```text
SESSION BOOTSTRAP → RECONCILE STATE → EXECUTE MILESTONE → VERIFY & CHECKPOINT → COMPACT CONTEXT → DURABLE HANDOFF
```

### Phase 1: Session Bootstrap & Reconcile
1. Read `.ai/state/task-state.json` (or active task state contract).
2. Validate `checkpoint_hash` and confirm `status`.
3. If resuming after interruption or handoff, re-inspect Git diff (`git status`) and workspace files before taking state-changing actions.
4. Set active status to `IN_PROGRESS` or `RECOVERING`.

### Phase 2: Execute Active Milestone
1. Select the current `IN_PROGRESS` milestone from the milestone tree.
2. If research is required before coding, delegate to a `researcher` or `analyst` and obtain a structured `RESEARCH_TO_CODE_HANDOFF` artifact.
3. Apply changes in small, coherent, verifiable batches.

### Phase 3: Verify & Checkpoint
1. Run local test suites and instruction validators (`python3 scripts/validate_instructions.py`).
2. Collect `VERIFIED` or `OBSERVED` evidence logs.
3. Update `.ai/state/task-state.json`: mark completed milestone, record updated `checkpoint_hash`, append newly modified files, and log failed attempts with lessons learned.

### Phase 4: Compact Context
1. Filter context into `HOT`, `WARM`, and `COLD` tiers.
2. Retain HOT context (active milestone, failing test, next step) in primary prompt.
3. Offload COLD context (large test logs, completed tool outputs) to disk storage (`.ai/logs/` or `.ai/artifacts/`).

### Phase 5: Failure Recovery (If Interrupted)
1. If a tool call fails or a session crashes, execute the **Failure-Resume Protocol**:
   - Compare Git working directory against `durable_state.files_modified`.
   - Restore clean state from last valid milestone checkpoint if corrupted.
   - Record failed attempt in `durable_state.failed_attempts`.
   - Retry with revised hypothesis or escalate if quota exceeded (3 consecutive failures).

### Phase 6: Durable Session Handoff
1. Populate `.ai/templates/handoff.md` with durable evidence references.
2. Ensure no failed attempt or lesson learned is omitted.
3. Yield execution with `PARTIAL` status if task exceeds current session budget.

---

## 2. Research-to-Code Handoff Workflow

When research or codebase analysis precedes implementation:

```text
RESEARCHER AGENT → ANALYZE REPO & DESIGN → GENERATE RESEARCH_TO_CODE_HANDOFF → CODER AGENT → RE-INSPECT CODEBASE → IMPLEMENT BATCHES
```

1. **Researcher Output**: Must contain explicit file paths, technical constraints, rationale, proposed diffs, and verification commands.
2. **Coder Ingestion**: Must re-inspect target files before modifying code. Never assume research claims reflect physical file contents without checking.

---

## 3. Cost & Token Budget Management

- **Session Token Ceiling**: When prompt token usage reaches 70% of the model context window, trigger context compaction immediately.
- **Budget Monitoring**: Track `tokens_consumed` and `cost_consumed_usd` in `.ai/state/task-state.json`.
- **Max Retry Boundary**: Limit failed attempts per milestone to 3. Upon 3 consecutive failures, halt execution, set status to `GOAL_BLOCKED`, and produce an escalation report (`.ai/templates/escalation-report.md`).
