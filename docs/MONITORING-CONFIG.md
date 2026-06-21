# Monitoring & Alerting Configuration

**Version**: 1.0  
**Last Updated**: 2026-06-21  
**Status**: Ready for Setup  
**Owner**: DevOps / SRE

---

## Overview

This document describes the monitoring, alerting, and observability setup for ZELEX brand operations. All checks are automated where possible and feed into `#zelex-ops` Slack channel.

---

## Monitoring Stack

### Services to Monitor

| Service | Type | Health Check | Tool | Frequency |
|---|---|---|---|---|
| **Website (Production)** | HTTP | GET / → 200 | Uptime Robot | 5 min |
| **Website (Staging)** | HTTP | GET /index.html → 200 | Uptime Robot | 5 min |
| **GitHub Pages Deploy** | Deployment | Latest workflow status | GitHub API | 15 min |
| **CI Build (main)** | Pipeline | Last 3 runs must be ✓ | GitHub Actions | 15 min |
| **Shopify Sync Job** | Scheduled Task | Last run success | GitHub Actions | 6 hours |
| **Catalog Freshness** | Data Quality | `/db/catalog.json` timestamp | Custom script | 1 hour |
| **Image CDN** | HTTP | Sample 10 random images | Uptime Robot | 15 min |
| **Analytics Pipeline** | Data | Event ingestion rate | Analytics Dashboard | 1 hour |

---

## Alert Configuration

### Alert Rules (Slack → #zelex-ops)

#### Rule 1: Site Down (P1)

**Trigger**: Website returns non-2xx for 2 consecutive checks (10 min total)

```
Condition: HTTP Status != 200
Count: 2 failures in a row
Duration: ≥10 minutes
Alert Level: CRITICAL (Red flag emoji)
Slack Message:
  :alert: CRITICAL: zelexdoll.com is DOWN
  Production: [Status]
  Staging: [Status]
  Last successful check: [timestamp]
  Action: @zelex-ops-oncall investigate immediately
```

**Response SLA**: 15 min  
**Runbook**: [OPERATIONS.md § Site Down](#site-down-p1)

---

#### Rule 2: CI Build Failure (P2)

**Trigger**: 2 consecutive failed builds on `main`

```
Condition: GitHub Actions workflow = FAILURE
Branch: main
Count: 2 in a row
Alert Level: HIGH (Orange flag emoji)
Slack Message:
  :warning: CI FAILURE: main branch build broken
  Workflow: [name]
  Last failure: [timestamp]
  Failed step: [step name]
  Logs: [link to GitHub Actions]
  Action: Primary on-call to investigate
```

**Response SLA**: 1 hour  
**Runbook**: [OPERATIONS.md § CI Build Failure](#ci-build-failure)

---

#### Rule 3: Shopify Sync Failed (P2)

**Trigger**: Shopify sync workflow returns exit code != 0

```
Condition: GitHub Actions shopify-sync.yml = FAILURE
Alert Level: HIGH (Orange flag emoji)
Slack Message:
  :warning: SHOPIFY SYNC FAILED
  Status: [sync status]
  Products affected: [count]
  Error: [from sync log]
  Last successful sync: [timestamp]
  Action: Re-trigger manually or investigate
```

**Response SLA**: 1 hour  
**Runbook**: [OPERATIONS.md § Shopify Sync Failed](#shopify-sync-failed)

---

#### Rule 4: Catalog Corruption (P2)

**Trigger**: `catalog.json` is invalid JSON or missing required keys

```
Condition: Parse catalog.json → Error
OR: catalog['products'] is empty
OR: catalog['products'].length < 50 (anomalous drop)
Alert Level: HIGH (Orange flag emoji)
Slack Message:
  :warning: CATALOG CORRUPTION DETECTED
  Catalog status: [valid/invalid]
  Product count: [number] (expected: ~150)
  Series count: [number] (expected: 4)
  Last clean timestamp: [when]
  Action: Restore from backup
```

**Response SLA**: 1 hour  
**Runbook**: [OPERATIONS.md § Catalog Corruption](#catalog-corruption)

---

#### Rule 5: Performance Degradation (P3)

**Trigger**: Homepage response time > 3 seconds (p99 latency)

```
Condition: Response time > 3s
Duration: ≥15 minutes
Alert Level: MEDIUM (Yellow flag emoji)
Slack Message:
  :hourglass: PERFORMANCE ALERT
  p99 latency: [X seconds]
  p95 latency: [X seconds]
  Status page: [link]
  Action: Monitor — investigate if sustained >30 min
```

**Response SLA**: 4 hours  
**Runbook**: [OPERATIONS.md § Performance Degradation](#performance-degradation-3s-load-time)

---

#### Rule 6: Image Serving Errors (P3)

**Trigger**: 5+ image 404s in 1 hour (sample monitoring)

```
Condition: Image CDN returns 404/403/5xx
Count: ≥5 errors
Duration: 1 hour window
Alert Level: MEDIUM (Yellow flag emoji)
Slack Message:
  :broken_image: IMAGE CDN ALERTS
  Errors in last hour: [count]
  Sample URL: [failed image]
  Cache header: [cache-control value]
  Action: Check CDN status, may need cache bust
```

**Response SLA**: 4 hours  
**Runbook**: [TBD - CDN recovery]

---

#### Rule 7: Data Freshness (P3)

**Trigger**: Catalog older than 8 hours (no sync in 8+ hours)

```
Condition: Catalog timestamp < now() - 8 hours
OR: Shopify sync hasn't run for 8 hours
Alert Level: MEDIUM (Yellow flag emoji)
Slack Message:
  :warning: CATALOG FRESHNESS
  Last sync: [X hours ago]
  Products synced: [count]
  Action: Investigate if Shopify sync is stuck
```

**Response SLA**: 4 hours  
**Runbook**: [OPERATIONS.md § Shopify Sync Failed](#shopify-sync-failed)

---

### Alert Channels

| Channel | Use | Recipients | Active |
|---|---|---|---|
| Slack `#zelex-ops` | All P1/P2/P3 alerts | On-call + team | YES (primary) |
| Email `ops@zelexdoll.com` | P1 only (backup) | Lead + ops | YES (secondary) |
| SMS | P1 only (escalation) | On-call primary | [TO CONFIGURE] |
| Status Page | User communication | Public | [OPTIONAL] |
| PagerDuty | Escalation | On-call rotation | [OPTIONAL] |

---

## Setting Up Monitoring Tools

### Uptime Robot (Recommended for Start)

**Free tier includes:**
- 50 monitors
- 5-minute interval
- Slack integration
- Email alerts

**Setup steps:**

1. Create account at [uptime.com](https://uptime.com) or [uptimerobot.com](https://uptimerobot.com)
2. Add monitor for production: `https://www.zelexdoll.com`
   - Method: GET
   - Interval: 5 minutes
   - Alert: Slack + Email
3. Add monitor for staging: `https://kas1987.github.io/HowieZZ/`
4. Add image CDN spot-check (optional)
5. Configure Slack webhook → `#zelex-ops`

**Example Slack notification:**

```
Uptime Robot [ALERT]
Site: zelexdoll.com
Status: DOWN
Duration: 10 min
Last check: 2 min ago
Checks before failure: 3 UP
Next check: in 5 min
```

---

### GitHub Actions Integration (Built-In)

**Automatic monitoring:**

All workflow files automatically notify on failure. Configure in repository:

1. Go to [GitHub → Settings → Notifications](https://github.com/kas1987/HowieZZ/settings/notifications)
2. Add Slack app to organization
3. Install [GitHub + Slack app](https://github.com/apps/slack)
4. Subscribe to repository notifications in Slack

**Configuration per workflow:**

Add to `.github/workflows/*.yml`:

```yaml
  - name: Notify Slack on Failure
    if: failure()
    uses: slackapi/slack-github-action@v1.24.0
    with:
      channel: '#zelex-ops'
      payload: |
        {
          "text": "Workflow Failed: ${{ github.workflow }}",
          "blocks": [
            {
              "type": "section",
              "text": {
                "type": "mrkdwn",
                "text": "*GitHub CI Failed*\nBranch: `${{ github.ref_name }}`\nCommit: <${{ github.server_url }}/${{ github.repository }}/commit/${{ github.sha }}|View>"
              }
            }
          ]
        }
```

---

### Custom Monitoring Scripts (Optional)

**Script: Check Catalog Freshness**

```bash
#!/bin/bash
# Run hourly via cron or GitHub Actions

CATALOG_PATH="db/catalog.json"
MAX_AGE_HOURS=8

if [ ! -f "$CATALOG_PATH" ]; then
  echo "CRITICAL: Catalog file not found"
  exit 2
fi

LAST_MODIFIED=$(stat -c %Y "$CATALOG_PATH")
NOW=$(date +%s)
AGE_HOURS=$(( ($NOW - $LAST_MODIFIED) / 3600 ))

if [ $AGE_HOURS -gt $MAX_AGE_HOURS ]; then
  echo "WARNING: Catalog is $AGE_HOURS hours old"
  # Send Slack alert
  exit 1
fi

echo "OK: Catalog is fresh ($AGE_HOURS hours old)"
exit 0
```

**Script: Validate Catalog Schema**

```python
#!/usr/bin/env python3
# Run after every Shopify sync

import json
import sys
from pathlib import Path

def validate_catalog(path="db/catalog.json"):
    try:
        with open(path) as f:
            catalog = json.load(f)
        
        # Check required keys
        required = ['products', 'series', 'families', 'bodies']
        for key in required:
            if key not in catalog:
                print(f"ERROR: Missing key '{key}'")
                return False
        
        # Check product count
        prod_count = len(catalog['products'])
        if prod_count < 50:  # anomaly threshold
            print(f"WARNING: Product count low: {prod_count}")
            return False  # Actually return True but log warning
        
        print(f"OK: Catalog valid ({prod_count} products, {len(catalog['series'])} series)")
        return True
    
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = validate_catalog()
    sys.exit(0 if success else 2)
```

---

## Dashboard Setup (Optional)

### Public Performance Dashboard

Host a simple HTML page at `https://www.zelexdoll.com/perf-dashboard.html`:

```html
<html>
<head>
  <title>ZELEX Operations Dashboard</title>
  <meta name="robots" content="noindex">
</head>
<body>
  <h1>ZELEX Operations Status</h1>
  
  <div id="status">
    <h2>Current Status</h2>
    <p>Last updated: <span id="timestamp"></span></p>
    <ul>
      <li>Website: <span id="web-status">🟢 UP</span></li>
      <li>Build: <span id="build-status">🟢 Passing</span></li>
      <li>Catalog: <span id="catalog-status">🟢 Fresh</span></li>
      <li>Shopify Sync: <span id="sync-status">🟢 OK</span></li>
    </ul>
  </div>
  
  <div id="metrics">
    <h2>Performance Metrics</h2>
    <ul>
      <li>Avg Latency (24h): <span id="latency"></span>ms</li>
      <li>p99 Latency (24h): <span id="latency-p99"></span>ms</li>
      <li>Error Rate (24h): <span id="error-rate"></span>%</li>
      <li>Uptime (30d): <span id="uptime"></span>%</li>
    </ul>
  </div>
  
  <script>
    // Fetch from monitoring API and update page
    // (implementation depends on your monitoring tool)
  </script>
</body>
</html>
```

---

## Alerting Best Practices

### Alert Fatigue Prevention

- **Don't alert on transient failures** (single 404, one slow request)
- **Use thresholds** (e.g., 5 errors in 1 hour, not 1 error)
- **Escalate, don't repeat** (alert once, escalate on silence)
- **Group related alerts** (don't send 10 separate Slack messages)

### On-Call Handoff

Every Monday at 23:30 UTC (15 min before shift change):

1. Outgoing on-call briefs incoming on-call
2. Review: open issues, recent incidents, alert tuning
3. Incoming on-call verifies all monitoring tools are live
4. Document handoff in `#zelex-ops` Slack thread

---

## Maintenance & Updates

### Weekly Tasks (On-Call)

- [ ] Check alert configuration is active (Uptime Robot, GitHub)
- [ ] Verify no stale alerts (false positives)
- [ ] Spot-check the site manually (cache, performance)

### Monthly Tasks (Team Lead)

- [ ] Review alert thresholds (adjust if needed)
- [ ] Audit false positives (reduce noise)
- [ ] Update monitoring dashboard
- [ ] Review SLA metrics vs. targets

### Quarterly Tasks (SRE)

- [ ] Audit monitoring coverage (gaps?)
- [ ] Test incident response (fire drill)
- [ ] Review and update runbooks
- [ ] Plan infrastructure improvements

---

## Escalation Matrix

```
Incident Detected
    ↓
[PRIMARY ON-CALL]
    ↓
Can resolve in <30 min?
    YES → Resolve, document, close
    NO ↓
[Page SECONDARY ON-CALL + LEAD]
    ↓
Is it security-related?
    YES → Email security@zelexdoll.com immediately
    NO ↓
Is it P1 (site down)?
    YES → Email CEO + slack @here
    NO ↓
Continue standard triage
```

---

## Monitoring Checklist

- [ ] Uptime Robot configured for production + staging
- [ ] GitHub + Slack app installed
- [ ] `#zelex-ops` Slack channel set up with webhooks
- [ ] CI/CD pipeline monitored (GitHub Actions)
- [ ] Shopify sync monitored (schedule + failures)
- [ ] Catalog freshness checked (hourly)
- [ ] Performance metrics collected (Google Analytics)
- [ ] Alert thresholds set (no false positives)
- [ ] On-call rotation established
- [ ] Post-mortem template ready
- [ ] Documentation linked in `#zelex-ops` bookmark

---

## References

- [OPERATIONS.md](../OPERATIONS.md) — On-call runbooks and SLAs
- [POSTMORTEM-TEMPLATE.md](POSTMORTEM-TEMPLATE.md) — Incident response
- [SECURITY.md](../SECURITY.md) — Security incident procedure
- [.github/workflows/ci.yml](../.github/workflows/ci.yml) — CI/CD pipeline
- [.github/workflows/shopify-sync.yml](../.github/workflows/shopify-sync.yml) — Data sync pipeline

---

**Version**: 1.0  
**Last Updated**: 2026-06-21  
**Next Review**: 2026-09-21  
**Owner**: DevOps / SRE Lead
