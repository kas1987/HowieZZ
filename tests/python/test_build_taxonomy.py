"""Unit tests for scripts/build_taxonomy.py."""
import json

import build_taxonomy


def _profiles_doc():
    return {
        "families": [
            {"name": "The Classic", "whr": [0.68, 0.72], "bwr": [1.40, 1.50],
             "silhouette": "Timeless hourglass", "premium": "+20%", "target": "First-time buyer"},
            {"name": "The Icon", "whr": [0.60, 0.65], "bwr": [1.50, 1.60],
             "silhouette": "Glamour model", "premium": "+30%", "target": "Curator"},
        ],
        "profiles": [
            {"body_code": "ZG170D", "series": "Inspiration", "height_cm": 170, "cup": "D",
             "WHR": 0.70, "BWR": 1.45, "bust_drop_cm": 16, "family": "The Classic",
             "family_confidence": "exact", "estimated": False},
            {"body_code": "ZK168B", "series": "K-Series", "height_cm": 168, "cup": "B",
             "WHR": None, "BWR": None, "bust_drop_cm": None, "family": "The Icon",
             "family_confidence": "near", "estimated": False},
        ],
    }


def test_main_builds_taxonomy(tmp_path, monkeypatch):
    src = tmp_path / "body_profiles.json"
    out = tmp_path / "family_taxonomy.json"
    src.write_text(json.dumps(_profiles_doc()), encoding="utf-8")

    monkeypatch.setattr(build_taxonomy, "SRC", src)
    monkeypatch.setattr(build_taxonomy, "OUT", out)
    monkeypatch.setattr(build_taxonomy, "ROOT", tmp_path)
    build_taxonomy.main()

    doc = json.loads(out.read_text(encoding="utf-8"))
    assert doc["version"] == "1.0.0"
    fams = {f["name"]: f for f in doc["families"]}

    classic = fams["The Classic"]
    assert classic["slug"] == "classic"
    assert classic["status"] == "active"
    assert classic["member_count"] == 1
    assert classic["members"] == ["ZG170D"]

    # The Icon has no body with a WHR -> remains in development.
    icon = fams["The Icon"]
    assert icon["status"] == "in_development"
    assert icon["member_count"] == 0

    # Bodies list excludes the one with WHR None.
    assert [b["body_code"] for b in doc["bodies"]] == ["ZG170D"]
