TASK_ID: HZZ-P2-010
PDR_PATH: docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md
OBJECTIVE: Complete final best-practice loop: add check-mode sync semantics, render provenance panel on Community Events, and publish unified community data contract.

## Scope
- Add -CheckOnly behavior to sync_community_channels_from_reference.ps1.
- Add CI step that runs sync script in check mode.
- Show provenance summary panel on community-events.html.
- Add unified contract doc for channels, handles, and events JSON.

## Acceptance
- Check mode exits non-zero only when source exists and destination is stale.
- Community Events displays provenance status from KB metadata.
- Contract documentation is present for contributors.
