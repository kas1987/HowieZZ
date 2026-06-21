# ZELEX Funnel Analytics — Event Tracking Schema

## Overview

This document defines the complete event tracking schema for the funnel optimization initiative. All events are emitted via `ZX.track()` and flow into the analytics dataLayer.

---

## Core Event Structure

Every event follows this base structure:

```javascript
{
  event: "<event_name>",              // Canonical event name (aliased)
  event_original: "<original_name>",  // Original event name (before aliasing)
  source: "howiezz-web",              // Always this value
  schema_version: "2026-06-06",       // Event schema version
  session_id: "zx_<timestamp>_<random>",
  ts: "2026-06-21T14:30:00Z",        // ISO 8601 timestamp
  page: "index.html",                 // Current page
  path: "/index.html",                // URL path
  
  // User-defined properties (vary by event)
  context: "funnel_engagement" | "funnel_drop" | "funnel_intervention" | "interaction",
  source_page: "index" | "quiz" | "contact" | ...,
  ...additional_props
}
```

---

## Funnel Stage Events

### STAGE 1: ENTRY

#### Event: `funnel_entry`
**Triggers:** When user arrives at discovery page (hero, browse, family, etc.)

```javascript
ZX.track('funnel_entry', {
  entry_source: "hero" | "browse" | "family" | "series" | "external",
  context: 'funnel_entry'
});
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| entry_source | string | Yes | Where user entered funnel (main entry points) |
| context | string | Yes | Always `funnel_entry` |

**Example:**
```javascript
// User clicks "Start Quiz" on homepage
ZX.track('funnel_entry', {
  entry_source: 'hero',
  context: 'funnel_entry'
});
```

---

#### Event: `page_view`
**Triggers:** When page loads (auto-tracked on DOMContentLoaded)

```javascript
ZX.track('page_view', {
  context: 'navigation',
  source_page: 'index' | 'quiz' | 'contact' | 'browse' | 'family' | 'character' | 'body' | 'compare' | 'series'
});
```

**Already Implemented:** Yes (auto-tracked in site.js, line ~177-185)

---

### STAGE 2: ENGAGEMENT

#### Event: `quiz_started`
**Triggers:** User clicks "Begin" button on quiz intro screen

```javascript
ZX.track('quiz_started', {
  entry_source: 'hero' | 'contact_page' | 'browse' | 'family',
  context: 'funnel_engagement'
});
```

**Integration Point:** quiz.html, line ~342 (`startQuiz()` function)

```javascript
function startQuiz() {
  answers = [];
  step = 0;
  hide('intro');
  hide('rscreen');
  showSection('qscreen');
  
  // NEW: Track quiz start
  ZX.track('quiz_started', {
    entry_source: 'hero',
    context: 'funnel_engagement'
  });
  
  renderQ();
}
```

---

#### Event: `quiz_question_answered`
**Triggers:** User selects an answer on any question

```javascript
ZX.track('quiz_question_answered', {
  question_number: 1-5,               // 1-indexed
  question_text: "<exact_question>",
  answer_text: "<exact_answer>",
  time_to_answer_sec: <number>,
  context: 'interaction'
});
```

**Integration Point:** quiz.html, line ~370 (in option click handler)

```javascript
document.querySelectorAll('#opts .opt').forEach(btn => {
  btn.addEventListener('click', () => {
    const o = Q.opts[+btn.dataset.i];
    if (!o) return;
    
    // NEW: Track answer
    const answerTime = Date.now() - window.__quizQuestionStart;
    ZX.track('quiz_question_answered', {
      question_number: step + 1,
      question_text: Q.q,
      answer_text: o.b,
      time_to_answer_sec: Math.round(answerTime / 1000),
      context: 'interaction'
    });
    window.__quizQuestionStart = null;
    
    answers.push(o);
    if (step < QUESTIONS.length - 1) {
      step++;
      renderQ();
    } else {
      finish();
    }
  });
});
```

---

#### Event: `quiz_completed`
**Triggers:** User completes all 5 questions and result screen displays

```javascript
ZX.track('quiz_completed', {
  winner_family: "<family_name>",     // e.g., "The Siren"
  source_family: "<family_name>",     // Family with available bodies
  in_development: 0 | 1,
  quiz_time_sec: <number>,
  lean_whr: <number>,                 // -1.0 to +1.0
  lean_bwr: <number>,                 // -1.0 to +1.0
  top3_families: "Family1|Family2|Family3",
  context: 'funnel_engagement'
});
```

**Integration Point:** quiz.html, line ~512 (end of `finish()` function)

```javascript
// NEW: Track quiz completion
const quizTimeSeconds = window.__quizStartTime 
  ? Math.round((Date.now() - window.__quizStartTime) / 1000) 
  : null;

ZX.track('quiz_completed', {
  winner_family: expressed,
  source_family: sourceFam,
  in_development: isInDev(expressed) ? 1 : 0,
  quiz_time_sec: quizTimeSeconds,
  lean_whr: avgWhr,
  lean_bwr: avgBwr,
  top3_families: ranked.slice(0, 3).join('|'),
  context: 'funnel_engagement'
});
```

---

#### Event: `quiz_abandoned`
**Triggers:** User leaves quiz before completing all 5 questions

```javascript
ZX.track('quiz_abandoned', {
  step: 1-5,                          // Which question they abandoned at
  time_in_quiz_sec: <number>,
  last_answer: "<text>",
  context: 'funnel_drop'
});
```

**Integration Point:** Add to `beforeunload` handler or visibility change listener

```javascript
// Detect quiz abandonment
window.addEventListener('beforeunload', () => {
  if (window.__quizInProgress && step > 0 && step < QUESTIONS.length) {
    ZX.track('quiz_abandoned', {
      step: step + 1,
      time_in_quiz_sec: window.__quizStartTime 
        ? Math.round((Date.now() - window.__quizStartTime) / 1000) 
        : null,
      last_answer: answers[answers.length - 1]?.b || '',
      context: 'funnel_drop'
    });
  }
});
```

---

### STAGE 3: CONVERSION

#### Event: `quiz_result_view`
**Triggers:** Quiz result screen renders successfully

```javascript
ZX.track('quiz_result_view', {
  winner_family: "<family_name>",
  match_count: 1-4,                   // Number of recommended matches
  matches: "CharID1|CharID2|CharID3|CharID4",
  compare_available: 0 | 1,
  context: 'content'
});
```

**Integration Point:** quiz.html, line ~630 (in `showResult()` function, after `showSection('rscreen')`)

```javascript
showSection('rscreen');
ZX.revealInit();

// NEW: Track result view
ZX.track('quiz_result_view', {
  winner_family: expressed,
  match_count: matches.length,
  matches: matches.map(c => c.character_id).join('|'),
  compare_available: 1,
  context: 'content'
});
```

---

#### Event: `quiz_result_cta_click`
**Triggers:** User clicks any CTA on quiz result page

```javascript
ZX.track('quiz_result_cta_click', {
  cta_type: 'consult' | 'retake' | 'compare' | 'browse_family' | 'view_matches',
  cta_label: "<button_text>",
  destination: 'contact' | 'quiz_intro' | 'compare' | 'family' | '#anchor',
  context: 'interaction'
});
```

**Integration Point:** quiz.html, line ~623 (wire all result CTAs)

```javascript
const compareBtn = document.getElementById('compare-matches-btn');
if (compareBtn) {
  compareBtn.addEventListener('click', () => {
    // NEW: Track CTA click
    ZX.track('quiz_result_cta_click', {
      cta_type: 'compare',
      cta_label: 'Compare these bodies',
      destination: 'compare',
      context: 'interaction'
    });
    
    ZX.setCompareBodies(compareBodies);
    ZX.track('compare_set_changed', { ... });
    location.href = 'compare.html';
  });
}

document.getElementById('retake-btn').addEventListener('click', () => {
  // NEW: Track retake
  ZX.track('quiz_result_cta_click', {
    cta_type: 'retake',
    cta_label: '↻ Retake the quiz',
    destination: 'quiz_intro',
    context: 'interaction'
  });
  
  hide('rscreen');
  showSection('intro');
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
```

---

#### Event: `form_started`
**Triggers:** User enters contact form (focused on form or scrolled into view)

```javascript
ZX.track('form_started', {
  audience_mode: 'new' | 'collector',  // From mode selection
  entry_point: 'quiz_result' | 'direct' | 'navigation',
  prefilled_context: null | 'character' | 'family' | 'compare',
  context: 'funnel_engagement'
});
```

**Integration Point:** contact.html, after FIT.init() (line ~789)

```javascript
ZX.load().then(function(m) {
  prefill(m);
  
  // NEW: Track form start (on first interaction)
  let formStartTracked = false;
  const formElement = document.getElementById('inquiry-form');
  
  function trackFormStart() {
    if (formStartTracked) return;
    formStartTracked = true;
    
    const modeCard = document.querySelector('.mode-card[aria-pressed="true"]');
    const audience = modeCard ? modeCard.getAttribute('data-mode') : 'new';
    
    ZX.track('form_started', {
      audience_mode: audience,
      entry_point: ZX.qs('src') || 'direct',
      prefilled_context: ZX.qs('id') ? 'character' : (ZX.qs('family') ? 'family' : (ZX.qs('compare') ? 'compare' : null)),
      context: 'funnel_engagement'
    });
  }
  
  if (formElement) {
    formElement.addEventListener('focus', trackFormStart, { once: true, capture: true });
    formElement.addEventListener('click', trackFormStart, { once: true });
  }
  
  ...
});
```

---

#### Event: `form_field_focus`
**Triggers:** User focuses on a form field

```javascript
ZX.track('form_field_focus', {
  field_id: 'f-name' | 'f-email' | 'f-family' | 'f-message' | ...,
  field_label: "<label_text>",
  section: 'contact_info' | 'preferences' | 'message' | 'consent',
  time_to_field_focus_sec: <number>,
  context: 'interaction'
});
```

**Integration Point:** contact.html, form field listeners (optional — can skip for MVP)

```javascript
// Lightweight form field tracking
const formFields = document.querySelectorAll('#inquiry-form input, #inquiry-form textarea, #inquiry-form select');
formFields.forEach(field => {
  field.addEventListener('focus', () => {
    ZX.track('form_field_focus', {
      field_id: field.id,
      field_label: field.parentElement?.querySelector('label')?.textContent?.trim() || '',
      section: field.closest('.fit-section')?.getAttribute('data-section') || 'contact_info',
      context: 'interaction'
    });
  });
});
```

---

#### Event: `form_abandoned`
**Triggers:** User leaves form page without submitting

```javascript
ZX.track('form_abandoned', {
  fields_completed: <number>,         // Count of filled fields
  total_fields: <number>,             // Count of all form fields
  last_focused_field: 'f-name' | 'f-email' | ...,
  time_in_form_sec: <number>,
  incomplete_section: 'contact_info' | 'preferences' | 'message' | null,
  context: 'funnel_drop'
});
```

**Integration Point:** contact.html, `beforeunload` handler

```javascript
window.addEventListener('beforeunload', () => {
  const formElement = document.getElementById('inquiry-form');
  const submitBtn = document.getElementById('submit-btn');
  
  // If form was started but not submitted
  if (formStartTracked && !submitBtn.disabled) {
    const fields = formElement.querySelectorAll('input, textarea, select');
    const filledCount = Array.from(fields).filter(f => f.value?.trim()).length;
    
    ZX.track('form_abandoned', {
      fields_completed: filledCount,
      total_fields: fields.length,
      last_focused_field: document.activeElement?.id || '',
      time_in_form_sec: window.__formStartTime 
        ? Math.round((Date.now() - window.__formStartTime) / 1000)
        : null,
      context: 'funnel_drop'
    });
  }
});
```

---

#### Event: `exit_intent_triggered`
**Triggers:** Exit-intent modal appears

```javascript
ZX.track('exit_intent_triggered', {
  trigger_type: 'mouse_leave' | 'inactivity' | 'scroll_exit',
  form_section: 'contact_info' | 'preferences' | 'message',
  progress_percent: <0-100>,
  context: 'funnel_intervention'
});
```

**Integration Point:** contact.html, exit-intent handler (new)

```javascript
// Exit-intent detection (in contact form JS section)
document.addEventListener('mouseleave', (e) => {
  if (e.clientY <= 0 && formStartTracked && !submitBtn.disabled) {
    const fieldsContainer = formElement.querySelector('.fit-section');
    const currentSection = fieldsContainer?.getAttribute('data-section') || 'message';
    const fields = formElement.querySelectorAll('input[type!=hidden], textarea, select');
    const filledCount = Array.from(fields).filter(f => f.value?.trim()).length;
    const progress = Math.round((filledCount / fields.length) * 100);
    
    ZX.track('exit_intent_triggered', {
      trigger_type: 'mouse_leave',
      form_section: currentSection,
      progress_percent: progress,
      context: 'funnel_intervention'
    });
    
    showQuickIntakeModal();
  }
});
```

---

#### Event: `inquiry_submit_attempt`
**Triggers:** User clicks form submit button (validation begins)

**Already Implemented:** Yes (contact.html, line ~1234)

```javascript
ZX.track('inquiry_submit_attempt', {
  has_character_context: true | false,
  has_compare_context: true | false,
  intent: 'First purchase guidance' | 'Returning buyer consultation',
  family: '<selected_family>' | '',
  timeline: '<selected_timeline>' | '',
  use_context: '<selected_use>' | '',
  realism: 'Natural' | 'Soft' | 'Balanced' | 'Bold' | 'Dramatic' | '',
  handling: '<selected_handling>' | '',
  privacy: '<selected_privacy>' | '',
  has_customization: true | false,
  context: 'funnel_engagement'
});
```

---

#### Event: `inquiry_validation_failed`
**Triggers:** Form validation errors occur (missing required fields)

**Already Implemented:** Yes (contact.html, line ~1219)

```javascript
ZX.track('inquiry_validation_failed', {
  failed_fields: 'name,email' | 'email' | 'message' | 'consent' | ...,
  first_error: '<field_id>',
  error_count: <number>,
  context: 'funnel_drop'
});
```

**Needs Enhancement:** Track which specific fields failed validation

```javascript
// In validate() function, update to track failed field(s)
function validate() {
  const failedFields = [];
  
  var name = (document.getElementById('f-name') || {}).value || '';
  if (!name.trim()) {
    showFieldError('f-name','err-name',true);
    failedFields.push('name');
  }
  
  var email = (document.getElementById('f-email') || {}).value || '';
  if (!validateEmail(email)) {
    showFieldError('f-email','err-email',true);
    failedFields.push('email');
  }
  
  // ... other validations ...
  
  if (failedFields.length > 0) {
    ZX.track('inquiry_validation_failed', {
      failed_fields: failedFields.join(','),
      first_error: failedFields[0],
      error_count: failedFields.length,
      context: 'funnel_drop'
    });
  }
  
  return failedFields.length === 0;
}
```

---

#### Event: `inquiry_submit_success`
**Triggers:** Form submission completed successfully

**Already Implemented:** Yes (contact.html, line ~1195)

```javascript
ZX.track('inquiry_submit_success', {
  channel: 'endpoint' | 'mailto',      // Backend vs. fallback
  audience_mode: 'new' | 'collector',
  intent: '<value>',
  family: '<selected_family>' | '',
  timeline: '<selected_timeline>' | '',
  context: 'funnel_engagement',
  entry_source: 'quiz' | 'contact' | 'direct' | ...
});
```

---

#### Event: `inquiry_submit_error`
**Triggers:** Form submission fails (server error or network issue)

**Already Implemented:** Yes (contact.html, line ~1210)

```javascript
ZX.track('inquiry_submit_error', {
  error_message: '<error_text>',       // Truncated to 180 chars
  channel: 'endpoint' | 'mailto',
  context: 'funnel_drop'
});
```

---

## A/B Testing Events

### Event: `ab_test_assigned`
**Triggers:** When test variant is assigned to user (on page load)

```javascript
ZX.track('ab_test_assigned', {
  test_name: 'hero_cta_text' | 'quiz_result_flow' | 'form_field_order' | ...,
  variant: 'control' | 'a' | 'b' | 'c',
  context: 'ab_test'
});
```

**Integration Point:** Global test assignment logic (site.js or contact.html/quiz.html)

```javascript
function getTestVariant(testName) {
  const stored = sessionStorage.getItem(`ab_${testName}`);
  if (stored) return stored;
  
  const variantMap = {
    'hero_cta_text': ['control', 'a', 'b', 'c'],
    'quiz_result_flow': ['control', 'optimized'],
    'form_field_order': ['control', 'intent_first'],
    'form_progress_bar': ['control', 'horizontal_pct', 'step_counter'],
    'exit_intent_modal': ['control', 'with_modal'],
    'quiz_intro_copy': ['control', 'a', 'b', 'c']
  };
  
  const variants = variantMap[testName] || ['control'];
  const variant = variants[Math.floor(Math.random() * variants.length)];
  
  sessionStorage.setItem(`ab_${testName}`, variant);
  ZX.track('ab_test_assigned', {
    test_name: testName,
    variant: variant,
    context: 'ab_test'
  });
  
  return variant;
}
```

---

## Summary: Event Tracking Integration Checklist

### Must Implement (Core Funnel)
- [ ] `quiz_started` (quiz.html, startQuiz function)
- [ ] `quiz_completed` (quiz.html, finish function)
- [ ] `quiz_result_view` (quiz.html, showResult function)
- [ ] `quiz_result_cta_click` (quiz.html, CTA handlers)
- [ ] `form_started` (contact.html, form init)
- [ ] `form_abandoned` (contact.html, beforeunload)
- [ ] `ab_test_assigned` (All pages, variant assignment)

### Should Implement (Secondary Value)
- [ ] `quiz_question_answered` (quiz.html, option handlers)
- [ ] `quiz_abandoned` (quiz.html, beforeunload)
- [ ] `form_field_focus` (contact.html, field listeners)
- [ ] `exit_intent_triggered` (contact.html, exit handler)
- [ ] `inquiry_validation_failed` (contact.html, enhance existing)

### Already Implemented (No Changes Needed)
- ✓ `page_view` (site.js, auto-tracked)
- ✓ `inquiry_submit_attempt` (contact.html)
- ✓ `inquiry_submit_success` (contact.html)
- ✓ `inquiry_submit_error` (contact.html)

---

## Data Validation Rules

### Event Payload Validation
```javascript
function validateEventPayload(event, payload) {
  const rules = {
    quiz_started: {
      entry_source: ['hero','contact_page','browse','family'],
      context: 'funnel_engagement'
    },
    quiz_completed: {
      winner_family: /^The (Classic|Icon|Muse|Siren|Empress|Sculpt)$/,
      in_development: [0, 1],
      quiz_time_sec: 'number (30-600)',
      context: 'funnel_engagement'
    },
    form_started: {
      audience_mode: ['new','collector'],
      context: 'funnel_engagement'
    },
    inquiry_submit_success: {
      channel: ['endpoint','mailto'],
      context: 'funnel_engagement'
    }
  };
  
  // Validate against rules
  const rule = rules[event];
  if (!rule) return true; // No rule = valid
  
  return Object.entries(rule).every(([key, validator]) => {
    const value = payload[key];
    if (Array.isArray(validator)) return validator.includes(value);
    if (typeof validator === 'string') return typeof value === 'number'; // Simplified
    if (validator instanceof RegExp) return validator.test(value);
    return value === validator;
  });
}
```

---

## Analytics Debug Mode

Enable debug mode to log all events to console:

**URL Parameter:** `?zx_analytics_debug=1`

**Persists in localStorage:** Once enabled, stays on until `?zx_analytics_debug=0`

**Output:** `[ZX analytics] { event: "...", ... }`

---

## Reporting Queries

### Query 1: Funnel Conversion by Stage
```sql
SELECT
  event,
  COUNT(*) as events,
  COUNT(DISTINCT session_id) as users,
  ROUND(100.0 * COUNT(DISTINCT session_id) / LAG(COUNT(DISTINCT session_id)) OVER (ORDER BY event_order), 2) as pct_of_prior
FROM events
WHERE event IN ('funnel_entry','quiz_started','quiz_completed','form_started','inquiry_submit_success')
  AND ts >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY 1
ORDER BY event_order;
```

### Query 2: A/B Test Performance
```sql
SELECT
  test_name,
  variant,
  COUNT(*) as impressions,
  COUNT(CASE WHEN converted = 1 THEN 1 END) as conversions,
  ROUND(100.0 * COUNT(CASE WHEN converted = 1 THEN 1 END) / COUNT(*), 2) as conversion_pct
FROM events
LEFT JOIN conversions ON events.session_id = conversions.session_id AND events.ts <= conversions.ts
WHERE event = 'ab_test_assigned'
  AND ts >= DATE_SUB(NOW(), INTERVAL 14 DAY)
GROUP BY test_name, variant
ORDER BY test_name, conversion_pct DESC;
```

---

**End of Event Tracking Schema**

Use this as reference when implementing events. All event names are stable and won't change mid-campaign.

