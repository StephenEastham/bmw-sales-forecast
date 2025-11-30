"""Utilities module.

Contains helper functions for file management and logging.
"""
import shutil
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from config import OUTPUT_DIR

def clean_outputs():
    """Delete all files in the output directory."""
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

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(title)
    print("="*80)

def zip_all_outputs(zip_filename=None, patterns=('*.png','*.html','*.csv','*.txt')):
    """Create a zip archive of generated outputs in `OUTPUT_DIR`."""
    if zip_filename is None:
        zip_path = OUTPUT_DIR / 'all_outputs.zip'
    else:
        zip_path = Path(zip_filename)
        if not zip_path.is_absolute():
            zip_path = OUTPUT_DIR / zip_path

    # Ensure OUTPUT_DIR exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    added = 0
    try:
        with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zf:
            for pat in patterns:
                for p in OUTPUT_DIR.glob(pat):
                    if p.is_file():
                        zf.write(p, arcname=p.name)
                        added += 1
        print(f"✅ Created zip: {zip_path.resolve()} ({added} files)")
        return zip_path
    except Exception as e:
        print(f"⚠️ Error while creating zip: {e}")
        raise
