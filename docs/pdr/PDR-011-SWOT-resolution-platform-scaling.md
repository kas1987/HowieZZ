# PDR-011: SWOT Resolution & Platform Scaling

**Status:** In Planning  
**Phase:** Foundation (Phase 1, Q3 2026)  
**Epic:** Platform resilience & revenue acceleration  
**Effort:** 240 person-hours (6 weeks)

---

## Overview

This PDR addresses all critical SWOT findings from the June 2026 repository audit:

| Quadrant | Issue | Resolution |
|---|---|---|
| **Weakness** | 41 HTML pages → maintenance burden | Phase 3: Component abstraction, template reuse |
| **Weakness** | 647-line monolithic CSS | Phase 1: Design token system + CSS refactor |
| **Weakness** | Single-threaded Python pipeline | Phase 1: Parallel builds + retry/resume logic |
| **Weakness** | Image storage outside git → sync friction | Phase 1: CDN + asset manifest versioning |
| **Threat** | Technical debt (no A/B testing infrastructure) | Phase 2: Multi-variant support + analytics |
| **Threat** | No personalization (static site limits conversion) | Phase 2: Edge function for quiz recommendations |
| **Threat** | Operational fragility (image + pipeline sync failures) | Phase 1: Automated freshness checks, CI guards |
| **Opportunity** | Untapped analytics (GA4 ready but not wired) | Phase 1: GTM dataLayer + GA4 integration |
| **Opportunity** | Shopify integration roadmap | Phase 2: Product feed → catalog.json sync |
| **Opportunity** | Underutilized community features | Phase 3: Community hub (galleries, events) |

---

## Strategic Pillars

### Pillar 1: Automation & Resilience (Phase 1, Weeks 1-6)

**Goal:** Eliminate manual toil, make builds bulletproof, empower async operations

#### 1.1 Design Token System
**Problem:** Single 647-line CSS file couples styling across 41 pages. Any design change touches ~50 lines across multiple files.

**Solution:** Define semantic token layer in `:root`, refactor site.css into token definitions + component styles.

**Deliverables:**
- [ ] `assets/site-tokens.css` (80 lines) — all variables for color, spacing, type, shadows, etc.
- [ ] Refactored `assets/site.css` (350 lines) — components reference tokens only
- [ ] Token documentation in `docs/design-tokens.md`
- [ ] Storybook-style component guide in `docs/component-library.md`

**Success Metrics:**
- CSS file size: 647 → 350 lines (46% reduction)
- Design change velocity: 30min per change → 5min (80% faster)
- Token coverage: 100% of color, spacing, type, and shadow usage

**Acceptance Criteria:**
- [x] All color values use CSS variables (no inline hex codes)
- [x] All spacing uses --sp* tokens (no inline padding/margin px values)
- [x] All shadows use --sh-* tokens
- [x] Token definitions documented in CONTRIBUTING.md
- [x] Zero visual regressions (pixels-match before/after)

---

#### 1.2 Image CDN & Asset Manifest Versioning
**Problem:** 260 MB images stored separately, manual sync needed for packaging. No versioning = risk of deploying with stale images.

**Solution:** CDN-host images with content-hash filenames, maintain manifest.json (image → hash → CDN URL mapping). CI guards verify freshness.

**Deliverables:**
- [ ] Evaluate CDN: Cloudinary, Bunny, or AWS CloudFront (brand compliance: US-hosted only)
- [ ] Upload script (`scripts/push_assets_to_cdn.py`) — batch upload with hash generation
- [ ] Manifest schema (`db/assets_manifest.json`) — records image path, hash, CDN URL, last-updated
- [ ] CI guard (`scripts/validate_manifest_freshness.py`) — fails build if manifest >48h old
- [ ] Image freshness check in pre-push hook

**Success Metrics:**
- Image upload time: <30sec for new batch
- CI manifest validation: 100% of builds checked
- Stale image detection: Zero missed updates

**Acceptance Criteria:**
- [x] CDN images load in <500ms (global latency)
- [x] Manifest schema defined and validated
- [x] Build fails if images missing from CDN
- [x] Rollback: old image versions retrievable from CDN history
- [x] Documentation: image refresh workflow in CONTRIBUTING.md

---

#### 1.3 Python Pipeline Parallelization & Retry
**Problem:** Sequential 6-step pipeline fails at any step, no resume. Build times: ~2min, no optimization.

**Solution:** Refactor build scripts to support:
- Parallel stage execution (step 2-3 can run concurrently with 1)
- Idempotent operations (safe to re-run any step)
- Automatic retry + resume (skip already-completed steps)

**Deliverables:**
- [ ] New `scripts/build_orchestrator.py` — coordinates parallel stages
- [ ] Audit each build script for idempotence (no side effects from partial runs)
- [ ] Add build state tracking (`db/.build_state.json`) — logs completed stages
- [ ] Implement retry logic with exponential backoff
- [ ] Add `--resume` flag to continue from last failed step

**Success Metrics:**
- Build time: 2min → <1min (with parallelization)
- Build failure recovery: manual restart → automatic resume
- Pipeline reliability: 95% → 99.5% (fewer transient failures)

**Acceptance Criteria:**
- [x] All build steps are idempotent (safe to re-run)
- [x] `scripts/build_orchestrator.py --resume` skips completed stages
- [x] CI runs orchestrator instead of individual scripts
- [x] Build state persisted across runs
- [x] Documentation: build troubleshooting guide in `docs/pipeline.md`

---

### Pillar 2: Observability & Revenue (Phase 1 + 2, Weeks 2-16)

**Goal:** Measure everything, unlock conversion funnels, prove ROI

#### 2.1 GTM + GA4 Wiring
**Problem:** Site deployed to GitHub Pages with working analytics fixtures, but GTM not configured, GA4 not wired.

**Solution:** Configure GTM container, define dataLayer schema, wire GA4 events for key flows.

**Deliverables:**
- [ ] GTM container created (brand account)
- [ ] `docs/pdr/PDR-101-analytics-stack-wiring.md` — detailed handoff
- [ ] dataLayer schema defined (`docs/analytics-datalayer-schema.md`)
- [ ] Event tracking implemented:
  - [ ] Quiz start/completion/result-view
  - [ ] Configurator load/interaction/save
  - [ ] Contact form: start/prefill/submit
  - [ ] Character detail: view, gallery-scroll, related-click
  - [ ] Comparison tool: bodies-selected, share-clicked
- [ ] GA4 custom events + dimensions configured
- [ ] Conversion funnels: Quiz → Inquiry → Lead Qualification
- [ ] Analytics dashboard (Looker Studio template)

**Success Metrics:**
- Event coverage: 100% of conversion-path flows tracked
- Data latency: <24h (real-time events preferred)
- Funnel visibility: Quiz start → Inquiry submit, with drop-off analysis

**Acceptance Criteria:**
- [x] GTM container deployed to all pages
- [x] dataLayer firing on all tracked events
- [x] GA4 events match schema specification
- [x] PII scrubbing verified (no email/phone in events)
- [x] Analytics dashboard live for leadership review
- [x] Documentation: GTM troubleshooting + event audit in CONTRIBUTING.md

---

#### 2.2 Analytics Dashboard (Leadership Visibility)
**Problem:** Competitive analysis data exists (PDR-010) but not live. No dashboard for leadership to track positioning progress.

**Solution:** Build Looker Studio dashboard pulling GA4 + competitor analysis JSON.

**Deliverables:**
- [ ] Looker Studio template: "ZELEX Atlas — Competitive Positioning & Conversion Funnel"
  - [ ] Competitor coverage heatmap (6 families, 10 competitors, coverage %)
  - [ ] Conversion funnel (Quiz → Inquiry → Premium intake)
  - [ ] Traffic source breakdown (organic, direct, referral)
  - [ ] Engagement by family (which bodies drive most traffic?)
- [ ] Scheduled refresh (GA4 → dashboard, daily)
- [ ] Embed link in `docs/analytics-dashboard-link.md`

**Success Metrics:**
- Dashboard updated daily
- Leadership uses it for weekly sprint planning
- Competitive gaps identified and prioritized

**Acceptance Criteria:**
- [x] Dashboard accessible to brand team
- [x] Data refreshes automatically (no manual pulls)
- [x] All metrics explained in dashboard legend
- [x] Trend analysis enabled (month-over-month comparison)

---

### Pillar 3: Personalization & Commerce (Phase 2, Weeks 7-16)

**Goal:** Convert site visitors into premium customers, automate product updates

#### 3.1 Shopify Sync Automation
**Problem:** Live product feed exists, but no automation to update catalog.json when products change.

**Solution:** Scheduled job pulls Shopify product feed, compares against catalog.db, auto-generates catalog.json updates.

**Deliverables:**
- [ ] `scripts/sync_shopify_feed.py` — fetch live products, map SKU → body architecture
- [ ] Mapping table: `db/shopify_sku_mapping.json` (manual: which SKU = which body)
- [ ] Scheduler (GitHub Actions or AWS Lambda): runs every 6 hours
- [ ] Diff detection: new products, price changes, stock status
- [ ] Auto-commit + PR workflow (human approval before merging)
- [ ] Documentation: setup runbook in `docs/shopify-sync.md`

**Success Metrics:**
- Sync latency: <30min (product change → atlas updated)
- Accuracy: 100% of in-stock products reflected in catalog
- Operational overhead: <5min per week (fully automated)

**Acceptance Criteria:**
- [x] Shopify API credentials stored securely (no hardcoded secrets)
- [x] Sync is idempotent (safe to run multiple times)
- [x] SKU mapping auditable and versioned
- [x] Failed syncs trigger alerts (Slack webhook)
- [x] Rollback procedure documented

---

#### 3.2 Quiz-to-Recommendation Engine
**Problem:** Quiz renders results, but doesn't route to personalized character recommendations or drive form prefill.

**Solution:** Edge function (Vercel or Netlify) receives quiz response, returns personalized recommendation + prefilled contact form.

**Deliverables:**
- [ ] Quiz result flow redesign (PDR-FE-005 follow-up)
- [ ] Edge function: recommend 3-4 characters based on quiz response
- [ ] Pre-fill contact form with recommended body + character
- [ ] Track quiz-to-form conversion in GA4
- [ ] A/B test: standard results vs. personalized recommendations (uplift target: +30%)

**Success Metrics:**
- Quiz-to-form submission rate: +30% (with personalization)
- Average recommendation accuracy: 85%+ (user satisfaction survey)
- Conversion funnel: Quiz → Inquiry (+50%)

**Acceptance Criteria:**
- [x] Recommendation logic tested against 100+ quiz responses
- [x] Recommended characters load >90% of the time
- [x] Fallback: if edge function unavailable, render standard results
- [x] A/B test results documented

---

### Pillar 4: Scaling & Modernization (Phase 3, Weeks 17-26)

**Goal:** Support 12+ body families without proportional overhead increase

#### 4.1 HTML Refactoring: Template Fragments
**Problem:** 41 HTML pages, ~70% code duplication (header, nav, footer, card templates).

**Solution:** Extract reusable fragments (.html template partials), generate pages from schema.

**Deliverables:**
- [ ] Fragment library:
  - [ ] `fragments/header.html`
  - [ ] `fragments/nav.html`
  - [ ] `fragments/footer.html`
  - [ ] `fragments/char-card.html`
  - [ ] `fragments/body-card.html`
  - [ ] `fragments/family-grid.html`
  - [ ] `fragments/contact-form.html` (with prefill variants)
- [ ] Build script: `scripts/generate_pages_from_schema.py` — generates pages from JSON config
- [ ] Page schema: `db/pages_config.json` — defines which fragments + data for each page
- [ ] Result: 41 pages → 15 hand-authored pages + 26 generated from schema

**Success Metrics:**
- HTML page count: 41 → 15 (hand-coded)
- Template reuse: >80% of markup is fragment-based
- Code duplication: 70% → <15%
- Time to add new character: 2h → 30min

**Acceptance Criteria:**
- [x] Fragment syntax is familiar (standard HTML + \`\{\{var\}\}\` substitution)
- [x] All 41 current pages regenerated without regressions
- [x] Build process is fully automated
- [x] Schema is human-readable and versioned

---

#### 4.2 CSS Modernization & Component Storybook
**Problem:** Design tokens exist, but no central catalog of components. Developers can't see all variants.

**Solution:** Build Storybook-style component reference (static HTML pages, not Node.js dependency).

**Deliverables:**
- [ ] `docs/component-storybook.html` — interactive component showcase
  - [ ] Buttons (4 variants: primary, secondary, ghost, concierge)
  - [ ] Cards (character, body, comparison)
  - [ ] Grids (browse layout, family grid, quiz results)
  - [ ] Forms (contact, intake, search)
  - [ ] Modals (confirmation, imagery viewer)
  - [ ] Status badges (live, concept, pending, verified)
  - [ ] Accessibility: dark mode, reduced motion, focus states
- [ ] Each component shows: markup, CSS, usage guidelines, accessibility notes
- [ ] Link from CONTRIBUTING.md

**Success Metrics:**
- Component coverage: 100% of site.css components documented
- Contributor time to find component: <2min (vs. 15min grepping code)
- Design consistency: all new pages use component library

**Acceptance Criteria:**
- [x] Storybook is a static HTML file (no build dependencies)
- [x] Every component has accessible markup examples
- [x] All token variations shown (e.g., all button sizes + states)

---

#### 4.3 Component Audit & Modernization
**Problem:** Cards and grids scattered across 41 pages, inconsistent styling.

**Solution:** Audit all components, standardize, consolidate duplicates.

**Deliverables:**
- [ ] Component inventory:
  - [ ] Character card (9 variants: featured, grid, mini, with/without hover, etc.) → standardize to 3
  - [ ] Body card (6 variants) → 2
  - [ ] Comparison grid (4 layouts) → 1
  - [ ] Contact form (3 variants) → 1
- [ ] Consolidation plan: which pages can share a component
- [ ] Refactored CSS: eliminate variant-specific overrides
- [ ] Result: CSS size further reduced, consistency increased

**Success Metrics:**
- Component variants: 30+ → 10 (eliminate redundancy)
- CSS specificity (max depth): 5+ → 3 (flatter hierarchy)
- Visual regression tests: 100% pass

**Acceptance Criteria:**
- [x] Consolidation audit documented in `docs/component-audit.md`
- [x] Zero visual regressions across all pages
- [x] CSS maintainability improved (lower specificity, fewer overrides)

---

#### 4.4 Community Hub Launch
**Problem:** Community channel data exists, but no user-facing features (galleries, events, reviews).

**Solution:** Launch community hub pages + submission workflow.

**Deliverables:**
- [ ] `community.html` redesign — hub landing with 4 sections
  - [ ] User galleries (submitted photos of ZELEX dolls)
  - [ ] Events (community meetups, photoshoots)
  - [ ] Reviews & testimonials (ZELEX ownership stories)
  - [ ] Partner links (forums, Discord, Reddit)
- [ ] User gallery submission form (Formspree + moderation queue)
- [ ] Gallery grid with filtering (by family, by contributor)
- [ ] Events calendar (iCal feed for integration)
- [ ] Moderation dashboard (brand team reviews submissions)

**Success Metrics:**
- Community submissions: 0 → 100+/month
- Gallery page engagement: 10%+ of site visitors
- User-generated content on homepage: 20% of featured content

**Acceptance Criteria:**
- [x] Submission workflow tested end-to-end
- [x] Moderation queue functional
- [x] Gallery pages SEO-optimized (schema markup for collections)

---

## Implementation Roadmap

### Timeline (Phase 1: Foundation, 6 weeks)

| Week | Deliverable | Owner | Status |
|---|---|---|---|
| 1 | Design token system defined + refactored | FE | 🔴 Backlog |
| 2 | CSS refactor complete, zero regressions tested | FE | 🔴 Backlog |
| 3 | CDN evaluation + image upload script | DevOps | 🔴 Backlog |
| 3 | Manifest schema + CI guard implementation | DevOps | 🔴 Backlog |
| 4 | Python pipeline parallelization complete | Platform | 🔴 Backlog |
| 4 | Build state tracking + resume logic | Platform | 🔴 Backlog |
| 5 | GTM container + dataLayer schema finalized | Analytics | 🔴 Backlog |
| 5 | Event tracking implemented (quiz, form, character) | FE + Analytics | 🔴 Backlog |
| 6 | Analytics dashboard live (Looker Studio) | Analytics | 🔴 Backlog |
| 6 | Documentation + runbooks complete | DevOps | 🔴 Backlog |

### Timeline (Phase 2: Personalization, 8 weeks)

| Week | Deliverable | Owner | Status |
|---|---|---|---|
| 1-2 | Shopify sync script + mapping table | Platform | 🔴 Backlog |
| 2-3 | GitHub Actions scheduler configured | DevOps | 🔴 Backlog |
| 3-4 | Quiz-to-recommendation edge function | FE | 🔴 Backlog |
| 4-5 | A/B test infrastructure (multi-variant quiz results) | FE + Analytics | 🔴 Backlog |
| 5-6 | Premium intake form optimization (PDR-FE-006 refresh) | FE | 🔴 Backlog |
| 6-7 | Conversion funnel analysis + optimization | Analytics | 🔴 Backlog |
| 7-8 | Documentation + training for brand team | DevOps + Product | 🔴 Backlog |

### Timeline (Phase 3: Scaling, 10 weeks)

| Week | Deliverable | Owner | Status |
|---|---|---|---|
| 1-2 | Fragment library extracted + documented | FE | 🔴 Backlog |
| 2-3 | Page schema + generation script | Platform | 🔴 Backlog |
| 3-4 | Component Storybook built | FE | 🔴 Backlog |
| 4-5 | Component audit + consolidation | FE | 🔴 Backlog |
| 5-6 | HTML refactoring complete (41 → 15 hand-coded) | FE | 🔴 Backlog |
| 6-7 | Community hub pages + submission workflow | FE | 🔴 Backlog |
| 7-8 | Moderation dashboard + gallery features | Platform + FE | 🔴 Backlog |
| 8-9 | Performance optimization pass (Lighthouse >90) | FE | 🔴 Backlog |
| 9-10 | Full regression testing + launch | QA | 🔴 Backlog |

---

## Dependencies & Risks

### Critical Path Dependencies
1. Design tokens → CSS refactor → component audit (linear)
2. Image CDN upload → manifest versioning → CI guards (linear)
3. GTM wiring → GA4 config → dashboard (linear, can parallelize dashboard design while GA4 wiring is in progress)

### Key Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| CSS refactor introduces visual regressions | High | High | Pixel-perfect testing (Percy or Chromatic), 48h QA review |
| CDN regional latency degrades performance | Medium | Medium | Multi-region failover, fallback to git-hosted images |
| Shopify API rate limiting during sync | Low | Medium | Batch requests, exponential backoff, caching |
| GTM PII leak (email in GA4 events) | Low | Critical | Audit GTM dataLayer before GA4 wiring, legal review |
| Fragment templating introduces edge cases | Medium | High | Comprehensive test coverage (100+ template combinations) |

---

## Success Criteria (Phase 1)

**Must Complete:**
- [x] Design token system deployed (zero visual regressions)
- [x] CSS bundle size: 647 → 350 lines
- [x] Image CDN live with manifest versioning
- [x] Python pipeline parallelized (<1min build time)
- [x] GTM + GA4 wired (100% event coverage)
- [x] Analytics dashboard live (daily refresh)
- [x] All changes pushed, CI passing, documentation complete

**Success Metrics:**
- CI pass rate: >98%
- Build time: <1min (target)
- Analytics data quality: 100% (no PII in events)
- Visual regression rate: 0% (pixel-perfect)
- Team satisfaction: 4/5 (easier builds, clearer docs)

---

## Approval & Sign-Off

- [ ] Platform Lead
- [ ] Frontend Lead
- [ ] Analytics Lead
- [ ] DevOps Lead

**Approved:** ________________  
**Date:** ________________

---

## Related PDRs

- [PDR-001: Luxury Design System v2](PDR-001-luxury-design-system-v2.md) (tokens foundation)
- [PDR-FE-005: Quiz Match Results](PDR-FE-005-quiz-match-results.md) (recommendation UI)
- [PDR-FE-006: Concierge Intake](PDR-FE-006-concierge-intake.md) (premium form optimization)
- [PDR-010: Competitor Lineup Brief](PDR-010-competitor-lineup-brief.md) (dashboard data source)
- [PDR-101: Analytics Stack Wiring](PDR-101-analytics-stack-wiring.md) (detailed GTM/GA4 spec)
- [PDR-102: Image CDN & Asset Versioning](PDR-102-image-cdn-asset-versioning.md) (detailed CDN spec)
- [PDR-103: Shopify Sync Automation](PDR-103-shopify-sync-automation.md) (detailed automation spec)

