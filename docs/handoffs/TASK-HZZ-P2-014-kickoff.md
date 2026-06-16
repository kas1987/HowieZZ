TASK_ID: HZZ-P2-014
PDR_PATH: docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md
OBJECTIVE: Unblock PR #31 by refreshing the tracked v2 HTML package after main-merge content changes.

## Scope
- Copy clean regenerated v2 HTML artifacts from a detached worktree at PR head.
- Commit package refresh only.
- Push and allow CI/auto-merge to continue.

## Acceptance
- v2 HTML freshness guard no longer fails.
- PR #31 required CI returns green or pending-only.
