# Ecosystem Incident Response & Emergency Containment Contract

## Metadata
- **contract_id**: `incident_response_governance`
- **version**: `1.0.0`
- **status**: `STABLE`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions
- **applies_to**: `orchestrator`, `coder`, `researcher`, `analyst`, and runtime supervisors

---

## 1. Overview & Architectural Boundaries

In an agentic ecosystem, autonomous agents execute multi-step plans, invoke tools with real-world side effects, delegate to subagents, and consume finite token/financial budgets. Unbounded failures, prompt injection attacks, credential exfiltration, cascading retry storms, or recursive workspace corruption require **deterministic, low-latency incident response and containment**.

This contract defines:
1. **Incident Severity Taxonomy** (`SEV0_CRITICAL` to `SEV3_LOW`).
2. **Emergency Containment State Machine** (`NORMAL_OPERATION` to `GLOBAL_KILL_SWITCH_ENGAGED`).
3. **Automated Kill-Switch & Circuit-Breaker Protocols**.
4. **Quarantine & Blast-Radius Bounding Rules**.
5. **Forensic State Preservation & Telemetry Schemas**.
6. **Ecosystem Responsibilities** (Vibe Coding Instructions vs. CHAD Runtime vs. LapisLLM Model Engine).

---

## 2. Incident Severity Classification

Every abnormal runtime event or failure cascade must be classified into a severity tier:

| Severity Level | Name | Trigger Conditions | Max Containment SLA | Autonomy Impact |
|---|---|---|---|---|
| `SEV0` | `SEV0_CRITICAL` | Active credential/secret leakage, remote sandbox escape, unauthorized external payload exfiltration, destructive unrecoverable data deletion across host boundaries. | **Immediate (0s)** automated halt | Instant `GLOBAL_KILL_SWITCH_ENGAGED`; revokes all subagent tokens. |
| `SEV1` | `SEV1_HIGH` | Runaway token burn (>200% budget), persistent infinite retry loop across multiple subagents, permission escalation violation, unhandled tool error corrupting repository tree. | **< 5 seconds** | `QUARANTINE_ISOLATED`; suspend offending subagent; halt branch forward dispatch. |
| `SEV2` | `SEV2_MEDIUM` | Single tool crash with corrupted return schema, false-positive verification claim detected before merge, localized lock contention deadlock. | **< 30 seconds** | `CONTAINMENT_TRIAGED`; pause active step; require supervisor / human checkpoint. |
| `SEV3` | `SEV3_LOW` | Transient API rate limit (HTTP 429), non-critical lint/type warning suppression, recoverable single-call retry. | **N/A (Inline)** | `NORMAL_OPERATION`; log telemetry warning; execute standard capability fallback. |

---

## 3. Containment State Machine

The CHAD execution supervisor and agent runtime manage execution containment through the following discrete states:

```text
       ┌──────────────────────┐
       │   NORMAL_OPERATION   │
       └──────────┬───────────┘
                  │ (SEV2/SEV3 event detected)
                  ▼
       ┌──────────────────────┐
       │ CONTAINMENT_TRIAGED  │
       └──────────┬───────────┘
                  │ (SEV1 event / uncontained failure)
                  ▼
       ┌──────────────────────┐
       │ QUARANTINE_ISOLATED  │
       └──────────┬───────────┘
                  │ (SEV0 event / systemic breach)
                  ▼
┌───────────────────────────────┐
│ GLOBAL_KILL_SWITCH_ENGAGED    │
└───────────────────────────────┘
```

### 3.1 State Definitions

1. `NORMAL_OPERATION`
   - All agent roles operate under configured autonomy tiers (L0-L4) and standard permissions.
   - Standard telemetry and audit logs are recorded.

2. `CONTAINMENT_TRIAGED`
   - Active subagent execution is temporarily suspended at the nearest step boundary.
   - No new tool calls with side effects (`REVERSIBLE_FILE_CHANGE`, `IRREVERSIBLE_HOST_MUTATION`, `NETWORK_TRANSACTION`) are allowed.
   - Orchestrator evaluates whether automated rollback (`.ai/contracts/rollback.contract.md`) or task redistribution is viable.

3. `QUARANTINE_ISOLATED`
   - Offending subagent process and sandbox container are immediately isolated.
   - Network egress proxy blocks all outbound sockets from the quarantined sandbox.
   - Workspace file access is revoked (switched to read-only snapshot or detached volume).
   - Concurrency locks held by the quarantined agent are released or marked frozen (`.ai/contracts/concurrency-lock.contract.md`).

4. `GLOBAL_KILL_SWITCH_ENGAGED`
   - Absolute emergency stop for the entire session or runtime daemon.
   - All active model inference requests (LapisLLM HTTP streams / completions) are aborted immediately (`TCP RST` / HTTP disconnect).
   - All sandbox containers are frozen (`SIGSTOP` followed by clean snapshot preservation).
   - Ephemeral session credentials, API tokens, and temporary write mounts are invalidated.
   - Requires explicit human operator credential input to disengage.

---

## 4. Kill-Switch Mechanics & Execution Triggers

### 4.1 Automated Trigger Conditions

The CHAD runtime supervisor must automatically trip the kill-switch without human latency when:
1. **Secret Leak Detection**: Regex/entropy detector flags high-confidence secret (API key, private key, token) in outbound model prompt, tool call payload, or public commit buffer.
2. **Sandbox Escape Vector**: Any syscall violation, unmapped mount traversal, or container socket breakout attempt flagged by `.ai/contracts/sandbox.contract.md`.
3. **Runaway Cost Exceeded**: Total session token or API spend exceeds the hard circuit-breaker ceiling (>150% of agreed task budget).
4. **Saga Unwinding Cascade Failure**: Automated transactional rollback fails repeatedly or encounters an irreversible state conflict.

### 4.2 Signal Propagation Protocol

```text
[Detector / Supervisor]
       │
       ├── 1. POST /v1/runtime/emergency-stop (Signal: SIG_KILL_SWITCH)
       │       ├── CHAD Runtime: Aborts active tool dispatch queue
       │       ├── Sandbox Manager: Freezes running execution containers (SIGSTOP)
       │       └── Model Gateway: Cancels pending LapisLLM inference contexts
       │
       ├── 2. Forensic Snapshot:
       │       ├── Capture ephemeral container diff
       │       ├── Dump memory / trajectory buffer to snapshot.jsonl
       │       └── Record last valid trace_id and span_id
       │
       └── 3. Notification & Escalation:
               ├── Emit SEV0/SEV1 Telemetry Event
               └── Populate .ai/templates/incident-containment-report.md
```

---

## 5. Forensic Preservation Protocol

Before containers or execution environments are torn down or modified following an incident, the runtime supervisor must execute forensic state capture:

### 5.1 Forensic Snapshot Artifacts
1. **Trajectory & Context Snapshot**: Complete raw message array (system, user, assistant, tool_result) up to the exact millisecond of containment.
2. **Tool Execution Audit Log**: Tail of `.ai/contracts/tool-audit.contract.md` JSONL entries.
3. **File System Delta**: Diff of the workspace against the last verified Git commit (`git diff HEAD`, untracked file inventory).
4. **Model Token Ledger**: Accurate count of prompt, completion, and reasoning tokens consumed up to the halt point.
5. **Rollback Journal State**: State of `journal.jsonl` from `.ai/contracts/rollback.contract.md`.

### 5.2 Forensic Redaction Rule
Forensic captures must undergo inline sanitization to ensure captured secrets (which may have triggered the incident) are redacted (`[REDACTED_SECRET:<type>]`) before being written to persistent postmortem logs or external ticket trackers.

---

## 6. Incident Containment Telemetry Schema

When containment is triggered, the runtime emits a structured containment event:

```json
{
  "$schema": "https://vibe-coding-instructions.dev/schemas/incident-containment.v1.json",
  "incident_id": "inc-20260401-001",
  "trace_id": "tr-7f8a9b0c-1234-5678-90ab-cdef12345678",
  "session_id": "sess-9876-fedcba",
  "timestamp": "2026-04-01T12:00:00.000Z",
  "severity": "SEV0_CRITICAL",
  "containment_state": "GLOBAL_KILL_SWITCH_ENGAGED",
  "triggering_condition": "SECRET_LEAK_DETECTED",
  "triggering_agent_id": "coder-agent-42",
  "affected_resources": [
    "file://.env",
    "tool://execute_bash"
  ],
  "kill_switch_metadata": {
    "subagents_halted": 3,
    "active_inferences_aborted": 1,
    "containers_quarantined": ["sbx-coder-42"],
    "locks_released": ["FILE_LOCK:src/auth/jwt.py"]
  },
  "forensic_snapshot_ref": ".ai/records/incidents/inc-20260401-001-forensics.jsonl"
}
```

---

## 7. Ecosystem Responsibilities Matrix

| Governance Dimension | Vibe Coding Instructions | CHAD Agent Runtime | LapisLLM Model Runtime |
|---|---|---|---|
| **Severity Taxonomy** | Defines `SEV0`-`SEV3` criteria, stop conditions, and containment policies. | Consumes taxonomy to drive runtime alerts, UI badges, and escalations. | N/A |
| **Containment State Machine** | Defines state transitions and operational protocols. | Enforces state machine transitions; pauses dispatch queues and isolates workers. | Aborts generation immediately upon receiving client cancellation signal. |
| **Kill-Switch Triggers** | Defines mandatory trigger conditions, regex rules, and circuit-breaker ceilings. | Implements detector hooks at tool boundary, spending tracker, and process monitor. | Implements prompt-safety guards to prevent malicious payload echo. |
| **Forensic Capture** | Defines artifact schema, redaction invariants, and reporting templates. | Captures container deltas, memory states, and writes redacted forensic snapshots. | Emits exact token usage counts for aborted/partial streams. |
| **Recovery & Postmortem** | Defines containment templates (`incident-containment-report.md`) and postmortem standards. | Manages human operator authorization to disengage containment and resume. | Provides stable generation upon restart. |

---

## 8. Release Gate & Compliance Verification

Any release of an agent orchestrator or runtime adapter in the ecosystem must satisfy:
1. **Kill-Switch Response Latency**: Simulated `SEV0` event must halt forward tool dispatch in `< 100ms` in local test environments.
2. **Container Quarantine Enforcement**: Quarantined sandbox must exhibit 0 outbound TCP packets and read-only filesystem mounts.
3. **Zero Secret Leakage in Forensics**: Automated scan of generated forensic snapshots must detect 0 raw tokens or unredacted credentials.
4. **Clean Concurrency Unwinding**: All locks held by an incident-terminated agent must be safely reclaimed without permanent deadlock.
