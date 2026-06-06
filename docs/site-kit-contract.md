# ZELEX site kit — build contract (read before building any page)

All pages live in the project ROOT (`C:\Users\kas41\archived\HowieZZ\`), are self-contained `.html`,
served by `python serve.py` from root, and share ONE design system. Do not invent new colors, fonts, or
data files. Match the visual language exactly.

## Required head (every page)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
```
Put any page-specific CSS in a `<style>` block AFTER that link. Reuse `assets/site.css` tokens/classes.

## Required boot (every page), at end of body:
```html
<script src="assets/site.js"></script>
<script>
ZX.mountNav('index.html');           // pass the nav item matching this page, or '' 
ZX.load().then(m => { render(m); ZX.mountFooter(); })
         .catch(() => ZX.fail());
function render(m){ /* page body */ }
</script>
```

## ZX runtime API (from assets/site.js)
- `ZX.load()` → Promise<model>. Caches. Throws on failure (use `.catch(ZX.fail)`).
- model fields:
  - `m.characters` — array of 108 character objects (shape below)
  - `m.byId[character_id]` — one character
  - `m.byBody[body_code]` — array of that body's 4 characters, sorted by slot
  - `m.bySeries[series]` — array of characters in a series
  - `m.btByCode[body_code]` — body_type record {body_code, series, family, height_cm, cup, WHR, BWR, spec_card, characters[], photoshoot_count, live_slots, additional_photoshoots[]}
  - `m.series` — ordered list of series present: ["K-Series","Inspiration","Fusion","SLE"]
  - `m.profiles` — body_profiles keyed by body_code (WHR/BWR/full measurements where available)
  - `m.SERIES_SUB[series]` — one-line series description string
- helpers: `ZX.famColor(family)` → css var; `ZX.qs('name')` → query param; `ZX.esc(s)` → html-escape;
  `ZX.img(char)` → best thumbnail url; `ZX.charCard(char)` → `<a>` card HTML (links to character.html);
  `ZX.bodyCard(body_code, m)` → `<a>` body-architecture card HTML (links to body.html).

## Character object shape (m.characters[i])
```
character_id "Fusion-ZF161D-01" | slot 1..4 | series "Fusion" | series_code | status "live"|"placeholder"
body_code "ZF161D"
body: { family (string|null e.g. "The Muse"), silhouette, height_cm, cup, weight_kg,
        bust, waist, hip, WHR, BWR, bust_drop_cm }   // many null when spec card pending
persona: { name, title, tagline, energy, target_buyer (often null), positioning (often null) }
face: { head_code, face_code (often null), skin_tone (often null) }
photoshoot: { status, product_code, folder, hero, gallery[], image_count, price (often null),
              hero_thumb, gallery_thumbs[],
              borrowed_from?, representative_only? }     // placeholders borrow a sibling shoot
placeholder?: { reason, art_direction }                  // only when status==='placeholder'
```
ALWAYS null-guard body measurements: if `body.WHR==null` show "spec card pending", not "null".
Use `*_thumb` images for grids; full `gallery[]` only for the large hero on character.html.

## Family accent colors (already in site.css as css vars)
Classic #8FB7E0 · Icon #D4A574 · Muse #9FD6B6 · Siren #E18B73 · Athlete #7FC8C0 · Empress #C792D6 · Sculpt #C7B07F
Use `ZX.famColor(c.body.family)` — returns `var(--Muse)` etc, or `var(--muted)` if null.

## Breadcrumbs
Pages below the homepage start with:
`<div class="crumbs"><a href="index.html">Atlas</a><span>›</span> ... </div>`

## Quality bar
- No `undefined`/`null`/`NaN` rendered. Null-guard everything.
- Mobile responsive (kit grids already handle it; test narrow).
- Keep it on-brand: dark, editorial, Playfair headers + Montserrat body, gold/blue/coral accents.
- Cross-link generously (every character → its body → its series).
