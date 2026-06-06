# PDR-005 — The Sculpt: Acquisition Brief

**Status:** Draft · **Date:** 2026-06-05 · **Author:** Product

---

## Executive Summary

ZELEX is the only Catalog Depth Leader in the 30-brand matrix with zero Sculpt bodies — a family now present in 20 of 30 catalogues surveyed and led by MD Doll with 37 entries. The gap is not a niche oversight; it is a structural absence that routes buyers seeking athletic, defined proportions to competitors who have already committed the SKU depth. This brief makes the case for a single, precisely specified hero Sculpt body as ZELEX's first entry, positioned at the premium end of a market that has largely served the segment with lower-cost TPE products.

---

## Market Signal

Across 30 brands and 495 classified body-style rows, The Sculpt family is the second-most-represented family in competitor catalogues by raw SKU count, driven almost entirely by MD Doll:

| Brand | Sculpt bodies | Sculpt share of catalogue | Material | Median price |
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

**Taxonomy note.** "The Sculpt" is a ZELEX internal classification applied retroactively to competitor measurements. Competitors do not use a shared "Sculpt" label — MD Doll presents these as fitness or athletic body variants; Gynoid markets them under its broader realism positioning. The classification is measurement-driven (WHR 0.65–0.68, BWR 1.45–1.55), not a label competitors themselves promote. The convergence of 20 brands arriving at bodies that fall in this range independently is the signal, not the terminology.

**Price tier observation.** The volume leader in this segment (MD Doll, 37 bodies at $2,599 median) and the mass-market providers (FunWest at $1,599, 6YE at $1,490) serve the segment at meaningfully different price points. The silicone-first, boutique-premium segment — Gynoid ($5,391), Tayu ($3,800) — validates that material quality commands a significant premium in this family. The mid-premium corridor ($2,000–$2,700) in silicone is underserved by brands with ZELEX's catalogue depth.

---

## ZELEX's Gap

The coverage matrix is unambiguous:

- **ZELEX (official): 19 bodies classified. Sculpt count: 0.**
- **ZELEX (Dollstudio): 10 bodies classified. Sculpt count: 0.**
- Family status in `family_taxonomy.json`: `in_development`, 0 members.
- ZELEX's 84.2% top-two concentration (Muse + Icon) is the highest in the matrix — a focused catalogue that is strong where it plays but absent from the athletic/defined segment entirely.

A buyer who arrives at ZELEX's quiz or family page having self-identified as wanting athletic, muscular definition — the buyer Gynoid and MD Doll are actively serving — currently hits a dead end. The quiz routing has no Sculpt destination to send them to. They leave.

ZELEX is classified as a Catalog Depth Leader (156 full-body SKUs, median $1,999). Every other Catalog Depth Leader in the matrix — FunWest, Irontech, SE Doll, WM Doll — covers the Sculpt family. ZELEX is the exception.

---

## Entry Specification

The Sculpt's hard measurement boundaries, as defined in `db/family_taxonomy.json` and surfaced in `family.html`:

| Axis | Floor | Ceiling | Context |
|---|---|---|---|
| WHR | 0.65 | 0.68 | Lower floor than The Muse (0.65–0.70); ceiling 0.02 below Muse ceiling |
| BWR | 1.45 | 1.55 | Above Muse (1.30–1.40); below Icon (1.50–1.60) at the high end |

**WHR–Muse boundary.** The Sculpt and The Muse share the same WHR lower bound (0.65) but diverge immediately on BWR: Muse bodies sit at 1.30–1.40, Sculpt bodies at 1.45–1.55. The visual difference is a slightly fuller bust relative to the waist — athletic torso geometry rather than the long, lean European line. A classifier placing a body at WHR 0.66 / BWR 1.35 lands in Muse. The same WHR at BWR 1.48 lands in Sculpt. The distinction is real and measurable.

**Surface geometry requirements** (from `FAM_META` description and family brand voice):
- Articulated abdominals — visible muscle definition, not smooth belly surface
- Defined deltoids and shoulder musculature
- Sculpted, lifted posterior with visible gluteal separation

These are render/sculpt-level requirements, not derivable from WHR/BWR alone. A body can hit the measurement ranges with a smooth, soft surface and still fail the family entry criteria.

**Height range.** The taxonomy does not set a Sculpt-specific height floor or ceiling. Competitor data spans 150–175 cm for classified Sculpt bodies. An entry at 163–168 cm sits within the ZELEX range (153–175 cm) and avoids the height extremes that narrow buyable configurations.

**Minimum viable entry:**
- WHR: 0.66–0.67 (centre of range, unambiguous classification, no border risk)
- BWR: 1.48–1.52 (mid-range, clear separation from Muse, below Icon overlap)
- Height: 163–168 cm
- Surface: articulated abs, defined deltoid caps, sculpted glutes — sculpt-reviewed at prototype stage
- Material: silicone (mandatory — TPE cannot render the surface detail that defines the family)

---

## Competitive Differentiation Angle

MD Doll's 37-body Sculpt catalogue is a volume play on a single family. It wins on choice; it does not win on character, narrative, or routing intelligence. Its Sculpt bodies are listed as product variants — SKUs to scroll through — not personas with backstory, aesthetic context, or quiz-matched entry points.

ZELEX's existing advantage is the named-character architecture: each body is a character with a profile, a skin match, and a quiz pathway. The Sculpt entry should not be "athletic body variant 001." It should be a named character — a persona designed around fitness realism, with a defined visual identity that the buyer encounters before they see measurements.

This matters because the buyer for a Sculpt body is different from the Muse or Icon buyer in one specific way: they arrived with a concrete physical idea in mind. They are not browsing aesthetics; they know they want definition. A quiz that identifies this preference and routes them to a character — rather than a measurement table — closes the sale that MD Doll's scrollable grid leaves open.

The differentiation is not a larger Sculpt catalogue than MD Doll. It is one Sculpt character, launched with ZELEX's full character-skin-quiz treatment, at a price point ($1,999–$2,199) that the silicone-first mid-premium segment has not yet occupied for this family.

---

## Recommended Next Step

Commission one hero Sculpt body at WHR 0.67 / BWR 1.50, height 165 cm, in silicone, with prototype sculpt review gated on surface geometry criteria (articulated abs, defined deltoids, sculpted glutes). Pair the body with two character skins at launch. Integrate the character into the body quiz as a Sculpt routing destination, making it the first family the quiz can actively close rather than redirect. Target debut price: $2,099.

This single entry closes the gap in the coverage matrix, activates the `in_development` Sculpt taxonomy status, and gives the quiz a destination it currently lacks — without committing to a MD Doll-style volume build before the demand signal is confirmed.
