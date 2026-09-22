# Quickstart

## Install

Copy `AGENTS.md`, `CLAUDE.md`, `.ai/`, and the desired `.github/` files into the target repository. Preserve paths so references work.

## First Session

Open the project from its repository root. Read `AGENTS.md`. Inspect the target repository's own rules and tooling. Load only the skill matching the active task.

## Claude Code + Anthropic API bootstrap

At the first session of each project, use the direct Anthropic API configuration documented in `docs/claude-code-anthropic.md`.

Recommended project settings are `.claude/settings.json` with Sonnet 4.6, `medium` effort, and `5m` prompt-cache TTL. Claude Code manages prompt caching automatically. Use `1h` only when the reusable context justifies the higher cache-write cost.

Use `/status`, `/usage`, `/context`, and `/insights` to verify configuration, spend, cache behavior, context pressure, and recurring waste.


## First Feature

Ask the agent to inspect and plan the feature before implementation. Review the plan, then authorize implementation if your workflow requires explicit approval.

## Verification

Require the agent to run the repository's documented focused tests, relevant static checks, and broader verification appropriate to the risk. Require a final diff review.

## Long Tasks

Use `.ai/templates/handoff.md` when the task spans sessions. Use a living plan for multi-phase efforts.

## Copilot

Use `.github/copilot-instructions.md` for repository-wide instructions and `.github/instructions/` for path-specific rules where the client supports them.

## Offline or Prompt-Only Hosts

Paste `MASTER-PROMPT.md` as the operating prompt. Then provide the project-specific context separately.
