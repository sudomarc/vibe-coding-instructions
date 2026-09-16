# Workflow

## Stage 0 — Inspect

Before planning, inspect repository status, applicable instructions, project shape, target files, nearby tests, and existing patterns.

### Output

`Observed:` repository facts and current state.

`Unknown:` information that remains missing.

`Constraints:` relevant rules.

### Stop Conditions

Stop if the target cannot be located, requirements conflict materially, or a required authorization is missing.

## Stage 1 — PLAN

State the observable goal, bounded scope, affected areas, key decisions, risks, dependencies, verification, and approval state.

### Output

```text
PLAN
Goal:
Scope:
Files:
Decisions:
Risks:
Verification:
Approval:
```

### Stop Conditions

Do not implement when architecture is materially ambiguous or approval is required and absent.

## Stage 2 — IMPLEMENT

Execute one logical batch at a time. After each batch, inspect the resulting diff and run focused verification. Do not silently widen the batch because another improvement appears convenient.

### Output

```text
BATCH
Purpose:
Changed:
Checks:
Result:
Next:
```

### Stop Conditions

Stop when a batch fails unexpectedly, exposes a new design decision, requires dangerous action, or expands scope.

## Stage 3 — VERIFY

Run appropriate tests, linters, type checks, builds, integration checks, or runtime inspection. Re-run regressions after fixes. Inspect the final diff.

### Output

```text
VERIFY
Checks run:
Evidence:
Failures:
Remaining uncertainty:
```

## Final Report

Separate implementation facts from evaluation. Report files changed, commands actually run, results, and limitations.

## Interruptions

When interrupted, preserve the current batch state. Do not restart from memory. Create a handoff with current repository status, completed work, evidence, blockers, and exact next actions.
