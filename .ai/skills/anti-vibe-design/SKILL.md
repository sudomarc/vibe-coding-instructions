---
name: anti-vibe-design
description: This skill should be used when reviewing or refining web UI for generic AI-generated visual patterns, trend stacking, template-like styling or insufficient product-specific design rationale.
---

# Anti-Vibe Design Skill

Use this as a heuristic against interfaces that look assembled from a familiar AI/web-design trend stack rather than designed for the product.

The patterns below are not forbidden. Gradients, glass, serif accents, badges, icon libraries, motion and dark themes can all be appropriate. The rule is to require context, restraint, consistency and a product-specific reason instead of using them as defaults.

## Twenty patterns to inspect

### Visual styling
1. Purple-to-blue gradients used as a default visual identity.
2. Gradient-filled hero headlines used without a content or brand reason.
3. Emojis used as heading decoration instead of meaningful product language.
4. Inter used everywhere without checking whether it is the right typographic voice.
5. Cards distinguished mainly by arbitrary colored borders.

### Component and composition patterns
6. Glassmorphism cards used as the default surface treatment.
7. Dark mode with weak contrast, muddy hierarchy or insufficient state separation.
8. Repeated three-icon-card rows used as generic feature filler.
9. A small badge placed above nearly every headline without semantic value.
10. Lucide or another icon library used for nearly every visual element instead of a deliberate icon language.
11. Default shadcn/ui components shipped with minimal customization when the product has a distinct visual identity.

### Motion and interaction
12. Generic fade-in-on-scroll applied to most sections without hierarchy or narrative value.
13. Cursor-following beams, spotlights or glows added as decorative pointer effects.
14. Buttons that only fade or dim on hover instead of communicating a meaningful interactive state.

### Consistency and content
15. Inconsistent spacing, alignment, radii, control heights or component density.
16. Em dashes or other stylized punctuation repeated as a recognizable AI-copy habit rather than a deliberate editorial choice.
17. Generic buzzword copy that could describe almost any SaaS, startup or agency.
18. Serif italic accents inserted as a fashionable contrast without a clear typographic role.

### Typography and texture
19. Space Grotesk + Instrument Serif (or a similar trendy display/body pairing) used by default rather than from product requirements.
20. Grain/noise texture layered over gradients mainly to create a fashionable "premium" surface.

## Review method

1. **Understand context** — identify product, audience, brand constraints, content goals and existing visual language.
2. **Inspect the changed surface** — compare with existing tokens, components, typography, spacing and content patterns.
3. **Detect stacking** — multiple trend patterns together are stronger evidence of generic styling than one isolated pattern.
4. **Ask for rationale** — for each non-trivial decorative choice, identify the user value, brand reason or information-hierarchy function.
5. **Check alternatives** — prefer simpler or more product-specific treatments when the effect does not improve comprehension, identity or interaction.
6. **Verify states and viewports** — inspect responsive behavior, hover/focus/disabled/error states, contrast, text wrapping and reduced-motion behavior where applicable.
7. **Report evidence** — cite the exact surface and concrete visual/UX consequence. Do not reject a pattern solely because it appears on this list.

## Positive heuristics

- Establish one clear visual thesis before adding effects.
- Prefer a small set of distinctive design decisions over many fashionable effects.
- Use typography because of hierarchy, character and readability, not because a font pairing is currently common.
- Customize reusable primitives enough that the component language matches the product.
- Use motion to explain state, causality, continuity or narrative progression.
- Use decorative effects as accents, not as substitutes for hierarchy or content quality.
- Keep spacing, radii, shadows, border treatments and control dimensions systematic.
- Make copy specific to the product, user and task.
- Preserve a usable interface when animation, pointer effects or decorative layers are removed.

## Completion gate

Before completing a substantial visual change, identify any listed patterns that were introduced or retained. For each one, either document a concrete product/brand rationale or simplify the treatment. When several patterns appear together without a coherent design system, treat that as a signal to revisit the visual direction before polishing details.

Anti-vibe review is a quality heuristic, not a prohibition on contemporary web design.
