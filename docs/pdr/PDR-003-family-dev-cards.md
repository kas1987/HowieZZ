# PDR-003: Family Dev Cards — WHR Ratio Line and Zero-Body Notify-Me Screens

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-06  
**Status:** Implemented

---

## Decision

**Add a WHR ratio line to every zero-body (dev) family card and replace the blank "Body Architectures" section on zero-body families with a narrative development update and a mailto notify-me CTA.** Two families — The Classic and The Sculpt — launched without live bodies. Showing an empty section damages credibility. Showing a blank page signals abandonment. The dev-card pattern converts a missing-product gap into an active holding state that captures buyer intent and communicates manufacturing honesty.

---

## 1. The WHR Ratio Line: Measurement on the Dev Card

Before this change, a buyer browsing the family index (`family.html`) could see the family name, a description excerpt, and a body count. The proportion signature — the WHR and BWR ranges that distinguish one family from another — was buried inside each family's expanded section.

The ratio line surfaces that proportion data to the card level **on dev (zero-body) cards only**. Live family cards with bodies do not render a `fc-ratio` element; they already carry their proportion data inside the landing page. The ratio line is specifically a compensating signal for cards that have no body count to show:

```js
const ratioLine = meta.whr
  ? `<div class="fc-ratio">WHR ${ZX.esc(meta.whr)} &middot; ${ZX.esc((meta.sig || '').split(' · ')[0])}</div>`
  : '';
```

Where `meta.whr` is the family's WHR range string (e.g., `"0.68–0.72"`) and `(meta.sig || '').split(' · ')[0]` extracts the first segment of the silhouette signature — the silhouette label (e.g., `"Balanced hourglass"` from `"Balanced hourglass · WHR 0.68–0.72 · BWR 1.40–1.50"`). The `&middot;` HTML entity is the separator between WHR value and label in the rendered output.

Note the relationship between `fc-ratio` and `fc-sig` on dev cards: both are rendered. `fc-sig` takes `sig.split(' · ').slice(1).join(' · ')` — the WHR and BWR segments — while `fc-ratio` takes the zeroth segment (the named silhouette label) plus `meta.whr` directly. Together they give a dev card the same proportion information that a live card communicates via its landing page.

The CSS keeps this line subdued — it is a data annotation, not a headline:

```css
.fam-card .fc-ratio {
  font-size: 11px;
  letter-spacing: 1.4px;
  color: var(--muted);
  margin-top: 4px;
  opacity: .75;
}
```

The rule is listed alongside `.fc-name`, `.fc-sig`, `.fc-desc`, and `.fc-count` in the shared z-index stacking declaration (`position:relative;z-index:2`), so it participates in the same layering above the card's photo backdrop scrim.

**Decision rationale:** ZELEX's primary differentiation from competitors is documented measurement. Publishing WHR at the card level on dev cards means a buyer can evaluate proportion fit even for families with no live bodies — the catalog remains scannable by proportion regardless of inventory state.

---

## 2. Zero-Body Families: The Blank State Problem

At launch, The Classic (WHR 0.68–0.72) and The Sculpt (WHR 0.65–0.68) have zero live bodies in the catalog. Without intervention, their family pages render an empty `Body Architectures` section — or worse, a section that is suppressed entirely, leaving the page without a clear content area.

Three alternatives were considered:

| Option | Problem |
|---|---|
| Hide the family entirely from navigation | Breaks quiz routing; a buyer who scores Classic gets an error or empty state |
| Show "Coming soon" placeholder | Non-committal; gives the buyer nothing to act on |
| Remove the family from the site until bodies are ready | Loses all interest signals; Classic and Sculpt buyers have nowhere to land |
| **Dev card with narrative + notify-me CTA** | **Captures intent, communicates status honestly, keeps the family in the taxonomy** |

The dev-card pattern was chosen because it treats the buyer as an adult: here is what this family is, here is where manufacturing stands, here is one action you can take.

One nuance not captured in the table: the family index card for a zero-body family is rendered as a non-interactive `<div class="fam-card dev">` rather than a live `<a>` element. It cannot be clicked; it reads `In Development` as a status badge. The narrative dev card is only reachable via direct URL (e.g., `family.html?f=The%20Classic`) or via quiz routing — not by clicking the index card.

---

## 3. DEV_COPY Narratives — Tone and Content Decisions

The narratives are defined as a static inline object keyed by exact family name string, inside `renderLanding()`:

```js
const DEV_COPY = {
  "The Classic": {
    narrative: "...",
    subject: "ZELEX — Notify me: The Classic"
  },
  "The Sculpt": {
    narrative: "...",
    subject: "ZELEX — Notify me: The Sculpt"
  }
};
```

The narratives are authored to match the site's voice — measured, precise, luxury-tier — not an e-commerce placeholder:

**The Classic** (exact source text):
> "The Classic is the proportion ZELEX returns to first — a true hourglass where waist, hip, and shoulder resolve into a single, self-evident harmony. WHR 0.68–0.72 places it at the centre of the feminine ideal: nothing exaggerated, nothing withheld. Its architectures are currently in final pre-production review; the first bodies are expected to reach the catalogue within the coming season."

**The Sculpt** (exact source text):
> "The Sculpt renders athletic musculature at fine-craft resolution — articulated abdominals, defined deltoids, sculpted posterior — not as caricature but as the body a serious athlete actually inhabits. At WHR 0.65–0.68 it carries the density of the Muse with the surface geometry of the gym. Engineering is underway; first production bodies will enter the catalogue once silicone durability trials are complete."

**Copy decisions:**

1. **Manufacturing stage is family-specific, not generic.** The Classic is in *pre-production review*; The Sculpt is in *silicone durability trials*. These are different statements about different engineering statuses. Using a generic "coming soon" would collapse this distinction.

2. **No hard commitment date.** Both narratives use soft timing language ("within the coming season", "once trials are complete"). A hard date that slips damages credibility more than no date at all. Buyers in this tier are accustomed to bespoke timelines.

3. **The narrative frames the silhouette, not the delay.** The majority of each paragraph describes what the family *is* — the proportion signature, the design intent — not what is missing. A buyer who reads the Classic narrative understands why they want a Classic body before they reach the notify-me CTA.

4. **Fallback for undocumented zero-body families.** If a family has zero bodies but no `DEV_COPY` key, the code falls through to a generic tile: `"No architectures catalogued yet — check back soon."` The `DEV_COPY` object is the authored premium path; the fallback is the minimal safe default.

---

## 4. The Notify-Me CTA: Why Mailto

The CTA is a standard `mailto:` link with a pre-filled subject line rendered inside `buildBodySec()`:

```js
`<a class="btn ghost" href="mailto:inquiries@zelexdoll.com?subject=${encodeURIComponent(copy.subject)}">Notify me when available</a>`
```

The `btn ghost` class is the design system's secondary button style (established in PDR-001). No local CSS override is required — the class resolves through `assets/site.css`.

Pre-filled subjects (from `DEV_COPY[fam].subject`):
- `"ZELEX — Notify me: The Classic"` → encoded as `ZELEX%20%E2%80%94%20Notify%20me%3A%20The%20Classic`
- `"ZELEX — Notify me: The Sculpt"` → encoded as `ZELEX%20%E2%80%94%20Notify%20me%3A%20The%20Sculpt`

The CTA label is `"Notify me when available"` (not "Notify Me When Available" — sentence case, consistent with the site's button copy convention).

**Why mailto over a form or waitlist:**

1. **No backend required.** A mailto fires immediately with no server infrastructure. At the current development stage, adding a waitlist database, confirmation email logic, and unsubscribe flow is engineering overhead that outweighs the benefit.

2. **The buyer self-qualifies.** Opening a mailto requires the buyer to have intent strong enough to launch their email client. A buyer who completes that action is a warm lead; a buyer who only considered it is not lost — they were not yet at inquiry threshold.

3. **The pre-filled subject routes the inquiry instantly.** Support can filter `"ZELEX — Notify me"` as a mailbox folder rule before the first body ships. No triage required.

4. **Privacy alignment.** No email address is captured without the buyer's explicit action. No confirmation email or unsubscribe infrastructure is needed. This is consistent with the site's broader privacy posture (see PDR-004 for the contact form's email-injection approach).

---

## 5. Quiz Routing Compatibility

The quiz may route a buyer to The Classic or The Sculpt based on their measurement inputs. The result grid (PDR-002) selects live characters, so a buyer routed to a zero-body family will have the runner-up fill fire — they will see characters from their second-best-scoring family instead of a blank grid.

However, the **"Browse The Classic"** CTA on the result screen still routes to `family.html?f=The%20Classic`. The routing guard in `render()` validates the `f` param against `ZX.FAMILIES`:

```js
const raw = ZX.qs('f');
const validFams = new Set(ZX.FAMILIES);
const f = (raw && validFams.has(raw)) ? raw : null;
if (!f) { renderIndex(m); } else { renderLanding(m, f); }
```

Because Classic and Sculpt are registered members of `ZX.FAMILIES`, `validFams.has("The Classic")` returns `true` and `renderLanding` is called correctly. There is no 404 risk. An invalid or malformed `f` param falls through to `renderIndex`, showing the full family grid — a safe, non-broken fallback.

**Zero-body family in `renderLanding`: what the buyer sees.** Once `renderLanding` runs for a zero-body family, `famBodyCodes` is an empty array (`famBodyCodes.length === 0`). The `buildBodySec()` function checks this condition, finds a `DEV_COPY` entry, and renders the narrative + notify-me CTA in place of an architecture grid. The buyer lands on a page with:
- A full family hero (name, sig-line, description, prop-badge showing WHR/BWR from `FAM_META`)
- The `Body Architectures` section rendered as a narrative + mailto CTA (not as an empty grid)
- Sibling family pills and footer actions

The dev card is the terminal node for Classic and Sculpt buyers in the current catalog state. It is a fully composed page, not a degraded one.

---

## 6. Commercial Translation

| Signal | Value |
|---|---|
| Buyer reaches Classic or Sculpt family page | Confirmed interest in that proportion archetype — even at zero inventory |
| Buyer clicks notify-me | Warm lead; pre-qualifies intent before any body exists |
| Subject-line filtering | Zero-effort waitlist management via mailbox rule |
| Narrative read time | Buyer understands the family's design identity before product exists; reduces post-launch education cost |

The notify-me pattern is the minimum viable waitlist. It does not require a database, a confirmation flow, or an unsubscribe mechanism. When bodies enter the catalog, the first outbound to everyone who sent a notify-me email is a direct announcement to a pre-qualified buyer pool.

---

## 7. Strategic Conclusion

1. The WHR ratio line on dev cards keeps zero-inventory entries scannable by proportion — consistent with ZELEX's measurement-documented positioning. It is limited to dev cards by design; live cards communicate proportion data through their landing pages.
2. Dev cards convert a catalog gap into an active holding state without engineering infrastructure. The index card is non-interactive; the landing page is fully composed.
3. The routing guard (`validFams.has(raw)`) ensures quiz routing to zero-body families never produces a broken page — unknown params fall back to the full index.
4. The narrative voice is family-specific and manufacturing-honest: different stages, different timelines, no generic placeholder language.
5. Mailto notify-me is the correct CTA for this development stage: no backend, self-qualifying buyer intent, instant inbox routing via subject-line filter.
6. If a zero-body family has no `DEV_COPY` entry, the code falls through to a generic empty tile — the premium narrative path is opt-in by authoring, not forced.

**Positioning headline:** *"Available when it's ready. Here is exactly what you are waiting for."*

---

## 8. Acceptance Review

| Criterion | Status |
|---|---|
| WHR ratio line rendered on zero-body (dev) family cards | ✓ `ratioLine` rendered only in the `!hasBodies` branch; live cards do not get a `fc-ratio` element |
| Ratio line shows WHR range and first silhouette-label segment | ✓ `(meta.sig || '').split(' · ')[0]` extracts first segment (e.g., `"Balanced hourglass"`); `meta.whr` supplies the range; `&middot;` separates them |
| `fc-sig` on dev cards shows remaining sig segments (WHR · BWR) | ✓ `.split(' · ').slice(1).join(' · ')` — complementary to `fc-ratio` |
| Classic family page shows DEV_COPY narrative (not empty section) | ✓ `DEV_COPY["The Classic"].narrative` renders when `famBodyCodes.length === 0` |
| Sculpt family page shows DEV_COPY narrative | ✓ `DEV_COPY["The Sculpt"].narrative` same path |
| Notify-me CTA fires mailto with pre-filled subject | ✓ `href="mailto:inquiries@zelexdoll.com?subject=${encodeURIComponent(copy.subject)}"` |
| CTA label text | ✓ `"Notify me when available"` (sentence case) |
| `btn ghost` class on CTA | ✓ `<a class="btn ghost" href="mailto:...">` — inherits design system button styles |
| Quiz can route to Classic/Sculpt without error | ✓ `validFams.has(raw)` guard; invalid `f` params fall back to `renderIndex` |
| Narrative copy discloses manufacturing stage (not generic "coming soon") | ✓ Pre-production review vs durability trials — family-specific |
| Notify-me requires no backend | ✓ Pure `mailto:` — no form submission, no database |
| Zero-body families without DEV_COPY entry | ✓ Falls through to generic empty-tile: `"No architectures catalogued yet — check back soon."` |

### Implementation Notes

- `DEV_COPY` is a static inline object scoped inside `renderLanding()`, keyed by exact family name string. If family names change in the data source, the `DEV_COPY` keys must be updated to match. The object is not accessible from `renderIndex` — the index card's `In Development` badge is rendered separately with no copy dependency.
- The `famBodyCodes.length === 0` check triggers on families with no live bodies at page-render time. If a body is added to The Classic or The Sculpt, the dev card section disappears automatically — no code change required.
- The `btn ghost` class on the notify-me link inherits the button styles from the design system (PDR-001). No local button CSS is needed.
- The non-interactive index card (`<div class="fam-card dev">`) has `opacity:.55`, `cursor:default`, and its `:hover` state suppresses the transform and gold border-color that live cards show. Buyers see the card as muted but readable; the `In Development` stat badge communicates status without explanation.
- The prop-badge in the family hero (WHR Range / BWR Range) derives its values from actual body data first (`fmt(whrs)` / `fmt(bwrs)`), falling back to `meta.whr` / `meta.bwr` from `FAM_META` when the family has no bodies. Zero-body families therefore still display correct proportion ranges in their hero.
