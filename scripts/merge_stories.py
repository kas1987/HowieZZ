"""Validate the per-series story files and merge into db/character_stories.json."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
PARTS = [
    "_stories_k-series.json",
    "_stories_inspiration.json",
    "_stories_fusion.json",
    "_stories_sle.json",
]
PROFILE_FIELDS = ("personality", "ideal_setting", "signature", "for_you_if")


def validate_and_merge(parts_data, valid_ids):
    """
    Validate and merge story data from multiple part files.

    parts_data: list of (filename: str, data: dict | None)
                data is None if the file was missing or had invalid JSON
    valid_ids:  set of known character_ids (strings)

    Returns: (merged: dict[str, dict], problems: list[str])
      merged maps character_id -> {"story": str|None, "profile": dict}
    """
    merged, problems = {}, []
    for filename, d in parts_data:
        if d is None:
            problems.append(f"MISSING OR INVALID FILE {filename}")
            continue
        for cid, body in d.items():
            if cid not in valid_ids:
                problems.append(f"{filename}: unknown character_id {cid}")
                continue
            if not isinstance(body, dict):
                problems.append(f"{cid}: invalid body format (expected dict)")
                continue
            if not body.get("story"):
                problems.append(f"{cid}: missing story")
            prof = body.get("profile")
            if not isinstance(prof, dict):
                prof = {}
            for f in PROFILE_FIELDS:
                if not prof.get(f):
                    problems.append(f"{cid}: profile.{f} missing")
            merged[cid] = {"story": body.get("story"), "profile": prof}
    return merged, problems


def main():
    chars = json.loads((DB / "characters.json").read_text(encoding="utf-8"))["characters"]
    valid_ids = {c["character_id"] for c in chars}

    parts_data = []
    for p in PARTS:
        fp = DB / p
        if not fp.exists():
            parts_data.append((p, None))
            continue
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
            parts_data.append((p, d))
        except json.JSONDecodeError as e:
            print(f"INVALID JSON {p}: {e}")
            parts_data.append((p, None))

    merged, problems = validate_and_merge(parts_data, valid_ids)

    missing = sorted(valid_ids - set(merged))
    print(f"characters total : {len(valid_ids)}")
    print(f"stories merged   : {len(merged)}")
    print(f"characters w/o story: {len(missing)}  {missing[:8]}")
    wc = [(cid, len(re.findall(r'\w+', m['story'] or ''))) for cid, m in merged.items()]
    short = [(c, w) for c, w in wc if w < 90]
    long_ = [(c, w) for c, w in wc if w > 210]
    print(f"stories <90 words: {len(short)} {short[:4]}")
    print(f"stories >210 words: {len(long_)} {long_[:4]}")
    print(f"problems: {len(problems)}")
    for pr in problems[:20]:
        print("  -", pr)

    (DB / "character_stories.json").write_text(
        json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    if not problems and not missing:
        print("WROTE db/character_stories.json")
    else:
        print("(wrote partial merge anyway for", len(merged), "characters)")


if __name__ == "__main__":
    main()
