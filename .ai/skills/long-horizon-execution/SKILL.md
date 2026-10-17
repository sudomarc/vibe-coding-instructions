---
name: long-horizon-execution
description: Governance and operational workflows for multi-session, multi-agent long-horizon engineering tasks. Defines phase transitions, research-to-code handoffs, context compaction, recovery semantics, and token budget controls.
---

# Long-Horizon Execution Skill

Use this skill when an engineering task spans multiple sessions, multi-role handoffs (Research → Architecture → Implementation → Verification), or high token budgets. It ensures execution continuity, context compaction discipline, failure recovery, and strict token budget enforcement.

---

## Operational Loop for Long-Horizon Tasks

```text
PHASE 1: DISCOVERY & RESEARCH
   │  Produce Research Dossier Artifact
   ▼
PHASE 2: ARCHITECTURAL SPECIFICATION
   │  Produce Implementation Roadmap & Checkpoints
   ▼
PHASE 3: BATCHED IMPLEMENTATION
   │  Incremental Commits + Verified Checkpoints
   ▼
PHASE 4: INTEGRATION & VERIFICATION
   │  End-to-End Verification + Test Suite
   ▼
PHASE 5: FINAL DIFF REVIEW & COMPLETION
```

---

## 1. Phase Gate Criteria

Transitions between phases are non-bypassable and require explicit evidence.

| Phase Transition | Gate Requirement | Output Artifact |
|---|---|---|
| **Phase 1 → Phase 2** | Research claims labeled `FACT`/`OBSERVED`/`VERIFIED` | `RESEARCH_DOSSIER` |
| **Phase 2 → Phase 3** | Plan broken into bounded, verifiable batches | `ARCHITECTURE_SPEC` |
| **Phase 3 → Phase 4** | Each implementation batch verified with passing tests | `IMPLEMENTATION_DIFF` |
| **Phase 4 → Phase 5** | All integration tests and static analysis pass | `VERIFICATION_LOG` |

---

## 2. Research-to-Code Phase Handoff Protocol

When handing off from Research to Implementation:

1. **Purge Conversational State**: Never pass raw user-agent conversation transcripts.
2. **Compile Research Dossier**: Format findings into a structured dossier conforming to `.ai/contracts/long-horizon-task.contract.md`.
3. **Verify Provenance**: Ensure every technical requirement in the dossier links to a verified file path, command output, or code symbol.
4. **Freeze Artifact Hash**: Record the checksum of the dossier in `.ai/templates/long-horizon-task.md` or active state file.

---

## 3. Context Compaction & State Preservation Rules

To prevent context rot and degraded model performance during long runs:

- **Utilization Threshold**: Trigger compaction when context utilization hits **70%**.
- **HOT State Preservation**: During compaction, retain only:
  - Current Task State & Active Phase
  - Verified Research Dossier Summary
  - Current Implementation Batch Goal
  - Last Verified Checkpoint Git SHA & Test Log
  - Active Technical Constraints and Non-Goals
- **COLD Context Pruning**: Discard old tool execution outputs, historical search results, past debugging logs, and intermediate terminal outputs.

---

## 4. Failure-Resume Recovery Protocol

When a long-running session crashes or encounters a timeout:

1. **Re-inspect Workspace State**:
   Run `git status` and `git log -1` to check repository state against the last recorded checkpoint SHA in the task state.
2. **Revert Unverified Mutated State**:
   If dirty, unverified changes exist from a crashed session, revert workspace state to the last verified Git SHA.
3. **Record Failure Observation**:
   Classify the failure according to `.ai/self-improvement/references/failure-taxonomy.md` (`PLAN_DEFECT`, `CONTEXT_EXCEEDED`, `INFRA_FAIL`, etc.).
4. **Resume with HOT Context Only**:
   Reload task state from `.ai/templates/long-horizon-task.md` or state store and continue execution at the current step.

---

## 5. Long-Horizon Cost & Token Budget Controls

- **Token Quota Allocation**:
  - Research: max 15% of total budget
  - Architectural Specs: max 10% of total budget
  - Implementation: max 50% of total budget
  - Verification: max 25% of total budget
- **Circuit Breaker**: If 3 consecutive implementation attempts fail verification, halt task execution, record a `CIRCUIT_BREAKER_TRIPPED` state, and request human review or architectural revision.
