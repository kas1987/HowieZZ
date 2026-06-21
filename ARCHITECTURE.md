# ZELEX Character Atlas — Architecture

A comprehensive reference for the static, data-driven catalog site serving the ZELEX doll collection.

> **Project Status:** Proprietary. For internal use and authorized partners only.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Core Domains](#core-domains)
3. [Technology Stack](#technology-stack)
4. [Data Flow](#data-flow)
5. [Repository Structure](#repository-structure)
6. [Build Pipeline](#build-pipeline)
7. [Frontend Architecture](#frontend-architecture)
8. [Page Routing & Navigation](#page-routing--navigation)
9. [Deployment](#deployment)
10. [Key Design Constraints](#key-design-constraints)

---

## System Overview

**ZELEX Character Atlas** is a **zero-framework, static-site catalog** that bridges product data (live Shopify feed, measurement cards) with curated personas and brand narrative. The system ingests product feeds, classifies bodies by morphometric properties (WHR/BWR), generates characters as branded personas, and serves a browsable, searchable, shareable site.

### Core Principle

- **Data-driven, not hard-coded:** Catalog evolves from live product availability, not database queries.
- **Opinionated classification:** Bodies fit into 6 Family archetypes (Classic, Icon, Muse, Siren, Empress, Sculpt).
- **Character = Persona:** Every body gets exactly 4 named characters, each linked to a real photoshoot or a branded placeholder.
- **Static delivery:** Vanilla HTML/CSS/JS; no build tool, no framework. No server-side rendering.

---

## Core Domains

### 1. **Body Architecture**

A **Body Type** is the measurement foundation:

```
body_code: ZG170C
  ├─ height_cm: 170
  ├─ cup: C
  ├─ weight_kg: 36.1
  ├─ bust, waist, hip (cm)
  ├─ WHR (waist÷hip): 0.686
  ├─ BWR (bust÷waist): 1.357
  ├─ body_family: "The Muse"
  └─ spec_card: measurement photo
```

**WHR & BWR Classification:**

Each body is plotted on two axes:
- **WHR (Waist-Hip Ratio):** Silhouette profile (petite to tall, curvy to straight).
- **BWR (Bust-Waist Ratio):** Upper-body emphasis (modest to dramatic).

These map to 6 **Body Families**:

| Family | WHR | BWR | Silhouette | Premium |
|--------|-----|-----|-----------|---------|
| **The Classic** | 0.68–0.72 | 1.4–1.5 | Timeless hourglass | +20% |
| **The Icon** | 0.60–0.65 | 1.5–1.6 | Glamour model | +30% |
| **The Muse** | 0.65–0.70 | 1.3–1.4 | Tall, hip-dominant | +25% |
| **The Siren** | 0.55–0.60 | 1.6–1.8 | Bust-dominant fantasy | +35% |
| **The Empress** | 0.70–0.75 | 1.5–1.7 | Majestic curves | +25% |
| **The Sculpt** | 0.50–0.55 | 1.2–1.3 | Athletic, sculptural | +15% |

**Storage:**
- `db/body_measurements.json` — hand-curated spec cards + measurement values.
- `db/body_profiles.json` — computed WHR/BWR + Family classification.
- `db/catalog.db` (SQLite) — denormalized records for fast queries.

---

### 2. **Characters & Personas**

A **Character** is a named, branded persona built on a body. Every body gets exactly 4 characters.

```
character_id: "SLE-ZX160J-03"
  ├─ slot: 3 (1–4 per body)
  ├─ body_code: ZX160J
  ├─ persona:
  │   ├─ name: "Vesper"
  │   ├─ title: "The Fantasy"
  │   ├─ tagline: "Pure imagination, made physical."
  │   ├─ energy: description
  │   ├─ target_buyer: segment
  │   ├─ positioning: market rationale
  │   ├─ story: 120–180 word narrative
  │   └─ profile: {personality, ideal_setting, signature, for_you_if}
  ├─ face: {head_code, face_code, skin_tone}
  ├─ status: "live" or "placeholder"
  └─ photoshoot: {product_code, folder, hero, gallery, price, …}
```

**Key rules:**
- 4 characters per body, differentiated by **face/head sculpture + makeup + name**.
- Status: **live** (real photoshoot exists) or **placeholder** (represents the body, actual shoot coming).
- Personas are **auto-generated** from series voice + family archetypes, then **hand-curated** via `db/character_overlay.json`.
- All 4 siblings share the same body silhouette but have **distinct personalities** in story and positioning.

**Character Counts (current):**

| Series | Total | Live | Placeholder |
|--------|-------|------|-------------|
| K-Series | 8 | 4 | 4 |
| Inspiration | 20 | 17 | 3 |
| Fusion | 12 | 5 | 7 |
| SLE | 68 | 63 | 5 |
| **TOTAL** | **108** | **89** | **19** |

**Storage:**
- `db/characters.json` — character inventory, all 108 records.
- `db/body_types.json` — body architecture aggregates (4 characters each + surplus photoshoot pool).
- `db/character_overlay.json` — hand-curated name/title/story swaps, image selection.

---

### 3. **Series**

A **Series** is a product line, each with distinct aesthetic and market positioning:

| Series | Folder | Mood | Target |
|--------|--------|------|--------|
| **K-Series** | `K-Series/` | Korean-creative flagship; refined, contemporary, artful | Premium enthusiasts |
| **Inspiration** | `I-Series/` | Western naturalism; warm, believable, hip-led "Muse" energy | Photographers, curators |
| **Fusion** | `Fusion-Series/` | Movable-jaw realism; quiet luxury, understated | Realism collectors |
| **SLE** | `SLE-Series/` | Widest spectrum; minimalist to maximal fantasy | All segments |

**Storage:**
- `db/catalog.json` → `series[]` array with metadata.
- `assets/{Series-Folder}/` → photoshoot images.

---

## Technology Stack

### Frontend

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Markup** | Vanilla HTML5 | No templating, no JSX |
| **Styling** | CSS3 (variables, Grid, Flexbox) | Single `assets/site.css` |
| **Runtime** | Vanilla JS (ES6+) | Single `assets/site.js` → global `ZX` object |
| **Data** | JSON files in `db/` | `catalog.json`, `characters.json`, `body_profiles.json` |

### Backend / Build

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Local server** | Python `http.server` | Development (fallback); `serve.py` |
| **Production server** | Caddy or Netlify | Static CDN delivery |
| **Build pipeline** | Python 3.8+ | Orchestrator + stage scripts |
| **Database** | SQLite (transient) | `db/catalog.db` — intermediate state only |
| **Testing** | pytest (139 tests) + vitest (61 tests) | CI/CD validation |

### Deployment

| Target | Method | Assets |
|--------|--------|--------|
| **Local dev** | `python serve.py` | Barebone (text + structure, no images) |
| **Staging/prod** | Netlify + CDN | Full package (code + images + metadata) |
| **Packaged build** | `scripts/build_package.py` | ZIP → Google Drive |

---

## Data Flow

### Ingest → Classification → Curation → Render

```
┌─ Product Feed (Shopify API) ─────┐
│  Series folders + metadata        │
└───────────────────────────────────┘
            ↓
┌─ build_db.py ─────────────────┐
│ • Scan assets/ folders          │
│ • Index product codes           │
│ • Match feed data               │
│ → catalog.db + catalog.json     │
└─────────────────────────────────┘
            ↓
┌─ build_profiles.py ────────────┐
│ • Read body_measurements.json   │
│ • Compute WHR, BWR             │
│ • Classify into 6 Families      │
│ → body_profiles.json            │
└─────────────────────────────────┘
            ↓
┌─ build_characters.py ──────────┐
│ • Pick 4 heads per body         │
│ • Link to photoshoots           │
│ • Generate placeholders         │
│ → characters.json               │
└─────────────────────────────────┘
            ↓
┌─ merge_stories.py ─────────────┐
│ • Fold stories from writers     │
│ • Merge persona overlays        │
│ → enrich characters.json        │
└─────────────────────────────────┘
            ↓
┌─ make_thumbs.py ───────────────┐
│ • Generate hero + gallery       │
│ • Cache thumbnails             │
│ → assets/thumbs/               │
└─────────────────────────────────┘
            ↓
┌─ HTML Pages (vanilla JS) ──────┐
│ • index.html                    │
│ • browse.html                   │
│ • character.html, etc.          │
└─────────────────────────────────┘
            ↓
    assets/site.js (ZX)
    • ZX.load() → fetch catalog
    • Mount components
    • Handle navigation
    • Track analytics
            ↓
    User sees site
```

### Curation Hooks

**Hand-editable JSON files** allow non-technical oversight:

1. **`db/body_measurements.json`** — Spec cards, measurement values (WHR/BWR overrides).
2. **`db/character_overlay.json`** — Name swaps, title tweaks, story/positioning edits, hero image selection.
3. **Story files** (`db/_stories_*.json`) — Written character narratives + profiles (per series).

---

## Repository Structure

```
.
├─ index.html, browse.html, character.html, …   Primary pages
├─ assets/
│   ├─ site.css                                  Shared design system
│   ├─ site.js                                   Shared runtime (ZX object)
│   ├─ {Series}/                                 Product photoshoots (not tracked)
│   ├─ placeholders/                             Generated SVG placeholders
│   ├─ thumbs/                                   Generated thumbnails
│   └─ data/                                     Misc data (generated)
│
├─ db/
│   ├─ catalog.json                              Series + product index
│   ├─ body_profiles.json                        Body classification (WHR/BWR)
│   ├─ body_types.json                           Body architecture + character lists
│   ├─ characters.json                           All 108 character records
│   ├─ character_stories.json                    Merged stories + profiles
│   ├─ character_overlay.json                    HAND-CURATED persona edits
│   ├─ body_measurements.json                    HAND-CURATED measurement specs
│   ├─ _stories_k-series.json                    Story inputs (per series)
│   ├─ _stories_inspiration.json
│   ├─ _stories_fusion.json
│   ├─ _stories_sle.json
│   ├─ .orchestrator/                            Build state tracking
│   │   └─ state.json                            Execution history + idempotence
│   └─ catalog.db                                SQLite (transient, not tracked)
│
├─ scripts/
│   ├─ build_orchestrator.py                     Pipeline orchestrator (main entry)
│   ├─ build_db.py                               Ingest catalog
│   ├─ build_profiles.py                         Classify families
│   ├─ build_characters.py                       Persona generation
│   ├─ merge_stories.py                          Merge narrative data
│   ├─ make_thumbs.py                            Generate thumbnails
│   ├─ build_package.py                          Stage deliverable
│   ├─ generate_pages.py                         Generate page inventory
│   └─ [40+ utility scripts]                     Analytics, CDN, Shopify sync, etc.
│
├─ docs/
│   ├─ ARCHITECTURE.md                           (you are here)
│   ├─ DATA-SCHEMA.md                            Detailed schema reference
│   ├─ API.md                                    Runtime JS API (ZX object)
│   ├─ GLOSSARY.md                               Terminology index
│   ├─ BUILD-ORCHESTRATOR.md                     Pipeline reference
│   ├─ character-schema.md                       Character structure spec
│   ├─ story-schema.md                           Story/profile structure spec
│   ├─ PDR-*.md                                  Product Direction Records
│   └─ [design docs, research, analysis]
│
├─ tests/
│   ├─ test_build_*.py                           pytest suite (139 tests)
│   ├─ *.test.js                                 vitest suite (61 tests)
│   └─ conftest.py                               Pytest fixtures
│
├─ .github/
│   ├─ workflows/                                CI/CD pipelines
│   └─ PULL_REQUEST_TEMPLATE.md
│
├─ serve.py                                      Local dev server
├─ Caddyfile                                     Caddy config (for howiez.local)
├─ README.md                                     Quick-start guide
├─ CLAUDE.md                                     Project instructions
└─ .gitignore                                    Excludes images (~260 MB)
```

---

## Build Pipeline

### Orchestrator

**Entry point:** `python scripts/build_orchestrator.py`

The **Build Orchestrator** manages parallel execution, idempotence, state tracking, and retry logic.

#### Execution Model

```
Group 0 (init):
  └─ db

Group 1 (parallel analysis):
  ├─ profiles
  └─ characters

Group 2 (post-processing):
  ├─ merge_stories
  └─ thumbs

Group 3 (inventory):
  └─ pages
```

- **Stages within a group run in parallel** (up to 2 concurrent processes).
- **Groups execute sequentially** (enforce dependency order).
- **Idempotent:** Skips stages if inputs are unchanged.
- **Resumable:** Can pick up from a failed stage with `--resume`.
- **Retryable:** Auto-retries transient failures (3 attempts per stage).

#### Key Commands

```bash
# Full pipeline (default, ~10s)
python scripts/build_orchestrator.py

# Full rebuild (reset database, re-scan all)
python scripts/build_orchestrator.py --reset

# Resume from last failure
python scripts/build_orchestrator.py --resume

# Run specific stages only
python scripts/build_orchestrator.py --stages=profiles,characters

# Dry-run (show what would execute)
python scripts/build_orchestrator.py --dry-run

# JSON status output (for CI/CD)
python scripts/build_orchestrator.py --json
```

#### State File

**Location:** `db/.orchestrator/state.json`

```json
{
  "timestamp": "2026-06-21T13:15:00Z",
  "status": "success",
  "stages": {
    "db": {
      "status": "complete",
      "start_time": 1234567890,
      "duration_secs": 2.3,
      "input_hash": "sha256:abc123…",
      "output_hash": "sha256:def456…"
    },
    …
  }
}
```

**Guarantees:**
- Stages run only if inputs changed or outputs missing.
- Exit codes: 0 (success), 1 (fatal), 2 (skipped), 3 (partial failure).

---

## Frontend Architecture

### Shared Assets

#### `assets/site.css`

One CSS file, everything:

- **Design tokens:** CSS variables for colors, spacing, typography.
- **Component library:** Modular class names (`.card`, `.button`, `.grid-3`, etc.).
- **Responsive:** Mobile-first breakpoints (480px, 768px, 1024px, 1440px).
- **Dark mode:** `:root[data-theme="dark"]` toggle.
- **Body Family colors:** `--Classic`, `--Icon`, `--Muse`, `--Siren`, `--Empress`, `--Sculpt`.

**Bundle size:** ~40 KB (minified); loads synchronously (no defer).

#### `assets/site.js`

Global `window.ZX` object; the only tracked JS file. Every HTML page calls:

```html
<script src="assets/site.js" defer></script>
```

**Core API:**

```javascript
// Load the catalog model
ZX.load().then(model => {
  // model = { catalog, characters, bodyProfiles, families, … }
  // Now render your page
});

// Navigation helpers
ZX.qs('family')              // Get URL parameter
ZX.ensureParams([…])         // Validate + normalize params

// Component mounting
ZX.mountNav()                // Render top nav
ZX.mountFooter()             // Render footer
ZX.renderCharacterCard(c)    // Render character card HTML

// Analytics
ZX.track(eventName, payload) // Fire analytics event
ZX.getSessionId()            // Get/create session ID

// Compare tool
ZX.addCompareBody(code)      // Add body to comparison
ZX.getCompareBodies()        // Retrieve comparison list
ZX.setCompareBodies([…])     // Overwrite comparison

// Quiz/recommendation
ZX.recommend(filters)        // Get matching characters
ZX.rankByFamily(characters, family) // Sort by family
```

**Analytics:** Integrated GA4 event tracking; see [ANALYTICS_TRACKING_SCHEMA.md](ANALYTICS_TRACKING_SCHEMA.md).

**Bundle size:** ~35 KB (unminified). **No external dependencies** (zero npm, zero CDN).

### Page Template Pattern

Every page follows the same structure:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="assets/site.css">
  <title>…</title>
</head>
<body>
  <div id="nav"></div>
  <main>…page content…</main>
  <div id="footer"></div>
  <script src="assets/site.js" defer></script>
  <script>
    ZX.load().then(model => {
      ZX.mountNav();
      // Render page-specific content
      document.querySelector('main').innerHTML = …;
      ZX.mountFooter();
    });
  </script>
</body>
</html>
```

### Session Storage

- **Compare tool state:** `localStorage['zx_compare_bodies']` (array of body codes, max 4).
- **Analytics session ID:** `sessionStorage` / `localStorage` with fallback.
- **Debug mode:** `localStorage['zx_analytics_debug']` (toggled via `?zx_analytics_debug=1`).

---

## Page Routing & Navigation

### Primary Navigation Pages

Pages that appear in `ZX.mountNav()` and `ZX.mountFooter()`:

| Page | Route | Purpose | Data Source |
|------|-------|---------|-------------|
| **index.html** | `/` | Homepage (hero, featured series, character cards) | `characters.json` |
| **browse.html** | `/browse.html` | Filterable grid of all 108 characters | `characters.json` |
| **family.html** | `/family.html?f=…` | Body-family landing + character index | `body_profiles.json` |
| **compare.html** | `/compare.html` | Side-by-side body architecture tool | Body families, `characters.json` |
| **options.html** | `/options.html` | Customization guide + accessories | Hand-authored content |
| **community.html** | `/community.html` | Community hub + gallery | Community data |
| **quiz.html** | `/quiz.html` | "Find Yours" persona quiz | Family archetypes, `characters.json` |
| **configurator.html** | `/configurator.html` | Live body configurator | Family ranges, visualization |
| **contact.html** | `/contact.html?id=…` | Inquiry form (prefillable per character) | `FORM_ENDPOINT`, `INQUIRY_EMAIL` |

### Content Pages

Reachable via in-page links; not in top nav:

| Page | Route | Purpose |
|------|-------|---------|
| **series.html** | `?s=K-Series` | Per-series landing (bodies + characters) |
| **body.html** | `?b=ZG170C` | Body architecture detail (spec + 4 characters) |
| **character.html** | `?id=SLE-ZX160J-03` | Character detail (hero, gallery, story, kin) |
| **craft.html** | `/craft.html` | Brand narrative (footer link) |
| **community-events.html** | `/community-events.html` | Linked from community.html |

### Variant / Legacy Pages

Not in nav; kept for reference or A/B testing:

| Page | Notes |
|------|-------|
| **404.html** | Custom error page |
| **hero.html** | Alternate homepage (A/B variant) |
| **Landing.html** | Alternate landing variant |
| **index-gallery-original.html** | Legacy standalone gallery (pre-site-js) |

### URL Parameters

**Navigation:**
- `?f=…` — Family filter (family.html, browse.html)
- `?s=…` — Series selector (series.html)
- `?b=…` — Body code (body.html)
- `?id=…` — Character ID (character.html)

**Analytics / Debug:**
- `?zx_analytics_debug=1|0` — Toggle analytics logging (persists to localStorage)
- `?utm_source=…` — Campaign tracking

---

## Deployment

### Local Development

```bash
# Option 1: Python built-in server
python serve.py              # http://localhost:8000

# Option 2: Caddy (requires Windows hosts entry)
caddy run                    # http://howiez.local
```

**Windows hosts entry** (`C:\Windows\System32\drivers\etc\hosts`):
```
127.0.0.1  howiez.local
```

**macOS/Linux launchers:**
- `Start-Mac-Linux.command` (double-click to launch Python server)
- `Start-Windows.bat` (Windows equivalent)

### Staging / Production

**Netlify (preferred):**
- Static deployment from `main` branch.
- Automatic builds on push (CI/CD via `.github/workflows/`).
- CDN + Netlify Edge Functions for performance.
- Environment: `FORM_ENDPOINT`, `INQUIRY_EMAIL` (in `assets/site.js`).

**Full Packaged Build:**

```bash
python scripts/build_package.py
# Outputs: zelex-deliverable.zip
# Contains: all HTML, CSS, JS + full image tree (~260 MB)
# Uploaded to: Google Drive (shared with stakeholders)
```

### Pre-Deployment Checklist

Before pushing to `main`:

1. **Config:** `assets/site.js` has correct `INQUIRY_EMAIL` + `FORM_ENDPOINT`.
2. **Analytics:** PDR analytics thresholds synced (`docs/pdr/PDR-analytics-sanity-thresholds.json`).
3. **Build:** `python scripts/build_orchestrator.py --reset` succeeds.
4. **Tests:** `pytest` + `npm test` both pass.
5. **Staging:** Deploy to staging branch; verify all pages load.
6. **CI/CD:** GitHub Actions pass (linter, tests, build).
7. **Git:** `git push` to `main` (protected branch; requires PR + approval).

---

## Key Design Constraints

### No Framework, No Build Step

**Why:**
- Minimizes deployment surface; zero runtime dependencies.
- Pages load immediately (no JS compilation, no bundler overhead).
- Easier to audit and debug.
- Suitable for a static, read-heavy site.

**Trade-offs:**
- No component re-use; copy common patterns across pages.
- Manual DOM management; no virtual DOM.
- No hot reload; refresh browser to see changes.

### Static Data (JSON), Not Queries

**Why:**
- Data is finite and known at build time (108 characters, 27 bodies, 4 series).
- No server-side queries = no latency, no database overhead.
- Data can be cached aggressively (far-future expires headers).

**Trade-offs:**
- Adding a new body requires a rebuild + redeploy.
- Real-time product availability requires periodic sync (Shopify feed polling).

### 6 Body Families (Fixed Classification)

**Why:**
- Reduces cognitive load; buyers understand archetypes.
- Drives premium positioning (each family has a distinct price tier).
- Scales; new bodies automatically classify.

**Trade-offs:**
- Some bodies fall into edge cases (WHR/BWR near family boundaries).
- Manual override mechanism needed (`db/body_measurements.json` → `family` field).

### 4 Characters Per Body

**Why:**
- Strikes a balance: enough variety, not overwhelming.
- Each character differentiated by a real photographed head.
- Drives sales (4 SKUs per body architecture).

**Trade-offs:**
- Limits persona permutations (no custom body+head mixing in catalog).
- Requires hand-curation of names/stories for 108 personas.

### Images Excluded from Git

**Why:**
- ~260 MB of product imagery; git is not a CDN.
- Images are binary; delta compression doesn't help much.
- Simpler to distribute as a packaged build.

**Trade-offs:**
- Bare clone shows no images (structure only).
- Image sync requires manual distribution or build artifact download.
- Deploy pipeline must fetch images separately.

---

## Next Steps

- **Data Schema Reference:** See [DATA-SCHEMA.md](DATA-SCHEMA.md).
- **Runtime API:** See [API.md](API.md).
- **Terminology:** See [GLOSSARY.md](GLOSSARY.md).
- **Architecture Decisions:** See [DECISIONS.md](DECISIONS.md).
- **Build Pipeline Details:** See [BUILD-ORCHESTRATOR.md](docs/BUILD-ORCHESTRATOR.md).
