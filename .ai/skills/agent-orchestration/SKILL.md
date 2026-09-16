---
name: agent-orchestration
description: This skill should be used when a task benefits from multiple specialized agents, parallel analysis, delegated review, or explicit agent handoffs.
---

# Agent Orchestration Skill

Use multiple agents only when decomposition creates real independent value. Keep one agent responsible for final integration. Give each delegate a narrow scope, inputs, expected output, and stop condition. Do not allow parallel agents to make overlapping writes without coordination.

Useful reviewer roles include correctness, tests, error handling, types, security, comments, and simplification. This mirrors the specialization pattern demonstrated in Anthropic's public PR review tooling while keeping the implementation repository-neutral.

References: `references/delegation.md`, `references/parallel-review.md`, `examples/delegated-review.md`.
