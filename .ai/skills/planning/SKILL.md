---
name: planning
description: >
  Use when a task changes architecture, introduces a feature, spans multiple files,
  or contains material ambiguity. Trigger before implementation when a plan is needed.
---

# Planning Skill

## When to Use

Use this skill before implementation when the task is multi-file, architectural, risky, ambiguous, or likely to expand scope. For a trivial safe change, the core workflow may provide sufficient planning.

## Workflow

1. Read the core rules.
2. Inspect repository structure and local instructions.
3. Identify the requested outcome and constraints.
4. Map the smallest affected file set.
5. Record design decisions and alternatives.
6. Identify risks and unknowns.
7. Define verification before implementation.
8. Present the plan in the template format.
9. Obtain approval when the workflow requires it.

## Plan format

```markdown
## Plan
Goal: <observable outcome>
Scope: <included and excluded work>
Files:
- <path> — <purpose>
Decisions:
- <decision>
Risks:
- <risk and mitigation>
Verification:
- <check>
Approval: <required | not required>
```

## Checklists

- [ ] Requirement is observable.
- [ ] Scope is bounded.
- [ ] Affected files are identified.
- [ ] Existing architecture was inspected.
- [ ] Dependencies are explicit.
- [ ] Risks and unknowns are visible.
- [ ] Verification is defined.
- [ ] Approval state is explicit.

## Stop conditions

Stop before coding when requirements conflict, a critical choice is missing, or a dangerous action is necessary without authorization.

## Reference Files

- `references/plan-template.md` — expanded planning template.
- `references/architecture-checklist.md` — architecture inspection checklist.
- `assets/plan-example.md` — concrete example of an approved plan.
