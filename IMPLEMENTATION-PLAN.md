# ZELEX Atlas Implementation Plan — 52 Weeks

**Version:** 1.0  
**Last Updated:** 2026-06-21  
**Scope:** Complete SWOT resolution via 4-phase strategic delivery  
**Tracking:** All work tracked in `bd (beads)` issue system

---

## Quick Reference

| Phase | Duration | FTE | Effort | Key Deliverables |
|---|---|---|---|---|
| **Phase 1: Foundation** | 6 weeks | 1.0 + 0.5 | 240h | Tokens + CDN + Pipeline + Analytics |
| **Phase 2: Monetization** | 8 weeks | 1.5 | 320h | Shopify sync + Quiz engine + Intake forms |
| **Phase 3: Scale** | 10 weeks | 1.5 | 400h | Component abstraction + Community hub |
| **Phase 4: Polish** | Ongoing | 0.75 | 36h/mo | Perf optimization, runbooks, handoff |
| **TOTAL (Year 1)** | 52 weeks | — | **960h** | 12 strategic PDRs, 100+ completed tasks |

---

## Phase 1: Foundation (6 weeks, Weeks 1-6)

**Objective:** Build automation, fix tech debt, enable observability  
**Owner:** Platform Engineering Lead  
**Success:** CI >98%, builds <1min, GA4 live, zero visual regressions

### Initiative 1.1: Design Token System (Weeks 1-2)

**Issue:** `ZELEX-ARCH-001` — Implement design token system v1  
**Effort:** 60h (FE lead 40h + FE contractor 20h)  
**Dependencies:** None

**Breakdown:**

```
1.1.1 Audit current site.css → identify all tokens (colors, spacing, type, shadows)
      Owner: FE Lead | Effort: 8h | Deliverable: audit.md

1.1.2 Define token schema + naming conventions
      Owner: FE Lead | Effort: 4h | Deliverable: docs/design-tokens.md

1.1.3 Extract colors into :root (12 semantic groups, ~40 variables)
      Owner: FE Contractor | Effort: 6h | Deliverable: site-tokens.css (draft)

1.1.4 Extract spacing into :root (--sp1 through --sp8, 4px → 64px grid)
      Owner: FE Contractor | Effort: 4h | Deliverable: updated site-tokens.css

1.1.5 Extract type scale into :root (--t-xs through --t-3xl)
      Owner: FE Contractor | Effort: 4h | Deliverable: updated site-tokens.css

1.1.6 Extract shadows into :root (--sh-card, --sh-hover, --sh-focus)
      Owner: FE Contractor | Effort: 4h | Deliverable: updated site-tokens.css

1.1.7 Refactor site.css to reference tokens only (no inline values)
      Owner: FE Lead | Effort: 20h | Deliverable: refactored site.css (350 lines)

1.1.8 Pixel-perfect regression testing (Percy/Chromatic comparison)
      Owner: FE Contractor | Effort: 6h | Deliverable: regression-report.md

1.1.9 Update CONTRIBUTING.md + token documentation
      Owner: FE Lead | Effort: 4h | Deliverable: updated CONTRIBUTING.md
```

**Definition of Done:**
- [ ] All colors use CSS variables (zero hex codes in site.css)
- [ ] All spacing uses --sp* tokens
- [ ] All shadows use --sh-* tokens
- [ ] CSS file size: 647 → 350 lines
- [ ] Pixel-perfect before/after comparison: 0 regressions
- [ ] Storybook component guide drafted (1.2.1)

---

### Initiative 1.2: Component Library & Storybook (Weeks 1-3)

**Issue:** `ZELEX-ARCH-002` — Build component Storybook (static HTML)  
**Effort:** 40h (FE lead 25h + FE contractor 15h)  
**Dependencies:** 1.1 (tokens finalized)

**Breakdown:**

```
1.2.1 Design Storybook structure + component taxonomy
      Owner: FE Lead | Effort: 4h | Deliverable: Storybook outline

1.2.2 Implement Storybook template (static HTML, no Node.js)
      Owner: FE Lead | Effort: 8h | Deliverable: docs/component-storybook.html (skeleton)

1.2.3 Document all button variants (primary, secondary, ghost, concierge)
      Owner: FE Contractor | Effort: 6h | Deliverable: buttons section

1.2.4 Document all card variants (character, body, comparison)
      Owner: FE Contractor | Effort: 6h | Deliverable: cards section

1.2.5 Document grid layouts (browse, family, quiz results)
      Owner: FE Contractor | Effort: 4h | Deliverable: grids section

1.2.6 Document forms (contact, intake, search)
      Owner: FE Contractor | Effort: 4h | Deliverable: forms section

1.2.7 Document modals + accessibility variants (dark mode, reduced motion, focus)
      Owner: FE Lead | Effort: 5h | Deliverable: modals + a11y sections

1.2.8 Add component usage guidelines + accessibility notes
      Owner: FE Lead | Effort: 3h | Deliverable: usage guide

1.2.9 Link Storybook from CONTRIBUTING.md + project README
      Owner: FE Lead | Effort: 1h | Deliverable: updated README.md
```

**Definition of Done:**
- [ ] Storybook file: 100% accessible (WCAG AA)
- [ ] All site.css components documented
- [ ] Component markup + CSS for each variant included
- [ ] Linked from CONTRIBUTING.md
- [ ] Load time: <2s (static HTML, no dependencies)

---

### Initiative 1.3: Image CDN & Asset Versioning (Weeks 2-4)

**Issue:** `ZELEX-OPS-001` — Implement image CDN + manifest versioning  
**Effort:** 80h (DevOps 60h + Platform 20h)  
**Dependencies:** None (parallel with 1.1)

**Breakdown:**

```
1.3.1 Evaluate CDN options (Cloudinary, Bunny, AWS CloudFront)
      Owner: DevOps | Effort: 8h | Deliverable: CDN-evaluation.md

1.3.2 Select CDN + provision account (brand-compliant, US-hosted)
      Owner: DevOps | Effort: 4h | Deliverable: CDN credentials (secure storage)

1.3.3 Design manifest schema (image path → hash → CDN URL → timestamp)
      Owner: Platform | Effort: 4h | Deliverable: db/assets_manifest_schema.json

1.3.4 Implement image upload script (batch upload with SHA256 hashing)
      Owner: DevOps | Effort: 12h | Deliverable: scripts/push_assets_to_cdn.py

1.3.5 Generate initial manifest (all current images → CDN)
      Owner: DevOps | Effort: 6h | Deliverable: db/assets_manifest.json (v1)

1.3.6 Implement CI guard: validate manifest freshness (fail if >48h old)
      Owner: Platform | Effort: 8h | Deliverable: scripts/validate_manifest_freshness.py

1.3.7 Add manifest freshness check to pre-push hook
      Owner: Platform | Effort: 4h | Deliverable: updated hooks/pre-push

1.3.8 Implement fallback logic (if CDN unavailable, use git images)
      Owner: Platform | Effort: 8h | Deliverable: assets/image-loader.js (fallback)

1.3.9 Update site.js image loading to use manifest URLs
      Owner: Platform | Effort: 10h | Deliverable: updated assets/site.js

1.3.10 Document image refresh workflow + troubleshooting
       Owner: DevOps | Effort: 8h | Deliverable: docs/image-cdn.md + runbook

1.3.11 Test image freshness checks + failover scenarios
       Owner: DevOps | Effort: 4h | Deliverable: test-report.md
```

**Definition of Done:**
- [ ] All images hosted on CDN (zero git-hosted images except dev fallback)
- [ ] Manifest schema defined + validated
- [ ] Upload script fully automated (<30s per batch)
- [ ] CI guard fails build if manifest stale
- [ ] Fallback logic tested
- [ ] Runbook documented + tested with brand team

---

### Initiative 1.4: Python Pipeline Parallelization (Weeks 3-4)

**Issue:** `ZELEX-OPS-002` — Parallelize build pipeline + add retry/resume  
**Effort:** 60h (Platform 50h + DevOps 10h)  
**Dependencies:** None (parallel with CDN work)

**Breakdown:**

```
1.4.1 Audit each build script for idempotence (safe to re-run)
      Owner: Platform | Effort: 12h | Deliverable: idempotence-audit.md

1.4.2 Refactor build_db.py to skip already-processed assets
      Owner: Platform | Effort: 8h | Deliverable: updated build_db.py

1.4.3 Refactor build_profiles.py to use cached input
      Owner: Platform | Effort: 6h | Deliverable: updated build_profiles.py

1.4.4 Refactor build_characters.py + merge_stories.py + make_thumbs.py
      Owner: Platform | Effort: 12h | Deliverable: 3 refactored scripts

1.4.5 Design build state tracking (which stages completed)
      Owner: Platform | Effort: 4h | Deliverable: db/.build_state_schema.json

1.4.6 Implement build_orchestrator.py (parallel stage execution + resume)
      Owner: Platform | Effort: 16h | Deliverable: scripts/build_orchestrator.py

1.4.7 Add --resume flag + exponential backoff retry logic
      Owner: Platform | Effort: 8h | Deliverable: updated orchestrator

1.4.8 Update CI to use orchestrator instead of individual scripts
      Owner: DevOps | Effort: 4h | Deliverable: updated .github/workflows/ci.yml

1.4.9 Test full pipeline: normal run, resume after failure, parallel stages
      Owner: Platform | Effort: 6h | Deliverable: test-report.md

1.4.10 Document pipeline troubleshooting + resume workflow
       Owner: DevOps | Effort: 4h | Deliverable: docs/pipeline-guide.md
```

**Definition of Done:**
- [ ] All build scripts are idempotent
- [ ] Orchestrator parallelizes stages 2-3, 4-5 (where possible)
- [ ] Build time: 2min → <1min (50% improvement minimum)
- [ ] Resume flag skips completed stages
- [ ] Retry logic tested with simulated failures
- [ ] CI updated + green

---

### Initiative 1.5: GTM + GA4 Wiring (Weeks 2-5)

**Issue:** `ZELEX-ANALYTICS-001` — Wire GTM container + GA4 integration  
**Effort:** 70h (Analytics 40h + FE 30h)  
**Dependencies:** None (parallel)

**Breakdown:**

```
1.5.1 Create GTM container in brand Google account
      Owner: Analytics | Effort: 2h | Deliverable: GTM container ID

1.5.2 Define dataLayer schema (events, user properties, conversion tracking)
      Owner: Analytics | Effort: 8h | Deliverable: docs/analytics-datalayer-schema.md

1.5.3 Design GA4 events + dimensions (quiz, form, character, family)
      Owner: Analytics | Effort: 6h | Deliverable: GA4-event-taxonomy.md

1.5.4 Implement quiz tracking (start, completion, result view)
      Owner: FE | Effort: 8h | Deliverable: updated assets/site.js (quiz)

1.5.5 Implement contact form tracking (start, prefill source, submit)
      Owner: FE | Effort: 6h | Deliverable: updated contact.html + site.js

1.5.6 Implement character detail tracking (view, gallery scroll, related click)
      Owner: FE | Effort: 6h | Deliverable: updated character.html + site.js

1.5.7 Implement comparison tool tracking (bodies selected, share clicked)
      Owner: FE | Effort: 4h | Deliverable: updated compare.html + site.js

1.5.8 Implement configurator tracking (load, interaction, save state)
      Owner: FE | Effort: 6h | Deliverable: updated configurator.html + site.js

1.5.9 Configure GTM variables + tags + triggers (all events)
      Owner: Analytics | Effort: 12h | Deliverable: GTM container (configured)

1.5.10 Audit dataLayer for PII (scrub email, phone, sensitive data)
       Owner: Analytics | Effort: 6h | Deliverable: PII-scrubbing-audit.md

1.5.11 Test GA4 event firing (QA checklist: 50+ event combinations)
       Owner: Analytics + FE | Effort: 6h | Deliverable: GA4-testing-report.md

1.5.12 Document GTM setup + event firing + troubleshooting
       Owner: Analytics | Effort: 4h | Deliverable: docs/gtm-setup.md
```

**Definition of Done:**
- [ ] GTM container deployed to all pages (zero missing tags)
- [ ] dataLayer firing on all tracked events
- [ ] GA4 events match taxonomy (50+ event types)
- [ ] PII audit complete (zero emails/phones in GA4)
- [ ] Test coverage: 100% of conversion paths
- [ ] Documentation + runbook complete

---

### Initiative 1.6: Analytics Dashboard (Weeks 5-6)

**Issue:** `ZELEX-ANALYTICS-002` — Build leadership analytics dashboard  
**Effort:** 40h (Analytics 30h + FE 10h)  
**Dependencies:** 1.5 (GA4 wired)

**Breakdown:**

```
1.6.1 Design dashboard structure (4 key sections: competitive, funnel, traffic, engagement)
      Owner: Analytics | Effort: 4h | Deliverable: dashboard-wireframe.md

1.6.2 Create Looker Studio report + import GA4 data source
      Owner: Analytics | Effort: 8h | Deliverable: Looker report (draft)

1.6.3 Build competitive positioning heatmap (family coverage %)
      Owner: Analytics | Effort: 8h | Deliverable: heatmap widget

1.6.4 Build conversion funnel (Quiz → Inquiry → Premium Intake)
      Owner: Analytics | Effort: 8h | Deliverable: funnel widget + drop-off analysis

1.6.5 Build traffic source breakdown (organic, direct, referral, paid)
      Owner: Analytics | Effort: 4h | Deliverable: traffic widget

1.6.6 Build engagement by family (which bodies drive most traffic/conversions)
      Owner: Analytics | Effort: 4h | Deliverable: engagement widget

1.6.7 Add dashboard legend + metric definitions
      Owner: Analytics | Effort: 2h | Deliverable: dashboard documentation

1.6.8 Configure daily refresh + test data flow
      Owner: Analytics | Effort: 2h | Deliverable: refresh schedule verified

1.6.9 Share with leadership + gather feedback
      Owner: Analytics | Effort: 2h | Deliverable: feedback-log.md
```

**Definition of Done:**
- [ ] Dashboard accessible to brand team (Looker Studio link shared)
- [ ] All widgets auto-refresh daily
- [ ] Metrics explained in legend
- [ ] Trend analysis enabled (month-over-month)
- [ ] Leadership sign-off

---

### Initiative 1.7: Documentation & Runbooks (Weeks 4-6)

**Issue:** `ZELEX-DEVEX-001` — Create complete Phase 1 runbooks  
**Effort:** 30h (DevOps 20h + Platform 10h)  
**Dependencies:** All initiatives 1.1-1.6 completed

**Breakdown:**

```
1.7.1 Create "Design Token System" runbook (how to add/modify tokens)
      Owner: DevOps | Effort: 4h | Deliverable: docs/design-tokens-runbook.md

1.7.2 Create "Image CDN Management" runbook (upload, refresh, troubleshoot)
      Owner: DevOps | Effort: 6h | Deliverable: docs/cdn-runbook.md

1.7.3 Create "Build Pipeline" runbook (how to run, resume, debug)
      Owner: Platform | Effort: 6h | Deliverable: docs/pipeline-runbook.md

1.7.4 Create "Analytics" runbook (event testing, GA4 debugging, dashboard refresh)
      Owner: DevOps | Effort: 4h | Deliverable: docs/analytics-runbook.md

1.7.5 Update CONTRIBUTING.md with all Phase 1 changes
      Owner: DevOps | Effort: 4h | Deliverable: updated CONTRIBUTING.md

1.7.6 Create FAQ + troubleshooting guide (common issues + fixes)
      Owner: DevOps | Effort: 4h | Deliverable: docs/phase1-faq.md

1.7.7 Internal team training session (all developers)
      Owner: DevOps | Effort: 2h | Deliverable: training-summary.md
```

**Definition of Done:**
- [ ] All runbooks linked from CONTRIBUTING.md
- [ ] Team trained + signed off
- [ ] FAQ addresses all common issues
- [ ] Troubleshooting guide covers >80% of error cases

---

### Phase 1 Success Criteria

**Must Complete (Green Exit):**
- [x] Design tokens: 100% color/spacing/type coverage, site.css 647 → 350 lines
- [x] Component Storybook: all 30+ components documented, accessible
- [x] Image CDN: all images hosted, manifest versioned, CI guard active
- [x] Pipeline: parallelized, build time <1min, retry logic working
- [x] GA4: all 50+ events firing, PII audit clean, data quality >99%
- [x] Dashboard: live, refreshing daily, leadership signed off
- [x] Documentation: all runbooks written, team trained

**Rollback Plan:**
- If token refactor introduces regressions: revert site.css, keep tokens defined in separate file
- If CDN has latency issues: use regional mirrors + fallback to git images
- If GA4 PII leak detected: disable tracking, audit, re-enable with scrubbing

**Phase 1 Gate:** All success criteria met + zero outstanding critical bugs + leadership sign-off

---

## Phase 2: Personalization & Revenue (8 weeks, Weeks 7-14)

**Objective:** Automate product updates, personalize recommendations, optimize conversion funnel  
**Owner:** Product & Platform Engineering  
**Success:** Quiz-to-inquiry +50%, Shopify sync <30min latency, premium form +30% conversions

### Initiative 2.1: Shopify Sync Automation (Weeks 7-10)

**Issue:** `ZELEX-PRODUCT-001` — Implement live Shopify product feed sync  
**Effort:** 100h (Platform 70h + DevOps 30h)  
**Dependencies:** Phase 1 complete (pipeline working)

**Breakdown:**

```
2.1.1 Design Shopify sync architecture (feed fetch, SKU mapping, diff detection)
      Owner: Platform | Effort: 6h | Deliverable: sync-architecture.md

2.1.2 Create SKU-to-body mapping table (manual input, Shopify SKU → body ID)
      Owner: Product | Effort: 8h | Deliverable: db/shopify_sku_mapping.json (v1)

2.1.3 Implement scripts/sync_shopify_feed.py (fetch, parse, map)
      Owner: Platform | Effort: 18h | Deliverable: sync script (draft)

2.1.4 Implement diff detection (new products, price changes, stock status)
      Owner: Platform | Effort: 12h | Deliverable: updated sync script

2.1.5 Implement auto-commit + PR workflow (human approval gate)
      Owner: Platform | Effort: 10h | Deliverable: sync script with git integration

2.1.6 Create GitHub Actions scheduler (runs every 6 hours)
      Owner: DevOps | Effort: 6h | Deliverable: updated .github/workflows/

2.1.7 Implement Slack alerts for failed syncs
      Owner: DevOps | Effort: 4h | Deliverable: alert configuration

2.1.8 Test full sync workflow (100+ products, edge cases: discontinued SKUs, variants)
      Owner: Platform | Effort: 12h | Deliverable: sync-test-report.md

2.1.9 Implement rollback procedure (revert catalog.json to previous version)
      Owner: Platform | Effort: 6h | Deliverable: rollback script

2.1.10 Document Shopify sync setup + troubleshooting
       Owner: DevOps | Effort: 8h | Deliverable: docs/shopify-sync.md

2.1.11 Train brand team on sync workflow + troubleshooting
       Owner: DevOps | Effort: 4h | Deliverable: training-summary.md
```

**Definition of Done:**
- [ ] Shopify API credentials stored securely (no hardcoded secrets)
- [ ] Sync runs every 6 hours automatically
- [ ] Sync is idempotent (safe to run multiple times)
- [ ] New products appear in atlas within 30min
- [ ] Failed syncs trigger Slack alerts immediately
- [ ] Rollback procedure tested + documented
- [ ] Brand team trained + can troubleshoot

---

### Initiative 2.2: Quiz-to-Recommendation Engine (Weeks 8-11)

**Issue:** `ZELEX-FE-001` — Build personalized quiz recommendations  
**Effort:** 90h (FE 60h + Platform 30h)  
**Dependencies:** Phase 1 complete (GA4 analytics)

**Breakdown:**

```
2.2.1 Analyze existing quiz questions + response mapping (family → characters)
      Owner: FE | Effort: 6h | Deliverable: quiz-analysis.md

2.2.2 Design recommendation algorithm (quiz response → top 3-4 characters)
      Owner: Platform | Effort: 8h | Deliverable: recommendation-algorithm.md

2.2.3 Implement edge function (Vercel/Netlify) for quiz recommendations
      Owner: Platform | Effort: 20h | Deliverable: edge function (draft)

2.2.4 Train recommendation model on character attributes (WHR, BWR, style)
      Owner: Platform | Effort: 8h | Deliverable: model weights/config

2.2.5 Refactor quiz results page (PDR-FE-005 follow-up)
      Owner: FE | Effort: 12h | Deliverable: updated quiz.html

2.2.6 Integrate recommendation engine into results flow
      Owner: FE | Effort: 10h | Deliverable: quiz.html + edge function integration

2.2.7 Pre-fill contact form with recommended body + character
      Owner: FE | Effort: 8h | Deliverable: updated contact.html

2.2.8 Test recommendation accuracy (100+ quiz responses, validate suggestions)
      Owner: FE + Platform | Effort: 8h | Deliverable: testing-report.md

2.2.9 Implement A/B test (standard results vs. personalized recommendations)
      Owner: FE + Analytics | Effort: 8h | Deliverable: a/b test setup in GA4

2.2.10 Document quiz recommendation system + edge function deployment
       Owner: Platform | Effort: 4h | Deliverable: docs/quiz-recommendations.md
```

**Definition of Done:**
- [ ] Recommendation engine returns 3-4 characters for any quiz response
- [ ] Recommendation accuracy: 85%+ (user satisfaction)
- [ ] Edge function latency: <500ms
- [ ] Fallback: if edge function unavailable, render standard results
- [ ] A/B test results tracked in GA4
- [ ] Quiz-to-form submission rate +30% (vs. control)
- [ ] Documentation complete

---

### Initiative 2.3: Premium Intake Form Optimization (Weeks 9-12)

**Issue:** `ZELEX-FE-002` — Optimize premium concierge intake form (PDR-FE-006)  
**Effort:** 70h (FE 50h + Analytics 20h)  
**Dependencies:** Phase 1 complete (analytics), 2.2 (recommendations)

**Breakdown:**

```
2.3.1 Audit existing intake form (current flow, drop-off points, conversion rate)
      Owner: Analytics | Effort: 6h | Deliverable: intake-audit.md

2.3.2 Review PDR-FE-006 spec + identify updates needed
      Owner: FE | Effort: 4h | Deliverable: pdr-fe-006-updates.md

2.3.3 Redesign form UX (progressive disclosure, inline validation)
      Owner: FE | Effort: 12h | Deliverable: updated contact.html (redesign)

2.3.4 Implement pre-fill from quiz recommendation (body + character)
      Owner: FE | Effort: 6h | Deliverable: form-prefill logic

2.3.5 Add contextual help text + accessibility improvements
      Owner: FE | Effort: 8h | Deliverable: updated form

2.3.6 Integrate with Formspree/Getform submission (if not already)
      Owner: FE | Effort: 4h | Deliverable: form submission verified

2.3.7 Implement form submission tracking in GA4
      Owner: Analytics | Effort: 6h | Deliverable: form events in GA4

2.3.8 A/B test form variants (layout, copy, field order)
      Owner: FE + Analytics | Effort: 12h | Deliverable: a/b test in GA4

2.3.9 Measure conversion improvement (baseline vs. optimized)
      Owner: Analytics | Effort: 6h | Deliverable: conversion-analysis.md

2.3.10 Document form optimization results + learnings
       Owner: FE | Effort: 6h | Deliverable: intake-optimization-summary.md
```

**Definition of Done:**
- [ ] Form UX improved (clearer labeling, better field order)
- [ ] Pre-fill working (quiz → form body/character prefilled)
- [ ] Form submission tracked in GA4
- [ ] A/B test results: +30% conversion rate (target)
- [ ] Accessibility audit passed (WCAG AA)
- [ ] Documentation + learnings documented

---

### Initiative 2.4: Conversion Funnel Optimization (Weeks 10-14)

**Issue:** `ZELEX-ANALYTICS-003` — Analyze + optimize full conversion funnel  
**Effort:** 60h (Analytics 40h + FE 20h)  
**Dependencies:** Phase 1 complete (GA4), 2.1-2.3 complete

**Breakdown:**

```
2.4.1 Analyze full funnel (entry point → quiz start → completion → form submission)
      Owner: Analytics | Effort: 8h | Deliverable: funnel-analysis.md

2.4.2 Identify drop-off points (where do users leave?)
      Owner: Analytics | Effort: 6h | Deliverable: drop-off-analysis.md

2.4.3 Correlate drop-off with device type, traffic source, time of day
      Owner: Analytics | Effort: 8h | Deliverable: correlation-analysis.md

2.4.4 Implement exit-intent survey (why users leave? gather feedback)
      Owner: FE | Effort: 6h | Deliverable: survey integration

2.4.5 A/B test high-impact changes (CTA copy, quiz intro, recommendation presentation)
      Owner: FE + Analytics | Effort: 16h | Deliverable: 3 a/b tests running in GA4

2.4.6 Measure impact of each optimization
      Owner: Analytics | Effort: 8h | Deliverable: optimization-impact-report.md

2.4.7 Document final conversion funnel + optimizations applied
      Owner: Analytics | Effort: 8h | Deliverable: funnel-optimization-summary.md
```

**Definition of Done:**
- [ ] Funnel analysis complete (entry → conversion mapped)
- [ ] Drop-off points identified + prioritized
- [ ] 3+ high-impact A/B tests running
- [ ] Overall conversion rate improvement: +50% (target)
- [ ] All insights documented + presented to leadership

---

### Phase 2 Success Criteria

**Must Complete:**
- [x] Shopify sync: automated, 6-hour schedule, <30min latency
- [x] Quiz recommendations: 85%+ accuracy, +30% form submission rate
- [x] Premium intake form: optimized UX, pre-fill working, +30% conversion
- [x] Funnel analysis: complete, drop-off points identified, optimizations live
- [x] GA4 tracking: 100% of events firing, data quality verified

**Success Metrics:**
- Quiz-to-inquiry conversion: 12% → 18% (target)
- Form submission rate: baseline + 30%
- Shopify sync latency: <30min (typically <5min)
- GA4 event accuracy: 99%+

**Phase 2 Gate:** All success criteria met + conversion funnel improvements tracked + leadership sign-off

---

## Phase 3: Scaling & Community (10 weeks, Weeks 15-24)

**Objective:** Support 12+ body families, build community engagement, reduce maintenance burden  
**Owner:** Frontend & Platform Engineering  
**Success:** HTML pages 41 → 15, community submissions 100+/month, CSS -40% bundle size

### Initiative 3.1: Fragment Library & Page Templates (Weeks 15-17)

**Issue:** `ZELEX-ARCH-003` — Extract reusable HTML fragments + page templates  
**Effort:** 80h (FE 60h + Platform 20h)  
**Dependencies:** Phase 1 complete (design tokens)

**Breakdown:**

```
3.1.1 Audit all 41 HTML pages for common patterns (headers, cards, grids, footers)
      Owner: FE | Effort: 8h | Deliverable: fragment-audit.md

3.1.2 Define fragment library (10-15 fragments to extract)
      Owner: FE | Effort: 6h | Deliverable: fragment-spec.md

3.1.3 Create fragments/header.html (page header, logo, brand messaging)
      Owner: FE | Effort: 4h | Deliverable: fragments/header.html

3.1.4 Create fragments/nav.html (main navigation, family links)
      Owner: FE | Effort: 4h | Deliverable: fragments/nav.html

3.1.5 Create fragments/footer.html (footer, links, brand info)
      Owner: FE | Effort: 4h | Deliverable: fragments/footer.html

3.1.6 Create fragments/char-card.html (character card + variants)
      Owner: FE | Effort: 6h | Deliverable: fragments/char-card.html

3.1.7 Create fragments/body-card.html (body architecture card + variants)
      Owner: FE | Effort: 6h | Deliverable: fragments/body-card.html

3.1.8 Create fragments/family-grid.html (family grid layout)
      Owner: FE | Effort: 4h | Deliverable: fragments/family-grid.html

3.1.9 Create fragments/contact-form.html (reusable contact form + variants)
      Owner: FE | Effort: 6h | Deliverable: fragments/contact-form.html

3.1.10 Create fragments/quiz-section.html (quiz questions + result display)
       Owner: FE | Effort: 6h | Deliverable: fragments/quiz-section.html

3.1.11 Design page template syntax (simple {{var}} substitution + fragment includes)
       Owner: Platform | Effort: 6h | Deliverable: template-syntax.md

3.1.12 Document all fragments + usage examples
       Owner: FE | Effort: 4h | Deliverable: docs/fragment-library.md
```

**Definition of Done:**
- [ ] 15+ fragments defined + implemented
- [ ] Fragment syntax is simple (no complex templating language)
- [ ] All fragments parameterized for reuse (accept options)
- [ ] Fragment library documented + tested

---

### Initiative 3.2: Page Generation Script (Weeks 16-18)

**Issue:** `ZELEX-ARCH-004` — Implement page generation from schema  
**Effort:** 70h (Platform 60h + FE 10h)  
**Dependencies:** 3.1 (fragments finalized)

**Breakdown:**

```
3.2.1 Design page configuration schema (which fragments, data, options per page)
      Owner: Platform | Effort: 6h | Deliverable: db/pages_config_schema.json

3.2.2 Create initial pages_config.json (all 41 current pages mapped)
      Owner: Platform | Effort: 8h | Deliverable: db/pages_config.json (draft)

3.2.3 Implement scripts/generate_pages.py (template substitution + fragment includes)
      Owner: Platform | Effort: 18h | Deliverable: page generation script

3.2.4 Implement template caching + incremental generation (only regenerate changed pages)
      Owner: Platform | Effort: 10h | Deliverable: updated generate_pages.py

3.2.5 Integrate page generation into build pipeline (orchestrator step)
      Owner: Platform | Effort: 8h | Deliverable: updated build_orchestrator.py

3.2.6 Regenerate all 41 pages from schema + verify no regressions
      Owner: FE + Platform | Effort: 12h | Deliverable: regressions-report.md

3.2.7 Test adding new character/body (verify pages auto-generated correctly)
      Owner: FE | Effort: 4h | Deliverable: test-report.md

3.2.8 Document page generation + schema updates
      Owner: Platform | Effort: 4h | Deliverable: docs/page-generation.md
```

**Definition of Done:**
- [ ] Page schema defined + all 41 current pages mapped
- [ ] Page generation script fully automated
- [ ] No visual regressions (pixel-perfect generated pages)
- [ ] New page generation time: <10 seconds
- [ ] Documentation complete

---

### Initiative 3.3: Component Audit & Consolidation (Weeks 18-20)

**Issue:** `ZELEX-ARCH-005` — Audit components, eliminate variants, standardize  
**Effort:** 60h (FE 50h + QA 10h)  
**Dependencies:** 3.1 (fragments complete)

**Breakdown:**

```
3.3.1 Inventory all components across 41 pages (cards, grids, forms, modals)
      Owner: FE | Effort: 8h | Deliverable: component-inventory.md

3.3.2 Identify duplicate components + redundant variants
      Owner: FE | Effort: 8h | Deliverable: duplication-report.md

3.3.3 Design consolidated component specs (reduce 30+ variants → 10 consolidated)
      Owner: FE | Effort: 8h | Deliverable: consolidation-plan.md

3.3.4 Refactor character card (9 variants → 3: featured, grid, mini)
      Owner: FE | Effort: 8h | Deliverable: refactored character card

3.3.5 Refactor body card (6 variants → 2: full spec, thumbnail)
      Owner: FE | Effort: 6h | Deliverable: refactored body card

3.3.6 Refactor comparison grid (4 layouts → 1 standardized)
      Owner: FE | Effort: 6h | Deliverable: refactored comparison grid

3.3.7 Refactor contact form (3 variants → 1 with preset options)
      Owner: FE | Effort: 6h | Deliverable: refactored form

3.3.8 Update CSS to eliminate variant-specific overrides
      Owner: FE | Effort: 8h | Deliverable: refactored site.css (further reduced)

3.3.9 Pixel-perfect regression testing (all 41 pages)
      Owner: QA | Effort: 6h | Deliverable: regression-report.md

3.3.10 Document component consolidation results + CSS savings
       Owner: FE | Effort: 4h | Deliverable: consolidation-summary.md
```

**Definition of Done:**
- [ ] Component variants: 30+ → 10 (67% reduction)
- [ ] CSS specificity: max depth 5+ → 3 (flatter hierarchy)
- [ ] CSS file size further reduced (350 → 250 lines target)
- [ ] Zero visual regressions across all pages
- [ ] Maintainability significantly improved

---

### Initiative 3.4: Community Hub Launch (Weeks 19-24)

**Issue:** `ZELEX-COMMUNITY-001` — Launch community hub (galleries, events, reviews)  
**Effort:** 100h (FE 60h + Platform 40h)  
**Dependencies:** Phase 1 complete (analytics), design tokens + fragments ready

**Breakdown:**

```
3.4.1 Design community hub structure + user flows
      Owner: FE | Effort: 8h | Deliverable: community-design.md

3.4.2 Implement user gallery submission form
      Owner: FE | Effort: 12h | Deliverable: community-gallery-submit.html

3.4.3 Implement gallery grid + filtering (by family, contributor)
      Owner: FE | Effort: 12h | Deliverable: community-gallery.html

3.4.4 Implement moderation workflow (brand team reviews submissions)
      Owner: Platform | Effort: 16h | Deliverable: moderation dashboard

3.4.5 Implement events calendar (community meetups, photoshoots)
      Owner: FE | Effort: 10h | Deliverable: community-events.html

3.4.6 Add iCal feed export (users can subscribe to event calendar)
      Owner: Platform | Effort: 8h | Deliverable: events iCal endpoint

3.4.7 Implement user reviews/testimonials (ZELEX ownership stories)
      Owner: FE | Effort: 8h | Deliverable: reviews carousel

3.4.8 Add community hub to main nav + featured section on homepage
      Owner: FE | Effort: 4h | Deliverable: updated index.html + nav

3.4.9 SEO optimization (schema markup for collections, user galleries)
      Owner: Platform | Effort: 6h | Deliverable: updated schema.org markup

3.4.10 Test end-to-end (submit gallery, approve in moderation, verify published)
       Owner: QA | Effort: 6h | Deliverable: testing-report.md

3.4.11 Document community hub features + moderation process
       Owner: Platform | Effort: 4h | Deliverable: community-hub-guide.md
```

**Definition of Done:**
- [ ] Community hub pages live + discoverable from nav
- [ ] Gallery submission form working + moderation queue active
- [ ] Events calendar published + iCal feed working
- [ ] Schema markup implemented (JSON-LD collections)
- [ ] Brand team trained on moderation workflow
- [ ] First 20+ submissions queued + moderation process validated

---

### Initiative 3.5: Performance Optimization Pass (Weeks 22-24)

**Issue:** `ZELEX-PERF-001` — Optimize all pages to Lighthouse >90  
**Effort:** 50h (FE 40h + DevOps 10h)  
**Dependencies:** All Phase 3 initiatives complete

**Breakdown:**

```
3.5.1 Audit all pages with Lighthouse + WebPageTest
      Owner: FE | Effort: 6h | Deliverable: perf-audit.md

3.5.2 Optimize LCP (Largest Contentful Paint) on hero images
      Owner: FE | Effort: 12h | Deliverable: optimized image loading

3.5.3 Optimize CLS (Cumulative Layout Shift) — prevent layout thrashing
      Owner: FE | Effort: 10h | Deliverable: fixed layout issues

3.5.4 Minimize JavaScript bundle + defer non-critical scripts
      Owner: FE | Effort: 8h | Deliverable: optimized site.js

3.5.5 Optimize font loading (system fonts for body, curated serif for headings)
      Owner: FE | Effort: 6h | Deliverable: optimized font strategy

3.5.6 Enable static asset compression + CDN caching headers
      Owner: DevOps | Effort: 4h | Deliverable: updated Caddyfile + CDN config

3.5.7 Verify Lighthouse scores >90 across all pages
      Owner: FE | Effort: 4h | Deliverable: lighthouse-report.md
```

**Definition of Done:**
- [ ] Lighthouse score: >90 on all pages (target: >95)
- [ ] LCP: <2.5s (target: <1.5s)
- [ ] CLS: <0.1 (target: <0.05)
- [ ] Mobile performance optimized (key metric: <3s load time)

---

### Phase 3 Success Criteria

**Must Complete:**
- [x] Fragment library: 15+ reusable fragments, fully documented
- [x] Page generation: all 41 pages generated from schema, zero regressions
- [x] HTML pages: 41 → 15 hand-coded (67% reduction)
- [x] CSS bundle: 350 → 250 lines (29% reduction vs. Phase 1)
- [x] Components: 30+ variants → 10 consolidated
- [x] Community hub: 100+ submissions in first month
- [x] Performance: Lighthouse >90 across all pages

**Success Metrics:**
- Community submissions: 100+/month (3+ months sustained)
- CSS maintainability: 80%+ improvement (per team survey)
- Time to add new character: 2h → 30min (75% faster)
- Pages maintainability score: A+ (per maintainability audit)

**Phase 3 Gate:** All success criteria met + community hub stable + Lighthouse >90 + leadership sign-off

---

## Phase 4: Optimization & Handoff (Ongoing, Weeks 25-52)

**Objective:** Polish, document, establish runbooks, prepare for brand team ownership  
**Owner:** DevOps & QA  
**Success:** <5min local setup, <1h contributor onboarding, zero incidents

### Initiative 4.1: Developer Experience & Onboarding (Weeks 25-28)

**Issue:** `ZELEX-DEVEX-002` — Optimize local setup + contributor onboarding  
**Effort:** 40h (DevOps 30h + FE 10h)  
**Dependencies:** All Phase 1-3 complete

**Breakdown:**

```
4.1.1 Audit current local setup (clone, install, run, build)
      Owner: DevOps | Effort: 4h | Deliverable: setup-audit.md

4.1.2 Create docker-compose.yml for one-command local dev setup
      Owner: DevOps | Effort: 12h | Deliverable: docker-compose.yml + README

4.1.3 Create start-dev.sh (automated environment setup)
      Owner: DevOps | Effort: 6h | Deliverable: start-dev.sh script

4.1.4 Simplify dependencies (minimize npm/pip packages)
      Owner: DevOps + FE | Effort: 8h | Deliverable: optimized package.json + requirements.txt

4.1.5 Create contributor quickstart guide (5 steps to first contribution)
      Owner: DevOps | Effort: 4h | Deliverable: QUICKSTART.md

4.1.6 Create "common tasks" guide (run tests, add character, deploy)
      Owner: DevOps | Effort: 6h | Deliverable: docs/common-tasks.md
```

**Definition of Done:**
- [ ] Local setup time: <5min (target)
- [ ] Contributor onboarding: <1h (clone → first test run)
- [ ] All setup steps automated (no manual steps)
- [ ] QUICKSTART.md provides end-to-end walkthrough

---

### Initiative 4.2: Runbook & Incident Response (Weeks 28-32)

**Issue:** `ZELEX-OPS-003` — Create complete runbooks + incident response plan  
**Effort:** 50h (DevOps 40h + Platform 10h)  
**Dependencies:** All Phase 1-3 complete

**Breakdown:**

```
4.2.1 Create Image Refresh runbook (when/how to update images)
      Owner: DevOps | Effort: 6h | Deliverable: docs/runbook-image-refresh.md

4.2.2 Create Character Curation runbook (data collection → character publication)
      Owner: DevOps | Effort: 8h | Deliverable: docs/runbook-character-curation.md

4.2.3 Create Shopify Sync troubleshooting guide
      Owner: DevOps | Effort: 6h | Deliverable: docs/runbook-shopify-sync.md

4.2.4 Create Build Pipeline troubleshooting guide
      Owner: Platform | Effort: 6h | Deliverable: docs/runbook-build-pipeline.md

4.2.5 Create Analytics troubleshooting guide (event debugging, data verification)
      Owner: DevOps | Effort: 6h | Deliverable: docs/runbook-analytics.md

4.2.6 Create Deployment & Rollback guide
      Owner: DevOps | Effort: 6h | Deliverable: docs/runbook-deployment.md

4.2.7 Create Incident Response Playbook (what to do if X breaks)
      Owner: DevOps | Effort: 10h | Deliverable: docs/incident-response.md

4.2.8 Create FAQ (50+ common questions + answers)
      Owner: DevOps | Effort: 6h | Deliverable: docs/FAQ.md
```

**Definition of Done:**
- [ ] 7 runbooks covering all major operations
- [ ] Incident response playbook for 10+ common failure modes
- [ ] All runbooks tested (brand team can execute without help)
- [ ] FAQ addresses 80%+ of common issues

---

### Initiative 4.3: Testing & Quality Assurance (Weeks 32-40)

**Issue:** `ZELEX-QA-001` — Comprehensive testing + quality gates  
**Effort:** 60h (QA 50h + FE 10h)  
**Dependencies:** All Phase 1-3 complete

**Breakdown:**

```
4.3.1 Create end-to-end test suite (Cypress/Playwright) for all key flows
      Owner: QA | Effort: 20h | Deliverable: e2e test suite

4.3.2 Create visual regression test suite (Percy/Chromatic, all pages)
      Owner: QA | Effort: 12h | Deliverable: visual regression baseline

4.3.3 Create accessibility audit suite (axe-core, all pages)
      Owner: QA | Effort: 10h | Deliverable: a11y test suite

4.3.4 Create performance benchmark suite (LCP, CLS, FID, TTL)
      Owner: QA | Effort: 8h | Deliverable: perf benchmark script

4.3.5 Integrate all test suites into CI (run on every PR)
      Owner: QA | Effort: 6h | Deliverable: updated .github/workflows/ci.yml

4.3.6 Document testing strategy + coverage targets
      Owner: QA | Effort: 4h | Deliverable: docs/testing-strategy.md
```

**Definition of Done:**
- [ ] E2E test coverage: 100% of conversion flows
- [ ] Visual regression: all pages baselined
- [ ] Accessibility: WCAG AA compliance verified on all pages
- [ ] Performance: benchmark targets defined + CI gates enabled
- [ ] Test coverage: >90% of critical paths

---

### Initiative 4.4: Documentation & Knowledge Transfer (Weeks 40-44)

**Issue:** `ZELEX-DEVEX-003` — Complete documentation handoff  
**Effort:** 40h (DevOps 30h + Platform 10h)  
**Dependencies:** All Phase 1-4 initiatives complete

**Breakdown:**

```
4.4.1 Create Architecture Overview document (systems, data flow, dependencies)
      Owner: Platform | Effort: 8h | Deliverable: docs/ARCHITECTURE.md

4.4.2 Create Data Schema documentation (all JSON structures, database schema)
      Owner: Platform | Effort: 8h | Deliverable: docs/DATA-SCHEMA.md

4.4.3 Create API documentation (all build scripts, endpoints, options)
      Owner: Platform | Effort: 6h | Deliverable: docs/API.md

4.4.4 Create Glossary (body family definitions, character types, technical terms)
      Owner: DevOps | Effort: 4h | Deliverable: docs/GLOSSARY.md

4.4.5 Create Decision Log (rationale for architectural choices)
      Owner: Platform | Effort: 4h | Deliverable: docs/DECISIONS.md

4.4.6 Update README.md to reflect all Phase 1-4 changes
      Owner: DevOps | Effort: 4h | Deliverable: updated README.md

4.4.7 Create migration guide (PDR-011 changes, how old docs map to new)
      Owner: DevOps | Effort: 6h | Deliverable: docs/MIGRATION-GUIDE.md
```

**Definition of Done:**
- [ ] All documentation linked from README.md + CONTRIBUTING.md
- [ ] Architecture overview complete + reviewed
- [ ] API documentation 100% coverage
- [ ] Glossary covers all domain terms
- [ ] Knowledge transfer test: brand team can execute all runbooks

---

### Initiative 4.5: Handoff & Operations (Weeks 44-52)

**Issue:** `ZELEX-OPS-004` — Transition to brand team operations  
**Effort:** 40h (DevOps 30h, Platform 10h)  
**Dependencies:** All Phase 1-4 complete

**Breakdown:**

```
4.5.1 Establish on-call rotation + escalation path
      Owner: DevOps | Effort: 4h | Deliverable: on-call-rotation.md

4.5.2 Create support ticket template + triage process
      Owner: DevOps | Effort: 4h | Deliverable: support-template.md

4.5.3 Setup monitoring + alerting (Sentry, uptime checks, build status)
      Owner: DevOps | Effort: 8h | Deliverable: monitoring-config

4.5.4 Train brand team (architecture, operations, incident response)
      Owner: DevOps + Platform | Effort: 12h | Deliverable: training-materials + certificates

4.5.5 Establish SLA + performance targets
      Owner: DevOps | Effort: 4h | Deliverable: SLA.md

4.5.6 Quarterly review + optimization roadmap
      Owner: Platform | Effort: 8h | Deliverable: quarterly-review.md

4.5.7 Archive old documentation + transition to brand team ownership
      Owner: DevOps | Effort: 4h | Deliverable: documentation-archive
```

**Definition of Done:**
- [ ] On-call rotation established + tested
- [ ] Brand team trained + signed off
- [ ] Monitoring + alerting live + tested
- [ ] Support process documented + tested
- [ ] SLA targets defined + tracked
- [ ] Quarterly review cadence established

---

### Phase 4 Success Criteria

**Must Complete:**
- [x] Local setup: <5min (fully automated)
- [x] Contributor onboarding: <1h
- [x] 7+ runbooks covering all major operations
- [x] E2E test coverage: 100% of conversion flows
- [x] Complete documentation (architecture, API, glossary, decisions)
- [x] Brand team trained + signed off
- [x] SLA established + targets met

**Success Metrics:**
- Setup time: <5min (vs. 30min baseline)
- Contributor onboarding: <1h (vs. 2h+ baseline)
- Incident MTTR: <30min (with runbooks)
- Team satisfaction: 4.5/5 (documentation + tools)

**Phase 4 Gate:** All success criteria met + brand team fully trained + operations stable

---

## Implementation Timeline (Gantt Overview)

```
Q3 2026 (Weeks 1-13)
├─ Phase 1: Foundation (Weeks 1-6)
│  ├─ 1.1: Design Tokens (W1-2, FE)
│  ├─ 1.2: Component Storybook (W1-3, FE)
│  ├─ 1.3: Image CDN (W2-4, DevOps)
│  ├─ 1.4: Pipeline Parallelization (W3-4, Platform)
│  ├─ 1.5: GTM + GA4 (W2-5, Analytics + FE)
│  ├─ 1.6: Analytics Dashboard (W5-6, Analytics)
│  └─ 1.7: Documentation (W4-6, DevOps)
│
└─ Phase 2 Start (W7+)

Q4 2026 (Weeks 7-26)
├─ Phase 2: Personalization (Weeks 7-14)
│  ├─ 2.1: Shopify Sync (W7-10, Platform + DevOps)
│  ├─ 2.2: Quiz Recommendations (W8-11, FE + Platform)
│  ├─ 2.3: Intake Form Optimization (W9-12, FE + Analytics)
│  └─ 2.4: Funnel Optimization (W10-14, Analytics + FE)
│
└─ Phase 3 Start (W15+)

Q1 2027 (Weeks 15-26)
├─ Phase 3: Scaling (Weeks 15-24)
│  ├─ 3.1: Fragment Library (W15-17, FE + Platform)
│  ├─ 3.2: Page Generation (W16-18, Platform + FE)
│  ├─ 3.3: Component Consolidation (W18-20, FE + QA)
│  ├─ 3.4: Community Hub (W19-24, FE + Platform)
│  └─ 3.5: Performance Optimization (W22-24, FE + DevOps)
│
└─ Phase 4 Start (W25+)

Q2 2027 (Weeks 25-26)
└─ Phase 4: Optimization & Handoff (Weeks 25-52, Ongoing)
   ├─ 4.1: Developer Experience (W25-28, DevOps + FE)
   ├─ 4.2: Runbooks & Incident Response (W28-32, DevOps + Platform)
   ├─ 4.3: Testing & QA (W32-40, QA + FE)
   ├─ 4.4: Documentation (W40-44, DevOps + Platform)
   └─ 4.5: Handoff & Operations (W44-52, DevOps + Platform)
```

---

## Resource Allocation

### Team Composition

| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Notes |
|---|---|---|---|---|---|
| Platform Lead | 0.5 FTE | 0.75 FTE | 0.5 FTE | 0.25 FTE | Architecture, orchestration |
| Frontend Lead | 0.5 FTE | 0.5 FTE | 1.0 FTE | 0.25 FTE | UI, components, quiz |
| DevOps Lead | 0.5 FTE | 0.5 FTE | 0.25 FTE | 0.5 FTE | Infrastructure, CDN, monitoring |
| Analytics Lead | 0.75 FTE | 0.75 FTE | — | — | GTM, GA4, funnels |
| FE Contractor | 0.5 FTE | — | 0.5 FTE | — | Token work, testing |
| QA Lead | — | — | 0.5 FTE | 0.75 FTE | Regression testing |

**Total:** 3.75 FTE (Phase 1) → 4.0 FTE (Phase 2-3) → 1.75 FTE (Phase 4)

---

## Success Criteria Checklist

### Phase 1 ✅
- [ ] Design tokens: 100% coverage, CSS 647 → 350 lines
- [ ] Component Storybook: all components documented
- [ ] Image CDN: operational, manifest versioned
- [ ] Build pipeline: <1min, parallelized, retry logic
- [ ] GA4 + GTM: all events firing, PII scrubbed
- [ ] Analytics dashboard: live, refreshing daily
- [ ] Documentation: all runbooks written, team trained
- **Exit Gate:** Leadership sign-off + CI >98% pass rate

### Phase 2 ✅
- [ ] Shopify sync: automated, <30min latency
- [ ] Quiz recommendations: 85%+ accuracy, +30% form submission
- [ ] Premium intake form: optimized, pre-fill working, +30% conversion
- [ ] Funnel analysis: complete, drop-off points identified
- [ ] GA4 tracking: 100% event coverage, data quality 99%+
- **Exit Gate:** Conversion metrics met + leadership sign-off

### Phase 3 ✅
- [ ] Fragment library: 15+ fragments, documented
- [ ] Page generation: 41 pages → schema, zero regressions
- [ ] HTML pages: 41 → 15 hand-coded
- [ ] CSS bundle: 350 → 250 lines
- [ ] Components: 30+ variants → 10 consolidated
- [ ] Community hub: 100+ submissions/month
- [ ] Performance: Lighthouse >90 all pages
- **Exit Gate:** Lighthouse scores verified + community hub stable

### Phase 4 ✅
- [ ] Setup: <5min (automated)
- [ ] Onboarding: <1h
- [ ] 7+ runbooks complete + tested
- [ ] E2E test coverage: 100%
- [ ] Complete documentation (architecture, API, glossary)
- [ ] Brand team trained + signed off
- [ ] SLA established + targets met
- **Exit Gate:** Full handoff to brand team operations

---

## Risk Management

| Risk | Probability | Impact | Mitigation | Owner |
|---|---|---|---|---|
| CSS refactor regressions | High | High | Pixel-perfect testing (Percy), 48h QA review | FE |
| CDN regional latency | Medium | Medium | Multi-region failover, fallback to git images | DevOps |
| PII leak in GA4 events | Low | Critical | Legal review, audit GTM dataLayer before wiring | Analytics |
| Shopify API changes | Low | Medium | Version-lock SDK, 6-month compatibility buffer | Platform |
| Build pipeline parallelization failures | Medium | High | Comprehensive testing, robust error handling | Platform |
| Community spam/moderation overhead | Medium | Medium | Moderation queue, auto-filter rules, brand team training | FE |
| Team capacity constraints | High | High | Hire contractor for Phase 2, prioritize Phase 1 foundation | Manager |

---

## Success Metrics Summary

### Business Metrics (Quarterly)
- **Revenue funnel:** Quiz start → inquiry → premium intake form (conversion rate +50%)
- **Community engagement:** Gallery submissions, event attendance, reviews posted
- **Competitive positioning:** Family coverage vs. competitors, SEO ranking improvement
- **Operational efficiency:** Build time, deployment frequency, incident MTTR

### Technical Metrics (Weekly)
- **Code quality:** CI pass rate >98%, test coverage >90%
- **Performance:** Lighthouse >90, LCP <2.5s, CLS <0.1
- **Analytics:** Event coverage 100%, data quality 99%+, latency <24h

### Team Metrics (Monthly)
- **Developer satisfaction:** 4+/5 (tools, docs, onboarding)
- **Time to contribute:** <1h onboarding, <30min first change
- **Incident handling:** MTTR <30min, resolution rate 95%+

---

## Next Steps (Week 1 Actions)

1. **Kickoff meeting** — All stakeholders, approve mission pack + PDR
2. **Resource confirmation** — Secure FTE commitments for Phase 1
3. **Create issues** — Breakdown all initiatives into bd (beads) issues
4. **Setup tracking** — Create Gantt chart in project management tool
5. **Begin Phase 1 Week 1** — Design tokens audit starts immediately

---

## Approval & Sign-Off

- [ ] Brand Lead (HowieZZ)
- [ ] Platform Engineering Lead
- [ ] Frontend Engineering Lead
- [ ] DevOps / Ops Lead
- [ ] Analytics Lead
- [ ] Product Lead

**Approved:** ________________  
**Date:** ________________  
**Review Cadence:** Weekly standup (Fridays 4pm) + bi-weekly leadership review

