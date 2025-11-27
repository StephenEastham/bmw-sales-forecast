"""
Utility functions: logging, paths, and helpers
"""

import logging
import shutil
from config import out_path, OUTPUT_DIR


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


def setup_logger(log_file='sales_alerts.log'):
    """Setup logging to file and console"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(out_path(log_file)),
            logging.StreamHandler()
        ],
        force=True
    )
    return logging.getLogger(__name__)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(title)
    print("="*80)
