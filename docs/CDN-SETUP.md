# ZELEX — CDN & Asset Versioning Setup

## Overview

This document explains the ZELEX Image CDN & Asset Versioning system. The system supports:

1. **Asset Upload Pipeline** — Python script to push images/CSS/JS to CDN
2. **Manifest Versioning** — `db/assets_manifest.json` tracks all assets with hashes and CDN paths
3. **Runtime Configuration** — `db/cdn_config.json` generated for use by `site.js`
4. **Fallback Logic** — Browser-side retry + local fallback when CDN is unavailable
5. **CI Guards** — Automated checks to ensure manifest freshness in CI

---

## Architecture

### Files

| File | Purpose |
|------|---------|
| `db/assets_manifest.json` | Master inventory: all assets, hashes, CDN paths, metadata |
| `db/cdn_config.json` | Runtime config for site.js (CDN URLs, fallback strategy) |
| `scripts/push_assets_to_cdn.py` | Main pipeline: collect assets, compute hashes, upload to CDN |
| `scripts/cdn_resolver.py` | Generate `cdn_config.json` from manifest |
| `.github/scripts/check-cdn-manifest.mjs` | CI guard: validate manifest freshness |
| `assets/site.js` | `ZX.loadCdnConfig()`, `ZX.getCdnUrl()`, `ZX.loadImageWithFallback()` |

### Data Flow

```
(collect assets)
        ↓
  push_assets_to_cdn.py
        ↓
assets_manifest.json (generated with hashes, sizes, CDN paths)
        ↓
  cdn_resolver.py
        ↓
cdn_config.json (runtime config)
        ↓
site.js (ZX.loadCdnConfig → ZX.getCdnUrl → load from CDN or fallback)
```

---

## Setup

### 1. Configure CDN Provider

Choose **Cloudinary** or **Bunny CDN** and set environment variables:

#### Cloudinary

```bash
export ZELEX_CDN_PROVIDER=cloudinary
export ZELEX_CDN_CLOUD_NAME=your_cloud_name
export ZELEX_CDN_API_KEY=your_api_key
export ZELEX_CDN_API_SECRET=your_api_secret
```

#### Bunny CDN

```bash
export ZELEX_CDN_PROVIDER=bunny
export ZELEX_CDN_STORAGE_ZONE=your_storage_zone
export ZELEX_CDN_BUCKET_NAME=your_bucket_name
export ZELEX_CDN_API_KEY=your_api_key
```

### 2. Generate Initial Manifest (Dry-Run)

```bash
python scripts/push_assets_to_cdn.py
```

This collects assets, computes hashes, and generates `db/assets_manifest.json` **without uploading**.

Output:
```
[INFO] Collecting assets (provider: cloudinary)...
[INFO] Collected site file: site.css (45621 bytes)
[INFO] Collected site file: site.js (128934 bytes)
[INFO] Collected 342 thumbnail files
[INFO] Collected 8234 photoshoot files
...
=== ASSET SUMMARY ===
Site files: 2
Thumbnails: 342
Photoshoots: 8234
Total size: 2450.5 MB
Total assets: 8578

=== DRY RUN (no upload) ===
Run with --upload to actually push to CDN

Writing manifest to db/assets_manifest.json
Manifest generated successfully
```

### 3. Review Manifest

```bash
cat db/assets_manifest.json | head -50
```

Verify:
- `cdn_provider` is correct
- `cdn_base_url` is set
- `fallback_local` is `true`
- Asset counts and sizes are reasonable

### 4. Generate CDN Config

```bash
python scripts/cdn_resolver.py
```

This creates `db/cdn_config.json` for use by `site.js`:

```json
{
  "version": "1.0",
  "generated_at": "2026-06-21T...",
  "cdn_enabled": true,
  "cdn_provider": "cloudinary",
  "cdn_base_url": "https://res.cloudinary.com/howiez/image/upload",
  "fallback_local": true,
  "asset_mappings": {
    "site_css": {
      "local_path": "assets/site.css",
      "cdn_url": "https://res.cloudinary.com/howiez/image/upload/zelex/site/site.css"
    },
    "site_js": {
      "local_path": "assets/site.js",
      "cdn_url": "https://res.cloudinary.com/howiez/image/upload/zelex/site/site.js"
    }
  },
  "image_folders": {
    "thumbs": {
      "local_folder": "assets/thumbs",
      "cdn_url_template": "https://res.cloudinary.com/howiez/image/upload/zelex/thumbs/"
    },
    "photoshoots": {
      "local_folder": "assets",
      "cdn_url_template": "https://res.cloudinary.com/howiez/image/upload/zelex/photoshoots/"
    }
  },
  "retry_strategy": {
    "max_attempts": 2,
    "timeout_ms": 5000,
    "fallback_delay_ms": 500
  }
}
```

### 5. Upload to CDN (Production Only)

```bash
python scripts/push_assets_to_cdn.py --upload
```

This actually uploads all assets to the configured CDN provider. The manifest is updated with:
- `last_sync`: timestamp of upload
- `sync_status`: `synced` (instead of `dry_run`)

### 6. Verify Upload

Check the manifest status:

```bash
python -c "import json; m = json.load(open('db/assets_manifest.json')); print(f\"Sync status: {m['metadata']['sync_status']}\\nLast sync: {m['metadata']['last_sync']}\")"
```

---

## Usage in site.js

The runtime CDN logic is fully integrated into `ZX`:

### Load CDN Config

```javascript
// Automatic on page load, or manual:
const config = await ZX.loadCdnConfig();
console.log(config.cdn_enabled);  // true or false
```

### Resolve Asset URL

```javascript
// Returns CDN URL if available, else local path
const cssUrl = ZX.getCdnUrl('assets/site.css');
// → "https://res.cloudinary.com/howiez/image/upload/zelex/site/site.css" (CDN)
// → "assets/site.css" (fallback)
```

### Load Images with Fallback

```javascript
// Load image with auto-retry and fallback
const result = await ZX.loadImageWithFallback('https://res.cloudinary.com/howiez/image/upload/zelex/thumbs/...');
if (result.loaded) {
  // Use CDN image
} else {
  // Fallback to local image
  console.warn('CDN load failed:', result.error);
}
```

### Configuration

In `ZX` (site.js), the retry strategy is configurable:

```javascript
const config = await ZX.loadCdnConfig();
const maxAttempts = config.retry_strategy.max_attempts;  // default: 2
const timeoutMs = config.retry_strategy.timeout_ms;      // default: 5000
```

---

## CI Integration

### Check Manifest Freshness

Add to `.github/workflows/ci.yml`:

```yaml
- name: Guard — CDN manifest freshness
  run: node .github/scripts/check-cdn-manifest.mjs
```

This runs automatically on every push and validates:
- ✓ Manifest exists and is valid JSON
- ✓ All required fields present
- ✓ Manifest is not too old (7 days dev, 30 days prod)
- ✓ CDN config is in sync

Exit codes:
- `0` = manifest is fresh
- `1` = manifest is stale or invalid
- `2` = fatal error (missing files)

---

## Workflow: Update Assets

When you add new photoshoots or thumbnails:

### 1. Add Images Locally

```bash
# Add new photoshoots to assets/Fusion-Series/...
# Add new thumbnails to assets/thumbs/...
```

### 2. Regenerate Manifest (Dry-Run)

```bash
python scripts/push_assets_to_cdn.py
```

This re-scans all asset folders and updates `assets_manifest.json`.

### 3. Review Changes

```bash
git diff db/assets_manifest.json
```

Verify new asset counts match your changes.

### 4. Commit Manifest

```bash
git add db/assets_manifest.json db/cdn_config.json
git commit -m "chore: update CDN manifest with new photoshoots"
```

### 5. Upload to CDN (If Production)

```bash
python scripts/push_assets_to_cdn.py --upload
```

### 6. CI Checks Pass

```bash
git push origin feature-branch
# CI runs check-cdn-manifest.mjs → passes
```

---

## Fallback Behavior

### When CDN Is Down

If `https://res.cloudinary.com/...` is unreachable:

1. Browser attempts to load from CDN (5s timeout)
2. On failure, retries once (if `max_attempts > 1`)
3. On second failure, falls back to local path
4. Local path is always in HTML/JS, so it always loads

### No CDN

If `cdn_enabled: false` in config:

- `ZX.getCdnUrl()` returns the local path
- No CDN URLs are constructed
- Site works normally from local assets

### Image Lazy-Loading

Images use `loading="lazy"`, so failed CDN images don't block page paint:

```html
<img loading="lazy" src="assets/thumbs/..." alt="...">
```

---

## Monitoring

### Log CDN Performance

Enable CDN debug logging:

```javascript
// In browser console:
localStorage.setItem('zx_analytics_debug', '1');
location.reload();
```

Then check console for CDN load events:

```
[ZX CDN] Config loaded: {cdn_enabled: true, ...}
[ZX analytics] {event: 'image_load_failed', error: 'timeout', ...}
```

### Manifest Metrics

Check manifest stats anytime:

```bash
python -c "
import json
m = json.load(open('db/assets_manifest.json'))
print(f\"Total assets: {m['metadata']['total_assets']}\")
print(f\"Total size: {m['metadata']['total_size_mb']} MB\")
print(f\"Sync status: {m['metadata']['sync_status']}\")
print(f\"CDN provider: {m['cdn_provider']}\")
"
```

---

## Troubleshooting

### Manifest is Empty

**Symptom:** `total_assets: 0`, no images listed

**Fix:** Ensure asset folders exist:
```bash
ls assets/thumbs/
ls assets/*-Series/
```

### CDN URLs are Empty

**Symptom:** `cdn_url: ""` in config

**Fix:** Verify environment variables:
```bash
echo $ZELEX_CDN_PROVIDER
echo $ZELEX_CDN_CLOUD_NAME
```

### Upload Fails

**Symptom:** `push_assets_to_cdn.py --upload` fails

**Fix:** Check credentials and CDN connectivity:
```bash
# Cloudinary
curl -X GET "https://api.cloudinary.com/v1_1/$ZELEX_CDN_CLOUD_NAME/resources/image" \
  -u "$ZELEX_CDN_API_KEY:$ZELEX_CDN_API_SECRET"
```

### CI Guard Fails

**Symptom:** `.github/scripts/check-cdn-manifest.mjs` fails with exit 1

**Fix:** Manifest is stale or invalid:
```bash
python scripts/push_assets_to_cdn.py  # regenerate
git add db/assets_manifest.json
git commit -m "chore: refresh CDN manifest"
git push
```

---

## Advanced: Custom CDN Transformations

The manifest supports transformation hints for each image folder:

```json
"images": {
  "thumbs": {
    "transformation": {
      "quality": "auto:low",
      "format": "auto",
      "width": 300
    }
  },
  "photoshoots": {
    "transformation": {
      "quality": "auto:good",
      "format": "auto",
      "responsive": true
    }
  }
}
```

These are hints for the CDN provider (Cloudinary/Bunny) to optimize delivery:
- `quality: auto:low` = use lowest quality that looks acceptable
- `format: auto` = use best format for client (WebP, AVIF, JPEG)
- `width: 300` = resize to 300px (for thumbs)
- `responsive: true` = serve responsive sizes

To implement in `site.js`, enhance `getCdnUrl()` to append transformation parameters:

```javascript
function getCdnUrl(localPath, transformKey = 'default') {
  const tx = _cdnConfig?.transformations?.[transformKey] || {};
  // Append transformation params to CDN URL
  // (provider-specific syntax)
}
```

---

## Next Steps

1. ✓ Set up CDN provider credentials (Cloudinary/Bunny)
2. ✓ Run `push_assets_to_cdn.py` (dry-run)
3. ✓ Review `db/assets_manifest.json`
4. ✓ Run `cdn_resolver.py` to generate config
5. ✓ Test local fallback (`ZX.loadImageWithFallback()`)
6. ✓ Add CI guard to `.github/workflows/ci.yml`
7. ✓ Run `push_assets_to_cdn.py --upload` (production only)
8. ✓ Monitor CI checks and fallback behavior

---

## Support

For questions or issues:
- Check `db/assets_manifest.json` schema in `scripts/push_assets_to_cdn.py`
- Review CI logs: `.github/workflows/ci.yml`
- Test locally: `python -m pytest tests/test_cdn*.py` (if test coverage added)
