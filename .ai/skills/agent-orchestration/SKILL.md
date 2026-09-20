---
name: agent-orchestration
description: This skill should be used when a task benefits from multiple specialized agents, parallel analysis, delegated review, or explicit agent handoffs.
---

# Agent Orchestration Skill

Use multiple agents only when decomposition creates real independent value. Keep one agent responsible for final integration. Give each delegate a narrow scope, inputs, expected output, and stop condition. Do not allow parallel agents to make overlapping writes without coordination.

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

## Delegation contract

Every delegate receives role, exact scope, relevant files or diff, required inputs, output format, permissions, and stop condition. Run independent read-only reviews in parallel only when the host can isolate them safely. The primary agent remains responsible for final integration.

For external integrations, give the reviewer the actual provider paths, capability contract, health evidence, authentication boundary and fallback behavior under review. Do not ask a reviewer to infer provider health from names or documentation alone.

Useful reviewer roles include correctness, tests, error handling, types, security, comments, simplification, visual fidelity, performance, provider health and capability routing. Specialization should reduce context load, not create unnecessary ceremony.

References: `references/delegation.md`, `references/parallel-review.md`, `examples/delegated-review.md`.
