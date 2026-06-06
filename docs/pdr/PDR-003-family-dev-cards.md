# PDR-003: Family Dev Cards — WHR Ratio Line and Zero-Body Notify-Me Screens

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-06  
**Status:** Implemented

---

## Decision

**Add a WHR/BWR ratio line to every family card and replace the blank "Body Architectures" section on zero-body families with a narrative development update and a mailto notify-me CTA.** Two families — The Classic and The Sculpt — launched without live bodies. Showing an empty section damages credibility. Showing a blank page signals abandonment. The dev-card pattern converts a missing-product gap into an active holding state that captures buyer intent and communicates manufacturing honesty.

---

## 1. The WHR Ratio Line: Measurement on the Card

Before this change, a buyer browsing the family index (`family.html`) could see the family name, a description excerpt, and a body count. The proportion signature — the WHR and BWR ranges that distinguish one family from another — was buried inside each family's expanded section.

The ratio line surfaces that data to the card level:

```js
`<div class="fc-ratio">WHR ${ZX.esc(meta.whr)} · ${ZX.esc((meta.sig || '').split(' · ')[0])}</div>`
```

Where `meta.whr` is the family's WHR range string (e.g., `"0.65–0.70"`) and `meta.sig` is the silhouette signature — only the first segment before ` · ` is shown (e.g., `"tall, hip-dominant"` from `"tall, hip-dominant · +25%"`).

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

**Decision rationale:** ZELEX's primary differentiation from competitors is documented measurement. Publishing WHR at the card level means a buyer can evaluate proportion fit without entering each family — the catalog becomes scannable by proportion, not just by name.

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

---

## 3. DEV_COPY Narratives — Tone and Content Decisions

The narratives are authored to match the site's voice — measured, precise, luxury-tier — not an e-commerce placeholder:

**The Classic:**
> "The Classic is the proportion ZELEX returns to first — a true hourglass where waist, hip, and shoulder resolve into a single, self-evident harmony. WHR 0.68–0.72 places it at the centre of the feminine ideal: nothing exaggerated, nothing withheld. Its architectures are currently in final pre-production review; the first bodies are expected to reach the catalogue within the coming season."

**The Sculpt:**
> "The Sculpt renders athletic musculature at fine-craft resolution — articulated abdominals, defined deltoids, sculpted posterior — not as caricature but as the body a serious athlete actually inhabits. At WHR 0.65–0.68 it carries the density of the Muse with the surface geometry of the gym. Engineering is underway; first production bodies will enter the catalogue once silicone durability trials are complete."

**Copy decisions:**

1. **Manufacturing stage is family-specific, not generic.** The Classic is in *pre-production review*; The Sculpt is in *silicone durability trials*. These are different statements about different engineering statuses. Using a generic "coming soon" would collapse this distinction.

2. **No hard commitment date.** Both narratives use soft timing language ("within the coming season", "once trials are complete"). A hard date that slips damages credibility more than no date at all. Buyers in this tier are accustomed to bespoke timelines.

3. **The narrative frames the silhouette, not the delay.** The majority of each paragraph describes what the family *is* — the proportion signature, the design intent — not what is missing. A buyer who reads the Classic narrative understands why they want a Classic body before they reach the notify-me CTA.

---

## 4. The Notify-Me CTA: Why Mailto

The CTA is a standard `mailto:` link with a pre-filled subject line:

```js
`<a class="btn ghost"
   href="mailto:inquiries@zelexdoll.com?subject=${encodeURIComponent(copy.subject)}">
  Notify me when available
</a>`
```

Pre-filled subjects:
- `"ZELEX — Notify me: The Classic"`
- `"ZELEX — Notify me: The Sculpt"`

**Why mailto over a form or waitlist:**

1. **No backend required.** A mailto fires immediately with no server infrastructure. At the current development stage, adding a waitlist database, confirmation email logic, and unsubscribe flow is engineering overhead that outweighs the benefit.

2. **The buyer self-qualifies.** Opening a mailto requires the buyer to have intent strong enough to launch their email client. A buyer who completes that action is a warm lead; a buyer who only considered it is not lost — they were not yet at inquiry threshold.

3. **The pre-filled subject routes the inquiry instantly.** Support can filter `"ZELEX — Notify me"` as a mailbox folder rule before the first body ships. No triage required.

4. **Privacy alignment.** No email address is captured without the buyer's explicit action. No confirmation email or unsubscribe infrastructure is needed. This is consistent with the site's broader privacy posture (see PDR-004 for the contact form's email-injection approach).

---

## 5. Quiz Routing Compatibility

The quiz may route a buyer to The Classic or The Sculpt based on their measurement inputs. The result grid (PDR-002) selects live characters, so a buyer routed to a zero-body family will have the runner-up fill fire — they will see characters from their second-best-scoring family instead of a blank grid.

However, the **"Browse The Classic"** CTA on the result screen still routes to `family.html?f=The Classic`. The dev-card pattern ensures this is a valid destination. A buyer who clicks through to The Classic family page lands on a narrative that explains the family, not a 404 or an empty page. The dev card is the terminal node for Classic and Sculpt buyers in the current catalog state.

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

1. The WHR ratio line at the card level makes the family index scannable by proportion — consistent with ZELEX's measurement-documented positioning.
2. Dev cards convert a catalog gap into an active holding state without engineering infrastructure.
3. The narrative voice is family-specific and manufacturing-honest: different stages, different timelines, no generic placeholder language.
4. Mailto notify-me is the correct CTA for this development stage: no backend, self-qualifying buyer intent, instant inbox routing via subject-line filter.
5. Quiz routing to zero-body families resolves gracefully — the dev card is a valid destination; buyers are never stranded.

**Positioning headline:** *"Available when it's ready. Here is exactly what you are waiting for."*

---

## 8. Acceptance Review

| Criterion | Status |
|---|---|
| WHR ratio line rendered on all six family cards | ✓ Generated from `meta.whr` and `meta.sig` on every card |
| Ratio line shows WHR range and first silhouette segment only | ✓ `sig.split(' · ')[0]` truncates after first segment |
| Classic family page shows DEV_COPY narrative (not empty section) | ✓ `DEV_COPY["The Classic"]` renders when `famBodyCodes.length === 0` |
| Sculpt family page shows DEV_COPY narrative | ✓ `DEV_COPY["The Sculpt"]` same path |
| Notify-me CTA fires mailto with pre-filled subject | ✓ `encodeURIComponent(copy.subject)` in href |
| Quiz can route to Classic/Sculpt without error | ✓ Dev card is a valid destination; no 404 |
| Narrative copy discloses manufacturing stage (not generic "coming soon") | ✓ Pre-production review vs durability trials — family-specific |
| Notify-me requires no backend | ✓ Pure `mailto:` — no form submission, no database |

### Implementation Notes

- `DEV_COPY` is a static inline object keyed by exact family name string. If family names change in the data source, the `DEV_COPY` keys must be updated to match.
- The `famBodyCodes.length === 0` check triggers on families with no live bodies at page-render time. If a body is added to The Classic or The Sculpt, the dev card section disappears automatically — no code change required.
- The `btn ghost` class on the notify-me link inherits the button styles from the design system (PDR-001). No local button CSS is needed.
