# Ecosystem Agent Role Contracts

This directory contains provider-neutral, portable role contracts for AI agents operating in the CHAD + LapisLLM ecosystem.

## Governance Architecture

```text
Vibe Coding Instructions (.ai/contracts/)
  ├─ Shared Vocabulary & Protocols (README.md)
  ├─ Orchestrator Contract (orchestrator.contract.md)
  ├─ Researcher Contract (researcher.contract.md)
  ├─ Coder Contract (coder.contract.md)
  ├─ Analyst Contract (analyst.contract.md)
  └─ Tool Governance Contract (tool.contract.md)
        │
        ▼ (Enforced at Runtime)
  CHAD Agent Runtime
        │
        ▼ (Inference Gateway)
  LapisLLM Model Runtime
```

---

## 1. Permission-Level Vocabulary

To prevent unauthorized side-effects and clarify boundary enforcement, all agent roles declare permissions from this standard taxonomy:

| Permission Level | Description | Allowed Actions | Restricted Actions |
|---|---|---|---|
| `READ_ONLY` | Pure inspection and synthesis | Reading workspace files, executing read-only tools, querying search indexes | Writing files, executing state-changing commands, network mutations |
| `WORKSPACE_WRITE` | Local file modifications | Modifying/creating/deleting project files within authorized workspace root | Executing arbitrary host commands, network calls, modifying outside root |
| `ISOLATED_EXECUTE` | Bounded sandbox execution | Running local build/test tools, linters, sandboxed scripts | Accessing host OS directly, network egress, privilege escalation |
| `NETWORK_ACCESS` | Approved external connectivity | Querying allowed APIs, web search, fetching documentation | Sending unapproved outbound payloads, credential exfiltration |
| `PRIVILEGED_MUTATION` | High-risk system state changes | Modifying production resources, Git force actions, database migrations | Requires explicit human checkpoint authorization |

---

## 2. Stop-Condition Conventions

Every agent execution loop must terminate predictably under one of five standard stop conditions:

1. `SUCCESS_VERIFIED`
   - **Trigger**: Target objective is achieved and confirmed with concrete verification evidence.
   - **Action**: Return structured handoff with status `SUCCESS` and verified evidence.

2. `MAX_BUDGET_REACHED`
   - **Trigger**: Step, token, time, or tool call limit reached before full completion.
   - **Action**: Yield execution back to Orchestrator with `PARTIAL` status, current state, and exact next actions.

3. `GOAL_BLOCKED`
   - **Trigger**: Unresolved ambiguity, missing dependency, or contradictory constraints encountered.
   - **Action**: Halt execution, document `BLOCKED` status, and list open questions or required context.

4. `SAFETY_TRIGGERED`
   - **Trigger**: High-risk action detected, untrusted prompt injection attempt, or credential boundary violation.
   - **Action**: Immediately abort execution, record `SAFETY_VIOLATION`, and notify host runtime/user.

5. `HUMAN_CHECKPOINT_REQUIRED`
   - **Trigger**: Action requires `PRIVILEGED_MUTATION` or explicit user confirmation.
   - **Action**: Suspend execution, present exact proposed action and risk assessment to user.

---

## 3. Tool Governance & Trust Schema

All tools available to agents follow `.ai/contracts/tool.contract.md` which categorizes tools by permission levels (`READ_ONLY`, `WORKSPACE_WRITE`, `ISOLATED_EXECUTE`, `NETWORK_ACCESS`, `PRIVILEGED_MUTATION`), side-effect risk (`NO_EFFECT`, `REVERSIBLE_FILE_CHANGE`, `IRREVERSIBLE_HOST_MUTATION`, `NETWORK_TRANSACTION`), and result trust labeling (`VERIFIED_LOCAL`, `UNTRUSTED_REMOTE`, `ISOLATED_SANDBOXED`).

## 4. Evidence Protocol Schema

All facts, results, and claims reported in agent handoffs must use the standardized evidence labels:

```json
{
  "status": "SUCCESS | PARTIAL | BLOCKED | SAFETY_VIOLATION | FAILED",
  "evidence": [
    {
      "label": "FACT | OBSERVED | VERIFIED | INFERENCE | ASSUMPTION | UNKNOWN | CONFLICT | UNVERIFIED",
      "statement": "Description of claim or result",
      "source": "Tool call name, test output, or file path",
      "timestamp": "ISO-8601 UTC timestamp or step index"
    }
  ]
}
```

### Label Definitions
- `FACT`: Immutable repository property or baseline configuration.
- `OBSERVED`: Raw output collected directly from tool execution or file inspection.
- `VERIFIED`: Confirmed passing test, successful build, or verified behavioral outcome.
- `INFERENCE`: Logical conclusion derived from observed facts.
- `ASSUMPTION`: Working hypothesis requiring verification before final completion.
- `UNKNOWN`: Missing piece of context or uninspected state.
- `CONFLICT`: Contradictory information between sources or instructions.
- `UNVERIFIED`: Claim or code change not yet checked with real evidence.

---

## 5. Ecosystem Compatibility (CHAD & LapisLLM)

### CHAD Runtime Layer
- CHAD enforces contract permissions dynamically at the tool dispatch boundary.
- CHAD uses stop conditions to drive state machine transitions and subagent delegation loops.
- CHAD parses the structured handoff schema to pass state between agents without context inflation.

### LapisLLM Model Layer
- LapisLLM receives contract requirements as system context and output constraints.
- LapisLLM's inference gateway applies output token limits matching agent role budgets.
- LapisLLM provides structured tool-calling schema validation ensuring role outputs match contract schemas.
