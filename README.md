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

The catalog data in `db/` is generated, not hand-authored. The **Build Orchestrator**
manages parallel execution with intelligent caching, resume capability, and retry logic.

### Quick build
```bash
# Full pipeline (parallel execution, ~10s)
python scripts/build_orchestrator.py

# Full rebuild (reset database, re-scan all assets)
python scripts/build_orchestrator.py --reset

# Resume from last failure
python scripts/build_orchestrator.py --resume

# Specific stages only
python scripts/build_orchestrator.py --stages=profiles,characters
```

### Execution plan
```
build_db.py          # scan assets + live feed → catalog.db + catalog.json
build_profiles.py    # WHR/BWR analysis → classify into the 6 Body Families (parallel)
build_characters.py  # Series → Body → 4 characters → photoshoot|placeholder (parallel)
merge_stories.py     # fold story/profile inputs into characters.json
make_thumbs.py       # generate hero/gallery thumbnails (parallel)
build_package.py     # stage the deliverable (code + referenced images) + zip
```

**Features:**
- ✓ **Parallel execution:** Groups 1–2 run concurrently (~3x speedup)
- ✓ **Idempotence:** Skips stages if inputs unchanged
- ✓ **Resume:** Pick up from last failure with `--resume`
- ✓ **Intelligent retry:** Auto-recover transient failures
- ✓ **State tracking:** Full execution history in `db/.orchestrator/state.json`

See [`docs/BUILD-ORCHESTRATOR.md`](docs/BUILD-ORCHESTRATOR.md) for detailed docs.

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
- `docs/pdr/PDR-analytics-sanity-thresholds.json` — single source of truth for analytics sanity fixture paths and threshold defaults.

---

## Testing

The project has 200 automated tests (139 Python via pytest, 61 JavaScript via
vitest) covering the classification engine, all catalog parsers, character
generation helpers, and the `site.js` browser runtime.

```bash
python -m pytest --tb=short -q   # Python tests
npm test                          # JavaScript tests
```

A pre-push hook can run both suites automatically — see
[CONTRIBUTING.md](CONTRIBUTING.md) for setup.

---

## Contributing / workflow

`main` is protected — work on a branch and open a PR; CI must pass. See
[CONTRIBUTING.md](CONTRIBUTING.md).

---

## Comprehensive Documentation

### Core References

- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System design, data flow, frontend architecture, page routing, deployment
- **[DATA-SCHEMA.md](DATA-SCHEMA.md)** — Detailed specifications for all JSON structures, database schema, validation rules
- **[API.md](API.md)** — Complete runtime API reference (ZX global object, methods, event hooks)
- **[GLOSSARY.md](GLOSSARY.md)** — Terminology index (Body, Character, Series, Family, WHR/BWR, etc.)
- **[DECISIONS.md](DECISIONS.md)** — Architecture decision log (rationale for key design choices)
- **[MIGRATION-GUIDE.md](MIGRATION-GUIDE.md)** — Operational tasks (adding bodies, editing characters, deploying, troubleshooting)

### Quick Links

- [Build Pipeline Details](docs/BUILD-ORCHESTRATOR.md) — Parallel execution, idempotence, resume mechanics
- [Character Schema](docs/character-schema.md) — Character record structure and validation
- [Story Schema](docs/story-schema.md) — Story input format and grounding rules
- [Product Direction Records](docs/pdr/) — Business strategy and positioning briefing

### Navigation by Role

**Developers:**
→ Start with [ARCHITECTURE.md](ARCHITECTURE.md), then [API.md](API.md) for runtime details.

**Data/Build Engineers:**
→ Read [DATA-SCHEMA.md](DATA-SCHEMA.md) and [docs/BUILD-ORCHESTRATOR.md](docs/BUILD-ORCHESTRATOR.md).

**Product/Content Team:**
→ Use [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) for adding bodies + characters, [GLOSSARY.md](GLOSSARY.md) for terminology.

**Operational/Deployment:**
→ See [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) (deployment, rollback, recovery).

---

## PDR source of truth

- Recovery baseline: `docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/`
- Canonical recovery directive: `docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md`
- Task prompts for Claude, Codex, and Cursor must include one explicit
  `PDR_PATH: ...` value that points to the exact repo path being implemented.
