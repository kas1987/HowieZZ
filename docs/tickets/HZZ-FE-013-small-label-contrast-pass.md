# HZZ-FE-013: Small-label contrast / legibility comfort pass

## Repo
`kas1987/HowieZZ`

## PDR
`docs/pdr/PDR-FE-009-visual-qa-findings.md` (Finding M-4)

## Owner agent
Claude Design

## Area
frontend/design-system

## Priority
25

## Status
ready

## Depends on
HZZ-FE-002, HZZ-FE-009

## Mission
`--muted` (#9a9a9a on #121212 ≈ 6.6:1) passes WCAG AA but is applied to dense 10–12px
uppercase/letter-spaced labels (nav links `assets/site.css:99`; `.fam` 10px `:226`;
`.metrics-legend .lg-note` 10.5px `:292`; footer 11px `:415`). No failures, but near the
comfortable floor. Consider bumping the smallest label sizes or using `--text` for the densest
metric labels. Cosmetic — low priority.

## Allowed actions
- Edit `assets/site.css` token usage / small-label sizes.

## Blocked actions
- Do not migrate frameworks. Do not edit `db/*.json`. Do not remove 18+/privacy language.

## Evidence required
- Files changed; before/after contrast notes.
