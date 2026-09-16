---
name: safety
description: >
  Use before destructive, irreversible, privileged, secret-affecting, or high-impact
  actions. Trigger for deletion, force pushes, destructive SQL, remote execution, and similar hazards.
---

# Safety Skill

## When to Use

Load this skill before any operation that can irreversibly destroy data, rewrite history, expose secrets, execute untrusted code with elevated privilege, or materially affect external systems.

## Dangerous actions

Examples include:

- `rm -rf` or broad file deletion;
- `git push --force`, history rewriting, or branch deletion;
- `DROP TABLE`, destructive migrations, or mass data updates;
- `curl ... | bash` or similar remote script execution;
- credential rotation or secret deletion;
- production deployment or rollback when impact is material;
- changing access controls or firewall rules;
- overwriting generated or user data without a recoverable path.

See `references/dangerous-actions.md`.

## Workflow

1. Identify the exact action.
2. Determine blast radius and reversibility.
3. Check repository or system policy.
4. Find a safer or reversible alternative.
5. Request explicit confirmation when policy requires it.
6. Execute only the approved action.
7. Verify the resulting state.

## Stop conditions

Stop when target, scope, authorization, recovery plan, or verification is unclear.

## Checklists

- [ ] Exact target identified.
- [ ] Authorization confirmed.
- [ ] Backup or recovery path considered.
- [ ] Blast radius understood.
- [ ] Safer alternative evaluated.
- [ ] Verification defined.

## Reference Files

- `references/dangerous-actions.md`
