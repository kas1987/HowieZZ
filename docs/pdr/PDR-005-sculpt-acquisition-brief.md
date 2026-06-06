# PDR-005: The Sculpt — Acquisition Brief

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-05  
**Status:** Draft — Pending CEO Review

---

## Decision

**Commission one hero Sculpt body for the next production cycle.**

ZELEX is the only Catalog Depth Leader in the 30-brand competitive matrix with zero Sculpt bodies — a family now present in 20 of 30 catalogues surveyed and owned at volume by MD Doll (37 bodies at $2,599). The silicone-first mid-premium corridor ($2,000–$2,700) remains structurally unoccupied. A single hero body at WHR 0.67 / BWR 1.50, 165 cm, silicone, priced at $2,099 — paired with two named character skins on debut — closes the coverage gap, activates the in-development Sculpt taxonomy status, and gives the discovery quiz its first Sculpt routing destination. Do not attempt a volume build before the demand signal is confirmed from a single hero entry.

---

## 1. Market Signal

Across 30 brands and 495 classified body-style rows, The Sculpt is the second-most-represented family in competitor catalogues by raw SKU count. The market has reached independent convergence on this silhouette: 20 brands across volume, mid-market, and premium tiers carry at least one body with WHR 0.65–0.68 and BWR 1.45–1.55 — the measurement window ZELEX defines as The Sculpt.

**Volume is concentrated at the mid-tier in TPE:**

| Brand | Sculpt bodies | Sculpt share | Material | Median price |
|---|---:|---:|---|---:|
| MD Doll | 37 | 53.6% | Mixed (silicone 33%) | $2,599 |
| FunWest | 17 | 16.0% | Mixed (silicone 46%) | $1,599 |
| Tayu | 5 | 23.8% | Silicone 86% | $3,800 |
| Lusandy Doll | 5 | 14.3% | Silicone 83% | $2,699 |
| Gynoid | 4 | 40.0% | Silicone 100% | $5,391 |
| Angel Kiss | 3 | 30.0% | Silicone 100% | $2,390 |
| XT Doll | 3 | 30.0% | Silicone 100% | $2,190 |
| YL Doll | 3 | 30.0% | Mixed (silicone 20%) | $1,740 |
| 6YE Premium | 3 | 30.0% | TPE 100% | $1,490 |

Nine additional brands carry 1–2 Sculpt bodies each: AS Doll, Dime Doll, Game Lady, Irokebijin, Jiusheng, JY Doll, Lilydoll, Piper Doll, SE Doll, SM Doll, Sanhui.

**Taxonomy note.** "The Sculpt" is a ZELEX internal classification applied retroactively to competitor measurements. Competitors do not use a shared label — MD Doll presents these as fitness or athletic body variants; Gynoid markets them under its broader realism positioning. The convergence of 20 brands arriving at bodies within this measurement window independently is the signal, not the terminology.

**Pricing structure.** The volume leader (MD Doll, 37 bodies at $2,599 median) and mass-market providers (FunWest $1,599, 6YE $1,490) serve the segment at meaningfully different price points. The boutique-silicone segment — Gynoid ($5,391), Tayu ($3,800) — validates that material quality commands a significant premium. The mid-premium corridor ($2,000–$2,700) in silicone is structurally underserved by brands with ZELEX's catalogue depth and character architecture.

---

## 2. ZELEX Gap Analysis

**Current state:** 0 Sculpt bodies. The family is marked `"status": "in_development"` with `"member_count": 0` in `db/family_taxonomy.json`. The ZELEX (Dollstudio) secondary catalog also shows 0 Sculpt bodies. No character slots in `db/characters.json` are assigned to The Sculpt family.

**Coverage matrix position:**
- ZELEX official: 19 bodies classified. Sculpt count: 0.
- Top-2 concentration (Muse + Icon): 84.2% — the highest concentration of any brand in the matrix.
- Every other Catalog Depth Leader in the dataset — FunWest, Irontech, SE Doll, WM Doll — covers the Sculpt family. ZELEX is the sole exception.

**Quiz dead-end.** A buyer who arrives at ZELEX's discovery quiz having self-identified as wanting athletic, defined proportions — the buyer MD Doll and Gynoid are actively serving — currently hits a dead end. The quiz routing has no Sculpt destination. They leave.

**Family descriptor is live.** The site already carries the Sculpt family descriptor ("Muscular definition — athletic, defined geometry built for precision") in the taxonomy and design system. The family infrastructure exists; the product does not.

---

## 3. Competitive Pricing Landscape

### Silicone Sculpt corridor

| Brand | Sculpt bodies | Silicone share | Price range | Positioning |
|---|---:|---:|---|---|
| Gynoid | 4 | 100% | $4,401–$7,038 | Ultra-premium artisan |
| Tayu | 5 | 86% | ~$3,800 median | Premium-official tier |
| Lusandy Doll | 5 | 83% | $2,599–$2,699 | Near-premium silicone |
| Angel Kiss | 3 | 100% | ~$2,390 | Mid-market silicone |
| XT Doll | 3 | 100% | ~$2,190 | Mid-market silicone |
| MD Doll | 37 | 33% | $1,674–$2,599 | Volume, mixed material |

**The $2,000–$2,700 silicone window** is occupied at its upper end by Lusandy ($2,699) and partially by MD Doll's few silicone variants ($2,599), but neither brand pairs the silhouette with a named-character architecture, quiz routing, or official measurement documentation. The window is open for a positioned entry.

**TPE reference tier:**
FunWest (17 bodies, $1,599 median) and 6YE ($1,490) define the commodity floor. A ZELEX silicone Sculpt at $2,099 commands a ~$500 material premium over FunWest and sits $500 below Lusandy's silicone ceiling — defensible in the mid-premium band.

---

## 4. Entry Specification

**Source of truth:** `db/family_taxonomy.json` — The Sculpt: WHR 0.65–0.68, BWR 1.45–1.55.

| Axis | Target | Range | Notes |
|---|---|---|---|
| WHR | 0.67 | 0.65–0.68 | Centre of range; unambiguous classification, no border risk |
| BWR | 1.50 | 1.45–1.55 | Mid-range; clear separation from Muse (BWR 1.30–1.40) |
| Height | 165 cm | 163–168 cm | Photographs neutrally; avoids height extremes that narrow configurations |
| Cup | D | D minimum | Proportional credibility at WHR 0.67 |
| Material | Silicone | Mandatory | TPE cannot render the surface detail that defines the family |

**WHR–Muse boundary.** The Sculpt and Muse share the same WHR lower bound (0.65) but diverge on BWR: Muse sits at BWR 1.30–1.40; Sculpt at 1.45–1.55. A body at WHR 0.66 / BWR 1.35 lands in Muse. The same WHR at BWR 1.48 lands in Sculpt. The distinction is real and measurable.

**Surface geometry requirements** (from family brand voice and taxonomy silhouette descriptor):
- Articulated abdominals — visible muscle definition, not smooth belly surface
- Defined deltoids and shoulder musculature
- Sculpted, lifted posterior with visible gluteal separation

These are sculpt-level requirements not derivable from WHR/BWR alone. A body can pass the measurement ranges with a smooth surface and still fail the family entry criteria. Prototype sign-off must include a surface geometry review gated on these three criteria.

---

## 5. Differentiation Strategy

MD Doll's 37-body Sculpt catalogue is a volume play on a single family. It wins on choice; it does not win on character, narrative, or routing intelligence. Its Sculpt bodies are listed as product variants — SKUs to scroll — not personas with backstory, aesthetic context, or quiz-matched entry points.

ZELEX's existing advantage is the named-character architecture: each body is a character with a profile, a skin match, and a quiz pathway. The Sculpt entry should not be "athletic body variant 001." It should be a named character — a persona designed around fitness realism, with a defined visual identity the buyer encounters before they see measurements.

The buyer for a Sculpt body is different from the Muse or Icon buyer in one specific way: **they arrived with a concrete physical idea.** They are not browsing aesthetics; they know they want definition. A quiz that identifies this preference and routes them to a character — rather than a scrollable measurement table — closes the sale that MD Doll's grid leaves open.

The differentiation is not a larger Sculpt catalogue than MD Doll. It is one Sculpt character, launched with ZELEX's full character-skin-quiz treatment, at a price point ($2,099) that the silicone-first mid-premium segment has not yet occupied for this family.

---

## 6. Commercial Translation

### Launch State

| Surface | State at debut |
|---|---|
| Homepage | Not present — no hero or teaser position until 3+ bodies active |
| Quiz | Eligible — Sculpt routing activates with the debut body; quiz can surface one result |
| Compare filter | Active — Sculpt filter visible in compare/browse |
| Landing page | Full depth — `/families/sculpt` exits dev-card status on debut day |
| SEO priority | P4 — placeholder exists; full SEO activation after 2+ bodies |
| Character badge | Yes — debut character carries Sculpt family badge |

### Quiz Routing

The Sculpt quiz path targets buyers who select preferences mapping to: athletic build, visible muscle definition, fitness-aesthetic appeal. With one body, the quiz returns a single result — acceptable for launch. The result page surfaces the debut character with full specs, measurement documentation, and the "why this body" narrative.

### Inquiry Tag

| Family | Tag | Routing |
|---|---|---|
| The Sculpt | `body:sculpt` | Route to fitness-realism persona funnel; separate from Muse/Icon inquiry flow |

### Pricing

| Target retail | Band | Rationale |
|---|---|---|
| $2,099 | $2,000–$2,200 | First silicone Sculpt in this corridor; ~$500 above FunWest TPE; $500 below Lusandy silicone ceiling |

**Character slot plan:** 2 character skins at debut, not 4. Launch lean; add remaining 2 slots after demand validation from first 90 days of sales. Character names and skin pairings to be developed alongside the body commission.

---

## 7. Strategic Conclusion

Three findings govern this recommendation:

1. **ZELEX is the only Catalog Depth Leader absent from the Sculpt family.** The structural gap is not a niche oversight — it is the one family where every peer with ZELEX's catalogue depth has committed SKU depth and ZELEX has zero. The quiz dead-end is an active revenue leak for buyers who self-identify as wanting athletic geometry.

2. **The silicone mid-premium corridor ($2,000–$2,700) is open.** MD Doll dominates Sculpt by volume but at mixed-material quality ($2,599, 33% silicone). Gynoid serves the ultra-premium at $4,401+. No brand owns silicone Sculpt in the accessible premium band with a named-character and quiz-routing architecture. A single positioned entry at $2,099 captures this lane before a competitor does.

3. **One character is the right launch scale.** Volume parity with MD Doll (37 bodies) is not the goal. The goal is a quiz destination, a landing page that exits dev-card status, and one silicone Sculpt character who embodies the family narrative at ZELEX's quality tier. Demand validation from 90 days of active sales informs whether to expand.

**Recommended action:** Commission one hero Sculpt body at WHR 0.67 / BWR 1.50, 165 cm, D cup, silicone. Surface-review prototype against articulated abs / defined deltoid / sculpted glute criteria before production sign-off. Debut at $2,099 with 2 character skins. Activate quiz routing and compare filter on launch day. Revisit homepage treatment when 3+ Sculpt bodies are active.

---

## 8. Acceptance Review

| Criterion | Status |
|---|---|
| Market signal documented (competitor Sculpt coverage ≥10 brands) | ✓ 20/30 brands |
| ZELEX gap confirmed against official taxonomy | ✓ 0 bodies, in_development status |
| Competitive pricing landscape with silicone/TPE split | ✓ Section 3 |
| Entry specification with WHR/BWR targets and surface criteria | ✓ Section 4 |
| Differentiation angle vs volume leader (MD Doll) | ✓ Section 5 |
| Commercial translation: quiz, landing page, pricing, character plan | ✓ Section 6 |
| Price recommendation with competitive justification | ✓ $2,099 — Section 6 |
| Direct answer to acquisition question | ✓ Decision: one hero body |

### Dataset Limitations

- All competitor Sculpt data except Tayu (official, 21 profiles) is sourced from secondary aggregators (DollStudio, SiliconWives). Sculpt body counts for secondary-sourced brands should be treated as directional.
- MD Doll's 33% silicone share is unexpectedly low given its positioning; actual silicone-only Sculpt body count may differ from the 37 classified rows.
- ZELEX official pricing is not published in the manufacturer catalog. Price comparisons use ZELEX Dollstudio secondary data as a proxy.

---

*Supporting artifacts: `docs/research/competitor-family-coverage-matrix.md` · `docs/research/roi-by-family.md` · `db/competitor_family_coverage.json` · `db/family_taxonomy.json`*
