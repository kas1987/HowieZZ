# HowieZZ / ZZhowie HTML — PDR Recovery Package

## Executive decision

HowieZZ is the implementation repository. Command Center is coordination only. Any issue/PDR created in Command-Center or 3D_Meta is evidence of planning but is not implementation authority unless mirrored into HowieZZ.

## Source-of-truth hierarchy

1. `kas1987/HowieZZ` repo files and PRs
2. `docs/pdr/*.md` inside HowieZZ
3. `docs/research/*.md` and `db/*.json` inside HowieZZ
4. Command Center issues that link back to a HowieZZ PR or PDR file
5. Prior chat summaries and external issue copies

## Current known state

The repo is a static, data-driven ZELEX Character Atlas. The tracked repo contains source code, catalog data, and docs; images are intentionally excluded and the image-heavy runnable package is produced separately. The repo uses shared `assets/site.css` and `assets/site.js`, and pages read data from `db/*.json`.

## Current implementation read

Partial PDR coverage exists:
- Design System v2 partially landed.
- Homepage is still more Atlas than concierge landing.
- Quiz scoring exists but needs stronger handoff and explanation.
- Contact exists but is not full concierge intake.
- Body compare is not yet a full product-decision workflow unless the local patch has been applied.
- SEO, analytics, and competitor ROI research remain incomplete.

## Recommended PR sequence

1. PR-1: PDR source-of-truth recovery
2. PR-2: Concierge homepage + compare scaffold
3. PR-3: Compare handoff + character page conversion
4. PR-4: Quiz and concierge intake
5. PR-5: SEO + analytics
6. PR-6: Competitor ROI research
