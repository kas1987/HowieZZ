# Design Token System Runbook

**Status:** Active (Phase 1)  
**Last Updated:** 2026-06-21  
**Owner:** Frontend Engineering Lead  
**Audience:** All developers

---

## Overview

This runbook explains how to add, modify, and debug design tokens in the ZELEX site. Tokens are centralized CSS variables defined in `:root` and referenced throughout `assets/site.css`. This enables rapid theme changes, consistency, and maintainability.

---

## Token Categories

### 1. Color Tokens (40 variables)

**Location:** `assets/site.css` — `:root` section, lines 1-45

**Categories:**
- **Primary Brand** (3): `--color-primary`, `--color-primary-dark`, `--color-primary-light`
- **Status** (5): `--st-live`, `--st-concept`, `--st-pending`, `--st-estimated`, `--st-verified`
- **Surfaces** (4): `--color-surface-0` through `--color-surface-3`
- **Text** (4): `--color-text`, `--color-text-secondary`, `--color-text-tertiary`, `--color-text-disabled`, `--color-text-inverse`
- **Borders** (3): `--color-border-soft`, `--color-border-accent`, `--color-border-subtle`
- **Semantic** (4): `--color-success`, `--color-error`, `--color-warning`, `--color-info`
- **Alert Faint** (4): `--color-success-faint`, `--color-error-faint`, `--color-warning-faint`, `--color-info-faint`

**Example:**
```css
:root {
  --color-primary: #d4a574;           /* Gold */
  --color-primary-dark: #8b6f47;      /* Dark gold */
  --color-error: #f44336;             /* Error red */
}
```

### 2. Spacing Tokens (8 variables)

**Location:** `assets/site.css` — `:root` section, lines 46-53

**Scale:** 4px grid from 4px to 64px

```css
:root {
  --sp1: 4px;    /* micro */
  --sp2: 8px;    /* extra small */
  --sp3: 12px;   /* small */
  --sp4: 16px;   /* base */
  --sp5: 24px;   /* medium */
  --sp6: 32px;   /* large */
  --sp7: 48px;   /* extra large */
  --sp8: 64px;   /* massive */
}
```

**Usage:**
```css
.card {
  padding: var(--sp5);     /* 24px */
  margin-bottom: var(--sp4); /* 16px */
}
```

### 3. Type Scale (7 variables)

**Location:** `assets/site.css` — `:root` section, lines 54-60

**Scale:** rem-based for accessible scaling

```css
:root {
  --t-xs: 0.75rem;    /* 12px */
  --t-sm: 0.875rem;   /* 14px */
  --t-base: 1rem;     /* 16px */
  --t-lg: 1.125rem;   /* 18px */
  --t-xl: 1.5rem;     /* 24px */
  --t-2xl: 2rem;      /* 32px */
  --t-3xl: 2.5rem;    /* 40px */
}
```

**Usage:**
```css
h1 { font-size: var(--t-3xl); font-weight: 700; }
label { font-size: var(--t-sm); }
```

### 4. Shadow Tokens (5 variables)

**Location:** `assets/site.css` — `:root` section, lines 61-65

```css
:root {
  --sh-card: 0 2px 8px rgba(0,0,0,.04);
  --sh-card-hover: 0 0 26px rgba(212,165,116,.08);
  --sh-focus: 0 0 0 3px rgba(212,165,116,.25);
  --sh-elevated: 0 4px 12px rgba(0,0,0,.08);
  --sh-deep: 0 8px 24px rgba(0,0,0,.12);
}
```

**Usage:**
```css
.card {
  box-shadow: var(--sh-card);
  transition: box-shadow 0.2s ease;
}
.card:hover {
  box-shadow: var(--sh-card-hover);
}
```

### 5. Border Radius Tokens (4 variables)

**Location:** `assets/site.css` — `:root` section, lines 66-69

```css
:root {
  --r-sm: 6px;        /* Small radius */
  --r-md: 10px;       /* Medium radius */
  --r-lg: 14px;       /* Large radius */
  --r-pill: 100px;    /* Pill shape */
}
```

---

## Adding a New Token

### Step 1: Identify the Need

Determine which category your token belongs to (color, spacing, type, shadow, radius).

**Example:** You need a new accent color for hover states.

### Step 2: Define in `:root`

Add the token to `assets/site.css` in the appropriate category section:

```css
:root {
  /* ... existing tokens ... */
  --color-accent-hover: #e8d4a8;  /* Light gold hover */
}
```

### Step 3: Use in Components

Reference the token via `var()` throughout the CSS:

```css
.feature:hover {
  background: var(--color-accent-hover);
  box-shadow: var(--sh-card-hover);
}
```

### Step 4: Validate

1. **Visual check:** Load all pages in browser and inspect the component
2. **Regression test:** Compare before/after using browser DevTools or Percy
3. **Accessibility check:** Verify sufficient color contrast (WCAG AA minimum 4.5:1 for text)

### Step 5: Document

Update `docs/pdr/PDR-100-design-token-system.md` with the new token:

```markdown
- **Your Category** (N): new token name and purpose
```

---

## Modifying an Existing Token

### Step 1: Check Dependencies

Search for the token name across the codebase:

```bash
grep -r "--color-primary:" . --include="*.css" --include="*.js" --include="*.html"
```

**Why?** Understand all components affected by the change.

### Step 2: Update in `:root`

Edit `assets/site.css`:

```css
:root {
  --color-primary: #c9945f;  /* Updated gold */
}
```

### Step 3: Verify Across All Pages

The change propagates instantly via CSS variable cascading. Test:

1. **Homepage** (index.html)
2. **Browse** (browse.html)
3. **Character detail** (character.html?id=…)
4. **Family** (family.html?f=…)
5. **Mobile views** (use DevTools device emulation)

### Step 4: Commit & PR

Create a focused PR with the token change:

```bash
git checkout -b chore/update-primary-color
# make changes
git add assets/site.css docs/pdr/PDR-100-design-token-system.md
git commit -m "chore(tokens): update --color-primary to #c9945f

Updates the gold accent across all components. No functional changes."
git push origin chore/update-primary-color
```

---

## Debugging Token Issues

### Issue: Color not applying

**Cause:** Token name typo or CSS specificity conflict

**Fix:**
1. Check token name spelling (case-sensitive): `--color-primary` not `--colorPrimary`
2. Verify token is defined in `:root` (browser DevTools → Inspect Element → Computed → filter by `--color`)
3. Check for inline styles overriding the token (remove inline `style="color: #xyz"`)

### Issue: Spacing inconsistent

**Cause:** Mixed use of tokens and pixel values

**Fix:**
1. Search component for hardcoded values: `grep "margin:\|padding:" component.css`
2. Replace with appropriate token: `padding: 16px` → `padding: var(--sp4)`
3. Run regression test to verify alignment

### Issue: Text too small on mobile

**Cause:** Type scale token too aggressive or not responsive

**Fix:**
1. Check media query breakpoints (768px, 480px)
2. Add mobile-specific overrides if needed:

```css
@media (max-width: 768px) {
  h1 { font-size: var(--t-2xl); }  /* Reduce from --t-3xl */
}
```

### Issue: Shadow not visible

**Cause:** Shadow token defined but not applied, or color/background conflict

**Fix:**
1. Verify element has `box-shadow: var(--sh-*)` applied
2. Check background color is not `transparent` (shadows need contrast)
3. Remove conflicting `text-shadow` or other shadow properties

---

## Accessibility Considerations

### Color Contrast

Every color token must meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text).

**Test your token:**
```
https://webaim.org/resources/contrastchecker/
```

Enter foreground (e.g., `--color-text: #1a1a1a`) and background (e.g., `--color-surface-0: #ffffff`) to verify contrast ratio.

### Type Scale

Never use `--t-xs` (12px) for body text—use `--t-base` (16px) minimum for readability.

### Motion Preferences

Tokens do not control animation duration. For reduced-motion support, add:

```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0s !important; transition-duration: 0s !important; }
}
```

---

## Token vs. Inline Styles

### Rule: Always use tokens

**Bad:**
```html
<div style="color: #d4a574; padding: 24px; font-size: 16px;">Text</div>
```

**Good:**
```css
.fancy-box {
  color: var(--color-primary);
  padding: var(--sp5);
  font-size: var(--t-base);
}
```

**Why?** Tokens enable:
- Global theme updates with one change
- Consistency across components
- Accessibility auditing
- Maintainability

---

## Common Workflows

### Workflow 1: Add a new component with tokens

```css
/* In assets/site.css or page-specific <style> block */
.my-component {
  padding: var(--sp4);
  background: var(--color-surface-1);
  border: 1px solid var(--color-border-soft);
  border-radius: var(--r-md);
  box-shadow: var(--sh-card);
  font-size: var(--t-sm);
  color: var(--color-text-secondary);
}

.my-component:hover {
  box-shadow: var(--sh-card-hover);
}
```

### Workflow 2: Create a dark mode variant

Define new tokens for dark mode:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #ffffff;
    --color-surface-0: #1a1a1a;
    --color-background: #0a0a0a;
  }
}
```

All components using tokens automatically adapt.

### Workflow 3: Audit token usage

Find all components using a specific token:

```bash
grep -r "--color-primary" assets/ --include="*.css"
grep -r "var(--color-primary)" . --include="*.html" --include="*.js"
```

---

## Testing Tokens

### Pre-Commit Checks

```bash
# 1. Lint CSS (check for missing tokens)
python -m py_compile assets/site.css

# 2. Run full test suite
npm test

# 3. Visual regression (if available)
# npx percy snapshot
```

### Manual Regression Testing

1. Open [http://localhost:8000/index.html](http://localhost:8000/index.html)
2. Take before/after screenshots of:
   - Homepage hero
   - Character cards (browse.html)
   - Body comparison (compare.html)
   - Quiz results (quiz.html)
3. Compare pixel-perfect using browser diff tools

---

## Token Documentation

Keep `docs/pdr/PDR-100-design-token-system.md` as the single source of truth for:
- All token definitions
- Token naming conventions
- Migration strategy (if refactoring)
- Usage examples

---

## FAQ

**Q: Can I create a token for a one-off color?**

A: No. Only create tokens for values that repeat 2+ times or represent a brand intent (e.g., "error", "success"). One-off colors suggest the design is inconsistent.

**Q: What if I need a color between two tokens?**

A: Stop and reconsider. Tokens enforce consistency. If you need a color between `--sp4 (16px)` and `--sp5 (24px)`, you likely need to update the scale, not add a one-off value.

**Q: Can I override a token in a media query?**

A: Yes, but sparingly. Example:

```css
@media (max-width: 768px) {
  :root {
    --sp5: 16px;  /* Reduce padding on mobile */
  }
}
```

**Q: How do I revert a broken token change?**

A: Use git:

```bash
git log --oneline assets/site.css  # Find the commit
git revert <commit-hash>           # Create a new commit reverting it
git push
```

---

## References

- **Source PDR:** `docs/pdr/PDR-100-design-token-system.md`
- **Style Guide:** `CONTRIBUTING.md` (token section)
- **Color Checker:** https://webaim.org/resources/contrastchecker/
- **Token Best Practices:** https://www.designtokens.org/

---

## Support

For token questions:
1. Check this runbook (search by keyword)
2. Review `docs/pdr/PDR-100-design-token-system.md`
3. Ask in team Slack / open an issue: `feat(tokens): [your question]`
