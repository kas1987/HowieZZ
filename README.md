# ZELEX — Character Atlas

A static, data-driven catalog site for the ZELEX collection. Every body is
treated as an *architecture* (a measured silhouette), every architecture is
cast as named *characters*, and the whole catalog is generated from the live
product feed plus spec-card measurements.

> **Proprietary.** See [LICENSE](LICENSE). This is a private brand project, not
> open source.

---

## What's in this repo

This repository tracks **source code + catalog data + docs only**. All imagery
and video are intentionally **excluded** (see [`.gitignore`](.gitignore)); the
runnable site — code *plus* its ~260 MB of images — is delivered as a packaged
build (Google Drive) produced by `scripts/build_package.py`.

```
.
├─ index.html                 Atlas homepage (hero, doors, series rail, featured)
├─ browse.html                All characters — filterable grid
├─ series.html?s=…            One series (body architectures + characters)
├─ family.html[?f=…]          Body-family index + per-family landing
├─ body.html?b=…              One body architecture (spec + cast)
├─ character.html?id=…        Flagship character detail (gallery, story, kin)
├─ quiz.html                  "Find Yours" persona quiz → family → matches
├─ craft.html                 Brand / method narrative
├─ contact.html?id=…          Inquiry form (prefillable per character)
├─ index-gallery-original.html  Original Collector's Gallery (kept for reference)
│
├─ assets/
│   ├─ site.css               Shared design system (the only tracked CSS)
│   └─ site.js                Shared runtime — global `ZX` (the only tracked JS)
│
├─ db/                        Catalog DATA (JSON) + schema.sql  (catalog.db is NOT tracked)
├─ scripts/                   Python build pipeline + tools
├─ docs/                      Schemas, site map, analysis notes
├─ serve.py                   Tiny local web server
└─ Start-Windows.bat / Start-Mac-Linux.command   one-click launchers
```

Because images are not in git, a bare clone renders structure and text but
shows empty image frames. To see the full site, use the packaged build (which
includes the images) or drop the image tree into `assets/` locally.

---

## Run it locally

```bash
python serve.py          # serves this folder at http://localhost:8000
```

Then open <http://localhost:8000/index.html>. Every page shares
`assets/site.css` + `assets/site.js` and reads its data from `db/*.json`.

Windows users can double-click **`Start-Windows.bat`**; macOS users
**`Start-Mac-Linux.command`**.

---

## The build pipeline

The catalog data in `db/` is generated, not hand-authored. Run order:

```
build_db.py          # scan assets + live feed → catalog.db + catalog.json
build_profiles.py    # WHR/BWR analysis → classify into the 6 Body Families
build_characters.py  # Series → Body → 4 characters → photoshoot|placeholder
merge_stories.py     # fold story/profile inputs into characters.json
make_thumbs.py       # generate hero/gallery thumbnails  (re-run after build_characters)
build_neck_compat.py # neck-connector classes → db/neck_compatibility.json (head interchangeability)
build_heads.py       # reverse-engineer heads → db/heads.json (configurator head gallery; imports build_neck_compat)
build_package.py     # stage the deliverable (code + referenced images) + zip
```

Hand-curation lives in `db/character_overlay.json` (name/title/story swaps, hero
image selection, gallery cleaning) and `db/body_measurements.json`
(spec-card + estimated measurements). See [`docs/`](docs/) for schemas.

### The 6 Body Families

Bodies are classified by WHR (waist÷hip) and BWR (bust÷waist) into:
**The Classic · The Icon · The Muse · The Siren · The Empress · The Sculpt.**
Classic and Sculpt are currently "in development" (no catalogued body yet).

---

## Owner settings before launch

In `assets/site.js`:

- `INQUIRY_EMAIL` — the real inquiry address (placeholder: `inquiries@zelexdoll.com`).
- `FORM_ENDPOINT` — optional Formspree/Getform URL; when empty, the contact form
  falls back to a prefilled `mailto:`.

---

## Contributing / workflow

`main` is protected — work on a branch and open a PR; CI must pass. See
[CONTRIBUTING.md](CONTRIBUTING.md).
