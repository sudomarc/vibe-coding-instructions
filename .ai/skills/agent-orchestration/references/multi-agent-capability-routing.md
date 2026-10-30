# Multi-Agent Capability Routing & Provider Failover Governance

## Metadata
- **reference_id**: `multi_agent_capability_routing`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions

## Purpose
Establish standard governance policies for routing capabilities across multi-agent hierarchies, managing shared capability health state, handling provider degradation/failover during subagent delegation, and executing task redistribution cascades when a delegate or underlying provider encounters errors or circuit-breaker activations.

---

## 1. Architecture Overview

In a multi-agent orchestration setup, the Orchestrator delegates subtasks to specialist subagents (e.g. `researcher`, `coder`, `analyst`). Subagents consume capabilities (LLM inference, sandboxed execution, search APIs, git operations, browser tools) supplied by underlying providers.

```text
Orchestrator
  ├─ Shared Capability Health Cache
  ├─ Subagent Delegation & Task Redistribution Engine
  │
  ├── Delegate: Researcher ──> [Capability: Web Search / Browser QA]
  ├── Delegate: Coder ───────> [Capability: Code Editing / Sandbox Exec]
  └── Delegate: Analyst ─────> [Capability: Data Ingestion / Analysis]
```

---

## 2. Shared Capability Health Cache

To prevent subagents from repeatedly calling unhealthy or degraded capabilities/providers:

1. **Centralized Health State**: CHAD maintains a runtime Shared Capability Health Cache accessible to the Orchestrator and all active subagents.
2. **Health States**:
   - `PRESENT`: Provider discovered but unverified.
   - `CONFIGURED`: Provider credentials validated.
   - `HEALTHY`: Latency within bounds, error rate < 1%, 200 OK responses.
   - `DEGRADED`: Transient errors (1-10%) or elevated latency. Primary route used with retry budget; secondary fallback prepared.
   - `UNHEALTHY`: 3 consecutive failures within 60s or HTTP 5xx / timeout. Triggers circuit breaker and routes to fallback provider.
   - `INACTIVE`: Provider disabled or blacklisted.
3. **Cross-Agent Health Propagation**: When Subagent A observes a capability failure or trips a provider circuit breaker, the health update instantly invalidates the cache for Subagent B and Subagent C.

---

## 3. Dynamic Capability Discovery & Subagent Matching

When delegating a subtask, the Orchestrator evaluates:

- **Required Capability**: Specific tool or inference capability required (e.g., `code_execution_level_2`, `web_search_v1`).
- **Permission Tier Bounds**: Maximum allowed permission level (`READ_ONLY`, `WORKSPACE_WRITE`, `ISOLATED_EXECUTE`, `NETWORK_ACCESS`, `PRIVILEGED_MUTATION`).
- **Provider Health & Cost**: Route to the highest-health, lowest-cost provider currently marked `HEALTHY` or `DEGRADED`.
- **Fallback Cascade (`multi_agent_capability_fallback`)**: If primary provider for Subagent A becomes `UNHEALTHY`, automatically trigger multi_agent_capability_fallback to route Subagent A to secondary provider, or trigger orchestrator redistribution to reassign the subtask to an alternate delegate with equivalent capability.

---

## 4. Subagent Failure Escalation & Orchestrator Redistribution Cascades

When a subagent execution fails or encounters provider errors, the runtime triggers subagent escalation:

```text
Subagent Escalation Pipeline
  │
  ├── Step 1: Subagent local retry (max 3 retries with modified parameters/context)
  │
  ├── Step 2: If provider circuit breaker trips -> Update Shared Capability Health Cache to UNHEALTHY
  │
  └── Step 3: Subagent Escalation to Orchestrator
        │
        ├── Cascade 1 (`multi_agent_capability_fallback`): Re-route subagent to Fallback Provider for same capability
        ├── Cascade 2 (`orchestrator redistribution`): Orchestrator redistribution of subtask to alternate specialist subagent
        └── Cascade 3: If no viable alternative -> Trigger HUMAN_CHECKPOINT_REQUIRED
```

### 4.1 Subagent Escalation Protocol
1. **Subagent Escalation Trigger**: Subagent raises a `SUBAGENT_CAPABILITY_FAILURE` event containing error trace, tool name, provider ID, and retry history.
2. **Orchestrator Redistribution Policy**: The Orchestrator receives the escalation event, inspects the Shared Capability Health Cache, and executes orchestrator redistribution to reallocate workload away from failing nodes.
3. **Multi-Agent Capability Fallback (`multi_agent_capability_fallback`)**: Fallback pathways are pre-registered per capability ID. The Orchestrator evaluates available providers and applies `multi_agent_capability_fallback` rules before halting execution or escalating to human review.

---

## 5. Circuit Breaker Interaction across Multi-Agent Boundaries

1. **Subagent Circuit Breaker**: Activates if a subagent executes 3 consecutive identical tool/model errors or produces zero net state progress.
2. **Provider Circuit Breaker**: Activates after 3 consecutive HTTP 5xx errors, timeouts (>30s), or auth failures across any subagents sharing the provider.
3. **Recovery & Cooling Period**: Marked `UNHEALTHY` for 300 seconds. A probe request is sent after 300s; if successful, state transitions to `HEALTHY`.

---

## 6. Multi-Agent Capability Telemetry Schema

All multi-agent capability dispatches emit standardized telemetry log events:

```json
{
  "trace_id": "tr-20250330-multi-001",
  "orchestrator_id": "orchestrator-main",
  "subagent_id": "coder-01",
  "capability_id": "sandboxed_code_execution",
  "provider_id": "docker_sandbox_primary",
  "health_state": "HEALTHY",
  "action": "EXECUTE_TOOL",
  "status": "SUCCESS",
  "latency_ms": 142,
  "circuit_breaker_triggered": false,
  "timestamp": "2025-03-30T12:00:00Z"
}
```

---

## 7. CHAD & LapisLLM Runtime Compatibility

- **CHAD Enforcement**: CHAD manages the Shared Capability Health Cache, intercepts subagent capability failures, enforces provider fallback cascades, and logs multi-agent capability telemetry.
- **LapisLLM Inference**: LapisLLM serves as a primary or secondary model inference provider in the multi-agent cascade, advertising capabilities via `GET /v1/models`.
