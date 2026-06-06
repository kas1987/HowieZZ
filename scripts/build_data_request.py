#!/usr/bin/env python3
"""
Generate the manufacturer data-request templates — the two data points the
configurator needs to graduate from ESTIMATE/PROPOSED to authoritative
(PDR-011 §8-9):

  1. neck_joint_mm per body   -> replaces the circumference-derived neck_class
  2. face_features per head   -> makes the Face & Finish axes head-aware

Emits ready-to-send CSVs (one row per real body / head, pre-filled with what we
already know, blank columns for what we're asking the factory to supply) plus a
cover README. Re-runnable so the templates never drift from db/.

Sources: db/neck_compatibility.json, db/heads.json
Usage: python scripts/build_data_request.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
OUT = ROOT / "docs" / "data-requests"


def load(name):
    return json.loads((DB / name).read_text(encoding="utf-8"))


def write_csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def neck_rows(neck):
    rows = []
    for code, b in sorted(neck["bodies"].items()):
        rows.append([
            code, b.get("line") or "", b.get("neck_circ_cm") if b.get("neck_circ_cm") is not None else "",
            b.get("neck_class") or "",
            "",  # neck_joint_diameter_mm  (FILL)
            "",  # neck_joint_type         (FILL: screw / bayonet / magnet / peg)
            "",  # interchange_group       (FILL: factory's own connector group id, if any)
            "",  # notes
        ])
    return rows


def head_rows(heads):
    rows = []
    # priority 1 = has cast characters (the heads buyers actually see) so the
    # factory can fill the ones that matter first.
    def prio(h):
        return (0 if h.get("characters") else 1, 0 if h.get("representative_image") else 1, h["head_code"])
    for h in sorted(heads.values(), key=prio):
        rows.append([
            h["head_code"], h.get("line") or "", h.get("neck_class") or "",
            "Y" if "Movable Jaw" in h.get("face_variants", []) else "N",
            1 if h.get("characters") else 2,   # priority
            "",  # default_eye_color   (FILL: Brown/Hazel/Blue/Green/Grey/...)
            "",  # eye_swappable        (FILL: Y/N)
            "",  # default_makeup       (FILL: Natural/Glam/...)
            "",  # eyebrows             (FILL: Painted/Implanted)
            "",  # default_wig_color    (FILL: Black/Brunette/Blonde/Red/...)
            "",  # wig_removable        (FILL: Y/N)
            "",  # freckles_available   (FILL: Y/N)
            "",  # notes
        ])
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    neck = load("neck_compatibility.json")
    heads = load("heads.json")["heads"]

    neck_header = [
        "body_code", "line", "neck_circ_cm (known)", "neck_class (current estimate)",
        "neck_joint_diameter_mm  <-- FILL",
        "neck_joint_type  <-- FILL (screw/bayonet/magnet/peg)",
        "interchange_group  <-- FILL (factory connector group, optional)",
        "notes",
    ]
    head_header = [
        "head_code", "line", "neck_class", "movable_jaw (known)", "priority (1=has cast)",
        "default_eye_color  <-- FILL",
        "eye_swappable  <-- FILL (Y/N)",
        "default_makeup  <-- FILL",
        "eyebrows  <-- FILL (Painted/Implanted)",
        "default_wig_color  <-- FILL",
        "wig_removable  <-- FILL (Y/N)",
        "freckles_available  <-- FILL (Y/N)",
        "notes",
    ]

    nrows = neck_rows(neck)
    hrows = head_rows(heads)
    write_csv(OUT / "neck-joint-request.csv", neck_header, nrows)
    write_csv(OUT / "head-features-request.csv", head_header, hrows)

    readme = f"""# ZELEX — Manufacturer Data Request

Two data points let the configurator (PDR-011) stop estimating and start using
real specs. Please fill the `<-- FILL` columns in the two CSVs in this folder and
return them. Pre-filled columns are what we already have — for context, do not
change them.

## 1. Neck joint spec — `neck-joint-request.csv` ({len(nrows)} bodies)

**Why:** heads are interchangeable when their neck CONNECTOR matches. We currently
estimate this from neck *circumference* (a soft-tissue proxy). The real connector
spec makes it exact.

| Column | What we need |
|---|---|
| `neck_joint_diameter_mm` | Diameter (mm) of the head-mount connector at the neck. |
| `neck_joint_type` | Connector mechanism: screw / bayonet / magnet / peg / other. |
| `interchange_group` | If the factory already groups connectors (e.g. "A"/"B"), the group id for this body. Optional. |

Two bodies with the same diameter + type are physically interchangeable,
regardless of product line.

## 2. Per-head face features — `head-features-request.csv` ({len(hrows)} heads)

**Why:** the configurator's *Face & Finish* options (eye colour, makeup, eyebrows,
wig, freckles) are currently GLOBAL proposals — we have no per-head defaults or
availability. Fill these to make each head show its true shipped finish and which
options it actually supports. Rows are sorted by **priority** (1 = heads with a
named character, i.e. the ones buyers see most) — fill those first if time is short.

| Column | What we need |
|---|---|
| `default_eye_color` | Eye colour the head ships with. |
| `eye_swappable` | Can the acrylic eyes be changed? Y/N. |
| `default_makeup` | Factory makeup style (Natural / Glam / …). |
| `eyebrows` | Painted or implanted brow hair. |
| `default_wig_color` | Wig colour shipped. |
| `wig_removable` | Removable wig? Y/N. |
| `freckles_available` | Optional painted freckles offered? Y/N. |

## Returning the data

Return the filled CSVs as-is. We load `neck_joint_mm` into
`db/neck_compatibility.json` (per body) and the face fields into the
`face_features` slot in `db/heads.json` (per head) — no schema changes needed; the
configurator picks them up automatically.

> Regenerate these templates after any catalog change:
> `python scripts/build_data_request.py`
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    print(f"Wrote templates to {OUT.relative_to(ROOT)}/")
    print(f"  neck-joint-request.csv     {len(nrows)} bodies")
    print(f"  head-features-request.csv  {len(hrows)} heads "
          f"({sum(1 for r in hrows if r[4]==1)} priority-1 with cast)")
    print(f"  README.md")


if __name__ == "__main__":
    main()
