#!/usr/bin/env python3
"""
Extract Per Drive zips into structured asset folders.

Usage:  python scripts/extract_assets.py
"""

import zipfile
import re
import shutil
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
PER_DRIVE = ASSETS / "Per Drive"


def extract_head_list():
    z = PER_DRIVE / "3. Head List-20260605T171659Z-3-001.zip"
    if not z.exists():
        print(f"[skip] {z.name} not found"); return
    dest = ASSETS / "Heads"
    dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(z) as zf:
        for member in zf.namelist():
            parts = Path(member).parts
            # structure: "3. Head List/JPG/Hard head/file.png"
            #         or "3. Head List/Head List Inspiration-....jpg"
            if len(parts) < 2 or parts[-1] == '':
                continue
            filename = parts[-1]
            if len(parts) >= 4 and parts[2].lower() in ('hard head', 'soft head'):
                subdir = "Hard" if "hard" in parts[2].lower() else "Soft"
                out = dest / subdir / filename
                out.parent.mkdir(exist_ok=True)
            elif len(parts) == 2:
                out = dest / filename   # inspiration image at root
            else:
                continue
            if not out.exists():
                data = zf.read(member)
                out.write_bytes(data)
    count = sum(1 for _ in dest.rglob("*") if _.is_file())
    print(f"Heads: {count} files extracted to {dest.relative_to(ROOT)}")


def extract_options():
    z = PER_DRIVE / "04. Options-20260605T171701Z-3-001.zip"
    if not z.exists():
        print(f"[skip] {z.name} not found"); return
    dest = ASSETS / "Options"
    dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(z) as zf:
        for member in zf.namelist():
            parts = Path(member).parts
            # structure: "04. Options/Body Options/Hand Type/1#-Hard Hand.jpg"
            if len(parts) < 4 or parts[-1] == '':
                continue
            # Strip leading "04. Options/" → keep "Body Options/Hand Type/file.jpg"
            rel = Path(*parts[1:])
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            if not out.exists():
                data = zf.read(member)
                out.write_bytes(data)
    count = sum(1 for _ in dest.rglob("*") if _.is_file())
    print(f"Options: {count} files extracted to {dest.relative_to(ROOT)}")


def extract_fusion():
    z = PER_DRIVE / "FUSION SERIES-20260605T171645Z-3-001.zip"
    if not z.exists():
        print(f"[skip] {z.name} not found"); return
    dest = ASSETS / "Fusion-Series"
    dest.mkdir(exist_ok=True)

    with zipfile.ZipFile(z) as zf:
        for member in zf.namelist():
            filename = Path(member).name
            if not filename:
                continue

            ext = Path(filename).suffix.lower()

            # Product images/videos: ZFE01_1+ZF168B-101.jpg
            m = re.match(r'(ZFE\d+_\d+\+ZF\d+[A-Z])', filename)
            if m:
                product = m.group(1)
                out = dest / product / filename
            # Body spec images: ZF168B(cm).jpg, ZF169C(inch).jpg
            elif re.match(r'ZF\d+[A-Z]\(', filename):
                out = dest / "specs" / filename
            # Standalone videos
            elif ext == '.mp4':
                out = dest / "videos" / filename
            # PSD source files
            elif ext == '.psd':
                out = dest / "source" / filename
            # Misc (1.jpg, 2.jpg)
            else:
                out = dest / "misc" / filename

            out.parent.mkdir(parents=True, exist_ok=True)
            if not out.exists():
                data = zf.read(member)
                out.write_bytes(data)

    count = sum(1 for _ in dest.rglob("*") if _.is_file())
    print(f"Fusion Series: {count} files extracted to {dest.relative_to(ROOT)}")


def move_guides():
    guides_dest = ASSETS / "Guides"
    guides_dest.mkdir(exist_ok=True)
    for name in ("01_WIG_BIBLE_Master_Edition.html", "doll_sizing_booklet_enhanced.html"):
        src = PER_DRIVE / name
        dst = guides_dest / name
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            print(f"Guides: copied {name}")
    print(f"Guides ready at {guides_dest.relative_to(ROOT)}")


def fix_loose_files():
    """Move any loose image files in series root dirs into per-product folders."""
    for series_dir in (ASSETS / "I-Series", ASSETS / "K-Series"):
        if not series_dir.exists():
            continue
        for f in list(series_dir.iterdir()):
            if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
                # Extract product code prefix (everything before the last -NNN)
                m = re.match(r'(.+)-\d{3}', f.stem)
                if m:
                    folder = series_dir / m.group(1)
                    folder.mkdir(exist_ok=True)
                    dst = folder / f.name
                    if not dst.exists():
                        shutil.move(str(f), str(dst))
                        print(f"Moved loose file: {f.name} → {folder.name}/")


if __name__ == "__main__":
    print("Extracting assets...")
    fix_loose_files()
    extract_head_list()
    extract_options()
    extract_fusion()
    move_guides()
    print("\nDone.")
