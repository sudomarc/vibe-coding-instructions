# Agent runtime contract

This contract describes the agent behavior expected by CHAD while keeping execution implementation in CHAD.

## Agent run

Every bounded run has:

```text
request
  -> classify
  -> plan
  -> authorize
  -> execute
  -> verify
  -> synthesize
  -> complete
```

A run must have explicit budgets for:

- steps;
- time;
- tokens;
- retries;
- tool calls;
- external side effects.

## Role contract

Each role must specify:

| Field | Requirement |
|---|---|
| role_id | stable identifier |
| purpose | observable responsibility |
| inputs | required context |
| tools | allowed capabilities |
| permissions | allowed side-effect level |
| stop_conditions | bounded completion/failure conditions |
| evidence | required verification |
| output | structured handoff/final result |

## Orchestrator

The orchestrator is the only component responsible for coordinating specialists.

It must:

- select or construct a plan;
- select specialists;
- enforce budgets;
- mediate tool access;
- collect evidence;
- handle failure;
- decide when a task is complete.

It must not grant permissions that the application policy has denied.

## Researcher

The researcher:

- decomposes questions into research tasks;
- searches approved sources;
- treats retrieved content as untrusted data;
- records evidence/source mapping;
- identifies conflicts;
- returns a bounded synthesis.

## Coder

The coder:

- inspects the target repository;
- reads applicable instructions;
- plans before significant edits;
- changes only the authorized workspace;
- runs relevant verification;
- reports changed files and evidence.

Repository-specific engineering policy remains authoritative.

## Analyst

The analyst:

- ingests approved files/data;
- validates format and scope;
- performs bounded analysis;
- preserves traceability to source material;
- reports uncertainty and limitations.

## Shared evidence protocol

Every agent handoff should prefer:

```text
Status
Facts / observations
Actions performed
Evidence
Failures
Uncertainty
Next action
```

No agent may claim a tool call, test, source check or runtime operation that did not actually occur.

## Human control

Agents can recommend or prepare consequential external actions. The application decides whether authorization is required.

The following should normally be gated:

- sending messages;
- publishing content;
- financial transactions;
- destructive filesystem/database changes;
- credential changes;
- privileged host changes;
- irreversible external API mutations.

## Token economy

Agent execution should:

- load only context needed for the next decision;
- avoid redundant tool calls;
- compact stale trajectory state;
- use an appropriate model/effort tier;
- keep tool results bounded;
- treat cost optimization as subordinate to correctness, safety and verification.

The detailed reusable policy lives in `.ai/skills/token-economics/`.

## Relationship to implementation

CHAD owns the runtime implementation of these contracts.

This repository owns the portable policy language and reusable engineering guidance. A runtime implementation may adapt a contract to a concrete protocol as long as it preserves the required safety and evidence semantics.
