# Claude Code + OpenRouter

Use this guide when Claude Code is the coding host and OpenRouter is the model gateway.

## Architecture

```
Claude Code (host)
   ↓ Anthropic-compatible API
OpenRouter (gateway / routing / billing)
   ↓
Anthropic Claude Sonnet 4.6
```

Do not confuse host controls with gateway controls. Claude Code owns the agent loop, tools, context handling and session state. OpenRouter owns provider routing, billing and OpenRouter-specific request fields.

## Current model note

As of 2026-09-22, Anthropic lists Claude Sonnet 4 as retired and Claude Sonnet 4.6 as active. Use Sonnet 4.6 when the intent is "Sonnet 4.x". Re-check model availability before pinning a production configuration.

## Recommended Claude Code → OpenRouter environment

Keep credentials outside the repository. A shell profile, secret manager, or Claude Code user settings can hold them.

```sh
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="<OPENROUTER_API_KEY>"
export ANTHROPIC_API_KEY=""
export OPENROUTER_API_KEY="<OPENROUTER_API_KEY>"

# Gateway/model discovery through Claude Code
export CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1

# Reduce the amount of tool-definition context when supported by the host
export ENABLE_TOOL_SEARCH=true
```

OpenRouter documents this Anthropic-compatible Claude Code setup and the use of gateway model discovery/tool search. Verify the exact environment-variable behavior against the current Claude Code/OpenRouter documentation before applying it globally.

## Model selection

Prefer an explicit Sonnet 4.6 model in Claude Code's model selector when possible.

OpenRouter has documented:

```sh
export ANTHROPIC_DEFAULT_SONNET_MODEL="~anthropic/claude-sonnet-4.6"
```

However, a current Claude Code issue reports that `ANTHROPIC_DEFAULT_*_MODEL` aliases can be ignored with a custom `ANTHROPIC_BASE_URL`. Therefore:

1. Do not treat the environment variable alone as proof that Sonnet 4.6 is active.
2. Verify the effective model from Claude Code's `/model` UI or runtime evidence.
3. Record `UNVERIFIED` when the gateway does not expose enough evidence to confirm the selected model.

## Prompt caching

Prompt caching is valuable for long-lived Claude Code sessions because stable instructions, tool definitions and reusable context can repeat across turns.

Do this at the instruction level:

- Keep repository policy and stable reference material stable.
- Put changing task state, timestamps, logs and transient outputs after the stable material.
- Avoid unnecessary edits to the stable instruction prefix during a session.
- Do not add filler text to make a prompt cacheable.
- Do not claim a cache hit unless provider telemetry or another concrete runtime signal confirms it.

OpenRouter documents Anthropic cache reads at a lower rate than fresh input and recommends stable prefixes plus sticky routing/session IDs for multi-turn agents.

## session_id: important limitation

OpenRouter supports a `session_id` request field/header for sticky routing, but Claude Code does not document a general user setting that lets a repository instruction file inject that field into every request.

Therefore:

- Claude Code projects MUST preserve stable session/context structure.
- Do not fabricate `session_id` support in `AGENTS.md`, `CLAUDE.md`, or project scripts.
- If the selected Claude Code/OpenRouter integration exposes a supported session-ID control, use one stable value per workflow.
- Otherwise mark OpenRouter sticky-routing control as `UNVERIFIED` and rely on Claude Code's native session handling plus stable prompts.

## Tool/plugin cost policy

Do not enable every OpenRouter plugin.

Use only capabilities needed by the task:

- Web search: only for genuinely current external information; bound result volume.
- PDF inputs: only when a PDF must be processed.
- Context compression: fallback for oversized context, not a substitute for context discipline.
- Response Healing: use when structured output needs repair.
- Multi-model/Fusion: escalation only when independent model analysis has clear value.

OpenRouter's legacy Web Search plugin and `:online` route are deprecated for new integrations. Prefer the `openrouter:web_search` server tool when fresh search is required.

## $5 operating policy

With a $5 balance, optimize the full Claude Code trajectory:

```
context ↓   tool results ↓   retries ↓   unnecessary delegation ↓
output ↓    expensive plugins ↓   cacheable prefix ↑   cache hits ↑
```

Use Sonnet 4.6 for normal coding work, but avoid paying Sonnet rates for simple discovery, formatting or extraction when Claude Code/OpenRouter routing can safely use a cheaper model.

Do not define a fixed "number of sessions" for $5. Measure actual OpenRouter spend instead.

## Per-project bootstrap checklist

At the first Claude Code session in every project:

1. Read `AGENTS.md`.
2. Detect whether OpenRouter is the active gateway.
3. Detect the effective model in Claude Code.
4. Confirm that tool search is enabled when supported.
5. Keep the stable instruction prefix unchanged for the session.
6. Use only task-required plugins/tools.
7. At meaningful checkpoints, inspect actual usage/cost telemetry when available.
8. Before completion, report cost signals only from observed telemetry; otherwise label them estimates/unknown.

## References

- OpenRouter Claude Code / gateway setup: https://openrouter.ai/blog/announcements/ori-harness/
- OpenRouter prompt caching and sticky routing: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/
- Claude Code model configuration: https://docs.claude.com/en/docs/claude-code/model-config
- Claude Code environment configuration: https://docs.claude.com/en/docs/claude-code/settings
- Anthropic model lifecycle: https://docs.anthropic.com/en/docs/about-claude/model-deprecations
