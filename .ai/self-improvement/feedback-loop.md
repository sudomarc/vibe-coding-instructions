# Feedback Loop

## 1. Observe

Record concrete failures, corrections, friction, or successful patterns. Prefer tool output, test results, diffs, and explicit user feedback over interpretation.

## 2. Record

Create a learning record using the repository template. Remove secrets and unnecessary personal data.

## 3. Classify

Classify the observation as local implementation, workflow, documentation, skill, provider adaptation, or governance.

## 4. Root Cause

Separate the observed symptom from the suspected cause. Identify alternative explanations when evidence is weak.

## 5. Propose

Create an improvement proposal with a precise scope, expected benefit, risks, and validation plan.

## 6. Validate

Check instruction precedence, related skills, examples, templates, and automated validation. Add regression coverage when practical.

## 7. Approve

Apply the approval policy in `rules.md`. Governance-critical changes require explicit human approval.

## 8. Apply

Make the smallest coherent change. Preserve unrelated work and avoid speculative cleanup.

## 9. Regress

Re-run the checks that failed before the improvement and relevant repository-wide validation.

## 10. Close the Loop

Record whether the change worked, what evidence supports that conclusion, and any remaining uncertainty.
