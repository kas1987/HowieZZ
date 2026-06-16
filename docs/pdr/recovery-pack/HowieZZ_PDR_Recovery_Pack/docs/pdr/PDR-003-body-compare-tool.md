# PDR-003: Body Compare Tool

## Objective
Create a first-class comparison workflow for body architectures.

## Scope
- Add `compare.html`.
- Add Compare nav link.
- Allow user to compare 2-4 body codes.
- Persist compare selection in localStorage.
- Compare height, weight, cup, family, WHR, BWR, bust drop, handling class, and confidence.
- Add contact handoff via `?compare=BODY1,BODY2`.

## Acceptance criteria
- Compare page works from static server.
- Table is readable on mobile via horizontal overflow.
- Missing/estimated data is clearly marked.
- Contact link preserves compare body codes.
- Compare can be expanded later from body/character cards.

## Dependencies
`db/characters.json`, `db/body_profiles.json`, `db/body_types.json`, `assets/site.js`.

## Owner
Cartographer + Sentinel.
