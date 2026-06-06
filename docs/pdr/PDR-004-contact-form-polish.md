# PDR-004: Contact Form Polish — Success State, Discreet Copy, Email Obfuscation, Validation

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-06  
**Status:** Implemented

---

## Decision

**Upgrade the inquiry form success state to use Playfair Display typography, discreet confirmation copy, and JS-injected email links; tighten message validation to a 10-character minimum; and architect the success path to behave correctly whether the submission used a backend endpoint or the mailto fallback.** The inquiry form is the only conversion event on the site. A buyer spending $1,800–$2,500 on a discreet purchase needs unambiguous confirmation that their message was received — and needs to trust that the operator handles their inquiry with the same discretion they applied when writing it.

---

## 1. The Success State Problem

Before this change, the inquiry form had no success state. On submission, the form either navigated away or showed a generic browser alert. For a luxury-tier, privacy-sensitive purchase this is a critical UX failure: the buyer has no confirmation that the inquiry was received, no fallback contact path if the submission silently failed, and no signal that the operator will handle their inquiry discreetly.

An absent or generic success state also signals volume e-commerce behavior — the kind of automated confirmation a buyer associates with a shopping cart, not a concierge relationship.

---

## 2. Success State Design: Typography and Color Choices

The success state is a distinct DOM element that replaces the form:

```html
<div id="form-success">
  <h3>Your inquiry has been received.</h3>
  <p>We will be in touch discreetly within one business day.<br>
    You may also reach us directly at
    <a id="success-email-link" href="#"><!-- filled by JS --></a>.</p>
</div>
```

**Playfair Display heading:**

```css
#form-success h3 {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  color: var(--Muse);
  margin-bottom: 8px;
}
```

Using Playfair Display for the confirmation heading (rather than the site's default sans-serif) is deliberate: the serif face is the typographic register of the Atlas headings and the family naming — it signals that the inquiry has entered the catalog's premium context. The confirmation is not a system message; it is a direct communication from the ZELEX voice.

`var(--Muse)` (`#9FD6B6`, sage green) is the site's confirmation color — the same token used for verified measurements and live-status indicators across the catalog. Applying it to the success heading creates a consistent visual grammar: green means confirmed.

The container uses a soft green tint:

```css
#form-success {
  background: rgba(159, 214, 182, .1);
  border: 1px solid rgba(159, 214, 182, .35);
  border-radius: 10px;
  padding: 24px 28px;
}
```

The tint is near-invisible — perceptible enough to mark the state change, subdued enough to avoid a generic "success banner" feel.

---

## 3. "Discreetly" — Copy Decision

The confirmation reads: *"We will be in touch discreetly within one business day."*

The word "discreetly" is not filler. This purchase is a privacy-sensitive transaction for a significant number of buyers. The operator commits to discretion in the confirmation itself — not in a buried privacy policy, but in the first sentence the buyer reads after submitting. For a buyer who hesitated before sending the inquiry, "discreetly" is the word that confirms they made the right decision.

"Within one business day" sets an explicit expectation. Luxury tier buyers are accustomed to bespoke timelines; one business day is fast enough to signal responsiveness without promising same-hour support that cannot be reliably delivered.

---

## 4. Email Obfuscation via JS Injection

The inquiry email address does not appear anywhere in the HTML source. It is injected at page load by a self-executing function:

```js
(function wireEmailLinks() {
  const email = ZX.INQUIRY_EMAIL || 'inquiries@zelexdoll.com';
  const mailto = 'mailto:' + email;
  const els = ['success-email-link', 'error-email-link', 'panel-email-link'];
  els.forEach(function(id) {
    var el = document.getElementById(id);
    if (el) { el.href = mailto; el.textContent = email; }
  });
}());
```

`ZX.INQUIRY_EMAIL` is the canonical email constant in the shared site module. The fallback `'inquiries@zelexdoll.com'` is only used if the constant is absent.

**Why inject via JS:**

1. **Spam harvester resistance.** Email scrapers that parse static HTML will not find the address. The address is only present in the rendered DOM after the IIFE fires — after JavaScript execution, which most scrapers do not run.

2. **Single source of truth.** All three link elements (`success-email-link`, `error-email-link`, `panel-email-link`) draw from `ZX.INQUIRY_EMAIL`. Changing the inquiry email requires one change in the module; the three link elements update automatically.

3. **No encoding tricks.** The obfuscation is structural (HTML has no email; JS writes it) rather than encoding-based (ROT13, HTML entities, etc.). Encoding tricks are fragile; JS injection is robust and readable.

The IIFE runs as an immediately-invoked function expression (not in a DOMContentLoaded or window.onload handler) because all three target elements are present in static HTML above the script tag. The injection is synchronous and completes before any async catalog or form logic runs.

---

## 5. Dual Success Path: Endpoint vs Mailto Fallback

The site supports two submission paths: a real fetch to a backend endpoint (POST), and a mailto fallback if the endpoint is unavailable. The success state behaves differently depending on which path fired:

```js
function showSuccess(usedMailto) {
  var form    = document.getElementById('inquiry-form');
  var success = document.getElementById('form-success');
  if (form)    form.style.display    = 'none';
  if (success) success.style.display = 'block';

  if (!usedMailto) {
    // Endpoint path: suppress the direct-email line
    var p = success.querySelector('p');
    if (p) p.innerHTML = 'We will be in touch discreetly within one business day.';
  }
  // Re-wire email link in case JS ran before catalog
  var sl = document.getElementById('success-email-link');
  if (sl) { sl.href = 'mailto:' + email; sl.textContent = email; }
}
```

**When the endpoint returned 2xx:** The backend received the submission and the operator will respond via that channel. Showing the "you may also reach us at…" fallback line would imply the endpoint might not have worked. The line is suppressed; the confirmation is unambiguous.

**When the mailto fallback fired:** The buyer's email client opened with a pre-composed inquiry. The direct-email line is shown, reinforcing that the same address they emailed is the correct point of contact — no ambiguity about where their message went.

This dual behavior requires only one success-screen element and one function call. The path decision (`usedMailto` boolean) is made in the form submission handler upstream.

---

## 6. Message Validation: 10-Character Minimum

The form uses `novalidate` to disable browser native validation. All validation is JS-driven:

```js
if (msg.trim().length < 10) {
  // show validation error for the message field
  return false;
}
```

**Why 10 characters:**

- Fewer than 10 trimmed characters cannot constitute a coherent inquiry. Single-word submissions ("hello", "price?") provide no information for the operator to act on.
- 10 is a floor, not a target. A buyer writing a real inquiry will easily exceed it; the threshold only rejects empty or near-empty submissions.
- Native browser `minlength` validation fires at typing-time and varies in error presentation across browsers. JS validation fires at submit, after the full message has been written — a better UX for a textarea where typing cadence is irregular.
- The `novalidate` attribute removes the browser's default validation UI entirely, so all error messages are site-branded and consistent with the design system.

The 10-character minimum is paired with a `required` attribute on the message field (for accessibility/screen-reader conformance), but the submission-time JS check is the enforced gate.

---

## 7. Commercial Translation

The contact form is the single conversion event in the Atlas. Every design decision in this PDR is an argument for inquiry completion:

| Decision | Conversion effect |
|---|---|
| Playfair Display success heading | Matches the site's luxury register; signals the inquiry entered the correct channel |
| "Discreetly within one business day" | Reduces post-submission anxiety for privacy-sensitive buyers; sets a clear response expectation |
| Direct-email fallback line (mailto path) | Provides a recovery path if the buyer suspects the mailto didn't send correctly |
| Endpoint-path suppression of fallback line | Prevents ambiguity about where the submission went; keeps the confirmation clean |
| JS email injection | Reduces spam exposure to the inquiry inbox; single point of update |
| 10-char validation | Blocks noise submissions; operator only receives actionable inquiries |

A buyer who reads "Your inquiry has been received. We will be in touch discreetly within one business day." has no remaining uncertainty about submission status. Reducing post-submission uncertainty is the last friction point between an intent signal and a confirmed lead.

---

## 8. Strategic Conclusion

1. The Playfair Display + Muse-green success state extends the site's typographic and color grammar into the confirmation moment — the inquiry has entered the ZELEX context, not a generic form pipeline.
2. "Discreetly" is the highest-value word in the confirmation copy for this buyer segment. It should not be removed or softened in future copy revisions.
3. JS email injection is the correct obfuscation strategy at this scale: structurally effective, maintainable, and consistent across all three link elements.
4. The dual success path (endpoint vs mailto) is a single function with one boolean argument — minimal complexity, correct behavior in both states.
5. The 10-character minimum is the correct validation gate: low enough to never block a real inquiry, high enough to block noise.

**Positioning headline:** *"Your inquiry has been received. Discreetly — as it should be."*

---

## 9. Acceptance Review

| Criterion | Status |
|---|---|
| Success heading uses Playfair Display at 22px in `var(--Muse)` | ✓ `#form-success h3` CSS confirmed |
| Success container uses soft green tint background | ✓ `rgba(159,214,182,.1)` background + `.35` border |
| Confirmation copy includes "discreetly" and one-business-day SLA | ✓ Literal copy in HTML |
| All three email link elements wired by `wireEmailLinks` IIFE | ✓ `success-email-link`, `error-email-link`, `panel-email-link` |
| Email not present in HTML source (JS injection only) | ✓ `<!-- filled by JS -->` placeholder in HTML |
| Endpoint success path suppresses direct-email fallback line | ✓ `!usedMailto` branch rewrites `<p>` innerHTML |
| Mailto success path shows direct-email link | ✓ Default `showSuccess(true)` leaves full `<p>` intact |
| Message field validates at 10-character trimmed minimum | ✓ `msg.trim().length < 10` gate in submit handler |
| Form uses `novalidate` (JS-only validation) | ✓ Attribute present on `<form id="inquiry-form">` |

### Implementation Notes

- The `wireEmailLinks` IIFE runs synchronously on parse; it does not wait for `DOMContentLoaded`. The three link elements must appear above the script tag in source order, or the `getElementById` calls will return `null` and the links will remain `href="#"`. This is the current layout; do not move the script above the link elements.
- `ZX.INQUIRY_EMAIL` is the canonical email source. The inline fallback `'inquiries@zelexdoll.com'` in `wireEmailLinks` is a safety net for local development without the ZX module. In production, `ZX.INQUIRY_EMAIL` should always be defined.
- The `form-success` and `form-error` elements are always present in the DOM (not dynamically created). Their initial `display: none` is set in CSS. The `showSuccess` / `showError` functions toggle to `display: block`. This means `getElementById` calls in those functions are always valid — no null check needed.
