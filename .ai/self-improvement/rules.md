# Self-Improvement Governance Rules

## Purpose

Self-improvement exists to make recurring lessons reusable without allowing an agent to rewrite its own authority.

## Allowed Automatically

An agent may record observations and propose improvements. It may apply changes only when the current task explicitly authorizes the change and the change remains within the existing governance boundary.

## Approval Required

Explicit human approval is required before changing:

- `.ai/core/` governance rules;
- security or safety boundaries;
- verification requirements;
- instruction precedence;
- provider trust boundaries;
- destructive-operation policy;
- data-retention or privacy rules.

## Evidence Requirement

A proposal must identify its observations, affected rule, suspected root cause, evidence quality, expected benefit, regression risk, and validation plan.

## Anti-Drift Rule

If a proposed improvement conflicts with a higher-priority instruction, broadens scope, weakens a safety control, or cannot be validated, reject it rather than adapting the governance to fit the failure.
