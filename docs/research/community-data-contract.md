# Community Data Contract

## Purpose
Define contributor-facing contract for all community data files rendered by web pages and validated in CI.

## Files
- [db/community_channels.json](db/community_channels.json)
- [db/community_events.json](db/community_events.json)

## community_channels.json

### Required top-level keys
- `meta` (object)
- `channels` (non-empty array)
- `official_handles` (array)

### meta fields
- `generated_utc` (string, ISO-style UTC timestamp preferred)
- `source_refs` (array of objects)
  - each object requires:
    - `path` (string, existing path in workspace)
    - `kind` (string)
- `notes` (string, optional but recommended)

### channels[] required fields
- `name`
- `purpose`
- `status`
- `cadence`
- `primary`
- `secondary`
- `primaryLabel`
- `secondaryLabel`

Field constraints:
- All required fields are non-empty strings.
- `primary` / `secondary` can be HTTP(S) URLs or local paths (+ optional query string).
- Local-path targets must exist.

### official_handles[] required fields
- `platform`
- `handle`
- `url`
- `verification`

Field constraints:
- All required fields are non-empty strings.
- `url` can be HTTP(S) URL or local path (+ optional query string).

## community_events.json

### Required top-level keys
- `events` (non-empty array)

### events[] required fields
- `title`
- `date` (format `YYYY-MM-DD`)
- `mode`
- `summary`
- `ctaLabel`
- `ctaHref`

Field constraints:
- All required fields are non-empty strings.
- `ctaHref` can be HTTP(S) URL or local path (+ optional query string).
- Local-path targets must exist.

## Validators
- [.github/scripts/validate-community-data.mjs](.github/scripts/validate-community-data.mjs)
- [.github/scripts/validate-community-events-data.mjs](.github/scripts/validate-community-events-data.mjs)

## CI Enforcement
- [.github/workflows/ci.yml](.github/workflows/ci.yml) runs both validators.
- CI also runs [scripts/sync_community_channels_from_reference.ps1](scripts/sync_community_channels_from_reference.ps1) in check mode.

### CI Sync Policy Controls
- `COMMUNITY_CHANNELS_REFERENCE_PATH`: reference source file path used by sync check mode.
- `COMMUNITY_CHANNELS_REQUIRE_SOURCE`: strictness toggle (`"true"`/`"false"`).

Recommended usage:
- Local/dev forks where source file may be absent: keep `COMMUNITY_CHANNELS_REQUIRE_SOURCE` as `"false"`.
- Controlled environments with guaranteed source availability: set `COMMUNITY_CHANNELS_REQUIRE_SOURCE` to `"true"`.

## Authoring Events Safely
Use [scripts/scaffold_community_event.ps1](scripts/scaffold_community_event.ps1) to append schema-valid entries to [db/community_events.json](db/community_events.json).

Example:

```powershell
./scripts/scaffold_community_event.ps1 `
  -Title "Collector Roundtable" `
  -Date "2026-07-10" `
  -Mode "Discord" `
  -Summary "Monthly collector discussion and Q&A." `
  -CtaLabel "Join Event" `
  -CtaHref "community.html?src=events&cta=join_roundtable"
```

Validation after update:

```powershell
node .github/scripts/validate-community-events-data.mjs
node .github/scripts/validate-site.mjs
./scripts/refresh_v2_html.ps1 1
```

Notes:
- Script rejects empty values and accidental placeholder `.` arguments.
- Date must use `YYYY-MM-DD`.
- `CtaHref` must be an HTTP(S) URL or a valid local path target.

## Rendering Consumers
- [community.html](community.html)
- [community-events.html](community-events.html)
