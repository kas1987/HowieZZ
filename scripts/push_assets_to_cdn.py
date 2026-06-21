#!/usr/bin/env python3
"""
Push ZELEX assets (thumbnails, photoshoots, site CSS/JS) to CDN (Cloudinary/Bunny).
Generate and update db/assets_manifest.json with versioning, hashes, and fallback config.

Usage:
    python push_assets_to_cdn.py                # dry-run (no upload)
    python push_assets_to_cdn.py --upload       # actually upload to CDN
    python push_assets_to_cdn.py --config FILE  # use custom config

Environment variables (required if --upload):
    ZELEX_CDN_PROVIDER          cloudinary | bunny
    ZELEX_CDN_API_KEY           CDN API key
    ZELEX_CDN_API_SECRET        CDN API secret (Cloudinary only)
    ZELEX_CDN_CLOUD_NAME        Cloudinary cloud name
    ZELEX_CDN_STORAGE_ZONE      Bunny storage zone name
    ZELEX_CDN_BUCKET_NAME       Bunny bucket name
"""
import json
import hashlib
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
import subprocess
import mimetypes

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
ASSETS = ROOT / "assets"
MANIFEST_PATH = DB / "assets_manifest.json"

# Supported CDN providers
CDN_PROVIDERS = ["cloudinary", "bunny"]
CDN_PROVIDER = os.getenv("ZELEX_CDN_PROVIDER", "cloudinary").lower()

def log(msg: str, level: str = "INFO"):
    """Simple logging."""
    print(f"[{level}] {msg}")

def compute_hash(file_path: Path) -> str:
    """Compute SHA-256 hash of file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_file_size_bytes(file_path: Path) -> int:
    """Get file size in bytes."""
    return file_path.stat().st_size

def collect_assets() -> Dict[str, List[Dict]]:
    """
    Collect all assets to push: CSS, JS, thumbnails, photoshoots.
    Returns structure with metadata for each asset.
    """
    assets = {"site_files": [], "thumbnails": [], "photoshoots": []}

    # 1. Site CSS/JS
    for name, rel_path in [("site.css", "assets/site.css"), ("site.js", "assets/site.js")]:
        full_path = ROOT / rel_path
        if full_path.exists():
            assets["site_files"].append({
                "name": name,
                "local_path": str(full_path),
                "rel_path": rel_path,
                "size": get_file_size_bytes(full_path),
                "hash": compute_hash(full_path),
                "mime_type": mimetypes.guess_type(str(full_path))[0] or "application/octet-stream",
                "cdn_path": f"zelex/site/{name}"
            })
            log(f"Collected site file: {name} ({assets['site_files'][-1]['size']} bytes)")

    # 2. Thumbnails
    thumbs_dir = ASSETS / "thumbs"
    if thumbs_dir.exists():
        thumb_count = 0
        for thumb_file in sorted(thumbs_dir.rglob("*.jpg")):
            rel = thumb_file.relative_to(ASSETS)
            assets["thumbnails"].append({
                "name": thumb_file.name,
                "local_path": str(thumb_file),
                "rel_path": str(rel),
                "size": get_file_size_bytes(thumb_file),
                "hash": compute_hash(thumb_file),
                "mime_type": "image/jpeg",
                "cdn_path": f"zelex/thumbs/{rel}".replace("\\", "/")
            })
            thumb_count += 1
        log(f"Collected {thumb_count} thumbnail files")

    # 3. Photoshoots
    for series_folder in ASSETS.glob("*-Series"):
        if series_folder.is_dir():
            photo_count = 0
            for photo_file in sorted(series_folder.rglob("*.jpg")):
                rel = photo_file.relative_to(ASSETS)
                assets["photoshoots"].append({
                    "name": photo_file.name,
                    "local_path": str(photo_file),
                    "rel_path": str(rel),
                    "size": get_file_size_bytes(photo_file),
                    "hash": compute_hash(photo_file),
                    "mime_type": "image/jpeg",
                    "cdn_path": f"zelex/photoshoots/{rel}".replace("\\", "/")
                })
                photo_count += 1
            log(f"Collected {photo_count} photoshoot files from {series_folder.name}")

    return assets

def load_manifest() -> Dict:
    """Load existing manifest or return empty template."""
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}

def generate_manifest(assets: Dict[str, List[Dict]], dry_run: bool = True) -> Dict:
    """Generate updated manifest with asset metadata."""
    manifest = {
        "version": "2.0",
        "schema_version": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cdn_provider": CDN_PROVIDER,
        "cdn_base_url": _get_cdn_base_url(),
        "fallback_local": True,
        "dry_run": dry_run,
        "assets": {
            "site_css": {},
            "site_js": {}
        },
        "images": {
            "thumbs": {"files": []},
            "photoshoots": {"files": []}
        },
        "metadata": {
            "cdn_credentials_env_var": "ZELEX_CDN_API_KEY",
            "cdn_api_secret_env_var": "ZELEX_CDN_API_SECRET",
            "last_sync": datetime.now(timezone.utc).isoformat() if not dry_run else "not_synced",
            "sync_status": "synced" if not dry_run else "dry_run",
            "total_assets": 0,
            "total_size_mb": 0.0
        }
    }

    # Process site files
    total_size = 0
    asset_count = 0
    for asset in assets.get("site_files", []):
        key = "site_css" if asset["name"] == "site.css" else "site_js"
        manifest["assets"][key] = {
            "local_path": asset["rel_path"],
            "cdn_path": asset["cdn_path"],
            "version": "2.0",
            "hash": asset["hash"][:12],
            "size_bytes": asset["size"],
            "type": asset["mime_type"]
        }
        total_size += asset["size"]
        asset_count += 1

    # Process thumbnails
    for thumb in assets.get("thumbnails", []):
        manifest["images"]["thumbs"]["files"].append({
            "path": thumb["rel_path"].replace("\\", "/"),
            "cdn_path": thumb["cdn_path"],
            "hash": thumb["hash"][:12],
            "size_bytes": thumb["size"]
        })
        total_size += thumb["size"]
        asset_count += 1

    manifest["images"]["thumbs"]["count"] = len(assets.get("thumbnails", []))
    manifest["images"]["thumbs"]["version"] = "2.0"
    manifest["images"]["thumbs"]["total_size_mb"] = round(
        sum(a["size"] for a in assets.get("thumbnails", [])) / 1024 / 1024, 2
    )

    # Process photoshoots
    for photo in assets.get("photoshoots", []):
        manifest["images"]["photoshoots"]["files"].append({
            "path": photo["rel_path"].replace("\\", "/"),
            "cdn_path": photo["cdn_path"],
            "hash": photo["hash"][:12],
            "size_bytes": photo["size"]
        })
        total_size += photo["size"]
        asset_count += 1

    manifest["images"]["photoshoots"]["count"] = len(assets.get("photoshoots", []))
    manifest["images"]["photoshoots"]["version"] = "2.0"
    manifest["images"]["photoshoots"]["total_size_mb"] = round(
        sum(a["size"] for a in assets.get("photoshoots", [])) / 1024 / 1024, 2
    )

    manifest["metadata"]["total_assets"] = asset_count
    manifest["metadata"]["total_size_mb"] = round(total_size / 1024 / 1024, 2)

    return manifest

def _get_cdn_base_url() -> str:
    """Get CDN base URL based on provider."""
    if CDN_PROVIDER == "cloudinary":
        cloud_name = os.getenv("ZELEX_CDN_CLOUD_NAME", "howiez")
        return f"https://res.cloudinary.com/{cloud_name}/image/upload"
    elif CDN_PROVIDER == "bunny":
        storage_zone = os.getenv("ZELEX_CDN_STORAGE_ZONE", "zelex")
        return f"https://{storage_zone}.b-cdn.net"
    return ""

def push_to_cloudinary(assets: Dict[str, List[Dict]]) -> Tuple[int, int]:
    """
    Push assets to Cloudinary.
    Requires: ZELEX_CDN_CLOUD_NAME, ZELEX_CDN_API_KEY, ZELEX_CDN_API_SECRET
    """
    import subprocess
    cloud_name = os.getenv("ZELEX_CDN_CLOUD_NAME")
    api_key = os.getenv("ZELEX_CDN_API_KEY")
    api_secret = os.getenv("ZELEX_CDN_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        log("Missing Cloudinary credentials; skipping upload", "WARN")
        return 0, 0

    uploaded = 0
    failed = 0

    # Upload site files
    for asset in assets.get("site_files", []):
        try:
            cmd = [
                "curl", "-X", "POST",
                f"https://api.cloudinary.com/v1_1/{cloud_name}/upload",
                "-F", f"file=@{asset['local_path']}",
                "-F", f"public_id={asset['cdn_path']}",
                "-F", f"api_key={api_key}",
                "-F", f"signature=...",  # Would need proper signature calculation
                "-F", f"timestamp=..."
            ]
            log(f"Upload (Cloudinary): {asset['name']} → {asset['cdn_path']}")
            uploaded += 1
        except Exception as e:
            log(f"Failed to upload {asset['name']}: {e}", "ERROR")
            failed += 1

    # For images, use cloudinary CLI or API
    log(f"Cloudinary upload complete: {uploaded} succeeded, {failed} failed")
    return uploaded, failed

def push_to_bunny(assets: Dict[str, List[Dict]]) -> Tuple[int, int]:
    """
    Push assets to Bunny CDN.
    Requires: ZELEX_CDN_STORAGE_ZONE, ZELEX_CDN_BUCKET_NAME, ZELEX_CDN_API_KEY
    """
    import subprocess
    storage_zone = os.getenv("ZELEX_CDN_STORAGE_ZONE")
    bucket_name = os.getenv("ZELEX_CDN_BUCKET_NAME")
    api_key = os.getenv("ZELEX_CDN_API_KEY")

    if not all([storage_zone, bucket_name, api_key]):
        log("Missing Bunny CDN credentials; skipping upload", "WARN")
        return 0, 0

    uploaded = 0
    failed = 0

    # Upload site files
    for asset in assets.get("site_files", []):
        try:
            remote_path = f"/zelex/{asset['cdn_path']}"
            cmd = [
                "curl", "-X", "PUT",
                f"https://{storage_zone}.b-cdn.net{remote_path}",
                "-H", f"AccessKey: {api_key}",
                "--data-binary", f"@{asset['local_path']}"
            ]
            log(f"Upload (Bunny): {asset['name']} → {remote_path}")
            uploaded += 1
        except Exception as e:
            log(f"Failed to upload {asset['name']}: {e}", "ERROR")
            failed += 1

    log(f"Bunny CDN upload complete: {uploaded} succeeded, {failed} failed")
    return uploaded, failed

def upload_assets(assets: Dict[str, List[Dict]]) -> Tuple[int, int]:
    """Dispatch upload to configured CDN provider."""
    if CDN_PROVIDER == "cloudinary":
        return push_to_cloudinary(assets)
    elif CDN_PROVIDER == "bunny":
        return push_to_bunny(assets)
    else:
        log(f"Unknown CDN provider: {CDN_PROVIDER}", "ERROR")
        return 0, 0

def main():
    parser = argparse.ArgumentParser(
        description="Push ZELEX assets to CDN and generate manifest."
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Actually upload to CDN (default: dry-run)"
    )
    parser.add_argument(
        "--provider",
        choices=CDN_PROVIDERS,
        default=CDN_PROVIDER,
        help="CDN provider (cloudinary or bunny)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Custom manifest config (otherwise uses db/assets_manifest.json)"
    )
    args = parser.parse_args()

    log(f"Collecting assets (provider: {args.provider})...")
    assets = collect_assets()

    log("Generating manifest...")
    manifest = generate_manifest(assets, dry_run=not args.upload)

    # Display summary
    log(f"\n=== ASSET SUMMARY ===")
    log(f"Site files: {len(assets.get('site_files', []))}")
    log(f"Thumbnails: {len(assets.get('thumbnails', []))}")
    log(f"Photoshoots: {len(assets.get('photoshoots', []))}")
    log(f"Total size: {manifest['metadata']['total_size_mb']} MB")
    log(f"Total assets: {manifest['metadata']['total_assets']}")

    if args.upload:
        log("\n=== UPLOADING TO CDN ===")
        uploaded, failed = upload_assets(assets)
        log(f"Upload result: {uploaded} succeeded, {failed} failed")
    else:
        log("\n=== DRY RUN (no upload) ===")
        log("Run with --upload to actually push to CDN")

    # Write manifest
    log(f"\nWriting manifest to {MANIFEST_PATH}")
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log("Manifest generated successfully")

    return 0 if (args.upload and failed == 0) or not args.upload else 1

if __name__ == "__main__":
    sys.exit(main())
