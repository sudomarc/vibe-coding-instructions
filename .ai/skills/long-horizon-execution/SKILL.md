# Long-Horizon Execution Skill

This skill provides operational guidance for engineering agents executing multi-session, long-horizon tasks across session boundaries, subagent handoffs, research-to-code transitions, and checkpoint recoveries.

## Scope

Applies to any engineering task that spans multiple execution sessions, requires milestone-based sub-goals, involves research-to-code handoffs, or risks exceeding context or budget limits.

---

## 1. Operating Rules for Long-Horizon Execution

1. **State Persistence First**: Always initialize or verify the task state in `.ai/state/tasks/{task_id}.json` before commencing execution.
2. **Milestone Decomposition**: Break complex tasks into 3 to 7 discrete, verifiable milestones. Never attempt an unbounded, single-session monolithic implementation.
3. **Compaction Before Checkpointing**: Compact intermediate trajectory noise (tool outputs, chat transcripts) before generating checkpoint handoffs.
4. **Re-Verify on Session Resume**: Upon resuming a task from a checkpoint, always run a lightweight verification pass to confirm workspace state before making new code changes.
5. **Enforce Budget Limits**: Monitor accumulated token and USD usage continuously. Pause and checkpoint when reaching budget boundaries.

---

## 2. Session Lifecycle Workflow

```text
START SESSION
    │
    ├── 1. Read Task State & Latest Checkpoint
    ├── 2. Re-Inspect Repository & Workspace Evidence
    ├── 3. Execute Active Milestone Step
    ├── 4. Perform Incremental Verification
    ├── 5. Compact Trajectory & Update Task State
    └── 6. Save Checkpoint or Complete Milestone
```

---

## 3. Research-to-Code Handoff Protocol

When research or analysis is required prior to code modifications:

1. **Conduct Research**: Investigate repository structure, dependencies, and design choices.
2. **Emit Handoff Artifact**: Save structured `Research-to-Code Handoff` containing architectural decisions, rejected options, targeted files, and verification criteria.
3. **Handoff Validation**: The implementing agent/session loads the research artifact, validates file targets against repository truth, and executes implementation passes.

---

## 4. Failure Recovery & Resume Semantics

If execution is interrupted due to errors, context exhaustion, or system failure:

| Failure Mode | Immediate Action | Resume Strategy |
|---|---|---|
| **Context Exhaustion** | Execute compaction pass | Load HOT context snapshot, resume active milestone |
| **Tool Execution Error** | Isolate root cause | Apply minimal repair, retry with adjusted parameters |
| **Budget Limit Reached** | Suspend execution | Save checkpoint, request budget escalation / user confirmation |
| **Unexpected Interruption** | Inspect git status | Reconcile workspace with last checkpoint commit, re-verify baseline |

---

## 5. Token Economy & Cost Optimization

- **Prompt Caching Alignment**: Ensure common system instructions and contracts are positioned at the top of context to maximize provider prompt caching across session resumes.
- **Bounded Tool Outputs**: Limit log/diff outputs during multi-session runs using pagination and targeted line filters.
- **HOT/WARM/COLD Context Layering**: Only keep active milestone context in HOT tier; archive prior milestone transcripts to COLD tier files.
