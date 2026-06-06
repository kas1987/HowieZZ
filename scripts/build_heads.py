#!/usr/bin/env python3
"""
Build the machine-readable head catalog (db/heads.json) by reverse-engineering
the 177 head sculpts that are otherwise scattered across the product feed,
live variants, character casts, and movable-jaw overrides.

This is the head-side companion to db/body_measurements.json: where bodies are
measured architectures, heads are sculpts with a series, a movable-jaw
availability, the skin tones they ship in, the bodies they pair with, the
characters cast on them, and a representative image. It is the data foundation
the configurator's head gallery picker reads (PDR-011).

Sources:
  db/catalog.json          products: head_code, face_code, body_code, series_id,
                           cover_image, image_count, price-less product rows
  db/live_variants.json    head + body + tone + price (the priced SKUs)
  db/product_overrides.json movable-jaw face_codes keyed by head
  db/characters.json       which named characters are cast on each head (+ thumbs)

Run after build_characters.py / make_thumbs.py (so hero_thumb paths exist).
Usage: python scripts/build_heads.py
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
OUT = DB / "heads.json"

# catalog series_id -> the line name used by the configurator schema
SERIES_LINE = {"Fusion": "Fusion", "I": "I-Series", "K": "K-Series", "SLE": "SLE 3.0"}
# fallback: head-code prefix -> line, for heads with no/ambiguous product series_id
PREFIX_LINE = {"ZXE": "SLE 3.0", "GE": "I-Series", "ZFE": "Fusion", "KE": "K-Series"}

# --- neck-connector classes (the basis for interchangeable heads) ----------------
# Heads attach at the neck. Marketing line is NOT the constraint; the neck
# circumference is. db/body_measurements.json shows two clusters: K-Series ~27cm
# (narrow) vs Fusion/I-Series/SLE ~31-33cm (standard). Heads sharing a class are
# physically swappable across lines even though the catalog only sells line-matched
# pairs. Threshold is an ESTIMATE from the spec cards — confirm against the physical
# neck joint before treating a cross-line swap as guaranteed-fit.
NECK_SLIM_MAX = 29.0  # cm; below this = the narrow (K-Series) connector


def neck_class(neck_cm):
    if neck_cm is None:
        return None
    return "slim" if neck_cm < NECK_SLIM_MAX else "standard"


# line -> default neck class, used when a head has no measured paired body
LINE_NECK_CLASS = {"K-Series": "slim", "I-Series": "standard", "Fusion": "standard", "SLE 3.0": "standard"}


def load(name):
    return json.loads((DB / name).read_text(encoding="utf-8"))


def line_for(head_code, series_ids):
    """Prefer the product's own series; fall back to the head-code prefix."""
    if series_ids:
        # most common series_id wins (a head can appear in one series' folders)
        sid = max(series_ids, key=lambda s: series_ids[s])
        if sid in SERIES_LINE:
            return SERIES_LINE[sid]
    m = re.match(r"^[A-Z]+", head_code or "")
    return PREFIX_LINE.get(m.group(0) if m else "", None)


def main():
    catalog = load("catalog.json")
    variants = load("live_variants.json")
    overrides = load("product_overrides.json")
    characters = load("characters.json").get("characters", [])
    bodies_meas = load("body_measurements.json").get("bodies", {})

    heads = defaultdict(lambda: {
        "series_ids": defaultdict(int),
        "bodies": set(),
        "tones": set(),
        "mj_face_codes": set(),
        "images": [],          # ordered candidate images (first = representative)
        "characters": [],
        "product_count": 0,
        "prices": [],
    })

    # --- products: the structural backbone (head <-> body pairings + imagery) ---
    for p in catalog.get("products", []):
        hc = p.get("head_code")
        if not hc:
            continue
        h = heads[hc]
        h["product_count"] += 1
        if p.get("series_id"):
            h["series_ids"][p["series_id"]] += 1
        if p.get("body_code"):
            h["bodies"].add(p["body_code"])
        if p.get("face_code") and "MJ" in p["face_code"]:
            h["mj_face_codes"].add(p["face_code"])
        cov = p.get("cover_image")
        if cov:
            # cover_image is repo-relative under assets/; the front-end serves from there
            h["images"].append("assets/" + cov if not cov.startswith("assets/") else cov)

    # --- movable-jaw overrides: authoritative MJ availability per head ---
    for o in overrides.values():
        hc, fc = o.get("head_code"), o.get("face_code")
        if hc and fc and "MJ" in fc:
            heads[hc]["mj_face_codes"].add(fc)
            if o.get("body_code"):
                heads[hc]["bodies"].add(o["body_code"])

    # --- live variants: priced SKUs -> tones + price range ---
    for v in variants:
        hc = v.get("head")
        if not hc:
            continue
        h = heads[hc]
        if v.get("tone"):
            h["tones"].add(v["tone"])
        if v.get("body"):
            h["bodies"].add(v["body"])
        try:
            if v.get("price"):
                h["prices"].append(float(v["price"]))
        except (TypeError, ValueError):
            pass

    # --- characters: named cast on each head + a real thumbnail to lead with ---
    for c in characters:
        hc = (c.get("face") or {}).get("head_code")
        if not hc:
            continue
        h = heads[hc]
        if c.get("status") == "live":
            h["characters"].append(c["character_id"])
            ps = c.get("photoshoot") or {}
            thumb = ps.get("hero_thumb") or ps.get("hero")
            if thumb:
                h["images"].insert(0, thumb)  # a cast hero_thumb leads the cover jpg
        tone = (c.get("face") or {}).get("skin_tone")
        if tone:
            h["tones"].add(tone)

    # --- finalize ---
    out_heads = {}
    for hc in sorted(heads):
        h = heads[hc]
        line = line_for(hc, h["series_ids"])
        face_variants = ["Standard"] + (["Movable Jaw"] if h["mj_face_codes"] else [])
        prices = sorted(h["prices"])
        # neck-connector class: from the measured necks of paired bodies, else line default
        necks = sorted(bodies_meas[bc]["neck"] for bc in h["bodies"]
                       if bodies_meas.get(bc) and bodies_meas[bc].get("neck") is not None)
        neck_cm = necks[len(necks) // 2] if necks else None  # median
        nclass = neck_class(neck_cm) or LINE_NECK_CLASS.get(line)
        # de-dup images, keep order
        seen, images = set(), []
        for img in h["images"]:
            if img not in seen:
                seen.add(img)
                images.append(img)
        out_heads[hc] = {
            "head_code": hc,
            "line": line,
            "neck_class": nclass,
            "neck_cm": neck_cm,
            "face_variants": face_variants,
            "mj_face_codes": sorted(h["mj_face_codes"]),
            "skin_tones": sorted(h["tones"]),
            "bodies": sorted(h["bodies"]),
            "characters": h["characters"],
            "product_count": h["product_count"],
            "representative_image": images[0] if images else None,
            "price_range": [prices[0], prices[-1]] if prices else None,
        }

    payload = {
        "version": "1.0.0",
        "_comment": (
            "Head catalog reverse-engineered from products + variants + characters + "
            "movable-jaw overrides (scripts/build_heads.py). One record per head sculpt: "
            "line, movable-jaw availability, skin tones, paired bodies, cast characters, "
            "a representative image, and price range. Feeds the configurator head gallery "
            "(PDR-011). Regenerate after build_characters.py / make_thumbs.py."
        ),
        "generated_from": [
            "db/catalog.json", "db/live_variants.json",
            "db/product_overrides.json", "db/characters.json",
        ],
        "series_line_map": SERIES_LINE,
        "neck_classes": {
            "_basis": "Neck-connector class is the interchangeability constraint, not the marketing line. "
                      f"Threshold: neck circumference < {NECK_SLIM_MAX}cm = 'slim', else 'standard'. "
                      "ESTIMATED from spec-card neck measurements — confirm against the physical neck joint.",
            "slim": "Narrow connector — K-Series (~27cm).",
            "standard": "Standard connector — Fusion / I-Series / SLE 3.0 (~31-33cm). Heads here are mutually swappable.",
        },
        "count": len(out_heads),
        "heads": out_heads,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # console summary
    by_line = defaultdict(int)
    mj = 0
    for h in out_heads.values():
        by_line[h["line"]] += 1
        if "Movable Jaw" in h["face_variants"]:
            mj += 1
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(out_heads)} heads")
    for ln, n in sorted(by_line.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        print(f"  {str(ln):10} {n}")
    print(f"  movable-jaw capable: {mj}")
    no_img = sum(1 for h in out_heads.values() if not h["representative_image"])
    print(f"  without a representative image: {no_img}")


if __name__ == "__main__":
    main()
