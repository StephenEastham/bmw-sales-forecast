import os
import pandas as pd
import requests
from typing import Optional

import config
from utils import print_section  # lightweight dependency on utils


def download_data_file(file_name: str, data_url: str | None = None) -> None:
    """Download a file if it does not already exist locally.

    This function avoids downloading if the file is present which is useful
    for iterative development in notebooks.
    """
    if data_url is None:
        data_url = config.DATA_CSV_URL

    if not os.path.exists(file_name):
        print(f"Attempting to download {file_name} from {data_url}...")
        response = requests.get(data_url)
        response.raise_for_status()
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"{file_name} already exists; skipping download")


def download_required_files() -> None:
    """Download any required files for the pipeline (small wrapper)."""
    download_data_file(config.DATA_CSV_FILE, config.DATA_CSV_URL)


def load_and_explore_data(csv_path: str, nrows: int = 10) -> pd.DataFrame:
    """Load CSV into a DataFrame and print a brief overview.

    Side-effects: prints to stdout (this is fine for interactive use).
    Returns: DataFrame
    """
    print_section("DATASET OVERVIEW")
    df = pd.read_csv(csv_path)
    print("Shape:", df.shape)
    print("First rows:")
    print(df.head(nrows))
    print("Dtypes:")
    print(df.dtypes)
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of `df`.

    This minimal implementation trims column names and reports empty columns.
    """
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.strip()
    empty_columns = []
    for col in df_clean.columns:
        non_na = ~df_clean[col].isna()
        if non_na.any():
            non_empty = df_clean.loc[non_na, col].astype(str).str.strip() != ""
            has_values = non_empty.any()
        else:
            has_values = False
        if not has_values:
            empty_columns.append(col)
    if empty_columns:
        print("Warning: empty columns:", empty_columns)
    return df_clean
