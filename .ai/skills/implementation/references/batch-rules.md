# Batch Rules

## Purpose

Batches limit blast radius and make failures localizable.

## Rules

1. One logical intent per batch.
2. Prefer less than 50 changed lines per unit when practical.
3. Keep a batch internally complete enough to verify.
4. Avoid mixing formatting-only edits with behavior changes.
5. Do not include unrelated refactoring.
6. Verify immediately after a risky batch.
7. Update the plan if a file outside the plan becomes necessary.

## Good batch examples

- Add a validation helper and its unit test.
- Register one API route and its focused test.
- Update one migration and its migration test.

## Poor batch examples

- Rewrite an entire module while fixing one bug.
- Reformat the repository during a feature change.
- Add five unrelated dependencies in one batch.

## Batch stop conditions

Stop if:

- targeted verification fails and the cause is unknown;
- a generated change is much larger than expected;
- a new architectural decision appears;
- a destructive operation becomes necessary;
- scope is no longer clear.

## Recovery

When stopped, preserve the safe state, record evidence, and return to planning or debugging as appropriate. Do not continue merely to make the batch look complete.

## Exception

Generated lockfiles, schemas, snapshots, or migration artifacts may exceed the line heuristic when the logical change is atomic. Record the exception and verify the artifact using repository-native tooling.
