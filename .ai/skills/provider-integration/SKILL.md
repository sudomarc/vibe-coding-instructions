---
name: provider-integration
description: >
  Use when adapting this instruction system to Codex, Claude Code, ChatGPT coding workflows, GitHub Copilot, or another agent host with different discovery and tooling semantics.
---

# Provider Integration Skill

## When to Use

Use when installing, adapting, or troubleshooting the instruction system for a specific coding-agent provider.

## When Not to Use

Do not use it to replace the provider's current official documentation or to assume identical behavior across hosts.

## Workflow

1. Identify the provider and exact product/surface.
2. Consult current primary documentation.
3. Identify supported instruction locations and precedence.
4. Map this repository's core, skills, references, and templates to those mechanisms.
5. Document capability gaps rather than inventing parity.
6. Verify the integration with a small representative task.

## Decision Rules

- Provider facts are version-sensitive.
- Provider-specific adapters must not silently change the portable core policy.
- Unsupported automatic skill loading must be handled explicitly.
- Real task verification outranks claimed compatibility.

## Checklists

- [ ] Current provider documentation consulted.
- [ ] Supported instruction mechanism identified.
- [ ] Precedence/discovery caveats documented.
- [ ] Portable fallback available.
- [ ] Representative verification performed where possible.

## Verification

Confirm the provider actually loads the intended instruction entry point and can access the referenced files in the target environment.

## Failure Modes

Assuming feature parity, relying on stale platform behavior, duplicating conflicting instructions, and confusing documentation support with runtime compliance.

## Reference Files

- `references/provider-matrix.md`

## Examples

- `examples/provider-adaptation.md`
