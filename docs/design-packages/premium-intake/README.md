# ZELEX — Premium Intake & Buyer-Fit (design package)

Two self-contained, offline-ready prototypes of the redesigned concierge intake.
Scope: **form UX, copy, and layout only.** No backend, no framework, no build step.

## What's in here

| File | What it is |
|---|---|
| `zelex-intake-guided.html` | The **guided form** — text-forward intake. Audience switch (New buyer ⇄ Collector) that re-tailors copy & depth, context summary card (Character / Body / Quiz / Compare), six buyer-fit fields with icons + meters + swatches, gradient realism scale, live "Your fit so far", trust sidebar, 18+/privacy/made-to-order consent. |
| `zelex-intake-configurator.html` | The **live configurator** — visually-forward intake. Parametric silhouette diagram that morphs with family + realism, tinted live by skin/hair/eye; a flowing filter-nav whose panel follows whatever you're editing; concierge tip popouts on every group; live build summary + CTA. |
| `src/` | Editable source (`*.dc.html`) + `support.js` runtime. Re-bundle from these if you change anything. |

Both standalone files have fonts and runtime inlined — open them directly in a browser, host them anywhere, or use them as a reference while porting. The header switch links the two together.

## Visual system (matches `assets/site.css`)

- Colors: gold `#D4A574`, cream `#F7E3C3`, app bg `#121212`, panel `#1b1b1b`, line `#333`, muted `#9a9a9a`.
- Family accents: Classic `#8FB7E0` · Icon `#D4A574` · Muse `#9FD6B6` · Siren `#E18B73` · Empress `#C792D6` · Sculpt `#C7B07F`.
- Type: Playfair Display (display) + Montserrat (body). Radii 6/10/14/100. Status: verified `#5EA6E8`, estimated `#C792D6`, live `#6BC88A`.

## Porting into the ZZ repo (kas1987/HowieZZ)

These are intentionally NOT wired to your stack — port the markup into your static pages:

1. Keep using `ZX.load()`, `ZX.mountNav()`, `ZX.charCard()`, `ZX.mountFooter()` and `assets/site.css` / `assets/site.js`. Drop in the section markup; replace inline colors with the existing CSS variables.
2. **Context summary card** maps to the existing `?id=` / `?compare=` prefill (the `char-chip` / `compare-chip` logic in `contact.html`). Reuse it; just render the richer card layout.
3. **Buyer-fit fields** (intended use, timeline, realism, handling, shipping/privacy, customization) become extra fields on the inquiry payload — same submit path as `contact.html` (`FORM_ENDPOINT` or mailto fallback).
4. The silhouette in the configurator is an **abstract architecture diagram** (SVG, driven by WHR/BWR), not a product render — swap in real per-family photography if you prefer.

### Honored constraints
No React/Next/Astro/Tailwind. No build-pipeline changes. No `db/*.json` edits. No image moves. Classic & Sculpt shown but labelled **"in development."** 18+ / privacy / made-to-order language kept intact. No external scripts/trackers added.

### Placeholder data
Catalog values (Seraphine / ZF161D, compare codes, stats) are representative — real values come from your catalog at prefill time.
