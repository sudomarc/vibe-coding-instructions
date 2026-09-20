# Sources and Provenance

This repository is an original synthesis. It does not reproduce source projects wholesale.

## Anthropic

- Claude Code public repository and plugin development skill guidance: https://github.com/anthropics/claude-code
- Anthropic skills repository: https://github.com/anthropics/skills
- Public skill-development guidance explains `SKILL.md`, YAML metadata, trigger descriptions, progressive disclosure, and bundled resources.
- Public Claude Code review tooling demonstrates specialized review agents for comments, tests, errors, types, general code quality, and simplification.

## OpenAI Codex

- Codex repository: https://github.com/openai/codex
- Codex `AGENTS.md` implementation and prompt materials document scoped repository instructions and precedence.
- OpenAI Cookbook Codex workflows: https://github.com/openai/openai-cookbook
- The Cookbook includes iterative development and persistent-plan patterns for complex work.

## GitHub Copilot

- Custom instructions: https://docs.github.com/en/copilot/concepts/prompting/response-customization
- Custom instruction support: https://docs.github.com/en/copilot/reference/custom-instructions-support
- GitHub documents repository-wide `.github/copilot-instructions.md`, path-specific `.github/instructions/**/*.instructions.md`, prompt files, and supported agent instructions.

## Web development and design

- Vercel Labs frontend design skill: https://github.com/vercel-labs/open-agents/tree/main/.agents/skills/frontend-design
- Vercel web interface guidelines: https://github.com/vercel-labs/web-interface-guidelines
- Vercel agent skills ecosystem: https://github.com/vercel-labs/skills
- Vercel agent skills repository: https://github.com/vercel-labs/agent-skills
- Next.js version-matched agent skills guidance: https://github.com/vercel-labs/next-skills
- Next.js repository skills: https://github.com/vercel/next.js/tree/canary/skills
- WAI accessibility resources: https://www.w3.org/WAI/
- Web performance guidance: https://web.dev/explore/learn-core-web-vitals
- MDN Web Docs: https://developer.mozilla.org/
- Three.js documentation: https://threejs.org/docs/
- Babylon.js documentation: https://doc.babylonjs.com/
- Playwright screenshots and visual assertions: https://playwright.dev/docs/screenshots
- Percy visual testing: https://percy.io/
- Applitools visual AI testing: https://applitools.com/
- Blender manual: https://docs.blender.org/

## External capability / integration research

### Agent Reach

Reviewed source: https://github.com/Panniantong/Agent-Reach

The reviewed repository models a stable capability layer over changing external providers. Relevant observed patterns include ordered primary/fallback backends, a `doctor` diagnostic that distinguishes availability from a healthy active path, safe-by-default installation with explicit system mutation and dry-run modes, dedicated state directories instead of project-workspace pollution, explicit authentication/session boundaries, upstream public-contract usage, and tests for false-positive or half-broken provider states.

These patterns were adapted as general engineering guidance in:
- `.ai/skills/capability-routing/SKILL.md`
- `.ai/templates/capability-matrix.md`
- `.ai/agents/integration-health-reviewer.agent.md`

The source is treated as an external engineering case study, not as an authority or specification for this repository.
