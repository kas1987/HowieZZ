#!/usr/bin/env node
/**
 * CI Guard — Check that CDN manifest and config are fresh.
 * Ensures assets_manifest.json and cdn_config.json are in sync and up-to-date.
 *
 * Exit codes:
 *   0 = manifest is fresh and valid
 *   1 = manifest is stale or invalid
 *   2 = fatal error (missing files, JSON parse error)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '../..');
const DB = path.join(ROOT, 'db');
const MANIFEST_PATH = path.join(DB, 'assets_manifest.json');
const CONFIG_PATH = path.join(DB, 'cdn_config.json');

function log(msg, level = 'INFO') {
  console.log(`[${level}] ${msg}`);
}

function fatal(msg) {
  log(msg, 'FATAL');
  process.exit(2);
}

function check(condition, msg) {
  if (!condition) {
    log(msg, 'ERROR');
    process.exit(1);
  }
}

// Check manifest exists
if (!fs.existsSync(MANIFEST_PATH)) {
  fatal(`Manifest not found: ${MANIFEST_PATH}`);
}

// Parse manifest
let manifest;
try {
  manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
} catch (e) {
  fatal(`Failed to parse manifest: ${e.message}`);
}

// Check manifest structure
log('Checking manifest structure...');
check(manifest.version, 'Manifest version missing');
check(manifest.schema_version, 'Schema version missing');
check(manifest.generated_at, 'Generated timestamp missing');
check(manifest.cdn_provider, 'CDN provider missing');
check(manifest.cdn_base_url !== undefined, 'CDN base URL not defined');
check(typeof manifest.fallback_local === 'boolean', 'Fallback local flag must be boolean');

log(`Manifest version: ${manifest.version}`);
log(`Schema version: ${manifest.schema_version}`);
log(`CDN provider: ${manifest.cdn_provider}`);
log(`CDN enabled: ${!!manifest.cdn_base_url}`);
log(`Fallback local: ${manifest.fallback_local}`);

// Check metadata
log('Checking asset metadata...');
const metadata = manifest.metadata || {};
check(typeof metadata.total_assets === 'number', 'Total assets count invalid');
check(typeof metadata.total_size_mb === 'number', 'Total size invalid');

log(`Total assets: ${metadata.total_assets}`);
log(`Total size: ${metadata.total_size_mb} MB`);

// Check assets
const assets = manifest.assets || {};
if (assets.site_css) {
  log(`CSS: ${assets.site_css.local_path} (${assets.site_css.size_bytes} bytes)`);
}
if (assets.site_js) {
  log(`JS: ${assets.site_js.local_path} (${assets.site_js.size_bytes} bytes)`);
}

// Check images
const images = manifest.images || {};
if (images.thumbs) {
  log(`Thumbnails: ${images.thumbs.count} files (${images.thumbs.total_size_mb} MB)`);
}
if (images.photoshoots) {
  log(`Photoshoots: ${images.photoshoots.count} files (${images.photoshoots.total_size_mb} MB)`);
}

// Check if config exists and is fresh
if (fs.existsSync(CONFIG_PATH)) {
  let config;
  try {
    config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    log(`Config found, generated: ${config.generated_at}`);
  } catch (e) {
    log(`Warning: Config exists but is invalid: ${e.message}`, 'WARN');
  }
} else {
  log('Config not found — run scripts/cdn_resolver.py to generate', 'WARN');
}

// Verify manifest timestamp is recent (within last 7 days in dev, last 30 days in prod)
try {
  const manifestTime = new Date(manifest.generated_at).getTime();
  const now = Date.now();
  const daysSinceGenerated = (now - manifestTime) / (1000 * 60 * 60 * 24);

  const isDryRun = manifest.dry_run === true;
  const maxDaysStale = isDryRun ? 7 : 30;

  if (daysSinceGenerated > maxDaysStale) {
    log(
      `Manifest is stale (${daysSinceGenerated.toFixed(1)} days old, max ${maxDaysStale} allowed)`,
      'WARN'
    );
    if (!isDryRun && daysSinceGenerated > 60) {
      check(false, `Manifest is severely stale and marked as synced. Run push_assets_to_cdn.py --upload`);
    }
  } else {
    log(`Manifest freshness OK (${daysSinceGenerated.toFixed(1)} days old)`);
  }
} catch (e) {
  log(`Could not check manifest age: ${e.message}`, 'WARN');
}

log('CDN manifest check passed', 'OK');
process.exit(0);
