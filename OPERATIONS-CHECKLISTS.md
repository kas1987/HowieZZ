# ZELEX Operations Checklists & Standard Procedures

**Version:** 1.0 | **Last Updated:** 2026-06-21

Ready-to-use checklists for common operational tasks.

---

## Pre-Deployment Checklist

**Purpose:** Ensure all code/content changes are production-ready  
**Duration:** 10-15 min  
**Performed By:** Developer, reviewed by lead  
**Block Deployment:** If any item fails

### Code Changes

- [ ] All tests pass locally: `python -m pytest tests/ -v`
- [ ] Linting passes: `pylint scripts/` and `eslint assets/`
- [ ] No hardcoded secrets (no API keys, tokens, passwords)
- [ ] No breaking changes to public APIs
- [ ] Database migrations (if applicable) tested
- [ ] Error handling implemented (no bare `except` blocks)
- [ ] Performance impact assessed (no new >1s operations)
- [ ] Accessibility checked (WCAG 2.1 AA minimum)

### Content Changes

- [ ] JSON files validated: `python -m json.tool db/file.json`
- [ ] Character data complete (no null required fields)
- [ ] Pricing matches Shopify (or intentional override documented)
- [ ] Images present and named correctly
- [ ] Community submissions moderated (no spam/PII)
- [ ] Copy reviewed for typos, brand consistency

### Documentation

- [ ] Comments added to complex code
- [ ] Runbook updated if procedure changed
- [ ] `CHANGELOG.md` updated with changes
- [ ] Screenshots/GIFs added if UI changed

### Final Checks

- [ ] Code reviewed by another engineer
- [ ] PR description complete and clear
- [ ] Branch name follows convention: `feature/xyz`, `hotfix/xyz`
- [ ] Commits squashed or logically organized
- [ ] `git status` shows clean (all committed)

---

## Deployment Checklist

**Purpose:** Ship code to production safely  
**Duration:** 5-10 min (automated via CI/CD)  
**Performed By:** Automated (GitHub Actions) + manual verification  
**Prerequisites:** Pre-deployment checklist passed

### Pre-Push

- [ ] Local branch is up to date: `git pull origin main`
- [ ] No local uncommitted changes: `git status` should be clean
- [ ] Tests pass locally: `python -m pytest tests/`
- [ ] Build succeeds locally: `python scripts/build_orchestrator.py`

### Git Push

- [ ] Create pull request (if not already created)
- [ ] Link to related issues/tasks
- [ ] Add meaningful PR description
- [ ] Push to origin: `git push origin branch-name`
- [ ] Verify PR appears on GitHub

### CI/CD (Automated)

- [ ] GitHub Actions workflow starts
- [ ] All checks pass (green checkmarks)
  - [ ] Tests (unit, integration, E2E)
  - [ ] Linting
  - [ ] Build
  - [ ] Lighthouse audit
- [ ] No new security warnings
- [ ] Artifacts generated (build logs, test results)

### Code Review

- [ ] Lead engineer reviews PR
- [ ] At least 1 approval received
- [ ] Comments addressed (no "request changes")
- [ ] Ready to merge

### Merge & Deploy

- [ ] Click "Merge" on GitHub
- [ ] Select "Squash and merge" (or "Create a merge commit" for hotfixes)
- [ ] Verify GitHub Actions re-triggers with `main` branch
- [ ] Watch deployment progress in Actions tab
- [ ] Check for "Deploy successful" notification in Slack

### Post-Deployment (5-10 min)

- [ ] Visit live site: `https://zelex.com`
- [ ] Spot-check changed pages load correctly
- [ ] Check browser console for errors (F12 → Console)
- [ ] Monitor GA4 for errors (should be 0 for first 5 min)
- [ ] Monitor Sentry for new errors
- [ ] Tag release (if major version): `git tag -a v1.2.3`

### If Deployment Fails

- [ ] Check GitHub Actions logs for error message
- [ ] Fix root cause (code error, missing env var, etc.)
- [ ] Push fix to same PR branch
- [ ] CI/CD re-runs, deploy retries automatically

---

## Daily Operations Checklist

**Purpose:** Routine daily operations  
**Duration:** 15-20 min  
**Performed By:** On-call engineer  
**Frequency:** Daily (8 AM, 2 PM, 6 PM)

### Morning Check (8 AM)

- [ ] Site accessibility: `curl https://zelex.com/ | grep -o "200 OK"`
- [ ] Database integrity: `python scripts/check_db.py --validate-all`
- [ ] Error rate check: "Sentry dashboard for errors >10"
- [ ] Last deployment: `git log -1 --pretty=format:"%ai %s"`
- [ ] Shopify sync status: `cat db/.shopify_sync_state.json | jq '.last_sync'`
- [ ] Slack #zelex-ops: Post "✅ Morning check passed"

### Afternoon Check (2 PM, Peak Hours)

- [ ] Real-time users: "GA4 Real-time view should show >50 users"
- [ ] Form submissions: "GA4 Events → form_submitted increasing"
- [ ] Quiz completions: "GA4 Events → quiz_completed increasing"
- [ ] Manual user journey:
  - [ ] Visit browse.html
  - [ ] Click character detail
  - [ ] Start quiz
  - [ ] Verify recommendation shown
  - [ ] Submit form (use test email)
- [ ] Performance: "Page load time <2.5s in DevTools"
- [ ] Slack #zelex-ops: Post status summary

### Evening Check (6 PM, Before Night)

- [ ] Sentry alert rules: "Verify notifications enabled"
- [ ] Slack webhook: "Test with curl -X POST $SLACK_WEBHOOK_URL"
- [ ] On-call engineer: "Confirm next engineer assigned"
- [ ] Backup status: "ls -lah db/.shopify_snapshots/ | tail -1"
- [ ] Review last 8h errors: "Sentry → Issues, any spikes?"
- [ ] Hand-off notes: "Update #zelex-ops channel with notes"

---

## Weekly Maintenance Checklist

**Purpose:** Preventive maintenance and optimization  
**Duration:** 1-2 hours  
**Performed By:** Ops or senior engineer  
**Frequency:** Friday 10 AM

### Analytics Review

- [ ] GA4 metrics: Pull weekly report (see OPERATIONS-MONITORING.md)
- [ ] Conversion funnel: Identify drop-offs
- [ ] Top pages: Verify expected pages are top viewed
- [ ] Traffic sources: Check where traffic comes from
- [ ] Device breakdown: Mobile vs desktop split

### Performance Audit

- [ ] Lighthouse score: `lighthouse https://zelex.com/ --view` (target >90)
- [ ] Page load time: GA4 → page_speed trend (target <2s avg)
- [ ] Core Web Vitals: GA4 → Web Vitals report (all green?)
- [ ] CDN cache hit rate: CloudFront → Cache statistics

### Security & Compliance

- [ ] SSL/TLS: Verify HTTPS on all pages
- [ ] PII scrubber: Check analytics for email/phone leaks
- [ ] GDPR compliance: Verify privacy policy up to date
- [ ] Dependency updates: `pip check` for Python, `npm audit` for JS

### Backup & Disaster Recovery

- [ ] Latest backup verification: "Restore test from oldest backup"
- [ ] Backup retention: "Verify 30+ days of backups available"
- [ ] Disaster recovery plan: "Review procedures, update if needed"

### Code Quality

- [ ] Test coverage: `pytest --cov=scripts tests/` (target >85%)
- [ ] Code review: All PRs merged this week reviewed
- [ ] Documentation: Runbooks up to date
- [ ] Dependency versions: Pin critical versions, review for vulnerabilities

### Stakeholder Communication

- [ ] Metrics report: Post weekly summary to Slack
- [ ] Upcoming changes: Communicate next week's deployments
- [ ] Action items: Assign owners for optimizations identified

---

## Monthly Operations Review

**Purpose:** Strategic review of operations effectiveness  
**Duration:** 1-2 hours  
**Performed By:** Ops lead + team  
**Frequency:** Last Friday of month, 3 PM

### Agenda

- [ ] Key metrics review (see OPERATIONS-MONITORING.md)
- [ ] Incident review (any critical incidents? Root causes?)
- [ ] Deployment velocity (how many deploys this month?)
- [ ] Performance trends (improving or degrading?)
- [ ] Uptime & reliability metrics
- [ ] Budget review (AWS costs, third-party services)
- [ ] Operational improvements (what went well? What to improve?)
- [ ] Plan for next month

### Incident Analysis

- [ ] Review all incidents from this month
- [ ] Classify by severity (critical, high, medium, low)
- [ ] Calculate MTTR (mean time to recovery)
- [ ] Identify root causes
- [ ] Document preventive actions for next month
- [ ] Update runbooks based on learnings

### Performance Metrics

```
Uptime: 99.8% (target: 99.5%) ✅
MTTR (Critical): 22 minutes (target: 30min) ✅
MTTR (High): 1.5 hours (target: 2hrs) ✅
Error rate: 8/day (target: <20/day) ✅
Deployment frequency: 3.2/week (target: 2-5) ✅
Test coverage: 87% (target: >85%) ✅
```

### Action Items for Next Month

| Item | Owner | Target Date |
|------|-------|-------------|
| Optimize image CDN caching | Ops-Lead | 2026-07-15 |
| Add E2E tests for forms | QA | 2026-07-10 |
| Reduce Lighthouse CLS issue | Frontend | 2026-07-20 |

---

## Emergency Response Checklist

**Purpose:** Rapid response to critical incidents  
**Duration:** 5-30 min (depending on issue)  
**Performed By:** On-call engineer + escalation  
**Triggered:** P1 severity alert

### Immediate Actions (0-5 min)

- [ ] **Acknowledge** alert: React with ✅ in Slack
- [ ] **Assess** severity: Is this really critical?
- [ ] **Alert team**: Post in #zelex-ops "INCIDENT: [description]"
- [ ] **Page on-call**: Notify lead engineer if needed
- [ ] **Don't panic**: Follow runbook procedures

### Investigation (5-15 min)

- [ ] **Identify scope**: How many users affected? Which pages/features?
- [ ] **Check monitoring**: Sentry, GA4, GitHub Actions logs
- [ ] **Root cause**: What changed? When did it start?
- [ ] **Communicate**: Keep team updated every 5 minutes

### Response (15-30 min)

- [ ] **Hotfix** (if simple): Create and deploy within 30 min
- [ ] **Workaround** (if fix complex): Implement temporary mitigation
- [ ] **Rollback** (if recent deploy caused): `git revert HEAD`
- [ ] **Verify**: Confirm fix resolves issue

### Post-Incident (After Resolved)

- [ ] **Confirm** metrics have recovered
- [ ] **Document** incident: Timestamp, impact, resolution
- [ ] **Root cause analysis**: Schedule deep-dive for next day
- [ ] **Prevent recurrence**: Action items to prevent this in future
- [ ] **Communicate**: Post incident summary to stakeholders

---

## Hotfix Deployment Checklist

**Purpose:** Safe, fast deployment of urgent fixes  
**Duration:** 15-30 min total  
**Performed By:** Any engineer (notify lead)  
**Prerequisite:** Security or revenue issue, can't wait for regular deploy

### Assessment

- [ ] Severity confirmed: Is this truly critical?
- [ ] Scope defined: Exactly what needs to change?
- [ ] Risks assessed: Minimal code changes = lower risk
- [ ] Team notified: Slack message to #zelex-ops

### Implementation

- [ ] Branch created: `git checkout -b hotfix/description`
- [ ] Minimal changes made: Only fix the critical issue
- [ ] Changes tested: Verified to work locally
- [ ] Commit message clear: "hotfix: [issue description]"

### Deployment

- [ ] Push to origin: `git push origin hotfix/description`
- [ ] PR created immediately
- [ ] PR merged ASAP (after CI passes, ideally without review wait)
- [ ] Monitor actions: Watch GitHub Actions for success
- [ ] Verify live: Check live site after 3-5 min

### Post-Deployment

- [ ] Verify fix: Confirm issue is resolved on production
- [ ] Monitor errors: Watch Sentry for next 30 min
- [ ] Team communication: "✅ Hotfix deployed" in Slack
- [ ] Clean up: Delete branch after merged
- [ ] Schedule followup: Deep-dive into root cause later

---

## Quarterly Compliance Audit

**Purpose:** Ensure operational and security compliance  
**Duration:** 4-6 hours  
**Performed By:** Operations + Security team  
**Frequency:** Q1, Q2, Q3, Q4

### Security Audit

- [ ] Dependency scan: `pip audit`, `npm audit` (no critical vulns?)
- [ ] Secrets scanning: Verify no credentials in git
- [ ] Access control: Review who has repo/server/AWS access
- [ ] SSL/TLS: Verify certificates valid, strong ciphers
- [ ] DDoS protection: Verify GitHub Pages protection active
- [ ] Incident log: Review and document any security incidents

### Operational Audit

- [ ] Backup testing: Restore from backup, verify
- [ ] Disaster recovery: Test failover procedures
- [ ] Documentation: Runbooks complete and current?
- [ ] Monitoring: Alert rules appropriate, no alert fatigue?
- [ ] On-call process: Defined SLAs, coverage, training

### Compliance & Legal

- [ ] GDPR: Privacy policy current, PII properly handled?
- [ ] CCPA: California privacy requirements met?
- [ ] Cookies: Consent management in place?
- [ ] Terms of Service: Current and accurate?
- [ ] Data retention: Old logs/backups properly deleted?

### Performance & Cost

- [ ] Cloud costs: AWS, CDN costs reviewed and optimized?
- [ ] Performance trends: Page load, error rate trends
- [ ] Capacity planning: Do we need to scale infrastructure?
- [ ] SLA compliance: Met 99.5% uptime target?

### Action Items

```
| Finding | Severity | Owner | Due Date | Status |
|---------|----------|-------|----------|--------|
| Dependency X outdated | Medium | Dev | 2026-08-31 | Open |
| PII leaked in error log | High | Ops | 2026-07-15 | Open |
| Backup not tested since Q3 | Low | Ops | 2026-08-31 | Open |
```

---

## Service Health Status Page

**Purpose:** Communicate outages/incidents to users  
**Location:** `status.zelex.com` (or similar)  
**Managed By:** Ops team

### Status Levels

| Level | Meaning | User Impact | Response |
|-------|---------|-------------|----------|
| 🟢 Operational | All systems normal | None | No action needed |
| 🟡 Degraded | Partial outage, some features down | Limited | Investigate within 30 min |
| 🔴 Outage | Major outage, site inaccessible | Severe | Page on-call, fix within 30 min |

### Incident Timeline Example

```
14:30 - 🔴 INCIDENT: Form submissions failing (discovered)
14:35 - Investigating root cause
14:40 - Identified issue: Formspree endpoint misconfigured
14:45 - Hotfix deployed
14:50 - Form submissions restored ✅
15:00 - Status updated to 🟢 Operational
```

### Notification Procedures

When incident starts:
1. Update status page to 🟡 or 🔴
2. Post to Twitter: "@zelex_official Brief outage detected. Investigating..."
3. Email subscribers (if applicable)

When resolved:
1. Update status page to 🟢
2. Post to Twitter: "Outage resolved. Thanks for your patience!"
3. Post incident summary within 24 hours

---

**END OF CHECKLISTS & PROCEDURES**

**Version:** 1.0 | **Last Updated:** 2026-06-21

Print and post on office wall for quick reference!
