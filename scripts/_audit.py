import json, re, sqlite3
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(ROOT/"db"/"catalog.db"); conn.row_factory = sqlite3.Row; cur = conn.cursor()

# ============================================================
# 1) CONTAMINATION AUDIT — products whose folder mixes >1 shoot
# ============================================================
print("="*64)
print("CONTAMINATION AUDIT — galleries that mix multiple shoots")
print("="*64)
def shoot_prefix(fn):
    return re.sub(r'-\d{2,4}.*$', '', fn or '')   # strip -NNN... → shoot id

rows = cur.execute("SELECT product_code, filename, rel_path FROM product_assets WHERE media_type='image'").fetchall()
byprod = {}
for r in rows:
    rp = (r["rel_path"] or "").lower()
    if "/heads/" in rp or "/specs/" in rp or "/measure" in rp: continue
    if not re.search(r'-\d{2,4}(?:[_.]|$)', r["filename"] or ""): continue  # skip non-photoshoot
    byprod.setdefault(r["product_code"], set()).add(shoot_prefix(r["filename"]))

# which products actually feed a live character (so we only care about visible ones)
chars = json.loads((ROOT/"db"/"characters.json").read_text(encoding="utf-8"))["characters"]
live_prod = {(c.get("photoshoot") or {}).get("product_code") for c in chars if c["status"]=="live"}

flagged = {pc: pre for pc, pre in byprod.items() if len(pre) > 1}
print(f"\nProducts whose folder mixes >1 shoot prefix: {len(flagged)} (of {len(byprod)})")
for pc in sorted(flagged):
    live = " <-- FEEDS A LIVE CHARACTER" if pc in live_prod else ""
    print(f"  {pc:30} prefixes={sorted(flagged[pc])}{live}")

print("\nOf those, the ones a visitor would actually SEE (live characters):")
seen = [pc for pc in flagged if pc in live_prod]
print(f"  {len(seen)}: {seen}")

# ============================================================
# 2) FAMILY-FIT — why Classic / Athlete / Sculpt are empty
# ============================================================
print("\n"+"="*64)
print("FAMILY FIT — every measured body vs the 7 family centers")
print("="*64)
FAMILIES = [
    ("The Classic", (0.68,0.72),(1.40,1.50)), ("The Icon",(0.60,0.65),(1.50,1.60)),
    ("The Muse",(0.65,0.70),(1.30,1.40)), ("The Siren",(0.55,0.60),(1.60,1.75)),
    ("The Athlete",(0.75,0.80),(1.30,1.35)), ("The Empress",(0.58,0.64),(1.55,1.65)),
    ("The Sculpt",(0.65,0.68),(1.45,1.55)),
]
ctr = lambda r:(r[0]+r[1])/2
prof = json.loads((ROOT/"db"/"body_profiles.json").read_text(encoding="utf-8"))["profiles"]
print(f"\nMeasured bodies: {len(prof)}")
print(f"{'body':9} {'WHR':>5} {'BWR':>5}  {'assigned':12} {'conf':9}  nearest Classic/Athlete/Sculpt distance")
from collections import Counter
famct = Counter()
for p in sorted(prof, key=lambda x:x['body_code']):
    whr,bwr = p['WHR'], p['BWR']; famct[p['family']]+=1
    def d(f): return abs(whr-ctr(f[1]))/0.05 + abs(bwr-ctr(f[2]))/0.10
    cas = {f[0]: round(d(f),2) for f in FAMILIES if f[0] in ("The Classic","The Athlete","The Sculpt")}
    print(f"{p['body_code']:9} {whr:>5.3f} {bwr:>5.3f}  {p['family']:12} {p['family_confidence']:9}  {cas}")

print("\nfamily counts:", dict(famct))

# unclassified bodies (no spec card → no WHR/BWR → no family)
classified = {p['body_code'] for p in prof}
all_char_bodies = {c['body_code'] for c in chars}
unclassified = sorted(all_char_bodies - classified)
print(f"\nUnclassified bodies (no spec card, family=null): {len(unclassified)}")
print(" ", unclassified)
conn.close()
