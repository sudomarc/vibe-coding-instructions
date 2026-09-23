---
name: agent-orchestration
description: This skill should be used when a task benefits from multiple specialized agents, parallel analysis, delegated review, explicit agent handoffs, bounded autonomy gating, or multi-agent failure escalation.
---

# Agent Orchestration Skill

Use multiple agents only when decomposition creates real independent value. Keep one orchestrator agent responsible for overall plan execution and final integration. Give each delegate a narrow scope, context inputs, expected output format, permission tier, and stop condition. Do not allow parallel agents to make overlapping writes without coordination.

## Routing

- Visual redesign: `ui-reviewer` + `visual-qa`
- Responsive layout: `responsive-reviewer` + `visual-qa`
- Advanced motion or browser 3D: `motion-3d-specialist` + `visual-qa` + `performance-auditor`
- Asset-heavy visual change: `asset-pipeline-specialist` + `performance-auditor`
- Screenshot baselines or visual regression: `visual-regression-reviewer` + `browser-tester`
- Accessibility-sensitive UI: `accessibility-reviewer`
- Forms or auth: `forms-ux-reviewer` + `accessibility-reviewer` + `browser-tester`
- Shared components: `component-reviewer` + `ui-reviewer`
- Next.js rendering or cache behavior: `nextjs-specialist` + `performance-auditor`
- Public/indexable pages: `seo-auditor` + `performance-auditor`
- Browser-facing security: `web-security-reviewer`
- External CLIs, MCPs, SaaS providers or multi-backend integrations: `integration-health-reviewer` + `security` or `provider-integration` specialist as relevant

## Delegation Economics

Delegation is justified only when independent analysis, context isolation, or parallelism creates net value after accounting for the delegated prompt, context, tool calls, and returned output. Prefer one primary owner plus narrow read-only reviewers. Do not delegate work that simply rereads the same evidence without independent value.

## Delegation Contract & Bounded Autonomy

Every delegate receives role, exact scope, relevant files or diff, required inputs, output format, permission tier (`READ_ONLY`, `WORKSPACE_WRITE`, `ISOLATED_EXECUTE`, `NETWORK_ACCESS`, `PRIVILEGED_MUTATION`), and stop condition.

- **Bounded Autonomy Tiers**: Operate strictly within granted autonomy tiers (L0 `READ_ONLY` to L4 `RESTRICTED`).
- **Human Checkpoints**: Immediately pause and transition to `HUMAN_CHECKPOINT_REQUIRED` state upon requesting `PRIVILEGED_MUTATION`, breaching >=80% budget, performing irreversible state changes, or encountering contradictory goal states (`GOAL_BLOCKED`).
- **Retry & Circuit Breaker**: Enforce a maximum of 3 retries per failed step with required context changes. Activate circuit breaker on 3 consecutive identical tool/model errors.
- **Traceability**: Propagate `trace_id` and `parent_agent_id` across all inter-agent communications and tool invocations.

## Failure Escalation Protocol

When a subagent reaches a stop condition other than `SUCCESS_VERIFIED` (such as `GOAL_BLOCKED`, `MAX_BUDGET_REACHED`, or `SAFETY_TRIGGERED`), it escalates execution back to the Orchestrator with structured diagnostic evidence. If the Orchestrator cannot safely resolve or replan the task, it formats an Escalation Report (`.ai/templates/escalation-report.md`) and requests a human checkpoint.

References:
- `references/delegation.md`
- `references/parallel-review.md`
- `references/bounded-autonomy-escalation.md`
- `.ai/templates/escalation-report.md`
- `examples/delegated-review.md`
