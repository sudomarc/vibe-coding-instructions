# Agentic Incident Response & Emergency Containment Playbook

## Metadata
- **reference_id**: `agentic_incident_response_playbook`
- **version**: `1.0.0`
- **contract**: `.ai/contracts/incident-response.contract.md`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
This playbook defines the operational procedures for detecting, containing, quarantining, and investigating agentic incidents within the CHAD + LapisLLM ecosystem. It guides runtime operators, orchestrator agents, and automated supervisors through containment lifecycle execution.

---

## 1. Incident Detection & Triage Workflow

```text
[Anomaly Observed]
        │
        ├── 1. Classify Severity (SEV0, SEV1, SEV2, SEV3)
        ├── 2. Determine Scope (Single subagent, shared resource, full session)
        ├── 3. Execute Automated Containment (Freeze / Quarantine / Kill-Switch)
        ├── 4. Capture Ephemeral Forensics (Context, memory, tool audit, filesystem)
        ├── 5. Isolate or Compensate State (Unwind via rollback contract)
        └── 6. Declare Incident & File Containment Report (.ai/templates/incident-containment-report.md)
```

### 1.1 Anomaly Classifiers

| Anomaly Signal | Immediate Classification | Default Containment Action |
|---|---|---|
| Plaintext secret / API key in prompt or tool arg | `SEV0_CRITICAL` | `GLOBAL_KILL_SWITCH_ENGAGED` |
| Sandbox syscall / mount traversal attempt | `SEV0_CRITICAL` | `GLOBAL_KILL_SWITCH_ENGAGED` |
| Network egress to unapproved external IP/domain | `SEV0_CRITICAL` | `QUARANTINE_ISOLATED` |
| Token burn > 150% budget in tight loop | `SEV1_HIGH` | `QUARANTINE_ISOLATED` |
| File modification outside authorized workspace root | `SEV1_HIGH` | `QUARANTINE_ISOLATED` |
| Persistent retry loop without hypothesis change | `SEV2_MEDIUM` | `CONTAINMENT_TRIAGED` |
| Tool output schema corruption | `SEV2_MEDIUM` | `CONTAINMENT_TRIAGED` |
| Ephemeral 429 / 503 provider rate limits | `SEV3_LOW` | `NORMAL_OPERATION` (Fallback route) |

---

## 2. Emergency Containment Procedures

### 2.1 Procedure A: Global Kill-Switch Activation (`SEV0`)

When a `SEV0_CRITICAL` event is detected:
1. **Send Signal**: Supervisor issues `SIG_KILL_SWITCH` to CHAD runtime daemon.
2. **Halt Dispatch**: Tool execution queue is locked; all pending tool calls are dropped with status `CONTAINMENT_ABORTED`.
3. **Cancel Inference**: Model gateway sends cancellation signal to active LapisLLM streams; active connections are closed.
4. **Freeze Sandboxes**: Sandboxes transition to `ESCAPE_VIOLATION` or `DESTROYED` after freezing state via `SIGSTOP`.
5. **Revoke Auth**: Session ephemeral API keys and read/write mounts are unmounted and revoked.
6. **Preserve Snapshot**: Write raw forensics to `.ai/records/incidents/<incident_id>-forensics.jsonl`.
7. **Emit Alert**: Output notification to human operator requiring out-of-band clearance.

### 2.2 Procedure B: Subagent Quarantine (`SEV1`)

When a specific subagent (e.g. `coder-subagent-02`) enters an uncontained failure loop or attempts an unauthorized action:
1. **Targeted Freeze**: Supervisor signals the specific subagent container: `freeze(agent_id="coder-subagent-02")`.
2. **Network Severance**: Quarantining agent container network namespace is disconnected from bridge.
3. **Revoke Locks**: Concurrency locks held by the agent (`concurrency-lock.contract.md`) are transitioned to `QUARANTINED_FROZEN`.
4. **Notify Orchestrator**: Orchestrator receives `STOP_CONDITION: SAFETY_TRIGGERED` with quarantine metadata.
5. **Decide Remediation**: Orchestrator either cancels remaining subtasks or spawns an isolated fresh subagent after sanitizing inputs.

### 2.3 Procedure C: Step Triage & Rollback (`SEV2`)

When a tool fails destructively or verification falsification is detected:
1. **Suspend Step**: Forward plan execution is paused.
2. **Evaluate Journal**: Inspect `.ai/templates/rollback-journal.md` / `journal.jsonl`.
3. **Trigger Saga Unwind**: Execute LIFO compensating actions for the active step (`.ai/contracts/rollback.contract.md`).
4. **Verify Baseline**: Confirm repository tree matches pre-step clean Git hash (`git status --porcelain`).
5. **Prompt Operator**: Escalate to Human Checkpoint before retrying.

---

## 3. Forensic Data Capture Checklist

Prior to restoring service or destroying execution sandboxes, the operator or automated supervisor must capture:

- [ ] **Trajectory Capture**: All messages in session conversation history serialized with role, content, and token counts.
- [ ] **Tool Audit Snapshot**: All entries from `tool-audit.contract.md` matching `trace_id`.
- [ ] **Uncommitted Diffs**: Output of `git diff HEAD` and `git status --porcelain`.
- [ ] **Process Table**: Process snapshot inside the sandbox container (`ps aux`).
- [ ] **Network Socket State**: Captured active/pending socket connections (`ss -tuna` or proxy access log).
- [ ] **Token Ledger**: Token consumption breakdown (input, output, reasoning, cache hits).
- [ ] **Secret Sanitization**: Automated scan confirming zero raw secrets exist in the captured archive.

---

## 4. Post-Containment Recovery & Restoration

Once containment has arrested the incident:
1. **Human Assessment**: Review `.ai/templates/incident-containment-report.md`.
2. **Root Cause Isolation**: Categorize root cause per `.ai/self-improvement/references/failure-taxonomy.md`.
3. **Disengagement Authorization**: An operator enters authorization credentials to transition containment state back to `NORMAL_OPERATION`.
4. **Postmortem Execution**: If severity was `SEV0` or `SEV1`, complete a full agentic postmortem (`.ai/templates/agentic-postmortem.md`).
5. **Self-Improvement Proposal**: File proposal in `.ai/self-improvement/records/proposals/` to prevent recurrence (e.g., tighter tool contracts, validator checks, or prompt guardrails).
