"""
Configuration and constants for BMW Sales Forecasting System
"""

from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings

# Project root and output directory (make paths robust to working directory)
PROJECT_ROOT = Path(__file__).resolve().parent

# Output directory for generated artifacts (inside the project root)
OUTPUT_DIR = PROJECT_ROOT / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def out_path(name: str) -> str:
    """Return a path inside the outputs directory as a string."""
    return str(OUTPUT_DIR / name)


# Matplotlib configuration
warnings.filterwarnings('ignore')
matplotlib.use('Agg')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Pandas options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# Data URLs
DATA_CSV_URL = 'https://raw.githubusercontent.com/StephenEastham/bmw-sales-forecast/refs/heads/main/v251125/BMW-sales-data-2010-2024.csv'
HOWTO_URL = 'https://raw.githubusercontent.com/StephenEastham/bmw-sales-forecast/refs/heads/main/how-to-test.md'

DATA_CSV_FILE = 'BMW-sales-data-2010-2024.csv'
HOWTO_FILE = 'how-to-test.md'

# Alert thresholds (multipliers) and forecasting parameters removed in simplified pipeline
# Feature Flags
ENABLE_DATA_PROCESSING = True
# Calls: download_required_files, load_and_explore_data, preprocess_data

ENABLE_EXPLORATORY_ANALYSIS = True
# Calls: exploratory_data_analysis

ENABLE_TIME_SERIES = True
# Calls: aggregate_time_series

ENABLE_STATIC_PLOTS = True
# Calls: create_overview_visualizations, create_heatmap

ENABLE_REPORTING = True
# Calls: generate_monthly_report, generate_final_summary

ENABLE_DASHBOARDS = True
# Calls: create_interactive_dashboard, create_heatmap_interactive

ENABLE_AGGREGATOR = True
# Calls: create_aggregator_html
