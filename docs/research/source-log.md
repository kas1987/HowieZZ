# PDR-010 Source Log — Evidence Quality by Brand

**Date:** 2026-06-05  
**Part of:** PDR-010 Competitor Family Coverage and ROI Validation  
**Dataset:** `db/competitor_family_coverage.json`

---

## Overview

| Metric | Value |
|---|---|
| Total classified rows | 495 |
| Brands classified | 30 |
| Brands excluded (no measurement data) | 2 (RealDoll, Doll Forever) |
| Official-source rows | 51 (10.3%) |
| Secondary-source rows | 444 (89.7%) |
| Dataset-wide measurement completeness | 100% |
| Dataset-wide exact+near confidence | ~77% (weighted by row count) |

---

## Tier 1 — Official Manufacturer Sources

Three brands were sourced directly from manufacturer-controlled endpoints. These rows carry `source_tier: "official"`.

---

### ZELEX
**Source:** `local:db/body_profiles.json` (official manufacturer specification database)  
**Profiles:** 19  
**Confidence mix:** exact 7 · near 11 · loose 1  
**Exact+near:** 94.7%  
**Measurement completeness:** 100%  
**Price coverage:** 0% — ZELEX does not publish retail pricing in the official catalog  
**Notes:** The ZELEX baseline is the primary subject of PDR-010, not a competitor row. Sourced from manufacturer specifications, not from a web crawl. The single loose-confidence body (ZX161C) has WHR/BWR values that sit at a family boundary and requires manual confirmation. Pricing is derived separately from ZELEX (Dollstudio) secondary data ($1390–2450) as a proxy.

---

### Irontech Doll
**Source:** `https://irontech.com/` (official manufacturer product pages)  
**Profiles:** 11  
**Confidence mix:** exact 1 · near 5 · manual-review 5  
**Exact+near:** 54.5%  
**Measurement completeness:** 100%  
**Price range:** $2750–3379  
**Notes:** Only official-source competitor brand at ZELEX's price tier. The high manual-review share (45.5%) reflects that Irontech's product pages present measurements in a format that required manual extraction rather than structured parsing. All 11 rows are classified; none are unclassified. Irontech is 81.8% Icon — the most concentrated premium catalog in the dataset. Used as the primary Irontech comparison benchmark in Section 3 (whitespace analysis) and Section 5 (launch hierarchy rationale).

---

### Tayu
**Source:** `https://www.tayu-doll.com/product-sitemap.xml` (official manufacturer sitemap)  
**Profiles:** 21  
**Confidence mix:** exact 6 · near 11 · manual-review 4  
**Exact+near:** 81.0%  
**Measurement completeness:** 100%  
**Price range:** $1980–4700  
**Notes:** Tayu was the only other competitor where official manufacturer data was machine-readable at crawl time. The alternate domain `tayudoll.com` was identified but not successfully integrated; all 21 classified rows come from `tayu-doll.com`. Price range ($1980–4700) places Tayu partially in ZELEX's tier and partially above it. Tayu's catalog is 42.9% Muse + 23.8% Icon (top-2 = 66.7%), with 5 Sculpt bodies (23.8%) — the only official-source brand with material Sculpt representation.

---

## Tier 2 — Secondary Sources: DollStudio Supplier Pages

21 brands were sourced from `us.dollstudio.org/supplier/{brand-slug}` pages. These rows carry `source_tier: "secondary"`. DollStudio is the largest US-market reseller aggregator and carries manufacturer-supplied specs, but measurements may differ from what the manufacturer would publish directly.

| Brand | Profiles | Exact+Near % | Confidence Mix | Price Range (USD) | Notes |
|---|---:|---:|---|---|---|
| 6YE Premium | 10 | 70.0% | exact 3 · near 4 · MR 3 | $1490–1990 | All TPE |
| AS Doll | 10 | 50.0% | exact 1 · near 4 · MR 5 | $1993 (flat) | All TPE; flat pricing unusual — may be single SKU tier |
| Angel Kiss | 10 | 50.0% | exact 1 · near 4 · MR 5 | $2150–2390 | All silicone; 50% confidence is the lowest of any silicone-only brand |
| Game Lady | 6 | 100.0% | exact 1 · near 5 | $2590 (flat) | All silicone; small catalog, high confidence |
| Gynoid | 10 | 100.0% | exact 5 · near 5 | $4401–7038 | All silicone; luxury tier; Classic-dominant (50%) and Sculpt (40%) — the only brand above $4000 in dataset |
| HR Doll | 10 | 60.0% | exact 4 · near 2 · MR 4 | $1390–2190 | Mixed silicone/TPE (90/10) |
| Hitdoll | 5 | 100.0% | exact 1 · near 4 | $1159–1558 | All silicone; small catalog |
| ILdoll | 5 | 100.0% | exact 1 · near 4 | $984–1558 | All silicone; entry price below $1000 on one SKU is notable at silicone quality |
| Irokebijin | 10 | 60.0% | exact 5 · near 1 · MR 4 | $740–2150 | Mixed (70/30 silicone/TPE); Japanese brand; height range 90–160cm suggests compact/torso products included |
| JK Doll | 4 | 75.0% | near 3 · MR 1 | $1699 (flat) | All TPE; small catalog; no exact confidence rows |
| JY Doll | 10 | 80.0% | exact 1 · near 7 · MR 2 | $1390–2390 | Mixed (60/40 silicone/TPE); Siren-dominant (50%) — the clearest mid-market Siren signal in the dataset |
| Jarliet | 10 | 100.0% | exact 1 · near 9 | $1401–1715 | All TPE; excellent confidence |
| Jiusheng | 8 | 37.5% | near 3 · MR 5 | $1490–2890 | All silicone; lowest exact+near of any brand in dataset; 62.5% manual-review means family assignments are directional only |
| Piper Doll | 10 | 70.0% | exact 4 · near 3 · MR 3 | $790–3090 | Mixed (90/10 silicone/TPE); wide price range; height 100–155cm confirms compact products included |
| Real Lady | 4 | 100.0% | exact 2 · near 2 | $2860–2990 | All silicone; small high-confidence catalog; Empress-dominant (50%) |
| SE Doll | 10 | 80.0% | exact 4 · near 4 · MR 2 | $1511–2990 | Mixed (20/80 silicone/TPE); wide price range |
| SM Doll | 10 | 70.0% | exact 3 · near 4 · MR 3 | $1473–2283 | All TPE |
| WM Doll | 10 | 80.0% | exact 5 · near 3 · MR 2 | $1390–1799 | All TPE |
| XT Doll | 10 | 90.0% | exact 4 · near 5 · MR 1 | $1649–2390 | All silicone |
| YL Doll | 10 | 70.0% | exact 2 · near 5 · MR 3 | $1230–2590 | Mixed (20/80 silicone/TPE); Siren-dominant (50% Siren + 30% Sculpt) |
| ZELEX (Dollstudio) | 10 | 100.0% | exact 6 · near 4 | $1390–2450 | Secondary proxy for ZELEX pricing; used as price reference since official ZELEX pricing is unpublished; 70% silicone, 30% TPE — the secondary catalog does not perfectly mirror official body specs |

*MR = manual-review.*

---

## Tier 3 — Secondary Sources: SiliconWives Collection Pages

Six brands were sourced from `siliconwives.com/collections/{brand-collection}/products.json`. These rows carry `source_tier: "secondary"`. SiliconWives is a US-market reseller with structured product JSON endpoints; measurement data is reseller-entered and may lag the manufacturer catalog.

| Brand | Profiles | Exact+Near % | Confidence Mix | Price Range (USD) | Notes |
|---|---:|---:|---|---|---|
| Dime Doll | 31 | 58.1% | exact 1 · near 17 · MR 13 | $1399–1799 | All silicone; depth leader for Muse (21/31); 42% manual-review rate reflects formatting variation in SiliconWives entries |
| FunWest | 106 | 78.3% | exact 11 · near 72 · MR 23 | $1299–2499 | Mixed (46/54 silicone/TPE); largest catalog in dataset; Icon (40) + Muse (38) dominate; most direct mid-market analog to ZELEX Icon/Muse positioning |
| Lilydoll | 14 | 100.0% | exact 5 · near 9 | $1199–1299 | Hybrid material; Classic-dominant (42.9%) and Empress (35.7%); lowest price point in dataset for Classic bodies |
| Lusandy Doll | 35 | 100.0% | near 35 | $2599–2699 | Mixed (83% silicone); Icon (10) + Muse (20) + Sculpt (5); all 35 rows are near-confidence with zero exact — measurement rounding is systematic across the catalog |
| MD Doll | 69 | 72.5% | exact 40 · near 10 · MR 19 | $1674–2599 | Second-largest catalog; Sculpt-dominant (53.6%); 37 Sculpt bodies is the highest single-family count of any brand; only 33.3% silicone despite being classified silicone — material field reflects stated product not independently verified |
| Sanhui | 7 | 85.7% | exact 4 · near 2 · MR 1 | $2499–3199 | All silicone; premium-silicone tier; Icon-dominant (42.9%); Sanhui's official site (sanhuidoll.com) was not integrated — SiliconWives data may be incomplete |

---

## Excluded / Partially Available Brands

### RealDoll
**Status:** Inventory-only — 0 classified profiles  
**Source attempted:** `https://www.realdoll.com/product-sitemap.xml`  
**Profiles found:** 13 model URLs captured (Olivia, Quinn, Harmony robot, Serenity robot, Solana robot, Tanya robot, Stephanie, Tanya, plus 5 non-full-body accessories)  
**Reason for exclusion:** RealDoll product pages do not expose consistent bust/waist/hip measurements. Proportional ratios (WHR, BWR) required for family classification cannot be derived. All 13 URLs are logged in `competitor_family_coverage.json` under `inventory_only`.  
**Impact:** RealDoll is not included in the 29-brand competitive count. The family penetration percentages and market concentration statistics in PDR-010 are computed without RealDoll. If RealDoll measurements were available, the premium-silicone Icon/Muse counts would likely increase.

### Doll Forever
**Status:** Pending source — 0 classified profiles  
**Source attempted:** `https://www.dollforever.com/`  
**Reason for exclusion:** No stable machine-readable body-style catalogue endpoint was integrated at the time of data collection.  
**Impact:** Not included in brand counts or penetration percentages.

---

## Data Quality Notes

**Manual-review confidence caveat.** Rows with `family_confidence: "manual-review"` represent cases where WHR and BWR values fell at a family boundary (within ±0.02 of the threshold) or where measurement completeness was marginal (missing one of hip/waist/bust). These rows are included in the classification but their family assignment has higher uncertainty than exact or near rows. Brands with >40% manual-review rate: AS Doll (50%), Angel Kiss (50%), Jiusheng (62.5%), Dime Doll (42%). Family counts for these brands should be treated as directional.

**Lusandy all-near caveat.** All 35 Lusandy Doll rows have `family_confidence: "near"` with zero exact — measurements appear to be systematically rounded to the nearest 5cm across all body dimensions. This is consistent with a reseller catalog that reports approximated rather than precise manufacturer specs. Lusandy's family distribution (57% Muse, 29% Icon, 14% Sculpt) is likely reliable at the family level but individual body assignments may shift if exact measurements become available.

**Pricing field.** All price data is retail USD at time of crawl (2026-06-05). Brand pricing changes frequently; price bands used in the PDR-010 analysis should be treated as directional. ZELEX official pricing is entirely absent from the dataset; the ZELEX (Dollstudio) secondary row ($1390–2450) is used as a proxy.

**Material field.** Material data reflects the string as presented in the source (e.g. "Silicone", "silicone", "hybrid", "TPE"). Normalization was not applied. "Hybrid" in Lilydoll and Lusandy indicates a silicone-head-TPE-body construction common in the $1200–1800 tier. MD Doll's 33.3% silicone share is unexpectedly low given its positioning; this may reflect TPE body variants within listed SKUs rather than a silicone-only catalog.

**Tayu dual-domain.** Tayu operates two domains: `tayu-doll.com` (classified, 21 official profiles) and `tayudoll.com` (alternate, not yet integrated). Both appear to be official manufacturer properties. The `tayudoll.com` endpoint is listed in `unavailable_competitors` as pending integration. The two domains may carry different or overlapping catalogs; the 21 classified profiles from `tayu-doll.com` should be treated as a partial view.

**Sanhui official site not integrated.** The SiliconWives endpoint for Sanhui yielded 7 profiles. The official Sanhui manufacturer site (`sanhuidoll.com`) was identified but not integrated. The official catalog may be larger or different from what SiliconWives carries.

---

## Source Coverage by Tier — Summary

| Source | Type | Brands | Profiles | % of Total |
|---|---|---:|---:|---:|
| Local ZELEX body database | Official | 1 | 19 | 3.8% |
| tayu-doll.com sitemap | Official | 1 | 21 | 4.2% |
| Irontech manufacturer pages | Official | 1 | 11 | 2.2% |
| us.dollstudio.org supplier pages | Secondary | 21 | 182 | 36.8% |
| siliconwives.com collection pages | Secondary | 6 | 262 | 52.9% |
| **Total classified** | | **30** | **495** | **100%** |
| realdoll.com sitemap | Inventory-only | 1 | 0 | — |
| dollforever.com | Not integrated | 1 | 0 | — |

---

*Generated for PDR-010. Raw data in `db/competitor_family_coverage.json`. Family assignments in `db/family_taxonomy.json`. Research matrix in `docs/research/competitor-family-coverage-matrix.md`.*
