# Quickstart

Install this instruction system in an existing project in about five minutes.

## 1. Copy the entry point

Place `AGENTS.md` in the target repository root. Merge its rules with any existing project-specific governance rather than overwriting stronger local requirements.

## 2. Copy the policy tree

Copy `.ai/core/`, `.ai/skills/`, `.ai/templates/`, and `.ai/meta/` into the target project.

## 3. Add tool-specific entry points

For Claude Code, add or merge `CLAUDE.md` so it points to `AGENTS.md`.

For GitHub Copilot, add or merge `.github/copilot-instructions.md`.

For ChatGPT Projects, add the repository or instruction files to the project context. Treat `AGENTS.md` as the main policy entry point.

For Codex, make the repository available to the agent and keep `AGENTS.md` at the root.

## 4. Start a task

Use a prompt with a clear objective, constraints, and acceptance criteria. The agent should inspect instructions before changing files and produce a plan.

## 5. Verify

Before completion, require the agent to show:

- relevant checks run;
- their results;
- files changed;
- remaining uncertainty.

## Suggested local layout

```text
project/
├── AGENTS.md
├── CLAUDE.md
├── .ai/
│   ├── core/
│   ├── skills/
│   ├── templates/
│   └── meta/
└── .github/
    └── copilot-instructions.md
```

## Minimal adoption

Teams that do not want the full tree can start with `AGENTS.md` plus `.ai/core/`. Add skills only when a recurring workflow justifies them.

## Updating the policy

When changing a rule, update the most specific canonical file first. Search for duplicates before editing other entry points. Afterward, review cross-references and check that the condensed Copilot instructions still agree with core policy.
