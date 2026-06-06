#!/usr/bin/env python3
"""
Rebuild K-Series persona manifests from curated folder/range rules.

Writes:
- assets/data/k-series-personas.json
- assets/K-Series/Characters/<Persona>/manifest.json

Usage:
  python scripts/rebuild_k_series_personas.py
  python scripts/rebuild_k_series_personas.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent

PERSONA_RULES = {
    "sora": {
        "displayName": "Sora",
        "archetype": "The Companion",
        "character": "Suyeon",
        "body": "ZK159D",
        "weightKg": 33.8,
        "sourceFolder": "assets/K-Series/KE02_1+ZK159D-1",
        "preferredSeq": [101, 104, 115, 122, 128, 133],
    },
    "lian": {
        "displayName": "Lian",
        "archetype": "The Muse",
        "character": "Arin",
        "body": "ZK168B",
        "weightKg": 37.5,
        "sourceFolder": "assets/K-Series/KE01_1+ZK168B-1",
        "preferredSeq": [123, 128, 133, 138, 141, 142],
    },
    "mira": {
        "displayName": "Mira",
        "archetype": "The Icon",
        "character": "Suyeon",
        "body": "ZK168B",
        "weightKg": 37.5,
        "sourceFolder": "assets/K-Series/KE02_1+ZK168B-1",
        "preferredSeq": [101, 104, 115, 122, 126, 128],
    },
    "zhen": {
        "displayName": "Zhen",
        "archetype": "The It-Girl",
        "character": "Somi",
        "body": "ZK168B",
        "weightKg": 37.5,
        "sourceFolder": "assets/K-Series/KE03_1+ZK168B-1",
        "preferredSeq": [101, 106, 116, 123, 127, 129],
    },
}

MODEL_CHARACTERS = {
    "arin": ["lian"],
    "suyeon": ["sora", "mira"],
    "somi": ["zhen"],
}


def parse_args() -> argparse.Namespace:
    # Ignore accidental placeholder args like '.' to avoid conversion failures.
    cleaned_argv = [a for a in sys.argv[1:] if a and a.strip() not in {"."}]
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(cleaned_argv)


def seq_from_name(path: Path) -> int:
    m = re.search(r"-(\d{3})\.[^.]+$", path.name)
    return int(m.group(1)) if m else -1


def collect_library(source_folder: Path, preferred_seq: List[int]) -> List[str]:
    by_seq: Dict[int, Path] = {}
    for file in source_folder.glob("*.jpg"):
        seq = seq_from_name(file)
        if seq >= 0:
            by_seq[seq] = file

    library: List[str] = []
    for seq in preferred_seq:
        file = by_seq.get(seq)
        if not file:
            continue
        rel = file.relative_to(ROOT).as_posix()
        library.append(rel)

    return library


def build_catalog() -> dict:
    personas = {}

    for key, rule in PERSONA_RULES.items():
        source_folder = ROOT / rule["sourceFolder"]
        library = collect_library(source_folder, rule["preferredSeq"])

        personas[key] = {
            "displayName": rule["displayName"],
            "archetype": rule["archetype"],
            "character": rule["character"],
            "body": rule["body"],
            "weightKg": rule["weightKg"],
            "sourceFolders": [rule["sourceFolder"]],
            "library": library,
        }

    return {
        "version": 1,
        "source": "ZELEX-CEO-Executive-Brief.md#appendix-b",
        "personas": personas,
        "modelCharacters": MODEL_CHARACTERS,
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_character_manifests(catalog: dict) -> None:
    personas = catalog.get("personas", {})
    base = ROOT / "assets" / "K-Series" / "Characters"
    base.mkdir(parents=True, exist_ok=True)

    readme = (
        "# K-Series Character Libraries\n\n"
        "This folder organizes APX-B personas into pullable character manifests.\n\n"
        "## Personas\n"
        "- Sora -> Characters/Sora/manifest.json\n"
        "- Lian -> Characters/Lian/manifest.json\n"
        "- Mira -> Characters/Mira/manifest.json\n"
        "- Zhen -> Characters/Zhen/manifest.json\n"
    )
    (base / "README.md").write_text(readme, encoding="utf-8")

    for key, persona in personas.items():
        folder = base / persona["displayName"]
        folder.mkdir(parents=True, exist_ok=True)
        manifest = {
            "persona": persona["displayName"],
            "apxBCharacter": persona["character"],
            "body": persona["body"],
            "sourceFolder": persona["sourceFolders"][0],
            "library": persona["library"],
        }
        write_json(folder / "manifest.json", manifest)


def main() -> int:
    args = parse_args()
    catalog = build_catalog()

    data_path = ROOT / "assets" / "data" / "k-series-personas.json"

    if args.dry_run:
        print(json.dumps(catalog, indent=2))
        return 0

    write_json(data_path, catalog)
    write_character_manifests(catalog)
    print("Rebuilt K-Series persona manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
