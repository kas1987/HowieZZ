# ZELEX Funnel A/B Testing Framework

## Overview

This document specifies the A/B testing strategy to validate and continuously improve the conversion funnel optimizations. All tests are designed to measure impact on the primary conversion metric: **consultation form submissions**.

---

## Core Testing Methodology

### Test Duration
- **Minimum:** 2 weeks (to capture weekly traffic patterns)
- **Optimal:** 4 weeks (to reach statistical significance at 95% confidence with n=500+)
- **Sample Size Target:** 500+ users per variant

### Statistical Threshold
- **Significance Level (α):** 0.05 (95% confidence)
- **Minimum Detectable Effect (MDE):** 15% lift (e.g., 3.7% → 4.25% conversion)
- **Power (1-β):** 0.80

### Analysis Schedule
- **Daily:** Monitor for statistical significance, major bugs, or user issues
- **Weekly:** Review learnings, capture qualitative feedback
- **Bi-weekly:** Make rollout/pivot decisions

---

## Test 1: Hero CTA Copy Variation

### Hypothesis
Explicit, benefit-driven CTA copy outperforms generic labels. Users respond better to urgency, personalization, or clear value propositions.

### Test Details

| Aspect | Control | Variant A | Variant B | Variant C |
|--------|---------|-----------|-----------|-----------|
| **Copy** | "Begin" | "Start Your Fit Quiz" | "Find Your Match in 90s" | "Get Personalized Recommendations" |
| **Visual** | Button | Button | Button | Button |
| **Weight** | 25% | 25% | 25% | 25% |

### Metrics Tracked
- **Primary:** Quiz initiation rate (button clicks / page visitors)
- **Secondary:** Quiz completion rate; time-to-quiz-start
- **Tertiary:** Overall funnel conversion

### Implementation
```javascript
// In index.html, quiz button:
function getCTAText() {
  const variant = getTestVariant('hero-cta-text');
  const texts = {
    control: 'Begin',
    a: 'Start Your Fit Quiz',
    b: 'Find Your Match in 90s',
    c: 'Get Personalized Recommendations'
  };
  return texts[variant] || texts.control;
}

document.getElementById('btn-begin').textContent = getCTAText();
```

### Success Criteria
- **Variant A or B significantly outperforms control** (>15% lift)
- **No variant underperforms control** (avoid negative surprises)

### Expected Winner
**Variant B** ("Find Your Match in 90s") — combines scarcity (time), personalization, and benefit.

---

## Test 2: Quiz Result → Form Flow

### Hypothesis
Consolidating CTAs and adding micro-copy about form brevity increases form clicks by 20%+.

### Test Details

| Aspect | Control | Optimized |
|--------|---------|-----------|
| **CTA Count** | 4 buttons (retake, compare, browse, consult) | 2 buttons (retake, consult) + secondary "View Matches" link |
| **Micro-copy** | None | "→ 2-minute form" sub-text |
| **Guidance Text** | None | "Based on your preferences, these bodies match your fit..." |
| **Visual Hierarchy** | All equal | Primary (solid) vs secondary (ghost) |

### Metrics Tracked
- **Primary:** Form click-through rate from quiz results (form clicks / quiz completions)
- **Secondary:** "Retake quiz" usage; abandonment time at this screen
- **Tertiary:** Overall funnel conversion; repeat quiz attempts

### Implementation
```html
<!-- Control: Original 4-button layout -->
<div class="ractions" id="ractions-control">
  <button class="btn ghost" id="retake-btn">↻ Retake the quiz</button>
  <button class="btn solid" id="compare-matches-btn">Compare these bodies</button>
  <a class="btn" href="family.html?f=...">Browse ${family}</a>
  <a class="btn concierge" href="contact.html?...">Request a private consultation</a>
</div>

<!-- Optimized: Streamlined layout -->
<div class="ractions ractions--optimized" id="ractions-optimized" style="display: none;">
  <p style="text-align: center; margin-bottom: 32px; color: var(--muted);">
    Based on your preferences, these bodies match your fit...
  </p>
  <a class="btn solid btn--large" href="contact.html?..." style="display: block; max-width: 400px; margin: 0 auto 14px; padding: 16px 32px;">
    Request Your Consultation
    <div style="font-size: 12px; margin-top: 4px;">→ 2-minute form</div>
  </a>
  <div style="display: flex; gap: 12px; justify-content: center;">
    <button class="btn ghost" id="retake-btn-opt">↻ Retake Quiz</button>
    <a class="btn ghost" href="#match-grid">View Matches ↓</a>
  </div>
</div>

<script>
// Variant selection
const variant = getTestVariant('quiz-result-flow');
if (variant === 'optimized') {
  document.getElementById('ractions-control').style.display = 'none';
  document.getElementById('ractions-optimized').style.display = 'block';
  ZX.track('ab_test_assigned', { test: 'quiz_result_flow', variant: 'optimized' });
} else {
  ZX.track('ab_test_assigned', { test: 'quiz_result_flow', variant: 'control' });
}
</script>
```

### Success Criteria
- **Optimized variant increases form CTR by >15%**
- **"Retake" button usage doesn't spike** (users aren't confused)
- **No increase in quiz result page abandonment**

### Expected Winner
**Optimized variant** — removes decision paralysis and makes next step explicit.

---

## Test 3: Contact Form Field Order

### Hypothesis
Collecting intent early (character of interest, family) before handling questions reduces friction and improves form submission rate. Alternatively, asking for PII first establishes commitment.

### Test Details

| Aspect | Control | Variant A |
|--------|---------|-----------|
| **Order (Section 1)** | Name → Email → Phone → Country | Email → Name → Country |
| **Order (Section 2)** | Character of interest → Family | Character of interest → Family |
| **Order (Section 3)** | Buyer-fit fields → Message | Buyer-fit fields → Message |
| **Rationale** | Current order (PII first) | Intent first (establishes commitment) |

### Metrics Tracked
- **Primary:** Form submission rate (starts → completions)
- **Secondary:** Field abandonment position; time-to-submit
- **Tertiary:** Message quality; consultation team feedback

### Implementation
```javascript
// Variant selection logic
const formVariant = getTestVariant('form-field-order');

// Dynamically reorder form fields based on variant
if (formVariant === 'intent-first') {
  // Move email to 1st position
  // Move character/family earlier
  reorderFormFields(['email','name','country','character','family',...rest]);
}

ZX.track('ab_test_assigned', { test: 'form_field_order', variant: formVariant });
```

### Success Criteria
- **Variant A increases form submission rate by >10%**
- **No significant change in message quality**
- **No increase in abandoned form errors**

### Expected Winner
**Variant A (Intent First)** — users commit to selection first, reducing cognitive load when entering PII.

---

## Test 4: Form Progress Bar Style

### Hypothesis
Showing progress (visual bar + % complete) reduces perceived form length and increases completion.

### Test Details

| Aspect | Control | Variant A | Variant B |
|--------|---------|-----------|-----------|
| **Progress Bar** | None | Horizontal % bar above form | Vertical step counter (1/3, 2/3, 3/3) |
| **Estimated Time** | None | "Estimated time: 2 minutes" | "Estimated time: 2 minutes" |
| **Reassurance** | None | "✓ Discreet · ✓ No pressure" | "✓ Discreet · ✓ No pressure" |

### Metrics Tracked
- **Primary:** Form submission rate; form abandonment rate
- **Secondary:** Average form completion time; page scroll distance
- **Tertiary:** Time-in-form by field

### Implementation
```html
<!-- Control: No progress indicator -->
<!-- Variant A: Horizontal progress bar -->
<div class="form__progress-bar">
  <div style="height: 3px; background: var(--s3); border-radius: 3px; overflow: hidden;">
    <div class="progress-fill" style="width: 0%; height: 100%; background: var(--gold); transition: width 0.3s;"></div>
  </div>
  <p style="text-align: center; font-size: 12px; color: var(--muted); margin-top: 8px;">
    <span id="progress-pct">0%</span> complete
  </p>
</div>

<!-- Variant B: Step counter -->
<div class="form__step-counter">
  <div style="text-align: center; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; color: var(--gold); margin-bottom: 12px;">
    Step <span id="current-step">1</span> of 3
  </div>
</div>
```

### Success Criteria
- **Variant with progress bar increases submission rate by >8%**
- **Form abandonment rate decreases by >5%**
- **Reassurance messaging is remembered** (survey: "Did you feel pressured?" → negative)

### Expected Winner
**Variant A (Horizontal %)** — provides clear, quantifiable progress without overwhelming with step labels.

---

## Test 5: Contact Form Modal (Exit Intent)

### Hypothesis
A simplified, exit-intent modal offering a "quick intake" path captures users who would otherwise abandon the full form.

### Test Details

| Aspect | Control | Exit-Intent Modal |
|--------|---------|-------------------|
| **Trigger** | None | User's mouse leaves form; >30s form inactivity |
| **Modal Content** | N/A | 3-field quick form (email, quick interest, brief message) |
| **Offer** | N/A | "Quick intake. We'll follow up personally." |
| **Dismissal** | N/A | 1x per session; can re-trigger after 2 minutes |

### Metrics Tracked
- **Primary:** Total form submissions (full form + modal submissions)
- **Secondary:** Modal appearance rate; conversion rate of modal vs. full form
- **Tertiary:** Lead quality (do quick-intake leads convert to consultations?)

### Implementation
```javascript
// Exit-intent detection
const formElement = document.getElementById('inquiry-form');
const modalShownThisSession = {};

function handleExitIntent(e) {
  if (modalShownThisSession.form || !isFormVisible()) return;
  
  // Detect mouse leaving viewport
  if (e.clientY <= 0 && !formElement.contains(e.relatedTarget)) {
    showQuickIntakeModal();
    modalShownThisSession.form = true;
    ZX.track('exit_intent_triggered', { context: 'contact_form' });
  }
}

document.addEventListener('mouseleave', handleExitIntent);

// Quick intake modal
function showQuickIntakeModal() {
  const modal = document.createElement('div');
  modal.className = 'quick-intake-modal';
  modal.innerHTML = `
    <div class="modal-overlay" onclick="this.parentElement.remove()"></div>
    <div class="modal-content">
      <button class="modal-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
      <h3>Before you go...</h3>
      <p>Leave your email and a quick message. We'll follow up personally within 24 hours.</p>
      <form id="quick-intake-form">
        <input type="email" placeholder="your@email.com" required>
        <textarea placeholder="Quick note..." required></textarea>
        <button type="submit" class="btn solid">Send Quick Intake</button>
      </form>
    </div>
  `;
  document.body.appendChild(modal);
}
```

### Success Criteria
- **Total submissions increase by >12%** (full form + modal combined)
- **Modal conversion rate >20%** (of modal impressions)
- **Lead quality is comparable or better** (follow-up response rate, consultation booking)
- **No modal annoyance complaints** (heuristic: monitor support feedback)

### Expected Winner
**Exit-Intent Modal** — captures abandonment and provides a lower-friction path for uncertain visitors.

---

## Test 6: Quiz Intro Copy Variation

### Hypothesis
Different framing of the quiz (speed, personalization, discovery) influences entry rates.

### Test Details

| Aspect | Control | Variant A | Variant B | Variant C |
|--------|---------|-----------|-----------|-----------|
| **Tagline** | "Five questions. Six body families. One introduction." | "Get a personalized body recommendation in 90 seconds." | "Discover the body that's made for you." | "5 quick questions. 3 perfect matches." |
| **Eyebrow** | "Find Your Character" | "Personalized Fit Quiz" | "The Body Discovery Quiz" | "Your Perfect Match" |

### Metrics Tracked
- **Primary:** Quiz completion rate; quiz abandonment at Step 1
- **Secondary:** Time-in-quiz; match satisfaction (post-quiz survey)
- **Tertiary:** Quiz-to-form conversion

### Implementation
```javascript
const quizIntroVariant = getTestVariant('quiz-intro-copy');
const copyMap = {
  control: {
    eyebrow: 'Find Your Character',
    tagline: 'Five questions. Six body families. One introduction.'
  },
  a: {
    eyebrow: 'Personalized Fit Quiz',
    tagline: 'Get a personalized body recommendation in 90 seconds.'
  },
  b: {
    eyebrow: 'The Body Discovery Quiz',
    tagline: 'Discover the body that\'s made for you.'
  },
  c: {
    eyebrow: 'Your Perfect Match',
    tagline: '5 quick questions. 3 perfect matches.'
  }
};

const copy = copyMap[quizIntroVariant] || copyMap.control;
document.querySelector('.intro .eyebrow').textContent = copy.eyebrow;
document.querySelector('.intro h1').textContent = copy.tagline;
```

### Success Criteria
- **Variant A increases completion rate by >8%**
- **Quiz entry rate increases by >10%** (if changed on landing page)

### Expected Winner
**Variant A** ("90 seconds" + "personalized") — combines speed and personalization.

---

## Test Registry & Rollout Schedule

### Timeline

| Week | Test | Status | Expected Outcome |
|------|------|--------|------------------|
| 1-2 | Hero CTA Copy (Test 1) | Running | 15-25% lift on quiz initiation |
| 2-3 | Quiz Result Flow (Test 2) | Running | 20% lift on form CTR |
| 3-4 | Form Field Order (Test 3) | Running | 10-12% lift on submission rate |
| 4-5 | Form Progress Bar (Test 4) | Queued | 8-10% lift on completion |
| 5-6 | Exit-Intent Modal (Test 5) | Queued | 12-15% increase in submissions |
| 6-7 | Quiz Copy (Test 6) | Queued | 8-10% lift on entry or completion |

### Rollout Decision Tree

```
┌─ Test Results Significant? ─────┐
│                                 │
├─ YES ─────────────────────────┐ └─ NO (inconclusive)
│                               │  └─ Extend test 2 weeks
├─ Variant wins by >15%?        │
│  YES → Roll out variant       │
│  NO  → Run different variant  │
│                               │
└─ After rollout: Run winner    │
   vs. next variant in pipeline │
```

---

## Tracking Implementation

### Required Event Extensions (assets/site.js)

```javascript
// A/B test assignment tracking
function getTestVariant(testName) {
  const stored = sessionStorage.getItem(`ab_${testName}`);
  if (stored) return stored;
  
  const variants = ['control', 'a', 'b', 'c'].slice(0, getVariantCount(testName));
  const variant = variants[Math.floor(Math.random() * variants.length)];
  
  sessionStorage.setItem(`ab_${testName}`, variant);
  ZX.track('ab_test_assigned', {
    test_name: testName,
    variant: variant
  });
  
  return variant;
}

// Track each funnel interaction with variant context
function trackFunnelEvent(eventName, payload) {
  const enrichedPayload = Object.assign({}, payload, {
    ab_tests_active: getActiveTests().join(',')
  });
  ZX.track(eventName, enrichedPayload);
}

function getActiveTests() {
  return [
    'hero-cta-text',
    'quiz-result-flow',
    'form-field-order',
    'form-progress-bar',
    'exit-intent-modal',
    'quiz-intro-copy'
  ].map(test => `${test}:${sessionStorage.getItem(`ab_${test}`) || 'control'}`);
}
```

### Dashboard Metrics to Track

```
Dashboard Columns:
├─ Event Name
├─ Total Events
├─ By Variant (Control, A, B, C, ...)
├─ Conversion Rate (% of prior step)
├─ Lift vs. Control (%)
├─ Statistical Significance (p-value)
├─ Confidence Interval (95%)
└─ Recommendation (Continue, Extend, Roll out, Pivot)

Key Metrics:
├─ Quiz Initiation Rate
├─ Quiz Completion Rate
├─ Quiz → Form Click Rate
├─ Form Submission Rate
├─ Overall Funnel Conversion
├─ Average Time-to-Action
├─ Bounce Rate (by page + variant)
└─ Message Quality (qualitative; concierge feedback)
```

---

## Statistical Significance Calculator

Use this formula to determine if your test has reached significance:

```
z = (p1 - p2) / sqrt(p * (1 - p) * (1/n1 + 1/n2))

Where:
p1 = Conversion rate, Variant A
p2 = Conversion rate, Control
p  = Pooled conversion rate = (events1 + events2) / (n1 + n2)
n1, n2 = Sample sizes

If |z| > 1.96 → 95% confidence (statistically significant)
If |z| > 1.645 → 90% confidence (likely significant, run 1 more week)
```

**Example:**
```
Control: 50 conversions / 1,000 users = 5%
Variant A: 70 conversions / 1,000 users = 7%
p = (50 + 70) / 2,000 = 0.06
z = (0.07 - 0.05) / sqrt(0.06 * 0.94 * 0.002) = 2.58
Result: SIGNIFICANT at 99.5% confidence
```

---

## Success Criteria (Overall)

If tests 1-3 (Quick Wins) show:
- **Test 1 (Hero CTA):** >15% lift ✓
- **Test 2 (Quiz Flow):** >20% lift ✓
- **Test 3 (Form Fields):** >10% lift ✓

**Expected Combined Lift: +45-48%** (compounding all three)

If combined result reaches 40-50%, **pause new tests and optimize based on learnings.**

---

## Monthly Review Cadence

Every 4 weeks:
1. **Review all active tests** — what won, what failed?
2. **Consolidate winners** — roll out best-performing variants
3. **Identify new hypotheses** — run next round of 2-3 tests
4. **Update funnel baseline** — recalculate target metrics based on new control
5. **Share results** with stakeholders — learnings, impact, next steps

---

**Target:** +50% funnel conversion by end of 8 weeks (Tests 1-6 completion).

