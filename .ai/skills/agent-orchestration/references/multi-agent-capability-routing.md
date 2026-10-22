# Multi-Agent Capability Routing & Fallback Protocol

This reference defines how tool capabilities, health states, and fallback cascades propagate across multi-agent orchestration hierarchies in the CHAD + LapisLLM ecosystem.

## 1. Multi-Agent Capability Fallback Architecture

In a multi-agent hierarchy, capability execution occurs within delegated subagents (e.g., `researcher`, `coder`, `analyst`), while global workflow coordination remains with the `orchestrator`.

```text
               +-----------------------+
               |     Orchestrator      |
               | (Global Health Cache) |
               +-----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
  +---------------+                 +---------------+
  |  Researcher   |                 |     Coder     |
  | (Local Scope) |                 | (Local Scope) |
  +---------------+                 +---------------+
```

When a subagent encounters a capability failure (e.g., tool timeout, rate limit, provider outage):

1. **In-Agent Local Fallback**: If the subagent possesses an authorized fallback provider within its granted permission tier, it executes local fallback silently and logs a `tool_fallback_event`.
2. **Subagent Escalation**: If no local fallback is available or authorized, the subagent halts execution and escalates to the `orchestrator` with a structured `CAPABILITY_FAILURE` status.
3. **Orchestrator Redistribution**: The `orchestrator` updates the **Shared Capability Health Cache**, marks the provider `UNHEALTHY` across all active delegates, and either:
   - Re-routes the task to another subagent with an alternative capability profile; or
   - Re-configures the task to use a degraded capability mode; or
   - Escalates to `HUMAN_CHECKPOINT_REQUIRED` if no viable fallback exists.

---

## 2. Shared Capability Health Cache

To prevent redundant tool failures across subagents, the Orchestrator maintains a centralized **Shared Capability Health Cache**.

### Health Cache Semantics
- **Health States**: `PRESENT`, `CONFIGURED`, `HEALTHY`, `DEGRADED`, `UNHEALTHY`, `INACTIVE`.
- **Cache TTL**: Health states expire after a configurable TTL (default: 300 seconds).
- **Propagation**:
  - When any subagent observes an `UNHEALTHY` or `RATE_LIMITED` failure, it publishes a health update event to the Orchestrator.
  - The Orchestrator broadcasts updated health states to all currently active delegates before their next tool invocation.

---

## 3. Delegation Matrix & Permission Isolation

Capabilities granted to subagents MUST adhere to permission isolation rules:

| Agent Role | Allowed Permission Tiers | Primary Capability Domain | Fallback Boundaries |
|---|---|---|---|
| `orchestrator` | `READ_ONLY`, `ISOLATED_EXECUTE` | Workflow & Health Coordination | Cannot execute mutations directly; delegates re-routing |
| `researcher` | `READ_ONLY`, `NETWORK_ACCESS` | Web Search & Document Retrieval | Fallback from Primary API -> Fallback Search API -> Cached Search |
| `coder` | `WORKSPACE_WRITE`, `ISOLATED_EXECUTE` | Repository File Modification & Tests | Fallback from Lapis AST edit -> RegEx diff patch |
| `analyst` | `READ_ONLY` | Data Analysis & Inspection | Fallback from GPU acceleration -> CPU processing |

### Isolation Invariant
A subagent MUST NOT switch to a fallback provider that requires a higher permission tier (`side_effect_level`) than originally granted by the Orchestrator.

---

## 4. Multi-Agent Fallback Escalation Loop

```text
SUBAGENT TOOL FAILURE
  ├──> Local Fallback Available & Authorized?
  │      ├──> YES: Execute Local Fallback -> Log Fallback Telemetry -> Continue
  │      └──> NO: Escalate CAPABILITY_FAILURE to Orchestrator
  │
  └──> ORCHESTRATOR RECEIVES ESCALATION
         ├──> Update Shared Capability Health Cache (mark provider UNHEALTHY)
         ├──> Alternative Provider or Subagent Available?
         │      ├──> YES: Re-assign Subtask with Updated Provider Routing -> Resume
         │      └──> NO: Trigger HUMAN_CHECKPOINT_REQUIRED
```

---

## 5. Audit & Telemetry Schema

Every multi-agent capability fallback event MUST produce a telemetry record correlated with `trace_id` and `parent_agent_id`:

```json
{
  "event_type": "multi_agent_capability_fallback",
  "trace_id": "tr-2026-994821",
  "parent_agent_id": "orchestrator-main",
  "subagent_id": "researcher-sub-1",
  "capability_id": "web_search",
  "failed_provider": "google_search_v1",
  "failure_classification": "RATE_LIMITED",
  "selected_fallback": "duckduckgo_api",
  "fallback_scope": "LOCAL_SUBAGENT | ORCHESTRATOR_REDISTRIBUTED",
  "timestamp_iso": "2026-03-31T12:00:00Z"
}
```

---

## 6. CHAD Runtime & LapisLLM Compatibility

- **CHAD Engine**: Enforces Shared Capability Health Cache synchronization across concurrent subagent processes and logs multi-agent fallback telemetry.
- **LapisLLM Gateway**: Ingests degraded capability state signals in prompt context to adapt model reasoning during task generation.
