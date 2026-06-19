"""Unit tests for scripts/build_profiles.py — classification + full main()."""
import json

import build_profiles


# ── Pure helpers ────────────────────────────────────────────────────────────

def test_center():
    assert build_profiles.center((0.68, 0.72)) == 0.70


def test_in_range():
    assert build_profiles.in_range(0.70, (0.68, 0.72)) is True
    assert build_profiles.in_range(0.80, (0.68, 0.72)) is False
    assert build_profiles.in_range(0.68, (0.68, 0.72)) is True  # inclusive


def test_classify_exact_single():
    fam, conf, _ = build_profiles.classify(0.70, 1.45)
    assert fam == "The Classic"
    assert conf == "exact"


def test_classify_exact_tie():
    # 0.68 / 1.475 falls inside both The Classic and The Sculpt ranges.
    fam, conf, _ = build_profiles.classify(0.68, 1.475)
    assert conf == "exact-tie"
    assert fam in {"The Classic", "The Sculpt"}


def test_classify_loose():
    # Far outside every family range on both axes.
    fam, conf, _ = build_profiles.classify(0.95, 2.2)
    assert conf == "loose"
    assert fam in {f[0] for f in build_profiles.FAMILIES}


def test_classify_near():
    # WHR inside at least one family range, BWR well outside all -> "near".
    fam, conf, _ = build_profiles.classify(0.70, 1.0)
    assert conf in {"near", "loose"}


# ── Full main() integration (DB present) ────────────────────────────────────

def test_main_writes_profiles_json(built_profiles):
    ws = built_profiles
    assert ws["body_profiles"].exists()
    data = json.loads(ws["body_profiles"].read_text(encoding="utf-8"))
    assert "families" in data and "profiles" in data

    by_code = {p["body_code"]: p for p in data["profiles"]}
    assert {"ZG170D", "ZK168B"} <= set(by_code)

    zg = by_code["ZG170D"]
    # WHR = waist/hip = 58/89; BWR = upper_bust/waist = 84/58.
    assert zg["WHR"] == round(58 / 89, 3)
    assert zg["BWR"] == round(84 / 58, 3)
    assert zg["family"] in {f[0] for f in build_profiles.FAMILIES}
    # Hero image is pulled from the product built on this body.
    assert zg["hero_image"] and zg["hero_image"].startswith("assets/")
    assert zg["product_count"] >= 1


def test_main_writes_markdown(built_profiles):
    md = built_profiles["profiles_md"].read_text(encoding="utf-8")
    assert "ZELEX Character Profiles" in md
    assert "ZG170D" in md


def test_main_writes_db_table(built_profiles):
    import sqlite3
    conn = sqlite3.connect(built_profiles["db_path"])
    n = conn.execute("SELECT COUNT(*) FROM body_profiles").fetchone()[0]
    conn.close()
    assert n == 2


def test_main_writes_character_manifests(built_profiles):
    manifests = list((built_profiles["assets"]).glob("*/Characters/*/manifest.json"))
    assert manifests, "expected at least one character manifest written"
    payload = json.loads(manifests[0].read_text(encoding="utf-8"))
    assert "body" in payload and "signature" in payload
