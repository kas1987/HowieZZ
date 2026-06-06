#!/usr/bin/env python3
"""
Body analysis + character profiles.

Computes the measurement signature (WHR, BWR, bust/waist/hip, drop) for every
body that has spec-card measurements, classifies each into one of the 7 Body
Families from the CEO brief, merges an optional curated persona overlay
(db/character_profiles.json), and writes:
    db/body_profiles.json     machine-readable analysis + profiles
    docs/character-profiles.md human-readable profiles, grouped by series
    table body_profiles        in catalog.db

Run after build_db.py. Reads measurements from db/body_measurements.json so it
works even if a body has no product images yet.

Usage: python scripts/build_profiles.py
"""
import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB   = ROOT / "db" / "catalog.db"
MEAS = ROOT / "db" / "body_measurements.json"
OVERLAY = ROOT / "db" / "character_profiles.json"
OUT_JSON = ROOT / "db" / "body_profiles.json"
OUT_MD   = ROOT / "docs" / "character-profiles.md"

SERIES_NAME = {"ZK": "K-Series", "ZG": "Inspiration", "ZGX": "Inspiration",
               "ZF": "Fusion", "ZX": "SLE"}

# 6 Body Families from the CEO brief — (WHR range, BWR range, meta)
# (The Athlete was retired 2026-06-05 — folded toward The Sculpt for a uniform 6-family set.)
FAMILIES = [
    ("The Classic",  (0.68, 0.72), (1.40, 1.50), "Timeless hourglass",      "+20%", "First-time premium buyer"),
    ("The Icon",     (0.60, 0.65), (1.50, 1.60), "Glamour model",           "+30%", "Photographer / curator"),
    ("The Muse",     (0.65, 0.70), (1.30, 1.40), "Tall, hip-dominant",      "+25%", "European aesthetic buyer"),
    ("The Siren",    (0.55, 0.60), (1.60, 1.75), "Bust-dominant fantasy",   "+35%", "Character / anime crossover"),
    ("The Empress",  (0.58, 0.64), (1.55, 1.65), "Maximum plush",           "+40%", "Body-positivity collector"),
    ("The Sculpt",   (0.65, 0.68), (1.45, 1.55), "Muscular definition",     "+30%", "Fitness realism seeker"),
]


def center(rng):
    return (rng[0] + rng[1]) / 2

def in_range(v, rng):
    return rng[0] <= v <= rng[1]

def classify(whr, bwr):
    """Return (family_name, confidence, meta). Exact-range match wins; else nearest center."""
    exact = [f for f in FAMILIES if in_range(whr, f[1]) and in_range(bwr, f[2])]
    if len(exact) == 1:
        return exact[0][0], "exact", exact[0]
    # Score by normalized distance to range centers (both axes)
    def dist(f):
        return abs(whr - center(f[1])) / 0.05 + abs(bwr - center(f[2])) / 0.10
    best = min(FAMILIES, key=dist)
    conf = "near" if (in_range(whr, best[1]) or in_range(bwr, best[2])) else "loose"
    if len(exact) > 1:
        # multiple ranges contain it — pick the closest, mark exact-tie
        best = min(exact, key=dist); conf = "exact-tie"
    return best[0], conf, best


def main():
    meas = json.loads(MEAS.read_text(encoding="utf-8"))["bodies"]
    overlay = {}
    if OVERLAY.exists():
        try:
            overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            print("  [warn] character_profiles.json unparseable; ignoring")

    profiles = []
    for code, m in meas.items():
        ub, lb = m.get("upper_bust"), m.get("under_bust")
        waist, hip = m.get("waist"), m.get("hip")
        if not (ub and waist and hip):
            continue
        whr = round(waist / hip, 3)
        bwr = round(ub / waist, 3)
        drop = round(ub - lb, 1) if (ub and lb) else None      # bust-underbust (cup volume proxy)
        fam, conf, fmeta = classify(whr, bwr)
        pre = "".join(c for c in code if c.isalpha())[:3]
        # normalize prefix to known (ZGX special-cased)
        line = "ZGX" if code.startswith("ZGX") else ("ZX" if code.startswith("ZX") else
               "ZK" if code.startswith("ZK") else "ZF" if code.startswith("ZF") else "ZG")
        ov = overlay.get(code, {})
        profiles.append({
            "body_code": code,
            "series": SERIES_NAME.get(line, line),
            "line": line,
            "height_cm": m.get("nominal_height"),
            "cup": m.get("cup"),
            "weight_kg": m.get("weight_kg"),
            "bust_cm": ub, "underbust_cm": lb, "waist_cm": waist, "hip_cm": hip,
            "bust_drop_cm": drop,
            "WHR": whr, "BWR": bwr,
            "family": fam, "family_confidence": conf,
            "estimated": bool(m.get("estimated")), "est_basis": m.get("est_basis"),
            "silhouette": fmeta[3], "premium": fmeta[4], "target_buyer": fmeta[5],
            # curated persona overlay (optional)
            "persona": ov.get("persona"),
            "energy": ov.get("energy"),
            "tagline": ov.get("tagline"),
            "positioning": ov.get("positioning"),
        })

    profiles.sort(key=lambda p: (p["series"], p["height_cm"] or 0, p["cup"] or ""))

    # Attach hero + gallery images from the products that use each body
    if DB.exists():
        conn0 = sqlite3.connect(DB); conn0.row_factory = sqlite3.Row
        for p in profiles:
            rows = conn0.execute(
                "SELECT pa.rel_path FROM product_assets pa JOIN products pr ON pr.code=pa.product_code "
                "WHERE pr.body_code=? AND pa.media_type='image' ORDER BY pr.image_count DESC, pa.sequence LIMIT 10",
                (p["body_code"],)).fetchall()
            imgs = ["assets/" + r["rel_path"] for r in rows]
            p["hero_image"] = imgs[0] if imgs else None
            p["gallery"] = imgs[:8]
            p["product_count"] = conn0.execute(
                "SELECT COUNT(*) FROM products WHERE body_code=?", (p["body_code"],)).fetchone()[0]
        conn0.close()

    OUT_JSON.write_text(json.dumps({"families": [
        {"name": f[0], "whr": f[1], "bwr": f[2], "silhouette": f[3], "premium": f[4], "target": f[5]}
        for f in FAMILIES], "profiles": profiles}, indent=2, ensure_ascii=False), encoding="utf-8")

    # ── DB table ────────────────────────────────────────────────────────────────
    if DB.exists():
        conn = sqlite3.connect(DB); cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS body_profiles")
        cur.execute("""CREATE TABLE body_profiles(
            body_code TEXT PRIMARY KEY, series TEXT, height_cm INTEGER, cup TEXT,
            weight_kg REAL, bust_cm REAL, waist_cm REAL, hip_cm REAL, bust_drop_cm REAL,
            whr REAL, bwr REAL, family TEXT, family_confidence TEXT,
            silhouette TEXT, premium TEXT, target_buyer TEXT,
            persona TEXT, energy TEXT, tagline TEXT)""")
        for p in profiles:
            cur.execute("""INSERT OR REPLACE INTO body_profiles VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["body_code"], p["series"], p["height_cm"], p["cup"], p["weight_kg"],
                 p["bust_cm"], p["waist_cm"], p["hip_cm"], p["bust_drop_cm"],
                 p["WHR"], p["BWR"], p["family"], p["family_confidence"],
                 p["silhouette"], p["premium"], p["target_buyer"],
                 p.get("persona"), p.get("energy"), p.get("tagline")))
        conn.commit(); conn.close()

    render_md(profiles)
    n_manifests = write_manifests(profiles)
    print(f"Profiles: {len(profiles)} bodies analyzed; {n_manifests} character manifests written")
    by_fam = {}
    for p in profiles:
        by_fam.setdefault(p["family"], []).append(p["body_code"])
    print("\nBody Family distribution:")
    for f in FAMILIES:
        members = by_fam.get(f[0], [])
        print(f"  {f[0]:<13} {len(members)}  {', '.join(members)}")
    print(f"\nWrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


SERIES_DIR = {"K-Series": "K-Series", "Inspiration": "I-Series",
              "Fusion": "Fusion-Series", "SLE": "SLE-Series"}

def write_manifests(profiles):
    """Emit one character manifest per body-type, matching the existing
    assets/K-Series/Characters/<Persona>/manifest.json convention. Each pulls a
    representative image library from the products that use that body."""
    if not DB.exists():
        return 0
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    written = 0
    for p in profiles:
        persona = p.get("persona") or p["family"].replace("The ", "")
        sdir = SERIES_DIR.get(p["series"])
        if not sdir:
            continue
        # Products built on this body, with their images
        prods = cur.execute(
            "SELECT code, folder_path FROM products WHERE body_code=? ORDER BY image_count DESC",
            (p["body_code"],)).fetchall()
        library, source_folders = [], []
        for pr in prods:
            source_folders.append(pr["folder_path"])
            imgs = cur.execute(
                "SELECT rel_path FROM product_assets WHERE product_code=? AND media_type='image' "
                "ORDER BY sequence LIMIT 6", (pr["code"],)).fetchall()
            library.extend("assets/" + r["rel_path"] for r in imgs)
        manifest = {
            "persona": persona,
            "series": p["series"],
            "body": p["body_code"],
            "family": p["family"],
            "silhouette": p["silhouette"],
            "signature": {
                "height_cm": p["height_cm"], "cup": p["cup"], "weight_kg": p["weight_kg"],
                "bust": p["bust_cm"], "waist": p["waist_cm"], "hip": p["hip_cm"],
                "WHR": p["WHR"], "BWR": p["BWR"], "bust_drop_cm": p["bust_drop_cm"],
            },
            "energy": p.get("energy"),
            "tagline": p.get("tagline"),
            "positioning": p.get("positioning"),
            "target_buyer": p["target_buyer"],
            "premium": p["premium"],
            "source_folders": source_folders,
            "product_count": len(prods),
            "library": library[:12],
        }
        safe = "".join(c if c.isalnum() or c in " -_" else "" for c in persona).strip().replace(" ", "_")
        out = ROOT / "assets" / sdir / "Characters" / safe / "manifest.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        written += 1
    conn.close()
    return written


def render_md(profiles):
    lines = ["# ZELEX Character Profiles — by Series & Body Type",
             "",
             "*Generated by `scripts/build_profiles.py`. Each body is analyzed on its spec-card",
             "measurements and mapped to one of the 7 Body Families from the CEO brief.*",
             "",
             "**Metrics:** WHR = waist÷hip (lower = more hourglass). BWR = bust÷waist (higher = more bust-forward).",
             "Bust drop = upper−under bust (cup volume proxy).",
             ""]
    by_series = {}
    for p in profiles:
        by_series.setdefault(p["series"], []).append(p)
    for series in ["K-Series", "Inspiration", "Fusion", "SLE"]:
        rows = by_series.get(series, [])
        if not rows:
            continue
        lines.append(f"\n## {series}\n")
        lines.append("| Body | H/cup | Wt | Bust·Waist·Hip | WHR | BWR | Body Family | Silhouette |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for p in rows:
            sig = f"{p['bust_cm']}·{p['waist_cm']}·{p['hip_cm']}"
            fam = p["family"] + ("" if p["family_confidence"].startswith("exact") else " *(near)*")
            lines.append(f"| **{p['body_code']}** | {p['height_cm']}cm {p['cup']} | "
                         f"{p['weight_kg']}kg | {sig} | {p['WHR']} | {p['BWR']} | {fam} | {p['silhouette']} |")
        # profile cards
        for p in rows:
            lines.append(f"\n### {p['body_code']} — {p.get('persona') or p['family']}")
            if p.get("tagline"):
                lines.append(f"*{p['tagline']}*\n")
            lines.append(f"- **Body Family:** {p['family']} ({p['silhouette']}) · premium {p['premium']}")
            lines.append(f"- **Signature:** {p['height_cm']}cm, {p['cup']}-cup, {p['weight_kg']}kg · "
                         f"bust {p['bust_cm']} / waist {p['waist_cm']} / hip {p['hip_cm']} · "
                         f"WHR {p['WHR']}, BWR {p['BWR']}, drop {p['bust_drop_cm']}cm")
            lines.append(f"- **Target buyer:** {p['target_buyer']}")
            if p.get("energy"):
                lines.append(f"- **Energy:** {p['energy']}")
            if p.get("positioning"):
                lines.append(f"- **Positioning:** {p['positioning']}")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
