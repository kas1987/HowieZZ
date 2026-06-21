# Glossary & Terminology Reference

Canonical definitions of domain-specific terms used throughout ZELEX Character Atlas.

> See also: [ARCHITECTURE.md](ARCHITECTURE.md), [DATA-SCHEMA.md](DATA-SCHEMA.md)

---

## Core Concepts

### Body / Body Type

**Definition:** A physical silhouette and measurement architecture. Identified by a unique body code (e.g., `ZG170C`).

**Properties:**
- Height in cm
- Cup size (A–J)
- Measurements: bust, waist, hip (all in cm)
- Computed morphometric ratios: WHR, BWR
- Classified Body Family

**Notes:**
- A body is a **reusable template**; it can host multiple characters.
- Exactly 4 characters per body (differentiated by head/face).
- One body appears in one series only (e.g., `ZG170C` is in Inspiration series).

**Plural:** Bodies | **Abbreviation:** n/a

---

### Body Family

**Definition:** One of 6 archetypal body silhouettes, defined by morphometric ranges (WHR & BWR).

**The 6 Families:**
1. **The Classic** — Timeless hourglass (WHR 0.68–0.72, BWR 1.4–1.5)
2. **The Icon** — Glamour model (WHR 0.60–0.65, BWR 1.5–1.6)
3. **The Muse** — Tall, hip-dominant (WHR 0.65–0.70, BWR 1.3–1.4)
4. **The Siren** — Bust-dominant fantasy (WHR 0.55–0.60, BWR 1.6–1.8)
5. **The Empress** — Majestic curves (WHR 0.70–0.75, BWR 1.5–1.7)
6. **The Sculpt** — Athletic, sculptural (WHR 0.50–0.55, BWR 1.2–1.3)

**Properties:**
- Silhouette descriptor (marketing narrative)
- Premium tier (price adjustment %) — drives positioning
- Target buyer segment
- UI color (hex for CSS)

**Notes:**
- Families are **fixed archetypes**, not dynamic clusters.
- Bodies map to families via computed WHR & BWR.
- Out-of-range bodies get `family = null` (Unclassified).
- Hand override possible via `body_measurements.json` → `family_override`.

**Abbreviation:** n/a | **Count:** 6 canonical

---

### Character

**Definition:** A named, branded persona built on a body. Every body hosts exactly 4 characters.

**Identity:**
- Name (e.g., "Vesper")
- Title (archetype, e.g., "The Fantasy")
- Tagline (one-liner brand promise)
- Story (120–180 word narrative)
- Profile fields: personality, ideal setting, signature, for_you_if

**Differentiation:**
- 4 characters on one body differ by **head/face sculpture + makeup + skin tone**.
- Each character gets a real **photoshoot** (product SKU) OR a **placeholder** (coming soon).

**Status:**
- **Live:** Real photoshoot exists; full imagery available.
- **Placeholder:** No photoshoot yet; branded SVG placeholder + aspirational story.

**Identifier:** `{Series}-{BodyCode}-{Slot:02d}` (e.g., `SLE-ZX160J-03`)

**Notes:**
- Personas are auto-generated from series voice + family archetypes, then hand-curated.
- All 4 siblings share body silhouette but have **distinct personalities**.
- No generic personas; every name/story is unique.

**Count (current):** 108 total (89 live, 19 placeholder)

---

### Series

**Definition:** A product line with distinct aesthetic, market positioning, and manufacturing philosophy.

**The 4 Series:**
1. **K-Series** — Korean-creative flagship; refined, contemporary, artful. (8 characters)
2. **Inspiration** (I-Series) — Western naturalism; believable, warm, hip-led "Muse" energy. (20 characters)
3. **Fusion** — Movable-jaw realism; quiet luxury, understated. (12 characters)
4. **SLE** — Widest spectrum; athletic minimalism to maximal fantasy. (68 characters)

**Canonical Series IDs:**
- `K` or `K-Series`
- `I` or `Inspiration`
- `Fusion` or `F`
- `SLE`

**Notes:**
- Each series has its own asset folder (`assets/K-Series/`, `assets/I-Series/`, etc.).
- Series is **not a product line** (no SKU); it's a grouping for browsing + marketing.
- Every body belongs to exactly one series.

**Plural:** Series (same in singular & plural)

---

## Morphometric & Classification

### WHR (Waist-Hip Ratio)

**Definition:** Computed ratio of waist circumference to hip circumference.

**Formula:** `WHR = waist_cm / hip_cm`

**Range:** [0.4, 0.9] (typical for dolls)

**Interpretation:**
- **Lower WHR** (0.4–0.6) → straighter silhouette, athletic.
- **Mid WHR** (0.6–0.7) → balanced, hourglass.
- **Higher WHR** (0.7–0.9) → dramatic curves, majestic.

**Family Correlation:**
- Classic: 0.68–0.72
- Icon: 0.60–0.65
- Muse: 0.65–0.70
- Siren: 0.55–0.60
- Empress: 0.70–0.75
- Sculpt: 0.50–0.55

---

### BWR (Bust-Waist Ratio)

**Definition:** Computed ratio of bust circumference to waist circumference.

**Formula:** `BWR = bust_cm / waist_cm`

**Range:** [1.0, 2.0] (typical for dolls)

**Interpretation:**
- **Lower BWR** (1.0–1.3) → modest bust, streamlined upper body.
- **Mid BWR** (1.3–1.5) → balanced proportions.
- **Higher BWR** (1.5–2.0) → dramatic bust emphasis, pronounced curves.

**Family Correlation:**
- Classic: 1.4–1.5
- Icon: 1.5–1.6
- Muse: 1.3–1.4
- Siren: 1.6–1.8
- Empress: 1.5–1.7
- Sculpt: 1.2–1.3

---

### Bust Drop

**Definition:** Vertical distance (cm) between bust fullness and waist narrowing point.

**Formula:** Usually `bust_cm / 2 - waist_cm / 2` (approximation)

**Usage:** Visual descriptor for profile; helps distinguish subtle body variations.

---

## Product & Asset Terminology

### Photoshoot / Product Code

**Definition:** A real product SKU (head + body combination) with an image set.

**Format:** `{HeadCode}+{BodyCode}` (e.g., `ZXE223_1+ZX160J`)

**Properties:**
- Asset folder: `assets/{Series}/{ProductCode}/`
- Hero image (main): `…/…-101.jpg`
- Hero thumbnail: `assets/thumbs/{Series}/{ProductCode}/…-101.jpg`
- Gallery: 15–40 additional images (`…-102.jpg`, `…-103.jpg`, …)
- Video (optional)
- Price (SKU-specific)
- Live Shopify handle (URL slug)

**Notes:**
- One photoshoot per character (1:1 mapping).
- A body can have multiple photoshoots (surplus pool stored in `additional_photoshoots[]`).

---

### Placeholder

**Definition:** A branded SVG image used when a character's real photoshoot does not yet exist.

**Components:**
- SVG file: `assets/placeholders/{Series}-{Title}-{Slot}.svg`
- Art direction (text description for future shoot)
- Reason (why photoshoot pending)

**Characteristics:**
- Generated automatically during build.
- Styled to reflect body family + character brand.
- Used in gallery/browse views; placeholder cards indicate "coming soon".

**Notes:**
- Placeholder character still has a full persona & story (not a stub).
- Story is aspirational, grounded in body data; does not mention photoshoot gap.

---

### Head Code / Face Code

**Definition:** Identifier for a head sculpture and face variant.

**Head Code:** Unique head sculpt (e.g., `ZXE223_1`)

**Face Code:** Optional variant of a head (e.g., `makeup_v2`, rare)

**Notes:**
- Every product has a head code.
- A head can be paired with multiple body codes → multiple product SKUs.
- Face code is rarely used; nearly always `null`.

---

### Spec Card

**Definition:** A measurement/specification sheet image for a body type.

**Asset Path:** `assets/Measure/{BodyCode}_pc_3.0.webp`

**Properties:**
- Photo of body (standing, measured points visible)
- Overlaid measurement annotations (bust, waist, hip lines)
- Dimensions + ratios printed on image
- Version stamp (e.g., "v3.0")

**Usage:**
- Buyer reference (detailed measurements)
- Visual confirmation of body classification
- Archive for spec revisions

---

## Curation & Workflow

### Character Overlay

**Definition:** Hand-curated persona edits applied after auto-generation.

**File:** `db/character_overlay.json`

**Fields (all optional):**
- `persona.*` — name, title, tagline, story, profile edits
- `photoshoot.hero` — hero image selection override

**Merge Strategy:** Shallow merge (only fields present in overlay override; others inherit).

**Notes:**
- Used to fix auto-generated names, refine stories, select best hero images.
- Does not delete; only adds/overrides.

---

### Body Measurements Curation

**Definition:** Hand-verified body specifications (height, cup, bust/waist/hip, spec card path).

**File:** `db/body_measurements.json`

**Fields (all optional):**
- Measurement values (override computed if different)
- `family_override` — force family classification (bypasses algorithm)
- `notes` — documentation

**Merge Strategy:** Authoritative (values here override computed values).

**Notes:**
- Source of truth for all body specs.
- Used by `build_profiles.py` as input.

---

### Story Input Files

**Definition:** Per-series narrative data provided by writers.

**Files:** `db/_stories_{series_slug}.json`
- `_stories_k-series.json`
- `_stories_inspiration.json`
- `_stories_fusion.json`
- `_stories_sle.json`

**Structure:**
```json
{
  "Character-ID": {
    "story": "120–180 word narrative",
    "profile": {
      "personality": "adjectives",
      "ideal_setting": "description",
      "signature": "detail",
      "for_you_if": "buyer profile"
    }
  }
}
```

**Merge Process:** `merge_stories.py` folds these into `db/character_stories.json`.

---

## Data Files & Artifacts

### Catalog Files

**`db/catalog.json`** — Master product index (series + products). Generated by `build_db.py`.

**`db/body_profiles.json`** — Body classification (WHR, BWR, families). Generated by `build_profiles.py`.

**`db/body_types.json`** — Body aggregates (4 characters each). Generated by `build_characters.py`.

**`db/characters.json`** — Full character inventory (108 records). Generated by `build_characters.py`, enhanced by `merge_stories.py`.

**`db/character_stories.json`** — Merged narratives. Generated by `merge_stories.py`.

---

### Curation Files (Hand-Edited)

**`db/body_measurements.json`** — Spec cards + measurement overrides.

**`db/character_overlay.json`** — Persona edits + image selection.

**`db/_stories_*.json`** — Writer input (stories + profiles per series).

---

### Transient Files (Not Tracked)

**`db/catalog.db`** — SQLite database (intermediate state during build).

**`assets/thumbs/`** — Generated thumbnail images.

**`assets/placeholders/`** — Generated SVG placeholders.

**`assets/{Series}/`** — Product photoshoots (live images; not tracked due to size ~260 MB).

---

## Build Pipeline

### Orchestrator

**Definition:** The master build executor managing parallel execution, idempotence, and state tracking.

**Entry Point:** `python scripts/build_orchestrator.py`

**Key Modes:**
- Normal run: `--resume` if last run failed
- Full rebuild: `--reset` (drop DB, re-scan all)
- Specific stages: `--stages=profiles,characters`
- Diagnostics: `--json`, `--dry-run`

**Exit Codes:** 0 (success), 1 (fatal), 2 (skipped), 3 (partial failure)

---

### Build Stages (in order)

1. **`db`** — Ingest catalog, scan assets.
2. **`profiles`** — Compute WHR/BWR, classify families.
3. **`characters`** — Generate 4 personas per body.
4. **`merge_stories`** — Fold writer narratives.
5. **`thumbs`** — Generate thumbnails + hero images.
6. **`pages`** — Generate page inventory.

**Parallelism:** Stages 2–3 run concurrently; others sequential.

---

## Frontend & Runtime

### ZX (Global Object)

**Definition:** The single global JS object (window.ZX) providing all runtime APIs.

**Responsibilities:**
- Load catalog data asynchronously
- Render UI components (nav, footer, character cards)
- Handle navigation & routing
- Manage analytics & session tracking
- Operate comparison tool

**Location:** `assets/site.js` (single file, no npm deps)

**Key Methods:**
- `ZX.load()` — Initialize
- `ZX.getCharacter(id)` — Fetch character
- `ZX.track(eventName, payload)` — Analytics
- `ZX.getCompareBodies()` — Comparison state
- `ZX.recommend(filters)` — Recommendation

---

### Session Storage

**Definition:** Browser storage for user state (persists during session + across sessions).

**Keys:**
- `zx_compare_bodies` → JSON array of body codes in comparison tool
- `zx_analytics_session_id` → Unique session ID for tracking
- `zx_analytics_debug` → Debug mode flag (0|1)

**Scope:** `localStorage` (fallback to `sessionStorage` if unavailable)

---

## Analytics

### Event Schema

**Definition:** Structured analytics event format (GA4 compatible).

**Core Fields:**
- `event_name` — Canonical event (e.g., `character_view`, `compare_add`)
- `session_id` — Unique session ID
- `timestamp` — ISO 8601 time
- Custom fields (context-dependent)

**Analytics Version:** `2026-06-06` (schema version for breaking change detection)

---

### Sanity Thresholds

**Definition:** Acceptable ranges for analytics metrics (used for anomaly detection).

**File:** `docs/pdr/PDR-analytics-sanity-thresholds.json`

**Examples:**
- Event latency (milliseconds)
- Session duration (seconds)
- Click-through rates (%)
- Page view counts per session

**Usage:** During testing & validation; flags outliers that might indicate bugs.

---

## Deployment

### Full Package

**Definition:** Deliverable ZIP containing all code + images + metadata.

**Generator:** `python scripts/build_package.py`

**Contents:**
- All HTML pages
- `assets/site.css` + `assets/site.js`
- Full image tree (photoshoots + thumbnails + placeholders)
- All data JSON files
- Metadata (analytics config, etc.)

**Size:** ~260 MB (compressed ~80 MB)

**Distribution:** Uploaded to Google Drive for stakeholders.

---

### Caddy

**Definition:** Local development server (reverse proxy + file serving).

**Config File:** `Caddyfile`

**Features:**
- HTTPS (auto TLS via localhost)
- Maps `howiez.local` → local folder
- Serves all file types

**Usage:** `caddy run`

---

## Frequently Confused Terms

### Body vs. Character

- **Body** = physical silhouette (reusable, 27 total)
- **Character** = branded persona (unique personality, 108 total)
- Relation: 1 body → exactly 4 characters

### Character vs. Photoshoot

- **Character** = persona record (name, story, profile, status)
- **Photoshoot** = real product SKU with images
- Relation: 1 character → 0 or 1 photoshoot (if live); else placeholder

### Series vs. Family

- **Series** = product line (K, Inspiration, Fusion, SLE)
- **Family** = body archetype (Classic, Icon, Muse, Siren, Empress, Sculpt)
- Relation: Orthogonal (Series is brand grouping; Family is morphometric archetype)

### WHR vs. BWR

- **WHR** = waist ÷ hip (silhouette profile)
- **BWR** = bust ÷ waist (upper-body emphasis)
- Both required for family classification

---

## Abbreviations

| Abbreviation | Meaning |
|---|---|
| **WHR** | Waist-Hip Ratio |
| **BWR** | Bust-Waist Ratio |
| **SKU** | Stock Keeping Unit (product code) |
| **CMS** | Content Management System |
| **GA4** | Google Analytics 4 |
| **SLE** | (Series name; no formal expansion) |
| **PDR** | Product Direction Record |
| **ZX** | Global runtime object (ZELEX runtime) |

---

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — System design overview
- [DATA-SCHEMA.md](DATA-SCHEMA.md) — Detailed schema specs
- [API.md](API.md) — Runtime API reference
- [DECISIONS.md](DECISIONS.md) — Architecture decision log
