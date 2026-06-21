# Phase 1 Kickoff & Team Training Summary

**Event:** Phase 1 Team Training Session  
**Date:** 2026-06-21  
**Duration:** 2 hours  
**Attendees:** Platform, DevOps, Frontend, Analytics, Product  
**Owner:** Howie (CEO) + Engineering Leadership

---

## Overview

Phase 1 ("Foundation") is a 6-week, 240-hour effort to build automation, fix tech debt, and enable observability for the ZELEX Atlas site. All developers and operators need to understand the four key initiatives and their runbooks.

---

## Phase 1 Initiatives (6 weeks)

### Initiative 1.1: Design Token System (Weeks 1-2)
**Owner:** Frontend Engineering Lead  
**Status:** In Implementation  

**What it is:**
- Extract all colors, spacing, type scale, shadows into CSS variables
- Simplify `site.css` from 647 → 350 lines
- Enable rapid theme changes and consistency

**Your action:**
1. **Read:** `docs/design-tokens-runbook.md`
2. **Do:** Review current site.css and identify tokens
3. **Test:** Pixel-perfect regression on all 41 pages
4. **Know:** Never use hardcoded colors/spacing in CSS

**Deliverable:** `assets/site.css` (refactored), token documentation

---

### Initiative 1.2: Component Library & Storybook (Weeks 1-3)
**Owner:** Frontend Engineering Lead  
**Status:** In Implementation  

**What it is:**
- Document all button, card, form, and grid components
- Create static HTML Storybook (no build step needed)
- Enable designers and developers to reuse components

**Your action:**
1. **Read:** Component documentation (in Storybook)
2. **Use:** Reference component markup in all pages
3. **Add:** New components to Storybook when created
4. **Test:** All variants (hover, focus, active, dark mode)

**Deliverable:** `docs/component-storybook.html`, linked from CONTRIBUTING.md

---

### Initiative 1.3: Image CDN & Asset Versioning (Weeks 2-4)
**Owner:** DevOps  
**Status:** In Implementation  

**What it is:**
- Host all images on CDN (not in git) with 30-day caching
- Version images via SHA256 hashing and manifest
- Enable fast, reliable image delivery globally

**Your action:**
1. **Read:** `docs/cdn-runbook.md`
2. **Do:** Add new images locally, run pipeline (auto-uploads)
3. **Test:** Verify manifest freshness before push (pre-hook validates)
4. **Know:** All images MUST be in CDN, zero git-hosted images

**Deliverable:** CDN account + manifest (`db/assets_manifest.json`)

---

### Initiative 1.4: Python Pipeline Parallelization (Weeks 3-4)
**Owner:** Platform Engineering  
**Status:** In Implementation  

**What it is:**
- Parallelize 5-stage build pipeline (scan → classify → generate → images → package)
- Add retry logic and resume-from-failure capability
- Reduce build time from 2 minutes → <1 minute

**Your action:**
1. **Read:** `docs/pipeline-runbook.md`
2. **Do:** Run full pipeline: `python scripts/build_orchestrator.py --full`
3. **Test:** Recover from simulated failures using `--resume` flag
4. **Know:** Pipeline is safe to re-run (idempotent)

**Deliverable:** `scripts/build_orchestrator.py`, CI integration

---

### Initiative 1.5: GTM + GA4 Wiring (Weeks 2-5)
**Owner:** Analytics  
**Status:** In Implementation  

**What it is:**
- Wire Google Tag Manager to all pages
- Define 50+ GA4 events (quiz, forms, character detail, comparisons)
- Enable real-time event tracking and funnel analysis

**Your action:**
1. **Read:** `docs/analytics-runbook.md`
2. **Do:** Test events locally using debug mode
3. **Test:** Verify event payload in GA4 Real-time report
4. **Know:** Never send PII (emails, phones) to GA4

**Deliverable:** GTM container + GA4 property configured

---

### Initiative 1.6: Analytics Dashboard (Weeks 5-6)
**Owner:** Analytics  
**Status:** In Implementation  

**What it is:**
- Build Looker Studio dashboard with 4 sections:
  - Traffic baseline
  - Funnel analysis (quiz → inquiry)
  - Engagement by family
  - Competitive positioning
- Leadership visibility into site performance

**Your action:**
1. **Access:** Looker Studio dashboard (shared link in Slack)
2. **Monitor:** Daily dashboard for anomalies
3. **Report:** Funnel drop-off, low traffic to leadership
4. **Know:** Dashboard auto-refreshes daily

**Deliverable:** Looker Studio dashboard (accessible to brand team)

---

### Initiative 1.7: Documentation & Runbooks (Weeks 4-6)
**Owner:** DevOps + Platform Engineering  
**Status:** IN PROGRESS (this session)  

**What it is:**
- Create 4 runbooks (tokens, CDN, pipeline, analytics)
- Write FAQ covering >80% of common issues
- Train team on all Phase 1 tools and workflows
- Update CONTRIBUTING.md with Phase 1 process

**Your action:**
1. **Read:** All 4 runbooks (takes ~30 minutes)
2. **Bookmark:** Runbooks in your IDE/browser
3. **Reference:** Before asking questions
4. **Report:** Missing docs or unclear sections

**Deliverable:** Phase 1 documentation (you're reading it!)

---

## Training: The Runbooks

### 1. Design Tokens Runbook (30 min read)
**File:** `docs/design-tokens-runbook.md`

**Key takeaways:**
- Tokens are CSS variables in `:root`
- Categories: colors, spacing, type, shadows, radius
- Never hardcode pixel values or hex codes
- Always use `var(--token-name)` in CSS
- Search `--color-primary` across codebase to find all uses

**Hands-on task:**
```bash
# Find all uses of a token
grep -r "--sp4" assets/

# Add a new token
# Edit assets/site.css, add to :root section
--my-new-color: #xyz;

# Use in CSS
.button { background: var(--my-new-color); }
```

---

### 2. CDN Runbook (30 min read)
**File:** `docs/cdn-runbook.md`

**Key takeaways:**
- All images hosted on CDN, not in git
- Manifest (`db/assets_manifest.json`) maps local paths → CDN URLs
- Run `push_assets_to_cdn.py --incremental` to upload new images
- Pre-push hook validates manifest freshness (must be <48 hours old)
- Fallback logic: if CDN timeout, load images from git (slow but safe)

**Hands-on task:**
```bash
# Add new images locally
cp new-photos/ assets/characters/[Series]-[Code]/

# Upload to CDN
python scripts/push_assets_to_cdn.py --incremental

# Verify manifest
python scripts/validate_manifest_freshness.py

# Commit
git add db/assets_manifest.json
git commit -m "chore(assets): upload new images"
```

---

### 3. Pipeline Runbook (30 min read)
**File:** `docs/pipeline-runbook.md`

**Key takeaways:**
- 5-stage pipeline: scan → classify → generate → images → package
- Run full: `python scripts/build_orchestrator.py --full` (~60 seconds)
- Resume after failure: `--resume` flag (skips completed stages)
- Parallelization: stages 3 & 4 run in parallel (saves 20 seconds)
- Retry logic: exponential backoff (1s, 2s, 4s, 8s, max 5 attempts)

**Hands-on task:**
```bash
# Run full pipeline
python scripts/build_orchestrator.py --full
# Output: build/zelex-site-2026-06-21.zip (~260 MB)

# Resume after simulated failure
# (Manually kill process mid-stage, then)
python scripts/build_orchestrator.py --resume
# Continues from where it failed

# Run single stage
python scripts/build_db.py  # Stage 1 only
```

---

### 4. Analytics Runbook (45 min read)
**File:** `docs/analytics-runbook.md`

**Key takeaways:**
- All events fire to `window.dataLayer` (pushed by site.js)
- GTM container reads dataLayer and sends to GA4
- 50+ events: quiz_start, character_detail_view, inquiry_submit_success, etc.
- Test events using debug mode: `localStorage.setItem('zx_analytics_debug', '1')`
- GA4 Real-time report shows events within 1 second
- Dashboard auto-refreshes daily (Looker Studio)

**Hands-on task:**
```javascript
// Enable debug mode in console
localStorage.setItem('zx_analytics_debug', '1');
location.reload();

// Trigger an event manually
ZX.analytics('quiz_start', {
  quiz_family: 'The Muse',
  entry_source: 'browse'
});

// Check console for event log and dataLayer push
```

---

## Updated Workflows

### Adding a New Page

1. **Create HTML file** (e.g., `newpage.html`)
2. **Use shared kit** from `docs/site-kit-contract.md`
3. **Add styles** using tokens only (no hardcoded values)
4. **Add analytics** via `ZX.analytics()` calls
5. **Test** all 4 gates (tokens, images, pipeline, analytics)

### Updating Site Data

1. **Edit hand-curated input** (`db/character_overlay.json` or `db/body_measurements.json`)
2. **Run pipeline:** `python scripts/build_orchestrator.py --full`
3. **Verify output** in `db/characters.json`
4. **Commit:** `db/characters.json` + manifest + inputs

### Deploying to Production

1. **Run full pipeline** (CI does this automatically)
2. **All tests pass** (Python, JavaScript, lint)
3. **Manifest validated** (freshness check)
4. **Merge PR to main**
5. **CI artifact** is the build zip (~260 MB)
6. **Download & deploy** to production server

---

## Success Criteria (Team Responsibility)

**Phase 1 exits when:**
- [ ] Design tokens: 100% color/spacing/type coverage, site.css 647 → 350 lines, zero regressions
- [ ] CDN: All images hosted, manifest versioned, CI guard active
- [ ] Pipeline: Parallelized, build time <1 min, retry logic working
- [ ] GA4: 50+ events firing, PII audit clean, data quality >99%
- [ ] Dashboard: Live, refreshing daily, leadership signed off
- [ ] Documentation: All runbooks written, team trained, FAQ covers 80% of issues
- [ ] **Team sign-off:** All developers comfortable with Phase 1 tools

---

## Your Responsibilities

**Every Developer:**
- [ ] Read all 4 runbooks (2 hours)
- [ ] Understand your role in Phase 1
- [ ] Know how to reference tokens (never hardcode)
- [ ] Know how to add images (run pipeline)
- [ ] Know how to test GA4 events (debug mode)

**Frontend Developers:**
- [ ] Token refactoring & regression testing
- [ ] Component documentation in Storybook
- [ ] GA4 event implementation in site.js

**DevOps / Platform:**
- [ ] CDN provider selection & account setup
- [ ] Pipeline orchestration & CI integration
- [ ] Manifest versioning & freshness checks

**Analytics / Product:**
- [ ] GA4 event taxonomy & dashboard design
- [ ] Event testing & data quality validation
- [ ] Leadership reporting & funnel analysis

---

## Key Dates

| Milestone | Date | Owner |
|-----------|------|-------|
| Initiative 1.1-1.2 Complete | Week 2 | Frontend |
| Initiative 1.3-1.4 Complete | Week 4 | DevOps + Platform |
| Initiative 1.5-1.6 Complete | Week 6 | Analytics |
| Phase 1 Runbooks & Training | Week 6 | DevOps + Team |
| **Phase 1 Exit Gate** | **Week 6** | **All stakeholders** |

---

## Phase 1 Repository Snapshot

After Phase 1, your repo will have:

```
├─ assets/
│  └─ site.css (350 lines, 100% tokens)
│
├─ db/
│  ├─ characters.json
│  └─ assets_manifest.json (new)
│
├─ scripts/
│  ├─ build_orchestrator.py (new)
│  ├─ validate_manifest_freshness.py (new)
│  └─ [others refactored for idempotence]
│
├─ docs/
│  ├─ design-tokens-runbook.md (new)
│  ├─ cdn-runbook.md (new)
│  ├─ pipeline-runbook.md (new)
│  ├─ analytics-runbook.md (new)
│  ├─ phase1-faq.md (new)
│  └─ pdr/ [Phase 1 design docs]
│
└─ CONTRIBUTING.md (updated with Phase 1 processes)
```

**All 41 pages** unchanged in function, only CSS refactored. **Zero functional regressions.**

---

## Common Questions from Team

### Q: "Do I have to memorize all the runbooks?"

**A:** No. Bookmark them and reference as needed. The FAQ covers 80% of common issues. When stuck, search the relevant runbook.

---

### Q: "What if a runbook is unclear or outdated?"

**A:** Report it! We'll fix it and add your question to the FAQ. Send feedback to DevOps owner or open an issue.

---

### Q: "Can I use Phase 1 tools before we formally exit Phase 1?"

**A:** Yes! Phase 1 code is deployed incrementally. As each initiative completes, start using those tools immediately.

---

### Q: "How much time should I spend learning Phase 1?"

**A:** ~3-4 hours total:
- Runbooks: 2 hours (read)
- Hands-on practice: 1-2 hours (run pipeline, test events, etc.)

Spread over next 2 weeks as you encounter each tool.

---

### Q: "What if Phase 1 tools break or conflict with existing workflows?"

**A:** We have a rollback plan for each initiative (see Implementation Plan, Section "Rollback"). Report issues immediately to initiative owner.

---

## Next Steps (Your Action Items)

**By end of this week:**
1. [ ] Read this document (PHASE1-KICKOFF.md) — 15 min
2. [ ] Read all 4 runbooks — 2 hours
3. [ ] Read the FAQ — 30 min
4. [ ] Bookmark runbooks in your IDE/browser

**By end of next week:**
1. [ ] Run `build_orchestrator.py --full` locally
2. [ ] Test a GA4 event in debug mode
3. [ ] Review tokens in site.css
4. [ ] Submit feedback on runbooks

**By end of Phase 1 (6 weeks):**
1. [ ] All Phase 1 initiatives complete
2. [ ] All team members trained & signed off
3. [ ] All tests passing (CI green)
4. [ ] Ready to merge Phase 1 to main

---

## Support Channels

**Questions about:**
- **Design Tokens** → #frontend or Frontend Lead
- **CDN / Images** → #devops or DevOps owner
- **Build Pipeline** → #platform or Platform Lead
- **Analytics / GA4** → #analytics or Analytics Lead
- **General / FAQ** → #general or Project Manager

**Office hours:**
- Tuesdays 2 PM ET: Design System Q&A (Frontend Lead)
- Thursdays 1 PM ET: Infrastructure Q&A (DevOps Lead)

---

## Appendix: Runbook Quick Links

| Runbook | File | Read Time | Audience |
|---------|------|-----------|----------|
| Design Tokens | `docs/design-tokens-runbook.md` | 30 min | Frontend |
| Image CDN | `docs/cdn-runbook.md` | 30 min | DevOps + All |
| Build Pipeline | `docs/pipeline-runbook.md` | 30 min | Platform + All |
| Analytics & GTM | `docs/analytics-runbook.md` | 45 min | Analytics + Frontend |
| Phase 1 FAQ | `docs/phase1-faq.md` | 20 min | All |
| **This Document** | `docs/PHASE1-KICKOFF.md` | 15 min | **All (start here)** |

---

## Acknowledgments

Phase 1 Foundation documentation created by:
- **Platform Engineering:** Orchestration, pipelines, tooling
- **DevOps:** Infrastructure, CDN, CI/CD integration
- **Frontend:** Design tokens, component library, site.js
- **Analytics:** GTM, GA4 events, dashboard
- **Product:** Requirements, QA, leadership alignment

**Sponsor:** Howie (CEO)  
**Delivery Date:** 2026-06-21  
**Version:** 1.0 (Initial)

---

## Ready to Begin?

You now have everything needed to execute Phase 1. Start with:

1. **Read:** `docs/PHASE1-KICKOFF.md` (this doc) ✓
2. **Read:** The 4 runbooks relevant to your role (2 hours)
3. **Ask:** Questions in Slack or office hours
4. **Execute:** Phase 1 initiatives with confidence

**Let's build the foundation for ZELEX Atlas success.**

---

**Document Status:** Active  
**Last Updated:** 2026-06-21  
**Next Review:** 2026-06-28 (end of Week 1)
