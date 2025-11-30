"""Main execution script - Step 5.

This step adds the Reporting Module. We verify that we can generate
text reports and summaries based on the analyzed data.
"""
import numpy as np
from datetime import datetime
from config import (
    DATA_CSV_FILE, ENABLE_DATA_PROCESSING, ENABLE_TIME_SERIES,
    ENABLE_STATIC_PLOTS, ENABLE_DASHBOARDS, ENABLE_REPORTING, out_path
)
from utils import clean_outputs, print_section
import data
import analysis
import visualization
import reporting

def test_reporting_module():
    print_section("STEP 5: REPORTING MODULE TEST")
    
    clean_outputs()
    
    # 1. Load & Analyze (Reusing previous steps)
    if ENABLE_DATA_PROCESSING and ENABLE_TIME_SERIES:
        data.download_required_files()
        df = data.load_and_explore_data(DATA_CSV_FILE)
        df_clean = data.preprocess_data(df)
        
        results = analysis.aggregate_time_series(df_clean)
        df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly = results
        
        # 2. Visualizations (Reusing previous steps)
        if ENABLE_STATIC_PLOTS:
            visualization.create_overview_visualizations(df_yearly, df_clean)
            visualization.create_heatmap(df_clean)
            
        if ENABLE_DASHBOARDS:
            visualization.create_interactive_dashboard(ts_years, ts_data, df_yearly, df_clean)
            visualization.create_heatmap_interactive(df_model_yearly)
            
        # 3. Reporting
        if ENABLE_REPORTING:
            print("\nTesting reporting module...")
            
            # Ensure we have necessary data or defaults
            average_sales = df_yearly['Total_Sales'].mean() if df_yearly is not None else 0

            # Create monthly report
            monthly_report = reporting.generate_monthly_report(df_clean, average_sales)
            print(monthly_report)

            report_filename = out_path(f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(monthly_report)
            print(f"\n✅ Saved: {report_filename}")
            
            # Create final summary
            if ts_data is None:
                ts_data = np.array([0, 0])
            if ts_years is None:
                ts_years = np.array([2020, 2021])

            reporting.generate_final_summary(df_clean, average_sales, ts_years, ts_data)
            
        print(f"\n✅ Step 5 Complete: Reports generated in 'outputs' directory.")

if __name__ == "__main__":
    test_reporting_module()
