#!/usr/bin/env python3
"""
Build the 108-character layer: 4 characters per body type per series.

Rules (per design decisions):
  - The 4 characters on a body differ by HEAD/FACE (real distinct photoshoots).
  - Bodies with <4 photographed heads: empty slots become PLACEHOLDERS that
    BORROW a sibling photoshoot on the same body (flagged representative_only).
  - Bodies with >4 heads: 4 are curated as characters; the surplus is parked in
    the body type's additional_photoshoots pool (never lost).
  - Persona identity is AUTO-GENERATED in the brief's voice, then overridable via
    db/character_overlay.json (keyed by character_id).

Inputs : catalog.db, db/body_profiles.json, db/character_profiles.json (lead titles)
Outputs: db/characters.json, db/body_types.json, tables characters + body_type_pool
Run after build_db.py + build_profiles.py.  Then run make_thumbs.py.
"""
import json, re, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB   = ROOT / "db" / "catalog.db"
BODY_PROFILES = ROOT / "db" / "body_profiles.json"
LEAD_PERSONAS = ROOT / "db" / "character_profiles.json"   # body-level lead titles
OVERLAY       = ROOT / "db" / "character_overlay.json"    # per-character hand edits
STORIES       = ROOT / "db" / "character_stories.json"    # per-character narrative story/profile
OUT_CHARS = ROOT / "db" / "characters.json"
OUT_BODIES = ROOT / "db" / "body_types.json"

# ── Torso bodies — EXCLUDED from the character catalog (no head, torso-only imagery).
# Confirmed via live Shopify titles ("SLE Sex Doll Torso — No Head"). All are short-stature.
TORSO_CODES = {"ZX84J", "ZX85G", "ZX86K", "ZX91E", "ZX108J", "ZX109G", "ZX111K", "ZX117E"}
def is_torso(code, height_cm):
    """A body is torso-only if it's on the known list or shorter than any real standing body (153cm)."""
    return code in TORSO_CODES or (height_cm is not None and height_cm < 150)

# Only REAL PHOTOSHOOT frames are eligible for hero/gallery — files named "…-101, -102, …".
# This excludes FACTORY/STOCK imagery that is "just an image, not a photoshoot": plain
# head-catalog shots (assets/Heads/…-Fair.png), spec/measure cards (assets/**/specs/…),
# and bare code-or-uuid stock files with no photo index.
PHOTO_RE = re.compile(r"-(\d{2,4})(?:[_.]|$)")
def is_factory(filename, rel_path):
    rp = (rel_path or "").replace("\\", "/").lower()
    # Paths are relative to ASSETS so Heads/ and Measure/ appear without a leading slash.
    # Use prefix-agnostic substrings ("heads/", "measure") rather than "/heads/", "/measure".
    if "heads/" in rp or "/specs/" in rp or "measure" in rp:
        return True
    return PHOTO_RE.search(filename or "") is None   # no -NNN index = not a photoshoot frame

SERIES_DIR = {"K": "K-Series", "I": "I-Series", "Fusion": "Fusion-Series", "SLE": "SLE-Series"}
SERIES_LABEL = {"K": "K-Series", "I": "Inspiration", "Fusion": "Fusion", "SLE": "SLE"}

# ── Name banks (deterministic assignment; editable in overlay) ────────────────
NAMES = {
 "K": ["Sora","Lian","Mira","Zhen","Yuna","Hana","Nari","Seo","Rae","Hwa","Suki","Jia"],
 "I": ["Ava","Mia","Chloe","Isla","Nora","Lena","Elsa","Romy","Tess","Quinn","Faye","June",
       "Cora","Vera","Lux","Dahlia","Skye","Wren","Pia","Noa","Elle","Greer","Maren","Sage"],
 "Fusion": ["Gwen","Baifern","Mali","Anya","Noor","Suri","Talia","Indira","Yara","Leah","Mina","Rhea"],
 "SLE": ["Vesper","Roxanne","Cleo","Lola","Bianca","Selena","Carmen","Davina","Eva","Fiona",
         "Gia","Helena","Ivy","Jolene","Kira","Layla","Monica","Nadia","Octavia","Priya",
         "Raven","Sienna","Tia","Ursula","Valentina","Willa","Xena","Yvonne","Zara","Anais",
         "Bella","Coco","Dita","Esme","Farah","Ginger","Honey","Iris","Jade","Kitty",
         "Lacey","Margot","Nova","Odette","Paloma","Rosa","Sabrina","Trixie","Uma","Vivien",
         "Wanda","Ximena","Yuki","Zoe","Aria","Brielle","Cira","Delphine","Estelle","Freya",
         "Giselle","Hazel","Inez","Juno","Kali","Liv","Maeve","Nyx","Opal","Petra"],
}

ALT_TITLES = {
 "The Classic": ["The Sweetheart","The Debutante","The Homecoming"],
 "The Icon":    ["The Starlet","The Cover","The Spotlight"],
 "The Muse":    ["The Naturalist","The Editorial","The Confidante"],
 "The Siren":   ["The Temptress","The Bombshell","The Vixen"],
 "The Athlete": ["The Dancer","The Runner","The Minimalist"],
 "The Empress": ["The Sovereign","The Plush","The Maximalist"],
 "The Sculpt":  ["The Statue","The Form","The Define"],
 None:          ["The Maven","The Wildcard","The Free Spirit"],
}

ENERGY_WORDS = {
 "The Classic":"timeless · balanced · inviting", "The Icon":"glamorous · camera-ready · poised",
 "The Muse":"natural · elongated · quietly confident", "The Siren":"bold · bust-forward · magnetic",
 "The Athlete":"lean · tapered · understated", "The Empress":"plush · abundant · regal",
 "The Sculpt":"defined · muscular · deliberate", None:"distinctive · expressive · individual",
}


# 4 distinct taglines per family (one per slot) — brief voice. {h}/{c} = height/cup.
TAGLINES = {
 "The Classic": ["Timeless lines, nothing to prove.", "The hourglass, uncomplicated.",
                 "Curves that never date.", "Effortless — and she knows it."],
 "The Icon": ["Built for the lens.", "Glamour, with the volume up.",
              "Camera-ready from any angle.", "The cover shot, in person."],
 "The Muse": ["{h}cm of quiet confidence.", "Tall, natural, unhurried.",
              "Hip-led elegance, head to toe.", "The one the room slows down for."],
 "The Siren": ["Impossible to look away from.", "{c}-cup, and unapologetic.",
               "Presence as a love language.", "She walks in; the story starts."],
 "The Athlete": ["Lean lines, zero excess.", "Restraint as a flex.",
                 "Toned, tapered, deliberate.", "Sleek where it counts."],
 "The Empress": ["Maximum plush, full stop.", "Abundance, worn like a crown.",
                 "Soft power, {c}-cup over.", "Generous by design."],
 "The Sculpt": ["Defined, deliberate, carved.", "Form you read across a room.",
                "Muscle and intention.", "Statuesque, and earned."],
}
DEFAULT_TAGLINES = ["{h}cm, one of a kind.", "Her own category.",
                    "{c}-cup, unfiled.", "No archetype required."]

def tagline(fam, cup, height, slot):
    pool = TAGLINES.get(fam, DEFAULT_TAGLINES)
    return pool[(slot - 1) % len(pool)].format(h=height, c=cup)


def load_json(p, default):
    if p.exists():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError): pass
    return default


def main():
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    bp = {p["body_code"]: p for p in load_json(BODY_PROFILES, {}).get("profiles", [])}
    leads = load_json(LEAD_PERSONAS, {})           # body_code -> {persona(title), tagline,...}
    overlay = load_json(OVERLAY, {})               # character_id -> {...}
    stories = load_json(STORIES, {})               # character_id -> {story, profile{...}}

    # product lookup for hand-curation (overlay can reassign a slot's photoshoot via use_product)
    prod_by_code = {pr["code"]: pr for pr in cur.execute(
        "SELECT code, head_code, face_code, folder_path, image_count, price, live_handle FROM products").fetchall()}

    # bodies grouped by series, each with its products (photoshoots) richest-first
    bodies = cur.execute("""
        SELECT b.code, b.series_id, b.height_cm, b.cup_size, b.line_label
        FROM bodies b
        WHERE b.code IN (SELECT DISTINCT body_code FROM products WHERE body_code IS NOT NULL)
        ORDER BY b.series_id, b.height_cm
    """).fetchall()

    characters = []
    body_types = []
    name_idx = {k: 0 for k in NAMES}

    skipped_torso = []
    for b in bodies:
        code, sid = b["code"], b["series_id"]
        if is_torso(code, b["height_cm"]):
            skipped_torso.append(code)
            continue
        prof = bp.get(code, {})
        fam = prof.get("family")
        # products on this body, richest photoshoot first, one per distinct head
        prods = cur.execute("""
            SELECT code, head_code, face_code, folder_path, image_count, price, live_handle
            FROM products WHERE body_code=? ORDER BY image_count DESC, code
        """, (code,)).fetchall()
        # photoshoot frames for a product, factory imagery stripped, -101 first.
        # prefix (optional) keeps only files whose name starts with it — used to clean
        # folders that were contaminated with images from another shoot.
        def shots(pcode, prefix=None):
            rows = cur.execute(
                "SELECT filename, rel_path, id FROM product_assets "
                "WHERE product_code=? AND media_type='image'", (pcode,)).fetchall()
            rows = [r for r in rows if not is_factory(r["filename"], r["rel_path"])]
            if prefix:
                rows = [r for r in rows if (r["filename"] or "").startswith(prefix)]
            rows.sort(key=lambda r: (int(PHOTO_RE.search(r["filename"] or "").group(1))
                                     if PHOTO_RE.search(r["filename"] or "") else 9999, r["id"]))
            return ["assets/" + r["rel_path"] for r in rows[:8]]

        # de-dup by head_code, keep richest — but only products that actually have a real
        # photoshoot (≥1 non-factory frame) may fill a live slot.
        seen, uniq, no_photoshoot = set(), [], []
        for pr in prods:
            h = pr["head_code"] or pr["code"]
            if h in seen: continue
            if not shots(pr["code"]):
                no_photoshoot.append(pr["code"]); continue   # factory-only product → not a character
            seen.add(h); uniq.append(pr)

        chosen = uniq[:4]
        surplus = [pr["code"] for pr in uniq[4:]]

        char_ids = []
        for slot in range(1, 5):
            cid = f"{sid}-{code}-{slot:02d}"
            char_ids.append(cid)
            nm = NAMES.get(sid, NAMES["I"])
            name = nm[name_idx[sid] % len(nm)]; name_idx[sid] += 1

            # title: slot 1 uses curated lead title if present, else family
            if slot == 1 and leads.get(code, {}).get("persona"):
                title = leads[code]["persona"]
            elif slot == 1:
                title = fam or "The Original"
            else:
                alts = ALT_TITLES.get(fam, ALT_TITLES[None])
                title = alts[(slot - 2) % len(alts)]

            live = slot <= len(chosen)
            rec = {
                "character_id": cid, "slot": slot, "series": SERIES_LABEL[sid], "series_code": sid,
                "status": "live" if live else "placeholder",
                "body_code": code,
                "body": {
                    "family": fam, "silhouette": prof.get("silhouette"),
                    "height_cm": b["height_cm"], "cup": b["cup_size"],
                    "weight_kg": prof.get("weight_kg"),
                    "bust": prof.get("bust_cm"), "waist": prof.get("waist_cm"), "hip": prof.get("hip_cm"),
                    "WHR": prof.get("WHR"), "BWR": prof.get("BWR"),
                    "bust_drop_cm": prof.get("bust_drop_cm"),
                    "estimated": bool(prof.get("estimated")), "est_basis": prof.get("est_basis"),
                },
                "persona": {
                    "name": name, "title": title,
                    "tagline": tagline(fam, b["cup_size"], b["height_cm"], slot),
                    "energy": ENERGY_WORDS.get(fam, ENERGY_WORDS[None]),
                    "target_buyer": prof.get("target_buyer") if slot == 1 else None,
                    "positioning": leads.get(code, {}).get("positioning") if slot == 1 else None,
                },
            }
            ovc = overlay.get(cid, {})   # hand-curation for this character
            if live:
                pr = chosen[slot - 1]
                # overlay can reassign this slot's photoshoot to another product (full swap)
                if ovc.get("use_product") and ovc["use_product"] in prod_by_code:
                    pr = prod_by_code[ovc["use_product"]]
                imgs = shots(pr["code"], ovc.get("gallery_prefix"))
                # overlay can choose a different hero: "last", "first", or a 0-based index.
                # The chosen image is moved to the front so it leads card + detail page.
                hsel = ovc.get("hero")
                if imgs and hsel is not None:
                    i = (len(imgs) - 1) if hsel == "last" else (0 if hsel == "first" else
                         (hsel if isinstance(hsel, int) and 0 <= hsel < len(imgs) else None))
                    if i is not None:
                        imgs = [imgs[i]] + imgs[:i] + imgs[i + 1:]
                rec["face"] = {"head_code": pr["head_code"], "face_code": pr["face_code"], "skin_tone": None}
                rec["photoshoot"] = {
                    "status": "live", "product_code": pr["code"], "folder": "assets/" + pr["folder_path"],
                    "hero": imgs[0] if imgs else None, "gallery": imgs,
                    "image_count": pr["image_count"], "price": pr["price"], "live_handle": pr["live_handle"],
                }
            else:
                # borrow a sibling shoot on the same body (cycle through chosen)
                if chosen:
                    borrow = chosen[(slot - 1) % len(chosen)]
                    imgs = shots(borrow["code"])
                    rec["face"] = {"head_code": None, "face_code": None, "skin_tone": None}
                    rec["photoshoot"] = {
                        "status": "placeholder", "representative_only": True,
                        "borrowed_from": borrow["code"], "folder": "assets/" + borrow["folder_path"],
                        "hero": imgs[0] if imgs else None, "gallery": imgs,
                        "image_count": 0, "price": borrow["price"], "live_handle": None,
                    }
                    rec["placeholder"] = {
                        "reason": f"No photoshoot yet for a {slot}{'st' if slot==1 else 'th'} head on {code}",
                        "art_direction": f"{prof.get('silhouette') or 'on-brand'} styling; new head on body {code}.",
                    }
                else:
                    rec["face"] = {"head_code": None, "face_code": None, "skin_tone": None}
                    rec["photoshoot"] = {"status": "placeholder", "hero": None, "gallery": []}

            # attach narrative story + structured profile (regenerable overlay).
            # story_from lets a swapped character keep their OWN story from another slot.
            st = stories.get(ovc.get("story_from") or cid)
            if st:
                if st.get("story"):   rec["persona"]["story"] = st["story"]
                if st.get("profile"): rec["persona"]["profile"] = st["profile"]

            # apply hand overlay last (wins over everything)
            ov = overlay.get(cid)
            if ov:
                rec["persona"].update({k: v for k, v in ov.items() if k in rec["persona"]})
                if "name" in ov: rec["persona"]["name"] = ov["name"]
            characters.append(rec)

        body_types.append({
            "body_code": code, "series": SERIES_LABEL[sid], "family": fam,
            "height_cm": b["height_cm"], "cup": b["cup_size"],
            "WHR": prof.get("WHR"), "BWR": prof.get("BWR"),
            "spec_card": None,
            "characters": char_ids,
            "photoshoot_count": len(prods),
            "live_slots": min(4, len(chosen)),
            "additional_photoshoots": surplus,
        })

    OUT_CHARS.write_text(json.dumps({"characters": characters}, indent=2, ensure_ascii=False), encoding="utf-8")
    OUT_BODIES.write_text(json.dumps({"body_types": body_types}, indent=2, ensure_ascii=False), encoding="utf-8")

    # ── DB tables ───────────────────────────────────────────────────────────────
    cur.execute("DROP TABLE IF EXISTS characters")
    cur.execute("""CREATE TABLE characters(
        character_id TEXT PRIMARY KEY, slot INTEGER, series TEXT, body_code TEXT,
        status TEXT, name TEXT, title TEXT, tagline TEXT,
        head_code TEXT, product_code TEXT, hero TEXT)""")
    for c in characters:
        cur.execute("INSERT OR REPLACE INTO characters VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (c["character_id"], c["slot"], c["series"], c["body_code"], c["status"],
             c["persona"]["name"], c["persona"]["title"], c["persona"]["tagline"],
             (c.get("face") or {}).get("head_code"),
             (c.get("photoshoot") or {}).get("product_code"),
             (c.get("photoshoot") or {}).get("hero")))
    cur.execute("DROP TABLE IF EXISTS body_type_pool")
    cur.execute("CREATE TABLE body_type_pool(body_code TEXT, product_code TEXT)")
    for bt in body_types:
        for pc in bt["additional_photoshoots"]:
            cur.execute("INSERT INTO body_type_pool VALUES(?,?)", (bt["body_code"], pc))
    conn.commit()

    live = sum(1 for c in characters if c["status"] == "live")
    ph = len(characters) - live
    print(f"Characters: {len(characters)} ({live} live, {ph} placeholder) across {len(body_types)} body types")
    bs = {}
    for c in characters:
        bs.setdefault(c["series"], [0, 0])
        bs[c["series"]][0 if c["status"] == "live" else 1] += 1
    for s, (l, p) in bs.items():
        print(f"  {s:<12} {l+p} chars  ({l} live, {p} placeholder)")
    pooled = sum(len(bt["additional_photoshoots"]) for bt in body_types)
    print(f"Surplus photoshoots pooled on body types: {pooled}")
    if skipped_torso:
        print(f"Excluded {len(skipped_torso)} torso-only bodies: {', '.join(sorted(set(skipped_torso)))}")
    withstory = sum(1 for c in characters if c['persona'].get('story'))
    print(f"Characters with written story: {withstory}/{len(characters)}")
    print(f"Wrote db/characters.json, db/body_types.json")
    conn.close()


if __name__ == "__main__":
    main()
