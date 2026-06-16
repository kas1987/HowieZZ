# PDR Analytics Dashboard Cookbook

Status: Active
Date: 2026-06-06
Source schema: `docs/pdr/PDR-analytics-event-taxonomy.md`

## Purpose

Provide exact metric formulas for the compare-to-inquiry funnel using canonical events.

## Event Scope

Use records where:

- `source = howiezz-web`
- `schema_version = 2026-06-06`

## Core Metrics

### 0) Page Traffic Baseline

Definition:

- Count of `page_view`

Breakdowns:

- by `page`
- by `session_id` (unique sessions)

### 1) Compare Engagement

Definition:

- Numerator A: count of `compare_add`
- Numerator B: count of `compare_view` where `view_state = filled`

Suggested display:

- total compare adds
- total filled compare views
- compare adds per session = `count(compare_add) / count(distinct session_id)`

### 2) Compare Handoff Rate

Definition:

- Numerator: count of `compare_handoff_click`
- Denominator: count of `compare_view` where `view_state = filled`
- Formula: `handoff_rate = numerator / denominator`

Breakdowns:

- by `channel` (`contact`, `quiz`, `compare`)
- by `source_page`

### 3) Inquiry Submit Rate

Definition:

- Numerator: count of `inquiry_submit_success`
- Denominator: count of `inquiry_submit_attempt`
- Formula: `submit_rate = numerator / denominator`

Breakdowns:

- by `channel` (`mailto`, `endpoint`)
- by `intent`
- by `timeline`

### 4) Validation Friction Rate

Definition:

- Numerator: count of `inquiry_validation_failed`
- Denominator: count of `page_view` where `page = contact.html`
- Formula: `validation_friction_rate = numerator / denominator`

If page-view events are unavailable:

- fallback denominator: `count(inquiry_submit_attempt) + count(inquiry_validation_failed)`

### 5) Compare Set Churn

Definition:

- Add actions: count of `compare_set_changed` where `action = add`
- Clear actions: count of `compare_set_changed` where `action = clear`
- Churn ratio: `clear_actions / add_actions`

Breakdowns:

- by `context` (`compare`, `browse_list`)
- by `source_page`

### 6) Contact Attribution Quality

Definition:

- Distribution of inquiry events by `entry_source`, `entry_cta`, `entry_context`, `entry_channel`

Primary checks:

- events with non-empty `entry_source` / total contact submit attempts
- conversion rate by `entry_source`

Suggested starting target ranges (establish and tune with first 2-4 weeks of live data):

- Attribution coverage: at least 85% of `inquiry_submit_attempt` events include non-empty `entry_source`.
- Compare-origin inquiry share: 25% to 55% of inquiry attempts with `entry_source = compare`.
- Compare-origin submit rate: 35% to 65% (`inquiry_submit_success / inquiry_submit_attempt` where `entry_source = compare`).
- Non-attributed attempts: below 15% of total attempts.

## Suggested Time-Series Panels

1. `compare_add` daily volume
2. `compare_handoff_click` daily volume by `channel`
3. `inquiry_submit_attempt` vs `inquiry_submit_success` daily
4. `inquiry_validation_failed` daily
5. `compare_set_changed` by `action` daily
6. `page_view` daily by `page`

## SQL-Like Reference Queries

### Handoff rate by day

```sql
SELECT
  DATE(ts) AS d,
  SUM(CASE WHEN event = 'compare_handoff_click' THEN 1 ELSE 0 END) AS handoffs,
  SUM(CASE WHEN event = 'compare_view' AND view_state = 'filled' THEN 1 ELSE 0 END) AS compare_views_filled,
  CASE
    WHEN SUM(CASE WHEN event = 'compare_view' AND view_state = 'filled' THEN 1 ELSE 0 END) = 0 THEN 0
    ELSE 1.0 * SUM(CASE WHEN event = 'compare_handoff_click' THEN 1 ELSE 0 END)
         / SUM(CASE WHEN event = 'compare_view' AND view_state = 'filled' THEN 1 ELSE 0 END)
  END AS handoff_rate
FROM events
WHERE source = 'howiezz-web'
  AND schema_version = '2026-06-06'
GROUP BY DATE(ts)
ORDER BY d;
```

### Inquiry submit rate by channel

```sql
SELECT
  channel,
  SUM(CASE WHEN event = 'inquiry_submit_success' THEN 1 ELSE 0 END) AS submit_success,
  SUM(CASE WHEN event = 'inquiry_submit_attempt' THEN 1 ELSE 0 END) AS submit_attempt,
  CASE
    WHEN SUM(CASE WHEN event = 'inquiry_submit_attempt' THEN 1 ELSE 0 END) = 0 THEN 0
    ELSE 1.0 * SUM(CASE WHEN event = 'inquiry_submit_success' THEN 1 ELSE 0 END)
         / SUM(CASE WHEN event = 'inquiry_submit_attempt' THEN 1 ELSE 0 END)
  END AS submit_rate
FROM events
WHERE source = 'howiezz-web'
  AND schema_version = '2026-06-06'
GROUP BY channel
ORDER BY channel;
```

### Compare-origin submit rate

```sql
SELECT
  SUM(CASE WHEN event = 'inquiry_submit_success' AND entry_source = 'compare' THEN 1 ELSE 0 END) AS compare_success,
  SUM(CASE WHEN event = 'inquiry_submit_attempt' AND entry_source = 'compare' THEN 1 ELSE 0 END) AS compare_attempt,
  CASE
    WHEN SUM(CASE WHEN event = 'inquiry_submit_attempt' AND entry_source = 'compare' THEN 1 ELSE 0 END) = 0 THEN 0
    ELSE 1.0 * SUM(CASE WHEN event = 'inquiry_submit_success' AND entry_source = 'compare' THEN 1 ELSE 0 END)
         / SUM(CASE WHEN event = 'inquiry_submit_attempt' AND entry_source = 'compare' THEN 1 ELSE 0 END)
  END AS compare_submit_rate
FROM events
WHERE source = 'howiezz-web'
  AND schema_version = '2026-06-06';
```

## Data Hygiene Checks

1. `event_original` should be present for all rows.
2. `session_id` should be present for all rows.
3. `compare_count` should be non-negative for compare-related events.
4. `channel` should be present for `compare_handoff_click` and `inquiry_submit_success`.
5. `page_view` should appear once per page load.
6. Contact events routed from compare should include `entry_source=compare` and `entry_cta=ask_about_these_bodies`.

## Current Threshold Rationale

- `minAttributionCoverage = 0.8`: strict enough to catch broken contact attribution wiring while allowing normal early-stage traffic variation.
- `minTotalEvents = 8` on the positive fixture: ensures each core event family appears at least once in the canonical sample.
- `minPageViews = 2`: guards against fixture truncation that removes multi-page flow context.
- `minCompareAdd = 1`: confirms compare funnel entry events are still present.
- `minInquiryAttempts = 1`: guarantees at least one measurable conversion attempt in sanity data.

Calibration note:

- Keep these defaults conservative until 2-4 weeks of production telemetry are available, then tune only in `docs/pdr/PDR-analytics-sanity-thresholds.json`.
