# ZELEX Service-Level Agreements (SLAs)

**Version**: 1.0  
**Effective Date**: 2026-06-21  
**Review Date**: 2026-09-21  
**Owner**: DevOps / SRE Lead

---

## Executive Summary

ZELEX Character Atlas commits to delivering a reliable, high-performance catalog experience for customers and internal stakeholders. This document defines the service levels we target and the metrics we track.

---

## Availability SLA

### Commitment

**Target Uptime: 99.5% per calendar month**

- Measured via automated monitoring (Uptime Robot or equivalent)
- Applies to `https://www.zelexdoll.com` (production)
- Excludes scheduled maintenance windows

### Calculation

```
Monthly Uptime % = (Total Minutes in Month - Downtime Minutes) / Total Minutes in Month × 100

99.5% uptime = ~18 minutes of allowed downtime per month
```

### Example

```
June 2026: 43,200 minutes in month
99.5% uptime = 216 minutes allowed downtime
Actual: 180 minutes downtime (0.42%)
Result: SLA MET ✓
```

### Exclusions

Downtime does **not** count against SLA if caused by:
- Scheduled maintenance (announced 7 days prior, performed Sundays 02:00–04:00 UTC)
- Upstream provider outage (GitHub Pages, Shopify)
- Force majeure (natural disaster, war, pandemic)
- Customer misconfiguration (e.g., DNS TTL too high)

### Credits

If uptime falls below 99.5%:

| Uptime | SLA Credit |
|---|---|
| 99.0–99.5% | 10% monthly fee |
| 98.0–99.0% | 25% monthly fee |
| 95.0–98.0% | 50% monthly fee |
| <95.0% | 100% refund + credit |

*Note: This is a private project. Credits apply to brand team internal "cost".*

---

## Response & Resolution SLAs

### By Severity Level

| Severity | Description | Initial Response | Target Resolution | Escalation |
|---|---|---|---|---|
| **P1 Critical** | Site down, security breach, payment failure | 15 min | 1 hour | Page all + CEO |
| **P2 High** | Feature broken, catalog corrupted, >50% slowdown | 1 hour | 4 hours | Page lead + team |
| **P3 Medium** | Visual bug, minor performance issue, typo | 4 hours | 1 business day | Open GitHub issue |
| **P4 Low** | Documentation error, cosmetic issue | 1 business day | Next sprint | Log and batch |

### Definitions

**Initial Response Time**: Acknowledge the issue in Slack / GitHub

**Target Resolution Time**: Issue fixed, deployed to production, verified

**Escalation**: Notify next level if first responder can't resolve within 50% of time window

---

## Data Freshness SLA

### Commitment

Catalog data shall be refreshed every 6 hours from Shopify source.

| Metric | Target | Alert At |
|---|---|---|
| Shopify sync frequency | Every 6 hours | No sync in 8+ hours |
| Catalog age | < 6 hours | > 8 hours old |
| Character count | ≥ 76 | < 50 |
| Image availability | 100% served | > 5 errors/hour |

### Monitoring

- Automated check hourly: is `db/catalog.json` timestamp < 8 hours?
- If stale: Slack alert to `#zelex-ops`
- Manual verification: browse page loads all characters

---

## Performance SLA

### Commitment

Website shall perform at industry-standard speeds.

| Metric | P50 (Median) | P95 | P99 | Alert Threshold |
|---|---|---|---|---|
| Homepage load (ttfb) | <300ms | <1s | <2s | P99 > 2s for 15 min |
| Browse page load | <500ms | <1.5s | <2.5s | P99 > 2.5s for 15 min |
| Character detail load | <400ms | <1.2s | <2s | P99 > 2s for 15 min |
| Image serving (CDN) | <100ms | <500ms | <1s | P99 > 1s for 15 min |

### Measurement

- Real User Monitoring (RUM) via Google Analytics
- Synthetic monitoring via Uptime Robot
- Build artifact timing in CI

### Target Response Times

- Asset size must be optimized (image file <500 KB each)
- CSS bundle must be < 50 KB
- JS bundle must be < 50 KB
- No blocking JavaScript in critical path

---

## Build & Deployment SLA

### Commitment

Code changes shall deploy to production within SLA.

| Stage | Target | Alert At |
|---|---|---|
| CI build time | < 10 minutes | > 15 min |
| Test suite | 100% pass rate | Any failure |
| Deploy time | < 5 min (GitHub Pages) | > 10 min |
| End-to-end time | < 20 min | > 30 min |

### Validation Gates

All deploys must pass:
1. Python syntax check (`py_compile`)
2. Unit tests (pytest + npm test)
3. Schema validation (catalog.json, characters.json)
4. Site validation (all pages, no 404s in assets)
5. Security scan (no images, secrets, confidential docs committed)

---

## On-Call SLA

### Commitment

Issues shall be monitored and triaged continuously during business hours and 24/7 for P1.

| Scenario | Coverage | Response Time |
|---|---|---|
| **Business hours** (09:00–17:00 UTC) | Primary on-call | 30 min |
| **After hours** (17:00–09:00 UTC) | Primary on-call | 1 hour (or escalate) |
| **P1 any time** | 24/7 | 15 min |
| **Weekends** | Primary on-call | 1 hour |

### Handoff Protocol

- **Weekly rotation**: Monday 00:00 UTC → Sunday 23:59 UTC
- **Handoff briefing**: Sunday 23:30 UTC (15 min)
- **Outgoing on-call**: briefs incoming, reviews open issues
- **Incoming on-call**: confirms tool access, verifies monitoring

---

## Communication SLA

### Incident Status Updates

| Severity | Frequency | Channel |
|---|---|---|
| P1 | Every 15 min | Slack `#zelex-ops` |
| P2 | Every 30 min | Slack thread + email |
| P3 | Hourly | GitHub issue |
| P4 | End of day | Email |

### Post-Incident Communication

- **P1 incidents**: Post-mortem due within 24 hours
- **P2 incidents**: Post-mortem due within 1 week
- **P3/P4**: Documented in GitHub issue

### Customer Communication (if applicable)

- **Site down**: Update status page within 15 min
- **Major outage**: Email notification within 30 min
- **Resolved**: Post resolution + ETA for next check within 1 hour

---

## Monthly Metrics Review

### Key Performance Indicators (KPIs)

Report monthly on:

1. **Availability**
   - Uptime %
   - Downtime minutes
   - Root causes
   - Prevented incidents

2. **Response**
   - P1 response time (avg)
   - P2 response time (avg)
   - P3 resolution time (avg)
   - % within SLA

3. **Quality**
   - Build pass rate %
   - Test coverage %
   - Security issues (count)
   - Performance regressions

4. **Operational Health**
   - Incidents (count by severity)
   - On-call shifts completed (count)
   - Escalations (count)
   - Training completions (count)

### Dashboard

Create a public dashboard showing:
- Current uptime %
- Response times (p50, p95, p99)
- Last 30 days incident trend
- Deployment frequency

---

## Escalation Triggers

### Automatic Escalation

If SLA is at risk of breach, automatically escalate:

| Condition | Action |
|---|---|
| P1 not responded within 10 min | Page secondary + lead |
| P1 not resolved within 45 min | Page CEO |
| 3+ P2s in 24 hours | Schedule post-mortem |
| 2+ P1s in 7 days | Postmortem + process review |

---

## SLA Exceptions

The following situations may warrant SLA exception:

1. **Scheduled maintenance** (announced 7 days prior, <2 hours/month)
2. **Upstream provider outage** (GitHub Pages, Shopify API, CDN)
3. **Force majeure** (natural disaster, war, cyberattack beyond control)
4. **Customer misconfiguration** (DNS, firewall, local network)

**Exception Process:**
1. Document in post-mortem
2. Note "SLA exception — [reason]"
3. Notify stakeholders
4. No credit issued for force majeure

---

## SLA Targets Over Time

As the service matures:

**Phase 1 (Launch, 2026 Q2–Q3):** 99.5% uptime, basic monitoring  
**Phase 2 (Stabilize, 2026 Q4):** 99.9% uptime, advanced monitoring  
**Phase 3 (Scale, 2027 Q1+):** 99.99% uptime, geographic redundancy  

---

## Review & Adjustment

### Monthly Review

Every month, on-call lead reviews:
- [ ] Metrics against targets
- [ ] Any breaches documented
- [ ] Trends (improving/degrading?)
- [ ] Adjustments needed

### Quarterly Review

Every quarter, SRE lead reviews:
- [ ] SLA targets still realistic?
- [ ] Any changes to scope?
- [ ] Monitoring coverage adequate?
- [ ] Training materials updated?
- [ ] Team capacity sufficient?

### Annual Review

Every year, leadership reviews:
- [ ] SLA alignment with business goals
- [ ] Investment in infrastructure
- [ ] Team staffing
- [ ] Technology debt
- [ ] Risk assessment

---

## Reporting Template

**Monthly SLA Report**

```
Period: [Month Year]
Prepared by: [Name]
Date: [Date]

UPTIME
  Target: 99.5%
  Actual: [X.XX]%
  Status: ✓ MET / ✗ MISSED
  Downtime: [X] minutes
  Incidents: [count]

RESPONSE TIMES
  P1: avg [X] min (target 15 min) — ✓/✗
  P2: avg [X] min (target 60 min) — ✓/✗
  P3: avg [X] min (target 240 min) — ✓/✗

QUALITY
  Build pass rate: [X]%
  Test coverage: [X]%
  Security issues: [count]
  Performance: p99 [X]ms (target <2s)

ACTION ITEMS
  - [Item 1]
  - [Item 2]
```

---

## Contacts

| Role | Name | Email | Phone |
|---|---|---|---|
| SLA Owner | [Name] | [email] | [phone] |
| On-Call Lead | [Name] | [email] | [phone] |
| DevOps Lead | [Name] | [email] | [phone] |
| CEO | Howie Wang | howie@zelexdoll.com | — |

---

## Related Documents

- [OPERATIONS.md](../OPERATIONS.md) — On-call runbooks
- [MONITORING-CONFIG.md](MONITORING-CONFIG.md) — Alert configuration
- [POSTMORTEM-TEMPLATE.md](POSTMORTEM-TEMPLATE.md) — Incident review
- [BRAND-TEAM-TRAINING.md](BRAND-TEAM-TRAINING.md) — Team training

---

**Version**: 1.0  
**Last Updated**: 2026-06-21  
**Next Review**: 2026-09-21
