# PDR Analytics Dashboard Handoff Runbook

Status: Active
Date: 2026-06-06
Audience: Dashboard implementers and data engineering owners

## Ownership

- Product owner: Howie (CEO sponsor)
- Analytics owner: Growth Lead (interim)
- Data engineering owner: Web/Data Engineering Lead (interim)
- Last reviewed on: 2026-06-06
- Next review date: 2026-06-13

## Objective

Move from instrumented website events to an operational dashboard with validated metrics.

## Source Artifacts

1. Taxonomy contract: `docs/pdr/PDR-analytics-event-taxonomy.md`
2. Metric formulas: `docs/pdr/PDR-analytics-dashboard-cookbook.md`
3. Validation checklist: `docs/pdr/PDR-analytics-smoke-test-checklist.md`
4. Current implementation status: `docs/pdr/PDR-implementation-audit.md`

## Handoff Steps

1. Confirm ingestion pipeline captures all payload keys with no schema truncation.
2. Verify `schema_version = 2026-06-06` and `source = howiezz-web` filters are available.
3. Validate smoke-test flow in staging and capture sample payloads.
4. Build dashboard panels defined in cookbook.
5. Publish target ranges and alert thresholds with product/marketing owners.

## Validation Commands

Positive-path sample:

1. `python scripts/analytics_event_sanity.py --input docs/pdr/PDR-analytics-sample-events.ndjson --strict --min-total-events 8 --min-page-views 2 --min-compare-add 1 --min-inquiry-attempts 1 --min-attribution-coverage 0.8`
2. `pwsh -File scripts/run_analytics_sanity.ps1 -Strict`
3. `pwsh -File scripts/run_analytics_sanity_ci_parity.ps1`

Artifact outputs:

- CI summaries: `.artifacts/analytics/*.json` (uploaded as workflow artifact `analytics-sanity-summaries`)
- Local suite summaries: `.artifacts/analytics/*-summary.local.json`

Negative-path sample (should fail):

1. `python scripts/analytics_event_sanity.py --input docs/pdr/PDR-analytics-sample-events-broken.ndjson --strict`

## Required Fields (Minimum)

Global:

- `event`
- `event_original`
- `source`
- `schema_version`
- `session_id`
- `ts`
- `page`
- `path`

Funnel-specific:

- `compare_count`
- `view_state`
- `channel`
- `context`
- `source_page`
- `entry_source`
- `entry_cta`
- `entry_context`
- `entry_channel`
- `entry_compare_count`

## Panel Build Order

1. Traffic baseline (`page_view` by page)
2. Compare engagement (`compare_add`, `compare_view`)
3. Compare handoff (`compare_handoff_click`)
4. Inquiry lifecycle (`inquiry_submit_attempt`, `inquiry_submit_success`, `inquiry_submit_error`)
5. Validation friction (`inquiry_validation_failed`)
6. Compare set churn (`compare_set_changed`)
7. Attribution quality (`entry_source`, `entry_cta`)

## QA Sign-Off Criteria

1. No missing required global fields in sampled records.
2. `session_id` remains consistent across multi-page journeys.
3. Compare-to-contact route preserves attribution fields into inquiry events.
4. Metric values match cookbook SQL reference for the same date window.
5. Dashboard refresh cadence and latency are documented.

## Operational Notes

- Debug mirror can be enabled in browser with `?zx_analytics_debug=1` and disabled with `?zx_analytics_debug=0`.
- Keep schema changes additive where possible; bump `schema_version` for breaking changes.
- Threshold and fixture defaults are centralized in `docs/pdr/PDR-analytics-sanity-thresholds.json`.
- Wrapper scripts read this config and now fail fast on missing required sections or invalid threshold ranges.

## Troubleshooting

### Exit code 2 from analytics sanity wrappers

Common causes:

- Config file path is missing or mistyped.
- Config JSON is malformed and cannot be parsed.
- Required sections/fixture input paths are missing.
- Attribution coverage thresholds are outside `[0, 1]`.

Quick checks:

1. Validate config file exists at `docs/pdr/PDR-analytics-sanity-thresholds.json`.
2. Run: `pwsh -File scripts/run_analytics_sanity_suite.ps1`.
3. For negative-test sanity, run: `pwsh -File scripts/run_analytics_sanity_suite.ps1 -ConfigPath docs/pdr/PDR-analytics-sanity-thresholds.invalid.json` and confirm exit code `2`.

Known error map:

| Error text | Likely cause | Primary fix |
| --- | --- | --- |
| `Missing config file: ...` | Config path typo or missing file | Confirm path and file existence, then rerun wrapper |
| `Failed to parse config file: ...` | Invalid JSON syntax | Fix JSON formatting and validate with `ConvertFrom-Json` |
| `Config file missing required sections: positiveFixture/negativeFixtures` | Required top-level blocks absent | Restore required sections in config |
| `Config file missing required fixture input paths.` | One or more required `input` fields missing | Add fixture input paths for positive, broken, and low-attribution fixtures |
| `Attribution coverage thresholds must be between 0 and 1.` | Threshold values outside valid range | Set attribution thresholds within `[0, 1]` |
