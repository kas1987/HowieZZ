# PDR Analytics Event Taxonomy

Status: Active
Date: 2026-06-06
Scope: Compare funnel and inquiry funnel instrumentation

## Purpose

Define a stable event schema and property contract for funnel analytics and dashboard mapping.

## Global Payload Contract

All `ZX.track(...)` events emit these global fields:

- `event`: canonical event name.
- `event_original`: raw event string passed by caller.
- `source`: fixed value `howiezz-web`.
- `schema_version`: fixed value `2026-06-06`.
- `session_id`: persistent analytics session identifier used across page transitions.
- `ts`: ISO timestamp in UTC.
- `page`: current page filename (for example `compare.html`).
- `path`: current browser path.

## Canonical Events

### `page_view`

Auto-emitted once per page load by shared runtime.

Required:

- `context` (`navigation`)
- `source_page`

### `compare_add`

When user adds a body architecture to compare set.

Required:

- `body_code`
- `compare_count`
- `context` (`body_detail`, `character_detail`, `compare`, `browse_list`)
- `source_page` (`body`, `character`, `compare`, `browse`)

Optional:

- `family`
- `series`
- `character_id`

### `compare_clear`

When user clears compare set.

Required:

- `context` (`compare` or `browse_list`)
- `source_page` (`compare` or `browse`)

Optional:

- `previous_count`

### `compare_set_changed`

When compare set membership changes in browse or compare surfaces.

Required:

- `action` (`add` or `clear`)
- `compare_count`
- `context` (`compare` or `browse_list`)
- `source_page` (`compare` or `browse`)

Optional:

- `body_codes`
- `previous_count` (clear actions)

### `compare_view`

When compare page renders a view state.

Required:

- `view_state` (`empty` or `filled`)
- `compare_count`
- `context` (`compare`)
- `source_page` (`compare`)

Optional:

- `body_codes` (comma-separated list)

### `compare_handoff_click`

When user exits compare into a next-step CTA.

Required:

- `channel` (`contact`, `quiz`, or `compare`)
- `cta` (`ask_about_these_bodies`, `take_match_quiz`, or `open_compare`)
- `compare_count`
- `context` (`compare` or `browse_list`)
- `source_page` (`compare` or `browse`)

Optional:

- `body_codes`

### `inquiry_validation_failed`

When contact form fails client validation.

Required:

- `context` (`contact_form`)
- `source_page` (`contact`)

### `inquiry_submit_attempt`

When contact form submit is attempted after passing validation.

Required:

- `context` (`contact_form`)
- `source_page` (`contact`)

Optional:

- `has_character_context` (boolean)
- `has_compare_context` (boolean)
- `intent`
- `timeline`
- `entry_source`
- `entry_cta`
- `entry_context`
- `entry_channel`
- `entry_compare_count`

### `inquiry_submit_success`

When inquiry submission is completed.

Required:

- `channel` (`mailto` or `endpoint`)
- `context` (`contact_form`)
- `source_page` (`contact`)

Optional:

- `entry_source`
- `entry_cta`
- `entry_context`
- `entry_channel`
- `entry_compare_count`

### `inquiry_submit_error`

When inquiry submission fails.

Required:

- `context` (`contact_form`)
- `source_page` (`contact`)

Optional:

- `error_message` (runtime-normalized from `message`, truncated)
- `entry_source`
- `entry_cta`
- `entry_context`
- `entry_channel`
- `entry_compare_count`

## Backward Compatibility Mapping

Runtime aliases in `assets/site.js` normalize old event names:

- `compare_add_from_body` -> `compare_add`
- `compare_add_from_character` -> `compare_add`
- `compare_add_from_compare_page` -> `compare_add`
- `compare_to_contact_click` -> `compare_handoff_click`
- `compare_to_quiz_click` -> `compare_handoff_click`
- `compare_view_empty` -> `compare_view`

## Dashboard Mapping (Suggested)

Primary funnel widgets:

1. Compare engagement: count of `compare_add`, count of `compare_view` where `view_state=filled`.
2. Compare handoff rate: `compare_handoff_click` / filled `compare_view`.
3. Contact conversion: `inquiry_submit_success` / `inquiry_submit_attempt`.
4. Validation friction: `inquiry_validation_failed` per `contact.html` sessions.
5. Channel split: success counts grouped by `channel`.
6. Compare state churn: count of `compare_set_changed` grouped by `action`.
7. Page traffic baseline: count of `page_view` grouped by `page`.

Recommended dimensions:

- `page`, `source_page`, `context`, `channel`, `body_code`, `body_codes`, `family`, `series`, `intent`, `timeline`, `action`, `session_id`, `entry_source`, `entry_cta`, `entry_context`, `entry_channel`, `entry_compare_count`.