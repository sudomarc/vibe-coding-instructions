---
name: review
description: >
  Use before declaring a task complete. Trigger after implementation or whenever
  the user asks for an audit, diff review, regression check, or readiness assessment.
---

# Review Skill

## When to Use

Use after implementation and before completion. It is also appropriate for reviewing an existing diff without making changes.

## Workflow

1. Read the task and plan.
2. Inspect repository status and diff.
3. Compare changed files with planned scope.
4. Run targeted and appropriate broad verification.
5. Inspect error handling, security, compatibility, tests, and documentation.
6. Record findings.
7. Correct issues only within authorized scope.
8. Re-run relevant checks after corrections.

## Review report

```markdown
## Review
Scope: ...
Findings:
- Severity: <critical|high|medium|low>
  Location: <path:line or symbol>
  Finding: ...
  Evidence: ...
Action: <fixed|accepted|blocked>
Verification: ...
Remaining uncertainty: ...
```

## Checklists

- [ ] Diff matches plan.
- [ ] No accidental files changed.
- [ ] Tests cover the requested behavior.
- [ ] Error paths are reasonable.
- [ ] Security boundaries are preserved.
- [ ] Public contracts are unchanged unless requested.
- [ ] Documentation matches behavior.
- [ ] Tooling checks ran.

## Severity

Critical or high findings block completion unless explicitly accepted by the appropriate human authority. Medium findings require a decision or correction. Low findings may be documented when outside scope.

## Reference Files

- `references/self-audit-checklist.md`
- `references/diff-review-guide.md`
- `assets/review-comment-examples.md`
