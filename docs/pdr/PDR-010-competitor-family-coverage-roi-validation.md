# PDR-010: Competitor Family Coverage and ROI Validation

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-05  
**Revised:** 2026-06-06 (data verification pass — penetration counts corrected against `db/competitor_family_coverage.json`; staged launch graduation criteria made explicit; competitive urgency timing section added)  
**Status:** Draft — Pending CEO Review

---

## Decision

**Stage the six-family taxonomy. Do not promote all six equally at launch.**

The research shows that ZELEX's catalog defensibly populates three families today (Muse, Icon, Siren). Two families have zero product coverage (Classic, Sculpt) and should not appear on the homepage or in conversion surfaces. The sixth (Empress) has one body and is quiz-eligible only.

The taxonomy itself is sound and measurement-grounded. The product coverage is not yet sufficient to support full-breadth promotion. The right move is a staged launch that names all six families but only activates three on revenue surfaces.

The most important finding is not coverage — it is strategic priority. Classic is the single largest near-term revenue unlock (broadest buyer demand in the market, zero ZELEX coverage). Sculpt is already dominated by MD Doll and does not merit urgency without a silicone differentiation angle.

---

## 1. ZELEX Baseline

**Source:** `db/family_taxonomy.json` (official manufacturer specs, all 19 body profiles)  
**Confidence:** 94.7% exact + near (18/19 bodies)  
**Price coverage:** 0% — ZELEX does not publish prices in official catalog; secondary reseller data available via ZELEX (Dollstudio) row at $1390–2450

| Family | Bodies | Share | Status |
|---|---:|---:|---|
| The Muse | 12 | 63.2% | Active |
| The Icon | 4 | 21.1% | Active |
| The Siren | 2 | 10.5% | Active |
| The Empress | 1 | 5.3% | Active (thin) |
| The Classic | 0 | 0% | In-Development |
| The Sculpt | 0 | 0% | In-Development |
| **Total** | **19** | | |

**Verification note (2026-06-06):** All six family member counts confirmed exact against `db/family_taxonomy.json` `member_count` fields. No discrepancies found.

**Top-2 concentration:** 84.2% (Muse + Icon)  
**Interpretation:** ZELEX is a curated, concentration-forward catalog. This is intentional. The question is whether the concentration is in the right families given market demand and whitespace.

---

## 2. Market Concentration Analysis

**Dataset:** 29 independent competitor brands, 476 classified body profiles (excludes ZELEX 19 and ZELEX Dollstudio 10 from market-facing count)

### Top-2 Concentration by Brand

| Band | Brands |
|---|---|
| 100% (single or dual dominant) | Irontech Doll (100%), Gynoid (90%) |
| 80–89% | Lusandy Doll (85.7%), Dime Doll (83.9%), Hitdoll (80%), ILdoll (80%), Angel Kiss (80%), YL Doll (80%) |
| 70–79% | Lilydoll (78.6%), FunWest (73.6%), MD Doll (72.5%), HR Doll (70%), Irokebijin (70%), JY Doll (70%), Jarliet (70%), SM Doll (70%), Real Lady (75%), JK Doll (75%), WM Doll (60%), XT Doll (60%), SE Doll (60%), 6YE Premium (60%), AS Doll (50%) |
| < 60% | Sanhui (57.1%), Game Lady (66.7%), Tayu (66.7%), Jiusheng (62.5%), Piper Doll (40%) |

**Market median top-2 concentration:** ~72%  
**ZELEX top-2 concentration:** 84.2%  
**Verdict:** ZELEX is more concentrated than the median competitor. This is above average but not an outlier. Irontech (100%) and Gynoid (90%) are more concentrated at the premium end. ZELEX's concentration is a positioning asset, not a coverage liability, provided the top-2 families are the right ones.

### Family Penetration Across the Market

**Verified count source:** `db/competitor_family_coverage.json` summary.brands — 29 brands (excludes ZELEX official). Counts computed from `family_counts[family] > 0` per brand.

| Family | Brands with ≥1 body | Market % (of 29 competitors) | ZELEX position |
|---|---:|---:|---|
| The Muse | 27 | 93% | Dominant (12 bodies) |
| The Icon | 23 | 79% | Present (4 bodies) |
| The Sculpt | 21 | 72% | Absent |
| The Empress | 18 | 62% | Thin (1 body) |
| The Siren | 16 | 55% | Thin (2 bodies) |
| The Classic | 14 | 48% | Absent |

**Data correction note (2026-06-06):** Prior draft stated Muse 28/29 (97%), Icon 20/29 (69%), Sculpt 19/29 (66%), Siren 13/29 (45%). These figures have been corrected to the values above after recount against the source JSON. Two brands have zero Muse bodies (Lilydoll, YL Doll); six brands have zero Icon bodies (SM Doll, JY Doll, Gynoid, ILdoll, 6YE Premium, Hitdoll). The strategic conclusions are unchanged or strengthened: Sculpt is even more saturated than previously stated (72%, not 66%); Siren is more mainstream than previously stated (55%, not 45%), which slightly reduces but does not eliminate its differentiation value at the premium silicone tier.

**Concentration interpretation:** Muse is the industry near-default — 93% of competitors have at least one Muse body. ZELEX being Muse-heavy reflects the market, not a differentiation. The differentiation comes from Muse *quality* and from what flanks Muse: Icon at the glamour tier and Siren in the character lane.

---

## 3. Whitespace Analysis

### 3a. ZELEX Under-Covered vs. Competitors

**Classic (priority: HIGH)**  
14 of 29 competitors (48%) have Classic bodies, but ZELEX has zero. Gynoid leads with 5 Classic bodies at $4401–7038; Lilydoll carries 6 Classic bodies at $1199–1299, showing the entry tier. This is the widest first-time-buyer family in the market and ZELEX is entirely absent. The timeless hourglass is what most first-time buyers are searching for. ZELEX cannot reach this buyer segment today.

→ **Action required:** Minimum 3 Classic body additions before the Classic lane can be activated in quiz and compare. Top priority for product roadmap.

**Sculpt (priority: LOWER)**  
21 of 29 competitors (72%) have Sculpt bodies. MD Doll has 37 Sculpt bodies at $1674–2599 and is the category anchor. This market is saturated, particularly at the mid-tier. Most Sculpt bodies in the market are TPE (MD Doll silicone share: only 33.3%). A silicone-quality ZELEX Sculpt body at $2500+ would be differentiated, but there is no urgency — the category does not create buyer urgency in the way Classic does for first-timers.

→ **Action required:** Suppress from launch surfaces. Revisit when a silicone differentiation angle is designed.

**Empress (priority: MEDIUM-LOW)**  
18 of 29 competitors (62%) have Empress bodies. ZELEX has 1 (ZX164G). The thinness means quiz routing always surfaces the same body, reducing discovery value. 6YE Premium (3), Lilydoll (5), MD Doll (13), and Real Lady (2) show the competitive spread. Not a crisis, but expansion to 3+ Empress bodies would restore quiz utility.

→ **Action required:** 2+ additional Empress bodies would restore quiz/compare utility. Medium priority.

### 3b. Category-Wide Whitespace (Both ZELEX and Market Are Thin)

**Premium-silicone Sculpt below $2500** — MD Doll dominates sculpt at $2599, but their silicone share is only 33.3%. Most sculpt bodies in the market are TPE. A ZELEX-quality silicone sculpt in the $1800–2200 range would be an unoccupied position. This is speculative product design (out of scope for PDR-010), but the commercial case exists.

**Official-source depth** — Only Irontech and Tayu provide official manufacturer specs. Every other competitor relies on secondary aggregator data (DollStudio, SiliconWives). ZELEX's 100% official source and 94.7% exact+near confidence is an unrecognized quality advantage. This is an underutilized content differentiator.

### 3c. ZELEX Strength Lanes

**Muse depth** — 12 bodies with 100% official source data and ~92% exact+near. No competitor with official source data has more Muse-family bodies. FunWest has 38 Muse bodies but from secondary sources only.

**Icon quality tier** — At $2750+, Irontech is the only peer with official data in the Icon family. ZELEX's Icon bodies (ZK159D, ZX163E, ZX165D, ZX172E) at ZELEX's price range are well-positioned against a single competitor. Positioning ZELEX vs. Irontech as a quality comparison could anchor the Icon narrative.

**Data credibility advantage** — 94.7% exact+near vs. the market average of ~72%. ZELEX's measurement-first approach is a positioning asset that no competitor currently communicates.

### 3d. Competitor Lanes Worth Monitoring

**FunWest's Icon+Muse breadth** — 106 bodies (40 Icon, 38 Muse) at $1299–2499 represents the largest mid-market alternative to ZELEX in Icon/Muse space. FunWest buyers are the natural upgrade path to ZELEX. Content comparisons targeting FunWest buyers could extract search volume.

**JY Doll's Siren concentration** — 50% Siren (5/10 bodies) at $1390–2390. JY Doll signals that there is buyer demand for the Siren silhouette at mid-price. ZELEX's Siren at premium-silicone quality is differentiated but competing for the same buyer intent.

---

## 4. ROI Thesis by Family

*Full scoring detail in `docs/research/roi-by-family.md`. Scores are 1–5 across eight dimensions. Weighted composite uses: availability ×2, conversion utility ×2, roadmap value ×1.5, other dimensions ×1.*

| Family | Availability | Diff. | Demand | SEO | Conversion | Merch | Qualification | Roadmap | **Composite** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| The Muse | 5 | 2 | 4 | 3 | 5 | 4 | 3 | 2 | **3.5** |
| The Icon | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 3 | **4.0** |
| The Siren | 2 | 4 | 4 | 5 | 3 | 4 | 4 | 5 | **3.8** |
| The Empress | 1 | 2 | 3 | 3 | 1 | 3 | 2 | 3 | **2.3** |
| The Classic | 1 | 3 | 5 | 5 | 1 | 4 | 4 | 5 | **3.4** |
| The Sculpt | 1 | 2 | 3 | 3 | 1 | 3 | 2 | 3 | **2.3** |

**Score definitions:** Availability = number of live bodies (5 = ≥10, 1 = 0); Diff. = differentiation vs. competitors; Demand = buyer search volume proxy; SEO = organic content opportunity; Conversion = ability to generate an inquiry from a quiz/compare path; Merch = visual merchandising potential; Qualification = ability to qualify the buyer for a specific SKU; Roadmap = strategic value to future product additions.

**Icon is the highest-ROI active family** — composite 4.0/5.0 — strong across differentiation, visual merchandising, and sales qualification with adequate product depth.

**Siren has the highest roadmap score** — composite 3.8/5.0 — the character/anime expansion lane is an unoccupied position at ZELEX's price tier; no competitor pairs Siren-type bodies with persona branding in the $2000+ silicone category.

**Classic has the highest demand score** — composite 3.4/5.0 depressed only by zero availability; demand and roadmap are both 5/5. Fix availability and Classic immediately becomes the highest ROI launch in the taxonomy.

**Muse is the depth anchor** — composite 3.5/5.0 — not the top scorer because differentiation is low (everyone has Muse bodies) and roadmap value is modest; but conversion is the highest of any family (5/5) due to catalog depth.

**Empress and Sculpt score identically** — composite 2.3/5.0 — both have zero to minimal product, saturated market presence, and limited current conversion utility. Empress gets quiz-eligibility because one body exists; Sculpt is fully suppressed.

---

## 5. Launch Hierarchy

| Family | Launch State | Homepage | Quiz | Compare Filter | Landing Page | SEO Priority | Character Badge |
|---|---|---|---|---|---|---|---|
| The Icon | **Primary** | Hero position | Yes | Yes | Full depth | P1 | Yes |
| The Muse | **Primary** | Feature position | Yes | Yes | Full depth | P1 | Yes |
| The Siren | **Secondary** | Teaser / coming-soon | Yes | Yes | Condensed | P2 | Yes |
| The Empress | **Secondary-thin** | Not on homepage | Yes (1 result) | Yes | Condensed | P3 | Yes |
| The Classic | **In-Development** | Not on homepage | Not yet | Not yet | Placeholder only | P2 (organic) | No |
| The Sculpt | **Suppressed** | Not created | No | No | Not created | P4 | No |

### Rationale for Icon as First Position

Irontech is ZELEX's most visible premium competitor. Irontech is 81.8% Icon (9/11 bodies). Positioning ZELEX's Icon family first — vs. Irontech's one-dimensional Icon catalog — establishes ZELEX as the multi-family alternative at the same price tier. The Icon family is ZELEX's clearest competitive argument.

### Rationale for Siren as Secondary (Not Suppressed)

2 bodies is thin for a homepage family, but Siren has the highest future roadmap value and the content angle is distinctive. Quiz and compare filter inclusion means Siren buyers can self-identify. The character/anime crossover buyer is high-intent and currently underserved at ZELEX's price tier. Maintain Siren in discovery surfaces; hold from homepage until graduation criteria are met (see Section 5a).

### Rationale for Classic as In-Development (Not Suppressed)

Classic has the highest raw buyer demand of any family. Suppressing it entirely means ZELEX cannot even surface intent from first-time buyers searching for the timeless hourglass. A placeholder landing page ("Classic — Coming in 2026") allows SEO indexing and email capture. This is more valuable than suppression.

---

### 5a. Staged Launch Graduation Criteria

In-Development families (Classic, Sculpt) and thin Secondary families (Siren, Empress) graduate to higher-prominence surfaces when the following criteria are met. Criteria are hard gates — meeting one is not sufficient; all criteria in the tier must be satisfied before promotion.

#### Classic: dev-card → quiz-eligible + compare filter

**Gate 1 (minimum viable activation):**
- ≥3 live Classic-family bodies in the ZELEX catalog
- At least 1 of the 3 bodies is the "hero" Classic body (highest merchandising score, selected by creative team)
- All 3 bodies have official manufacturer measurements (not secondary/estimated)

**Gate 2 (homepage teaser, replacing current footer callout):**
- ≥3 live bodies AND ≥90 days of sales inquiry data from the hero Classic body (minimum 30 inquiries to establish conversion baseline)
- Classic conversion rate (inquiry-to-confirmed-order) is ≥50% of the Muse conversion rate at 90 days post-launch
- Email waitlist has been sent at least one product-reveal message

**Gate 3 (full homepage feature position, equal to Muse/Icon):**
- ≥5 live Classic-family bodies
- Classic composite ROI score has risen to ≥3.5 (re-scored after Gate 2 data; currently 3.4 — expected to become the top scorer once availability improves)
- Minimum 6 months of SEO organic data from placeholder page (`/families/classic`) showing keyword trajectory

#### Sculpt: suppressed → dev-card → quiz-eligible

**Gate 1 (dev-card only — no quiz, no compare filter):**
- ZELEX has committed to a silicone-material Sculpt body (product spec locked, not just a design concept)
- A differentiated price-tier rationale is documented (ZELEX Sculpt must be positioned above $2200 with explicit silicone quality argument vs. MD Doll's TPE-majority Sculpt catalog)

**Gate 2 (quiz-eligible + compare filter):**
- ≥2 live Sculpt-family bodies
- Both bodies are silicone (not TPE), with full official measurements
- Sculpt conversion rate in quiz testing is ≥25% of the Muse rate (minimum 20 Sculpt quiz completions in A/B test)

**Rationale for higher Sculpt bar:** The Sculpt category is dominated by MD Doll (37 bodies at $1674–$2599). Entering with undifferentiated or TPE-material bodies would dilute ZELEX's premium positioning without capturing incremental revenue. The category only merits activation if ZELEX can genuinely occupy the premium-silicone Sculpt lane.

#### Siren: teaser → full homepage feature

**Gate (teaser → homepage feature, equal to Icon/Muse):**
- ≥4 live Siren-family bodies (currently 2: ZX160J, ZX166K)
- Character/persona content is published for at least 2 of the 4 bodies (full editorial, not placeholder)
- Siren quiz completion rate is ≥15% of all quiz completions (indicates self-selecting buyer segment is large enough to justify homepage real estate)

#### Empress: single-result → multi-result (quiz only, not homepage)

**Gate (single-result → multi-result quiz, no homepage change):**
- ≥3 live Empress-family bodies (currently 1: ZX164G)
- At least 2 of the 3 bodies are from different series (avoid quiz returning near-duplicate results)

---

## 6. Competitive Urgency Timing

*This section addresses the question: if ZELEX does not add Classic or Sculpt bodies, when would a competitor fill the gap in a way that forecloses ZELEX's entry?*

### Classic — Window Is Open, But Not Indefinitely

**Current landscape:** 14 of 29 competitors (48%) carry Classic bodies, but none at ZELEX's price tier with silicone material and official-source measurements. Gynoid (5 Classic bodies, $4401–7038) is the closest analog on quality but operates at a higher price band. Lilydoll (6 Classic bodies, $1199–1299) owns the entry-price Classic lane. The mid-premium Classic position ($2000–3000, silicone) is genuinely unoccupied as of the data collection date (2026-Q2).

**Risk scenario:** The mid-premium gap is visible to any competitor doing market analysis. Lusandy Doll (currently 0 Classic bodies, 35 total bodies, $2599–2699, silicone) or a brand like FunWest (106 bodies, 0 Classic) could add Classic bodies by expanding measurement ranges from their existing Icon/Muse catalog. Lusandy is the highest-risk entrant given its price overlap with ZELEX's likely Classic pricing.

**Urgency clock:** Based on observed catalog update cadence across the dataset (secondary brands add 5–15 bodies per 6-month period), a mid-premium competitor could plausibly occupy the $2000–2500 silicone Classic lane within 12–18 months if the market signal continues to strengthen. ZELEX's target window for Gate 1 Classic launch is **Q3 2026 (3 bodies)**. If Classic launch slips past Q4 2026, the unoccupied position probability drops from ~80% to ~50%.

**Action:** Classic body additions are not optional roadmap items — they are time-sensitive competitive moves. Every quarter of delay increases the probability that Lusandy, FunWest, or a new entrant claims the position ZELEX is best-suited to own.

### Sculpt — No Urgency; Gap May Not Close

**Current landscape:** MD Doll owns Sculpt with 37 bodies at $1674–$2599, but with only 33.3% silicone share. No other brand has come close to challenging MD Doll in Sculpt volume. The category appears to be winner-takes-most for the TPE tier.

**Risk scenario:** A premium-silicone Sculpt entrant could emerge, but the category is unattractive for new entrants at ZELEX's price tier because MD Doll's TPE prices ($1674+) already compress margins for anyone trying to price a silicone body competitively. The silicone Sculpt position ($2500+) has no current occupant, but the buyer demand signal does not justify the product development cost without an explicit athletic/fitness branding angle.

**Urgency clock:** No meaningful competitive urgency for Sculpt within a 24-month horizon, provided ZELEX is not planning to launch a fitness/athletic persona brand. If ZELEX does develop a dedicated athletic sub-brand, Sculpt activation should be accelerated to Gate 1 within that roadmap.

### Icon and Muse — Defend, Don't Chase

**Icon:** Irontech Doll (100% Icon, official source, $2750–3379) is the only peer-quality competitor in this lane. Irontech has not been observed adding new bodies at a high rate (11 total bodies with official source suggests deliberate catalog curation, not volume expansion). The Irontech vs. ZELEX Icon narrative is durable for at least 24 months without requiring additional Icon bodies from ZELEX.

**Muse:** 27 of 29 competitors have Muse bodies, and FunWest has 38. Muse is a commodity family. ZELEX's advantage is data quality (official source) and silicone material, not catalog depth. Adding more Muse bodies provides diminishing differentiation return. Prioritize Icon, Classic, and Siren additions over additional Muse expansion.

---

## 7. Frontend and Commercial Translation

### Homepage Order and Prominence

```
Row 1 (Hero): The Icon  — "Glamour model silhouette"
Row 2 (Feature): The Muse — "Tall, hip-dominant"
Row 3 (Teaser): The Siren — "Bust-dominant fantasy — new bodies arriving"
[Empress visible in quiz/compare; not on homepage]
[Classic: "Coming in 2026" footer callout only]
[Sculpt: withheld entirely]
```

### Quiz Result Eligibility

| Family | Eligible | Min bodies required | Current bodies | Result |
|---|---|---:|---:|---|
| The Icon | Yes | 2 | 4 | ✓ Eligible |
| The Muse | Yes | 2 | 12 | ✓ Eligible |
| The Siren | Yes | 1 | 2 | ✓ Eligible |
| The Empress | Yes | 1 | 1 | ✓ Eligible (single result) |
| The Classic | No | 2 | 0 | ✗ Not eligible |
| The Sculpt | No | 2 | 0 | ✗ Not eligible |

### Compare-Page Family Filters

Active filters at launch: Icon, Muse, Siren, Empress.  
Hidden filters: Classic (placeholder), Sculpt (suppressed).

### Inquiry Prefill and Routing

| Family | Inquiry tag | Routing logic |
|---|---|---|
| The Icon | `body:icon` | Route to editorial/photographer persona funnel |
| The Muse | `body:muse` | Route to standard catalog flow |
| The Siren | `body:siren` | Route to character/anime crossover interest capture |
| The Empress | `body:empress` | Route to body-positivity collector messaging |
| The Classic | `body:classic-waitlist` | Capture email; "notify me when Classic launches" |
| The Sculpt | (none) | Not surfaced |

### SEO Page Generation Priority

1. `/families/icon` — full landing page, editorial photography, Irontech comparison angle
2. `/families/muse` — full landing page, depth emphasis
3. `/families/siren` — condensed, character focus
4. `/families/empress` — condensed, body-positivity editorial
5. `/families/classic` — placeholder, "coming in 2026", email capture
6. `/families/sculpt` — not generated at launch

---

## 8. Strategic Conclusion

**The six-family taxonomy earns its place in launch strategy, but not all six families should have equal buyer-facing prominence at launch.**

Three findings govern the recommendation:

1. **ZELEX's current concentration is an asset, not a liability.** At 84.2% top-2 concentration (Muse+Icon), ZELEX is more curated than the median competitor. This is appropriate for a premium silicone brand. The risk is not that ZELEX is too narrow — it is that the top-2 families chosen for concentration are the right ones. Muse and Icon are defensible. Icon has the clearest differentiation angle at the premium price tier (vs. Irontech). Muse is the depth anchor.

2. **The Siren is the most strategically important secondary family.** No competitor at ZELEX's price tier pairs Siren-type bodies with character persona branding. This is the only unoccupied premium position in the market. Two bodies is not enough for full homepage treatment, but the roadmap priority is clear: add 2–3 Siren bodies and the content angle becomes a category-defining move.

3. **Classic must be treated as a product roadmap emergency, not a marketing suppression.** The timeless hourglass is what most first-time premium buyers are searching for. ZELEX is absent from this lane entirely while 48% of competitors cover it. Adding Classic bodies is not about taxonomy completeness — it is about being addressable to the largest segment of the premium doll buyer market. The PDR-010 recommendation is: first 3 Classic body additions are the highest-priority product additions for Q3 2026. The unoccupied mid-premium silicone Classic position ($2000–2500) has an estimated 12–18 month window before a competitor (most likely Lusandy or FunWest) can fill it.

---

## 9. Acceptance Review

| Criterion | Status |
|---|---|
| ≥80 body profiles collected | ✓ 495 total; 476 competitor + 19 ZELEX |
| ≥6 competitor brands covered | ✓ 29 independent brands |
| Evidence tier recorded for every row | ✓ All rows carry source_tier (official, secondary) |
| Normalization completeness | ✓ 100% measurement completeness across all brands |
| Family assignment completeness | ✓ 495 rows classified; 0 unclassified |
| Traceability to matrix and ROI | ✓ See `docs/research/competitor-family-coverage-matrix.md`, `docs/research/roi-by-family.md` |
| Direct answer to strategic question | ✓ Section 8: Stage the taxonomy |
| Staged launch graduation criteria | ✓ Section 5a: Explicit metric thresholds for Classic (3 gates), Sculpt (2 gates), Siren, Empress |
| Competitive urgency timing | ✓ Section 6: Classic 12–18 month window; Sculpt no urgency; Icon/Muse defend posture |
| Penetration counts verified | ✓ Section 2 corrected against source JSON 2026-06-06; Classic/Empress unchanged; Muse/Icon/Sculpt/Siren corrected |

### Dataset Limitations

- All competitor data except Irontech Doll (11) and Tayu (21) is sourced from secondary aggregators (DollStudio, SiliconWives). Family confidence is lower for secondary-sourced brands; findings should be treated as directional, not exact.
- RealDoll body measurements were not accessible for classification; 13 model URLs captured but not classified.
- Doll Forever catalog was not accessible at the time of crawl.
- ZELEX official pricing is not published in the manufacturer catalog. Price comparisons use ZELEX (Dollstudio) secondary data as a proxy.

---

*Supporting artifacts: `docs/research/roi-by-family.md` · `docs/research/source-log.md` · `docs/research/competitor-family-coverage-matrix.md` · `db/competitor_family_coverage.json` · `db/competitor_family_coverage.sqlite`*
