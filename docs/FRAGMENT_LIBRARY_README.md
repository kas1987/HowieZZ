# ZELEX Fragment Library — Complete Reference

**Production-ready component library for the ZELEX Character Atlas (41 pages, 30+ reusable fragments).**

---

## What Is This?

A systematic breakdown of every reusable HTML/CSS component across the ZELEX site. Each fragment is:
- **Isolated** — works independently
- **Tested** — used in production across multiple pages
- **Documented** — with usage examples and customization patterns
- **Responsive** — follows design system breakpoints
- **Accessible** — includes ARIA labels and focus states

---

## Quick Start

### For Developers

1. **Copy a fragment** from the examples below
2. **Paste into your page** `<style>` block (page-specific CSS)
3. **Customize with CSS variables** from `assets/site.css`
4. **Test at 5 breakpoints:** 480px, 680px, 820px, 980px, 1120px

### For Designers

1. **Open** [`fragment-showcase.html`](fragment-showcase.html) in a browser
2. **Inspect any component** to see the HTML structure
3. **Reference** [`FRAGMENT_LIBRARY.md`](FRAGMENT_LIBRARY.md) for detailed documentation

### For Team Reference

- **Full Documentation:** [`FRAGMENT_LIBRARY.md`](FRAGMENT_LIBRARY.md) — 16 sections, every component with CSS and variants
- **Quick Lookup:** [`FRAGMENT_QUICK_REF.md`](FRAGMENT_QUICK_REF.md) — copy-paste snippets, breakpoints, color palettes
- **Interactive Demo:** [`fragment-showcase.html`](fragment-showcase.html) — visually browse all 30+ fragments

---

## Fragment Categories (30 Components)

### 1. Navigation & Headers (3 fragments)
- **Header Hero** — Radial gradient hero with background image, eyebrow, title, CTAs
- **Breadcrumbs** — Navigation trail with separators
- **Section Headers** — Eyebrow + title + subtitle pattern

**Used in:** All pages  
**Key Files:** `assets/site.css` lines 51–87, 88–100

---

### 2. Buttons & CTAs (2 fragments)
- **Button Group** — Solid, ghost, outline, concierge variants with hover states
- **Concierge Band** — Two-column CTA panel with gradient accent border

**Used in:** All pages  
**Key Files:** `assets/site.css` lines 89–104

---

### 3. Card Components (4 fragments)
- **Character Card** — 3:4 image + name, series, tagline, status badges
- **Body Card** — 4:5 silhouette + specs, family badge, ratios
- **Family Card** — Index card with background image scrim, active/dev states
- **Intent Card Router** — Call-to-action card with icon + heading + description

**Used in:** Grid layouts, browse, index, family pages  
**Key Files:** `assets/site.css` lines 129–155

---

### 4. Filters & Controls (2 fragments)
- **Filter Bar (Sticky)** — Pill buttons, family color-coded, search box, toggle
- **Count Bar** — Result count + compare quick action + reset link

**Used in:** `browse.html`, `family.html`  
**Key Files:** `assets/site.css` lines 224–230

---

### 5. Forms (4 fragments)
- **Form Group** — Text input + label + hint + error states
- **Form Row** — Two-column layout with responsive stacking
- **Consent Row** — Checkbox + linked label
- **Option Grid** — Multi-select card buttons with aria-pressed state

**Used in:** `contact.html`, `quiz.html`, `configurator.html`  
**Key Files:** `assets/site.css` lines 206–230

---

### 6. Panels & Info (3 fragments)
- **Panel** — Standard + accent variants with gradient border
- **Info Panel** — Sticky sidebar with icon + title + description list
- **Context Card** — Character/body preview card with stats grid

**Used in:** `contact.html`, `character.html`, sidebar sections  
**Key Files:** `assets/site.css` lines 201–204

---

### 7. Statistics & Metrics (2 fragments)
- **Stats Display** — Large number + label pairs (e.g., "6 Body Families")
- **Ratio Stats** — WHR/BWR badges with inline SVG icons + confidence chips

**Used in:** `index.html`, `family.html`, profile pages  
**Key Files:** `assets/site.css` lines 160–163

---

### 8. Comparison (2 fragments)
- **Compare Preview** — Two-column highlight with bullet points
- **Compare Table** — Horizontal metric table with sticky headers

**Used in:** `index.html`, `compare.html`  
**Key Files:** `assets/site.css` lines 265–300

---

### 9. Status & Badges (2 fragments)
- **Status Badges (Stat Chips)** — 5 types: live (green), verified (blue), pending (orange), estimated (purple), concept (gray)
- **Family Badges** — Color-coded badges for all 6 families + unclassified

**Used in:** All pages  
**Key Files:** `assets/site.css` lines 105–121

---

### 10. Animations (2 fragments)
- **Scroll Reveal** — Staggered fade-in on scroll (d1–d6 delay classes)
- **Ken Burns Background** — Infinite zoom animation on hero images

**Used in:** `index.html`, `browse.html`, many listing pages  
**Key Files:** `assets/site.css` lines 174–182, 170–173

---

### 11. Utilities (2 fragments)
- **Empty State** — No results messaging with reset button + action CTA
- **Key-Value Display** — Definition list layout for specs

**Used in:** `browse.html`, comparison pages, profile sections  
**Key Files:** `assets/site.css` lines 197–199

---

## Design Tokens (Always Use These)

All colors, spacing, typography, and sizing are CSS custom properties. Never hardcode values.

### Color Palette
```css
--color-primary-blue:    #5EA6E8    /* Accents, links, section heads */
--color-primary-gold:    #D4A574    /* Primary accent, borders */
--color-primary-coral:   #E18B73    /* Error, alerts, warnings */
--color-primary-cream:   #F7E3C3    /* Light text, highlights */
--color-surface-1:       #121212    /* Page background */
--color-surface-2:       #1b1b1b    /* Card/panel background */
--color-text-primary:    #e8e8e8    /* Body text */
--color-text-muted:      #ababab    /* Hint/secondary text */
--color-border-strong:   #333       /* Card borders */
--color-border-subtle:   rgba(255,255,255,0.02)  /* Faint lines */
```

### Typography
```css
--font-serif:            'Playfair Display', Georgia
--font-sans:             'Montserrat', system-ui
--size-text-xs:          0.625rem   (10px)
--size-text-sm:          0.75rem    (12px)
--size-text-base:        0.875rem   (14px)
--size-text-md:          1rem       (16px)
--size-text-lg:          1.25rem    (20px)
--size-text-xl:          1.75rem    (28px)
```

### Spacing
```css
--spacing-1: 4px    --spacing-5: 24px
--spacing-2: 8px    --spacing-6: 32px
--spacing-3: 12px   --spacing-7: 48px
--spacing-4: 16px   --spacing-8: 64px
```

### Radius
```css
--radius-sm:       6px
--radius-md:       10px
--radius-lg:       14px
--radius-xl:       18px
--radius-pill:     100px
```

### Shadows
```css
--shadow-card-rest:       0 2px 10px rgba(0,0,0,0.45)
--shadow-card-hover:      0 16px 40px rgba(0,0,0,0.6), ...
--shadow-panel:           0 1px 3px rgba(0,0,0,0.4)
--shadow-drop-small:      0 4px 18px rgba(0,0,0,0.45)
```

### Transitions
```css
--transition-fast:        .15s
--transition-smooth:      .25s
--transition-reveal:      .6s cubic-bezier(.22,.61,.36,1)
--transition-drawer:      .32s cubic-bezier(.22,.61,.36,1)
```

---

## Family Color Palette

Used for body family badges and filter highlights:

```css
--color-family-classic:   #8FB7E0   /* The Classic — Blue */
--color-family-icon:      #D4A574   /* The Icon — Gold */
--color-family-muse:      #9FD6B6   /* The Muse — Green */
--color-family-siren:     #E18B73   /* The Siren — Coral */
--color-family-empress:   #C792D6   /* The Empress — Purple */
--color-family-sculpt:    #C7B07F   /* The Sculpt — Tan */
```

---

## Responsive Breakpoints (Don't Use Others!)

Standard breakpoints across all pages:

```css
@media(max-width: 1120px) { /* Large tablets — 3-col → 2-col */ }
@media(max-width: 980px)  { /* Tablets — adjust grids */ }
@media(max-width: 820px)  { /* Small tablets — nav drawer */ }
@media(max-width: 720px)  { /* Small tablets — tighter */ }
@media(max-width: 680px)  { /* Large phones */ }
@media(max-width: 620px)  { /* Standard phones */ }
@media(max-width: 560px)  { /* Small phones — stack */ }
@media(max-width: 480px)  { /* Extra small — mobile */ }
```

---

## Example: Building a New Page

### Step 1: Copy the Hero
```html
<header class="hero">
  <div class="inner">
    <div class="eyebrow">Section Label</div>
    <h1>Page Title <span class="em-grad">Emphasis</span></h1>
    <p>Description up to 80 words.</p>
    <div class="cta">
      <a class="btn solid" href="#">Primary Action</a>
      <a class="btn" href="#">Secondary Action</a>
    </div>
  </div>
</header>
```

### Step 2: Add Section Content
```html
<main>
  <div class="section-head">Featured Items</div>
  <div class="section-sub">Introduction text goes here.</div>
  <div class="grid g4">
    <!-- Character cards loop here -->
  </div>
</main>
```

### Step 3: Add CTA Band
```html
<section class="concierge-band reveal d2">
  <div>
    <div class="eyebrow no-rule">Next Step</div>
    <h3>Call to action heading.</h3>
    <p>Supporting copy.</p>
  </div>
  <div class="actions-end">
    <a class="btn solid" href="#">Primary</a>
    <a class="btn concierge" href="#">Concierge</a>
  </div>
</section>
```

### Step 4: Use Page-Specific CSS
```html
<style>
/* Override fragment styles only when needed */
.custom-section {
  padding: 80px 24px;
  background: linear-gradient(...);
}
</style>
```

**All other styling comes from `assets/site.css` — no duplication!**

---

## Common Customizations

### Change Hero Text Color
```css
.hero h1 { color: var(--color-primary-cream); }
```

### Adjust Card Spacing
```css
.grid.g4 { gap: calc(var(--spacing-4) * 1.5); }
```

### Modify Button Padding
```css
.btn { padding: var(--spacing-3) var(--spacing-5); }
```

### Add Custom Section Background
```css
.my-section {
  background: linear-gradient(
    135deg,
    rgba(212, 165, 116, 0.08),
    transparent 40%
  ),
  var(--color-surface-2);
}
```

---

## Accessibility Requirements

✅ **Always include:**
- `alt` text on all images
- `for` attribute on form labels
- `aria-pressed`, `aria-label` on interactive elements
- Semantic HTML (`<button>`, `<a>`, `<form>`)
- Focus visible states (auto from `site.css`)

✅ **Test with:**
- Keyboard navigation (Tab through all links/buttons)
- Screen reader (NVDA, JAWS, or VoiceOver)
- High contrast mode
- Reduced motion preference (`prefers-reduced-motion`)

❌ **Never:**
- Use `<a>` for actions (use `<button>`)
- Remove focus outlines
- Use color alone to convey meaning
- Autoplay audio/video
- Trap keyboard focus

---

## Performance Best Practices

1. **Images:**
   - Optimize with appropriate formats (JPG for photos, SVG for icons)
   - Use `object-fit: cover` for image containers
   - Lazy-load images below the fold

2. **CSS:**
   - Never duplicate `site.css` rules
   - Keep page-specific `<style>` under 2KB
   - Use CSS variables for all colors/spacing

3. **JS:**
   - Keep page scripts under 5KB
   - Use `ZX` namespace (avoid global conflicts)
   - Load `site.js` before page script

4. **Animations:**
   - Use `transform` and `opacity` (GPU-optimized)
   - Avoid animating `left`, `top`, `width`, `height`
   - Add `will-change: transform` sparingly

---

## Files & Structure

```
amazing-tu-a4bd34/
├── docs/
│   ├── FRAGMENT_LIBRARY.md           ← Full documentation (16 sections)
│   ├── FRAGMENT_QUICK_REF.md         ← Quick reference (copy-paste)
│   ├── FRAGMENT_LIBRARY_README.md    ← This file
│   └── fragment-showcase.html        ← Interactive component demo
├── assets/
│   ├── site.css                      ← Design tokens + all fragment base classes
│   └── site.js                       ← ZX namespace, shared helpers
├── db/
│   ├── catalog.json
│   ├── characters.json
│   └── families.json
├── index.html                        ← Homepage (most fragments used)
├── browse.html                       ← Character grid + filters
├── character.html                    ← Character detail page
├── family.html                       ← Family index
├── compare.html                      ← Body comparison
├── contact.html                      ← Inquiry form
├── quiz.html                         ← Persona quiz
└── [other pages...]
```

---

## Inventory

| # | Fragment | Category | Pages Used | Status |
|----|----------|----------|-----------|--------|
| 1 | Header Hero | Nav & Headers | Most | ✅ |
| 2 | Breadcrumbs | Nav & Headers | 6 | ✅ |
| 3 | Section Headers | Nav & Headers | All | ✅ |
| 4 | Button Group | Buttons & CTAs | All | ✅ |
| 5 | Concierge Band | Buttons & CTAs | 3 | ✅ |
| 6 | Character Card | Cards | 5 | ✅ |
| 7 | Body Card | Cards | 3 | ✅ |
| 8 | Family Card | Cards | 2 | ✅ |
| 9 | Intent Card | Cards | 2 | ✅ |
| 10 | Filter Bar | Filters & Controls | 2 | ✅ |
| 11 | Count Bar | Filters & Controls | 1 | ✅ |
| 12 | Form Group | Forms | 3 | ✅ |
| 13 | Form Row | Forms | 1 | ✅ |
| 14 | Consent Row | Forms | 2 | ✅ |
| 15 | Option Grid | Forms | 3 | ✅ |
| 16 | Panel | Panels & Info | 10+ | ✅ |
| 17 | Info Panel | Panels & Info | 2 | ✅ |
| 18 | Context Card | Panels & Info | 2 | ✅ |
| 19 | Stats Display | Stats & Metrics | 2 | ✅ |
| 20 | Ratio Stats | Stats & Metrics | 5 | ✅ |
| 21 | Compare Preview | Comparison | 1 | ✅ |
| 22 | Compare Table | Comparison | 1 | ✅ |
| 23 | Status Badges | Status & Badges | All | ✅ |
| 24 | Family Badges | Status & Badges | All | ✅ |
| 25 | Scroll Reveal | Animations | 10+ | ✅ |
| 26 | Ken Burns | Animations | 3 | ✅ |
| 27 | Empty State | Utilities | 2 | ✅ |
| 28 | Key-Value | Utilities | 5 | ✅ |
| 29 | Loading State | Utilities | 4 | ✅ |
| 30 | Error State | Utilities | Error pages | ✅ |

---

## Documentation Map

### For Implementation
→ **Start with:** [`FRAGMENT_QUICK_REF.md`](FRAGMENT_QUICK_REF.md)  
Copy-paste snippets, breakpoints, color codes

### For Deep Dives
→ **Read:** [`FRAGMENT_LIBRARY.md`](FRAGMENT_LIBRARY.md) (Section 1–16)  
Every fragment with structure, CSS, variants, responsive behavior

### For Visual Testing
→ **Open:** [`fragment-showcase.html`](fragment-showcase.html)  
Browser-based demo of all 30+ components

### For Reference
→ **Check:** [`assets/site.css`](../assets/site.css) (350 lines)  
All design tokens and base fragment classes

---

## FAQ

**Q: Can I customize fragments?**  
A: Yes! Override in page-specific `<style>` tags. Always use CSS variables first.

**Q: What if a breakpoint isn't covered?**  
A: Use one of the 8 standard breakpoints. Never add custom breakpoints (maintenance nightmare).

**Q: How do I add a new fragment?**  
A: Create `.fragment-name` class in `site.css`, document it here, add to `fragment-showcase.html`.

**Q: Can I use this without `site.css`?**  
A: No. All fragments depend on design tokens and base classes. Always import `site.css`.

**Q: Are there animations on small screens?**  
A: Yes, but they respect `prefers-reduced-motion: reduce`. Animations use `transform` (GPU-safe).

**Q: How do I test accessibility?**  
A: Use axe DevTools, WAVE, or keyboard navigation. Check focus outlines, ARIA labels, contrast.

---

## Contact & Support

For questions on component usage:
1. Check the relevant section in [`FRAGMENT_LIBRARY.md`](FRAGMENT_LIBRARY.md)
2. Search `assets/site.css` for the CSS class name
3. Reference existing page using the fragment (e.g., `index.html` for hero)
4. Inspect [`fragment-showcase.html`](fragment-showcase.html) for visual examples

---

**Library Status:** ✅ Complete  
**Components:** 30/30  
**Pages Audited:** 41  
**Last Updated:** June 21, 2026  
**Framework:** Vanilla HTML/CSS/JS (no build step, no dependencies)

