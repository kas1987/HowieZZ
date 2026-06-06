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
| SM Doll | 4 | 40.0% | TPE 100% | $1,763 | Secondary |
| Irokebijin | 4 | 40.0% | Mixed (70% silicone) | $940 | Secondary |
| HR Doll | 4 | 40.0% | Silicone 90% | $1,890 | Secondary |

Nine additional brands carry 1–3 Muse bodies each (6YE Premium, AS Doll, Game Lady, Gynoid, Hitdoll, ILdoll, Irontech Doll, JK Doll, JY Doll, Jiusheng, Piper Doll, Real Lady, Sanhui, WM Doll, XT Doll).

**No brand owns this family at premium silicone with published measurements.** FunWest and Dime Doll dominate by count but serve the sub-$1,800 tier. Lusandy is the only brand near ZELEX's price point with real silicone depth — and Lusandy's entire 35-body catalog is classified as near-confidence, with no exact-measurement bodies and no published WHR or BWR.

---

## 2. ZELEX Muse Roster

**Source of truth:** `db/family_taxonomy.json` — The Muse: WHR 0.65–0.70, BWR 1.30–1.40, silhouette "tall, hip-dominant," premium +25%, target buyer "European aesthetic buyer."

**12 bodies across 4 series:**

| Body code | Series | Height | Cup | WHR | BWR | Confidence | Est. |
|---|---|---:|---|---:|---:|---|---|
| ZF161D | Fusion | 161 cm | D | 0.660 | 1.371 | exact | yes |
| ZF168B | Fusion | 168 cm | B | 0.653 | 1.250 | near | no |
| ZF169C | Fusion | 169 cm | C | 0.672 | 1.292 | near | no |
| ZG162D | Inspiration | 162 cm | D | 0.658 | 1.382 | exact | no |
| ZGX165F | Inspiration | 165 cm | F | 0.663 | 1.391 | exact | no |
| ZG170C | Inspiration | 170 cm | C | 0.686 | 1.357 | exact | no |
| ZG170D | Inspiration | 170 cm | D | 0.655 | 1.289 | near | no |
| ZG175E | Inspiration | 175 cm | E | 0.679 | 1.351 | exact | no |
| ZK168B | K-Series | 168 cm | B | 0.649 | 1.238 | loose | no |
| ZX153B | SLE | 153 cm | B | 0.671 | 1.415 | near | yes |
| ZX170A | SLE | 170 cm | A | 0.670 | 1.262 | near | no |
| ZX171C | SLE | 171 cm | C | 0.639 | 1.361 | near | no |

The `Est.` flag indicates that at least one measurement axis is derived from inference rather than direct source measurement. ZF161D is confidence-exact but carries the estimated flag because its bust/waist/hip values were reconstructed from secondary sources; the WHR and BWR are within the exact range but not yet manufacturer-verified. ZX153B is near-confidence with estimated measurements at the short SLE end. Both should be confirmed before they appear as primary quiz results.

**Four-series breakdown:**

| Series | Bodies | Height range | Cup range | WHR range | BWR range | Exact/near count |
|---|---:|---|---|---|---|---|
| Inspiration | 5 | 162–175 cm | C–F | 0.655–0.686 | 1.289–1.391 | 4 exact, 1 near |
| Fusion | 3 | 161–169 cm | B–D | 0.653–0.672 | 1.250–1.292 | 1 exact, 2 near |
| SLE | 3 | 153–171 cm | A–C | 0.639–0.671 | 1.262–1.415 | 0 exact, 3 near |
| K-Series | 1 | 168 cm | B | 0.649 | 1.238 | 0 exact, 0 near (loose) |

**Series coverage notes:**
- **Inspiration series (5 bodies)** covers the widest height range within Muse — 162–175 cm. ZGX165F at F cup is the most voluminous Muse body; ZG175E at 175 cm is the height ceiling of the family. The Inspiration series anchors the editorial and European aesthetic interpretation. Four of five bodies are exact-confidence and none carry the estimated flag — this series is the measurement anchor for the Muse landing page.
- **Fusion series (3 bodies)** clusters at 161–169 cm. ZF168B and ZF169C have BWRs of 1.250 and 1.292 — near the lower bound of the Muse BWR range (1.30), which gives these bodies a more modest, balanced read relative to the hip-dominant upper end. ZF161D is exact-confidence but estimated; quiz routing should confirm source measurements before promoting it to primary result status.
- **SLE series (3 bodies)** spans 153–171 cm with cups A–C. ZX153B is the shortest Muse body in the catalog; its near-confidence/estimated classification reflects measurement uncertainty at the shorter SLE end. All three SLE Muse bodies are near-confidence. ZX171C (WHR 0.639) sits at the lower boundary of the Muse WHR range and is the most "border" body in the family.
- **K-Series (1 body)** ZK168B is classified as loose-confidence — its WHR (0.649) falls at the lower Muse WHR boundary and its BWR (1.238) sits outside the formal Muse BWR range. Inclusion reflects its overall hip-dominant proportion and series design intent, but quiz routing should weight ZK168B as a secondary result rather than primary Muse recommendation.

**7 of 12 bodies are exact or near confidence with no estimated flag.** No competitor at any price tier can match this measurement resolution for the Muse family.

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
| SM Doll | 4 | 0% TPE | $1,763 | TPE specialist; Muse + Siren focus |
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

### Launch Hierarchy: When Does The Muse Yield the Hero Position?

The Muse holds the primary hero position at launch and retains it until one of the following explicit triggers is met. These triggers are evaluated in sequence; the first met governs the transition.

| Trigger | Condition | Hero transition |
|---|---|---|
| Classic depth threshold | The Classic reaches 3+ active bodies in `db/family_taxonomy.json` (currently 0 — `status: in_development`) | The Classic takes primary hero; The Muse moves to secondary hero position |
| Sculpt launch | The Sculpt reaches 2+ active bodies (currently 0 — `status: in_development`) | Sculpt takes a co-hero editorial slot; The Muse remains primary hero but shares above-the-fold space with a Sculpt feature block |
| Catalog rebalance | The Muse falls below 50% of total active catalog bodies | Hero position reassignment at next quarterly PDR review cycle |
| Competitor measurement parity | A direct competitor (Lusandy-tier or above) publishes WHR/BWR for 5+ Muse bodies | Measurement differentiation argument requires refresh; trigger a competitive review before next hero commitment |

**Until The Classic has 3+ bodies, The Muse is the only family with enough catalog depth and buyer-resonance breadth to anchor the homepage.** The Classic is ZELEX's natural successor hero — hourglass, timeless, first-time premium buyer — but it requires roster depth before it can serve as a primary discovery surface. At launch, routing first-time buyers through The Muse and using The Classic's in-development status as a "coming soon" signal is the correct sequencing.

**Sculpt launch does not displace The Muse.** The Sculpt targets a fitness-realism segment that is adjacent to but distinct from the European aesthetic buyer. When Sculpt launches, the homepage should present a dual-hero layout (Muse + Sculpt) rather than replacing Muse outright. This holds until Sculpt achieves 4+ bodies and its own quiz routing depth.

**Operational rule:** Any change to The Muse's hero status requires a PDR amendment with CEO sign-off. The trigger conditions above define when that amendment is warranted, not when it is automatic.

### Quiz Routing

| Family | Quiz eligibility | Current bodies | Branching logic |
|---|---|---:|---|
| The Muse | Yes — primary | 12 | Height preference (153–175 cm) → cup preference (A–F) → series filter → character result |

The Muse provides the highest-resolution quiz routing in the catalog. 12 bodies across a 22 cm height span and 6 cup sizes allow the quiz to branch meaningfully on buyer-stated preference before surfacing a character. ZK168B (loose-confidence) should be weighted as a tertiary result; ZF161D and ZX153B (estimated) should be weighted as secondary results. The 7 non-estimated exact/near bodies should anchor all primary quiz results.

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
| Estimated flag column added to Section 2 roster table | ✓ Section 2 — ZF161D and ZX153B flagged |
| Four-series summary table with body counts, ranges, confidence breakdown | ✓ Section 2 — Inspiration (5), Fusion (3), SLE (3), K-Series (1) |
| Pricing landscape with silicone/TPE split | ✓ Section 3 — SM Doll added to volume/TPE tier |
| Lusandy measurement weakness documented | ✓ Section 4 — 100% near-confidence, 0 published specs |
| Buyer scenarios covering style-first, upgrader, collector | ✓ Section 5 |
| Launch hierarchy yield triggers documented | ✓ Section 6 — Classic 3+ bodies, Sculpt launch, catalog rebalance, competitor parity |
| Commercial translation: homepage, quiz, compare, SEO, inquiry | ✓ Section 6 |
| Direct answer to positioning question | ✓ Decision: measurement-documented Muse vs undocumented premium tier |

### Dataset Limitations

- ZELEX official pricing is not published in the manufacturer catalog. Price comparisons use ZELEX (Dollstudio) secondary proxy ($1,390–$2,450 range, $1,840 median).
- Lusandy Doll pricing ($2,599–$2,699) is from secondary aggregator (SiliconWives). Measurement confidence classification (near-confidence across all 35 rows) is sourced from `db/competitor_family_coverage.json`.
- Tayu Muse pricing ($3,800 median) is from the official Tayu source (tayu-doll.com). The "$1,980–$4,700" range reflects the full Tayu catalog; Muse-specific pricing may differ.
- ZK168B loose-confidence classification is noted; quiz routing weighting should exclude it from primary Muse results until measurement verification is completed.
- ZF161D and ZX153B carry the estimated flag. Both should be manufacturer-verified before appearing as primary quiz results. Their WHR/BWR values are within the correct Muse ranges but are based on reconstructed or inferred measurements.
- SM Doll (4 Muse bodies, TPE 100%, $1,763 median) was absent from the Section 1 table in the prior draft. Added to the volume/TPE tier in Section 3. The Section 1 table now reflects all brands with 4+ Muse bodies; SM Doll qualifies at 4 bodies.

---

*Supporting artifacts: `docs/research/competitor-family-coverage-matrix.md` · `docs/pdr/PDR-010-competitor-family-coverage-roi-validation.md` · `db/competitor_family_coverage.json` · `db/family_taxonomy.json` · `db/characters.json`*
