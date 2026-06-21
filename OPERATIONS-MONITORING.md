# ZELEX Operations Monitoring & Health Checks

**Version:** 1.0 | **Last Updated:** 2026-06-21

Comprehensive monitoring guide for the ZELEX Character Atlas production environment.

---

## Table of Contents

1. [Monitoring Stack](#monitoring-stack)
2. [Key Performance Indicators (KPIs)](#key-performance-indicators-kpis)
3. [Daily Health Checks](#daily-health-checks)
4. [Weekly Metrics Review](#weekly-metrics-review)
5. [Alert Rules & Thresholds](#alert-rules--thresholds)
6. [Dashboard Setup](#dashboard-setup)
7. [Logging & Audit Trails](#logging--audit-trails)
8. [Disaster Recovery & Backups](#disaster-recovery--backups)

---

## Monitoring Stack

### Components

| Tool | Purpose | Access |
|------|---------|--------|
| **Google Analytics 4** | User behavior, conversions, pageviews | https://analytics.google.com |
| **Sentry.io** | Error tracking, performance monitoring | https://sentry.io/organizations/zelex/ |
| **GitHub Actions** | Build & deployment pipeline | https://github.com/howiez/zelex-atlas/actions |
| **AWS CloudWatch** | CDN & S3 metrics (if using AWS) | https://console.aws.amazon.com/cloudwatch/ |
| **Slack** | Alert notifications | #zelex-ops channel |
| **Custom Scripts** | Local system health checks | `scripts/health_check.py` |

---

## Key Performance Indicators (KPIs)

### Traffic & Engagement

```
KPI: Monthly Active Users (MAU)
Definition: Unique users visiting site per month
Target: 50,000+
Measurement: GA4 → Users metric
Alert: <40,000 MAU = investigate
```

```
KPI: Average Session Duration
Definition: Time spent per session (seconds)
Target: >180 seconds (3 minutes)
Measurement: GA4 → Engagement metric
Alert: <120 seconds = content issue (quiz too short? form unclear?)
```

```
KPI: Bounce Rate
Definition: % of sessions where user leaves without interaction
Target: <35%
Measurement: GA4 → Engagement
Alert: >50% = site usability issue, check Lighthouse score
```

### Conversion Funnel

```
KPI: Browse → Quiz Conversion
Definition: % of browse.html views that start quiz
Target: 15-20%
Measurement: GA4 Funnels → step 1 (page_view /browse) → step 2 (event quiz_started)
Alert: <10% = quiz visibility/UX issue, check click tracking
```

```
KPI: Quiz → Recommendation Conversion
Definition: % of quiz starts that show recommendations
Target: 95%+ (should be near 100%)
Measurement: GA4 Events → quiz_completed / recommendation_shown ratio
Alert: <90% = recommendation algorithm broken, see Runbook 5
```

```
KPI: Quiz → Form Submission Conversion
Definition: % of recommendations that lead to form submission
Target: 40-50%
Measurement: GA4 Funnels → event quiz_completed → event form_submitted
Alert: <30% = form UX issue, test form locally
```

```
KPI: Overall Funnel Conversion
Definition: Browse → Quiz → Form submission
Target: 3-5%
Measurement: (Form submissions / Browse page views)
Alert: <2% = investigate each step
```

### Performance

```
KPI: Average Page Load Time
Definition: Time until page interactive (ms)
Target: <2000ms (2 seconds)
Measurement: GA4 → page_speed event
Alert: >3000ms = CDN issue or code regression, run Lighthouse
```

```
KPI: Core Web Vitals
Definition: Google's user experience metrics
- LCP (Largest Contentful Paint): <2.5s ✓
- FID (First Input Delay): <100ms ✓
- CLS (Cumulative Layout Shift): <0.1 ✓
Target: All "Good" (green)
Measurement: GA4 → Web Vitals report
Alert: Any "Poor" = performance regression, investigate
```

```
KPI: Lighthouse Score
Definition: Automated site quality audit (0-100)
Target: >90
Measurement: lighthouse https://zelex.com/ (or in CI)
Alert: <85 = code quality issue
```

### Reliability

```
KPI: Error Rate
Definition: # of errors per hour
Target: <5 errors/hour
Measurement: Sentry → Issues
Alert: >50 errors/hour = incident
```

```
KPI: Uptime
Definition: % of time site is accessible (200 OK)
Target: 99.5%+
Measurement: Custom uptime monitor
Alert: <99% = infrastructure issue
```

```
KPI: Deployment Frequency
Definition: # of deployments per week
Target: 2-5 (depending on workload)
Measurement: GitHub Actions → Workflow runs
Alert: 0 deploys in 2 weeks = no activity (check if backlog exists)
```

```
KPI: Mean Time to Recovery (MTTR)
Definition: Time from incident detection to resolution
Target: <30 min for critical, <2 hours for high
Measurement: Incident logs
Alert: Log any incident >2 hours to identify bottlenecks
```

### Business

```
KPI: Inquiry Submission Count
Definition: # of form submissions per day
Target: 10-50 (depends on campaign)
Measurement: GA4 → event form_submitted daily count
Alert: <5/day (after controlling for traffic) = funnel problem
```

```
KPI: Character Interest Distribution
Definition: Views per character
Target: Top 5 characters get 30-40% of views (concentrated interest)
Measurement: GA4 → Page views /character.html?id=* by ID
Alert: Imbalanced (one character >60%) = marketing focus issue
```

```
KPI: Shopify Inventory Accuracy
Definition: % of Atlas inventory matching Shopify
Target: 100%
Measurement: Last Shopify sync delta report
Alert: <99% = sync issue, see Runbook 3
```

---

## Daily Health Checks

### 8:00 AM Check

**Objective:** Verify overnight stability

```bash
#!/bin/bash
# scripts/health_check_morning.sh

echo "🌅 Morning Health Check ($(date))"
echo "================================================"

# 1. Availability
echo "Availability:"
for page in index browse quiz contact; do
  status=$(curl -s -o /dev/null -w "%{http_code}" https://zelex.com/$page.html)
  [ "$status" == "200" ] && echo "  ✓ $page.html" || echo "  ✗ $page.html: $status"
done

# 2. Database check
echo ""
echo "Database Integrity:"
python scripts/check_db.py --validate-all 2>&1 | head -5

# 3. Image serving
echo ""
echo "Image Serving:"
for image in K-KM00-01-320.jpg M-MS00-01-320.jpg; do
  status=$(curl -s -I "https://zelex.com/assets/thumbs/$image" 2>&1 | head -1 | grep -o "[0-9][0-9][0-9]")
  [ "$status" == "200" ] && echo "  ✓ $image" || echo "  ✗ $image: $status"
done

# 4. Analytics
echo ""
echo "Analytics Status:"
# Check GTM container is loaded
gtm_check=$(curl -s https://zelex.com/assets/ga4-init.js | grep -c "googletagmanager")
[ "$gtm_check" -gt 0 ] && echo "  ✓ GTM container loaded" || echo "  ✗ GTM not found"

# 5. Last deploy
echo ""
echo "Last Deployment:"
git log -1 --pretty="format:%h %ad %s" --date=relative

# 6. Error check (Sentry)
echo ""
echo "Error Count (last 24h):"
echo "  (Check Sentry dashboard manually)"

echo ""
echo "✅ Morning check complete"
```

**Success Criteria:**
- [ ] All main pages return 200 OK
- [ ] Database validation passes
- [ ] Images loading from CDN
- [ ] GTM container loaded
- [ ] Error count <20 in last 24h

**If Any Fails:** Escalate to senior engineer, follow Incident Response (Runbook 8)

---

### 2:00 PM Check (Peak Hours)

**Objective:** Monitor conversion funnel during peak traffic

```bash
# Check real-time conversion metrics
# GA4 Dashboard → Real-time view
# 1. Current users: should be >50 (depending on campaign)
# 2. Quiz started events: should be increasing
# 3. Form submitted events: should be increasing

# Look for anomalies:
# - No quiz events for 30+ min → quiz form broken
# - No form events for 1hr → form submission failing
# - High error rate spike → JS issue

# Quick test (as user):
# 1. Navigate to browse.html
# 2. Click character detail
# 3. Complete quiz
# 4. Verify recommendation shows
# 5. Submit form (test email)
```

---

### 6:00 PM Check (Before Night)

**Objective:** Prepare for monitoring-free overnight period

```bash
# 1. Check Sentry alerts configured
# https://sentry.io → Alerts → should have notifications enabled

# 2. Verify Slack webhook active
# Try test alert: curl -X POST $SLACK_WEBHOOK_URL -d "Test"

# 3. Check on-call engineer is assigned
# (Verify Pagerduty or manual on-call list)

# 4. Review last 8 hours of metrics
# GA4: any unusual spikes/drops?
# Errors: any new error types?
# Performance: any degradation?

# 5. Verify backups completed
ls -lah db/.shopify_snapshots/ | tail -5
# Should see snapshot from today
```

---

## Weekly Metrics Review

**Schedule:** Friday 4:00 PM  
**Attendees:** Ops, Product, Marketing  
**Duration:** 30 minutes

### Agenda

```
1. Traffic & Engagement (5 min)
   - Weekly active users
   - Session duration
   - Bounce rate
   - Top pages

2. Conversion Funnel (10 min)
   - Browse → Quiz: XX% conversion
   - Quiz → Form: XX% conversion
   - Overall funnel: XX%
   - Identify drop-off points

3. Performance (5 min)
   - Page load time trend
   - Lighthouse score
   - Core Web Vitals
   - Error rate

4. Incidents & Blockers (5 min)
   - Any incidents this week?
   - Deployment frequency
   - Testing coverage

5. Action Items (5 min)
   - Identify optimizations
   - Plan next week's work
```

### Metrics Report Template

```
📊 ZELEX Weekly Report (Jun 16-22, 2026)

Traffic:
  • Users: 8,341 (↑12% from previous week)
  • Sessions: 11,204
  • Pageviews: 34,567
  • Avg Session Duration: 3m 12s

Conversions:
  • Browse → Quiz: 16.3% (↑2% from target)
  • Quiz → Form: 42.1% (↓5% from target)
  • Overall Conv Rate: 3.1%
  • Form Submissions: 342 (↑8%)

Performance:
  • Avg Page Load: 1.8s (✓ good)
  • Lighthouse: 94/100
  • Errors: 12 total (↓50% from previous week)

Top Performers:
  • K-KM00-01 (Kira): 523 views
  • M-MS00-01 (Sage): 487 views
  • I-IC00-01 (Iris): 412 views

Action Items:
  - Investigate quiz→form drop (was 47%, now 42%)
  - A/B test new CTA copy
  - Optimize character detail page images (CLS issue)
```

---

## Alert Rules & Thresholds

### Critical Alerts (Page On-Call Immediately)

| Alert | Threshold | Action |
|-------|-----------|--------|
| Site Down | HTTP 500+ for 2 min | CRITICAL: Follow Runbook 8, Incident 2 |
| Error Rate Spike | >100 errors/hour | P1: Check Sentry, identify root cause |
| Form Not Submitting | 0 form_submitted events for 30 min | P1: Test locally, hotfix |
| Image 404 Rate | >5% of image requests | P1: Check CDN, verify S3 bucket |

### High Priority Alerts (Respond <30 min)

| Alert | Threshold | Action |
|-------|-----------|--------|
| Slow Page Load | >3s avg for 30 min | Investigate performance, run Lighthouse |
| Funnel Conversion Drop | >50% drop from baseline | Check quiz logic, form submission |
| Deployment Failed | CI/CD failed 3x in row | Debug build, check logs |
| Shopify Sync Error | Sync failed 2x in row | Check API credentials, retry manually |

### Low Priority Alerts (Respond <2 hours)

| Alert | Threshold | Action |
|-------|-----------|--------|
| High Bounce Rate | >60% | Review page UX, check if content is clear |
| Low Traffic | <50% of daily average | Check if marketing campaign running, or seasonal low |
| Sentry New Issue | New error type detected | Review error, plan fix for next release |

### Slack Integration

```
# In GitHub Actions, add post-deployment notification:

- name: Notify Slack
  run: |
    curl -X POST $SLACK_WEBHOOK \
      -H 'Content-Type: application/json' \
      -d '{
        "text": "ZELEX Deployment Status",
        "blocks": [
          {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "✅ *Deployment Complete*\nVersion: ${{ github.sha }}\nTime: $(date)"}
          }
        ]
      }'
```

---

## Dashboard Setup

### Google Analytics 4 Dashboard

**URL:** https://analytics.google.com → ZELEX Atlas property

**Recommended Cards:**

1. **Real-Time Users** (top-left)
   - Current users on site
   - Refresh: 1 min
   - Target: >50 during peak hours

2. **Conversion Funnel** (center)
   - 4 steps: Browse → Quiz → Recommendation → Form
   - Shows drop-off at each stage
   - Update daily

3. **Top Characters** (right)
   - 10 most-viewed characters
   - Helps identify marketing success
   - Update daily

4. **Page Speed** (bottom-left)
   - Average page load time
   - Core Web Vitals status
   - Alert if >2.5s

5. **Error Events** (bottom-right)
   - Error count by type
   - Alert if spike occurs
   - Update hourly

### Looker Studio Dashboard (Advanced)

Create interactive, shareable dashboard:

1. Data source: Google Analytics 4
2. Add cards:
   - Sessions by traffic source
   - Conversion rate over time
   - Top converting characters
   - Funnel progression
3. Filters: Date range, traffic source, device
4. Share with marketing team

---

## Logging & Audit Trails

### Application Logs

```
Location: db/.application_logs.jsonl
Format: JSON Line (one JSON object per line)
Retention: 90 days (auto-rotated)

Example entry:
{
  "timestamp": "2026-06-21T14:30:45Z",
  "level": "INFO",
  "component": "build_orchestrator",
  "message": "Pipeline completed",
  "duration_seconds": 47,
  "stage_details": {
    "db": "12s",
    "profiles": "5s",
    "characters": "8s"
  }
}
```

### Deployment Audit Log

```
Location: DEPLOYMENT_LOG.txt
Entries: Every deployment
Format:

[2026-06-21 14:30:45] DEPLOYMENT START
  Branch: main
  Commit: abc123def456
  Changes: 5 files modified
  
[2026-06-21 14:32:10] BUILD COMPLETE (47s)
[2026-06-21 14:34:20] TESTS PASSED (210 tests)
[2026-06-21 14:35:00] DEPLOYED TO GITHUB PAGES
[2026-06-21 14:35:15] DEPLOYMENT COMPLETE ✅

Viewable: git log --oneline
```

### Data Change Audit Log

```
Location: db/.curation_log.jsonl
Logged: Every change to character data via overlay

Example:
{
  "timestamp": "2026-06-21T10:15:30Z",
  "action": "update_character",
  "character_id": "K-KM00-01",
  "fields_changed": ["story", "personality"],
  "old_value": {"story": "...old..."},
  "new_value": {"story": "...new..."},
  "editor": "kas1987+",
  "commit_hash": "abc123"
}
```

### Shopify Sync Log

```
Location: db/.shopify_sync_history.jsonl
Logged: Every sync run

Example:
{
  "timestamp": "2026-06-21T20:30:45Z",
  "status": "complete",
  "products_synced": 247,
  "duration_seconds": 154,
  "deltas": {
    "price_changes": 3,
    "inventory_updates": 12,
    "new_products": 0,
    "discontinued": 0
  },
  "errors": []
}
```

---

## Disaster Recovery & Backups

### Backup Strategy

**Frequency:** Automatic (every 6 hours) + manual before risky operations

**What's Backed Up:**
- `db/characters.json` (character data)
- `db/body_profiles.json` (WHR classifications)
- `db/shopify_sku_mapping.json` (inventory)
- `.shopify_snapshots/` (versioned sync snapshots)

**Storage:**
- Local: `backups/zelex-atlas-YYYYMMDD-HHMMSS/`
- Cloud: (optional) S3 backup bucket

### Backup Locations

```
backups/
├── zelex-atlas-20260621-080000/
│   ├── db-backup/
│   │   ├── characters.json
│   │   ├── body_profiles.json
│   │   └── shopify_sku_mapping.json
│   └── assets-backup/
│       └── (all images)
├── zelex-atlas-20260621-140000/
└── zelex-atlas-20260621-200000/
```

### Recovery Procedures

**Scenario: Database Corrupted**

```bash
# Step 1: Stop all processes
pkill -f "build_orchestrator.py"

# Step 2: Identify good backup
ls -lah backups/ | head -20

# Step 3: Restore
cp backups/zelex-atlas-20260621-140000/db-backup/* db/

# Step 4: Verify
python scripts/check_db.py --validate-all

# Step 5: Re-deploy
git add db/
git commit -m "recovery: Restore from backup (data corruption)"
git push origin main
```

**Scenario: Images Lost**

```bash
# Step 1: Check CDN/S3 (may still be available)
aws s3 ls s3://zelex-atlas-prod/ | wc -l

# Step 2: If CDN intact, re-sync locally
python scripts/download_assets.py --from-cdn

# Step 3: If CDN also lost, restore from backup
cp -r backups/zelex-atlas-20260621-140000/assets-backup/* assets/

# Step 4: Re-upload to CDN
python scripts/push_assets_to_cdn.py --apply
```

### Testing Recovery

**Monthly:** Restore from oldest backup and verify it works

```bash
# 1st of each month
BACKUP_DIR=$(ls -d backups/* | head -1)
cp -r $BACKUP_DIR/db-backup/* db.test/
python scripts/check_db.py --database db.test/catalog.db --validate-all
# Should succeed, confirming backup is valid

# If test fails: backup is corrupted, fix backup strategy
```

---

## On-Call Responsibilities

### Weekly On-Call Engineer

**Hours:** Monday 12:00 AM (UTC-7) → Sunday 11:59 PM  
**Response Time:** <15 min for alerts  
**Escalation:** Notify lead engineer if unsure

### On-Call Checklist (Start of Week)

- [ ] Add name to on-call rotation
- [ ] Test Slack notifications (verify alerts come through)
- [ ] Review Sentry alert rules
- [ ] Read through latest incident log
- [ ] Verify you can SSH to servers (if applicable)
- [ ] Confirm knowledge of Hotfix process (Runbook 7)

### Daily On-Call Tasks

**Morning (8 AM):**
- [ ] Run health check
- [ ] Review overnight errors in Sentry
- [ ] Check Shopify sync completed

**Afternoon (2 PM):**
- [ ] Monitor conversion funnel
- [ ] Test quiz/form as user
- [ ] Check performance metrics

**Evening (6 PM):**
- [ ] Verify backups completed
- [ ] Confirm Slack alerts enabled
- [ ] Hand-off to next engineer (if rotating hourly)

### Incident Response (During On-Call)

When alert fires:

1. **Acknowledge** receipt within 5 min (Slack reaction or message)
2. **Assess** severity: is this a P1 (site down) or P3 (typo)?
3. **Respond** per Incident Playbook (Runbook 8)
4. **Escalate** if needed: ping @lead-engineer in Slack
5. **Document** incident in INCIDENT_LOG.txt with:
   - Timestamp
   - Description
   - Impact
   - Resolution time
   - Root cause (if known)

### End-of-Week Hand-Off

Before your rotation ends:
- [ ] Document any ongoing issues
- [ ] Pass Sentry context to next on-call engineer
- [ ] Leave notes in #zelex-ops Slack channel
- [ ] Update runbooks if procedures changed

---

**END OF MONITORING GUIDE**

**Version:** 1.0 | **Last Updated:** 2026-06-21

For questions, contact ops-lead@zelex.com
