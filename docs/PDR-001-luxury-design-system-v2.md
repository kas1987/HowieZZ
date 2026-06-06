# PDR-001: Luxury Design System v2

**Status:** Implemented  
**Branch:** feat/pdr-001-design-system-v2  
**File:** `assets/site.css`

---

## What Changed

### v2 Token Layer (`:root` extension)
A semantic token layer sits on top of the raw palette — use these in new components.

| Token group | Tokens |
|---|---|
| Surfaces | `--s0`…`--s3` (deepest → elevated) |
| Borders | `--b-soft`, `--b-accent`, `--b-subtle` |
| Type scale | `--t-xs`…`--t-3xl` |
| Spacing | `--sp1`…`--sp8` (4px → 64px) |
| Radii | `--r-sm` (6) · `--r-md` (10) · `--r-lg` (14) · `--r-pill` (100) |
| Shadows | `--sh-card`, `--sh-card-hover`, `--sh-focus` |
| Status | `--st-live`, `--st-concept`, `--st-pending`, `--st-estimated`, `--st-verified` |

### Card Glow — Quieted at Rest
Cards previously always emitted a gold ambient glow (`box-shadow: 0 0 26px rgba(212,165,116,.08)`).  
Now cards rest with `--sh-card` (a neutral dark shadow); glow activates only on `:hover` via `--sh-card-hover`.

### Button Hierarchy (4 variants)
| Class | Use |
|---|---|
| `.btn` | Primary — gold border, transparent fill |
| `.btn.solid` | Secondary — filled cream/gold with sheen sweep |
| `.btn.ghost` | Low-emphasis — muted border |
| `.btn.concierge` | Final CTA — Playfair italic, dark gradient, premium shadow |

### Status Primitives (`.stat`)
Five pill badges with dot indicator, colored by state:

```html
<span class="stat stat-live">Live</span>
<span class="stat stat-concept">Concept</span>
<span class="stat stat-pending">Shoot Pending</span>
<span class="stat stat-estimated">Estimated Spec</span>
<span class="stat stat-verified">Verified Spec</span>
```

### Focus States
`:focus-visible` outlines (gold, 2px, offset 3px) on all interactive elements.  
Cards additionally get `--sh-focus` shadow ring. Zero regression on no-JS/reduced-motion paths.

### Reduced-Motion
Added `transition:border-color .15s` to cards under `prefers-reduced-motion` so state still communicates without motion.

---

## Acceptance Criteria Checklist

- [x] `assets/site.css` has a documented v2 token section
- [x] Character cards and body cards: quiet at rest, glow on hover only
- [x] Buttons: primary, secondary, ghost, concierge variants
- [x] Status primitives: live, concept, pending, estimated, verified
- [x] Accessible focus states via `:focus-visible`
- [x] Reduced-motion safe (cards, reveal, ken-burns, sheen)
- [x] No-JS behavior unchanged (reveal only hidden under `.js`)

---

## Dependencies Consumed
- `assets/site.css` (modified in place — backward compat maintained)
- `assets/site.js` (unchanged)
