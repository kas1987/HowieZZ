# Architecture Decision Log (ADL)

A record of major design decisions, rationales, and trade-offs in ZELEX Character Atlas.

> See also: [ARCHITECTURE.md](ARCHITECTURE.md), [GLOSSARY.md](GLOSSARY.md)

---

## Table of Contents

1. [No Framework, No Build Step](#no-framework-no-build-step)
2. [6 Body Families (Fixed Classification)](#6-body-families-fixed-classification)
3. [4 Characters Per Body](#4-characters-per-body)
4. [Static JSON Data](#static-json-data)
5. [Morphometric Classification (WHR & BWR)](#morphometric-classification-whr--bwr)
6. [Hand-Curated Overlays](#hand-curated-overlays)
7. [Images Excluded from Git](#images-excluded-from-git)
8. [Parallel Build Pipeline](#parallel-build-pipeline)
9. [Single Global JS Object (ZX)](#single-global-js-object-zx)
10. [SQLite as Transient State](#sqlite-as-transient-state)

---

## No Framework, No Build Step

**Decision:** Use vanilla HTML/CSS/JS; no React, Vue, framework, or build tool (webpack, vite, etc.).

**Date:** 2025-Q1 | **Status:** Approved | **Confidence:** High

### Rationale

1. **Deployment simplicity:** No build step = instant deploy. No node_modules, no bundler bugs, no transpilation errors.
2. **Runtime overhead:** Zero JS dependencies. Pages load immediately; no webpack/React overhead.
3. **Audit-ability:** Single 35 KB JS file; easy to review, debug, and understand.
4. **Maintenance:** Minimal tech debt. No version conflicts, no deprecated library churn.
5. **Suitable use case:** A static, read-heavy site with finite data (108 characters, 27 bodies, 4 series).

### Trade-offs

- **Con:** Manual DOM management; no virtual DOM, no hooks, no state management library.
- **Con:** Code duplication across pages (no component re-use); pages copy common patterns.
- **Con:** No hot reload during development; must refresh browser.
- **Mitigation:** Extract common patterns into library functions in `site.js`.

### Alternatives Considered

1. **Next.js / Nuxt:** Over-engineered for a static site; adds build complexity, deployment overhead.
2. **Astro:** Better fit than Next.js, but still adds build step + node_modules.
3. **Static site generator (Hugo, Jekyll):** Adds another tool; template language learning curve; tight coupling to build process.

### Decision Outcome

✓ **Chosen:** Vanilla stack. Proven on three deployed versions (2024–2026).

---

## 6 Body Families (Fixed Classification)

**Decision:** Define exactly 6 body archetypes (The Classic, Icon, Muse, Siren, Empress, Sculpt); classify all bodies into these families using morphometric criteria (WHR & BWR).

**Date:** 2025-Q2 | **Status:** Approved | **Confidence:** High

### Rationale

1. **Cognitive load:** Buyers need to understand body categories. 6 is a memorable number (rule of 7±2).
2. **Marketing tier:** Each family has a distinct positioning + price premium (15–35%).
3. **Scalability:** New bodies automatically classify into existing families; no schema change needed.
4. **Data-driven:** Classification is algorithmic (WHR/BWR ranges), not subjective.
5. **Differentiation:** Drives premium positioning ("Choose your silhouette archetype").

### Morphometric Basis

**Why WHR & BWR?**
- **WHR (Waist-Hip Ratio):** Captures overall silhouette profile (straight vs. curvy).
- **BWR (Bust-Waist Ratio):** Captures upper-body emphasis (modest vs. dramatic).
- **Combined:** Two orthogonal axes covering 80% of human silhouette diversity.
- **Objective:** Computable from spec-card measurements; no subjective guessing.

### Family Ranges (Current)

| Family | WHR | BWR | Silhouette | Position |
|--------|-----|-----|-----------|----------|
| Classic | 0.68–0.72 | 1.4–1.5 | Timeless hourglass | Prestige, heritage |
| Icon | 0.60–0.65 | 1.5–1.6 | Glamour model | Editorial, photography |
| Muse | 0.65–0.70 | 1.3–1.4 | Tall, hip-dominant | Western naturalism |
| Siren | 0.55–0.60 | 1.6–1.8 | Bust-dominant fantasy | Fantasy, maximalist |
| Empress | 0.70–0.75 | 1.5–1.7 | Majestic curves | Luxury, confidence |
| Sculpt | 0.50–0.55 | 1.2–1.3 | Athletic, sculptural | Modern, minimalist |

### Trade-offs

- **Con:** Bodies near family boundaries (WHR 0.64–0.66) are ambiguous.
- **Con:** Some real bodies fall outside all ranges (Unclassified, `family = null`).
- **Mitigation:** `body_measurements.json` → `family_override` field allows manual assignment.

### Edge Cases

**Out-of-Range Bodies:**
- A few SLE bodies have no spec card (no measurements available).
- These get `family = null` (Unclassified).
- Rendering still works (UI falls back to series mood + height).

### Alternatives Considered

1. **Dynamic clustering (k-means):** Mathematically elegant, but opaque to buyers ("What does 'Cluster 3' mean?").
2. **Subjective categories ("Petite", "Curvy", "Tall"):** Simpler for buyers, but harder to scale; no objective rule for new bodies.
3. **Single-axis classification (WHR only):** Insufficient; misses upper-body emphasis (BWR).
4. **Buyer-selected categories (quiz):** Works for marketing, but doesn't classify the actual body data.

### Decision Outcome

✓ **Chosen:** 6 families, WHR/BWR algorithm with manual override. Proven marketing messaging.

---

## 4 Characters Per Body

**Decision:** Every body hosts exactly 4 named characters, differentiated by head/face sculpture (+ makeup, skin tone).

**Date:** 2025-Q3 | **Status:** Approved | **Confidence:** Medium

### Rationale

1. **Variety without overwhelming:** 4 is enough to show personality range; 1 would be limiting, 10 would be confusing.
2. **Sales alignment:** Each body → 4 SKUs (one per character/head pairing).
3. **Realistic collection:** 4 × 27 bodies = 108 characters — manageable for a catalog, enough for discovery.
4. **Manufacturing reality:** Bodies are hand-crafted; producing 4 distinct heads per body is a reasonable batch size.
5. **Narrative consistency:** 4 siblings on one body allows character siblings/kin relationships (sister dynamics).

### Differentiation

**Each character on a body differs by:**
- Head sculpture (male/female variation, face proportions)
- Makeup (natural, bold, editorial, etc.)
- Skin tone (pale, tan, medium, etc.)
- **NOT by body measurements** (all 4 siblings have identical body measurements)

**Story uniqueness:**
- All 4 share body architecture (height, cup, family) but have distinct personalities.
- Stories reflect individual character arcs, not body variations.

### Trade-offs

- **Con:** Limits persona permutations. No custom head+body mixing in the catalog view.
- **Con:** Requires hand-curation of 108 distinct personas (names, stories, profiles).
- **Mitigation:** Auto-generation + overlay curation model balances work + consistency.

### Implications

**Inventory:**
- 27 bodies × 4 characters = 108 characters (perfect for marketing "complete collection" messaging).
- Surplus heads (bodies with >4 photoshoots) are pooled in `additional_photoshoots[]` for future swaps or new characters.

**Placeholder Handling:**
- If only 2 real photoshoots exist for a body, the 3rd and 4th characters get placeholder SVGs.
- Placeholder characters still have full personas & stories (aspirational, not stubs).
- When a new photoshoot arrives, placeholder can be upgraded to live (overlay edit + image update).

### Alternatives Considered

1. **1 character per body:** Simple, but no variety; less engaging for browsing.
2. **Unlimited characters per body:** Overwhelming; no curation; becomes a generic product catalog.
3. **Variable count (e.g., 2–5 per body):** Inconsistent; UX complexity (what if some bodies have 2, others 6?).
4. **8 characters per body (2 genders × 4 variants):** Would be 216 characters total; exceeds practical curation effort.

### Decision Outcome

✓ **Chosen:** 4 characters per body (fixed). Justified by sales + brand + curation constraints.

---

## Static JSON Data

**Decision:** All catalog data is generated at build time and exported to JSON files; no database queries at runtime.

**Date:** 2025-Q1 | **Status:** Approved | **Confidence:** High

### Rationale

1. **Performance:** No server latency; data is baked into the CDN.
2. **Scalability to read:** Perfect for a read-heavy, write-rarely site.
3. **Simplicity:** No database connection strings, no SQL injection risks, no query optimization.
4. **Portability:** JSON is self-documenting; can be version-controlled (partially) + audited.
5. **Finite data:** Catalog is known at build time (108 characters, 27 bodies, 4 series — unchanging at runtime).

### Data Flow

```
(build time)
Product feed + spec cards
  ↓ build_db.py
catalog.db (SQLite, transient)
  ↓ build_profiles.py, build_characters.py, merge_stories.py
db/catalog.json, db/characters.json, db/body_profiles.json
  ↓ build_package.py
zelex-deliverable.zip

(runtime)
Browser fetches db/catalog.json, etc.
ZX.load() caches in memory
No further I/O
```

### Trade-offs

- **Con:** Adding a new body requires a rebuild + redeploy.
- **Con:** Real-time product availability requires periodic sync (Shopify feed polling).
- **Mitigation:** Deploy ~2 per week (manageable manual schedule). Automated Shopify sync can pull feed periodically.

### Data Freshness

**Current model:**
- Build runs ~1–2 per week.
- Data is ~5 minutes old at worst (time between code commit + deploy).
- Real-time sync: optional Shopify polling (`sync_shopify_feed.py` can run on a schedule).

### Alternatives Considered

1. **Runtime database (Firebase, Supabase, Airtable):** Adds latency, cold-start overhead, API costs, dependency on third-party availability.
2. **Server-side rendering (Node + Express):** Defeats "no framework" goal; adds infrastructure (Heroku, AWS, etc.).
3. **Hybrid (static HTML + API calls):** More complex; no perf benefit; extra failure mode (API down while HTML cached).

### Decision Outcome

✓ **Chosen:** Static JSON, built at build time, cached in CDN. Proven fast + reliable.

---

## Morphometric Classification (WHR & BWR)

**Decision:** Use two computed ratios (Waist-Hip & Bust-Waist) as the basis for body family classification.

**Date:** 2025-Q2 | **Status:** Approved | **Confidence:** High

### Rationale

1. **Objective:** Computable from measurement spec cards; not subjective.
2. **Orthogonal:** WHR and BWR capture independent dimensions of silhouette.
3. **Grounded in body science:** Used in anthropometry, fashion, and product design.
4. **Interpretable:** Non-technical buyers can understand "waist-to-hip" and "bust emphasis".
5. **Scalable:** Works for any new body added.

### Formula & Ranges

**WHR = waist_cm ÷ hip_cm**
- Typical range: [0.4, 0.9]
- Lower (0.4–0.6): athletic, straight silhouette
- Mid (0.6–0.7): balanced, hourglass
- Higher (0.7–0.9): dramatic curves, majestic

**BWR = bust_cm ÷ waist_cm**
- Typical range: [1.0, 2.0]
- Lower (1.0–1.3): modest bust, streamlined
- Mid (1.3–1.5): balanced
- Higher (1.5–2.0): dramatic bust, fantasy proportions

### Validation

**Current corpus:**
- 27 bodies, all within [0.4, 0.9] WHR and [1.0, 2.0] BWR ranges.
- 2 bodies (SLE-torsos, no upper body) have `family = null` (out-of-range).
- 25 bodies successfully classified into 6 families.
- Manual override available for edge cases via `body_measurements.json` → `family_override`.

### Trade-offs

- **Con:** Assumes linear family ranges; real silhouettes may not cluster perfectly.
- **Con:** Doesn't capture height, which matters for visual proportion.
- **Mitigation:** Height is rendered separately (body spec card image + character height field).

### Alternatives Considered

1. **Three-factor model (WHR + BWR + height):** More accurate, but harder to visualize (3D space).
2. **Single-factor (WHR only):** Simpler, but ignores bust emphasis (misses Siren vs. Empress distinction).
3. **Subjective categories ("Curvy", "Petite"):** Not scalable; no objective rule for new bodies.

### Decision Outcome

✓ **Chosen:** WHR + BWR, two-dimensional classification. Validated across 27 bodies.

---

## Hand-Curated Overlays

**Decision:** Auto-generate persona data (names, stories, profiles) from algorithms + templates, then allow hand-curation via JSON overlay files.

**Date:** 2025-Q3 | **Status:** Approved | **Confidence:** High

### Rationale

1. **Consistency:** Auto-generation ensures all 108 characters have complete data (no gaps).
2. **Efficiency:** 80% of work is mechanical (slot assignment, family-derived titles).
3. **Quality control:** Final 20% (names, stories, positioning) is hand-polished.
4. **Auditability:** All edits are in JSON files; changes are reviewable + version-controlled.
5. **Non-destructive:** Overlay only adds/overrides; missing entries inherit auto-generated data.

### Overlay Files

1. **`db/character_overlay.json`** — Persona edits (name, title, tagline, story, profile).
2. **`db/body_measurements.json`** — Spec card + measurement overrides (includes `family_override`).
3. **`db/_stories_*.json`** — Writer-provided stories (per series).

### Merge Strategy

```
auto-generated character
  ↓ merge with character_overlay.json
character with user edits
  ↓ merge with _stories_*.json
character with stories
  ↓ final output
db/characters.json
```

**Merge is shallow:** Only fields present in overlay override; others inherit.

### Trade-offs

- **Con:** Two sources of truth (auto-generated + overlay). Risk of divergence.
- **Mitigation:** Both are JSON; can be diffed + validated. Schema is consistent.

### Workflow

1. **Day 1:** Run `build_orchestrator.py` → auto-generates 108 characters.
2. **Day 2–5:** Story writers fill `db/_stories_*.json`.
3. **Day 6–7:** Brand team edits `db/character_overlay.json` (names, hero images, positioning).
4. **Day 8:** Final build run; output is `db/characters.json`.

### Alternatives Considered

1. **Fully manual:** 108 characters × 5 fields = 540 hand-written records. Unsustainable.
2. **Fully automated:** No brand control; names + stories + positioning feel generic.
3. **Spreadsheet + sync script:** Works, but adds another tool (Excel/Airtable); harder to version-control.

### Decision Outcome

✓ **Chosen:** Auto-generate + hand-curate overlay. Proven on 108 characters (2025–2026).

---

## Images Excluded from Git

**Decision:** Do not track product images (~260 MB) in the git repository. Deliver as a packaged build (ZIP) distributed separately.

**Date:** 2025-Q1 | **Status:** Approved | **Confidence:** High

### Rationale

1. **Repository size:** Git is not a CDN. 260 MB of images bloats clone time, CI/CD runs, and development.
2. **Binary efficiency:** Image delta compression is poor; each new version stores nearly the full file.
3. **Distribution:** Packaged build (ZIP) is faster for stakeholders to download + extract.
4. **Media workflow:** Images are managed separately (Dropbox, Google Drive, or internal asset management).

### Repository vs. Package

**What's tracked in git:**
- HTML, CSS, JS (code)
- JSON data files (catalog, characters, etc.)
- Spec-card images (small, measurement reference only; ~5 MB)
- Documentation

**What's NOT tracked:**
- Product photoshoots (assets/K-Series/, assets/I-Series/, etc.; ~200 MB)
- Generated thumbnails (assets/thumbs/; ~30 MB)
- Placeholder SVGs (assets/placeholders/; ~2 MB)

**Result:** Bare clone shows structure + text, no images. Full site requires packaged build.

### Packaged Build Workflow

```
Build machine:
  1. git clone
  2. python scripts/build_orchestrator.py
  3. Sync images from Google Drive / Dropbox
  4. python scripts/build_package.py
  5. Upload zelex-deliverable.zip to Google Drive

Stakeholder:
  1. Download zelex-deliverable.zip
  2. Unzip
  3. Open index.html in browser
  → Full site with all images
```

### Trade-offs

- **Con:** Bare clone doesn't show final appearance (useful for development, but confusing for new contributors).
- **Con:** Image sync is manual (no automatic versioning via git).
- **Mitigation:** README clearly documents this; setup instructions explain where to find packaged build.

### `.gitignore` Rules

```
assets/K-Series/
assets/I-Series/
assets/Fusion-Series/
assets/SLE-Series/
assets/thumbs/
assets/placeholders/
db/catalog.db
```

### Alternatives Considered

1. **Git LFS (Large File Storage):** Tracks images in git but with pointer files. Adds infrastructure + complexity; still slow.
2. **CDN URL placeholders:** Hardcode production CDN paths in code; images download at runtime. No offline browsing.
3. **Tiered Git:** Keep full history in private repo, public repo has `.gitignore`. More complex workflow.

### Decision Outcome

✓ **Chosen:** Exclude images from git; deliver as packaged ZIP. Proven workflow (2025–2026).

---

## Parallel Build Pipeline

**Decision:** Structure the build pipeline to allow certain stages to execute in parallel, with intelligent caching and resume capability.

**Date:** 2026-Q1 | **Status:** Approved | **Confidence:** High

### Rationale

1. **Speed:** Profiles + characters stages can run concurrently (~3x speedup vs. serial).
2. **Resiliency:** If a stage fails, can resume from that point without re-running earlier stages.
3. **Idempotence:** Stages skip if inputs unchanged; no redundant work.
4. **Observability:** Each stage tracked in `db/.orchestrator/state.json`; audit trail of builds.

### Execution Model

```
Group 0 (init):
  └─ db                   [5s]

Group 1 (parallel):
  ├─ profiles             [3s] ⎯⎯⎯⎯⎯⎯┐
  └─ characters           [4s] ⎯⎯⎯⎯ (concurrent)

Group 2 (post):
  ├─ merge_stories        [1s]
  └─ thumbs               [5s]

Group 3 (inventory):
  └─ pages                [2s]

Total: ~15s (parallel) vs. ~25s (serial)
```

### State Tracking

Every build run produces a state record:

```json
{
  "timestamp": "2026-06-21T13:15:00Z",
  "status": "success",
  "duration_secs": 15.2,
  "stages": {
    "db": {
      "status": "complete",
      "duration_secs": 5.1,
      "input_hash": "…",
      "output_hash": "…"
    },
    …
  }
}
```

### Resume Logic

If a run fails:

```bash
python scripts/build_orchestrator.py --resume
# Reads last state entry
# Identifies first failed stage
# Re-runs from that stage onward
# Reuses outputs from earlier stages
```

### Trade-offs

- **Con:** Parallel execution adds complexity (thread safety, race conditions).
- **Con:** Harder to debug (output mixed from concurrent processes).
- **Mitigation:** Each stage writes to separate files; no shared state during execution.

### Idempotence Strategy

```
input_hash = hash(modification_times + file_sizes of input files)
if input_hash == cached_hash && outputs_exist:
  skip stage
else:
  run stage
  update cache
```

**Skipping logic:**
- Stage is skipped if inputs unchanged and outputs exist.
- Can be forced with `--reset` or `--force`.

### Alternatives Considered

1. **Serial execution:** Simpler, but slower (25s vs. 15s). Acceptable, but suboptimal.
2. **Task queue (Celery, etc.):** Overkill for a simple pipeline; adds infrastructure.
3. **Make / Makefile:** Works, but less flexible than Python + orchestrator.

### Decision Outcome

✓ **Chosen:** Parallel pipeline with idempotence + resume. Implemented in `build_orchestrator.py`.

---

## Single Global JS Object (ZX)

**Decision:** Expose all runtime functionality via a single global object `window.ZX`, rather than multiple globals or modules.

**Date:** 2025-Q1 | **Status:** Approved | **Confidence:** Medium-High

### Rationale

1. **Namespace collision:** Single global `ZX` is less risky than `catalog`, `character`, `track`, etc.
2. **Discoverability:** Developers can `console.log(ZX)` to see all available methods.
3. **Testability:** Single object is easier to mock + test.
4. **Consistency:** All pages use the same API; no learning curve.

### API Organization

```javascript
// Data loading
ZX.load()
ZX.getModel()

// Data access
ZX.getCharacter(id)
ZX.getBody(code)
ZX.getCharactersByFamily(family)

// UI rendering
ZX.mountNav()
ZX.renderCharacterCard(character)

// Navigation
ZX.qs(paramName)
ZX.setParam(name, value)
ZX.navigate(path, params)

// Analytics
ZX.track(eventName, payload)
ZX.getSessionId()

// Comparison tool
ZX.getCompareBodies()
ZX.addCompareBody(code)
```

### Code Organization

**Single file:** `assets/site.js` (no module system, no imports)

```javascript
window.ZX = (function() {
  // Private state
  let _model = null;
  
  // Public API
  return {
    load: function() { … },
    getModel: function() { … },
    track: function() { … },
    …
  };
})();
```

### Trade-offs

- **Con:** No module encapsulation. All code in one file (35 KB).
- **Con:** Risk of namespace pollution if third-party code defines `window.ZX`.
- **Mitigation:** Prefix all methods with `ZX.*`; document in README.

### Alternatives Considered

1. **Multiple globals:** `window.catalog`, `window.characters`, `window.track`, etc. More granular, but harder to discover.
2. **ES modules:** Requires a bundler (webpack, vite). Violates "no build step" principle.
3. **UMD / CommonJS wrapper:** Adds complexity; overkill for a static site.

### Decision Outcome

✓ **Chosen:** Single `ZX` global object, IIFE pattern in `site.js`.

---

## SQLite as Transient State

**Decision:** Use SQLite (`db/catalog.db`) as an intermediate database during the build pipeline, but do not track it in git or deploy it.

**Date:** 2025-Q1 | **Status:** Approved | **Confidence:** High

### Rationale

1. **Pipeline efficiency:** SQL queries are faster than re-scanning asset folders for each stage.
2. **Normalization:** SQL schema prevents data duplication during intermediate steps.
3. **Transient nature:** DB is rebuilt every run; no need to persist between builds.
4. **Simplicity:** Better than passing large JSON files between Python scripts.

### Lifecycle

```
Build starts
  ↓ build_db.py
  Creates / populates db/catalog.db
  (Reads asset folders, Shopify feed)
  ↓
  build_profiles.py, build_characters.py
  Query db/catalog.db for data
  ↓ Export to JSON
  Produce db/characters.json, db/body_types.json
  ↓
Build ends
  db/catalog.db is not tracked / deployed
  Only JSON outputs matter
```

### Database Schema

Tables:
- `series` — Product lines (K, Inspiration, Fusion, SLE)
- `bodies` — Body architectures (27 bodies)
- `products` — Product SKUs (head + body combinations)
- `characters` — Persona records (108 characters)

(See DATA-SCHEMA.md for full schema.)

### Trade-offs

- **Con:** Database is ephemeral; can't query historical state (without archiving).
- **Con:** Python + SQLite adds a dependency (though SQLite is built-in).
- **Mitigation:** All meaningful data is exported to JSON; if DB is lost, rebuild via `--reset`.

### Why Not Keep the DB?

1. **Git doesn't track binary files well:** Binary deltas are large; clones would be slow.
2. **No runtime use:** Frontend never queries DB; all data is JSON.
3. **Build artifacts:** DB is a build artifact, not source code or configuration.

### Alternatives Considered

1. **All JSON throughout:** No SQL; pass JSON between stages. Slower (no indexing), more RAM.
2. **Keep deployed DB:** Deploy SQLite to CDN; runtime queries DB. Adds latency; defeats static-site goal.
3. **Use a different DB (PostgreSQL):** Overkill; requires running a server; not portable.

### Decision Outcome

✓ **Chosen:** SQLite as transient state during build; export to JSON for deployment.

---

## Summary Table

| Decision | Date | Status | Confidence | Reversibility |
|----------|------|--------|------------|---------------|
| No framework, no build | Q1 2025 | Approved | High | Medium (hard to retrofit framework) |
| 6 Body Families | Q2 2025 | Approved | High | Low (marketing messaging tied to families) |
| 4 Characters/Body | Q3 2025 | Approved | Medium | Medium (affects SKU count) |
| Static JSON data | Q1 2025 | Approved | High | High (can add DB layer later) |
| WHR & BWR classification | Q2 2025 | Approved | High | Low (family ranges are published) |
| Hand-curated overlays | Q3 2025 | Approved | High | High (just a file format) |
| Images excluded from git | Q1 2025 | Approved | High | Medium (requires CDN setup) |
| Parallel build pipeline | Q1 2026 | Approved | High | High (can revert to serial) |
| Single global ZX object | Q1 2025 | Approved | Medium | Medium (API redesign effort) |
| SQLite as transient state | Q1 2025 | Approved | High | High (can switch to JSON-only) |

---

## Process for Future Decisions

1. **Identify the decision:** What problem are we solving?
2. **List alternatives:** At least 3 options.
3. **Evaluate trade-offs:** Pros, cons, reversibility.
4. **Document here:** Add new section with rationale + decision.
5. **Get approval:** Architect review + team sign-off.
6. **Implement:** Follow decision in code.
7. **Review:** Revisit in 3–6 months; assess if decision still holds.

---

## References

- [ARCHITECTURE.md](ARCHITECTURE.md) — System overview
- [GLOSSARY.md](GLOSSARY.md) — Terminology
- [DATA-SCHEMA.md](DATA-SCHEMA.md) — Schema details
- Product Direction Records (PDR-*.md) — Business rationale
