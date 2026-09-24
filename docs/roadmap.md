# Vibe Coding Instructions roadmap

The framework is evolving from a coding-agent instruction library into a **general engineering-agent governance framework** that can provide reusable policy to systems such as CHAD.

## Phase 0 — Core governance [current]

- [x] Evidence-driven operating loop.
- [x] Instruction precedence.
- [x] Repository inspection rules.
- [x] Verification discipline.
- [x] Token economy invariant.
- [x] Security/safety constraints.
- [x] Controlled self-improvement.
- [x] Provider-neutral integration guidance.

## Phase 1 — Agent-role contracts [completed]

- [x] Orchestrator role contract (`.ai/contracts/orchestrator.contract.md`).
- [x] Researcher role contract (`.ai/contracts/researcher.contract.md`).
- [x] Coder role contract (`.ai/contracts/coder.contract.md`).
- [x] Analyst role contract (`.ai/contracts/analyst.contract.md`).
- [x] Shared handoff schema (`.ai/contracts/README.md`).
- [x] Shared evidence schema (`.ai/contracts/README.md`).
- [x] Stop-condition conventions (`.ai/contracts/README.md`).
- [x] Permission-level vocabulary (`.ai/contracts/README.md`).
- [x] Runtime-neutral role examples (`.ai/contracts/`).

## Phase 2 — Agent orchestration governance [completed]

- [x] Delegation policy (`.ai/skills/agent-orchestration/references/delegation.md`).
- [x] Parallelism policy (`.ai/skills/agent-orchestration/references/parallel-review.md`).
- [x] Retry/loop policy (`.ai/skills/agent-orchestration/references/bounded-autonomy-escalation.md`).
- [x] Bounded autonomy policy (`.ai/skills/agent-orchestration/references/bounded-autonomy-escalation.md`).
- [x] Human checkpoint policy (`.ai/skills/agent-orchestration/references/bounded-autonomy-escalation.md`).
- [x] Failure escalation rules (`.ai/skills/agent-orchestration/references/bounded-autonomy-escalation.md`).
- [x] Agent identity and correlation guidance (`.ai/skills/agent-orchestration/references/bounded-autonomy-escalation.md`).
- [x] Multi-agent audit conventions (`.ai/skills/agent-orchestration/references/bounded-autonomy-escalation.md`).

## Phase 3 — Tool governance

- [x] Standard tool contract (`.ai/contracts/tool.contract.md`).
- [x] Tool permission taxonomy (`.ai/contracts/tool.contract.md`).
- [x] Side-effect classification (`.ai/contracts/tool.contract.md`).
- [x] Tool result trust labeling (`.ai/contracts/tool.contract.md`).
- [ ] External content/prompt-injection guidance.
- [ ] Sandbox requirements.
- [ ] Tool audit-log conventions.
- [ ] Capability/fallback templates.

## Phase 4 — Context, memory and knowledge governance

- [ ] Context composition policy.
- [ ] Memory write policy.
- [ ] Memory deletion semantics.
- [ ] Retrieval evidence contract.
- [ ] Knowledge-source provenance contract.
- [ ] Long-running task compaction policy.

## Phase 5 — Model/provider governance

- [ ] Provider-neutral model capability schema.
- [ ] Routing-policy guidance.
- [ ] Provider health-state definitions.
- [ ] Fallback semantics.
- [ ] Cost/latency/privacy routing guidance.
- [ ] Model evaluation reporting format.
- [ ] Contract-testing guidance for model backends.

## Phase 6 — Agent security

- [ ] Prompt-injection threat model.
- [ ] Tool-confusion threat model.
- [ ] Data-exfiltration patterns.
- [ ] Permission escalation controls.
- [ ] Sandbox escape test guidance.
- [ ] Secret-handling guidance for agent runtimes.
- [ ] Security review playbooks.

## Phase 7 — Evaluation and observability

- [ ] Agent-task benchmark format.
- [ ] Tool-call reliability metrics.
- [ ] Plan quality metrics.
- [ ] Completion/recovery metrics.
- [ ] Cost-per-verified-success metric.
- [ ] Trace schema guidance.
- [ ] Release-gate templates.
- [ ] Incident-analysis templates.

## Phase 8 — CHAD/Lapis integration reference

- [ ] Stable CHAD/Lapis interface reference.
- [ ] Cross-repository compatibility matrix.
- [ ] Version compatibility policy.
- [ ] Shared change-propagation workflow.
- [ ] Contract-test examples.
- [ ] Integration incident runbook.

## Phase 9 — Self-improvement for agent systems

- [x] Observation/proposal/outcome records.
- [ ] Agent failure taxonomy.
- [ ] Repeated-failure clustering.
- [ ] Skill effectiveness measurement.
- [ ] Regression-aware skill updates.
- [ ] Human approval workflow for governance changes.
- [ ] Agentic-system postmortem templates.

## Phase 10 — Long-horizon engineering agents

- [ ] Durable task handoffs.
- [ ] Context compaction conventions.
- [ ] Multi-session task state.
- [ ] Research-to-code handoffs.
- [ ] Cross-agent artifact contracts.
- [ ] Failure-resume semantics.
- [ ] Long-running cost controls.

## Completion principle

This repository should remain **portable and provider-neutral**. Product/runtime implementation remains in CHAD; model implementation remains in LapisLLM.
