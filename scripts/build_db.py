#!/usr/bin/env python3
"""
HowieZZ Catalog Builder
Scans asset folders, populates SQLite catalog, exports catalog.json
and per-product JSON files for front-end use.

Usage:
    python scripts/build_db.py           # incremental (INSERT OR REPLACE)
    python scripts/build_db.py --reset   # drop tables and rebuild from scratch
"""

import sqlite3
import json
import re
import sys
from pathlib import Path

ROOT    = Path(__file__).resolve().parent.parent
ASSETS  = ROOT / "assets"
DB_DIR  = ROOT / "db"
DB_PATH = DB_DIR / "catalog.db"
JSON_PATH = DB_DIR / "catalog.json"
MEAS_PATH = DB_DIR / "body_measurements.json"
OVERRIDES_PATH = DB_DIR / "product_overrides.json"   # from fetch_catalog.py (optional)
VARIANTS_PATH  = DB_DIR / "live_variants.json"        # from fetch_catalog.py (optional)
DATA_DIR  = ASSETS / "data"

def _load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        print(f"  [warn] could not parse {path.name}; ignoring")
        return default

RESET = "--reset" in sys.argv

# Body measurements (transcribed spec cards) + alias map for source typos
_meas_raw   = json.loads(MEAS_PATH.read_text(encoding='utf-8'))
MEASUREMENTS = _meas_raw["bodies"]
BODY_ALIASES = _meas_raw.get("_aliases", {})

def canon_body(code):
    """Resolve a raw body code to its canonical form (typo aliases)."""
    if not code:
        return code
    return BODY_ALIASES.get(code, code)

# ── Schema ────────────────────────────────────────────────────────────────────

SCHEMA_PATH = DB_DIR / "schema.sql"

DROP_SQL = """
PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS product_variants;
DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS product_assets;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS head_images;
DROP TABLE IF EXISTS heads;
DROP TABLE IF EXISTS body_specs;
DROP TABLE IF EXISTS bodies;
DROP TABLE IF EXISTS series;
PRAGMA foreign_keys = ON;
"""

# ── Parsing helpers ───────────────────────────────────────────────────────────

def parse_i_folder(name):
    """
    GE149_1_GE74MJ_ZG170D → head=GE149_1, face=GE74MJ, body=ZG170D, shoot=None
    GE52_1                → head=GE52_1,  face=None,   body=None,   shoot=None
    """
    head = re.match(r'(GE\d+_\d+)', name)
    face = re.search(r'_(GE\d+MJ)', name)
    body = re.search(r'_(Z[A-Z]*\d+[A-Z])\b', name)
    shoot = re.search(r'-(\d+)$', name)
    return (head.group(1) if head else None,
            face.group(1) if face else None,
            body.group(1) if body else None,
            int(shoot.group(1)) if shoot else None)

def parse_k_folder(name):
    """KE03_1+ZK168B-1 → head=KE03_1, face=None, body=ZK168B, shoot=1"""
    head = re.match(r'(KE\d+_\d+)', name)
    body = re.search(r'\+(ZK\d+[A-Z])', name)
    shoot = re.search(r'-(\d+)$', name)
    return (head.group(1) if head else None,
            None,
            body.group(1) if body else None,
            int(shoot.group(1)) if shoot else None)

def parse_fusion_folder(name):
    """ZFE01_1+ZF168B → head=ZFE01_1, face=None, body=ZF168B, shoot=None"""
    head = re.match(r'(ZFE\d+_\d+)', name)
    body = re.search(r'\+(ZF\d+[A-Z])', name)
    shoot = re.search(r'-(\d+)$', name)
    return (head.group(1) if head else None,
            None,
            body.group(1) if body else None,
            int(shoot.group(1)) if shoot else None)

def parse_sle_folder(name):
    """
    ZXE200_1_ZX166K           → head=ZXE200_1,  body=ZX166K
    ZX201_2_ZX172E            → head=ZX201_2,   body=ZX172E   (some heads are ZX, not ZXE)
    ZXE200_W1_ZX171C          → head=ZXE200_W1, body=ZX171C   (letter-prefixed version)
    ZXE201_1_ZX84J            → head=ZXE201_1,  body=ZX84J    (2-digit torso body)
    ZXE200_1+ZX165D-Tan-Sle3.0→ head=ZXE200_1,  body=ZX165D
    """
    head = re.match(r'(ZXE?\d+_[A-Z]?\d+)', name)
    body = re.search(r'[_+](ZX\d{2,3}[A-Z])(?=[-_+.]|$)', name)
    shoot = re.search(r'-(\d+)$', name)
    return (head.group(1) if head else None,
            None,
            body.group(1) if body else None,
            int(shoot.group(1)) if shoot else None)

def decode_body(code):
    """ZGX165F → (line='ZGX', height=165, cup='F'). Returns (None,None,None) on miss."""
    m = re.match(r'(Z[A-Z]*?)(\d{2,3})([A-Z])$', code)
    if not m:
        return None, None, None
    return m.group(1), int(m.group(2)), m.group(3)

def parse_head_filename(filename):
    """
    GE03_2 (GE70MJ)-Fair-2.png → (GE03_2, GE70MJ, Fair, 2)
    GE82_1(GE47MJ)-Fair.png    → (GE82_1, GE47MJ, Fair, 1)
    GE45_8-Fair.jpg            → (GE45_8, None,   Fair, 1)
    GE02-1(GE46MJ)-Tan.png     → (GE02_1, GE46MJ, Tan,  1)  [hyphen variant]
    """
    stem = Path(filename).stem
    m = re.match(r'(GE\d+)[_-](\d+)\s*(?:\((GE\d+MJ)\))?[-\s]*(Fair|Tan)(?:-(\d+))?', stem, re.I)
    if m:
        head = f"{m.group(1)}_{m.group(2)}"
        return head, m.group(3), m.group(4).capitalize(), int(m.group(5) or 1)
    return None, None, None, None

def parse_body_spec(filename):
    """
    ZG162D.webp         → ZG162D
    ZG170C-cm-pc.webp   → ZG170C
    spec-zk159d.webp    → ZK159D
    ZX160J_pc_3.0.webp  → ZX160J
    """
    stem = Path(filename).stem.upper()
    m = re.match(r'SPEC-([A-Z0-9]+)', stem)
    if m: return m.group(1)
    m = re.match(r'(Z[GXFK]+\d+[A-Z]+)', stem)
    if m: return m.group(1)
    return None

def parse_option(filename):
    """1#-Hard Hand.jpg → (1#, Hard Hand)"""
    stem = Path(filename).stem
    m = re.match(r'(\d+[#.]\d*#?)\s*[-\s]*(.*)', stem)
    if m:
        return m.group(1).strip(), m.group(2).strip() or None
    return stem, None

def seq(filename):
    """Extract sequence number from -NNN pattern."""
    m = re.search(r'-(\d{3})\b', filename)
    return int(m.group(1)) if m else None

def body_series(code):
    if code.startswith('ZK'):  return 'K'
    if code.startswith('ZF'):  return 'Fusion'
    if code.startswith('ZX'):  return 'SLE'
    return 'I'   # ZG / ZGX

# ── Build ─────────────────────────────────────────────────────────────────────

def build():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur  = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    if RESET:
        cur.executescript(DROP_SQL)
        conn.commit()
        print("Tables dropped.")

    cur.executescript(SCHEMA_PATH.read_text())
    conn.commit()

    # Optional live-store reconciliation data (produced by scripts/fetch_catalog.py)
    OVERRIDES = _load_json(OVERRIDES_PATH, {})
    if OVERRIDES:
        print(f"Loaded {len(OVERRIDES)} live-store overrides")

    # ── Series ────────────────────────────────────────────────────────────────
    cur.executemany(
        "INSERT OR IGNORE INTO series(id,name,folder) VALUES(?,?,?)",
        [('I',      'I-Series',      'I-Series'),
         ('K',      'K-Series',      'K-Series'),
         ('Fusion', 'Fusion Series', 'Fusion-Series'),
         ('SLE',    'SLE Series',    'SLE-Series')]
    )
    conn.commit()

    # ── Bodies (decode code → line/height/cup, attach spec + measurements) ──────
    bodies_seen = set()

    def ensure_body(code, series_id, spec_rel=None):
        """Insert-or-update a body row with decoded fields, spec image, measurements."""
        if not code:
            return
        line, height, cup = decode_body(code)
        meas = MEASUREMENTS.get(code)
        line_label = meas["line"] if meas else (
            'K-Series' if line == 'ZK' else
            'Fusion'   if line == 'ZF' else
            'SLE 3.0'  if line == 'ZX' else
            'I-Series' if line in ('ZG', 'ZGX') else None)
        if meas:
            cup = meas.get("cup", cup)
            height = meas.get("nominal_height", height)
        has_specs = 1 if meas else 0
        cur.execute("""
            INSERT INTO bodies(code,series_id,body_line,line_label,height_cm,cup_size,spec_image,has_specs)
            VALUES(?,?,?,?,?,?,?,?)
            ON CONFLICT(code) DO UPDATE SET
                body_line  = COALESCE(excluded.body_line,  bodies.body_line),
                line_label = COALESCE(excluded.line_label, bodies.line_label),
                height_cm  = COALESCE(excluded.height_cm,  bodies.height_cm),
                cup_size   = COALESCE(excluded.cup_size,   bodies.cup_size),
                spec_image = COALESCE(excluded.spec_image, bodies.spec_image),
                has_specs  = MAX(bodies.has_specs, excluded.has_specs)
        """, (code, series_id, line, line_label, height, cup, spec_rel, has_specs))

        if meas and code not in bodies_seen:
            cur.execute("""
                INSERT OR REPLACE INTO body_measurements(
                    body_code,cup,upper_bust,under_bust,waist,hip,neck,shoulder_width,
                    arm_length,hand_length,leg_length,foot_length,thigh_circ,calf_circ,
                    body_height,head_body_height,weight_kg,spec_label)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (code, meas.get("cup"), meas.get("upper_bust"), meas.get("under_bust"),
                  meas.get("waist"), meas.get("hip"), meas.get("neck"), meas.get("shoulder_width"),
                  meas.get("arm_length"), meas.get("hand_length"), meas.get("leg_length"),
                  meas.get("foot_length"), meas.get("thigh_circ"), meas.get("calf_circ"),
                  meas.get("body_height"), meas.get("head_body_height"), meas.get("weight_kg"),
                  meas.get("spec_label")))
        bodies_seen.add(code)

    spec_count = 0
    for d in (ASSETS / "Measure", ASSETS / "Z-Series", ASSETS / "Fusion-Series" / "specs"):
        if not d.exists(): continue
        for f in d.iterdir():
            if f.suffix.lower() not in ('.webp', '.jpg', '.png'): continue
            code = parse_body_spec(f.name)
            if not code: continue
            rel  = f.relative_to(ASSETS).as_posix()
            sid  = body_series(code)
            cur.execute("INSERT OR REPLACE INTO body_specs(body_code,filename,rel_path) VALUES(?,?,?)",
                        (code, f.name, rel))
            ensure_body(code, sid, rel)
            spec_count += 1
    # Bodies that have measurements but no spec-card file under Measure/ (e.g. Fusion)
    for code, m in MEASUREMENTS.items():
        if code not in bodies_seen:
            ensure_body(code, body_series(code))
    conn.commit()
    n_meas = cur.execute("SELECT COUNT(*) FROM body_measurements").fetchone()[0]
    print(f"Body specs: {spec_count} cards, {n_meas} measurement sets")

    # ── Head reference images ─────────────────────────────────────────────────
    heads_seen = set()
    head_img_n = 0
    heads_dir  = ASSETS / "Heads"
    if heads_dir.exists():
        for subdir in heads_dir.iterdir():
            if not subdir.is_dir(): continue
            htype = subdir.name   # Hard / Soft
            for f in subdir.iterdir():
                if f.suffix.lower() not in ('.jpg', '.jpeg', '.png'): continue
                code, face, tone, variant = parse_head_filename(f.name)
                if not code: continue
                rel = f.relative_to(ASSETS).as_posix()
                if code not in heads_seen:
                    cur.execute("INSERT OR IGNORE INTO heads(code,series_id,head_type) VALUES(?,?,?)",
                                (code, 'I', htype))
                    heads_seen.add(code)
                cur.execute("INSERT INTO head_images(head_code,face_code,skin_tone,variant,filename,rel_path) VALUES(?,?,?,?,?,?)",
                            (code, face, tone, variant, f.name, rel))
                head_img_n += 1
    conn.commit()
    print(f"Head images: {head_img_n} across {len(heads_seen)} heads")

    # ── Customization options ─────────────────────────────────────────────────
    opt_n = 0
    opts_dir = ASSETS / "Options"
    if opts_dir.exists():
        for group_dir in opts_dir.iterdir():   # Body Options / Head Options
            if not group_dir.is_dir(): continue
            for cat_dir in group_dir.iterdir():
                if not cat_dir.is_dir(): continue
                for f in cat_dir.iterdir():
                    if f.suffix.lower() not in ('.jpg', '.jpeg', '.png'): continue
                    key, label = parse_option(f.name)
                    rel = f.relative_to(ASSETS).as_posix()
                    cur.execute(
                        "INSERT INTO options(group_type,category,option_key,label,filename,rel_path) VALUES(?,?,?,?,?,?)",
                        (group_dir.name, cat_dir.name, key, label, f.name, rel)
                    )
                    opt_n += 1
    conn.commit()
    print(f"Options: {opt_n}")

    # ── Products & assets ─────────────────────────────────────────────────────
    SKIP_FOLDERS = {'OpenArt', 'specs', 'videos', 'source', 'misc', 'Characters', 'data'}

    def is_dup_cover(name):
        # UUID-duplicate cover-image folders created during download (canonical
        # underscore-stem folder holds the same shots without the UUID suffix)
        return bool(re.search(r'Sle\d', name, re.I))

    def scan_series(series_id, series_dir, parse_fn):
        if not series_dir.exists():
            print(f"  [skip] {series_dir.name} — not found"); return 0, 0
        prod_n = asset_n = 0
        for folder in sorted(series_dir.iterdir()):
            if not folder.is_dir(): continue
            if folder.name in SKIP_FOLDERS: continue
            if is_dup_cover(folder.name): continue
            head_code, face_code, raw_body, photoshoot = parse_fn(folder.name)
            body_code = canon_body(raw_body)   # resolve typo aliases (e.g. ZGE175E→ZG175E)
            body_source = 'folder' if body_code else None

            # Apply live-store override (fill-only: never overwrite folder-derived codes)
            ov = OVERRIDES.get(folder.name, {})
            if not body_code and ov.get("body_code"):
                body_code = canon_body(ov["body_code"])
                body_source = 'live'
            if not face_code and ov.get("face_code"):
                face_code = ov["face_code"]
            live_handle = ov.get("live_handle")
            live_title  = ov.get("live_title")
            price       = ov.get("price")

            if head_code and head_code not in heads_seen:
                cur.execute("INSERT OR IGNORE INTO heads(code,series_id) VALUES(?,?)",
                            (head_code, series_id))
                heads_seen.add(head_code)

            if body_code:
                ensure_body(body_code, series_id)

            imgs   = sorted(f for f in folder.iterdir() if f.suffix.lower() in ('.jpg','.jpeg','.png','.webp'))
            videos = sorted(f for f in folder.iterdir() if f.suffix.lower() == '.mp4')

            rel_folder = folder.relative_to(ASSETS).as_posix()
            cur.execute(
                "INSERT OR REPLACE INTO products(code,head_code,face_code,body_code,raw_body,photoshoot,series_id,folder_path,image_count,video_count,live_handle,live_title,price,body_source) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (folder.name, head_code, face_code, body_code, raw_body, photoshoot, series_id, rel_folder, len(imgs), len(videos), live_handle, live_title, price, body_source)
            )
            prod_n += 1

            for f in imgs:
                cur.execute("INSERT INTO product_assets(product_code,filename,sequence,media_type,rel_path) VALUES(?,?,?,?,?)",
                            (folder.name, f.name, seq(f.name), 'image', f.relative_to(ASSETS).as_posix()))
                asset_n += 1
            for f in videos:
                cur.execute("INSERT INTO product_assets(product_code,filename,sequence,media_type,rel_path) VALUES(?,?,?,?,?)",
                            (folder.name, f.name, seq(f.name), 'video', f.relative_to(ASSETS).as_posix()))
                asset_n += 1
        return prod_n, asset_n

    total_prod = total_asset = 0
    for sid, sdir, pfn in [
        ('I',      ASSETS / "I-Series",      parse_i_folder),
        ('K',      ASSETS / "K-Series",      parse_k_folder),
        ('Fusion', ASSETS / "Fusion-Series", parse_fusion_folder),
        ('SLE',    ASSETS / "SLE-Series",    parse_sle_folder),
    ]:
        p, a = scan_series(sid, sdir, pfn)
        print(f"  {sid}: {p} products, {a} assets")
        total_prod += p; total_asset += a

    conn.commit()
    print(f"Products: {total_prod} total, {total_asset} assets")

    # ── Standalone videos (MP4/) ──────────────────────────────────────────────
    mp4_dir = ASSETS / "MP4"
    vid_n = 0
    if mp4_dir.exists():
        for f in sorted(mp4_dir.iterdir()):
            if f.suffix.lower() == '.mp4':
                cur.execute("INSERT OR IGNORE INTO videos(series_id,filename,rel_path) VALUES(?,?,?)",
                            ('I', f.name, f.relative_to(ASSETS).as_posix()))
                vid_n += 1
    conn.commit()
    print(f"Standalone videos: {vid_n}")

    # ── Live variants (pricing + options) ──────────────────────────────────────
    variants = _load_json(VARIANTS_PATH, [])
    if variants:
        # Map live_handle -> our product code (from overrides) to link variants back
        handle_to_code = {ov["live_handle"]: code
                          for code, ov in OVERRIDES.items() if ov.get("live_handle")}
        vn = 0
        for v in variants:
            sku = v.get("sku")
            if not sku:
                continue
            code = handle_to_code.get(v.get("handle"))
            cur.execute("""
                INSERT OR REPLACE INTO product_variants(
                    sku,product_code,live_handle,head_code,face_code,body_code,
                    skin_tone,price,compare_at_price,option1,option2,option3,title)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (sku, code, v.get("handle"), v.get("head"), v.get("face"),
                  canon_body(v.get("body")), v.get("tone"), v.get("price"),
                  v.get("compare_at_price"), v.get("option1"), v.get("option2"),
                  v.get("option3"), v.get("product_title")))
            vn += 1
        conn.commit()
        linked = cur.execute("SELECT COUNT(*) FROM product_variants WHERE product_code IS NOT NULL").fetchone()[0]
        print(f"Live variants: {vn} SKUs ({linked} linked to local products)")

    export_json(conn)
    conn.close()
    print(f"\nDatabase : {DB_PATH}")
    print(f"JSON     : {JSON_PATH}")
    print("Done.")


# ── JSON export ───────────────────────────────────────────────────────────────

def export_json(conn):
    cur = conn.cursor()

    def rows(sql, *args):
        return [dict(r) for r in cur.execute(sql, args)]

    catalog = {
        "series":    rows("SELECT * FROM series ORDER BY id"),
        "products":  rows("""
            SELECT p.code, p.head_code, p.face_code, p.body_code, p.raw_body,
                   p.photoshoot, p.series_id, p.folder_path,
                   p.image_count, p.video_count,
                   b.height_cm, b.cup_size, b.line_label AS body_line,
                   pa.rel_path AS cover_image
            FROM products p
            LEFT JOIN bodies b ON b.code = p.body_code
            LEFT JOIN product_assets pa
              ON pa.product_code = p.code
             AND pa.media_type   = 'image'
             AND pa.sequence     = (
                     SELECT MIN(sequence)
                     FROM product_assets
                     WHERE product_code = p.code AND media_type = 'image'
                 )
            ORDER BY p.series_id, p.code
        """),
        "heads":     rows("""
            SELECT h.code, h.series_id, h.head_type,
                   hi.face_code, hi.rel_path AS reference_image, hi.skin_tone
            FROM heads h
            LEFT JOIN head_images hi
              ON hi.head_code = h.code AND hi.skin_tone = 'Fair' AND hi.variant = 1
            ORDER BY h.series_id, h.code
        """),
        "bodies":    rows("""
            SELECT b.code, b.series_id, b.body_line, b.line_label,
                   b.height_cm, b.cup_size, b.has_specs,
                   bs.rel_path AS spec_image,
                   m.upper_bust, m.under_bust, m.waist, m.hip,
                   m.body_height, m.head_body_height, m.weight_kg, m.spec_label
            FROM bodies b
            LEFT JOIN body_specs bs ON bs.body_code = b.code
            LEFT JOIN body_measurements m ON m.body_code = b.code
            ORDER BY b.series_id, b.code
        """),
        "options_summary": rows("""
            SELECT group_type, category, COUNT(*) AS option_count
            FROM options GROUP BY group_type, category ORDER BY group_type, category
        """),
        "videos":    rows("SELECT * FROM videos"),
    }

    JSON_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding='utf-8')

    # Per-product detail JSON for front-end lazy loading
    # Use a separate cursor so the inner query doesn't interrupt the outer loop
    cur2 = conn.cursor()
    cur2.row_factory = sqlite3.Row
    product_codes = [r[0] for r in cur.execute("SELECT code FROM products")]
    for code in product_codes:
        assets = [dict(r) for r in cur2.execute(
            "SELECT filename,sequence,media_type,rel_path FROM product_assets WHERE product_code=? ORDER BY media_type,sequence",
            (code,)
        )]
        (DATA_DIR / f"{code}.json").write_text(
            json.dumps({"code": code, "assets": assets}, indent=2), encoding='utf-8'
        )

    totals = {k: len(v) for k, v in catalog.items()}
    print(f"JSON export: {totals}")


if __name__ == "__main__":
    build()
