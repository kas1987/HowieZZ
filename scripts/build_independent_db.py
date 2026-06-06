"""
Build independent competitor database from web-scraped catalog data.
Sources: SiliconWives (Shopify API, 1731 products), FantasyWives (60 products)
Output: db/independent_competitor.sqlite + db/independent_competitor_report.json
"""

import json
import sqlite3
import re
import statistics
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRAPE_JSON = ROOT / 'db' / 'competitor_web_scrape.json'
SQLITE_OUT  = ROOT / 'db' / 'independent_competitor.sqlite'
REPORT_OUT  = ROOT / 'db' / 'independent_competitor_report.json'

# ── Brand normalisation map ───────────────────────────────────────────────────
# Maps raw vendor string → (canonical_brand, line/variant, tier)
BRAND_MAP = {
    'ZELEX Doll':           ('ZELEX', 'Inspiration', 'premium'),
    'ZELEX SLE':            ('ZELEX', 'SLE', 'mid'),
    'ZELEX ZFE':            ('ZELEX', 'ZFE', 'premium'),
    'Irontech Doll':        ('Irontech', 'full-body', 'mid'),
    'Irontech Doll Torso':  ('Irontech', 'torso', 'mid'),
    'WM Doll':              ('WM Doll', 'full-body', 'budget'),
    'WM Doll Torso':        ('WM Doll', 'torso', 'budget'),
    'WM Doll (Male)':       ('WM Doll', 'male', 'budget'),
    'Starpery Doll':        ('Starpery', 'full-body', 'mid'),
    'Starpery Torso':       ('Starpery', 'torso', 'mid'),
    'Jiusheng Doll':        ('Jiusheng', 'full-body', 'mid'),
    'SE Doll':              ('SE Doll', 'full-body', 'mid'),
    'Real Lady':            ('Real Lady', 'full-body', 'premium'),
    'Sanhui':               ('Sanhui', 'full-body', 'premium'),
    'Sino Doll':            ('Sino Doll', 'full-body', 'premium'),
    'Lusandy Doll':         ('Lusandy', 'full-body', 'mid'),
    'MD Doll':              ('MD Doll', 'full-body', 'mid'),
    'XT Doll':              ('XT Doll', 'full-body', 'mid'),
    'YL Doll':              ('YL Doll', 'full-body', 'mid'),
    'YL Doll (Male)':       ('YL Doll', 'male', 'mid'),
    'FunWest Doll':         ('FunWest', 'full-body', 'budget'),
    '6Ye Doll':             ('6Ye', 'full-body', 'budget'),
    '6Ye Torso':            ('6Ye', 'torso', 'budget'),
    'Angel Kiss':           ('Angel Kiss', 'full-body', 'budget'),
    'Dime Doll':            ('Dime Doll', 'full-body', 'budget'),
    'Top-CYDoll':           ('CY Doll', 'full-body', 'budget'),
    'LilyDoll':             ('LilyDoll', 'full-body', 'budget'),
    'Qita Doll':            ('Qita', 'full-body', 'mid'),
    'Qita Doll Torso':      ('Qita', 'torso', 'mid'),
    'SY Doll':              ('SY Doll', 'full-body', 'mid'),
    'Sigafun':              ('Sigafun', 'full-body', 'budget'),
    'Cyber Girl':           ('Cyber Girl', 'full-body', 'mid'),
    'Warm Doll':            ('Warm Doll', 'accessory', 'budget'),
    'AI Tech':              ('AI Tech', 'full-body', 'ultra-premium'),
    'Magic Moment Doll':    ('Magic Moment', 'full-body', 'mid'),
    'JM Doll':              ('JM Doll', 'full-body', 'mid'),
    'Arcana':               ('Arcana', 'full-body', 'mid'),
    'Silicon Wives':        ('Silicon Wives', 'house-brand', 'mixed'),
    'Silicon Wives Exclusive': ('Silicon Wives', 'exclusive', 'mid'),
    'FantasyWives':         ('FantasyWives', 'multi-brand', 'mixed'),
    'Route':                ('Route', 'accessory', 'budget'),
}

# Torso / accessory / male → exclude from full-body analysis
EXCLUDE_LINES = {'torso', 'accessory', 'male', 'house-brand', 'multi-brand'}

def clean_price(p):
    if p is None:
        return None
    if isinstance(p, (int, float)):
        return float(p) if p > 0 else None
    return None

def stats(values):
    v = [x for x in values if x is not None]
    if not v:
        return {'count': 0, 'median': None, 'mean': None, 'min': None, 'max': None, 'p25': None, 'p75': None}
    v.sort()
    n = len(v)
    p25 = v[max(0, int(n * 0.25) - 1)]
    p75 = v[min(n - 1, int(n * 0.75))]
    return {
        'count': n,
        'median': round(statistics.median(v)),
        'mean':   round(statistics.mean(v)),
        'min':    round(min(v)),
        'max':    round(max(v)),
        'p25':    round(p25),
        'p75':    round(p75),
    }

# ── Load scrape ───────────────────────────────────────────────────────────────
print("Loading scrape data...")
with open(SCRAPE_JSON, encoding='utf-8') as f:
    scrape = json.load(f)

products_raw = scrape['products']
print(f"  {len(products_raw)} raw products from {len(scrape['summary'])} sources")

# ── Normalise + clean ─────────────────────────────────────────────────────────
rows = []
skipped = 0
for p in products_raw:
    raw_brand = (p.get('brand') or '').strip()
    if not raw_brand:
        skipped += 1
        continue

    mapping = BRAND_MAP.get(raw_brand)
    if mapping:
        canonical, line, tier = mapping
    else:
        canonical, line, tier = raw_brand, 'unknown', 'unknown'

    price = clean_price(p.get('price_usd'))

    # Filter out obviously bad prices (accessories, $1 placeholder, >$20k)
    if price is not None and (price < 50 or price > 20000):
        price = None

    rows.append({
        'source':           p.get('source'),
        'source_url':       p.get('source_url'),
        'method':           p.get('method'),
        'raw_brand':        raw_brand,
        'brand':            canonical,
        'line':             line,
        'tier':             tier,
        'title':            p.get('title'),
        'handle':           p.get('handle'),
        'product_type':     p.get('product_type'),
        'price_usd':        price,
        'available':        p.get('available'),
        'height_cm':        p.get('height_cm'),
        'weight_kg':        p.get('weight_kg'),
        'bust_cm':          p.get('bust_cm'),
        'waist_cm':         p.get('waist_cm'),
        'hip_cm':           p.get('hip_cm'),
        'cup_size':         p.get('cup_size'),
        'tags':             json.dumps(p.get('tags') or []),
        'scraped_at':       scrape.get('scraped_at'),
    })

print(f"  {len(rows)} normalised rows ({skipped} skipped — no brand)")

# ── Full-body only subset (for market analysis) ───────────────────────────────
full_body = [r for r in rows if r['line'] not in EXCLUDE_LINES]
print(f"  {len(full_body)} full-body rows (torso/accessory/house excluded)")

# ── SQLite build ──────────────────────────────────────────────────────────────
print(f"\nBuilding SQLite: {SQLITE_OUT}")
SQLITE_OUT.unlink(missing_ok=True)
con = sqlite3.connect(SQLITE_OUT)
cur = con.cursor()

cur.executescript("""
CREATE TABLE products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source          TEXT,
    source_url      TEXT,
    method          TEXT,
    raw_brand       TEXT,
    brand           TEXT,
    line            TEXT,
    tier            TEXT,
    title           TEXT,
    handle          TEXT,
    product_type    TEXT,
    price_usd       REAL,
    available       INTEGER,
    height_cm       INTEGER,
    weight_kg       REAL,
    bust_cm         REAL,
    waist_cm        REAL,
    hip_cm          REAL,
    cup_size        TEXT,
    tags            TEXT,
    scraped_at      TEXT
);

CREATE INDEX idx_brand  ON products(brand);
CREATE INDEX idx_tier   ON products(tier);
CREATE INDEX idx_price  ON products(price_usd);
CREATE INDEX idx_height ON products(height_cm);

CREATE TABLE brand_summary (
    brand               TEXT PRIMARY KEY,
    tier                TEXT,
    lines               TEXT,
    total_skus          INTEGER,
    full_body_skus      INTEGER,
    priced_skus         INTEGER,
    price_median        REAL,
    price_mean          REAL,
    price_min           REAL,
    price_max           REAL,
    price_p25           REAL,
    price_p75           REAL,
    measured_skus       INTEGER,
    height_median       REAL,
    height_min          INTEGER,
    height_max          INTEGER,
    cup_sizes           TEXT,
    sources             TEXT,
    notes               TEXT
);
""")

cur.executemany("""
INSERT INTO products
(source, source_url, method, raw_brand, brand, line, tier, title, handle, product_type,
 price_usd, available, height_cm, weight_kg, bust_cm, waist_cm, hip_cm, cup_size, tags, scraped_at)
VALUES
(:source,:source_url,:method,:raw_brand,:brand,:line,:tier,:title,:handle,:product_type,
 :price_usd,:available,:height_cm,:weight_kg,:bust_cm,:waist_cm,:hip_cm,:cup_size,:tags,:scraped_at)
""", rows)

# ── Brand summaries ───────────────────────────────────────────────────────────
brand_groups = {}
for r in rows:
    b = r['brand']
    if b not in brand_groups:
        brand_groups[b] = []
    brand_groups[b].append(r)

brand_summary_rows = []
for brand, items in sorted(brand_groups.items()):
    fb_items   = [i for i in items if i['line'] not in EXCLUDE_LINES]
    prices     = [i['price_usd'] for i in fb_items if i['price_usd'] is not None]
    heights    = [i['height_cm'] for i in fb_items if i['height_cm'] is not None]
    cups       = sorted(set(i['cup_size'] for i in fb_items if i['cup_size']))
    tiers      = list(dict.fromkeys(i['tier'] for i in items))
    lines      = sorted(set(i['line'] for i in items))
    sources    = sorted(set(i['source'] for i in items))
    ps         = stats(prices)
    hs         = stats(heights)

    brand_summary_rows.append((
        brand,
        tiers[0] if tiers else 'unknown',
        json.dumps(lines),
        len(items),
        len(fb_items),
        ps['count'],
        ps['median'],
        ps['mean'],
        ps['min'],
        ps['max'],
        ps['p25'],
        ps['p75'],
        hs['count'],
        hs['median'],
        hs['min'],
        hs['max'],
        json.dumps(cups),
        json.dumps(sources),
        None,
    ))

cur.executemany("""
INSERT INTO brand_summary
(brand, tier, lines, total_skus, full_body_skus, priced_skus,
 price_median, price_mean, price_min, price_max, price_p25, price_p75,
 measured_skus, height_median, height_min, height_max, cup_sizes, sources, notes)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", brand_summary_rows)

con.commit()
con.close()
print(f"  SQLite written: {len(rows)} product rows, {len(brand_summary_rows)} brand rows")

# ── JSON report ───────────────────────────────────────────────────────────────
print(f"\nBuilding JSON report: {REPORT_OUT}")

# Full-body brands only, sorted by median price desc
fb_brand_map = {}
for r in full_body:
    b = r['brand']
    if b not in fb_brand_map:
        fb_brand_map[b] = []
    fb_brand_map[b].append(r)

brand_report = []
for brand, items in fb_brand_map.items():
    prices  = [i['price_usd'] for i in items if i['price_usd'] is not None]
    heights = [i['height_cm'] for i in items if i['height_cm'] is not None]
    cups    = sorted(set(i['cup_size'] for i in items if i['cup_size']))
    tiers   = list(dict.fromkeys(i['tier'] for i in items))
    ps      = stats(prices)
    hs      = stats(heights)

    brand_report.append({
        'brand':            brand,
        'tier':             tiers[0] if tiers else 'unknown',
        'full_body_skus':   len(items),
        'price':            ps,
        'height':           hs,
        'cup_sizes':        cups,
        'sources':          sorted(set(i['source'] for i in items)),
    })

brand_report.sort(key=lambda x: x['price']['median'] or 0, reverse=True)

# Identify gaps vs prior DB
prior_brands = ['Gynoid', 'Tayu', 'Game Lady', 'Doll Forever', 'JK Doll']
found_brands = {b['brand'] for b in brand_report}
gaps = [b for b in prior_brands if b not in found_brands]

report = {
    'generated_at':         scrape['scraped_at'],
    'sources': [
        {'name': s['source'], 'product_count': s['product_count'],
         'priced_count': s['priced_count'], 'method': s['method']}
        for s in scrape['summary']
    ],
    'totals': {
        'raw_products':     len(products_raw),
        'normalised_rows':  len(rows),
        'full_body_rows':   len(full_body),
        'brands_found':     len(brand_report),
    },
    'brands_not_found':     gaps,
    'brands':               brand_report,
}

with open(REPORT_OUT, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"  JSON report written")

# ── Console summary ───────────────────────────────────────────────────────────
print("\n" + "═"*80)
print("INDEPENDENT COMPETITOR DB — BRAND SUMMARY (full-body, sorted by median price)")
print("═"*80)
print(f"{'Brand':<22} {'Tier':<14} {'SKUs':>5} {'$N':>4} {'Median':>8} {'Min':>7} {'Max':>7}  Heights")
print("-"*80)
for b in brand_report:
    p = b['price']
    h = b['height']
    med_str = f"${p['median']}" if p['median'] else "—"
    min_str = f"${p['min']}"   if p['min']    else "—"
    max_str = f"${p['max']}"   if p['max']    else "—"
    hs_str  = f"{h['min']}–{h['max']} cm" if h['min'] else "—"
    print(f"{b['brand']:<22} {b['tier']:<14} {b['full_body_skus']:>5} {p['count']:>4} {med_str:>8} {min_str:>7} {max_str:>7}  {hs_str}")

print()
print(f"Brands NOT found (gap vs prior taxonomy DB): {', '.join(gaps) if gaps else 'none'}")
print(f"\nOutput files:")
print(f"  {SQLITE_OUT}")
print(f"  {REPORT_OUT}")
