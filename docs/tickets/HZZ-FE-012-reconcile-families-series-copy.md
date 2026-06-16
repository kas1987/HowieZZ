# HZZ-FE-012: Reconcile "six families" vs "four series" taxonomy copy

## Repo
`kas1987/HowieZZ`

## PDR
`docs/pdr/PDR-FE-009-visual-qa-findings.md` (Finding M-3)

## Owner agent
Claude Design

## Area
frontend/copy

## Priority
30

## Status
ready

## Depends on
HZZ-FE-009

## Mission
Quiz and family.html speak of "six body families"; the global footer reads "four series ·
full-body architectures". The family-vs-series distinction may read as a contradiction to a
first-time buyer. Align the glossary/footer line so families and series are consistently and
clearly distinguished across pages. Cross-check `docs/body-family-method.md` and
`docs/body-family-copy-guide.md` for the canonical phrasing.

## Allowed actions
- Edit shared footer copy (`assets/site.js mountFooter`) and any page copy involved.

## Blocked actions
- Do not migrate frameworks. Do not edit `db/*.json`. Do not remove 18+/privacy language.

## Evidence required
- Files changed; before/after copy; alignment with the copy guide.
