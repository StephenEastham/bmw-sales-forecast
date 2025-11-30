"""Configuration module - Step 1.

Contains basic paths and constants for the project infrastructure.
"""
from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def out_path(name: str) -> str:
    return str(OUTPUT_DIR / name)

# --- Data Constants ---
DATA_CSV_URL = 'https://raw.githubusercontent.com/StephenEastham/bmw-sales-forecast/refs/heads/main/v251125/BMW-sales-data-2010-2024.csv'
DATA_CSV_FILE = 'BMW-sales-data-2010-2024.csv'

# --- Feature Flags (Infrastructure) ---
# We include this here as it's referenced in the infrastructure test,
# even though the logic isn't implemented until Step 2.
ENABLE_DATA_PROCESSING = True
