# Manufacturing Intelligence Matrix
## A Pull-Based Production Framework for ZELEX's 6-Family Lineup

**Date:** 2026-06-06  
**Prepared for:** Howie, CEO  
**Status:** Strategic framework — analyst estimates, not ZELEX actuals  
**Branch:** feat/pdr-010-ceo-roi-analysis

---

## The Problem with Make-to-Order

ZELEX's current production model is almost entirely make-to-order: a customer places an order, a work order is generated, and the factory starts cold. This produces 8–12 week lead times, uneven factory utilization, and no structural advantage for ZELEX's most predictable demand — the SKUs that account for the majority of quiz completions and repeat buyer segments.

The conventional fix is to pre-build finished inventory, but that creates a different problem: incorrect SKUs, skin tone mismatches, head combinations that don't move, and capital locked in unsold stock.

The third path — the one this brief describes — is **Build-to-Stage**: pre-position the right sub-assemblies based on demand signals, not finished products based on guesses. The factory is never starting cold; it's completing the last steps of a body that's already 40–60% built.

This only works if the signal layer is precise enough to know *which* sub-assemblies to stage. That precision comes from market intelligence — and ZELEX already has most of it.

---

## The Foundation: What the Data Already Tells Us

The competitor analysis database (30 brands, 495 body-style rows, classified June 2026) produces three outputs that function as manufacturing inputs, not just market research:

### 1. Family Centroids → Frame Specification Targets

Each family centroid (height, bust, waist, hip averages across all competitor bodies in that family) defines the geometry of a frame that would serve that family's market. These are not aspirational — they are derived from what the market has already validated commercially.

| Family | Target Frame Spec | Market Validation |
|--------|------------------|-------------------|
| Classic | H161, B83, W58, Hip87 | 27 competitor bodies, $1,299–$5,391 range |
| Sculpt | H158, B82, W56, Hip89 | 97 competitor bodies, category leader MD Doll 163 |
| Icon | H157, B83, W55, Hip94 | 108 competitor bodies, largest single family by count |
| Empress | H160, B87, W55, Hip93 | 46 competitor bodies, premium tier concentration |
| Muse | H160, B79, W60, Hip92 | 172 competitor bodies, ZELEX's home territory |
| Siren | H156, B88, W50, Hip87 | 45 competitor bodies, extreme BWR segment |

These specs are not estimates of what might work — they are the market's revealed preference. A frame built to these specs is entering a proven geometry.

### 2. Dimensional Distance Scores → Which Existing Inventory Is Transferable

The distance score for each ZELEX body against each family centroid tells the factory which existing skeleton frames can serve multiple families with minor or zero modification. This eliminates the need to commission a new mold for every family activation.

Key transferable frames (distance < 1.5 = like-kind, usable now):

| ZELEX Frame | Classic | Sculpt | Muse | Icon | Empress | Status |
|-------------|---------|--------|------|------|---------|--------|
| ZG S155C | **0.90** | **1.16** | 1.04 | — | — | Pre-stage for Classic/Sculpt 155cm |
| ZE T168E | **1.00** | **1.05** | — | — | — | Pre-stage for Sculpt/Classic 168cm |
| ZX163E | **1.15** | **1.32** | 1.38 | 1.41 | **1.27** | Cross-route for 4 families at 163cm |

This is the factory equivalent of shared tooling: one production line, multiple output families.

### 3. Market Coverage Gaps by Height Band → Demand Probability Weights

ZELEX's market share vs. the full competitor field, broken out by height band, gives a prior probability for where unmet demand is concentrated:

| Height Band | Classic | Sculpt | Icon | Empress | Muse | Siren |
|-------------|---------|--------|------|---------|------|-------|
| 150–159cm | **0%** | **0%** | 2% | **0%** | 4% | **0%** |
| 160–164cm | **0%** | **0%** | 6% | 5% | 12% | — |
| 165–169cm | **0%** | 5% | 20% | — | 18% | — |
| 170cm+ | **0%** | — | 33% | — | 24% | — |

Gaps = demand that is going to competitors. Gaps in a band where ZELEX *does* have frames suggest a routing or catalog problem. Gaps in bands where ZELEX has *no* frames are hard manufacturing gaps — the factory has nothing to stage.

---

## The Matrix Architecture

The Manufacturing Intelligence Matrix maps three dimensions:

```
Family (6)  ×  Component Layer (4)  ×  Demand Confidence Tier (3)
```

### Dimension 1 — The 6 Families (demand categories)

Each family represents a distinct buyer archetype. Quiz completions, cart adds, and order history are family-level signals — a Sculpt buyer doesn't convert to Muse inventory.

### Dimension 2 — The 4 Component Layers (production stages)

Every doll moves through four discrete production stages. Build-to-Stage works by advancing inventory as far through these stages as the demand signal justifies:

| Layer | Component | Family Specificity | Pre-Stage Cost | Notes |
|-------|-----------|-------------------|----------------|-------|
| **L1 — Skeleton Frame** | Internal armature, joint assembly | Family-specific (geometry locked here) | Low — frames are compact, long shelf life | First and most critical pre-stage point |
| **L2 — TPE Pour Shell** | Body silicone/TPE cast over frame | Frame-specific (height/weight class) | Medium — poured and cured, shape locked | Can queue before customer skin tone choice |
| **L3 — Skin Tone Finish** | Pigmentation pass, surface texture | Customer-configurable | High — skin tone is a personalization variable | Stage only after order confirmation |
| **L4 — Head + Assembly** | Head attachment, eye install, quality check | Customer-configurable (head choice) | Highest — customer selection | Never pre-stage: personalization completes here |

**The pre-stage decision:** L1 and L2 can be queued before an order exists if demand confidence is high. L3 and L4 should only proceed post-order. This collapses lead time from 8–12 weeks (starting from L1) to 2–3 weeks (completing from L3 or L4 only).

### Dimension 3 — The 3 Demand Confidence Tiers

| Tier | Signal Basis | Pre-Stage Depth | Current Data Source |
|------|-------------|----------------|-------------------|
| **Tier 1 — High Confidence** | Historical order velocity for this family+height band, quiz completion rate | Pre-stage L1 + L2 (frame + pour ready) | Market gap analysis + quiz routing data |
| **Tier 2 — Medium Confidence** | Quiz completions trending, wishlist/cart adds, seasonal patterns | Pre-stage L1 only (frame queued, pour on order trigger) | Quiz analytics, cart data |
| **Tier 3 — Low Confidence** | New family launch, untested SKU, low historical velocity | Make-to-order from L1 (no pre-stage, but frame spec is known) | Market centroid estimate only |

---

## The Work Order Flow

With the matrix in place, a demand signal generates a structured work order rather than an unstructured factory request. The flow:

```
Demand Signal
    │
    ├─ Signal type: quiz completion → map to family + height band
    ├─ Signal type: cart add → map to specific SKU
    ├─ Signal type: confirmed order → trigger L3 + L4 queue
    │
    ▼
Matrix lookup: [Family] × [Height Band] → Confidence Tier
    │
    ├─ Tier 1 → Release L1 + L2 work order to factory queue
    ├─ Tier 2 → Release L1 work order; flag L2 for trigger
    └─ Tier 3 → Record signal; accumulate toward Tier 2 threshold
    │
    ▼
Factory receives: Component spec (frame geometry from centroid),
                  Quantity, Target completion window,
                  Skin tone / head deferred (awaits customer order)
    │
    ▼
Customer Order Arrives
    │
    ├─ L1/L2 already staged → Release L3 work order (skin tone)
    ├─ Head selected → Release L4 assembly
    └─ Ship in 2–3 weeks instead of 8–12
```

---

## What the Current Data Enables vs. What It Doesn't

The market intelligence database is sufficient to populate the matrix's structural layer. Here is an honest accounting of what it covers and where gaps remain:

### Enabled now by market data:

- **Frame specification targets** for all 6 families (from family centroids)
- **Like-kind routing decisions** — which existing ZELEX frames serve multiple families (from dimensional distance scores)
- **Height-band demand weights** — where market gaps indicate highest unmet demand
- **Bridge frame geometry** — which single new frame investment serves multiple family dead-ends
- **Component layer architecture** — the L1–L4 model applies regardless of demand data

### Requires customer/order data to sharpen:

- **Tier assignment per SKU** — current assignment is market-estimate-based. Actual order history by family+height band would replace estimates with measured velocity
- **Quiz completion → purchase conversion rate** — needed to weight quiz signals correctly (a family with high quiz completions but low conversion produces false Tier 1 signals)
- **Seasonal demand curves** — which families over-index by season (Muse in summer vs. Empress in winter, hypothetically)
- **Head-body co-selection patterns** — which heads are ordered with which bodies at high frequency enables L4 pre-positioning at scale

### The data maturity path:

| Phase | Data Available | Matrix Precision |
|-------|---------------|-----------------|
| **Now** | Competitor market intelligence + quiz routing estimates | Tier assignments estimated; frame specs accurate; bridge routing validated |
| **3–6 months post-launch** | ZELEX order history by family, quiz completion data | Tier assignments measured; conversion rates known |
| **12+ months** | Seasonal curves, head-body co-selection, repeat buyer patterns | Full matrix calibration; predictive work order generation |

The matrix is functional at Phase 1 with analyst estimates. It becomes predictive at Phase 2 when ZELEX's own sales data replaces competitor proxies.

---

## Priority Pre-Stage Actions (Phase 1, Now)

Based on current market data and dimensional distance analysis, three immediate pre-stage targets have the highest demand confidence:

| Family | Height | Frame | Tier | Basis | Action |
|--------|--------|-------|------|-------|--------|
| Sculpt | 165–169cm | ZE T168E (existing) | **Tier 1** | ZE T168E is already in catalog; zero new tooling; Sculpt centroid distance 1.05 | Stage L1+L2 inventory now; route quiz |
| Classic | 150–159cm | ZG S155C (existing) | **Tier 1** | WHR 0.66, waist 59cm on-target; Classic centroid distance 0.90; zero tooling | Stage L1+L2; route as Classic pilot |
| Classic+Sculpt | 158–162cm | Convergence Frame (new) | **Tier 2** | Market gap confirmed in both families at this height band; bridge geometry validated by Gynoid GT 160 comp | Commission frame; pre-stage L1 on delivery |

The two Tier 1 actions require no factory work — the frames exist. The pre-stage investment is in finished body inventory at L2, sized to expected quarterly demand.

---

## What This Unlocks at Scale

A fully calibrated Manufacturing Intelligence Matrix changes ZELEX's competitive position in a specific way: **lead time becomes a product feature.**

The current 8–12 week industry standard is structural — most competitors are in the same make-to-order position. A ZELEX that ships Tier 1 SKUs in 2–3 weeks captures buyers who decide at the point of comparison, not after waiting 10 weeks to see how the competitor's product actually arrives.

The data infrastructure to build this is already partially in place. The family centroids are calculated. The distance scores are computed. The market gap coverage map exists. The next layer — order velocity and quiz conversion — turns on when the product catalog is active and customers start generating signal.

The matrix is not a future-state aspiration. It is the next-level use of the intelligence already built.

---

*Market centroids and dimensional distances from 30-brand competitor dataset (495 body-style rows, classified June 2026). Lead time estimates are analyst assumptions based on industry benchmarks. Not ZELEX actuals.*
