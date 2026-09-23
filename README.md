# Vibe Coding Instructions

> **Ecosystem role:** portable governance and policy layer for the CHAD + LapisLLM agentic AI system.

The three-repository architecture is documented in [docs/ecosystem.md](docs/ecosystem.md). Vibe Coding Instructions defines reusable policies, skills and role contracts; CHAD executes the agent runtime; LapisLLM provides model/runtime capabilities.

See the [ecosystem roadmap](docs/roadmap.md) and [agent runtime contract](docs/agent-runtime-contract.md).


A repository-native instruction system for disciplined AI coding agents, with a controlled evidence-driven self-improvement loop.

## Why this exists

AI coding agents are capable of producing large changes quickly. The failure mode is not only bad code. It is also premature coding, misunderstood architecture, silent scope expansion, unverifiable claims, dependency drift, accidental destructive actions, loss of context across sessions, and brittle dependence on one external tool or provider.

This repository turns those concerns into a layered operating system:

## Web development and design layer

The framework separates web concerns that benefit from independent reasoning: project completeness baseline, design direction, design systems, responsive behavior, motion, anti-vibe visual review, legal/compliance review, capability routing for external tools, browser 3D, asset pipelines, visual regression, forms UX, accessibility, browser QA, performance, SEO, browser-facing security, and Next.js-specific work.

For new public web projects, the baseline starts with .ai/skills/web-project-baseline/SKILL.md and its applicability matrix. Provider-neutral primary and specialist agent profiles live under .ai/agents/. The intended pipeline is BASELINE → DESIGN DIRECTION → ARCHITECTURE → IMPLEMENT → BROWSER VERIFY → SPECIALIST REVIEW → FINAL DIFF.

### Production web baseline

The web-project-baseline skill turns lessons from Amplio Web into a reusable launch discipline: shared shell, route inventory, content/data source of truth, form lifecycle, cookies and browser storage audit, consent when applicable, privacy/legal surfaces, SEO, accessibility, responsive behavior, motion and 3D fallbacks, assets and third-party resource governance, browser security, performance, failure states, hosting state and evidence-backed release verification. It does not require every feature on every project; it classifies each capability as required, applicable, not applicable, deferred or unknown.

The framework deliberately does not require a cookie banner by default. It requires storage/tracking inventory first, then consent controls only when the actual project behavior and applicable rules call for them.

### Anti-vibe visual quality

The web layer includes .ai/skills/anti-vibe-design/SKILL.md, a contextual checklist for recognizable AI/web-design patterns. These are not hard bans. The objective is to detect trend stacking and lack of product-specific rationale while preserving legitimate use of contemporary design patterns.

### Legal/compliance quality

The web layer also includes .ai/skills/legal-compliance/SKILL.md, derived from the attached September 2026 audit prompt. It audits six recurring exposure areas and secondary privacy/security checks. The legal layer is evidence-first and separates engineering remediation from jurisdictional/legal conclusions, registrations and human-owned policy work.

### Capability resilience

The web/engineering layer includes .ai/skills/capability-routing/SKILL.md, inspired by the reviewed Agent Reach architecture.

It treats external tools as replaceable providers behind stable capabilities:

`CAPABILITY → PRIMARY → FALLBACK → HEALTH CHECK → ACTIVE ROUTE`

The framework now expects real health evidence rather than "the binary exists" checks, explicit fallback ordering, safe diagnostics, dry-run/read-only provisioning, dedicated state directories, strict credential/browser-session boundaries, actionable failure taxonomy and explicit upstream version strategy.

Use .ai/templates/capability-matrix.md when a project has several external providers or interchangeable implementation paths.

## Core philosophy

### Plan before code

Every implementation begins with an observable goal, bounded scope, known constraints, and a verification strategy. Tiny changes use tiny plans; complex changes use living plans.

### Verify, do not assume

Use repository tools, tests, type checks, linters, builds, diffs, and runtime checks as evidence. Do not replace evidence with confidence.

### Surface uncertainty

State unknowns, assumptions, conflicting evidence, and unverified behavior explicitly.

### Preserve human control

Self-improvement is controlled evolution, not unrestricted self-modification. Confidence never authorizes a change to governance.

## Specialist routing

Use the narrowest matching capability rather than preloading every rule:

| Surface | Skill | Specialist |
|---|---|---|
| Public web project / launch baseline | web-project-baseline | web-project-auditor |
| Visual direction/UI | design-direction, design-system | ui-reviewer, design-director |
| Anti-vibe visual quality | anti-vibe-design | anti-vibe-reviewer |
| Compliance-sensitive flows | legal-compliance | legal-compliance-reviewer |
| External tool/provider integration | capability-routing | integration-health-reviewer |
| Responsive behavior | responsive-design | responsive-reviewer |
| Motion / scroll / micro-interactions | interaction-motion | motion-3d-specialist when advanced |
| Browser 3D | web-3d | motion-3d-specialist |
| Media / 3D assets | asset-pipeline | asset-pipeline-specialist |
| Screenshot regression | visual-regression | visual-regression-reviewer |
| Runtime browser checks | browser-qa | browser-tester, visual-qa |
| Performance | web-performance | performance-auditor |
| Accessibility | accessibility | accessibility-reviewer |

Do not invoke every specialist by default. Use changed surface and risk to determine the review set.

## Token economy

The framework includes `.ai/skills/token-economics/SKILL.md` for context budgeting, targeted retrieval, tool-result control, compaction, retry discipline, delegation economics, model/effort routing, prompt caching, and provider-aware cost measurement. It is intentionally modular so token policy does not become another large always-loaded prompt.

Use `.ai/templates/agent-cost-report.md` when a task needs a usage record. Provider-specific pricing and semantics live under `.ai/skills/token-economics/references/providers/` and must be rechecked against current official documentation.

## Self-improvement system

REAL-WORLD USE → OBSERVE / COLLECT → ANALYZE / CLASSIFY → ROOT-CAUSE HYPOTHESIS → PROPOSE → VALIDATE → APPROVE* / APPLY → TEST / REGRESSION CHECK → MEASURE → RECORD OUTCOME

* Human approval is mandatory for governed changes.

### Evidence and memory

The durable record store lives in .ai/self-improvement/records/:

- observations/ stores evidence and recurrence classification;
- proposals/ stores bounded changes, risks, and validation plans;
- outcomes/ stores post-change measurements and regression results.

The periodic collector at scripts/self_improvement_cycle.py produces transient evidence artifacts. It does not decide that a rule should change.

### Anti-drift

The system explicitly supports ADD, REMOVE, MERGE, SIMPLIFY, and REPLACE. A useful improvement can be deletion or consolidation rather than another rule.

## Legal audit reporting

Use .ai/templates/legal-audit.md for the six-item report shape. Each item must end with explicit human follow-up or a documented reason it is not applicable.

## Capability audit reporting

Use .ai/templates/capability-matrix.md for external-provider integrations. The matrix distinguishes capability presence, configuration, health and active routing, plus authentication, reproducibility and recovery evidence.

## GitHub integration

The repository contains the repository-level Custom Agent profile at .github/agents/self-improvement.agent.md.

## Validation

The framework validator is scripts/validate_instructions.py. It checks required paths, governance markers, Markdown links, the Custom Agent contract, and explicit workflow permissions. The self-improvement workflow runs this validator before opening an automated draft PR.

## Using it in another repository

Copy the policy entry files and the .ai/ directory into the target repository. Preserve paths so references remain valid. Then adapt only project-specific sections such as runtime, framework, commands, architecture, branching, tests, deployment, and ownership.

Do not blindly copy project-specific rules from this repository into another project. This repository defines a general operating system, not application-specific truth.

## What this repository does not guarantee

It does not guarantee perfect agent behavior. Instruction-following is probabilistic, tools vary, repositories contain ambiguous requirements, and validation has blind spots. The purpose is to make decisions, evidence, changes, and uncertainty reviewable.

## Further reading

Start with .ai/self-improvement/daily-cycle.md, MASTER-PROMPT.md, AGENTS.md, and the relevant web, engineering, or capability skill. For source attribution, see docs/sources.md.
