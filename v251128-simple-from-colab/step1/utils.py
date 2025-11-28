from pathlib import Path
import shutil
import logging
from zipfile import ZipFile, ZIP_DEFLATED
from typing import Iterable

import config
from config import OUTPUT_DIR, out_path


def clean_outputs() -> None:
    """Delete all files and folders under the `OUTPUT_DIR`.
    """
    print(f"Cleaning output directory: {OUTPUT_DIR}")
    if OUTPUT_DIR.exists():
        for item in OUTPUT_DIR.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Failed to delete {item}: {e}")
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def print_section(title: str) -> None:
    """Print a formatted section header for console output."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def zip_all_outputs(zip_filename: str | None = None, patterns: Iterable[str] = ("*.png", "*.html", "*.csv", "*.txt")) -> Path:
    """Create a zip archive of files under `OUTPUT_DIR` matching `patterns`.

    Returns the path to the created zip file. Patterns are glob patterns.
    """
    if zip_filename is None:
        zip_path = OUTPUT_DIR / "all_outputs.zip"
    else:
        zip_path = Path(zip_filename)
        if not zip_path.is_absolute():
            zip_path = OUTPUT_DIR / zip_path

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    added = 0
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        for pat in patterns:
            for p in OUTPUT_DIR.glob(pat):
                if p.is_file():
                    zf.write(p, arcname=p.name)
                    added += 1
    print(f"Created zip: {zip_path.resolve()} ({added} files)")
    return zip_path
