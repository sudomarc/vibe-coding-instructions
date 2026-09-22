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

## Phase 1 — Agent-role contracts

- [ ] Orchestrator role contract.
- [ ] Researcher role contract.
- [ ] Coder role contract.
- [ ] Analyst role contract.
- [ ] Shared handoff schema.
- [ ] Shared evidence schema.
- [ ] Stop-condition conventions.
- [ ] Permission-level vocabulary.
- [ ] Runtime-neutral role examples.

## Phase 2 — Agent orchestration governance

- [ ] Delegation policy.
- [ ] Parallelism policy.
- [ ] Retry/loop policy.
- [ ] Bounded autonomy policy.
- [ ] Human checkpoint policy.
- [ ] Failure escalation rules.
- [ ] Agent identity and correlation guidance.
- [ ] Multi-agent audit conventions.

## Phase 3 — Tool governance

- [ ] Standard tool contract.
- [ ] Tool permission taxonomy.
- [ ] Side-effect classification.
- [ ] Tool result trust labeling.
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
