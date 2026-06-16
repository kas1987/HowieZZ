# ZELEX — The Character Atlas (site guide)

The measurement-grounded catalog site for the ZELEX doll range, rebuilt for CEO Howie Wang.
Every body is treated as a measured *architecture*; every architecture is cast as named
*characters* with their own story, photoshoot, and profile.

> Note: the original pre-project landing page is preserved as `index-gallery-original.html`
> and documented in `README.md`. This file documents the new Atlas site.

**By the numbers:** 4 series · 19 full-body architectures · 76 characters (57 photographed,
19 concept/placeholder). Torso-only bodies are intentionally excluded.

---

## Run it locally

```bash
cd HowieZZ
python serve.py 8000          # then open http://localhost:8000/
```
Static site, no build step or dependencies to view — just Python 3 to serve it.

## The pages (all share `assets/site.css` + `assets/site.js`)

| Page | URL | What it is |
|------|-----|-----------|
| Home | `index.html` | The Atlas landing — hero, three doors, six-family rail, series rail, featured cast |
| Browse | `browse.html` | All 76 characters in one filterable grid (series / family / photographed / search) |
| Series | `series.html?s=SLE` | One series → its body architectures |
| Body | `body.html?b=ZK168B` | One architecture → measurement signature + its 4 characters |
| Character | `character.html?id=K-ZK168B-01` | Full detail: gallery, story, profile, specs, sisters, inquire CTA |
| Families | `family.html` / `family.html?f=The Muse` | The 7 Body Families index + per-family landings |
| Find Yours | `quiz.html` | 5-question persona quiz → Body Family → 3 character matches |
| The Craft | `craft.html` | Brand & method narrative |
| Contact | `contact.html` / `contact.html?id=…` | Real inquiry form (prefilled per character) |

## Discoverability & accessibility support files

The site ships with the launch hygiene a static catalog needs — all enforced by CI
(`.github/scripts/validate-site.mjs`):

- Per-page SEO + social metadata — every kit page carries a unique `<meta name="description">`,
  a `<link rel="canonical">`, Open Graph / Twitter Card tags, `theme-color`, and an SVG favicon.
- `robots.txt` + `sitemap.xml` — point crawlers at the nine canonical pages.
- `404.html` — branded not-found page (kit nav + footer).
- `assets/favicon.svg` — the monogram mark (SVG so no binary asset enters the repo).
- Skip-to-content link + visible focus rings — injected by `ZX.mountNav`, styled in `site.css`.

> Canonical/OG URLs use `https://www.zelexdoll.com` as the base — update if the production
> domain differs.

## ⚙️ Before launch — owner settings (edit the top of `assets/site.js`)

- `INQUIRY_EMAIL` — currently the placeholder `inquiries@zelexdoll.com`. Set the real inbox.
- `FORM_ENDPOINT` — leave empty to use the email fallback, OR paste a Formspree/Getform
  URL to have the contact form POST submissions to a real backend.

## Data & how it's built

```
db/
  catalog.db             SQLite — products, heads, bodies, images, variants
  characters.json        the 76 characters (what the site reads)        ← generated
  body_types.json        19 architectures + character/photoshoot pools  ← generated
  body_profiles.json     WHR/BWR + Body Family classification           ← generated
  character_stories.json per-character story + profile (merged overlay) ← generated
  body_measurements.json hand-transcribed spec-card measurements (source of truth)
  character_overlay.json optional hand edits, win over generated copy
```

Pipeline (run from `scripts/`, in order):

```
build_db.py         scan assets + live catalog → catalog.db + per-product JSON
build_profiles.py   compute WHR/BWR, classify into 7 Body Families
build_characters.py 4 characters per body; excludes torsos; filters factory imagery;
                    merges db/character_stories.json
merge_stories.py    validate db/_stories_<series>.json → db/character_stories.json
make_thumbs.py      520px thumbnails; MUST run after build_characters (it adds *_thumb)
```

Typical regen after editing data: `build_characters.py` → `make_thumbs.py`.
Run with `PYTHONIOENCODING=utf-8` on Windows consoles.

## Rules baked into the build

- **Torso bodies excluded** — 8 short SLE "Sex Doll Torso (No Head)" bodies are dropped
  (`is_torso()` in build_characters.py).
- **Factory images excluded** — only real photoshoot frames (`…-101, -102, …`) are eligible
  for heroes/galleries; head-catalog shots, spec cards, and stock files are filtered
  (`is_factory()`). A product with no photoshoot frame cannot fill a live character slot.
- **Best hero first** — images order by photo index so the `-101` full-body front shot leads.
- **Placeholders** borrow a sibling shoot (flagged "Concept"); a character with no image at
  all falls back to a branded monogram tile.

## Naming grammar (quick reference)

`HEAD + FACE(MJ) + BODY + PHOTOSHOOT(-1/-2)` → e.g. `KE01 + ZK168B`.
Body code = `{LINE}{HEIGHT}{CUP}`: ZK=K-Series, ZG/ZGX=Inspiration, ZF=Fusion, ZX=SLE.

## Reference docs (in `docs/`)

`site-kit-contract.md` (page-build contract) · `story-schema.md` · `character-schema.md` ·
`competitor-analysis.md` · `zelexdoll-site-map.md` · `character-profiles.md`.

## Earlier explorations (kept, not part of the live site)

`home-atlas.html`, `home-discovery.html`, `home-atelier.html` (the three original homepage
directions) and `prototypes.html` (their review hub). Superseded by the multi-page site above.
