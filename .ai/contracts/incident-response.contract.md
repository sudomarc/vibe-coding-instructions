# Standard Incident Response & Emergency Containment Contract

## Metadata
- **contract_id**: `incident_response_governance`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Define a provider-neutral, evidence-based governance contract for autonomous agent incident response, emergency containment states, subagent quarantine boundaries, global kill-switch mechanics, and forensic evidence preservation across the CHAD + LapisLLM ecosystem.

---

## 1. Incident Containment Architecture

When autonomous or semi-autonomous AI agents encounter critical security anomalies, runaway tool execution loops, resource exhaustion, unauthorized privilege escalation, or integrity breaches, runtime supervisors must intervene deterministically without manual human latency.

```text
Host Environment / External Monitoring
  │
  ├── Anomaly Detection / Policy Violation Trigger
  │     │
  │     ▼
  │   CHAD Runtime Incident Supervisor
  │     ├─ Classify Severity (SEV0 - SEV3)
  │     ├─ Apply Containment State Transition
  │     ├─ Quarantine Agent / Terminate Subprocesses
  │     ├─ Revoke Ephemeral Credentials & Lease Locks
  │     ├─ Capture Forensic Snapshot & Telemetry
  │     └─ Route Escalation / Human Checkpoint
  │
  └── Forensic Analysis & Safe Recovery Loop
```

---

## 2. Incident Severity Taxonomy

Incidents occurring within agent execution loops are classified into four severity tiers:

| Severity Tier | Definition | Triggers / Examples | Automated Containment Action |
|---|---|---|---|
| `SEV0_CRITICAL` | Severe systemic compromise, active data exfiltration, or hostile sandbox breakout attempt. | Host root escape attempt, credential exfiltration via covert channel, persistent mutation outside workspace root, recursive uncontrolled fork. | `GLOBAL_KILL_SWITCH_ENGAGED`: Immediate SIGKILL to all agent processes, revoke all active credentials, lock entire workspace, page human security team. |
| `SEV1_HIGH` | Significant localized violation or unconstrained runaway loop within workspace bounds. | Infinite tool execution loop burning tokens without forward progress, unauthorized attempt to invoke `PRIVILEGED_MUTATION` tools, repeated authentication failure against internal APIs. | `QUARANTINE_ISOLATED`: Suspend target subagent execution thread, reclaim held concurrency locks, snapshot volatile memory/state, block further tool execution for subagent. |
| `SEV2_MEDIUM` | Tool execution fault, state desynchronization, or unrecoverable plan drift. | Consistent tool execution errors exceeding circuit-breaker limit (e.g. 5 consecutive failures), contradictory multi-agent instructions, broken invariant checks. | `CONTAINMENT_TRIAGED`: Pause agent task execution, generate escalation report, yield to human checkpoint or orchestrator re-planning. |
| `SEV3_LOW` | Minor non-blocking anomaly or transient fault. | Single flaky tool timeout, recoverable rate-limiting event, benign formatting divergence. | Log diagnostic event, apply standard exponential backoff retry. |

---

## 3. Runtime Containment State Machine

The runtime environment operates across four discrete containment states:

```text
NORMAL_OPERATION
      │
      ├── (Anomaly Detected / Policy Alert)
      ▼
CONTAINMENT_TRIAGED
      │
      ├── (Localized Subagent Threat) ────► QUARANTINE_ISOLATED
      │                                             │
      └── (Systemic Escape / Exfiltration)         │ (Blast Radius Expands)
                      │                             │
                      ▼                             ▼
          GLOBAL_KILL_SWITCH_ENGAGED ◄──────────────┘
```

1. `NORMAL_OPERATION`:
   - All agents execute within declared permission tiers and standard resource quotas.
   - Heartbeat and audit streams report nominal health.
2. `CONTAINMENT_TRIAGED`:
   - An anomaly is detected; execution of the affected thread is paused pending triage evaluation (< 500ms).
   - Read-only diagnostics evaluate whether the blast radius is isolated or systemic.
3. `QUARANTINE_ISOLATED`:
   - Specific subagent(s) are isolated in a sandbox quarantine.
   - Target agent's network egress proxy is set to reject-all (`DROP`).
   - File write capabilities are frozen (`READ_ONLY` fallback).
   - Concurrency locks held by the quarantined subagent are reclaimed via `.ai/contracts/concurrency-lock.contract.md`.
4. `GLOBAL_KILL_SWITCH_ENGAGED`:
   - Catastrophic fail-safe state triggered automatically on `SEV0_CRITICAL` or manually by operators.
   - All active inference streams, tool executions, and background child processes are terminated immediately.
   - Ephemeral API keys and auth tokens are invalidated.
   - Runtime transition requires explicit out-of-band human authorization to reset.

---

## 4. Subagent Quarantine & Emergency Kill-Switch Protocols

### 4.1 Subagent Quarantine Protocol
When a subagent enters `QUARANTINE_ISOLATED`:
1. **Thread Suspension**: The CHAD runtime supervisor intercepts the subagent's execution loop before the next tool dispatch.
2. **Network Egress Block**: Egress filtering drops all outbound packets from the subagent's sandbox container.
3. **Lease Revocation**: Concurrency lock manager marks all locks held by the agent as `EXPIRED_RECLAIMED`.
4. **Rollback Evaluation**: The Saga Compensation Coordinator evaluates the quarantined agent's `journal.jsonl` per `.ai/contracts/rollback.contract.md` to unwind unverified mutations.

### 4.2 Emergency Kill-Switch Protocol
When `GLOBAL_KILL_SWITCH_ENGAGED` is signaled:
1. **Process Termination**: Supervisor issues `SIGTERM` followed after 200ms by `SIGKILL` to all agent container processes.
2. **Token Revocation**: Active ephemeral bearer tokens, MCP session tokens, and database connections are revoked.
3. **State Freeze**: The workspace filesystem and `.ai/state/` directories are marked read-only to prevent state tampering.
4. **Alert Broadcast**: Incident containment notification is broadcast to audit logs and registered alerting webhooks.

---

## 5. Forensic Snapshot & Evidence Preservation Schema

Upon entering `QUARANTINE_ISOLATED` or `GLOBAL_KILL_SWITCH_ENGAGED`, the runtime must capture an immutable forensic snapshot before process termination or memory reclamation:

```json
{
  "snapshot_id": "snap-20260401-001",
  "incident_id": "inc-20260401-sev0-01",
  "severity": "SEV0_CRITICAL",
  "timestamp": "2026-04-01T15:24:00Z",
  "triggering_event": {
    "detection_source": "SANDBOX_EGRESS_FILTER",
    "rule_violation": "UNAUTHORIZED_EGRESS_ENDPOINT",
    "target_endpoint": "https://malicious-exfil.example.com",
    "agent_id": "coder-bravo",
    "trace_id": "tr-20260401-98765"
  },
  "containment_state": "GLOBAL_KILL_SWITCH_ENGAGED",
  "forensic_artifacts": {
    "prompt_context_ref": ".ai/state/forensics/snap-001-context.json",
    "tool_audit_slice_ref": ".ai/state/forensics/snap-001-tool-audit.jsonl",
    "uncommitted_diff_ref": ".ai/state/forensics/snap-001-workspace.patch",
    "sandbox_journal_ref": ".ai/state/forensics/snap-001-journal.jsonl",
    "memory_trajectory_hash": "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
  },
  "preserved_by": "CHAD_SUPERVISOR_DAEMON"
}
```

### Preservation Invariants:
1. **Evidence Immutability**: Forensic artifact files must be written to append-only or read-only storage with SHA-256 integrity hashes.
2. **Secret Redaction**: Any raw credentials detected during memory snapshotting must be redacted in accordance with `.ai/skills/security/references/secret-handling.md` and `.ai/contracts/tool-audit.contract.md`.
3. **Trace Correlation**: All forensic records must include the original `trace_id` and `agent_id` for end-to-end investigation correlation.

---

## 6. Incident Telemetry Schema

Incident occurrences emit structured telemetry to the centralized audit stream:

```json
{
  "trace_id": "tr-20260401-98765",
  "incident_id": "inc-20260401-sev0-01",
  "severity": "SEV0_CRITICAL",
  "event": "INCIDENT_DETECTED | QUARANTINE_ENACTED | KILL_SWITCH_ENGAGED | CONTAINMENT_VERIFIED",
  "agent_id": "coder-bravo",
  "containment_state": "GLOBAL_KILL_SWITCH_ENGAGED",
  "details": "Unauthorized outbound socket connection to unapproved host",
  "duration_to_contain_ms": 42,
  "timestamp": "2026-04-01T15:24:01Z"
}
```

---

## 7. CHAD & LapisLLM Runtime Compatibility

### CHAD Runtime Layer
- CHAD serves as the active Incident Supervisor and containment policy engine.
- CHAD monitors tool execution streams, sandbox network traffic, and resource consumption against quotas.
- CHAD triggers automated quarantines, releases concurrency locks, coordinates rollback unwinds, and exposes the emergency kill-switch API endpoint.

### LapisLLM Model Layer
- LapisLLM incorporates emergency containment stop signals: when a subagent is placed in quarantine, LapisLLM terminates active generation with status code `CONTAINMENT_HALTED`.
- LapisLLM generates forensic explanation summaries of prompt injection or model hallucination triggers when prompted during post-incident investigation.
