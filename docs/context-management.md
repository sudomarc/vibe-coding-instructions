# Context Management

## Why session handoff exists

Long-lived agent sessions accumulate dead ends, failed fixes, stale assumptions, and redundant trajectory context. Compression can reduce size, but it does not replace an explicit state transfer.

## Operating model

    HEALTHY → CONTINUE
    PRESSURED → PRUNE/COMPACT
    DEGRADED → WRITE HANDOFF → RESET
    HANDOFF READY → READ → RE-INSPECT → CONTINUE

## Handoff versus compaction

Compaction reduces active context while preserving the current trajectory.

Handoff terminates that trajectory and transfers only durable state to a fresh session.

## Canonical handoff

Use .ai/templates/handoff.md. Preserve objective, repository state, instructions, decisions, changed files, verification evidence, failed attempts, risks, open questions, exact next actions, and completion criteria.

## Trust rule

The handoff is orientation data. Repository evidence remains the technical source of truth. A fresh session must re-inspect the repository before implementation.

## Failure preservation

Material failed attempts are durable project state. Preserve the attempt, observed result, cause of failure, and any condition for reconsideration.

## Provider neutrality

The protocol is provider-neutral. Host-specific reset commands such as Claude Code /clear belong in provider guidance; the lifecycle and handoff format do not.
