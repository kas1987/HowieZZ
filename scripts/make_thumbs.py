#!/usr/bin/env python3
"""
Generate web-friendly thumbnails for every image referenced by the profiles and
characters. Full-res product JPEGs are 2-3 MB each; loading many at once stalls
the browser. Thumbs are ~520px-wide JPEGs under assets/thumbs/, mirroring the
source path. Writes thumb-path fields back into the JSON so the front-end can
use them. Re-run after build_profiles.py / build_characters.py.

Usage: python scripts/make_thumbs.py
"""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BODY_PROFILES = ROOT / "db" / "body_profiles.json"
CHARACTERS    = ROOT / "db" / "characters.json"
THUMB_DIR = ROOT / "assets" / "thumbs"
WIDTH = 520

def thumb_rel(rel):
    p = Path(rel)
    sub = Path(*p.parts[1:]) if p.parts and p.parts[0] == "assets" else p
    return "assets/thumbs/" + str(sub).replace("\\", "/")

def make(rel, cache):
    if rel in cache:
        return cache[rel]
    src = ROOT / rel
    if not src.exists():
        cache[rel] = rel; return rel
    out_rel = thumb_rel(rel)
    dst = ROOT / out_rel
    if dst.exists():
        cache[rel] = out_rel; return out_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(src) as im:
            im = im.convert("RGB")
            w, h = im.size
            if w > WIDTH:
                im = im.resize((WIDTH, int(h * WIDTH / w)), Image.LANCZOS)
            im.save(dst, "JPEG", quality=82, optimize=True)
        cache[rel] = out_rel; return out_rel
    except Exception as e:
        print(f"  [warn] {rel}: {e}")
        cache[rel] = rel; return rel

def main():
    cache = {}
    made_before = len(cache)

    # body_profiles.json
    if BODY_PROFILES.exists():
        data = json.loads(BODY_PROFILES.read_text(encoding="utf-8"))
        for p in data.get("profiles", []):
            if p.get("hero_image"):
                p["hero_thumb"] = make(p["hero_image"], cache)
            p["gallery_thumbs"] = [make(g, cache) for g in p.get("gallery", [])]
        BODY_PROFILES.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    # characters.json
    if CHARACTERS.exists():
        data = json.loads(CHARACTERS.read_text(encoding="utf-8"))
        for c in data.get("characters", []):
            ps = c.get("photoshoot") or {}
            if ps.get("hero"):
                ps["hero_thumb"] = make(ps["hero"], cache)
            if ps.get("gallery"):
                ps["gallery_thumbs"] = [make(g, cache) for g in ps["gallery"]]
            c["photoshoot"] = ps
        CHARACTERS.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    made = sum(1 for v in cache.values() if v.startswith("assets/thumbs/"))
    print(f"Thumbnails ready: {made} unique images thumbnailed. JSON updated with thumb paths.")

if __name__ == "__main__":
    main()
