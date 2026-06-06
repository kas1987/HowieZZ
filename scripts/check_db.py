#!/usr/bin/env python3
"""Reconciliation report for the HowieZZ catalog."""
import sqlite3
from pathlib import Path

DB = Path(__file__).parent.parent / "db" / "catalog.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def q(sql, *a): return cur.execute(sql, a).fetchall()

print("=" * 70)
print("BODY CATALOG — decoded code grammar  {LINE}{HEIGHT}{CUP}")
print("=" * 70)
print(f"{'code':<10}{'line':<10}{'H(cm)':<7}{'cup':<5}{'specs':<7}{'weight':<8}{'spec card'}")
for r in q("SELECT b.code,b.line_label,b.height_cm,b.cup_size,b.has_specs,m.weight_kg,b.spec_image FROM bodies b LEFT JOIN body_measurements m ON m.body_code=b.code ORDER BY b.line_label,b.height_cm"):
    card = 'yes' if r['spec_image'] else '—'
    w = f"{r['weight_kg']}kg" if r['weight_kg'] else '—'
    print(f"{r['code']:<10}{(r['line_label'] or '?'):<10}{str(r['height_cm'] or '?'):<7}{(r['cup_size'] or '?'):<5}{('full' if r['has_specs'] else 'partial'):<7}{w:<8}{card}")

print()
print("=" * 70)
print("PRODUCT -> HEAD / FACE / BODY reconciliation")
print("=" * 70)
total = q("SELECT COUNT(*) c FROM products")[0]['c']
with_body = q("SELECT COUNT(*) c FROM products WHERE body_code IS NOT NULL")[0]['c']
with_face = q("SELECT COUNT(*) c FROM products WHERE face_code IS NOT NULL")[0]['c']
with_shoot = q("SELECT COUNT(*) c FROM products WHERE photoshoot IS NOT NULL")[0]['c']
body_specd = q("SELECT COUNT(*) c FROM products p JOIN bodies b ON b.code=p.body_code WHERE b.has_specs=1")[0]['c']
print(f"  {total} products")
print(f"  {with_body} have a body code  ({body_specd} of those map to a full spec card)")
print(f"  {with_face} have a face/makeup (MJ) code")
print(f"  {with_shoot} have a photoshoot suffix (-1/-2 = same head+body, diff shoot)")

print()
print("  Products grouped by head+body (multiple rows = multiple photoshoots):")
for r in q("""SELECT head_code, body_code, COUNT(*) n, GROUP_CONCAT(photoshoot) shoots
              FROM products WHERE photoshoot IS NOT NULL
              GROUP BY head_code, body_code HAVING n>1 ORDER BY head_code"""):
    print(f"    {r['head_code']} + {r['body_code']}: {r['n']} shoots ({r['shoots']})")

print()
print("=" * 70)
print("SAMPLE: fully-decoded I-series products")
print("=" * 70)
print(f"{'product folder':<28}{'head':<10}{'face':<9}{'body':<9}{'H':<5}{'cup'}")
for r in q("""SELECT p.code,p.head_code,p.face_code,p.body_code,b.height_cm,b.cup_size
              FROM products p LEFT JOIN bodies b ON b.code=p.body_code
              WHERE p.series_id='I' AND p.face_code IS NOT NULL ORDER BY p.code LIMIT 8"""):
    print(f"{r['code']:<28}{(r['head_code'] or '—'):<10}{(r['face_code'] or '—'):<9}{(r['body_code'] or '—'):<9}{str(r['height_cm'] or '—'):<5}{r['cup_size'] or '—'}")

print()
print("=" * 70)
print("LIVE-STORE RECONCILIATION (from fetch_catalog.py)")
print("=" * 70)
by_src = {r['body_source'] or 'none': r['n'] for r in q("SELECT body_source, COUNT(*) n FROM products GROUP BY body_source")}
print(f"  body code source:  folder={by_src.get('folder',0)}  live-backfilled={by_src.get('live',0)}  none={by_src.get('none',0)}")
linked = q("SELECT COUNT(*) c FROM products WHERE live_handle IS NOT NULL")[0]['c']
priced = q("SELECT COUNT(*) c FROM products WHERE price IS NOT NULL")[0]['c']
print(f"  {linked}/77 products linked to a live zelexdoll.com listing; {priced} have a price")
if q("SELECT COUNT(*) c FROM product_variants")[0]['c']:
    nv = q("SELECT COUNT(*) c FROM product_variants")[0]['c']
    nl = q("SELECT COUNT(*) c FROM product_variants WHERE product_code IS NOT NULL")[0]['c']
    print(f"  product_variants: {nv} live SKUs ({nl} linked to our folders)")
    print("  price range (linked products):")
    for r in q("""SELECT series_id, MIN(CAST(price AS REAL)) lo, MAX(CAST(price AS REAL)) hi
                  FROM products WHERE price IS NOT NULL GROUP BY series_id"""):
        print(f"    {r['series_id']}: ${r['lo']:.0f} - ${r['hi']:.0f}")

print()
print("=" * 70)
print("GAPS / things to resolve")
print("=" * 70)
# bodies referenced by products but no spec card
g = q("""SELECT DISTINCT p.body_code FROM products p JOIN bodies b ON b.code=p.body_code
         WHERE b.has_specs=0 AND p.body_code IS NOT NULL ORDER BY p.body_code""")
if g:
    print("  Body codes in use without a full spec card:")
    for r in g: print(f"    {r['body_code']}")
# I-series products with no body code (older naming)
n_nobody = q("SELECT COUNT(*) c FROM products WHERE body_code IS NULL AND series_id='I'")[0]['c']
print(f"  {n_nobody} I-series products have no body code in their folder name (older slug format)")
# heads with no reference image
nh = q("SELECT COUNT(*) c FROM heads WHERE code NOT IN (SELECT DISTINCT head_code FROM head_images)")[0]['c']
print(f"  {nh} heads have no reference image (K/Fusion heads + I heads not in Head List)")

conn.close()
