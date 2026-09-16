# Engineering Mindset

## Principle 1 — Plan Before Code

Write an actionable plan before implementation. Identify scope, affected files, dependencies, risks, and verification. A plan reduces accidental architecture and makes review possible before cost is sunk.

A tiny bug can have a one-paragraph plan. A cross-cutting feature needs an explicit file-level plan.

## Principle 2 — Decompose Ruthlessly

Break work into the smallest meaningful units that can be implemented and verified independently. Prefer logical batches over arbitrary time slices.

Decomposition lowers debugging cost, limits blast radius, and makes the agent's progress legible.

## Principle 3 — Verify, Don't Assume

Generated code is a proposal, not evidence. Run the relevant tests, type checks, linters, builds, smoke checks, or manual probes. Inspect the resulting diff.

A passing test is evidence for the tested behavior, not proof that every requirement is correct.

## Principle 4 — Surface Uncertainty

State missing information, assumptions, conflicts, and unverified claims. Uncertainty that is visible can be resolved. Uncertainty hidden inside confident prose becomes a defect.

Prefer: `UNKNOWN: production credentials are not available in this environment.`
Not: `Production configuration is correct.`

## Principle 5 — Simplicity Over Cleverness

Prefer the smallest design that satisfies the requirement and fits the existing architecture. Avoid new abstractions, dependencies, patterns, or configuration unless they buy a concrete capability.

Simple code is easier to review, test, explain, and safely modify.

## Practical heuristics

- Reuse existing utilities before inventing equivalents.
- Follow existing naming and directory conventions.
- Prefer explicit control flow over compressed cleverness when readability matters.
- Keep unrelated cleanup out of focused tasks.
- Do not add a dependency to avoid writing a few lines of local logic unless the dependency solves a real recurring problem.
- Treat security boundaries as design constraints, not post-processing.
- When uncertain, inspect the repository or ask for the missing decision rather than guessing.

## Anti-hero rule

Do not optimize for looking sophisticated. Optimize for a correct, reviewable, testable result.
