# PDR-012: Hero Split Cover — v2 Rebuild

**Status:** Spec complete, ready to implement  
**Date:** 2026-06-18  
**File scope:** `hero.html` (full rewrite)  
**Spec:** `docs/superpowers/specs/2026-06-18-hero-split-cover-v2-design.md`  
**Supersedes:** Initial `hero.html` build (pre-v2 spec) and `docs/superpowers/specs/2026-06-18-hero-split-cover-design.md`

---

## Problem

The initial `hero.html` was built from the first-pass spec and missed a full brainstorming refinement cycle. The result had several issues:

- **Logo treatment** wrong — old spec used Playfair Display gold, centered straddling the divider; actual brand requires bold white ZELEX wordmark top-right with italic gold tagline "Luxury. Lives."
- **Pacing too fast** — all transitions at 0.5s felt abrupt; luxury-commercial references (perfume, watches) require 1.2–1.8s easing
- **Image distortion** — `scale(1.04)` on `background-image` div stretches photos on zoom
- **Divider line** — the vertical gold divider between panels proved visually heavy; removed in final design
- **CTA buttons** — were full-width at panel center; redesigned as pill-rounded, positioned adjacent to thumbnails at panel bottom
- **Thumbnails** — original spec placed at top corners; refined through multiple iterations to panel-level bottom corners with slide-up reveal
- **Quote behavior** — always visible in initial build; should only appear on panel hover, sliding in from the center direction with the doll's name, then model label
- **No editorial card concept** — final design frames each panel as a floating editorial card (~88% fill) that expands to full bleed on hover
- **Color atmosphere** — left panel needs gold radial glow, right panel needs purple radial glow

---

## Solution

Full rewrite of `hero.html` based on the v10 brainstorming mockup. The page is a fullscreen split editorial cover: two floating cards at rest, expanding to full bleed on hover with character quotes, doll names, and product labels emerging from the center divide.

### Architecture

```
hero.html (fullscreen, no nav, no footer)
  ├── .stage               — flex row, 100vw × 100vh
  │   ├── .panel.panel-l   — left half → index.html (Discover)
  │   │   ├── .editorial-card
  │   │   │   ├── .card-image   — <img> object-fit:cover, rotates 3–7s
  │   │   │   ├── .card-glow    — gold radial bloom
  │   │   │   ├── .card-scrim   — bottom gradient for text readability
  │   │   │   └── .card-quote-block  — doll name + quote + model label
  │   │   ├── .card-cta-group.cta-l  — label + pill button, panel level
  │   │   └── .thumb.thumb-l         — previous image thumbnail, panel level
  │   └── .panel.panel-r   — right half → Landing.html (Explore)
  │       ├── .editorial-card
  │       │   ├── .card-image
  │       │   ├── .card-glow    — purple radial bloom
  │       │   ├── .card-scrim
  │       │   └── .card-quote-block
  │       ├── .card-cta-group.cta-r
  │       └── .thumb.thumb-r
  ├── .logo                — ZELEX wordmark, top-right, above both panels
  └── .hint                — "Choose your Atlas", bottom center
```

### Key Design Decisions

| Decision | v1 (old) | v2 (this spec) |
|---|---|---|
| Logo | Playfair gold, centered, 18px | Bold white, top-right, 28px + italic gold tagline |
| Panels | Full-bleed only | Editorial card 88%×87% → expands to full bleed |
| Divider | 1px gold vertical line | Removed |
| Panel expansion | 62/38 at 0.5s | 56/44 at 1.2s |
| Color atmosphere | None | Gold glow left, purple glow right |
| Image | background-image + scale() | `<img>` object-fit:cover, scale(1.03) |
| Quote visibility | Always visible | Hover-only, slides in from center |
| Quote content | Quote only | Doll name (above) + quote + model label |
| CTA position | Panel center | Bottom row, adjacent to thumbnail |
| Thumbnails | Top corners | Bottom corners, slide-up reveal |
| Hint text | "Move to choose your path" | "Choose your Atlas" |
| Transition speed | 0.5s | 1.2s panels, 1.8s image crossfade |

---

## Files

| File | Action |
|---|---|
| `hero.html` | Full rewrite — all inline styles, no external CSS dependencies |
| `docs/pdr/PDR-012-hero-split-cover-rebuild.md` | This document |
| `docs/superpowers/specs/2026-06-18-hero-split-cover-v2-design.md` | Full design spec |
| `docs/superpowers/specs/2026-06-18-hero-split-cover-design.md` | Superseded — do not use |

---

## Implementation Notes

- Use `ZX.load()` for character data; select two `status === 'live'` characters with valid images, different series
- Image rotation: `setInterval` with `Math.random() * 4000 + 3000` (3–7s jitter)
- On image swap: current image becomes thumbnail; thumbnail triggers `.visible` class → 4s auto-dismiss
- Doll name color: randomly pick from `['#F472B6','#E85878','#FF6B35','#FB923C','#E63946','#F9A8D4','#FF4D6D','#F4845F']` on load
- Quote pool: randomly pick one quote per panel per load; apply `<br>` after any comma or period
- `:has()` CSS hover works in all modern browsers; include JS `.hover-l` / `.hover-r` class fallback for older
- Mobile: stack vertically, 100vw × 50vh per panel, tap-to-navigate (no hover)
- Google Fonts: load `Dancing Script:wght@700` for doll name

---

## Next

- Implement `hero.html` per spec
- Update `index.html` hero link to point to `hero.html` as the site entry point
- Future: `Landing.html` redesign (experienced collector atlas navigator) — separate PDR
