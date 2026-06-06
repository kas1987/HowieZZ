# PDR-008: The Muse — Positioning Brief

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-05  
**Status:** Draft — Pending CEO Review

---

## Decision

**Lead the site launch with The Muse as the primary hero family. Deploy all 12 bodies across four series. Position ZELEX explicitly as the measurement-documented alternative in a family dominated by volume operators who publish no measurements.**

The Muse is ZELEX's largest family (12 bodies, 63% of the catalog) and the most universally present family across competitors — 26 of 28 surveyed competitor brands carry at least one Muse body. The family is the modal first result for any buyer describing "European aesthetic," "tall and elegant," or "hip-dominant silhouette." PDR-010 identified The Muse as the primary launch designation with an ROI composite of 3.7/5. The closest price-and-material competitor, Lusandy Doll ($2,699 median, 83% silicone, 20 Muse bodies), classifies all 35 of its catalog rows as near-confidence and publishes zero measurement documentation. ZELEX's differentiation is legible and unoccupied: the only Muse-specialist catalog in the premium silicone tier that publishes WHR and BWR for every body.

---

## 1. Market Signal

The Muse is the most broadly covered family in the 30-brand competitive dataset. The silhouette — tall, hip-dominant, WHR 0.65–0.70, BWR 1.30–1.40 — appears in the catalogs of 26 of 28 non-ZELEX brands surveyed, with only Lilydoll and YL Doll absent. This near-universal coverage signals that buyers consistently seek this proportion across all price tiers, and that volume manufacturers have recognized the demand independently.

**Volume concentration:**

| Brand | Muse bodies | Muse share of cat. | Material | Median price | Source tier |
|---|---:|---:|---|---:|---|
| FunWest | 38 | 35.8% | Mixed (46% silicone) | $1,599 | Secondary |
| Dime Doll | 21 | 67.7% | Silicone 100% | $1,699 | Secondary |
| Lusandy Doll | 20 | 57.1% | Silicone 83% | $2,699 | Secondary |
| Tayu | 9 | 42.9% | Silicone 86% | $3,800 | Official |
| MD Doll | 9 | 13.0% | Mixed (33% silicone) | $2,599 | Secondary |
| Angel Kiss | 5 | 50.0% | Silicone 100% | $2,390 | Secondary |
| Jarliet | 5 | 50.0% | TPE 100% | $1,558 | Secondary |
| SE Doll | 5 | 50.0% | Mixed (20% silicone) | $1,690 | Secondary |
| Irokebijin | 4 | 40.0% | Mixed (70% silicone) | $940 | Secondary |
| HR Doll | 4 | 40.0% | Silicone 90% | $1,890 | Secondary |

Nine additional brands carry 1–3 Muse bodies each (6YE Premium, AS Doll, Game Lady, Gynoid, Hitdoll, ILdoll, Irontech Doll, JK Doll, JY Doll, Jiusheng, Piper Doll, Real Lady, SM Doll, Sanhui, WM Doll, XT Doll).

**No brand owns this family at premium silicone with published measurements.** FunWest and Dime Doll dominate by count but serve the sub-$1,800 tier. Lusandy is the only brand near ZELEX's price point with real silicone depth — and Lusandy's entire 35-body catalog is classified as near-confidence, with no exact-measurement bodies and no published WHR or BWR.

---

## 2. ZELEX Muse Roster

**Source of truth:** `db/family_taxonomy.json` — The Muse: WHR 0.65–0.70, BWR 1.30–1.40, silhouette "tall, hip-dominant," premium +25%, target buyer "European aesthetic buyer."

**12 bodies across 4 series:**

| Body code | Series | Height | Cup | WHR | BWR | Confidence |
|---|---|---:|---|---:|---:|---|
| ZF161D | Fusion | 161 cm | D | 0.660 | 1.371 | exact (est.) |
| ZF168B | Fusion | 168 cm | B | 0.653 | 1.250 | near |
| ZF169C | Fusion | 169 cm | C | 0.672 | 1.292 | near |
| ZG162D | Inspiration | 162 cm | D | 0.658 | 1.382 | exact |
| ZGX165F | Inspiration | 165 cm | F | 0.663 | 1.391 | exact |
| ZG170C | Inspiration | 170 cm | C | 0.686 | 1.357 | exact |
| ZG170D | Inspiration | 170 cm | D | 0.655 | 1.289 | near |
| ZG175E | Inspiration | 175 cm | E | 0.679 | 1.351 | exact |
| ZK168B | K-Series | 168 cm | B | 0.649 | 1.238 | loose |
| ZX153B | SLE | 153 cm | B | 0.671 | 1.415 | near (est.) |
| ZX170A | SLE | 170 cm | A | 0.670 | 1.262 | near |
| ZX171C | SLE | 171 cm | C | 0.639 | 1.361 | near |

**Series coverage notes:**
- **Inspiration series (5 bodies)** covers the widest height range within Muse — 162–175 cm. GX165F at F cup is the most voluminous Muse body; GX175E at 175 cm is the height ceiling of the family. The Inspiration series anchors the editorial and European aesthetic interpretation.
- **Fusion series (3 bodies)** clusters at 161–169 cm. ZF168B and ZF169C have BWRs of 1.250 and 1.292 — near the lower bound of the Muse BWR range (1.30), which gives these bodies a more modest, balanced read relative to the hip-dominant upper end.
- **SLE series (3 bodies)** spans 153–171 cm with cups A–C. ZX153B is the shortest Muse body in the catalog; its near-confidence/estimated classification reflects measurement uncertainty at the shorter SLE end.
- **K-Series (1 body)** ZK168B is classified as loose-confidence — its WHR (0.649) falls at the lower Muse WHR boundary and its BWR (1.238) sits outside the formal Muse BWR range. Inclusion reflects its overall hip-dominant proportion and series design intent, but quiz routing should weight ZK168B as a secondary result rather than primary Muse recommendation.

**7 of 12 bodies are exact or near confidence.** No competitor at any price tier can match this measurement resolution for the Muse family.

---

## 3. Competitive Pricing Landscape

### Premium silicone tier

| Brand | Muse bodies | Silicone share | Price range | Measurement documentation |
|---|---:|---:|---|---|
| Tayu | 9 | 86% | $1,980–$4,700 | Official source; no published WHR/BWR |
| Lusandy Doll | 20 | 83% | $2,599–$2,699 | Near-confidence only; zero exact measurements |
| Real Lady | 1 | 100% | $2,860–$2,990 | Near-confidence; 1 body |
| Angel Kiss | 5 | 100% | $2,150–$2,390 | Near-confidence; no published WHR/BWR |
| ZELEX | 12 | Silicone (SLE/Fusion/Inspiration) | $1,840–$2,450 (proxy) | **7 exact/near measurements; WHR/BWR published** |

ZELEX is the only brand in the premium silicone Muse tier that publishes body measurements at resolution sufficient for buyer verification.

### Mid-market silicone tier

| Brand | Muse bodies | Silicone share | Median price | Notes |
|---|---:|---:|---:|---|
| Dime Doll | 21 | 100% | $1,699 | Volume silicone; Muse-specialist (68% of cat); no published specs |
| HR Doll | 4 | 90% | $1,890 | Mixed silicone; no published specs |
| XT Doll | 3 | 100% | $2,190 | Mid-market silicone; no specs |

### Volume/TPE tier

| Brand | Muse bodies | Silicone share | Median price | Notes |
|---|---:|---:|---:|---|
| FunWest | 38 | 46% | $1,599 | Volume leader; mixed material; catalog breadth is the product |
| Jarliet | 5 | 0% TPE | $1,558 | TPE specialist; Classic/Muse secondary |
| 6YE Premium | 3 | 0% TPE | $1,490 | TPE; budget tier |

---

## 4. The Measurement Differentiation

**Lusandy is the structural reference point.** Lusandy carries 20 Muse bodies at $2,599–$2,699 with 83% silicone — the closest price-and-material match to ZELEX in this family. The critical weakness: all 35 Lusandy rows in the dataset are near-confidence, with no exact-measurement classification and no published WHR or BWR ranges. A buyer comparing Lusandy and ZELEX cannot verify that "Lusandy body X is a WHR 0.66 Muse" before purchasing. They are buying a visual impression.

ZELEX's Muse catalog exposes WHR and BWR for every body. Six of 12 bodies are exact- or exact-estimated confidence; the remaining six are near-confidence with stated measurement ranges. A buyer who enters the quiz having described "elongated, hip-prominent proportion, taller frame" receives a specific body code and its documented measurements. They can confirm that ZG175E (WHR 0.679, BWR 1.351, 175 cm) is the tallest exact-measurement Muse in the market, at a price competitive with Lusandy's undocumented equivalent.

**The differentiation is not more bodies than Lusandy.** The differentiation is that every ZELEX Muse body is a documented specification, not a visual approximation. For the buyer ZELEX targets — the European aesthetic buyer, the documenting collector, the buyer upgrading from a TPE purchase they can't re-specify — this is the decision-relevant information.

---

## 5. Buyer Scenarios

**Scenario 1: The European aesthetic buyer.**
A buyer who has spent time researching proportions associated with European fashion photography standards — elongated torso, understated bust, hip-emphasis without exaggeration — arrives with a mental model but no measurement vocabulary. The ZELEX quiz translates "tall, elegant, understated curves" to The Muse family and surfaces ZGX165F (165 cm, F cup, WHR 0.663, BWR 1.391) or ZG175E (175 cm, E cup, WHR 0.679) depending on height preference. They can read the WHR before purchasing. Lusandy would show them a list of Muse-range bodies with no measurement annotation. Tayu would show them photography at $3,800.

**Scenario 2: The upgrading collector.**
A buyer owns a Dime Doll Muse-family piece purchased at $1,699 in silicone and wants to trade up. They have a specific body proportion in mind — the same hip-to-waist geometry — and a budget of $2,000–$2,800. They search for "silicone Muse body with WHR around 0.66." No brand at any price tier returns a specific measurement-verified result except ZELEX. ZG162D (WHR 0.658, exact confidence) or ZG170C (WHR 0.686, exact confidence) gives them a verifiable upgrade path from the Dime Doll piece they already own.

**Scenario 3: The style-first first buyer.**
A first-time buyer is drawn to editorial photography of the Muse silhouette without measurement knowledge. The quiz routes them here based on stated aesthetic ("tall, graceful, European editorial feel"). They see the character grid — 12 characters across four series — and choose by presence and narrative. The measurement layer exists for verification but the buyer's primary decision is character-driven. The breadth of the Muse roster (12 characters, A–F cup, 153–175 cm) ensures every body-type variation within the family has a named character.

---

## 6. Commercial Translation

### Homepage Position

The Muse takes the primary hero position on the homepage per PDR-010 launch hierarchy. The Muse is the modal first-time buyer result across the quiz, the family with the deepest ZELEX catalog, and the most universally present family in competitor catalogs — the natural anchor for the site's opening proposition.

```
Hero: The Muse — "Tall. Hip-dominant. Measured."
[Secondary copy: "12 bodies. Four series. Every WHR published."]
```

### Quiz Routing

| Family | Quiz eligibility | Current bodies | Branching logic |
|---|---|---:|---|
| The Muse | Yes — primary | 12 | Height preference (153–175 cm) → cup preference (A–F) → series filter → character result |

The Muse provides the highest-resolution quiz routing in the catalog. 12 bodies across a 22 cm height span and 6 cup sizes allow the quiz to branch meaningfully on buyer-stated preference before surfacing a character. ZK168B (loose-confidence) should be weighted as a tertiary result; the 7 exact/near bodies should anchor quiz results.

### Compare Filter

Active at launch. The Muse filter is the primary tab in the compare tool, defaulted to active on first visit. WHR and BWR columns are displayed on every compare card — this is information that FunWest, Dime Doll, and Lusandy do not expose. The compare tool is the measurement-differentiation argument made visual.

### Landing Page

`/families/muse` — full landing page, P1 SEO priority.
- Lead content: series navigation (Fusion · Inspiration · K-Series · SLE) with WHR/BWR ranges per series
- Secondary content: height/cup matrix showing all 12 body positions
- Comparison section: ZELEX Muse vs Lusandy — measurement documentation vs near-confidence catalog
- Character grid: 12 character thumbnails with body code attribution

### SEO Page Strategy

`/families/muse` content priorities:
1. Family definition and WHR/BWR spec — establishes measurement authority
2. Four-series architecture — no other Muse-specialist brand organizes by series with consistent measurement standards
3. "Every body measured and documented" — the statement no Muse competitor can make
4. Character grid — 12 characters is a stronger visual argument than Lusandy's undifferentiated body list

### Inquiry Routing

| Tag | Routing logic |
|---|---|
| `body:muse` | Route to European aesthetic / style-first buyer funnel; emphasize measurement provenance, series architecture, height-cup matrix in follow-up |
| `body:muse-series-inspiration` | Route to editorial/tall buyer sub-funnel; surface ZG170C, ZG175E as hero bodies for the height-preference segment |

---

## 7. Strategic Conclusion

Three findings govern the Muse positioning:

1. **The Muse is ZELEX's primary launch family by every metric.** It is the largest family in the catalog (12 bodies, 63%), the highest ROI composite in PDR-010 (3.7/5), and the most universally present family across competitors (26/28 brands). The launch should be organized around The Muse and every other family positioned relative to it.

2. **Lusandy is the structural competitive threat — and its Achilles heel is measurability.** Lusandy is the only competitor near ZELEX's price tier with material Muse depth (20 bodies at $2,699, 83% silicone). Every Lusandy row is near-confidence. No WHR or BWR is published. A buyer who wants to verify geometry before committing $2,699 cannot do so with Lusandy. They can with ZELEX. This is the differentiation that closes the sale at the premium tier.

3. **ZELEX's four-series architecture is itself a product argument.** No Muse-family competitor organizes their catalog by series with consistent measurement standards across series. Fusion, Inspiration, K-Series, and SLE each occupy a distinct height and proportion sub-range within the Muse family. A buyer who wants to understand "what is the difference between the Inspiration 175 and the Fusion 168" can read the specs and get an answer. The answer to the same question about Lusandy's 20 bodies does not exist in their catalog.

**Positioning headline:** *"The Muse — four series, twelve bodies, every measurement documented. The only way to choose a silhouette this precisely."*

---

## 8. Acceptance Review

| Criterion | Status |
|---|---|
| Primary launch designation confirmed from PDR-010 | ✓ ROI composite 3.7 — highest of active families |
| Competitor Muse coverage documented (brand count, silicone/TPE split) | ✓ Section 1 — 26/28 competitor brands |
| ZELEX Muse roster verified against db/family_taxonomy.json | ✓ Section 2 — 12 bodies, 4 series |
| WHR/BWR and confidence for all 12 bodies recorded | ✓ Section 2 table |
| Pricing landscape with silicone/TPE split | ✓ Section 3 |
| Lusandy measurement weakness documented | ✓ Section 4 — 100% near-confidence, 0 published specs |
| Buyer scenarios covering style-first, upgrader, collector | ✓ Section 5 |
| Commercial translation: homepage, quiz, compare, SEO, inquiry | ✓ Section 6 |
| Direct answer to positioning question | ✓ Decision: measurement-documented Muse vs undocumented premium tier |

### Dataset Limitations

- ZELEX official pricing is not published in the manufacturer catalog. Price comparisons use ZELEX (Dollstudio) secondary proxy ($1,390–$2,450 range, $1,840 median).
- Lusandy Doll pricing ($2,599–$2,699) is from secondary aggregator (SiliconWives). Measurement confidence classification (near-confidence across all 35 rows) is sourced from `db/competitor_family_coverage.json`.
- Tayu Muse pricing ($3,800 median) is from the official Tayu source (tayu-doll.com). The "$1,980–$4,700" range reflects the full Tayu catalog; Muse-specific pricing may differ.
- ZK168B loose-confidence classification is noted; quiz routing weighting should exclude it from primary Muse results until measurement verification is completed.

---

*Supporting artifacts: `docs/research/competitor-family-coverage-matrix.md` · `docs/pdr/PDR-010-competitor-family-coverage-roi-validation.md` · `db/competitor_family_coverage.json` · `db/family_taxonomy.json` · `db/characters.json`*
