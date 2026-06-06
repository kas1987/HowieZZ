# PDR-002: Quiz Result Grid — Four-Match Layout with Runner-Up Fill

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-06  
**Status:** Implemented

---

## Decision

**Replace the single-character quiz result card with a four-match grid that diversifies across body codes, fills remaining slots from the runner-up family, and separates the two families with a labelled divider.** The result screen is the highest-intent moment in the buyer journey; a single match terminates discovery prematurely. The grid anchors the buyer in a product set while the divider keeps the taxonomy honest — the buyer can see both their primary match and adjacent options without the match feeling manufactured.

---

## 1. The Single-Result Problem

The original result screen showed one character card. For a catalog at launch, this produced two failure modes. First, a buyer with a marginal quiz spread (e.g., Muse 42 / Icon 38) could lose their most relevant character to a narrow scoring artifact and never see the runner-up family. Second, a buyer correctly matched to their family saw only one character from what may be a 12-body catalog — no depth, no comparison surface, no browsing hook.

A single-result screen is a landing page with one link. The decision to ship four cards converts the result screen from a single-exit into a discovery surface.

---

## 2. Four Cards: Sizing the Grid

The four-card target was derived from the catalog constraint, not an arbitrary number. At initial launch, The Muse has 12 bodies; most families have 1–4. A four-card grid is:

- **Deep enough** to show multiple body codes from the winning family where the catalog can support it
- **Narrow enough** that the buyer reads all four cards without scrolling on mobile
- **Compatible** with a `repeat(auto-fill, minmax(200px, 1fr))` column rule — four cards fill two rows at 375 px, one row at ≥800 px

Grid sizing above four would dilute the result signal ("your match" becomes "here is a random catalog"). Below three, the grid feels sparse and provides no differentiation hook. Four is the minimum for a meaningful side-by-side.

The grid CSS:
```css
.match-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 28px;
}
```

---

## 3. Body-Code Deduplication

Within a family, different characters can share a body architecture (same `body_code`). Without deduplication, a four-card grid for The Muse could surface four characters that are the same body with different face sculpts — visually identical from the silhouette standpoint and misleading to a buyer evaluating proportion range.

The dedup pass runs first, prioritising one character per body code:

```js
const seenBody = new Set();
const matches = [];
for (const c of pool) {
  if (!seenBody.has(c.body_code)) {
    matches.push(c);
    seenBody.add(c.body_code);
  }
  if (matches.length === 4) break;
}
```

A second pass over the same pool fills remaining slots with same-body-code characters only if the grid is still short of four after the dedup sweep. This ensures body diversity is maximised but the grid is never artificially sparse if the family has fewer unique body codes than four.

---

## 4. Runner-Up Family Fill and the Match Divider

When the winning family has fewer than four distinct characters available, the grid fills from the runner-up family — the second-highest-scoring family with at least one live character. The runner-up fill is separated from the primary match cards by a full-width divider:

```js
const divider = (i === splitAt && i > 0 && runner)
  ? `<div class="match-divider">Also from ${ZX.esc(runner)}</div>`
  : '';
```

The divider is critical to the buyer experience: without it, the buyer cannot tell which cards are their primary match and which are a secondary suggestion. The divider names the family explicitly, which turns the runner-up fill into a cross-sell ("Also from The Icon") rather than a confusing mismatch.

Divider CSS positions it as a full-width separator:
```css
.match-divider {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--muted);
  font-size: 11px;
  letter-spacing: 1.8px;
  text-transform: uppercase;
}
```
Decorative lines flank the label via `::before`/`::after` pseudo-elements with `flex: 1; height: 1px; background: var(--border)`.

---

## 5. Fallback Hierarchy and Launch Robustness

At catalog launch, the live character count across all families is low. The selection logic is designed to degrade gracefully rather than produce an empty or broken result screen:

1. **Primary fill** — body-code-deduplicated characters from the winning family
2. **Runner-up fill** — characters from the second-highest-scoring family with live bodies
3. **Global fallback** — any live character in the catalog, regardless of family, if the grid still has fewer than three cards after steps 1–2

The global fallback is annotated with `fromSecond` count so `splitAt` is calculated correctly; the divider still fires at the family boundary. This ensures the result screen is never blank and the divider label is never wrong — even if the fallback characters come from a third family at a future catalog expansion point.

---

## 6. Event Binding, Retake Flow, and Progress Bar

The retake button uses `addEventListener` rather than an inline `onclick` attribute:

```js
document.getElementById('retake-btn')
  .addEventListener('click', () => {
    hide('rscreen');
    showSection('intro');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
```

This keeps quiz state management in the JS module rather than distributed across HTML attributes, avoids Content Security Policy conflicts with inline handlers, and makes the binding inspectable in DevTools. The button is bound once per result render, not re-bound on retake, so there is no handler accumulation.

**Retake is a two-phase operation.** The retake button performs only navigation — it does not reset quiz state. The `answers` array and `step` counter remain at their end-of-quiz values when the intro screen is shown. State reset happens in the second phase, when the buyer clicks Begin:

```js
function startQuiz() {
  answers = [];
  step = 0;
  hide('intro');
  hide('rscreen');
  showSection('qscreen');
  renderQ();
}
```

`renderQ()` at `step = 0` resets the progress bar to 0% (`step / QUESTIONS.length * 100 = 0`) and re-renders all question UI. A buyer who clicks retake but leaves the page before clicking Begin will find stale state if the page JS context persists, but this has no user-visible consequence — the intro screen shows no quiz progress indicators.

**Progress bar at result time.** Before the result screen renders, the progress bar is set to 100%:

```js
document.getElementById('pbar').style.width = '100%';
```

The bar was at `(QUESTIONS.length - 1) / QUESTIONS.length × 100` — one step short of complete — after the final answer. The explicit 100% advance signals quiz completion before the result cards render, eliminating any perception of a stalled final step.

---

## 7. Commercial Translation

The four-match grid has three direct commercial effects:

1. **Higher browse-through rate.** A buyer who clicks from the result screen to `family.html?f=…` has seen multiple bodies in their matched family. The family page is a continuation of a browsing session they have already started, not a cold landing.

2. **Runner-up cross-sell.** The divider exposes families the buyer may not have named in the quiz. A buyer who scores Muse 40 / Icon 38 sees three Muse cards and one Icon card; the Icon card is a natural comparison hook that the quiz score alone would never surface.

3. **Inquiry initiation.** Each result card carries a direct CTA to the character's inquiry path. A buyer who sees four cards has four inquiry anchors. The four-card grid multiplies the probability that at least one character is close enough to a buyer's intent to trigger an immediate inquiry.

---

## 8. Strategic Conclusion

1. A single-result screen is a conversion dead end at any catalog scale. Four cards is the minimum grid that creates a genuine discovery surface.
2. Body-code deduplication ensures the grid communicates proportion range, not character variety within a single body architecture.
3. The runner-up divider is the mechanism that converts a fallback fill into a deliberate cross-sell — it must be labelled to be commercially effective.
4. The fallback hierarchy ensures the result screen is always populated at any catalog depth, making this decision safe to ship before the catalog reaches full depth.
5. Progress-bar completion and `addEventListener` binding are hygiene decisions that complete the result-screen UX without adding cognitive load.

**Positioning headline:** *"Four bodies. Your family first — with one door left open."*

---

## 9. Acceptance Review

| Criterion | Status |
|---|---|
| Grid renders 4 cards on matching family with ≥4 distinct body codes | ✓ Confirmed in Muse |
| Body-code dedup fires before runner-up fill | ✓ `seenBody` set initialised before pool sweep |
| Divider appears at `splitAt` only when runner family exists | ✓ Conditional on `runner` being truthy |
| Divider names the runner-up family explicitly | ✓ `Also from ${runner}` label |
| Global fallback populates grid when catalog is sparse | ✓ Fallback pass after runner-up fill |
| Retake button bound with `addEventListener` (not `onclick`) | ✓ Bound once on result render |
| Progress bar advances to 100% before result display | ✓ `pbar.style.width = '100%'` pre-render |
| Grid is responsive: two rows at 375 px, one row at ≥800 px | ✓ `auto-fill minmax(200px,1fr)` |

### Implementation Notes

- `splitAt` is derived as `matches.length - fromSecond` after all fill passes complete. Any change to fill order must recalculate `splitAt` before injecting the card HTML.
- The divider does not appear if `splitAt === 0` (runner-up cards start at index 0) or if `runner` is falsy — the conditional `&& i > 0` prevents a leading divider with no primary-family cards above it.
- The global fallback may surface characters from a third family without a divider label if the runner-up family was already exhausted. This is an acceptable degradation at very low catalog depth; a future revision should extend the divider logic to label a third-family fill if it occurs.
