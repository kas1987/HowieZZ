#!/usr/bin/env python3
"""Quick sanity checks for ZELEX analytics event exports.

Supports JSON array files or NDJSON (one JSON object per line).

Usage:
  python scripts/analytics_event_sanity.py --input path/to/events.ndjson
  python scripts/analytics_event_sanity.py --input path/to/events.json --pretty
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from typing import Any, Dict, Iterable, List


REQUIRED_GLOBAL_FIELDS = (
    "event",
    "event_original",
    "source",
    "schema_version",
    "session_id",
    "ts",
    "page",
    "path",
)

CANONICAL_EVENTS = {
    "page_view",
    "compare_add",
    "compare_clear",
    "compare_set_changed",
    "compare_view",
    "compare_handoff_click",
    "inquiry_validation_failed",
    "inquiry_submit_attempt",
    "inquiry_submit_success",
    "inquiry_submit_error",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sanity-check analytics event payload exports.")
    parser.add_argument("--input", required=True, help="Path to NDJSON or JSON array export")
    parser.add_argument("--schema-version", default="2026-06-06", help="Expected schema_version")
    parser.add_argument("--source", default="howiezz-web", help="Expected source")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON summary")
    parser.add_argument("--strict", action="store_true", help="Fail when required fields are missing or non-canonical events exist")
    parser.add_argument("--min-total-events", type=int, default=0, help="Minimum total events expected")
    parser.add_argument("--min-page-views", type=int, default=0, help="Minimum page_view count expected")
    parser.add_argument("--min-compare-add", type=int, default=0, help="Minimum compare_add count expected")
    parser.add_argument("--min-inquiry-attempts", type=int, default=0, help="Minimum inquiry_submit_attempt count expected")
    parser.add_argument("--min-attribution-coverage", type=float, default=0.0, help="Minimum attribution coverage ratio (0.0-1.0)")
    parser.add_argument("--max-missing-global", type=int, default=0, help="Maximum allowed missing required global fields")
    parser.add_argument("--output-json", default="", help="Optional path to write JSON summary output")
    return parser.parse_args()


def is_placeholder_path(path: str) -> bool:
    return path.strip() in {".", "./", ".\\"}


def load_events(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    raw_strip = raw.strip()
    if not raw_strip:
        return []

    if raw_strip.startswith("["):
        data = json.loads(raw_strip)
        if not isinstance(data, list):
            raise ValueError("JSON file must be an array when bracket format is used")
        return [x for x in data if isinstance(x, dict)]

    events: List[Dict[str, Any]] = []
    for idx, line in enumerate(raw.splitlines(), start=1):
        s = line.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid NDJSON at line {idx}: {exc}") from exc
        if isinstance(obj, dict):
            events.append(obj)
    return events


def missing_global_fields(events: Iterable[Dict[str, Any]]) -> Counter:
    c: Counter = Counter()
    for e in events:
        for key in REQUIRED_GLOBAL_FIELDS:
            if e.get(key) in (None, ""):
                c[key] += 1
    return c


def canonical_violations(events: Iterable[Dict[str, Any]]) -> Counter:
    c: Counter = Counter()
    for e in events:
        name = str(e.get("event") or "")
        if name and name not in CANONICAL_EVENTS:
            c[name] += 1
    return c


def coverage_checks(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    attempts = [e for e in events if e.get("event") == "inquiry_submit_attempt"]
    compare_attempts = [e for e in attempts if str(e.get("entry_source") or "") == "compare"]
    attributed_attempts = [e for e in attempts if str(e.get("entry_source") or "").strip()]
    compare_success = [
        e
        for e in events
        if e.get("event") == "inquiry_submit_success" and str(e.get("entry_source") or "") == "compare"
    ]

    attr_coverage = (len(attributed_attempts) / len(attempts)) if attempts else 0.0
    compare_submit_rate = (len(compare_success) / len(compare_attempts)) if compare_attempts else 0.0

    return {
        "inquiry_attempts": len(attempts),
        "attributed_attempts": len(attributed_attempts),
        "attribution_coverage": round(attr_coverage, 4),
        "compare_attempts": len(compare_attempts),
        "compare_success": len(compare_success),
        "compare_submit_rate": round(compare_submit_rate, 4),
    }


def summarize(events: List[Dict[str, Any]], expected_source: str, expected_schema: str) -> Dict[str, Any]:
    by_event = Counter(str(e.get("event") or "") for e in events)
    by_source = Counter(str(e.get("source") or "") for e in events)
    by_schema = Counter(str(e.get("schema_version") or "") for e in events)
    page_views = [e for e in events if e.get("event") == "page_view"]
    session_ids = {str(e.get("session_id") or "") for e in events if str(e.get("session_id") or "").strip()}

    missing = missing_global_fields(events)
    canonical = canonical_violations(events)

    return {
        "total_events": len(events),
        "event_counts": dict(by_event),
        "source_counts": dict(by_source),
        "schema_version_counts": dict(by_schema),
        "distinct_sessions": len(session_ids),
        "page_view_count": len(page_views),
        "expected_source_present": by_source.get(expected_source, 0),
        "expected_schema_present": by_schema.get(expected_schema, 0),
        "missing_global_field_counts": dict(missing),
        "non_canonical_event_counts": dict(canonical),
        "coverage": coverage_checks(events),
    }


def print_human(summary: Dict[str, Any]) -> None:
    print("Analytics Event Sanity Summary")
    print("-" * 40)
    print(f"Total events: {summary['total_events']}")
    print(f"Distinct sessions: {summary['distinct_sessions']}")
    print(f"Page views: {summary['page_view_count']}")
    print(f"Expected source matches: {summary['expected_source_present']}")
    print(f"Expected schema matches: {summary['expected_schema_present']}")

    print("\nEvent counts:")
    for k, v in sorted(summary["event_counts"].items()):
        if not k:
            continue
        print(f"  {k}: {v}")

    if summary["missing_global_field_counts"]:
        print("\nMissing required global fields:")
        for k, v in sorted(summary["missing_global_field_counts"].items()):
            print(f"  {k}: {v}")
    else:
        print("\nMissing required global fields: none")

    if summary["non_canonical_event_counts"]:
        print("\nNon-canonical event names:")
        for k, v in sorted(summary["non_canonical_event_counts"].items()):
            print(f"  {k}: {v}")
    else:
        print("\nNon-canonical event names: none")

    c = summary["coverage"]
    print("\nAttribution coverage checks:")
    print(f"  inquiry_attempts: {c['inquiry_attempts']}")
    print(f"  attributed_attempts: {c['attributed_attempts']}")
    print(f"  attribution_coverage: {c['attribution_coverage']}")
    print(f"  compare_attempts: {c['compare_attempts']}")
    print(f"  compare_success: {c['compare_success']}")
    print(f"  compare_submit_rate: {c['compare_submit_rate']}")


def evaluate_thresholds(summary: Dict[str, Any], args: argparse.Namespace) -> List[str]:
    failures: List[str] = []
    event_counts = summary.get("event_counts", {})
    total_missing = sum((summary.get("missing_global_field_counts", {}) or {}).values())
    non_canonical_total = sum((summary.get("non_canonical_event_counts", {}) or {}).values())
    coverage = summary.get("coverage", {}) or {}

    if summary.get("total_events", 0) < args.min_total_events:
      failures.append(
          f"total_events below minimum: {summary.get('total_events', 0)} < {args.min_total_events}"
      )

    if summary.get("page_view_count", 0) < args.min_page_views:
        failures.append(
            f"page_view_count below minimum: {summary.get('page_view_count', 0)} < {args.min_page_views}"
        )

    compare_add = int(event_counts.get("compare_add", 0) or 0)
    if compare_add < args.min_compare_add:
        failures.append(f"compare_add below minimum: {compare_add} < {args.min_compare_add}")

    inquiry_attempts = int(event_counts.get("inquiry_submit_attempt", 0) or 0)
    if inquiry_attempts < args.min_inquiry_attempts:
        failures.append(
            f"inquiry_submit_attempt below minimum: {inquiry_attempts} < {args.min_inquiry_attempts}"
        )

    attr_coverage = float(coverage.get("attribution_coverage", 0.0) or 0.0)
    if attr_coverage < args.min_attribution_coverage:
        failures.append(
            f"attribution_coverage below minimum: {attr_coverage:.4f} < {args.min_attribution_coverage:.4f}"
        )

    if total_missing > args.max_missing_global:
        failures.append(
            f"missing required global fields above threshold: {total_missing} > {args.max_missing_global}"
        )

    if args.strict:
        if total_missing > 0:
            failures.append(f"strict mode: missing required global fields found ({total_missing})")
        if non_canonical_total > 0:
            failures.append(f"strict mode: non-canonical events found ({non_canonical_total})")

    return failures


def main() -> int:
    args = parse_args()
    input_path = args.input.strip()

    # Guard against accidental placeholder path usage on Windows shells.
    if is_placeholder_path(input_path):
        print("Error: --input received a placeholder path ('.'). Provide a file path.", file=sys.stderr)
        return 2

    if not os.path.exists(input_path):
        print(f"Error: input file does not exist: {input_path}", file=sys.stderr)
        return 2

    try:
        events = load_events(input_path)
    except Exception as exc:
        print(f"Error: failed to parse events: {exc}", file=sys.stderr)
        return 2

    summary = summarize(events, args.source, args.schema_version)

    if args.output_json and str(args.output_json).strip():
        out_path = str(args.output_json).strip()
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, sort_keys=True)

    if args.pretty:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print_human(summary)

    failures = evaluate_thresholds(summary, args)
    if failures:
        print("\nThreshold check failures:")
        for msg in failures:
            print(f"  - {msg}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
