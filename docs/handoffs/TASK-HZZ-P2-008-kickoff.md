TASK_ID: HZZ-P2-008
PDR_PATH: docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md
OBJECTIVE: Complete final do-all pass by tying Community data to downloaded ZELEX knowledge base with CI schema/provenance checks and adding a Community Events page.

## Scope
- Add community data schema/provenance validator and run it in CI.
- Extend community data with source references to downloaded assets.
- Add community-events.html and data source db/community_events.json.

## Acceptance
- CI fails on malformed community data or missing provenance sources.
- Community content references documented source paths from local knowledge base.
- Community events page is reachable from community hub and validated.
