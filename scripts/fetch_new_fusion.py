#!/usr/bin/env python3
"""Download the 2 genuinely-new Fusion products into convention-named folders.
The other 3 live Fusion products are content we already hold under +-style names."""
import json, urllib.request, urllib.error, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CDN = "https://cdn.shopify.com/s/files/1/0661/6059/1091/files/"
UA = "Mozilla/5.0 (HowieZZ asset fetch; local use)"

# handle -> folder name (using our +-convention so parse_fusion_folder reads it)
NEW = {
    "gwen-movable-jaws-version-zf161d-5ft3-d-cup-realistic-fair-curvy-sex-doll-zfe01_1-fusion-series": "ZFE01_1+ZF161D",
    "baifern-movable-jaws-version-zf168b-5ft6-b-cup-realistic-fair-curvy-sex-doll-zfe05_1-fusion-series": "ZFE05_1+ZF168B",
}

live = json.load(open(ROOT / "db" / "live_products.json", encoding="utf-8"))
by_handle = {p["handle"]: p for p in live}

def get(url, dest):
    for a in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if len(data) < 1024:
                raise IOError("too small")
            dest.write_bytes(data); return True
        except (urllib.error.URLError, urllib.error.HTTPError, IOError, TimeoutError):
            time.sleep(1.0 * (a + 1))
    return False

total_ok = total_fail = 0
for handle, folder in NEW.items():
    p = by_handle.get(handle)
    if not p:
        print(f"[miss] {handle} not in live dump"); continue
    dest_dir = ASSETS / "Fusion-Series" / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for b in p["images"]:
        if not b.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        dest = dest_dir / b
        if dest.exists():
            continue
        if get(CDN + b, dest): ok += 1
        else: fail += 1
    print(f"{folder}: {ok} ok, {fail} failed ({len(p['images'])} listed)")
    total_ok += ok; total_fail += fail

print(f"\nTotal: {total_ok} downloaded, {total_fail} failed")
