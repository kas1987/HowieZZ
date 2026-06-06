# PDR-004: Contact Form Polish — Success State, Discreet Copy, Email Obfuscation, Validation

**Branch:** feat/pdr-010-ceo-roi-analysis  
**Date:** 2026-06-06  
**Status:** Implemented

---

## Decision

**Upgrade the inquiry form success state to use Playfair Display typography, discreet confirmation copy, and JS-injected email links; implement full JS-driven validation across all required fields; and architect the success path to behave correctly whether the submission used a backend endpoint or the mailto fallback.** The inquiry form is the only conversion event on the site. A buyer spending $3,000–$5,000+ on a discreet made-to-order purchase needs unambiguous confirmation that their message was received — and needs to trust that the operator handles their inquiry with the same care and discretion they applied when writing it.

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

The body text inside `#form-success` is styled at `font-size: 14px; color: var(--muted); line-height: 1.7`, and the inline email link uses `color: var(--gold)` with underline — consistent with every other inline action link on the page.

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
  const els = ['success-email-link','error-email-link','panel-email-link'];
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

The IIFE is defined in the inline `<script>` block that runs after `<script src="assets/site.js">`. `ZX` is therefore already defined when the IIFE executes. All three target elements appear in the HTML above the inline script tag, so `getElementById` calls are synchronous and always find their targets. The injection completes before any async catalog or form logic runs.

---

## 5. Dual Success Path: Endpoint vs Mailto Fallback

The site supports two submission paths: a real `fetch` POST to a backend endpoint, and a mailto fallback if no endpoint is configured. The success state behaves differently depending on which path fired:

```js
function showSuccess(usedMailto) {
  var form     = document.getElementById('inquiry-form');
  var success  = document.getElementById('form-success');
  var chipArea = document.getElementById('char-chip-area');
  if (form)    form.style.display    = 'none';
  if (success) success.style.display = 'block';

  if (!usedMailto) {
    // Endpoint path: suppress the direct-email fallback line
    var p = success.querySelector('p');
    if (p) p.innerHTML = 'We will be in touch discreetly within one business day.';
  }
  // Update success email link with real href
  var email = ZX.INQUIRY_EMAIL || 'inquiries@zelexdoll.com';
  var sl = document.getElementById('success-email-link');
  if (sl) { sl.href = 'mailto:' + email; sl.textContent = email; }
}
```

**Exact condition for each path:**

- `showSuccess(false)` — called immediately when `res.ok` is truthy (HTTP 2xx) in the fetch `.then()` handler. The endpoint is only tried when `ZX.FORM_ENDPOINT` is a non-empty string.
- `showSuccess(true)` — called inside a `setTimeout(..., 400)` in the `else` branch (no `FORM_ENDPOINT`). The 400ms delay gives the browser a moment to open the native email client before the form is replaced. There is no fetch involved in this path; `window.location.href = mailto` fires immediately and the delay is purely UX.

**Behavioral difference:**

- **Endpoint path (`usedMailto = false`):** The backend received the submission. The direct-email fallback line is suppressed; the confirmation shows only "We will be in touch discreetly within one business day." Showing the "you may also reach us at…" line would imply the endpoint might not have worked.
- **Mailto path (`usedMailto = true`):** The buyer's email client opened with a pre-composed inquiry. The full `<p>` is left intact, including the "You may also reach us directly at [email]" line — reinforcing that the same address they emailed is the correct point of contact.

The character chip (`#char-chip-area`) is fetched inside `showSuccess` but is not hidden. It remains visible above the success state on character-originated inquiries — preserving the "you're inquiring about X" context while the form is replaced.

This dual behavior requires only one success-screen element and one function call. The path decision (`usedMailto` boolean) is made in the form submission handler upstream.

---

## 6. Validation: All Required Fields

The form uses `novalidate` to disable browser native validation. All validation is JS-driven through the `validate()` function, which checks four fields and tracks the first invalid one for focus:

```js
function validate() {
  var ok = true;
  var firstBad = null;
  // ... checks name, email, message, consent
  if (firstBad) { try { firstBad.focus(); } catch(e) {} }
  return ok;
}
```

A `clearErrors()` call resets all error states before each submission attempt.

### Fields validated

| Field | Check | Error element | Error text |
|---|---|---|---|
| Name | `name.trim()` non-empty | `#err-name` | "Please enter your name." |
| Email | regex `/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/` | `#err-email` | "Please enter a valid email address." |
| Message | `msg.trim().length < 10` | `#err-message` | "Please include a short message so we can assist you." |
| Consent checkbox | `consent.checked` | `#err-consent` | "Please confirm you are 18+ to proceed." |

Phone and country are optional fields — they carry no validation gate.

### Error UI

Each invalid field receives two simultaneous changes:

1. **Field highlight:** `err-field` class is added to the `<input>` or `<textarea>`, switching `border-color` to `var(--coral)`.
2. **Inline error text:** `show` class is added to the `.field-err` `<div>` immediately below the field, making it visible (`display: none` → `display: block`). The text is site-branded at `font-size: 11px; color: var(--coral)`.

Both are applied via `showFieldError(fieldId, errId, show)`, which handles the add/remove symmetrically so the same function clears errors on a corrected field.

### Why 10 characters for message

- Fewer than 10 trimmed characters cannot constitute a coherent inquiry. Single-word submissions ("hello", "price?") provide no information for the operator to act on.
- 10 is a floor, not a target. A buyer writing a real inquiry will easily exceed it; the threshold only rejects empty or near-empty submissions.
- Native browser `minlength` validation fires at typing-time and varies in error presentation across browsers. JS validation fires at submit, after the full message has been written — a better UX for a textarea where typing cadence is irregular.

### Why regex for email

The regex `/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/` validates that the value has exactly one `@`, a non-empty local part, and a domain with a TLD of at least two characters. It is not RFC 5321 exhaustive — it accepts all common formats while blocking obviously invalid inputs ("foo", "foo@", "@bar.com"). The error message says "valid email address" rather than specifying format requirements, which avoids confusing buyers with technical constraint language.

The `novalidate` attribute removes the browser's default validation UI entirely, so all error messages are site-branded and consistent with the design system.

---

## 7. Character-Originated Inquiries: the `?id=` Prefill Path

When a buyer clicks an inquiry link on a character's catalog card, the URL arrives as `contact.html?id=<body_code>`. The `prefill()` function reads this parameter after the catalog loads and customizes the form in two ways.

### Character chip

A character identification chip is injected into `#char-chip-area` — the empty `<div>` that sits between the breadcrumb and the form in the DOM:

```js
chipArea.innerHTML =
  '<div class="char-chip">' +
    thumbHtml +                          // <img> or initial placeholder
    '<div class="chip-info">' +
      '<div class="chip-label">You\'re inquiring about</div>' +
      '<div class="chip-name">' + ZX.esc(name) + '</div>' +
      '<div class="chip-sub">' + ZX.esc(title) + ' · ' + ZX.esc(bc) + ' · ' + ZX.esc(series) + ZX.esc(price) + '</div>' +
    '</div>' +
  '</div>';
```

The chip shows: the character's catalog thumbnail (or a Playfair Display initial if no image), the `chip-label` "You're inquiring about" in gold uppercase, the character name in Playfair Display at 18px, and a subtitle line with persona title, body code, series, and price. The thumbnail is `52×70px`, cropped `object-position: top center` — the face-priority crop used throughout the catalog.

The chip sits outside `<form id="inquiry-form">` and is not hidden when `showSuccess` fires. On the success screen, the buyer can still see which character they inquired about — useful confirmation that the pre-composed email or backend payload referenced the correct character.

### Character field prefill

The free-text character input is replaced with a readonly display value and a hidden input:

```js
charGroup.innerHTML =
  '<label>Character of interest</label>' +
  '<div class="readonly-field">' + ZX.esc(prefillVal) + '</div>' +
  '<input type="hidden" name="character" value="' + ZX.esc(prefillVal) + '">';
```

`prefillVal` is constructed as `name — body_code (series) · body_family`, pulling from the catalog record. The hidden input ensures the prefilled character value is still included in the form submission payload (both the fetch JSON and the mailto body) without allowing the buyer to accidentally overwrite it.

### Fallback behavior

If `?id=` is absent, or if the catalog fails to load, or if the ID does not match any catalog record, `prefill()` returns early and the form renders in its default state: free-text character field, no chip. The form is fully functional without the prefill path.

The hero backdrop image also uses `?id=` — if the ID resolves to a catalog character, that character's image is used as the backdrop; otherwise a representative catalog image is selected.

---

## 8. Commercial Translation

The contact form is the single conversion event in the Atlas. Every design decision in this PDR is an argument for inquiry completion:

| Decision | Conversion effect |
|---|---|
| Playfair Display success heading | Matches the site's luxury register; signals the inquiry entered the correct channel |
| "Discreetly within one business day" | Reduces post-submission anxiety for privacy-sensitive buyers; sets a clear response expectation |
| Direct-email fallback line (mailto path) | Provides a recovery path if the buyer suspects the mailto didn't send correctly |
| Endpoint-path suppression of fallback line | Prevents ambiguity about where the submission went; keeps the confirmation clean |
| JS email injection | Reduces spam exposure to the inquiry inbox; single point of update |
| Character chip + prefill | Reduces friction for catalog-originated inquiries; pre-qualifies the lead with character and price context |
| 10-char message minimum | Blocks noise submissions; operator only receives actionable inquiries |
| Email regex validation | Catches mistyped addresses at submit time, before a silently-failed submission |
| Consent checkbox + focus-on-first-error | Ensures legal consent is captured; auto-focuses the first failing field to reduce abandonment |

A buyer who reads "Your inquiry has been received. We will be in touch discreetly within one business day." has no remaining uncertainty about submission status. Reducing post-submission uncertainty is the last friction point between an intent signal and a confirmed lead.

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
| Mailto success path shows direct-email link | ✓ `showSuccess(true)` after 400ms timeout; full `<p>` left intact |
| Message field validates at 10-character trimmed minimum | ✓ `msg.trim().length < 10` gate in `validate()` |
| Email field validates against regex pattern | ✓ `validateEmail()` with `/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/` |
| Name field validates as non-empty | ✓ `name.trim()` check in `validate()` |
| Consent checkbox validates as checked | ✓ `consent.checked` gate; error "Please confirm you are 18+ to proceed." |
| Error UI: `err-field` class on input + `show` class on `.field-err` div | ✓ `showFieldError()` applies both simultaneously |
| First invalid field receives focus on failed submit | ✓ `firstBad.focus()` at end of `validate()` |
| Form uses `novalidate` (JS-only validation) | ✓ Attribute present on `<form id="inquiry-form">` |
| Character chip injected into `#char-chip-area` when `?id=` present | ✓ `prefill()` function; chip persists through success state |
| Character field replaced with readonly display + hidden input on prefill | ✓ `charGroup.innerHTML` replacement in `prefill()` |

### Implementation Notes

- The `wireEmailLinks` IIFE is defined in the inline `<script>` block, which runs after `<script src="assets/site.js">` loads. `ZX` is therefore defined before the IIFE executes. The three link elements (`success-email-link`, `error-email-link`, `panel-email-link`) appear in the HTML above the inline script tag — `getElementById` calls are synchronous and always resolve. Do not move the inline script above those elements.
- `ZX.INQUIRY_EMAIL` is the canonical email source. The inline fallback `'inquiries@zelexdoll.com'` in both `wireEmailLinks` and `showSuccess` is a safety net for local development without the ZX module. In production, `ZX.INQUIRY_EMAIL` should always be defined.
- The `form-success` and `form-error` elements are always present in the DOM (not dynamically created). Their initial `display: none` is set in CSS via `#form-success,#form-error{display:none}`. The `showSuccess` / `showError` functions toggle to `display: block`. `getElementById` calls in those functions are always valid.
- The `showError` function re-enables the submit button and hides the spinner, allowing the buyer to retry. `showSuccess` does not re-enable the button — the form is hidden entirely, so the button state is irrelevant.
- `ZX.FORM_ENDPOINT` is configured in `assets/site.js` (constant `FORM_ENDPOINT`). When it is an empty string (the default), the mailto path fires. Setting it to a Formspree, Getform, or custom endpoint URL activates the fetch path. The inline HTML includes a comment block documenting this configuration step.
- The `prefill()` function is called inside `ZX.load().then(...)`. If the catalog fetch fails, `prefill()` is never called and `#char-chip-area` remains an empty `<div>`. The form remains fully functional.
