#!/usr/bin/env python3
"""
Build the machine-readable Six-Family taxonomy (db/family_taxonomy.json) from
the body classification in db/body_profiles.json (produced by build_profiles.py).

This is the data contract behind PDR-009 — consumed by the UI (quiz scoring,
compare tool, character/family pages) and by scripts. Companion docs:
  docs/body-family-method.md         (classification methodology)
  docs/body-family-copy-guide.md     (voice & messaging)
  docs/body-family-product-matrix.md (body-code -> family table)
  docs/PDR-009-six-family-product-taxonomy.md (implementation handoff)

Run after build_profiles.py.
Usage: python scripts/build_taxonomy.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "db" / "body_profiles.json"
OUT = ROOT / "db" / "family_taxonomy.json"

CONFIDENCE = {
    "exact": "Exactly one family contains both WHR and BWR within its ranges.",
    "exact-tie": "More than one family's ranges contain the body; the nearest range-center wins.",
    "near": "No family contains both axes; the nearest-center family is chosen and it contains at least one axis in range.",
    "loose": "No family contains both axes and the nearest-center family contains neither axis in range.",
}


def main():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    members = {f["name"]: [] for f in d["families"]}
    bodies = []
    for p in d["profiles"]:
        if p.get("WHR") is None:
            continue
        bodies.append({
            "body_code": p["body_code"],
            "series": p["series"],
            "height_cm": p.get("height_cm"),
            "cup": p.get("cup"),
            "WHR": p["WHR"],
            "BWR": p["BWR"],
            "bust_drop_cm": p.get("bust_drop_cm"),
            "family": p["family"],
            "confidence": p["family_confidence"],
            "estimated": bool(p.get("estimated")),
        })
        members.setdefault(p["family"], []).append(p["body_code"])
    bodies.sort(key=lambda b: (b["family"], b["series"], b["height_cm"] or 0))

    families = []
    for f in d["families"]:
        mem = sorted(members.get(f["name"], []))
        families.append({
            "name": f["name"],
            "slug": f["name"].replace("The ", "").lower(),
            "whr_range": f["whr"],
            "bwr_range": f["bwr"],
            "silhouette": f["silhouette"],
            "premium": f["premium"],
            "target_buyer": f["target"],
            "status": "active" if mem else "in_development",
            "member_count": len(mem),
            "members": mem,
        })

    doc = {
        "version": "1.0.0",
        "generated_from": "db/body_profiles.json (scripts/build_profiles.py)",
        "metric_definitions": {
            "WHR": "waist / hip — lower is more hourglass",
            "BWR": "bust / waist — higher is more bust-forward",
            "bust_drop_cm": "upper-bust minus under-bust (cup-volume proxy)",
        },
        "confidence_labels": CONFIDENCE,
        "families": families,
        "bodies": bodies,
    }
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    active = [(f["name"], f["member_count"]) for f in families if f["status"] == "active"]
    dev = [f["name"] for f in families if f["status"] == "in_development"]
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(bodies)} bodies, "
          f"{len(families)} families (active: {active}; in-development: {dev})")


if __name__ == "__main__":
    main()
