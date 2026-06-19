"""Unit tests for scripts/analytics_event_sanity.py."""
import json

import analytics_event_sanity as aes


def make_event(**over):
    base = {
        "event": "page_view",
        "event_original": "page_view",
        "source": "howiezz-web",
        "schema_version": "2026-06-06",
        "session_id": "zx_abc",
        "ts": "2026-06-19T00:00:00Z",
        "page": "index.html",
        "path": "/index.html",
    }
    base.update(over)
    return base


# ── is_placeholder_path ─────────────────────────────────────────────────────

def test_is_placeholder_path():
    assert aes.is_placeholder_path(".") is True
    assert aes.is_placeholder_path("./") is True
    assert aes.is_placeholder_path(".\\") is True
    assert aes.is_placeholder_path("events.json") is False


# ── load_events ─────────────────────────────────────────────────────────────

def test_load_events_json_array(tmp_path):
    p = tmp_path / "e.json"
    p.write_text(json.dumps([make_event(), {"event": "compare_add"}, "skip-me"]), encoding="utf-8")
    events = aes.load_events(str(p))
    assert len(events) == 2  # the bare string is dropped


def test_load_events_ndjson(tmp_path):
    p = tmp_path / "e.ndjson"
    p.write_text("\n".join([json.dumps(make_event()), "", json.dumps(make_event())]), encoding="utf-8")
    assert len(aes.load_events(str(p))) == 2


def test_load_events_empty(tmp_path):
    p = tmp_path / "empty.ndjson"
    p.write_text("   \n", encoding="utf-8")
    assert aes.load_events(str(p)) == []


def test_load_events_bad_ndjson(tmp_path):
    p = tmp_path / "bad.ndjson"
    p.write_text("{not json}", encoding="utf-8")
    try:
        aes.load_events(str(p))
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "Invalid NDJSON" in str(exc)


def test_load_events_non_list_json(tmp_path):
    p = tmp_path / "obj.json"
    p.write_text('["a"]'.replace("[", "{").replace("]", "}"), encoding="utf-8")
    # A JSON object that *starts* with "[" is required to trigger the array path;
    # here it starts with "{" so it falls through NDJSON parsing of one line.
    # Explicitly test the bracket-but-not-array guard instead:
    p2 = tmp_path / "weird.json"
    p2.write_text("[", encoding="utf-8")
    try:
        aes.load_events(str(p2))
        assert False
    except ValueError:
        pass


# ── field / event validators ────────────────────────────────────────────────

def test_missing_global_fields():
    events = [make_event(session_id=""), make_event(page=None), make_event()]
    missing = aes.missing_global_fields(events)
    assert missing["session_id"] == 1
    assert missing["page"] == 1


def test_canonical_violations():
    events = [make_event(event="page_view"), make_event(event="totally_made_up")]
    viol = aes.canonical_violations(events)
    assert viol["totally_made_up"] == 1
    assert "page_view" not in viol


# ── coverage + summary ──────────────────────────────────────────────────────

def test_coverage_checks():
    events = [
        make_event(event="inquiry_submit_attempt", entry_source="compare"),
        make_event(event="inquiry_submit_attempt", entry_source=""),
        make_event(event="inquiry_submit_success", entry_source="compare"),
    ]
    cov = aes.coverage_checks(events)
    assert cov["inquiry_attempts"] == 2
    assert cov["attributed_attempts"] == 1
    assert cov["attribution_coverage"] == 0.5
    assert cov["compare_attempts"] == 1
    assert cov["compare_success"] == 1
    assert cov["compare_submit_rate"] == 1.0


def test_coverage_checks_empty():
    cov = aes.coverage_checks([])
    assert cov["attribution_coverage"] == 0.0
    assert cov["compare_submit_rate"] == 0.0


def test_summarize():
    events = [make_event(), make_event(event="compare_add"), make_event(event="bogus")]
    s = aes.summarize(events, "howiezz-web", "2026-06-06")
    assert s["total_events"] == 3
    assert s["page_view_count"] == 1
    assert s["distinct_sessions"] == 1
    assert s["expected_source_present"] == 3
    assert s["non_canonical_event_counts"]["bogus"] == 1


# ── evaluate_thresholds ─────────────────────────────────────────────────────

class Args:
    def __init__(self, **kw):
        self.min_total_events = kw.get("min_total_events", 0)
        self.min_page_views = kw.get("min_page_views", 0)
        self.min_compare_add = kw.get("min_compare_add", 0)
        self.min_inquiry_attempts = kw.get("min_inquiry_attempts", 0)
        self.min_attribution_coverage = kw.get("min_attribution_coverage", 0.0)
        self.max_missing_global = kw.get("max_missing_global", 0)
        self.strict = kw.get("strict", False)


def test_evaluate_thresholds_pass():
    s = aes.summarize([make_event(), make_event(event="compare_add")], "howiezz-web", "2026-06-06")
    assert aes.evaluate_thresholds(s, Args()) == []


def test_evaluate_thresholds_minimums_fail():
    s = aes.summarize([make_event()], "howiezz-web", "2026-06-06")
    failures = aes.evaluate_thresholds(
        s, Args(min_total_events=5, min_page_views=5, min_compare_add=1, min_inquiry_attempts=1,
                min_attribution_coverage=0.5)
    )
    joined = " ".join(failures)
    assert "total_events below minimum" in joined
    assert "page_view_count below minimum" in joined
    assert "compare_add below minimum" in joined
    assert "inquiry_submit_attempt below minimum" in joined
    assert "attribution_coverage below minimum" in joined


def test_evaluate_thresholds_strict_and_missing():
    s = aes.summarize([make_event(session_id=""), make_event(event="bogus")], "howiezz-web", "2026-06-06")
    failures = aes.evaluate_thresholds(s, Args(strict=True))
    joined = " ".join(failures)
    assert "missing required global fields above threshold" in joined
    assert "strict mode: missing required global fields" in joined
    assert "strict mode: non-canonical events" in joined


# ── print_human (smoke) ─────────────────────────────────────────────────────

def test_print_human(capsys):
    s = aes.summarize([make_event(), make_event(session_id="")], "howiezz-web", "2026-06-06")
    aes.print_human(s)
    out = capsys.readouterr().out
    assert "Analytics Event Sanity Summary" in out
    assert "Total events: 2" in out


def test_print_human_clean(capsys):
    s = aes.summarize([make_event()], "howiezz-web", "2026-06-06")
    aes.print_human(s)
    out = capsys.readouterr().out
    assert "Missing required global fields: none" in out
    assert "Non-canonical event names: none" in out


# ── main() end to end via argv ──────────────────────────────────────────────

def _run_main(monkeypatch, argv):
    monkeypatch.setattr(aes.sys, "argv", ["analytics_event_sanity.py"] + argv)
    return aes.main()


def test_main_success(tmp_path, monkeypatch, capsys):
    p = tmp_path / "e.ndjson"
    p.write_text("\n".join(json.dumps(make_event()) for _ in range(3)), encoding="utf-8")
    rc = _run_main(monkeypatch, ["--input", str(p), "--min-total-events", "3"])
    assert rc == 0
    assert "Analytics Event Sanity Summary" in capsys.readouterr().out


def test_main_pretty_and_output_json(tmp_path, monkeypatch, capsys):
    p = tmp_path / "e.json"
    p.write_text(json.dumps([make_event()]), encoding="utf-8")
    out = tmp_path / "out" / "summary.json"
    rc = _run_main(monkeypatch, ["--input", str(p), "--pretty", "--output-json", str(out)])
    assert rc == 0
    assert out.exists()
    summary = json.loads(out.read_text(encoding="utf-8"))
    assert summary["total_events"] == 1


def test_main_missing_file(tmp_path, monkeypatch):
    rc = _run_main(monkeypatch, ["--input", str(tmp_path / "nope.json")])
    assert rc == 2


def test_main_placeholder_path(monkeypatch):
    rc = _run_main(monkeypatch, ["--input", "."])
    assert rc == 2


def test_main_parse_error(tmp_path, monkeypatch):
    p = tmp_path / "bad.ndjson"
    p.write_text("{nope}", encoding="utf-8")
    rc = _run_main(monkeypatch, ["--input", str(p)])
    assert rc == 2


def test_main_threshold_failure(tmp_path, monkeypatch, capsys):
    p = tmp_path / "e.ndjson"
    p.write_text(json.dumps(make_event()), encoding="utf-8")
    rc = _run_main(monkeypatch, ["--input", str(p), "--min-total-events", "99"])
    assert rc == 1
    assert "Threshold check failures" in capsys.readouterr().out
