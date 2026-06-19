"""Unit tests for scripts/build_sitemap.py."""
import json

import build_sitemap


def test_enc():
    assert build_sitemap.enc("The Classic") == "The%20Classic"
    assert build_sitemap.enc("a/b?c") == "a%2Fb%3Fc"


def test_main_writes_sitemap(tmp_path, monkeypatch):
    db = tmp_path / "db"
    db.mkdir()
    (db / "characters.json").write_text(json.dumps({"characters": [
        {"series": "K-Series", "body_code": "ZK168B", "character_id": "K-ZK168B-01"},
        {"series": "Inspiration", "body_code": "ZG170D", "character_id": "I-ZG170D-01"},
        {"series": "K-Series", "body_code": "ZK168B", "character_id": "K-ZK168B-02"},
    ]}), encoding="utf-8")
    (db / "family_taxonomy.json").write_text(json.dumps({"families": [
        {"name": "The Classic"}, {"name": "The Icon"},
    ]}), encoding="utf-8")

    monkeypatch.setattr(build_sitemap, "ROOT", tmp_path)
    build_sitemap.main()

    xml = (tmp_path / "sitemap.xml").read_text(encoding="utf-8")
    assert xml.startswith('<?xml version="1.0"')
    assert "<urlset" in xml
    # static + family + series + body + character URLs
    assert "index.html" in xml
    assert "family.html?f=The%20Classic" in xml
    assert "series.html?s=K-Series" in xml
    assert "body.html?b=ZK168B" in xml
    assert "character.html?id=K-ZK168B-01" in xml
    # Distinct body codes only appear once.
    assert xml.count("body.html?b=ZK168B") == 1
