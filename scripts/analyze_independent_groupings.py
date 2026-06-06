"""
Build independent competitor catalog grouping artifacts from db/independent_competitor.sqlite.
Outputs:
- docs/research/independent-catalog-grouping-matrix.csv
- docs/research/independent-catalog-grouping-heatmap.md
- db/independent_catalog_groupings.json
"""

import csv
import json
import sqlite3
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
except ImportError as exc:
    raise SystemExit(
        "This script requires matplotlib, pandas, and seaborn. "
        "Install with: pip install matplotlib pandas seaborn"
    ) from exc

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "db" / "independent_competitor.sqlite"
OUT_CSV = ROOT / "docs" / "research" / "independent-catalog-grouping-matrix.csv"
OUT_MD = ROOT / "docs" / "research" / "independent-catalog-grouping-heatmap.md"
OUT_JSON = ROOT / "db" / "independent_catalog_groupings.json"

LINE_COLUMNS = [
    "full-body",
    "torso",
    "male",
    "exclusive",
    "house-brand",
    "multi-brand",
    "accessory",
    "unknown",
]

PRICE_BANDS = [
    ("lt_1200", 0, 1200),
    ("1200_1799", 1200, 1800),
    ("1800_2499", 1800, 2500),
    ("2500_3499", 2500, 3500),
    ("3500_plus", 3500, 10**9),
]

HEAT_CHARS = " .:-=+*#%@"
ZELEX_FULL_BODY_LINES = {"Inspiration", "SLE", "ZFE"}


def pct(part: int, whole: int) -> float:
    return 0.0 if whole == 0 else round((part / whole) * 100.0, 1)


def heat_char(value: float, max_value: float) -> str:
    if max_value <= 0:
        return " "
    ratio = min(1.0, max(0.0, value / max_value))
    idx = int(round(ratio * (len(HEAT_CHARS) - 1)))
    return HEAT_CHARS[idx]


def price_band(value: float | None) -> str:
    if value is None:
        return "unknown"
    for label, lo, hi in PRICE_BANDS:
        if lo <= value < hi:
            return label
    return "unknown"


def normalize_line(brand: str, line: str | None) -> str:
    if brand == "ZELEX" and (line in ZELEX_FULL_BODY_LINES):
        return "full-body"
    return line or "unknown"


def dominant_price_band(row: dict) -> str:
    keys = [label for label, _, _ in PRICE_BANDS]
    best = max(keys, key=lambda k: row.get(k, 0))
    if row.get(best, 0) == 0:
        return "unknown"
    return best


def price_band_breadth(row: dict) -> int:
    return sum(1 for label, _, _ in PRICE_BANDS if row.get(label, 0) > 0)


def write_png_heatmaps(line_matrix: list[dict], price_matrix: list[dict]) -> None:
    OUT_LINE_PNG.parent.mkdir(parents=True, exist_ok=True)

    line_df = pd.DataFrame(line_matrix)
    line_df = line_df.sort_values(["full_body_skus", "brand"], ascending=[False, True])
    line_df = line_df.set_index("brand")[["full-body", "torso", "male", "exclusive", "house-brand", "multi-brand", "accessory", "unknown"]]

    plt.figure(figsize=(13, max(6, len(line_df) * 0.35)))
    sns.heatmap(line_df, cmap="YlOrRd", linewidths=0.2, cbar_kws={"label": "SKU Count"})
    plt.title("Independent Competitor Line Architecture Heatmap")
    plt.xlabel("Line Type")
    plt.ylabel("Brand")
    plt.tight_layout()
    plt.savefig(OUT_LINE_PNG, dpi=180)
    plt.close()

    price_df = pd.DataFrame(price_matrix)
    price_df = price_df.sort_values(["brand"], ascending=[True])
    price_df = price_df.set_index("brand")[["lt_1200", "1200_1799", "1800_2499", "2500_3499", "3500_plus", "unknown_price"]]

    plt.figure(figsize=(12, max(6, len(price_df) * 0.3)))
    sns.heatmap(price_df, cmap="GnBu", linewidths=0.2, cbar_kws={"label": "SKU Count"})
    plt.title("Independent Competitor Price-Band Heatmap")
    plt.xlabel("Price Band")
    plt.ylabel("Brand")
    plt.tight_layout()
    plt.savefig(OUT_PRICE_PNG, dpi=180)
    plt.close()


def write_pdr_brief(
    line_matrix: list[dict],
    full_body_rows: list[dict],
    price_matrix: list[dict],
    wm_row: dict | None,
) -> None:
    price_by_brand = {row["brand"]: row for row in price_matrix}
    depth_top10 = sorted(full_body_rows, key=lambda r: (-r["full_body_skus"], r["brand"]))[:10]
    breadth_rows = [
        {
            "brand": r["brand"],
            "breadth": price_band_breadth(price_by_brand[r["brand"]]),
            "full_body_skus": r["full_body_skus"],
            "strategy_group": r["strategy_group"],
        }
        for r in full_body_rows
        if r["brand"] in price_by_brand
    ]
    breadth_top10 = sorted(
        breadth_rows,
        key=lambda r: (-r["breadth"], -r["full_body_skus"], r["brand"]),
    )[:10]

    depth_leaders = [r for r in full_body_rows if r["strategy_group"] == "Catalog Depth Leader"]
    aggregator_count = sum(1 for r in line_matrix if r["strategy_group"] == "Retail Aggregator")

    lines: list[str] = []
    lines.append("# PDR-010 Competitor Lineup Brief")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(
        f"Independent competitor grouping confirms {len(full_body_rows)} full-body competitor brands plus {aggregator_count} retail-aggregator catalogs."
    )
    if wm_row:
        lines.append(
            f"WM Doll remains the deepest observed line architecture in this crawl with {wm_row['full_body_skus']} full-body SKUs and additional torso/male extensions ({wm_row['torso']} torso, {wm_row['male']} male)."
        )
    lines.append(
        f"Depth leaders are {', '.join(r['brand'] for r in depth_leaders[:5])}; these brands define the current high-coverage benchmark for lineup breadth."
    )
    lines.append("Price-ladder breadth analysis highlights which brands compete across multiple consumer budget bands versus focused single-band positioning.")
    lines.append("")

    lines.append("## Top 10 by Full-Body Depth")
    lines.append("")
    lines.append("| Rank | Brand | Full-body SKUs | Strategy |")
    lines.append("|---:|---|---:|---|")
    for idx, row in enumerate(depth_top10, start=1):
        lines.append(f"| {idx} | {row['brand']} | {row['full_body_skus']} | {row['strategy_group']} |")
    lines.append("")

    lines.append("## Top 10 by Price-Ladder Breadth")
    lines.append("")
    lines.append("| Rank | Brand | Active Price Bands | Full-body SKUs | Strategy |")
    lines.append("|---:|---|---:|---:|---|")
    for idx, row in enumerate(breadth_top10, start=1):
        lines.append(
            f"| {idx} | {row['brand']} | {row['breadth']} | {row['full_body_skus']} | {row['strategy_group']} |"
        )
    lines.append("")

    lines.append("## Visual Matrix Artifacts")
    lines.append("")
    lines.append(f"- Line architecture heatmap: {OUT_LINE_PNG.relative_to(ROOT).as_posix()}")
    lines.append(f"- Price-band heatmap: {OUT_PRICE_PNG.relative_to(ROOT).as_posix()}")
    lines.append(f"- Full matrix CSV: {OUT_CSV.relative_to(ROOT).as_posix()}")
    lines.append(f"- Narrative matrix report: {OUT_MD.relative_to(ROOT).as_posix()}")

    OUT_PDR_BRIEF.parent.mkdir(parents=True, exist_ok=True)
    OUT_PDR_BRIEF.write_text("\n".join(lines) + "\n", encoding="utf-8")


def strategy_group(full_body_skus: int, line_counts: dict[str, int], median_price: float | None) -> str:
    total = sum(line_counts.values())
    torso_share = (line_counts.get("torso", 0) + line_counts.get("male", 0)) / total if total else 0.0
    retailer_share = (
        line_counts.get("house-brand", 0)
        + line_counts.get("multi-brand", 0)
        + line_counts.get("exclusive", 0)
        + line_counts.get("accessory", 0)
    ) / total if total else 0.0

    if retailer_share >= 0.25:
        return "Retail Aggregator"
    if full_body_skus >= 100:
        return "Catalog Depth Leader"
    if torso_share >= 0.20:
        return "Line Extension (torso/male)"
    if full_body_skus < 20 and (median_price or 0) >= 2500:
        return "Boutique Premium"
    return "Focused Midline"


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Missing database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    brands = [r["brand"] for r in cur.execute("SELECT DISTINCT brand FROM products ORDER BY brand")]

    line_matrix: list[dict] = []
    price_matrix: list[dict] = []
    strategies: list[dict] = []

    for brand in brands:
        total = cur.execute("SELECT COUNT(*) c FROM products WHERE brand=?", (brand,)).fetchone()["c"]
        median_price = cur.execute(
            "SELECT price_median FROM brand_summary WHERE brand=?", (brand,)
        ).fetchone()
        median_price_val = median_price["price_median"] if median_price else None

        line_counts = {k: 0 for k in LINE_COLUMNS}
        for row in cur.execute(
            "SELECT line, COUNT(*) c FROM products WHERE brand=? GROUP BY line", (brand,)
        ):
            line = normalize_line(brand, row["line"])
            line = line if line in line_counts else "unknown"
            line_counts[line] += row["c"]

        full_body = line_counts["full-body"]

        line_matrix.append(
            {
                "brand": brand,
                "total_products": total,
                "full_body_skus": full_body,
                **line_counts,
                "full_body_share_pct": pct(full_body, total),
                "strategy_group": strategy_group(full_body, line_counts, median_price_val),
            }
        )

        band_counts = {label: 0 for label, _, _ in PRICE_BANDS}
        unknown_price = 0
        for row in cur.execute("SELECT price_usd FROM products WHERE brand=?", (brand,)):
            label = price_band(row["price_usd"])
            if label == "unknown":
                unknown_price += 1
            else:
                band_counts[label] += 1
        price_matrix.append(
            {
                "brand": brand,
                **band_counts,
                "unknown_price": unknown_price,
            }
        )

        strategies.append(
            {
                "brand": brand,
                "strategy_group": line_matrix[-1]["strategy_group"],
                "full_body_skus": full_body,
                "median_price_usd": median_price_val,
            }
        )

    conn.close()

    full_body_rows = [
        r
        for r in line_matrix
        if r["full_body_skus"] > 0 and r["strategy_group"] != "Retail Aggregator"
    ]

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "brand",
            "total_products",
            "full_body_skus",
            *LINE_COLUMNS,
            "full_body_share_pct",
            "strategy_group",
            "lt_1200",
            "1200_1799",
            "1800_2499",
            "2500_3499",
            "3500_plus",
            "unknown_price",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        price_by_brand = {row["brand"]: row for row in price_matrix}
        for row in line_matrix:
            merged = dict(row)
            merged.update(price_by_brand[row["brand"]])
            writer.writerow(merged)

    lines = []
    lines.append("# Independent Catalog Groupings")
    lines.append("")
    lines.append("This report groups independent competitor catalogs by line architecture and price-band mix.")
    lines.append("")
    lines.append("## WM Doll Coverage Check")
    wm_row = next((r for r in line_matrix if r["brand"] == "WM Doll"), None)
    if wm_row:
        lines.append(
            f"- WM Doll present with {wm_row['total_products']} products, {wm_row['full_body_skus']} full-body SKUs, and line split across full-body/torso/male."
        )
    else:
        lines.append("- WM Doll not found in independent catalog DB.")
    lines.append("")

    lines.append("## Line Matrix Heatmap")
    lines.append("Legend: darker symbols indicate larger counts within each line column.")
    lines.append("")
    lines.append("| Brand | full-body | torso | male | exclusive | house-brand | multi-brand | accessory | unknown | Strategy |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")

    col_max = {k: max((r[k] for r in line_matrix), default=1) for k in LINE_COLUMNS}
    for row in sorted(line_matrix, key=lambda r: (-r["full_body_skus"], r["brand"])):
        cell = {}
        for col in LINE_COLUMNS:
            c = row[col]
            cell[col] = f"{c} {heat_char(c, col_max[col])}"
        lines.append(
            "| {brand} | {full-body} | {torso} | {male} | {exclusive} | {house-brand} | {multi-brand} | {accessory} | {unknown} | {strategy} |".format(
                brand=row["brand"],
                strategy=row["strategy_group"],
                **cell,
            )
        )

    lines.append("")
    lines.append("## Full-Body Competitor Heatmap")
    lines.append("Excludes retail aggregators and accessory-only catalogs; focuses on full-body competitor line architecture.")
    lines.append("")
    lines.append("| Brand | full-body | torso | male | unknown | Strategy |")
    lines.append("|---|---:|---:|---:|---:|---|")

    fb_cols = ["full-body", "torso", "male", "unknown"]
    fb_col_max = {k: max((r[k] for r in full_body_rows), default=1) for k in fb_cols}

    for row in sorted(full_body_rows, key=lambda r: (-r["full_body_skus"], r["brand"])):
        cell = {}
        for col in fb_cols:
            c = row[col]
            cell[col] = f"{c} {heat_char(c, fb_col_max[col])}"
        lines.append(
            "| {brand} | {full-body} | {torso} | {male} | {unknown} | {strategy} |".format(
                brand=row["brand"],
                strategy=row["strategy_group"],
                **cell,
            )
        )

    lines.append("")
    lines.append("## Competitor Line Archetypes")
    lines.append("Compact view of how each brand structures catalog depth, extensions, and price-ladder center.")
    lines.append("")
    lines.append("| Brand | Archetype | Full-body SKUs | Full-body share | Dominant price band |")
    lines.append("|---|---|---:|---:|---|")

    price_by_brand = {row["brand"]: row for row in price_matrix}
    for row in sorted(full_body_rows, key=lambda r: (r["strategy_group"], -r["full_body_skus"], r["brand"])):
        p = price_by_brand[row["brand"]]
        lines.append(
            f"| {row['brand']} | {row['strategy_group']} | {row['full_body_skus']} | {row['full_body_share_pct']}% | {dominant_price_band(p)} |"
        )

    lines.append("")
    lines.append("## Price-Band Matrix")
    lines.append("")
    lines.append("| Brand | <1200 | 1200-1799 | 1800-2499 | 2500-3499 | 3500+ | Unknown |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for row in sorted(price_matrix, key=lambda r: r["brand"]):
        lines.append(
            f"| {row['brand']} | {row['lt_1200']} | {row['1200_1799']} | {row['1800_2499']} | {row['2500_3499']} | {row['3500_plus']} | {row['unknown_price']} |"
        )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_from": str(DB_PATH.relative_to(ROOT)),
                "line_columns": LINE_COLUMNS,
                "line_matrix": line_matrix,
                "full_body_competitor_matrix": full_body_rows,
                "price_matrix": price_matrix,
                "strategy_groups": sorted(strategies, key=lambda r: (r["strategy_group"], r["brand"])),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        "Wrote "
        f"{OUT_CSV.relative_to(ROOT).as_posix()}, {OUT_MD.relative_to(ROOT).as_posix()}, {OUT_JSON.relative_to(ROOT).as_posix()}, "
        f"{OUT_LINE_PNG.relative_to(ROOT).as_posix()}, {OUT_PRICE_PNG.relative_to(ROOT).as_posix()}, and {OUT_PDR_BRIEF.relative_to(ROOT).as_posix()}"
    )


if __name__ == "__main__":
    main()
