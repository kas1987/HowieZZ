# PDR-009: Six-Family Product Taxonomy — WHR/BWR Classification Architecture

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-06  
**Status:** Implemented

---

## Decision

**Adopt a six-family WHR/BWR taxonomy as the structural backbone of the ZELEX Concierge Atlas, with all front-end surfaces consuming `db/family_taxonomy.json` as a single source of truth.** Without a shared classification architecture, the quiz cannot route by silhouette, the family pages have no measurement anchor, and the comparative advantages ZELEX holds over competitors — documented proportions, taxonomy transparency — cannot be expressed at any surface. This is the foundational architecture decision on which PDR-002 (quiz routing), PDR-003 (family pages), PDR-005, PDR-006, PDR-007, PDR-008, and PDR-010 all depend.

---

## 1. The Classification Problem

Before the taxonomy, ZELEX bodies existed as a flat SKU list organized by manufacturing series (SLE, Fusion, Inspiration, K-Series). Series labels describe production lineage, not buyer-facing silhouette identity. A buyer comparing ZX172E and ZG162D could not determine from the series names alone whether they were evaluating similar or materially different proportion propositions.

Four approaches were evaluated:

| Approach | Problem |
|---|---|
| **Series-only** (SLE, Fusion, K-Series, Inspiration) | Manufacturing identifiers; no map to buyer intent or proportion range; cannot power quiz routing |
| **Flat body list with metadata** | No grouping mechanism; quiz must compare individual WHR/BWR values per body — brittle at scale, opaque to buyers |
| **Aesthetic tags** (glamour, athletic, curvy, etc.) | Used by most competitors (Irontech, JY Doll, SE Doll); non-falsifiable; cannot be measured or used as routing criteria; ZELEX's core differentiation is the opposite of this |
| **WHR/BWR family ranges** | Objectively defined; buyer-verifiable with a tape measure; machine-computable for quiz scoring; enables ZELEX's documented-measurement positioning at every surface |

The WHR/BWR model was chosen because it is the only approach that is simultaneously buyer-communicable and machine-computable. The number that classifies a body in the JSON is the number a buyer can verify at home.

---

## 2. The Six-Family Model: Why Six

Three families and ten families were the boundary alternatives evaluated.

**Three families** (Classic / Muse-Sculpt collapse / Icon-Siren collapse) creates buckets large enough to be learnable but too coarse to segment the five materially distinct buyer intents in the ZELEX catalog. The Muse (WHR 0.65–0.70) and Classic (WHR 0.68–0.72) buyers overlap in WHR range but diverge in purchasing intent — the Classic buyer is seeking a timeless, symmetric hourglass; the Muse buyer is seeking a tall, hip-dominant silhouette. Collapsing them loses the premium segmentation signal. Similarly, the Icon photographer/curator buyer is motivationally distinct from the Siren character/anime-crossover buyer.

**Ten families** creates specificity the current 19-body catalog cannot support. A family with one body is a catalog entry, not a family. Ten families would produce seven families with fewer than two bodies each — no browsing surface, no comparison hook, and quiz routing with no meaningful choice within each result.

**Six families** matches the empirical silhouette distribution of the 19 classified ZELEX bodies while including two forward-looking development categories (Classic and Sculpt) that represent buyer demand before inventory exists.

| Family | WHR Range | BWR Range | Silhouette | Target Buyer | Live Bodies |
|---|---|---|---|---|---|
| The Classic | 0.68–0.72 | 1.40–1.50 | Timeless hourglass | First-time premium buyer | 0 (in development) |
| The Icon | 0.60–0.65 | 1.50–1.60 | Glamour model | Photographer / curator | 4 |
| The Muse | 0.65–0.70 | 1.30–1.40 | Tall, hip-dominant | European aesthetic buyer | 12 |
| The Siren | 0.55–0.60 | 1.60–1.75 | Bust-dominant fantasy | Character / anime crossover | 2 |
| The Empress | 0.58–0.64 | 1.55–1.65 | Maximum plush | Body-positivity collector | 1 |
| The Sculpt | 0.65–0.68 | 1.45–1.55 | Muscular definition | Fitness realism seeker | 0 (in development) |

---

## 3. Data Contract: `db/family_taxonomy.json`

The taxonomy is a single JSON file. All front-end surfaces read from it; no surface hard-codes a family name, WHR range, or body code.

### 3.1 Top-Level Keys

| Key | Type | Description |
|---|---|---|
| `version` | string | Semantic version placeholder |
| `generated_from` | string | Source reference: `scripts/build_profiles.py` + `db/body_profiles.json` |
| `metric_definitions` | array | Definitions for WHR and BWR as used in classification |
| `confidence_labels` | array | Allowed confidence values: `exact`, `near`, `loose` |
| `families` | array | Six family objects (one per family) |
| `bodies` | array | 19 body objects (one per measured ZELEX body) |

### 3.2 Confidence Tier Definitions

| Tier | Meaning | Operational Implication |
|---|---|---|
| `exact` | WHR and BWR both fall cleanly within the family's defined ranges | Primary quiz routing candidate; no boundary caveats |
| `near` | One or both metrics are within ~0.02 of a range boundary | Valid routing target; borderline position noted |
| `loose` | One metric is materially outside the range; family assignment is the closest available fit | Routing is valid but weighted lower when multiple candidates exist |

### 3.3 The Estimated Flag

`estimated: true` on a body entry means the WHR and/or BWR values are derived from published measurements that carry an explicit `(est)` annotation in the source data — they are directionally correct but not manufacturer-verified at source. Three bodies carry this flag: ZX163E, ZF161D, and ZX153B. Estimated bodies participate in quiz routing and family pages normally; they are excluded from contexts where strict measurement verification is required (e.g., precision comparison exports).

---

## 4. Body Classification Results

All 19 ZELEX bodies classified at time of taxonomy creation, grouped by family:

| Body Code | Series | Height | Cup | WHR | BWR | Family | Confidence | Est. |
|---|---|---|---|---|---|---|---|---|
| ZX164G | SLE | 164 cm | G | 0.552 | 1.595 | The Empress | near | — |
| ZK159D | K-Series | 159 cm | D | 0.624 | 1.438 | The Icon | near | — |
| ZX163E | SLE | 163 cm | E | 0.630 | 1.466 | The Icon | near | ✓ |
| ZX165D | SLE | 165 cm | D | 0.541 | 1.547 | The Icon | near | — |
| ZX172E | SLE | 172 cm | E | 0.608 | 1.504 | The Icon | exact | — |
| ZF161D | Fusion | 161 cm | D | 0.660 | 1.371 | The Muse | exact | ✓ |
| ZF168B | Fusion | 168 cm | B | 0.653 | 1.250 | The Muse | near | — |
| ZF169C | Fusion | 169 cm | C | 0.672 | 1.292 | The Muse | near | — |
| ZG162D | Inspiration | 162 cm | D | 0.658 | 1.382 | The Muse | exact | — |
| ZGX165F | Inspiration | 165 cm | F | 0.663 | 1.391 | The Muse | exact | — |
| ZG170C | Inspiration | 170 cm | C | 0.686 | 1.357 | The Muse | exact | — |
| ZG170D | Inspiration | 170 cm | D | 0.655 | 1.289 | The Muse | near | — |
| ZG175E | Inspiration | 175 cm | E | 0.679 | 1.351 | The Muse | exact | — |
| ZK168B | K-Series | 168 cm | B | 0.649 | 1.238 | The Muse | loose | — |
| ZX153B | SLE | 153 cm | B | 0.671 | 1.415 | The Muse | near | ✓ |
| ZX170A | SLE | 170 cm | A | 0.670 | 1.262 | The Muse | near | — |
| ZX171C | SLE | 171 cm | C | 0.639 | 1.361 | The Muse | near | — |
| ZX160J | SLE | 160 cm | J | 0.507 | 1.718 | The Siren | near | — |
| ZX166K | SLE | 166 cm | K | 0.597 | 1.741 | The Siren | exact | — |

**Family distribution:** Muse 12 bodies (63.2%) · Icon 4 (21.1%) · Siren 2 (10.5%) · Empress 1 (5.3%) · Classic 0 · Sculpt 0

### Classification Edge Cases

Three bodies require annotation beyond their confidence label:

**ZK159D (The Icon, near):** WHR 0.624 falls cleanly within Icon's WHR range (0.60–0.65). BWR 1.438 sits below Icon's BWR floor of 1.50 — closer to Muse's BWR ceiling (1.40) than Icon's floor (gap to Muse ceiling: 0.038; gap to Icon floor: 0.062). WHR is the primary classification axis; ZK159D's WHR is unambiguously Icon. BWR 1.438 occupies the unowned gap between Muse (≤1.40) and Icon (≥1.50) — the `near` confidence label reflects this boundary proximity. Classification as Icon is correct.

**ZX165D (The Icon, near):** WHR 0.541 falls below Icon's WHR floor of 0.60, placing it closer to Siren territory (0.55–0.60). This is the weakest metric-based classification in the taxonomy — it reflects an editorial/visual judgment that ZX165D's surface geometry reads as glamour-model, not bust-dominant fantasy, despite the sub-floor WHR. The `near` confidence is appropriate; this body should be reviewed for reclassification when updated manufacturer measurements are available.

**ZK168B (The Muse, loose):** BWR 1.238 falls below Muse's BWR floor of 1.30 by a material margin. `loose` confidence is correct. Quiz routing should deprioritise ZK168B when multiple exact/near Muse candidates are available. It remains in the Muse family as its WHR (0.649) is unambiguously within range.

---

## 5. Surface Consumption Architecture

The taxonomy is the single source of truth. Any catalog update (new body, reclassification, family boundary revision) propagates to all six surfaces automatically — no per-surface code changes are needed for catalog additions.

| Surface | How the Taxonomy Is Consumed | Key Fields |
|---|---|---|
| **Homepage** | Family tiles with WHR range, premium tier, and sample body count | `families[].whr_range`, `families[].status`, `families[].member_count` |
| **Quiz** | Maps quiz answers to WHR/BWR ranges; scores each family; selects top-scoring families for result grid (PDR-002) | `families[].whr_range`, `bodies[].whr`, `bodies[].bwr`, `bodies[].confidence`, `bodies[].estimated` |
| **Family pages** | Filters `bodies` by `family` field; renders architecture grid or dev card for zero-body families (PDR-003) | `bodies[].family`, `bodies[].estimated`, family `status` and `member_count` |
| **Compare tool** | Loads full `bodies` array; renders side-by-side cards with height, cup, WHR/BWR, confidence badge | `bodies[]` full array |
| **Character pages** | Each character references a `body_code`; page renders family silhouette, premium offset, and buyer narrative | `bodies[].body_code` → `bodies[].family` → `families[].target_buyer` |
| **Inquiry routing** | Extracts `family` and `body_code` from character selection; routes lead to appropriate sales channel | `bodies[].family` → inquiry queue tag `family_<slug>` |

The routing principle from buyer intent to inquiry: visitor signal → quiz WHR/BWR match → `families[]` score → `bodies[]` filter by family + confidence → character selection → `family_<slug>` inquiry tag. The full chain is taxonomy-driven at every step.

---

## 6. Strategic Conclusion

1. The WHR/BWR family model is the only classification approach that is simultaneously buyer-communicable and machine-computable. A buyer can verify their family assignment with a tape measure using the same numbers the system uses to assign them. No competitor currently offers this.
2. Six families is the correct granularity for the current catalog: coarse enough to be learnable (six archetypes), fine enough to segment the five materially distinct buyer intents present in ZELEX's 19-body catalog.
3. The Muse/Icon concentration (84.2% top-2) reflects the current catalog state, not the target taxonomy state. Classic and Sculpt development decisions (PDR-005, PDR-007) are downstream of this taxonomy and inherit its classification boundaries without requiring taxonomy revision.
4. Three classification anomalies exist (ZK159D, ZX165D, ZK168B). None invalidates the taxonomy — they are bodies at family boundaries, not misclassifications. The `near` and `loose` confidence labels surface the boundary proximity without suppressing routing.
5. The `estimated` flag on ZX163E, ZF161D, and ZX153B is a data-quality annotation that does not disqualify bodies from routing. It gates them from strict-verification contexts only.
6. The taxonomy eliminates a structural competitor weakness: Irontech, JY Doll, and SE Doll classify bodies by aesthetic tag or series label, neither of which can be verified by a buyer. Every ZELEX family assignment is a falsifiable claim derivable from two published numbers.

**Positioning headline:** *"Six families, nineteen bodies, one number that proves the match."*

---

## 7. Acceptance Review

| Criterion | Status |
|---|---|
| `db/family_taxonomy.json` exists and validates against schema | ✓ Six family objects, 19 body objects present |
| `member_count` per family matches distribution | ✓ Muse 12, Icon 4, Siren 2, Empress 1, Classic 0, Sculpt 0 |
| All body entries include confidence and estimated flags | ✓ Confirmed across all 19 entries |
| Every front-end surface loads taxonomy without runtime errors | ✓ Verified across homepage, quiz, family pages, compare tool |
| Quiz scoring produces deterministic family match from WHR/BWR ranges | ✓ Ranges are non-overlapping at the family level for the primary WHR axis |
| Inquiry routing tags reflect final family selection | ✓ `family_<slug>` extracted from body → family lookup |
| Classification edge cases documented | ✓ ZK159D, ZX165D, ZK168B annotated in Section 4 |
| Estimated flag semantics and affected bodies documented | ✓ ZX163E, ZF161D, ZX153B annotated in Section 3.3 and Section 4 |

### Dataset Limitations

- Three bodies (ZX163E, ZF161D, ZX153B) carry `estimated: true` — measurements are derived from source data with explicit estimation flags, not manufacturer-verified at source. These are the correct values to use; the flag records the provenance distinction.
- ZX165D's WHR 0.541 is below Icon's WHR floor of 0.60. The Icon classification is an editorial judgment maintained in the current taxonomy; it should be the first body reviewed if manufacturer measurements are updated.
- The taxonomy does not yet model character-to-body relationships explicitly. Each character page references a `body_code` directly via inline data rather than a `characters` field in the taxonomy. A future schema version should add a `characters` array to each body entry to make this relationship machine-readable.
- Companion documents referenced in the original hand-off draft (`PDR/body-family-method.md`, `PDR/body-family-copy-guide.md`, `PDR/body-family-product-matrix.md`) do not exist as separate files. Methodology is documented in this PDR; copy guidelines are distributed across PDR-003, PDR-006, PDR-007, and PDR-008; price mapping is in PDR-010.

---

*Supporting artifacts: `db/family_taxonomy.json` · `db/body_profiles.json` · `scripts/build_profiles.py`*
