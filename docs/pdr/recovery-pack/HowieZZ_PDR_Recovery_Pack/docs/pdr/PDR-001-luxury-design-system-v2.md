# PDR-001: Luxury Design System v2

## Objective
Upgrade HowieZZ from a polished static catalog into a premium private-atelier frontend.

## Current state
Design System v2 tokens and status primitives appear partially present in `assets/site.css`, but usage is incomplete.

## Scope
- Standardize semantic tokens for surfaces, borders, shadows, spacing, status, family colors, and premium CTAs.
- Normalize card, body-card, quiz, compare, form, and character-page primitives.
- Add live/concept/shoot-pending/verified/estimated visual states.
- Preserve no-JS and reduced-motion safe behavior.

## Acceptance criteria
- Shared primitives are centralized in `assets/site.css`.
- All primary pages use consistent button, card, chip, and status classes.
- Accessibility focus states are visible.
- Mobile layouts remain stable.
- No image-missing state appears broken.

## Dependencies
`assets/site.css`, `assets/site.js`, all HTML pages.

## Owner
Cartographer + Sentinel.
