# ZELEX Operations — Quick Reference Card

**Print this page and keep at your desk!**

---

## 🚨 Emergency Contact

| Situation | Contact | Response Time |
|-----------|---------|---|
| Site Down (P1) | @lead-engineer + page on-call | <5 min |
| High Error Rate (P1) | @lead-engineer | <15 min |
| Security Issue | security@zelex.com | <1 hour |
| General Questions | ops-lead@zelex.com | <24 hours |

**Slack: #zelex-ops** (team channel)

---

## ⏰ Daily Schedule (On-Call)

| Time | Task | Duration |
|------|------|----------|
| **8:00 AM** | Morning Health Check | 15 min |
| **2:00 PM** | Peak Hours Monitoring | 15 min |
| **6:00 PM** | Evening Check | 15 min |
| **24/7** | Monitor for alerts | Continuous |

---

## 🔧 Common Commands

### Check Site Status
```bash
curl -I https://zelex.com/
curl -s https://zelex.com/db/characters.json | jq '.characters | length'
```

### Run Health Check
```bash
python scripts/check_db.py --validate-all
```

### Build Pipeline
```bash
python scripts/build_orchestrator.py        # Full pipeline
python scripts/build_orchestrator.py --dry-run  # Preview
python scripts/build_orchestrator.py --resume   # Resume from failure
```

### Shopify Sync
```bash
python scripts/sync_shopify_feed.py                    # Full sync
python scripts/sync_shopify_feed.py --dry-run          # Preview
python scripts/sync_shopify_feed.py --report           # Show deltas
```

### Deploy to Production
```bash
git checkout main && git pull
git checkout -b feature/name
# Make changes
git add . && git commit -m "..."
git push origin feature/name
# Create PR, merge when CI passes
```

### Hotfix (Emergency Only)
```bash
git checkout -b hotfix/critical-issue
# Make minimal changes
git add . && git commit -m "hotfix: [description]"
git push origin hotfix/critical-issue
# Create PR, merge immediately after CI
```

### Rollback Last Deploy
```bash
git revert HEAD && git push origin main
```

### Restore from Backup
```bash
cp backups/zelex-atlas-YYYYMMDD-HHMMSS/db-backup/* db/
git add db/ && git commit -m "recovery: Restore from backup"
git push origin main
```

---

## 🎯 Key Metrics (GA4 Dashboard)

| Metric | Target | How to Check |
|--------|--------|---|
| **Users (daily)** | 100-300 | GA4 → Acquisition |
| **Bounce Rate** | <35% | GA4 → Engagement |
| **Page Load** | <2.5s | GA4 → page_speed event |
| **Form Submissions** | 10-50/day | GA4 → form_submitted event |
| **Error Rate** | <20/day | Sentry or GA4 → error_event |

---

## ⚠️ Critical Alert Thresholds

| Alert | Threshold | Action |
|-------|-----------|--------|
| **Site Returns 500** | Any | Immediate: Follow Incident Runbook |
| **Form Not Submitting** | 0 events for 30min | Urgent: Test locally, hotfix |
| **Image 404 Errors** | >5% of requests | Urgent: Check CDN, verify S3 |
| **Error Spike** | >100/hour | High: Check Sentry, identify cause |
| **Slow Pages** | >3s avg for 30min | High: Run Lighthouse, optimize |

---

## 📋 Weekly Checklist

Every Friday at 4 PM:

- [ ] Pull GA4 metrics (copy to dashboard)
- [ ] Check conversion funnel (drill into drops)
- [ ] Review Sentry issues (any new patterns?)
- [ ] Verify latest deployment successful
- [ ] Post summary to #zelex-ops
- [ ] Plan next week's work

---

## 📚 Documentation Map

**Quick Answer?** → FAQ (OPERATIONS-RUNBOOKS.md section 9)

**Something Broken?** → Incident Playbook (OPERATIONS-RUNBOOKS.md section 8)

**How to Do X?** → Relevant Runbook (OPERATIONS-RUNBOOKS.md sections 1-7)

**Daily Tasks?** → Daily Checklist (OPERATIONS-CHECKLISTS.md)

**Monitoring Setup?** → OPERATIONS-MONITORING.md

**Full Details?** → OPERATIONS-DELIVERY-SUMMARY.md

---

## 🚀 30-Second Emergency Response

**Site is down (500 errors):**
1. Check GitHub Actions: https://github.com/howiez/zelex-atlas/actions
2. Last deploy failed? → `git revert HEAD && git push`
3. Still down? → Restore from backup (see Common Commands)
4. Page on-call engineer: @lead-engineer

**Form not working:**
1. Test locally: `python serve.py` → submit form
2. Check console (F12): any JS errors?
3. Check Sentry: https://sentry.io
4. Hotfix needed? → Follow hotfix procedure above

**Images won't load (404s):**
1. Check CDN: `curl -I https://d123456789abc.cloudfront.net/image.jpg`
2. Check S3: `aws s3 ls s3://zelex-atlas-prod/` | grep image
3. Re-upload? → `python scripts/push_assets_to_cdn.py --apply`
4. Invalidate cache: `aws cloudfront create-invalidation --distribution-id E1234ABCD5678 --paths "/*"`

---

## 🔐 Critical Passwords & Tokens

⚠️ **NEVER commit to GitHub!** Store in:
- GitHub Secrets (for Actions)
- Environment variables (local)
- AWS Secrets Manager (if using)

**Required Credentials:**
- `SHOPIFY_ACCESS_TOKEN` (Shopify API)
- `SHOPIFY_STORE_URL` (Store domain)
- `SLACK_WEBHOOK_URL` (Notifications)
- `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` (S3/CloudFront)

Verify set correctly:
```bash
echo "Shopify: $SHOPIFY_STORE_URL"
echo "Slack: ${SLACK_WEBHOOK_URL:0:30}..."
```

---

## 📊 Monitoring Dashboard Links

| Tool | URL | Purpose |
|------|-----|---------|
| **GA4** | https://analytics.google.com | User behavior, conversions |
| **Sentry** | https://sentry.io/organizations/zelex/ | Error tracking, issues |
| **GitHub Actions** | https://github.com/howiez/zelex-atlas/actions | Deployments, CI/CD |
| **AWS CloudWatch** | https://console.aws.amazon.com/cloudwatch/ | CDN metrics (if AWS) |
| **Site** | https://zelex.com | Production site |

---

## 🆘 Runbook Quick Find

Need help with...

- **Images not loading?** → Runbook 1 & 6
- **Character data wrong?** → Runbook 2
- **Shopify prices wrong?** → Runbook 3
- **Deploy failed?** → Runbook 4
- **Analytics broken?** → Runbook 5
- **Images slow?** → Runbook 6
- **Urgent fix needed?** → Runbook 7
- **Not in runbooks?** → Incident Playbook or FAQ

---

## ✅ Before You Deploy

- [ ] `git status` clean (nothing uncommitted)
- [ ] Tests pass: `python -m pytest tests/`
- [ ] Build works: `python scripts/build_orchestrator.py`
- [ ] No secrets in code
- [ ] PR reviewed & approved
- [ ] CI/CD green checkmarks

---

## 📞 Weekly On-Call Duties

**Monday-Sunday:**
- [ ] Assigned to on-call rotation
- [ ] Phone/Slack reachable
- [ ] Can respond <15 min to critical alerts
- [ ] Run daily checks (8 AM, 2 PM, 6 PM)
- [ ] Document any incidents
- [ ] Hand off to next engineer Sunday night

---

## 🎓 Getting Help

**I don't know how to...**

1. Check FAQ first (50+ Q&A)
2. Search Runbooks (Ctrl+F)
3. Ask in #zelex-ops Slack
4. Email ops-lead@zelex.com
5. Schedule pairing session with senior op

**Remember:** Every question has been asked before. It's in the docs somewhere!

---

## 📝 Incident Template

When something breaks, log it:

```
INCIDENT LOG ENTRY
Date/Time: 2026-06-21 14:30:00 UTC
Severity: P1 (Critical) | P2 (High) | P3 (Low)
Issue: [Brief description]
Impact: [Who/what affected, how many users]
Duration: [Start time - End time] = X minutes
Root Cause: [What caused it]
Resolution: [How was it fixed]
Lessons: [What we'll do differently next time]
```

File location: `INCIDENT_LOG.txt`

---

## 🎯 Mission: Uptime

**Our Goal:** 99.5% uptime, <30 min MTTR for critical issues

**Your Role:** Follow procedures, stay calm, respond fast

**The Docs:** Everything you need. Print, reference, improve.

---

**Last Updated:** 2026-06-21  
**Version:** 1.0  
**Status:** Ready for production

Questions? → ops-lead@zelex.com or #zelex-ops Slack
