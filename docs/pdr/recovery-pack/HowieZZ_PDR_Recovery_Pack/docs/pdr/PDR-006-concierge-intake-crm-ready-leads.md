# PDR-006: Concierge Intake and CRM-Ready Leads

## Objective
Upgrade `contact.html` from basic inquiry form into a qualified concierge intake flow.

## Scope
- Add fields: intended use, timeline, realism preference, handling comfort, shipping/privacy concern, customization interest.
- Accept context from `?id=`, `?compare=`, and saved quiz result.
- Preserve mailto fallback.
- Prepare JSON payload for future backend/CRM/n8n.
- Avoid logging PII to console.
- Add success/error states.

## Acceptance criteria
- 18+ consent remains required.
- Form includes context summary before submit.
- Backend endpoint remains configurable.
- Fallback mailto works when no endpoint is set.
- No private message/name/email/phone is emitted in analytics events.

## Dependencies
`contact.html`, `assets/site.js`, PDR-003, PDR-004.

## Owner
Cartographer + Auditor.
