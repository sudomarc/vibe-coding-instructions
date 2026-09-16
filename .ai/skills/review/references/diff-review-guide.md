# Diff Review Guide

## First pass

Read the summary: files changed, insertions, deletions, renames. Unexpected file count is an immediate scope signal.

## Second pass

Read the diff from top to bottom. For each hunk ask:

- What behavior changes?
- Which plan item does it satisfy?
- What assumptions does it introduce?
- Is the change larger than necessary?

## Third pass

Inspect surrounding code, not just the changed lines. A locally correct edit may violate a nearby invariant.

## High-risk patterns

Watch for:

- authentication or authorization changes;
- input deserialization;
- shell commands;
- SQL construction;
- file deletion or overwrite;
- network calls;
- environment variable handling;
- concurrency changes;
- migrations;
- public API changes.

## Diff hygiene

Avoid accidental whitespace churn, generated artifacts without cause, debug logging, commented-out code, temporary files, and unrelated formatting.

## Verification linkage

Every material behavior change should have at least one corresponding verification item. When direct automation is unavailable, record the manual inspection or reason that verification could not be completed.

## Review conclusion

Use one of:

- `ready` — requested scope is verified enough for the current workflow;
- `blocked` — a material issue or missing approval prevents completion;
- `conditional` — work is usable only with an explicit documented caveat.
