# Shopify Product Feed Sync — Architecture & Operations

## Overview

**Shopify Sync Automation** maintains real-time alignment between the ZELEX Character Atlas catalog and Shopify store inventory. Targets **<30min latency** with automated reconciliation, conflict detection, and rollback capability.

### Key Features

- **Automated 6-hour sync** via GitHub Actions scheduler
- **SKU mapping** — bidirectional conversion between internal codes and Shopify products
- **Reconciliation engine** — detects new products, discontinued SKUs, price/inventory changes
- **Versioned snapshots** — full sync history for audit trail and rollback
- **Slack alerts** — real-time sync status notifications
- **Zero-downtime rollback** — restore to any prior sync state

---

## Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions (6h scheduler)                              │
│  Workflow: .github/workflows/shopify-sync.yml               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  sync_shopify_feed.py │
        │  (main orchestrator)  │
        └──────────┬───────────┘
                   │
         ┌─────────┴──────────┐
         ▼                    ▼
    ┌────────────┐      ┌──────────────────┐
    │  Shopify   │      │  ZELEX Catalog   │
    │  REST API  │      │  (db/*.json)     │
    │  (paginated)       │                  │
    └────────┬───┘      └────────┬─────────┘
             │                   │
             └───────┬───────────┘
                     ▼
          ┌────────────────────────┐
          │  Reconciliation Engine │
          │ ─ Parse SKUs           │
          │ ─ Match codes          │
          │ ─ Detect deltas        │
          │ ─ Generate report      │
          └───────┬────────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
    ┌──────────────┐   ┌──────────────────┐
    │  Versioned   │   │  Slack Alert     │
    │  Snapshots   │   │  (sync status)   │
    │  (rollback)  │   └──────────────────┘
    └──────────────┘
        │
        ▼
    ┌──────────────────────┐
    │  Sync State          │
    │  (.shopify_sync_*.)  │
    └──────────────────────┘
```

### Components

#### 1. `sync_shopify_feed.py`

Main synchronization engine. Responsibilities:

- **Credential validation** — ensures Shopify URL + token are set
- **API pagination** — fetches all active products from Shopify (batches of 250)
- **SKU parsing** — converts Shopify SKUs back to internal product codes
- **Reconciliation** — compares Shopify against catalog:
  - `in_sync` — matching SKU, no changes
  - `new_shopify` — SKU not in catalog
  - `discontinued` — in catalog but not on Shopify
  - `modified` — same SKU, different specs (price, inventory, status)
  - `errors` — unparseable SKUs
- **State management** — logs sync history, saves state
- **Snapshot creation** — versioned JSON records for each sync
- **Slack integration** — alerts on completion/warnings/errors

**Exit codes:**
- `0` — success
- `1` — fatal (config missing, API failure, bad catalog)
- `2` — warnings (deltas detected, handled gracefully)
- `3` — dry-run mode (no writes, report only)

#### 2. GitHub Actions Workflow (`.github/workflows/shopify-sync.yml`)

Orchestrates scheduled and manual sync runs.

**Triggers:**
- **Schedule:** 00:00, 06:00, 12:00, 18:00 UTC (6-hour intervals)
- **Manual:** Workflow dispatch (input: full/incremental/dry-run)

**Jobs:**
1. **shopify-sync** — runs Python sync script
2. **rollback-guard** — validates catalog schema post-sync (integrity check)
3. **slack-notification** — sends status alert to Slack channel

**Artifact retention:** 30 days

#### 3. `rollback_shopify_sync.py`

Rollback orchestrator with snapshot management.

**Commands:**
```bash
# List all snapshots
python scripts/rollback_shopify_sync.py --list

# Rollback to most recent
python scripts/rollback_shopify_sync.py --last

# Rollback to specific snapshot
python scripts/rollback_shopify_sync.py --snapshot 20260621-120000-abc12345

# Dry-run (preview without changes)
python scripts/rollback_shopify_sync.py --last --dry-run
```

**Current behavior:** restores sync state; future: restores product inventory/prices via API.

---

## SKU Mapping System

### SKU Generation Rules

```python
# Complete dolls (head + body)
ZELEX-{head_code}-{body_code}
Example: ZELEX-ZFE01_1-ZF161D

# Standalone bodies
ZX-BODY-{body_code}
Example: ZX-BODY-ZF161D

# Standalone heads
ZX-HEAD-{head_code}
Example: ZX-HEAD-ZFE01_1

# Generic fallback
ZX-{internal_code}
```

### Mapping Config (`db/shopify_sku_mapping.json`)

```json
{
  "mapping_rules": {
    "complete_dolls": {
      "pattern": "{head_code}+{body_code}",
      "shopify_prefix": "ZELEX-"
    },
    "bodies_standalone": {
      "pattern": "{body_code}",
      "shopify_prefix": "ZX-BODY-"
    },
    "heads_standalone": {
      "pattern": "{head_code}",
      "shopify_prefix": "ZX-HEAD-"
    }
  },
  "sync_fields": [
    "title", "description", "sku", "price", "inventory_quantity",
    "status", "tags", "metafields"
  ],
  "full_sync_interval_hours": 6,
  "conflict_resolution": {
    "strategy": "shopify_canonical",
    "description": "Shopify = inventory source of truth; ZELEX DB = canonical specs"
  }
}
```

---

## State Management

### Sync State File (`.shopify_sync_state.json`)

```json
{
  "last_sync": "2026-06-21T12:00:00.000000",
  "last_full_sync": "2026-06-21T12:00:00.000000",
  "state": "clean",
  "updated_at": "2026-06-21T12:00:15.123456"
}
```

**States:**
- `clean` — no issues detected
- `warning` — deltas or unparseable SKUs found (handled)
- `error` — sync failed, manual intervention may be needed

### Sync History (`.shopify_sync_history.jsonl`)

Newline-delimited JSON log of all sync events.

```json
{"timestamp": "2026-06-21T12:00:00.000000", "level": "INFO", "message": "Configuration validated"}
{"timestamp": "2026-06-21T12:00:05.123456", "level": "INFO", "message": "Fetched 342 products from Shopify", "data": {"api_calls": 2, "api_errors": 0}}
{"timestamp": "2026-06-21T12:00:15.654321", "level": "INFO", "message": "Reconciliation complete", "data": {"in_sync": 310, "new_shopify": 15, "discontinued": 2, "modified": 0, "errors": 0}}
```

### Versioned Snapshots (`.shopify_snapshots/`)

Each sync creates a timestamped snapshot:

```
.shopify_snapshots/
├── 20260621-120000-a1b2c3d4.json
├── 20260621-060000-b2c3d4e5.json
├── 20260620-180000-c3d4e5f6.json
└── ...
```

**Snapshot structure:**
```json
{
  "timestamp": "2026-06-21T12:00:00.000000",
  "reconciliation": {
    "in_sync": [...],
    "new_shopify": [...],
    "discontinued": [...],
    "modified": [...],
    "errors": [...],
    "stats": {
      "shopify_total": 325,
      "catalog_total": 108
    }
  }
}
```

---

## Configuration

### Environment Variables

Required (must be set before sync):

| Variable | Purpose | Example |
|----------|---------|---------|
| `SHOPIFY_STORE_URL` | Shopify store base URL | `https://zelex.myshopify.com` |
| `SHOPIFY_ACCESS_TOKEN` | REST API Bearer token | (Personal Access Token with `read_products` scope) |

Optional:

| Variable | Purpose | Default |
|----------|---------|---------|
| `SLACK_WEBHOOK_URL` | Incoming webhook for alerts | (disabled if not set) |
| `SYNC_MODE` | `full` or `incremental` | `full` |
| `SYNC_DRY_RUN` | `true` = preview only | `false` |
| `API_TIMEOUT` | HTTP timeout (seconds) | `30` |
| `MAX_RETRIES` | Retry count on transient errors | `3` |

### GitHub Secrets Setup

Store these in your repository settings (**Settings > Secrets and variables > Actions**):

```
SHOPIFY_STORE_URL         = https://zelex.myshopify.com
SHOPIFY_ACCESS_TOKEN      = shpat_xxxxxxxxxxxx
SLACK_WEBHOOK_URL         = https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
```

### Slack Integration

**To enable Slack alerts:**

1. Create an Incoming Webhook in your Slack workspace:
   - **Slack App Directory** → search "Incoming Webhooks"
   - Create new webhook for a channel (e.g., `#shopify-sync`)
   - Copy webhook URL

2. Add to GitHub Secrets:
   - `SLACK_WEBHOOK_URL` = (webhook URL)

3. Alerts appear on sync completion with status (success/warning/error)

---

## Operational Procedures

### Manual Full Sync

Trigger from GitHub Actions UI:

```
Actions > Shopify Feed Sync > Run workflow
  Branch: main
  Mode: full
  [Run workflow]
```

### Manual Dry-Run (Preview)

```
Actions > Shopify Feed Sync > Run workflow
  Branch: main
  Mode: dry-run
  [Run workflow]
```

**Output:** artifact with reconciliation report, no state changes.

### Check Sync Status

**In GitHub:**
```
Actions > Shopify Feed Sync > [latest run]
  ✓ Build (shopify-sync job)
  ✓ Verify (rollback-guard job)
  ✓ Notify (slack-notification job)
```

**Programmatically:**
```bash
# Check last sync state
cat db/.shopify_sync_state.json

# View sync history (last 10 events)
tail -10 db/.shopify_sync_history.jsonl

# List snapshots
python scripts/rollback_shopify_sync.py --list
```

### List All Snapshots

```bash
python scripts/rollback_shopify_sync.py --list
```

Output:
```
Available snapshots (12):

  1. 20260621-180000-a1b2c3d4.json
     Timestamp: 2026-06-21T18:00:00.000000
     Shopify total: 325 products
     Catalog total: 108 products

  2. 20260621-120000-b2c3d4e5.json
     Timestamp: 2026-06-21T12:00:00.000000
     Shopify total: 323 products
     Catalog total: 108 products
  ...
```

### Rollback to Previous Sync

```bash
# Rollback to most recent
python scripts/rollback_shopify_sync.py --last

# Or specific snapshot
python scripts/rollback_shopify_sync.py --snapshot 20260621-120000-b2c3d4e5

# Preview rollback
python scripts/rollback_shopify_sync.py --last --dry-run
```

**What happens:**
1. Current sync state backed up to `.shopify_sync_state.backup.json`
2. Rollback event logged to sync history
3. Manual verification recommended before next sync

**Future enhancement:** restore actual product data (price, inventory) to Shopify via API.

---

## Latency Analysis

### Sync Timeline (6-hour cycle)

| Phase | Time | Notes |
|-------|------|-------|
| **Schedule trigger** | T+0 | GitHub Actions scheduler fires (00:00, 06:00, 12:00, 18:00 UTC) |
| **Job start** | T+0-5s | Runner spins up, checks out code, installs Python |
| **Config validation** | T+5-10s | Verify Shopify credentials |
| **API paginate** | T+10-60s | Fetch all products (typically 2-4 API calls) |
| **Reconciliation** | T+60-90s | Parse SKUs, match codes, detect deltas |
| **Snapshot + state** | T+90-95s | Write versioned snapshot, update sync state |
| **Slack alert** | T+95-100s | Post status to Slack channel |
| **Rollback guard** | T+100-120s | Validate catalog schema integrity |

**Total end-to-end latency: ~2 minutes**

### Next Sync Window

With 6-hour intervals (00:00, 06:00, 12:00, 18:00 UTC):

- If sync runs at 12:00 UTC, next sync window is 18:00 UTC = **6 hours max latency**
- Worst case: product change at 12:01 UTC → detected at 18:00 UTC (5h 59m)
- Best case: product change at 11:59 UTC → detected at 12:00 UTC (1m)
- Average latency: **~3 hours** (uniform distribution across sync window)

### Meeting <30min Target

To achieve <30min latency, consider:

**Option 1: Increase sync frequency**
```yaml
schedule:
  - cron: '*/30 * * * *'  # Every 30 minutes
```
*Tradeoff:* higher API call volume, more Shopify rate-limit pressure

**Option 2: Webhook-triggered sync**
- Configure Shopify webhooks (products/create, products/update) → GitHub webhook endpoint
- Trigger sync immediately on product change
- Requires public endpoint (GitHub Actions doesn't support inbound webhooks natively; use Cloudflare Workers or AWS Lambda as relay)

**Option 3: Hybrid mode (recommended)**
- Keep 6-hour full sync (audit trail + catch missed webhooks)
- Add 30-minute incremental syncs
- Incremental = only products changed since last sync (cheaper, faster)

---

## Error Handling & Recovery

### Error Scenarios

| Scenario | Exit Code | Recovery |
|----------|-----------|----------|
| Missing SHOPIFY_ACCESS_TOKEN | 1 | Add to GitHub Secrets |
| Network timeout (Shopify API) | 1 (retries 3x first) | Auto-retry with backoff; manual retry if persists |
| Bad SKU format in Shopify | 2 | Log to sync history; doesn't block other products |
| Catalog missing/corrupted | 1 | Rollback guard catches; investigate db/*.json |
| Slack alert fails | 2 | Doesn't block sync; retry on next cycle |

### Automatic Retry Logic

```python
# Transient failures (500+, timeout) auto-retry with exponential backoff
for attempt in range(MAX_RETRIES):
    try:
        response = api_call()
        return response
    except (Timeout, ServerError):
        if attempt < MAX_RETRIES - 1:
            sleep(RETRY_BACKOFF ** attempt)  # 1s, 2s, 4s
        continue
```

**Rate limiting (429):** respects `Retry-After` header, waits before retry

### Manual Recovery

If sync fails:

```bash
# 1. Check sync history for root cause
tail -50 db/.shopify_sync_history.jsonl

# 2. Verify Shopify credentials
echo $SHOPIFY_ACCESS_TOKEN | head -c 20

# 3. Run dry-run to diagnose
SYNC_DRY_RUN=true python scripts/sync_shopify_feed.py

# 4. If needed, rollback to known-good state
python scripts/rollback_shopify_sync.py --last

# 5. Manually trigger sync retry
Actions > Shopify Feed Sync > Run workflow [full]
```

---

## Testing & Validation

### Unit Tests

```bash
pytest scripts/sync_shopify_feed.py -v
```

**Covered:**
- SKU parsing (complete, body, head, invalid formats)
- Reconciliation logic (match, new, discontinued, modified)
- Config validation
- Snapshot creation

### Integration Test (dry-run)

```bash
SYNC_DRY_RUN=true python scripts/sync_shopify_feed.py
```

**Verifies:**
- Shopify API connectivity
- Catalog loading
- Reconciliation report generation
- No state mutations

### Manual Verification

After each sync:

1. **Check sync state:**
   ```bash
   cat db/.shopify_sync_state.json | jq '.state'  # Should be "clean"
   ```

2. **Review reconciliation report:**
   ```bash
   ls -ltr db/.shopify_snapshots/ | tail -1  # Latest snapshot
   cat db/.shopify_snapshots/[latest].json | jq '.reconciliation.stats'
   ```

3. **Verify Slack alert:**
   - Check Slack channel for sync notification
   - Confirm status (✓ Success or ⚠ Warning)

---

## Monitoring & Alerting

### Metrics to Track

- **Sync latency:** time from scheduler trigger to completion
- **Product delta rate:** new/discontinued products per sync
- **Error rate:** failed syncs / total syncs
- **API call efficiency:** products per API call
- **Rollback frequency:** rollbacks per month

### Dashboard Setup (Future)

```
ZELEX Shopify Sync Dashboard
├─ Last sync: [timestamp]
├─ Status: [clean/warning/error]
├─ Products in sync: [count]
├─ New on Shopify: [count]
├─ Discontinued: [count]
├─ Sync latency: [seconds]
├─ Error rate (30d): [%]
└─ Last rollback: [timestamp or "Never"]
```

### Alert Thresholds (Recommended)

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Sync failure | >1 in 24h | Page on-call |
| Error count | >10 per sync | Investigate SKU mapping |
| Latency | >5min | Optimize API pagination |
| Discontinued products | >5 per sync | Verify Shopify catalog state |

---

## Security Considerations

### Credential Management

- **Shopify token:** Personal Access Token with **read_products** scope only (no write permissions)
- **Storage:** GitHub Secrets (encrypted, not logged)
- **Rotation:** quarterly or on compromise
- **Audit:** log all API calls with timestamp + user (via GitHub Actions context)

### Data Isolation

- Sync snapshots contain no PII (only product SKUs + metadata)
- Sync history contains only operational events (no sensitive data)
- Slack alerts redact full URLs, show only domain + status

### Access Control

- Sync script runs in GitHub Actions CI/CD context (no user access required)
- Rollback requires repository write access (protected by GitHub branch rules + CODEOWNERS)
- Sync state files in `db/` — not committed, local-only storage

---

## Troubleshooting

### Sync Won't Start

**Check:** GitHub Secrets configured?
```bash
# In repo settings, verify:
SHOPIFY_STORE_URL      ✓ https://zelex.myshopify.com
SHOPIFY_ACCESS_TOKEN   ✓ shpat_... (hidden)
SLACK_WEBHOOK_URL      ✓ https://hooks.slack.com/...
```

**Check:** Secrets accessible in workflow?
```bash
# Add debug step to workflow:
- name: Debug secrets
  run: |
    [ -z "$SHOPIFY_STORE_URL" ] && echo "ERROR: SHOPIFY_STORE_URL not set" || echo "✓ SHOPIFY_STORE_URL set"
```

### High Error Count

**Symptoms:** Sync completes but error_count > 0

**Debug:**
```bash
# View erroneous SKUs
cat db/.shopify_snapshots/[latest].json | jq '.reconciliation.errors'

# Expected format:
[
  {
    "sku": "INVALID-SKU-123",
    "title": "Product Title",
    "reason": "unparseable_sku"
  }
]

# Action: Contact Shopify store admin to fix SKU format
```

### Rollback Fails

**Symptoms:** `python rollback_shopify_sync.py --last` errors

**Debug:**
```bash
# Check snapshots exist
ls -la db/.shopify_snapshots/

# Check snapshot is readable
cat db/.shopify_snapshots/[filename].json | jq '.' > /dev/null

# Check disk space
df -h db/
```

### Slack Alert Not Sending

**Check:** Webhook URL valid?
```bash
# Test webhook manually
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-type: application/json' \
  -d '{"text": "Test"}'
```

**Check:** GitHub secret set?
```bash
# In workflow, verify SLACK_WEBHOOK_URL passed:
env:
  SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Future Enhancements

1. **Bidirectional sync** — push ZELEX catalog updates (price, inventory) to Shopify
2. **Incremental sync** — only sync products changed since last sync (cheaper, faster)
3. **Webhook-triggered sync** — immediate sync on Shopify product changes
4. **Conflict resolution UI** — dashboard to review + approve deltas before commit
5. **Metric dashboard** — real-time sync status, error rates, latency trends
6. **Advanced rollback** — restore actual product inventory/prices (not just state)
7. **Catalog diff viewer** — visual comparison of Shopify vs. ZELEX before/after sync

---

## Support & Escalation

**For issues:**

1. Check sync history: `tail -50 db/.shopify_sync_history.jsonl`
2. Review latest snapshot: `cat db/.shopify_snapshots/[latest].json`
3. Run dry-run diagnostic: `SYNC_DRY_RUN=true python scripts/sync_shopify_feed.py`
4. Check GitHub Actions logs: Actions > Shopify Feed Sync > [run]
5. Escalate: @on-call-engineer in Slack (channel: #shopify-sync)

**On-call SLA:** 15min response time for sync failures
