# Error Report Format

## Symptom

State exactly what failed, including command, endpoint, test name, exit code, or visible behavior.

## Reproduction

```text
Command: <exact command>
Environment: <relevant context>
Expected: <expected result>
Observed: <actual result>
```

## Evidence

Record the smallest useful logs, stack trace excerpts, or assertions. Never include credentials or secrets.

## Isolation

State what was ruled out and which smallest component still fails.

## Hypothesis

Describe the suspected cause and why the evidence supports it.

## Test

Describe the discriminating experiment. A good test should distinguish the hypothesis from at least one plausible alternative.

## Fix

State the minimal root-cause correction and why it should resolve the failure.

## Regression

Record the original failing check plus relevant neighboring tests.

## Remaining uncertainty

Use explicit labels:

- `VERIFIED:` confirmed by executed checks.
- `UNKNOWN:` not observable in the current environment.
- `HYPOTHESIS:` still unconfirmed.

## Example

```markdown
## Debug
Symptom: `npm test -- auth/session.test.ts` fails on expired tokens.
Isolation: failure occurs only in refresh-token path.
Hypothesis: expiry timestamp is compared using seconds against milliseconds.
Test: print parsed values and add a unit assertion for a known epoch.
Fix: normalize timestamps at the boundary.
Regression: focused test plus adjacent session tests.
```
