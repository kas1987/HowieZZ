# GTM + GA4 Implementation Guide — ZELEX Character Atlas

**Version:** 2026-06-21  
**Status:** Ready for Deployment  
**Schema Version:** 2026-06-06

---

## Executive Summary

This document describes the complete Google Tag Manager (GTM) and Google Analytics 4 (GA4) implementation for the ZELEX Character Atlas. The system captures **50+ custom events** across all user journeys (browse, compare, quiz, contact, configurator, community) with built-in PII scrubbing and real-time debugging.

**Key Deliverables:**

1. ✅ **GTM Container Configuration** (`gtm-schema.json`)
2. ✅ **GA4 Event Schema** (50+ events with dataLayer structure)
3. ✅ **PII Scrubber & Audit** (automatic detection and removal)
4. ✅ **Event Tracking Module** (50+ convenience functions)
5. ✅ **Testing & Deployment Guide** (local, staging, production)
6. ✅ **Debug Console** (one-click event inspection)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Action on Page                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │  Page-Specific Tracking Code   │
        │  (e.g., trackQuizComplete)     │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │   ZX.EventTracker Module       │
        │  (50+ tracking functions)      │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │  ZX.track(eventName, payload)  │
        │  (site.js — core emitter)      │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │  PIIScrubber.scrubPayload()    │
        │  (removes PII, validates)      │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │  window.dataLayer.push()       │
        │  (emits to GTM/GA4)            │
        └────────────┬───────────────────┘
                     │
        ┌────────────┴───────────────────┐
        │                                 │
        ▼                                 ▼
   ┌──────────────┐              ┌──────────────┐
   │     GTM      │              │   Console    │
   │  Container   │              │    Event     │
   │  (tag mgr)   │              │     Log      │
   └──────┬───────┘              └──────────────┘
          │
          ▼
   ┌──────────────┐
   │     GA4      │
   │  Property    │
   │ (analytics)  │
   └──────────────┘
```

---

## Implementation Files

### Core Analytics Files

| File | Purpose | Size | Load Order |
|------|---------|------|-----------|
| `assets/ga4-init.js` | GTM container init + dataLayer bootstrap | ~2KB | 1st (in `<head>`) |
| `assets/site.js` | Core `ZX.track()` emitter + data models | ~24KB | 2nd (before page init) |
| `assets/pii-scrubber.js` | PII detection & auto-scrubbing | ~8KB | 3rd (wraps track()) |
| `assets/event-tracking.js` | 50+ tracking function convenience API | ~28KB | 4th (after site.js) |

### Documentation & Configuration

| File | Purpose |
|------|---------|
| `docs/GA4-EVENT-SCHEMA.md` | Complete dataLayer schema + 50+ event definitions |
| `docs/GA4-TESTING-GUIDE.md` | Local, staging, production testing checklist |
| `docs/ANALYTICS-INJECTION.html` | HTML snippet showing correct script load order |
| `docs/GTM-GA4-IMPLEMENTATION.md` | This file |
| `assets/gtm-schema.json` | GTM container export template (for manual import) |

---

## Setup Instructions

### Phase 1: Google Tag Manager Setup

#### 1a. Create GTM Container

1. Go to **Google Tag Manager** → **Accounts**
2. Click **+ Create Account**
3. Account name: `ZELEX` (or your preference)
4. Container name: `zelexdoll.com`
5. Target platform: **Web**
6. Click **Create**
7. Accept terms, copy your **Container ID** (format: `GTM-XXXXXXX`)

#### 1b. Update `assets/ga4-init.js`

```javascript
// Replace this:
const GTM_CONTAINER_ID = 'REPLACE_WITH_CONTAINER_ID';
const GA4_MEASUREMENT_ID = 'REPLACE_WITH_GA4_MEASUREMENT_ID';

// With your actual IDs:
const GTM_CONTAINER_ID = 'GTM-ABC12345';
const GA4_MEASUREMENT_ID = 'G-XXXXXXXXXX';
```

#### 1c. (Optional) Import Pre-Built Container

1. In GTM, go to **Admin** → **Container settings**
2. Click **Export container** (to back up) or **Import container**
3. Upload `assets/gtm-schema.json` (after replacing placeholders)

This will create the base tag & trigger setup. Then customize as needed.

### Phase 2: Google Analytics 4 Setup

#### 2a. Create GA4 Property

1. Go to **Google Analytics** → **Admin** → **Properties**
2. Click **Create Property**
3. Property name: `ZELEX Character Atlas`
4. Reporting timezone: `America/New_York` (or your preference)
5. Currency: `USD`
6. Click **Create**
7. Copy your **Measurement ID** (format: `G-XXXXXXXXXX`)

#### 2b. Link GTM to GA4

In GTM:
1. **Tags** → Create new tag
2. Tag type: **Google Analytics: GA4 Configuration**
3. Measurement ID: `G-XXXXXXXXXX` (from 2a)
4. Trigger: **All Pages**
5. Click **Save**

#### 2c. Create Custom Event Definitions in GA4

For each event in the GA4 Event Schema, create a custom event:

1. Go to GA4 **Admin** → **Events**
2. Click **+ Create event**
3. Event name: `page_view`
4. Matching condition: `event` equals `page_view`
5. Click **Create event** → **Save**
6. **Repeat for all 50+ events** (or use GTM auto-mapping)

### Phase 3: Custom Dimensions & Metrics

#### 3a. Create Custom Dimensions

In GA4 **Admin** → **Custom Definitions** → **Custom Dimensions**:

| Dimension | Parameter | Scope |
|-----------|-----------|-------|
| Session ID | `session_id` | Session |
| Source Page | `source_page` | User |
| Intent | `intent` | User |
| Timeline | `timeline` | User |

#### 3b. Create Custom Metrics

In GA4 **Admin** → **Custom Definitions** → **Custom Metrics**:

| Metric | Parameter | Type |
|--------|-----------|------|
| Quiz Duration | `quiz_duration_sec` | Seconds |
| Time on Page | `time_spent_sec` | Seconds |
| Compare Count | `compare_count` | Standard |

#### 3c. Flag Conversions

In GA4 **Admin** → **Conversions**:

- [ ] `contact_form_submit` → Mark as **Conversion**
- [ ] `quiz_complete` → Mark as **Conversion**
- [ ] `newsletter_signup_success` → Mark as **Conversion**

### Phase 4: Data Privacy & Policies

#### 4a. Enable Data Governance

1. GA4 **Admin** → **Data Collection and modification** → **Data Policies**
2. Enable **Data-driven attribution** (if desired)
3. Set **Data retention**: 14 months
4. Add prohibited fields to Data Protection policies

#### 4b. Review PII Scrubber

Review `assets/pii-scrubber.js`:

- [ ] Email regex matches your expectations
- [ ] Phone regex includes all regional formats
- [ ] Prohibited field list is complete
- [ ] No false positives in test data

---

## Local Development Testing

### Quick Start

1. **Clone the repo and run local server:**
   ```bash
   cd E:\HowieZZ\.claude\worktrees\amazing-tu-a4bd34
   python serve.py
   # Opens http://localhost:8000
   ```

2. **Enable analytics debug mode:**
   ```
   http://localhost:8000/index.html?zx_analytics_debug=1
   ```

3. **Open browser console (F12):**
   ```
   Look for [ZX analytics] prefixed logs
   ```

4. **Verify dataLayer:**
   ```javascript
   // In console:
   console.table(window.dataLayer);
   ```

### Testing Event Categories

See `docs/GA4-TESTING-GUIDE.md` § Local Testing for detailed steps:

- Page views
- Navigation events
- Browse & filter
- Comparison tool
- Quiz flow
- Contact form
- Error handling
- PII scrubbing

---

## Staging Deployment

1. Replace GTM/GA4 IDs in `assets/ga4-init.js` with **staging** container/property
2. Deploy to staging server
3. Run full test suite (see GA4-TESTING-GUIDE.md)
4. Monitor GA4 Real-Time for 1+ hour
5. Check for PII leaks: GA4 Admin → Data Protection
6. Get sign-off from team

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] All staging tests pass
- [ ] No PII detected in GA4
- [ ] 50+ events firing correctly
- [ ] Custom dimensions/metrics active
- [ ] Conversion events configured
- [ ] Team access granted to GA4 dashboard
- [ ] Data retention policy set
- [ ] Rollback plan documented

### Deployment Steps

1. Update **all HTML templates** with correct script injection order (see ANALYTICS-INJECTION.html)
2. Replace GTM/GA4 IDs in `assets/ga4-init.js` with **production** IDs
3. Commit and push:
   ```bash
   git add assets/ga4-init.js
   git commit -m "feat: deploy GA4 + GTM analytics (production)"
   git push origin main
   ```
4. Verify in GA4 Real-Time within 1–2 minutes
5. Monitor for 24 hours for any anomalies

### Post-Deployment Monitoring

- **Hour 1:** Real-time event flow, no errors
- **Day 1:** Event counts, custom dimensions, conversions
- **Week 1:** Trend analysis, data quality, PII audit
- **Month 1:** Funnel analysis, user segments, ROI

---

## Event Categories Overview

### 1. Navigation & Page Views (6 events)

Fired whenever user navigates between pages or lands on a page.

```javascript
ZX.EventTracker.trackPageView('navigation');
ZX.EventTracker.trackNavigate('index.html', 'Browse All', 'explore');
ZX.EventTracker.trackNavigateSeries('K-Series', 'index.html');
ZX.EventTracker.trackNavigateBody('ICON-2203', 'The Muse', 'browse.html');
ZX.EventTracker.trackNavigateCharacter('K-001-Muse', 'ICON-2203', 'K-Series', 'browse.html');
```

### 2. Browse & Filter (8 events)

Fired during catalog exploration and filtering.

```javascript
ZX.EventTracker.trackBrowseView(false);
ZX.EventTracker.trackBrowseFilterApply('series', 'K-Series', ['K-001', 'K-002']);
ZX.EventTracker.trackBrowseFilterClear();
ZX.EventTracker.trackBrowseSortApply('height', 'ascending');
ZX.EventTracker.trackSeriesView('K-Series');
ZX.EventTracker.trackBodyView('ICON-2203', 'The Muse', 'K-Series', 170, 'C-cup');
ZX.EventTracker.trackCharacterView('K-001-Muse', 'ICON-2203', 'K-Series', 'The Muse', 'Akira');
```

### 3. Comparison Tool (6 events)

Fired during body comparison workflows.

```javascript
ZX.EventTracker.trackCompareView(['ICON-2203', 'SIREN-1505']);
ZX.EventTracker.trackCompareAdd('ICON-2203', 'browse.html', 1);
ZX.EventTracker.trackCompareRemove('SIREN-1505', 1);
ZX.EventTracker.trackCompareReset(2);
ZX.EventTracker.trackCompareMetricInspect('WHR', 'ICON-2203');
ZX.EventTracker.trackCompareHandoffClick('inquire', 'compare.html', ['ICON-2203'], 1);
```

### 4. Quiz (9 events)

Fired during "Find Your Character" quiz flow.

```javascript
ZX.EventTracker.trackQuizStart('browse.html');
ZX.EventTracker.trackQuizQuestionView(1);
ZX.EventTracker.trackQuizAnswerSelect(1, 'elegant');
ZX.EventTracker.trackQuizQuestionSkip(2);
ZX.EventTracker.trackQuizAnswerChange(1, 'minimalist');
ZX.EventTracker.trackQuizComplete('The Muse', ['K-001-Muse'], 95);
ZX.EventTracker.trackQuizAbandon(3, 60);
ZX.EventTracker.trackQuizResultToContact(['K-001-Muse']);
ZX.EventTracker.trackQuizResultToBrowse();
```

### 5. Contact & Inquiry (10 events)

Fired during contact form interactions.

```javascript
ZX.EventTracker.trackContactView('K-001-Muse', 'character.html');
ZX.EventTracker.trackContactFormFocus('email');
ZX.EventTracker.trackContactFormInput('email');
ZX.EventTracker.trackContactFormBlur('email');
ZX.EventTracker.trackContactFormValidate('email', null);  // success
ZX.EventTracker.trackContactFormValidate('email', 'invalid_format');  // error
ZX.EventTracker.trackContactFormSubmit(3);  // 3 fields
ZX.EventTracker.trackContactFormSuccess();
ZX.EventTracker.trackContactFormError('network_error', 'Failed to submit');
ZX.EventTracker.trackContactMailtoClick('K-001-Muse');
ZX.EventTracker.trackInquiryPrefillDetect('K-001-Muse');
```

### 6. Configurator (6 events)

Fired during live customization tool.

```javascript
ZX.EventTracker.trackConfiguratorView('index.html');
ZX.EventTracker.trackConfiguratorOptionSelect('color', 'rose_gold');
ZX.EventTracker.trackConfiguratorPreviewUpdate('color');
ZX.EventTracker.trackConfiguratorSaveConfig('config_abc123');
ZX.EventTracker.trackConfiguratorShareConfig('config_abc123');
ZX.EventTracker.trackConfiguratorToInquiry('config_abc123');
```

### 7. Media & Downloads (5 events)

Fired for image/video/PDF interactions.

```javascript
ZX.EventTracker.trackMediaView('image', 'K-001-Muse Hero Shot', 'K-001-Muse', 'ICON-2203');
ZX.EventTracker.trackMediaFullScreen('K-001-Muse Detail', 'K-001-Muse');
ZX.EventTracker.trackMediaCarouselNav('image', 2, 5);
ZX.EventTracker.trackDownloadStart('pdf', '/assets/specs/ICON-2203.pdf', 'K-001-Muse');
ZX.EventTracker.trackDownloadComplete('pdf', 2.5);
```

### 8. Community (5 events)

Fired for social/community engagement.

```javascript
ZX.EventTracker.trackCommunityView('index.html');
ZX.EventTracker.trackCommunityChannelLink('instagram', 'https://instagram.com/zelexdoll');
ZX.EventTracker.trackCommunityEventView('Summer Meetup 2026', 'instagram');
ZX.EventTracker.trackCommunityEventRegister('Summer Meetup 2026', '2026-07-15');
ZX.EventTracker.trackShareClick('twitter', 'K-001-Muse', 'ICON-2203');
```

### 9. Errors (4 events)

Fired when something goes wrong.

```javascript
ZX.EventTracker.trackErrorPageLoad('data_load_failed', 'Failed to fetch characters.json');
ZX.EventTracker.trackErrorDataFetch('json_parse_error', 'Invalid JSON', 'db/characters.json');
ZX.EventTracker.trackErrorFormValidation('contact', 'email', 'invalid_format', 'Must be valid email');
ZX.EventTracker.trackErrorAnalyticsDebug('scrubber_error', 'PII regex failed');
```

### 10. Engagement Metrics (4 events)

Fired for time-based / scrolling metrics.

```javascript
ZX.EventTracker.trackScrollDepth(50);  // User scrolled to 50% of page
ZX.EventTracker.trackTimeOnPage(120);  // User spent 120 seconds on page
ZX.EventTracker.trackViewportResize(1920, 1080);
ZX.EventTracker.trackLinkClick('Browse All', 'browse.html', 'index.html');
```

### 11. Newsletter (3 events)

Fired for email signup flow.

```javascript
ZX.EventTracker.trackNewsletterSignupView('index.html');
ZX.EventTracker.trackNewsletterSignupSubmit();
ZX.EventTracker.trackNewsletterSignupSuccess();
```

### 12. Intent & Funnel (5 events)

Fired to track user journey through conversion funnel.

```javascript
ZX.EventTracker.trackFunnelExplore('browse');
ZX.EventTracker.trackFunnelConsider('ICON-2203', 'compare');
ZX.EventTracker.trackFunnelCompare(2);
ZX.EventTracker.trackFunnelInquire('K-001-Muse', 'compare.html');
ZX.EventTracker.trackFunnelAbandon('quiz.html', 45);
```

---

## PII Scrubbing Details

### Automatic Scrubbing

Every call to `ZX.track()` automatically:

1. **Checks field names** against prohibited list (email, phone, address, etc.)
2. **Scans field values** against PII regex patterns (email format, phone format, SSN, etc.)
3. **Truncates** error_message to 180 chars
4. **Removes** any field matching either rule

### Debug PII Scrubbing

```javascript
// Enable audit mode
ZX.PIIScrubber.enableAudit();

// Trigger a suspected leak
window.dataLayer.push({
  event: 'test_leak',
  email: 'user@example.com',  // This will be removed
  phone: '+1-555-123-4567'     // This will be removed
});

// View what was removed
console.log(ZX.PIIScrubber.getAuditLog());

// Export as CSV for review
console.log(ZX.PIIScrubber.exportAudit('csv'));
```

### Validate Individual Events

```javascript
// Check a single event before emission
const report = ZX.PIIScrubber.validateEvent('contact_form_submit', {
  event: 'contact_form_submit',
  form_name: 'contact',
  email: 'user@example.com'  // PII
});

console.log(report);
// { valid: false, errors: ["Field 'email' contains PII"], ... }
```

---

## Monitoring & Alerts

### GA4 Real-Time Dashboard

1. Go to **GA4 > Real-time**
2. **Realtime Users** card shows active visitors
3. Click **Event** column to see recent events
4. **Page URL** shows which pages are sending events

Expected behavior:
- Events appear within 1–2 seconds
- Event count matches user actions
- No suspicious PII in event details

### Weekly PII Audit

```javascript
// Run in production console (dev tools)
ZX.PIIScrubber.enableAudit();
// ... let site run for a while ...
const log = ZX.PIIScrubber.exportAudit('csv');
// Copy/paste into spreadsheet
```

Expected result: Empty audit log (no PII detected)

### Custom Event Report

1. GA4 → **Events** report
2. Verify all expected events are listed:
   - page_view
   - quiz_complete
   - contact_form_submit
   - compare_add
   - etc.

### Conversion Funnel Analysis

1. GA4 → **Exploration > Funnel Analysis**
2. Add steps:
   - page_view (step 1)
   - funnel_explore (step 2)
   - funnel_consider (step 3)
   - funnel_compare (step 4)
   - contact_form_submit (step 5 — conversion)
3. Analyze drop-off points

---

## Troubleshooting

### Q: Events not appearing in GA4 Real-Time

**Check:**
1. GTM/GA4 IDs are correct in `assets/ga4-init.js`
2. No JavaScript errors in console (F12)
3. `window.dataLayer` exists and is an array
4. Wait 1–2 minutes (GA4 Real-Time has delay)

**Fix:** See GA4-TESTING-GUIDE.md § Troubleshooting

### Q: PII appears in GA4 despite scrubbing

**Check:**
1. Is PII scrubber loaded? `ZX.PIIScrubber` should exist
2. Load order: ga4-init.js → site.js → pii-scrubber.js → event-tracking.js
3. Check audit log: `ZX.PIIScrubber.getAuditLog()`

**Fix:** Update PII regex patterns or add field to prohibited list

### Q: Session ID not persisting

**Check:**
1. Are you in private/incognito mode? (sessionStorage often disabled)
2. Check browser storage: `sessionStorage.getItem('zx_analytics_session_id')`
3. Check local storage: `localStorage.getItem('zx_analytics_session_id')`

**Fix:** Reload page in normal browsing mode

---

## References

- **GA4 Event Implementation:** https://developers.google.com/analytics/devguides/collection/ga4/events
- **GTM Best Practices:** https://support.google.com/tagmanager/answer/6103696
- **dataLayer Schema:** https://support.google.com/tagmanager/answer/6164391
- **GA4 Custom Dimensions:** https://support.google.com/analytics/answer/10075209
- **Data Protection:** https://support.google.com/analytics/answer/9019185

---

## Support

For questions or issues:

1. Check **GA4-TESTING-GUIDE.md** for common solutions
2. Review **GA4-EVENT-SCHEMA.md** for event details
3. Enable debug mode: `?zx_analytics_debug=1`
4. Export audit log: `ZX.PIIScrubber.exportAudit('csv')`
5. Contact analytics team with debug output

---

**End of Implementation Guide**
