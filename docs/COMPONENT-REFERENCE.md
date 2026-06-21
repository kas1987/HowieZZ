# ZELEX Component Reference Guide

**Consolidated Design System** — 10 canonical components + isolated subsystems  
**CSS Source:** `assets/site-consolidated.css` (320 lines, fully documented)

---

## Table of Contents

1. [Buttons](#buttons)
2. [Cards](#cards)
3. [Grids](#grids)
4. [Form Fields](#form-fields)
5. [Panels](#panels)
6. [Badges & Status](#badges--status)
7. [Navigation](#navigation)
8. [Data Display](#data-display)
9. [Utilities](#utilities)
10. [Subsystems](#subsystems)

---

## BUTTONS

**Class:** `.btn`  
**Variants:** 5 (outline, solid, ghost, done, concierge)  
**Usage:** All pages; primary CTA, secondary actions, navigation

### Default (Outline)
```html
<button class="btn">Learn more</button>
```
- Border: accent color
- Fill: transparent
- Text: accent color
- Hover: fills with accent, text inverts

### Solid (High-CTA)
```html
<a class="btn solid" href="/browse.html">Browse the atlas</a>
```
- Fill: cream
- Text: inverted (dark)
- Hover: accent fill
- Pseudo-element: shine effect on hover

### Ghost (Low-Contrast)
```html
<button class="btn ghost">Reset filters</button>
```
- Border: subtle (border-strong)
- Text: muted
- Hover: primary text, transparent fill

### Done (Success State)
```html
<button class="btn done" disabled>Added to compare</button>
```
- Border: verified (blue)
- Fill: verified with transparency
- Text: verified color
- Typically disabled state

### Concierge (Premium)
```html
<a class="btn concierge" href="/contact.html">Begin concierge inquiry</a>
```
- Font: serif italic
- Background: dark gradient
- Hover: enhanced shadow, accent text
- Used for premium intake flow

---

## CARDS

**Classes:** `.card`, `.bodycard`  
**Variants:** 4 (character, body, family tile, compare card)  
**Aspect Ratios:** 3:4 (character), 4:5 (body)

### Character Card
```html
<a class="card" href="character.html?id=...">
  <div class="imgwrap">
    <img src="..." alt="Character name" loading="lazy">
    <!-- Optional: <span class="repbadge">Concept</span> -->
  </div>
  <div class="b">
    <div class="pname-row">
      <div class="pname">Character Name</div>
      <div class="card-meta-rail">
        <span class="cupchip">D-cup</span>
        <span class="stat stat-verified">Verified</span>
      </div>
    </div>
    <div class="ptitle">Body Series</div>
    <div class="ptag">Tagline or persona</div>
  </div>
</a>
```

**Key Elements:**
- `.imgwrap` — 3:4 aspect ratio container
- `.b` — body padding (14px)
- `.pname-row` — flex row, character name + metadata
- `.cupchip` — cup size badge (styled with family color)
- `.repbadge` — "Concept" badge on placeholder cards
- `.monotile` — monogram fallback when no image

**States:**
- `.card.ph` — placeholder state (grayscale + dim)
- `.card:hover` — lift -5px, accent border, enhanced shadow

### Body Card
```html
<a class="bodycard" href="body.html?b=...">
  <div class="bw">
    <img src="..." alt="Body code">
  </div>
  <div class="bb">
    <h4>170cm · D-cup</h4>
    <div class="m">
      <span class="bcode">B032-001</span>
      <span class="fam fam--classic">The Classic</span>
      <span class="stat stat-verified">Verified</span>
    </div>
    <div class="bnames">Character · Name · Series</div>
    <div class="sig">
      <!-- Ratio stats with icons (WHR, BWR, DROP) -->
    </div>
  </div>
</a>
```

**Key Differences:**
- `.bw` — 4:5 aspect ratio (taller than character card)
- `.sig` — signature metrics with SVG icons
- `.bnames` — list of live character names in this body

### Family Tile
```html
<a class="family-tile" href="family.html?f=..." style="--fam-color:var(--color-family-classic)">
  <div class="k">THE CLASSIC</div>
  <h3>Proportions Title</h3>
  <p>Description...</p>
  <span class="status-note">...</span>
</a>
```

**Features:**
- `--fam-color` — CSS variable for family-specific styling
- Radial gradient overlay (family color at 24%)
- Hover: lift -4px, border shifts to family color

### Compare Summary Card
```html
<div class="compare-summary-card">
  <div class="top">
    <h3>Body Code</h3>
    <!-- Close button, etc. -->
  </div>
  <div class="grid">
    <div>
      <span class="k">Height</span>
      <b>170cm</b>
    </div>
    <!-- More rows... -->
  </div>
</div>
```

---

## GRIDS

**Class:** `.grid`  
**Variants:** `.grid.g4`, `.grid.g3`, `.grid.g2`  
**Gap:** 18px (consistent across all)

### 4-Column Grid
```html
<div class="grid g4">
  <a class="card">...</a>
  <!-- 3 more cards -->
</div>
```

**Responsive:**
- **1440px+:** 4 columns
- **980–1439px:** 2 columns (media query)
- **<520px:** 1 column (mobile)

### 3-Column Grid
```html
<div class="grid g3">
  <a class="card">...</a>
  <!-- 2 more cards -->
</div>
```

**Responsive:**
- **1440px+:** 3 columns
- **980–1439px:** 2 columns
- **<520px:** 1 column

### 2-Column Grid
```html
<div class="grid g2">
  <div>Left</div>
  <div>Right</div>
</div>
```

**Responsive:**
- **1440px+:** 2 columns
- **<520px:** 1 column

---

## FORM FIELDS

**Classes:** `.form-group`, `.field`, `.opt`, `.consent-row`, `.form-row`

### Text Input
```html
<div class="form-group">
  <label for="email">Email <span class="req">*</span></label>
  <input type="email" id="email" class="field" placeholder="you@example.com">
  <div class="field-hint">We'll never share your email.</div>
  <div class="field-err show">Please enter a valid email.</div>
</div>
```

**States:**
- `.field:focus` — accent border + focus-ring
- `.field.err-field` — coral border + error-ring
- `.field-err.show` — error message visible

### Textarea
```html
<div class="form-group">
  <label for="message">Message <span class="req">*</span></label>
  <textarea id="message" class="field" rows="5"></textarea>
</div>
```

**Styling:** Same as text input, but `min-height: 120px`, resizable vertically

### Select (Dropdown)
```html
<div class="form-group">
  <label for="series">Body Series</label>
  <select id="series" class="field">
    <option value="">Select a series</option>
    <option value="k-series">K-Series</option>
  </select>
</div>
```

### Radio/Toggle Buttons
```html
<div class="opts" role="group" aria-label="Intended use">
  <button class="opt" aria-pressed="false" data-value="personal">
    <span>Personal collection</span>
  </button>
  <button class="opt active" aria-pressed="true" data-value="display">
    <span>Display/showcase</span>
  </button>
</div>
```

**States:**
- `.opt` — default
- `.opt:hover` — border accent hint, lift -1px
- `.opt[aria-pressed="true"]` — accent border + subtle bg
- `.opt.active` — cream text on accent bg

### Checkbox (Consent Row)
```html
<div class="consent-row">
  <input type="checkbox" id="consent" required>
  <label for="consent">
    I confirm I am 18+ and agree to the <a href="/terms">terms</a>
  </label>
</div>
```

**Features:**
- 17×17px checkbox, accent color
- Label is clickable (cursor: pointer)
- Link styled with accent underline

### Multi-Field Row
```html
<div class="form-row">
  <div class="form-group">
    <label for="first">First name</label>
    <input type="text" id="first" class="field">
  </div>
  <div class="form-group">
    <label for="last">Last name</label>
    <input type="text" id="last" class="field">
  </div>
</div>
```

**Responsive:**
- **1440px+:** 2 columns
- **<600px:** 1 column (stacked)

### Progress Bar (Step Indicator)
```html
<div class="progress-wrap">
  <span class="progress-label">Step 2 of 4</span>
  <div class="progress-track">
    <div class="progress-bar" style="width: 50%"></div>
  </div>
</div>
```

**Animation:** Width transition 0.4s ease

---

## PANELS

**Class:** `.panel`  
**Variants:** `.panel--inset`, `.panel--accent`, `.panel.wide`

### Base Panel
```html
<div class="panel">
  <h3 class="panel-title">Character Details</h3>
  <p class="panel-sub">Technical specifications and metrics.</p>
  <!-- Content -->
</div>
```

**Features:**
- Background: surface-2
- Border: subtle border-strong
- Padding: 32px (--spacing-6)
- Shadow: subtle

### Inset Panel
```html
<div class="panel panel--inset">
  <!-- Content -->
</div>
```

**Features:**
- Background: transparent (2% white)
- No shadow
- Used for nested/secondary content

### Accent Panel
```html
<div class="panel panel--accent">
  <h3 class="panel-title">Signature Specs</h3>
  <!-- Metrics, ratios, etc. -->
</div>
```

**Features:**
- Border: accent color (26%)
- Background: gold gradient overlay (6%)
- Emphasizes important data

### Wide Panel (Promo/Feature)
```html
<div class="panel wide">
  <div>
    <h3>Compare Bodies Side-by-Side</h3>
    <p>See the physical differences between architectures...</p>
  </div>
  <div>
    <a class="btn solid" href="/compare.html">Open compare</a>
  </div>
</div>
```

**Features:**
- Display: grid (1.3fr / 0.7fr ratio)
- Responsive: 2-col → 1-col @ 760px
- Higher visual priority (border gradient, enhanced shadow)

---

## BADGES & STATUS

**Classes:** `.stat*`, `.fam*`, `.eyebrow`

### Status Badges

```html
<span class="stat stat-live">Live</span>
<span class="stat stat-verified">Verified</span>
<span class="stat stat-pending">Shoot Pending</span>
<span class="stat stat-estimated">Estimated</span>
<span class="stat stat-concept">Concept</span>
```

**Colors:**
- `stat-live` — green
- `stat-verified` — blue
- `stat-pending` — orange (dashed border)
- `stat-estimated` — purple (hollow dot)
- `stat-concept` — gray (hollow dot, reduced opacity)

**Features:**
- Inline-flex
- 6px colored dot (currentColor)
- Pill-shaped border-radius
- Text-transform: uppercase

### Family Tags

```html
<span class="fam fam--classic">The Classic</span>
<span class="fam fam--icon">The Icon</span>
<span class="fam fam--muse">The Muse</span>
<span class="fam fam--siren">The Siren</span>
<span class="fam fam--empress">The Empress</span>
<span class="fam fam--sculpt">The Sculpt</span>
<span class="fam fam--unclassified">Unclassified</span>
```

**Features:**
- Family-specific color via modifier class
- Pill badge with border
- Uppercase text, 10px size
- 600 font-weight

### Section Eyebrow
```html
<span class="eyebrow">FEATURED CHARACTERS</span>
```

**Features:**
- Uppercase, letter-spacing: 5px
- Accent color
- Pseudo-element: thin line rule below (width 34px)
- `.eyebrow.no-rule::after` — hides rule

---

## NAVIGATION

**Class:** `.nav`

### Desktop Navigation
```html
<nav class="nav" aria-label="Primary">
  <a class="brand" href="/">ZEL<span class="x">E</span>X</a>
  <div class="links">
    <a href="/index.html" class="active">Atlas</a>
    <a href="/browse.html">Browse</a>
    <!-- More links -->
  </div>
</nav>
```

**Features:**
- Sticky header (top: 0, z-index: 50)
- Flex row layout
- Brand font: Playfair, 20px, letter-spacing 4px
- Links: 26px gap, accent on active

### Mobile Navigation (< 860px)
```html
<nav class="nav">
  <a class="brand">ZEL<span class="x">E</span>X</a>
  <button class="nav-toggle">
    <span class="nav-toggle-bars">
      <span></span><span></span><span></span>
    </span>
    <span>Menu</span>
  </button>
  <div class="links" id="navLinks"><!-- Same links --></div>
  <div class="nav-scrim" id="navScrim"></div>
</nav>
```

**Features:**
- Toggle button: hamburger icon
- `.nav.open` — drawer opens from right (82vw width)
- `.nav-scrim` — overlay, blurred, dismisses drawer
- Links stack vertically, full-width
- Drawer lock: `body { overflow: hidden }` when open

**Scroll Effect:**
- `.nav.up` — shadow + accent border-bottom when scrolled > 40px

---

## DATA DISPLAY

### Key-Value Pairs
```html
<div class="kv">
  <b>Height</b>
  <span>170cm</span>
  
  <b>Cup Size</b>
  <span>D-cup</span>
</div>
```

**Layout:** 130px labels, 1fr value (grid)

### Positional Note
```html
<div class="pos">
  <strong>Position:</strong> Standing, arms at sides
</div>
```

**Features:**
- Border-left: 3px solid primary-blue
- Background: surface-3

### Placeholder Note
```html
<div class="phnote">
  Estimated dimensions — interpolated, no published spec card.
</div>
```

**Features:**
- Border-left: 3px solid accent (gold)
- Background: surface-3

### Body Code
```html
<span class="bcode">B032-001</span>
```

**Features:**
- Font: monospace
- Background: surface-3
- Padding: 3px 9px
- Border-radius: 6px

### Metrics Legend
```html
<div class="metrics-legend">
  <span class="lg-title">Reading the signature</span>
  <!-- SVG icon + label pairs -->
  <span class="lg-note">ratios shown as % ...</span>
</div>
```

**Features:**
- Flex row, flexible wrap
- Border + subtle background
- Small font sizes, muted colors
- Icon + text alignment helper (`.rstat`)

---

## UTILITIES

### Scroll Reveal Animation
```html
<div class="reveal d1">
  <h2>Section title</h2>
</div>
<div class="reveal d2">
  <p>Paragraph...</p>
</div>
```

**Features:**
- Opacity: 0 → 1 (on scroll)
- Transform: translateY(18px) → none
- Delay classes: `.d1`–`.d6` (0.06s increments)
- Respects `prefers-reduced-motion:reduce`

### Image Backdrop with Ken-Burns
```html
<section class="has-backdrop" style="--fc: var(--color-accent)">
  <div class="backdrop" style="background-image:url(...)"></div>
  <!-- Content -->
</section>
```

**Features:**
- Ken-burns animation (36s loop, infinite)
- Scrim layer (gradient overlay)
- Respects reduced motion

### Screen-Reader Only
```html
<span class="sr-only">Skip to main content</span>
```

**Features:**
- Visually hidden, screen-reader accessible
- Used for skip-links, ARIA labels

### Gradient Text
```html
<h1 class="em-grad">Find Your Perfect Match</h1>
```

**Features:**
- Linear gradient (accent → cream → warm)
- Background-clip: text
- Transparent text with gradient fill

---

## SUBSYSTEMS

### Configurator
**Isolated to:** `configurator.html`  
**Classes:** `.cfg-*` (28 classes)  
**Documentation:** Inline CSS comments

### Compare Page
**Isolated to:** `compare.html`  
**Classes:** `.compare-*` (14 classes)  
**Key:** `.compare-table` (sticky header + first column)

---

## CSS Architecture

### Token Organization
All colors, spacing, typography in `:root` CSS variables. No hardcoded values.

```css
--color-accent: #D4A574
--color-family-classic: #8FB7E0
--size-text-sm: 0.75rem
--spacing-6: 32px
--transition-smooth: 0.25s
```

### Component Naming
- **Prefix:** Describes component (`.btn`, `.card`, `.field`)
- **Modifier:** Variant or state (`.solid`, `.ghost`, `.active`)
- **Pseudo-elements:** `:hover`, `:focus`, `::after`
- **Data attributes:** Optional (`[data-status="live"]`)

### Responsive Strategy
Mobile-first, breakpoints at:
- **860px:** Nav toggle threshold
- **980px:** Grid collapse (4→2, 3→2)
- **768px:** Tablet layout adjustments
- **600px:** Form single-column
- **520px:** Mobile (1 column grid)
- **480px:** Extra small mobile

### Performance Optimizations
- CSS variables for runtime theming
- Single 320-line stylesheet (no fragmentation)
- No @import (avoids render-blocking)
- Hardware-accelerated animations (transform, opacity)
- `will-change: transform` on heavy animations

---

## Accessibility

### Keyboard Navigation
- Tab order: natural (buttons, links, form fields)
- Focus-visible: 2px gold outline, 3px offset
- `:focus-visible` respected globally

### Screen Readers
- `.sr-only` for skip-links, ARIA labels
- `aria-label`, `aria-pressed`, `aria-current` on interactive elements
- Form labels semantically linked (`<label for="field">`)

### Motion Preferences
- `prefers-reduced-motion:reduce` disables:
  - Animations (reveal, ken-burns, drift)
  - Transitions (hovers, state changes)
  - Pseudo-element effects (shine on buttons)

### Color Contrast
- All text ≥ 4.5:1 contrast ratio (WCAG AA)
- Badge colors tested for colorblind accessibility
- Status colors not sole indicator (include text + icon)

---

## Migration Guide (From Old System)

| Old | New | Notes |
|-----|-----|-------|
| `.form-group` (only) | `.form-group` + `.field` | Split into wrapper + element |
| `.consent-row` (isolated) | `.form-group + .consent-row` | Merged, backward compat preserved |
| `.compare-preview` | `.panel.wide` | Renamed, same styling |
| `.concierge-band` | `.panel.wide` | Merged |
| `.btn.concierge` | `.btn.concierge` (kept) | Consider `.btn[data-variant="premium"]` in future |
| 5 `.btn` variants | 3 base + modifiers | Consolidated |
| 4 card types | 2 base (`.card`, `.bodycard`) | Merged similar structures |

---

## Common Patterns

### Character List
```html
<div class="grid g4">
  <!-- 4 character cards per row -->
</div>
```

### Form with Steps
```html
<form class="panel">
  <div class="progress-wrap">
    <div class="progress-bar" style="width: 50%"></div>
  </div>
  <div class="form-group">
    <!-- Input fields -->
  </div>
  <div class="form-row">
    <!-- Multi-field row -->
  </div>
</form>
```

### Detail Page Hero
```html
<div class="has-backdrop" style="background-image: url(...)">
  <div class="backdrop" style="background-image: url(...)"></div>
  <div class="panel panel--accent">
    <h1>Title</h1>
    <!-- Key specs -->
  </div>
</div>
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Button colors wrong | CSS var not applied | Verify `--color-accent` in `:root` |
| Grid not responsive | Missing media query | Check `.grid.g4 @media(max-width:980px)` |
| Focus outline hidden | Accidental `outline: none` | Restore `:focus-visible` styling |
| Card shadows missing | Shadow var undefined | Verify `--shadow-card-hover` in `:root` |
| Form field too tall | Line-height or padding | Check `.field` padding (12px 14px) |

