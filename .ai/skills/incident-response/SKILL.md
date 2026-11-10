---
name: incident-response
description: This skill should be used when diagnosing production incidents, outages, severe regressions, agentic cascade failures, security events, or executing emergency containment.
---

# Incident Response & Emergency Containment Skill

## When to Use

Use when diagnosing production incidents, agentic execution cascade failures, outages, severe regressions, data integrity breaches, sandbox escapes, credential leaks, or runaway token burn events.

## Architectural Boundaries

This skill operates in compliance with [.ai/contracts/incident-response.contract.md](../../contracts/incident-response.contract.md). It standardizes severity classification (`SEV0_CRITICAL` to `SEV3_LOW`), automated containment states (`CONTAINMENT_TRIAGED`, `QUARANTINE_ISOLATED`, `GLOBAL_KILL_SWITCH_ENGAGED`), subagent isolation, and forensic state preservation.

## Incident Workflow

1. **Detect & Classify**: Map the observed anomaly to a severity level (`SEV0`-`SEV3`).
2. **Execute Containment**:
   - For `SEV0` (credential leak, escape, malicious payload): Trip kill-switch (`SIG_KILL_SWITCH`), halt all dispatch, abort active model streams, and freeze sandboxes.
   - For `SEV1` (runaway burn, loop storm, tree corruption): Isolate and quarantine the offending subagent.
   - For `SEV2` (tool crash, localized deadlock): Suspend step and trigger transactional Saga unwind (`.ai/contracts/rollback.contract.md`).
3. **Capture Forensics**: Snapshot conversation trajectories, `tool-audit.contract.md` tails, Git diffs, and sanitize raw secrets before saving.
4. **Declare & Track**: Populate containment status in [.ai/templates/incident-containment-report.md](../../templates/incident-containment-report.md).
5. **Human Checkpoint Authorization**: Obtain explicit human operator credential input before lifting containment.
6. **Postmortem & Self-Improvement**: For `SEV0`/`SEV1`, conduct an agentic postmortem using [.ai/templates/agentic-postmortem.md](../../templates/agentic-postmortem.md) and file self-improvement proposals to prevent recurrence.

## Core Reference Files

- Contract: [.ai/contracts/incident-response.contract.md](../../contracts/incident-response.contract.md)
- Operational Playbook: [references/agentic-incident-response.md](references/agentic-incident-response.md)
- Incident Protocol: [references/incident-protocol.md](references/incident-protocol.md)
- Containment Template: [.ai/templates/incident-containment-report.md](../../templates/incident-containment-report.md)
- Postmortem Template: [.ai/templates/agentic-postmortem.md](../../templates/agentic-postmortem.md)
- Transactional Rollback: [.ai/contracts/rollback.contract.md](../../contracts/rollback.contract.md)
