# GA4 Testing & Deployment Guide — ZELEX Character Atlas

**Schema Version:** 2026-06-06  
**Last Updated:** 2026-06-21

---

## Pre-Deployment Checklist

### 1. GTM Container Setup

- [ ] Create a new GTM Container (or use existing)
- [ ] Note the **Container ID** (format: GTM-XXXXXXX)
- [ ] In `assets/ga4-init.js`, replace:
  - `REPLACE_WITH_CONTAINER_ID` → your Container ID
  - `REPLACE_WITH_GA4_MEASUREMENT_ID` → your GA4 Measurement ID

### 2. GA4 Property Setup

- [ ] Create GA4 property in Google Analytics
- [ ] Note the **Measurement ID** (format: G-XXXXXXXXXX)
- [ ] Enable **Google Signals** (Admin > Data Collection > Google Signals)
- [ ] Set **Data retention** to 14 months (Admin > Data Settings)
- [ ] Create custom event definitions (see GA4 Event Schema doc)

### 3. PII Data Policy

- [ ] Review `assets/pii-scrubber.js` — confirm all PII patterns match your risk profile
- [ ] Enable **Data Protection** in GA4 Admin > Data Policies
- [ ] Exclude prohibited field list: email, phone, address, ssn, credit_card, etc.
- [ ] Test scrubber with `?zx_analytics_debug=1`

---

## Local Testing

### Step 1: Enable Debug Mode

Open any page with the debug flag:

```
http://localhost:8000/index.html?zx_analytics_debug=1
```

Or:

```
http://localhost:8000/index.html?zx_analytics_debug=1&zx_env=test
```

### Step 2: Monitor Console Logs

Open **Developer Tools** (F12) → **Console** tab.

Look for:

- `[ZX analytics]` — every event fired
- `[EventTracker]` — event tracking module messages
- `[PIIScrubber]` — PII detection/scrubbing actions
- `[ga4-init]` — GTM/GA4 initialization status

Example console output:

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

### Step 3: Inspect dataLayer

In the console, type:

```javascript
console.table(window.dataLayer);
```

This prints all events emitted to the dataLayer in a table format.

### Step 4: Test Key Flows

#### Page View Event
1. Load any page with `?zx_analytics_debug=1`
2. Should see `page_view` event in console within 1 second

#### Quiz Tracking
1. Navigate to `quiz.html?zx_analytics_debug=1`
2. Click "Begin" → should see `quiz_start`
3. Select answer → should see `quiz_answer_select`
4. Answer all 5 questions → should see `quiz_complete` with `quiz_result_family` and `quiz_result_characters`

#### Browse & Filter
1. Navigate to `browse.html?zx_analytics_debug=1`
2. Click a filter chip (e.g., "K-Series") → should see `browse_filter_apply`
3. Click a body card → should see `navigate_body` or `body_view`

#### Comparison Tool
1. Navigate to `compare.html?zx_analytics_debug=1`
2. Add a body from browse (or via direct link) → should see `compare_add` or `compare_view`
3. Click on comparison metric → should see `compare_metric_inspect`

#### Contact Form
1. Navigate to `contact.html?zx_analytics_debug=1` (or `contact.html?id=K-Series-001-Muse`)
2. Focus on a field → should see `contact_form_focus`
3. Type in field → should see `contact_form_input`
4. Blur field → should see `contact_form_blur`
5. Submit → should see `contact_form_submit` and `contact_form_success` (or `contact_form_error`)

#### PII Scrubbing
1. Manually trigger in console:
   ```javascript
   window.dataLayer.push({
     event: 'test_pii_leak',
     email: 'user@example.com',
     phone: '+1-555-123-4567',
     user_input: 'Hello, my name is John Doe'
   });
   ```
2. Should see console warning: `Removed PII fields: ['email', 'phone', 'user_input']`
3. Check that the event was not pushed to dataLayer with PII

### Step 5: GA4 Real-Time Debugger (if GTM/GA4 connected)

1. In Google Analytics, go to **Real-time** report
2. On your local site, trigger an event
3. Check that the event appears in Real-time within 1–2 seconds
4. Click the event to inspect full payload

---

## Staging Testing

### Deploy to Staging

1. Replace GTM/GA4 IDs in `assets/ga4-init.js` with **staging** container/property IDs
2. Deploy code to staging server
3. Do NOT yet enable in production GTM

### Test Event Flow

1. Open staging site: `https://staging.zelexdoll.com/`
2. Append `?zx_analytics_debug=1`
3. Perform all key user flows (see Local Testing § Step 4)
4. Open GA4 Real-Time → confirm events appear

### Monitor for Errors

```javascript
// In console, check for analytics errors:
window.ZX.analyticsStatus
```

Output should show:

```javascript
{
  gtmLoaded: true,
  ga4Loaded: true,
  gtmId: "GTM-XXXXXXX",
  ga4Id: "G-XXXXXXXXXX",
  dataLayerReady: true
}
```

### QA Checklist

- [ ] All 50+ events fire on correct user actions
- [ ] Session ID persists across page refreshes
- [ ] No PII fields appear in GA4 (Admin > Data Policies > Data Governance)
- [ ] Custom dimensions (session_id, source_page, intent) appear in reports
- [ ] Custom metrics (quiz_duration_sec, time_spent_sec) are logged
- [ ] Conversion events flagged in GA4 actually convert:
  - `contact_form_submit` → conversion
  - `quiz_complete` → conversion
  - `newsletter_signup_success` → conversion

---

## Production Deployment

### Final Checklist

- [ ] All staging tests pass
- [ ] PII scrubber has caught and removed test PII
- [ ] GA4 Real-Time shows 50+ events
- [ ] No console errors in DevTools
- [ ] Custom events appear in GA4 event list
- [ ] Team has access to GA4 dashboard
- [ ] Data retention policy is set

### Step-by-Step Deploy

1. **Update HTML templates** to include GA4 scripts in correct order:

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <!-- ... other head tags ... -->
     
     <!-- 1. GA4 Initialization (MUST be first) -->
     <script src="assets/ga4-init.js"></script>
   </head>
   <body>
     <!-- 2. GTM noscript fallback (inserted by ga4-init.js) -->
     
     <!-- 3. Main content -->
     
     <!-- 4. Site JS (at end of body) -->
     <script src="assets/site.js"></script>
     
     <!-- 5. PII Scrubber (runs before any tracking) -->
     <script src="assets/pii-scrubber.js"></script>
     
     <!-- 6. Event Tracking (uses ZX.track) -->
     <script src="assets/event-tracking.js"></script>
     
     <!-- 7. Page-specific initialization -->
     <script>
       ZX.load().then(model => {
         // Initialize page
       }).catch(() => {
         ZX.fail();
       });
     </script>
   </body>
   </html>
   ```

2. **Replace placeholders:**
   - In `assets/ga4-init.js`:
     - `REPLACE_WITH_CONTAINER_ID` → **production** Container ID
     - `REPLACE_WITH_GA4_MEASUREMENT_ID` → **production** Measurement ID

3. **Push to production:**
   ```bash
   git add assets/ga4-init.js assets/event-tracking.js assets/pii-scrubber.js
   git commit -m "feat: deploy GA4 + GTM analytics (production)"
   git push origin main
   ```

4. **Verify in GA4:**
   - Real-time report should show events within 1–2 seconds
   - Custom events should be in the event list
   - Conversion events should track properly

---

## Monitoring & Maintenance

### Daily Checks

1. **GA4 Real-time** → Any events coming in? If not, check:
   - GTM container ID is correct
   - GA4 Measurement ID is correct
   - No JS console errors
   - Analytics debug mode still working

2. **Data Quality** → In GA4, check:
   - No PII fields in custom events
   - Event count trending correctly
   - Conversion rates reasonable

### Weekly Checks

1. **Custom Events** → GA4 Admin > Events
   - All expected events should be listed
   - Any new events from bad tracking? Investigate.

2. **Custom Dimensions** → GA4 Admin > Custom Definitions
   - Session_id, source_page, intent showing?
   - Dimensions have reasonable cardinality?

3. **Data Governance** → GA4 Admin > Data Policies
   - Is data scrubbing active?
   - Any PII flags? (Should be zero)

### Monthly Checks

1. **Event Trends** → GA4 Events report
   - User count trending up/down?
   - New user / returning user ratio healthy?
   - Conversion rate stable?

2. **Funnel Analysis** → GA4 Exploration > Funnel Analysis
   - Does the flow look right: explore → consider → compare → inquire?
   - Any unexpected drop-off points?

3. **Audit Log** → Console memory (if audit enabled)
   ```javascript
   ZX.PIIScrubber.exportAudit('csv')  // Export scrubber audit log
   ```

---

## Troubleshooting

### Events Not Appearing in GA4 Real-Time

**Diagnosis:**

```javascript
// In console:
console.log(window.ZX.analyticsStatus);
```

**Fix checklist:**

- [ ] GTM container ID is correct (not `REPLACE_WITH_CONTAINER_ID`)
- [ ] GA4 property ID is correct
- [ ] GA4 property is actually receiving data (check in GA4 Admin)
- [ ] No JS errors preventing script load (check DevTools Console)
- [ ] Wait 1–2 minutes (GA4 Real-time has slight delay)

### PII Being Logged

**Diagnosis:**

```javascript
ZX.PIIScrubber.enableAudit();
// Trigger suspected PII leak
console.log(ZX.PIIScrubber.getAuditLog());
```

**Fix:**

- [ ] Add field name to `PROHIBITED_FIELDS` set in `pii-scrubber.js`
- [ ] Or add PII pattern to `PII_PATTERNS` regex
- [ ] Redeploy and test

### dataLayer Events Not Pushing

**Diagnosis:**

```javascript
// Manually push test event
window.dataLayer.push({
  event: 'test_manual',
  session_id: 'test_' + Date.now()
});
```

**Fix:**

- [ ] Confirm `window.dataLayer` exists: `console.log(window.dataLayer)`
- [ ] Confirm ZX.track() is being called
- [ ] Check for JS errors in console that stop execution
- [ ] Confirm ga4-init.js is loaded first

### Session ID Not Persisting

**Diagnosis:**

```javascript
console.log(sessionStorage.getItem('zx_analytics_session_id'));
console.log(localStorage.getItem('zx_analytics_session_id'));
```

**Expected:** Same ID should persist across page reloads.

**Fix:**

- [ ] Not using private/incognito mode (sessionStorage often disabled)
- [ ] Check browser storage permissions
- [ ] Confirm `createSessionId()` is running on first page load

---

## Event Validation Report Template

Use this when investigating missing events:

```markdown
## Event Validation Report

**Date:** 2026-06-21  
**Page:** index.html  
**Browser:** Chrome 120  

### Events Expected

- [ ] page_view
- [ ] series_nav
- [ ] (list any others)

### Events Observed (Console)

```
[ZX analytics] { event: 'page_view', ... }
[ZX analytics] { event: 'navigate', ... }
```

### GA4 Real-Time

- [ ] Events appeared within 2 seconds?
- [ ] Custom fields populated correctly?
- [ ] No PII detected?

### Issues Found

- Issue 1: Description
- Issue 2: Description

### Resolution

- Fixed by: ...
- Verified: Y/N
```

---

## Rollback Plan

If analytics causes issues in production:

```bash
# Remove GA4 scripts from HTML (revert to last known-good)
git revert <commit-with-ga4>
git push origin main

# Disable in GTM (temporarily)
# Go to GTM container → Tags → disable GA4 tag → Publish
```

Once disabled, investigate in staging before re-enabling.

---

## References

- [GA4 Event Implementation Guide](https://developers.google.com/analytics/devguides/collection/ga4/events)
- [GTM Troubleshooting](https://support.google.com/tagmanager/answer/7237751)
- [Data Protection in GA4](https://support.google.com/analytics/answer/9019185)
- [GA4 Real-Time Reports](https://support.google.com/analytics/answer/9271545)
