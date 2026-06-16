# HZZ-FE-009: Visual QA screenshot review

## Repo
`kas1987/HowieZZ`

## PDR
`docs/pdr/PDR-FE-009-visual-qa-screenshot-review.md`

## Owner agent
Auditor

## Area
frontend/qa

## Priority
70

## Status
planned

## Depends on
HZZ-FE-001, HZZ-FE-003, HZZ-FE-004, HZZ-FE-005, HZZ-FE-006

## Mission
Execute the frontend/design work defined in the linked PDR.

## Allowed actions
- Edit only files named in the PDR.
- Preserve static HTML/CSS/JS architecture.
- Reuse existing `ZX` runtime patterns.
- Keep changes reviewable and PR-sized.

## Blocked actions
- Do not migrate to React, Next, Astro, Tailwind, or a new framework.
- Do not rewrite build scripts.
- Do not edit generated `db/*.json` unless explicitly allowed.
- Do not move image/video assets into Git.
- Do not remove 18+ or privacy trust language.

## Evidence required
- List of files changed.
- Before/after UX explanation.
- Mobile considerations.
- Assumptions.
- Blockers or follow-up tickets.
