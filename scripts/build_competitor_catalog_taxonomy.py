#!/usr/bin/env python3
"""Build a competitor catalogue taxonomy comparison from accessible supplier pages.

This script scrapes whole body-style catalogues from public supplier pages,
classifies each body against the existing ZELEX family ranges, and writes a
machine-readable dataset plus a markdown summary.

Current priority: catalogue taxonomy coverage and family comparison, not the
full ROI package.
"""

from __future__ import annotations

import csv
import json
import math
import re
import sqlite3
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import requests
    from bs4 import BeautifulSoup, Tag
except ImportError as exc:  # pragma: no cover - explicit runtime guidance
    raise SystemExit(
        "This script requires requests and beautifulsoup4. "
        "Install them with: pip install requests beautifulsoup4"
    ) from exc


ROOT = Path(__file__).resolve().parent.parent
FAMILY_TAXONOMY = ROOT / "db" / "family_taxonomy.json"
BODY_PROFILES = ROOT / "db" / "body_profiles.json"
OUT_JSON = ROOT / "db" / "competitor_family_coverage.json"
OUT_SQLITE = ROOT / "db" / "competitor_family_coverage.sqlite"
OUT_CSV = ROOT / "docs" / "research" / "competitor-family-coverage-matrix.csv"
OUT_MD = ROOT / "docs" / "research" / "competitor-family-coverage-matrix.md"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; HowieZZ/1.0)"}


@dataclass(frozen=True)
class SupplierConfig:
    brand: str
    slug: str
    source_tier: str = "secondary"
    source_label: str = "Dollstudio supplier catalogue"

    @property
    def url(self) -> str:
        return f"https://us.dollstudio.org/supplier/{self.slug}"


SUPPLIERS = [
    # Core volume brands
    SupplierConfig("WM Doll", "wm-doll"),
    SupplierConfig("JY Doll", "jy-doll"),
    SupplierConfig("YL Doll", "yl-doll"),
    SupplierConfig("SE Doll", "se-doll"),
    SupplierConfig("6YE Premium", "6ye-premium"),
    SupplierConfig("Jarliet", "jarliet"),
    SupplierConfig("AS Doll", "as-doll"),
    SupplierConfig("XT Doll", "xt-doll"),
    SupplierConfig("HR Doll", "hr-doll"),
    # Mid-premium brands
    SupplierConfig("Piper Doll", "piper-doll"),
    SupplierConfig("Real Lady", "real-lady"),
    SupplierConfig("Angel Kiss", "angel-kiss"),
    SupplierConfig("Irokebijin", "irokebijin"),
    SupplierConfig("JK Doll", "jk-doll"),
    SupplierConfig("SM Doll", "sm-doll"),
    SupplierConfig("Hitdoll", "hitdoll"),
    SupplierConfig("ILdoll", "ildoll"),
    SupplierConfig("Jiusheng", "jiusheng"),
    # Premium / ultra-premium brands
    SupplierConfig("Game Lady", "game-lady"),
    SupplierConfig("Gynoid", "gynoid"),
    # ZELEX via Dollstudio (cross-check against local baseline)
    SupplierConfig("ZELEX (Dollstudio)", "zelex"),
]

# ---------------------------------------------------------------------------
# Geographic / market metadata — encoded from public brand knowledge
# ---------------------------------------------------------------------------
BRAND_GEO: dict[str, dict] = {
    "ZELEX": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
              "primary_markets": ["NA", "EU", "AU", "APAC"],
              "tier": "premium", "tier_usd_floor": 2800,
              "segment": "silicone", "market_notes": "Premium silicone; strong EU and North America presence"},
    "WM Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU", "APAC"],
                "tier": "mid", "tier_usd_floor": 1500,
                "segment": "tpe", "market_notes": "Largest volume TPE manufacturer; global reseller network"},
    "Irontech Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                      "primary_markets": ["NA", "EU", "AU"],
                      "tier": "premium", "tier_usd_floor": 2750,
                      "segment": "silicone", "market_notes": "#1 silicone claim; US/EU stock; direct persona branding"},
    "Piper Doll": {"country": "China", "hq_city": "Shenzhen", "region": "Asia",
                   "primary_markets": ["NA", "EU", "AU"],
                   "tier": "mid-premium", "tier_usd_floor": 1200,
                   "segment": "silicone_tpe", "market_notes": "Broadest family taxonomy; strong NA reseller network"},
    "JY Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "mid", "tier_usd_floor": 1800,
                "segment": "silicone_tpe", "market_notes": "Fantasy/anime crossover skew; heavy Siren catalogue"},
    "YL Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "mid", "tier_usd_floor": 1500,
                "segment": "silicone_tpe", "market_notes": "Fantasy and athletic skew; Siren/Sculpt heavy catalogue"},
    "SE Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "mid", "tier_usd_floor": 1400,
                "segment": "silicone_tpe", "market_notes": "Broad family spread; closest to ZELEX Muse positioning"},
    "Real Lady": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                  "primary_markets": ["NA", "EU"],
                  "tier": "premium", "tier_usd_floor": 2500,
                  "segment": "silicone", "market_notes": "Irontech sub-brand; Empress/plush skew"},
    "6YE Premium": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                    "primary_markets": ["NA", "EU"],
                    "tier": "budget-mid", "tier_usd_floor": 1200,
                    "segment": "silicone_tpe", "market_notes": "Entry price silicone; broad Asia/NA distribution"},
    "Tayu": {"country": "China", "hq_city": "Guangzhou", "region": "Asia",
             "primary_markets": ["NA", "EU", "AU"],
             "tier": "mid-premium", "tier_usd_floor": 2500,
             "segment": "silicone", "market_notes": "NOVA series; compact and proportional; strong NA DTC presence"},
    "RealDoll": {"country": "USA", "hq_city": "San Marcos CA", "region": "North America",
                 "primary_markets": ["NA", "EU"],
                 "tier": "ultra-premium", "tier_usd_floor": 5000,
                 "segment": "silicone", "market_notes": "US-made; 20yr prestige; AI/robot pivot; no guided discovery"},
    "Gynoid": {"country": "China", "hq_city": "Shenzhen", "region": "Asia",
               "primary_markets": ["NA", "EU", "JP"],
               "tier": "ultra-premium", "tier_usd_floor": 4500,
               "segment": "silicone", "market_notes": "Hyper-realist sculptural detail; collector market; near RealDoll price tier"},
    "Game Lady": {"country": "China", "hq_city": "Shenzhen", "region": "Asia",
                  "primary_markets": ["NA", "EU", "JP"],
                  "tier": "premium", "tier_usd_floor": 2500,
                  "segment": "silicone", "market_notes": "Character/cosplay focus; Western game-character replicas"},
    "Irokebijin": {"country": "Japan", "hq_city": "Tokyo", "region": "Asia",
                   "primary_markets": ["JP", "NA", "EU"],
                   "tier": "mid-premium", "tier_usd_floor": 1800,
                   "segment": "silicone", "market_notes": "Japanese domestic brand; natural proportions; strong JP market"},
    "Jarliet": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "budget-mid", "tier_usd_floor": 1200,
                "segment": "tpe", "market_notes": "Budget TPE entry; wide body range"},
    "HR Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "mid", "tier_usd_floor": 1500,
                "segment": "silicone", "market_notes": "BBW/plush specialist; Empress-lane depth"},
    "XT Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "mid", "tier_usd_floor": 1800,
                "segment": "silicone", "market_notes": "Broad silicone catalogue; mid-tier pricing"},
    "Angel Kiss": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                   "primary_markets": ["NA", "EU"],
                   "tier": "mid-premium", "tier_usd_floor": 2000,
                   "segment": "silicone", "market_notes": "Soft-realist silicone; growing NA presence"},
    "AS Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "budget-mid", "tier_usd_floor": 1500,
                "segment": "tpe", "market_notes": "TPE with silicone head options"},
    "JK Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU", "JP"],
                "tier": "mid-premium", "tier_usd_floor": 2000,
                "segment": "silicone", "market_notes": "Anime/character crossover; similar to JY in positioning"},
    "SM Doll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "mid", "tier_usd_floor": 1500,
                "segment": "silicone_tpe", "market_notes": "Multi-material; broad body range"},
    "Hitdoll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                "primary_markets": ["NA", "EU"],
                "tier": "mid", "tier_usd_floor": 1500,
                "segment": "silicone", "market_notes": "Silicone specialist; limited Western brand recognition"},
    "ILdoll": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
               "primary_markets": ["NA", "EU"],
               "tier": "mid", "tier_usd_floor": 1500,
               "segment": "silicone", "market_notes": "Realistic silicone; niche mid-tier brand"},
    "Jiusheng": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                 "primary_markets": ["NA", "EU", "APAC"],
                 "tier": "mid", "tier_usd_floor": 1600,
                 "segment": "silicone_tpe", "market_notes": "Volume mid-tier; moderate Western distribution"},
    "ZELEX (Dollstudio)": {"country": "China", "hq_city": "Zhongshan", "region": "Asia",
                           "primary_markets": ["NA", "EU", "AU", "APAC"],
                           "tier": "premium", "tier_usd_floor": 2800,
                           "segment": "silicone", "market_notes": "Same brand as baseline; Dollstudio cross-check"},
}

# Market tier definitions for the market analysis table
MARKET_TIERS = [
    {"tier": "budget", "usd_range": "<$1,200", "description": "Entry-level TPE; volume-first; minimal brand investment"},
    {"tier": "budget-mid", "usd_range": "$1,200-$1,800", "description": "Entry silicone or mid TPE; broad reseller distribution"},
    {"tier": "mid", "usd_range": "$1,800-$2,500", "description": "Established mid silicone; multiple series; reseller networks"},
    {"tier": "mid-premium", "usd_range": "$2,500-$3,500", "description": "Premium silicone features; branded; limited editions"},
    {"tier": "premium", "usd_range": "$3,500-$5,000", "description": "High-craft silicone; curated discovery; buyer personas"},
    {"tier": "ultra-premium", "usd_range": ">$5,000", "description": "Artisan/collector; US-made or flagship; bespoke options"},
]

# Geographic market segments referenced in BRAND_GEO
MARKET_REGIONS = [
    {"code": "NA", "label": "North America", "key_countries": "USA, Canada",
     "notes": "Largest single revenue market; highest price tolerance; RealDoll, Irontech, Tayu strong here"},
    {"code": "EU", "label": "Europe", "key_countries": "Germany, UK, France, Netherlands",
     "notes": "Second-largest market; stricter import/content regulations in some countries"},
    {"code": "APAC", "label": "Asia-Pacific", "key_countries": "Australia, South Korea, Singapore",
     "notes": "Growing premium segment; Australia is key English-speaking premium market"},
    {"code": "JP", "label": "Japan", "key_countries": "Japan",
     "notes": "Domestic market with local brands (Irokebijin); different aesthetic preferences"},
    {"code": "AU", "label": "Australia", "key_countries": "Australia, NZ",
     "notes": "English-speaking premium market; high customs scrutiny; ZELEX has presence"},
    {"code": "AS", "label": "Asia (other)", "key_countries": "China, Taiwan, SEA",
     "notes": "Manufacturer home markets; growing domestic consumption"},
]

UNAVAILABLE_COMPETITORS = [
    {
        "brand": "Doll Forever",
        "status": "pending-source",
        "reason": "No stable machine-readable body-style catalogue endpoint has been integrated yet.",
        "source_url": "https://www.dollforever.com/",
    },
    {
        "brand": "Tayu",
        "status": "pending-source",
        "reason": "No stable machine-readable body-style catalogue endpoint has been integrated yet.",
        "source_url": "https://www.tayudoll.com/",
    },
    {
        "brand": "Sanhui",
        "status": "pending-source",
        "reason": "No stable machine-readable body-style catalogue endpoint has been integrated yet.",
        "source_url": "https://www.sanhuidoll.com/",
    },
    {
        "brand": "6YE",
        "status": "pending-source",
        "reason": "No stable machine-readable body-style catalogue endpoint has been integrated yet.",
        "source_url": "https://www.6yedoll.com/",
    },
]


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def parse_number(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def parse_text(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    return normalize_space(match.group(1))


def format_pct(count: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return f"{(count / total) * 100:.1f}%"


def median_value(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def load_family_ranges() -> list[dict]:
    doc = json.loads(FAMILY_TAXONOMY.read_text(encoding="utf-8"))
    families = []
    for family in doc["families"]:
        families.append(
            {
                "name": family["name"],
                "slug": family["slug"],
                "whr_range": family["whr_range"],
                "bwr_range": family["bwr_range"],
                "whr_center": sum(family["whr_range"]) / 2,
                "bwr_center": sum(family["bwr_range"]) / 2,
            }
        )
    return families


def load_zelex_baseline() -> list[dict]:
    doc = json.loads(BODY_PROFILES.read_text(encoding="utf-8"))
    rows = []
    for profile in doc["profiles"]:
        bust = profile.get("bust_cm")
        waist = profile.get("waist_cm")
        hips = profile.get("hip_cm")
        if not (bust and waist and hips):
            continue
        rows.append(
            {
                "brand": "ZELEX",
                "source_url": "local:db/body_profiles.json",
                "source_tier": "official",
                "source_label": "Local ZELEX body profile database",
                "body_code": profile["body_code"],
                "title": profile["body_code"],
                "series": profile.get("series"),
                "material": None,
                "height_cm": profile.get("height_cm"),
                "weight_kg": profile.get("weight_kg"),
                "bust_cm": bust,
                "waist_cm": waist,
                "hip_cm": hips,
                "underbust_cm": profile.get("underbust_cm"),
                "cup": profile.get("cup"),
                "price": None,
                "price_currency": None,
                "WHR": round(profile["WHR"], 3),
                "BWR": round(profile["BWR"], 3),
                "assigned_family": profile["family"],
                "family_confidence": profile.get("family_confidence", "manual-review"),
                "family_basis": "Existing ZELEX family taxonomy",
                "notes": "Local baseline row",
            }
        )
    return rows


def nearest_family(whr: float, bwr: float, families: Iterable[dict]) -> tuple[str, str, str]:
    exact_matches = []
    candidates = []
    for family in families:
        whr_in = family["whr_range"][0] <= whr <= family["whr_range"][1]
        bwr_in = family["bwr_range"][0] <= bwr <= family["bwr_range"][1]
        score = math.hypot(whr - family["whr_center"], bwr - family["bwr_center"])
        candidates.append((score, family, whr_in, bwr_in))
        if whr_in and bwr_in:
            exact_matches.append((score, family))

    if exact_matches:
        exact_matches.sort(key=lambda item: item[0])
        winner = exact_matches[0][1]
        return winner["name"], "exact", "Both WHR and BWR fall inside the family range"

    candidates.sort(key=lambda item: item[0])
    _, winner, whr_in, bwr_in = candidates[0]
    if whr_in or bwr_in:
        return winner["name"], "near", "Nearest family center with one ratio inside range"
    return winner["name"], "manual-review", "Nearest family center outside both range bands"


def extract_body_code(title: str, href: str) -> str:
    patterns = [
        r"\b([A-Z]{1,4}(?:-[A-Z0-9]{1,6})+\/[A-Z0-9]{1,3})\b",
        r"\b([A-Z]{1,4}(?:-[A-Z0-9]{1,6})+)\b",
        r"\b([A-Z]{2,5}[/-][A-Z0-9]{2,})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(1)
    return Path(href).name.replace("-", " ").upper()


def measurement_text_from_card(anchor: Tag) -> str:
    current: Tag | None = anchor
    for _ in range(6):
        if current is None:
            break
        if isinstance(current, Tag):
            block = normalize_space(current.get_text(" ", strip=True))
            if all(token in block for token in ("Height:", "Waist:", "Hips:")):
                return block
        current = current.parent  # type: ignore[assignment]
    return ""


def fetch_text(url: str, session: requests.Session) -> str:
    response = session.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def scrape_supplier(config: SupplierConfig, session: requests.Session, families: list[dict]) -> list[dict]:
    html = fetch_text(config.url, session)
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    seen_urls: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if f"/products/doll/{config.slug}/" not in href:
            continue
        url = f"https://us.dollstudio.org{href}"
        if url in seen_urls:
            continue
        seen_urls.add(url)

        title = normalize_space(anchor.get_text(" ", strip=True)) or extract_body_code("", href)
        if title.startswith("‣"):
            continue

        block = measurement_text_from_card(anchor)
        if not block:
            # Avoid deep per-product fetches in supplier mode; rely on inline card specs.
            continue

        height = parse_number(r"Height:\s*([\d.]+)\s*cm", block) or parse_number(r"Body height[^\d]*([\d.]+)\s*cm", block)
        weight = parse_number(r"Weight:\s*([\d.]+)\s*kg", block) or parse_number(r"weights?\s*(?:ca\.)?\s*([\d.]+)\s*kg", block)
        bust = parse_number(r"Breasts?:\s*([\d.]+)\s*cm", block) or parse_number(r"Bust/Chest\s*([\d.]+)\s*cm", block)
        waist = parse_number(r"Waist:\s*([\d.]+)\s*cm", block)
        hips = parse_number(r"Hips?:\s*([\d.]+)\s*cm", block)
        underbust = parse_number(r"under bust\)?[:\s]*([\d.]+)\s*cm", block)
        price = parse_number(r"Price:\s*\$([\d,]+(?:\.\d+)?)", block)
        material = parse_text(r"Material:\s*([A-Za-z\-/ ]+?)(?:\s+Price:|\s+SKU\b|\s+Product\b|\s*$)", block)
        cup = parse_text(r"Cup Size\s*([A-Z][^\s,;)]*)", block) or parse_text(r"Cup\s*size\s*([A-Z][^\s,;)]*)", block)

        if not (height and bust and waist and hips):
            continue

        whr = round(waist / hips, 3)
        bwr = round(bust / waist, 3)
        family, confidence, basis = nearest_family(whr, bwr, families)

        rows.append(
            {
                "brand": config.brand,
                "source_url": url,
                "source_tier": config.source_tier,
                "source_label": config.source_label,
                "body_code": extract_body_code(title, href),
                "title": title,
                "series": None,
                "material": material,
                "height_cm": height,
                "weight_kg": weight,
                "bust_cm": bust,
                "waist_cm": waist,
                "hip_cm": hips,
                "underbust_cm": underbust,
                "cup": cup,
                "price": price,
                "price_currency": "USD" if price is not None else None,
                "WHR": whr,
                "BWR": bwr,
                "assigned_family": family,
                "family_confidence": confidence,
                "family_basis": basis,
                "notes": None,
            }
        )

    rows.sort(key=lambda row: (row["brand"], row["height_cm"], row["body_code"]))
    return rows


def irontech_product_links(session: requests.Session) -> list[str]:
    seeds = ["https://www.irontechdoll.com/", "https://www.irontechdoll.com/shop/"]
    links: set[str] = set()
    for seed in seeds:
        html = fetch_text(seed, session)
        soup = BeautifulSoup(html, "html.parser")
        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            if "/product/" not in href:
                continue
            if href.startswith("http"):
                links.add(href.rstrip("/"))
            else:
                links.add(f"https://www.irontechdoll.com{href}".rstrip("/"))
    return sorted(links)


def parse_irontech_specs(soup: BeautifulSoup) -> dict[str, str]:
    # Irontech product pages include a structured two-column spec table.
    pairs: dict[str, str] = {}
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) != 2:
            continue
        key = normalize_space(cells[0].get_text(" ", strip=True)).lower()
        value = normalize_space(cells[1].get_text(" ", strip=True))
        if not key:
            continue
        pairs[key] = value
    return pairs


def scrape_irontech(session: requests.Session, families: list[dict]) -> list[dict]:
    rows = []
    seen_codes: set[str] = set()
    for url in irontech_product_links(session):
        html = fetch_text(url, session)
        soup = BeautifulSoup(html, "html.parser")
        specs = parse_irontech_specs(soup)
        if not specs:
            continue

        title = normalize_space(soup.title.get_text(strip=True)) if soup.title else Path(url).name
        body_code = extract_body_code(title, url)

        if body_code in seen_codes:
            continue

        material = specs.get("material")
        cup_raw = specs.get("cup size")
        cup = None
        if cup_raw:
            cup_match = re.search(r"([A-Z]+)", cup_raw, re.IGNORECASE)
            cup = cup_match.group(1).upper() if cup_match else None

        height = parse_number(r"([\d.]+)\s*cm", specs.get("height", ""))
        bust = parse_number(r"([\d.]+)\s*cm", specs.get("breastline", ""))
        underbust = parse_number(r"([\d.]+)\s*cm", specs.get("under breastline", ""))
        waist = parse_number(r"([\d.]+)\s*cm", specs.get("waistline", ""))
        hips = parse_number(r"([\d.]+)\s*cm", specs.get("hipline", ""))
        weight = parse_number(r"body:\s*([\d.]+)\s*kg", specs.get("weight", ""))

        if not (height and bust and waist and hips):
            continue

        seen_codes.add(body_code)
        whr = round(waist / hips, 3)
        bwr = round(bust / waist, 3)
        family, confidence, basis = nearest_family(whr, bwr, families)

        rows.append(
            {
                "brand": "Irontech Doll",
                "source_url": url,
                "source_tier": "official",
                "source_label": "Irontech official product specifications",
                "body_code": body_code,
                "title": title,
                "series": None,
                "material": material,
                "height_cm": height,
                "weight_kg": weight,
                "bust_cm": bust,
                "waist_cm": waist,
                "hip_cm": hips,
                "underbust_cm": underbust,
                "cup": cup,
                "price": parse_number(r'"product:price:amount"\s+content="([\d.]+)"', html),
                "price_currency": "USD",
                "WHR": whr,
                "BWR": bwr,
                "assigned_family": family,
                "family_confidence": confidence,
                "family_basis": basis,
                "notes": "Deduplicated by body code from Irontech product catalogue",
            }
        )

    rows.sort(key=lambda row: (row["height_cm"], row["body_code"]))
    return rows


def parse_xml_locs(xml_text: str) -> list[str]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    return [node.text for node in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if node.text]


def scrape_tayu(session: requests.Session, families: list[dict]) -> list[dict]:
    rows = []
    seen_codes: set[str] = set()
    idx = fetch_text("https://www.tayu-doll.com/sitemap.xml", session)
    sitemap_urls = parse_xml_locs(idx)
    product_sitemap = next((u for u in sitemap_urls if "product-sitemap" in u), None)
    if not product_sitemap:
        return rows

    product_urls = [u for u in parse_xml_locs(fetch_text(product_sitemap, session)) if "/product/" in u]

    # Tayu sitemap has many head/set variants for the same underlying body.
    # Pre-dedupe by URL body key so we fetch one representative page per body.
    representative_urls: dict[str, str] = {}
    for url in product_urls:
        slug = Path(url.rstrip("/")).name.lower()
        key_match = re.search(r"(\d{3}cm-[a-z]\+?-cup)", slug)
        if key_match:
            key = key_match.group(1)
        else:
            parts = slug.split("-")
            key = "-".join(parts[:3]) if len(parts) >= 3 else slug
        representative_urls.setdefault(key, url)

    for url in representative_urls.values():
        html = fetch_text(url, session)
        soup = BeautifulSoup(html, "html.parser")
        text = normalize_space(soup.get_text(" ", strip=True))

        body_label = parse_text(r"Body:\s*([^:]+?)\s+Head:", text) or parse_text(r"Body:\s*(Tayu[^.]{4,80})", text)
        if not body_label:
            body_label = Path(url).name
        body_code = normalize_space(body_label.upper())
        if body_code in seen_codes:
            continue

        height = parse_number(r"Height:\s*([\d.]+)\s*cm", text)
        bust = parse_number(r"Bust:\s*([\d.]+)\s*cm", text)
        waist = parse_number(r"Waist:\s*([\d.]+)\s*cm", text)
        hips = parse_number(r"Hips:\s*([\d.]+)\s*cm", text)
        underbust = parse_number(r"Under\s*Bust:\s*([\d.]+)\s*cm", text)
        weight = parse_number(r"Body\s*weight:\s*([\d.]+)\s*kg", text)
        cup = parse_text(r"Body:\s*[^,]*\b([A-Z]\+?)\s*Cup", text) or parse_text(r"\b([A-Z]\+?)\s*Cup\b", text)
        price = parse_number(r'"product:price:amount"\s+content="([\d.]+)"', html)

        if not (height and bust and waist and hips):
            continue

        seen_codes.add(body_code)
        whr = round(waist / hips, 3)
        bwr = round(bust / waist, 3)
        family, confidence, basis = nearest_family(whr, bwr, families)

        rows.append(
            {
                "brand": "Tayu",
                "source_url": url,
                "source_tier": "official",
                "source_label": "Tayu official product specifications",
                "body_code": body_code,
                "title": normalize_space(soup.title.get_text(strip=True)) if soup.title else body_code,
                "series": parse_text(r"Collection:\s*([A-Za-z0-9\- ]+)", text),
                "material": parse_text(r"Body\s*Material:\s*([A-Za-z0-9\- ]+)", text),
                "height_cm": height,
                "weight_kg": weight,
                "bust_cm": bust,
                "waist_cm": waist,
                "hip_cm": hips,
                "underbust_cm": underbust,
                "cup": cup,
                "price": price,
                "price_currency": "USD" if price is not None else None,
                "WHR": whr,
                "BWR": bwr,
                "assigned_family": family,
                "family_confidence": confidence,
                "family_basis": basis,
                "notes": "Deduplicated by body descriptor from Tayu product sitemap",
            }
        )
    rows.sort(key=lambda row: (row["height_cm"], row["body_code"]))
    return rows


def capture_realdoll_inventory(session: requests.Session) -> list[dict]:
    idx = fetch_text("https://www.realdoll.com/sitemap_index.xml", session)
    sitemap_urls = parse_xml_locs(idx)
    product_sitemap = next((u for u in sitemap_urls if "product-sitemap" in u), None)
    if not product_sitemap:
        return []
    product_urls = [u for u in parse_xml_locs(fetch_text(product_sitemap, session)) if "/product/" in u]

    body_keywords = ("olivia", "quinn", "stephanie", "tanya", "robot-", "rc2-")
    inventory = []
    for url in sorted(product_urls):
        slug = Path(url.rstrip("/")).name
        if not any(key in slug for key in body_keywords):
            continue
        html = fetch_text(url, session)
        soup = BeautifulSoup(html, "html.parser")
        title = normalize_space(soup.title.get_text(strip=True)) if soup.title else slug
        inventory.append(
            {
                "brand": "RealDoll",
                "model_slug": slug,
                "title": title,
                "source_url": url,
                "classification_status": "inventory-only",
                "reason": "No consistent bust/waist/hip measurements exposed on product pages.",
            }
        )
    return inventory


def build_summary(rows: list[dict], unavailable: list[dict], inventory_only: list[dict] | None = None) -> dict:
    brand_rows: dict[str, list[dict]] = {}
    for row in rows:
        brand_rows.setdefault(row["brand"], []).append(row)

    families = ["The Classic", "The Icon", "The Muse", "The Siren", "The Empress", "The Sculpt"]
    brands = []
    for brand, items in sorted(brand_rows.items()):
        counts = Counter(item["assigned_family"] for item in items)
        confidence_counts = Counter(item.get("family_confidence") for item in items)
        source_tier_counts = Counter(item.get("source_tier") for item in items)
        total = len(items)
        top = counts.most_common(2)
        top_share = round(sum(count for _, count in top) / total * 100, 1) if total else 0.0
        prices = [float(item["price"]) for item in items if item.get("price") is not None]
        complete_measurements = [
            item for item in items if all(item.get(k) is not None for k in ("height_cm", "bust_cm", "waist_cm", "hip_cm"))
        ]
        material_text = " ".join((item.get("material") or "").lower() for item in items)
        silicone_count = sum(1 for item in items if "silicone" in (item.get("material") or "").lower())
        tpe_count = sum(1 for item in items if "tpe" in (item.get("material") or "").lower())
        brands.append(
            {
                "brand": brand,
                "total": total,
                "top_two_share_pct": top_share,
                "family_counts": {family: counts.get(family, 0) for family in families},
                "materials": sorted({item["material"] for item in items if item.get("material")}),
                "height_min_cm": min(item["height_cm"] for item in items),
                "height_max_cm": max(item["height_cm"] for item in items),
                "pricing": {
                    "count": len(prices),
                    "coverage_pct": round((len(prices) / total) * 100, 1) if total else 0.0,
                    "median_usd": round(median_value(prices), 2) if prices else None,
                    "min_usd": round(min(prices), 2) if prices else None,
                    "max_usd": round(max(prices), 2) if prices else None,
                },
                "quality_signals": {
                    "measurement_completeness_pct": round((len(complete_measurements) / total) * 100, 1) if total else 0.0,
                    "silicone_share_pct": round((silicone_count / total) * 100, 1) if total else 0.0,
                    "tpe_share_pct": round((tpe_count / total) * 100, 1) if total else 0.0,
                    "exact_plus_near_pct": round(((confidence_counts.get("exact", 0) + confidence_counts.get("near", 0)) / total) * 100, 1) if total else 0.0,
                    "source_tier_mix": dict(source_tier_counts),
                },
                "confidence_mix": dict(confidence_counts),
            }
        )

    return {
        "row_count": len(rows),
        "brand_count": len(brands),
        "brands": brands,
        "unavailable_competitors": unavailable,
        "inventory_only": inventory_only or [],
    }


def write_csv(rows: list[dict]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "brand",
        "body_code",
        "title",
        "source_url",
        "source_tier",
        "height_cm",
        "weight_kg",
        "bust_cm",
        "waist_cm",
        "hip_cm",
        "underbust_cm",
        "cup",
        "material",
        "price",
        "price_currency",
        "WHR",
        "BWR",
        "assigned_family",
        "family_confidence",
        "family_basis",
        "notes",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name) for name in fieldnames})


def write_sqlite(rows: list[dict], summary: dict) -> None:
    OUT_SQLITE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(OUT_SQLITE)
    try:
        cur = conn.cursor()
        cur.executescript(
            """
            PRAGMA journal_mode = WAL;
            DROP TABLE IF EXISTS competitor_rows;
            DROP TABLE IF EXISTS brand_summary;
            DROP TABLE IF EXISTS inventory_only;

            CREATE TABLE competitor_rows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT,
                body_code TEXT,
                title TEXT,
                source_url TEXT,
                source_tier TEXT,
                source_label TEXT,
                series TEXT,
                material TEXT,
                height_cm REAL,
                weight_kg REAL,
                bust_cm REAL,
                waist_cm REAL,
                hip_cm REAL,
                underbust_cm REAL,
                cup TEXT,
                price REAL,
                price_currency TEXT,
                whr REAL,
                bwr REAL,
                assigned_family TEXT,
                family_confidence TEXT,
                family_basis TEXT,
                notes TEXT
            );

            CREATE TABLE brand_summary (
                brand TEXT PRIMARY KEY,
                total INTEGER,
                top_two_share_pct REAL,
                classic_count INTEGER,
                icon_count INTEGER,
                muse_count INTEGER,
                siren_count INTEGER,
                empress_count INTEGER,
                sculpt_count INTEGER,
                height_min_cm REAL,
                height_max_cm REAL,
                pricing_count INTEGER,
                pricing_coverage_pct REAL,
                median_price_usd REAL,
                min_price_usd REAL,
                max_price_usd REAL,
                measurement_completeness_pct REAL,
                silicone_share_pct REAL,
                tpe_share_pct REAL,
                exact_plus_near_pct REAL,
                source_tier_mix_json TEXT,
                confidence_mix_json TEXT,
                materials_json TEXT
            );

            CREATE TABLE inventory_only (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT,
                model_slug TEXT,
                title TEXT,
                source_url TEXT,
                classification_status TEXT,
                reason TEXT
            );

            CREATE INDEX idx_competitor_rows_brand ON competitor_rows(brand);
            CREATE INDEX idx_competitor_rows_family ON competitor_rows(assigned_family);
            CREATE INDEX idx_competitor_rows_tier ON competitor_rows(source_tier);

            CREATE TABLE IF NOT EXISTS brand_geographic (
                brand TEXT PRIMARY KEY,
                country TEXT,
                hq_city TEXT,
                region TEXT,
                primary_markets_json TEXT,
                tier TEXT,
                tier_usd_floor REAL,
                segment TEXT,
                market_notes TEXT
            );

            CREATE TABLE IF NOT EXISTS market_tiers (
                tier TEXT PRIMARY KEY,
                usd_range TEXT,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS market_regions (
                code TEXT PRIMARY KEY,
                label TEXT,
                key_countries TEXT,
                notes TEXT
            );
            """
        )

        cur.executemany(
            """
            INSERT INTO competitor_rows (
                brand, body_code, title, source_url, source_tier, source_label,
                series, material, height_cm, weight_kg, bust_cm, waist_cm, hip_cm,
                underbust_cm, cup, price, price_currency, whr, bwr,
                assigned_family, family_confidence, family_basis, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row.get("brand"),
                    row.get("body_code"),
                    row.get("title"),
                    row.get("source_url"),
                    row.get("source_tier"),
                    row.get("source_label"),
                    row.get("series"),
                    row.get("material"),
                    row.get("height_cm"),
                    row.get("weight_kg"),
                    row.get("bust_cm"),
                    row.get("waist_cm"),
                    row.get("hip_cm"),
                    row.get("underbust_cm"),
                    row.get("cup"),
                    row.get("price"),
                    row.get("price_currency"),
                    row.get("WHR"),
                    row.get("BWR"),
                    row.get("assigned_family"),
                    row.get("family_confidence"),
                    row.get("family_basis"),
                    row.get("notes"),
                )
                for row in rows
            ],
        )

        cur.executemany(
            """
            INSERT INTO brand_summary (
                brand, total, top_two_share_pct,
                classic_count, icon_count, muse_count, siren_count, empress_count, sculpt_count,
                height_min_cm, height_max_cm,
                pricing_count, pricing_coverage_pct, median_price_usd, min_price_usd, max_price_usd,
                measurement_completeness_pct, silicone_share_pct, tpe_share_pct, exact_plus_near_pct,
                source_tier_mix_json, confidence_mix_json, materials_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    brand.get("brand"),
                    brand.get("total"),
                    brand.get("top_two_share_pct"),
                    brand.get("family_counts", {}).get("The Classic", 0),
                    brand.get("family_counts", {}).get("The Icon", 0),
                    brand.get("family_counts", {}).get("The Muse", 0),
                    brand.get("family_counts", {}).get("The Siren", 0),
                    brand.get("family_counts", {}).get("The Empress", 0),
                    brand.get("family_counts", {}).get("The Sculpt", 0),
                    brand.get("height_min_cm"),
                    brand.get("height_max_cm"),
                    brand.get("pricing", {}).get("count"),
                    brand.get("pricing", {}).get("coverage_pct"),
                    brand.get("pricing", {}).get("median_usd"),
                    brand.get("pricing", {}).get("min_usd"),
                    brand.get("pricing", {}).get("max_usd"),
                    brand.get("quality_signals", {}).get("measurement_completeness_pct"),
                    brand.get("quality_signals", {}).get("silicone_share_pct"),
                    brand.get("quality_signals", {}).get("tpe_share_pct"),
                    brand.get("quality_signals", {}).get("exact_plus_near_pct"),
                    json.dumps(brand.get("quality_signals", {}).get("source_tier_mix", {}), ensure_ascii=False),
                    json.dumps(brand.get("confidence_mix", {}), ensure_ascii=False),
                    json.dumps(brand.get("materials", []), ensure_ascii=False),
                )
                for brand in summary.get("brands", [])
            ],
        )

        cur.executemany(
            """
            INSERT INTO inventory_only (
                brand, model_slug, title, source_url, classification_status, reason
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item.get("brand"),
                    item.get("model_slug"),
                    item.get("title"),
                    item.get("source_url"),
                    item.get("classification_status"),
                    item.get("reason"),
                )
                for item in summary.get("inventory_only", [])
            ],
        )
        # brand_geographic
        cur.executemany(
            "INSERT OR REPLACE INTO brand_geographic "
            "(brand, country, hq_city, region, primary_markets_json, tier, tier_usd_floor, segment, market_notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    brand_name,
                    geo.get("country"),
                    geo.get("hq_city"),
                    geo.get("region"),
                    json.dumps(geo.get("primary_markets", []), ensure_ascii=False),
                    geo.get("tier"),
                    geo.get("tier_usd_floor"),
                    geo.get("segment"),
                    geo.get("market_notes"),
                )
                for brand_name, geo in BRAND_GEO.items()
            ],
        )

        # market_tiers
        cur.executemany(
            "INSERT OR REPLACE INTO market_tiers (tier, usd_range, description) VALUES (?, ?, ?)",
            [(t["tier"], t["usd_range"], t["description"]) for t in MARKET_TIERS],
        )

        # market_regions
        cur.executemany(
            "INSERT OR REPLACE INTO market_regions (code, label, key_countries, notes) VALUES (?, ?, ?, ?)",
            [(r["code"], r["label"], r["key_countries"], r["notes"]) for r in MARKET_REGIONS],
        )

        conn.commit()
    finally:
        conn.close()


def write_markdown(summary: dict) -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    brands_by_name = {brand["brand"]: brand for brand in summary["brands"]}
    zelex = brands_by_name.get("ZELEX")
    lines = [
        "# Competitor Catalogue Taxonomy Comparison",
        "",
        "This report maps accessible competitor body-style catalogues into the ZELEX six-family system so we can compare catalogue shape before the full ROI layer is written.",
        "",
        f"- Brands covered: {summary['brand_count']}",
        f"- Body-style rows classified: {summary['row_count']}",
        "- Source standard: public supplier catalogue pages with explicit measurements, classified against the current ZELEX family ranges",
        "",
        "## Apples-to-Apples Signals",
        "",
        "| Brand | Price coverage | Median price (USD) | Price range (USD) | Measurement completeness | Silicone share | TPE share | Exact+Near confidence | Source mix |",
        "|---|---:|---:|---|---:|---:|---:|---:|---|",
    ]

    for brand in summary["brands"]:
        pricing = brand["pricing"]
        quality = brand["quality_signals"]
        range_text = "n/a"
        if pricing["min_usd"] is not None and pricing["max_usd"] is not None:
            range_text = f"{pricing['min_usd']:.0f}-{pricing['max_usd']:.0f}"
        lines.append(
            "| {brand} | {cov}% ({cnt}/{total}) | {med} | {rng} | {mc}% | {sil}% | {tpe}% | {conf}% | {mix} |".format(
                brand=brand["brand"],
                cov=pricing["coverage_pct"],
                cnt=pricing["count"],
                total=brand["total"],
                med=f"{pricing['median_usd']:.0f}" if pricing["median_usd"] is not None else "n/a",
                rng=range_text,
                mc=quality["measurement_completeness_pct"],
                sil=quality["silicone_share_pct"],
                tpe=quality["tpe_share_pct"],
                conf=quality["exact_plus_near_pct"],
                mix=", ".join(f"{k}:{v}" for k, v in sorted(quality["source_tier_mix"].items())),
            )
        )

    lines.extend([
        "",
        "## Brand Coverage Table",
        "",
        "| Brand | Total bodies | Classic | Icon | Muse | Siren | Empress | Sculpt | Top-2 share | Height span |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ])

    for brand in summary["brands"]:
        counts = brand["family_counts"]
        height_span = f"{int(brand['height_min_cm'])}-{int(brand['height_max_cm'])} cm"
        lines.append(
            "| {brand} | {total} | {classic} | {icon} | {muse} | {siren} | {empress} | {sculpt} | {share}% | {span} |".format(
                brand=brand["brand"],
                total=brand["total"],
                classic=counts["The Classic"],
                icon=counts["The Icon"],
                muse=counts["The Muse"],
                siren=counts["The Siren"],
                empress=counts["The Empress"],
                sculpt=counts["The Sculpt"],
                share=brand["top_two_share_pct"],
                span=height_span,
            )
        )

    if summary["unavailable_competitors"]:
        lines.extend([
            "",
            "## Current Gaps",
            "",
        ])
        for item in summary["unavailable_competitors"]:
            lines.append(f"- {item['brand']}: {item['reason']} ({item['source_url']})")

    if summary.get("inventory_only"):
        lines.extend([
            "",
            "## Inventory-Only Captures",
            "",
            "The following brands were crawled for catalogue inventory, but family classification is not yet possible because standardized body measurements are not exposed.",
            "",
        ])
        grouped: dict[str, list[dict]] = {}
        for item in summary["inventory_only"]:
            grouped.setdefault(item["brand"], []).append(item)
        for brand, items in sorted(grouped.items()):
            lines.append(f"- {brand}: {len(items)} model URLs captured (classification pending).")

    lines.extend([
        "",
        "## Brand-by-Brand Read",
        "",
    ])

    for brand in summary["brands"]:
        if brand["brand"] == "ZELEX":
            continue

        counts = brand["family_counts"]
        total = brand["total"]
        ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        present = [name.replace("The ", "") for name, count in ranked if count > 0]
        top_family, top_count = ranked[0]
        second_family, second_count = ranked[1]
        missing = [name.replace("The ", "") for name, count in counts.items() if count == 0]
        overlap = []
        whitespace = []
        if zelex:
            for family_name, count in counts.items():
                zelex_count = zelex["family_counts"].get(family_name, 0)
                label = family_name.replace("The ", "")
                if count > 0 and zelex_count > 0:
                    overlap.append(label)
                if count > 0 and zelex_count == 0:
                    whitespace.append(label)

        lines.extend([
            f"### {brand['brand']}",
            "",
            f"- Catalogue shape: {total} classified bodies across {len(present)} active families, led by {top_family.replace('The ', '')} ({format_pct(top_count, total)}) and {second_family.replace('The ', '')} ({format_pct(second_count, total)}).",
            f"- Compared with ZELEX: top-two concentration is {brand['top_two_share_pct']}% versus ZELEX at {zelex['top_two_share_pct']}%, so this catalogue is {'broader' if brand['top_two_share_pct'] < zelex['top_two_share_pct'] else 'narrower'} than the current ZELEX spread.",
            f"- Family overlap with ZELEX: {', '.join(overlap) if overlap else 'none'}.",
            f"- Families present here but absent in ZELEX today: {', '.join(whitespace) if whitespace else 'none'}.",
            f"- Families missing from this brand's accessible catalogue: {', '.join(missing) if missing else 'none'}.",
            "",
        ])

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    families = load_family_ranges()
    session = requests.Session()

    rows = load_zelex_baseline()
    for supplier in SUPPLIERS:
        rows.extend(scrape_supplier(supplier, session, families))
    rows.extend(scrape_irontech(session, families))
    rows.extend(scrape_tayu(session, families))
    realdoll_inventory = capture_realdoll_inventory(session)

    unavailable = list(UNAVAILABLE_COMPETITORS)
    if realdoll_inventory:
        unavailable.insert(
            0,
            {
                "brand": "RealDoll",
                "status": "inventory-only",
                "reason": "Model-line inventory captured, but body measurements are not consistently exposed for family classification.",
                "source_url": "https://www.realdoll.com/product-sitemap.xml",
            },
        )

    summary = build_summary(rows, unavailable, inventory_only=realdoll_inventory)
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_from": [
                    str(FAMILY_TAXONOMY.relative_to(ROOT)),
                    *[supplier.url for supplier in SUPPLIERS],
                    "https://www.tayu-doll.com/product-sitemap.xml",
                    "https://www.realdoll.com/product-sitemap.xml",
                ],
                "summary": summary,
                "rows": rows,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    write_csv(rows)
    write_sqlite(rows, summary)
    write_markdown(summary)

    print(
        f"Wrote {OUT_JSON.relative_to(ROOT)}, {OUT_SQLITE.relative_to(ROOT)}, {OUT_CSV.relative_to(ROOT)}, and {OUT_MD.relative_to(ROOT)} "
        f"for {summary['brand_count']} brands and {summary['row_count']} classified rows."
    )


if __name__ == "__main__":
    main()