"""Unit tests for scripts/fetch_catalog.py — code extraction, HTTP, and main()."""
import json
from contextlib import contextmanager

import fetch_catalog


# ── pure helpers ────────────────────────────────────────────────────────────

def test_basename():
    assert fetch_catalog.basename("https://cdn.shop/x/y/GE149-101.jpg?v=2") == "GE149-101.jpg"
    assert fetch_catalog.basename("GE149-101.jpg") == "GE149-101.jpg"


def test_decode_sku_full():
    head, face, body, tone = fetch_catalog.decode_sku("GE149_1(GE74MJ)+ZG170D-Fair", "")
    assert head == "GE149_1"
    assert face == "GE74MJ"
    assert body == "ZG170D"
    assert tone == "Fair"


def test_decode_sku_body_from_title():
    head, face, body, tone = fetch_catalog.decode_sku("", "ZELEX ZG170D Premium Doll")
    assert head is None and face is None
    assert body == "ZG170D"
    assert tone is None


def test_decode_sku_tone_variants():
    _, _, _, tone = fetch_catalog.decode_sku("KE03_1+ZK168B-Tan", "")
    assert tone == "Tan"


# ── get_json (mocked urlopen) ───────────────────────────────────────────────

class _FakeResp:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self):
        return self._payload


@contextmanager
def _ctx(resp):
    yield resp


def test_get_json_success(monkeypatch):
    payload = json.dumps({"products": [{"id": 1}]}).encode("utf-8")
    monkeypatch.setattr(fetch_catalog.urllib.request, "urlopen",
                        lambda req, timeout=30: _ctx(_FakeResp(payload)))
    data = fetch_catalog.get_json("https://x/products.json")
    assert data == {"products": [{"id": 1}]}


def test_get_json_bad_json(monkeypatch, capsys):
    monkeypatch.setattr(fetch_catalog.urllib.request, "urlopen",
                        lambda req, timeout=30: _ctx(_FakeResp(b"not json")))
    assert fetch_catalog.get_json("https://x/products.json") is None
    assert "bad JSON" in capsys.readouterr().out


def test_get_json_network_failure(monkeypatch):
    monkeypatch.setattr(fetch_catalog.time, "sleep", lambda *_: None)

    def boom(req, timeout=30):
        raise fetch_catalog.urllib.error.URLError("down")

    monkeypatch.setattr(fetch_catalog.urllib.request, "urlopen", boom)
    assert fetch_catalog.get_json("https://x/products.json", retries=2) is None


# ── fetch_all_products (mocked get_json) ────────────────────────────────────

def test_fetch_all_products_paginates(monkeypatch):
    pages = {1: {"products": [{"id": 1}, {"id": 2}]}, 2: {"products": []}}

    def fake_get_json(url, retries=3):
        page = 2 if "page=2" in url else 1
        return pages[page]

    monkeypatch.setattr(fetch_catalog, "get_json", fake_get_json)
    monkeypatch.setattr(fetch_catalog, "USE_COLLECTIONS", False)
    products = fetch_catalog.fetch_all_products()
    assert [p["id"] for p in products] == [1, 2]


# ── main() integration against the synthetic catalog DB ─────────────────────

def test_main_matches_and_writes(built_db, monkeypatch, capsys):
    ws = built_db

    live_products = [{
        "id": 99,
        "handle": "ge149-zg170d-doll",
        "title": "ZELEX ZG170D Premium Doll",
        "vendor": "ZELEX",
        "tags": "silicone",
        "options": [{"name": "Skin", "values": ["Fair"]}],
        "images": [
            {"src": "https://cdn.shop/a/GE149-101.jpg"},
            {"src": "https://cdn.shop/a/GE149-102.jpg"},
            {"src": "https://cdn.shop/a/extra-200.jpg"},  # one image we don't have -> asset gap
        ],
        "variants": [{
            "sku": "GE149_1(GE74MJ)+ZG170D-Fair",
            "title": "Fair",
            "price": "1999.00",
            "compare_at_price": None,
            "option1": "Fair", "option2": None, "option3": None,
        }],
    }]

    monkeypatch.setattr(fetch_catalog, "DB", ws["db_path"])
    monkeypatch.setattr(fetch_catalog, "DB_DIR", ws["db_dir"])
    monkeypatch.setattr(fetch_catalog, "fetch_all_products", lambda: live_products)
    fetch_catalog.main()

    overrides = json.loads((ws["db_dir"] / "product_overrides.json").read_text(encoding="utf-8"))
    assert "GE149_1_GE74MJ_ZG170D" in overrides
    ov = overrides["GE149_1_GE74MJ_ZG170D"]
    assert ov["live_handle"] == "ge149-zg170d-doll"
    assert ov["body_code"] == "ZG170D"

    gaps = json.loads((ws["db_dir"] / "asset_gaps.json").read_text(encoding="utf-8"))
    assert gaps["GE149_1_GE74MJ_ZG170D"] == ["extra-200.jpg"]

    variants = json.loads((ws["db_dir"] / "live_variants.json").read_text(encoding="utf-8"))
    assert variants[0]["handle"] == "ge149-zg170d-doll"
    assert "Matched" in capsys.readouterr().out
