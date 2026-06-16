# PDR-008: Analytics Event Taxonomy

## Objective
Instrument buyer behavior without leaking PII.

## Scope
- Define event taxonomy: page view, family view, character view, body view, compare add/remove, quiz start/finish, contact start/submit, CTA click.
- Add no-op analytics adapter configurable in `assets/site.js`.
- Add `data-event` attributes to CTAs.
- Add docs for event names and payload fields.
- Exclude names, emails, phone numbers, freeform message body.

## Acceptance criteria
- Analytics can be disabled from one config point.
- Local dev runs without analytics errors.
- No PII in event payload.
- Event docs exist in `docs/analytics/`.

## Dependencies
PDR-002 through PDR-006.

## Owner
Auditor + Sentinel.
