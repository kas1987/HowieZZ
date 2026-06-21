# Shopify Sync Automation — Deployment & Configuration

## Quick Start (5 minutes)

### 1. Create Shopify Personal Access Token

1. **Log in to Shopify admin:** https://zelex.myshopify.com/admin
2. **Navigate:** Settings > Apps and integrations > Develop apps
3. **Create app:**
   - Name: "ZELEX Sync"
   - (Save, continue)
4. **Assign scopes:**
   - Under "Admin API scopes," enable:
     - `read_products` (required)
     - (Optional: `write_products` for future bidirectional sync)
5. **Generate token:**
   - "API Credentials" tab
   - Click "Generate access token"
   - Copy token (e.g., `shpat_1a2b3c4d5e6f7g8h9i0j`)
6. **Save securely** — you'll add to GitHub next

### 2. Configure GitHub Repository Secrets

1. **Repository Settings:**
   - Navigate: GitHub repo > Settings > Secrets and variables > Actions
2. **Add three secrets:**

   | Secret Name | Value | Source |
   |---|---|---|
   | `SHOPIFY_STORE_URL` | `https://zelex.myshopify.com` | Shopify admin URL |
   | `SHOPIFY_ACCESS_TOKEN` | `shpat_1a2b3c4d...` | Shopify admin (step 1 above) |
   | `SLACK_WEBHOOK_URL` | `https://hooks.slack.com/services/T.../B.../X...` | Slack (optional, see step 3) |

   **Verify:** Each secret should show ✓ after creation

### 3. (Optional) Create Slack Incoming Webhook

For automated sync alerts to Slack channel:

1. **Open Slack workspace**
2. **Create Incoming Webhook:**
   - Browse: https://api.slack.com/apps
   - Click "Create New App"
   - Choose "From scratch"
   - App name: "ZELEX Shopify Sync"
   - Workspace: (your workspace)
3. **Add features:**
   - Left sidebar > "Incoming Webhooks"
   - Toggle: "Activate Incoming Webhooks"
   - Click "Add New Webhook to Workspace"
   - Select channel: `#shopify-sync` (or create it)
4. **Copy webhook URL:** e.g., `https://hooks.slack.com/services/T.../B.../X...`
5. **Add to GitHub Secrets** (step 2 above)

### 4. Verify Workflow Activation

1. **GitHub repo:**
   - Navigate: Actions > Shopify Feed Sync
   - Should see workflow card (blue)
   - If not visible, enable in Settings > Actions > General > "Allow workflows"

2. **Test trigger (optional):**
   - Click workflow
   - "Run workflow" dropdown
   - Select mode: `full`
   - Click "Run workflow"
   - Check run output for status

**Done!** Automated syncs will run at:
- 00:00 UTC
- 06:00 UTC
- 12:00 UTC
- 18:00 UTC

---

## Detailed Deployment Checklist

### Pre-Deployment

- [ ] Shopify store is live and accessible
- [ ] Shopify admin account has API access permissions
- [ ] GitHub repository is public or private (doesn't matter)
- [ ] Repository has Actions enabled (Settings > Actions > General)
- [ ] You have admin access to both Shopify and GitHub

### Step 1: Shopify Setup

**Create Personal Access Token with minimal permissions:**

```
Shopify Admin > Settings > Apps and integrations > Develop apps
  Create app "ZELEX Sync"
  Admin API scopes:
    ✓ read_products
  API Credentials:
    Generate access token
    Copy token value
```

**Verify token works (local test):**

```bash
# Test API call (replace with your values)
curl -X GET "https://zelex.myshopify.com/admin/api/2024-01/products.json?limit=1" \
  -H "X-Shopify-Access-Token: shpat_1a2b3c4d..."
```

Expected response: JSON with `products` array (first product)

### Step 2: GitHub Secrets

**Repository Settings:**

1. Go: GitHub > [your-repo] > Settings > Secrets and variables > Actions
2. Create secrets:

   **Secret 1: SHOPIFY_STORE_URL**
   ```
   Name:  SHOPIFY_STORE_URL
   Value: https://zelex.myshopify.com
   ```

   **Secret 2: SHOPIFY_ACCESS_TOKEN**
   ```
   Name:  SHOPIFY_ACCESS_TOKEN
   Value: shpat_1a2b3c4d5e6f7g8h9i0j
   ```

   **Secret 3: SLACK_WEBHOOK_URL (optional)**
   ```
   Name:  SLACK_WEBHOOK_URL
   Value: https://hooks.slack.com/services/T.../B.../X...
   ```

3. Verify: Each should show a green checkmark

### Step 3: Slack Integration (Optional)

**Create Slack workspace app:**

1. Go: https://api.slack.com/apps
2. "Create New App" > "From scratch"
   - App name: `ZELEX Shopify Sync`
   - Workspace: (select yours)
3. Left menu > "Incoming Webhooks"
   - Toggle: "Activate Incoming Webhooks"
   - "Add New Webhook to Workspace"
   - Select channel: `#shopify-sync` (or create)
4. Copy webhook URL: `https://hooks.slack.com/services/T.../B.../X...`
5. Add to GitHub Secrets (step 2 above)

### Step 4: Workflow Activation

**Enable GitHub Actions:**

1. Repository > Settings > Actions > General
   - "Actions permissions": `Allow all actions and reusable workflows`
   - Save

**Verify workflow file:**

1. Repository > .github/workflows/shopify-sync.yml
   - Should exist and be readable
   - No YAML errors (GitHub shows red X if invalid)

**Trigger test run (optional):**

1. Repository > Actions > "Shopify Feed Sync" workflow
2. "Run workflow" button (top right)
   - Branch: `main`
   - Mode: `full` (dropdown)
   - Click "Run workflow"
3. Wait ~1-2 minutes for run to complete
4. Check status:
   - ✓ green = success
   - ✗ red = check logs

**Check workflow logs:**

1. Actions > Shopify Feed Sync > [latest run]
2. View job output:
   - `shopify-sync` — main sync execution
   - `rollback-guard` — catalog validation
   - `slack-notification` — alert delivery

### Step 5: Verify Setup

**Check sync state:**

```bash
# After first sync run, verify state file exists
git status
# Should show (if committed): db/.shopify_sync_state.json
```

**Manual verification:**

1. GitHub Actions page should show successful run
2. Slack channel `#shopify-sync` should have alert message
3. Repository > Actions > artifacts should have sync data

---

## Environment Variables Reference

### Required

| Variable | Required | Default | Example |
|----------|----------|---------|---------|
| `SHOPIFY_STORE_URL` | Yes | — | `https://zelex.myshopify.com` |
| `SHOPIFY_ACCESS_TOKEN` | Yes | — | `shpat_1a2b3c4d...` |

### Optional

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `SLACK_WEBHOOK_URL` | No | (disabled) | For alerts; leave empty to disable |
| `SYNC_MODE` | No | `full` | `full` or `incremental` |
| `SYNC_DRY_RUN` | No | `false` | `true` = preview only, no writes |
| `API_TIMEOUT` | No | `30` | HTTP timeout in seconds |
| `MAX_RETRIES` | No | `3` | Retry count on transient errors |

### GitHub Actions Context Variables

Automatically available in workflow (no setup needed):

```yaml
${{ github.ref }}           # Current branch (e.g., refs/heads/main)
${{ github.repository }}    # Repo slug (e.g., kas1987/zelex-atlas)
${{ github.run_id }}        # Workflow run ID
${{ secrets.XXX }}          # Access secret by name
```

---

## Manual Workflow Triggers

### Trigger from GitHub UI

1. Repository > Actions > "Shopify Feed Sync" workflow
2. "Run workflow" button (right side)
   ```
   Branch: [main]
   Mode: [full ▾]  — select: full | incremental | dry-run
   ```
3. "Run workflow"

### Trigger from Command Line

```bash
# Full sync
gh workflow run shopify-sync.yml --ref main -f mode=full

# Dry-run preview
gh workflow run shopify-sync.yml --ref main -f mode=dry-run

# View workflow runs
gh workflow view shopify-sync.yml
gh run list --workflow shopify-sync.yml --limit 10
```

### Scheduled Triggers

Automatic runs (no action needed):

```
00:00 UTC
06:00 UTC
12:00 UTC
18:00 UTC
```

To modify schedule, edit `.github/workflows/shopify-sync.yml`:

```yaml
on:
  schedule:
    # Change cron expression to your preferred times
    - cron: '0 0,6,12,18 * * *'  # 6-hour interval
    # - cron: '*/30 * * * *'      # Every 30 minutes (faster)
    # - cron: '0 2 * * *'         # Daily at 02:00 UTC
```

---

## Troubleshooting Deployment

### Issue: Workflow doesn't appear in Actions tab

**Cause:** Actions not enabled, or workflow file has YAML syntax error

**Fix:**
1. Repository > Settings > Actions > General
   - "Actions permissions": `Allow all actions and reusable workflows`
2. Check YAML syntax: `.github/workflows/shopify-sync.yml`
   - Run: `yamllint .github/workflows/shopify-sync.yml`
   - Or validate at: https://www.yamllint.com/

### Issue: Sync fails with "SHOPIFY_ACCESS_TOKEN not found"

**Cause:** Secret not created or not visible to workflow

**Fix:**
1. Verify secret exists: Settings > Secrets and variables > Actions
2. Verify secret name matches exactly: `SHOPIFY_ACCESS_TOKEN`
3. Secrets are case-sensitive
4. Wait ~5 minutes after creating secret for GitHub to propagate

### Issue: Sync starts but hangs/times out

**Cause:** Shopify API slow or network issue

**Fix:**
1. Check Shopify status: https://status.shopify.com
2. Increase timeout in workflow:
   ```yaml
   jobs:
     shopify-sync:
       timeout-minutes: 30  # (default 15)
   ```
3. Run dry-run to isolate API issue:
   ```bash
   SYNC_DRY_RUN=true python scripts/sync_shopify_feed.py
   ```

### Issue: Slack alert not sending

**Cause:** Webhook URL invalid or not authorized

**Fix:**
1. Test webhook manually:
   ```bash
   curl -X POST $SLACK_WEBHOOK_URL \
     -H 'Content-type: application/json' \
     -d '{"text": "Test message"}'
   ```
   Should respond: `ok`

2. Regenerate webhook:
   - Slack workspace > API > Apps
   - "ZELEX Shopify Sync" app
   - Incoming Webhooks > delete old, create new
   - Update GitHub secret with new URL

### Issue: Catalog validation (rollback-guard) fails

**Cause:** `catalog.json` or `characters.json` missing or corrupted

**Fix:**
1. Verify files exist:
   ```bash
   ls -l db/catalog.json db/characters.json
   ```
2. Validate JSON:
   ```bash
   python -c "import json; json.load(open('db/catalog.json'))"
   ```
3. Rebuild catalog:
   ```bash
   python scripts/build_db.py
   ```

---

## Post-Deployment Verification

### Checklist After First Sync

- [ ] Workflow ran without errors (green checkmark)
- [ ] Sync artifacts uploaded (Actions > artifacts)
- [ ] Slack alert posted (if Slack enabled)
- [ ] `.shopify_sync_state.json` created with state: `clean`
- [ ] `.shopify_sync_history.jsonl` has log entries
- [ ] `.shopify_snapshots/` has versioned snapshot file

### Run Manual Verification Tests

```bash
# Test SKU parsing
python -c "
from scripts.sync_shopify_feed import generate_sku, parse_sku
sku = generate_sku('ZFE01_1+ZF161D', 'complete')
print(f'Generated SKU: {sku}')
parsed = parse_sku(sku)
print(f'Parsed back: {parsed}')
assert parsed['product_code'] == 'ZFE01_1+ZF161D', 'Round-trip failed'
print('✓ SKU mapping works')
"

# Test reconciliation logic
python -c "
from scripts.sync_shopify_feed import reconcile_products
catalog = {
    'products': [
        {'code': 'ZFE01_1+ZF161D'},
        {'code': 'ZFE02_1+ZF161D'},
    ],
    'series': []
}
shopify_products = [
    {'sku': 'ZELEX-ZFE01_1-ZF161D', 'title': 'Product 1', 'status': 'active', 'variants': []},
]
result = reconcile_products(shopify_products, catalog)
print(f'In sync: {len(result[\"in_sync\"])}')
print(f'Discontinued: {len(result[\"discontinued\"])}')
print('✓ Reconciliation works')
"
```

### Check Sync Metrics

```bash
# Last sync timestamp
cat db/.shopify_sync_state.json | jq '.last_sync'

# Recent events (last 5)
tail -5 db/.shopify_sync_history.jsonl | jq -r '[.timestamp, .level, .message] | join(" | ")'

# Latest snapshot stats
ls -ltr db/.shopify_snapshots/ | tail -1
cat db/.shopify_snapshots/[latest-file].json | jq '.reconciliation.stats'
```

---

## Production Runbook

### Daily Checks

**Every morning (or after each sync):**

1. **Check sync state:**
   ```bash
   cat db/.shopify_sync_state.json
   ```
   Expected: `state: "clean"` (or `"warning"` if minor issues)

2. **Review latest sync:**
   ```bash
   tail -1 db/.shopify_sync_history.jsonl | jq '.'
   ```
   Expected: level = "INFO", message mentions reconciliation complete

3. **Monitor error count:**
   ```bash
   cat db/.shopify_snapshots/[latest].json | jq '.reconciliation.errors | length'
   ```
   Expected: 0 errors (if >10, investigate)

### If Sync Fails

**Step 1: Check logs**
```bash
tail -50 db/.shopify_sync_history.jsonl
# Look for ERROR entries — note the root cause
```

**Step 2: Diagnose**
```bash
# Run dry-run to isolate issue
SYNC_DRY_RUN=true python scripts/sync_shopify_feed.py

# Verify Shopify credentials
curl -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "$SHOPIFY_STORE_URL/admin/api/2024-01/products.json?limit=1"
```

**Step 3: Recover**
- If credentials expired: regenerate at Shopify admin
- If catalog corrupted: `python scripts/build_db.py`
- If temporary API failure: wait 5min + retry

### If Sync Shows Warnings

**Check error details:**
```bash
cat db/.shopify_snapshots/[latest].json | jq '.reconciliation.errors'
```

**Common warnings:**
- Unparseable SKU: Shopify product has non-standard SKU format
  - *Action:* Contact store admin to fix SKU
- New products on Shopify: Not in internal catalog
  - *Action:* Decide: curate into catalog or archive on Shopify
- Discontinued: In catalog but not on Shopify
  - *Action:* Verify product was intentionally delisted

### Regular Maintenance

**Weekly:**
- Review snapshot count: `ls db/.shopify_snapshots/ | wc -l`
- If >100 old snapshots, consider pruning (keep last 30 for rollback history)

**Monthly:**
- Review sync history for trends: `wc -l db/.shopify_sync_history.jsonl`
- Export metrics for reporting: `cat db/.shopify_snapshots/*.json | jq '.reconciliation.stats'`

---

## Rollback Procedures

### Scenario: Sync introduced errors or incorrect data

**Rollback to previous state:**

```bash
# List all snapshots
python scripts/rollback_shopify_sync.py --list

# Rollback to most recent known-good sync
python scripts/rollback_shopify_sync.py --last

# Or rollback to specific snapshot (dry-run preview)
python scripts/rollback_shopify_sync.py --snapshot 20260621-120000-abc12345 --dry-run

# Confirm and apply
python scripts/rollback_shopify_sync.py --snapshot 20260621-120000-abc12345
```

**What rollback does (current implementation):**
- Backs up current sync state
- Logs rollback event to history
- Restores sync state to pre-sync condition

**What rollback will do (future):**
- Restore product inventory/prices to Shopify via API
- Revert all product modifications

---

## Monitoring & Alerting Setup

### GitHub Actions Status Checks

Enable auto-notifications:

1. Repository > Settings > Notifications
   - "Watching": Check "All Activity"
2. Or: Profile > Settings > Notifications
   - "GitHub Actions": Check "Always" (for workflow failures)

### Slack Notifications (if enabled)

Alerts post to configured Slack channel:

```
Shopify Feed Sync SUCCESS
Synced: 310 | New: 5 | Discontinued: 2 | Modified: 0
Repository: kas1987/zelex-atlas | Branch: main | Run: [View]
```

### Email Alerts (GitHub native)

1. Profile > Settings > Notifications
   - "Email": Check boxes for workflow failures

### Grafana/Datadog Integration (Future)

```bash
# Export sync metrics to monitoring system
cat db/.shopify_snapshots/*.json | jq -s '
  group_by(.timestamp | split("T")[0]) |
  map({
    date: .[0].timestamp | split("T")[0],
    total_syncs: length,
    errors: map(.reconciliation.errors | length) | add
  })
'
```

---

## Support & Escalation

**Need help?**

1. **Check documentation:**
   - `docs/SHOPIFY-SYNC-ARCHITECTURE.md` — detailed architecture
   - `docs/SHOPIFY-SYNC-DEPLOYMENT.md` — this file

2. **Review logs:**
   - GitHub Actions > Shopify Feed Sync > [run] > [job logs]
   - `db/.shopify_sync_history.jsonl` — local sync history

3. **Test in isolation:**
   ```bash
   SYNC_DRY_RUN=true python scripts/sync_shopify_feed.py
   ```

4. **Escalate:** 
   - Slack: #shopify-sync channel
   - Email: engineering@zelex.com
   - Response SLA: 15min for production sync failures

---

## Next Steps

1. **Immediate:** Complete Quick Start (5 min above)
2. **Next:** Verify first sync runs successfully
3. **Later:** Set up monitoring dashboard (optional)
4. **Planned:** Implement bidirectional sync + webhook triggers

---

## Appendix: Example Outputs

### Successful Sync Run

```
✓ Shopify sync started
✓ Configuration validated
✓ Fetched 325 products from Shopify (2 API calls)
✓ Reconciliation complete
  - In sync: 310
  - New: 5
  - Discontinued: 2
  - Modified: 0
  - Errors: 0
✓ Snapshot saved: db/.shopify_snapshots/20260621-180000-a1b2c3d4.json
✓ Sync state updated: clean
✓ Slack alert sent
✓ Catalog integrity verified
```

### Sync with Warnings

```
⚠ Shopify sync started
✓ Configuration validated
✓ Fetched 325 products from Shopify
✓ Reconciliation complete
  - In sync: 308
  - New: 5
  - Discontinued: 2
  - Modified: 0
  - Errors: 3
⚠ Found 3 unparseable SKUs:
  - "INVALID-SKU-001" (product: "Unknown Item")
  - "INVALID-SKU-002" (product: "Mystery Box")
  - "INVALID-SKU-003" (product: "Promo Item")
✓ Snapshot saved: db/.shopify_snapshots/20260621-180000-b2c3d4e5.json
⚠ Sync state: warning
✓ Slack alert sent (⚠ warning)
✓ Catalog integrity verified
```

### Snapshot File Example

```json
{
  "timestamp": "2026-06-21T18:00:00.123456",
  "reconciliation": {
    "in_sync": [
      {
        "sku": "ZELEX-ZFE01_1-ZF161D",
        "title": "Fusion Series Complete - Model ZFE01_1+ZF161D"
      },
      ...
    ],
    "new_shopify": [
      {
        "sku": "ZELEX-ZFE99_9-ZF999D",
        "title": "New Product",
        "variants": 2
      }
    ],
    "discontinued": [
      {
        "code": "ZFE02_1+ZF161D",
        "sku": "ZELEX-ZFE02_1-ZF161D"
      }
    ],
    "modified": [],
    "errors": [],
    "stats": {
      "shopify_total": 325,
      "catalog_total": 108
    }
  }
}
```
