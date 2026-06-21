# Phase 1 FAQ & Troubleshooting Guide

**Status:** Active (Phase 1 Completion)  
**Last Updated:** 2026-06-21  
**Scope:** Common issues & resolutions for Phase 1 deliverables  
**Audience:** All team members

---

## Table of Contents

1. [Design Tokens](#design-tokens)
2. [Image CDN](#image-cdn)
3. [Build Pipeline](#build-pipeline)
4. [Analytics & GTM](#analytics--gtm)
5. [General Troubleshooting](#general-troubleshooting)

---

## Design Tokens

### Q: How do I change a color across the entire site?

**A:** Edit the token in `assets/site.css` under `:root` section. The change applies globally to all pages using that token.

**Example:**
```css
:root {
  --color-primary: #d4a574;  /* Change from #d4a574 to #c9945f */
}
```

All components referencing `var(--color-primary)` update instantly.

---

### Q: I added a color to site.css but it's not showing up.

**A:** Check these in order:

1. **Verify token name spelling**
   - Tokens are case-sensitive: `--color-primary` not `--colorPrimary`
   - Check for typos: `--color-priamry` vs `--color-primary`

2. **Verify the CSS rule uses the token**
   ```css
   .button { color: var(--color-primary); }  /* ✓ Uses token */
   .button { color: #d4a574; }               /* ✗ Hardcoded */
   ```

3. **Reload page in browser**
   - Hard refresh (Ctrl+Shift+R on Windows)
   - Check DevTools → Elements → Styles for the value

4. **Check CSS specificity**
   - Inline styles override CSS: `<div style="color: red;">` wins
   - Remove inline styles or increase specificity

---

### Q: Can I create a token for a single use?

**A:** No. Tokens should represent design decisions that repeat 2+ times or embody brand intent. One-off colors suggest your design is inconsistent.

**Alternative:**
- Review the design (why is this color unique?)
- Map it to an existing token or family
- Update the token scale if it doesn't fit

---

### Q: How do I test if a token change broke anything?

**A:** Use browser DevTools pixel-perfect comparison:

1. Take screenshot before change
2. Make token change
3. Hard reload browser (Ctrl+Shift+R)
4. Take screenshot after change
5. Use DevTools → Screenshots or online diff tool to compare

**Visual regression checklist:**
- [ ] Text colors are readable (WCAG AA 4.5:1 minimum)
- [ ] Card shadows still visible
- [ ] Button hover states work
- [ ] Mobile layout doesn't shift
- [ ] All 41 pages look right

---

### Q: Where are the token definitions?

**A:** `assets/site.css`, lines 1-70 (roughly):

```
--color-* (40 tokens)
--sp* (8 tokens)
--t-* (7 tokens)
--sh-* (5 tokens)
--r-* (4 tokens)
```

Also documented in: `docs/pdr/PDR-100-design-token-system.md`

---

## Image CDN

### Q: Are my images cached on the CDN or always fresh?

**A:** Images are cached with 30-day expiration by default. To force refresh:

```bash
python scripts/push_assets_to_cdn.py --cache-bust
# Generates new URLs with cache-busting query params
```

---

### Q: I see a 404 on a character image. What went wrong?

**A:** Follow the troubleshooting guide:

1. **Check manifest exists**
   ```bash
   ls -lh db/assets_manifest.json
   ```

2. **Check image path is in manifest**
   ```bash
   python scripts/debug_manifest.py --path "characters/Fusion-ZF161D-01/hero.jpg"
   ```

3. **Check CDN URL is valid**
   - Copy the CDN URL from manifest
   - Visit it directly in browser
   - Should load the image

4. **If 404 persists:**
   - Image may not be uploaded to CDN
   - Re-run upload: `python scripts/push_assets_to_cdn.py --incremental`

See `docs/cdn-runbook.md` for full troubleshooting.

---

### Q: How do I add new images to the site?

**A:** Follow the pipeline:

1. **Add images locally**
   ```
   assets/characters/[Series]-[Body]-[Slot]/
   └─ hero.jpg
   └─ gallery/
      ├─ 01.jpg
      ├─ 02.jpg
      └─ ...
   ```

2. **Run build pipeline**
   ```bash
   python scripts/build_orchestrator.py --full
   ```
   This scans images, generates thumbnails, uploads to CDN, and updates manifest.

3. **Commit manifest**
   ```bash
   git add db/assets_manifest.json
   git commit -m "feat: add images for [Series]"
   git push
   ```

---

### Q: The CDN is slow. What can I do?

**A:** Check these in order:

1. **Verify CDN status**
   - Check CDN provider status page
   - Run: `python scripts/test_cdn_connectivity.py`

2. **Check image size**
   - Ensure images are optimized (<500 KB each)
   - Use `scripts/optimize_images.py` to compress batch

3. **Check network latency**
   - Use browser DevTools → Network → filter by images
   - Check "Download time" column
   - If >2 seconds, CDN provider may be slow

4. **Consider regional mirror**
   - Phase 2 roadmap includes multi-region CDN
   - For now, monitor and report to DevOps

---

### Q: Can I delete an image from the CDN?

**A:** Images are immutable once uploaded. To "delete":

1. **Mark as archived in manifest**
   ```bash
   python scripts/archive_asset.py --path "characters/old-char/hero.jpg"
   ```

2. **Update pages to use new image**
   ```bash
   # Edit character_overlay.json to point to new hero
   ```

3. **Commit manifest update**
   ```bash
   git add db/assets_manifest.json db/character_overlay.json
   git commit -m "chore: archive old character image"
   git push
   ```

The old image remains on CDN but is no longer referenced.

---

## Build Pipeline

### Q: The build failed. How do I recover?

**A:** Use the `--resume` flag:

```bash
python scripts/build_orchestrator.py --resume
```

This skips completed stages and retries from where it failed.

**If retry fails again:**
1. Read the error message (last 20 lines of console output)
2. Check the troubleshooting guide (`docs/pipeline-runbook.md`)
3. Fix the root cause (e.g., CDN timeout, missing data file)
4. Retry: `python scripts/build_orchestrator.py --resume --max-retries 10`

---

### Q: The build is too slow. How can I speed it up?

**A:** Several options:

1. **Increase worker threads** (default is 2)
   ```bash
   python scripts/build_orchestrator.py --full --workers 4
   ```

2. **Skip CDN upload** (for local testing only)
   ```bash
   python scripts/build_orchestrator.py --full --skip-cdn
   ```

3. **Cache live feed** (reuse previous feed if fresh)
   ```bash
   python scripts/build_orchestrator.py --full --cache-feed
   ```

4. **Use SSD for temp files**
   ```bash
   TMPDIR=/fast-ssd python scripts/build_orchestrator.py --full
   ```

Expected time after optimization: <45 seconds (vs. 60 seconds baseline).

---

### Q: I changed character data but the build still shows old data.

**A:** The pipeline caches data. Clear the cache:

```bash
# Option 1: Reset pipeline state (forces full re-run)
rm .build_state.json
python scripts/build_orchestrator.py --full

# Option 2: Clear specific cache
python scripts/cleanup_builds.py --full

# Option 3: Run with no cache
python scripts/build_orchestrator.py --full --no-cache
```

---

### Q: How do I run just one stage of the pipeline?

**A:** Run the script directly:

```bash
python scripts/build_db.py              # Stage 1 only
python scripts/build_profiles.py        # Stage 2 only
python scripts/build_characters.py      # Stage 3a only
python scripts/merge_stories.py         # Stage 3b only
python scripts/make_thumbs.py           # Stage 4a only
python scripts/push_assets_to_cdn.py    # Stage 4b only
python scripts/build_package.py         # Stage 5 only
```

---

### Q: What's in the build output? Can I download it?

**A:** Build output is in `build/zelex-site-2026-06-21.zip` (~260 MB):

```
zelex-site-2026-06-21.zip
├─ index.html, browse.html, ... (41 pages)
├─ assets/site.css, assets/site.js
├─ db/characters.json, db/assets_manifest.json
└─ assets/characters/, assets/series/, ... (all images)
```

**To download and deploy:**
1. CI automatically uploads to Google Drive (workflow artifact)
2. Download from Drive or local: `cp build/zelex-site-*.zip ~/Downloads/`
3. Extract and deploy to production

---

### Q: Can I run multiple builds at the same time?

**A:** No. The pipeline uses a shared database (db/catalog.db) which cannot be accessed by multiple processes simultaneously. Run builds sequentially:

```bash
# Run build 1
python scripts/build_orchestrator.py --full
# Wait for completion

# Run build 2
python scripts/build_orchestrator.py --full
```

---

## Analytics & GTM

### Q: I don't see my events in GA4. What's wrong?

**A:** Check in this order:

1. **Enable debug mode in browser**
   ```javascript
   localStorage.setItem('zx_analytics_debug', '1');
   location.reload();
   ```
   Check console for event logs.

2. **Check GTM Preview mode**
   - In GTM Workspace, click Preview
   - Visit site in preview tab
   - Every event should appear in GTM debug panel

3. **Check GA4 Real-time report**
   - Go to https://analytics.google.com/
   - Select "zelexdoll" property
   - Go to Real-time
   - Trigger an event (visit quiz.html, etc.)
   - Should see event within 1 second

4. **Wait 24-48 hours** for initial GA4 data propagation

See `docs/analytics-runbook.md` for detailed troubleshooting.

---

### Q: My GA4 property shows events but numbers look low.

**A:** Common causes:

1. **Events just started firing** (24-48 hour delay before GA4 processes)
2. **Traffic is actually low** (check page views in real-time)
3. **Filter is applied** (check date range and filters in GA4 report)
4. **Event is duplicate of page_view** (GA4 shows both, avoid double-counting)

**Fix:** Wait 48 hours for data to settle, then review GA4 reports.

---

### Q: How do I test an event locally?

**A:** Three ways:

**Method 1: Browser console**
```javascript
ZX.analytics('quiz_start', {
  quiz_family: 'The Muse',
  entry_source: 'browse'
});
```

**Method 2: Debug mode**
```javascript
localStorage.setItem('zx_analytics_debug', '1');
location.reload();
// Trigger event normally (e.g., click button)
// Check console for logs
```

**Method 3: GTM Preview mode**
- GTM Workspace → Preview
- Visit site in preview tab
- Check GTM debug panel for fired tags

---

### Q: I'm concerned about PII in GA4 (emails, phone numbers).

**A:** Valid concern. GA4 must not contain PII. Audit:

```bash
python scripts/audit_datalayer_pii.py \
  --input docs/pdr/PDR-analytics-sample-events.ndjson
```

**If PII found:**
1. Remove from dataLayer in site.js
2. Use hashed user ID instead
3. Re-audit and verify clean

See `docs/analytics-runbook.md` for PII scrubbing details.

---

### Q: How do I add a new GA4 event?

**A:** Four steps:

1. **Push event from site.js**
   ```javascript
   ZX.analytics('my_custom_event', {
     custom_property: 'value'
   });
   ```

2. **Create custom event in GA4** (if not auto-detected)
   - GA4 Admin → Custom Definitions → Create Custom Event
   - Event name: `my_custom_event`

3. **Create custom dimension** (if tracking custom properties)
   - GA4 Admin → Custom Definitions → Create Custom Dimension
   - Parameter name: `custom_property`
   - Scope: Event

4. **Map variable in GTM** (optional, for more control)
   - GTM Variables → Create Variable → Data Layer Variable
   - Variable name: `custom_property`

Events auto-appear in GA4 within 24-48 hours.

---

### Q: The dashboard shows no data for a date range.

**A:** Check:

1. **GA4 has data for that period** (Real-time report)
2. **Dashboard date filter is correct** (should include data dates)
3. **GA4 data source is connected** (check data source in Looker Studio)

**Fix:**
1. Manually refresh GA4 data source in Looker Studio
2. Update dashboard date filter to include latest dates
3. Wait 24 hours for GA4 to process historical data

---

## General Troubleshooting

### Q: Pre-push hook is blocking my commit. What do I do?

**A:** The hook validates that everything is ready for merge. Check each validation:

**Manifest freshness check**
```bash
python scripts/validate_manifest_freshness.py
```

If stale (>48 hours old):
```bash
python scripts/push_assets_to_cdn.py --refresh-manifest
git add db/assets_manifest.json
git commit -m "chore(assets): refresh manifest"
```

**Test suite**
```bash
npm test
python -m pytest --tb=short -q
```

If tests fail, fix the issues and re-run.

**To bypass pre-push (not recommended):**
```bash
git push --no-verify
```

Only use if you understand why validations failed.

---

### Q: CI is failing on my PR. How do I debug?

**A:** Check the GitHub Actions log:

1. Go to PR on GitHub
2. Scroll to "Checks" section
3. Click failing check (e.g., "Python Tests")
4. Expand job log and read error message

**Common failures:**

- **Manifest stale:** Run `python scripts/push_assets_to_cdn.py --refresh-manifest`
- **Tests failing:** Run locally and fix issues
- **Build timeout:** Check if build time exceeded 5 minutes (increase if needed)

Then push a new commit with fixes.

---

### Q: How do I know if a runbook is up to date?

**A:** Each runbook has a "Last Updated" date at the top. If it's older than 30 days, check with the owner (listed in same header).

**Runbook owners:**
- Design Tokens: Frontend Engineering Lead
- Image CDN: DevOps / Platform Engineering
- Build Pipeline: Platform Engineering
- Analytics: Analytics / Product

---

### Q: Where do I report a bug found in Phase 1 docs/code?

**A:** Open an issue:

```bash
git issue create \
  --title "fix: [component] [brief issue]" \
  --body "
  **Component:** Design Tokens / CDN / Pipeline / Analytics

  **Issue:**
  [Describe the bug]

  **Steps to reproduce:**
  1. [Step 1]
  2. [Step 2]

  **Expected:** [What should happen]
  **Actual:** [What happened]

  **Impact:** [How does this affect the team?]
  "
```

Or email team with issue details.

---

### Q: Which runbook should I read first?

**A:** Depends on your role:

| Role | Read First |
|------|-----------|
| Frontend Developer | Design Tokens, Analytics |
| DevOps / Infra | CDN, Pipeline |
| Data / Analytics | Analytics, then Dashboard setup |
| QA / Tester | Pipeline, Analytics (testing events) |
| Project Manager | This FAQ, then skim all others |

---

## Quick Reference

### Critical Runbooks

1. **Design Tokens Runbook:** `docs/design-tokens-runbook.md`
2. **CDN Runbook:** `docs/cdn-runbook.md`
3. **Pipeline Runbook:** `docs/pipeline-runbook.md`
4. **Analytics Runbook:** `docs/analytics-runbook.md`

### Key Commands

```bash
# Design Tokens
grep -r "--color-primary" assets/       # Find token usage

# CDN
python scripts/push_assets_to_cdn.py --incremental  # Upload new images

# Pipeline
python scripts/build_orchestrator.py --full    # Run full pipeline
python scripts/build_orchestrator.py --resume  # Resume after failure

# Analytics
localStorage.setItem('zx_analytics_debug', '1'); location.reload()  # Enable debug
python scripts/analytics_event_sanity.py --strict  # Validate events
```

### Emergency Contacts

| Issue | Owner | Slack |
|-------|-------|-------|
| Design System | Frontend Lead | #frontend |
| CDN / Images | DevOps | #devops |
| Build Pipeline | Platform Lead | #platform |
| Analytics / GA4 | Analytics Lead | #analytics |
| General Questions | Project Manager | #general |

---

## Got a Question Not Listed Here?

1. **Search** the specific runbook (Ctrl+F)
2. **Check GitHub issues** for similar questions
3. **Ask in Slack** in the relevant channel
4. **Email owner** (contact info at top of each runbook)

We'll add your question to this FAQ if it's common.

---

## References

- **Phase 1 Implementation Plan:** `IMPLEMENTATION-PLAN.md`
- **All Runbooks:** `docs/` folder
- **Contributing Guide:** `CONTRIBUTING.md`
- **Source PDRs:** `docs/pdr/` folder
