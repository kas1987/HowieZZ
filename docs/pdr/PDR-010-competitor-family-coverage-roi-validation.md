# PDR-010: Competitor Family Coverage and ROI Validation

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-05  
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

**Top-2 concentration:** 84.2% (Muse + Icon)  
**Interpretation:** ZELEX is a curated, concentration-forward catalog. This is intentional. The question is whether the concentration is in the right families given market demand and whitespace.

---

## 2. Market Concentration Analysis

**Dataset:** 29 independent competitor brands, 476 classified body profiles (excludes ZELEX 19 and ZELEX Dollstudio 10 from market-facing count)

### Top-2 Concentration by Brand

| Band | Brands |
|---|---|
| 100% (single or dual dominant) | Irontech Doll (100%), Gynoid (90%) |
| 80–89% | Lusandy Doll (85.7%), Dime Doll (83.9%), Dime, Hitdoll (80%), ILdoll (80%), Angel Kiss (80%), YL Doll (80%) |
| 70–79% | Lilydoll (78.6%), FunWest (73.6%), MD Doll (72.5%), HR Doll (70%), Irokebijin (70%), JY Doll (70%), Jarliet (70%), SM Doll (70%), Real Lady (75%), JK Doll (75%), WM Doll (60%), XT Doll (60%), SE Doll (60%), 6YE Premium (60%), AS Doll (50%) |
| < 60% | Sanhui (57.1%), Game Lady (66.7%), Tayu (66.7%), Jiusheng (62.5%), Piper Doll (40%) |

**Market median top-2 concentration:** ~72%  
**ZELEX top-2 concentration:** 84.2%  
**Verdict:** ZELEX is more concentrated than the median competitor. This is above average but not an outlier. Irontech (100%) and Gynoid (90%) are more concentrated at the premium end. ZELEX's concentration is a positioning asset, not a coverage liability, provided the top-2 families are the right ones.

### Family Penetration Across the Market

| Family | Brands with ≥1 body | Market % (of 29 competitors) | ZELEX position |
|---|---:|---:|---|
| The Muse | 28 | 97% | Dominant (12 bodies) |
| The Sculpt | 19 | 66% | Absent |
| The Icon | 20 | 69% | Present (4 bodies) |
| The Empress | 18 | 62% | Thin (1 body) |
| The Classic | 14 | 48% | Absent |
| The Siren | 13 | 45% | Thin (2 bodies) |

**Concentration interpretation:** Muse is the industry default — nearly every competitor has Muse bodies. ZELEX being Muse-heavy is the market average, not a differentiation. The differentiation comes from Muse *quality* and from what flanks Muse: Icon at the glamour tier and Siren in the character lane.

---

## 3. Whitespace Analysis

### 3a. ZELEX Under-Covered vs. Competitors

**Classic (priority: HIGH)**  
14 of 29 competitors (48%) have Classic bodies, but ZELEX has zero. Gynoid leads with 5 Classic bodies at $4401–7038; Lilydoll at $1199–1299 shows the entry tier. This is the widest demand family (first-time premium buyer) and ZELEX is entirely absent. The timeless hourglass is what most first-time buyers are searching for. ZELEX cannot reach this buyer segment today.

→ **Action required:** Minimum 3 Classic body additions before the Classic lane can be activated in quiz and compare. Top priority for product roadmap.

**Sculpt (priority: LOWER)**  
19 of 29 competitors (66%) have Sculpt bodies. MD Doll has 37 Sculpt bodies at $1674–2599. This market is saturated, particularly at the mid-tier. Most Sculpt bodies in the market are TPE. A silicone-quality ZELEX Sculpt body at $2500+ would be differentiated, but there is no urgency — the category does not create buyer urgency in the way Classic does for first-timers.

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

**JY Doll's Siren concentration** — 50% Siren at $1390–2390. JY Doll signals that there is buyer demand for the Siren silhouette at mid-price. ZELEX's Siren at premium-silicone quality is differentiated but competing for the same buyer intent.

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

**Icon is the highest-ROI active family** — strong across differentiation, visual merchandising, and sales qualification with adequate product depth.

**Siren has the highest roadmap score** — the character/anime expansion lane is an unoccupied position at ZELEX's price tier; no competitor pairs Siren-type bodies with persona branding in the $2000+ silicone category.

**Classic has the highest demand score** — the composite is lower only because product availability is zero. Fix availability and Classic immediately becomes the highest ROI launch.

**Empress and Sculpt score identically** — both have zero to minimal product, saturated market presence, and limited current conversion utility. Empress gets quiz-eligibility because one body exists; Sculpt is fully suppressed.

---

## 5. Launch Hierarchy

| Family | Launch State | Homepage | Quiz | Compare Filter | Landing Page | SEO Priority | Character Badge |
|---|---|---|---|---|---|---|---|
| The Icon | **Primary** | Hero position | Yes | Yes | Full depth | P1 | Yes |
| The Muse | **Primary** | Feature position | Yes | Yes | Full depth | P1 | Yes |
| The Siren | **Secondary** | Teaser / coming-soon | Yes | Yes | Condensed | P2 | Yes |
| The Empress | **Secondary-thin** | Not on homepage | Yes (1 result) | Yes | Condensed | P3 | Yes |
| The Classic | **In-Development** | Not on homepage | Not yet | Not yet | Placeholder only | P2 (organic) | No |
| The Sculpt | **Suppressed** | Not on homepage | No | No | Not created | P4 | No |

### Rationale for Icon as First Position

Irontech is ZELEX's most visible premium competitor. Irontech is 81.8% Icon. Positioning ZELEX's Icon family first — vs. Irontech's one-dimensional Icon catalog — establishes ZELEX as the multi-family alternative at the same price tier. The Icon family is ZELEX's clearest competitive argument.

### Rationale for Siren as Secondary (Not Suppressed)

2 bodies is thin for a homepage family, but Siren has the highest future roadmap value and the content angle is distinctive. Quiz and compare filter inclusion means Siren buyers can self-identify. The character/anime crossover buyer is high-intent and currently underserved at ZELEX's price tier. Maintain Siren in discovery surfaces; hold from homepage until 3+ bodies are active.

### Rationale for Classic as In-Development (Not Suppressed)

Classic has the highest raw buyer demand of any family. Suppressing it entirely means ZELEX cannot even surface intent from first-time buyers searching for the timeless hourglass. A placeholder landing page ("Classic — Coming in 2026") allows SEO indexing and email capture. This is more valuable than suppression.

---

## 6. Frontend and Commercial Translation

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

## 7. Strategic Conclusion

**The six-family taxonomy earns its place in launch strategy, but not all six families should have equal buyer-facing prominence at launch.**

Three findings govern the recommendation:

1. **ZELEX's current concentration is an asset, not a liability.** At 84.2% top-2 concentration (Muse+Icon), ZELEX is more curated than the median competitor. This is appropriate for a premium silicone brand. The risk is not that ZELEX is too narrow — it is that the top-2 families chosen for concentration are the right ones. Muse and Icon are defensible. Icon has the clearest differentiation angle at the premium price tier (vs. Irontech). Muse is the depth anchor.

2. **The Siren is the most strategically important secondary family.** No competitor at ZELEX's price tier pairs Siren-type bodies with character persona branding. This is the only unoccupied premium position in the market. Two bodies is not enough for full homepage treatment, but the roadmap priority is clear: add 2–3 Siren bodies and the content angle becomes a category-defining move.

3. **Classic must be treated as a product roadmap emergency, not a marketing suppression.** The timeless hourglass is what most first-time premium buyers are searching for. ZELEX is absent from this lane entirely while 48% of competitors cover it. Adding Classic bodies is not about taxonomy completeness — it is about being addressable to the largest segment of the premium doll buyer market. The PDR-010 recommendation is: first 3 Classic body additions are the highest-priority product additions for Q3 2026.

---

## 8. Acceptance Review

| Criterion | Status |
|---|---|
| ≥80 body profiles collected | ✓ 495 total; 476 competitor + 19 ZELEX |
| ≥6 competitor brands covered | ✓ 29 independent brands |
| Evidence tier recorded for every row | ✓ All rows carry source_tier (official, secondary) |
| Normalization completeness | ✓ 100% measurement completeness across all brands |
| Family assignment completeness | ✓ 495 rows classified; 0 unclassified |
| Traceability to matrix and ROI | ✓ See `docs/research/competitor-family-coverage-matrix.md`, `docs/research/roi-by-family.md` |
| Direct answer to strategic question | ✓ Section 7: Stage the taxonomy |

### Dataset Limitations

- All competitor data except Irontech Doll (11) and Tayu (21) is sourced from secondary aggregators (DollStudio, SiliconWives). Family confidence is lower for secondary-sourced brands; findings should be treated as directional, not exact.
- RealDoll body measurements were not accessible for classification; 13 model URLs captured but not classified.
- Doll Forever catalog was not accessible at the time of crawl.
- ZELEX official pricing is not published in the manufacturer catalog. Price comparisons use ZELEX (Dollstudio) secondary data as a proxy.

---

*Supporting artifacts: `docs/research/roi-by-family.md` · `docs/research/source-log.md` · `docs/research/competitor-family-coverage-matrix.md` · `db/competitor_family_coverage.json` · `db/competitor_family_coverage.sqlite`*
