# Image CDN Management Runbook

**Status:** Active (Phase 1)  
**Last Updated:** 2026-06-21  
**Owner:** DevOps / Platform Engineering  
**Audience:** All developers, DevOps, CI/CD

---

## Overview

This runbook explains how to manage images on the CDN, refresh the asset manifest, diagnose delivery issues, and handle failover scenarios. All ZELEX images are hosted on a CDN (not in git) and versioned via `db/assets_manifest.json`.

---

## Architecture

```
Local Dev                CI/CD Pipeline              Production
├─ images/          ├─ build_db.py            ├─ CDN (images hosted)
├─ assets/          ├─ push_assets_to_cdn.py  ├─ db/assets_manifest.json
└─ db/*.json        ├─ validate_manifest.py   └─ Fallback (git images)
                    └─ site.js (image loader)
```

**Key Files:**
- `scripts/push_assets_to_cdn.py` — Upload images to CDN with SHA256 hashing
- `db/assets_manifest.json` — Manifest mapping local paths → CDN URLs
- `scripts/validate_manifest_freshness.py` — CI guard (fail if manifest stale >48h)
- `assets/image-loader.js` — Runtime fallback logic
- `assets/site.js` — Image URL resolution via manifest

---

## The Asset Manifest

**Location:** `db/assets_manifest.json`

**Schema:**

```json
{
  "version": "1.0",
  "generated_at": "2026-06-21T14:32:00Z",
  "source": "howiezz-web",
  "cdn_provider": "cloudinary",
  "cdn_bucket": "zelexdoll",
  "assets": {
    "characters/Fusion-ZF161D-01/hero.jpg": {
      "hash": "abc123def456…",
      "cdn_url": "https://res.cloudinary.com/zelexdoll/image/upload/c_fill,w_800/characters/Fusion-ZF161D-01/hero.jpg",
      "file_size_bytes": 245000,
      "uploaded_at": "2026-06-21T14:30:00Z",
      "status": "live"
    },
    "characters/Fusion-ZF161D-01/gallery/01.jpg": {
      "hash": "xyz789abc123…",
      "cdn_url": "https://res.cloudinary.com/zelexdoll/image/upload/c_fill,w_600/characters/Fusion-ZF161D-01/gallery/01.jpg",
      "file_size_bytes": 156000,
      "uploaded_at": "2026-06-21T14:30:15Z",
      "status": "live"
    }
  }
}
```

**Fields:**
- `version` — Manifest format version (increment on breaking changes)
- `generated_at` — UTC timestamp of last update
- `source` — Origin of images (always `howiezz-web`)
- `cdn_provider` — CDN name (e.g., Cloudinary, Bunny, AWS CloudFront)
- `cdn_bucket` — CDN bucket/namespace
- `assets[path]` — Per-image metadata
  - `hash` — SHA256 of original file (for integrity checking)
  - `cdn_url` — Full CDN URL (with transformations)
  - `file_size_bytes` — Uncompressed size
  - `uploaded_at` — UTC timestamp
  - `status` — `live`, `archived`, or `pending`

---

## Uploading Images to CDN

### Prerequisites

1. **CDN credentials** configured locally (environment variables):
   ```bash
   export CDN_API_KEY=your_api_key
   export CDN_API_SECRET=your_secret
   export CDN_BUCKET=zelexdoll
   ```

2. **Python 3.11+** with dependencies:
   ```bash
   pip install requests pillow tqdm
   ```

3. **Local images in:**
   - `assets/characters/` — Character photoshoots
   - `assets/series/` — Series imagery
   - `assets/bodies/` — Body architecture images

### One-Time Setup

```bash
cd E:\HowieZZ\.claude\worktrees\amazing-tu-a4bd34

# Configure CDN provider (Cloudinary example)
python scripts/push_assets_to_cdn.py --init-cloudinary

# This prompts for:
# - CDN API Key
# - CDN API Secret
# - CDN bucket name
# - Image transformations (width, quality, format)
```

### Full Batch Upload

```bash
python scripts/push_assets_to_cdn.py --batch-upload

# Output:
# ✓ Scanning local images... [123 files found]
# ✓ Computing hashes... [100%]
# ✓ Uploading to CDN... [100%] (45 seconds)
# ✓ Generating manifest... [db/assets_manifest.json]
# ✓ Manifest freshness check: OK (generated now)
```

**Time estimate:** ~30 seconds for full batch (260 MB)

### Incremental Upload (Only New Images)

```bash
python scripts/push_assets_to_cdn.py --incremental

# Output:
# ✓ Comparing local vs manifest...
# ✓ New images found: 12
# ✓ Uploading 12 new images... [100%] (8 seconds)
# ✓ Updating manifest... [db/assets_manifest.json]
```

**Time estimate:** ~5-8 seconds for new images only

---

## Refreshing the Manifest

The manifest must be regenerated after:
1. New photoshoots added
2. Gallery images updated
3. Thumbnails regenerated
4. Any mass image change

### Automatic Refresh (CI)

On every push to main, CI automatically:
1. Runs `build_db.py` (scans local images)
2. Runs `push_assets_to_cdn.py --incremental`
3. Validates manifest freshness with `validate_manifest_freshness.py`
4. Fails build if manifest >48 hours old

### Manual Refresh (Local)

```bash
python scripts/push_assets_to_cdn.py --refresh-manifest

# Output:
# ✓ Manifest generated: db/assets_manifest.json
# ✓ Freshness: 0 minutes old ✓
# ✓ Total assets: 256
# ✓ Total size: 258 MB
```

### Verify Manifest Health

```bash
python scripts/validate_manifest_freshness.py

# Output:
# Checking manifest age...
# Last generated: 2026-06-21 14:32 UTC
# Age: 15 minutes old ✓
# Threshold: 48 hours
# Status: HEALTHY
```

---

## Image Delivery at Runtime

### How site.js Loads Images

When a page loads, `site.js` does:

1. **Fetch manifest** from `db/assets_manifest.json`
2. **Resolve URL** via manifest lookup:
   ```javascript
   const charHeroUrl = ZX.img(character);
   // Looks up character.photoshoot.hero path in manifest
   // Returns CDN URL or falls back to git copy
   ```
3. **Fallback to git** if CDN unavailable (after 3-second timeout)

### Image URL Resolution

**In site.js:**

```javascript
ZX.img = function(character) {
  const path = character.photoshoot.hero;
  const manifest = ZX.manifest; // loaded from db/assets_manifest.json
  
  if (manifest && manifest.assets[path]) {
    return manifest.assets[path].cdn_url;  // CDN URL
  }
  return `/assets/${path}`;  // Fallback to git
};
```

**In HTML:**

```html
<img src="..." alt="...">
<!-- site.js fills in from manifest on page load -->
```

---

## Troubleshooting

### Issue: Images 404 on production (CDN URL broken)

**Cause:** Manifest outdated or CDN URL malformed

**Diagnosis:**

```bash
# 1. Check manifest age
python scripts/validate_manifest_freshness.py

# 2. Inspect a specific image
python scripts/debug_manifest.py --path "characters/Fusion-ZF161D-01/hero.jpg"

# Output:
# Path: characters/Fusion-ZF161D-01/hero.jpg
# Hash: abc123def456…
# CDN URL: https://res.cloudinary.com/…
# Status: live
# Size: 245 KB
# Uploaded: 2026-06-21 14:30:00 UTC
```

**Fix:**

1. **If manifest is stale (>48h old):**
   ```bash
   python scripts/push_assets_to_cdn.py --refresh-manifest
   git add db/assets_manifest.json
   git commit -m "chore(assets): refresh manifest (age >48h)"
   git push
   ```

2. **If CDN URL is wrong:**
   ```bash
   python scripts/push_assets_to_cdn.py --revalidate-urls
   # Re-checks all URLs against CDN provider
   ```

### Issue: Upload timeout (slow network)

**Cause:** Large image batch, slow internet, or CDN provider issue

**Fix:**

```bash
# Resume from where it failed
python scripts/push_assets_to_cdn.py --incremental --resume

# Or reduce batch size
python scripts/push_assets_to_cdn.py --batch-upload --max-batch-size 10
```

### Issue: CI fails with "Manifest freshness check failed"

**Cause:** Manifest older than 48 hours

**Fix:**

1. **Locally:**
   ```bash
   python scripts/push_assets_to_cdn.py --refresh-manifest
   git add db/assets_manifest.json
   git commit -m "chore(assets): refresh manifest"
   git push
   ```

2. **In CI (if manual fix needed):**
   - Push to `main` (triggers CI)
   - CI will auto-refresh if authorized

### Issue: Fallback images loading (CDN unreachable)

**Cause:** CDN provider down, network latency, or DNS issues

**Debug in browser:**

```javascript
// Open DevTools console
console.log(ZX.manifest);  // Check if manifest loaded
// Check Network tab for failed CDN requests
// If timeout: network is slow (>3 seconds)
```

**User impact:** Fallback images (git-hosted) display, which is slow but functional. No need for immediate action—monitor and investigate CDN provider status.

---

## Manifest in CI/CD

### Pre-Push Hook

The pre-push hook validates manifest freshness locally:

```bash
scripts/hooks/pre-push
```

If manifest is stale:

```
✗ Manifest freshness check failed
  Manifest age: 72 hours (threshold: 48 hours)
  Please run: python scripts/push_assets_to_cdn.py --refresh-manifest
  Then: git add db/assets_manifest.json && git commit -m "chore(assets): refresh"
```

**To bypass (not recommended):**

```bash
git push --no-verify
```

### GitHub Actions CI

On every push, `.github/workflows/ci.yml` runs:

1. `build_db.py` (scans images)
2. `push_assets_to_cdn.py --incremental` (upload new images)
3. `validate_manifest_freshness.py` (fail if stale)

If validation fails, the build fails and the PR cannot merge until fixed.

---

## Image Transformations

The CDN supports on-the-fly transformations via URL parameters:

```
Base URL:
https://res.cloudinary.com/zelexdoll/image/upload/…

Width limiting:
https://res.cloudinary.com/zelexdoll/image/upload/w_600/…  (max 600px width)

Quality adjustment:
https://res.cloudinary.com/zelexdoll/image/upload/q_80/…  (80% quality)

Format conversion:
https://res.cloudinary.com/zelexdoll/image/upload/f_webp/…  (convert to WebP)

Combined:
https://res.cloudinary.com/zelexdoll/image/upload/c_fill,w_600,q_80,f_webp/…
```

**In manifest:**

```json
{
  "cdn_url": "https://res.cloudinary.com/zelexdoll/image/upload/c_fill,w_800/…"
}
```

The manifest includes transformations already, so no additional URL building needed.

---

## Performance Optimization

### Lazy Loading

Images should be lazy-loaded on grids:

```html
<img src="..." alt="..." loading="lazy">
```

**In site.js:**

```javascript
// Inspect image elements and add loading="lazy" if not present
document.querySelectorAll('img').forEach(img => {
  if (!img.loading) img.loading = 'lazy';
});
```

### Thumbnail Generation

Thumbnails are auto-generated during build pipeline:

```bash
python scripts/make_thumbs.py
```

Creates:
- `*_thumb.jpg` (150px width) for grids
- Full `gallery/*.jpg` (1200px width) for detail pages

All thumbnails are included in the manifest and uploaded to CDN.

---

## Disaster Recovery

### Scenario: CDN Provider Down

**Impact:** All images return 503. Fallback logic kicks in after 3 seconds.

**Recovery:**

1. Switch to fallback provider:
   ```bash
   python scripts/push_assets_to_cdn.py --switch-provider bunny
   ```

2. Regenerate manifest with new provider:
   ```bash
   python scripts/push_assets_to_cdn.py --refresh-manifest
   git add db/assets_manifest.json
   git commit -m "chore(assets): switch CDN provider to Bunny"
   git push
   ```

### Scenario: Manifest Lost/Corrupted

**Recovery:**

```bash
# Regenerate from scratch
python scripts/push_assets_to_cdn.py --refresh-manifest --force

# Verify
python scripts/validate_manifest_freshness.py
```

### Scenario: All Images Lost on CDN

**Recovery:**

```bash
# Re-upload entire catalog
python scripts/push_assets_to_cdn.py --batch-upload --force

# Verify all images reachable
python scripts/test_cdn_availability.py
```

---

## Monitoring

### Daily Health Check

```bash
# Run in cron or scheduled task
python scripts/validate_manifest_freshness.py
python scripts/test_cdn_availability.py
```

**Expected output:**

```
✓ Manifest freshness: OK (12 hours old)
✓ CDN availability: 99.8% (255/256 images reachable)
✓ Average response time: 120ms
```

### Alerts

Set up alerts for:
- Manifest >48 hours old (pre-push hook would catch this)
- CDN availability <98% (investigate provider issue)
- Image 404s on production (investigate manifest sync)

---

## FAQ

**Q: How often should I refresh the manifest?**

A: CI does it automatically on every push. Manually refresh if you add new images outside CI.

**Q: Can I revert to old manifest versions?**

A: Yes, use git history:
```bash
git log db/assets_manifest.json  # Find old version
git checkout <commit-hash> db/assets_manifest.json
git commit -m "chore(assets): revert manifest to <date>"
```

**Q: What if I delete an image locally?**

A: The manifest entry remains. It won't hurt (CDN still has it), but it's orphaned. Clean up:
```bash
python scripts/push_assets_to_cdn.py --cleanup-orphaned
```

**Q: Can I host images on multiple CDNs for redundancy?**

A: Yes, but requires multi-provider support in manifest schema. Currently single-provider. See Phase 2 roadmap.

**Q: How do I test the fallback locally?**

A: Simulate CDN timeout in browser DevTools:
1. Open DevTools → Network tab
2. Throttle to "Slow 4G"
3. Reload page
4. Images fall back to git-hosted after 3 seconds

---

## Support

For CDN issues:
1. Check this runbook (search by keyword)
2. Run diagnostic scripts (see Troubleshooting)
3. Check CDN provider status page
4. Open issue: `chore(cdn): [your issue]`

---

## References

- **Source PDR:** `docs/pdr/PDR-OPS-001-image-cdn.md`
- **Upload Script:** `scripts/push_assets_to_cdn.py`
- **Validation Script:** `scripts/validate_manifest_freshness.py`
- **CI Workflow:** `.github/workflows/ci.yml`
- **Manifest Schema:** `db/assets_manifest_schema.json`
