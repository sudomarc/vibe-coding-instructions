# Capability & Fallback Contract

This contract defines standard schemas, health states, routing rules, and fallback cascade semantics for external capabilities, CLI tools, MCP servers, SaaS/API providers, and multi-provider backends in the CHAD + LapisLLM ecosystem.

## Provider-neutral policy boundary

This contract provides standard policy schemas for tool capability routing and fallback handling.

```text
vibe-coding-instructions (.ai/contracts/capability-fallback.contract.md)
  -> defines capability schemas, provider health states, and fallback cascade semantics
  -> consumed by CHAD Capability Router & Orchestrator runtime
  -> compatible with LapisLLM model provider capabilities
```

## Capability Definition Schema

Every capability contract MUST define the abstract function independently of specific brand or provider implementations.

```yaml
capability_id: string          # e.g., "code_search", "browser_automation", "llm_inference"
description: string            # Human-readable purpose of the capability
required_operations: list[str]  # e.g., ["search_query", "fetch_content"]
output_schema: string           # Expected structured output shape or JSON Schema reference
authentication_tier: string     # NONE | USER_BEARER | API_KEY | OAUTH2 | BROWSER_SESSION
side_effect_level: string       # READ_ONLY | WORKSPACE_WRITE | ISOLATED_EXECUTE | NETWORK_ACCESS | PRIVILEGED_MUTATION
cost_tier: string               # FREE | LOW | MEDIUM | HIGH
```

## Provider Health States

An external provider MUST be classified into exactly one of the following health states based on active probes, not mere static installation or configuration presence:

| Health State | Definition | Routing Eligibility |
|---|---|---|
| `PRESENT` | Binary, library, or MCP server is installed on host/sandbox, but configuration and auth are unverified. | Ineligible for active routing |
| `CONFIGURED` | Credentials or configuration exist, but connectivity or health check probe has not run. | Ineligible until probe completes |
| `HEALTHY` | Probe succeeded within TTL. Provider operates within latency/error thresholds. | Eligible primary or fallback target |
| `DEGRADED` | Operational but exhibiting high latency, rate limits, or non-fatal partial errors. | Eligible secondary fallback |
| `UNHEALTHY` | Probe failed, auth expired, or consecutive error threshold exceeded. | Ineligible; trigger fallback cascade |
| `INACTIVE` | Explicitly disabled by user or application policy. | Ineligible |

## Health Check Probe Contract

Probes MUST be read-only, non-destructive, and low-cost. Probes MUST NOT consume scarce quotas, perform financial transactions, or mutate workspace state.

```yaml
probe_spec:
  type: READ_ONLY_PROBE          # PING | VERSION_CHECK | LIST_MODELS | STATUS_ENDPOINT
  timeout_ms: integer            # Default: 3000ms
  cache_ttl_seconds: integer     # Default: 300s (5 minutes)
  max_retries: integer           # Default: 1
```

## Fallback Cascade Specification

When a primary provider fails or transitions to `UNHEALTHY` or `INACTIVE`, the capability router MUST evaluate fallback providers in strict array order.

```yaml
capability_routing_policy:
  capability_id: string
  primary_provider: string
  fallback_cascade:
    - provider_id: string
      min_health_state: HEALTHY | DEGRADED
      degradation_penalty: float   # Cost or quality impact factor
      fallback_trigger:
        - ON_UNHEALTHY
        - ON_RATE_LIMIT
        - ON_TIMEOUT
        - ON_AUTH_FAILURE
  prohibited_substitutions: list[str] # Provider substitutions that violate semantic or privacy guarantees
```

### Fallback Invariants

1. **Semantic Equivalence**: A fallback provider MUST fulfill the required operations of the capability contract. A semantically weaker provider (e.g., regex search vs semantic AST search) MUST NOT be substituted silently without explicit agent notification.
2. **Permission Boundary**: A fallback provider MUST NOT require higher permission tiers (`side_effect_level`) than authorized for the primary task.
3. **Privacy & Data Boundary**: If a primary provider is local/air-gapped, routing to a public SaaS fallback MUST be explicitly authorized by application policy.
4. **Audit Logging**: Every fallback cascade execution MUST record a `tool_fallback_event` in the tool audit log containing: `capability_id`, `failed_provider`, `failure_reason`, `selected_fallback`, and `latency_ms`.

## Error Taxonomy for Capabilities

When a provider fails, the capability router MUST classify the error into one of the standard classifications:

- `NOT_INSTALLED`: Required binary, library, or server missing from runtime environment.
- `MISCONFIGURED`: Invalid configuration syntax, missing endpoint URL, or incompatible version.
- `AUTH_REQUIRED`: Credential missing, expired token, or unauthorized response (401/403).
- `RATE_LIMITED`: Provider returned 429 or quota exceeded response.
- `UPSTREAM_UNAVAILABLE`: Network failure, host unreachable, or 5xx server error.
- `BROKEN`: Unexpected output format, schema violation, or process crash.
- `ENVIRONMENT_RISK`: Sandbox policy or permissions forbid execution.
- `UNSUPPORTED`: Requested sub-operation not implemented by this specific provider.
