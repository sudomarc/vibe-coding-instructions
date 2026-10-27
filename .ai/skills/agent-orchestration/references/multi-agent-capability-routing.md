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
- **Fallback Cascade**: If primary provider for Subagent A becomes `UNHEALTHY`, automatically route Subagent A to secondary provider, or redistribute subtask to an alternate delegate with equivalent capability.

---

## 4. Subagent Failure Escalation & Redistribution Cascades

When a subagent execution fails or encounters provider degradation or circuit-breaker events:

```text
Subagent Error / Timeout
  │
  ├── Try local retry (max 3 retries with modified parameters/context)
  │
  ├── If provider circuit breaker trips -> Update Shared Capability Health Cache to UNHEALTHY
  │
  └── Subagent Escalation to Orchestrator
        │
        ├── Cascade 1: Re-route subagent via multi_agent_capability_fallback
        ├── Cascade 2: Orchestrator Redistribution to alternate specialist subagent
        └── Cascade 3: If no viable alternative -> Trigger HUMAN_CHECKPOINT_REQUIRED
```

### 4.1 Subagent Escalation Protocol
When local retries are exhausted or a provider circuit breaker activates, the delegate generates a structured **subagent escalation** payload sent to the Orchestrator:

```json
{
  "escalation_event": "subagent_escalation",
  "failed_subagent_id": "coder-01",
  "capability_id": "sandboxed_code_execution",
  "provider_id": "docker_sandbox_primary",
  "error_type": "PROVIDER_TIMEOUT",
  "retry_count": 3,
  "circuit_breaker_triggered": true,
  "context_snapshot": "Executed pytest run; 3 consecutive timeouts > 30s.",
  "timestamp": "2025-03-30T12:05:00Z"
}
```

### 4.2 Multi-Agent Capability Fallback Execution Rules (`multi_agent_capability_fallback`)
1. **Fallback Cascade Resolution**: The Orchestrator evaluates `multi_agent_capability_fallback` policy to select an alternative provider offering equivalent capability (e.g., falling back from `docker_sandbox_primary` to `gvisor_sandbox_secondary` or an alternative LLM backend).
2. **Health Cache Invalidation**: The primary provider is marked `UNHEALTHY` in the Shared Capability Health Cache, causing immediate failover across all concurrent subagents.

### 4.3 Orchestrator Redistribution
If no alternative provider exists for the requested capability, the Orchestrator performs **orchestrator redistribution**:
1. **Re-assignment to Alternate Delegate**: Re-assigns the subtask to another delegate (e.g. re-routing a web search subtask from `researcher-01` to `analyst-01` equipped with offline document lookup tools).
2. **Task Scope Decomposition**: Decomposes the blocked subtask into smaller, lower-overhead subtasks that consume lower-tier capabilities.
3. **Escalation to Human Checkpoint**: If orchestrator redistribution fails or all fallback routes are exhausted, the task transitions to `HUMAN_CHECKPOINT_REQUIRED`.

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
