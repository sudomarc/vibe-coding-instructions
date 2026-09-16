---
name: implementation
description: >
  Use when turning an approved plan into repository changes. Trigger for coding,
  configuration, test, migration, or documentation edits that implement the plan.
---

# Implementation Skill

## When to Use

Use after a plan exists and the required approval gate has passed. Do not use this skill to invent scope that planning did not establish.

## Workflow

1. Re-read the plan and relevant repository instructions.
2. Load `references/batch-rules.md` and `references/coding-standards.md` when applicable.
3. Confirm the target files still match the plan.
4. Implement one logical batch at a time.
5. Verify the batch with the cheapest meaningful check.
6. Record the batch report.
7. Continue only if the current state is safe and consistent with the plan.
8. Finish with the review skill.

## Batch contract

A batch should normally stay below 50 changed lines per logical unit. The threshold is a control heuristic, not a reason to split a naturally atomic generated file into nonsense fragments.

Each batch report contains:

```markdown
### Batch N
Changed: <files and behavior>
Reason: <plan item>
Verification: <command/check and result>
Status: <complete | blocked>
Next: <next batch>
```

## Checklists

- [ ] Plan item identified.
- [ ] Only planned files touched.
- [ ] Existing conventions followed.
- [ ] No unnecessary dependency added.
- [ ] Batch verification performed.
- [ ] No unrelated cleanup included.

## Stop conditions

Stop when a batch reveals an architecture conflict, unexpected file dependency, destructive requirement, failing verification without a known safe correction, or scope expansion.

## Reference Files

- `references/batch-rules.md` — batching and stop controls.
- `references/coding-standards.md` — generic coding quality rules.
- `assets/commit-conventions.md` — concrete commit message examples.
