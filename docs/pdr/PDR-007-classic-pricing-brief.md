# PDR-007: The Classic — Pricing and Entry Brief

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-05  
**Status:** Draft — Pending CEO Review

---

## Decision

**Commission one Classic hero body at WHR 0.70 / BWR 1.45, 165 cm, D cup, silicone, priced at $2,299 retail.**

The Classic is the most-wanted body shape in the market — the timeless hourglass, balanced curves, WHR 0.68–0.72, BWR 1.40–1.50 — and ZELEX has zero Classic bodies today. The $2,000–$3,000 silicone window is structurally empty: Gynoid is the only credible silicone incumbent at $4,401+, and the mid-premium silicone band is unoccupied. A single hero body at $2,299, launched with two character skins and a full family landing page, closes the gap that is currently routing first-time premium buyers — ZELEX's declared target segment for The Classic — to competitors or to nothing. This is the highest-priority product addition for Q3 2026.

---

## 1. The Gap

**Current state:** ZELEX has 0 Classic bodies. The family is marked `"status": "in_development"` with `"member_count": 0` in `db/family_taxonomy.json`. The character database (`db/characters.json`) contains zero character slots assigned to The Classic. The family landing page (`/families/classic`) exists as a dev-card with no live product behind it.

**Quiz dead-end.** The Classic's WHR/BWR range (0.68–0.72 / 1.40–1.50) sits at the geometric centre of the six-family space — the most common natural body shape proportion in the population. In a quiz routing buyers by proportion preference, The Classic is the modal first-time buyer result. Every quiz completion that routes to Classic today hits a dead end. The buyer exits. There is no email capture, no comparable alternative, no waitlist — just a dead end.

**Family descriptor is live.** The site already carries: *"The timeless hourglass — balanced curves, centred mass, a body that reads as effortlessly complete."* The product does not yet exist to put behind it. The copy is written; the commission has not been made.

**Coverage context.** 14 of 29 independent competitor brands carry at least one Classic body. Classic is the second most-demanded family (after Muse) by competitor catalogue presence and by estimated first-time buyer intent. ZELEX is absent from this lane entirely while 48% of competitors cover it.

---

## 2. Competitor Pricing Landscape

### Gynoid — the silicone incumbent

Gynoid is the dominant silicone Classic operator in the dataset:

| Metric | Value |
|---|---|
| Classic bodies | 5 of 10 (50.0% of catalogue) |
| Material | 100% silicone |
| Price range | $4,401–$7,038 |
| Median price | $5,391 |
| Positioning | Ultra-premium artisan |

Gynoid does not compete on accessibility. Their Classic bodies serve the Japanese/European hyper-realism collector. The $4,401 floor is the lowest a silicone Classic currently enters the market from any brand with meaningful catalogue depth. ZELEX at $2,299 is not competing with Gynoid — it is opening a new tier.

### Other silicone brands with Classic presence

| Brand | Classic bodies | Silicone share | Median price | Notes |
|---|---:|---:|---:|---|
| Gynoid | 5 | 100% | $5,391 | Ultra-premium; Classic primary family |
| Jiusheng | 2 | 100% | $2,290 | 2 Classic bodies in an 8-body catalogue; not Classic-specialist |
| Sanhui | 1 | 100% | $2,599 | 1 Classic in a 7-body silicone catalogue |
| Hitdoll | 1 | 100% | $1,437 | Single Classic body; budget tier |
| ILdoll | 1 | 100% | $1,437 | Single Classic body; budget tier |
| Piper Doll | 2 | 90% | $1,290 | 2 Classic bodies; broad catalogue, budget positioning |
| Tayu | 1 | 86% | $3,800 | 1 Classic body; catalogue is Muse/Icon-heavy |

No silicone brand owns the $2,000–$3,000 Classic segment with catalogue depth and strategic intent. Jiusheng ($2,290 median, 2 Classic bodies) and Sanhui ($2,599 median, 1 Classic body) are the closest price neighbours — neither is Classic-specialist; both carry Classic bodies by measurement accident, not design. The window is open.

### The TPE tier — current floor

| Brand | Classic bodies | Silicone share | Median price | Notes |
|---|---:|---:|---:|---|
| Lilydoll | 6 | 0% | $1,199 | Largest Classic count after Gynoid; not silicone |
| Jarliet | 2 | 0% TPE | $1,558 | Classic as secondary family |
| Dime Doll | 2 | 0% TPE | $1,699 | Classic as minor family |
| WM Doll | 1 | 0% TPE | $1,694 | Single Classic; volume brand |
| AS Doll | 1 | 0% TPE | $1,993 | Single Classic |

The TPE Classic tier clusters under $2,000. This defines the floor expectation: a Classic body "should" be accessible. ZELEX at $2,299 in silicone would be ~$300–$500 above the TPE ceiling and $2,100 below Gynoid's silicone floor. That is a defensible pricing band — and the only silicone entry in it.

---

## 3. ZELEX Positioning

**Source of truth:** `db/family_taxonomy.json` — The Classic: WHR 0.68–0.72, BWR 1.40–1.50, premium marker +20%, target buyer "First-time premium buyer."

**vs Gynoid ($4,401+):** ZELEX at $2,299 does not compete with Gynoid's collector market. The positioning is: *silicone Classic, accessible premium, first-time buyer.* Gynoid is the artisan reference point that validates material quality commands a premium. ZELEX is the entry to the silhouette category in silicone at all — two tiers below Gynoid's floor, accessible to the first-time buyer who wants quality material but is not a hyper-realism collector.

**vs TPE ($1,199–$1,699):** The buyer trading from TPE to silicone in The Classic body shape has no current destination. ZELEX at $2,299 commands a ~$600–$1,100 premium over TPE alternatives. The material justification (silicone skin feel, durability, oil-free surface) plus ZELEX's character architecture (named characters, quiz-matched entry, measurement documentation) supports this spread cleanly.

**Price derivation:** ZELEX's overall catalog median is approximately $1,999 (ZELEX Dollstudio proxy: range $1,390–$2,450, median ~$1,840). The Classic's +20% premium marker in the taxonomy applied to a ~$1,999 base gives a natural band of $2,199–$2,399. A debut price of $2,299 sits at the midpoint of that band and at the structural midpoint between the TPE floor and the Gynoid silicone entry.

**Positioning headline (draft):** *"The Classic — the silhouette every buyer recognises, in silicone, under $2,500. The first of its kind."*

---

## 4. Entry Specification

**Minimum viable Classic body.**

The Classic is the most geometrically "centred" of the six families — the intersection point between the Muse (hip-dominant, lower BWR) and the Icon (waist-suppressed, higher BWR). The silhouette reads as complete only when both axes land inside the window simultaneously.

| Axis | Target | Range | Notes |
|---|---|---|---|
| WHR | 0.70 | 0.68–0.72 | Centre of range; the most "balanced" hourglass proportion |
| BWR | 1.45 | 1.40–1.50 | Mid-range; clear separation from Icon (BWR 1.50–1.60) |
| Cup | D | D minimum | Proportional credibility at WHR 0.70; E is acceptable |
| Height | 165 cm | 160–168 cm | Photographs neutrally; avoids height extremes |
| Material | Silicone | Mandatory | The Classic's "effortlessly complete" tactile read requires silicone |

**Manufacturing implications.**

A WHR of 0.70 at a standard waist of 58 cm implies hips of ~83 cm. At BWR 1.45, bust = 58 × 1.45 ≈ 84 cm. Bust and hip within ~1 cm of each other — close-set proportions. The mould must be sculpted to balance without either dimension reading as dominant. This is harder to execute credibly than either the Siren (bust-dominant, visually obvious) or the Muse (hip-dominant, visually obvious). The visual brief is "effortlessly complete" — no feature calls attention to itself.

Silicone-specific: A D or E cup at this waist-to-hip geometry should feel substantive without overwhelming. Platinum-cure silicone Shore hardness in the 0–10A range (consistent with ZELEX's SLE line) achieves this. TPE cannot replicate the self-supporting feel at this cup size and WHR.

**Suggested first SKU:** 165 cm, D cup, WHR 0.70, BWR 1.45 — the geometric centre of the family, the safest first proof-of-concept.

---

## 5. Revenue Opportunity

*The figures below are estimated from catalogue data and general e-commerce benchmarks, not from ZELEX transaction data. They are directional, not financial projections.*

**Demand signal — catalogue gap.** Classic is the second-most-present family in competitor catalogues after Muse. Buyer demand for the Classic silhouette is broad enough that volume-generic brands (WM, SE, AS, Jarliet) add at least one Classic SKU to their catalogues even when it is not their strategy. Presence at 14/29 (48%) of competitors signals sustained, cross-tier buyer demand that has not consolidated behind a single premium-silicone provider.

**Quiz dead-end cost (estimated).** The Classic WHR/BWR range sits at the geometric centre of the six-family space — the most common natural body shape proportion. In a quiz routing buyers by proportion preference, The Classic is the most likely modal result for a first-time buyer describing "realistic, balanced proportions." If 20–35% of quiz completions route to Classic, and if 100 buyers/month complete the quiz at launch, that is 20–35 monthly Classic-first buyers with no product to purchase. At $2,299 target price and a 10% conversion (standard e-commerce baseline for high-consideration product), the per-month opportunity cost is approximately $460–$805 — or $5,500–$9,700/year — from a single SKU gap. This is a conservative illustrative estimate based on general benchmarks and proportional geometry logic, not observed ZELEX traffic data.

**Competitive urgency.** No brand currently owns the $2–3k silicone Classic tier with strategic intent. This window is open today. Any silicone manufacturer with Classic-range measurement profiles already in production can enter this tier with a price change and a landing page. ZELEX's advantage is the taxonomy infrastructure — quiz routing, family architecture, character layer — that a price adjustment alone cannot replicate.

---

## 6. Commercial Translation

### Launch Sequence

1. **Factory brief** — Commission 165 cm, D cup, WHR 0.70 ± 0.01, BWR 1.45 ± 0.03. Confirm measurement feasibility against existing SLE tooling. Prototype review before production sign-off.
2. **Character development** — Write two character profiles and commission photography against the hero body before site launch. Launch with 2 slots, not 4 — lean launch, expand after 90-day sales validation.
3. **Landing page activation** — `/families/classic` exits dev-card status on launch day. Full landing page: WHR/BWR spec, character grid, "first silicone Classic under $2,500" positioning copy.
4. **Pricing** — $2,299 retail at debut. Positioned explicitly as "silicone hourglass, accessible premium" — not competing upward toward Gynoid, not discounting into TPE territory.
5. **Quiz routing** — Classic quiz path activates on launch day. Buyers who preference-route to "realistic, balanced proportions" receive a Classic result and a live product page. Email capture is removed; the dev-card waitlist is replaced by a purchase flow.

### Launch State

| Surface | State at debut |
|---|---|
| Homepage | Not present — no hero or teaser; family descriptor in footer only until 3+ bodies active |
| Quiz | Active — Classic routing resolves to a live product page on day one |
| Compare filter | Active — Classic filter enabled |
| Landing page | Full depth — `/families/classic` fully deployed |
| SEO priority | P2 (organic) — Classic queries have the highest organic demand of any family; placeholder indexed immediately |
| Character badge | No — reserved for families with 2+ characters deployed |
| Email capture | Removed on launch day — replaced by purchase flow |

### Inquiry Routing

| Tag | Routing logic |
|---|---|
| `body:classic` | Route to first-time buyer guided discovery flow; emphasize material upgrade positioning (silicone vs TPE) and ZELEX character architecture |
| `body:classic-waitlist` | Pre-launch only — capture email, "notify me when Classic launches." Remove on launch day. |

### SEO Page Strategy

`/families/classic` content priorities:
1. Family definition and WHR/BWR specs — establishes measurement authority
2. "First silicone Classic under $2,500" — the competitive differentiator
3. Character grid with two deployed characters — gives the landing page a product, not just a promise
4. Material comparison copy — why silicone at this price point vs TPE alternatives at $1,200–$1,700

---

## 7. Strategic Conclusion

Three findings govern the Classic entry decision:

1. **The Classic gap is a first-time buyer access problem, not a product completeness problem.** The timeless hourglass is what most first-time premium buyers are searching for. ZELEX is absent from this lane entirely while 48% of competitors cover it. Every quiz completion that routes to Classic today loses a buyer. The PDR-010 analysis identified adding Classic bodies as the highest-priority product addition for Q3 2026; this brief operationalises that recommendation.

2. **The $2,000–$3,000 silicone Classic window is structurally open and time-limited.** No brand owns this tier with catalogue depth and positioning intent today. The brands nearest in price (Jiusheng at $2,290, Sanhui at $2,599) are not Classic-specialists — they carry Classic bodies by measurement accident. A deliberate entry at $2,299 with ZELEX's character architecture captures the lane before a competitor fills it intentionally.

3. **One body at the right price is the complete thesis.** The revenue opportunity is not a 6-body Classic build — it is removing the dead end from the quiz flow for the largest buyer segment ZELEX does not currently serve. A single hero body at $2,299, paired with two named characters and a full landing page, achieves this. The demand signal from the first 90 days of Classic sales informs whether to expand to a second body.

**Positioning headline (final):** *"The Classic — the silhouette every buyer recognises, in silicone, under $2,500. The first of its kind."*

---

## 8. Acceptance Review

| Criterion | Status |
|---|---|
| ZELEX gap confirmed against official taxonomy (0 Classic bodies) | ✓ db/family_taxonomy.json member_count: 0 |
| Competitor pricing landscape with silicone/TPE split | ✓ Section 2 |
| Silicone window ($2,000–$3,000) emptiness documented | ✓ Section 2 — no incumbent with catalogue depth |
| Entry specification with WHR/BWR, cup, height, material | ✓ Section 4 |
| Manufacturing implications for balanced hourglass geometry | ✓ Section 4 |
| Revenue opportunity estimate with caveats | ✓ Section 5 |
| Pricing justification vs Gynoid and TPE tier | ✓ Section 3 |
| 5-step launch sequence documented | ✓ Section 6 |
| Commercial translation: quiz, landing page, SEO, inquiry routing | ✓ Section 6 |
| Direct answer to entry question | ✓ Decision: WHR 0.70 / BWR 1.45, 165 cm, silicone, $2,299 |

### Dataset Limitations

- Revenue opportunity estimates (quiz dead-end cost) are based on general e-commerce benchmarks and proportional geometry logic, not observed ZELEX quiz or traffic data. Figures are directional.
- All competitor Classic pricing is sourced from secondary aggregators (DollStudio, SiliconWives) except Tayu (official). Prices reflect crawl date (2026-06-05) and change frequently.
- ZELEX official pricing is not published in the manufacturer catalog. The $1,999 catalog median and $2,199–$2,399 target band are derived from the ZELEX Dollstudio secondary proxy ($1,390–$2,450 range).

---

*Supporting artifacts: `docs/research/competitor-family-coverage-matrix.md` · `docs/research/roi-by-family.md` · `docs/pdr/PDR-010-competitor-family-coverage-roi-validation.md` · `db/competitor_family_coverage.json` · `db/family_taxonomy.json`*
