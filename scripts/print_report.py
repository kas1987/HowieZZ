import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
with open(ROOT / 'db' / 'independent_competitor_report.json', encoding='utf-8') as f:
    r = json.load(f)

print('Sources:')
for s in r['sources']:
    print(f'  {s["name"]:<16} {s["product_count"]:>5} products  [{s["method"]}]')

print(f'\nTotals: {r["totals"]["raw_products"]} raw  /  {r["totals"]["full_body_rows"]} full-body  /  {r["totals"]["brands_found"]} brands')
print(f'Brands not found: {r["brands_not_found"]}')
print()
print(f'{"Brand":<22} {"Tier":<14} {"SKUs":>5} {"Priced":>6} {"Median":>8} {"Min":>7} {"Max":>7}  Heights')
print('-'*80)
for b in r['brands']:
    p = b['price']
    h = b['height']
    med = f'${p["median"]}' if p['median'] else '-'
    mn  = f'${p["min"]}'    if p['min']    else '-'
    mx  = f'${p["max"]}'    if p['max']    else '-'
    hs  = f'{h["min"]}-{h["max"]}cm' if h.get('min') else '-'
    print(f'{b["brand"]:<22} {b["tier"]:<14} {b["full_body_skus"]:>5} {p["count"]:>6} {med:>8} {mn:>7} {mx:>7}  {hs}')
