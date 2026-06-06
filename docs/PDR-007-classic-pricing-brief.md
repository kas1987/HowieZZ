# PDR-007 — The Classic: Pricing & Entry Brief

**Date:** 2026-06-05
**Status:** Draft — do not publish
**Spec reference:** `db/family_taxonomy.json` · `family.html` FAM_META · `docs/research/competitor-family-coverage-matrix.md`

---

## The Gap

The Classic is the most-wanted body shape in the market — the timeless hourglass, balanced curves, WHR 0.68–0.72, BWR 1.40–1.50 — and it has exactly one credible silicone incumbent at premium price: Gynoid Doll, at $4,401–$7,038. Below that level, Classic coverage is thin and predominantly TPE.

The $2,000–$3,000 silicone window is structurally empty. Of the 30 brands tracked across 495 classified body rows, 17 brands carry at least one Classic body in their catalogues. Of those 17, only a handful offer silicone at all, and none price a silicone Classic body in the $2,000–$3,000 band with real catalogue depth. The coverage matrix makes this concrete: across all 30 brands, Gynoid is the only pure-silicone operator with Classic as its primary family (5 of 10 bodies, 50% concentration) — and Gynoid's floor is $4,401.

ZELEX today has zero Classic bodies (confirmed: `db/family_taxonomy.json` `member_count: 0`; `db/characters.json` yields 0 characters with `body.family = "The Classic"`). The family is marked `"status": "in_development"` in both the taxonomy and the `family.html` dev-card. The site copy is written and ready: *"The timeless hourglass — balanced curves, centred mass, a body that reads as effortlessly complete."* The product does not yet exist to put behind it.

Entering at ~$2,299 would be a market first: the only silicone Classic body priced accessibly to the first-time premium buyer.

---

## Competitor Pricing Landscape

### Gynoid Doll — the silicone incumbent

Gynoid is the dominant silicone Classic operator in the dataset:

- **Classic bodies:** 5 of 10 classified bodies (50.0% of catalogue), the highest Classic concentration of any brand in the matrix
- **Material:** 100% silicone
- **Price range:** $4,401–$7,038
- **Median price:** $5,391

Gynoid's positioning is ultra-premium artisan. Their Classic bodies compete on hyper-realism and Japanese/European collector demand. They do not compete on accessibility. The $4,401 floor is the lowest a silicone Classic currently enters the market from any brand with meaningful catalogue depth.

### Other silicone brands with Classic presence

Several silicone or mixed-material brands carry isolated Classic bodies, but none with catalogue commitment or pricing that fills the $2–3k window:

| Brand | Classic bodies | Silicone share | Median price (all bodies) | Notes |
|---|---:|---:|---:|---|
| Gynoid | 5 | 100% | $5,391 | Ultra-premium; Classic is primary family |
| Jiusheng | 2 | 100% | $2,290 | 2 Classic bodies in an 8-body catalogue; not Classic-specialist |
| Hitdoll | 1 | 100% | $1,437 | Single Classic body; budget tier |
| ILdoll | 1 | 100% | $1,437 | Single Classic body; budget tier |
| Sanhui | 1 | 100% | $2,599 | 1 Classic in a 7-body silicone catalogue |
| Piper Doll | 2 | 90% | $1,290 | 2 Classic bodies; broad catalogue, budget positioning |
| Tayu | 1 | 85.7% | $3,800 | 1 Classic body; catalogue is Muse/Icon-heavy |

No silicone brand owns the $2,000–$3,000 Classic segment with catalogue depth. The closest is Jiusheng ($2,290 median, 2 Classic bodies) and Sanhui ($2,599 median, 1 Classic body) — neither is Classic-specialist; both are general silicone catalogues where Classic bodies appear by accident of measurement, not strategic intent.

### The TPE tier — what fills the gap today

The majority of Classic coverage in the matrix is TPE-material, priced at $1,400–$1,999:

| Brand | Classic bodies | Silicone share | Median price | Material note |
|---|---:|---:|---:|---|
| Lilydoll | 6 | 0% (unknown) | $1,199 | Largest Classic count after Gynoid; not silicone |
| Jarliet | 2 | 0% TPE | $1,558 | Classic as secondary family |
| Dime Doll | 2 | 0% TPE | $1,699 | Classic as minor family |
| WM Doll | 1 | 0% TPE | $1,694 | Single Classic; volume brand |
| AS Doll | 1 | 0% TPE | $1,993 | Single Classic |

The TPE Classic tier clusters under $2,000. It serves buyers who want the Classic silhouette but cannot or will not pay for silicone. This is a different buyer from ZELEX's target — but it defines the floor expectation: a Classic body "should" be accessible. ZELEX at ~$2,299 in silicone would be ~$300–$500 above the TPE ceiling and $2,100 below Gynoid's silicone floor. That is a defensible positioning band.

---

## ZELEX's Position

**Current state:** 0 Classic bodies. The family is in development. The site has the family descriptor live but routes buyers to a dev-card with no product. Any quiz or discovery flow that routes a buyer to The Classic today hits a dead end.

**Price target:** ZELEX's overall retailer median is approximately $1,999 (ZELEX Dollstudio proxy: median $1,840, range $1,390–$2,450; independent catalogue price_matrix shows 102 ZELEX SKUs in the $1,800–$2,499 band, 40 in $1,200–$1,799, 13 in $2,500–$3,499). A Classic body at the top of ZELEX's natural band — $2,199–$2,499 — is consistent with the +20% premium marker assigned to The Classic in `family_taxonomy.json` applied to a ~$1,999 base.

**Positioning vs Gynoid:** Gynoid owns the ultra-premium Classic at $4,401+. ZELEX at $2,299 is not competing with Gynoid's collector market — it is opening a new tier. The positioning is: *silicone Classic, accessible premium, first-time buyer*. Gynoid is the artisan reference; ZELEX is the entry to the silhouette category in silicone at all.

**Positioning vs TPE:** The TPE Classic floor is $1,199–$1,699. ZELEX at $2,299 commands a ~$600–$1,100 premium over TPE alternatives. The material justification (silicone skin feel, durability, oil-free surface) plus the ZELEX brand architecture (named characters, quiz-matched) supports this spread cleanly. The buyer trading from TPE to silicone in The Classic body shape has no current destination — ZELEX fills it.

**WHR/BWR spec (source of truth: `db/family_taxonomy.json`):**
- WHR range: 0.68–0.72
- BWR range: 1.40–1.50
- Silhouette: "Timeless hourglass"
- Premium marker: +20%
- Target buyer: "First-time premium buyer"

---

## Entry Specification

**Minimum viable Classic body:**

The Classic is the most geometrically "centred" of the six families — the intersection point between the Muse (hip-dominant, lower BWR) and the Icon (waist-suppressed, higher BWR). It demands precision manufacturing: the silhouette reads as complete only when both axes land inside the window simultaneously.

| Axis | Target | Range |
|---|---|---|
| WHR | 0.70 | 0.68–0.72 |
| BWR | 1.45 | 1.40–1.50 |
| Cup | D–E | D minimum for proportional credibility at WHR 0.70 |
| Height | 160–168 cm | Consistent with Classic's "balanced, not dramatic" posture |

**Manufacturing implications:**

- A WHR of 0.70 at a standard waist of 58 cm implies hips of ~83 cm. At BWR 1.45, bust = 58 × 1.45 ≈ 84 cm. These are close-set proportions: bust and hip within ~1 cm of each other. The mould must be sculpted to balance without either dimension reading as dominant — this is harder to execute credibly than either the Siren (bust-dominant, obvious) or the Muse (hip-dominant, obvious).
- Silicone-specific: The Classic's tactile read depends on the breast fill — a D or E cup at this waist-to-hip geometry should feel substantive without overwhelming. Platinum-cure silicone Shore hardness in the 0–10A range (consistent with ZELEX's SLE line) achieves this. TPE cannot replicate the self-supporting feel at this cup size and WHR.
- The family descriptor phrase "effortlessly complete" is the manufacturing brief in two words: no feature should call attention to itself.

**Suggested first SKU:** 165 cm, D cup, WHR 0.70, BWR 1.45 — the geometric centre of the family, the safest first proof-of-concept, and a height that photographs neutrally across all campaign contexts.

---

## Revenue Opportunity

**Caveat:** Figures below are estimated from catalogue data, not from ZELEX transaction data. They are directional, not financial projections.

**Demand signal — catalogue gap:**
Across 30 brands and 495 classified bodies, 17 brands have at least one Classic body. Classic is the second-most-present family in competitor catalogues after Muse. Buyer demand for the Classic silhouette is broad enough that even volume-generic brands (WM, SE, AS, Jarliet) add at least one Classic body to their catalogues. There is a demonstrated pattern: Classic buyers exist in sufficient numbers that competitors add Classic SKUs even when it is not their strategy.

**Quiz dead-end cost (estimated):**
The Classic's WHR/BWR range (0.68–0.72 / 1.40–1.50) sits at the geometric centre of the six-family space — the most common natural body shape in the population. In a quiz routing buyers by proportion preference, The Classic is the most likely modal answer for a first-time buyer describing "realistic, balanced proportions." If 20–35% of quiz completions route to Classic (estimated — no quiz data exists yet), and if 100 buyers per month complete the quiz at launch, that is 20–35 monthly Classic-first buyers with no product to purchase. At a $2,299 target price and an optimistic 10% conversion (standard e-commerce baseline for high-consideration product), the per-month opportunity cost is approximately $460–$805/month — or $5,500–$9,700/year — from a single SKU gap. This is a conservative, illustrative estimate based on general e-commerce benchmarks and proportional geometry logic, not observed ZELEX traffic data.

**Competitive urgency:**
No brand currently owns the $2–3k silicone Classic tier with strategic intent. This window is open today. It will not remain structurally empty indefinitely — any silicone manufacturer with Classic-range measurement profiles already in production can enter this tier with a price and a landing page. ZELEX's advantage is the taxonomy infrastructure (quiz, family architecture, character layer) that a price-cut alone cannot replicate.

---

## Recommended Next Step

**Immediate action:** Prioritize one Classic hero body at WHR 0.70 ± 0.01, BWR 1.45 ± 0.03 for the next production cycle. Target retail price $2,299. Commission 2 character slots against this body on debut (not all 4 — launch lean, add characters after sales validation).

**Sequencing:**
1. Production brief to factory: 165 cm, D cup, WHR 0.70 target — confirm measurement feasibility against existing SLE tooling.
2. Two character profiles written and shot against the hero body before site launch.
3. Family landing page (`/family?f=classic`) exits dev-card status; the quiz routing to Classic resolves to a live product page, not a dead end.
4. Pricing set at $2,299 retail — positioned explicitly as "silicone hourglass, premium accessible" in copy, not competing upward with Gynoid and not discounting into TPE territory.
5. PDR-003 landing copy (if applicable) debuts alongside the Classic family activation.

**Positioning headline (draft):** *"The Classic — the silhouette every buyer recognises, in silicone, under $2,500. The first of its kind."*

This is the positioning ZELEX can own today. No other brand has claimed it.

---

*Sources: `db/family_taxonomy.json` · `db/characters.json` · `db/independent_catalog_groupings.json` · `docs/research/competitor-family-coverage-matrix.md` · `docs/competitor-analysis.md` · `family.html` FAM_META*
