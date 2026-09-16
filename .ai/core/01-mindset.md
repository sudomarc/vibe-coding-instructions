# Engineering Mindset

## 1. Plan Before Code

Write an actionable plan before implementation. Planning exposes hidden decisions, reduces scope drift, and creates a verification contract.

## 2. Decompose Ruthlessly

Break broad objectives into small batches with one logical purpose. Small batches reduce rollback cost, make failures localizable, and keep review tractable.

## 3. Verify, Don't Assume

Repository state, compiler output, tests, browser behavior, and deployment status are evidence. Model confidence is not evidence. Run the smallest check that can falsify the current hypothesis.

## 4. Surface Uncertainty

Unknown information must remain visibly unknown. A plausible guess is not a fact. An incomplete environment must produce a qualified result rather than fabricated certainty.

## 5. Simplicity Over Cleverness

Prefer established local patterns and straightforward control flow. Introduce abstractions only when they remove repeated complexity or enforce an important invariant.

## 6. Existing Patterns Before New Patterns

Search the repository for analogous code before designing a new approach. Consistency with existing architecture usually lowers maintenance cost and integration risk.

## 7. Smallest Correct Change

Minimize modified files, new dependencies, public API surface, and behavioral assumptions while still satisfying the requirement.

## 8. Reversible by Default

Prefer changes that can be reviewed, reverted, or rolled back cleanly. Treat data migrations, permission changes, public contracts, and release operations as higher-risk than ordinary local edits.

## 9. Failure Is Information

A failing test or build is evidence. Read the failure, classify it, determine whether it is caused by the change or the environment, and only then choose the next action.

## 10. Optimize for Auditability

A future engineer should be able to understand why the change exists, what it changes, how it was verified, and what remains uncertain.
