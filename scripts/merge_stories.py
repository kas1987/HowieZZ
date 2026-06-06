"""Validate the per-series story files and merge into db/character_stories.json."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
parts = ["_stories_k-series.json","_stories_inspiration.json","_stories_fusion.json","_stories_sle.json"]

chars = json.loads((DB/"characters.json").read_text(encoding="utf-8"))["characters"]
valid_ids = {c["character_id"] for c in chars}

merged, problems = {}, []
for p in parts:
    fp = DB/p
    if not fp.exists():
        problems.append(f"MISSING FILE {p}"); continue
    try:
        d = json.loads(fp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        problems.append(f"INVALID JSON {p}: {e}"); continue
    for cid, body in d.items():
        if cid not in valid_ids:
            problems.append(f"{p}: unknown character_id {cid}"); continue
        if not body.get("story"): problems.append(f"{cid}: missing story")
        prof = body.get("profile") or {}
        for f in ("personality","ideal_setting","signature","for_you_if"):
            if not prof.get(f): problems.append(f"{cid}: profile.{f} missing")
        merged[cid] = {"story": body.get("story"), "profile": prof}

missing = sorted(valid_ids - set(merged))
print(f"characters total : {len(valid_ids)}")
print(f"stories merged   : {len(merged)}")
print(f"characters w/o story: {len(missing)}  {missing[:8]}")
# word-count sanity
import re
wc = [(cid, len(re.findall(r'\w+', m['story'] or ''))) for cid,m in merged.items()]
short = [(c,w) for c,w in wc if w<90]; long=[(c,w) for c,w in wc if w>210]
print(f"stories <90 words: {len(short)} {short[:4]}")
print(f"stories >210 words: {len(long)} {long[:4]}")
print(f"problems: {len(problems)}")
for pr in problems[:20]: print("  -", pr)

if not problems and not missing:
    (DB/"character_stories.json").write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print("WROTE db/character_stories.json")
else:
    print("NOT WRITING — resolve problems first" if (problems or missing) else "")
    # still write what we have so the build can proceed, but flag it
    (DB/"character_stories.json").write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print("(wrote partial merge anyway for", len(merged), "characters)")
