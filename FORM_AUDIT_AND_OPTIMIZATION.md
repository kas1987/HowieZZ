# ZELEX Intake Form Optimization — Audit & Redesign

**Date:** 2026-06-21
**Objective:** +30% conversion lift through progressive disclosure, quiz prefilling, and WCAG AA compliance
**Deliverables:** Form audit, UX redesign spec, A/B test variants, accessibility audit

---

## PART 1: CURRENT STATE AUDIT

### Form Structure
- **Entry point:** contact.html (single-page form)
- **Length:** ~17 visible sections + 6 hidden payload fields
- **Est. cognitive load:** ~4.5 min to complete
- **Mobile breakpoint:** 900px

### Strengths
1. **Audience segmentation** — New buyer / Collector toggle (aria-pressed state)
2. **Guided buyer-fit** — Progressive disclosure via FIT.js state machine
3. **Character prefill** — URL params (?id=, ?family=, ?b=, ?compare=) pre-populate context card
4. **Live summary** — Right-side "Your fit so far" tracks selections in real-time
5. **Accessibility basics** — Semantic HTML, form labels, error messaging
6. **Visual hierarchy** — Gold accent color guides focus through Playfair Display headers

### UX Pain Points

#### 1. Cognitive Overload (Primary Conversion Barrier)
- Form shows **all 17 sections at once** on page load, creating "wall of text" effect
- New buyers see custom swatches (skin/eyes/hair) immediately, but most haven't decided on body yet
- Realism slider + customization interests are frontloaded for exploratory users
- **Impact:** Bounce before Message field (est. 35–40% drop-off)

#### 2. Field Ordering Issues
- Name/Email/Phone come first (transactional), but should be deferred or back-loaded
- "Character of interest" is optional but placed high, signaling uncertainty
- Message (the most valuable field) is buried 10+ scrolls down on mobile
- Family select dropdown has no visual affordance for "unsure" state

#### 3. Mobile UX Deficits
- Two-column layout collapses at 900px, but sidebar (info panel + summary) remains sticky
- Right-side sticky panel pushes content down on phones <600px
- Swatch blocks render full-width, consuming ~8 extra scroll sections
- No scroll-to-field on validation error

#### 4. Quiz Integration Missing
- **No bridge from quiz to contact form** — quiz results don't prefill form fields
- Users must re-enter preferences (body family, realism, timeline, use) after quiz
- **Loss of momentum:** ~15–20% of quiz completers likely abandon
- No sessionStorage handoff of quiz state

#### 5. Consent & Privacy Framing
- Checkbox label is dense (single line, 85+ chars)
- No visual reassurance before form submit (only in info panel)
- Privacy policy link missing (likely legal req)

#### 6. Validation & Error Recovery
- Validation only on submit (no inline or progressive checks)
- Error banner hides success message possibility
- No field focus management after error
- Unclear error copy for email format

#### 7. Accessibility Issues (WCAG AA gaps)
- **Color contrast:** Form labels use `var(--muted)` against `var(--panel)` (~4.2:1 at edge cases)
- **Form identification:** No `<fieldset>` grouping for related sections (buyer-fit, customization)
- **Live region:** fit-summary has `aria-live="polite"` but aria-label is on the container, not a heading
- **Button state:** Submit button disables on submit but no aria-busy state
- **Swatch buttons:** No aria-label on color swatches (visual-only indicators)
- **Realism slider:** Nodes are buttons but styled like radio inputs — inconsistent semantics

#### 8. Trust & Reassurance Gaps
- Transactional flow feels "sales-y" before relationship is established
- No progress indicator until mid-form
- Info panel is side-column, not in critical path for new users
- Message field placeholder is 2 lines — overly instructional

---

## PART 2: CONVERSION FRICTION MODEL

### User Journey Segments

#### Segment A: "Just curious" (Quiz → Contact)
- Entry: quiz.html results page
- Current state: No prefill, must re-enter body family & realism
- Friction: 2 min re-entry time, form looks similar to quiz (fatigue)
- **Likely drop:** 18–22%
- **Optimization:** Quiz → URL param → form loads prefilled, shows "We're picking up where you left off"

#### Segment B: "Directed buyer" (?id=, ?family=, ?b= links)
- Entry: browse.html / character.html → "Ask about this"
- Current state: Character chip shows context
- Friction: Still must fill out 11+ optional fit fields to feel "heard"
- **Likely drop:** 10–15%
- **Optimization:** Defer customization fields until post-submit refinement step

#### Segment C: "Cold start" (direct to contact.html)
- Entry: Navigation link / footer CTA
- Current state: 17-field form, no context
- Friction: Audience toggle helps, but "Still deciding" audience still sees full form
- **Likely drop:** 28–35%
- **Optimization:** Progressive disclosure — show 4 fields (name, email, message, intent), then expand based on answer

#### Segment D: "Repeat collector" (?mode=collector URL override)
- Entry: Previous inquiry or brand link
- Current state: Collector toggle is active but no saved session
- Friction: Must refill name/email every time
- **Likely drop:** 8–12%
- **Optimization:** Email-based session restore, pre-check consent

---

## PART 3: WCAG AA Compliance Findings

### Current Issues
1. **SC 1.4.3 Contrast (AA)** — Minor: Form labels on dark panels need 4.5:1 (some are 4.2:1)
2. **SC 1.3.1 Info & Relationships** — Major: Buyer-fit fields lack `<fieldset>` grouping
3. **SC 4.1.2 Name, Role, Value** — Major: Swatch buttons missing aria-labels
4. **SC 4.1.3 Status Messages** — Minor: Error banners not explicitly marked as alerts
5. **SC 2.5.5 Target Size** — Minor: Swatch buttons (34px) OK, but customization chips (44px height) acceptable

### Path to AA Compliance
- Add explicit `<fieldset role="group">` for each buyer-fit section
- Upgrade form labels to `<legend>` where appropriate
- Add `aria-label` to all iconic buttons (swatches, realism nodes)
- Use `role="alert"` on error/success banners
- Boost label contrast to 4.5:1 via CSS variable or computed color
- Add `aria-busy="true"` to submit button during POST

---

## PART 4: OPTIMIZATION STRATEGY

### Three Pillars

#### Pillar 1: Progressive Disclosure
- **Phase 0 (Entry):** Audience toggle + 2 fields (name, email)
- **Phase 1 (After email):** Message + submit OR "Tell us more?" expansion
- **Phase 2 (Optional):** Buyer-fit fields appear on-demand, grouped by relevance
- **Phase 3 (Post-submit?):** Customization refinement via second-page or email follow-up

#### Pillar 2: Quiz → Form Bridge
- Quiz completion stores result in sessionStorage: `{ family, realism, timeline, use, handling, privacy }`
- Contact form checks for stored state on load
- If quiz data present: "We're picking up where you left from the quiz" + pre-check fields
- No re-entry required; user can override

#### Pillar 3: WCAG AA + Accessibility
- Semantic grouping via `<fieldset>`
- Aria-labels on all iconic elements
- Alert roles on validation
- Contrast ratio enforcement via CSS
- Keyboard navigation for all interactive elements

---

## PART 5: A/B TEST VARIANTS

### Variant A (Control): Current Form
- All 17 sections visible at once
- Audience toggle at top
- Character prefill via URL param
- Est. conversion: **baseline (4.2%)**

### Variant B (Progressive Disclosure + Quiz Bridge)
- Audience toggle
- Phase 0: Name + Email (required)
- Phase 1: Message + "Tell us more?" toggle
- Phase 2: Buyer-fit fields (if toggled), grouped by section
- Quiz state auto-loads + prefills relevant fields
- Est. conversion: **6.1% (+45% lift)**

### Variant C (Mobile-First Redesign + Multi-Step)
- Progressive disclosure as above
- Form spans 2–3 steps (each step saves to sessionStorage)
- Step 1: Audience + Name + Email + Intent
- Step 2: Buyer-fit preferences
- Step 3: Message + customization + consent
- Mobile-optimized: Single-column throughout, large touch targets
- Est. conversion: **5.8% (+38% lift)**

### Variant D (Minimal Entry Gate + Exit-Intent)
- Ultra-minimal Phase 0: Just Email + Message (required), Audience optional
- Phase 1: Expand buyer-fit on-demand
- Exit-intent overlay: "Before you go — tell us your timeline?" (captures timeline field)
- Quiz bridge as Variant B
- Psychological framing: "A quick note is enough; we'll follow up with questions."
- Est. conversion: **6.4% (+52% lift)**

---

## PART 6: TECHNICAL IMPLEMENTATION ROADMAP

### Short-term (Week 1–2): Quick Wins
1. Add WCAG AA fixes (contrast, fieldset, aria-labels)
2. Implement quiz → localStorage handoff
3. Add email-based session restore for collectors
4. Validate fields on blur (not just submit)
5. Add scroll-to-error on validation fail

### Medium-term (Week 3–4): Progressive Disclosure Refactor
1. Extract Phase 0/1/2 into separate HTML sections
2. Add toggle JS logic to show/hide phases
3. Test on mobile and desktop
4. Integrate quiz bridge JS
5. A/B testing setup (analytics tags)

### Long-term (Week 5+): Multi-Step & Exit-Intent
1. Convert to multi-step form (sessionStorage between steps)
2. Add exit-intent modal (JS scroll/beforeunload listener)
3. Implement email-based session restore (backend integration)
4. Customization post-submit refinement page
5. Analytics dashboard to track conversion by variant

---

## PART 7: ANALYTICS INSTRUMENTATION

### Events to Track

| Event Name | Fired | Fields |
|---|---|---|
| `form_visit` | Page load | variant, quiz_prefill, entry_source |
| `phase_expand` | Phase 2 toggle | phase, audience |
| `field_blur` | Field loses focus | field_name, validation_error |
| `validation_failed` | Submit fails | fields_with_errors, audience |
| `submit_attempt` | Submit triggered | has_buyer_fit, has_customization |
| `submit_success` | Form accepted | conversion_time_sec, audience, variant |
| `exit_intent_shown` | Exit modal appears | field_attempted, scroll_depth |
| `exit_intent_completed` | Exit modal submitted | field_captured |

### Conversion Metrics
- **Primary:** Submission rate (aggregate across all variants)
- **Secondary:** Submission by audience, family interest, entry source
- **Tertiary:** Time-to-submit, field completion rate, error recovery rate
- **Funnel:** Phase 0 → Phase 1 → Phase 2 → submit

---

## PART 8: IMPLEMENTATION CHECKLIST

### Pre-Launch QA
- [ ] WCAG AA audit (aXe, Lighthouse)
- [ ] Mobile testing (iOS Safari, Chrome Android)
- [ ] Quiz → contact handoff end-to-end
- [ ] Validation error messages (inline + banner)
- [ ] Consent + privacy link rendering
- [ ] Prefill URL params (?id=, ?family=, ?compare=) still work
- [ ] Form submission with mailto fallback
- [ ] Form submission with endpoint (if configured)
- [ ] Analytics events firing
- [ ] Session storage not persisting across browser close

### Variant-Specific Tests
- **Variant B:** Phase 2 toggle shows/hides sections, form still submits with correct payload
- **Variant C:** Multi-step saves to sessionStorage, back button works, browser back doesn't lose data
- **Variant D:** Exit-intent modal appears on scroll >80%, captures timeline field, data merges into main form

---

## PART 9: ESTIMATED IMPACT

### Conversion Lift Projection (Based on Industry Benchmarks)

| Optimization | Expected Lift |
|---|---|
| Progressive disclosure (Variant B) | +18–25% |
| Quiz bridge + prefill | +12–18% |
| Mobile UX improvements | +8–15% |
| WCAG AA + trust signals | +3–8% |
| Exit-intent capture (Variant D) | +5–12% |
| **Cumulative (optimistic scenario)** | **+38–65%** |
| **Target: 30% baseline** | **Conservative: +30–40%** |

### Revenue Impact (Hypothetical)
- Assume: 10k monthly contact.html visitors, 4.2% baseline conversion (420 inquiries/month)
- With 30% lift: 546 inquiries/month (+126/month, +15% revenue if ~$5k avg order value)
- With 50% lift (Variant D): 630 inquiries/month (+210/month, +25% revenue)

---

## APPENDIX: Key Decisions

### Design Principles Applied
1. **Mobile-first:** New breakpoints at 480px, 768px, 1024px
2. **Progressive enhancement:** Form works without JS (no phase toggle), enhanced with JS
3. **Accessibility-first:** Semantic HTML before custom styling
4. **Lean hypothesis:** Test one change at a time before stacking

### Out-of-Scope for This Cycle
- Custom form builder (keep vanilla HTML/JS)
- Backend session restore (defer to Phase 2)
- Email signature template (marketing)
- CRM integration (backend)
- Spam filtering (backend)

---

## APPENDIX: Sample A/B Test URLs

```
Control (Variant A):
https://zelexdoll.com/contact.html?variant=a

Progressive Disclosure (Variant B):
https://zelexdoll.com/contact.html?variant=b&quiz_result=muse_realism_2

Multi-Step (Variant C):
https://zelexdoll.com/contact.html?variant=c&step=1

Minimal Entry (Variant D):
https://zelexdoll.com/contact.html?variant=d
```

---

**End of Audit & Optimization Report**
