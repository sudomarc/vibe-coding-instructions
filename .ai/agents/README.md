# Web Development & Design Agent Catalog

Provider-neutral agent profiles. Hosts can map these profiles to native primary-agent and subagent systems.

## Kinds

- primary: owns a user-facing workflow or final integration.
- subagent: performs a bounded specialist task.
- reviewer: read-oriented specialist focused on evidence-backed findings.

## Primary agents

- web-architect
- design-director
- frontend-builder
- web-quality-orchestrator

## Specialist agents

- token-economics-reviewer

- ui-reviewer
- anti-vibe-reviewer
- legal-compliance-reviewer
- responsive-reviewer
- accessibility-reviewer
- visual-qa
- visual-regression-reviewer
- performance-auditor
- motion-3d-specialist
- asset-pipeline-specialist
- seo-auditor
- web-security-reviewer
- nextjs-specialist
- forms-ux-reviewer
- component-reviewer
- browser-tester

## Default pipeline

REQUEST → DESIGN DIRECTION → ARCHITECTURE → IMPLEMENT → BROWSER VERIFY → SPECIALIST REVIEW → INTEGRATE → FINAL DIFF

## High-value routing

- Substantial visual redesign: ui-reviewer + anti-vibe-reviewer + visual-qa
- Compliance-sensitive flows: legal-compliance-reviewer + relevant technical reviewer
- Advanced animation or 3D: motion-3d-specialist + visual-qa + performance-auditor
- Asset-heavy interface: asset-pipeline-specialist + performance-auditor
- Screenshot baseline or regression: visual-regression-reviewer + browser-tester
- Responsive work: responsive-reviewer + visual-qa
- Accessibility-sensitive UI: accessibility-reviewer
- Forms/auth: forms-ux-reviewer + accessibility-reviewer + browser-tester
- Next.js rendering/cache: nextjs-specialist + performance-auditor
- Public pages: seo-auditor + performance-auditor
- Browser trust boundary: web-security-reviewer

Do not invoke every specialist by default. Route by changed surface and risk.
