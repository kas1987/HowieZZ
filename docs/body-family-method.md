# Body‑Family Classification Methodology (`body-family-method.md`)

## 1. Purpose & Position in the Taxonomy  
The **Body‑Family Methodology** is the authoritative backbone of ZELEX’s “Concierge Atlas” taxonomy. Every quiz result, comparison tool, character page, and inquiry flow references this document to map a measured (or estimated) body onto one of the six defined **Families**. The process is deterministic, reproducible, and serves as the single source of truth for downstream engineering and design implementations.

---

## 2. Core Ratios & Editorial Metric  

| Metric | Definition | Interpretation |
|--------|------------|----------------|
| **WHR** (Waist‑to‑Hip Ratio) | `waist ÷ hip` (lower = more hourglass) | Primary axis for silhouette definition |
| **BWR** (Bust‑to‑Waist Ratio) | `bust ÷ waist` (higher = more bust‑forward) | Secondary axis for silhouette definition |
| **Bust Drop** | `upper‑bust – under‑bust` (cm) – a proxy for cup volume | **Editorial only** – never used in automated family assignment |

> **Note:** Only **WHR** and **BWR** drive the algorithmic classification. Bust Drop is retained for editorial commentary (e.g., “drop 24.5 cm”) and must be displayed on product pages but excluded from any automated decision logic.

---

## 3. Families Overview  

| Family | WHR Range | BWR Range | Silhouette | Premium Δ | Target Buyer |
|--------|-----------|-----------|------------|-----------|--------------|
| **The Classic** | 0.68 – 0.72 | 1.40 – 1.50 | Timeless hourglass | +20 % | First‑time premium buyer |
| **The Icon** | 0.60 – 0.65 | 1.50 – 1.60 | Glamour model | +30 % | Photographer / curator |
| **The Muse** | 0.65 – 0.70 | 1.30 – 1.40 | Tall, hip‑dominant | +25 % | European aesthetic buyer |
| **The Siren** | 0.55 – 0.60 | 1.60 – 1.75 | Bust‑dominant fantasy | +35 % | Character / anime crossover |
| **The Empress** | 0.58 – 0.64 | 1.55 – 1.65 | Maximum plush | +40 % | Body‑positivity collector |
| **The Sculpt** | 0.65 – 0.68 | 1.45 – 1.55 | Muscular definition | +30 % | Fitness realism seeker |

*All ranges are inclusive.*

---

## 4. Classification Algorithm  

1. **Exact Range Match**  
   - If a body’s **WHR** *and* **BWR** both fall **within** the same family’s listed ranges, assign that family.  

2. **Nearest‑Center Fallback** *(when no family contains both axes)*  
   - Compute each family’s **center**:  
     - `WHR_center = (WHR_min + WHR_max) / 2`  
     - `BWR_center = (BWR_min + BWR_max) / 2`  
   - For every family calculate a **normalized distance**:  

```
d = ( |WHR − WHR_center| / 0.05 ) + ( |BWR − BWR_center| / 0.10 )
```

   - Select the family with the **smallest d**.  

3. **Tie‑Breaking**  
   - If multiple families share the same minimal **d**, choose the one whose **center** is nearest in Euclidean terms (i.e., the smaller raw \(|WHR‑WHR_center|\) and \(|BWR‑BWR_center|\) combination).

---

## 5. Confidence Labels  

| Label | Definition |
|-------|------------|
| **exact** | **Exactly one** family contains **both** WHR and BWR within its ranges. |
| **exact‑tie** | **More than one** family’s ranges contain the body; the nearest‑center family (per algorithm) wins. |
| **near** | No family contains **both** axes, but the selected nearest‑center family **contains at least one** axis (WHR **or** BWR) within its range. |
| **loose** | No family contains **both** axes, and the selected nearest‑center family contains **neither** axis within its range. |

The confidence label is attached to every classification result and drives UI wording (e.g., “matches **The Muse** (near)”).  

---

## 6. Current Distribution & Development Families  

| Family | Catalogued Bodies (measured) |
|--------|------------------------------|
| **The Empress** | 1 |
| **The Icon** | 4 |
| **The Muse** | 12 |
| **The Siren** | 2 |
| **The Classic** *(in‑development)* | 0 |
| **The Sculpt** *(in‑development)* | 0 |
| **Total measured bodies** | 19 |

*Only the four families above have at least one measured body in the current dataset.*  

---

## 7. Estimated‑Measurement Handling  

Three entries have **interpolated** dimensions and are flagged as **estimated**:

| Body ID | Model | Height | Cup | WHR | BWR | Drop (cm) | Estimated? |
|---------|-------|--------|-----|-----|-----|-----------|------------|
| **ZF161D** | Fusion | 161 cm | D‑cup | 0.660 | 1.371 | 18 cm | ✅ |
| **ZX153B** | SLE | 153 cm | B‑cup | 0.671 | 1.415 | 11 cm | ✅ |
| **ZX163E** | SLE | 163 cm | E‑cup | 0.630 | 1.466 | 19 cm | ✅ |

- **Display Requirement:** All UI components (quiz results, product pages, comparison tables) must show an explicit “*Estimated dimensions*” badge or note for these bodies.  
- **Confidence:** Despite estimation, the bodies are treated **exactly** as per the algorithm; the only difference is the visual annotation.

---

*This document is the definitive reference for implementing ZELEX’s body‑to‑family mapping across all Concierge Atlas experiences.*  
