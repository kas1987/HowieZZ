"""Unit tests for scripts/build_db.py — folder/filename parsers + full build()."""
import json
import sqlite3

import build_db


# ── Folder-name parsers ─────────────────────────────────────────────────────

def test_parse_i_folder_full():
    assert build_db.parse_i_folder("GE149_1_GE74MJ_ZG170D") == ("GE149_1", "GE74MJ", "ZG170D", None)


def test_parse_i_folder_head_only():
    assert build_db.parse_i_folder("GE52_1") == ("GE52_1", None, None, None)


def test_parse_i_folder_with_shoot():
    head, face, body, shoot = build_db.parse_i_folder("GE149_1_GE74MJ_ZG170D-2")
    assert (head, face, body, shoot) == ("GE149_1", "GE74MJ", "ZG170D", 2)


def test_parse_k_folder():
    assert build_db.parse_k_folder("KE03_1+ZK168B-1") == ("KE03_1", None, "ZK168B", 1)


def test_parse_fusion_folder():
    assert build_db.parse_fusion_folder("ZFE01_1+ZF168B") == ("ZFE01_1", None, "ZF168B", None)


def test_parse_sle_folder_variants():
    assert build_db.parse_sle_folder("ZXE200_1_ZX166K") == ("ZXE200_1", None, "ZX166K", None)
    assert build_db.parse_sle_folder("ZX201_2_ZX172E") == ("ZX201_2", None, "ZX172E", None)
    assert build_db.parse_sle_folder("ZXE200_W1_ZX171C") == ("ZXE200_W1", None, "ZX171C", None)
    assert build_db.parse_sle_folder("ZXE201_1_ZX84J") == ("ZXE201_1", None, "ZX84J", None)
    head, _, body, _ = build_db.parse_sle_folder("ZXE200_1+ZX165D-Tan-Sle3.0")
    assert (head, body) == ("ZXE200_1", "ZX165D")


# ── Code decoders ───────────────────────────────────────────────────────────

def test_decode_body():
    assert build_db.decode_body("ZGX165F") == ("ZGX", 165, "F")
    assert build_db.decode_body("ZK168B") == ("ZK", 168, "B")


def test_decode_body_miss():
    assert build_db.decode_body("not-a-code") == (None, None, None)


def test_body_series():
    assert build_db.body_series("ZK168B") == "K"
    assert build_db.body_series("ZF168B") == "Fusion"
    assert build_db.body_series("ZX166K") == "SLE"
    assert build_db.body_series("ZG170D") == "I"
    assert build_db.body_series("ZGX165F") == "I"


def test_canon_body(monkeypatch):
    monkeypatch.setattr(build_db, "BODY_ALIASES", {"ZGE175E": "ZG175E"})
    assert build_db.canon_body("ZGE175E") == "ZG175E"
    assert build_db.canon_body("ZG170D") == "ZG170D"
    assert build_db.canon_body(None) is None
    assert build_db.canon_body("") == ""


# ── Filename parsers ────────────────────────────────────────────────────────

def test_parse_head_filename_variants():
    assert build_db.parse_head_filename("GE03_2 (GE70MJ)-Fair-2.png") == ("GE03_2", "GE70MJ", "Fair", 2)
    assert build_db.parse_head_filename("GE82_1(GE47MJ)-Fair.png") == ("GE82_1", "GE47MJ", "Fair", 1)
    assert build_db.parse_head_filename("GE45_8-Fair.jpg") == ("GE45_8", None, "Fair", 1)
    assert build_db.parse_head_filename("GE02-1(GE46MJ)-Tan.png") == ("GE02_1", "GE46MJ", "Tan", 1)


def test_parse_head_filename_miss():
    assert build_db.parse_head_filename("random.png") == (None, None, None, None)


def test_parse_body_spec():
    assert build_db.parse_body_spec("ZG162D.webp") == "ZG162D"
    assert build_db.parse_body_spec("ZG170C-cm-pc.webp") == "ZG170C"
    assert build_db.parse_body_spec("spec-zk159d.webp") == "ZK159D"
    assert build_db.parse_body_spec("nope.webp") is None


def test_parse_option():
    assert build_db.parse_option("1#-Hard Hand.jpg") == ("1#", "Hard Hand")
    key, label = build_db.parse_option("justastem.jpg")
    assert key == "justastem" and label is None


def test_seq():
    assert build_db.seq("cover-101.jpg") == 101
    assert build_db.seq("cover.jpg") is None


# ── JSON loader helper ──────────────────────────────────────────────────────

def test_load_json_missing(tmp_path):
    assert build_db._load_json(tmp_path / "absent.json", {"d": 1}) == {"d": 1}


def test_load_json_bad(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid", encoding="utf-8")
    assert build_db._load_json(bad, []) == []
    assert "could not parse" in capsys.readouterr().out


def test_load_json_ok(tmp_path):
    good = tmp_path / "good.json"
    good.write_text('{"a": 1}', encoding="utf-8")
    assert build_db._load_json(good, {}) == {"a": 1}


# ── Full build() integration ────────────────────────────────────────────────

def test_build_creates_db_and_json(built_db):
    ws = built_db
    assert ws["db_path"].exists()
    assert ws["json_path"].exists()

    catalog = json.loads(ws["json_path"].read_text(encoding="utf-8"))
    codes = {p["code"] for p in catalog["products"]}
    assert "GE149_1_GE74MJ_ZG170D" in codes
    assert "KE03_1+ZK168B-1" in codes
    # Skipped folders must not appear as products.
    assert "OpenArt" not in codes
    assert not any("Sle3" in c for c in codes)

    body_codes = {b["code"] for b in catalog["bodies"]}
    assert {"ZG170D", "ZK168B"} <= body_codes


def test_build_decodes_product_fields(built_db):
    conn = sqlite3.connect(built_db["db_path"])
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM products WHERE code='GE149_1_GE74MJ_ZG170D'"
    ).fetchone()
    conn.close()
    assert row["head_code"] == "GE149_1"
    assert row["face_code"] == "GE74MJ"
    assert row["body_code"] == "ZG170D"
    assert row["image_count"] == 2
    assert row["video_count"] == 1


def test_build_writes_measurements_and_specs(built_db):
    conn = sqlite3.connect(built_db["db_path"])
    n_meas = conn.execute("SELECT COUNT(*) FROM body_measurements").fetchone()[0]
    n_specs = conn.execute("SELECT COUNT(*) FROM body_specs").fetchone()[0]
    n_heads = conn.execute("SELECT COUNT(*) FROM head_images").fetchone()[0]
    n_opts = conn.execute("SELECT COUNT(*) FROM options").fetchone()[0]
    n_vids = conn.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
    conn.close()
    assert n_meas == 2
    assert n_specs == 2
    assert n_heads == 1
    assert n_opts == 1
    assert n_vids == 1


def test_build_writes_per_product_json(built_db):
    detail = built_db["data_dir"] / "GE149_1_GE74MJ_ZG170D.json"
    assert detail.exists()
    payload = json.loads(detail.read_text(encoding="utf-8"))
    assert payload["code"] == "GE149_1_GE74MJ_ZG170D"
    assert len(payload["assets"]) == 3  # two images + one video
