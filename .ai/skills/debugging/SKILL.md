---
name: debugging
description: >
  Use when behavior is failing, tests are red, a command errors, or the cause of
  a defect is unclear. Trigger for evidence-driven fault isolation and regression fixes.
---

# Debugging Skill

## When to Use

Use whenever the problem is not already sufficiently explained by a direct, verified cause.

## Workflow

1. **Reproduce** the failure with the smallest reliable command or test.
2. **Isolate** the smallest failing component or input.
3. **Hypothesize** one or more causes based on evidence.
4. **Test** the hypothesis with a discriminating check.
5. **Correct** the root cause, not merely the symptom.
6. **Regress** with the original failing case and relevant neighboring checks.

## Rules

Do not patch blindly.
Do not make multiple unrelated changes between evidence checks.
Do not delete a failing test merely because it is inconvenient.
Do not label a hypothesis as a root cause before testing it.

## Debug report

Use `references/error-report-format.md`.

## Checklists

- [ ] Original failure reproduced.
- [ ] Evidence captured.
- [ ] Smallest failing unit isolated.
- [ ] Hypothesis stated.
- [ ] Hypothesis tested.
- [ ] Root cause supported by evidence.
- [ ] Minimal fix applied.
- [ ] Regression check passes.

## Escalate when

The failure depends on unavailable infrastructure, missing credentials, nondeterministic external state, or conflicting requirements. Preserve evidence rather than guessing.

## Reference Files

- `references/error-report-format.md`
