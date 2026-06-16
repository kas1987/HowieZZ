TASK_ID: HZZ-P2-007
PDR_PATH: docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md
OBJECTIVE: Complete remaining best-practice hardening by enforcing v2 package freshness in CI and making Community page data-driven with official handle verification.

## Scope
- Add CI check to fail when v2 HTML package artifacts are stale.
- Move community channel definitions into db/community_channels.json.
- Add official-handle verification section on Community page.

## Acceptance
- CI fails when v2 HTML package is not refreshed.
- Community page renders from JSON data and degrades gracefully.
- Official handles section is visible and tracked for click analytics.
