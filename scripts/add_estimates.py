#!/usr/bin/env python3
"""Add ESTIMATED measurements for the 3 bodies with no published spec card.
Estimates are interpolated from comparable measured bodies + each body's build
descriptor, and flagged estimated:true so the UI can label them honestly.
Re-runnable (idempotent)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
MEAS = ROOT / "db" / "body_measurements.json"

# code -> estimated measurements (upper_bust, under_bust, waist, hip drive WHR/BWR)
EST = {
  # 161cm D-cup, Fusion "curvy" (Gwen) — between ZG162D and the fuller Fusion line
  "ZF161D": {"line":"Fusion","nominal_height":161,"cup":"D","upper_bust":85,"under_bust":67,
             "waist":62,"hip":94,"weight_kg":35,
             "estimated":True,"est_basis":"Interpolated from ZG162D / ZF168B (no published spec card)"},
  # 153cm B-cup, SLE 1.0/2.0 "skinny milf" — petite slim frame
  "ZX153B": {"line":"SLE 3.0","nominal_height":153,"cup":"B","upper_bust":75,"under_bust":64,
             "waist":53,"hip":79,"weight_kg":28,
             "estimated":True,"est_basis":"Interpolated from ZK168B (B-cup) scaled petite/slim (no published spec card)"},
  # 163cm E-cup, SLE 1.0 "tan skinny milf" — slim E-cup
  "ZX163E": {"line":"SLE 3.0","nominal_height":163,"cup":"E","upper_bust":85,"under_bust":66,
             "waist":58,"hip":92,"weight_kg":31,
             "estimated":True,"est_basis":"Interpolated from ZX172E / ZG175E (E-cup) slim build (no published spec card)"},
}

data = json.loads(MEAS.read_text(encoding="utf-8"))
bodies = data["bodies"]
for code, m in EST.items():
    # fill the remaining schema keys as null so the record is shape-complete
    full = {"spec_label": None, "neck": None, "shoulder_width": None, "arm_length": None,
            "hand_length": None, "leg_length": None, "foot_length": None, "thigh_circ": None,
            "calf_circ": None, "body_height": None, "head_body_height": m["nominal_height"]}
    full.update(m)
    bodies[code] = full
    whr = round(full["waist"]/full["hip"],3); bwr = round(full["upper_bust"]/full["waist"],3)
    print(f"  {code}: WHR {whr}  BWR {bwr}  (estimated)")

MEAS.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(EST)} estimated bodies into body_measurements.json")
