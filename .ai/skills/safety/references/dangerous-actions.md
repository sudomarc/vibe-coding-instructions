# Dangerous Actions Reference

## File deletion

Examples: `rm -rf`, recursive deletion of project directories, bulk overwrites, or deleting migration history.

Before acting, identify exact paths, confirm they are disposable, and prefer moving to a recoverable location when practical.

## Git history

Examples: `git push --force`, `git reset --hard` on shared work, rebasing published history, deleting a remote branch.

Require explicit authorization and capture the target ref and recovery point.

## Database destruction

Examples: `DROP TABLE`, destructive migrations, mass `DELETE` or `UPDATE` without a bounded predicate.

Prefer a transaction, backup, dry run, bounded query, or migration rollback path.

## Remote execution

Examples: piping downloaded content directly into a shell, executing unreviewed install scripts, or evaluating remote code.

Download and inspect first when possible. Prefer pinned, trusted package sources.

## Secrets

Never print, commit, paste, or store credentials unnecessarily. If a secret appears in output, stop exposing it and follow the project's rotation procedure.

## Privilege

Examples: `sudo`, root shell, modifying system services, firewall rules, IAM roles, access control lists.

Confirm the exact command, reason, and blast radius.

## External systems

Deployments, production configuration, billing, messaging, and user-data changes may be materially consequential even when technically reversible. Apply the same authorization and verification discipline.

## Safe response

When confirmation is required, state:

```markdown
Action: <exact operation>
Target: <exact target>
Impact: <what can change>
Recovery: <known rollback/backup>
Verification: <how success will be checked>
Confirmation required: yes
```

Do not weaken the operation merely by hiding it inside a script or alias.
