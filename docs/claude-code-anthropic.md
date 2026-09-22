# Claude Code + Anthropic API — Cost-Efficient Operating Profile

## Scope

Use this profile when Claude Code connects directly to the Anthropic API with API-key billing. It is the default provider-specific cost profile for this framework when the user uses Claude Code without an LLM gateway.

## Current verified facts — 2026-09-22

- Claude Sonnet 4.6 model ID: `claude-sonnet-4-6`.
- Sonnet 4.6 pricing: $3/M input tokens, $15/M output tokens.
- 5-minute prompt-cache writes: $3.75/M.
- 1-hour prompt-cache writes: $6/M.
- Prompt-cache reads: $0.30/M.
- Sonnet 4.6 supports a 1M-token context window; direct Anthropic API access has full access to it, subject to the account/API configuration.
- Claude Code automatically uses prompt caching unless it is explicitly disabled.
- With API-key billing, Claude Code uses a 5-minute cache TTL for the main conversation by default.
- Claude Code can explicitly set the main and subagent cache TTLs to `5m` or `1h`.
- Sonnet 4.6 supports effort levels `low`, `medium`, `high`, and `max`; Claude Code's default effort is `high`.
- Claude Code's `/usage` shows session token/cost information and prompt-cache statistics on sufficiently recent versions.
- Claude Code's `/insights` analyzes recent sessions and can reveal recurring cost/friction patterns.

Re-check current Anthropic pricing and Claude Code behavior before making a new financial commitment.

## Mandatory project bootstrap

At the start of every new project:

1. Use Claude Code as the host and connect directly to Anthropic when that is the configured account.
2. Default the main model to Sonnet 4.6 unless the task has a documented reason to use another model.
3. Start ordinary coding at `medium` effort when it preserves verified quality. Escalate to `high` or `max` only for tasks where deeper reasoning is likely to change the outcome.
4. Leave prompt caching enabled.
5. Keep the stable prefix stable: `CLAUDE.md`, core instructions, tool configuration, and durable project context should not be rewritten mid-session unless necessary.
6. Keep volatile logs, test output, timestamps, and task-specific state late in the context.
7. Keep the project cache TTL at `5m` by default. Use `1h` only when a session contains a large reusable context and the user routinely returns within an hour; the 1-hour write costs more.
8. Keep subagent cache TTL at `5m` by default.
9. Use Haiku for simple bounded subagent work when quality is sufficient; keep Sonnet for tasks requiring meaningful coding judgment.
10. For direct Anthropic API calls, set max_tokens explicitly for bounded-output requests. Treat it as the maximum output budget, and choose a value comfortably above the expected completion so normal work does not truncate.
11. Do not infer that an omitted output cap creates a hidden limiter or silently wastes tokens. The cap constrains maximum generated output; input, reasoning, cache, and tool-use accounting remain governed by their respective API semantics.
12. Do not use agent teams for ordinary work. Each teammate is a separate Claude Code instance and materially increases token consumption.
13. Use `/clear` between unrelated tasks rather than carrying stale context forward.
14. Use `/compact` at natural task boundaries when the history contains obsolete exploration.
15. Check `/usage` after expensive sessions and inspect cache hit rate before concluding that an optimization helped.
16. Never claim a dollar saving from cache/effort changes without observed usage evidence.

## Cache-preservation rules

Claude Code's cache is prefix-based. The system prompt and project context are placed before the conversation, and changes to model, effort, some tool definitions, plugins, and compaction can cause cache rebuilds.

Therefore:

- choose the model and effort before beginning a substantial task;
- avoid changing effort repeatedly during one long task;
- avoid adding/removing MCP servers mid-task;
- avoid enabling/disabling plugins mid-task unless required;
- avoid unnecessary Claude Code upgrades in the middle of a cost-sensitive work block;
- prefer `/rewind` when abandoning a path because it can preserve an already-cached prefix;
- remember that editing repository files does not itself invalidate the cached prefix.

## $5 budget policy

A $5 balance is a spend limit, not a session quota.

For Sonnet 4.6 at current list pricing:

- $5 corresponds to about 1.67M uncached input tokens if input were the only charge.
- $5 corresponds to about 333k output tokens if output were the only charge.
- Actual Claude Code turns also include reasoning/tool trajectory costs, so these are not promises of sessions.

The practical objective is to minimize:

`uncached context + output + reasoning + redundant tool calls + retries + unnecessary subagents`

while preserving verification.

## Recommended persistent project settings

A committed `.claude/settings.json` can set the model and economical defaults for everyone using the project:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-sonnet-4-6",
  "effortLevel": "medium",
  "promptCacheTtl": "5m",
  "subagentPromptCacheTtl": "5m"
}
```

This contains no secret. API credentials must stay outside the repository.

For a cost-sensitive private setup, the same values can be kept in `.claude/settings.local.json` instead.

## Verification commands

Use these inside Claude Code:

```text
/status
/usage
/context
/insights
```

`/status` confirms loaded settings, `/usage` exposes token/cost and cache statistics, `/context` shows context consumers, and `/insights` analyzes recent usage patterns.

## Official references

- Claude Code settings: https://code.claude.com/docs/en/settings
- Claude Code model configuration: https://code.claude.com/docs/en/model-config
- Claude Code costs: https://code.claude.com/docs/en/costs
- Claude Code prompt caching: https://code.claude.com/docs/en/prompt-caching
- Sonnet 4.6 model/pricing: https://platform.claude.com/docs/en/models/sonnet-4-6/overview
- Anthropic pricing: https://platform.claude.com/docs/en/about-claude/pricing
