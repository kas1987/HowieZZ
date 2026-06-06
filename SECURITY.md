# Security Policy

## Reporting

This is a private brand project. If you discover a security or privacy issue
(exposed credentials, leaked confidential material, a vulnerability in the
build tooling), **do not open a public issue.** Contact the repository owner
directly.

## Secrets

No credentials, API keys, or tokens should ever be committed to this
repository. The site itself ships no secrets:

- Inquiry routing is configured at runtime via `INQUIRY_EMAIL` / `FORM_ENDPOINT`
  in `assets/site.js` (public by design — a contact address / form URL).
- The build pipeline reads any private inputs (e.g. live-feed scraping) from the
  local environment, never from tracked files.

## Confidential material

Business documents (executive briefs, board summaries, leadership packages,
redaction logs) are excluded by [`.gitignore`](.gitignore) and must not be added
to this **public** repository. If one is committed by mistake, treat it as a
disclosure: rotate/redact as needed and purge it from history.
