# Component Consolidation Report

**Date:** June 21, 2026  
**Status:** INVENTORY → UNIFICATION  
**Goal:** 30+ variants → 10 canonical components + modifiers

---

## Executive Summary

The ZELEX site has accumulated **31 unique component classes** (many with undocumented variants) across 27 HTML pages. This consolidation merges duplicates, eliminates naming conflicts, and defines a single source-of-truth CSS system.

**Key Findings:**
- **10 canonical components** identified (Button, Card, Form/Field, Grid, Panel, etc.)
- **8 component families** with 2–4 variants each
- **107 CSS class definitions** (reduced from scattered patterns)
- **3 duplicate form patterns** (contact, contact-variant-b, contact-variant-d)
- **2 landing page variants** (index.html, hero.html, Landing.html)

---

## Component Inventory (Before)

### 1. BUTTON FAMILY (5 variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.btn` | Outline default | All pages (100+) |
| `.btn.solid` | Filled, high-CTA | Hero, browse, character |
| `.btn.ghost` | Low-contrast muted | Browse filters, character sidebar |
| `.btn.done` | Success state | Compare page |
| `.btn.concierge` | Premium intake | Index hero, contact |

**Variants:** 5 distinct styling patterns for essentially one element  
**CSS lines:** 26 (scattered across tokens + modifiers)

### 2. CARD FAMILY (4 variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.card` | Character card (3:4 AR, hover lift) | Browse, family, series, character siblings |
| `.bodycard` | Body architecture card (4:5 AR, taller) | Body detail, browse, family |
| `.family-tile` | Family hexagon tile | Family.html, index hero |
| `.compare-summary-card` | Compare results micro-card | Compare page |

**Variants:** 4 distinct card types, each w/ redundant CSS patterns  
**CSS lines:** 64 (base card + variants + hovers)

### 3. FORM/FIELD FAMILY (6+ variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.form-group` | Input wrapper + label | contact.html (all 3 variants) |
| `.field` | Text input element | Generic input |
| `.form-group input/textarea/select` | Scoped form elements | All inputs |
| `.opt` | Custom radio/toggle button | Quiz, contact (phase selectors) |
| `.opts` | Option grid container | Quiz, contact |
| `.consent-row` | Checkbox wrapper | contact, contact-variant-b |
| `.progress-wrap / .progress-bar` | Step indicator | Quiz, contact phase bars |

**Variants:** 6+ distinct field/input patterns  
**CSS lines:** 52

### 4. GRID FAMILY (3 variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.grid.g4` | 4-column responsive grid | Character grid, family grid, body grid |
| `.grid.g3` | 3-column responsive grid | Character siblings, body family section |
| `.grid.g2` | 2-column responsive grid | (Less common, utility) |

**Variants:** 3 layouts (col count only, no semantic diff)  
**CSS lines:** 8

### 5. PANEL/LAYOUT FAMILY (4 variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.panel` | Base container card | Character detail, body detail, form wrapper |
| `.panel--inset` | Subtle recessed variant | Character detail (stats panel) |
| `.panel--accent` | Gold border, gradient background | Detail page hero data |
| `.compare-preview / .concierge-band` | Full-width promo panel | Compare hero, index promo |

**Variants:** 4 distinct container patterns (2 are aliases)  
**CSS lines:** 12

### 6. TYPOGRAPHY/STATUS FAMILY (11 variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.stat` | Status badge base | Character/body cards (all pages) |
| `.stat-live`, `.stat-verified`, `.stat-pending`, `.stat-estimated`, `.stat-concept` | Status colors | Character cards, body cards |
| `.fam` | Family tag badge | Body cards, body detail, options |
| `.fam--classic`, `.fam--icon`, `.fam--muse`, `.fam--siren`, `.fam--empress`, `.fam--sculpt` | Family-specific colors | All pages |
| `.eyebrow` | Section label with underline rule | Page sections |

**Variants:** 11 distinct badge/label types  
**CSS lines:** 32

### 7. CONFIGURATOR FAMILY (28 variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.cfg-*` (28 distinct classes) | Configurator UI subsystem | configurator.html only |

**Variants:** 28 (isolated subsystem; not consolidated here)  
**CSS lines:** 103

### 8. COMPARE FAMILY (14 variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.compare-table`, `.compare-chip`, `.compare-empty`, etc. | Comparison UI | compare.html only |

**Variants:** 14 (mostly isolated to one page)  
**CSS lines:** 73

### 9. NAVIGATION/LAYOUT (5 variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.nav` | Sticky header | All pages |
| `.skip-link` | A11y focus link | All pages |
| `.crumbs` | Breadcrumb trail | Character, body, series, family |
| `.wrap`, `main` | Content container | All pages |
| `.grid` (base) | Flex grid container | All pages |

**Variants:** 5 layout/navigation types  
**CSS lines:** 28

### 10. UTILITY/STATE (7+ variants)
| Class | Purpose | Used In |
|-------|---------|---------|
| `.reveal` | Scroll reveal animation | All pages (LazyLoad effect) |
| `.sr-only` | Screen-reader only text | Navigation, skip link |
| `.em-grad` | Accent gradient text | Hero text effects |
| `.has-backdrop` | Image backdrop + scrim | Hero sections |
| `.monotile` | Family monogram tile | Character cards (placeholder art) |
| `.kv`, `.pos`, `.phnote`, `.bcode` | Data display mini-components | Detail pages |

**Variants:** 7+ utility patterns  
**CSS lines:** 28

---

## Duplicate/Variant Pages

| File | Status | Action |
|------|--------|--------|
| `index.html` | PRIMARY | Keep (canonical landing) |
| `hero.html` | VARIANT | Consolidate into index.html with A/B switch flag |
| `Landing.html` | VARIANT | Archive; duplicate of hero.html |
| `contact.html` | PRIMARY | Keep (canonical intake form) |
| `contact-variant-b.html` | VARIANT | Delete; legacy test version |
| `contact-variant-d.html` | VARIANT | Delete; legacy test version |
| `index-gallery-original.html` | LEGACY | Archive to `/docs/legacy/` |

---

## Consolidation Strategy: 10 Canonical Components

### TIER 1: Core Components (95% of page surfaces)

#### 1. **Button** (5 → 3)
```css
.btn                           /* outline default */
.btn.solid                     /* filled, high-CTA */
.btn.ghost                     /* low-contrast, inverted style */
.btn[data-variant="premium"]   /* concierge-style (keep as state) */
.btn[data-state="done"]        /* success state */
```
**Consolidation:** Merge `.btn.concierge` into `.btn[data-variant="premium"]` or `.btn.premium`  
**Reasoning:** Variant is a modifier, not a base class

#### 2. **Card** (4 → 2 + modifiers)
```css
.card                          /* base character card (3:4 AR) */
.card[data-aspect="body"]      /* body card variant (4:5 AR) */
.card.ph                       /* placeholder state (concept art) */

/* Or preserve semantic names w/ shared base: */
.card, .bodycard               /* Allow both names, shared CSS */
```
**Consolidation:** Base `.card` with aspect-ratio modifier or preserve `.bodycard` as semantic alias  
**Reasoning:** Different AR only; core structure identical

#### 3. **Form Field** (6 → 3)
```css
.form-group                    /* label + input wrapper */
.field                         /* single input element */
.opt                           /* custom toggle/radio button */
.consent-row                   /* checkbox with label (→ rename .form-checkbox) */
.form-row                      /* grid wrapper for multi-input rows */
```
**Consolidation:** Merge `.consent-row` → `.form-group[data-type="checkbox"]`  
**Reasoning:** Identical structure; only display differs

#### 4. **Grid Layout** (3 → 1 + responsive modifiers)
```css
.grid                          /* responsive container base */
.grid.g4                       /* 4-col on desktop, 2 on tablet, 1 on mobile */
.grid.g3                       /* 3-col → 2 → 1 */
.grid.g2                       /* 2-col → 1 → 1 */
```
**Keep as-is:** Already semantic & minimal (8 lines CSS)

#### 5. **Panel** (4 → 1 + modifiers)
```css
.panel                         /* base container */
.panel--inset                  /* subtle recessed variant */
.panel--accent                 /* gold-bordered promo */
.panel.wide                    /* full-width variant (combine .compare-preview, .concierge-band) */
```
**Consolidation:** Merge `.compare-preview` + `.concierge-band` into `.panel.wide` or rename to `.panel--feature`  
**Reasoning:** Identical structure; gradient + border are modifiers

#### 6. **Status Badge** (11 → 2 + data-attr)
```css
.stat                          /* base badge */
.stat[data-status="live"]      /* or .stat-live (keep for backward compat) */
.stat[data-status="verified"]
.stat[data-status="pending"]
.stat[data-status="estimated"]
.stat[data-status="concept"]

.fam                           /* family tag */
.fam[data-family="classic"]    /* or .fam--classic (keep) */
/* ... 5 family colors ... */
```
**Keep as-is:** Minimal CSS; data-attrs are semantic (preserve class names for compat)

#### 7. **Typography/Labels**
```css
.eyebrow                       /* section header with underline rule */
.section-head                  /* section title */
.section-sub                   /* section subtitle */
```
**Keep as-is:** Already concise

#### 8. **Navigation**
```css
.nav                           /* sticky header + hamburger */
.nav-toggle                    /* mobile menu button */
.nav-scrim                     /* overlay scrim when drawer open */
```
**Keep as-is:** Already optimal

#### 9. **Utility/Animation**
```css
.reveal                        /* scroll reveal effect */
.has-backdrop                  /* image backdrop + scrim */
.sr-only                       /* screen-reader only */
.em-grad                       /* gradient text effect */
```
**Keep as-is:** Minimal, well-documented

#### 10. **Data Display**
```css
.kv                            /* key-value pair table (label: value) */
.pos                           /* positioned note (blue left border) */
.phnote                        /* placeholder note (gold left border) */
.bcode                         /* body code monospace badge */
```
**Keep as-is:** Micro-components; minimal CSS

---

## Configurator & Compare: Isolated Subsystems

### Configurator (`.cfg-*`)
- **28 classes** used only on `configurator.html`
- **103 lines CSS**, self-contained
- **Action:** Keep as-is; mark with subsystem prefix documentation

### Compare (`.compare-*`)
- **14 classes** used mostly on `compare.html`
- **73 lines CSS**, 2 classes (`.compare-preview`, `.compare-points`) used elsewhere
- **Action:** Keep `.compare-table`, `.compare-empty` etc.; merge `.compare-preview` into `.panel.wide`

---

## CSS Refactor: Before → After

### Before (fragmented)
```css
/* site.css: 396 lines, scattered patterns, inconsistent naming */

.btn { ... }                              /* line 89 */
.btn:hover { ... }                        /* line 90 */
.btn.solid { ... }                        /* line 91 */
/* ... 4 more btn variants spread across 20 lines ... */

.card { ... }                             /* line 129 */
.card:hover { ... }                       /* line 130 */
.bodycard { ... }                         /* line 146 */
.bodycard:hover { ... }                   /* line 147 */
/* ... duplicated :hover logic, different selectors ... */

.opt { ... }                              /* line 224 */
.opt:hover { ... }                        /* line 225 */
.opt[aria-pressed="true"] { ... }         /* line 226 */
.opt.selected { ... }                     /* line 226 (same line as above) */
.opt.active { ... }                       /* line 226 */

/* Form variants all mixed: */
.field { ... }                            /* line 209 */
.form-group input { ... }                 /* line 209 */
.form-group textarea { ... }              /* line 209 */
.consent-row { ... }                      /* line 219 (isolated, duplicates .form-group) */
```

### After (consolidated)
```css
/* site.css: 320 lines, organized by component */

/* ====== BUTTONS ====== */
.btn { ... }                              /* base */
.btn:hover { ... }                        /* interaction */
.btn.solid { ... }                        /* variant */
.btn.solid:hover { ... }
.btn.ghost { ... }                        /* variant */
.btn.ghost:hover { ... }
.btn[data-variant="premium"] { ... }      /* or .btn.premium */
.btn[data-state="done"] { ... }

/* ====== CARDS ====== */
.card { ... }                             /* base */
.card:hover { ... }
.card.ph { ... }                          /* placeholder state */
.card[data-aspect="body"] { ... }         /* or keep .bodycard as alias */

/* ====== FORM FIELDS ====== */
.form-group { ... }                       /* wrapper */
.form-group > label { ... }               /* shared label */
.field { ... }                            /* input element */
.field:focus { ... }
.opt { ... }                              /* custom toggle */
.opt[aria-pressed="true"] { ... }         /* state */
.form-row { ... }                         /* grid for multiple fields */

/* ====== PANELS ====== */
.panel { ... }                            /* base */
.panel--inset { ... }                     /* variant */
.panel--accent { ... }                    /* variant */
.panel.wide { ... }                       /* feature panel (was .compare-preview) */

/* ====== GRIDS ====== */
.grid { ... }                             /* base flex grid */
.grid.g4 { ... }                          /* 4-col responsive */
.grid.g3 { ... }
.grid.g2 { ... }

/* ====== BADGES & LABELS ====== */
.stat { ... }
.stat-live, .stat-verified, etc. { ... } /* 5 status colors */
.fam { ... }
.fam--classic, .fam--icon, etc. { ... }  /* 6 family colors */
.eyebrow { ... }

/* ====== NAVIGATION ====== */
.nav { ... }
.nav-toggle { ... }
/* ... */

/* ====== UTILITIES ====== */
.reveal { ... }
.has-backdrop { ... }
/* ... */

/* ====== SUBSYSTEMS (isolated, minimal doc) ====== */
/* Configurator: see configurator.html & CSS section below */
.cfg-* { ... }                            /* 28 classes, line 350+ */

/* Compare: mostly isolated */
.compare-table { ... }
/* ... */
```

---

## Action Items

### Phase 1: CSS Consolidation (this task)
- [ ] Refactor `assets/site.css` → **320 lines** (76% reduction in scattered definitions)
- [ ] Add CSS section comments (/* ====== BUTTONS ====== */ style)
- [ ] Document all `.btn` variants in comment block
- [ ] Merge `.consent-row` into `.form-group[data-type="checkbox"]` semantics
- [ ] Verify `.bodycard` is alias or merge with `.card[data-aspect="body"]`
- [ ] Confirm `.compare-preview` → `.panel.wide` (or `.panel--feature`)

### Phase 2: HTML Consolidation (follow-up task)
- [ ] Audit `contact-variant-b.html` differences from `contact.html`
- [ ] Audit `contact-variant-d.html` differences from `contact.html`
- [ ] Merge into single `contact.html` with feature flags (if necessary)
- [ ] Delete `/contact-variant-*.html`
- [ ] Merge `hero.html` into `index.html` with A/B variant flag
- [ ] Archive `Landing.html`, `index-gallery-original.html` to `/docs/legacy/`

### Phase 3: Testing & Verification (follow-up task)
- [ ] Pixel-perfect regression test: each page at 3 breakpoints (desktop 1440, tablet 768, mobile 375)
- [ ] Visual diff: before/after screenshots
- [ ] Verify button hover states, card animations, form interactions
- [ ] QA all 27 pages render identically
- [ ] Run Lighthouse / Axe accessibility audit (no regressions)

---

## Component Usage Matrix

| Component | Pages Using | Count |
|-----------|------------|-------|
| `.btn` | All 27 pages | 100+ |
| `.card` | browse, family, series, character (siblings), index hero | 60+ |
| `.bodycard` | browse, body, family | 40+ |
| `.grid.g4` | browse, family, series, index | 15+ |
| `.form-group` | contact (all 3 variants), quiz | 20+ |
| `.opt` | quiz, contact | 30+ |
| `.stat` | All card pages | 80+ |
| `.panel` | character, body detail | 12+ |
| `.cfg-*` | configurator.html only | 40+ |
| `.compare-*` | compare.html primarily | 30+ |

---

## Risk & Mitigation

| Risk | Mitigation |
|------|-----------|
| Regression: CSS changes affect 100+ button instances | Use visual diff tooling; test all pages at 3 breakpoints |
| Merge `.bodycard` → `.card` breaks specificity | Create alias `.bodycard { /* empty */ }` for 1 sprint; audit selectors |
| Consolidating form variants affects quiz + 3 contact pages | Regression test contact-all variants; verify quiz fields |
| Removing variant pages breaks links | CI/pre-push check for broken internal links; 404 redirects |

---

## Summary

**Scope:** 30+ component variants → 10 canonical components  
**Effort:** 1 session  
**Deliverables:**
1. Refactored `assets/site.css` (~320 lines, -24%)
2. Component documentation (this file + inline CSS comments)
3. Pixel-perfect regression testing (visual diff report)
4. Updated `.gitignore` (archived files marked)

**Follow-up:** HTML consolidation (merge contact variants, landing pages, archive legacy).

