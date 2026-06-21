# ZELEX CDN & Asset Versioning — Implementation Guide

## Overview

This implementation provides a complete, production-ready CDN infrastructure for the ZELEX Character Atlas with automatic asset versioning, intelligent fallback, and CI guards.

### Key Features

1. **Asset Pipeline** (`push_assets_to_cdn.py`)
   - Scans local assets (CSS, JS, thumbnails, photoshoots)
   - Computes SHA-256 hashes for versioning
   - Generates comprehensive manifest
   - Uploads to Cloudinary or Bunny CDN (with credentials)

2. **Manifest System** (`db/assets_manifest.json`)
   - Complete asset inventory with metadata
   - Hash-based versioning for cache-busting
   - File sizes and CDN paths
   - Sync status tracking

3. **Runtime Config** (`db/cdn_config.json`)
   - Generated from manifest for browser use
   - CDN URL mappings for all asset types
   - Retry strategy configuration
   - Fallback settings

4. **Browser-Side Fallback** (site.js enhancements)
   - `ZX.loadCdnConfig()` — async config loader
   - `ZX.getCdnUrl()` — CDN URL resolver
   - `ZX.loadImageWithFallback()` — retry + fallback logic
   - Graceful degradation when CDN is unavailable

5. **CI Guardrails** (`.github/scripts/check-cdn-manifest.mjs`)
   - Validates manifest schema and freshness
   - Checks manifest age (7 days dev, 30 days prod)
   - Prevents stale assets from reaching production
   - Integration with GitHub Actions

---

## Quick Start

### 1. Generate Manifest (Local Development)

```bash
# Collect assets and compute hashes (dry-run, no upload)
python scripts/push_assets_to_cdn.py

# Output:
# [INFO] Collected site file: site.css (45621 bytes)
# [INFO] Collected site file: site.js (128934 bytes)
# [INFO] Collected 342 thumbnail files
# [INFO] Collected 8234 photoshoot files
# ...
# Writing manifest to db/assets_manifest.json
```

This creates `db/assets_manifest.json` with:
- All asset metadata (path, size, hash)
- CDN provider and base URL
- Fallback configuration
- Sync status: `dry_run`

### 2. Generate Runtime Config

```bash
python scripts/cdn_resolver.py

# Output:
# Generated CDN config: db/cdn_config.json
# CDN enabled: false
# Fallback local: true
```

This creates `db/cdn_config.json` used by site.js at runtime.

### 3. Test Locally

```bash
# Start dev server
python serve.py

# Or use Caddy
caddy run
```

Visit `http://localhost:8000` and check console for CDN debug output:

```javascript
// In browser console
localStorage.setItem('zx_analytics_debug', '1');
location.reload();

// Then check console
// [ZX CDN] Config loaded: {cdn_enabled: false, fallback_local: true, ...}
```

### 4. Upload to CDN (Production Only)

Set environment variables and upload:

```bash
export ZELEX_CDN_PROVIDER=cloudinary
export ZELEX_CDN_CLOUD_NAME=howiez
export ZELEX_CDN_API_KEY=...
export ZELEX_CDN_API_SECRET=...

python scripts/push_assets_to_cdn.py --upload

# Output:
# [INFO] Upload (Cloudinary): site.css → zelex/site/site.css
# [INFO] Upload (Cloudinary): site.js → zelex/site/site.js
# [INFO] Cloudinary upload complete: 8578 succeeded, 0 failed
#
# Manifest updated:
# - sync_status: synced
# - last_sync: 2026-06-21T15:30:00Z
```

### 5. Commit and Push

```bash
git add db/assets_manifest.json db/cdn_config.json
git commit -m "chore: CDN manifest sync with production assets"
git push origin main

# CI runs check-cdn-manifest.mjs automatically
```

---

## Files Created

### Core Pipeline

| File | Purpose | Type |
|------|---------|------|
| `scripts/push_assets_to_cdn.py` | Main asset collection & upload pipeline | Python |
| `scripts/cdn_resolver.py` | Generate runtime config from manifest | Python |
| `db/assets_manifest.json` | Master asset inventory with hashes | JSON |
| `db/cdn_config.json` | Runtime config for site.js | JSON |

### Site Integration

| File | Purpose | Type |
|------|---------|------|
| `assets/site.js` | Enhanced with CDN module (loadCdnConfig, getCdnUrl, loadImageWithFallback) | JavaScript |

### Testing

| File | Purpose | Type |
|------|---------|------|
| `tests/test_cdn_setup.py` | Unit tests for asset collection & manifest generation | Python |
| `tests/site-cdn.test.js` | Unit tests for browser-side CDN functions | JavaScript |

### CI/CD

| File | Purpose | Type |
|------|---------|------|
| `.github/scripts/check-cdn-manifest.mjs` | CI guard for manifest freshness | Node.js |
| `.github/workflows/ci.yml` | Updated to run CDN manifest check | YAML |

### Documentation

| File | Purpose |
|------|---------|
| `docs/CDN-SETUP.md` | Comprehensive CDN setup & configuration guide |
| `CDN-README.md` | This file |

---

## Manifest Schema

### `db/assets_manifest.json` Structure

```json
{
  "version": "2.0",
  "schema_version": "2026-06-21",
  "generated_at": "2026-06-21T15:30:00Z",
  "cdn_provider": "cloudinary",
  "cdn_base_url": "https://res.cloudinary.com/howiez/image/upload",
  "fallback_local": true,
  "dry_run": true,
  "assets": {
    "site_css": {
      "local_path": "assets/site.css",
      "cdn_path": "zelex/site/site.css",
      "version": "2.0",
      "hash": "a1b2c3d4",
      "size_bytes": 45621,
      "type": "text/css"
    },
    "site_js": {
      "local_path": "assets/site.js",
      "cdn_path": "zelex/site/site.js",
      "version": "2.0",
      "hash": "e5f6g7h8",
      "size_bytes": 128934,
      "type": "application/javascript"
    }
  },
  "images": {
    "thumbs": {
      "count": 342,
      "version": "2.0",
      "total_size_mb": 125.4,
      "files": [
        {
          "path": "thumbs/Fusion-Series/ZFE01_1+ZF161D/ZFE01_1_ZF161D-101.jpg",
          "cdn_path": "zelex/thumbs/Fusion-Series/ZFE01_1+ZF161D/ZFE01_1_ZF161D-101.jpg",
          "hash": "i9j0k1l2",
          "size_bytes": 45000
        }
      ]
    },
    "photoshoots": {
      "count": 8234,
      "version": "2.0",
      "total_size_mb": 2325.1,
      "files": [...]
    }
  },
  "metadata": {
    "cdn_credentials_env_var": "ZELEX_CDN_API_KEY",
    "cdn_api_secret_env_var": "ZELEX_CDN_API_SECRET",
    "last_sync": "2026-06-21T15:30:00Z",
    "sync_status": "synced",
    "total_assets": 8578,
    "total_size_mb": 2450.5
  }
}
```

---

## Runtime Configuration

### `db/cdn_config.json` Structure

```json
{
  "version": "1.0",
  "generated_at": "2026-06-21T15:30:00Z",
  "cdn_enabled": true,
  "cdn_provider": "cloudinary",
  "cdn_base_url": "https://res.cloudinary.com/howiez/image/upload",
  "fallback_local": true,
  "asset_mappings": {
    "site_css": {
      "local_path": "assets/site.css",
      "cdn_path": "zelex/site/site.css",
      "cdn_url": "https://res.cloudinary.com/howiez/image/upload/zelex/site/site.css",
      "hash": "a1b2c3d4",
      "size_bytes": 45621,
      "type": "text/css"
    },
    "site_js": {
      "local_path": "assets/site.js",
      "cdn_path": "zelex/site/site.js",
      "cdn_url": "https://res.cloudinary.com/howiez/image/upload/zelex/site/site.js",
      "hash": "e5f6g7h8",
      "size_bytes": 128934,
      "type": "application/javascript"
    }
  },
  "image_folders": {
    "thumbs": {
      "local_folder": "assets/thumbs",
      "cdn_folder": "zelex/thumbs",
      "cdn_url_template": "https://res.cloudinary.com/howiez/image/upload/zelex/thumbs/",
      "count": 342,
      "total_size_mb": 125.4,
      "transformations": {
        "quality": "auto:low",
        "format": "auto",
        "width": 300
      }
    },
    "photoshoots": {
      "local_folder": "assets",
      "cdn_folder": "zelex/photoshoots",
      "cdn_url_template": "https://res.cloudinary.com/howiez/image/upload/zelex/photoshoots/",
      "count": 8234,
      "total_size_mb": 2325.1,
      "transformations": {
        "quality": "auto:good",
        "format": "auto",
        "responsive": true
      }
    }
  },
  "retry_strategy": {
    "max_attempts": 2,
    "timeout_ms": 5000,
    "fallback_delay_ms": 500
  }
}
```

---

## Browser-Side API

All functions are accessed via the `ZX` global object.

### Load CDN Config

```javascript
// Automatic on DOMContentLoaded, or manual:
const config = await ZX.loadCdnConfig();

console.log(config.cdn_enabled);      // true or false
console.log(config.cdn_provider);     // "cloudinary", "bunny", or "none"
console.log(config.fallback_local);   // true (always)
```

### Resolve Asset URL

```javascript
// Get CDN URL for a local path
const cssUrl = ZX.getCdnUrl('assets/site.css');
// → "https://res.cloudinary.com/howiez/image/upload/zelex/site/site.css" (CDN)
// → "assets/site.css" (fallback)

const thumbUrl = ZX.getCdnUrl('assets/thumbs/Fusion-Series/.../file.jpg');
// → "https://res.cloudinary.com/howiez/image/upload/zelex/thumbs/..." (CDN)
// → "assets/thumbs/..." (fallback)
```

### Load Image with Retry + Fallback

```javascript
// Load image with automatic retry and fallback
const result = await ZX.loadImageWithFallback('https://res.cloudinary.com/howiez/image/upload/zelex/thumbs/...');

if (result.loaded) {
  // CDN image loaded successfully
  console.log('Image loaded:', result.src);
} else {
  // CDN failed, fallback used
  console.warn('CDN load failed:', result.error, '- using fallback:', result.src);
}
```

### Debug Logging

Enable detailed CDN logging:

```javascript
// In browser console
localStorage.setItem('zx_analytics_debug', '1');
location.reload();

// Then check console for CDN events:
// [ZX CDN] Config loaded: {...}
// [ZX analytics] {event: 'image_load_retry', attempt: 1, ...}
// [ZX analytics] {event: 'image_load_failed', error: 'timeout', ...}
```

---

## Testing

### Python Tests

```bash
# Run CDN setup tests
python -m pytest tests/test_cdn_setup.py -v

# Expected output:
# test_cdn_setup.py::TestHashComputation::test_compute_hash_consistency PASSED
# test_cdn_setup.py::TestHashComputation::test_compute_hash_different_content PASSED
# test_cdn_setup.py::TestFileSizeBytes::test_get_file_size_bytes PASSED
# test_cdn_setup.py::TestManifestGeneration::test_generate_manifest_dry_run PASSED
# ...
# 15 passed in 0.23s
```

### JavaScript Tests

```bash
# Run all JS tests (including CDN)
npm test

# Expected output:
# ✓ tests/site-cdn.test.js (12 tests)
# ...
# Test Files  3 passed (3)
#      Tests  50 passed (50)
```

### CI Tests

```bash
# Run CI manifest check locally
node .github/scripts/check-cdn-manifest.mjs

# Expected output:
# [INFO] Checking manifest structure...
# [INFO] Manifest version: 2.0
# [INFO] Schema version: 2026-06-21
# [INFO] CDN provider: cloudinary
# [INFO] CDN enabled: true
# [INFO] Fallback local: true
# [INFO] Total assets: 8578
# [INFO] Total size: 2450.5 MB
# [INFO] CDN manifest check passed
# exit 0
```

---

## Troubleshooting

### Issue: Manifest is Empty

**Symptoms:**
- `total_assets: 0` in manifest
- No files listed in image folders

**Diagnosis:**
```bash
ls -la assets/thumbs/
ls -la assets/*-Series/
```

**Fix:** Ensure asset directories exist with correct structure.

### Issue: CDN URLs are Not Being Used

**Symptoms:**
- `cdn_enabled: false` in config
- Browser always loads from local paths

**Diagnosis:**
```javascript
ZX.loadCdnConfig().then(cfg => console.log(cfg));
```

**Fix:** Verify environment variables are set:
```bash
echo $ZELEX_CDN_PROVIDER
echo $ZELEX_CDN_CLOUD_NAME
```

### Issue: Upload Fails with "Invalid Credentials"

**Symptoms:**
- `push_assets_to_cdn.py --upload` fails
- Error: "Unauthorized" or "Invalid API key"

**Fix:**
```bash
# Cloudinary: verify credentials
curl -u "$ZELEX_CDN_API_KEY:$ZELEX_CDN_API_SECRET" \
  "https://api.cloudinary.com/v1_1/$ZELEX_CDN_CLOUD_NAME/resources/image?max_results=1"

# Bunny CDN: verify API key
curl -H "AccessKey: $ZELEX_CDN_API_KEY" \
  "https://$ZELEX_CDN_STORAGE_ZONE.b-cdn.net/"
```

### Issue: CI Guard Fails

**Symptoms:**
- `check-cdn-manifest.mjs` fails with exit 1
- Error: "Manifest is stale"

**Fix:**
```bash
# Regenerate manifest
python scripts/push_assets_to_cdn.py

# Commit and push
git add db/assets_manifest.json db/cdn_config.json
git commit -m "chore: refresh CDN manifest"
git push
```

---

## Maintenance

### Weekly: Check Manifest Freshness

```bash
# View last sync time
python -c "import json; m = json.load(open('db/assets_manifest.json')); \
  print(f\"Last sync: {m['metadata']['last_sync']}\\nStatus: {m['metadata']['sync_status']}\")"
```

### Monthly: Re-Upload to CDN

```bash
# Ensure assets are fresh
python scripts/push_assets_to_cdn.py --upload

# Commit if changes detected
git add db/assets_manifest.json
git commit -m "chore: re-sync CDN assets"
```

### After Adding New Photoshoots/Thumbnails

```bash
# 1. Copy images to local folders
# 2. Regenerate manifest
python scripts/push_assets_to_cdn.py

# 3. Review changes
git diff db/assets_manifest.json | head -50

# 4. Commit manifest
git add db/assets_manifest.json db/cdn_config.json
git commit -m "chore: add new photoshoots to CDN manifest"

# 5. Upload to CDN (if production)
python scripts/push_assets_to_cdn.py --upload
```

---

## Performance Metrics

### Asset Sizes (Typical)

| Asset | Count | Size |
|-------|-------|------|
| Site CSS | 1 | ~45 KB |
| Site JS | 1 | ~130 KB |
| Thumbnails | ~342 | ~125 MB |
| Photoshoots | ~8,234 | ~2.3 GB |
| **Total** | ~8,578 | ~2.4 GB |

### CDN Performance (Cloudinary)

- Automatic image optimization (format, quality, compression)
- Global CDN with ~275 data centers
- Responsive image delivery
- Estimated 60-80% bandwidth reduction vs. unoptimized

### Browser-Side Fallback

- Retry timeout: 5 seconds per attempt
- Max attempts: 2
- Fallback delay: 500ms between attempts
- Total max wait: ~10 seconds before falling back to local

---

## Future Enhancements

1. **Image Transformations**
   - Cloudinary URL-based transformations (resize, crop, quality)
   - AVIF/WebP format negotiation
   - Responsive image srcset generation

2. **Analytics Integration**
   - Track CDN vs. local asset loads
   - Monitor fallback rates
   - Alert on unusual CDN failures

3. **Cache Headers**
   - Set-Cache-Control headers in CI
   - Invalidate CDN cache on manifest update

4. **Multi-CDN Failover**
   - Try primary CDN (Cloudinary)
   - Fall back to secondary CDN (Bunny)
   - Final fallback to local

5. **Asset Compression**
   - Gzip site.css/site.js
   - WebP thumbnails alongside JPEG
   - AVIF support for modern browsers

---

## Support & Questions

For detailed setup and configuration, see `docs/CDN-SETUP.md`.

For API reference, see inline comments in:
- `scripts/push_assets_to_cdn.py`
- `scripts/cdn_resolver.py`
- `assets/site.js` (CDN module)
- `.github/scripts/check-cdn-manifest.mjs`

---

## Summary

✓ Complete asset pipeline with versioning  
✓ Automatic hash computation for cache-busting  
✓ Manifest schema with metadata and sync status  
✓ Runtime configuration for browser-side usage  
✓ Intelligent retry and fallback logic  
✓ CI guards for manifest freshness  
✓ Comprehensive testing (Python + JavaScript)  
✓ Full documentation and troubleshooting  

**Status:** Production-ready. Ready to integrate with Cloudinary or Bunny CDN.
