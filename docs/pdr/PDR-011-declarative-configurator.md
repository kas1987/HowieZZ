# PDR-011: Declarative Configurator — Build-a-ZELEX from Catalog Data

**Branch:** claude/zelex-config-ui-builder-rso32
**Date:** 2026-06-06
**Status:** Proposed (PDR + schema + worked examples; no live UI yet)

---

## Decision

**Build the ZELEX configurator as a *declarative* tool: a UI generated from a data
spec rather than hand-coded, where a buyer's selections form a JSON "build
document" that resolves — through declared rules — to a catalogued body
architecture, a SKU, a measurement signature, a Body Family, and a price.**

The configurator must not let buyers invent arbitrary bodies. ZELEX's entire
positioning is *documented measurement* — every body is a measured architecture,
not a slider toy. So the body axes (line / height / cup) are **selectors that
resolve to an existing `body_code`**, which then locks in the spec-card
signature and family. Heads, faces, tone, and components compose on top to form a
SKU. This keeps the catalog as the single source of truth and makes the tool
honest about what is real (catalogued) versus bespoke (an inquiry, not a
checkout).

This package proves the model is sound before any UI is built:

- `db/configurator_schema.json` — the declarative spec the UI is generated from.
- `db/configurator_examples.json` — three strong-data bodies reverse-engineered
  into build documents, with truthful resolved values.
- This PDR — the method, the data grounding, and the rules.

---

## 1. Why declarative, and what "declarative" means here

A hand-coded configurator hard-codes its options in markup and logic: a
`<select>` of heights, an `if` per family, a price table in JavaScript. Every
new body, tone, or head means editing code. That is exactly the wrong shape for
a catalog that regenerates from a build pipeline (see README "build pipeline").

A **declarative** configurator inverts this. A single spec file declares, per
axis: its control (slider / select / swatch / toggle), its type, where its
options come from, its provenance, and how it affects price. A generic renderer
walks that spec and produces the UI; a generic resolver walks the same spec's
`derivations` to compute outputs. Adding a body or a tone is a **data** change in
`db/`, not a code change — identical in spirit to how `build_characters.py`
regenerates the site from JSON.

This is the "json-dev / like-kind tools" the request asks for: the spec is JSON
Schema-shaped, a build document validates against
`configurator_schema.json#/build_document_schema`, and the same tooling that
validates catalog JSON validates a build.

### Three principles

1. **Catalog is truth.** Options enumerate from `db/`; large sets (163 heads) are
   *referenced by source*, never copied inline. The catalog can't drift from the
   configurator because they read the same files.
2. **Inputs vs. derived.** A build document stores only buyer choices. Family,
   WHR/BWR, signature, SKU, and price are recomputed every time — never trusted
   from input. This is why the build schema lists only inputs and the resolved
   values live in a separate `resolved` block.
3. **Honest provenance.** Every axis carries a `provenance` tag —
   `catalog` / `spec-card` / `derived` / `proposed`. `proposed` axes (standing
   feet, articulated fingers) are real ZELEX options *not yet structured in
   `db/`*; they're surfaced so the team decides to backfill the data before the
   axis goes live, instead of shipping a picker backed by nothing.

---

## 2. The reverse-engineering method

The request: "take a few bodies that we know have strong data and reverse engineer
how to build that with a json-dev." Here is the method applied, then generalized.

**Step 1 — pick strong-data bodies.** Of 21 bodies in
`db/body_measurements.json`, ~15 carry a full spec card (16–17 measured fields).
Three were chosen to span the axis space:

| Body | Line | Family | Why |
|---|---|---|---|
| `ZG170C` | I-Series | The Muse (exact) | 17 fields, 59 live variants — richest head/face/tone coverage |
| `ZK168B` | K-Series | The Muse (near) | Sits on a family boundary — exercises the classifier's fallback |
| `ZX172E` | SLE 3.0 | The Icon (exact) | SLE-only axes: TPE material + skeleton version + version/tone SKU suffix |

**Step 2 — decompose each into axes.** A catalogued product
(`KE03_1+ZK168B-1`, `ZXE215_1+ZX172E-Tan-Sle3.0`) is just a SKU string. Reading
it against the naming grammar (`HEAD + FACE(MJ) + BODY + TONE/VERSION`) and the
spec card yields the axis values: line, height, cup, material, head_code,
face_variant, skin_tone, skeleton_version.

**Step 3 — declare the derivations that rebuild the SKU.** The reverse of
decomposition is `resolve_body_code` + `resolve_sku` + `classify_family` +
`resolve_price`. If those rules, fed the decomposed axes, reproduce the original
SKU, family, and price, the model round-trips. They do — see
`configurator_examples.json` (every `resolved` block is transcribed from `db/`,
not recomputed by hand).

**Step 4 — generalize.** The same four selectors + grammar describe any
catalogued body, so the spec covers the catalog without per-body code.

---

## 3. The axis model (grounded in real option domains)

Every enum below was extracted from `db/`, not chosen by taste:

| Group | Axis | Control | Source / real domain |
|---|---|---|---|
| Body | line | select | 4 live series + 2 dev (`catalog.json`) |
| Body | height_cm | slider | 153–175 full bodies; <120 excluded as torso |
| Body | cup | select | A,B,C,D,E,F,G,J,K (`catalog.json`) |
| Body | material | radio | Silicone / TPE (from product titles) |
| Body | skeleton_version | select | SLE 2.0 / 3.0 — SLE line only (SKU suffix) |
| Body | body_code / signature / family | **derived** | resolved + spec-card + classified |
| Head | head_code | gallery | 163 distinct heads, referenced not inlined |
| Head | face_variant | radio | Standard / Movable Jaw (~50 MJ variants) |
| Components | skin_tone | swatch | Fair / Tan / White (Tan 228, Fair 72, White 23 SKUs) |
| Components | breast_type | radio | Standard / Gel-Implant (15 implant SKUs) |
| Components | standing_feet, fingers | toggle | **proposed** — not yet in `db/` |

**Body axes are filters, not free composition.** `resolve_body_code` maps
`line + height + cup → body_code` and *requires* a hit in
`body_measurements.json`. A miss (e.g. K-Series 175 K-cup → `ZK175K`) is not an
error to swallow — it raises the `bespoke_combination` warning and routes to the
notify-me / inquiry path (the PDR-003 pattern), not to a fake "add to cart."

---

## 4. Derivations (the reversible core)

Four declared rules, all in `configurator_schema.json#/derivations`:

- **`resolve_body_code`** — `code_prefix(line) + height_cm + cup`, must exist in
  `db/body_measurements.json`. `K-Series + 168 + B → ZK168B`.
- **`classify_family`** — `WHR = waist/hip`, `BWR = upper_bust/waist`; pick the
  family whose ranges contain the point (`body_profiles.json#/families`); on no
  containment, nearest-center with `near`/`loose` confidence
  (`family_taxonomy.json`). **Prefer the stored classification** over a live
  re-derive — see ZK168B below.
- **`resolve_sku`** — rebuilds the SKU string from head + face + body + tone +
  version, matched against `live_variants.json`.
- **`resolve_price`** — catalogued SKU price always wins; otherwise estimate
  `base_by_line × material_factor × (1 + family_premium)` and flag
  `estimated:true`. Premiums mirror `body_profiles.json` (Muse +25%, Icon +30%,
  Siren +35%, …).

### The boundary case worth calling out (ZK168B)

ZK168B has WHR 0.649 and BWR 1.238. WHR 0.649 falls *below* the Muse floor
(0.65) and *inside* the Icon band (0.60–0.65) — but BWR 1.238 is below both
families' bands. No family contains the point on both axes, so nearest-center
wins → **The Muse (near)**. A naive live re-derive could just as easily snap it
to Icon on the WHR axis alone. This is precisely why `classify_family` and
`resolve_price` **prefer the precomputed `body_profiles` value** and only
recompute for genuinely bespoke combinations. The stored taxonomy is the
adjudicated answer; the live formula is the fallback.

---

## 5. What the worked examples prove

`db/configurator_examples.json` carries three round-trips plus a bespoke case:

1. **ZG170C** — `I-Series + 170 + C / Silicone / GE52_2 / Tan` →
   `GE52_2+ZG170C-Tan` @ `$3599` (catalogued). Flipping `face_variant → Movable
   Jaw` resolves a different head+face SKU (`GE02_1_2(GE46MJ)+ZG170C-Tan`),
   proving the face axis is real.
2. **ZK168B** — `K-Series + 168 + B / KE03_1 / Fair` → `KE03_1+ZK168B-1` @
   `$3869.10`; carries the `near`-confidence classifier note above.
3. **ZX172E** — `SLE 3.0 + 172 + E / TPE / SLE 3.0 / ZXE215_1 / Tan` →
   `ZXE215_1+ZX172E-Tan-Sle3.0` @ `$2000`. The SLE-2.0 skeleton alternate
   resolves a *different, cheaper* SKU (`$1600`) — proving `skeleton_version` is
   a price axis, not cosmetic.
4. **Bespoke** — `K-Series + 175 + K` resolves `body_code:null`, raises
   `bespoke_combination`, and routes to inquiry. The model fails *honestly*.

Every `resolved` number is transcribed from `db/` (verified against
`body_measurements.json`, `body_profiles.json`, and `live_variants.json`), so the
spec demonstrably round-trips real catalogued bodies.

---

## 6. Validation rules

Declared in `configurator_schema.json#/validation` so the renderer enforces them
without bespoke code:

| Rule | Severity | Trigger |
|---|---|---|
| `bespoke_combination` | warn | line+height+cup has no catalogued body_code |
| `mj_unsupported` | error | Movable Jaw chosen for a head with no MJ face |
| `skeleton_scope` | error | skeleton_version set on a non-SLE line |
| `torso_excluded` | error | height_cm < 120 |
| `dev_line` | warn | The Classic / The Sculpt (route to notify-me) |

---

## 7. Scope of this package vs. the next step

**In this package (proposed, no UI):**
the spec, the worked examples, this PDR. It proves the declarative model
round-trips real bodies and is buildable from existing `db/` files alone.

**Deliberately not in this package:**

- A live `configurator.html` page. The natural next PDR: a generic renderer that
  walks `groups[].axes[]` to emit the kit's controls (per the
  `site-kit-contract.md`), and a resolver that runs `derivations` and renders the
  resulting body + family card via the existing `ZX.bodyCard`. No new design
  system — it reuses `assets/site.css` tokens and `ZX` helpers.
- Backfilling the `proposed` component axes (standing feet, articulated fingers)
  with per-body capability flags in `db/`.
- A `build_configurator.py` pipeline step that pre-resolves every catalogued
  combination into a lookup table (so the runtime resolver is a map, not a
  search).

---

## 8. Strategic conclusion

1. Declarative beats hand-coded for a catalog that already regenerates from JSON:
   new bodies/tones/heads become **data** changes, not code changes.
2. Body axes resolve to catalogued architectures — the configurator can't
   manufacture a body that doesn't exist, which protects the
   measurement-documented positioning.
3. Inputs and derived values are strictly separated; the catalog stays the single
   source of truth; provenance tags keep the tool honest about real vs. proposed
   options.
4. The reverse-engineering round-trips three strong-data bodies (and fails
   honestly on a bespoke fourth), so the model is proven before a line of UI is
   written.

**Positioning headline:** *"Configure from the catalog, not from imagination —
every build is a measured architecture or an honest inquiry."*

---

## 9. Acceptance Review

| Criterion | Status |
|---|---|
| Declarative spec exists and is valid JSON | ✓ `db/configurator_schema.json` (draft-07 shaped) |
| Spec is generated from / references real `db/` sources, not inlined guesses | ✓ `data_sources` + `enum_source` references; large sets referenced |
| Body / head / component axes all modeled | ✓ three `groups` with grounded enums |
| Inputs vs. derived separated | ✓ `build_document_schema` = inputs only; `derivations` produce `resolved` |
| Provenance honest (real vs. proposed) | ✓ `provenance` tag per axis; standing-feet/fingers flagged `proposed` |
| ≥2 strong-data bodies reverse-engineered with truthful resolved values | ✓ ZG170C, ZK168B, ZX172E in `configurator_examples.json`, transcribed from `db/` |
| Round-trip reproduces real SKU + price + family | ✓ each example's `resolved` matches `live_variants.json` / `body_profiles.json` |
| Bespoke / failure path defined | ✓ `bespoke_combination` rule + worked bespoke example |
| Reuses existing patterns (no new design system, notify-me reuse) | ✓ next-step renderer reuses `site-kit-contract`; dev lines reuse PDR-003 notify-me |
| Both JSON artifacts parse | ✓ verified with `json.load` |
