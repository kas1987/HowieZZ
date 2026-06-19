"""Unit tests for scripts/build_characters.py — helpers + full main()."""
import json

import build_characters


# ── Pure helpers ────────────────────────────────────────────────────────────

def test_is_torso_known_code():
    assert build_characters.is_torso("ZX84J", 168) is True


def test_is_torso_short_stature():
    assert build_characters.is_torso("ZG140A", 140) is True


def test_is_torso_standing_body():
    assert build_characters.is_torso("ZG170D", 170) is False
    assert build_characters.is_torso("ZG170D", None) is False


def test_is_factory_by_path():
    assert build_characters.is_factory("x-101.jpg", "assets/Heads/Hard/x-101.jpg") is True
    assert build_characters.is_factory("x-101.jpg", "assets/I-Series/specs/x-101.jpg") is True


def test_is_factory_no_photo_index():
    # No -NNN index => not a photoshoot frame => factory.
    assert build_characters.is_factory("cover.jpg", "assets/I-Series/Foo/cover.jpg") is True


def test_is_factory_real_photoshoot_frame():
    assert build_characters.is_factory("GE149-101.jpg", "assets/I-Series/Foo/GE149-101.jpg") is False


def test_tagline_known_family():
    assert build_characters.tagline("The Classic", "D", 170, 1) == "Timeless lines, nothing to prove."
    # slot wraps around the 4-entry pool.
    assert build_characters.tagline("The Classic", "D", 170, 5) == build_characters.tagline("The Classic", "D", 170, 1)


def test_tagline_formats_height_and_cup():
    assert build_characters.tagline("The Muse", "E", 175, 1) == "175cm of quiet confidence."
    assert build_characters.tagline("The Siren", "G", 160, 2) == "G-cup, and unapologetic."


def test_tagline_unknown_family_uses_default():
    assert build_characters.tagline(None, "D", 165, 1) == "165cm, one of a kind."


def test_load_json_missing(tmp_path):
    assert build_characters.load_json(tmp_path / "absent.json", {"x": 1}) == {"x": 1}


def test_load_json_bad(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{nope", encoding="utf-8")
    assert build_characters.load_json(bad, []) == []


# ── Full main() integration ─────────────────────────────────────────────────

def test_main_builds_characters(built_profiles, monkeypatch):
    ws = built_profiles
    out_chars = ws["db_dir"] / "characters.json"
    out_bodies = ws["db_dir"] / "body_types.json"

    monkeypatch.setattr(build_characters, "DB", ws["db_path"])
    monkeypatch.setattr(build_characters, "BODY_PROFILES", ws["body_profiles"])
    monkeypatch.setattr(build_characters, "LEAD_PERSONAS", ws["db_dir"] / "_no_leads.json")
    monkeypatch.setattr(build_characters, "OVERLAY", ws["db_dir"] / "_no_overlay.json")
    monkeypatch.setattr(build_characters, "STORIES", ws["db_dir"] / "_no_stories.json")
    monkeypatch.setattr(build_characters, "OUT_CHARS", out_chars)
    monkeypatch.setattr(build_characters, "OUT_BODIES", out_bodies)
    build_characters.main()

    chars = json.loads(out_chars.read_text(encoding="utf-8"))["characters"]
    bodies = json.loads(out_bodies.read_text(encoding="utf-8"))["body_types"]

    # 2 bodies x 4 slots each.
    assert len(chars) == 8
    assert len(bodies) == 2

    statuses = {c["status"] for c in chars}
    assert "live" in statuses          # slot 1 has a real photoshoot
    assert "placeholder" in statuses   # slots 2-4 borrow a sibling shoot

    # Slot 1 of each body is live and carries a hero image.
    live = [c for c in chars if c["status"] == "live"]
    assert all(c["photoshoot"]["hero"] for c in live)
    # Every character has a generated persona name + tagline.
    assert all(c["persona"]["name"] and c["persona"]["tagline"] for c in chars)


def test_main_writes_db_tables(built_profiles, monkeypatch):
    import sqlite3
    ws = built_profiles
    monkeypatch.setattr(build_characters, "DB", ws["db_path"])
    monkeypatch.setattr(build_characters, "BODY_PROFILES", ws["body_profiles"])
    monkeypatch.setattr(build_characters, "LEAD_PERSONAS", ws["db_dir"] / "_no_leads.json")
    monkeypatch.setattr(build_characters, "OVERLAY", ws["db_dir"] / "_no_overlay.json")
    monkeypatch.setattr(build_characters, "STORIES", ws["db_dir"] / "_no_stories.json")
    monkeypatch.setattr(build_characters, "OUT_CHARS", ws["db_dir"] / "characters.json")
    monkeypatch.setattr(build_characters, "OUT_BODIES", ws["db_dir"] / "body_types.json")
    build_characters.main()

    conn = sqlite3.connect(ws["db_path"])
    n = conn.execute("SELECT COUNT(*) FROM characters").fetchone()[0]
    conn.close()
    assert n == 8
