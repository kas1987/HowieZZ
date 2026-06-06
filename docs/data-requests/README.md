# ZELEX — Manufacturer Data Request

Two data points let the configurator (PDR-011) stop estimating and start using
real specs. Please fill the `<-- FILL` columns in the two CSVs in this folder and
return them. Pre-filled columns are what we already have — for context, do not
change them.

## 1. Neck joint spec — `neck-joint-request.csv` (21 bodies)

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

## 2. Per-head face features — `head-features-request.csv` (189 heads)

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
