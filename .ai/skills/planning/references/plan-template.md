# Expanded Plan Template

## Goal

State the user-visible or system-observable outcome in one sentence.

## Context

Summarize the relevant repository facts discovered during inspection.

## Scope

### Included

- Feature or behavior explicitly requested.
- Necessary supporting changes.
- Verification work required to establish correctness.

### Excluded

- Unrelated refactors.
- Cosmetic changes without task value.
- Speculative future architecture.

## Files

| File | Action | Purpose | Risk |
|---|---|---|---|
| `path/to/file` | modify | behavior | low |
| `path/to/test` | add | regression | low |

## Decisions

Record concrete choices, not implementation narration.

Examples:

- Reuse the existing validation helper instead of adding another validator.
- Keep the existing API shape to avoid breaking consumers.
- Add a focused test before a broad integration test.

## Dependencies

List new packages, services, environment variables, migrations, or external APIs. State whether each is already present.

## Risks

For each material risk, provide mitigation or a reason it is accepted.

## Verification

Define checks before implementation:

1. targeted unit test;
2. type check;
3. lint or format check;
4. build or smoke test when applicable;
5. diff and status inspection.

## Approval

State one of:

- `not required` — task is clearly authorized within existing scope;
- `required and received` — approval was explicitly given;
- `required and pending` — do not implement yet.

## Exit criteria

The plan is ready when another engineer could implement it without reconstructing the missing decisions.
