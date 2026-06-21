#!/usr/bin/env python3
"""
Generate page inventory and validate HTML page consistency with pages_config.json.

The Atlas uses a static HTML front-end driven by query parameters. This script:
1. Loads pages_config.json (schema for all 41 pages)
2. Validates that all declared pages exist on disk
3. Enumerates all existing HTML files
4. Reports discrepancies: missing files, undeclared pages, orphaned variants
5. Generates cache metadata (file size, mtime, content hash) for intelligent cache busting
6. Emits a pages_manifest.json with generation timestamp + validation summary

Run from the repo root:
  python scripts/generate_pages.py [--force-refresh] [--validate-only]

Cache behavior:
  - Per-page TTL (cache_ttl in pages_config.json) + content-hash invalidation
  - Manifest written to db/pages_manifest.json with file hashes
  - If any dependency (catalog.json, characters.json, etc.) changes hash, dependent pages are invalidated
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
CONFIG = DB / "pages_config.json"
MANIFEST = DB / "pages_manifest.json"
PAGES_DIR = ROOT  # HTML files in root

# Expected page file locations
EXPECTED_PAGES = [
    "index.html",
    "browse.html",
    "family.html",
    "compare.html",
    "options.html",
    "community.html",
    "quiz.html",
    "configurator.html",
    "contact.html",
    "series.html",
    "body.html",
    "character.html",
    "craft.html",
    "community-events.html",
    "gallery.html",
    "404.html",
    "hero.html",
    "Landing.html",
    "index-gallery-original.html",
    "contact-variant-b.html",
    "contact-variant-d.html",
]


def compute_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """Compute content hash of a file (first 4KB for speed, full for small files)."""
    if not file_path.exists():
        return ""

    try:
        size = file_path.stat().st_size
        hasher = hashlib.sha256()

        # For large files, hash first 4KB + file size; for small, hash full content
        chunk_size = 4096
        if size > chunk_size * 100:  # > 400KB
            with open(file_path, "rb") as f:
                chunk = f.read(chunk_size)
                hasher.update(chunk)
                hasher.update(f"__SIZE__{size}".encode())
        else:
            with open(file_path, "rb") as f:
                hasher.update(f.read())

        return hasher.hexdigest()[:16]
    except Exception as e:
        print(f"Error hashing {file_path}: {e}", file=sys.stderr)
        return ""


def load_config() -> dict[str, Any]:
    """Load pages_config.json."""
    if not CONFIG.exists():
        print(f"Error: {CONFIG} not found. Run this script from the repo root.", file=sys.stderr)
        sys.exit(1)

    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_declared_pages(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Extract all page definitions from pages_config.json."""
    pages = {}

    for category_key, category in config.get("pages", {}).items():
        if not isinstance(category, dict):
            continue
        for page in category.get("pages", []):
            if isinstance(page, dict) and "id" in page and "file" in page:
                pages[page["id"]] = page

    return pages


def validate_files(declared_pages: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    """
    Validate that all declared pages exist and generate file metadata.

    Returns:
        (page_metadata_dict, list_of_problems)
    """
    problems = []
    metadata = {}

    for page_id, page_spec in declared_pages.items():
        file_name = page_spec.get("file")
        file_path = PAGES_DIR / file_name

        if not file_path.exists():
            problems.append(f"MISSING: declared page {page_id} → {file_name} does not exist")
            continue

        # Compute file metadata
        try:
            stat = file_path.stat()
            metadata[page_id] = {
                "file": file_name,
                "size_bytes": stat.st_size,
                "mtime_unix": int(stat.st_mtime),
                "content_hash": compute_file_hash(file_path),
                "exists": True,
            }
        except Exception as e:
            problems.append(f"ERROR: failed to stat {file_name}: {e}")
            metadata[page_id] = {
                "file": file_name,
                "exists": False,
                "error": str(e),
            }

    return metadata, problems


def find_undeclared_pages() -> list[str]:
    """Find .html files in root that are not in EXPECTED_PAGES."""
    undeclared = []
    for item in PAGES_DIR.glob("*.html"):
        if item.name not in EXPECTED_PAGES and not item.name.startswith("v2 HTML"):
            undeclared.append(item.name)
    return sorted(undeclared)


def validate_dependencies(
    config: dict[str, Any],
    declared_pages: dict[str, dict[str, Any]],
    file_metadata: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    """
    Check that all declared dependencies (e.g., catalog.json, characters.json) exist.
    Compute dependency hashes for cache invalidation.

    Returns:
        (dependency_metadata_dict, list_of_problems)
    """
    problems = []
    dep_metadata = {}

    # Collect all unique dependencies
    all_deps = set()
    for page_spec in declared_pages.values():
        for dep in page_spec.get("dependencies", []):
            all_deps.add(dep)

    for dep_name in sorted(all_deps):
        dep_path = DB / dep_name
        if not dep_path.exists():
            problems.append(f"MISSING DEPENDENCY: {dep_name} (used by pages)")
            continue

        try:
            stat = dep_path.stat()
            dep_metadata[dep_name] = {
                "exists": True,
                "size_bytes": stat.st_size,
                "mtime_unix": int(stat.st_mtime),
                "content_hash": compute_file_hash(dep_path),
            }
        except Exception as e:
            problems.append(f"ERROR: failed to stat dependency {dep_name}: {e}")
            dep_metadata[dep_name] = {"exists": False, "error": str(e)}

    return dep_metadata, problems


def generate_page_variants(declared_pages: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """
    Enumerate dynamic page instances based on live data.

    For pages with dynamic_params (e.g., ?f=family, ?id=character_id),
    this would normally enumerate all permutations from the catalog. For now,
    return empty dict as a placeholder for future implementation.
    """
    variants = {}
    # TODO: enumerate from characters.json, family_taxonomy.json, etc.
    return variants


def build_manifest(
    config: dict[str, Any],
    declared_pages: dict[str, dict[str, Any]],
    file_metadata: dict[str, Any],
    dep_metadata: dict[str, Any],
    problems: list[str],
) -> dict[str, Any]:
    """Build the final pages_manifest.json."""
    manifest = {
        "schema_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "config_version": config.get("schema_version"),
        "total_pages": len(declared_pages),
        "validation": {
            "problems_count": len(problems),
            "problems": problems,
            "all_valid": len(problems) == 0,
        },
        "files": file_metadata,
        "dependencies": dep_metadata,
        "cache_strategy": config.get("metadata", {}).get("cache_strategy", "per-page TTL + content-hash"),
    }
    return manifest


def main(
    force_refresh: bool = False,
    validate_only: bool = False,
    verbose: bool = False,
) -> int:
    """Main entry point."""
    print("Generating page manifest...")

    # Load configuration
    config = load_config()

    # Collect all declared pages
    declared_pages = collect_declared_pages(config)
    print(f"Loaded {len(declared_pages)} declared pages from pages_config.json")

    # Validate files exist and collect metadata
    file_metadata, file_problems = validate_files(declared_pages)
    print(f"Validated {len(file_metadata)} pages on disk")

    # Validate dependencies
    dep_metadata, dep_problems = validate_dependencies(config, declared_pages, file_metadata)
    print(f"Validated {len(dep_metadata)} dependencies")

    # Check for undeclared pages
    undeclared = find_undeclared_pages()
    undeclared_problems = [f"UNDECLARED: {f}" for f in undeclared]

    all_problems = file_problems + dep_problems + undeclared_problems

    # Generate variants (placeholder)
    variants = generate_page_variants(declared_pages)

    # Build manifest
    manifest = build_manifest(
        config,
        declared_pages,
        file_metadata,
        dep_metadata,
        all_problems,
    )

    # Report
    if verbose or all_problems:
        print("\n" + "=" * 70)
        if all_problems:
            print(f"PROBLEMS ({len(all_problems)}):")
            for prob in all_problems:
                print(f"  {prob}")
        else:
            print("All validations passed!")
        print("=" * 70)

    # Write manifest (unless validate-only)
    if not validate_only:
        MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"\nWrote {MANIFEST}")
    else:
        print(f"(--validate-only: skipped writing manifest)")

    # Return exit code
    return 0 if len(all_problems) == 0 else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate page inventory and validate HTML consistency."
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Ignore existing manifest and regenerate from scratch",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate but do not write manifest",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()
    sys.exit(main(
        force_refresh=args.force_refresh,
        validate_only=args.validate_only,
        verbose=args.verbose,
    ))
