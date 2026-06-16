# Community Knowledge-Base Linkage

## Short Answer
Yes. The Community hub is now tied to downloaded ZELEX knowledge-base assets.

## Linked Sources
- [_local/reference/zelexdoll-theme](_local/reference/zelexdoll-theme): downloaded storefront/theme reference.
- [db/competitor_web_scrape.json](db/competitor_web_scrape.json): downloaded scrape corpus containing ZELEX rows.
- [docs/research/source-log.md](docs/research/source-log.md): source provenance log.

## Where Linkage Is Enforced
- Community data file includes explicit source references:
  - [db/community_channels.json](db/community_channels.json)
- CI validates schema and source-provenance path existence:
  - [.github/scripts/validate-community-data.mjs](.github/scripts/validate-community-data.mjs)
  - [.github/workflows/ci.yml](.github/workflows/ci.yml)

## Rendering Surfaces
- [community.html](community.html): data-driven channel and handle verification cards.
- [community-events.html](community-events.html): curated event schedule from [db/community_events.json](db/community_events.json).

## Operational Note
When direct live endpoints are unstable or redirect-gated, community links can route through concierge-confirmation paths until canonical URLs are verified.
