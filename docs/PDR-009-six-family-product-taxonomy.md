# PDR‑009: Six‑Family Product Taxonomy  

*Implementation hand‑off for the Concierge Atlas product family taxonomy.*

---  

## 1. Objective  
Create a single source‑of‑truth taxonomy that maps **buyer intent → product family → measured body → character page → private inquiry**. The taxonomy will be stored as `db/family_taxonomy.json` and consumed by all front‑end surfaces (homepage, quiz, compare tool, character pages, inquiry routing) and downstream analytics pipelines.

---  

## 2. Strategic Thesis  

| Stage | Description | Key Output |
|------|-------------|------------|
| **Buyer intent** | Visitor signals (e.g., “first‑time premium”, “photographer”, “European aesthetic”, “anime crossover”, “body‑positivity”, “fitness realism”) are captured via copy and UI prompts. | Intent tag that maps to one of the six families. |
| **Family** | Intent tag selects a **Family** (Classic, Icon, Muse, Siren, Empress, Sculpt). Each family defines WHR/BWR silhouette ranges, premium uplift, and target buyer. | Family slug (e.g., `the-muse`). |
| **Body** | Measured body profiles (19 total) are matched to the selected family using WHR, BWR, height and cup size. Confidence (exact / near / loose) and estimation flags are stored. | Body code (e.g., `ZX172E`). |
| **Character** | Body profiles are linked to curated character pages (e.g., “The Iconic Model”) that showcase the silhouette, story and styling. | Character page URL. |
| **Private inquiry** | When a visitor requests a quote, the system routes the inquiry to the appropriate sales channel based on the final family‑body match. | Inquiry queue tag (e.g., `family_empress`). |

The flow guarantees that every shopper sees content that reflects their self‑identified intent, reinforced with measured data, and ends in a high‑value, private sales interaction.

---  

## 3. Taxonomy Model & Data Contract  

### 3.1 File location & top‑level keys  

| Key | Type | Description |
|-----|------|-------------|
| `version` | string | Semantic version placeholder (e.g., `"v_placeholder"`). |
| `generated_from` | string | Reference to the source script & raw profile data (`scripts/build_profiles.py` + `db/body_profiles.json`). |
| `metric_definitions` | array of objects | Definitions for each quantitative metric used in matching (WHR, BWR). |
| `confidence_labels` | array of strings | Allowed confidence values – `exact`, `near`, `loose`. |
| `families` | array of objects | One entry per product family (six total). |
| `bodies` | array of objects | One entry per measured body (19 total). |

### 3.2 `families` array  

| name | slug | WHR range | BWR range | silhouette | premium | target_buyer | status | member_count | members |
|------|------|-----------|-----------|------------|---------|--------------|--------|--------------|---------|
| The Classic | the‑classic | 0.68 – 0.72 | 1.4 – 1.5 | timeless hourglass | +20 % | First‑time premium buyer | active | 0 | — |
| The Icon | the‑icon | 0.60 – 0.65 | 1.5 – 1.6 | glamour model | +30 % | Photographer / curator | active | 4 | ZK159D, ZX163E, ZX165D, ZX172E |
| The Muse | the‑muse | 0.65 – 0.70 | 1.3 – 1.4 | tall, hip‑dominant | +25 % | European aesthetic buyer | active | 12 | ZF161D, ZF168B, ZF169C, ZG162D, ZGX165F, ZG170C, ZG170D, ZG175E, ZK168B, ZX153B, ZX170A, ZX171C |
| The Siren | the‑siren | 0.55 – 0.60 | 1.6 – 1.75 | bust‑dominant fantasy | +35 % | Character / anime crossover | active | 2 | ZX160J, ZX166K |
| The Empress | the‑empress | 0.58 – 0.64 | 1.55 – 1.65 | maximum plush | +40 % | Body‑positivity collector | active | 1 | ZX164G |
| The Sculpt | the‑sculpt | 0.65 – 0.68 | 1.45 – 1.55 | muscular definition | +30 % | Fitness realism seeker | active | 0 | — |

*All ranges are inclusive of the values shown in the authoritative data.*

### 3.3 `bodies` array  

| body_code | series | height_cm | cup | WHR | BWR | bust_drop_cm | family | confidence | estimated |
|-----------|--------|----------|-----|-----|-----|--------------|--------|------------|-----------|
| ZX164G | SLE | 164 | G | 0.552 | 1.595 | 24.5 | The Empress | near | false |
| ZK159D | K‑Series | 159 | D | 0.624 | 1.438 | 18 | The Icon | near | false |
| ZX163E | SLE | 163 | E | 0.630 | 1.466 | 19 | The Icon | near | true |
| ZX165D | SLE | 165 | D | 0.541 | 1.547 | 18.5 | The Icon | near | false |
| ZX172E | SLE | 172 | E | 0.608 | 1.504 | 19.5 | The Icon | exact | false |
| ZF161D | Fusion | 161 | D | 0.660 | 1.371 | 18 | The Muse | exact | true |
| ZF168B | Fusion | 168 | B | 0.653 | 1.250 | 13 | The Muse | near | false |
| ZF169C | Fusion | 169 | C | 0.672 | 1.292 | 15.5 | The Muse | near | false |
| ZG162D | Inspiration | 162 | D | 0.658 | 1.382 | 17.5 | The Muse | exact | false |
| ZGX165F | Inspiration | 165 | F | 0.663 | 1.391 | 21.5 | The Muse | exact | false |
| ZG170C | Inspiration | 170 | C | 0.686 | 1.357 | 16.0 | The Muse | exact | false |
| ZG170D | Inspiration | 170 | D | 0.655 | 1.289 | 18 | The Muse | near | false |
| ZG175E | Inspiration | 175 | E | 0.679 | 1.351 | 19.5 | The Muse | exact | false |
| ZK168B | K‑Series | 168 | B | 0.649 | 1.238 | 12 | The Muse | loose | false |
| ZX153B | SLE | 153 | B | 0.671 | 1.415 | 11 | The Muse | near | true |
| ZX170A | SLE | 170 | A | 0.670 | 1.262 | 10 | The Muse | near | false |
| ZX171C | SLE | 171 | C | 0.639 | 1.361 | 15.5 | The Muse | near | false |
| ZX160J | SLE | 160 | J | 0.507 | 1.718 | 32.5 | The Siren | near | false |
| ZX166K | SLE | 166 | K | 0.597 | 1.741 | 34.5 | The Siren | exact | false |

*`estimated` is true when the source line includes an explicit “(est)” flag.*

---  

## 4. How the Taxonomy Powers Each Surface  

| Surface | Taxonomy Usage | Impact |
|---------|----------------|--------|
| **Homepage discovery** | Pre‑filters families based on highlighted buyer intents; displays silhouettes, premium uplift, and sample body thumbnails drawn from the `members` list. | Immediate relevance; higher click‑through on premium offers. |
| **Quiz match‑scoring** | Each quiz answer maps to a metric (e.g., “I love hourglass” → Classic WHR range). The engine filters `families` → `bodies` and selects the highest‑confidence body. | Precise, data‑backed recommendations; reduces mismatches. |
| **Body compare tool** | Pulls the full `bodies` array; renders side‑by‑side cards with height, cup, WHR/BWR, and confidence badge. Allows users to switch families via tabs. | Transparency; encourages higher‑value upgrades. |
| **Character pages** | Each character page is linked to a specific body code (e.g., `ZX172E` for “The Iconic Model”). The page renders family silhouette, premium price offset, and narrative aligned with the target buyer. | Consistent storytelling anchored in measured data. |
| **Inquiry routing** | After a quote request, the backend extracts the selected `family` and `body_code` to route the lead to the correct sales channel (e.g., Empress specialists, Icon curators). | Faster response, higher conversion on premium segments. |

---  

## 5. Dependencies  

| Component | Source |
|-----------|--------|
| `scripts/build_profiles.py` | Generates `db/family_taxonomy.json` by ingesting `db/body_profiles.json` and the family definition table. |
| `db/body_profiles.json` | Raw measured body data (height, cup, WHR, BWR, bust drop, series). |
| Front‑end components (homepage, quiz, compare, character, inquiry) | Consume the JSON via a shared service layer. |

All downstream code must reference the generated JSON **only** – no hard‑coded family or body values elsewhere.

---  

## 6. Acceptance Criteria  

*The implementation is considered complete when all of the following are true:*  

1. `db/family_taxonomy.json` exists and validates against the schema described in Section 3.  
2. The file contains **six** family objects and **19** body objects.  
3. `member_count` for each family matches the distribution (Empress 1, Icon 4, Muse 12, Siren 2, Classic 0, Sculpt 0).  
4. Every body entry includes the fields listed in Section 3.3 with correct confidence and `estimated` flags.  
5. All front‑end surfaces load the taxonomy without runtime errors and display family‑specific content as described in Section 4.  
6. Quiz scoring produces a deterministic body match that aligns with the WHR/BWR ranges defined for the selected family.  
7. Inquiry routing tags (`family_<slug>`) correctly reflect the final family selection for **100 %** of submitted inquiries.  

---  

## 7. Companion Documents  

| Document | Location |
|----------|----------|
| Body‑Family Methodology | `PDR/body-family-method.md` |
| Copy Guidelines (Family & Body) | `PDR/body-family-copy-guide.md` |
| Product Matrix (Family ↔ Body ↔ Price) | `PDR/body-family-product-matrix.md` |
| Generated Taxonomy Data | `db/family_taxonomy.json` |

These documents provide deeper methodological rationale, editorial tone, and price‑mapping tables that complement the taxonomy hand‑off.

---  

*Prepared by the senior product & design documentation team – ZELEX Concierge Atlas*  

