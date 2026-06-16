# HZZ-FE-010: Confirm browse grid renders in a real browser; harden ZX.load() for headless/CI

## Repo
`kas1987/HowieZZ`

## PDR
`docs/pdr/PDR-FE-009-visual-qa-findings.md` (Finding M-1)

## Owner agent
Claude Design

## Area
frontend/browse

## Priority
40

## Status
ready

## Depends on
HZZ-FE-007, HZZ-FE-009

## Mission
During HZZ-FE-009 visual QA, `browse.html` stayed at "Loading the ZELEX catalog…" under
headless Chrome (`--virtual-time-budget` up to 12s) while every other `ZX.load()`-driven page
rendered. Suspected a Chrome-headless virtual-time + parallel-`fetch` artifact, not a runtime
bug. First **verify in a real browser**; only if the grid genuinely fails to populate, fix the
load path. Optionally add a "catalog-ready" signal so headless/CI screenshot tooling can wait
deterministically.

## Allowed actions
- Edit `browse.html` and/or `assets/site.js` only if a real bug is confirmed.
- Reuse existing `ZX` runtime patterns.

## Blocked actions
- Do not migrate frameworks. Do not edit `db/*.json`. Do not remove 18+/privacy language.

## Evidence required
- Real-browser confirmation (screenshot) of the populated grid.
- If changed: files changed, before/after, root cause.
