# ZELEX Fragment Library

**Complete reusable component reference for the ZELEX Character Atlas.**

---

## Overview

This library documents 15+ reusable HTML/CSS fragments across 41 pages. Each fragment is production-ready, follows the design system, and can be dropped into any page with minimal customization.

**Design System Tokens:**
- Colors: `--color-primary-blue`, `--color-primary-gold`, `--color-primary-cream`, `--color-family-*`
- Typography: `--font-serif`, `--font-sans`, `--size-text-*`
- Spacing: `--spacing-*` (1–8)
- Radius: `--radius-sm` (6px) to `--radius-pill` (100px)
- Shadows: `--shadow-card-rest`, `--shadow-card-hover`
- All tokens defined in `assets/site.css` (root variables)

---

## 1. Navigation & Header Fragments

### 1.1 **Header Hero**
**Used in:** `index.html`, `browse.html`, `family.html`, `character.html`, `contact.html`, `compare.html`

**Structure:**
```html
<header class="hero">
  <div class="bgimg" id="heroBg"></div>
  <div class="inner">
    <div class="eyebrow">A Curated Collection</div>
    <h1>Find the body <span class="em-grad">made for you.</span></h1>
    <p>Descriptive subheading up to 3 sentences, max 80 words.</p>
    <div class="cta">
      <a class="btn solid" href="">Primary Action</a>
      <a class="btn" href="">Secondary Action</a>
      <a class="btn ghost" href="">Tertiary Action</a>
    </div>
    <div class="stats" id="stats"></div>
  </div>
</header>
```

**Key Properties:**
- Radial gradient background: `radial-gradient(ellipse at top, #1e1e1e, #121212 72%)`
- Hero text uses `font-size: clamp()` for responsive scaling
- `.em-grad` creates a gradient text effect (gold → cream → coral)
- `.bgimg` is an optional background image with opacity and scrim
- `.stats` auto-populates via JS; expects array of `[[number, label], ...]`

**Responsive Behavior:**
- Desktop: CTA buttons inline horizontal
- Mobile (<560px): CTA buttons stack full-width

**Common Customizations:**
```css
/* Darker background variant */
.hero { background: radial-gradient(ellipse at top, #1a1a1a, #0f0f0f 72%); }

/* Tighter padding for secondary pages */
.hero { padding: 52px 24px 36px; }
```

---

### 1.2 **Breadcrumbs (Crumbs)**
**Used in:** `browse.html`, `character.html`, `compare.html`, `body.html`, `series.html`

**Structure:**
```html
<div class="crumbs">
  <a href="index.html">Atlas</a><span>›</span>Browse
</div>
```

**Key Properties:**
- Fixed max-width container matching main content
- Muted color with hover state
- Separator uses `›` or `|` (style-agnostic)

**CSS:**
```css
.crumbs {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 18px 24px 0;
  font-size: var(--size-text-sm);
  color: var(--color-text-muted);
}
```

---

### 1.3 **Section Headers (Eyebrow + Title)**
**Used in:** All pages

**Structure:**
```html
<div class="featrow">
  <div class="section-head">The Six Body Families</div>
  <a href="family.html">See all families →</a>
</div>
<div class="section-sub">The Atlas's backbone — every body belongs to one silhouette family.</div>
```

**Variants:**

**Standard:**
```css
.section-head {
  margin: 46px 0 6px;
  font-size: var(--size-text-sm);
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--color-primary-blue);
}
.section-sub {
  color: var(--color-text-muted);
  font-size: var(--size-text-sm);
  margin-bottom: 10px;
  max-width: 760px;
}
```

**With Right-Aligned CTA:**
```html
<div class="featrow" id="families">
  <div class="section-head" style="margin: 0;">The Six Body Families</div>
  <a href="family.html" style="color: var(--color-accent); font-size: 11px;">See all →</a>
</div>
```

---

## 2. Button & CTA Fragments

### 2.1 **Button Group (Solid, Ghost, Outline)**
**Used in:** All pages

**Structure:**
```html
<div class="cta">
  <a class="btn solid" href="/quiz">Find your match</a>
  <a class="btn" href="/compare">Compare bodies</a>
  <a class="btn ghost" href="#explore">Browse the atlas</a>
</div>
```

**Variants:**

| Class | Style | Use Case |
|-------|-------|----------|
| `.btn.solid` | Cream background, dark text, shimmer on hover | Primary actions |
| `.btn` (default) | Gold border, gold text, reverse on hover | Secondary actions |
| `.btn.ghost` | Muted border, muted text | Tertiary / low-emphasis |
| `.btn.concierge` | Serif italic, gradient bg, luxury feel | Concierge CTAs |
| `.btn.done` | Verified green, disabled state | Post-action confirmation |

**CSS:**
```css
.btn {
  display: inline-block;
  padding: 12px 26px;
  border: 1px solid var(--color-accent);
  border-radius: var(--radius-md);
  color: var(--color-accent);
  letter-spacing: var(--letter-spacing-widest);
  text-transform: uppercase;
  font-size: var(--size-text-sm);
  transition: all var(--transition-smooth);
  cursor: pointer;
  font-family: inherit;
  background: transparent;
}
```

**Mobile Adaptation:**
```css
@media(max-width: 560px) {
  .cta {
    flex-direction: column;
    align-items: stretch;
    gap: 11px;
  }
  .cta .btn {
    width: 100%;
    text-align: center;
    padding: 15px 22px;
  }
}
```

---

### 2.2 **Concierge Band / CTA Panel**
**Used in:** `index.html`, `browse.html`, `character.html`

**Structure:**
```html
<section class="concierge-band reveal d2">
  <div>
    <div class="eyebrow no-rule">Private Next Step</div>
    <h3>Still deciding? Let the body architecture narrow it down.</h3>
    <p>Use the quiz or compare tool first, then send a cleaner inquiry with the exact bodies, family, and buyer intent attached.</p>
  </div>
  <div class="actions-end">
    <a class="btn solid" href="quiz.html">Find your match</a>
    <a class="btn concierge" href="contact.html">Begin concierge inquiry</a>
  </div>
</section>
```

**Key Properties:**
- Two-column layout (text + actions) on desktop, stacked on mobile
- Gradient background with gold accent border
- `.actions-end` forces right alignment and flex wrapping
- `.reveal.d2` enables staggered scroll animation (6-unit delay)

**CSS:**
```css
.concierge-band {
  margin: 54px 0 18px;
  border: 1px solid color-mix(in srgb, var(--color-accent) 26%, transparent);
  border-radius: var(--radius-xl);
  background: linear-gradient(135deg, rgba(212, 165, 116, 0.08), transparent 36%), var(--color-surface-2);
  padding: 28px;
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  gap: 24px;
  align-items: center;
  box-shadow: var(--shadow-card-rest);
}

@media(max-width: 760px) {
  .concierge-band {
    grid-template-columns: 1fr;
  }
}
```

---

## 3. Card Fragments

### 3.1 **Character Card (Grid Item)**
**Used in:** `index.html`, `browse.html`, `series.html`, `family.html`

**Structure:**
```html
<a class="card" href="character.html?id=CH-001">
  <div class="imgwrap">
    <img src="img/ch-001-hero.jpg" alt="Character name">
    <span class="repbadge">Live</span>
    <span class="slotchip">Slot 2</span>
  </div>
  <div class="b">
    <div class="pname-row">
      <span class="pname">Character Name</span>
      <div class="card-meta-rail">
        <span class="cupchip">B Cup</span>
        <span class="stat stat-live">Live</span>
      </div>
    </div>
    <div class="ptitle">Series Name</div>
    <div class="ptag">Character tagline or role</div>
  </div>
</a>
```

**Key Properties:**
- 3:4 aspect ratio for images
- `.imgwrap` handles image sizing and badges
- `.pname` uses serif font for emphasis
- `.stat-live` / `.stat-verified` / `.stat-pending` color badges
- Hover effect: -5px translateY + shadow enhancement

**Grid Integration:**
```css
.grid {
  display: grid;
  gap: 18px;
}
.grid.g4 {
  grid-template-columns: repeat(4, 1fr);
}
@media(max-width: 980px) {
  .grid.g4 {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media(max-width: 520px) {
  .grid.g4 {
    grid-template-columns: 1fr;
  }
}
```

---

### 3.2 **Body Card**
**Used in:** `body.html`, `compare.html` (summary), `options.html`

**Structure:**
```html
<a class="bodycard" href="body.html?b=B-001">
  <div class="bw">
    <img src="img/body-b-001-silhouette.png" alt="Body silhouette">
  </div>
  <div class="bb">
    <h4>Body Code</h4>
    <div class="m">
      <span class="fam fam--classic">The Classic</span>
      <span class="stat stat-verified">Verified</span>
    </div>
    <div class="bnames">Character names cast on this body</div>
    <div class="sig">
      <span class="rstat">
        <svg class="rsvg" viewBox="0 0 16 16"><!-- WHR icon --></svg>
        <span>0.68–0.70</span>
      </span>
    </div>
  </div>
</a>
```

**Key Properties:**
- 4:5 aspect ratio (taller than character cards)
- `.fam--*` classes color-code families
- `.rstat` displays measurement ratios with inline icons
- Metadata grouped in `.m` (meta row)

---

### 3.3 **Family Card (Index/Landing)**
**Used in:** `index.html`, `family.html`

**Structure:**
```html
<a class="fcard" href="family.html?f=The%20Classic">
  <div class="fn" style="color: #8FB7E0;">The Classic</div>
  <div class="fs">Timeless hourglass · WHR 0.68–0.72</div>
  <div class="fm">
    <span class="arrow">→</span>
    3 architectures · 12 characters
  </div>
</a>
```

**Variants:**

**With Background Image (Active):**
```html
<a class="fcard" href="family.html?f=The%20Classic">
  <div style="background-image: url('img/classic-hero.jpg');" 
       class="fc-bg"></div>
  <!-- content -->
</a>
```

**Development/Inactive State:**
```html
<div class="fcard dev">
  <div class="fn" style="color: #C792D6;">The Empress</div>
  <div class="fs">Maximum plush · WHR 0.58–0.64</div>
  <div class="fm">
    <span class="stat stat-concept">In Development</span>
  </div>
</div>
```

**CSS:**
```css
.fcard {
  position: relative;
  border: 1px solid var(--b-subtle);
  border-radius: 14px;
  padding: 20px;
  background: var(--color-surface-2);
  transition: 0.2s;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-height: 148px;
  box-shadow: 0 0 0 1px rgba(212, 165, 116, 0.10), 0 0 24px rgba(212, 165, 116, 0.06);
}

.fcard:hover {
  transform: translateY(-4px);
  border-color: var(--color-accent);
  box-shadow: var(--shadow-card-hover);
}
```

---

### 3.4 **Intent Card (Action Router)**
**Used in:** `index.html`, `contact.html`

**Structure:**
```html
<article class="intent-card">
  <div class="step">Guided</div>
  <h3>Find Your Match</h3>
  <p>Answer a short intent quiz to get your best-fit family and three character starting points.</p>
  <a class="btn solid" href="quiz.html">Start quiz</a>
</article>
```

**Grid Container:**
```css
.intent-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

@media(max-width: 980px) {
  .intent-grid {
    grid-template-columns: 1fr;
  }
}
```

**Key Properties:**
- `.step` uses uppercase, gold color for the label
- Icon area above heading (optional SVG icon)
- Button always `.btn.solid` for consistency
- Center-aligned by default

---

### 3.5 **Trust Strip (Confidence Signals)**
**Used in:** `index.html`, `contact.html`

**Structure:**
```html
<section class="trust-strip" aria-label="Buyer confidence signals">
  <div class="trust-item">
    <b>Made to order</b>
    <span>No standing-stock confusion</span>
  </div>
  <div class="trust-item">
    <b>Measured bodies</b>
    <span>WHR/BWR silhouette logic</span>
  </div>
  <div class="trust-item">
    <b>Private inquiry</b>
    <span>Concierge-first decision path</span>
  </div>
  <div class="trust-item">
    <b>Adults only</b>
    <span>18+ collector experience</span>
  </div>
</section>
```

**CSS:**
```css
.trust-strip {
  max-width: var(--max-width);
  margin: -18px auto 34px;
  padding: 0 24px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  position: relative;
  z-index: var(--z-sticky);
}

.trust-item {
  background: rgba(27, 27, 27, 0.92);
  border: 1px solid color-mix(in srgb, var(--color-accent) 22%, transparent);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  text-align: center;
  box-shadow: var(--shadow-card-rest);
}

.trust-item b {
  display: block;
  color: var(--color-primary-cream);
  font-size: var(--size-text-sm);
  letter-spacing: var(--letter-spacing-wider);
  text-transform: uppercase;
}
```

**Responsive:**
```css
@media(max-width: 820px) {
  .trust-strip {
    grid-template-columns: repeat(2, 1fr);
    margin-top: 18px;
  }
}

@media(max-width: 480px) {
  .trust-strip {
    grid-template-columns: 1fr;
  }
}
```

---

## 4. Filter & Control Fragments

### 4.1 **Filter Bar (Sticky)**
**Used in:** `browse.html`, `family.html`

**Structure:**
```html
<div class="filterbar" id="filterbar">
  <div class="filterbar-inner">
    <!-- Series filter -->
    <div class="filter-group" id="series-pills">
      <span class="filter-label">Series</span>
    </div>

    <div class="filter-sep"></div>

    <!-- Family filter -->
    <div class="filter-group" id="family-pills">
      <span class="filter-label">Family</span>
    </div>

    <div class="filter-sep"></div>

    <!-- Photo-only toggle -->
    <label class="toggle-wrap">
      <input type="checkbox" id="photo-toggle">
      <span class="toggle-label">Photographed only</span>
    </label>

    <!-- Search box -->
    <div class="search-wrap">
      <span class="search-icon">⌕</span>
      <input type="text" id="search-box" placeholder="Name or body code…">
    </div>
  </div>
</div>
```

**Key Properties:**
- Sticky positioning at `top: 62px` (below nav)
- Flex wrap for responsive stacking
- Pill buttons with active state
- Search box expands on focus

**Pill Button States:**
```css
.pill {
  padding: 6px 16px;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-pill);
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: 0.2s;
  white-space: nowrap;
}

.pill:hover {
  color: var(--color-text-primary);
  border-color: var(--color-text-muted);
}

.pill.active {
  background: var(--color-primary-cream);
  color: #111;
  border-color: var(--color-primary-cream);
  font-weight: 600;
}
```

**Family Pill Variant (Color-Coded):**
```html
<button class="pill fam-pill" data-val="The Classic">
  <span class="fam-dot" style="background: #8FB7E0;"></span>
  <span>Classic</span>
</button>
```

---

### 4.2 **Count Bar**
**Used in:** `browse.html`

**Structure:**
```html
<div class="count-bar">
  <div class="count-text" id="count-text">
    Showing <strong>24</strong> of <strong>102</strong> characters
  </div>
  <div class="compare-quick" id="compare-quick">
    <span class="compare-count" id="compare-count">Compare set: 0</span>
    <a class="btn ghost" href="compare.html">Open Compare</a>
    <button class="btn ghost" type="button">Clear Compare</button>
  </div>
  <span class="reset-link" id="reset-link">Reset filters</span>
</div>
```

**CSS:**
```css
.count-bar {
  max-width: var(--max-width);
  margin: 20px auto 14px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.count-text {
  font-size: 13px;
  color: var(--color-text-muted);
}

.count-text strong {
  color: var(--color-text-primary);
}
```

---

## 5. Form Fragments

### 5.1 **Form Group (Text Input)**
**Used in:** `contact.html`, `quiz.html`, `configurator.html`

**Structure:**
```html
<div class="form-group">
  <label for="name">
    Full Name <span class="req">*</span>
  </label>
  <input type="text" id="name" name="name" placeholder="First and last name">
  <div class="field-hint">We'll use this for your inquiry response.</div>
  <div class="field-err show">This field is required</div>
</div>
```

**Key Properties:**
- Label with required indicator (`.req` in coral)
- Hint text below input (optional)
- Error message with `.show` class to display
- Focus state: gold border + gold shadow

**CSS:**
```css
.form-group {
  margin-bottom: var(--spacing-5);
}

.form-group > label {
  display: block;
  font-size: var(--size-text-sm);
  letter-spacing: var(--letter-spacing-widest);
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 7px;
}

.form-group input {
  width: 100%;
  background: var(--form-field-bg);
  border: 1px solid var(--form-field-border);
  color: var(--color-text-primary);
  border-radius: var(--form-field-radius);
  padding: var(--form-field-padding);
  font-family: inherit;
  transition: 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: var(--form-field-focus-ring);
}

.form-group input.err-field {
  border-color: var(--color-primary-coral);
  box-shadow: var(--form-field-error-ring);
}
```

---

### 5.2 **Form Row (Two-Column)**
**Used in:** `contact.html`

**Structure:**
```html
<div class="form-row">
  <div class="form-group">
    <label for="first">First Name <span class="req">*</span></label>
    <input type="text" id="first" name="first">
  </div>
  <div class="form-group">
    <label for="last">Last Name <span class="req">*</span></label>
    <input type="text" id="last" name="last">
  </div>
</div>
```

**CSS:**
```css
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-4);
}

@media(max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
```

---

### 5.3 **Consent Row (Checkbox)**
**Used in:** `contact.html`, `quiz.html`

**Structure:**
```html
<div class="consent-row">
  <input type="checkbox" id="consent" name="consent">
  <label for="consent">
    I agree to the <a href="/privacy">privacy policy</a> and consent to 
    be contacted at the email above.
  </label>
</div>
```

**CSS:**
```css
.consent-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: var(--spacing-5);
}

.consent-row input[type="checkbox"] {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
  margin-top: 2px;
  accent-color: var(--color-accent);
  cursor: pointer;
}

.consent-row label {
  font-size: var(--size-text-base);
  color: var(--color-text-muted);
  line-height: var(--line-height-readable);
  cursor: pointer;
}

.consent-row label a {
  color: var(--color-accent);
  text-decoration: underline;
}
```

---

### 5.4 **Option Grid (Multi-Select Cards)**
**Used in:** `contact.html`, `quiz.html`, `configurator.html`

**Structure:**
```html
<div class="opt-grid">
  <button class="opt" aria-pressed="false" data-value="body-focused">
    <span style="width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; color: var(--color-accent);">✓</span>
    <div style="text-align: left; flex: 1;">
      <div style="font-weight: 600; font-size: var(--size-text-sm);">Body-Focused</div>
      <div style="font-size: 12px; color: var(--color-text-muted); margin-top: 3px;">Drawn to proportion & silhouette</div>
    </div>
  </button>
  <button class="opt" aria-pressed="false" data-value="face-features">
    <span style="width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; color: var(--color-accent);">✓</span>
    <div style="text-align: left; flex: 1;">
      <div style="font-weight: 600; font-size: var(--size-text-sm);">Face & Features</div>
      <div style="font-size: 12px; color: var(--color-text-muted); margin-top: 3px;">Character expression matters most</div>
    </div>
  </button>
</div>
```

**CSS:**
```css
.opt-grid {
  display: grid;
  gap: var(--spacing-3);
}

.opt {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  text-align: left;
  cursor: pointer;
  background: var(--color-surface-2);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  color: var(--color-text-primary);
  font-family: inherit;
  transition: 0.2s;
}

.opt:hover {
  border-color: color-mix(in srgb, var(--color-accent) 45%, transparent);
  transform: translateY(-1px);
}

.opt[aria-pressed="true"],
.opt.selected,
.opt.active {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 9%, var(--color-surface-2));
  color: var(--color-primary-cream);
}
```

---

## 6. Panel & Info Fragments

### 6.1 **Panel (General Container)**
**Used in:** Throughout (flexible container)

**Variants:**

**Standard Panel:**
```html
<div class="panel">
  <h3>Title</h3>
  <p>Content goes here.</p>
</div>
```

**Accent Panel (Gold Border + Gradient):**
```html
<div class="panel panel--accent">
  <h3>Highlight This Section</h3>
  <p>Important information with accent styling.</p>
</div>
```

**CSS:**
```css
.panel {
  background: var(--color-surface-2);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-panel);
}

.panel--accent {
  border-color: color-mix(in srgb, var(--color-accent) 26%, transparent);
  background: linear-gradient(135deg, rgba(212, 165, 116, 0.06), transparent 38%), var(--color-surface-2);
}

.panel-title {
  font-family: var(--font-serif);
  font-size: var(--size-text-xl);
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-2);
}

.panel-sub {
  color: var(--color-text-muted);
  font-size: var(--size-text-base);
  margin-bottom: var(--spacing-5);
  max-width: 62ch;
}
```

---

### 6.2 **Info Panel (Sticky Sidebar)**
**Used in:** `contact.html`, `character.html`

**Structure:**
```html
<div class="info-panel">
  <h3>Quick Answers</h3>
  <div class="info-item">
    <div class="info-icon">📧</div>
    <div>
      <h4>Concierge Email</h4>
      <p><a href="mailto:inquiry@zelexdoll.com">inquiry@zelexdoll.com</a></p>
    </div>
  </div>
  <div class="info-item">
    <div class="info-icon">🕐</div>
    <div>
      <h4>Response Time</h4>
      <p>Within 24 business hours</p>
    </div>
  </div>
  <div class="info-divider"></div>
  <div class="info-email-row">
    Questions? <a href="mailto:inquiry@zelexdoll.com">Contact us</a>
  </div>
</div>
```

**CSS:**
```css
.info-panel {
  background: var(--color-surface-2);
  border: 1px solid rgba(212, 165, 116, 0.22);
  border-radius: 14px;
  padding: 32px 28px;
  position: sticky;
  top: 86px;
}

.info-panel h3 {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--color-primary-cream);
}

.info-item {
  display: flex;
  gap: 14px;
  margin-bottom: 22px;
  align-items: flex-start;
}

.info-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 15px;
  background: rgba(212, 165, 116, 0.12);
  border: 1px solid rgba(212, 165, 116, 0.22);
}

.info-item h4 {
  font-size: 12px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--color-accent);
  margin-bottom: 4px;
}

.info-item p {
  font-size: 13px;
  color: var(--color-text-muted);
  line-height: 1.6;
}
```

---

### 6.3 **Context Card (Character/Body Preview)**
**Used in:** `contact.html`, `character.html`

**Structure:**
```html
<div class="context-card fam-edge">
  <div class="cc-head">
    <img src="img/ch-001-thumb.jpg" alt="Character" class="cc-thumb">
    <div class="cc-id">
      <div class="cc-eyebrow">Character</div>
      <div class="cc-name">Character Name</div>
      <div class="cc-title">Series Name</div>
      <div class="cc-fam">
        <span class="dot" style="background: #8FB7E0;"></span>
        The Classic
      </div>
    </div>
  </div>
  <div class="cc-stats">
    <div class="cc-stat">
      <div class="k">Height</div>
      <div class="v">165 <small>cm</small></div>
    </div>
    <div class="cc-stat">
      <div class="k">Cup</div>
      <div class="v">C</div>
    </div>
    <div class="cc-stat cc-premium">
      <div class="k">WHR</div>
      <div class="v">0.70</div>
    </div>
  </div>
  <div class="cc-note">
    This character is part of your inquiry. <em>Modify your selection</em> at any time.
  </div>
</div>
```

**CSS:**
```css
.context-card {
  background: var(--color-surface-2);
  border: 1px solid color-mix(in srgb, var(--color-accent) 26%, transparent);
  border-radius: 14px;
  padding: 0;
  margin-bottom: 26px;
  overflow: hidden;
  position: relative;
}

.context-card.fam-edge {
  border-left: 3px solid var(--color-accent);
}

.cc-head {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 18px 20px 16px;
}

.cc-thumb {
  width: 60px;
  height: 80px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
  background: #0d0d0d;
}
```

---

## 7. Statistics & Metrics Fragments

### 7.1 **Stats Display**
**Used in:** `index.html`, `family.html`

**Structure:**
```html
<div class="stats">
  <div>
    <span class="n">6</span>
    <span class="l">Body Families</span>
  </div>
  <div>
    <span class="n">48</span>
    <span class="l">Body Architectures</span>
  </div>
  <div>
    <span class="n">102</span>
    <span class="l">Characters</span>
  </div>
  <div>
    <span class="n">87</span>
    <span class="l">Photographed</span>
  </div>
</div>
```

**CSS:**
```css
.stats {
  display: flex;
  gap: 40px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 40px;
}

.stats .n {
  font-family: var(--font-serif);
  font-size: 32px;
  color: var(--color-primary-cream);
  display: block;
  line-height: 1;
}

.stats .l {
  font-size: var(--size-text-xs);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 6px;
  color: var(--color-text-muted);
}
```

---

### 7.2 **Ratio Stats (WHR/BWR)**
**Used in:** `character.html`, `compare.html`, `body.html`

**Structure:**
```html
<div class="glance-ratios">
  <span class="rstat">
    <svg class="rsvg" viewBox="0 0 16 16">
      <path d="M4 6h8M4 10h8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
    </svg>
    <span>WHR 0.70 (In range)</span>
  </span>
  <span class="rstat">
    <svg class="rsvg" viewBox="0 0 16 16">
      <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
    </svg>
    <span>BWR 0.45</span>
  </span>
  <span class="conf-chip exact">Verified</span>
</div>
```

**CSS:**
```css
.rstat {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 12px;
  color: var(--color-text-primary);
}

.rsvg {
  width: 13px;
  height: 13px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.4;
  flex-shrink: 0;
}

.conf-chip {
  font-size: 9px;
  letter-spacing: 1.4px;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-strong);
  color: var(--color-text-muted);
}

.conf-chip.exact {
  color: var(--color-status-verified);
  border-color: color-mix(in srgb, var(--color-status-verified) 34%, transparent);
}
```

---

## 8. Comparison Fragments

### 8.1 **Compare Preview (Two-Column)**
**Used in:** `index.html`

**Structure:**
```html
<section class="compare-preview reveal d2">
  <div>
    <div class="eyebrow no-rule">Compare before contact</div>
    <h3>Body architecture is the real decision layer.</h3>
    <p>Compare up to four bodies by height, weight, cup, family, WHR/BWR, bust drop, and handling class before asking concierge.</p>
    <div class="mt-18">
      <a class="btn solid" href="compare.html">Open body compare</a>
    </div>
  </div>
  <div class="compare-points">
    <span>Natural vs dramatic silhouette</span>
    <span>Solo-manageable vs dedicated-space handling</span>
    <span>Verified vs estimated family confidence</span>
  </div>
</section>
```

**CSS:**
```css
.compare-preview {
  margin: 54px 0 18px;
  border: 1px solid color-mix(in srgb, var(--color-accent) 26%, transparent);
  border-radius: var(--radius-xl);
  background: linear-gradient(135deg, rgba(212, 165, 116, 0.08), transparent 36%), var(--color-surface-2);
  padding: 28px;
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  gap: 24px;
  align-items: center;
  box-shadow: var(--shadow-card-rest);
}

.compare-points {
  display: grid;
  gap: 8px;
}

.compare-points span {
  display: block;
  color: var(--color-primary-cream);
  background: rgba(255, 255, 255, 0.035);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  padding: 9px 11px;
  font-size: var(--size-text-sm);
}
```

---

### 8.2 **Compare Table**
**Used in:** `compare.html`

**Structure:**
```html
<div class="compare-table-wrap">
  <table class="compare-table">
    <thead>
      <tr>
        <th>Metric</th>
        <th>Body A</th>
        <th>Body B</th>
        <th>Body C</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong class="hl-read">Height</strong><span class="hl-note">Standing height</span></td>
        <td>165 cm</td>
        <td>168 cm</td>
        <td>162 cm</td>
      </tr>
      <tr>
        <td><strong class="hl-read">WHR Ratio</strong><span class="hl-note">Waist-to-hip</span></td>
        <td>0.70<span style="color: var(--color-primary-blue);">●</span></td>
        <td>0.65<span style="color: var(--color-primary-blue);">●</span></td>
        <td>0.72</td>
      </tr>
    </tbody>
  </table>
</div>
```

**CSS:**
```css
.compare-table-wrap {
  overflow: auto;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-lg);
  background: var(--color-surface-2);
}

.compare-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 780px;
}

.compare-table th,
.compare-table td {
  border-bottom: 1px solid var(--color-border-strong);
  padding: 12px 14px;
  text-align: left;
  vertical-align: top;
  font-size: var(--size-text-base);
}

.compare-table th {
  color: var(--color-accent);
  font-size: var(--size-text-xs);
  letter-spacing: var(--letter-spacing-wider);
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.025);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
}

.compare-table tbody tr:nth-child(even) td {
  background: rgba(255, 255, 255, 0.018);
}

.compare-table tbody tr:hover td {
  background: rgba(212, 165, 116, 0.05);
}
```

---

## 9. Status & Badge Fragments

### 9.1 **Status Badges (Stat Chips)**
**Used in:** All pages (cards, profile views)

**Variants:**

```html
<!-- Live (green) -->
<span class="stat stat-live">Live</span>

<!-- Verified (blue) -->
<span class="stat stat-verified">Verified</span>

<!-- Pending (orange, dashed border) -->
<span class="stat stat-pending">Estimated</span>

<!-- Estimated (purple) -->
<span class="stat stat-estimated">Estimated</span>

<!-- Concept/Dev (gray) -->
<span class="stat stat-concept">In Development</span>
```

**CSS:**
```css
.stat {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-1);
  font-size: var(--size-text-xs);
  letter-spacing: var(--letter-spacing-wider);
  text-transform: uppercase;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: var(--radius-pill);
  white-space: nowrap;
}

.stat::before {
  content: "";
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
  background: currentColor;
  box-shadow: 0 0 0 1px color-mix(in srgb, currentColor 35%, transparent);
}

.stat-live {
  color: var(--color-status-live);
  background: color-mix(in srgb, var(--color-status-live) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--color-status-live) 30%, transparent);
}

.stat-verified {
  color: var(--color-status-verified);
  background: color-mix(in srgb, var(--color-status-verified) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--color-status-verified) 34%, transparent);
}
```

---

### 9.2 **Family Badges**
**Used in:** All pages (filters, cards, profile)

**Structure:**
```html
<span class="fam fam--classic">The Classic</span>
<span class="fam fam--icon">The Icon</span>
<span class="fam fam--muse">The Muse</span>
<span class="fam fam--siren">The Siren</span>
<span class="fam fam--empress">The Empress</span>
<span class="fam fam--sculpt">The Sculpt</span>
<span class="fam fam--unclassified">Unclassified</span>
```

**CSS:**
```css
.fam {
  font-size: 10px;
  letter-spacing: var(--letter-spacing-wider);
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  font-weight: 600;
  display: inline-block;
  border: 1px solid currentColor;
  background: transparent;
  color: var(--color-text-muted);
}

.fam--classic {
  color: var(--color-family-classic);
}

.fam--icon {
  color: var(--color-family-icon);
}

.fam--muse {
  color: var(--color-family-muse);
}

.fam--siren {
  color: var(--color-family-siren);
}

.fam--empress {
  color: var(--color-family-empress);
}

.fam--sculpt {
  color: var(--color-family-sculpt);
}
```

---

## 10. Animation & Reveal Fragments

### 10.1 **Scroll Reveal (Staggered)**
**Used in:** `index.html`, `browse.html`, many listing pages

**Structure:**
```html
<!-- Apply .reveal class to any element -->
<article class="card reveal d1"></article>
<article class="card reveal d2"></article>
<article class="card reveal d3"></article>
<!-- etc. -->
```

**CSS:**
```css
.js .reveal {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity var(--transition-reveal), transform var(--transition-reveal);
}

.js .reveal.in {
  opacity: 1;
  transform: none;
}

/* Stagger delays: d1 to d6 (0.06s increments) */
.reveal.d1 {
  transition-delay: 0.06s;
}
.reveal.d2 {
  transition-delay: 0.12s;
}
.reveal.d3 {
  transition-delay: 0.18s;
}
.reveal.d4 {
  transition-delay: 0.24s;
}
.reveal.d5 {
  transition-delay: 0.30s;
}
.reveal.d6 {
  transition-delay: 0.36s;
}
```

**JS Initialization (in site.js):**
```javascript
function ZX.revealInit() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}
```

---

### 10.2 **Hero Background Ken Burns Animation**
**Used in:** `index.html`, `browse.html`, pages with `.has-backdrop`

**CSS:**
```css
.has-backdrop {
  position: relative;
  overflow: hidden;
  isolation: isolate;
}

.has-backdrop > .backdrop {
  position: absolute;
  inset: 0;
  z-index: var(--z-base);
  background-size: cover;
  background-position: top center;
  opacity: 0.18;
  filter: grayscale(0.18);
  transform: scale(1.06);
  animation: kenburns var(--anim-kenburns-duration) ease-in-out infinite alternate;
  will-change: transform;
}

@keyframes kenburns {
  from {
    transform: scale(1.06) translate3d(0, 0, 0);
  }
  to {
    transform: scale(1.16) translate3d(0, -2.2%, 0);
  }
}
```

---

## 11. Utility Fragments

### 11.1 **Empty State**
**Used in:** `browse.html`, comparison pages, search/filter results

**Structure:**
```html
<div class="empty-state">
  <div class="big">No characters match this combination</div>
  <p>Loosen a filter to see more of the cast — or let the concierge curate options in this silhouette for you.</p>
  <div class="es-actions">
    <button class="btn ghost" onclick="resetFilters()">Reset all filters</button>
    <a class="btn solid" href="contact.html">Ask the Concierge</a>
  </div>
</div>
```

**CSS:**
```css
.empty-state {
  text-align: center;
  padding: 80px 24px;
}

.empty-state .big {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: clamp(22px, 4vw, 36px);
  color: var(--color-text-muted);
  margin-bottom: 16px;
}

.empty-state p {
  color: var(--color-text-muted);
  font-size: var(--size-text-base);
  max-width: 400px;
  margin: 0 auto 24px;
}

.empty-state .es-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 8px;
}
```

---

### 11.2 **Loading State**
**Used in:** Async pages (`browse.html`, `compare.html`, `character.html`)

**Structure:**
```html
<div class="loading">Loading the ZELEX catalog…</div>
```

**CSS:**
```css
.loading {
  max-width: 600px;
  margin: 80px auto;
  text-align: center;
  color: var(--color-text-muted);
}
```

---

### 11.3 **Error Message**
**Used in:** Form submissions, API failures

**Structure:**
```html
<div class="err">
  <p>Something went wrong: <code>Error loading the catalog</code></p>
  <p><a href="/">Go back to the atlas</a></p>
</div>
```

**CSS:**
```css
.err {
  max-width: 600px;
  margin: 60px auto;
  text-align: center;
  color: var(--color-primary-coral);
}

.err code {
  background: #222;
  padding: 2px 7px;
  border-radius: var(--radius-sm);
  color: var(--color-primary-cream);
}
```

---

### 11.4 **Key-Value Display**
**Used in:** Profile sections, spec sheets

**Structure:**
```html
<dl class="kv">
  <dt>Height</dt><dd>165 cm</dd>
  <dt>Weight</dt><dd>62 kg</dd>
  <dt>Cup</dt><dd>C</dd>
  <dt>Handling Class</dt><dd>Solo-manageable</dd>
</dl>
```

**CSS:**
```css
.kv {
  display: grid;
  grid-template-columns: 130px 1fr;
  gap: 7px 14px;
  font-size: var(--size-text-base);
  color: var(--color-text-muted);
}

.kv b {
  color: var(--color-text-primary);
  font-weight: 600;
}
```

---

## 12. Component Best Practices

### Design Token Usage

Always prefer CSS custom properties over hardcoded values:

**Good:**
```css
.card {
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-card-rest);
}
```

**Avoid:**
```css
.card {
  border: 1px solid #333;
  border-radius: 14px;
  padding: 32px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.45);
}
```

### Responsive Breakpoints

Standard breakpoints used across all pages:

```css
@media(max-width: 1120px) { /* Large tablets */ }
@media(max-width: 980px)  { /* Tablets */ }
@media(max-width: 820px)  { /* Smaller tablets */ }
@media(max-width: 720px)  { /* Small tablets */ }
@media(max-width: 680px)  { /* Large phones */ }
@media(max-width: 620px)  { /* Standard phones */ }
@media(max-width: 560px)  { /* Small phones */ }
@media(max-width: 480px)  { /* Extra small phones */ }
```

### Accessibility

Every interactive component includes:

```css
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
  border-radius: 2px;
}
```

**Semantic HTML:**
- Use `<button>` for actions, not `<a>`
- Use `<a>` for navigation/links
- Use `aria-pressed`, `aria-label`, `aria-live` where needed
- Buttons with state use `aria-pressed="true"|"false"`

### Dark Mode

All colors are designed for the dark theme (no light mode). Text uses:
- Primary: `#e8e8e8`
- Muted: `#ababab`
- Inverted (on light bg): `#111`

---

## 13. Usage Examples

### Example 1: Adding a New Series Card to index.html

```html
<!-- Add to the seriesrail container -->
<a class="srow reveal d1" href="series.html?s=New%20Series">
  <div class="srow-bg" style="background-image: url('img/series-hero.jpg')"></div>
  <h4>New Series</h4>
  <div class="sc">Description of the series design language.</div>
  <div class="sm">3 architectures · 8 photographed →</div>
</a>
```

### Example 2: Creating a Character Profile Card on contact.html

```html
<div class="context-card fam-edge">
  <div class="cc-head">
    <img src="img/ch-profile.jpg" alt="Character" class="cc-thumb">
    <div class="cc-id">
      <div class="cc-eyebrow">Character</div>
      <div class="cc-name">Character Name</div>
      <div class="cc-title">Series</div>
      <div class="cc-fam">
        <span class="dot" style="background: var(--color-family-icon);"></span>
        The Icon
      </div>
    </div>
  </div>
  <div class="cc-stats">
    <div class="cc-stat">
      <div class="k">Height</div>
      <div class="v">165 <small>cm</small></div>
    </div>
  </div>
</div>
```

### Example 3: Building a Custom Filter Pill Set

```javascript
// In page JS: build filter pills dynamically
function buildFamilyPills(families) {
  const container = document.getElementById('family-pills');
  families.forEach((fam, idx) => {
    const btn = document.createElement('button');
    btn.className = 'pill fam-pill';
    btn.dataset.val = fam;
    btn.innerHTML = `<span class="fam-dot" style="background: ${famColor(fam)};"></span>${fam}`;
    btn.addEventListener('click', () => {
      state.family = fam;
      updateView();
    });
    container.appendChild(btn);
  });
}
```

---

## 14. Common Customization Patterns

### Changing the Primary Color

Replace all instances of `var(--color-primary-gold)` in root variables, or override per-page:

```css
:root {
  --color-primary-gold: #E0B584; /* New shade */
}
```

### Adjusting Spacing/Padding

Use spacing multipliers:

```css
.card {
  padding: calc(var(--spacing-6) * 1.5); /* 48px instead of 32px */
}
```

### Creating a Variant Card

```css
.card.featured {
  border: 2px solid var(--color-accent);
  background: linear-gradient(135deg, rgba(212, 165, 116, 0.08), transparent 36%), var(--color-surface-2);
}

.card.featured:hover {
  box-shadow: var(--shadow-card-outline);
}
```

---

## 15. Maintenance & Future Updates

- **Design Token Changes:** Update in `assets/site.css` root variables; all fragments auto-update
- **New Component Needed?** Follow the naming convention: `.fragment-name` with page-specific overrides in `<style>` tags
- **Responsive Issues?** Test at key breakpoints: 480px, 680px, 820px, 1120px
- **Animation Performance?** Use `will-change` sparingly; prefer `transform` over `left`/`top`
- **Accessibility Review:** Run axe/WAVE on each new page; check contrast, focus states, ARIA labels

---

## 16. Fragment Inventory

| # | Fragment | Pages Used | Status |
|---|----------|-----------|--------|
| 1 | Header Hero | index, browse, character, contact, compare | Production |
| 2 | Breadcrumbs | browse, character, series, body, family | Production |
| 3 | Section Headers | All | Production |
| 4 | Button Group (Solid/Ghost) | All | Production |
| 5 | Concierge Band CTA | index, browse, character | Production |
| 6 | Character Card | index, browse, series, family, character | Production |
| 7 | Body Card | body, compare, options | Production |
| 8 | Family Card | index, family | Production |
| 9 | Intent Card Router | index, contact | Production |
| 10 | Trust Strip | index | Production |
| 11 | Filter Bar (Sticky) | browse, family | Production |
| 12 | Count Bar | browse | Production |
| 13 | Form Group (Text) | contact, quiz | Production |
| 14 | Form Row (Two-Col) | contact | Production |
| 15 | Consent Row | contact | Production |
| 16 | Option Grid | contact, quiz, configurator | Production |
| 17 | Panel (General) | Throughout | Production |
| 18 | Info Panel (Sidebar) | contact, character | Production |
| 19 | Context Card | contact, character | Production |
| 20 | Stats Display | index, family | Production |
| 21 | Ratio Stats | character, compare, body | Production |
| 22 | Compare Preview | index | Production |
| 23 | Compare Table | compare | Production |
| 24 | Status Badges | All | Production |
| 25 | Family Badges | All | Production |
| 26 | Scroll Reveal | Most pages | Production |
| 27 | Ken Burns Animation | index, browse | Production |
| 28 | Empty State | browse, compare | Production |
| 29 | Loading State | async pages | Production |
| 30 | Error Message | Error handling | Production |
| 31 | Key-Value Display | Profile sections | Production |

---

**Maintained:** June 21, 2026  
**Framework:** Vanilla HTML/CSS/JS (no build step)  
**Design System:** ZELEX Brand Standards  
**Author:** Claude Code
