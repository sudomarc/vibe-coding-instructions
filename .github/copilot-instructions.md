# Repository Instructions for GitHub Copilot

Follow `AGENTS.md` as the canonical project policy when it is available in the repository.

Before changing code, inspect the repository and applicable instructions. Plan first, then implement small coherent batches. Reuse existing architecture and dependencies. Do not silently expand scope.

Verify changed behavior with the narrowest useful tests, type checks, linters, builds, or runtime checks. Inspect the final diff. Never claim a command or test ran unless it actually ran.

Treat destructive Git commands, production operations, credential changes, recursive deletion, destructive migrations, and remote command execution as high-risk. Follow `.ai/skills/safety/SKILL.md` before such actions.

Use the matching skill under `.ai/skills/` for planning, implementation, review, debugging, security, testing, database, API, frontend, backend, Git, dependencies, documentation, refactoring, performance, accessibility, release, research, incident response, and agent orchestration.

For path-specific conventions, inspect `.github/instructions/` when present.

Completion requires implementation within scope, relevant verification, final diff review, and explicit remaining uncertainty.
