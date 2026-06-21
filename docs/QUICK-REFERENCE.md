# ZELEX On-Call Quick Reference Card

**Print this or save to your phone for emergencies.**

---

## Incident Severity & Response Time

| Severity | Example | Response | Action |
|---|---|---|---|
| **P1** | Site down, payment form broken | 15 min | Page all, immediate action |
| **P2** | Feature broken, catalog stale | 1 hour | Investigate + assess |
| **P3** | Visual bug, slow load | 4 hours | Fix during business hours |
| **P4** | Typo, minor issue | Best effort | Log and batch |

---

## First Steps When Alerted

```
1. Read alert in Slack #zelex-ops
2. Check https://www.zelexdoll.com (is it up?)
3. Check https://github.com/kas1987/HowieZZ/actions (any red badges?)
4. Decide severity using matrix above
5. Follow appropriate runbook (see below)
```

---

## Top 5 Issues & Fixes

### 1️⃣ Site Down (P1)
**Runbook**: [OPERATIONS.md § Site Down](#site-down-p1)
```bash
curl -I https://www.zelexdoll.com         # Should return 200
# If 502/503: GitHub Pages down (wait & monitor)
# If 4xx: Deployment failed (check GitHub Actions)
# If timeout: Network issue (try from different location)
```

### 2️⃣ CI Build Failed (P2)
**Runbook**: [OPERATIONS.md § CI Build Failure](#ci-build-failure)
```bash
# 1. Go to https://github.com/kas1987/HowieZZ/actions
# 2. Click red workflow run
# 3. Find failed step and read error
# 4. Apply common fix (see runbook table)
# 5. Commit fix to feature branch
```

### 3️⃣ Shopify Sync Stuck (P2)
**Runbook**: [OPERATIONS.md § Shopify Sync Failed](#shopify-sync-failed)
```bash
# 1. Check artifacts: https://github.com/kas1987/HowieZZ/actions
# 2. If "401 Unauthorized": contact DevOps for token rotation
# 3. If timeout: wait 15 min, manually trigger workflow
# 4. If recurring: escalate to @lead-engineer
```

### 4️⃣ Missing Image (P3)
**Runbook**: [OPERATIONS.md § Missing or Wrong Character Image](#missing-or-wrong-character-image)
```bash
cd scripts
python build_characters.py
python make_thumbs.py
# Commit and push
```

### 5️⃣ Slow Site (P3)
**Runbook**: [OPERATIONS.md § Performance Degradation](#performance-degradation-3s-load-time)
```bash
curl -w "Total time: %{time_total}s\n" https://www.zelexdoll.com
# <2s: normal
# 2-3s: monitor
# >3s: escalate to @lead-engineer
```

---

## Emergency Contacts

**Keep these handy:**

```
ON-CALL PRIMARY:     @zelex-ops-oncall (Slack)
LEAD ENGINEER:       [Name] — [phone] — [email]
DEVOPS/SRE:          [Name] — [phone] — [email]
CEO (P1 only):       howie@zelexdoll.com
SECURITY (P1 sec):   kas41866@gmail.com
```

---

## Critical Commands

```bash
# Check site status
curl -I https://www.zelexdoll.com

# Run local build (verify everything works)
python scripts/build_orchestrator.py --json

# Run tests
python -m pytest --tb=short -q
npm test

# Start dev server
python serve.py 8000

# Check catalog
python -c "import json; c = json.load(open('db/catalog.json')); \
  print(f'Products: {len(c[\"products\"])}')"

# Revert a commit
git log --oneline | head -3
git revert <commit-hash>
git push
```

---

## Escalation Flowchart

```
Incident Detected
       ↓
Can I follow a runbook?
  YES → Follow it, document action
  NO ↓
Is it security-related?
  YES → Email security: kas41866@gmail.com immediately
  NO ↓
Is it P1 (site down)?
  YES → Page on-call lead + CEO
        Slack: @incident-commander @zelex-ops
  NO ↓
P2 (high priority)?
  YES → Page on-call lead
        Slack: @zelex-ops-oncall
  NO ↓
Continue standard triage (P3/P4)
```

---

## Tools You Need

| Tool | Use | Link |
|---|---|---|
| GitHub | Code, CI/CD, deployments | https://github.com/kas1987/HowieZZ |
| Slack | Alerts, team communication | #zelex-ops |
| Uptime Robot | Website health | https://uptimerobot.com |
| Browser DevTools | Debug JS/CSS issues | F12 in Chrome/Firefox |
| VS Code | Edit files locally | Set up git + Python |

---

## Slack Commands

```bash
# Find runbook
/search in:#zelex-ops Site Down

# Link to GitHub issue
#123

# Page on-call
@zelex-ops-oncall

# Create thread (keep channel clean)
Click "Reply in thread" on alert
```

---

## GitHub Workflow

**Create feature branch → Make fix → Push → Create PR → Merge**

```bash
git checkout -b fix/issue-name
# Edit files
git add -A
git commit -m "fix: [description]"
git push -u origin fix/issue-name

# Go to GitHub, create PR, wait for CI to pass, merge
```

---

## Before Escalating

Ask yourself:

- [ ] Did I read the error message fully?
- [ ] Did I check the relevant runbook?
- [ ] Did I try the "common fixes" in the runbook?
- [ ] Did I reproduce locally if possible?
- [ ] Did I search Slack history for similar issues?

If all no → escalate with context (error + runbook link + what you tried)

---

## Post-Incident

1. **Document**: What went wrong? What did you do?
2. **Slack thread**: Reply in the alert thread with resolution
3. **Issue**: If not routine, open GitHub issue for post-mortem
4. **Handoff**: Brief the next on-call (Sun 23:30 UTC)

---

## Quick Health Check (Do Daily)

```
☐ Site loads (https://www.zelexdoll.com)
☐ Browse works (search + filters)
☐ Contact form loads (no console errors)
☐ CI is green (no red badges)
☐ No Slack alerts (or all resolved)
☐ Catalog fresh (<8 hours old)
```

---

## Runbook Index

- [Site Down (P1)](../OPERATIONS.md#site-down-p1)
- [CI Build Failure](../OPERATIONS.md#ci-build-failure)
- [Catalog Corruption](../OPERATIONS.md#catalog-corruption)
- [Performance Degradation](../OPERATIONS.md#performance-degradation-3s-load-time)
- [Payment Form Broken](../OPERATIONS.md#payment-form-broken-p1)
- [Shopify Sync Failed](../OPERATIONS.md#shopify-sync-failed)
- [Missing Image](../OPERATIONS.md#missing-or-wrong-character-image)

**Full docs**: [OPERATIONS.md](../OPERATIONS.md)

---

## Cheat Sheet: Git Fixes

```bash
# Revert last commit (keep changes)
git revert HEAD

# Revert to stable state
git checkout -- db/catalog.json

# See what changed
git diff db/characters.json

# Find who broke it
git blame db/catalog.json | head -20

# Undo a revert
git revert <revert-commit-hash>
```

---

## SLA Targets

- **Availability**: 99.5% uptime (18 min/month downtime allowed)
- **P1 response**: Within 15 minutes
- **P1 resolution**: Within 1 hour
- **P2 response**: Within 1 hour
- **P2 resolution**: Within 4 hours
- **Deployment**: < 5 minutes after CI passes

---

## When to Call the Lead

- You've tried a runbook and it's not working
- An error message isn't in the runbook
- You're unsure about severity
- Something seems wrong but you can't diagnose it
- P1 incident and you need backup

**Don't wait — escalate early.**

---

## Final Reminders

✓ You're not expected to know everything  
✓ It's OK to ask for help  
✓ Follow runbooks, don't improvise  
✓ Document everything you do  
✓ Keep the team informed  
✓ This job is about *process*, not heroics  

---

**Printed**: [Your Date]  
**Valid Through**: Next quarter (refresh before then)  
**Contact**: On-call lead @ zelexdoll.com

---
