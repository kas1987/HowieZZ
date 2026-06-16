import json, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
with open(ROOT / 'db' / 'competitor_web_scrape.json', encoding='utf-8') as f:
    d = json.load(f)

brands = {}
for p in d['products']:
    b = (p.get('brand') or '').strip()
    if not b:
        continue
    if b not in brands:
        brands[b] = {'count': 0, 'prices': [], 'heights': [], 'cups': set(), 'types': set()}
    brands[b]['count'] += 1
    if p.get('price_usd'):
        brands[b]['prices'].append(p['price_usd'])
    if p.get('height_cm'):
        brands[b]['heights'].append(p['height_cm'])
    if p.get('cup_size'):
        brands[b]['cups'].add(p['cup_size'])
    if p.get('product_type'):
        brands[b]['types'].add(p['product_type'])

print(f"Total brands: {len(brands)}")
print(f"Total products: {len(d['products'])}")
print()
print(f"{'Brand':<30} {'N':>5} {'$N':>5} {'Median':>8} {'Min':>7} {'Max':>7}  Heights")
print('-' * 85)
for b, v in sorted(brands.items()):
    n = v['count']
    prices = sorted(v['prices'])
    med = round(statistics.median(prices)) if prices else None
    mn = round(min(prices)) if prices else None
    mx = round(max(prices)) if prices else None
    hs = sorted(set(v['heights']))[:6]
    hstr = ', '.join(str(h) for h in hs)
    med_str = f"${med}" if med else ""
    mn_str  = f"${mn}"  if mn  else ""
    mx_str  = f"${mx}"  if mx  else ""
    print(f"{b:<30} {n:>5} {len(prices):>5} {med_str:>8} {mn_str:>7} {mx_str:>7}  {hstr}")
