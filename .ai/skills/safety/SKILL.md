---
name: safety
description: This skill should be used before destructive, privileged, irreversible, credential-affecting, production-impacting, or remote-execution actions.
---

# Safety Skill

## Trigger Examples

Recursive deletion, force push, hard reset, branch deletion, production data mutation, destructive migration, privilege escalation, secret rotation, firewall changes, downloaded-command execution, system package installation, credential provisioning, browser-profile access, and broad permission changes.

## Workflow

1. Identify the exact action.
2. Identify the target and scope.
3. Determine whether it is reversible.
4. Check authorization.
5. Prefer a dry run or read-only inspection.
6. Minimize scope.
7. Create a rollback or recovery path when possible.
8. Confirm before execution when required.

## Safe provisioning defaults

When an integration or tool installer can modify the host:

- default to environment inspection or dry-run;
- require explicit authorization for system-wide installs, elevated permissions, host configuration, firewall/security changes, credential writes, or persistent browser-profile changes;
- keep downloaded tools, caches and configuration in dedicated locations rather than the project workspace;
- do not use `sudo` merely to overcome a convenient installation path;
- never disable security controls to make an integration work;
- verify the exact files/commands that a provisioning step will create or modify before execution.

A command that installs software or writes configuration is a host mutation even if the application itself is not changed.

## Hard Stop

Never execute `rm -rf` on an uncertain path, `git push --force` on shared history, destructive SQL without validated scope, or arbitrary `curl | bash` without explicit trusted-source authorization and a safer reviewed alternative.

## Reversibility & Compensation

Before performing state-changing mutations:
- Classify reversibility tier (`PURE_REVERSIBLE`, `COMPENSABLE`, `FORWARD_FIX_ONLY`, `IRREVERSIBLE`) according to `.ai/contracts/rollback.contract.md`.
- Register the action and inverse compensation handler in the append-only transaction journal (`journal.jsonl`).
- When a failure or abort occurs, execute LIFO saga compensation unwinding and verify restored state before completing or escalating.

## Reference

- `references/dangerous-actions.md`
- `references/safe-shell-patterns.md`
- `references/reversibility-and-compensation.md`
