"""
Integration tests for build_characters.main().

Strategy: create a temporary directory mirroring the real db/ layout, populate
a minimal SQLite database with known fixture rows, monkeypatch all module-level
Path attributes in build_characters, then call main() and assert on the output.
"""
import json
import sqlite3
import pytest
import build_characters as bc


SERIES_ID = "K"
BODY_CODE = "ZK168B"


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """
    Build a minimal catalog.db + supporting JSON files in tmp_path,
    then monkeypatch build_characters module paths to point there.
    Returns tmp_path for further inspection.
    """
    db_dir = tmp_path / "db"
    db_dir.mkdir()

    # ── SQLite ────────────────────────────────────────────────────────────
    conn = sqlite3.connect(db_dir / "catalog.db")
    conn.executescript("""
        CREATE TABLE bodies (
            code TEXT PRIMARY KEY,
            series_id TEXT,
            height_cm REAL,
            cup_size TEXT,
            line_label TEXT
        );
        CREATE TABLE products (
            code TEXT PRIMARY KEY,
            head_code TEXT,
            face_code TEXT,
            folder_path TEXT,
            image_count INTEGER,
            price REAL,
            live_handle TEXT,
            body_code TEXT
        );
        CREATE TABLE product_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT,
            media_type TEXT,
            filename TEXT,
            rel_path TEXT
        );
    """)

    # body
    conn.execute(
        "INSERT INTO bodies VALUES (?,?,?,?,?)",
        (BODY_CODE, SERIES_ID, 168.0, "B", "ZK168B Classic"),
    )

    # products — 2 with real photoshoots, 0 additional
    for prod_code, head, face, img_count in [
        ("PROD1", "GE01_1", "GE01MJ", 4),
        ("PROD2", "GE02_1", None, 2),
    ]:
        conn.execute(
            "INSERT INTO products VALUES (?,?,?,?,?,?,?,?)",
            (prod_code, head, face, f"K-Series/{prod_code}/", img_count, 2000.0, prod_code.lower(), BODY_CODE),
        )
        for i in range(1, img_count + 1):
            fname = f"IMG-1{i:02d}.jpg"
            conn.execute(
                "INSERT INTO product_assets(product_code, media_type, filename, rel_path) VALUES (?,?,?,?)",
                (prod_code, "image", fname, f"K-Series/{prod_code}/{fname}"),
            )

    conn.commit()
    conn.close()

    # ── JSON stubs ─────────────────────────────────────────────────────────
    (db_dir / "body_profiles.json").write_text(
        json.dumps({"profiles": [
            {"body_code": BODY_CODE, "family": "The Classic", "silhouette": "hourglass",
             "WHR": 0.65, "BWR": 1.2, "bust_cm": 90, "waist_cm": 60, "hip_cm": 92,
             "weight_kg": 30, "bust_drop_cm": 15, "estimated": False}
        ]}), encoding="utf-8"
    )
    for fname in ("character_profiles.json", "character_overlay.json", "character_stories.json"):
        (db_dir / fname).write_text("{}", encoding="utf-8")

    # ── Monkeypatch module paths ────────────────────────────────────────────
    monkeypatch.setattr(bc, "ROOT", tmp_path)
    monkeypatch.setattr(bc, "DB",           db_dir / "catalog.db")
    monkeypatch.setattr(bc, "BODY_PROFILES", db_dir / "body_profiles.json")
    monkeypatch.setattr(bc, "LEAD_PERSONAS", db_dir / "character_profiles.json")
    monkeypatch.setattr(bc, "OVERLAY",       db_dir / "character_overlay.json")
    monkeypatch.setattr(bc, "STORIES",       db_dir / "character_stories.json")
    monkeypatch.setattr(bc, "OUT_CHARS",     db_dir / "characters.json")
    monkeypatch.setattr(bc, "OUT_BODIES",    db_dir / "body_types.json")

    return tmp_path


class TestBuildCharactersMain:

    def test_runs_without_error(self, tmp_db):
        bc.main()

    def test_writes_characters_json(self, tmp_db):
        bc.main()
        out = tmp_db / "db" / "characters.json"
        assert out.exists()

    def test_writes_body_types_json(self, tmp_db):
        bc.main()
        out = tmp_db / "db" / "body_types.json"
        assert out.exists()

    def test_produces_four_characters_per_body(self, tmp_db):
        bc.main()
        data = json.loads((tmp_db / "db" / "characters.json").read_text())
        chars = data["characters"]
        # 1 body × 4 slots = 4
        assert len(chars) == 4

    def test_character_ids_follow_pattern(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        expected_ids = {f"K-{BODY_CODE}-0{s}" for s in range(1, 5)}
        actual_ids = {c["character_id"] for c in chars}
        assert actual_ids == expected_ids

    def test_slot_numbering(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        slots = sorted(c["slot"] for c in chars)
        assert slots == [1, 2, 3, 4]

    def test_live_slots_match_product_count(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        live = [c for c in chars if c["status"] == "live"]
        # 2 products have real photoshoots
        assert len(live) == 2

    def test_placeholder_slots(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        placeholders = [c for c in chars if c["status"] == "placeholder"]
        assert len(placeholders) == 2

    def test_live_character_has_photoshoot(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        live = next(c for c in chars if c["status"] == "live")
        assert live["photoshoot"]["status"] == "live"
        assert live["photoshoot"]["hero"] is not None

    def test_placeholder_has_representative_only_flag(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        ph = next(c for c in chars if c["status"] == "placeholder")
        assert ph["photoshoot"].get("representative_only") is True

    def test_persona_name_assigned(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        for c in chars:
            assert c["persona"]["name"]  # non-empty string

    def test_persona_tagline_assigned(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        for c in chars:
            assert c["persona"]["tagline"]

    def test_body_metadata_in_character(self, tmp_db):
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        for c in chars:
            assert c["body"]["height_cm"] == 168.0
            assert c["body"]["cup"] == "B"
            assert c["body"]["family"] == "The Classic"

    def test_body_types_json_structure(self, tmp_db):
        bc.main()
        bts = json.loads((tmp_db / "db" / "body_types.json").read_text())["body_types"]
        assert len(bts) == 1
        bt = bts[0]
        assert bt["body_code"] == BODY_CODE
        assert bt["live_slots"] == 2
        assert len(bt["characters"]) == 4

    def test_torso_body_excluded(self, tmp_db, monkeypatch):
        # ZX84J is in TORSO_CODES, so even if we add it, it should be skipped
        db_path = tmp_db / "db" / "catalog.db"
        conn = sqlite3.connect(db_path)
        conn.execute("INSERT INTO bodies VALUES (?,?,?,?,?)", ('ZX84J', 'K', 84.0, 'E', 'Torso'))
        conn.execute(
            "INSERT INTO products(code, head_code, face_code, folder_path, image_count, price, live_handle, body_code) VALUES (?,?,?,?,?,?,?,?)",
            ('TORSO_PROD', 'GE99_1', None, 'K-Series/TORSO_PROD/', 2, 500.0, 'tp', 'ZX84J')
        )
        conn.execute("INSERT INTO product_assets(product_code, media_type, filename, rel_path) VALUES (?,?,?,?)",
                     ('TORSO_PROD', 'image', 'IMG-101.jpg', 'K-Series/TORSO_PROD/IMG-101.jpg'))
        conn.commit()
        conn.close()
        bc.main()
        chars = json.loads((tmp_db / "db" / "characters.json").read_text())["characters"]
        # ZX84J should be excluded — only ZK168B's 4 chars
        assert all(c["body_code"] != "ZX84J" for c in chars)
