# Analytics Quick Reference — ZELEX Character Atlas

**One-page cheat sheet for event tracking, PII audit, and debugging.**

---

## Script Load Order (Critical!)

```html
<!-- 1. In <head> -->
<script src="assets/ga4-init.js"></script>

<!-- 2. Before page init (end of body) -->
<script src="assets/site.js"></script>
<script src="assets/pii-scrubber.js"></script>
<script src="assets/event-tracking.js"></script>
```

---

## Debug Mode

**Enable:** Append `?zx_analytics_debug=1` to any URL

**Disable:** Append `?zx_analytics_debug=0`

**Console Output:**
```javascript
[ZX analytics] { event: 'page_view', ... }
[EventTracker] page_view index.html navigation
[PIIScrubber] Removed PII fields: ['email']
```

---

## Common Tracking Calls

### Page Navigation
```javascript
ZX.EventTracker.trackPageView('navigation');
ZX.EventTracker.trackNavigate('index.html', 'Browse All', 'explore');
ZX.EventTracker.trackNavigateBody('ICON-2203', 'The Muse', 'browse.html');
ZX.EventTracker.trackNavigateCharacter('K-001-Muse', 'ICON-2203', 'K-Series', 'browse.html');
```

### Browse
```javascript
ZX.EventTracker.trackBrowseView(false);
ZX.EventTracker.trackBrowseFilterApply('series', 'K-Series', ['K-001', 'K-002']);
ZX.EventTracker.trackCharacterView('K-001-Muse', 'ICON-2203', 'K-Series', 'The Muse', 'Akira');
```

### Quiz
```javascript
ZX.EventTracker.trackQuizStart('browse.html');
ZX.EventTracker.trackQuizAnswerSelect(1, 'elegant');
ZX.EventTracker.trackQuizComplete('The Muse', ['K-001-Muse'], 95);  // family, chars, duration_sec
ZX.EventTracker.trackQuizAbandon(3, 60);  // question_num, duration_sec
```

### Comparison
```javascript
ZX.EventTracker.trackCompareAdd('ICON-2203', 'browse.html', 1);  // body_code, source, count
ZX.EventTracker.trackCompareView(['ICON-2203', 'SIREN-1505']);
ZX.EventTracker.trackCompareHandoffClick('inquire', 'compare.html', ['ICON-2203'], 1);
```

### Contact Form
```javascript
ZX.EventTracker.trackContactView('K-001-Muse', 'character.html');
ZX.EventTracker.trackContactFormFocus('email');
ZX.EventTracker.trackContactFormInput('email');
ZX.EventTracker.trackContactFormSubmit(3);  // field_count
ZX.EventTracker.trackContactFormSuccess();
ZX.EventTracker.trackContactFormError('network_error', 'Failed to submit');
```

### Errors
```javascript
ZX.EventTracker.trackErrorPageLoad('data_load_failed', 'Failed to fetch');
ZX.EventTracker.trackErrorFormValidation('contact', 'email', 'invalid_format');
```

---

## PII Audit

### Check What's Being Scrubbed
```javascript
ZX.PIIScrubber.enableAudit();
// ... interact with site ...
console.table(ZX.PIIScrubber.getAuditLog());
```

### Export Audit Log
```javascript
// As JSON
const json = ZX.PIIScrubber.exportAudit('json');
console.log(json);

// As CSV
const csv = ZX.PISScrubber.exportAudit('csv');
console.log(csv);
```

### Validate Single Event
```javascript
const report = ZX.PIIScrubber.validateEvent('contact_form_submit', {
  event: 'contact_form_submit',
  form_name: 'contact',
  email: 'user@example.com'  // Will show as error
});
console.log(report);
```

### Test PII Detection
```javascript
console.log(ZX.PIIScrubber.isEmail('user@example.com'));        // true
console.log(ZX.PIIScrubber.isPhone('+1-555-123-4567'));         // true
console.log(ZX.PIIScrubber.isAddress('123 Main St'));           // true
console.log(ZX.PIIScrubber.isPII('hello world'));               // false
```

---

## Analytics Status

```javascript
console.log(window.ZX.analyticsStatus);

// Output:
{
  gtmLoaded: true,
  ga4Loaded: true,
  gtmId: "GTM-ABC12345",
  ga4Id: "G-XXXXXXXXXX",
  dataLayerReady: true
}
```

---

## Event Payload Structure

Every event has this minimum structure:

```javascript
{
  event: string,              // 'page_view', 'quiz_complete', etc.
  session_id: string,         // 'zx_1234567_abcdef12' — persists per session
  ts: ISO 8601,               // '2026-06-21T14:30:45.123Z'
  page: string,               // 'index.html', 'quiz.html', etc.
  path: string,               // '/', '/quiz.html', etc.
  source: 'howiezz-web',      // Source identifier
  schema_version: '2026-06-06'
  // ... plus event-specific fields below
}
```

---

## Event-Specific Fields

| Event | Fields |
|-------|--------|
| `page_view` | `page`, `path`, `source_page` (optional) |
| `navigate` | `source_page`, `cta`, `intent` (optional) |
| `quiz_answer_select` | `quiz_question` (1-5), `quiz_answer` |
| `quiz_complete` | `quiz_result_family`, `quiz_result_characters`, `quiz_duration_sec` |
| `compare_add` | `body_code`, `compare_count`, `source_page` |
| `contact_form_submit` | `form_name` ('contact'), `form_field_count` |
| `browse_filter_apply` | `filter_field`, `filter_value`, `body_codes`, `compare_count` |
| `error_*` | `error_type`, `error_message` (max 180 chars) |

See **GA4-EVENT-SCHEMA.md** for complete list of all 50+ events.

---

## Real-Time Debugging in GA4

1. Open **Google Analytics → Real-time**
2. On site, trigger an event (e.g., click a button)
3. Event should appear in Real-time within 1–2 seconds
4. Click event name to inspect full payload
5. Check **Custom dimensions** column for session_id, source_page, etc.

---

## Deployed IDs (Replace These!)

| Component | Location | Production | Staging | Dev |
|-----------|----------|-----------|---------|-----|
| GTM Container | `assets/ga4-init.js` | `GTM-...` | `GTM-...` | local |
| GA4 Measurement | `assets/ga4-init.js` | `G-...` | `G-...` | local |

---

## PII Prohibited Fields

These field names are **always scrubbed**:

```
email, phone, address, zip_code, postal_code,
name, first_name, last_name, full_name,
street, city, state, country,
credit_card, ccn, card_number,
ssn, social_security,
dob, birthdate, age,
user_id, customer_id, account_id,
password, secret, token, api_key,
ip_address, ip,
user_input, raw_input, form_data
```

## PII Patterns (Auto-Detected)

- Email: `user@example.com`
- Phone: `+1-555-123-4567`, `555.123.4567`, `(555) 123-4567`
- SSN: `123-45-6789`
- Postal: `12345` or `12345-6789`
- Address keywords: street, st, avenue, ave, road, rd, etc.
- Credit card: `1234 5678 9012 3456`

---

## Common Issues

| Issue | Solution |
|-------|----------|
| No events in GA4 | Check GTM/GA4 IDs, verify ga4-init.js loaded, wait 1–2 min |
| PII in GA4 events | Add field to PROHIBITED_FIELDS or update regex in pii-scrubber.js |
| Session ID changes on each page | Browser storage disabled? Check sessionStorage/localStorage |
| Stale debug logs | Run `ZX.PIIScrubber.clearAuditLog()` |
| Script load order wrong | Verify order: ga4-init → site.js → pii-scrubber → event-tracking |

---

## Contact & Inquiry Page Special Handling

### Character Prefill
```javascript
// URL: contact.html?id=K-001-Muse
// Automatically tracked:
ZX.EventTracker.trackInquiryPrefillDetect('K-001-Muse');

// When form submits, also track:
ZX.EventTracker.trackContactFormSubmit(fieldCount);
ZX.EventTracker.trackContactFormSuccess();
```

### Mailto Fallback (no form endpoint)
```javascript
// When user clicks "Inquire via email":
ZX.EventTracker.trackContactMailtoClick('K-001-Muse');
// Then browser opens mailto: (no server submission)
```

---

## Funnel Tracking

Track user journey through decision funnel:

```javascript
// Step 1: User lands and explores
ZX.EventTracker.trackFunnelExplore('browse');

// Step 2: User considers a specific body
ZX.EventTracker.trackFunnelConsider('ICON-2203', 'compare');

// Step 3: User enters comparison tool
ZX.EventTracker.trackFunnelCompare(2);  // 2 bodies compared

// Step 4: User inquires about a character
ZX.EventTracker.trackFunnelInquire('K-001-Muse', 'compare.html');

// (Optional) User abandons without inquiring
ZX.EventTracker.trackFunnelAbandon('quiz.html', 45);  // spent 45 sec on quiz, then left
```

Then in GA4 → Explore → Funnel Analysis, build a funnel:
1. funnel_explore
2. funnel_consider
3. funnel_compare
4. funnel_inquire (mark as conversion)

---

## Documentation Files

| File | Purpose |
|------|---------|
| `GA4-EVENT-SCHEMA.md` | Complete dataLayer schema + 50 event definitions |
| `GA4-TESTING-GUIDE.md` | Local/staging/production testing checklist |
| `GTM-GA4-IMPLEMENTATION.md` | Full setup & deployment guide |
| `ANALYTICS-INJECTION.html` | HTML snippet showing correct script order |
| `ANALYTICS-QUICK-REFERENCE.md` | This file — one-page cheat sheet |

---

**Last Updated:** 2026-06-21  
**Schema Version:** 2026-06-06  
**Status:** Production Ready
