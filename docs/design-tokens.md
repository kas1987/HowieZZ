# Design Token System — ZELEX Atlas

**Status:** Refactored & Centralized  
**Reduction:** 647 lines → 395 lines (39% reduction)  
**Type:** CSS Custom Properties (:root variables)  
**Authority:** `/assets/site.css` — all tokens defined in `:root` block only

---

## Overview

The ZELEX design system is fully token-based. All values (colors, spacing, typography, shadows, transitions, z-indices) are declared once in `:root` as CSS custom properties. Rules use only `var(--token-name)` — no hardcoded values.

**Key principle:** If a value appears in a rule, it should be a token variable. If you need the same value twice, create a token alias.

---

## Color System

### Primary Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary-blue` | `#5EA6E8` | Brand emphasis, section headers, signatures |
| `--color-primary-coral` | `#E18B73` | Accent warm, error/warning states |
| `--color-primary-gold` | `#D4A574` | Primary CTA, borders, active states |
| `--color-primary-cream` | `#F7E3C3` | Light text on dark, premium button fill |

### Surface Hierarchy (Dark Theme)

| Token | Value | Usage |
|-------|-------|-------|
| `--color-surface-0` | `#0d0d0d` | Deepest backgrounds (image placeholders) |
| `--color-surface-1` | `#121212` | Page background (body) |
| `--color-surface-2` | `#1b1b1b` | Cards, panels, primary containers |
| `--color-surface-3` | `#242424` | Secondary surfaces, striped tables |
| `--color-surface-overlay` | `#141312` | Configurator stage, overlay regions |

### Text Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-text-primary` | `#e8e8e8` | Body text, headings |
| `--color-text-muted` | `#ababab` | Secondary labels, hints, metadata |
| `--color-text-inverted` | `#111` | Dark text on light (skip-link, button.solid) |
| `--color-text-placeholder` | `#6f6f6f` | Form input placeholders |

### Borders

| Token | Value | Usage |
|-------|-------|-------|
| `--color-border-strong` | `#333` | Primary borders (inputs, dividers) |
| `--color-border-subtle` | `rgba(255,255,255,.02)` | Light overlay borders |

### Body Family Classifications (WHR/BWR)

| Token | Value | Family |
|-------|-------|--------|
| `--color-family-classic` | `#8FB7E0` | Classic body (blue tone) |
| `--color-family-icon` | `#D4A574` | Icon body (gold tone) |
| `--color-family-muse` | `#9FD6B6` | Muse body (green tone) |
| `--color-family-siren` | `#E18B73` | Siren body (coral tone) |
| `--color-family-empress` | `#C792D6` | Empress body (orchid tone) |
| `--color-family-sculpt` | `#C7B07F` | Sculpt body (beige tone) |

### Status Palette (Buyer Trust Signals)

Five honest, visually distinct states — hue + visual weight ensure they are never mistaken:

| Token | Value | State | Dot | Ring |
|-------|-------|-------|-----|------|
| `--color-status-live` | `#6BC88A` | In catalog, available | filled | solid |
| `--color-status-verified` | `#5EA6E8` | Confirmed + shot, real | filled | solid |
| `--color-status-pending` | `#E0A945` | Promised, shoot pending | filled | dashed |
| `--color-status-estimated` | `#C792D6` | Data interpolated | hollow | solid |
| `--color-status-concept` | `#9EA8B8` | Concept only, quietest | hollow | solid |

### Semantic Aliases

```css
--color-accent: var(--color-primary-gold);           /* Primary focus color */
--color-accent-warm: var(--color-primary-coral);     /* Warm accent (error/warning) */
--color-emphasis: var(--color-primary-blue);         /* Section headers */
```

---

## Typography

### Font Families

| Token | Value | Usage |
|-------|-------|-------|
| `--font-sans` | `'Montserrat', system-ui, sans-serif` | Body, UI labels |
| `--font-serif` | `'Playfair Display', Georgia, serif` | Headings, premium text |
| `--font-serif-italic` | `'Playfair Display', serif` | Italic serif text |
| `--font-mono` | `ui-monospace, monospace` | Code, technical values |

### Type Scale (0.875rem base, 1.2x multiplier)

| Token | Value (rem) | Value (px) | Usage |
|-------|-------------|-----------|-------|
| `--size-text-xs` | 0.625 | 10 | Badge labels, tiny text |
| `--size-text-sm` | 0.75 | 12 | UI labels, small text |
| `--size-text-base` | 0.875 | 14 | Body text, form inputs |
| `--size-text-md` | 1 | 16 | Larger body, nav |
| `--size-text-lg` | 1.25 | 20 | Card titles, smaller headings |
| `--size-text-xl` | 1.75 | 28 | Panel titles, section heads |
| `--size-text-2xl` | 2.375 | 38 | Large section headings |
| `--size-text-3xl` | 3.25 | 52 | Hero titles |

### Line Height Constants

| Token | Value | Usage |
|-------|-------|-------|
| `--line-height-tight` | 1.1 | Headings, display text |
| `--line-height-normal` | 1.6 | Body text (default) |
| `--line-height-relaxed` | 1.7 | Large body, intro text |
| `--line-height-readable` | 1.55 | Long-form prose, list items |

### Letter Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--letter-spacing-normal` | normal | Default, no override |
| `--letter-spacing-tight` | 0.5px | Compact labels |
| `--letter-spacing-loose` | 1px | Build lists, form values |
| `--letter-spacing-wider` | 1.5px | Stat badges, field labels |
| `--letter-spacing-widest` | 2px | Nav links, button labels |
| `--letter-spacing-ultra` | 4px | Brand eyebrows |
| `--letter-spacing-hero` | 5px | Extra-wide decorative |

---

## Spacing Scale

Modular 4px base with 8-step scale. All padding/margin/gaps use these tokens.

| Token | Value | Multiplier |
|-------|-------|-----------|
| `--spacing-1` | 4px | ×1 |
| `--spacing-2` | 8px | ×2 |
| `--spacing-3` | 12px | ×3 |
| `--spacing-4` | 16px | ×4 |
| `--spacing-5` | 24px | ×6 |
| `--spacing-6` | 32px | ×8 |
| `--spacing-7` | 48px | ×12 |
| `--spacing-8` | 64px | ×16 |

---

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 6px | Small pills, badges |
| `--radius-md` | 10px | Buttons, input fields |
| `--radius-lg` | 14px | Cards, panels |
| `--radius-xl` | 18px | Large feature cards |
| `--radius-pill` | 100px | Pills, full-round buttons |
| `--radius-large-card` | 20px | Configurator stage |

---

## Shadows

All shadows use `rgba(0,0,0,alpha)` with soft blur for depth.

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-card-rest` | `0 2px 10px rgba(0,0,0,.45)` | Card resting state |
| `--shadow-card-hover` | `0 16px 40px rgba(0,0,0,.6), 0 0 28px rgba(212,165,116,.14)` | Card on hover (lift + warm halo) |
| `--shadow-card-outline` | `0 0 0 3px rgba(212,165,116,.35)` | Focus ring outline |
| `--shadow-panel` | `0 1px 3px rgba(0,0,0,.4)` | Panel, inset surface |
| `--shadow-nav-scroll` | `0 8px 28px rgba(0,0,0,.45)` | Nav after scroll |
| `--shadow-drawer` | `-18px 0 50px rgba(0,0,0,.5)` | Mobile drawer |
| `--shadow-drop-small` | `0 4px 18px rgba(0,0,0,.45)` | Small drop |
| `--shadow-drop-large` | `0 8px 28px rgba(0,0,0,.55)` | Large drop (concierge button) |

**Design principle:** Cards are quiet at rest (single soft drop). On hover, they lift with a deeper shadow + faintest warm halo (212,165,116 at 14% opacity) — luxury signal without casino loudness.

---

## Layout

| Token | Value | Usage |
|-------|-------|-------|
| `--max-width` | 1340px | Main container max-width |

---

## Transitions

### Duration

| Token | Value | Purpose |
|-------|-------|---------|
| `--transition-fast` | .15s | Accessibility (reduced-motion use only) |
| `--transition-base` | .2s | Standard UI feedback |
| `--transition-smooth` | .25s | Card hover, color shifts |
| `--transition-reveal` | .6s cubic-bezier(.22,.61,.36,1) | Scroll reveal animations |
| `--transition-drawer` | .32s cubic-bezier(.22,.61,.36,1) | Mobile drawer slide |
| `--transition-modal-scrim` | .2s ease | Scrim fade |

### Easing Functions

| Token | Value | Purpose |
|-------|-------|---------|
| `--transition-easing-reveal` | cubic-bezier(.22,.61,.36,1) | Smooth in/out for entrance |
| `--transition-easing-cubic` | cubic-bezier(.34,1.1,.64,1) | Bouncy, playful (SVG paths) |

---

## Z-Index Stack

Predictable, non-competing layers:

| Token | Value | Layer |
|-------|-------|-------|
| `--z-base` | 1 | Content, default |
| `--z-sticky` | 2 | Sticky headers, table headers |
| `--z-overlay` | 50 | Nav (sticky) |
| `--z-drawer-close` | 55 | Mobile nav scrim |
| `--z-drawer-open` | 60 | Mobile nav drawer |
| `--z-menu` | 100 | Skip-link, top-level UI |

**Rule:** Always use tokens. Never write raw `z-index: 999` or duplicate values.

---

## Form Field System

Coherent field styling for contact, quiz, and future panels:

| Token | Value | Purpose |
|-------|-------|---------|
| `--form-field-bg` | `#161616` | Input background |
| `--form-field-border` | `var(--color-border-strong)` | Input border at rest |
| `--form-field-radius` | `var(--radius-md)` | Input border-radius |
| `--form-field-padding` | `12px 14px` | Input padding |
| `--form-field-focus-ring` | `0 0 0 2px rgba(212,165,116,.16)` | Focus ring on input |
| `--form-field-error-ring` | `0 0 0 2px rgba(225,139,115,.16)` | Error ring on input |

---

## Animation Durations

| Token | Value | Usage |
|-------|-------|-------|
| `--anim-kenburns-duration` | 36s | Hero backdrop slide |
| `--anim-cfg-drift-duration` | 9s | Configurator glow drift |
| `--anim-cfg-pop-duration` | .22s | Configurator tip pop-in |

---

## Backdrop Filters

| Token | Value | Usage |
|-------|-------|-------|
| `--backdrop-blur-nav` | `blur(10px)` | Nav, drawer background |
| `--backdrop-blur-drawer` | `blur(14px)` | Mobile drawer (stronger) |
| `--backdrop-blur-thin` | `blur(1px)` | Scrim overlay |

---

## Usage Examples

### Adding a new component

1. **Identify all hardcoded values** in your rule:
   ```css
   .my-component {
     background: #1b1b1b;           /* ← hardcoded */
     padding: 16px 24px;            /* ← hardcoded */
     border-radius: 10px;           /* ← hardcoded */
     box-shadow: 0 2px 10px rgba(0,0,0,.45);  /* ← hardcoded */
   }
   ```

2. **Replace with tokens**:
   ```css
   .my-component {
     background: var(--color-surface-2);
     padding: var(--spacing-4) var(--spacing-5);
     border-radius: var(--radius-md);
     box-shadow: var(--shadow-card-rest);
   }
   ```

3. **If a token is missing**, add it to `:root`:
   - New color? → `--color-feature-name`
   - New spacing? → Adjust to fit modular scale, or add `--spacing-9: 80px`
   - New shadow? → Define once, reuse everywhere

### Consistency checks

Before commit, grep for hardcoded values:
```bash
# Find hex colors not in :root
grep -n '#[0-9A-Fa-f]\{6\}' assets/site.css | grep -v ':root'

# Find hardcoded px values (will need manual review)
grep -n '[0-9]\+px' assets/site.css | head -20
```

Some hardcoded values are intentional (e.g., specific keyframe transforms, grid-template values). Only replace if they appear multiple times.

---

## Refactoring Notes

**Original:** 647 lines, mixed hardcoded + token approach  
**Refactored:** 395 lines, 100% token-based

### Changes

1. **Centralized all color definitions** — removed duplicates, added semantic aliases
2. **Unified typography** — all font sizes, weights, spacing use `:root` variables
3. **Shadow standardization** — 8 shadows defined, reused across all interactive surfaces
4. **Z-index cleanup** — predictable stack, no competing values
5. **Transition unification** — consistent timing across the design
6. **Form field consolidation** — one source of truth for input styling

### Browser Support

All CSS custom properties (100% of this system) require modern browsers:
- Chrome 49+
- Firefox 31+
- Safari 9.1+
- Edge 15+

**Fallback strategy:** Include prefixed versions for older Safari if required.

---

## Maintenance

### Adding a new token

1. Declare in `:root` block (group by category)
2. Document in this file (add row to relevant table)
3. Use `var(--token-name)` in all rules
4. Never duplicate a value across rules

### Deprecating a token

1. Search for usage: `grep -r "var(--old-token)" .`
2. Replace all usage with new token
3. Remove from `:root`
4. Update this doc

### Validating tokens

Before release, ensure:
- No hardcoded colors in rules (except transparent, currentColor)
- No repeated values across rules
- All new features use token-based approach
- Test in both light/dark modes (if applicable)

---

## Quick Reference: Most-Used Tokens

```css
/* Colors */
var(--color-primary-gold)      /* Primary CTA, borders */
var(--color-text-primary)      /* Body text */
var(--color-text-muted)        /* Secondary labels */
var(--color-surface-2)         /* Card/panel backgrounds */

/* Spacing */
var(--spacing-4)               /* Standard margin/padding */
var(--spacing-5)               /* Larger sections */

/* Radius */
var(--radius-md)               /* Buttons, inputs */
var(--radius-lg)               /* Cards, panels */

/* Shadows */
var(--shadow-card-rest)        /* Card at rest */
var(--shadow-card-hover)       /* Card on hover */

/* Transitions */
var(--transition-smooth)       /* Standard animation */

/* Typography */
var(--font-sans)               /* Body font */
var(--font-serif)              /* Heading font */
var(--size-text-base)          /* Body font size */
```

---

**Last updated:** 2026-06-21  
**Maintained by:** Design Systems Team  
**Repository:** E:\HowieZZ\.claude\worktrees\amazing-tu-a4bd34
