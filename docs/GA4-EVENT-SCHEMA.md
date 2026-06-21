# GA4 Event Schema — ZELEX Character Atlas

**Schema Version:** 2026-06-06  
**Last Updated:** 2026-06-21

This document defines the complete event taxonomy, dataLayer structure, and GA4 event configuration for the ZELEX Character Atlas analytics pipeline.

---

## Table of Contents

1. [Core Event Types](#core-event-types)
2. [dataLayer Schema](#datalayer-schema)
3. [PII Policy](#pii-policy)
4. [Event Taxonomy (50+ Events)](#event-taxonomy-50-events)
5. [GA4 Configuration](#ga4-configuration)
6. [Testing & Validation](#testing--validation)

---

## Core Event Types

All events follow a **canonical event model**:

```javascript
{
  event: string,              // GA4 event name (normalized via EVENT_ALIASES)
  event_original: string,     // Raw event name (before aliasing)
  source: 'howiezz-web',      // Source identifier
  schema_version: '2026-06-06',
  session_id: string,         // Persistent within session
  ts: ISO 8601,               // Event timestamp
  page: string,               // Current page (e.g., 'browse.html')
  path: string,               // Full URL path
  ...custom_fields            // Event-specific payload
}
```

### Event Aliasing

Some events are normalized to canonical names for GA4 cohesion:

```javascript
{
  'compare_add_from_body': 'compare_add',
  'compare_add_from_character': 'compare_add',
  'compare_add_from_compare_page': 'compare_add',
  'compare_to_contact_click': 'compare_handoff_click',
  'compare_to_quiz_click': 'compare_handoff_click',
  'compare_view_empty': 'compare_view'
}
```

---

## dataLayer Schema

### Root dataLayer Object

```javascript
window.dataLayer = [
  {
    // === MANDATORY ===
    event: string,                        // e.g., 'page_view', 'quiz_start'
    session_id: string,                   // e.g., 'zx_1234567_abcdef12'
    ts: '2026-06-21T14:30:45.123Z',       // ISO 8601
    page: string,                         // Current page filename
    path: string,                         // Current path
    source: 'howiezz-web',

    // === OPTIONAL: Core IDs ===
    character_id?: string,                // e.g., 'K-Series-001-Muse'
    body_code?: string,                   // e.g., 'ICON-2203'
    series?: string,                      // e.g., 'K-Series', 'Fusion'
    family?: string,                      // e.g., 'The Muse', 'The Siren'

    // === OPTIONAL: Context ===
    context?: string,                     // 'navigation', 'content', 'interaction'
    source_page?: string,                 // Referrer page
    view_state?: string,                  // 'browse', 'detail', 'compare', 'quiz'
    cta?: string,                         // Call-to-action label

    // === OPTIONAL: Navigation/Content ===
    intent?: string,                      // 'explore', 'compare', 'inquire', 'configure'
    timeline?: string,                    // 'first', 'repeat', 'deep_dive'

    // === OPTIONAL: Engagement ===
    compare_count?: number,               // Number of bodies in comparison
    body_codes?: string,                  // Comma-separated body codes
    filter_applied?: boolean,
    filter_field?: string,
    filter_value?: string,

    // === OPTIONAL: Quiz/Form ===
    quiz_question?: number,               // Question index (1-5)
    quiz_answer?: string,                 // Answer value/label
    quiz_result_family?: string,          // Predicted family
    quiz_result_characters?: string,      // Comma-separated character IDs

    // === OPTIONAL: Form ===
    form_name?: string,                   // 'contact', 'inquiry', 'newsletter'
    form_field?: string,                  // Field being completed
    form_error?: string,                  // Error type if validation fails
    form_complete?: boolean,
    form_submit_success?: boolean,

    // === OPTIONAL: Media ===
    media_type?: string,                  // 'image', 'video', 'pdf'
    media_title?: string,
    download_url?: string,
    file_type?: string,

    // === OPTIONAL: Errors ===
    error_type?: string,                  // 'load_error', 'validation_error'
    error_message?: string,               // Max 180 chars (sanitized)

    // === OPTIONAL: Community ===
    channel?: string,                     // 'instagram', 'discord', 'email'
    event_name?: string,                  // Community event name

    // === OPTIONAL: E-commerce Intent ===
    product_code?: string,
    product_price?: number,
    currency?: string,                    // Default: 'USD'

    // === GTM DEBUG ===
    debug_mode?: boolean,                 // Only in debug mode
  }
]
```

---

## PII Policy

**Golden Rule:** NO email, phone, name, address, or personally identifiable data in dataLayer.

### Prohibited Fields
- Email addresses (user@example.com)
- Phone numbers
- Postal addresses
- Full names
- Birthdate / age details
- Payment information
- IP addresses
- Cookies / session tokens

### Sanitization Rules

1. **Auto-Truncation:** error_message is clamped to 180 chars, all HTML/control chars stripped.
2. **Placeholder Detection:** If a field looks like PII (regex: `@|(\+1|\d{3}[-.\s]?)\d{3}[-.\s]?\d{4}|(?:St|Ave|Rd|Blvd)\s`), it is **dropped entirely** from dataLayer.
3. **Manual Scrubbing:** Fields like `form_field`, `quiz_answer` are allowed to be descriptive but never to contain actual user input (e.g., `form_field: 'email'` ✓, but `form_field_value: 'user@example.com'` ✗).

### Scrubber Implementation

```javascript
// Built into ZX.track() — never emit PII
function scrubbPII(payload) {
  const piiRegex = /@|(\+1|\d{3}[-.\s]?)\d{3}[-.\s]?\d{4}|(?:St|Ave|Rd|Blvd)\s/;
  const piiKeys = ['email', 'phone', 'address', 'name', 'user_id'];
  
  Object.keys(payload).forEach(k => {
    if (piiKeys.includes(k.toLowerCase()) || piiRegex.test(String(payload[k]))) {
      delete payload[k];
    }
  });
  return payload;
}
```

---

## Event Taxonomy (50+ Events)

### Page Navigation

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `page_view` | Every page load | `page`, `path` | `source_page`, `intent` |
| `navigate` | Link click to another page | `source_page`, `cta` | `intent`, `context` |
| `navigate_series` | Series card / link click | `series`, `source_page` | |
| `navigate_family` | Family index click | `family`, `source_page` | |
| `navigate_body` | Body detail link | `body_code`, `source_page` | `family` |
| `navigate_character` | Character card / link | `character_id`, `source_page` | `body_code`, `series` |

### Content Browse & Filter

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `browse_view` | Browse page loaded | | `filter_applied` |
| `browse_filter_apply` | Filter button clicked | `filter_field`, `filter_value` | `body_codes`, `compare_count` |
| `browse_filter_clear` | Clear all filters | | |
| `browse_sort_apply` | Sort order changed | `sort_field`, `sort_order` | |
| `series_view` | Series landing page load | `series` | `series_character_count` |
| `body_view` | Body detail page load | `body_code`, `family` | `series`, `body_height_cm`, `body_cup` |
| `character_view` | Character detail page load | `character_id`, `body_code` | `series`, `family`, `persona_name` |

### Comparison Tool

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `compare_view` | Compare page viewed | | `compare_count`, `body_codes` |
| `compare_add` | Body added to comparison | `body_code` | `compare_count`, `source_page` |
| `compare_remove` | Body removed from comparison | `body_code` | `compare_count` |
| `compare_reset` | Compare cleared | | `compare_count` |
| `compare_metric_inspect` | Metric tooltip/expand | `metric_type` | `body_code` |
| `compare_handoff_click` | From compare → contact or quiz | `intent`, `source_page` | `body_codes`, `compare_count` |

### Quiz ("Find Your Character")

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `quiz_start` | Quiz intro / begin button clicked | | `source_page` |
| `quiz_question_view` | Question screen displayed | `quiz_question` | |
| `quiz_answer_select` | Answer selected (before next) | `quiz_question`, `quiz_answer` | |
| `quiz_question_skip` | Question skipped | `quiz_question` | |
| `quiz_answer_change` | Re-selected answer to same Q | `quiz_question`, `quiz_answer` | |
| `quiz_complete` | All questions answered | `quiz_result_family`, `quiz_result_characters` | `quiz_duration_sec` |
| `quiz_abandon` | Quiz exited without completing | `quiz_question` | `quiz_duration_sec` |
| `quiz_result_to_contact` | From results → contact form | `quiz_result_characters` | |
| `quiz_result_to_browse` | From results → browse page | | |

### Inquiry & Contact

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `contact_view` | Contact form page load | | `character_id`, `source_page` |
| `contact_form_focus` | Form field focused | `form_name`, `form_field` | |
| `contact_form_input` | Form field value entered | `form_name`, `form_field` | |
| `contact_form_blur` | Form field blurred | `form_name`, `form_field` | |
| `contact_form_validate` | Form field validated | `form_name`, `form_field` | `form_error` |
| `contact_form_submit` | Form submitted | `form_name` | `form_complete`, `form_field_count` |
| `contact_form_success` | Server confirms receipt | `form_name`, `form_submit_success` | |
| `contact_form_error` | Form error returned | `form_name`, `form_error`, `error_message` | |
| `contact_mailto_click` | mailto: link clicked (fallback) | `form_name` | `character_id` |
| `inquiry_prefill_detect` | Auto-filled form via ?id= param | `character_id` | `form_name` |

### Configurator

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `configurator_view` | Configurator page load | | `source_page` |
| `configurator_option_select` | Customization option clicked | `option_category`, `option_value` | |
| `configurator_preview_update` | 3D/image preview refreshed | | `option_category` |
| `configurator_save_config` | Configuration saved | | `config_hash` |
| `configurator_share_config` | Share link generated | | |
| `configurator_to_inquiry` | From config → inquiry form | | `config_hash` |

### Media & Downloads

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `media_view` | Image/video viewed | `media_type`, `media_title` | `character_id`, `body_code` |
| `media_full_screen` | Image opened full-screen | `media_title` | `character_id` |
| `media_carousel_nav` | Carousel image advanced | `media_type` | `media_index`, `media_count` |
| `download_start` | Download initiated | `file_type`, `download_url` | `character_id` |
| `download_complete` | Download finished | `file_type` | `file_size_mb` |

### Community & Social

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `community_view` | Community hub page load | | `source_page` |
| `community_channel_link` | Social channel link clicked | `channel` | `channel_url` |
| `community_event_view` | Event detail opened | `event_name`, `channel` | |
| `community_event_register` | Event RSVP/register clicked | `event_name` | `event_date` |
| `share_click` | Share button clicked | `share_channel` | `character_id`, `body_code` |

### Site Errors & Diagnostics

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `error_page_load` | Page failed to load | `error_type`, `page` | `error_message` |
| `error_data_fetch` | JSON/data fetch failed | `error_type` | `error_message`, `endpoint` |
| `error_form_validation` | Form validation failed | `form_name`, `form_field`, `error_type` | `error_message` |
| `error_analytics_debug` | Analytics itself errored | `error_type` | `error_message` |

### Engagement Metrics

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `scroll_depth` | User scrolled to % of page | `scroll_percentage` | |
| `time_on_page` | User spent N seconds on page | `time_spent_sec` | `page` |
| `viewport_resize` | Viewport resized (for analytics) | `viewport_width`, `viewport_height` | |
| `link_click` | Generic link click | `link_text`, `link_url` | `source_page` |

### Newsletter & Opt-In

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `newsletter_signup_view` | Newsletter form shown | | `source_page` |
| `newsletter_signup_submit` | Newsletter form submitted | `form_name` | `form_complete` |
| `newsletter_signup_success` | Server confirms subscription | | |

### Intent & Funnel

| Event | Context | Required Fields | Optional Fields |
|-------|---------|-----------------|-----------------|
| `funnel_explore` | User began exploration | | `intent` |
| `funnel_consider` | User moved to consideration | `body_code` | `intent` |
| `funnel_compare` | User entered comparison | `compare_count` | |
| `funnel_inquire` | User opened inquiry form | | `character_id`, `source_page` |
| `funnel_abandon` | User left without action | | `source_page`, `time_spent_sec` |

---

## GA4 Configuration

### Custom Event Mapping

All events above are **custom events** in GA4. Map them in the GA4 admin console:

**Admin > Events > Create Event** for each custom event:

```
Event name (in GA4): page_view
Event condition: event equals page_view
Create event → Save
```

### Custom Dimensions (User & Session Level)

Configure these in **Admin > Custom Definitions > Custom Dimensions**:

| Dimension Name | Parameter Name | Scope | Type |
|---|---|---|---|
| Session ID | `session_id` | Session | Text |
| Source Page | `source_page` | User | Text |
| Intent | `intent` | User | Text |
| Timeline | `timeline` | User | Text |

### Custom Metrics (Count & Duration)

Configure in **Admin > Custom Definitions > Custom Metrics**:

| Metric Name | Parameter Name | Type | Unit |
|---|---|---|---|
| Quiz Duration | `quiz_duration_sec` | Seconds | second |
| Time on Page | `time_spent_sec` | Seconds | second |
| Comparison Count | `compare_count` | Standard | count |

### Conversion Events

Flag key events as **Conversions** in Admin > Conversions:

- `contact_form_submit` — Mark as conversion
- `quiz_complete` — Mark as conversion
- `newsletter_signup_success` — Mark as conversion

---

## Testing & Validation

### Debug Mode Activation

Append `?zx_analytics_debug=1` to any page URL:

```
https://zelexdoll.com/index.html?zx_analytics_debug=1
```

**Effect:**
- All events logged to browser console via `[ZX analytics]` prefix
- `debug_mode: true` added to each event payload
- Persistent across session via `localStorage.zx_analytics_debug`

Disable with `?zx_analytics_debug=0`

### GA4 Real-Time Debugger

1. Open Google Analytics > Realtime
2. Trigger an event on the site
3. Event should appear in Realtime within 1–2 seconds
4. Click event to inspect full payload

### Test Events

```javascript
// Manually dispatch test event (console)
window.dataLayer.push({
  event: 'test_event',
  session_id: 'test_123',
  ts: new Date().toISOString(),
  page: 'index.html',
  path: '/',
  source: 'howiezz-web'
});
```

### Validation Checklist

- [ ] Session ID persists across pages in same session
- [ ] Event timestamp is valid ISO 8601
- [ ] No PII fields present in any event
- [ ] Custom events fire in GA4 Real-Time within 2 seconds
- [ ] Custom dimensions appear in GA4 reports
- [ ] Conversion events marked correctly

---

## Implementation Checklist

- [x] dataLayer schema defined
- [x] Event taxonomy complete (50+ events)
- [x] PII scrubber implemented
- [x] GA4 tag template created
- [x] GTM container configuration ready
- [ ] Replace placeholders: `REPLACE_WITH_ACCOUNT_ID`, `REPLACE_WITH_CONTAINER_ID`
- [ ] Upload GTM container JSON
- [ ] Create custom events in GA4
- [ ] Create custom dimensions in GA4
- [ ] Test Real-Time events
- [ ] Deploy to production
- [ ] Monitor for PII leaks in GA4 Admin > Data Protection

---

## References

- [GA4 Event Structure](https://developers.google.com/analytics/devguides/collection/ga4/events)
- [GTM Best Practices](https://support.google.com/tagmanager/answer/6103696)
- [dataLayer Schema Design](https://support.google.com/tagmanager/answer/6164391)
- [GA4 Custom Dimensions](https://support.google.com/analytics/answer/10075209)
