#!/usr/bin/env python3
"""
CDN URL resolver and fallback configuration generator.
Generates a cdn_config.json file used by site.js at runtime.

This script reads the assets_manifest.json and produces a runtime config
that site.js uses to decide whether to load assets from CDN or local fallback.
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
MANIFEST_PATH = DB / "assets_manifest.json"
CONFIG_PATH = DB / "cdn_config.json"

def generate_cdn_config(manifest_path: Path = MANIFEST_PATH) -> dict:
    """Generate runtime CDN configuration from manifest."""
    if not manifest_path.exists():
        return _fallback_config()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    cdn_provider = manifest.get("cdn_provider", "cloudinary")
    cdn_base_url = manifest.get("cdn_base_url", "")
    fallback_local = manifest.get("fallback_local", True)

    config = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cdn_enabled": bool(cdn_base_url),
        "cdn_provider": cdn_provider,
        "cdn_base_url": cdn_base_url,
        "fallback_local": fallback_local,
        "asset_mappings": {
            "site_css": _map_asset(manifest.get("assets", {}).get("site_css", {}), cdn_base_url),
            "site_js": _map_asset(manifest.get("assets", {}).get("site_js", {}), cdn_base_url)
        },
        "image_folders": {
            "thumbs": _map_folder(
                manifest.get("images", {}).get("thumbs", {}),
                cdn_base_url,
                "zelex/thumbs"
            ),
            "photoshoots": _map_folder(
                manifest.get("images", {}).get("photoshoots", {}),
                cdn_base_url,
                "zelex/photoshoots"
            )
        },
        "transformations": {
            "thumbs": {
                "quality": "auto:low",
                "format": "auto",
                "width": 300
            },
            "photoshoots": {
                "quality": "auto:good",
                "format": "auto",
                "responsive": True
            }
        },
        "retry_strategy": {
            "max_attempts": 2,
            "timeout_ms": 5000,
            "fallback_delay_ms": 500
        }
    }

    return config

def _map_asset(asset_data: dict, cdn_base_url: str) -> dict:
    """Map a single asset (CSS/JS) to CDN URL."""
    local_path = asset_data.get("local_path", "")
    cdn_path = asset_data.get("cdn_path", "")

    cdn_url = ""
    if cdn_base_url and cdn_path:
        cdn_url = f"{cdn_base_url}/{cdn_path}"

    return {
        "local_path": local_path,
        "cdn_path": cdn_path,
        "cdn_url": cdn_url,
        "hash": asset_data.get("hash", ""),
        "size_bytes": asset_data.get("size_bytes", 0),
        "type": asset_data.get("type", "")
    }

def _map_folder(folder_data: dict, cdn_base_url: str, default_cdn_folder: str) -> dict:
    """Map a folder of images to CDN URL template."""
    local_folder = folder_data.get("local_folder", "")
    cdn_folder = folder_data.get("cdn_folder", default_cdn_folder)

    cdn_url_template = ""
    if cdn_base_url and cdn_folder:
        cdn_url_template = f"{cdn_base_url}/{cdn_folder}/"

    return {
        "local_folder": local_folder,
        "cdn_folder": cdn_folder,
        "cdn_url_template": cdn_url_template,
        "count": folder_data.get("count", 0),
        "total_size_mb": folder_data.get("total_size_mb", 0),
        "transformations": folder_data.get("transformation", {})
    }

def _fallback_config() -> dict:
    """Return fallback config when manifest doesn't exist."""
    return {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cdn_enabled": False,
        "cdn_provider": "none",
        "cdn_base_url": "",
        "fallback_local": True,
        "asset_mappings": {
            "site_css": {"local_path": "assets/site.css", "cdn_url": ""},
            "site_js": {"local_path": "assets/site.js", "cdn_url": ""}
        },
        "image_folders": {
            "thumbs": {"local_folder": "assets/thumbs", "cdn_url_template": ""},
            "photoshoots": {"local_folder": "assets", "cdn_url_template": ""}
        },
        "retry_strategy": {
            "max_attempts": 1,
            "timeout_ms": 5000,
            "fallback_delay_ms": 500
        }
    }

def main():
    """Generate and write CDN config."""
    config = generate_cdn_config()
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"Generated CDN config: {CONFIG_PATH}")
    print(f"CDN enabled: {config['cdn_enabled']}")
    print(f"Fallback local: {config['fallback_local']}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
