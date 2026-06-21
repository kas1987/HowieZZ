# Pixel-Perfect Regression Testing Plan

**Date:** June 21, 2026  
**Scope:** Component consolidation (site.css refactor)  
**Objective:** Verify visual fidelity across all pages at 3 breakpoints

---

## Testing Strategy

### Test Matrix

| Breakpoint | Width | Pages | Components |
|------------|-------|-------|------------|
| Desktop | 1440px | All 27 active | Button hover, card hover, form states |
| Tablet | 768px | All 27 active | Responsive grid, mobile nav (closed) |
| Mobile | 375px | All 27 active | Mobile nav drawer, stacked forms, full-width cards |

### Pages to Test (27 active + 3 variants)

**Core Pages:**
- index.html (hero + featured cards)
- hero.html (variant landing)
- browse.html (grid + filters)
- family.html?f=* (6 family pages)
- body.html?b=* (body detail + metrics)
- character.html?id=* (character detail + siblings)
- series.html?s=* (series grid)
- contact.html (form + variants B, D if kept)
- contact-variant-b.html (comparison)
- contact-variant-d.html (comparison)
- quiz.html (progress bars + options)
- compare.html (compare table + chips)
- configurator.html (isolated subsystem)
- options.html (info page)
- community.html (hub page)
- community-events.html (events list)
- craft.html (narrative page)

**Variant/Legacy Pages (archive only):**
- Landing.html
- index-gallery-original.html

---

## Visual Regression Test Cases

### 1. BUTTONS (All States)

**Test:** `.btn` in all variants  
**Pages:** Every page (100+ instances)  
**Cases:**
- [ ] `.btn` (outline, default) — at rest
- [ ] `.btn:hover` — lift + accent fill
- [ ] `.btn.solid` — filled cream, before pseudo-element shine
- [ ] `.btn.solid:hover` — accent fill
- [ ] `.btn.ghost` — muted outline
- [ ] `.btn.ghost:hover` — primary text + transparent bg
- [ ] `.btn.done` — verified state (compare page)
- [ ] `.btn.concierge` — premium gradient button
- [ ] `.btn.concierge:hover` — enhanced glow

**Breakpoints:** 1440, 768, 375  
**Expected:** No color shift, no layout drift, touch target ≥44px on mobile

---

### 2. CARDS (All Variants)

**Test:** `.card`, `.bodycard`, `.family-tile`, `.compare-summary-card`  
**Pages:** browse, family, series, index, body, character  
**Cases:**
- [ ] `.card` (character card 3:4 AR) — at rest
- [ ] `.card:hover` — lift -5px, border accent, shadow enhance
- [ ] `.card.ph` (placeholder state) — grayscale + dim image
- [ ] `.card .imgwrap img` — scale(1.05) on parent hover
- [ ] `.monotile` (monogram fallback) — centered, gradient bg
- [ ] `.bodycard` (4:5 AR) — layout matches `.card`, AR only differs
- [ ] `.family-tile` — radial gradient overlay, family color
- [ ] `.family-tile:hover` — lift -4px, border shifts to family color
- [ ] `.compare-summary-card` — nested grid layout

**Breakpoints:** 1440, 768, 375  
**Expected:** Consistent shadow depth, no image aspect ratio distortion, text legibility maintained

---

### 3. FORMS & FIELDS (All Variants)

**Test:** `.form-group`, `.field`, `.opt`, `.consent-row`, `.progress-wrap`  
**Pages:** contact*, quiz, options  
**Cases:**
- [ ] `.field` (text input) — padding, border, bg, focus ring
- [ ] `.field:focus` — accent border + focus-ring shadow
- [ ] `.field.err-field` — error state (coral border + error ring)
- [ ] `.form-group label` — correct spacing, text-transform
- [ ] `.form-row` (2-col on desktop) → 1-col on mobile
- [ ] `.opt` (toggle button) — at rest + hover
- [ ] `.opt[aria-pressed="true"]` — accent border + subtle bg
- [ ] `.opt.active` — cream text on accent bg
- [ ] `.consent-row` (checkbox) — 17x17px, accent accent-color
- [ ] `.consent-row label` — proper line-height, a tag underline
- [ ] `.progress-wrap .progress-bar` — gradient animation, width transition
- [ ] `.progress-bar` (prefers-reduced-motion) — no transition

**Breakpoints:** 1440, 768, 375  
**Expected:** Form fields 100% width, no text overflow, focus states clear and consistent

---

### 4. PANELS & LAYOUTS

**Test:** `.panel`, `.panel--inset`, `.panel--accent`, `.compare-preview`, `.concierge-band`  
**Pages:** character, body, compare, index  
**Cases:**
- [ ] `.panel` (base) — 32px padding, correct borders
- [ ] `.panel--inset` — transparent bg, no shadow
- [ ] `.panel--accent` — gold border, subtle gradient
- [ ] `.panel.wide` (merged `.compare-preview`) — 2-col grid → 1-col on tablet
- [ ] `.panel-title` (Playfair, 1.75rem) — line-height tight
- [ ] `.panel-sub` (muted, base font) — max-width 62ch, margin-bottom
- [ ] Nested `.grid` inside `.panel` — gap consistency

**Breakpoints:** 1440, 768, 375  
**Expected:** No layout shift, consistent padding, readable hierarchy

---

### 5. GRIDS (Responsive)

**Test:** `.grid.g4`, `.grid.g3`, `.grid.g2`  
**Pages:** browse, family, series, index  
**Cases:**
- [ ] `.grid.g4` @ 1440 — 4 columns, 18px gap
- [ ] `.grid.g4` @ 980 — 2 columns (media query)
- [ ] `.grid.g4` @ 520 — 1 column (mobile)
- [ ] `.grid.g3` @ 1440 — 3 columns
- [ ] `.grid.g3` @ 980 → 2 columns
- [ ] `.grid.g3` @ 520 → 1 column
- [ ] Gap remains 18px across breakpoints
- [ ] Card heights auto-grow, widths fill grid

**Breakpoints:** 1440, 980, 768, 520, 375  
**Expected:** Grid columns collapse correctly, no card distortion, gap consistent

---

### 6. NAVIGATION

**Test:** `.nav`, `.nav-toggle`, `.nav.open`, `.nav-scrim`  
**Pages:** All (sticky at top)  
**Cases:**
- [ ] `.nav` @ 1440 — sticky, flex row, links inline, no toggle
- [ ] `.nav .brand` — "ZELEX" styling with x in color-primary-blue
- [ ] `.nav .links a` — 26px gap, uppercase, accent on active
- [ ] `.nav-toggle` @ 860 — appears, hamburger icon
- [ ] `.nav-toggle:hover` — border accent, text accent
- [ ] `.nav.open` @ 860 — drawer slides in from right
- [ ] `.nav.open .links` — 82vw width, flex column, proper padding
- [ ] `.nav-scrim` — fixed overlay, blur(14px), animates in
- [ ] `.nav.up` — shadow + border-bottom-color lift (after 40px scroll)

**Breakpoints:** 1440, 860, 768, 375  
**Expected:** Mobile drawer doesn't trap content, scroll lock applied when open, accessible

---

### 7. BADGES & LABELS

**Test:** `.stat*`, `.fam*`, `.eyebrow`, `.section-head`  
**Pages:** All (used across every card)  
**Cases:**
- [ ] `.stat` (base) — inline-flex, 6px dot with shadow
- [ ] `.stat-live` — green bg + border
- [ ] `.stat-verified` — blue bg + border
- [ ] `.stat-pending` — dashed border, orange
- [ ] `.stat-estimated` — estimated bg, hollow dot
- [ ] `.stat-concept` — concept bg, hollow dot
- [ ] `.fam` (base) — 10px text, pill border
- [ ] `.fam--classic`, `.fam--icon`, etc. — correct family colors
- [ ] `.eyebrow` — uppercase, thin line rule below
- [ ] `.eyebrow.no-rule::after` — rule hidden
- [ ] `.section-head` — blue text, uppercase, margin correct

**Breakpoints:** 1440, 768, 375  
**Expected:** Badge colors accurate, rule line visible, no text cutoff

---

### 8. COMPARE PAGE (Isolated Subsystem)

**Test:** `.compare-table`, `.compare-chip`, `.compare-empty`, `.compare-summary-card`  
**Pages:** compare.html  
**Cases:**
- [ ] `.compare-table` — sticky header, sticky first column
- [ ] `.compare-table th` — blue text, uppercase, correct z-index stacking
- [ ] `.compare-table tr:nth-child(even)` — subtle bg stripe
- [ ] `.compare-table tbody tr:hover` — gold tint highlight
- [ ] `.compare-chip` — inline flex, pill badge with fam chip
- [ ] `.compare-chip-x` — small close button, hover color
- [ ] `.compare-empty` — centered, 40px padding, no cards message
- [ ] `.compare-summary-card .grid` — 2-col → 1-col @ 900px
- [ ] `.compare-summary-card .hl-note` — small, muted, readable

**Breakpoints:** 1440, 900, 768, 375  
**Expected:** Table scroll smooth, no cell content overflow, chip layout clear

---

### 9. CONFIGURATOR (Isolated Subsystem)

**Test:** `.cfg-*` (28 classes)  
**Pages:** configurator.html only  
**Cases:**
- [ ] `.cfg-grid` — 2-col → 1-col @ 980px
- [ ] `.cfg-stage` — centered silhouette, glow animation
- [ ] `.cfg-glow` — blur drift animation (prefers-reduced-motion respects)
- [ ] `.cfg-fam-grid` — 2-col cards, selection state accent
- [ ] `.cfg-scale-node.sel .cfg-node-dot` — 22x22 with cream border
- [ ] `.cfg-swatch.sel` — double shadow ring, scale(1.06)
- [ ] `.cfg-summary-eyebrow` — gold text, uppercase
- [ ] `.cfg-build-list` — 2-col layout, values right-aligned
- [ ] `.cfg-mto-note` — readable, no bold overflow

**Breakpoints:** 1440, 980, 768, 375  
**Expected:** Configurator visual hierarchy clear, selection states obvious, animations smooth

---

### 10. UTILITIES & ANIMATIONS

**Test:** `.reveal`, `.has-backdrop`, `.em-grad`, `.monotile`  
**Pages:** index, body, character (scroll-reveal on elements)  
**Cases:**
- [ ] `.reveal` (at rest) — opacity 0, translateY(18px)
- [ ] `.reveal.in` — opacity 1, no transform
- [ ] `.reveal.d1` through `.d6` — cascading delays (0.06s steps)
- [ ] `.has-backdrop` — ken-burns drift animation (36s loop)
- [ ] `.has-backdrop::after` — gradient scrim (0deg to transparent to 0deg)
- [ ] `.em-grad` — gradient text, proper -webkit-text-fill-color
- [ ] `.monotile` — radial gradient, centered span, family color via --fc var
- [ ] prefers-reduced-motion:reduce — all animations disabled

**Breakpoints:** All  
**Expected:** Scroll reveal triggers at 94% of viewport height, no jump, animations smooth

---

## Regression Test Execution

### Step 1: Setup Screenshots (Baseline)

```bash
# Before changes:
npm test -- --screenshot baseline/
# Creates: baseline/[page]/[breakpoint].png (81 images)
```

### Step 2: Apply Consolidation

1. Backup original `assets/site.css` → `assets/site-BACKUP-20260621.css`
2. Consolidation: merge `site-consolidated.css` into main `site.css`
3. Update all HTML pages: `<link rel="stylesheet" href="assets/site.css">`
4. Clear browser cache: `rm -rf ~/.cache/chromium/*`

### Step 3: Capture Screenshots (After)

```bash
npm test -- --screenshot after/
# Creates: after/[page]/[breakpoint].png (81 images)
```

### Step 4: Visual Diff

```bash
# Compare side-by-side:
npm run test:visual-diff baseline/ after/
# Generates: diff-report.html (highlights pixel changes)
```

### Step 5: Review & QA

| Result | Action |
|--------|--------|
| **0 diffs** | ✓ Pass — consolidation complete |
| **1–2 diffs** (minor) | Review pixels; document knowns (e.g., anti-alias) |
| **3+ diffs** | Investigate — likely CSS specificity or selector change |

---

## Specific Visual Checks (Manual)

### Desktop (1440px)

- [ ] All buttons visible, hover states trigger
- [ ] Cards stack in correct grid (4, 3, 2 col as expected)
- [ ] Form labels, inputs, buttons properly spaced
- [ ] Navigation links aligned, active state visible
- [ ] Footer copyright text centered, links readable

### Tablet (768px)

- [ ] Grid collapses to 2-col (g4, g3 → 2, g2 → 1)
- [ ] Mobile nav hamburger visible on < 860px
- [ ] Form rows stack to single column
- [ ] Compare table scrolls horizontally
- [ ] Footer adjusts to 2-col layout

### Mobile (375px)

- [ ] Mobile nav drawer opens/closes (touch-friendly)
- [ ] All cards render full-width
- [ ] Form stacks vertically, inputs tap-able (≥44px height)
- [ ] Compare table fully functional (horizontal scroll)
- [ ] Footer links wrapped, readable on small screen

---

## Known Differences (Acceptable)

| Item | Reason | Impact |
|------|--------|--------|
| Anti-alias rendering | Browser sub-pixel rasterization varies | <1px, visual no-op |
| Font rendering (Windows vs Mac) | OS native font rendering | Subtle weight/spacing diff, acceptable |
| Screenshot timing | Scroll position, animation frames | Retake if layout differs |

---

## Failure Criteria

- **CSS breaks layout:** Grid doesn't collapse, form fields overflow
- **Color shift:** Accent colors don't match tokens (e.g., `--color-accent` not rendering)
- **Interactive state missing:** Hover, focus, active states don't apply
- **Accessibility regression:** Focus-visible removed, skip-link broken, labels detached
- **Animation jerky:** Reveal, ken-burns, transitions stutter

---

## Sign-Off

**Tester:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Desktop (1440):** ✓ Pass / ✗ Fail  
**Tablet (768):** ✓ Pass / ✗ Fail  
**Mobile (375):** ✓ Pass / ✗ Fail  

**Notes:** 

---

## Automated Testing (Node.js)

### Axe Accessibility Audit

```bash
npm install axe-core axe-playwright
npx axe-playwright scan https://localhost:8000/index.html
# Output: a11y-report.json (no regressions)
```

### Lighthouse Performance

```bash
npm install lighthouse
npx lighthouse https://localhost:8000/index.html --output=json
# Verify: FCP, LCP, CLS unchanged (CSS consolidation shouldn't impact perf)
```

### CSS Validation (W3C)

```bash
npm install w3c-css-validator
npx validate-css assets/site.css
# Output: no warnings or errors
```

---

## Notes

- **DNS:** Serve via `python serve.py` or `caddy run` (see CLAUDE.md)
- **Cache:** Clear all browser caches before baseline
- **Screenshots:** Use Playwright @ 1x DPI (no scaling)
- **Diff tool:** pixelmatch or resemble.js for pixel-level detection
- **Diff threshold:** Allow ≤5% variance per image (anti-alias tolerance)

