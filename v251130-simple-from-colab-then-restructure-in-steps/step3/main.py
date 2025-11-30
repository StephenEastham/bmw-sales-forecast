"""Main execution script - Step 3.

This step adds the Analysis Module. We verify that we can perform
time series aggregation and statistical analysis on the loaded data.
"""
from config import DATA_CSV_FILE, ENABLE_DATA_PROCESSING, ENABLE_TIME_SERIES, ENABLE_EXPLORATORY_ANALYSIS
from utils import clean_outputs, print_section
import data
import analysis

def test_analysis_module():
    print_section("STEP 3: ANALYSIS MODULE TEST")
    
    clean_outputs()
    
    # 1. Load Data (Reusing Step 2)
    if ENABLE_DATA_PROCESSING:
        data.download_required_files()
        df = data.load_and_explore_data(DATA_CSV_FILE)
        df_clean = data.preprocess_data(df)
        
        # 2. Run Exploratory Analysis
        if ENABLE_EXPLORATORY_ANALYSIS:
            analysis.exploratory_data_analysis(df_clean)

        # 3. Run Time Series Analysis
        if ENABLE_TIME_SERIES:
            print("\nTesting time series aggregation...")
            results = analysis.aggregate_time_series(df_clean)
            df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly = results
            
            print(f"\n✅ Step 3 Complete: Analysis finished.")
            print(f"   Yearly Data Shape: {df_yearly.shape}")
            print(f"   Time Series Points: {len(ts_data)}")
            return results

if __name__ == "__main__":
    test_analysis_module()
