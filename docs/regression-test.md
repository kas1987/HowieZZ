# Pixel-Perfect Regression Test: Design Token Refactor

**Test Date:** 2026-06-21  
**Change:** Refactored site.css (647 → 395 lines), all rules now token-based  
**Goal:** Verify zero visual regression across all pages

---

## Test Environment

- Browser: Chrome 120+, Firefox 121+, Safari 17+
- Viewport: Desktop (1440px), Tablet (768px), Mobile (375px)
- Light/Dark: N/A (single dark theme)
- Network: 4G throttle (optional, for performance)

---

## Pre-Test Checklist

1. **Branch state:** Confirm site.css refactor is the only CSS change
   ```bash
   git diff HEAD -- assets/site.css | head -20
   ```

2. **Build clean:** No stale CSS cache
   ```bash
   # Clear browser cache or open in private window
   # Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
   ```

3. **Baseline screenshot:** Before testing, take reference screenshots of each page in current state

---

## Test Pages (in order)

### 1. **index.html** — Atlas Homepage

**Viewport:** 1440px (desktop)

| Component | Check | Status |
|-----------|-------|--------|
| Nav bar | Spacing, text color, underline | [ ] |
| Hero section | Backdrop opacity, text gradient | [ ] |
| Section headers | Gold color, line decoration | [ ] |
| Primary buttons | Border, text color, hover lift | [ ] |
| Trust strip | Border, shadow, grid spacing | [ ] |
| Footer | Text color, link hover | [ ] |

**Viewport:** 768px (tablet)

| Component | Check | Status |
|-----------|-------|--------|
| Nav collapse | Hamburger visible, drawer styling | [ ] |
| Main padding | Adjust from 24px to 18px | [ ] |
| Grid layout | Cards responsive | [ ] |

**Viewport:** 375px (mobile)

| Component | Check | Status |
|-----------|-------|--------|
| Nav drawer | 82vw width, slide-in animation | [ ] |
| Button padding | 13px 22px override | [ ] |
| Touch targets | ≥44px min-height | [ ] |

---

### 2. **browse.html** — Character Grid

**Viewport:** 1440px

| Component | Check | Status |
|-----------|-------|--------|
| Character cards | Border color (gold soft 18%), hover lift, image scale | [ ] |
| Card text | Font sizing, muted color on metadata | [ ] |
| Family chips | Color per family (--color-family-*) | [ ] |
| Status badges | Dot fill/hollow, ring (solid/dashed/hollow), background opacity | [ ] |
| Grid gaps | 18px on desktop, 14px on tablet | [ ] |
| Filter section | Border, background, text color | [ ] |

**Hover interaction check:**
- Card elevates -5px ✓
- Border becomes gold ✓
- Shadow darkens + warm halo visible ✓
- Image zooms to 1.05 ✓

---

### 3. **family.html** — Body Family Index

**Viewport:** 1440px

| Component | Check | Status |
|-----------|-------|--------|
| Family tiles | Radial gradient background (var(--fam-color) 24%), border color | [ ] |
| Tile hover | Transform -4px, border to fam-color, shadow | [ ] |
| Grid | 6 columns on desktop, 3 on tablet, 1 on mobile | [ ] |
| Text colors | Title (serif), description (muted), label (fam-color) | [ ] |

---

### 4. **compare.html** — Side-by-Side Comparison

**Viewport:** 1440px

| Component | Check | Status |
|-----------|-------|--------|
| Compare table | Sticky first column, scroll on narrow | [ ] |
| Table header | Gold text, uppercase, background opacity | [ ] |
| Zebra rows | Alternating background opacity | [ ] |
| Table hover | Background gold tint | [ ] |
| Compare chips | Border, background surface-3, close button | [ ] |
| Primary CTA | Full-width on mobile | [ ] |
| Summary cards | Border, padding, grid layout | [ ] |

**Interaction check:**
- Remove chip: Close button visible ✓
- Chip count: Muted color ✓

---

### 5. **quiz.html** — Persona Quiz

**Viewport:** 1440px

| Component | Check | Status |
|-----------|-------|--------|
| Option cards (.opt) | Surface-2 background, border surface-1, padding 14px 16px | [ ] |
| Option hover | Border gold 45%, transform -1px | [ ] |
| Option selected | Border gold, background gold 9%, text cream | [ ] |
| Progress bar | Gold → cream gradient, smooth width | [ ] |
| Progress label | Muted color, uppercase letter-spacing | [ ] |
| Form fields | Field-bg, border-focus ring, error ring | [ ] |
| Consent row | Checkbox ≥17px, label readable | [ ] |

**Reduced-motion check** (enable in accessibility settings):
- No lift animation on hover ✓
- Progress bar instant ✓
- Transitions disabled ✓

---

### 6. **configurator.html** — Live Configurator (PDR-FE-006)

**Viewport:** 1440px

| Component | Check | Status |
|-----------|-------|--------|
| Configurator stage | surface-overlay background, 20px radius, glow visible | [ ] |
| Silhouette | Drop shadow, SVG paths animate smoothly | [ ] |
| Stat pills | Background rgba(13,13,13,.6), backdrop blur, border | [ ] |
| Panel sidebar | Position sticky top:88px, background surface-2 | [ ] |
| Family cards | Grid 2 col, border surface-1, selected state | [ ] |
| Family card selected | Gold border 60%, gradient background, inset shadow | [ ] |
| Scale track | Gradient (Muse → Gold → Coral), opacity .55 | [ ] |
| Scale nodes | Dot 14px, selected 22px + border cream | [ ] |
| Swatches | Dot 34px, selected glow + scale | [ ] |
| Summary | Border-top gold 30%, 2-col grid | [ ] |
| Build list | 2 col gap, k (key) muted, v (value) right-aligned | [ ] |

**Animation check** (normal motion):
- Glow drifts smoothly (9s cycle) ✓
- SVG paths transition smoothly (.45s easing-cubic) ✓
- Tip pops in (.22s) ✓

**Viewport:** 768px

| Component | Check | Status |
|-----------|-------|--------|
| Configurator grid | 1 col (stage full-width above panel) | [ ] |
| Stage height | 440px (reduced from 560px) | [ ] |
| Family grid | 1 col | [ ] |
| Build list | 1 col | [ ] |

---

### 7. **contact.html** — Contact/Inquiry Form

**Viewport:** 1440px

| Component | Check | Status |
|-----------|-------|--------|
| Form groups | margin-bottom spacing-5 (24px) | [ ] |
| Labels | font-size text-sm, letter-spacing widest, color muted | [ ] |
| Input fields | font-field-bg, border, padding, focus ring | [ ] |
| Placeholder | color text-placeholder (#6f6f6f) | [ ] |
| Error state | Border coral, ring coral 16%, message displayed | [ ] |
| Form row | 2 col gap spacing-4, 1 col on mobile | [ ] |
| Checkbox (consent) | 17×17px, accent gold, label readable line-height 1.55 | [ ] |
| Required indicator | Coral bullet | [ ] |
| Submit button | Primary CTA styling | [ ] |

**Form validation check:**
- Invalid field: Border red, ring red, error text visible ✓
- Focus: Border gold, ring gold ✓

---

### 8. **character.html** — Character Detail

**Viewport:** 1440px

| Component | Check | Status |
|-----------|-------|--------|
| Hero image | Aspect 3/4, background surface-0, grayscale on placeholder | [ ] |
| Breadcrumbs | Font small, letter-spacing loose, color muted | [ ] |
| Detail panels | Surface-2, border, radius-lg, padding spacing-6 | [ ] |
| Panel--accent | Border gold 26%, gradient background | [ ] |
| Key-value grid | 130px label col, 1fr value col, gap 7px 14px | [ ] |
| Data blocks (.pos, .phnote) | Surface-3 background, left border blue/gold, radius 0 sm sm 0 | [ ] |
| CTA buttons | Concierge style (serif italic, gradient, glow on hover) | [ ] |

---

### 9. **craft.html** — Brand Narrative

**Viewport:** 1440px

| Component | Check | Status |
|-----------|-------|--------|
| Hero backdrop | Scale 1.06 → 1.16 over 36s (kenburns animation) | [ ] |
| Hero scrim | Gradient top/bottom to surface-1 | [ ] |
| Reveal animations | Stagger d1-d6 (06s → 36s increments) | [ ] |
| Em-grad text | Gold → cream → coral gradient, text-fill transparent | [ ] |

---

## Global Checks (All Pages)

### Focus Management

| Scenario | Expected | Status |
|----------|----------|--------|
| Tab to button | Gold 2px outline, offset 4px | [ ] |
| Tab to nav link | Gold 2px outline, offset 5px | [ ] |
| Tab to card | No outline, gold border + shadow | [ ] |
| Tab to form field | No outline, gold border + ring | [ ] |

### Reduced-Motion (prefers-reduced-motion: reduce)

| Component | Expected | Status |
|-----------|----------|--------|
| Card hover | No lift, color feedback only | [ ] |
| Reveal animation | Instant (no transition) | [ ] |
| Backdrop kenburns | No animation | [ ] |
| Drawer slide | Instant, no hamburger morph | [ ] |
| Scrim fade | Instant | [ ] |

### Responsive Breakpoints

| Breakpoint | Trigger | Test |
|-----------|---------|------|
| max-width: 1120px | Family chooser | 6 col → 3 col |
| max-width: 980px | Config grid, compare summary | 2 col → 1 col |
| max-width: 860px | Nav toggle | Inline → drawer |
| max-width: 720px | Mobile rhythm | Padding, gap, button sizing |
| max-width: 600px | Form row | 2 col → 1 col |
| max-width: 520px | Grid | g4/g3/g2 → 1 col |
| max-width: 480px | Trust strip | 4 col → 2 col → 1 col |

---

## Performance Checks

| Metric | Target | Status |
|--------|--------|--------|
| CSS file size | < 50 KB | [ ] (currently ~40 KB) |
| First paint | < 1s | [ ] |
| Largest contentful paint | < 2.5s | [ ] |
| Layout shift (CLS) | < 0.1 | [ ] |

---

## Screenshot Comparison Workflow

1. **Take desktop screenshots** before & after refactor (all pages listed above)
2. **Use browser DevTools side-by-side compare** or [pixelmatch](https://github.com/mapbox/pixelmatch) for automated diffing
3. **Expected result:** Zero pixel differences (same visual output, cleaner CSS)
4. **If differences found:**
   - Identify component & token usage
   - Check token value vs. original hardcoded value
   - Update token if needed (do not revert to hardcoded value)

---

## Sign-Off

| Role | Check | Date | Notes |
|------|-------|------|-------|
| Developer | All tests pass, no regressions | [ ] / [ ] |  |
| QA | Visual verification on 3+ browsers | [ ] / [ ] |  |
| Product | Spot-check premium pages (Concierge, Compare) | [ ] / [ ] |  |

---

## Rollback Plan

If regression found that cannot be fixed with token adjustment:

1. Revert site.css to pre-refactor commit
2. Identify the specific rule causing issue
3. Audit original CSS (may reveal a pre-existing bug)
4. Refactor that rule separately with token
5. Re-test before committing

---

**Test completed:** __________  
**Tester name:** __________  
**Issues found:** [ ] None  [ ] Minor (non-blocking)  [ ] Critical (block release)  
**Details:** _____________________________
