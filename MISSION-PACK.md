# ZELEX Character Atlas — Mission Pack

**Version:** 1.0  
**Date:** 2026-06-21  
**Scope:** Atlas platform scaling, operational resilience, revenue acceleration  
**Approver:** HowieZZ Brand Team

---

## Executive Summary

ZELEX Character Atlas is at an inflection point. The current static site (41 HTML pages, vanilla stack) successfully showcases 6 body families + ~60 characters with robust data architecture. However, **scaling beyond this point requires architectural investment** to unlock:

1. **Revenue acceleration** — Real-time personalization, Shopify sync, premium intake forms
2. **Operational resilience** — Decouple images from git, parallel pipeline builds, asset versioning
3. **Team scaling** — Component abstraction, design tokens, contributor-friendly workflows
4. **Competitive positioning** — Analytics, SEO optimization, community-driven differentiation

**This mission pack outlines the path to 10x the platform without 10x the overhead.**

---

## Strategic Goals (12-month horizon)

### Goal 1: Unlock Revenue Streams
**Target:** $2M incremental GMV through premium customization + concierge pipeline  
**KPIs:**
- Quiz-to-inquiry conversion rate: 12% → 18%
- Configurator engagement: <5% → 25%
- Premium intake form qualification: 40% → 60%

**Initiatives:**
- [ ] Wire GTM + GA4 to measure quiz-to-inquiry flow
- [ ] Cross-link quiz, configurator, and concierge forms from homepage
- [ ] Build live-update Shopify sync (product catalog → atlas updates)
- [ ] A/B test hero variants (2 planned, need testing infrastructure)

---

### Goal 2: Operational Resilience
**Target:** Zero-downtime deployments, reliable builds, versioned assets  
**KPIs:**
- Build failure recovery time: 1h → 5min (automated retry/resume)
- Image sync consistency: 100% (manifest-based versioning)
- Unplanned downtime: 2h/year → 0h

**Initiatives:**
- [ ] Implement design token system (CSS custom properties)
- [ ] Decouple images from git (CDN + asset manifest)
- [ ] Add retry/resume logic to Python pipeline
- [ ] Automate image freshness checks in CI

---

### Goal 3: Scalable Architecture
**Target:** Support 12+ body families, 200+ characters, with <20% development overhead  
**KPIs:**
- HTML page count: 41 → 15 (template reuse)
- CSS file size: 647 lines → 300 lines + tokens
- Curation time per character: 2h → 30min (guided UX)

**Initiatives:**
- [ ] Extract card/grid/section components into reusable fragments
- [ ] Build component library + design token storybook
- [ ] Automate character curation workflow (story templates, image pre-selection)
- [ ] Implement data-driven page generation (fewer static HTML files)

---

### Goal 4: Competitive Differentiation
**Target:** Own luxury body-type positioning; capture affiliate/retail partnerships  
**KPIs:**
- Organic search traffic: +50% (SEO optimization)
- Competitor coverage parity: 6/10 → 9/10 families
- Community submissions: 0 → 200+ (user galleries)

**Initiatives:**
- [ ] Publish competitive positioning dashboard (leadership tool)
- [ ] Implement structured data for search (family, body, character schema)
- [ ] Launch community hub features (user-generated galleries, events)
- [ ] Create affiliate/retail partner program (bulk inquiry routing)

---

## Phasing Strategy

### Phase 1: Foundation (Q3 2026, 6 weeks)
**Objective:** Build automation, observability, and component infrastructure  
**Deliverables:**
- Design token system + Storybook component library
- GTM + GA4 wiring, analytics dashboard
- Image CDN + asset manifest versioning
- Python pipeline retry/resume + parallel builds
- Pre-built issue templates + contribution guide refresh

**Success Metrics:**
- CI pass rate: >98%
- Build time: <5min (target: 3min)
- Analytics coverage: 100% of key flows tracked

**Effort:** 240 person-hours (6 weeks × 1 FTE + 0.5 FTE support)

---

### Phase 2: Personalization & Commerce (Q4 2026, 8 weeks)
**Objective:** Wire Shopify sync, unlock premium intake flows  
**Deliverables:**
- Shopify product feed → catalog.json automation
- Premium intake form integration (Formspree/Getform)
- Quiz-to-recommendation engine (edge function)
- Real-time configurator state persistence
- A/B testing infrastructure (hero variants, CTA copy)

**Success Metrics:**
- Shopify sync latency: <30min
- Intake form conversion: +50% (from baseline)
- Quiz engagement: 25%+ of site visitors

**Effort:** 320 person-hours (8 weeks × 1.5 FTE)

---

### Phase 3: Scaling & Community (Q1 2027, 10 weeks)
**Objective:** Prepare for 12+ body families, launch community features  
**Deliverables:**
- Refactored page structure (41 → 15 HTML files via templating)
- Component reusability audit + modernization
- Community hub (events, user galleries, reviews)
- Competitive positioning dashboard (live, leadership-facing)
- Bulk inquiry + affiliate routing system

**Success Metrics:**
- CSS + JS bundle size: -40% reduction
- New character onboarding time: 2h → 30min
- Community submissions: 100+ galleries/month

**Effort:** 400 person-hours (10 weeks × 1.5 FTE)

---

### Phase 4: Optimization & Handoff (Q2 2027, ongoing)
**Objective:** Polish, handoff to brand team, establish runbooks  
**Deliverables:**
- Performance optimization (LCP, CLS targets)
- SEO audit + structured data enhancement
- Runbooks: image refresh, curation workflow, incident response
- Developer experience: local setup <5min, contributor onboarding <1h
- Documentation: API, schema, data pipeline, deployment

**Success Metrics:**
- Lighthouse: >90 across all pages
- Contributor setup time: <5min
- Runbook coverage: 100% of common operations

**Effort:** Ongoing (0.5 FTE QA + 0.25 FTE ops)

---

## Budget & Resource Model

| Phase | Duration | FTE | Estimated Cost | Funding |
|---|---|---|---|---|
| Phase 1 | 6 weeks | 1.0 + 0.5 support | $45K | Q3 roadmap |
| Phase 2 | 8 weeks | 1.5 FTE | $60K | Q4 roadmap |
| Phase 3 | 10 weeks | 1.5 FTE | $75K | Q1 roadmap |
| Phase 4 | Ongoing | 0.75 FTE | $36K/quarter | Operational budget |
| **Total Year 1** | — | — | **$216K** | — |

**FTE roles required:**
- 1 Platform Engineer (full time, all phases)
- 1 Frontend Engineer (Q2-Q3)
- 1 Product/Data Analyst (Q3-Q4, ongoing)
- 1 DevOps/Ops (Phase 1, Phase 4 ongoing)

---

## Success Criteria & Guardrails

### Must-Have (Phase 1)
- [ ] Design tokens defined + applied to 100% of components
- [ ] GA4 + GTM wired, revenue-funnel events firing
- [ ] Image CDN live, manifest versioning in CI
- [ ] Python pipeline 100% retry-safe (idempotent builds)

### Should-Have (Phase 2-3)
- [ ] Shopify sync operational (auto-updates on feed change)
- [ ] Quiz-to-inquiry conversion +50%
- [ ] New character curation time <1h (was 2h)
- [ ] HTML page count <20 (was 41)

### Nice-to-Have (Phase 4)
- [ ] Community hub with 100+ user submissions
- [ ] Affiliate partner dashboard (analytics for partners)
- [ ] Mobile app companion (wishlist, saved configurator states)

### Guardrails (Non-negotiables)
- ✅ Zero regression: All existing flows tested, no broken pages
- ✅ Performance: LCP <2.5s, CLS <0.1 (target Lighthouse >90)
- ✅ Privacy: No analytics code bloat, GDPR-compliant cookie handling
- ✅ Brand compliance: No external CDN for core assets (keep control)

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Image CDN latency (regional) | Medium | High | Multi-region CDN, fallback to git-hosted for low-traffic regions |
| Shopify API changes | Low | Medium | Version-lock Shopify SDK, maintain 6-month compatibility buffer |
| Team capacity constraints | Medium | High | Hire contract backend engineer for Phase 2; prioritize Phase 1 foundation |
| Analytics PII leak (GTM misconfiguration) | Low | Critical | Audit GTM dataLayer before GA4 wiring; legal review of data consent |
| Build pipeline failure during scale | Medium | High | Implement robust error handling, parallel builds, asset caching |

---

## Decision Log

| Date | Decision | Rationale | Owner |
|---|---|---|---|
| 2026-06-21 | Use design tokens over CSS preprocessor | Vanilla CSS stack, easier to audit + maintain | Platform |
| 2026-06-21 | Shopify sync via product feed, not direct API | Decoupled, easier to test + version | Product |
| 2026-06-21 | Community hub in Phase 3, not Phase 2 | Phase 2 focused on revenue (quiz + intake); community is engagement |  Product |
| 2026-06-21 | Keep image storage separate (CDN) | Static site limitation; images too large for git, need independent versioning | Ops |

---

## Appendix: PDR & Issue Index

**Strategic PDRs:**
- [PDR-011: SWOT Resolution & Platform Scaling](docs/pdr/PDR-011-SWOT-resolution-platform-scaling.md)
- [PDR-100: Design Token System v1](docs/pdr/PDR-100-design-token-system.md)
- [PDR-101: Analytics Stack Wiring (GTM + GA4)](docs/pdr/PDR-101-analytics-stack-wiring.md)
- [PDR-102: Image CDN & Asset Versioning](docs/pdr/PDR-102-image-cdn-asset-versioning.md)
- [PDR-103: Shopify Sync Automation](docs/pdr/PDR-103-shopify-sync-automation.md)

**Tracking:** All work tracked in [bd (beads) issue system](CLAUDE.md#beads-issue-tracker). Start with `bd ready` to see available work.

---

## Approval & Sign-Off

- [ ] Brand Lead (HowieZZ)
- [ ] Platform Engineering Lead
- [ ] Product Lead (Revenue goals)
- [ ] Ops Lead (Infrastructure)

**Approved:** ________________  
**Date:** ________________

