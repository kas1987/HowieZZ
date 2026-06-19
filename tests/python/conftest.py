"""Shared fixtures for the Python unit + pipeline-integration tests.

The build scripts use module-level path constants (ASSETS, DB, OUT_*). The
fixtures here construct a small synthetic asset tree in a temp directory and
monkeypatch those constants so the real catalog-build pipeline
(build_db -> build_profiles -> build_characters) can run end to end against
disposable data.
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
for _p in (str(REPO_ROOT), str(SCRIPTS_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

SCHEMA_SQL = (REPO_ROOT / "db" / "schema.sql").read_text(encoding="utf-8")

# Two synthetic bodies with full measurements so the WHR/BWR pipeline produces
# real profiles. Keys mirror db/body_measurements.json.
MEASUREMENTS = {
    "ZG170D": {
        "line": "I-Series", "spec_label": None, "nominal_height": 170, "cup": "D",
        "upper_bust": 84, "under_bust": 68, "waist": 58, "hip": 89, "weight_kg": 30.0,
    },
    "ZK168B": {
        "line": "K-Series", "spec_label": None, "nominal_height": 168, "cup": "B",
        "upper_bust": 80, "under_bust": 68, "waist": 56, "hip": 84, "weight_kg": 29.0,
    },
}

BODY_ALIASES = {"ZGE175E": "ZG175E"}


def _touch(path: Path, content: bytes = b"x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _make_assets(assets: Path):
    # I-Series product folder — head/face/body decodable, two photoshoot frames.
    i_dir = assets / "I-Series" / "GE149_1_GE74MJ_ZG170D"
    _touch(i_dir / "GE149-101.jpg")
    _touch(i_dir / "GE149-102.jpg")
    _touch(i_dir / "clip.mp4")
    # K-Series product folder.
    _touch(assets / "K-Series" / "KE03_1+ZK168B-1" / "KE03-101.jpg")
    # A SKIP_FOLDERS entry and a duplicate-cover folder to exercise skip branches.
    _touch(assets / "I-Series" / "OpenArt" / "x-101.jpg")
    _touch(assets / "SLE-Series" / "Sle3-cover" / "y-101.jpg")
    # Body spec cards (one plain code, one "spec-" prefixed).
    _touch(assets / "Measure" / "ZG170D.webp")
    _touch(assets / "Measure" / "spec-zk168b.webp")
    # Head reference image.
    _touch(assets / "Heads" / "Hard" / "GE03_2 (GE70MJ)-Fair-2.png")
    # Customization option.
    _touch(assets / "Options" / "Body Options" / "Hands" / "1#-Hard Hand.jpg")
    # Standalone video.
    _touch(assets / "MP4" / "promo.mp4")


@pytest.fixture
def workspace(tmp_path):
    ws_root = tmp_path / "ws"
    assets = ws_root / "assets"
    db_dir = ws_root / "db"
    assets.mkdir(parents=True)
    db_dir.mkdir(parents=True)
    (db_dir / "schema.sql").write_text(SCHEMA_SQL, encoding="utf-8")
    _make_assets(assets)
    return {
        "root": ws_root,
        "assets": assets,
        "db_dir": db_dir,
        "data_dir": assets / "data",
        "db_path": db_dir / "catalog.db",
        "json_path": db_dir / "catalog.json",
    }


@pytest.fixture
def built_db(workspace, monkeypatch):
    """Run build_db.build() against the synthetic asset tree."""
    import build_db

    ws = workspace
    monkeypatch.setattr(build_db, "ASSETS", ws["assets"])
    monkeypatch.setattr(build_db, "DB_DIR", ws["db_dir"])
    monkeypatch.setattr(build_db, "DB_PATH", ws["db_path"])
    monkeypatch.setattr(build_db, "JSON_PATH", ws["json_path"])
    monkeypatch.setattr(build_db, "DATA_DIR", ws["data_dir"])
    monkeypatch.setattr(build_db, "SCHEMA_PATH", ws["db_dir"] / "schema.sql")
    monkeypatch.setattr(build_db, "OVERRIDES_PATH", ws["db_dir"] / "_no_overrides.json")
    monkeypatch.setattr(build_db, "VARIANTS_PATH", ws["db_dir"] / "_no_variants.json")
    monkeypatch.setattr(build_db, "MEASUREMENTS", dict(MEASUREMENTS))
    monkeypatch.setattr(build_db, "BODY_ALIASES", dict(BODY_ALIASES))
    monkeypatch.setattr(build_db, "RESET", False)
    build_db.build()
    return ws


@pytest.fixture
def built_profiles(built_db, monkeypatch):
    """Run build_profiles.main() on top of the freshly built catalog DB."""
    import build_profiles

    ws = built_db
    meas_path = ws["db_dir"] / "body_measurements.json"
    meas_path.write_text(json.dumps({"bodies": MEASUREMENTS}), encoding="utf-8")
    out_json = ws["db_dir"] / "body_profiles.json"
    docs_dir = ws["root"] / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    out_md = docs_dir / "character-profiles.md"

    monkeypatch.setattr(build_profiles, "ROOT", ws["root"])
    monkeypatch.setattr(build_profiles, "DB", ws["db_path"])
    monkeypatch.setattr(build_profiles, "MEAS", meas_path)
    monkeypatch.setattr(build_profiles, "OVERLAY", ws["db_dir"] / "_no_overlay.json")
    monkeypatch.setattr(build_profiles, "OUT_JSON", out_json)
    monkeypatch.setattr(build_profiles, "OUT_MD", out_md)
    build_profiles.main()

    ws["body_profiles"] = out_json
    ws["profiles_md"] = out_md
    return ws
