#!/usr/bin/env python3
"""
Download every doll-product image we don't already have, from the live catalog
dump (db/live_products.json). Routes each product to its series folder and
derives a folder name from the image filenames (same convention as existing
folders). Skips any image basename already present anywhere under assets/, so
the 77 products we already hold are not re-downloaded.

Usage:
  python scripts/download_assets.py            # all missing doll products
  python scripts/download_assets.py --series SLE,I   # limit to series
  python scripts/download_assets.py --dry-run  # plan only, no downloads
"""

import json, re, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import urllib.request, urllib.error

ROOT   = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
LIVE   = ROOT / "db" / "live_products.json"
CDN    = "https://cdn.shopify.com/s/files/1/0661/6059/1091/files/"
UA     = "Mozilla/5.0 (HowieZZ asset fetch; local use)"
WORKERS = 8
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")

DRY = "--dry-run" in sys.argv
SERIES_FILTER = None
if "--series" in sys.argv:
    SERIES_FILTER = set(sys.argv[sys.argv.index("--series") + 1].split(","))

SERIES_DIR = {"I": "I-Series", "K": "K-Series", "Fusion": "Fusion-Series", "SLE": "SLE-Series"}


def series_of(head, body):
    h, b = (head or ""), (body or "")
    if h.startswith("ZXE") or b.startswith("ZX"):  return "SLE"
    if h.startswith("KE")  or b.startswith("ZK"):  return "K"
    if h.startswith("ZFE") or b.startswith("ZF"):  return "Fusion"
    if h.startswith("GE")  or b.startswith(("ZG", "ZGX")): return "I"
    return None


def folder_name(images, fallback):
    """Folder = most common image stem after stripping the -NNN sequence suffix."""
    stems = Counter()
    for b in images:
        m = re.match(r'(.+?)-\d{2,4}\.\w+$', b)
        if m:
            stems[m.group(1)] += 1
    if stems:
        return stems.most_common(1)[0][0]
    return fallback


def existing_basenames():
    have = set()
    for f in ASSETS.rglob("*"):
        if f.is_file() and f.suffix.lower() in IMG_EXT:
            have.add(f.name)
    return have


def download(url, dest):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if len(data) < 1024:
                raise IOError(f"suspiciously small ({len(data)}b)")
            dest.write_bytes(data)
            return True, len(data)
        except (urllib.error.URLError, urllib.error.HTTPError, IOError, TimeoutError) as e:
            last = e
            time.sleep(1.0 * (attempt + 1))
    return False, str(last)


def main():
    live = json.load(open(LIVE, encoding="utf-8"))
    have = existing_basenames()
    print(f"Already hold {len(have)} image files under assets/")

    jobs = []           # (url, dest_path)
    plan = Counter()    # series -> products planned
    plan_imgs = Counter()  # series -> images planned
    new_folders = Counter()  # series -> folders that don't exist yet
    skipped_products = 0

    for p in live:
        head = body = None
        for v in p.get("variants", []):
            head = head or v.get("head")
            body = body or v.get("body")
        s = series_of(head, body)
        if not s:
            skipped_products += 1
            continue
        if SERIES_FILTER and s not in SERIES_FILTER:
            continue

        imgs = [b for b in p.get("images", []) if b.lower().endswith(IMG_EXT)]
        if not imgs:
            continue
        fol = folder_name(imgs, fallback=(p.get("variants", [{}])[0].get("sku") or p["handle"]))
        # sanitize folder name for Windows
        fol = re.sub(r'[<>:"/\\|?*]', "_", fol).strip()
        dest_dir = ASSETS / SERIES_DIR[s] / fol

        missing = [b for b in imgs if b not in have]
        if not missing:
            continue
        plan[s] += 1
        plan_imgs[s] += len(missing)
        if not dest_dir.exists():
            new_folders[s] += 1
        for b in missing:
            jobs.append((CDN + b, dest_dir / b))
            have.add(b)   # avoid duplicate queueing across products sharing an image

    print(f"\nPlan: {len(jobs)} images to download across {sum(plan.values())} products")
    for s, n in plan.items():
        print(f"  {SERIES_DIR[s]}: {n} products, {plan_imgs[s]} images "
              f"({new_folders[s]} new folders, {n - new_folders[s]} adding to existing)")
    print(f"  ({skipped_products} non-doll live listings skipped: heads-only, torsos, extras)")

    if DRY:
        print("\n--dry-run: no downloads performed.")
        return
    if not jobs:
        print("\nNothing to download.")
        return

    # Create dirs
    for _, dest in jobs:
        dest.parent.mkdir(parents=True, exist_ok=True)

    ok = fail = 0
    failures = []
    print(f"\nDownloading with {WORKERS} workers...")
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        fut = {ex.submit(download, url, dest): (url, dest) for url, dest in jobs}
        for i, f in enumerate(as_completed(fut), 1):
            url, dest = fut[f]
            success, info = f.result()
            if success:
                ok += 1
            else:
                fail += 1
                failures.append({"url": url, "dest": str(dest.relative_to(ASSETS)), "error": str(info)})
            if i % 100 == 0:
                print(f"  {i}/{len(jobs)}  (ok={ok} fail={fail})")

    print(f"\nDone. Downloaded {ok}, failed {fail}.")
    report = {"downloaded": ok, "failed": fail, "failures": failures}
    (ROOT / "db" / "download_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if failures:
        print(f"  {fail} failures logged to db/download_report.json")
    print("\nNext: python scripts/build_db.py --reset   (index the new products)")


if __name__ == "__main__":
    main()
