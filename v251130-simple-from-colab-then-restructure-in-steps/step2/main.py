"""Main execution script - Step 2.

This step adds the Data Module. We verify that we can download,
load, and preprocess the data using the infrastructure from Step 1.
"""
from config import DATA_CSV_FILE, ENABLE_DATA_PROCESSING
from utils import clean_outputs, print_section
import data

def test_data_module():
    print_section("STEP 2: DATA MODULE TEST")
    
    clean_outputs()
    
    if ENABLE_DATA_PROCESSING:
        # 1. Download
        print("\nTesting data download...")
        data.download_required_files()
        
        # 2. Load
        print("\nTesting data loading...")
        df = data.load_and_explore_data(DATA_CSV_FILE)
        
        # 3. Preprocess
        print("\nTesting data preprocessing...")
        df_clean = data.preprocess_data(df)
        
        print(f"\n✅ Step 2 Complete: Data loaded and cleaned. Shape: {df_clean.shape}")
        return df_clean

if __name__ == "__main__":
    test_data_module()
