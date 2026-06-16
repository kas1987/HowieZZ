# PDR Analytics Smoke Test Checklist

Status: Active
Date: 2026-06-06
Purpose: Verify analytics payload integrity after deploy.

## Preconditions

1. Serve site locally or in staging.
2. Ensure browser devtools is open on Network and Console.
3. Optional: add temporary listener:

```javascript
window.addEventListener('zx:track', (e) => console.log('zx:track', e.detail));
```

4. Optional automated sanity run on exported events:

```powershell
python scripts/analytics_event_sanity.py --input path\to\events.ndjson
```

PowerShell wrapper option:

```powershell
pwsh -File scripts/run_analytics_sanity.ps1 -Strict
```

Full suite wrapper (positive + negative path checks):

```powershell
pwsh -File scripts/run_analytics_sanity_suite.ps1
```

CI uses this same wrapper as the canonical gate command.

Reference sample:

```powershell
python scripts/analytics_event_sanity.py --input docs/pdr/PDR-analytics-sample-events.ndjson --strict --min-total-events 8 --min-page-views 2 --min-compare-add 1 --min-inquiry-attempts 1 --min-attribution-coverage 0.8
```

Negative-path sample (expected failure):

```powershell
python scripts/analytics_event_sanity.py --input docs/pdr/PDR-analytics-sample-events-broken.ndjson --strict
```

Low-attribution negative sample (expected failure):

```powershell
python scripts/analytics_event_sanity.py --input docs/pdr/PDR-analytics-sample-events-low-attribution.ndjson --strict --min-attribution-coverage 0.8
```

Notes:

- Script accepts NDJSON or JSON array files.
- Use `--pretty` for machine-friendly JSON output.
- Use `--strict` and `--min-*` flags for CI gating.
- Wrapper script centralizes default thresholds and Windows-safe input validation.
- CI artifact bundle name: `analytics-sanity-summaries`.
- Shared threshold config: `docs/pdr/PDR-analytics-sanity-thresholds.json`.

## Test Flow A: Page Views

1. Open index page.
2. Open browse page.
3. Open compare page.
4. Open contact page.

Expected:

- One `page_view` event on each page load.
- Each event includes: `session_id`, `schema_version`, `page`, `path`.

## Test Flow B: Compare Set Management

1. On browse, click Add to Compare for at least two cards.
2. Click Open Compare.
3. On compare page, add one more body.
4. Clear compare set.

Expected:

- `compare_add` events emitted on each add.
- `compare_set_changed` emitted with `action=add` and growing `compare_count`.
- `compare_handoff_click` emitted on browse Open Compare.
- `compare_clear` and `compare_set_changed` with `action=clear` on clear.

## Test Flow C: Contact Attribution

1. On compare page with a non-empty set, click Ask about these bodies.
2. Submit contact form with valid test data (mailto or endpoint path).

Expected:

- URL carries `src=compare`, `cta=ask_about_these_bodies`, `context=compare`, `channel=contact`.
- `inquiry_submit_attempt` includes:
  - `entry_source=compare`
  - `entry_cta=ask_about_these_bodies`
  - `entry_context=compare`
  - `entry_channel=contact`
  - `entry_compare_count` greater than 0
- `inquiry_submit_success` includes same entry fields.

## Required Field Checklist

For all events:

- `event`
- `event_original`
- `source`
- `schema_version`
- `session_id`
- `ts`
- `page`
- `path`

## Pass Criteria

1. No missing required global fields.
2. Canonical event names only in `event`.
3. `session_id` is stable across page transitions in one session.
4. Compare-to-contact attribution fields present for compare-routed inquiry submits.
5. No console errors triggered by tracking calls.
6. `scripts/analytics_event_sanity.py` reports no non-canonical events and no missing required global fields.
