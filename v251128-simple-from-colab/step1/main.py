"""Minimal runner that ties together the `step 1` helpers.

This file is intentionally tiny: it adjusts `sys.path` so the local
folder imports work when executed as a script, runs a safe pipeline that
cleans outputs, downloads required data (if missing), loads and preprocesses
the CSV, and prints a short summary.
"""
from pathlib import Path
from datetime import datetime

from . import config, data, utils


def run_pipeline():
    print("[step1] Starting minimal pipeline —", datetime.now().isoformat())
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
