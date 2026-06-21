# A/B Testing Setup Guide — ZELEX Intake Form Optimization

**Objective:** Test 2–3 form variants to achieve +30% conversion lift  
**Primary Metric:** Submission rate (inquiries / visitors)  
**Secondary Metrics:** Time-to-submit, field completion rate, error recovery  
**Test Duration:** 4–6 weeks (minimum 2,000 visitors per variant)  
**Confidence Level:** 95% (p < 0.05)

---

## PHASE 1: TEST SETUP (Week 1–2)

### 1.1 Variant Definitions

#### Variant A: Control (Current Form)
- **File:** `contact.html` (existing)
- **URL:** `https://zelexdoll.com/contact.html?variant=a`
- **Description:** All 17 sections visible at once, audience toggle at top
- **Expected Conversion:** 4.2% (baseline)

#### Variant B: Progressive Disclosure + Quiz Bridge
- **File:** `contact-variant-b.html`
- **URL:** `https://zelexdoll.com/contact.html?variant=b`
- **Description:**
  - Phase 0: Minimal entry (name, email, message)
  - Phase 1: Character context (if URL prefill present)
  - Phase 2: Collapsible buyer-fit fields
  - Quiz bridge: Auto-loads quiz state from sessionStorage
- **Expected Conversion:** 6.1% (+45% lift)
- **Key Metrics to Track:**
  - Phase 2 toggle click rate (measure expand interest)
  - Quiz prefill banner impression & clearance rate
  - Message field bounce rate

#### Variant D: Minimal Entry + Exit-Intent
- **File:** `contact-variant-d.html`
- **URL:** `https://zelexdoll.com/contact.html?variant=d`
- **Description:**
  - Ultra-minimal form: Email + Message only
  - Exit-intent modal at 80% scroll depth or mouse-leave
  - Modal captures timeline field
  - Psychology: "Brief note is enough" framing
- **Expected Conversion:** 6.4% (+52% lift)
- **Key Metrics to Track:**
  - Exit-intent modal impression rate
  - Exit-intent modal submission rate (timeline capture)
  - Form submission rate (with/without exit-intent capture)

---

### 1.2 Variant Deployment Checklist

#### Before Going Live
- [ ] Variant B: WCAG AA compliance verified (aXe, Lighthouse ≥95)
- [ ] Variant D: WCAG AA compliance verified
- [ ] All three variants tested on:
  - [ ] Chrome (desktop, mobile)
  - [ ] Safari (desktop, iOS)
  - [ ] Firefox (desktop)
  - [ ] Edge (desktop)
- [ ] Prefill URL params (?id=, ?family=, ?b=, ?compare=) work on all variants
- [ ] Form submission works with mailto fallback and endpoint (if configured)
- [ ] Analytics events fire (inquiry_submit_attempt, inquiry_submit_success, inquiry_validation_failed)
- [ ] Session storage for quiz bridge persists correctly
- [ ] Exit-intent modal (Variant D) closes properly on Escape, modal submit, and skip
- [ ] No console errors (dev tools should be clean)
- [ ] Performance: Page load <3s on 4G throttled connection

#### Deployment Steps
1. Copy `contact-variant-b.html` to `contact-b.html` (or host at variant path)
2. Copy `contact-variant-d.html` to `contact-d.html`
3. Set up redirect or routing:
   ```
   contact.html?variant=a → contact.html (control)
   contact.html?variant=b → contact-b.html (progressive disclosure)
   contact.html?variant=d → contact-d.html (minimal entry + exit-intent)
   ```
4. Verify routing works end-to-end
5. Set up analytics tracking (see Section 1.4)

---

### 1.3 Traffic Allocation

**Recommended Split (equal distribution):**
- Variant A (Control): 33% of traffic
- Variant B (Progressive Disclosure): 33% of traffic
- Variant D (Minimal Entry + Exit-Intent): 34% of traffic

**Implementation (via JavaScript or server-side routing):**

```javascript
// Client-side variant assignment (if no server-side setup available)
function assignVariant() {
  const stored = sessionStorage.getItem('zx_form_variant');
  if (stored) return stored;
  
  const rand = Math.random();
  let variant = 'a';
  if (rand < 0.33) variant = 'a';
  else if (rand < 0.66) variant = 'b';
  else variant = 'd';
  
  sessionStorage.setItem('zx_form_variant', variant);
  return variant;
}

const variant = assignVariant();
const contactUrl = variant === 'a' 
  ? '/contact.html' 
  : `/contact-${variant}.html`;

// Redirect or update links
if (variant !== 'a') {
  window.location.pathname = contactUrl;
}
```

**Alternatively (server-side via cookie or query string):**
```
// On every contact link click or navigation
const variant = Math.random() < 0.33 ? 'a' : Math.random() < 0.5 ? 'b' : 'd';
const url = `/contact.html?variant=${variant}`;
```

---

### 1.4 Analytics Instrumentation

#### Events to Track (via ZX.track)

**Form Visit**
```javascript
ZX.track('form_visit', {
  variant: 'a|b|d',
  entry_source: 'quiz|browse|footer|direct|character_page',
  quiz_prefill: true|false,
  timestamp: new Date().toISOString()
});
```

**Phase Expansion (Variant B only)**
```javascript
ZX.track('phase_expand', {
  variant: 'b',
  phase: 2,
  user_scroll_depth: 35,  // % of page scrolled
  time_to_expand_ms: 450
});
```

**Field Blur / Validation**
```javascript
ZX.track('field_blur', {
  variant: 'a|b|d',
  field_name: 'name|email|message|family',
  validation_error: true|false,
  error_type: 'required|email_format|length'
});
```

**Validation Failed (Submit Attempt)**
```javascript
ZX.track('inquiry_validation_failed', {
  variant: 'a|b|d',
  fields_with_errors: ['email','message'],
  audience: 'new|collector',
  error_count: 2
});
```

**Submit Attempt**
```javascript
ZX.track('inquiry_submit_attempt', {
  variant: 'a|b|d',
  has_buyer_fit: true|false,
  has_character_context: true|false,
  has_customization: true|false,
  intent: 'new_buyer|collector',
  timeline: 'now|soon|plan|explore',
  use_context: 'private|photo|display|companion|undecided'
});
```

**Submit Success**
```javascript
ZX.track('inquiry_submit_success', {
  variant: 'a|b|d',
  conversion_time_sec: 145,  // Time from page load to submit
  audience: 'new|collector',
  message_length: 42,  // Character count
  exit_intent_triggered: false,  // Variant D only
  exit_intent_completed: false   // Variant D only
});
```

**Submit Error**
```javascript
ZX.track('inquiry_submit_error', {
  variant: 'a|b|d',
  error_message: 'Network error|Server error|Timeout',
  error_code: 500|timeout,
  retry_attempt: 1
});
```

**Exit-Intent Modal (Variant D only)**
```javascript
ZX.track('exit_intent_shown', {
  variant: 'd',
  trigger: 'scroll_depth|mouse_leave',
  scroll_depth_percent: 85
});

ZX.track('exit_intent_completed', {
  variant: 'd',
  field_captured: 'timeline',
  field_value: 'now|soon|plan|explore',
  time_to_capture_sec: 12
});

ZX.track('exit_intent_skipped', {
  variant: 'd',
  reason: 'skip_button|escape_key|timeout'
});
```

---

### 1.5 Statistical Analysis Setup

#### Sample Size Calculation
Assuming:
- Baseline conversion: 4.2%
- Target lift: +30% (→ 5.46%)
- Significance level (α): 0.05
- Power (1-β): 0.80
- Test type: Two-tailed

**Result:** ~2,100 visitors per variant needed (6,300 total)  
**Duration:** ~4–6 weeks at typical traffic levels (100–150 daily visitors)

#### Success Criteria
1. **Primary:** Variant achieves statistically significant (p < 0.05) conversion lift over control
2. **Secondary:** No regression in secondary metrics (time-to-submit, error rate)
3. **Tertiary:** Positive user feedback (surveys, support emails)

#### Tools for Analysis
- **Google Analytics:** Built-in A/B testing (Goals → Conversion Rate)
- **Optimizely:** Commercial A/B testing platform
- **VWO (Visual Website Optimizer):** No-code A/B testing
- **Python/R:** Manual statistical analysis using scipy.stats or equivalent

**Simple conversion rate comparison (spreadsheet):**
```
Variant | Visitors | Conversions | Rate | 95% CI
--------|----------|-------------|------|----------
A       | 2,100    | 88          | 4.2% | [3.4%, 5.1%]
B       | 2,100    | 129         | 6.1% | [5.2%, 7.1%] ← Significant uplift
D       | 2,100    | 134         | 6.4% | [5.5%, 7.3%] ← Highest winner
```

---

## PHASE 2: MONITORING & OPTIMIZATION (Week 2–6)

### 2.1 Daily Monitoring Checklist
- [ ] All three forms loading without errors (check browser console)
- [ ] Analytics events firing consistently
- [ ] Variant assignment is random & balanced (check Analytics → Audience)
- [ ] Form submissions being captured (check backend inbox or form endpoint)
- [ ] No unusual bot traffic or spam submissions
- [ ] Exit-intent modal (Variant D) firing at expected scroll depth
- [ ] Quiz bridge (Variant B) prefilling correctly (check sessionStorage in DevTools)

### 2.2 Weekly Analysis

**Metrics to Review:**
1. **Conversion Rate** (primary metric)
   - Calculate: Submissions / Visitors (per variant)
   - Target: Variant B/D ≥ +30% vs. Variant A

2. **Submission Funnel**
   - Form visited → Field 1 interaction → Submit attempt → Submit success
   - Identify where each variant loses users
   - Drop-off rate should be <50% for Phase 0 → Phase 1 (Variant B)

3. **Time-to-Submit**
   - Average time from page load to form submission
   - Variant B expected: Slightly higher (due to progressive disclosure reading)
   - Variant D expected: Lower (minimal form, faster completion)

4. **Error Recovery Rate**
   - Users who fail validation but retry and succeed
   - Should be ≥60% for all variants (healthy recovery)

5. **Device & Browser Performance**
   - Conversion rate by device (mobile vs. desktop)
   - Variant D should perform particularly well on mobile (minimal input)

**Weekly Report Template:**
```
Week 3 (Jun 25–Jul 1)
Variant A (Control)
  - Visitors: 485
  - Conversions: 21
  - Conversion Rate: 4.33%
  - Avg Time-to-Submit: 342 sec
  - Error Recovery: 58%

Variant B (Progressive Disclosure)
  - Visitors: 492
  - Conversions: 32
  - Conversion Rate: 6.50% (+50% vs A) ✅
  - Phase 2 Expansion Rate: 38%
  - Avg Time-to-Submit: 378 sec
  - Error Recovery: 64%

Variant D (Minimal Entry + Exit-Intent)
  - Visitors: 488
  - Conversions: 34
  - Conversion Rate: 6.97% (+61% vs A) ✅✅
  - Exit-Intent Modal Trigger Rate: 62%
  - Exit-Intent Completion Rate: 23% (of triggered)
  - Avg Time-to-Submit: 198 sec
  - Error Recovery: 71%

Winner (this week): Variant D
```

---

## PHASE 3: WINNER SELECTION & ROLLOUT (Week 6+)

### 3.1 Determining the Winner

**Criteria (in priority order):**

1. **Statistical Significance**
   - Primary metric (conversion rate) must reach p < 0.05
   - Use chi-square test or online calculator (e.g., AB Tasty)
   
2. **Conversion Lift**
   - Must achieve ≥30% uplift target
   - Confidence interval should not cross control baseline

3. **Secondary Metrics Health**
   - No regression in time-to-submit or error rate
   - Mobile performance must be equal or better
   - Exit rate should not increase

4. **Qualitative Feedback**
   - Support email feedback (user confusion, praise, issues)
   - UserTesting session observations
   - Accessibility audit results (must be WCAG AA compliant)

### 3.2 Rollout Plan for Winner

**If Variant B wins (Progressive Disclosure):**
```
Day 1: Update contact.html from contact-b.html
Day 2: Remove old contact.html backup (after verification)
Day 3: Update all internal links to point to new form
Day 4–5: Monitor for issues, rollback if critical bug
Day 7: Archive contact-variant-*.html for future reference
```

**If Variant D wins (Minimal Entry + Exit-Intent):**
```
Day 1: Update contact.html from contact-d.html
Day 2: Verify exit-intent modal triggers correctly
Day 3–5: Monitor conversion rate stability
Day 7: Archive old forms
```

**If no clear winner (A/B results inconclusive):**
- Extend test by 2–3 weeks for statistical confidence
- Run post-test survey (500+ respondents) on preferences
- Consider multivariate test with hybrid features

---

## PHASE 4: POST-WINNER OPTIMIZATION (Week 8+)

### 4.1 Continuous Improvement

**After winner is live, test incremental improvements:**

1. **Refinement Test 1:** Exit-intent messaging (Variant D)
   - Test different modal headlines
   - Test incentive (timeline capture vs. "why are you leaving?")

2. **Refinement Test 2:** Customization prefill (Variant B)
   - Test auto-checking skin tone swatch based on quiz
   - Measure impact on message field specificity

3. **Refinement Test 3:** Follow-up email sequence
   - Test 1-day vs. same-day response times
   - Measure conversion from inquiry to order

### 4.2 Analytics Dashboard Setup

**Create permanent dashboard in Google Analytics / Looker / Tableau:**
- Daily conversion rate (with trendline)
- Submission funnel visualization
- Time-to-submit distribution (histogram)
- Exit-intent modal performance (Variant D)
- Device & browser breakdown
- Geographic distribution

**Review cadence:** Weekly (first month), bi-weekly (ongoing)

---

## APPENDIX: URL SCHEMES & IMPLEMENTATION

### URL Routing Examples

#### Option 1: Query String (Simplest)
```
/contact.html?variant=a  → Control form
/contact.html?variant=b  → Progressive Disclosure
/contact.html?variant=d  → Minimal Entry + Exit-Intent
```

**Implementation (in navigation links):**
```javascript
// In site.js or navigation
function getContactLink(source = 'footer') {
  const variant = assignVariant();  // See 1.3
  return `/contact.html?variant=${variant}&src=${source}`;
}

// All "Contact" links in nav/footer
document.querySelectorAll('a[href*="contact.html"]').forEach(link => {
  link.href = getContactLink('nav');
});
```

#### Option 2: Path-Based Routing (If server supports)
```
/contact/      → Control (variant=a)
/contact-b/    → Progressive Disclosure (variant=b)
/contact-d/    → Minimal Entry + Exit-Intent (variant=d)
```

**Implementation (Caddy or nginx):**
```caddy
# Caddyfile
route /contact {
  redir @variant-b /contact-b
  redir @variant-d /contact-d
  file_server
}

@variant-b {
  query variant=b
}

@variant-d {
  query variant=d
}
```

#### Option 3: Cookie-Based (Most Persistent)
```javascript
// On first visit, assign & store variant
const variant = assignVariant();
document.cookie = `zx_form_variant=${variant}; max-age=2592000; path=/`;

// All subsequent visits use same variant
const storedVariant = getCookie('zx_form_variant') || assignVariant();
```

---

## APPENDIX: ANALYTICS SETUP (Google Analytics)

### Goal Definition
```
Goal Name: Inquiry Submission
Goal Type: Event
Event Category: inquiry
Event Action: submit_success
Conversion Value: $5000 (estimated order value)
```

### Conversion Rate Calculation
```
Conversion Rate = Total Conversions / Total Sessions

Example:
Variant B: 129 conversions / 2,100 sessions = 6.14%
```

### Segment Creation (for filtering)
```
Analytics → Audience → Segments → Create

Segment: Variant B Traffic
Conditions:
  - Page: /contact.html
  - Query Parameter: variant = b
```

### Report Template
```
Reporting → Conversion → Goals → Overview
Select: Primary Dimension = Source/Medium
Add secondary dimension: Custom Dimension (variant)
Date range: Current week vs. Previous week
```

---

## APPENDIX: STATISTICAL SIGNIFICANCE CALCULATOR

**Online tool:** https://www.optimizely.com/ab-testing-statistics-calculator/

**Or manual calculation (Python):**
```python
from scipy.stats import chi2_contingency
import numpy as np

# Variant A: 88 conversions out of 2,100 visitors
# Variant B: 129 conversions out of 2,100 visitors

contingency_table = np.array([
    [88, 2100 - 88],      # Variant A: converted, not converted
    [129, 2100 - 129]     # Variant B: converted, not converted
])

chi2, p_value, dof, expected = chi2_contingency(contingency_table)
print(f"p-value: {p_value:.4f}")
print(f"Significant at α=0.05: {p_value < 0.05}")
```

---

**End of A/B Testing Setup Guide**
