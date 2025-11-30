"""Main execution script - Step 6.

This step adds the Aggregator Module. We verify that we can collect all
generated outputs into a single HTML index page and zip archive.
This completes the modularization process.
"""
import numpy as np
from datetime import datetime
from config import (
    DATA_CSV_FILE, ENABLE_DATA_PROCESSING, ENABLE_TIME_SERIES,
    ENABLE_STATIC_PLOTS, ENABLE_DASHBOARDS, ENABLE_REPORTING,
    ENABLE_AGGREGATOR, out_path
)
from utils import clean_outputs, print_section, zip_all_outputs
import data
import analysis
import visualization
import reporting
import aggregator

def test_full_pipeline():
    print_section("STEP 6: FULL PIPELINE & AGGREGATOR TEST")
    
    clean_outputs()
    
    # 1. Load & Analyze
    if ENABLE_DATA_PROCESSING and ENABLE_TIME_SERIES:
        data.download_required_files()
        df = data.load_and_explore_data(DATA_CSV_FILE)
        df_clean = data.preprocess_data(df)
        
        results = analysis.aggregate_time_series(df_clean)
        df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly = results
        
        # 2. Visualizations
        if ENABLE_STATIC_PLOTS:
            visualization.create_overview_visualizations(df_yearly, df_clean)
            visualization.create_heatmap(df_clean)
            
        if ENABLE_DASHBOARDS:
            visualization.create_interactive_dashboard(ts_years, ts_data, df_yearly, df_clean)
            visualization.create_heatmap_interactive(df_model_yearly)
            
        # 3. Reporting
        if ENABLE_REPORTING:
            average_sales = df_yearly['Total_Sales'].mean() if df_yearly is not None else 0
            monthly_report = reporting.generate_monthly_report(df_clean, average_sales)
            
            report_filename = out_path(f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(monthly_report)
            
            if ts_data is None: ts_data = np.array([0, 0])
            if ts_years is None: ts_years = np.array([2020, 2021])
            reporting.generate_final_summary(df_clean, average_sales, ts_years, ts_data)
            
        # 4. Aggregation
        if ENABLE_AGGREGATOR:
            print("\nTesting aggregator module...")
            aggregator.create_aggregator_html()
            zip_all_outputs()
            
        print(f"\n✅ Step 6 Complete: Full pipeline executed successfully.")

if __name__ == "__main__":
    test_full_pipeline()
