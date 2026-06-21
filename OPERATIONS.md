# ZELEX Brand Team Operations Manual

**Version:** 1.0  
**Last Updated:** 2026-06-21  
**Status:** Ready for Production  
**Audience:** Brand Operations Team, SRE, On-Call

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [On-Call Rotation](#on-call-rotation)
3. [Incident Triage & Escalation](#incident-triage--escalation)
4. [Service-Level Agreements (SLAs)](#service-level-agreements-slas)
5. [Monitoring & Alerting](#monitoring--alerting)
6. [Common Runbooks](#common-runbooks)
7. [Support Process](#support-process)
8. [Emergency Contacts](#emergency-contacts)

---

## Quick Start

### For First-Time Responders

1. **Check the dashboard**: [GitHub Actions](https://github.com/kas1987/HowieZZ/actions)
2. **Verify the site**: [Production](https://www.zelexdoll.com) — compare to [GitHub Pages staging](https://kas1987.github.io/HowieZZ/)
3. **Run the local test suite**: See [Runbook: Local Verification](#local-verification)
4. **Determine severity**: See [Incident Severity Matrix](#incident-severity-matrix)
5. **Escalate if needed**: See [Escalation Path](#escalation-path)

---

## On-Call Rotation

### Rotation Schedule

- **Primary**: Rotates weekly (Monday 00:00 UTC)
- **Secondary**: Available for backup/handoff
- **On-call tools**: GitHub, Slack, email
- **Shift duration**: 7 days (Monday–Sunday UTC)
- **Handoff briefing**: Sunday 23:30 UTC (15 min)

### Responsibilities

| Responsibility | Primary | Secondary | Optional |
|---|---|---|---|
| Monitor GitHub Actions | Required | Standby | — |
| Respond to Slack alerts | Required | Standby | — |
| Triage incoming issues | Required | Assist | — |
| Execute runbooks | Required | Assist | — |
| Post mortem on incident | Required | Attend | — |

### Roster

```
[TO BE FILLED BY OPS TEAM]

Week of Jun 21: [Name] (primary), [Name] (secondary)
Week of Jun 28: [Name] (primary), [Name] (secondary)
...
```

**Update this roster in Slack's bookmark #zelex-ops.**

---

## Incident Triage & Escalation

### Incident Severity Matrix

| Severity | Condition | Response Time | Who | Action |
|---|---|---|---|---|
| **P1 (Critical)** | Site down, zero visitors, payment form broken, security breach | 15 min | Primary + Secondary + Lead | Page all, immediate response |
| **P2 (High)** | Features broken, catalog corrupted, performance degradation >50% | 1 hour | Primary + optionally Secondary | Investigate + assess |
| **P3 (Medium)** | Minor visual bug, slow load (>3s), missing text | 4 hours | Primary | Fix during business hours |
| **P4 (Low)** | Documentation unclear, typo, cosmetic issue | Best effort | — | Log and batch in sprint |

### Incident Severity Matrix Decision Tree

```
Is the site completely unreachable?
  YES → P1 (Critical)
  NO ↓

Is a major feature broken (browse, quiz, contact)?
  YES → P2 (High)
  NO ↓

Is catalog data corrupted or missing?
  YES → P2 (High)
  NO ↓

Is there a performance issue (>50% slowdown)?
  YES → P2 (High)
  NO ↓

Is there a visual bug or UX issue?
  YES → P3 (Medium)
  NO ↓

Everything else → P4 (Low)
```

### Escalation Path

```
Incident Detected
      ↓
[Primary On-Call]
      ↓
Can resolve in <1 hour?
  YES → Execute, document, notify
  NO ↓
[Invoke Secondary + Lead]
      ↓
Is it security-related?
  YES → Notify CISO (kas41866@gmail.com) immediately
  NO ↓
P1 severity?
  YES → Notify CEO (howie@zelexdoll.com)
  NO ↓
Continue investigation
```

### How to Page the Team

1. **Critical incidents (P1)**: Slack `@incident-commander`, `@zelex-ops-oncall`
2. **High priority (P2)**: Slack `#zelex-ops`, `@zelex-ops-oncall`
3. **Medium/Low**: Open GitHub issue, tag `urgent` or `backlog`

---

## Service-Level Agreements (SLAs)

### Availability SLA

- **Target**: 99.5% uptime (monthly, measured via Uptime Robot)
- **Planned maintenance window**: First Sunday of each month, 02:00–04:00 UTC
- **Maintenance communication**: Posted to `#zelex-ops` 7 days prior

### Response SLA

| Severity | Initial Response | Mitigation Target |
|---|---|---|
| P1 | 15 minutes | 1 hour |
| P2 | 1 hour | 4 hours |
| P3 | 4 hours | 1 business day |
| P4 | 1 business day | Best effort |

### Deployment SLA

- **Code deployed to main**: GitHub Actions CI validates automatically
- **Deployment to production**: <5 minutes after merge (GitHub Pages)
- **Catalog sync (Shopify)**: Every 6 hours (automated)

### Success Metrics (SLIs)

- **Request latency p99**: <2 seconds
- **Build time**: <10 minutes (CI)
- **Test coverage**: >80% (Python + JavaScript)
- **Catalog freshness**: <6 hours old

---

## Monitoring & Alerting

### Automated Monitoring

| Service | Health Check | Interval | Alert On |
|---|---|---|---|
| GitHub Pages | HTTP GET / | 5 min | Any 4xx/5xx |
| Catalog JSON | Schema + record count | 1 hour | Missing/corrupted |
| Images | CDN availability | 15 min | 404s |
| Analytics | Event funnel | 1 hour | Flatline (0 events) |

**Tool**: Uptime Robot (free tier, SMS + Slack alerts)

### GitHub Actions Monitoring

All workflows are monitored automatically:

- **CI (build + validate)**: Runs on every push to `main`
- **Shopify Sync**: Runs every 6 hours (UTC 00:00, 06:00, 12:00, 18:00)
- **Alerts**: Slack channel `#zelex-ops` (via GitHub integration)

### Setting Up Uptime Robot

1. Go to [uptime.com](https://uptime.com) (or your chosen provider)
2. Add monitor: `https://www.zelexdoll.com` (GET /)
3. Set interval: 5 minutes
4. Alert: Slack `#zelex-ops` on failure
5. Alert: SMS to on-call primary on P1

### Log Aggregation

- **GitHub Actions logs**: [Actions tab](https://github.com/kas1987/HowieZZ/actions)
- **Artifacts**: Analytics summaries, Shopify sync reports (auto-uploaded)
- **Local logs** (if self-hosted): `/var/log/zelex/*.log` (TBD by devops)

### Performance Dashboard (Optional)

Create a public dashboard at `/perf-dashboard.html` showing:

- Avg request latency (last 24h)
- 99th percentile latency
- Error rate (4xx/5xx)
- Uptime %
- Last Shopify sync timestamp

---

## Common Runbooks

### Local Verification

**When**: Need to confirm an issue locally before responding  
**Time**: 5 minutes

```bash
cd /path/to/HowieZZ

# 1. Verify Python environment
python --version  # Should be 3.11+

# 2. Install dependencies (one-time)
pip install pytest pytest-cov Pillow

# 3. Run build pipeline
python scripts/build_orchestrator.py --json

# 4. Run tests
python -m pytest --tb=short -q
npm test

# 5. Start dev server
python serve.py 8000

# 6. Open browser to http://localhost:8000
# Check: homepage loads, navigation works, no console errors
```

### Site Down (P1)

**When**: Homepage returns 500 or is completely unreachable  
**Time**: <15 minutes

**Step 1: Verify status**

```bash
# Check GitHub Pages deployment status
curl -I https://www.zelexdoll.com
# Expected: HTTP 200

# Check staging
curl -I https://kas1987.github.io/HowieZZ/
# Expected: HTTP 200
```

**Step 2: Check CI**

1. Go to [GitHub Actions](https://github.com/kas1987/HowieZZ/actions)
2. Look at most recent run on `main`
3. If red (failed): See [CI Build Failure](#ci-build-failure)
4. If green: GitHub Pages may be having downtime (check GitHub status page)

**Step 3: Escalate**

If CI is passing but site is down:
- Notify GitHub support (status.github.com)
- Escalate to CEO/lead: "GitHub Pages is unresponsive, investigating"
- ETA: GitHub typically restores within 30 min

### CI Build Failure

**When**: Red badge on [Actions](https://github.com/kas1987/HowieZZ/actions)  
**Time**: 10–30 minutes

**Step 1: Identify the failure**

1. Click the red workflow run
2. Find the failed step (e.g., "Validate site + data")
3. Read the error message (see examples below)

**Step 2: Common build failures**

| Failure | Cause | Fix |
|---|---|---|
| `SyntaxError` in Python | Script has typo | Push fix to feature branch, re-run |
| `Module not found` | Missing import | `pip install` in CI, commit `requirements.txt` |
| `JSON parse error` | Corrupted `db/*.json` | See [Catalog Corruption](#catalog-corruption) |
| `Test failed` | Logic error or flaky test | Debug locally, fix, push |
| `Image/secret committed` | Hygiene guard triggered | Remove file, `git rm --cached`, push |

**Step 3: Fix & push**

```bash
# Create feature branch
git checkout -b fix/build-failure

# Make fix
# (edit file, run local test)

# Commit & push
git add -A
git commit -m "fix: resolve build failure in [step name]"
git push -u origin fix/build-failure

# Create PR, wait for CI to pass, merge to main
```

### Catalog Corruption

**When**: Shopify sync fails or catalog.json is invalid  
**Time**: 15–45 minutes

**Symptoms**:
- "JSON parse error" in CI
- Browse page shows no characters
- Character count is zero

**Step 1: Verify corruption**

```bash
# Check catalog schema
python -c "
import json
with open('db/catalog.json') as f:
    c = json.load(f)
print(f'Products: {len(c.get(\"products\", []))}')
print(f'Series: {c.get(\"series\", [])}')
print(f'Keys: {c.keys()}')
"
```

**Step 2: Restore from backup**

If the catalog is corrupted:

```bash
# Option A: Re-run build (if source data is clean)
cd scripts
python build_db.py
python build_profiles.py
python build_characters.py
make_thumbs.py

# Option B: Revert last commit
git log --oneline db/catalog.json | head -3
git revert <commit-hash>
git push
```

**Step 3: Investigate root cause**

- Check Shopify sync artifacts in [Actions](https://github.com/kas1987/HowieZZ/actions)
- Look for `.shopify_sync_history.jsonl` errors
- Verify Shopify credentials are still valid

**Step 4: Escalate if unable to restore**

Contact: Lead engineer (see Emergency Contacts)

### Performance Degradation (>3s load time)

**When**: Users report slow site or monitoring shows p99 latency >2s  
**Time**: 15–30 minutes

**Step 1: Measure**

```bash
# From browser console
performance.measure('page-load')
performance.getEntriesByType('measure')

# From CLI
curl -w "Time to first byte: %{time_starttransfer}s\nTotal time: %{time_total}s\n" \
  https://www.zelexdoll.com
```

**Step 2: Identify bottleneck**

- **HTML load slow**: Likely GitHub Pages CDN issue. Monitor for 15 min.
- **Asset load slow** (images): Check CDN cache headers; may need cache bust.
- **JavaScript slow**: Use browser DevTools → Performance tab. Look for long tasks.
- **API calls slow**: Check Shopify/external service latency.

**Step 3: Mitigation**

- **Short-term**: Post "We're experiencing slower load times" to Slack
- **Long-term**: File performance bug, assign to engineering

### Payment Form Broken (P1)

**When**: Contact form won't submit or shows errors  
**Time**: 10–20 minutes

**Step 1: Test form locally**

```bash
# Open http://localhost:8000/contact.html
# Try to fill and submit the form
# Check browser console for errors
```

**Step 2: Verify configuration**

```bash
# Check contact.html and assets/site.js
grep -n "INQUIRY_EMAIL\|FORM_ENDPOINT" assets/site.js
# Should see real email or Formspree URL

# If empty, that's the bug:
# Edit assets/site.js, set INQUIRY_EMAIL or FORM_ENDPOINT
git add assets/site.js
git commit -m "fix: configure contact form endpoint"
git push -u origin fix/contact-form
```

**Step 3: Escalate**

If form is configured but still broken, contact backend team (Formspree/Getform may be down).

### Shopify Sync Failed

**When**: Workflow shows red for "Shopify Feed Sync"  
**Time**: 15–30 minutes

**Step 1: Check sync artifacts**

1. Go to [Actions](https://github.com/kas1987/HowieZZ/actions)
2. Find "Shopify Feed Sync" run
3. Download artifact: `shopify-sync-artifacts`
4. Read `db/.shopify_sync_history.jsonl` (last 50 lines)

**Step 2: Common errors**

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Token expired | Rotate Shopify API token in Secrets |
| `Connection timeout` | Shopify API down | Wait 15 min, manually trigger workflow |
| `Rate limited` | Too many requests | Reduce sync frequency or request quota |
| `Product not found` | SKU mismatch | Update `db/shopify_sku_mapping.json` |

**Step 3: Retry**

Go to [Actions → Shopify Feed Sync → Run workflow](https://github.com/kas1987/HowieZZ/actions/workflows/shopify-sync.yml)

```
Mode: full
Run
```

**Step 4: If still failing**

- Contact Shopify API support (api@shopify.com)
- Escalate to DevOps (see Emergency Contacts)

### Missing or Wrong Character Image

**When**: Character detail page shows placeholder/wrong hero  
**Time**: 20–45 minutes

**Cause**: Usually Shopify sync missed a product or CDN cache needs bust

**Step 1: Verify**

```bash
# Find character ID from URL
# e.g., K-ZK168B-01

# Check characters.json
python -c "
import json
with open('db/characters.json') as f:
    chars = json.load(f)
char = [c for c in chars if c['id'] == 'K-ZK168B-01'][0]
print(f'Hero: {char.get(\"hero_image\")}')
print(f'Gallery: {[img for img in char.get(\"images\", [])]}')
"
```

**Step 2: Re-run character build**

```bash
cd scripts
python build_characters.py
python make_thumbs.py  # regenerate thumbnails
git add ../db/characters.json
git commit -m "fix: regenerate character images"
git push -u origin fix/character-images
```

**Step 3: Verify CDN**

Check if image URL has cache headers:

```bash
curl -I https://cdn.zelexdoll.com/thumb/K-ZK168B-01_thumb.jpg
# Look for: Cache-Control: max-age=31536000 (1 year)
```

If stale, manually bust cache (if available).

---

## Support Process

### Support Channels

| Channel | Use Case | Response Time |
|---|---|---|
| Slack `#zelex-ops` | Operational alerts, on-call chat | 15 min (during shift) |
| Email `ops@zelexdoll.com` | Tickets, formal handoff | 1 hour (business hours) |
| GitHub Issues | Bug reports, features, doc updates | 1 business day |
| `SECURITY.md` contact | Security/privacy concerns | 24 hours (immediate response) |

### Support Ticket Template

When opening an issue, include:

```
Title: [BRIEF DESCRIPTION]

Environment:
- Browser: [Chrome / Safari / Firefox]
- OS: [Windows / macOS / Linux]
- URL: [https://www.zelexdoll.com/...]

Steps to Reproduce:
1. ...
2. ...
3. ...

Expected: ...
Actual: ...

Severity: [P1/P2/P3/P4]
Logs: [if applicable]
```

### Feature Request Process

1. Open GitHub issue with label `enhancement`
2. Describe user need + acceptance criteria
3. Link to relevant PDR (Product Decision Record)
4. Assign to product owner for prioritization

---

## Emergency Contacts

| Role | Name | Email | Phone | Slack |
|---|---|---|---|---|
| **CEO** | Howie Wang | howie@zelexdoll.com | — | @howie |
| **Lead Engineer** | [Name] | [email] | [phone] | @[slack] |
| **DevOps/SRE** | [Name] | [email] | [phone] | @[slack] |
| **Brand Manager** | [Name] | [email] | [phone] | @[slack] |
| **Security Officer** | — | kas41866@gmail.com | — | — |

**Update this table with real contacts.**

### Escalation Protocol

**For P1 incidents:**

1. Notify lead engineer immediately (Slack + email)
2. Notify DevOps if infrastructure issue
3. Notify CEO if business-critical or public-facing outage
4. Update status page (`#zelex-ops` Slack pin)

**For security issues:**

1. Do NOT post in public channels
2. Email security officer immediately
3. Follow [SECURITY.md](SECURITY.md) protocol

---

## Training Checklist

Before taking the on-call shift, confirm:

- [ ] You can access GitHub (ops account or personal account with team access)
- [ ] You have Slack notifications enabled for `#zelex-ops`
- [ ] You can run local build (`python scripts/build_orchestrator.py`)
- [ ] You have read all runbooks (this file)
- [ ] You know how to revert a commit (`git revert`)
- [ ] You know the on-call rotation for next week
- [ ] You have contact info for escalation (see above)
- [ ] You've done a dry-run of a P2 triage

**First-time on-call?** Schedule a 30-min walkthrough with previous on-call.

---

## Audit & Review

- **Monthly review**: On-call lead reviews incidents, updates runbooks
- **Quarterly review**: Team reviews SLAs, monitoring, alert fatigue
- **Post-mortem template**: See `docs/postmortem-template.md`

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-21 | Initial release: on-call, SLA, runbooks |

---

**Last Updated**: 2026-06-21  
**Next Review**: 2026-09-21  
**Owner**: DevOps / SRE Lead
