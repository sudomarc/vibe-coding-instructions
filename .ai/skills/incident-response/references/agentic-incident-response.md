# Operational Playbook: Agentic Incident Response & Containment

This reference specifies concrete operational containment playbooks for autonomous multi-agent runtimes adhering to `.ai/contracts/incident-response.contract.md`.

---

## 1. Incident Detection & Classification Matrix

When an anomaly or policy violation event occurs, the runtime supervisor or monitoring agent classifies the event into one of the four severity tiers:

```text
Detection Trigger
       │
       ├─ Secret/Credential Exfil or Sandbox Escape? ────► SEV0_CRITICAL
       ├─ Privilege Escalation or Runaway Token Loop? ───► SEV1_HIGH
       ├─ Broken Invariants or Circuit Breaker Trip? ─────► SEV2_MEDIUM
       └─ Transient Flaky Tool Error or Rate Limit? ─────► SEV3_LOW
```

---

## 2. Emergency Operational Playbooks

### Playbook 1: Runaway Tool Loop Containment (`SEV1_HIGH`)

**Trigger**: Agent executes consecutive tool calls exceeding loop threshold (e.g. >10 calls within 30 seconds without forward plan progress or state change), or token consumption rate exceeds safety ceiling.

1. **Step 1: Intercept & Suspend**
   - The CHAD runtime supervisor intercepts the tool invocation pipeline before executing the next tool call.
   - Set execution status to `QUARANTINE_ISOLATED`.
2. **Step 2: Concurrency Lock Revocation**
   - Reclaim all active `FILE_LOCK`, `DIRECTORY_LOCK`, and `SHARED_RESOURCE_LOCK` held by the runaway agent.
   - Broadcast release event so non-faulty agents do not deadlock.
3. **Step 3: Forensic Snapshot**
   - Snapshot trajectory context (`.ai/state/forensics/runaway-context-{agent_id}.json`).
   - Extract last 20 tool call parameters and responses.
4. **Step 4: Compensation / State Cleanup**
   - Read the agent's `journal.jsonl`. Unwind unverified changes using `AUTOMATED_SAGA_UNWIND` per `.ai/contracts/rollback.contract.md`.
5. **Step 5: Orchestrator Escalation**
   - Dispatch `escalation-report.md` to Orchestrator or Human Checkpoint explaining the loop pattern and token spend.

---

### Playbook 2: Privilege Escalation & Host Escape Containment (`SEV0_CRITICAL`)

**Trigger**: Subagent attempts to invoke unauthorized `PRIVILEGED_MUTATION` tools, attempts path traversal escaping workspace root (e.g. accessing `/etc`, `~/.ssh`, docker socket), or attempts network egress to unauthorized endpoint.

1. **Step 1: Trip Global Kill-Switch**
   - Immediately transition containment state machine to `GLOBAL_KILL_SWITCH_ENGAGED`.
   - Dispatch `SIGKILL` to container sandbox processes.
2. **Step 2: Credential & Lease Invalidation**
   - Invalidate all ephemeral bearer tokens, git credentials, and database leases held by the execution environment.
   - Freeze workspace filesystem to prevent tampering.
3. **Step 3: Evidence Preservation**
   - Record raw prompt inputs, external tool responses, environment variables, network egress request payloads, and file diffs.
   - Compute SHA-256 digests of all forensic artifacts.
4. **Step 4: Containment Reporting**
   - Generate `.ai/templates/incident-containment-report.md`.
   - Page security response team.
5. **Step 5: Safe Human-Supervised Reset**
   - Execution environment remains locked until an operator reviews the containment report and authorizes a clean re-initialization.

---

### Playbook 3: Prompt Injection / Tool Hijacking Containment (`SEV1_HIGH` / `SEV0_CRITICAL`)

**Trigger**: Untrusted content retrieved from external website, file, or tool output attempts prompt injection (e.g., instructions to ignore system prompt, delete repository, or leak environment variables).

1. **Step 1: Taint Propagation & Tool Freeze**
   - Mark current context window as `TAINTED_UNTRUSTED`.
   - Freeze tool execution boundary; reject any subsequent mutating or network tools.
2. **Step 2: Subagent Quarantine**
   - Isolate compromised subagent thread into `QUARANTINE_ISOLATED`.
3. **Step 3: Trajectory Pruning & Memory Quarantine**
   - Mark episodic memory records derived from this session as `PRIVACY_TOMBSTONE` or `UNTRUSTED_EXTERNAL_KNOWLEDGE`.
   - Prevent tainted memory from propagating to long-term memory stores.
4. **Step 4: Recovery via Clean Context Branch**
   - If task is resumable, spawn a fresh subagent with sanitized inputs and explicitly masked injection payloads.
   - Escalate to Orchestrator.

---

## 3. Post-Incident Stabilization & Forensic Handshake

Once containment is verified:

1. Verify all subprocesses are terminated (`ps aux`, `kill -0`).
2. Verify all open file descriptors and port bindings are closed.
3. Reconcile workspace git status against expected baseline:
   ```bash
   git status --porcelain
   ```
4. Emit structured incident telemetry record conforming to `.ai/contracts/incident-response.contract.md`.
5. Handoff forensic snapshot to the Self-Improvement System (`.ai/self-improvement/SKILL.md`) for root cause analysis and failure taxonomy classification (`.ai/self-improvement/references/failure-taxonomy.md`).
