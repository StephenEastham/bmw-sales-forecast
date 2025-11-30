"""Data module.

Handles downloading, loading, and preprocessing of the dataset.
"""
import os
import requests
import pandas as pd
from utils import print_section
from config import DATA_CSV_FILE, DATA_CSV_URL

def download_data_file(file_name, data_url):
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
    download_data_file(DATA_CSV_FILE, DATA_CSV_URL)

def load_and_explore_data(csv_path):
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
    df_clean = df.copy()
    print_section("📋 COLUMN ANALYSIS")
    print('\nColumn names:')
    for i, col in enumerate(df_clean.columns, 1):
        print(f"  {i}. '{col}' ({df_clean[col].dtype})")
    print(f"\n🔍 Missing values:")
    print(df_clean.isnull().sum())
    df_clean.columns = df_clean.columns.str.strip()
    empty_columns = []
    for col in df_clean.columns:
        non_na = ~df_clean[col].isna()
        if non_na.any():
            non_empty = df_clean.loc[non_na, col].astype(str).str.strip() != ''
            has_values = non_empty.any()
        else:
            has_values = False
        if not has_values:
            empty_columns.append(col)
    if empty_columns:
        print("\n⚠️ Warning: The following columns contain empty values:")
        for c in empty_columns:
            print(f"  - {c}")
        print("Consider dropping or filling these columns before further processing.")
    else:
        print("\n✅ No empty columns found. All columns contain at least one non-empty value.")
    print(f"\n✅ Data preprocessing complete. Shape: {df_clean.shape}")
    print(f"\n📊 Cleaned columns:")
    print(df_clean.columns.tolist())
    return df_clean
