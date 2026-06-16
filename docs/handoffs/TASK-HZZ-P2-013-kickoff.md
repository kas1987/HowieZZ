TASK_ID: HZZ-P2-013
PDR_PATH: docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md
OBJECTIVE: Unblock PR #31 CI by making community provenance source_refs repository-resolvable in CI checkout.

## Scope
- Update db/community_channels.json source_refs to point only to tracked repository paths.
- Re-run validators and push fix.
- Confirm PR #31 status moves from failed check to pending/green.

## Acceptance
- validate-community-data passes in local run.
- PR #31 CI check is no longer failing on missing source_refs path.
