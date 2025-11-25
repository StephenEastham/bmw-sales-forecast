"""
Data loading, downloading, and preprocessing
"""

import os
import requests
import pandas as pd
from config import DATA_CSV_FILE, HOWTO_FILE, DATA_CSV_URL, HOWTO_URL
from utils import print_section


def download_data_file(file_name, data_url):
    """Download data file from URL if not exists"""
    if not os.path.exists(file_name):
        try:
            print(f"Attempting to download {file_name} from {data_url}...")
            response = requests.get(data_url)
            response.raise_for_status()
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"✅ {file_name} downloaded successfully!")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to download {file_name}. Please ensure the URL is correct and accessible.\nError: {e}")
    else:
        print(f"✅ {file_name} already exists.")


def download_required_files():
    """Download all required data files"""
    download_data_file(DATA_CSV_FILE, DATA_CSV_URL)
    download_data_file(HOWTO_FILE, HOWTO_URL)


def load_and_explore_data(csv_path):
    """Load and display dataset overview"""
    print_section("📊 DATASET OVERVIEW")
    
    df = pd.read_csv(csv_path)
    print(f"\n✅ Data loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head(10))
    print(f"\nColumn names and types:")
    print(df.dtypes)
    print(f"\nData summary:")
    print(df.describe())
    
    return df


def preprocess_data(df):
    """Clean and preprocess data"""
    df_clean = df.copy()
    
    print_section("📋 COLUMN ANALYSIS")
    
    print("\nColumn names:")
    for i, col in enumerate(df_clean.columns, 1):
        print(f"  {i}. '{col}' ({df_clean[col].dtype})")
    
    print(f"\n🔍 Missing values:")
    print(df_clean.isnull().sum())
    
    df_clean.columns = df_clean.columns.str.strip()
    
    print(f"\n✅ Data preprocessing complete. Shape: {df_clean.shape}")
    print(f"\n📊 Cleaned columns:")
    print(df_clean.columns.tolist())
    
    return df_clean
