# Claude Code Compatibility

Use `AGENTS.md` as the canonical project policy. Do not create a second conflicting policy in this file.

For Claude Code-specific task behavior, use the modular skills under `.ai/skills/`. Load only the matching skill and its required references. Skills follow a progressive-disclosure model with YAML metadata, a focused `SKILL.md`, and optional `references/`, `examples/`, `scripts/`, or `assets/` resources.

When a task concerns Claude Code itself, inspect the current official Claude Code documentation or repository before relying on remembered behavior. When a task concerns generic software engineering, use the portable rules in `AGENTS.md` and the relevant skill.

Recommended sequence:

1. Read `AGENTS.md`.
2. Read the applicable `.ai/core/` files when they are not already loaded.
3. Select the matching skill from `.ai/skills/`.
4. Read only the references required by that skill.
5. Inspect the repository before editing.
6. Plan, implement, verify, review, and report evidence.

Claude Code commands, agents, hooks, permissions, plugins, and skills are documented in `docs/claude-code.md` and the source-backed references listed in `docs/sources.md`.
