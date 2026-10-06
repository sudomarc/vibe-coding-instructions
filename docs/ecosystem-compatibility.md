# Ecosystem compatibility matrix

This matrix records observed public integration state. It is not a promise that every feature works in every environment.

| Component | Current state | Public capability | Consumer |
|---|---|---|---|
| Vibe Coding Instructions | main | policy, skills, role contracts | CHAD agents / coding agents |
| LapisLLM 0.2.0 | current verified repo release | model discovery + non-streaming chat HTTP; public runtime generation/streaming primitives | CHAD Model Gateway |
| CHAD | current development | conversation application + Lapis HTTP client; agent runtime planned | end users |

## Lapis -> CHAD compatibility currently observed

The current Lapis HTTP serving script exposes:

- GET /v1/models
- POST /v1/chat/completions

The current serving request supports model, messages, temperature, max_tokens, top_k and top_p.

The current HTTP serving path returns a completed chat response and does not expose an incremental HTTP streaming contract in that script.

Therefore:

- model discovery: PRESENT;
- non-streaming generation: PRESENT;
- context_length metadata: NOT ADVERTISED by the current /v1/models response;
- HTTP streaming: NOT VERIFIED / NOT EXPOSED by the current serving script;
- HTTP cancellation: NOT VERIFIED.

CHAD must not infer unsupported capabilities from the underlying Python runtime.

## Vibe -> CHAD compatibility

Vibe Coding Instructions currently provides portable skills, agent-role governance, tool governance, and model provider contracts. CHAD's planned runtime adapter will consume selected policy/role contracts.

State:

- role policy: PRESENT;
- tool governance contract: PRESENT;
- capability fallback contract: PRESENT (`.ai/contracts/capability-fallback.contract.md`);
- permission escalation controls: PRESENT (`.ai/skills/security/references/permission-escalation-controls.md`);
- model provider contract: PRESENT (`.ai/contracts/model-provider.contract.md`);
- runtime interface contract: PRESENT (`.ai/contracts/runtime-interface.contract.md`);
- runtime adapter: PLANNED;
- automatic synchronization of arbitrary framework files: NOT REQUIRED.

## Change protocol

When one capability changes materially:

1. update the owning repository's public contract;
2. update this matrix;
3. update the dependent adapter;
4. add or update integration tests;
5. record incompatibility or migration notes;
6. verify the public interface.

Unknown remains UNKNOWN until evidence exists.
