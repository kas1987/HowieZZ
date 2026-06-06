#!/usr/bin/env python3
"""
Pull the live Zelexdoll catalog (Shopify JSON) and reconcile it against our
local asset catalog to:
  1. Backfill body/face codes for products whose folder name dropped them.
  2. Capture per-SKU variants (price, skin tone, options) for the rebuild.
  3. Diff live image lists against our downloaded files to flag missing assets.

Outputs (all under db/, consumed by build_db.py):
  db/live_products.json     raw-ish dump of every live product (trimmed)
  db/live_variants.json     flat per-SKU variant list
  db/product_overrides.json our_product_code -> {body_code, face_code, sku, ...}
  db/asset_gaps.json        our_product_code -> [missing image filenames]

Usage:
  python scripts/fetch_catalog.py            # uses /products.json
  python scripts/fetch_catalog.py --collections  # fall back to per-collection pull

No external deps (urllib only). Read-only HTTP GETs against the public store.
"""

import json
import re
import sys
import time
import sqlite3
import urllib.request
import urllib.error
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
DB_DIR = ROOT / "db"
DB     = DB_DIR / "catalog.db"
STORE  = "https://www.zelexdoll.com"
UA     = "Mozilla/5.0 (HowieZZ catalog reconciler; contact: local use)"

SERIES_COLLECTIONS = ["silicone", "k-series", "fusion", "sle-doll-3-0"]

USE_COLLECTIONS = "--collections" in sys.argv


# ── HTTP ──────────────────────────────────────────────────────────────────────

def get_json(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read().decode("utf-8", errors="replace")
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"  [warn] bad JSON from {url}: {e}")
                return None
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"  [warn] fetch {url} attempt {attempt+1}: {e}")
            time.sleep(1.5 * (attempt + 1))
    return None


def fetch_all_products():
    products = []
    if not USE_COLLECTIONS:
        page = 1
        while True:
            url = f"{STORE}/products.json?limit=250&page={page}"
            data = get_json(url)
            batch = (data or {}).get("products", []) if data else []
            if not batch:
                break
            products.extend(batch)
            print(f"  /products.json page {page}: {len(batch)} (total {len(products)})")
            page += 1
            if page > 50:
                break
        if products:
            return products
        print("  /products.json empty — falling back to per-collection pull")

    # Per-collection fallback
    seen = set()
    for handle in SERIES_COLLECTIONS:
        page = 1
        while True:
            url = f"{STORE}/collections/{handle}/products.json?limit=250&page={page}"
            data = get_json(url)
            batch = (data or {}).get("products", []) if data else []
            if not batch:
                break
            for p in batch:
                if p.get("id") not in seen:
                    seen.add(p.get("id"))
                    products.append(p)
            print(f"  /collections/{handle} page {page}: {len(batch)} (total {len(products)})")
            page += 1
            if page > 50:
                break
    return products


# ── Code extraction ───────────────────────────────────────────────────────────

HEAD_RE = re.compile(r'((?:GE|KE|ZFE|ZXE)\d+_\d+)')
FACE_RE = re.compile(r'\((GE\d+MJ)\)')
BODY_RE = re.compile(r'\+(Z[A-Z]*\d{3}[A-Z])')
BODY_IN_TITLE_RE = re.compile(r'\b(Z[A-Z]*\d{3}[A-Z])\b')


def decode_sku(sku, title):
    """Return (head, face, body, tone) from a variant sku, backstopped by title."""
    s = sku or ""
    t = title or ""
    head = (HEAD_RE.search(s) or HEAD_RE.search(t))
    face = (FACE_RE.search(s) or FACE_RE.search(t))
    body = BODY_RE.search(s) or BODY_IN_TITLE_RE.search(t)
    tone = None
    m = re.search(r'-(Fair|Tan|White|Wheat|Tanned)\b', s, re.I)
    if m:
        tone = m.group(1).capitalize()
    return (head.group(1) if head else None,
            face.group(1) if face else None,
            body.group(1) if body else None,
            tone)


def basename(src):
    """CDN src -> bare filename (drop query + path)."""
    return src.split("?")[0].rsplit("/", 1)[-1]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not DB.exists():
        print("catalog.db not found — run build_db.py first."); sys.exit(1)

    print("Fetching live catalog...")
    live = fetch_all_products()
    print(f"Live products: {len(live)}")
    if not live:
        print("No products fetched. Try: python scripts/fetch_catalog.py --collections")
        sys.exit(1)

    # Trim + index live products
    trimmed = []
    variants_flat = []
    img_index = {}          # live image basename -> set of live indices
    for i, p in enumerate(live):
        imgs = [basename(im.get("src", "")) for im in p.get("images", []) if im.get("src")]
        for b in imgs:
            img_index.setdefault(b, set()).add(i)
        vrows = []
        for v in p.get("variants", []):
            head, face, body, tone = decode_sku(v.get("sku"), p.get("title"))
            row = {
                "sku": v.get("sku"), "title": v.get("title"),
                "price": v.get("price"), "compare_at_price": v.get("compare_at_price"),
                "head": head, "face": face, "body": body, "tone": tone,
                "option1": v.get("option1"), "option2": v.get("option2"), "option3": v.get("option3"),
            }
            vrows.append(row)
            variants_flat.append({**row, "handle": p.get("handle"), "product_title": p.get("title")})
        trimmed.append({
            "id": p.get("id"), "handle": p.get("handle"), "title": p.get("title"),
            "vendor": p.get("vendor"), "tags": p.get("tags"),
            "options": [{"name": o.get("name"), "values": o.get("values")} for o in p.get("options", [])],
            "images": imgs, "variants": vrows,
        })

    (DB_DIR / "live_products.json").write_text(json.dumps(trimmed, indent=2, ensure_ascii=False), encoding="utf-8")
    (DB_DIR / "live_variants.json").write_text(json.dumps(variants_flat, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote live_products.json ({len(trimmed)}), live_variants.json ({len(variants_flat)})")

    # ── Match our products to live products by image-basename overlap ───────────
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    our = cur.execute("SELECT code, head_code, body_code FROM products").fetchall()
    our_imgs = {}
    for r in cur.execute("SELECT product_code, filename FROM product_assets WHERE media_type='image'"):
        our_imgs.setdefault(r["product_code"], set()).add(r["filename"])

    overrides = {}
    asset_gaps = {}
    matched = filled = 0

    for r in our:
        code = r["code"]
        my_imgs = our_imgs.get(code, set())

        # Vote for the live product sharing the most image filenames
        votes = {}
        for b in my_imgs:
            for idx in img_index.get(b, ()):
                votes[idx] = votes.get(idx, 0) + 1

        best_idx, best_n = None, 0
        if votes:
            best_idx, best_n = max(votes.items(), key=lambda kv: kv[1])

        def head_ok(idx):
            """Live product must carry our head code (guards coincidental image overlap)."""
            if not r["head_code"]:
                return True
            return any(v["head"] == r["head_code"] for v in trimmed[idx]["variants"])

        # Reject coincidental overlap (e.g. a defective-stock listing reusing stock images)
        if best_idx is not None and not head_ok(best_idx):
            best_idx, best_n = None, 0

        # Fallback / correction: search by head code, prefer a body that matches our folder
        if best_idx is None and r["head_code"]:
            cands = [i for i in range(len(trimmed))
                     if any(v["head"] == r["head_code"] for v in trimmed[i]["variants"])]
            if cands:
                if r["body_code"]:
                    pref = [i for i in cands
                            if any(v["body"] == r["body_code"] for v in trimmed[i]["variants"])]
                    cands = pref or cands
                best_idx = max(cands, key=lambda i: votes.get(i, 0))
                best_n = votes.get(best_idx, 0)

        if best_idx is None:
            continue
        matched += 1
        lp = trimmed[best_idx]

        # Resolve codes from the matched live product's first decodable variant
        head = face = body = None
        for v in lp["variants"]:
            head = head or v["head"]; face = face or v["face"]; body = body or v["body"]
        if not body:  # try title
            mb = BODY_IN_TITLE_RE.search(lp["title"] or "")
            body = mb.group(1) if mb else None

        ov = {
            "live_handle": lp["handle"], "live_title": lp["title"],
            "match_image_overlap": best_n,
            "head_code": head, "face_code": face, "body_code": body,
            "sku": lp["variants"][0]["sku"] if lp["variants"] else None,
            "price": lp["variants"][0]["price"] if lp["variants"] else None,
        }
        overrides[code] = ov
        if body and not r["body_code"]:
            filled += 1

        # Image diff: live images we don't have locally
        missing = sorted(set(lp["images"]) - my_imgs)
        if missing:
            asset_gaps[code] = missing

    (DB_DIR / "product_overrides.json").write_text(json.dumps(overrides, indent=2, ensure_ascii=False), encoding="utf-8")
    (DB_DIR / "asset_gaps.json").write_text(json.dumps(asset_gaps, indent=2, ensure_ascii=False), encoding="utf-8")
    conn.close()

    print()
    print(f"Matched {matched}/{len(our)} local products to live products")
    print(f"Body code backfilled for {filled} products that were missing it")
    print(f"Asset gaps recorded for {len(asset_gaps)} products "
          f"({sum(len(v) for v in asset_gaps.values())} live images we don't have)")
    print()
    print("Wrote: db/product_overrides.json, db/asset_gaps.json")
    print("Now run:  python scripts/build_db.py --reset   (applies overrides + variants)")


if __name__ == "__main__":
    main()
