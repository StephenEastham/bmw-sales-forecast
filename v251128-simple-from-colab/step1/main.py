"""Minimal runner that ties together the `step 1` helpers.
"""
from pathlib import Path
from datetime import datetime

# Local imports
import config
import data
import utils


def run_pipeline():
    print("Starting pipeline —", datetime.now().isoformat())
    utils.clean_outputs()
    try:
        data.download_required_files()
    except Exception as e:
        print(f"[step1] Warning: download failed: {e}")
    try:
        df = data.load_and_explore_data(config.DATA_CSV_FILE)
        df_clean = data.preprocess_data(df)
        print(f"[step1] Preprocessed data: rows={len(df_clean):,}, cols={df_clean.shape[1]}")
    except Exception as e:
        print(f"[step1] Error loading/preprocessing data: {e}")
    print("[step1] Pipeline complete —", datetime.now().isoformat())


if __name__ == "__main__":
    run_pipeline()
