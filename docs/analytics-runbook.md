# Analytics & GTM Runbook

**Status:** Active (Phase 1)  
**Last Updated:** 2026-06-21  
**Owner:** Analytics / Product  
**Audience:** Analytics team, product, data engineers

---

## Overview

This runbook explains how to manage Google Tag Manager (GTM), test GA4 events, debug data quality issues, and maintain the analytics dashboard. All events are captured via GTM and flow into Google Analytics 4 (GA4).

---

## Architecture

```
Website (assets/site.js)
├─ Fires events to dataLayer
│
GTM Container (zelexdoll.com)
├─ Variables: page, user ID, event properties
├─ Triggers: on event firing
├─ Tags: send to GA4, send to 3rd-party analytics
│
GA4 Property (zelexdoll)
├─ Events (100+ event types)
├─ Dimensions (page, family, character, user properties)
├─ Metrics (sessions, events, conversions)
│
Looker Studio Dashboard
└─ Visualizations of GA4 data
```

---

## GTM Setup

### GTM Container ID

**Container:** `GTM-XXXXXX` (created in Google Tag Manager)

**Location:** In every page's `<head>` section:

```html
<script>
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXX');
</script>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
```

### Accessing GTM

1. Go to https://tagmanager.google.com/
2. Select **ZELEX** account
3. Select **zelexdoll.com** container
4. Click **Workspace** to edit

---

## Event Firing & DataLayer

### DataLayer Schema

Every event pushed to the dataLayer includes:

```javascript
{
  "event": "quiz_start",                  // Event name
  "event_original": "quiz_start",         // Original event (for debugging)
  "source": "howiezz-web",                // Always "howiezz-web"
  "schema_version": "2026-06-21",         // Date of schema
  "session_id": "abc123xyz789",           // Session identifier
  "ts": "2026-06-21T14:32:00Z",          // Event timestamp (ISO 8601)
  "page": "quiz.html",                    // Current page
  "path": "/quiz.html",                   // Page path
  
  // Event-specific properties
  "quiz_family": "The Muse",              // For quiz_start
  "quiz_result": "The Siren",             // For quiz_complete
  "entry_source": "browse",               // Entry point (browse|family|etc)
  "entry_cta": "take-quiz",               // CTA clicked
  "character_id": "Fusion-ZF161D-01",    // For character detail events
  "compare_count": 3,                     // For compare events
  
  // Custom user properties
  "user_id": "user_123abc",               // Persistent user ID (if known)
  "session_duration": 45,                 // Seconds since session start
}
```

### Pushing Events in site.js

```javascript
// In assets/site.js
ZX.analytics = function(event, properties) {
  const payload = {
    event: event,
    event_original: event,
    source: "howiezz-web",
    schema_version: "2026-06-21",
    session_id: ZX.getSessionId(),
    ts: new Date().toISOString(),
    page: document.title,
    path: window.location.pathname,
    ...properties  // Merge event-specific properties
  };
  
  window.dataLayer.push(payload);
  console.log('[GTM]', event, payload);  // Debug logging
};

// Usage
ZX.analytics('quiz_start', {
  quiz_family: 'The Muse',
  entry_source: 'browse',
  entry_cta: 'take-quiz'
});
```

### Event Categories

**Quiz Events:**
- `quiz_start` — User starts quiz
- `quiz_answer` — User answers a question
- `quiz_complete` — User completes quiz
- `quiz_result_view` — User views results

**Character Events:**
- `character_detail_view` — User views character page
- `character_gallery_scroll` — User scrolls gallery
- `character_related_click` — User clicks related character

**Comparison Events:**
- `compare_start` — User enters comparison tool
- `compare_add` — User adds body to comparison
- `compare_remove` — User removes body from comparison
- `compare_handoff_click` — User clicks "Handoff to Inquiry"

**Contact Form Events:**
- `inquiry_form_start` — User starts inquiry form
- `inquiry_form_prefill` — Form auto-prefills (from character)
- `inquiry_validation_failed` — Form validation error
- `inquiry_submit_attempt` — User attempts to submit
- `inquiry_submit_success` — Form submitted successfully
- `inquiry_submit_error` — Server error on submit

**Page Events:**
- `page_view` — User loads any page
- `page_scroll` — User scrolls past 25%, 50%, 75%, 100%
- `scroll_depth` — Depth of scroll on page

---

## Testing Events

### Browser Debug Mode

Enable analytics debugging in browser console:

```javascript
// Enable debug mode
localStorage.setItem('zx_analytics_debug', '1');
location.reload();

// Disable debug mode
localStorage.setItem('zx_analytics_debug', '0');
location.reload();
```

**With debug mode enabled:**
- All events logged to console
- DataLayer visible in DevTools
- GTM Preview mode activated

### GTM Preview Mode

1. In GTM Workspace, click **Preview** (top right)
2. Enter site URL: https://zelexdoll.com/ or http://localhost:8000
3. A new tab opens with GTM debug panel
4. Every GTM tag fired shows in the panel with payload

**Debug panel shows:**
- `Tags Fired` — Which GA4 tags executed
- `Variables` — Resolved variable values
- `Data Layer` — Current dataLayer state
- `Errors` — Any GTM configuration errors

### QA Checklist: Event Firing

```bash
# 1. Load site in browser with debug mode
# Open DevTools Console

# 2. Test quiz flow
- Go to quiz.html
- Check console: "quiz_start" event logged
- Answer 5 questions
- Check console: 5 "quiz_answer" events logged
- Finish quiz
- Check console: "quiz_complete" + "quiz_result_view" events logged

# 3. Test character detail
- Go to character.html?id=Fusion-ZF161D-01
- Check console: "character_detail_view" event logged
- Scroll gallery
- Check console: "character_gallery_scroll" event logged
- Click related character
- Check console: "character_related_click" event logged

# 4. Test comparison
- Go to browse.html
- Add 2 bodies to compare
- Check console: 2 "compare_add" events logged
- Remove 1 body
- Check console: "compare_remove" event logged
- Click handoff
- Check console: "compare_handoff_click" event logged

# 5. Test contact form
- Go to contact.html
- Check console: "inquiry_form_start" event logged
- Fill form
- Check console: "inquiry_validation_failed" or "inquiry_submit_attempt" events
- Submit
- Check console: "inquiry_submit_success" event logged
```

### Automated Event Validation

```bash
python scripts/analytics_event_sanity.py \
  --input docs/pdr/PDR-analytics-sample-events.ndjson \
  --strict
```

**Output:**

```
Validating event payload...
✓ All required fields present
✓ Event schema matches v2026-06-21
✓ Session continuity preserved
✓ PII audit clean (no emails, phones)
✓ Total events: 8
✓ Unique event types: 5
✓ Funnel completion rate: 62.5%
Status: PASS
```

---

## GA4 Configuration

### GA4 Property Setup

**Property:** zelexdoll (Google Analytics 4)

**Steps to configure (if not already done):**

1. **Create GA4 property**
   - https://analytics.google.com/
   - Create Property: "zelexdoll"
   - Select "Web" as data stream

2. **Link to GTM**
   - In GA4, go to Admin → Data Streams → Web
   - Copy Measurement ID: `G-XXXXXX`
   - In GTM, create GA4 Configuration Tag
   - Set Measurement ID: `G-XXXXXX`

3. **Configure custom events**
   - Admin → Custom Definitions → Create Custom Event
   - Event name: `quiz_start`, `character_detail_view`, etc.
   - Set scope: Event

4. **Configure custom dimensions**
   - Admin → Custom Definitions → Create Custom Dimension
   - Dimension name: `entry_source`, `character_id`, `quiz_family`, etc.
   - Set scope: Event

---

## Debugging GA4 Events

### Issue: Events not appearing in GA4

**Cause:** GTM tag misconfigured, event not firing, or 48-hour propagation delay

**Diagnosis:**

1. **Check GTM Preview mode** (see Testing Events above)
   - Verify tag fires when expected
   - Check payload in Real-time tab

2. **Check GA4 Real-time Report**
   - https://analytics.google.com/ → Reports → Real-time
   - Trigger event (e.g., visit quiz.html)
   - Should see event in Real-time within 1 second

3. **Check dataLayer push**
   ```javascript
   // Console
   console.log(window.dataLayer);
   // Should show all events pushed
   ```

**Fix:**

1. **Verify event name in dataLayer matches GA4 event config**
   - Example: `quiz_start` in dataLayer should be `quiz_start` in GA4

2. **Verify GA4 tag is triggered**
   - In GTM, check GA4 tag's Trigger (should be "All Pages" or custom trigger)

3. **Wait 24-48 hours** for GA4 to process (initial propagation delay)

### Issue: Events firing but custom dimensions missing

**Cause:** Custom dimension not configured in GA4, or wrong scope

**Diagnosis:**

1. **Verify custom dimension exists in GA4**
   ```
   Admin → Custom Definitions → Custom Dimensions
   Look for "entry_source", "character_id", etc.
   ```

2. **Check dimension scope**
   - Should be **Event** scope for per-event properties
   - Should be **User** scope for persistent user properties

3. **Verify dataLayer has the property**
   ```javascript
   console.log(window.dataLayer[window.dataLayer.length - 1]);
   // Should have "entry_source", "character_id", etc.
   ```

**Fix:**

1. **Create missing custom dimension in GA4**
   - Admin → Custom Definitions → Create Custom Dimension
   - Parameter name (in dataLayer): `entry_source`
   - Dimension name: "Entry Source"
   - Scope: Event

2. **Re-map variable in GTM**
   - Variables → Create Variable → Data Layer Variable
   - Variable name: `entry_source`
   - Data Layer Variable Name: `entry_source`
   - Add to GA4 Configuration Tag as custom parameter

### Issue: PII in GA4 (emails, phone numbers)

**Cause:** User data captured in dataLayer without scrubbing

**Diagnosis:**

```bash
# Check for PII in sample events
python scripts/audit_datalayer_pii.py \
  --input docs/pdr/PDR-analytics-sample-events.ndjson
```

**Output:**

```
Scanning for PII...
✗ Found 3 potential email addresses in "user_email" field
✗ Found 2 potential phone numbers in "contact_phone" field
⚠ These fields should NOT be sent to GA4
Recommendation: Remove from dataLayer or use hash/pseudonym
```

**Fix:**

1. **Remove sensitive fields from dataLayer**
   ```javascript
   // BAD: Don't do this
   ZX.analytics('inquiry_submit_success', {
     user_email: 'user@example.com',  // ❌ PII
     user_phone: '555-1234'           // ❌ PII
   });
   
   // GOOD: Use hashed or anonymous identifiers
   ZX.analytics('inquiry_submit_success', {
     user_id: hashEmail(user_email),  // Hash the email
     session_id: 'abc123xyz789'       // Use session ID instead
   });
   ```

2. **Audit dataLayer in site.js**
   - Search for: `email`, `phone`, `address`, `name`, `credit_card`
   - Remove or anonymize before pushing to dataLayer

---

## Dashboard Setup

### Looker Studio Dashboard

**URL:** https://looker.studio/ (sign in with ZELEX brand account)

**Existing Dashboard:** "ZELEX Analytics Dashboard" (shared with team)

### Dashboard Sections

**1. Traffic Overview**
- Page views by page
- Sessions by traffic source
- User retention (return visitor %)

**2. Funnel Analysis**
- Quiz starts → Completions
- Character views → Inquiry attempts
- Comparison sets → Handoffs

**3. Engagement**
- Most viewed characters
- Most compared bodies
- Quiz result distribution

**4. Competitive Positioning**
- Family coverage (which families drive most views)
- Family-to-inquiry conversion rate
- Family comparison heatmap

### Refreshing Dashboard

Looker Studio auto-refreshes GA4 data daily. **Manual refresh:**

1. Open dashboard
2. Click **Refresh** (icon, top right)
3. Wait for data to reload (~5 seconds)

---

## Data Quality Monitoring

### Daily Health Check

```bash
# Run morning health check
python scripts/analytics_event_sanity.py \
  --input docs/pdr/PDR-analytics-smoke-test-checklist.md \
  --strict
```

**Expected output:**

```
✓ Event volume: 8000+ events/day
✓ Funnel drop-off: <20% between stages
✓ Session duration: avg 3+ minutes
✓ PII audit: clean (0 violations)
✓ Event latency: <1 second to GA4
Status: HEALTHY
```

### Alerts & Thresholds

Monitor these metrics daily:

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Daily events | >5000 | 2000-5000 | <2000 |
| Quiz completion rate | >60% | 40-60% | <40% |
| Inquiry conversion rate | >5% | 2-5% | <2% |
| Session duration | >3 min | 1-3 min | <1 min |
| PII violations | 0 | 0 | >0 |

**Alert thresholds defined in:** `docs/pdr/PDR-analytics-sanity-thresholds.json`

---

## Troubleshooting Common Issues

### Issue: GA4 shows 0 events after deployment

**Cause:** GTM tag not deployed, GTM container ID wrong, or GA4 tag misconfigured

**Diagnosis:**

```bash
# 1. Check page has GTM container
curl https://zelexdoll.com/index.html | grep GTM-

# 2. Check GTM Preview mode
# (see GTM Preview Mode section)

# 3. Check GA4 Real-time
# (see GA4 Debugging section)
```

**Fix:**

1. **Verify GTM container ID in page head**
   - Should be `GTM-XXXXXX` in all pages
   - Use `grep GTM- *.html` to check

2. **Publish GTM workspace**
   - In GTM Workspace, click **Publish** (top right)
   - Select "Production" version
   - This deploys all tags to live site

3. **Wait 5-10 minutes** for GTM container to update globally

### Issue: Quiz events fire, but "quiz_complete" missing

**Cause:** Event not pushed at end of quiz, or form validation blocking submit

**Diagnosis:**

```javascript
// Check quiz.html JavaScript
// Look for "quiz_complete" event firing in quiz submission
```

**Fix:**

1. **Verify quiz.js fires the event**
   ```javascript
   // In quiz.html script section
   form.addEventListener('submit', (e) => {
     e.preventDefault();
     ZX.analytics('quiz_complete', {
       quiz_family: selectedFamily,
       quiz_result: result_family
     });
     // Then submit
   });
   ```

2. **Test in browser DevTools**
   ```javascript
   // Manually trigger event
   ZX.analytics('quiz_complete', { quiz_family: 'The Muse' });
   ```

### Issue: Dashboard shows no data (blank charts)

**Cause:** GA4 data source not connected, or date range set incorrectly

**Diagnosis:**

1. **Check GA4 data source connection**
   - Open Looker Studio dashboard
   - Click **Edit** (pencil icon)
   - Check data source: should be "Google Analytics 4"
   - Should show "zelexdoll" property

2. **Check date range**
   - Bottom of dashboard should show date range (e.g., "Last 7 days")
   - Make sure it includes data-generating period

**Fix:**

1. **Re-connect GA4 data source**
   - Click data source name
   - Click **Reconnect**
   - Sign in with ZELEX brand account
   - Select "zelexdoll" property

2. **Update date range**
   - Click date filter
   - Select "Last 30 days" or custom range

---

## Advanced: Custom Reports

### Creating a Custom Report in GA4

1. **Go to GA4:** https://analytics.google.com/
2. **Select "zelexdoll" property**
3. **Click "Reports" → "Create New Report"**
4. **Configure:**
   - Dimensions: Page, Event Name, Entry Source
   - Metrics: Event Count, Session Duration
   - Filters: Event Name = "quiz_complete"
5. **Save as:** "Quiz Completion Analysis"

### Exporting Data from GA4

```bash
# Use GA4 API to export raw event data
python scripts/export_ga4_data.py \
  --property-id G-XXXXXX \
  --date-range 2026-06-01:2026-06-21 \
  --output reports/events-june.csv
```

---

## FAQ

**Q: How often is GA4 data updated?**

A: Real-time data updates every 1-2 seconds. Historical data (reports) refreshes every 4-24 hours.

**Q: Can I track user email in GA4?**

A: No. Use a hashed user ID instead. See PII section above.

**Q: How do I set up conversion tracking?**

A: Mark any event as a "conversion" in GA4:
- Admin → Conversions → Create New Conversion
- Select event: `inquiry_submit_success`
- This event now counts as a conversion in reports

**Q: Can I A/B test using GA4?**

A: Yes, using Experiments feature:
- Reports → Experimentation
- Create new experiment
- Track conversion event (e.g., quiz_complete)

**Q: How long does GA4 keep data?**

A: 14 months (events) + 2 years (aggregated reports).

---

## Support

For analytics issues:
1. Check this runbook (search by keyword)
2. Check GTM Preview mode (see Testing Events)
3. Check GA4 Real-time report
4. Review GA4 documentation: https://support.google.com/analytics
5. Open issue: `chore(analytics): [your issue]`

---

## References

- **Source PDR:** `docs/pdr/PDR-ANALYTICS-001-gtm-ga4.md`
- **Event Taxonomy:** `docs/pdr/PDR-analytics-event-taxonomy.md`
- **Dashboard Cookbook:** `docs/pdr/PDR-analytics-dashboard-cookbook.md`
- **Sanity Check:** `docs/pdr/PDR-analytics-sanity-thresholds.json`
- **GTM Docs:** https://support.google.com/tagmanager
- **GA4 Docs:** https://support.google.com/analytics
