# Self-Audit Checklist

## Correctness

- [ ] Requirement is implemented exactly as planned.
- [ ] Main success path works.
- [ ] Failure paths behave intentionally.
- [ ] Edge cases relevant to the task are covered.

## Scope

- [ ] Every changed file is justified.
- [ ] No unrelated cleanup slipped in.
- [ ] New dependencies are justified.

## Tests

- [ ] New or changed behavior has appropriate coverage.
- [ ] Focused checks pass.
- [ ] Broader checks were considered.
- [ ] Test failures are investigated rather than ignored.

## Security

- [ ] Secrets are not exposed.
- [ ] Input validation is appropriate.
- [ ] Authorization remains correct.
- [ ] Dangerous shell or query construction is absent or constrained.
- [ ] File and network access remains within intended boundaries.

## Reliability

- [ ] Error handling preserves useful context.
- [ ] Timeouts or retries are not accidentally unbounded.
- [ ] Resource cleanup is handled where required.

## Maintainability

- [ ] Names explain intent.
- [ ] Abstractions are justified.
- [ ] Comments explain why rather than restating code.
- [ ] Documentation is updated where behavior changed.

## Final evidence

Record commands run, results, and anything that could not be verified. A clean diff is evidence of scope control, not evidence of correctness by itself.
