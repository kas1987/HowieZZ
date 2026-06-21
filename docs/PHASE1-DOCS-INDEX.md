# Phase 1 Documentation Index

**Location:** `docs/PHASE1-*` and related runbooks  
**Status:** Active (Phase 1, 2026-06-21)  
**Audience:** All developers, DevOps, analytics team

---

## Start Here

1. **New to the team?** Read [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md) first (15 min)
2. **Need a quick answer?** Search [`phase1-faq.md`](phase1-faq.md) (5 min per question)
3. **Learning a specific tool?** Pick the runbook below matching your task

---

## Documentation Files

### Core Phase 1 Documents

| Document | Purpose | Read Time | When to Read |
|----------|---------|-----------|--------------|
| [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md) | Team training summary, responsibilities, success criteria | 15 min | First thing (orientation) |
| [`phase1-faq.md`](phase1-faq.md) | 30+ common questions & answers, grouped by topic | 20 min | When stuck on something |
| **This index** | Map of all Phase 1 docs and when to use each | 10 min | Navigating documentation |

### Runbooks (Detailed How-To Guides)

| Runbook | Owner | Purpose | Audience | Length |
|---------|-------|---------|----------|--------|
| [`design-tokens-runbook.md`](design-tokens-runbook.md) | Frontend Lead | Add/modify CSS tokens; understand token categories; troubleshoot styling issues | Developers editing CSS | 30 min |
| [`cdn-runbook.md`](cdn-runbook.md) | DevOps Lead | Upload images to CDN; refresh manifest; diagnose delivery issues; disaster recovery | All developers; DevOps focus | 30 min |
| [`pipeline-runbook.md`](pipeline-runbook.md) | Platform Lead | Run orchestrator; resume after failures; parallelize stages; debug build issues | All developers; Platform focus | 30 min |
| [`analytics-runbook.md`](analytics-runbook.md) | Analytics Lead | Wire GA4 events; test with GTM; debug PII issues; manage dashboard | Analytics team; Frontend developers | 45 min |

---

## By Role

### Frontend Developer

**Read in this order:**
1. [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md) — understand Phase 1 context
2. [`design-tokens-runbook.md`](design-tokens-runbook.md) — how to use tokens in CSS
3. [`analytics-runbook.md`](analytics-runbook.md) — how to fire GA4 events from site.js
4. [`cdn-runbook.md`](cdn-runbook.md) — how new images flow to production

**Key workflows:**
- Adding a new component: Use design tokens (no hardcoded values)
- Updating styles: Reference `--color-*`, `--sp-*`, `--t-*` tokens
- Testing site: Run `npm test` (JavaScript tests)
- Triggering analytics: Call `ZX.analytics('event_name', {...})`

---

### DevOps / Platform Engineering

**Read in this order:**
1. [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md) — understand Phase 1 goals
2. [`cdn-runbook.md`](cdn-runbook.md) — CDN management & provisioning
3. [`pipeline-runbook.md`](pipeline-runbook.md) — orchestrator & CI/CD integration
4. [`design-tokens-runbook.md`](design-tokens-runbook.md) — tokens (for understanding full stack)

**Key workflows:**
- CI setup: See Pipeline Runbook → "CI/CD Integration" section
- Image upload: See CDN Runbook → "Uploading Images to CDN" section
- Manifest validation: See CDN Runbook → "Manifest Health Check" section
- Build troubleshooting: See Pipeline Runbook → "Debugging Failures" section

---

### Analytics / Product

**Read in this order:**
1. [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md) — understand Phase 1 goals
2. [`analytics-runbook.md`](analytics-runbook.md) — GA4, GTM, event taxonomy, dashboard
3. [`phase1-faq.md`](phase1-faq.md) — common analytics questions

**Key workflows:**
- Testing events: See Analytics Runbook → "Testing Events" section
- Debugging GA4: See Analytics Runbook → "Debugging GA4 Events" section
- Dashboard setup: See Analytics Runbook → "Dashboard Setup" section
- Data quality monitoring: See Analytics Runbook → "Monitoring" section

---

### Project Manager / Leadership

**Read in this order:**
1. [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md) — overview, timelines, responsibilities
2. [`phase1-faq.md`](phase1-faq.md) — common issues & how they're resolved
3. Skim other runbooks (optional, for deeper context)

**Key takeaways:**
- Phase 1 is 6 weeks, 7 initiatives, 240 person-hours
- Phase 1 exits when all initiatives complete + zero critical bugs + leadership sign-off
- Team is trained on 4 runbooks (tokens, CDN, pipeline, analytics)
- Success metrics: CI >98%, build <1min, GA4 live, zero visual regressions

---

## Common Scenarios

### "I'm adding a new page. Where do I start?"

1. Read: [`docs/site-kit-contract.md`](site-kit-contract.md) (page structure requirements)
2. Use: Design tokens (see [`design-tokens-runbook.md`](design-tokens-runbook.md))
3. Add: GA4 events (see [`analytics-runbook.md`](analytics-runbook.md), "Event Firing" section)
4. Test: `npm test` + CI gates (see [`CONTRIBUTING.md`](../CONTRIBUTING.md))

---

### "I'm adding new character images. What's the workflow?"

1. Add images locally: `assets/characters/[Series]-[Code]/hero.jpg` + `gallery/*.jpg`
2. Run: `python scripts/build_orchestrator.py --full`
3. Verify: `python scripts/validate_manifest_freshness.py`
4. Commit: `db/assets_manifest.json` + manifest
5. See: [`cdn-runbook.md`](cdn-runbook.md), "Uploading Images" section for details

---

### "The build is failing. Where do I look?"

1. Check: [`pipeline-runbook.md`](pipeline-runbook.md), "Debugging Failures" section
2. Run: `python scripts/build_orchestrator.py --resume` (to retry from failure point)
3. If still failing: See FAQ at [`phase1-faq.md`](phase1-faq.md#build-pipeline)
4. Report: Open issue with error message and log output

---

### "GA4 events aren't showing up. Where do I debug?"

1. Check: [`analytics-runbook.md`](analytics-runbook.md), "Debugging GA4 Events" section
2. Enable: Debug mode in browser (see Analytics Runbook, "Testing Events" section)
3. Verify: GTM Preview mode (see Analytics Runbook, "GTM Preview Mode" section)
4. If still broken: See FAQ at [`phase1-faq.md`](phase1-faq.md#analytics--gtm)

---

### "A token changed but I don't see it updating. Where do I look?"

1. Check: [`design-tokens-runbook.md`](design-tokens-runbook.md), "Debugging Token Issues" section
2. Verify: Token exists in `assets/site.css` `:root` section
3. Test: Hard reload browser (Ctrl+Shift+R), check DevTools Computed styles
4. If still broken: See FAQ at [`phase1-faq.md`](phase1-faq.md#design-tokens)

---

## FAQ Quick Links

**By Component:**
- Design Tokens: [`phase1-faq.md#design-tokens`](phase1-faq.md#design-tokens)
- Image CDN: [`phase1-faq.md#image-cdn`](phase1-faq.md#image-cdn)
- Build Pipeline: [`phase1-faq.md#build-pipeline`](phase1-faq.md#build-pipeline)
- Analytics & GTM: [`phase1-faq.md#analytics--gtm`](phase1-faq.md#analytics--gtm)
- General Troubleshooting: [`phase1-faq.md#general-troubleshooting`](phase1-faq.md#general-troubleshooting)

**By Urgency:**
- Blocking me now: Start with [`phase1-faq.md`](phase1-faq.md)
- Want to understand better: Read full runbook for that component
- Want to learn Phase 1 holistically: Start with [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md)

---

## How to Use This Index

1. **Find your role** (Frontend, DevOps, Analytics, Manager) ← Start here
2. **Read documents in recommended order** (ensures context builds)
3. **Reference runbooks** when you hit a specific task
4. **Check FAQ** when something breaks or is confusing
5. **Ask in Slack** if docs are unclear or missing

---

## Related Documentation

**For context on why Phase 1 exists:**
- [`IMPLEMENTATION-PLAN.md`](../IMPLEMENTATION-PLAN.md) — Full 52-week roadmap, Phase 1 breakdown

**For specific design decisions:**
- [`docs/pdr/PDR-100-design-token-system.md`](pdr/PDR-100-design-token-system.md) — Token schema & rationale
- [`docs/pdr/PDR-analytics-event-taxonomy.md`](pdr/PDR-analytics-event-taxonomy.md) — Event taxonomy & definitions

**For general project info:**
- [`README.md`](../README.md) — Project overview & setup
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — Git workflow, conventions, testing
- [`docs/site-kit-contract.md`](site-kit-contract.md) — Shared page structure requirements

---

## Updates & Maintenance

**This index is updated when:**
- New runbooks are added
- Documentation significantly changes
- FAQ grows beyond 50 entries

**Last updated:** 2026-06-21  
**Next review:** 2026-06-28 (end of Week 1)  
**Owner:** DevOps + Platform Engineering

---

## Quick Reference: File Paths

```
docs/
├─ PHASE1-KICKOFF.md                    ← START HERE (team training)
├─ PHASE1-DOCS-INDEX.md                 ← YOU ARE HERE
├─ phase1-faq.md                        ← Common questions
├─ design-tokens-runbook.md             ← CSS tokens how-to
├─ cdn-runbook.md                       ← Image delivery how-to
├─ pipeline-runbook.md                  ← Build orchestrator how-to
├─ analytics-runbook.md                 ← GA4/GTM how-to
├─ site-kit-contract.md                 ← Shared page structure
├─ pdr/
│  ├─ PDR-100-design-token-system.md    ← Token design rationale
│  └─ PDR-analytics-event-taxonomy.md   ← Event definitions
└─ ...
```

---

## Still Lost?

1. **Closest match wins:** If docs mention your question, start with that runbook
2. **Google it:** Try searching the specific runbook file (Ctrl+F)
3. **Ask in Slack:** Post in channel matching your component (see Support section below)
4. **Office hours:** See schedule in [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md#support-channels)

---

## Support Channels

| Issue | Channel | Owner |
|-------|---------|-------|
| Design Tokens | #frontend | Frontend Lead |
| CDN / Images | #devops | DevOps Lead |
| Build Pipeline | #platform | Platform Lead |
| Analytics / GA4 | #analytics | Analytics Lead |
| General Phase 1 | #general | Project Manager |

---

**Ready to dive in? Start with [`PHASE1-KICKOFF.md`](PHASE1-KICKOFF.md).**
