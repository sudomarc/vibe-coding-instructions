---
name: incident-response
description: This skill should be used when diagnosing production incidents, outages, severe regressions, data integrity problems, agent runaway loops, sandbox breakouts, or security events.
---

# Incident Response Skill

Prioritize stabilization and evidence preservation. Establish impact, timeline, current state, and safe containment. Avoid speculative broad changes during an active incident. Preserve logs and relevant identifiers without exposing secrets. After stabilization, identify root cause, corrective action, regression tests, and follow-up work.

For autonomous agent anomalies, runaway execution loops, privilege violations, or security events, follow the emergency containment protocols defined in `.ai/contracts/incident-response.contract.md` and `references/agentic-incident-response.md`.

## Key Protocols
- General Incident Protocol: `references/incident-protocol.md`
- Agentic Containment & Quarantine Playbooks: `references/agentic-incident-response.md`
- Governance Contract: `.ai/contracts/incident-response.contract.md`
- Incident Containment Template: `.ai/templates/incident-containment-report.md`
