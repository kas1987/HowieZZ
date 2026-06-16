# PDR-009: Six-Family Product Taxonomy

## Objective
Formalize the six-family system as the product taxonomy backbone.

## Families
- The Classic: balanced / first-time buyer / timeless hourglass.
- The Icon: glamour / camera-forward / editorial.
- The Muse: natural / hip-dominant / realism-forward.
- The Siren: bust-forward / fantasy / dramatic.
- The Empress: plush / abundant / full-bodied.
- The Sculpt: athletic / defined / muscular realism.

## Scope
- Document WHR/BWR thresholds.
- Map every body code to family status.
- Mark exact, near, estimated, manual-review, or unclassified.
- Define copy tone, visual treatment, CTAs, and buyer archetype by family.
- Produce machine-readable `db/family_taxonomy.json`.

## Acceptance criteria
- Every body code has a family status.
- In-development families are clearly marked.
- Estimated data is not represented as verified.
- Quiz, compare, character, and contact flows consume the same taxonomy.

## Dependencies
`db/body_profiles.json`, `db/body_types.json`, `db/characters.json`.

## Owner
Archivist + Auditor.
