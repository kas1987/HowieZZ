#!/usr/bin/env python3
"""
Build a clean, self-contained ZELEX Atlas site package for Howie.

Includes: the 9 site pages + kit + the full-res photoshoot images the site actually
references + all thumbnails + the data JSON the site reads + the run guide + the
executive/leadership brief docs.  EXCLUDES raw source (Per Drive, Heads, Options,
scrape, Shopify theme, old zips).
"""
import json, shutil, os
from pathlib import Path

ROOT  = Path(__file__).resolve().parent.parent
STAGE = ROOT.parent / "_ZELEX-Atlas-dist" / "ZELEX-Character-Atlas"
ZIPBASE = ROOT.parent / "_ZELEX-Atlas-dist" / "ZELEX-Character-Atlas-2026-06-05"

# clean stage
if STAGE.exists(): shutil.rmtree(STAGE)
STAGE.mkdir(parents=True)

def copy(rel, dest_rel=None):
    src = ROOT / rel
    dst = STAGE / (dest_rel or rel)
    if not src.exists():
        print("  ! missing, skipped:", rel); return 0
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir(): shutil.copytree(src, dst, dirs_exist_ok=True)
    else: shutil.copy2(src, dst)
    return 1

# ---- 1. site pages ----
PAGES = ["index.html","browse.html","series.html","body.html","character.html",
         "family.html","quiz.html","craft.html","contact.html",
         "index-gallery-original.html","serve.py","SITE-GUIDE.md","README.md"]
for p in PAGES: copy(p)

# ---- 2. shared kit ----
for k in ["assets/site.css","assets/site.js"]: copy(k)

# ---- 3. data the site reads (+ stories source for reference) ----
for d in ["db/characters.json","db/body_types.json","db/body_profiles.json",
          "db/character_stories.json"]:
    copy(d)

# ---- 4. all thumbnails (small, guarantees grids never miss) ----
copy("assets/thumbs")

# ---- 5. referenced full-res photoshoot images ----
chars = json.loads((ROOT/"db"/"characters.json").read_text(encoding="utf-8"))["characters"]
full = set()
for c in chars:
    p = c.get("photoshoot") or {}
    v = p.get("hero");      full.add(v) if v else None
    for x in (p.get("gallery") or []): full.add(x)
n_img = 0
for rel in sorted(x for x in full if x):
    n_img += copy(rel)

# ---- 6. brief / leadership docs ----
BRIEFS = ["ZELEX-CEO-Executive-Brief.md","ZELEX-CEO-Executive-Brief-v2.md",
          "ZELEX-CEO-Executive-Brief-v2-light.pdf","ZELEX-Board-1Page-Summary-v2.md",
          "ZELEX-Leadership-Package-v2.html"]
for b in BRIEFS: copy(b, f"briefs/{Path(b).name}")
# reference/build docs
copy("docs", "docs")

# ---- summary ----
def dirsize(p):
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
total = dirsize(STAGE)
print(f"\nStaged {n_img} full-res images.")
print(f"Package staged at: {STAGE}")
print(f"Staged size: {total/1024/1024:.1f} MB")

# ---- zip ----
print("Zipping (this can take a moment)...")
shutil.make_archive(str(ZIPBASE), "zip", root_dir=STAGE.parent, base_dir=STAGE.name)
zp = Path(str(ZIPBASE)+".zip")
print(f"ZIP: {zp}")
print(f"ZIP size: {zp.stat().st_size/1024/1024:.1f} MB")
