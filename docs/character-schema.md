# Character Profile Schema — Proposal

## The hierarchy

```
Series (4: K, Inspiration, Fusion, SLE)
 └─ Body Type (27 bodies — measurements, WHR/BWR, Body Family, spec card)
     └─ Character (exactly 4 per body type  →  108 total)
         └─ Photoshoot  (a real product image set)   ── or ──   Placeholder
```

- A **Body Type** is the measurement architecture (e.g. `ZX160J`). It owns the
  objective data: stature, WHR/BWR, Body Family, spec card.
- A **Character** is a named persona built on that body. Four per body type.
  What differentiates the four = the **face/head** (sculpt + makeup + skin tone)
  plus persona identity.
- A **Photoshoot** is one of our actual product folders (head+body image set).
  A character links to one. When no shoot exists for that slot → **placeholder**.

Counts today: 108 characters; **89 slots have a real photoshoot, 19 are placeholders.**
Bodies with more than 4 photographed heads keep the surplus in an
`additional_photoshoots` pool on the body type (e.g. ZG170C has 42 — 4 become
characters, 38 stay in the pool, available for swap or future characters).

---

## Character record (the core entity)

```jsonc
{
  "character_id": "SLE-ZX160J-03",      // {series_code}-{body}-{slot:02}
  "slot": 3,                            // 1..4 within the body type
  "series": "SLE",
  "status": "live",                     // "live" | "placeholder"

  // ── links back to BODY TYPE (denormalized for convenience) ──
  "body_code": "ZX160J",
  "body": {
    "family": "The Siren", "silhouette": "Bust-dominant fantasy",
    "height_cm": 160, "cup": "J", "weight_kg": 37.2,
    "bust": 88.5, "waist": 51.5, "hip": 101.5,
    "WHR": 0.507, "BWR": 1.718, "bust_drop_cm": 32.5,
    "spec_card": "assets/Measure/ZX160J_pc_3.0.webp"
  },

  // ── CHARACTER identity ──
  "persona": {
    "name": "Vesper",                   // character given-name
    "title": "The Fantasy",             // archetype title
    "tagline": "Pure imagination, made physical.",
    "energy": "Explosive curves · tiny waist · gravity-defying",
    "target_buyer": "Character / anime crossover",
    "positioning": "…one-paragraph market rationale…",
    "premium": "+35%"
  },

  // ── FACE/head defining this character (null fields if placeholder) ──
  "face": { "head_code": "ZXE223_1", "face_code": null, "skin_tone": "Tan" },

  // ── PHOTOSHOOT linkage (real images) ──
  "photoshoot": {
    "product_code": "ZXE223_1_ZX160J",
    "folder": "assets/SLE-Series/ZXE223_1_ZX160J",
    "hero": "assets/SLE-Series/ZXE223_1_ZX160J/ZXE223_1_ZX160J-101.jpg",
    "hero_thumb": "assets/thumbs/SLE-Series/ZXE223_1_ZX160J/…-101.jpg",
    "gallery": ["…","…"], "image_count": 22,
    "price": "2899.00", "live_handle": "…"
  },

  // ── PLACEHOLDER block (present only when status = placeholder) ──
  "placeholder": {
    "reason": "No 3rd head photographed on this body yet",
    "hero": "assets/placeholders/SLE-The-Fantasy-03.svg",
    "art_direction": "Tan skin, dramatic studio light, ¾ turn — see body family."
  }
}
```

### Body-type record (aggregates its 4 characters + surplus pool)

```jsonc
{
  "body_code": "ZG170C", "series": "I", "family": "The Muse",
  "height_cm": 170, "cup": "C", "weight_kg": 36.1,
  "WHR": 0.686, "BWR": 1.357, "spec_card": "assets/Measure/ZG170C-cm-pc.webp",
  "characters": ["I-ZG170C-01","I-ZG170C-02","I-ZG170C-03","I-ZG170C-04"],
  "photoshoot_count": 43,
  "additional_photoshoots": ["GE02_1","GE03_2","…38 more…"]   // surplus, not lost
}
```

---

## Storage

- New tables in `catalog.db`: `characters`, `body_type_pool` (surplus shoots).
- Exports: `db/characters.json` (all 108), kept beside `body_profiles.json`.
- Curated identity lives in a hand-editable `db/character_overlay.json`
  (names/taglines/positioning), merged at build time — same pattern as the
  existing `character_profiles.json` and `body_measurements.json`.
- Placeholders get generated SVG art under `assets/placeholders/`.

## Locked design decisions (2026-06-05)

1. **The 4 differ by head/face** — each character = a distinct photographed head on the body.
2. **Placeholders borrow a sibling shoot** on the same body, flagged `representative_only:true` + an `art_direction` note for the future shoot.
3. **Personas auto-generated** in the brief's voice (name banks per series + family-derived titles/taglines), overridable per-character via `db/character_overlay.json`.
4. **Surplus pooled** — bodies with >4 heads keep 4 characters; the rest go to `additional_photoshoots[]` on the body type.

## Implemented

`scripts/build_characters.py` realizes this schema. Current output:

| Series | Characters | Live | Placeholder |
|---|---|---|---|
| K-Series | 8 | 4 | 4 |
| Inspiration | 20 | 17 | 3 |
| Fusion | 12 | 5 | 7 |
| SLE | 68 | 63 | 5 |
| **Total** | **108** | **89** | **19** |

138 surplus photoshoots pooled. Outputs: `db/characters.json`, `db/body_types.json`,
tables `characters` + `body_type_pool`. Pipeline order: `build_db.py` →
`build_profiles.py` → `build_characters.py` → `make_thumbs.py`.

Known refinements (all overlay-editable, non-blocking): the 4 characters on a body
currently share a family-derived tagline; bodies without spec cards (ZF161D + 10
SLE torsos) have `family:null`; SLE photoshoots have no price yet (live-variant
link covered only the original I/K/Fusion SKUs).
