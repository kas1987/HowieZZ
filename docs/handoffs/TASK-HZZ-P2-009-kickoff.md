TASK_ID: HZZ-P2-009
PDR_PATH: docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md
OBJECTIVE: Finish remaining do-all hardening: community-events schema guard in CI, last-verified timestamp in community UI, and reference-sync script for community channels.

## Scope
- Add validator for db/community_events.json and wire into CI.
- Render last verified timestamp in community.html from db/community_channels.json meta.
- Add script to sync db/community_channels.json from downloaded ZELEX reference source when available.

## Acceptance
- CI fails on malformed community events data.
- Community page displays provenance timestamp.
- Sync script supports safe no-op when source file is unavailable.
