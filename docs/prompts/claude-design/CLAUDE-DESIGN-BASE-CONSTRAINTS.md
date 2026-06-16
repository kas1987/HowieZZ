# Claude Design Base Constraints for HowieZZ

You are Claude Design working on `kas1987/HowieZZ`.

## Project architecture
This is a static, data-driven ZELEX Character Atlas:
- HTML pages
- shared `assets/site.css`
- shared `assets/site.js`
- data from `db/*.json`
- existing helpers such as `ZX.load()`, `ZX.mountNav()`, `ZX.charCard()`, `ZX.mountFooter()`

## Hard constraints
Do not migrate to React, Next, Astro, Tailwind, or a new framework.
Do not rewrite build scripts.
Do not edit generated DB files unless explicitly scoped.
Do not move images/videos into Git.
Do not add external analytics/forms/scripts without approval.
Do not weaken 18+ or privacy trust language.
Do not present Classic or Sculpt as fully available if product coverage is in-development.

## Design direction
Premium private atelier, cinematic collector catalog, guided buyer concierge, trustworthy made-to-order consultation path.

Avoid generic ecommerce, cheap luxury, excessive gold/glow, clutter, aggressive sales pressure.

## Response required
Return:
1. Summary of design changes
2. Files changed
3. Exact diff or patch
4. Before/after UX explanation
5. Mobile considerations
6. Assumptions
7. Blockers / follow-up tickets
