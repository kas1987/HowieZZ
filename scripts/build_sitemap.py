#!/usr/bin/env python3
"""Generate sitemap.xml from the catalog data.

The Atlas is a small set of static templates driven by query parameters
(character.html?id=, body.html?b=, series.html?s=, family.html?f=). A sitemap
that lists only the bare templates points crawlers at empty pages, so this script
enumerates the real, content-bearing URLs from db/characters.json plus the family
taxonomy and writes them out.

Run from the repo root:  python scripts/build_sitemap.py
Re-run whenever the catalog changes (new characters/bodies/families).
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.zelexdoll.com"

# Canonical manufacturing-series order (mirrors ZX.SERIES_ORDER in assets/site.js).
SERIES_ORDER = ["K-Series", "Inspiration", "Fusion", "SLE"]


def enc(value: str) -> str:
    """URL-encode a query value the way encodeURIComponent does (space -> %20)."""
    return quote(str(value), safe="")


def main() -> None:
    chars = json.loads((ROOT / "db" / "characters.json").read_text("utf-8"))["characters"]
    families = json.loads((ROOT / "db" / "family_taxonomy.json").read_text("utf-8"))["families"]

    # (path, changefreq, priority) — bare pages that render meaningful content as-is.
    urls: list[tuple[str, str, str]] = [
        ("index.html", "weekly", "1.0"),
        ("browse.html", "weekly", "0.9"),
        ("family.html", "weekly", "0.9"),
        ("community.html", "weekly", "0.8"),
        ("quiz.html", "monthly", "0.8"),
        ("compare.html", "monthly", "0.7"),
        ("options.html", "monthly", "0.7"),
        ("configurator.html", "monthly", "0.6"),
        ("craft.html", "monthly", "0.6"),
        ("community-events.html", "monthly", "0.6"),
        ("contact.html", "monthly", "0.6"),
    ]

    # Family landings — all six (zero-body families render a development landing).
    for fam in families:
        urls.append((f"family.html?f={enc(fam['name'])}", "monthly", "0.7"))

    # Series landings, in canonical order, only those actually present.
    present_series = {c.get("series") for c in chars if c.get("series")}
    for s in SERIES_ORDER:
        if s in present_series:
            urls.append((f"series.html?s={enc(s)}", "weekly", "0.7"))

    # Body architectures — one URL per distinct body code.
    for bc in sorted({c["body_code"] for c in chars if c.get("body_code")}):
        urls.append((f"body.html?b={enc(bc)}", "weekly", "0.6"))

    # Characters — one URL per character id.
    for cid in sorted({c["character_id"] for c in chars if c.get("character_id")}):
        urls.append((f"character.html?id={enc(cid)}", "monthly", "0.5"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq, prio in urls:
        lines.append(
            f"  <url><loc>{BASE}/{path}</loc>"
            f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        )
    lines.append("</urlset>")
    lines.append("")

    out = ROOT / "sitemap.xml"
    out.write_text("\n".join(lines), "utf-8")
    print(f"Wrote {out} — {len(urls)} URLs")


if __name__ == "__main__":
    main()
