# Feedback Loop

## 1. Observe

Record concrete failures, corrections, friction, or successful patterns. Prefer tool output, test results, diffs, and explicit user feedback over interpretation.

## 2. Collect

Run deterministic collection when a periodic cycle is active. Gather repository integrity, Git history, GitHub Issues/PRs, workflow results, and existing learning records available to the collector.

## 3. Record

Create an observation or learning record using the structures in `.ai/self-improvement/schemas/` and templates in `.ai/self-improvement/templates/`. Remove secrets and unnecessary personal data.

## 4. Classify

Classify the signal as `ONE_OFF_FAILURE`, `RECURRING_FAILURE`, or `SYSTEMIC_FAILURE` only when the evidence supports that classification.

## 5. Root Cause

Separate the observed symptom from the suspected cause. Identify alternative explanations when evidence is weak. Label conclusions as `HYPOTHESIS` until validated.

## 6. Propose

Create an improvement proposal with precise scope, expected benefit, risks, regression risk, confidence, approval requirement, and validation plan. Prefer local fixes before governance changes.

## 7. Validate

Check instruction precedence, related skills, examples, templates, references, and automated validation. Add regression coverage when practical.

## 8. Approve

Apply `rules.md`. Governance-critical changes require explicit human approval. Confidence is evidence quality, not authorization.

## 9. Apply

Make the smallest coherent change. Preserve unrelated work and avoid speculative cleanup. For substantial changes, use a branch and pull request.

## 10. Regress

Re-run the checks that failed before the improvement and relevant repository-wide validation. Treat a material regression as a reason to reject, revise, or revert.

## 11. Measure

Compare `BEFORE` and `AFTER` when the target signal can be measured. Do not mark an improvement confirmed without supporting post-change evidence.

## 12. Close the Loop

Record the actual outcome, remaining uncertainty, and next measurement window. Useful outcome states include `CONFIRMED`, `PARTIALLY_CONFIRMED`, `INEFFECTIVE`, `REVERTED`, and `AWAITING_EVIDENCE`.

## Evidence Vocabulary

- `FACT` — directly established evidence.
- `OBSERVED` — directly seen during a run/session.
- `HYPOTHESIS` — tentative explanation.
- `INTERPRETATION` — conclusion derived from evidence.
- `UNKNOWN` — not established.
- `CONFLICT` — sources disagree.
- `UNVERIFIED` — not yet tested.
