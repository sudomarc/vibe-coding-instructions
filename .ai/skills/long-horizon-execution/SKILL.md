---
name: long-horizon-execution
description: This skill should be used when engineering tasks span multiple agent sessions, phases, context compactions, or cross-agent handoffs in the CHAD + LapisLLM ecosystem.
---

# Long-Horizon Task Execution Skill

Use this skill when managing complex, multi-session engineering tasks that require state persistence across session boundaries, research-to-code handoffs, failure recovery, or context compaction in accordance with `.ai/contracts/long-horizon-task.contract.md`.

---

## 1. Operating Rules for Long-Horizon Tasks

When managing multi-session or long-running engineering tasks:

1. **Maintain Persistent State Manifest**:
   - Always initialize or update `.ai/artifacts/<task_id>/state.json` (conforming to `.ai/contracts/long-horizon-task.contract.md`).
   - Track active phase, current session ID, cumulative token budget, and checkpoints.
2. **Require Research-to-Code Handoff**:
   - Never begin implementation phase without a structured `research-handoff.json` produced by the Research/Analyst agent.
   - Re-verify repository source files against the handoff claims before writing new code.
3. **Execute Incremental Checkpointing**:
   - Create a checkpoint (`chk-N`) after every verified subtask or batch completion.
   - Associate each checkpoint with a git commit SHA and verified test evidence reference.
4. **Trigger Context Compaction Proactively**:
   - When active conversation context reaches 75% utilization, run context compaction.
   - Preserve primary objectives, confirmed facts (`FACT`, `VERIFIED`), rejection decisions, and remaining pending subtasks while pruning raw logs and unchanged file reads.
5. **Apply Failure-Resume Recovery**:
   - Upon starting a resumed session, read `.ai/artifacts/<task_id>/state.json`, inspect `resume_state`, and re-verify git/workspace state before taking action.

---

## 2. Workflows & Procedures

### Workflow 1: Long-Horizon Task Initialization & Lifecycle

```text
TASK RECEIVED → INITIALIZE STATE MANIFEST (.ai/artifacts/<task_id>/state.json)
              → EXECUTE PHASE 1 (RESEARCH)
              → WRITE RESEARCH HANDOFF (.ai/artifacts/<task_id>/research-handoff.json)
              → TRANSITION TO PHASE 2 (IMPLEMENTATION)
              → EXECUTE BATCH & CHECKPOINT (chk-N)
              → VERIFY & FINAL HANDOFF
```

### Workflow 2: Session Resume & Failure Recovery

```text
SESSION START → READ STATE MANIFEST & LATEST CHECKPOINT (chk-N)
              → CHECK GIT COMMIT SHA MATCHES WORKSPACE
              → INSPECT resume_state & KNOWN BLOCKERS
              → RUN FOCUSED RE-VERIFICATION PASS (tests/lint)
              → RESUME EXECUTION ON PENDING SUBTASK
```

### Workflow 3: Context Compaction Procedure

```text
CONTEXT > 75% → EXTRACT DECISION-BEARING FACTS (FACT, VERIFIED)
              → SUMMARIZE COMPLETED SUBTASKS & GIT COMMITS
              → RETAIN PENDING SUBTASKS & ACCEPTANCE CRITERIA
              → PRUNE RAW TOOL OUTPUTS & UNCHANGED FILE READS
              → COMPACT TRAJECTORY STATE
```

---

## 3. Budget & Resource Controls

- Monitor cumulative session count (`budget.max_sessions`) and token expenditure.
- Abort and trigger escalation report (`.ai/templates/escalation-report.md`) if 3 consecutive sessions fail on the same subtask (`REPEATED_PHASE_FAILURE`).
