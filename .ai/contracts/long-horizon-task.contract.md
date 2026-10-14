# Long-Horizon Task Governance Contract

This contract defines the governance schema, artifact boundaries, failure-resume semantics, and cost controls for **long-horizon engineering agent tasks** that span multiple execution sessions, subagent handoffs, or research-to-code transitions.

## Purpose

Long-horizon tasks (such as multi-day refactoring, system migration, deep architecture research, or cross-repository integrations) exceed the single-session context boundary. This contract ensures:
1. **Durable Multi-Session State**: State survives session resets, context compaction, process terminations, or worker rotations.
2. **Deterministic Research-to-Code Handoff**: Strict contracts govern the transition from exploration/research to code modifications.
3. **Cross-Agent Artifact Exchange**: Immutable, verifiable schemas for passing artifacts between subagents.
4. **Failure-Resume Recovery**: Safe recovery protocols with state reconciliation after unexpected failures or timeouts.
5. **Long-Running Cost Controls**: Hard budget caps, token burn controls, and circuit breakers for prolonged autonomous execution.

---

## 1. Multi-Session Task State Schema

A long-horizon task MUST maintain a durable state manifest (e.g., `.ai/tasks/<task-id>/state.json` or `.ai/templates/long-horizon-task.md`).

```json
{
  "task_id": "lh-2025-05-12-auth-refactor",
  "version": "1.0.0",
  "status": "IN_PROGRESS",
  "created_at": "2025-05-12T10:00:00Z",
  "updated_at": "2025-05-12T14:30:00Z",
  "budget": {
    "max_sessions": 10,
    "current_session": 3,
    "max_total_cost_usd": 15.00,
    "consumed_cost_usd": 4.25,
    "max_token_budget": 5000000,
    "consumed_token_budget": 1420000
  },
  "phases": [
    {
      "phase_id": "phase-1-research",
      "status": "COMPLETED",
      "artifact_uri": ".ai/tasks/lh-2025-05-12-auth-refactor/artifacts/research-spec.md"
    },
    {
      "phase_id": "phase-2-implementation",
      "status": "IN_PROGRESS",
      "active_session_id": "sess-003",
      "completed_subtasks": ["schema-migration", "adapter-interface"],
      "pending_subtasks": ["token-verification-handler", "integration-tests"]
    }
  ],
  "checkpoint": {
    "last_verified_git_commit": "a1b2c3d4e5f6",
    "working_branch": "feat/lh-auth-refactor",
    "dirty_files": ["src/auth/jwt.ts"],
    "open_risks": ["token expiration race condition in background refresh"]
  }
}
```

### State Properties
- **Durable Identity**: `task_id` is invariant across all sessions.
- **Monotonic Session Count**: `current_session` increments deterministically upon each session initialization/resume.
- **Checkpoint Verifiability**: `last_verified_git_commit` must point to an actual commit verified by automated tests.

---

## 2. Research-to-Code Handoff Contract

Transitioning from a research/analyst role to a coding role MUST produce a formal **Research-to-Code Handoff Artifact** before any repository mutation begins.

### Required Handoff Fields
1. **Target Outcome & Non-Goals**: Clear boundary of what the code change will and will NOT touch.
2. **Verified Technical Hypotheses**: Architectural decisions backed by file evidence, line references, or spike results.
3. **Target File Plan**: Explicit list of files to add, modify, or delete.
4. **Acceptance Criteria & Verification Plan**: Exact commands (`pytest`, `npm test`, `python scripts/validate.py`) required to validate success.
5. **Architectural Invariants**: Hard rules that must not be broken during coding.

---

## 3. Cross-Agent Artifact Exchange Protocol

Artifacts exchanged between agents (e.g. Researcher → Coder → Analyst) MUST satisfy the following rules:
- **Immutability**: Once an artifact is written to `.ai/tasks/<task-id>/artifacts/`, it MUST NOT be edited in place. Revisions generate a new versioned file (e.g., `research-spec-v2.md`).
- **Cryptographic/Hash Verification**: Artifacts should include an SHA-256 digest or Git blob ID when referenced in task state.
- **Trust Labeling**: Every artifact MUST bear trust metadata:
  - `VERIFIED_INTERNAL`: Produced and verified by internal agent tools.
  - `UNTRUSTED_EXTERNAL`: Containing unverified web search, external API, or third-party code context.

---

## 4. Failure-Resume Recovery Semantics

When a session terminates unexpectedly (context overflow, process crash, API timeout, or tool error), the recovery agent MUST execute the **Reconciliation Protocol**:

```text
CRASH/DISRUPTION -> READ STATE MANIFEST -> RE-INSPECT GIT REPOSITORY -> RECONCILE DIFFERENCE -> SET RESUME SESSION -> CONTINUE
```

### Recovery Protocol Steps
1. **Read Manifest**: Retrieve `state.json` or task handoff document.
2. **Re-Inspect Environment**: Execute `git status`, `git diff`, and test suites to assess actual repository state vs manifest state.
3. **Reconcile State**:
   - If uncommitted changes exist that pass tests: Commit or stash cleanly before proceeding.
   - If uncommitted changes fail tests: Revert dirty files to `last_verified_git_commit` or fix immediate syntax errors.
4. **Log Incident**: Record recovery event in the task incident log (`.ai/tasks/<task-id>/incidents.log`).
5. **Resume Execution**: Initialize new session with updated context snapshot.

---

## 5. Long-Running Cost & Token Controls

Long-horizon tasks present compound cost and context exhaustion risks. Agents operating under this contract MUST observe these hard bounds:

1. **Session Token Cap**: Single session budget MUST NOT exceed configured threshold without explicit user checkpoint approval.
2. **Compaction Circuit Breaker**: When context length reaches 75% of model limits, the agent MUST issue a context compaction/handoff pass before executing further complex tools.
3. **Retry Exhaustion Rule**: Maximum 3 consecutive failed tool executions or test failures on the same hypothesis before triggering a human checkpoint escalation (`L2_CHECKPOINT`).
4. **Cumulative Budget Cap**: Execution halts immediately if cumulative task spend reaches `max_total_cost_usd`.

---

## CHAD & LapisLLM Runtime Compatibility

- **CHAD Agent Runtime**: Consumes this contract to manage persistent task state in `.ai/tasks/` or CHAD's native state store, enforcing budget caps and human checkpoint triggers.
- **LapisLLM Inference Gateway**: Benefits from predictable context compaction and structured state snapshots, optimizing prompt caching efficiency across multi-session trajectories.
