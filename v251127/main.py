"""
BM Sales Trend Forecasting & Alert System - Main Entry Point

This script orchestrates the complete analysis pipeline:
- Data loading and preprocessing
- Exploratory data analysis
- Time series forecasting
- Alert system
- Reporting and visualization
- HTML aggregation and browser automation
"""

import sys
import numpy as np
from config import (
    TEST_MODE, TEST_OVERALL_FORECAST_LOW, TEST_MODEL_UNDERPERFORMANCE,
    TEST_REGION_DECLINE, TEST_DECLINING_TREND, DATA_CSV_FILE, HOWTO_FILE,
    DECLINE_THRESHOLD, OVERALL_THRESHOLD_MULTIPLIER, out_path,
    ENABLE_DATA_PROCESSING, ENABLE_TIME_SERIES, ENABLE_STATIC_PLOTS,
    ENABLE_ARIMA_FORECAST, ENABLE_MODEL_FORECASTS, ENABLE_ALERTS,
    ENABLE_REPORTING, ENABLE_DASHBOARDS, ENABLE_EXPORTS, ENABLE_AGGREGATOR,
    ENABLE_EXPLORATORY_ANALYSIS
)
from utils import print_section
from data import download_required_files, load_and_explore_data, preprocess_data
from analysis import aggregate_time_series
from exploratory_analysis import exploratory_data_analysis
from visualization import (
    create_overview_visualizations, create_heatmap, visualize_forecast,
    forecast_model_specific, create_interactive_dashboard, create_heatmap_interactive
)
from forecasting import forecast_with_arima
from alerts import setup_alert_system
from alerts_helpers import run_alert_checks, inject_test_metrics
from reporting import generate_monthly_report, export_data, generate_final_summary
from aggregator import create_aggregator_html
from datetime import datetime


def main():
    """Main execution function"""
    print_section("BMW SALES TREND FORECASTING & ALERT SYSTEM")
    
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version.splitlines()[0]}")
    
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
    
    # ===== ARIMA FORECASTING =====
    if ENABLE_ARIMA_FORECAST:
        train_size, forecast_test_values, forecast_test_ci, future_values, future_years, future_ci = \
            forecast_with_arima(ts_data, ts_years)
        visualize_forecast(ts_data, ts_years, train_size, forecast_test_values, forecast_test_ci, 
                        future_values, future_years, future_ci)
    
    # ===== MODEL-SPECIFIC FORECASTS =====
    if ENABLE_MODEL_FORECASTS:
        top_models = df_clean.groupby('Model')['Sales_Volume'].sum().nlargest(5).index.tolist()
        model_forecasts = forecast_model_specific(df_model_yearly, top_models, {})
    
    # ===== ALERT SYSTEM SETUP =====
    if ENABLE_ALERTS:
        alert_system, ALERT_THRESHOLD_OVERALL, model_thresholds, region_thresholds, unique_regions = \
            setup_alert_system(df_clean, df_yearly, top_models)
        
        # ===== RUN ALERT CHECKS =====
        latest_year = df_region_yearly['Year'].max()
        alert_system = run_alert_checks(
            alert_system, future_values, model_forecasts, df_region_yearly,
            ALERT_THRESHOLD_OVERALL, model_thresholds, region_thresholds,
            unique_regions, latest_year
        )
        alert_system.generate_alert_report()
        print(f"\n✅ Alert system initialized with {len(alert_system.alerts)} alerts")
        
        # ===== TEST MODE: INJECT BAD METRICS =====
        if TEST_MODE:
            future_values = inject_test_metrics(
                future_values, model_forecasts, df_region_yearly,
                ALERT_THRESHOLD_OVERALL, model_thresholds, region_thresholds,
                latest_year, unique_regions, top_models
            )
            
            # Re-run alert checks with injected data
            alert_system.alerts = []
            alert_system = run_alert_checks(
                alert_system, future_values, model_forecasts, df_region_yearly,
                ALERT_THRESHOLD_OVERALL, model_thresholds, region_thresholds,
                unique_regions, latest_year
            )
            alert_system.generate_alert_report()
            print(f"\n✅ Alert system re-initialized with {len(alert_system.alerts)} TRIGGERED ALERTS")
    
    # ===== REPORTING & VISUALIZATION =====
    if ENABLE_REPORTING:
        average_sales = df_yearly['Total_Sales'].mean()
        monthly_report = generate_monthly_report(
            alert_system.alerts, model_forecasts, df_clean, average_sales, 
            future_values, ts_data, future_years, ALERT_THRESHOLD_OVERALL
        )
        print(monthly_report)
        
        report_filename = out_path(f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(monthly_report)
        print(f"\n✅ Saved: {report_filename}")
    
    # ===== INTERACTIVE DASHBOARDS =====
    if ENABLE_DASHBOARDS:
        create_interactive_dashboard(ts_years, ts_data, future_years, future_values, 
                                    df_yearly, df_clean)
        create_heatmap_interactive(df_model_yearly)
    
    # ===== DATA EXPORT =====
    if ENABLE_EXPORTS:
        export_data(future_years, future_values, ALERT_THRESHOLD_OVERALL, alert_system, 
                    model_forecasts, model_thresholds, df_clean)
    
    # ===== AGGREGATOR & BROWSER =====
    if ENABLE_AGGREGATOR:
        create_aggregator_html()
    
    # ===== FINAL SUMMARY =====
    if ENABLE_REPORTING:
        generate_final_summary(df_clean, average_sales, ts_years, ts_data, future_years, 
                            future_values, model_forecasts, alert_system)
    
    print("\n" + "="*80)
    print("SUCCESS: All tasks completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
