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

## Phase 3 — Tool governance [completed]

- [x] Standard tool contract (`.ai/contracts/tool.contract.md`).
- [x] Tool permission taxonomy (`.ai/contracts/tool.contract.md`).
- [x] Side-effect classification (`.ai/contracts/tool.contract.md`).
- [x] Tool result trust labeling (`.ai/contracts/tool.contract.md`).
- [x] External content/prompt-injection guidance (`.ai/skills/security/references/prompt-injection-threat-model.md`).
- [x] Sandbox requirements (`.ai/skills/security/references/sandbox-requirements.md`).
- [x] Tool audit-log conventions (`.ai/contracts/tool-audit.contract.md`).
- [x] Capability/fallback templates (`.ai/contracts/capability-fallback.contract.md`).

## Phase 4 — Context, memory and knowledge governance [completed]

- [x] Context composition policy (`.ai/skills/memory-governance/SKILL.md`).
- [x] Memory write policy (`.ai/contracts/memory.contract.md`).
- [x] Memory deletion semantics (`.ai/contracts/memory.contract.md`).
- [x] Retrieval evidence contract (`.ai/contracts/memory.contract.md`).
- [x] Knowledge-source provenance contract (`.ai/contracts/memory.contract.md`).
- [x] Long-running task compaction policy (`.ai/skills/memory-governance/SKILL.md`).

## Phase 5 — Model/provider governance [completed]

- [x] Provider-neutral model capability schema (`.ai/contracts/model-provider.contract.md`).
- [x] Routing-policy guidance (`.ai/skills/model-governance/SKILL.md`).
- [x] Provider health-state definitions (`.ai/skills/model-governance/SKILL.md`).
- [x] Fallback semantics (`.ai/contracts/model-provider.contract.md`).
- [x] Cost/latency/privacy routing guidance (`.ai/skills/model-governance/SKILL.md`).
- [x] Model evaluation reporting format (`.ai/templates/model-evaluation-report.md`).
- [x] Contract-testing guidance for model backends (`.ai/skills/model-governance/references/contract-testing.md`).

## Phase 6 — Agent security [completed]

- [x] Prompt-injection threat model (`.ai/skills/security/references/prompt-injection-threat-model.md`).
- [x] Tool-confusion threat model (`.ai/skills/security/references/prompt-injection-threat-model.md`).
- [x] Data-exfiltration patterns (`.ai/skills/security/references/prompt-injection-threat-model.md`).
- [x] Permission escalation controls (`.ai/skills/security/references/permission-escalation-controls.md`).
- [x] Sandbox escape test guidance (`.ai/skills/security/references/sandbox-escape-testing.md`).
- [x] Secret-handling guidance for agent runtimes (`.ai/skills/security/references/secret-handling.md`).
- [x] Security review playbooks (`.ai/skills/security/references/security-review-playbook.md`).

## Phase 7 — Evaluation and observability [completed]

- [x] Agent-task benchmark format (`.ai/skills/evaluation/SKILL.md`).
- [x] Tool-call reliability metrics (`.ai/skills/evaluation/SKILL.md`).
- [x] Plan quality metrics (`.ai/skills/evaluation/SKILL.md`).
- [x] Completion/recovery metrics (`.ai/skills/evaluation/SKILL.md`).
- [x] Cost-per-verified-success metric (`.ai/skills/evaluation/SKILL.md`).
- [x] Trace schema guidance (`.ai/skills/evaluation/SKILL.md`).
- [x] Release-gate templates (`.ai/skills/evaluation/SKILL.md`, `.ai/templates/agent-evaluation-report.md`).
- [x] Incident-analysis templates (`.ai/skills/evaluation/SKILL.md`).

## Phase 8 — CHAD/Lapis integration reference [completed]

- [x] Stable CHAD/Lapis interface reference (`.ai/contracts/runtime-interface.contract.md`).
- [x] Cross-repository compatibility matrix (`docs/ecosystem-compatibility.md`).
- [x] Version compatibility policy (`.ai/contracts/runtime-interface.contract.md`).
- [x] Shared change-propagation workflow (`.ai/contracts/runtime-interface.contract.md`).
- [x] Contract-test examples (`.ai/contracts/runtime-interface.contract.md`).
- [x] Integration incident runbook (`.ai/contracts/runtime-interface.contract.md`).

## Phase 9 — Self-improvement for agent systems [completed]

- [x] Observation/proposal/outcome records.
- [x] Agent failure taxonomy (`.ai/self-improvement/references/failure-taxonomy.md`).
- [x] Repeated-failure clustering (`.ai/self-improvement/references/failure-clustering-and-skill-eval.md`).
- [x] Skill effectiveness measurement (`.ai/self-improvement/references/failure-clustering-and-skill-eval.md`).
- [x] Regression-aware skill updates (`.ai/self-improvement/references/failure-clustering-and-skill-eval.md`).
- [x] Human approval workflow for governance changes (`.ai/self-improvement/references/governance-approval-workflow.md`).
- [x] Agentic-system postmortem templates (`.ai/templates/agentic-postmortem.md`).

## Phase 10 — Long-horizon engineering agents [completed]

- [x] Multi-session task state (`.ai/contracts/long-horizon-task.contract.md`).
- [x] Durable task handoffs (`.ai/contracts/long-horizon-task.contract.md`, `.ai/skills/long-horizon-execution/SKILL.md`).
- [x] Context compaction conventions (`.ai/contracts/long-horizon-task.contract.md`, `.ai/skills/long-horizon-execution/SKILL.md`).
- [x] Research-to-code handoffs (`.ai/contracts/long-horizon-task.contract.md`, `.ai/skills/long-horizon-execution/SKILL.md`).
- [x] Cross-agent artifact contracts (`.ai/contracts/long-horizon-task.contract.md`).
- [x] Failure-resume semantics (`.ai/contracts/long-horizon-task.contract.md`, `.ai/skills/long-horizon-execution/SKILL.md`).
- [x] Long-running cost controls (`.ai/contracts/long-horizon-task.contract.md`, `.ai/skills/long-horizon-execution/SKILL.md`).

## Completion principle

This repository should remain **portable and provider-neutral**. Product/runtime implementation remains in CHAD; model implementation remains in LapisLLM.
