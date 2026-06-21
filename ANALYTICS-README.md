# GTM + GA4 Analytics — ZELEX Character Atlas

**Status:** Production-Ready | **Version:** 2026-06-21 | **Schema:** 2026-06-06

Complete Google Tag Manager (GTM) + Google Analytics 4 (GA4) implementation with **50+ custom events**, PII scrubbing, and real-time debugging.

---

## What You Get

✅ **GTM Container Configuration** — Ready-to-import JSON template  
✅ **GA4 Event Schema** — 50+ events with dataLayer definitions  
✅ **PII Auto-Scrubber** — Removes email, phone, addresses before emission  
✅ **Event Tracking API** — 50+ convenience functions (no raw dataLayer calls)  
✅ **Debug Console** — One-click event inspection with `?zx_analytics_debug=1`  
✅ **Testing Guide** — Local → staging → production validation  
✅ **Audit Logging** — CSV export for compliance review  

---

## Quick Start (5 minutes)

### 1. Get Your IDs

**GTM Container:**
1. Go to [Google Tag Manager](https://tagmanager.google.com)
2. Create account/container → copy **Container ID** (GTM-XXXXXXX)

**GA4 Measurement:**
1. Go to [Google Analytics](https://analytics.google.com)
2. Create GA4 property → copy **Measurement ID** (G-XXXXXXXXXX)

### 2. Update `assets/ga4-init.js`

```javascript
// Line 11-12: Replace these placeholders
const GTM_CONTAINER_ID = 'GTM-ABC12345';       // Your GTM ID
const GA4_MEASUREMENT_ID = 'G-XXXXXXXXXX';     // Your GA4 ID
```

### 3. Add Scripts to HTML (Correct Order!)

```html
<!DOCTYPE html>
<html>
<head>
  <!-- 1. GA4 init (MUST be first) -->
  <script src="assets/ga4-init.js"></script>
</head>
<body>
  <!-- 2. Site core + tracking modules (before page init) -->
  <script src="assets/site.js"></script>
  <script src="assets/pii-scrubber.js"></script>
  <script src="assets/event-tracking.js"></script>

  <!-- 3. Page-specific tracking -->
  <script>
    ZX.load().then(model => {
      // Page content here...
      ZX.EventTracker.trackPageView('navigation');
    });
  </script>
</body>
</html>
```

### 4. Test Locally

```bash
# Terminal 1: Start local server
python serve.py
# Opens http://localhost:8000

# Terminal 2 (browser): Enable debug mode
http://localhost:8000/index.html?zx_analytics_debug=1

# Browser DevTools (F12): View events
[ZX analytics] { event: 'page_view', session_id: 'zx_...', ... }
```

### 5. Deploy to Production

```bash
git add assets/ga4-init.js
git commit -m "analytics: set production GTM/GA4 IDs"
git push
```

**Verify in GA4 Real-Time within 2 minutes.**

---

## File Structure

```
assets/
├── ga4-init.js                 # GTM + GA4 bootstrap (2KB)
├── event-tracking.js           # 50+ tracking functions (28KB)
├── pii-scrubber.js            # PII auto-removal (8KB)
├── gtm-schema.json            # GTM container template
├── site.js                     # Core framework (unchanged)
└── site.css                    # Styles (unchanged)

docs/
├── GA4-EVENT-SCHEMA.md         # Complete event taxonomy
├── GA4-TESTING-GUIDE.md        # Testing procedures
├── GTM-GA4-IMPLEMENTATION.md   # Full setup guide
├── ANALYTICS-INJECTION.html    # HTML snippet reference
├── ANALYTICS-QUICK-REFERENCE.md # One-page cheat sheet
└── (this file)
```

---

## Event Categories (50+ Events)

### 1. Navigation & Page Views (6)
```javascript
trackPageView()
trackNavigate()
trackNavigateSeries()
trackNavigateFamily()
trackNavigateBody()
trackNavigateCharacter()
```

### 2. Browse & Filter (8)
```javascript
trackBrowseView()
trackBrowseFilterApply()
trackBrowseFilterClear()
trackBrowseSortApply()
trackSeriesView()
trackBodyView()
trackCharacterView()
```

### 3. Comparison (6)
```javascript
trackCompareView()
trackCompareAdd()
trackCompareRemove()
trackCompareReset()
trackCompareMetricInspect()
trackCompareHandoffClick()
```

### 4. Quiz (9)
```javascript
trackQuizStart()
trackQuizQuestionView()
trackQuizAnswerSelect()
trackQuizQuestionSkip()
trackQuizAnswerChange()
trackQuizComplete()
trackQuizAbandon()
trackQuizResultToContact()
trackQuizResultToBrowse()
```

### 5. Contact Form (10)
```javascript
trackContactView()
trackContactFormFocus()
trackContactFormInput()
trackContactFormBlur()
trackContactFormValidate()
trackContactFormSubmit()
trackContactFormSuccess()
trackContactFormError()
trackContactMailtoClick()
trackInquiryPrefillDetect()
```

### 6. Configurator (6)
```javascript
trackConfiguratorView()
trackConfiguratorOptionSelect()
trackConfiguratorPreviewUpdate()
trackConfiguratorSaveConfig()
trackConfiguratorShareConfig()
trackConfiguratorToInquiry()
```

### 7. Media (5)
```javascript
trackMediaView()
trackMediaFullScreen()
trackMediaCarouselNav()
trackDownloadStart()
trackDownloadComplete()
```

### 8. Community (5)
```javascript
trackCommunityView()
trackCommunityChannelLink()
trackCommunityEventView()
trackCommunityEventRegister()
trackShareClick()
```

### 9. Errors (4)
```javascript
trackErrorPageLoad()
trackErrorDataFetch()
trackErrorFormValidation()
trackErrorAnalyticsDebug()
```

### 10. Engagement (4)
```javascript
trackScrollDepth()
trackTimeOnPage()
trackViewportResize()
trackLinkClick()
```

### 11. Newsletter (3)
```javascript
trackNewsletterSignupView()
trackNewsletterSignupSubmit()
trackNewsletterSignupSuccess()
```

### 12. Funnel (5)
```javascript
trackFunnelExplore()
trackFunnelConsider()
trackFunnelCompare()
trackFunnelInquire()
trackFunnelAbandon()
```

---

## Usage Examples

### Quiz Tracking
```javascript
ZX.EventTracker.trackQuizStart('browse.html');
ZX.EventTracker.trackQuizQuestionView(1);
ZX.EventTracker.trackQuizAnswerSelect(1, 'elegant');
// ... questions 2-5 ...
ZX.EventTracker.trackQuizComplete('The Muse', ['K-001-Muse'], 95);
```

### Comparison Workflow
```javascript
ZX.EventTracker.trackCompareAdd('ICON-2203', 'browse.html', 1);
ZX.EventTracker.trackCompareAdd('SIREN-1505', 'browse.html', 2);
ZX.EventTracker.trackCompareView(['ICON-2203', 'SIREN-1505']);
ZX.EventTracker.trackCompareMetricInspect('WHR', 'ICON-2203');
ZX.EventTracker.trackCompareHandoffClick('inquire', 'compare.html', ['ICON-2203', 'SIREN-1505'], 2);
```

### Contact Form
```javascript
ZX.EventTracker.trackContactView('K-001-Muse', 'character.html');
ZX.EventTracker.trackContactFormFocus('email');
ZX.EventTracker.trackContactFormInput('email');
ZX.EventTracker.trackContactFormSubmit(3);
ZX.EventTracker.trackContactFormSuccess();
```

### Error Tracking
```javascript
try {
  const data = await fetch('db/characters.json').then(r => r.json());
} catch (err) {
  ZX.EventTracker.trackErrorDataFetch('json_parse_error', err.message, 'db/characters.json');
  ZX.fail();
}
```

---

## Debug Mode

### Enable
```
http://localhost:8000/index.html?zx_analytics_debug=1
```

### Console Output
```
[ZX analytics] {
  event: 'page_view',
  session_id: 'zx_1234567_abcdef12',
  ts: '2026-06-21T14:30:45.123Z',
  page: 'index.html',
  path: '/',
  source: 'howiezz-web'
}
```

### Inspect All Events
```javascript
console.table(window.dataLayer);
```

### Check Analytics Status
```javascript
console.log(window.ZX.analyticsStatus);
// {
//   gtmLoaded: true,
//   ga4Loaded: true,
//   gtmId: "GTM-ABC12345",
//   ga4Id: "G-XXXXXXXXXX",
//   dataLayerReady: true
// }
```

---

## PII Protection

### Automatic Scrubbing

Every event is automatically scanned for:
- Email addresses (`user@example.com`)
- Phone numbers (`+1-555-123-4567`)
- Social Security numbers (`123-45-6789`)
- Postal codes (`12345`)
- Addresses (streets, avenues, etc.)
- Credit cards (`1234 5678 9012 3456`)

**Matching fields are removed before GA4 receives them.**

### Prohibited Field Names

These are **always removed**, regardless of value:

```
email, phone, address, name, ssn, credit_card,
dob, user_id, password, api_key, ip_address, ...
```

### Manual Audit

```javascript
ZX.PIIScrubber.enableAudit();
// ... interact with site ...
console.table(ZX.PIIScrubber.getAuditLog());

// Export for security review
const csv = ZX.PIIScrubber.exportAudit('csv');
console.log(csv);
```

### Validate Events

```javascript
const report = ZX.PIIScrubber.validateEvent('contact_form_submit', {
  form_name: 'contact',
  email: 'user@example.com'  // Will flag as error
});
console.log(report);
```

---

## Testing Checklist

### Local Testing
- [ ] `?zx_analytics_debug=1` shows events in console
- [ ] `window.dataLayer` contains events
- [ ] Session ID persists across page reloads
- [ ] No PII appears in events (try: `ZX.PIIScrubber.enableAudit()`)
- [ ] Quiz flow fires all expected events
- [ ] Contact form submission tracked
- [ ] Compare tool interactions logged

### Staging Deployment
- [ ] Replace GTM/GA4 IDs with **staging** values
- [ ] Deploy to staging server
- [ ] Open GA4 Real-Time report
- [ ] Trigger events on staging site
- [ ] Verify events appear in Real-Time within 2 seconds
- [ ] Check for PII in GA4 Admin > Data Policies
- [ ] Run full test suite (see GA4-TESTING-GUIDE.md)

### Production Deployment
- [ ] All staging tests pass
- [ ] Replace GTM/GA4 IDs with **production** values
- [ ] Update all HTML templates with correct script order
- [ ] Commit and push to main
- [ ] Monitor GA4 Real-Time for 1+ hour
- [ ] Check custom events in GA4 Admin > Events
- [ ] Verify conversion events are tracking
- [ ] Weekly: Export audit log, check for PII

---

## Real-Time Monitoring

### GA4 Real-Time Dashboard

1. Open Google Analytics → **Real-time**
2. On your site, trigger an action (click a button, fill form, etc.)
3. Event should appear in Real-Time within **1–2 seconds**
4. Click event name to inspect full payload

**Expected fields:**
```
Event name: page_view
Session ID: zx_1234567_abcdef12
User properties:
  - source_page: browse
  - intent: explore
  - timeline: first
```

### Weekly Checks

- [ ] GA4 Real-Time showing events?
- [ ] Custom events in Admin > Events?
- [ ] Custom dimensions appearing?
- [ ] Any PII detected? (Should be 0)
- [ ] Conversion events tracking?

---

## Troubleshooting

### Events Not in GA4

**Problem:** Events fired locally but not showing in GA4 Real-Time.

**Checklist:**
1. GTM/GA4 IDs correct? Check `assets/ga4-init.js`
2. Script load order correct? See ANALYTICS-INJECTION.html
3. No JS errors? Check DevTools Console (F12)
4. Waited 1–2 minutes? GA4 Real-Time has slight delay
5. GA4 property receiving data? Check GA4 Admin

**Fix:** Re-check IDs, reload page, wait 2 minutes, try again.

### PII Appearing in GA4

**Problem:** Sensitive data leaking into analytics.

**Debug:**
```javascript
ZX.PIIScrubber.enableAudit();
// Trigger suspected leak
console.log(ZX.PIIScrubber.getAuditLog());
```

**Fix:**
- Add field name to `PROHIBITED_FIELDS` in `pii-scrubber.js`
- Or update PII regex pattern
- Redeploy and test

### Session ID Changes

**Problem:** Different session_id on each page.

**Likely cause:** Browser storage (sessionStorage/localStorage) disabled.

**Check:**
```javascript
console.log(sessionStorage.getItem('zx_analytics_session_id'));
```

**Fix:** Not using private/incognito mode? Browser storage permissions correct?

---

## Configuration Reference

### Placeholder Replacements

| Placeholder | Meaning | Example |
|-------------|---------|---------|
| `REPLACE_WITH_CONTAINER_ID` | GTM container ID | `GTM-ABC12345` |
| `REPLACE_WITH_GA4_MEASUREMENT_ID` | GA4 measurement ID | `G-XXXXXXXXXX` |
| `REPLACE_WITH_ACCOUNT_ID` | Google Account ID | (from GTM) |

### GTM Trigger Setup

**Tag:** GA4 - Page View  
**Trigger:** All Pages

**Tag:** GA4 - Custom Events  
**Trigger:** Custom Event - dataLayer push

### GA4 Custom Events

Run in GA4 Admin > Events to create custom events for each of the 50+ event names.

### GA4 Custom Dimensions

- `session_id` → Session scope
- `source_page` → User scope
- `intent` → User scope
- `timeline` → User scope

### GA4 Custom Metrics

- `quiz_duration_sec` → Seconds
- `time_spent_sec` → Seconds
- `compare_count` → Standard

### GA4 Conversions

Mark these as conversions:
- `contact_form_submit`
- `quiz_complete`
- `newsletter_signup_success`

---

## Documentation

- **GA4-EVENT-SCHEMA.md** — Complete dataLayer schema (50+ events)
- **GA4-TESTING-GUIDE.md** — Local/staging/production testing
- **GTM-GA4-IMPLEMENTATION.md** — Full setup + deployment
- **ANALYTICS-INJECTION.html** — HTML snippet reference
- **ANALYTICS-QUICK-REFERENCE.md** — One-page cheat sheet

---

## Support & Questions

1. **Console debug:** `?zx_analytics_debug=1`
2. **Check status:** `console.log(window.ZX.analyticsStatus)`
3. **Audit PII:** `ZX.PIIScrubber.getAuditLog()`
4. **Review schema:** See GA4-EVENT-SCHEMA.md
5. **Test procedures:** See GA4-TESTING-GUIDE.md

---

## Compliance & Privacy

- ✅ **GDPR-ready** — No personal data in events by design
- ✅ **CCPA-ready** — PII auto-scrubber prevents leaks
- ✅ **Audit trail** — CSVexport of scrubbed fields for compliance
- ✅ **Data minimization** — Only essential fields captured
- ✅ **Anonymized sessions** — Session IDs are pseudo-random, not user identifiable

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-06-21 | 1.0.0 | Initial release: 50+ events, PII scrubber, GTM/GA4 integration |

---

**Status:** Production-Ready  
**Last Updated:** 2026-06-21  
**Maintained By:** Analytics Team

For bugs or features, create an issue or contact the analytics team.
