# Standard Workflow

## Overview

All ordinary implementation follows three operational stages:

1. **PLAN**
2. **IMPLEMENT**
3. **VERIFY**

The full communication loop is:

`PROMPT → PLAN → IMPLEMENT → VERIFY → REPORT`

## Stage 1 — PLAN

Inspect the repository and relevant instructions before changing files.

Produce:

```markdown
## Plan
Goal: ...
Scope: ...
Files: ...
Decisions: ...
Risks: ...
Verification: ...
```

Stop if a required decision or approval is missing.

### Plan stop conditions

- requirements are materially ambiguous;
- a destructive action is required without authorization;
- a repository rule conflicts with the request and cannot be resolved;
- a critical external dependency cannot be verified;
- implementation would exceed the agreed scope.

## Stage 2 — IMPLEMENT

Use the implementation skill when the task is non-trivial. Work in bounded batches, normally one logical unit and fewer than 50 changed lines where practical.

After each batch report:

```markdown
### Batch N
Changed: ...
Reason: ...
Verification: ...
Next: ...
```

Do not mix unrelated refactors into a batch merely because the file is open.

## Stage 3 — VERIFY

Perform checks appropriate to the risk: targeted tests, broader tests, type checking, linting, formatting, build, smoke test, or manual inspection.

Then inspect the diff and repository status.

Report:

```markdown
## Verification
Passed: ...
Failed: ...
Not run: ...
Evidence: ...
Remaining uncertainty: ...
```

## Interruptions

When the user changes direction, stop new implementation and update the plan. Preserve correct work already completed unless the new instruction explicitly supersedes it.

When a tool fails, do not conceal it. Diagnose the failure, determine whether retrying is safe, and report the actual state.

## Completion gate

Do not say “done” until:

- scope is implemented;
- relevant checks ran;
- diff was inspected;
- unresolved failures are explicit;
- no unauthorized destructive action was taken.

## Short tasks

For a one-line safe change, the plan can be implicit in a concise action note, but the invariant remains: understand the target and verify the change.
