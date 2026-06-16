# HZZ-FE-011: Fix mobile horizontal overflow on quiz/configurator at 390px

## Repo
`kas1987/HowieZZ`

## PDR
`docs/pdr/PDR-FE-009-visual-qa-findings.md` (Finding M-2)

## Owner agent
Claude Design

## Area
frontend/mobile

## Priority
50

## Status
ready

## Depends on
HZZ-FE-005, HZZ-FE-008, HZZ-FE-009

## Mission
QA mobile captures (`m-quiz.png`, `m-configurator.png`) showed content clipped at the right
edge at 390px. There is no `overflow-x` / width guard on `html`/`body` (`assets/site.css:60-62`),
and the quiz hero `h1` clamps to a 36px floor at 390px (`quiz.html:36`). First confirm the
overflow in a real narrow viewport (captures used `--hide-scrollbars`, which can render at
intrinsic width). If real: lower the quiz `h1` mobile floor and/or add `overflow-x:hidden` to
`body`, and audit the configurator spec panel width.

## Allowed actions
- Edit `assets/site.css`, `quiz.html`, `configurator.html` as needed.
- Keep changes PR-sized; reuse existing tokens.

## Blocked actions
- Do not migrate frameworks. Do not edit `db/*.json`. Do not remove 18+/privacy language.

## Evidence required
- Real 390px viewport before/after screenshots.
- Files changed; mobile considerations.
