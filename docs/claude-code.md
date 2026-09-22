# Claude Code Compatibility

Anthropic's public Claude Code material documents modular skills built around `SKILL.md` files with YAML metadata, explicit triggers, and optional bundled references, examples, scripts, and assets. This repository follows that shape while keeping its instructions original.

Anthropic's public tooling also demonstrates specialized agent roles for review and other tasks. This repository uses the same architectural idea through task-specific skills and optional orchestration guidance.

Claude Code-specific behavior can change between releases. For current behavior, consult the official Anthropic documentation or repository before relying on remembered details.

Sources: `docs/sources.md`.


## Claude Code + OpenRouter

When Claude Code is the host and OpenRouter is the gateway, use `docs/claude-code-openrouter.md` for the integration bootstrap, model verification, cache/session limitations, tool-search guidance, and $5 budget controls.

Claude Code remains the host: do not encode undocumented OpenRouter request fields such as `session_id` as though `AGENTS.md` can inject them into every request. Treat such controls as active only when the actual host/gateway exposes runtime evidence.

Current model selection must be verified. Anthropic currently lists Claude Sonnet 4 as retired and Claude Sonnet 4.6 as active, so "Sonnet 4.x" should normally resolve to Sonnet 4.6.

Sources: `docs/claude-code-openrouter.md`, `docs/sources.md`.
