"""Download helpers and a dataset inspector.

This file only LOOKS at the datasets for now. The loading, cleaning and splitting
code gets written after we've seen what the real files contain.
"""
import zipfile
from collections import Counter
from pathlib import Path

import pandas as pd

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}
TABLE_EXTS = {".csv", ".xlsx", ".xls"}


def unzip_all(folder):
    """Unzip every .zip in `folder` (in place) that hasn't been unzipped yet."""
    for z in Path(folder).rglob("*.zip"):
        target = z.with_suffix("")
        if target.exists():
            continue
        print(f"Unzipping {z.name} ...")
        with zipfile.ZipFile(z) as f:
            f.extractall(target)


def _read_table(path):
    if path.suffix.lower() == ".csv":
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin-1")
    return pd.read_excel(path)


def describe_dataset(root, n_names=8):
    """Print everything we need to write the loader: file types, folders with image
    counts, example file names, and the columns of every label table."""
    root = Path(root)
    files = [p for p in root.rglob("*") if p.is_file()]
    print(f"== {root} ==  ({len(files)} files)")
    print("file types:", dict(Counter(p.suffix.lower() or "(none)" for p in files)))

    folders = Counter(p.parent for p in files if p.suffix.lower() in IMAGE_EXTS)
    print("\nfolders with images:")
    for folder, n in sorted(folders.items()):
        print(f"  {n:6d} images  {folder.relative_to(root)}")

    images = sorted(p for p in files if p.suffix.lower() in IMAGE_EXTS)
    print(f"\nexample image paths (of {len(images)}):")
    for p in images[:n_names]:
        print("  ", p.relative_to(root))

    tables = sorted(p for p in files if p.suffix.lower() in TABLE_EXTS and not p.name.startswith("~$"))
    if not tables:
        print("\nNo csv/xlsx label files found. Labels may be in file names or folder names.")
    for f in tables:
        df = _read_table(f)
        print(f"\nlabel file: {f.relative_to(root)}  ({len(df)} rows)")
        print("  columns:", list(df.columns))
        print(df.head(3).to_string(index=False))
