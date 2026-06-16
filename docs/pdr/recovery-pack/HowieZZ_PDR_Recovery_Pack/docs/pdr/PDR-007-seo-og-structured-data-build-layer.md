# PDR-007: SEO, Open Graph, Sitemap, and Structured Data

## Objective
Make the static Atlas discoverable, shareable, and indexable.

## Scope
- Generate `sitemap.xml` from catalog data.
- Add canonical URL strategy.
- Add Open Graph and social metadata.
- Add JSON-LD where appropriate.
- Add per-character/per-body metadata.
- Document adult-content/18+ indexing guardrails.
- Add validation checklist/script.

## Acceptance criteria
- Sitemap includes core static pages and generated character/body URLs.
- Character pages have unique metadata.
- Generated metadata does not expose unintended private image paths.
- SEO generation can be rerun after catalog build.

## Dependencies
Build scripts and `db/*.json`.

## Owner
Archivist + Sentinel.
