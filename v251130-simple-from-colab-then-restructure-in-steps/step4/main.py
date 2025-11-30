"""Main execution script - Step 4.

This step adds the Visualization Module. We verify that we can generate
static and interactive plots based on the analyzed data.
"""
from config import (
    DATA_CSV_FILE, ENABLE_DATA_PROCESSING, ENABLE_TIME_SERIES,
    ENABLE_STATIC_PLOTS, ENABLE_DASHBOARDS
)
from utils import clean_outputs, print_section
import data
import analysis
import visualization

def test_visualization_module():
    print_section("STEP 4: VISUALIZATION MODULE TEST")
    
    clean_outputs()
    
    # 1. Load & Analyze (Reusing previous steps)
    if ENABLE_DATA_PROCESSING and ENABLE_TIME_SERIES:
        data.download_required_files()
        df = data.load_and_explore_data(DATA_CSV_FILE)
        df_clean = data.preprocess_data(df)
        
        results = analysis.aggregate_time_series(df_clean)
        df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly = results
        
        # 2. Static Visualizations
        if ENABLE_STATIC_PLOTS:
            print("\nTesting static visualizations...")
            visualization.create_overview_visualizations(df_yearly, df_clean)
            visualization.create_heatmap(df_clean)
            
        # 3. Interactive Dashboards
        if ENABLE_DASHBOARDS:
            print("\nTesting interactive dashboards...")
            visualization.create_interactive_dashboard(ts_years, ts_data, df_yearly, df_clean)
            visualization.create_heatmap_interactive(df_model_yearly)
            
        print(f"\n✅ Step 4 Complete: Visualizations generated in 'outputs' directory.")

if __name__ == "__main__":
    test_visualization_module()
