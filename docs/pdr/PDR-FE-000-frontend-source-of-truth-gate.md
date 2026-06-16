# PDR-FE-000: Frontend Source-of-Truth Gate

## Objective
Prevent further drift by forcing all Claude Design and frontend implementation work to reference HowieZZ-local PDR and ticket files.

## Source of truth
- Repo: `kas1987/HowieZZ`
- PDRs: `docs/pdr/*.md`
- Tickets: `docs/tickets/*.md`
- Coordination queue: `command-center/next-work.howiezz.frontend.json`

## Scope
- Add this ticket/PDR pack into HowieZZ.
- Confirm local server still runs.
- Confirm no frontend work starts until source files are present in HowieZZ.

## Acceptance criteria
- PDRs and ticket files exist in HowieZZ.
- Command Center references point back to HowieZZ files.
- Claude Design prompt references only HowieZZ PDR/ticket paths.
- No agent writes to Command Center or 3D_Meta as implementation repo.

## Stop condition
If GitHub connector or PR target resolves to any repo other than `kas1987/HowieZZ`, stop and use local PR commands instead.
