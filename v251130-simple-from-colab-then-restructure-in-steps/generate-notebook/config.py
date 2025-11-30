"""Configuration module - Step 6.

Adds Aggregator flags.
"""
from pathlib import Path
import warnings
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# --- Paths ---
PROJECT_ROOT = Path.cwd()
OUTPUT_DIR = PROJECT_ROOT / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def out_path(name: str) -> str:
    return str(OUTPUT_DIR / name)

# --- Plotting Configuration ---
warnings.filterwarnings('ignore')
matplotlib.use('Agg')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# --- Data Constants ---
DATA_CSV_URL = 'https://raw.githubusercontent.com/StephenEastham/bmw-sales-forecast/refs/heads/main/v251125/BMW-sales-data-2010-2024.csv'
DATA_CSV_FILE = 'BMW-sales-data-2010-2024.csv'

# --- Feature Flags ---
ENABLE_DATA_PROCESSING = True
ENABLE_EXPLORATORY_ANALYSIS = True
ENABLE_TIME_SERIES = True
ENABLE_STATIC_PLOTS = True
ENABLE_DASHBOARDS = True
ENABLE_REPORTING = True
ENABLE_AGGREGATOR = True
