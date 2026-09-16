# FAQ

## 1. Is this a replacement for AGENTS.md?

No. It is a reusable instruction system whose root `AGENTS.md` is itself suitable as an entry point. Project-specific `AGENTS.md` rules remain authoritative for that project.

## 2. Why require a plan before code?

Because implementation without a scope model makes architecture emerge accidentally. The plan is a lightweight checkpoint against wrong assumptions and scope drift.

## 3. Does every one-line change need a long plan?

No. The invariant requires understanding and an actionable plan, not paperwork. A trivial change can use a concise action note.

## 4. Why progressive disclosure?

Loading every rule, checklist, and example into every context wastes attention and increases instruction collisions. Core rules stay stable; skills and references load only when needed.

## 5. Should every skill be loaded at startup?

No. Trigger skills by task type. Load references only when the selected skill requires them.

## 6. What counts as verification?

The check should match the risk: a focused unit test, integration test, type check, linter, build, smoke test, or careful manual inspection. State exactly what was run.

## 7. Does a passing test prove the task is correct?

No. Tests provide evidence for covered behavior. Requirements, compatibility, security, and untested paths still need review.

## 8. Can the agent add dependencies?

Only with a justified need and according to repository approval rules. Existing dependencies should be considered first.

## 9. Can the agent commit automatically?

Not by default. A commit is a repository mutation and should follow explicit user or workflow authorization.

## 10. What about push or deployment?

Treat them as higher-impact actions. Apply project policy and the safety skill when an operation can affect remote history, production systems, users, or data.

## 11. What if repository instructions conflict?

Do not hide the conflict. Apply the most specific applicable instruction when the hierarchy is clear; otherwise stop and surface the decision.

## 12. What if a test is too slow?

Use the cheapest meaningful targeted check first, then run broader verification when risk and time justify it. Document checks that were not run.

## 13. What if context gets too large?

Use `.ai/skills/context-management/SKILL.md` and create a factual handoff before starting a new session.

## 14. How should uncertain claims be phrased?

Use explicit labels such as `FACT`, `VERIFIED`, `INFERENCE`, `HYPOTHESIS`, `UNKNOWN`, and `CONFLICT` when they materially improve clarity.

## 15. Why include examples?

Examples help agents pattern-match concrete output without turning every example into a global rule. The governing behavior remains in the core and skill documents.
