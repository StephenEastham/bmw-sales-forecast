"""
BM Sales Trend Forecasting & Alert System - Main Entry Point

This script orchestrates the complete analysis pipeline:
- Deletes existing items in outputs directory
- Data loading and preprocessing
- Exploratory data analysis
- Time series forecasting
- Reporting and visualization
- HTML aggregation and browser automation
- Zips all outputs into one .zip file.
"""

import sys
import numpy as np
from config import (
    DATA_CSV_FILE, out_path,
    ENABLE_DATA_PROCESSING, ENABLE_TIME_SERIES, ENABLE_STATIC_PLOTS,
    ENABLE_REPORTING, ENABLE_DASHBOARDS, ENABLE_AGGREGATOR,
    ENABLE_EXPLORATORY_ANALYSIS
)
from utils import print_section, clean_outputs, zip_all_outputs
from data import download_required_files, load_and_explore_data, preprocess_data
from analysis import aggregate_time_series
from exploratory_analysis import exploratory_data_analysis
from viz_static import create_overview_visualizations, create_heatmap
from viz_interactive import create_interactive_dashboard, create_heatmap_interactive
from reporting import generate_monthly_report, generate_final_summary
from aggregator import create_aggregator_html
from datetime import datetime


def main():
    """Main execution function"""
    print_section("BMW SALES TREND SYSTEM")
    
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version.splitlines()[0]}")

    # Initialize variables to None/Empty to handle feature flags
    df = None
    df_clean = None
    df_yearly = None
    ts_data = None
    ts_years = None
    df_model_yearly = None
    
    # Clean output directory before starting
    clean_outputs()

    # ===== DATA LOADING & PREPROCESSING =====
    if ENABLE_DATA_PROCESSING:
        download_required_files()
        df = load_and_explore_data(DATA_CSV_FILE)
        df_clean = preprocess_data(df)
        
        if ENABLE_EXPLORATORY_ANALYSIS:
            exploratory_data_analysis(df_clean)
    
    # ===== TIME SERIES AGGREGATION =====
    if ENABLE_TIME_SERIES:
        df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly = aggregate_time_series(df_clean)
    
    # ===== STATIC VISUALIZATIONS =====
    if ENABLE_STATIC_PLOTS:
        create_overview_visualizations(df_yearly, df_clean)
        create_heatmap(df_clean)

    # ===== REPORTING & VISUALIZATION =====
    if ENABLE_REPORTING:
        # Ensure we have necessary data or defaults
        average_sales = df_yearly['Total_Sales'].mean() if df_yearly is not None else 0
        
        # Create dummy data for reporting if missing
        monthly_report = generate_monthly_report(df_clean, average_sales)
        print(monthly_report)
        
        report_filename = out_path(f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(monthly_report)
        print(f"\n✅ Saved: {report_filename}")
    
    # ===== INTERACTIVE DASHBOARDS =====
    if ENABLE_DASHBOARDS:
        create_interactive_dashboard(ts_years, ts_data, df_yearly, df_clean)
        create_heatmap_interactive(df_model_yearly)
    
    # ===== AGGREGATOR & BROWSER =====
    if ENABLE_AGGREGATOR:
        create_aggregator_html()
        zip_all_outputs()
    
    # ===== FINAL SUMMARY =====
    if ENABLE_REPORTING:
        average_sales = df_yearly['Total_Sales'].mean() if df_yearly is not None else 0
        
        # Create dummy data for summary if missing
        if ts_data is None:
            ts_data = np.array([0, 0])
        if ts_years is None:
            ts_years = np.array([2020, 2021])

        generate_final_summary(df_clean, average_sales, ts_years, ts_data)
    
    print("\n" + "="*80)
    print("SUCCESS: All tasks completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
