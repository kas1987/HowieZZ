# ZELEX Fragment Library — Quick Reference

**Fast lookup for copy-paste fragments and common patterns.**

---

## Fragment Checklist (30 Components)

- [x] Header Hero
- [x] Breadcrumbs
- [x] Section Headers (Eyebrow + Title)
- [x] Button Group (Solid/Ghost/Outline)
- [x] Concierge Band CTA
- [x] Character Card
- [x] Body Card
- [x] Family Card (Active & Dev states)
- [x] Intent Card Router
- [x] Trust Strip (4-item confidence signals)
- [x] Filter Bar (Sticky with pills)
- [x] Count Bar (Result summary + compare quick)
- [x] Form Group (Text input with hint/error)
- [x] Form Row (Two-column layout)
- [x] Consent Row (Checkbox)
- [x] Option Grid (Multi-select cards)
- [x] Panel (Standard & Accent variants)
- [x] Info Panel (Sticky sidebar)
- [x] Context Card (Character/body preview)
- [x] Stats Display (Numeric KPIs)
- [x] Ratio Stats (WHR/BWR with icons)
- [x] Compare Preview (Two-column highlight)
- [x] Compare Table (Horizontal metric table)
- [x] Status Badges (5 types: live, verified, pending, estimated, concept)
- [x] Family Badges (6 families + unclassified)
- [x] Scroll Reveal (Staggered animation d1–d6)
- [x] Ken Burns Hero Background (infinite zoom)
- [x] Empty State (No results + action)
- [x] Key-Value Display (Definition list)
- [x] Loading / Error States

---

## Copy-Paste Snippets

### Quick Hero
```html
<header class="hero">
  <div class="inner">
    <div class="eyebrow">Subtitle</div>
    <h1>Page Title <span class="em-grad">Emphasis</span></h1>
    <p>Description (max 80 words).</p>
    <div class="cta">
      <a class="btn solid" href="#">Primary</a>
      <a class="btn" href="#">Secondary</a>
      <a class="btn ghost" href="#">Tertiary</a>
    </div>
  </div>
</header>
```

### Quick Card
```html
<a class="card" href="#">
  <div class="imgwrap">
    <img src="img.jpg" alt="">
    <span class="repbadge">Live</span>
  </div>
  <div class="b">
    <div class="pname-row">
      <span class="pname">Title</span>
      <div class="card-meta-rail">
        <span class="stat stat-live">Status</span>
      </div>
    </div>
    <div class="ptitle">Subtitle</div>
    <div class="ptag">Tagline</div>
  </div>
</a>
```

### Quick Panel
```html
<div class="panel panel--accent">
  <h3>Title</h3>
  <p>Content...</p>
</div>
```

### Quick Form Group
```html
<div class="form-group">
  <label for="field">Label <span class="req">*</span></label>
  <input type="text" id="field">
  <div class="field-hint">Optional hint text</div>
  <div class="field-err show">Error message</div>
</div>
```

### Quick Button Set
```html
<div style="display: flex; gap: 12px; flex-wrap: wrap;">
  <a class="btn solid" href="#">Primary</a>
  <a class="btn" href="#">Secondary</a>
  <a class="btn ghost" href="#">Ghost</a>
</div>
```

---

## CSS Custom Properties (Always Use These)

| Token | Value | Use |
|-------|-------|-----|
| `--color-primary-blue` | #5EA6E8 | Accents, section heads, links |
| `--color-primary-gold` | #D4A574 | Primary accent, borders |
| `--color-primary-coral` | #E18B73 | Error, alerts, warnings |
| `--color-primary-cream` | #F7E3C3 | Light text, highlights |
| `--color-surface-1` | #121212 | Page background |
| `--color-surface-2` | #1b1b1b | Card/panel background |
| `--color-text-primary` | #e8e8e8 | Body text |
| `--color-text-muted` | #ababab | Hint/secondary text |
| `--color-border-strong` | #333 | Card borders |
| `--color-border-subtle` | rgba(255,255,255,0.02) | Faint lines |
| `--font-serif` | 'Playfair Display', Georgia | Headings |
| `--font-sans` | 'Montserrat', system-ui | Body text |
| `--size-text-xs` | 0.625rem | 10px |
| `--size-text-sm` | 0.75rem | 12px |
| `--size-text-base` | 0.875rem | 14px |
| `--size-text-md` | 1rem | 16px |
| `--size-text-lg` | 1.25rem | 20px |
| `--spacing-1` | 4px | Tiny gap |
| `--spacing-3` | 12px | Small gap |
| `--spacing-4` | 16px | Medium gap |
| `--spacing-5` | 24px | Large gap |
| `--spacing-6` | 32px | XL gap |
| `--radius-sm` | 6px | Small radius |
| `--radius-md` | 10px | Medium radius |
| `--radius-lg` | 14px | Large radius |
| `--radius-pill` | 100px | Fully rounded |
| `--shadow-card-rest` | 0 2px 10px rgba(0,0,0,0.45) | Card default |
| `--shadow-card-hover` | 0 16px 40px rgba(0,0,0,0.6),... | Card hover |
| `--transition-smooth` | 0.25s | Hover animations |
| `--transition-reveal` | 0.6s cubic-bezier(...) | Scroll-in animation |
| `--max-width` | 1340px | Container max-width |

---

## Responsive Breakpoints (Don't Hardcode!)

```css
@media(max-width: 1120px) { /* Large tablets */ }
@media(max-width: 980px)  { /* Tablets */ }
@media(max-width: 820px)  { /* Smaller tablets */ }
@media(max-width: 720px)  { /* Small tablets */ }
@media(max-width: 680px)  { /* Large phones */ }
@media(max-width: 620px)  { /* Standard phones */ }
@media(max-width: 560px)  { /* Small phones */ }
@media(max-width: 480px)  { /* Extra small */ }
```

---

## Grid Templates (Common Patterns)

### 4-Column Card Grid (Auto-responsive)
```css
.grid.g4 {
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}
@media(max-width: 980px) { .grid.g4 { grid-template-columns: repeat(2, 1fr); } }
@media(max-width: 520px) { .grid.g4 { grid-template-columns: 1fr; } }
```

### 2-Column Layout (Text + Sidebar)
```css
.layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
  align-items: start;
}
@media(max-width: 900px) { .layout { grid-template-columns: 1fr; } }
```

### Flex Row (Buttons)
```css
.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}
```

---

## Color Palettes (Family Colors)

```css
/* Applied via --fam-color or inline */
--color-family-classic: #8FB7E0;  /* Blue */
--color-family-icon:    #D4A574;  /* Gold */
--color-family-muse:    #9FD6B6;  /* Green */
--color-family-siren:   #E18B73;  /* Coral */
--color-family-empress: #C792D6;  /* Purple */
--color-family-sculpt:  #C7B07F;  /* Tan */
```

**Usage:**
```html
<span class="fam fam--classic">The Classic</span>
<!-- OR -->
<div style="color: var(--color-family-muse);">The Muse</div>
```

---

## Status Badge Types

| Class | Color | Use |
|-------|-------|-----|
| `.stat-live` | Green (#6BC88A) | Character is photographed |
| `.stat-verified` | Blue (#5EA6E8) | Body measurement verified |
| `.stat-pending` | Orange (#E0A945) | Awaiting confirmation |
| `.stat-estimated` | Purple (#C792D6) | Estimated dimensions |
| `.stat-concept` | Gray (#9EA8B8) | In development / placeholder |

**Usage:**
```html
<span class="stat stat-live">Live</span>
<span class="stat stat-verified">Verified</span>
<span class="stat stat-pending">Estimated</span>
```

---

## Form Field States

### Normal
```html
<input type="text" placeholder="Enter value">
```

### Focus (Auto)
```css
border-color: var(--color-primary-gold);
box-shadow: var(--form-field-focus-ring);
```

### Error
```html
<input class="err-field" type="text">
<div class="field-err show">Required field</div>
```

```css
.err-field {
  border-color: var(--color-primary-coral);
  box-shadow: var(--form-field-error-ring);
}
```

### Disabled
```html
<input type="text" disabled>
```

---

## Animation Classes

### Scroll Reveal (Staggered)
```html
<div class="reveal d1">Fades in 1st</div>
<div class="reveal d2">Fades in 2nd</div>
<div class="reveal d3">Fades in 3rd</div>
<!-- etc. -->
```

**JS Initialize:**
```javascript
ZX.revealInit();
```

### Hero Background Ken Burns
```html
<header class="has-backdrop">
  <div class="backdrop" style="background-image: url(...)"></div>
  <!-- content -->
</header>
```

---

## Accessibility Checklist

✅ **Always include:**
- `alt` text on images
- `for` attribute on labels (linked to `id`)
- `aria-pressed`, `aria-label`, `aria-live` on interactive elements
- Semantic HTML (`<button>`, not `<a onclick>`)
- Focus visible state (auto via site.css)

✅ **Test with:**
- Tab navigation
- Screen reader (NVDA/JAWS)
- Keyboard only
- High contrast mode
- Reduced motion preference

---

## Common Mistakes to Avoid

### ❌ Don't
```css
.card { background: #1b1b1b; } /* Hardcoded color */
.btn { padding: 12px 26px; } /* Hardcoded spacing */
.heading { font-size: 28px; } /* Hardcoded size */
@media(max-width: 768px) { } /* Non-standard breakpoint */
```

### ✅ Do
```css
.card { background: var(--color-surface-2); }
.btn { padding: var(--spacing-4) var(--spacing-5); }
.heading { font-size: clamp(24px, 4vw, 36px); }
@media(max-width: 820px) { }
```

---

## Production Checklist

Before shipping a new page:

- [ ] All colors use CSS variables
- [ ] Responsive tested at 5+ breakpoints (480, 680, 820, 980, 1120px)
- [ ] Focus states visible on all interactive elements
- [ ] Images optimized and have `alt` text
- [ ] Forms have labels and error states defined
- [ ] Empty states designed (no results, loading, error)
- [ ] Dark mode contrast passes WCAG AA (4.5:1 text)
- [ ] No hardcoded font sizes (use `clamp()` or `var(--size-text-*)`)
- [ ] Animations work with `prefers-reduced-motion: reduce`
- [ ] All external links have security attributes (`rel="noopener"`)
- [ ] Page load performance monitored (images lazy-loaded where possible)
- [ ] Link colors distinct from surrounding text (gold accent)

---

## File Structure Reference

```
amazing-tu-a4bd34/
├── assets/
│   ├── site.css              ← All design tokens + reusable classes
│   └── site.js               ← ZX namespace, helpers
├── docs/
│   ├── FRAGMENT_LIBRARY.md   ← Full documentation (THIS)
│   ├── FRAGMENT_QUICK_REF.md ← Quick lookup (you are here)
│   └── fragment-showcase.html ← Interactive demo
├── db/
│   ├── catalog.json
│   ├── characters.json
│   └── families.json
├── index.html                ← Homepage (longest page, most fragments)
├── browse.html               ← Character grid + filters
├── character.html            ← Character detail
├── family.html               ← Family index
├── compare.html              ← Body comparison tool
├── contact.html              ← Inquiry form
├── quiz.html                 ← Persona quiz
├── series.html               ← Series landing
├── body.html                 ← Body detail
├── options.html              ← Customization guide
└── [other pages...]
```

---

## Quick Links

- 📖 **Full Documentation:** [`FRAGMENT_LIBRARY.md`](FRAGMENT_LIBRARY.md)
- 🎨 **Interactive Showcase:** [`fragment-showcase.html`](fragment-showcase.html) (open in browser)
- 🎯 **Design System:** [`assets/site.css`](../assets/site.css) (350 lines, all tokens)
- 🔧 **Shared JS:** [`assets/site.js`](../assets/site.js) (ZX namespace)

---

## Support

For questions on:
- **Component usage:** Check `FRAGMENT_LIBRARY.md` section
- **CSS tokens:** Search `assets/site.css` for `:root`
- **Visual examples:** Open `fragment-showcase.html` in a browser
- **Implementation:** Find nearest existing page for reference

---

**Last Updated:** June 21, 2026  
**Status:** 30/30 fragments documented & production-ready
