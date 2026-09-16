# Architecture Checklist

## Repository understanding

- [ ] Root instructions located.
- [ ] Framework and language identified.
- [ ] Package manager identified.
- [ ] Existing entry points identified.
- [ ] Relevant tests located.
- [ ] Build and lint commands located.

## Boundary analysis

- [ ] Public interfaces identified.
- [ ] Internal interfaces identified.
- [ ] Persistence boundaries identified.
- [ ] Network boundaries identified.
- [ ] Authentication and authorization boundaries identified.
- [ ] Trust boundaries identified.

## Change surface

- [ ] Smallest file set identified.
- [ ] Existing abstraction that can be reused identified.
- [ ] Duplicate behavior avoided.
- [ ] Backward compatibility considered.
- [ ] Configuration impact considered.
- [ ] Migration impact considered.

## Failure modes

- [ ] Input validation failures considered.
- [ ] Dependency failures considered.
- [ ] Timeout or retry behavior considered.
- [ ] Partial failure behavior considered.
- [ ] Logging and observability impact considered.
- [ ] Security impact considered.

## Simplicity test

Ask:

1. Can this be solved without a new abstraction?
2. Can this be solved without a new dependency?
3. Can an existing boundary absorb the change?
4. Does the proposed design introduce behavior the user did not request?
5. Is the verification strategy proportionate to risk?

## Decision quality

The plan should identify the chosen approach, the main alternative considered, and why the chosen approach fits the repository. Do not create a fake alternative simply to satisfy documentation.
