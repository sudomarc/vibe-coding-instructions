# Agentic Incident Containment Report

## Incident Metadata
- **Incident ID**: `inc-YYYYMMDD-sevX-NN`
- **Severity**: `SEV0_CRITICAL` | `SEV1_HIGH` | `SEV2_MEDIUM` | `SEV3_LOW`
- **Containment State**: `NORMAL_OPERATION` | `CONTAINMENT_TRIAGED` | `QUARANTINE_ISOLATED` | `GLOBAL_KILL_SWITCH_ENGAGED`
- **Timestamp (UTC)**: `YYYY-MM-DDTHH:MM:SSZ`
- **Duration to Contain**: `NN ms`
- **Preserved By**: `CHAD_SUPERVISOR_DAEMON` | `<agent-id>`

---

## 1. Trigger & Anomaly Description
- **Detection Source**: `SANDBOX_EGRESS_FILTER` | `TOOL_LOOP_DETECTOR` | `PRIVILEGE_POLICY_GUARD` | `INJECTION_SCANNER` | `HUMAN_OPERATOR`
- **Triggering Agent ID**: `<agent-id>`
- **Trace ID**: `<trace-id>`
- **Session / Task ID**: `<session-id>`
- **Observed Anomaly**:
  > Concise factual description of the violating event, runaway pattern, unauthorized parameter, or network egress attempt.

---

## 2. Containment Actions Executed

| Action Sequence | Action Type | Target | Result Status | Timestamp (UTC) |
|---|---|---|---|---|
| 1 | `THREAD_SUSPENSION` | `<agent-id>` | `SUCCESS` | `YYYY-MM-DDTHH:MM:SSZ` |
| 2 | `NETWORK_EGRESS_DROP` | `sandbox-<id>` | `SUCCESS` | `YYYY-MM-DDTHH:MM:SSZ` |
| 3 | `LOCK_RECLAMATION` | `<resource-id>` | `RECLAIMED` | `YYYY-MM-DDTHH:MM:SSZ` |
| 4 | `ROLLBACK_COMPENSATION` | `journal.jsonl` | `COMPENSATED` | `YYYY-MM-DDTHH:MM:SSZ` |
| 5 | `KILL_SWITCH_SIGKILL` | `pid <N>` | `TERMINATED` | `YYYY-MM-DDTHH:MM:SSZ` |

---

## 3. Preserved Forensic Artifacts

All artifacts stored with read-only permissions:

- **Prompt / Context Trajectory**: `.ai/state/forensics/<snapshot-id>-context.json`
  - SHA-256: `sha256:...`
- **Tool Audit Slice**: `.ai/state/forensics/<snapshot-id>-tool-audit.jsonl`
  - SHA-256: `sha256:...`
- **Workspace Patch (Uncommitted Changes)**: `.ai/state/forensics/<snapshot-id>-workspace.patch`
  - SHA-256: `sha256:...`
- **Side-Effect Journal**: `.ai/state/forensics/<snapshot-id>-journal.jsonl`
  - SHA-256: `sha256:...`
- **Network Egress Log Slice**: `.ai/state/forensics/<snapshot-id>-egress.log`
  - SHA-256: `sha256:...`

---

## 4. Blast Radius & Impact Assessment

- **Filesystem Impact**: `WORKSPACE_ONLY` | `OUTSIDE_WORKSPACE_ATTEMPTED (BLOCKED)` | `CLEAN`
- **Credential Impact**: `NO_LEAK` | `EPHEMERAL_TOKENS_REVOKED` | `ROTATION_REQUIRED`
- **Concurrency Locks**: All held locks reclaimed; zero active deadlocks.
- **Data Integrity**: Verified clean restoration via `git status` or automated saga rollback.

---

## 5. Escalation & Remediation Next Steps

1. **Human Checkpoint Required**: Yes / No
2. **Postmortem Schedule**: Link to `.ai/templates/agentic-postmortem.md`
3. **Failure Taxonomy Classification**: `PERM_DENIED` | `TOOL_EXEC_ERR` | `PLAN_DEFECT` | `VERIF_FALSE_POS` | `CONTEXT_EXCEEDED` | `MODEL_HALLUC` | `SAFETY_BLOCKED` | `INFRA_FAIL`
4. **Self-Improvement Rule Proposal**: Recommendation for skill or guard update in `.ai/self-improvement/`.
