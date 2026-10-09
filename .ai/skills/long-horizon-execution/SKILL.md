---
name: long-horizon-execution
description: Governs multi-session, long-horizon engineering tasks. Defines operational procedures for session boundary management, research-to-code artifact handoffs, context compaction triggers, failure-resume recovery semantics, and long-horizon cost & budget controls without sacrificing security or verification.
---

# Long-Horizon Execution Skill

Use this skill when managing or executing complex engineering tasks that span across multiple sessions, large trajectories, or subagent handoffs.

---

## 1. Trigger Conditions & Applicability

Activate `long-horizon-execution` when:
- The task requires changes across > 5 files or multiple distinct architectural modules.
- The estimated context footprint exceeds 50k tokens or spans multiple execution sessions.
- Execution transfers from research/analysis agents to code implementation agents.
- Session resumption occurs after an interruption, failure, or context compaction.

---

## 2. Execution Operating Protocol

```text
INITIATE TASK → PERSIST CHECKPOINT → RESEARCH-TO-CODE HANDOFF → COMPACTION/PRUNING → VERIFICATION GATE → CLOSE SESSION
```

### 2.1 Multi-Session Task State Persistence
1. Maintain `.ai/records/tasks/{task_id}/state.json` matching `.ai/contracts/long-horizon-task.contract.md`.
2. Update `session_index`, `cost_burn_usd`, and `cumulative_metrics` after every implementation pass or subagent execution loop.
3. Every checkpoint MUST contain a SHA-256 state digest hash and a pointer to the relevant Git commit or handoff reference (`handoff_ref`).

### 2.2 Research-to-Code Handoff Protocol
1. Before any `WORKSPACE_WRITE` tool is invoked, the Researcher or Analyst agent MUST generate a `research_to_code_handoff` artifact.
2. The handoff MUST explicitly state:
   - Evaluated technical options and rejected alternatives with concrete rationale.
   - Exact target file paths (`target_surfaces`).
   - Verification gate criteria (unit tests, integration tests, lint checks, type checks).
3. The Coder agent MUST inspect current repository state and verify that research assumptions remain accurate before editing code.

### 2.3 Cross-Agent Artifact Exchange
- Do NOT pass unparsed raw trajectory text or conversational history between subagents.
- Subagents MUST pass validated `cross_agent_artifact` objects containing typed payloads (`RESEARCH_BRIEF`, `CODE_DIFF_SPEC`, `TEST_SUITE_SPEC`, `POSTMORTEM_SUMMARY`).

### 2.4 Compaction & Context Pruning Rules
- **Trigger**: Perform compaction when context window usage reaches 80% capacity or before starting a major subagent delegation pass.
- **HOT Context (Preserve Exact)**: Unresolved errors, failing test logs, pending task requirements, target file diffs.
- **WARM Context (Summarize)**: Completed subtask trajectory logs, research explorations, passed test outputs.
- **COLD Context (Prune)**: Raw tool execution stdout, unedited file contents, superseded diff attempts.
- **INVARIANT**: Failed hypotheses and failed attempts MUST NOT be pruned during compaction; they are required to prevent infinite retry loops.

### 2.5 Failure-Resume & Recovery Semantics
When a session crashes, times out, or encounters an unhandled tool exception:
1. Load the latest stable `checkpoint_id` from `.ai/records/tasks/{task_id}/state.json`.
2. Construct a `failure_resume_recovery` record specifying:
   - `restoration_scope` (`LAST_STABLE_CHECKPOINT`, `RESTART_CURRENT_STAGE`, `ROLLBACK_TO_RESEARCH`).
   - `invalidated_assumptions` causing the failure.
   - Exact `recovery_step` and context pruning rule.
3. Re-inspect repository state to detect any partial or uncommitted file modifications before resuming.

---

## 3. Cost & Budget Controls (`cost_burn_usd`)

- **Task Hard Cap**: Halt execution and set stop condition `MAX_BUDGET_REACHED` if cumulative `cost_burn_usd` >= `max_task_budget_usd`.
- **Session Cap**: Single session index budget limit = 30% of total task budget.
- **Escalation Trigger**: If cumulative `cost_burn_usd` exceeds 80% of budget without reaching `VERIFICATION` stage, trigger human checkpoint for re-authorization.

---

## 4. Verification & Defense-in-Depth

- Every session resumption MUST execute a verification check (`python3 scripts/validate_instructions.py` or project test suite) to confirm baseline sanity before making new code modifications.
- Never substitute handoff claims for direct repository inspection.
