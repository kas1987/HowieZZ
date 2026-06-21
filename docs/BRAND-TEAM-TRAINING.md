# ZELEX Brand Team — Operations Training Guide

**Version**: 1.0  
**Date**: 2026-06-21  
**Duration**: 4 hours (self-paced) + 2 hours (hands-on session)  
**Audience**: Brand team, marketing, ops, support staff

---

## Welcome to Operations

This guide onboards the ZELEX brand team to run the Character Atlas site in production. By the end, you'll:

- Understand the architecture and data pipeline
- Respond to common issues (performance, missing images, broken forms)
- Escalate incidents appropriately
- Use monitoring and alerting tools
- Run local verification and debugging

---

## Part 1: Architecture Overview (30 min)

### What is ZELEX?

ZELEX Character Atlas is a **static, data-driven catalog site** for a luxury doll collection.

- **Frontend**: HTML, CSS, JavaScript (no framework)
- **Data**: 76 characters across 6 body families, 19 architectures, 4 series
- **Source**: Shopify product feed + hand-curated spec data
- **Deployment**: GitHub Pages (automatic on each code push)
- **Hosting**: GitHub (free tier)

### Technology Stack

```
┌─────────────────────────────────────────────────────┐
│  Browser (User)                                     │
│  index.html, browse.html, character.html, etc.     │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  GitHub Pages CDN (Production)                      │
│  https://www.zelexdoll.com                          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  Git Repository (Code + Data)                       │
│  db/catalog.json, db/characters.json                │
│  assets/site.css, assets/site.js                    │
│  .github/workflows/ (CI/CD)                         │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  Shopify Product Feed (Source of Truth)             │
│  Syncs every 6 hours                                │
│  Updates db/catalog.json + character images         │
└─────────────────────────────────────────────────────┘
```

### Key Files

| File/Folder | Purpose | Who Edits |
|---|---|---|
| `index.html`, `browse.html`, etc. | Page templates | Frontend developers |
| `assets/site.css` | Global styles | Frontend developers |
| `assets/site.js` | Global JavaScript + ZX object | Frontend developers |
| `db/catalog.json` | Product catalog (auto-generated) | Shopify sync (automated) |
| `db/characters.json` | 76 characters, metadata, images | Build scripts (automated) |
| `db/character_overlay.json` | Manual overrides (copy, tags) | Content team (hand-curated) |
| `.github/workflows/ci.yml` | Build + test + deploy | DevOps |
| `.github/workflows/shopify-sync.yml` | Sync products from Shopify | DevOps |

---

## Part 2: Data Pipeline (30 min)

### How Data Flows

```
Shopify Admin Dashboard
  ↓ (every 6 hours)
GitHub Actions Workflow (shopify-sync.yml)
  ↓
scripts/sync_shopify_feed.py
  ↓
db/catalog.json (products + variants)
  ↓
scripts/build_characters.py
  ↓
db/characters.json (76 characters with images, stories)
  ↓
CI/CD validates schema + test coverage
  ↓
GitHub Pages deploys → www.zelexdoll.com
```

### Data Update Lifecycle

**Scenario 1: New product added to Shopify**

1. Shopify admin adds product (e.g., "K-Series Body ZK999")
2. 6-hour sync trigger
3. `sync_shopify_feed.py` fetches product + images
4. `build_characters.py` generates 4 characters from that body
5. CI validates the new character records
6. Website redeploys with new character
7. Browse page now shows 77 characters (if no torso filter)

**Scenario 2: Character story needs editing**

1. Brand team edits `db/character_overlay.json` (hand-curated)
2. Commits to `main` branch
3. CI runs validation tests
4. GitHub Pages deploys
5. Character detail page shows updated story

### Important: Immutable vs. Mutable Data

| Data | Source | Mutable? | How to Change |
|---|---|---|---|
| Product info | Shopify | No (synced) | Update in Shopify |
| Character photos | Shopify | No (synced) | Upload to Shopify |
| Character stories | `character_overlay.json` | **Yes** | Edit file + commit |
| Body measurements | `body_measurements.json` | **Yes** | Edit file (hand-curated) |
| CSS/JS | `assets/` folder | **Yes** | Edit + commit |

---

## Part 3: Common Issues & How to Fix Them (60 min)

### Issue 1: Missing or Wrong Character Image

**Symptoms**: Character detail page shows placeholder/wrong hero image

**Root cause**: Shopify image not synced, or build script picked wrong photo

**Quick fix**:
```bash
# Check if character exists in db/characters.json
grep "K-ZK168B-01" db/characters.json

# Re-run character build (regenerates from Shopify)
cd scripts
python build_characters.py
python make_thumbs.py

# Commit and push
git add ../db/characters.json
git commit -m "fix: regenerate character images"
git push origin fix/character-images
```

**When to escalate**: If image is correct in Shopify but not showing, contact Shopify support.

---

### Issue 2: Character Not Appearing in Browse

**Symptoms**: A character exists but doesn't show in Browse grid or search

**Root cause**: Character marked as placeholder/concept, or not in `characters.json`

**Quick fix**:
```bash
# Check character record
python -c "
import json
with open('db/characters.json') as f:
    chars = json.load(f)
char = [c for c in chars if c['id'] == 'K-ZK168B-01'][0]
print(f\"ID: {char.get('id')}\")
print(f\"Is placeholder: {char.get('is_placeholder')}\")
print(f\"Series: {char.get('series')}\")
"

# If is_placeholder=true, you can override in character_overlay.json
# Edit db/character_overlay.json and set "is_placeholder": false
```

**When to escalate**: If character is correct but still missing, there may be a Browse page filter issue.

---

### Issue 3: Contact Form Not Working

**Symptoms**: User tries to submit inquiry, gets error or no email received

**Root cause**: INQUIRY_EMAIL or FORM_ENDPOINT not configured

**Quick fix**:
```bash
# Check contact configuration
grep -n "INQUIRY_EMAIL\|FORM_ENDPOINT" assets/site.js

# Should see:
# const INQUIRY_EMAIL = 'inquiries@zelexdoll.com';
# const FORM_ENDPOINT = 'https://formspree.io/f/xxxxx';

# If empty, edit assets/site.js and set real values
# Then commit and push
```

**Long-term**: Use Formspree or Getform for better form handling (not just email).

---

### Issue 4: Site Loads Slowly (>3 seconds)

**Symptoms**: Homepage or browse page slow to load

**Root cause**: 
1. GitHub Pages CDN slowness (temporary)
2. Large image not optimized
3. Too much JavaScript

**Quick check**:
```bash
# Measure load time
curl -w "Total time: %{time_total}s\n" https://www.zelexdoll.com

# Check JavaScript file size
ls -lh assets/site.js
# Should be <50 KB

# Check largest images
find assets/images -type f -exec ls -lh {} \; | sort -k5 -rh | head -5
```

**What to do**:
- If <2s: Normal variation, no action needed
- If 2-3s: Monitor, may be CDN cache issue
- If >3s: File a bug, escalate to engineering

---

### Issue 5: CI Build Fails

**Symptoms**: Red badge on GitHub, deploy doesn't happen

**Root cause**: Usually bad JSON, missing file, or script error

**Quick fix**:
```bash
# Look at the error in GitHub Actions
# Click the red workflow run → find failed step

# Common fixes:
# 1. JSON syntax error
python -c "import json; json.load(open('db/catalog.json'))"

# 2. Missing Python dependency
pip install pytest pytest-cov Pillow

# 3. Image file accidentally committed
git ls-files | grep -i '\.jpg\|\.png\|\.gif'

# Fix the issue and commit
git add -A
git commit -m "fix: resolve CI failure"
git push origin feature-branch
```

**When to escalate**: If you can't find the error, ask engineering team.

---

### Issue 6: Shopify Sync Failed

**Symptoms**: Workflow shows red for "Shopify Feed Sync" every 6 hours

**Root cause**: API credentials expired, Shopify API down, or network issue

**Quick fix**:
```bash
# Check Shopify sync artifacts
# Go to: GitHub → Actions → Shopify Feed Sync → latest run
# Download: shopify-sync-artifacts

# Read the log file
tail -50 db/.shopify_sync_history.jsonl

# If you see "401 Unauthorized": Token expired
# Contact: DevOps team to rotate Shopify API token in GitHub Secrets

# If you see "Connection timeout": Shopify API down
# Wait 15 minutes and manually re-trigger the workflow
```

**When to escalate**: If error is not in the runbook, contact DevOps.

---

## Part 4: Monitoring & On-Call (45 min)

### How to Know if Something is Wrong

#### 1. GitHub Actions Dashboard

Go to: https://github.com/kas1987/HowieZZ/actions

**What to look for:**
- Red badge = workflow failed
- Green badge = all good
- Recent commits should all be green

#### 2. Uptime Robot (Health Checks)

Go to: https://uptimerobot.com (or your monitoring tool)

**What to look for:**
- Website status should be GREEN
- Response time should be <2 seconds
- No red alerts in the last 24 hours

#### 3. Slack #zelex-ops Channel

This channel receives automatic alerts:
- CI failures
- Shopify sync errors
- Performance issues
- Deployment status

**What to do if you see an alert:**
1. Read the alert message
2. Check the GitHub Actions link
3. Follow the runbook in [OPERATIONS.md](../OPERATIONS.md)
4. Reply in Slack thread with status

---

### On-Call Shift

**What is on-call?**

One person is "on-call" each week and responsible for:
- Monitoring Slack alerts
- Responding within 15 min (for P1) or 1 hour (for P2)
- Following runbooks to resolve issues
- Escalating if needed

**Your shift responsibilities:**

| Time | What You Do |
|---|---|
| Start of shift (Mon 00:00 UTC) | Check that all monitoring is active |
| Throughout week | Watch Slack for alerts, respond as needed |
| Every 24 hours | Do a quick health check (site loads, browse works) |
| End of shift (Sun 23:30 UTC) | Handoff to next on-call, brief them |

**You are NOT expected to:**
- Fix complex bugs (escalate to engineering)
- Deploy new code (only follow runbooks)
- Work 24/7 (respond to alerts, then follow runbook)

---

### How to Escalate

```
I see a problem
  ↓
Can I follow a runbook?
  YES → Follow it
  NO → Post in Slack #zelex-ops: "@zelex-ops-oncall need help with [issue]"
  ↓
Is it P1 (site completely down)?
  YES → Also email: lead@zelexdoll.com, cc: ops@zelexdoll.com
  NO → Just Slack is fine
```

---

## Part 5: Hands-On Practice (120 min)

### Exercise 1: Local Setup (30 min)

**Goal**: Get the site running locally and verify you can build

**Steps:**

1. **Clone the repo** (if not already done)
   ```bash
   git clone https://github.com/kas1987/HowieZZ.git
   cd HowieZZ
   ```

2. **Check Python version**
   ```bash
   python --version
   # Should be 3.11 or higher
   ```

3. **Install dependencies**
   ```bash
   pip install pytest pytest-cov Pillow
   ```

4. **Run the build**
   ```bash
   python scripts/build_orchestrator.py --json
   echo "Build exit code: $?"
   # Should print: Build exit code: 0
   ```

5. **Start local server**
   ```bash
   python serve.py 8000
   # Open http://localhost:8000 in browser
   ```

6. **Verify pages load**
   - [ ] Homepage loads (index.html)
   - [ ] Browse shows characters (browse.html)
   - [ ] Click on a character → detail page loads
   - [ ] Quiz page loads and is interactive
   - [ ] Contact form loads

**Success criteria**: All pages load, no console errors

---

### Exercise 2: Simulate a P3 Issue (30 min)

**Scenario**: A character image is missing. Investigate and fix.

**Step 1: Corrupt an image**
```bash
# Introduce a fake issue
cd db
cp characters.json characters.json.backup
# Edit characters.json: change one hero_image URL to "/missing.jpg"
```

**Step 2: Notice the issue**
```bash
# Rebuild and test
python ../scripts/build_characters.py

# Load http://localhost:8000 and verify broken image
```

**Step 3: Fix it**
```bash
# Restore from backup
cp characters.json.backup characters.json

# Or re-run build
python ../scripts/build_characters.py
```

**Step 4: Verify**
```bash
# Reload page, image should be back
```

---

### Exercise 3: Follow a Runbook (30 min)

**Scenario**: You're on-call and see a Slack alert: "CI FAILURE: main branch build broken"

**Step 1: Investigate**
- Go to GitHub Actions
- Click the failed workflow
- Read the error message
- Search for that error in [OPERATIONS.md § CI Build Failure](#ci-build-failure)

**Step 2: Reproduce locally**
```bash
# Simulate what CI does
python -m py_compile scripts/*.py  # Check syntax
python -m pytest --tb=short -q      # Run tests
```

**Step 3: Fix (or escalate)**
- If you find the issue: fix it locally, commit, push
- If you don't: post in Slack `@lead-engineer need help with CI failure`

**Step 4: Follow up**
- Confirm the workflow passes after your fix
- Post in Slack: "Fixed: [what was wrong]"

---

### Exercise 4: Create an Incident Ticket (30 min)

**Scenario**: You notice the Shopify sync hasn't run in 8 hours.

**Step 1: Verify the issue**
```bash
# Check last sync timestamp
ls -l db/catalog.json
# Check GitHub Actions for latest Shopify sync run
```

**Step 2: Open a GitHub issue**
- Go to: https://github.com/kas1987/HowieZZ/issues/new
- Title: "Shopify Sync Stuck — Last Run 8+ Hours Ago"
- Labels: `urgent`, `operations`
- Body:
  ```
  Severity: P2
  
  Last Shopify sync: [timestamp from artifacts]
  Expected sync: every 6 hours
  
  Impact: Character catalog may be stale
  
  Runbook: See OPERATIONS.md § Shopify Sync Failed
  ```

**Step 3: Post to Slack**
- Link the issue in `#zelex-ops`
- Tag on-call lead: "@zelex-ops-oncall ⬆️ issue opened"

**Step 4: Follow up**
- Monitor the next scheduled sync (6 hours later)
- Close the issue if it auto-recovers
- Escalate if it fails again

---

## Part 6: SLAs & Expectations (15 min)

### What We Commit To

| Scenario | Response Time | Target Resolution |
|---|---|---|
| Site is down | 15 minutes | 1 hour |
| Feature broken | 1 hour | 4 hours |
| Visual bug | 4 hours | 1 business day |
| Typo or minor issue | Best effort | Next sprint |

### Your Role

As a brand team member, you:
- Monitor Slack and respond to alerts
- Follow runbooks (don't improvise)
- Escalate when stuck (don't guess)
- Document what you did (help the next person)
- Keep the team informed

### What Success Looks Like

- Site is up 99.5% of the time
- Issues resolved within SLA
- No alert fatigue (tuned thresholds)
- Incidents documented in post-mortems
- Team continuously improves

---

## Part 7: Key Documents (Reference)

These documents are your go-to guides:

1. **[OPERATIONS.md](../OPERATIONS.md)** — Runbooks, SLAs, escalation
2. **[MONITORING-CONFIG.md](MONITORING-CONFIG.md)** — Alerts, tools, setup
3. **[POSTMORTEM-TEMPLATE.md](POSTMORTEM-TEMPLATE.md)** — Incident review
4. **[SECURITY.md](../SECURITY.md)** — Security incidents
5. **[SITE-GUIDE.md](../SITE-GUIDE.md)** — Site pages and features
6. **[CLAUDE.md](../CLAUDE.md)** — Tech stack, running locally

**Bookmark these in your browser.**

---

## Part 8: Quiz (Test Your Knowledge)

### Question 1: Site Down (P1)
You wake up to a Slack alert: "zelexdoll.com is DOWN (HTTP 500)". What's your first action?

**A)** Email the CEO immediately  
**B)** Check if GitHub Pages is having downtime  
**C)** Restart the server  
**D)** Wait 15 minutes to see if it auto-fixes

**Answer**: B. Check GitHub status page + Actions for recent CI failures. → [Runbook](../OPERATIONS.md#site-down-p1)

---

### Question 2: Data Pipeline
A new product was added to Shopify. When will it appear on the website?

**A)** Immediately  
**B)** Within 1 hour  
**C)** Within 6 hours  
**D)** Next business day

**Answer**: C. Shopify sync runs every 6 hours. → [Data Pipeline](#how-data-flows)

---

### Question 3: Incident Severity
A typo in the "About" page text (misspelled "Sculptor"). What's the severity?

**A)** P1 (Critical)  
**B)** P2 (High)  
**C)** P3 (Medium)  
**D)** P4 (Low)

**Answer**: D. Fix it in the next sprint. → [Severity Matrix](../OPERATIONS.md#incident-severity-matrix)

---

### Question 4: Escalation
You're on-call. You see a CI build failure with an error you don't recognize. What do you do?

**A)** Start editing Python files to fix it  
**B)** Post in Slack: "@lead-engineer need help with CI failure [link]"  
**C)** Revert the last 10 commits  
**D)** Email everyone

**Answer**: B. Escalate clearly with context. → [Escalation Path](../OPERATIONS.md#escalation-path)

---

### Question 5: Data Integrity
You accidentally commit a large image file. The CI fails. What's the fix?

**A)** Delete the image file and re-commit  
**B)** Use `git rm --cached` to remove it from tracking, then commit  
**C)** Force push to remove it from history  
**D)** Ignore it; CI will warn

**Answer**: B. Remove from tracking without deleting locally. → [Guard Rules](../OPERATIONS.md#ci-build-failure)

---

## Checklist: Ready for On-Call?

Before your first shift, verify:

- [ ] You can log into GitHub with proper access
- [ ] You've read OPERATIONS.md completely
- [ ] You can run local build (`python scripts/build_orchestrator.py`)
- [ ] You can clone, edit, commit, and push a test branch
- [ ] You know the on-call rotation for this week
- [ ] You have Slack notifications enabled for `#zelex-ops`
- [ ] You know how to contact the lead engineer (phone/email)
- [ ] You've done the hands-on exercises above
- [ ] You've reviewed the SLAs and incident severity matrix
- [ ] You know where to find runbooks (this guide + OPERATIONS.md)

**First shift?** Schedule a 30-min walkthrough with the previous on-call.

---

## Getting Help

| Question | Answer | Where |
|---|---|---|
| How do I respond to X issue? | See runbook | OPERATIONS.md |
| What's the SLA for Y? | See matrix | OPERATIONS.md § SLAs |
| I need to escalate | Use path | OPERATIONS.md § Escalation Path |
| I'm stuck on Z | Ask for help | Slack @lead-engineer |
| I found a bug | Document it | GitHub issue + [POSTMORTEM-TEMPLATE.md](POSTMORTEM-TEMPLATE.md) |

---

## Feedback & Improvement

After your first on-call shift:

1. Note anything confusing (unclear runbook, missing tool access)
2. Post in Slack: "Feedback from this week's on-call: [items]"
3. We'll update this guide to be clearer

---

**You've got this! Welcome to the ZELEX ops team.**

---

**Version**: 1.0  
**Last Updated**: 2026-06-21  
**Contact**: Lead Engineer  
**Next Review**: After first cohort completes training
