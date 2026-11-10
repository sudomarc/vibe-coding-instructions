# Incident Containment Report

> **Incident ID:** `inc-YYYYMMDD-xxx`
> **Trace ID:** `tr-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
> **Session ID:** `sess-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
> **Declaration Timestamp (UTC):** `YYYY-MM-DDTHH:MM:SSZ`
> **Severity Tier:** `SEV0_CRITICAL` | `SEV1_HIGH` | `SEV2_MEDIUM` | `SEV3_LOW`
> **Current Containment State:** `NORMAL_OPERATION` | `CONTAINMENT_TRIAGED` | `QUARANTINE_ISOLATED` | `GLOBAL_KILL_SWITCH_ENGAGED`

---

## 1. Incident Overview & Signal

- **Incident Summary:** {Concise 1-2 sentence description of the abnormal event or security boundary trip}
- **Triggering Condition:** `SECRET_LEAK_DETECTED` | `SANDBOX_ESCAPE_ATTEMPT` | `RUNAWAY_TOKEN_BURN` | `UNAUTHORIZED_EGRESS` | `TREE_CORRUPTION` | `VERIF_FALSE_POSITIVE`
- **Originating Agent / Process:** `{agent_id}` (`{role_id}`)
- **Affected Sandbox / Workspace:** `{sandbox_container_id}` / `{target_directory}`

---

## 2. Containment Execution Status

| Containment Action | Executed? | Timestamp (UTC) | Verification Evidence |
|---|---|---|---|
| **Forward Dispatch Halted** | `YES` / `NO` | `HH:MM:SS` | `VERIFIED`: Tool execution queue paused |
| **Model Stream Cancelled** | `YES` / `NO` / `N/A` | `HH:MM:SS` | `VERIFIED`: LapisLLM HTTP stream aborted |
| **Container Quarantined / Frozen** | `YES` / `NO` / `N/A` | `HH:MM:SS` | `VERIFIED`: Container signaled SIGSTOP, egress blocked |
| **Concurrency Locks Reclaimed** | `YES` / `NO` | `HH:MM:SS` | `VERIFIED`: Locks released or transitioned to frozen |
| **Session Credentials Revoked** | `YES` / `NO` / `N/A` | `HH:MM:SS` | `VERIFIED`: Ephemeral tokens invalidated |

---

## 3. Forensic Preservation Summary

- **Forensic Snapshot Path:** `.ai/records/incidents/inc-YYYYMMDD-xxx-forensics.jsonl`
- **Trajectory Capture Completed:** `YES` / `NO`
- **Tool Audit Tail Captured:** `YES` / `NO` (Entries: `{count}`)
- **Workspace Delta Snapshot:** `YES` / `NO` (`{diff_file_count}` files modified)
- **Zero Secrets in Forensics Verified:** `YES` / `NO` (`VERIFIED`: Sanitizer confirmed 0 raw secrets)

---

## 4. Blast-Radius Assessment & Immediate Impact

- **Filesystem Impact:** {Local branch only / Ephemeral build dir / Destructive modifications detected}
- **Cost / Token Delta:** {Actual tokens consumed: Input: `x`, Output: `y`, Reasoning: `z`}
- **Remote / Network Exposure:** {None / Blocked at proxy / External request observed}

---

## 5. Next Actions & Recovery Path

1. **Compensating Rollback:** {Execute Saga unwind via `journal.jsonl` / Manual branch reset}
2. **Human Checkpoint Required:** `YES` (Operator approval required to clear containment)
3. **Postmortem Scheduled:** {For SEV0/SEV1: Populate `.ai/templates/agentic-postmortem.md`}
