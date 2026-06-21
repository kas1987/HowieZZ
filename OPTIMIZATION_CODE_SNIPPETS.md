# ZELEX Funnel Optimization — Code Implementation Guide

## Quick Reference: Where to Make Changes

This document provides the exact code changes needed to implement the funnel optimizations outlined in `FUNNEL_OPTIMIZATION_ANALYSIS.md`.

---

## 1. HERO PAGE IMPROVEMENTS (index.html)

### Change 1.1: Update Hero CTA with Trust Badges

**Current Code (lines ~30-50 in hero section):**
```html
<div class="cta"></div>
```

**Updated Code:**
```html
<!-- Trust row before CTA buttons -->
<div class="hero__trust-row" style="margin-top: 24px; margin-bottom: 20px; font-size: 13px; color: var(--muted); letter-spacing: 0.5px;">
  <span>✓ Trusted by collectors worldwide</span>
  <span style="margin: 0 10px;">·</span>
  <span>90-second personalized fit guide</span>
  <span style="margin: 0 10px;">·</span>
  <span>No obligation</span>
</div>

<div class="cta">
  <!-- Primary CTA: Quiz -->
  <a href="quiz.html" class="btn solid btn--primary" style="padding: 16px 48px; font-size: 15px; font-weight: 600;">
    Start Your Fit Quiz
  </a>
  
  <!-- Secondary CTAs -->
  <a href="browse.html" class="btn ghost">Explore Gallery</a>
  <a href="family.html" class="btn ghost">Browse Families</a>
</div>

<div class="hero__subtext" style="margin-top: 18px; font-size: 12px; color: var(--muted); letter-spacing: 1px;">
  Fully personalized. Completely discreet. Zero pressure.
</div>
```

---

## 2. QUIZ RESULT PAGE IMPROVEMENTS (quiz.html)

### Change 2.1: Streamline Action Buttons

**Current Code (lines ~622-627):**
```html
<div class="ractions">
  <button class="btn ghost" id="retake-btn">↻ Retake the quiz</button>
  <button class="btn solid" id="compare-matches-btn">Compare these bodies</button>
  <a class="btn" href="family.html?f=${encodeURIComponent(sourceFam)}">Browse ${ZX.esc(sourceFam)}</a>
  <a class="btn concierge" href="contact.html?compare=...">Request a private consultation</a>
</div>
```

**Updated Code:**
```html
<div class="ractions ractions--optimized">
  <!-- Guidance text -->
  <div class="ractions__guidance" style="text-align: center; margin-bottom: 32px; color: var(--muted); font-size: 14px; line-height: 1.6;">
    <p>Based on your preferences, these bodies match your fit. The next step is a quick conversation with our concierge about finishing, pricing, and delivery.</p>
  </div>
  
  <!-- Primary CTA -->
  <a class="btn solid btn--large" href="contact.html?compare=${encodeURIComponent(compareCodes)}&src=quiz&cta=ask_concierge_after_quiz&context=quiz_result&channel=contact&quiz_summary=${encodeURIComponent(quizSummary)}" style="display: block; margin: 0 auto 14px; max-width: 400px; padding: 16px 32px; text-align: center; font-size: 15px; font-weight: 600;">
    Request Your Consultation
    <div style="font-size: 12px; margin-top: 4px; opacity: 0.8;">→ 2-minute form</div>
  </a>
  
  <!-- Secondary actions (reduced visual weight) -->
  <div class="ractions__secondary" style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
    <button class="btn ghost" id="retake-btn" style="padding: 11px 20px; font-size: 13px;">↻ Retake Quiz</button>
    <a class="btn ghost" href="#match-grid" style="padding: 11px 20px; font-size: 13px;">View Matches ↓</a>
  </div>
</div>
```

**CSS to add (in quiz.html <style> section, after line ~230):**
```css
.ractions--optimized {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
  margin-top: 48px;
}

.ractions__guidance {
  margin-bottom: 28px;
}

.ractions__secondary {
  margin-top: 8px;
  gap: 12px;
}

@media(max-width: 600px) {
  .ractions__secondary {
    flex-direction: column;
    width: 100%;
  }
  .ractions__secondary .btn {
    width: 100%;
  }
}
```

---

## 3. CONTACT FORM IMPROVEMENTS (contact.html)

### Change 3.1: Add Form Progress Bar

**Location:** Before `<div class="audience-switch">` (line ~233)

**Add this code:**
```html
<!-- Form progress indicator -->
<div class="form__progress-tracker" style="margin-bottom: 36px;">
  <div style="display: flex; gap: 2px; margin-bottom: 12px; align-items: center;">
    <div class="progress-step active" style="flex: 1; text-align: center; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: var(--gold); font-weight: 600;">Step 1</div>
    <div style="width: 20px; height: 1px; background: var(--line);"></div>
    <div class="progress-step" style="flex: 1; text-align: center; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: var(--muted); opacity: 0.5;">Step 2</div>
    <div style="width: 20px; height: 1px; background: var(--line);"></div>
    <div class="progress-step" style="flex: 1; text-align: center; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: var(--muted); opacity: 0.5;">Message</div>
  </div>
  <div style="height: 3px; border-radius: 3px; background: var(--s3); overflow: hidden;">
    <div style="height: 100%; width: 33%; background: var(--gold); transition: width 0.4s ease;"></div>
  </div>
  <div style="margin-top: 10px; text-align: center; font-size: 12px; color: var(--muted);">Estimated time: 2 minutes</div>
</div>

<!-- Reassurance banner -->
<div class="form__reassurance" style="background: linear-gradient(90deg, rgba(159,214,182,.08), transparent), rgba(255,255,255,.02); border: 1px solid rgba(159,214,182,.25); border-radius: 12px; padding: 14px 18px; margin-bottom: 28px; font-size: 12px; letter-spacing: 0.5px; color: var(--muted);">
  <span style="color: var(--Muse); font-weight: 600;">✓</span> Fully discreet 
  <span style="margin: 0 8px;">·</span>
  <span style="color: var(--Muse); font-weight: 600;">✓</span> No pressure 
  <span style="margin: 0 8px;">·</span>
  <span style="color: var(--Muse); font-weight: 600;">✓</span> Response in 1 business day
</div>
```

### Change 3.2: Reposition Consent Checkbox

**Current Location:** Line ~379 (near bottom of form)

**New Location:** Right after the name/email row (around line ~289)

**Locate this section:**
```html
<div class="form-row">
  <div class="form-group">
    <label for="f-name">Name <span class="req">*</span></label>
    <input type="text" id="f-name" name="name" ...>
  </div>
  <div class="form-group">
    <label for="f-email">Email <span class="req">*</span></label>
    <input type="email" id="f-email" name="email" ...>
  </div>
</div>
<!-- ADD CONSENT HERE -->
```

**Add this after the name/email form-row:**
```html
<!-- Early consent — establishes trust immediately -->
<div class="consent-row" style="margin-top: 28px; margin-bottom: 24px; padding: 18px; border: 1px solid color-mix(in srgb, var(--gold) 22%, transparent); border-radius: 12px; background: rgba(212,165,116,.04);">
  <input type="checkbox" id="f-consent" name="consent" required>
  <label for="f-consent" style="font-size: 13px; line-height: 1.6;">
    I confirm that I am 18+ years old. I agree to be contacted about this inquiry and understand my information is <strong style="color: var(--Muse);">completely discreet</strong> and <strong style="color: var(--Muse);">never shared</strong> with third parties.
  </label>
</div>
<div class="field-err" id="err-consent" style="margin-top: -16px; margin-bottom: 20px;">Please confirm you are 18+ to proceed.</div>
```

**Remove or comment out** the consent row near line 379 (the one that currently appears at the bottom).

### Change 3.3: Make Audience Selection Automatic (Pre-select "New Buyer")

**Current Code (line ~236):**
```html
<button type="button" class="mode-card" data-mode="new" aria-pressed="true">
```

This is already set to `aria-pressed="true"`, so no change needed. But ensure the JavaScript respects this default state.

---

## 4. FORM FIELD ORGANIZATION IMPROVEMENTS (contact.html)

### Change 4.1: Add Section Headers + Collapsible Sections (Optional - Advanced)

This requires modifying the form structure. For a quick win, just add visual section headers:

**Before the buyer-fit fields section (line ~323):**
```html
<!-- Visual divider + section header -->
<div style="margin-top: 32px; margin-bottom: 20px; padding-top: 24px; border-top: 1px solid var(--line);">
  <h3 style="font-size: 14px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gold); margin-bottom: 6px;">Your Preferences</h3>
  <p style="font-size: 12px; color: var(--muted); line-height: 1.5;">Help us understand your vision so we can match the perfect body and finishing options.</p>
</div>
```

---

## 5. NEW TRACKING EVENTS (assets/site.js)

### Change 5.1: Add Funnel Tracking Events

**Location:** End of the `track()` function or in a new section after line ~175

**Add this code:**
```javascript
// ─────────────────────────────────────────────────────────
// FUNNEL TRACKING EVENTS (new)
// ─────────────────────────────────────────────────────────

// Track quiz entry (call from quiz.html when "Begin" is clicked)
function trackQuizStart(sourceLocation = 'hero') {
  track('quiz_started', {
    entry_source: sourceLocation,
    context: 'funnel_engagement'
  });
}

// Track quiz completion (call from quiz.html finish() function)
function trackQuizComplete(winnerFamily, sourceFamily, inDev, quizTimeSeconds = null) {
  const payload = {
    winner_family: winnerFamily,
    source_family: sourceFamily,
    in_development: inDev ? 1 : 0,
    context: 'funnel_engagement'
  };
  if (quizTimeSeconds) payload.quiz_time_sec = quizTimeSeconds;
  track('quiz_completed', payload);
}

// Track quiz abandonment (call if user leaves quiz mid-way)
function trackQuizAbandoned(currentStep, timeSpentSeconds = null) {
  const payload = {
    step: currentStep,
    context: 'funnel_drop'
  };
  if (timeSpentSeconds) payload.time_in_quiz_sec = timeSpentSeconds;
  track('quiz_abandoned', payload);
}

// Track form interaction (call on form focus)
function trackFormStarted(audienceMode = 'new') {
  track('form_started', {
    audience_mode: audienceMode,
    context: 'funnel_engagement'
  });
}

// Track form abandonment (call on page unload if form not submitted)
function trackFormAbandoned(fieldsCompleted, totalFields, lastFocusedField, timeInFormSeconds = null) {
  const payload = {
    fields_completed: fieldsCompleted,
    total_fields: totalFields,
    last_focused_field: lastFocusedField,
    context: 'funnel_drop'
  };
  if (timeInFormSeconds) payload.time_in_form_sec = timeInFormSeconds;
  track('form_abandoned', payload);
}

// Track exit-intent trigger (when modal/offer appears)
function trackExitIntentTriggered(formSection, progressPercent) {
  track('exit_intent_triggered', {
    form_section: formSection,
    progress_percent: progressPercent,
    context: 'funnel_intervention'
  });
}
```

### Change 5.2: Integrate Quiz Tracking in quiz.html

**Location:** Line ~342 (in `startQuiz()` function)

**Add this after line 348:**
```javascript
function startQuiz() {
  answers = [];
  step = 0;
  hide('intro');
  hide('rscreen');
  showSection('qscreen');
  // NEW: Track quiz start
  if (typeof trackQuizStart === 'function') {
    trackQuizStart('hero');
  }
  renderQ();
}
```

**Location:** Line ~385 (in `finish()` function)

**Add this after line ~513:**
```javascript
// NEW: Track quiz completion
if (typeof trackQuizComplete === 'function') {
  trackQuizComplete(expressed, sourceFam, isInDev(expressed));
}
```

---

## 6. FAQ SECTION (contact.html)

### Change 6.1: Add FAQ Before Footer

**Location:** Before `</main>` closing tag (around line ~457)

**Add this code:**
```html
<!-- FAQ Section -->
<section class="faq-section" style="margin-top: 80px; padding: 60px 24px; border-top: 1px solid var(--line); max-width: 1200px; margin-left: auto; margin-right: auto;">
  <div style="max-width: 760px; margin: 0 auto;">
    <h2 style="font-size: clamp(28px, 4vw, 44px); font-weight: 700; margin-bottom: 14px; text-align: center;">Common Questions</h2>
    <p style="text-align: center; color: var(--muted); font-size: 15px; margin-bottom: 48px; line-height: 1.6;">
      Ready to take the next step? Here's what to expect after you submit your consultation request.
    </p>

    <div class="faq-list" style="display: flex; flex-direction: column; gap: 16px;">
      <!-- FAQ Item 1 -->
      <details class="faq-item" style="border: 1px solid var(--line); border-radius: 12px; padding: 20px; background: var(--panel); cursor: pointer;">
        <summary style="font-weight: 600; font-size: 15px; display: flex; justify-content: space-between; align-items: center; cursor: pointer;">
          <span>What happens after I submit my consultation request?</span>
          <span style="color: var(--gold);">▼</span>
        </summary>
        <p style="margin-top: 14px; color: var(--muted); font-size: 14px; line-height: 1.7;">
          A member of our team will reach out within one business day via email or phone (whichever you prefer). During your private consultation, we'll confirm which body architecture matches your fit, walk through customization options, and provide transparent pricing. No obligation — just a professional, discreet conversation.
        </p>
      </details>

      <!-- FAQ Item 2 -->
      <details class="faq-item" style="border: 1px solid var(--line); border-radius: 12px; padding: 20px; background: var(--panel); cursor: pointer;">
        <summary style="font-weight: 600; font-size: 15px; display: flex; justify-content: space-between; align-items: center; cursor: pointer;">
          <span>How long does a consultation take?</span>
          <span style="color: var(--gold);">▼</span>
        </summary>
        <p style="margin-top: 14px; color: var(--muted); font-size: 14px; line-height: 1.7;">
          A typical consultation is 15–30 minutes. We'll cover what you're looking for, answer any questions about the bodies you're interested in, discuss customization, and clarify pricing and lead time. We work at your pace — no rush.
        </p>
      </details>

      <!-- FAQ Item 3 -->
      <details class="faq-item" style="border: 1px solid var(--line); border-radius: 12px; padding: 20px; background: var(--panel); cursor: pointer;">
        <summary style="font-weight: 600; font-size: 15px; display: flex; justify-content: space-between; align-items: center; cursor: pointer;">
          <span>Is my information completely private?</span>
          <span style="color: var(--gold);">▼</span>
        </summary>
        <p style="margin-top: 14px; color: var(--muted); font-size: 14px; line-height: 1.7;">
          Yes. All inquiry details are handled in complete confidence. We never share information with third parties, never send unsolicited marketing, and ship discreetly in plain, unbranded packaging. Every consultation is a private conversation between you and our concierge.
        </p>
      </details>

      <!-- FAQ Item 4 -->
      <details class="faq-item" style="border: 1px solid var(--line); border-radius: 12px; padding: 20px; background: var(--panel); cursor: pointer;">
        <summary style="font-weight: 600; font-size: 15px; display: flex; justify-content: space-between; align-items: center; cursor: pointer;">
          <span>What if I'm not sure which family is right for me?</span>
          <span style="color: var(--gold);">▼</span>
        </summary>
        <p style="margin-top: 14px; color: var(--muted); font-size: 14px; line-height: 1.7;">
          That's exactly what the consultation is for. Our concierge team is trained to help you explore the silhouettes, understand the measurement language (WHR/BWR), and narrow down the body that feels right for you. You don't need to have all the answers upfront.
        </p>
      </details>
    </div>
  </div>
</section>

<style>
details.faq-item {
  transition: all 0.2s ease;
}
details.faq-item[open] {
  background: linear-gradient(135deg, rgba(212,165,116,.08), transparent), var(--panel);
  border-color: var(--gold);
}
details.faq-item[open] summary {
  color: var(--cream);
  margin-bottom: 12px;
}
details.faq-item[open] summary span:last-child {
  transform: rotate(180deg);
  transition: transform 0.2s ease;
}
summary:hover {
  color: var(--cream);
}
</style>
```

---

## 7. MOBILE OPTIMIZATION (Universal - All Pages)

### Change 7.1: Ensure Mobile CTA is Full-Width

**For index.html hero (.cta section):**
```css
@media(max-width: 560px) {
  .hero .cta .btn {
    width: 100%;
    padding: 16px 24px;
  }
}
```

**For quiz.html result actions:**
```css
@media(max-width: 600px) {
  .ractions a.btn,
  .ractions button.btn {
    width: 100%;
    display: block;
    text-align: center;
  }
  
  .ractions__secondary {
    flex-direction: column;
  }
}
```

---

## 8. IMPLEMENTATION CHECKLIST

Use this to track your progress:

- [ ] **1.1** Update hero CTA + add trust badges (index.html)
- [ ] **2.1** Streamline quiz result buttons (quiz.html)
- [ ] **3.1** Add form progress bar (contact.html)
- [ ] **3.2** Reposition consent checkbox (contact.html)
- [ ] **4.1** Add section headers to form (contact.html)
- [ ] **5.1** Add funnel tracking events (assets/site.js)
- [ ] **5.2** Integrate quiz tracking (quiz.html)
- [ ] **6.1** Add FAQ section (contact.html)
- [ ] **7.1** Mobile CTA optimization (all pages)
- [ ] **Test** Load each page and verify all changes render correctly
- [ ] **Validate** Form submission works end-to-end
- [ ] **Deploy** Commit changes and merge to main

---

## Notes

- All changes are backward-compatible (no breaking changes)
- Inline styles used for quick implementation; consider moving to `assets/site.css` for production
- Progress bar width should be updated dynamically via JavaScript if form sections are made collapsible (advanced enhancement)
- A/B testing framework ready for implementation (see Section 5 in main analysis)

