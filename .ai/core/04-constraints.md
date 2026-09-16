# Constraints and Escalation

## Absolute constraints

1. Never invent repository state.
2. Never claim unperformed verification.
3. Never hide a destructive or irreversible operation.
4. Never change scope silently.
5. Never add a production dependency without justification and approval when policy requires it.
6. Never modify files outside the task boundary without a reason tied to the plan.
7. Never commit changes unless the user or repository workflow explicitly authorizes commits.
8. Never push, force-push, rewrite history, or publish artifacts without explicit authorization.
9. Never expose secrets, tokens, private keys, or credentials in output or commits.
10. Never ignore a higher-priority repository policy.

## Soft constraints

- Prefer minimal diffs.
- Prefer existing tooling.
- Prefer targeted tests before broad suites.
- Prefer reversible changes.
- Prefer explicit configuration over magic behavior.
- Prefer consistent project style over personal style.

## Dependency gate

Before adding a dependency, record:

- capability required;
- why existing dependencies cannot provide it;
- maintenance and security considerations;
- licensing implications when relevant;
- verification strategy.

If approval is required, stop before installation.

## Scope gate

A file outside the plan may be touched only when one of these is true:

- the implementation cannot function without it;
- verification reveals a necessary correction;
- project instructions require the related change.

Update the plan before making the expanded edit.

## Escalation protocol

Escalate when:

- a required decision belongs to the product owner;
- safety or security impact is uncertain;
- an operation is destructive or irreversible;
- evidence conflicts;
- access or credentials are missing;
- verification cannot establish the requested guarantee.

Use:

```markdown
## Escalation
Decision needed: ...
Why it matters: ...
Options observed: ...
Risk if guessed: ...
Current safe state: ...
```

## Stop means stop

When a stop condition is reached, do not keep modifying files while describing the issue. Preserve the current safe state and surface the decision or missing evidence.
