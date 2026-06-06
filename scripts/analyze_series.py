#!/usr/bin/env python3
"""Enumerate every Zelex product line present in the live catalog vs. what we hold."""
import json, re, sqlite3
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB   = ROOT / "db" / "catalog.db"
live = json.load(open(ROOT / "db" / "live_products.json", encoding="utf-8"))

HEAD_RE = re.compile(r'((?:GE|KE|ZFE|ZXE|ZE)\d+)_\d+')
BODY_RE = re.compile(r'\b(Z[A-Z]*\d{3}[A-Z])\b')

head_prefix = Counter()
body_prefix = Counter()
body_codes  = Counter()
no_code     = []

for p in live:
    skus   = [v.get("sku") or "" for v in p["variants"]]
    title  = p.get("title") or ""
    blob   = " ".join(skus) + " " + title
    hm = HEAD_RE.search(blob)
    bm = BODY_RE.findall(blob)
    if hm:
        head_prefix[hm.group(1)[:re.match(r'[A-Z]+', hm.group(1)).end()]] += 1
    bodies = set(bm)
    if bodies:
        for b in bodies:
            pre = re.match(r'Z[A-Z]*', b).group(0)
            body_prefix[pre] += 1
            body_codes[b] += 1
    if not hm and not bodies:
        no_code.append(title[:70])

print("=" * 68)
print(f"LIVE CATALOG: {len(live)} products")
print("=" * 68)
print("\nHEAD code prefixes (sculpt family):")
for k, n in head_prefix.most_common():
    print(f"  {k:6} {n}")
print("\nBODY code prefixes (body line):")
for k, n in body_prefix.most_common():
    print(f"  {k:6} {n}")

print("\nDistinct BODY codes seen live (prefix grouped):")
by_pre = defaultdict(list)
for b in body_codes:
    by_pre[re.match(r'Z[A-Z]*', b).group(0)].append(b)
for pre in sorted(by_pre):
    print(f"  {pre:5}: {', '.join(sorted(by_pre[pre]))}")

if no_code:
    print(f"\n{len(no_code)} live products with no decodable head/body code (heads-only, torsos, bundles):")
    for t in no_code[:12]:
        print(f"    - {t}")

# What we hold
conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
ours_body = set(r[0] for r in conn.execute("SELECT DISTINCT body_code FROM products WHERE body_code IS NOT NULL"))
ours_pre  = Counter(re.match(r'Z[A-Z]*', b).group(0) for b in ours_body)
print("\n" + "=" * 68)
print("WHAT WE HAVE CATALOGUED")
print("=" * 68)
print("Our body lines:", dict(ours_pre))
print("Our distinct body codes:", ", ".join(sorted(ours_body)))

print("\nBody codes LIVE but NOT in our catalog:")
missing = sorted(set(body_codes) - ours_body)
mby = defaultdict(list)
for b in missing:
    mby[re.match(r'Z[A-Z]*', b).group(0)].append(b)
for pre in sorted(mby):
    print(f"  {pre:5}: {', '.join(sorted(mby[pre]))}  ({sum(body_codes[b] for b in mby[pre])} live products)")
conn.close()
