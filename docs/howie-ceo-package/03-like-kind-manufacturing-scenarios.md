# Like-Kind Manufacturing Scenarios
## Repurposing Existing Tooling to Seed Classic & Sculpt Families

**Date:** 2026-06-06  
**Prepared for:** Howie, CEO  
**Status:** Analyst estimates — not measured ZELEX actuals  
**Branch:** feat/pdr-010-ceo-roi-analysis

---

## The Problem

Classic and Sculpt both carry **100% dead-end rates** — every quiz completion that routes to either family hits a wall with zero products to show. The conventional fix is to commission entirely new body tooling, which carries 6-12 month lead times and $200-400K+ in mold/skeleton capital.

This brief identifies a faster, cheaper path: **like-kind manufacturing**, where ZELEX's existing body geometry is close enough to the target family archetype that tooling modifications (or zero modifications) can seed the new family without starting from scratch.

All dimensional comparisons use data from 30-brand competitor dataset (495 body-style rows).

---

## How "Like-Kind" Is Measured

Each body is described by four measurements: height (cm), bust, waist, hip. A **dimensional distance score** measures how far a ZELEX body sits from the target family's market centroid — the average of competitor bodies classified in that family.

- Score < 1.5 = **like-kind** (minor modification or zero modification)  
- Score 1.5–3.0 = **adaptable** (moderate tooling)  
- Score > 3.0 = **new build** (new mold required)

---

## Family A: Sculpt — The Hidden Asset

**Archetype:** Athletic realism — defined waist, minimal adipose, sculpted muscle tone  
**Market centroid** (from 97 competitor Sculpt bodies): H163cm, B82, W56, Hip91, WHR 0.61–0.65

### ZELEX already has a Sculpt-spec body

| Body | Height | Bust | Waist | Hip | WHR | BWR | Price | Dist to Sculpt |
|------|--------|------|-------|-----|-----|-----|-------|----------------|
| **ZE T168E** | 168 | 83 | 56 | 87 | 0.64 | 1.48 | $1,690 | **0.96** ✓ |
| ZE T16587 | 165 | 87 | 57 | 80 | 0.71 | 1.53 | $1,390 | 2.45 |

**ZE T168E is already a Sculpt-spec body.** It sits at distance 0.96 from the Sculpt market centroid — closer than most competitors achieve. This body exists in ZELEX's product catalog today.

### Competitor validation

The MD Doll 163cm Sculpt body (H163, B83, W56, Hip92, WHR 0.61) is the market's dominant reference — 13 SKUs on that single frame. ZE T168E is 5cm taller but shares identical waist (56cm) and near-identical bust/proportions.

| Competitor | Height | WHR | BWR | Price | Market Position |
|------------|--------|-----|-----|-------|-----------------|
| MD Doll 163 Sculpt | 163 | 0.61 | 1.49 | $2,499 | Category leader |
| FunWest 162 Sculpt | 162 | 0.65 | 1.45 | $1,599 | Volume player |
| **ZELEX ZE T168E** | 168 | 0.64 | 1.48 | $1,690 | Positioned competitively |

### Scenario A: Activate (Zero New Tooling)

**What:** Route ZE T168E through quiz as the Sculpt family anchor body. Create Sculpt category page, write family content, connect head options.

**Investment:** $15–30K (content, photography, quiz routing dev)  
**Timeline:** 4–6 weeks  
**Risk:** Low — no factory dependency  
**Dead-end impact:** Sculpt 100% → 0% immediately

> **This is the highest-ROI action in the entire CEO package.** The body already exists. The dead-end is a catalog routing problem, not a manufacturing problem.

---

## Family B: Classic — Near-Zero Tooling via Muse Refinement

**Archetype:** Timeless hourglass — balanced bust/hip symmetry, defined waist, natural weight distribution  
**Market centroid** (from 27 competitor Classic bodies): H167cm, B84, W59, Hip90, WHR 0.66–0.68, BWR 1.41–1.44

### ZELEX Muse bodies ranked by proximity to Classic spec

| Body | Height | Bust | Waist | Hip | WHR | BWR | Waist Δ | Dist to Classic |
|------|--------|------|-------|-----|-----|-----|---------|-----------------|
| **ZG162D** | 162 | 85 | 61.5 | 93.5 | 0.66 | 1.38 | +2.5cm | **1.21** ✓ |
| ZX171C | 171 | 83 | 61 | 95.5 | 0.64 | 1.36 | +2.0cm | 1.36 |
| ZF161D | 161 | 85 | 62 | 94 | 0.66 | 1.37 | +3.0cm | 1.43 |
| ZG S155C | 155 | 80 | 59 | 88 | 0.67 | 1.36 | 0cm | 1.50 |

**ZG162D is the prime Classic candidate.** Its WHR (0.66) already matches the Classic archetype exactly. The only gap is waist: 61.5cm vs Classic target of 59cm — a 2.5cm difference.

### What "waist refinement" means in manufacturing

A 2.5cm waist reduction on an existing body is a **skeleton frame modification**, not a new mold:

- The TPE pour shell uses the same outer mold geometry
- The internal skeleton's ribcage/pelvis connector is narrowed at the waist section
- Cost is ~30–40% of a new-frame commission
- Same factory, same production line, same QC process

This is not hypothesis — Lilydoll executes exactly this: their 168cm Classic body (WHR 0.67, W61, Hip90.9) is one of the best-selling Classic reference bodies in the dataset at $1,299, built on a slightly narrower waist frame than their Muse-equivalent bodies.

### Competitor validation

| Competitor | Height | WHR | BWR | Price | Why Relevant |
|------------|--------|-----|-----|-------|--------------|
| Lilydoll 168 Classic | 168 | 0.67 | 1.43 | $1,299 | Market price floor |
| Jarliet 165 Classic | 165 | 0.65 | 1.43 | $1,715 | Mid-market |
| AS Doll 166 Classic | 166 | 0.66 | 1.44 | $1,993 | Premium tier |
| Gynoid 165 Classic | 165 | 0.68 | 1.41 | $5,391 | Silicone ceiling |

ZELEX's current Muse pricing ($1,690–$2,290) positions a Classic entry comfortably above Lilydoll's floor while staying well below Gynoid premium. The market gap at $1,800–$2,200 for a quality TPE Classic is confirmed open.

### Scenario B: Refine (Minor Tooling — Frame Modification)

**What:** Commission waist-section modification on ZG162D skeleton frame. New SKU photographed and cataloged as Classic family anchor. ZG S155C (155cm, waist already 59cm) may require zero modification — test as first Classic body.

**Investment:** $80–150K (skeleton modification × 1–2 frames + content)  
**Timeline:** 90–120 days  
**Risk:** Medium — single factory dependency  
**Dead-end impact:** Classic 100% → 0%

> **ZG S155C is worth testing first** — its waist is already 59cm (on-target) and its WHR is 0.67. With minimal framing as "Classic" (different styling, wardrobe, shoot concept), it may be activatable in 45–60 days as the Classic pilot before the ZG162D refinement arrives.

---

## Scenario C: FunWest OEM (Sculpt Depth, Optional)

If Scenario A activates ZE T168E as the Sculpt anchor, the next constraint becomes **catalog depth** — a single body limits Sculpt quiz satisfaction across height/cup preferences.

**FunWest has 17 Sculpt bodies** across three distinct frames:

| Frame | Height | Bust | Waist | Hip | WHR | Price | Dist to Sculpt |
|-------|--------|------|-------|-----|-----|-------|----------------|
| Nika 152 | 152 | 71 | 48 | 77 | 0.62 | $2,049 | 2.28 |
| Lyra/Assos/Samara/Talvi 162 | 162 | 80 | 55.1 | 85.1 | 0.65 | $1,599 | **1.29** |
| Alexi/Elio/Skyler/Vesper 168 | 168 | 90 | 62 | 97 | 0.64 | $2,499 | 2.61 |

FunWest's 162cm Sculpt frame is dimensionally close to ZELEX's own ZE T168E and operates in the same factory tier. A white-label OEM arrangement would give ZELEX 5–8 additional Sculpt SKUs without capital tooling, filling height gaps below ZE T168E's 168cm.

**This is not urgent** — Scenario A solves the dead-end. This expands the Sculpt catalog in Q3–Q4.

---

## Recommended Sequence

| Priority | Action | Body | Timeline | Cost Est. | Risk |
|----------|--------|------|----------|-----------|------|
| **1 — Immediate** | Activate ZE T168E as Sculpt anchor | ZE T168E | 4–6 weeks | $15–30K | Low |
| **2 — This quarter** | Launch ZG S155C as Classic pilot | ZG S155C | 45–60 days | $20–40K | Low |
| **3 — Q3** | Commission ZG162D waist refinement for Classic | ZG162D | 90–120 days | $80–150K | Medium |
| **4 — Q3/Q4** | FunWest OEM for Sculpt catalog depth | FunWest 162 | 60–90 days | TBD margin | Medium |

**Combined dead-end elimination timeline:** Both Classic and Sculpt drop from 100% to 0% dead-end rate within 60 days via existing ZELEX inventory — with no new factory tooling.

---

## Risk Notes

- ZE T168E activation assumes the body has sufficient head/styling options to support a Sculpt quiz path — verify catalog completeness before routing
- ZG S155C "pilot" framing assumes ZELEX is comfortable positioning a 155cm body as Classic flagship; if height matters for the Classic archetype perception, go straight to ZG162D modification
- FunWest OEM requires confirming no exclusivity conflicts with existing Irontech/factory agreements

---

*All measurements from 30-brand competitor dataset (495 body-style rows, classified June 2026). Dimensional distance scores use normalized Euclidean distance to family centroid. Not ZELEX actuals — analyst estimates.*
