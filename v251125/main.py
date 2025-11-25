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
    DECLINE_THRESHOLD, OVERALL_THRESHOLD_MULTIPLIER, out_path
)
from utils import print_section
from data import download_required_files, load_and_explore_data, preprocess_data
from analysis import exploratory_data_analysis, aggregate_time_series
from visualization import (
    create_overview_visualizations, create_heatmap, visualize_forecast,
    forecast_model_specific, create_interactive_dashboard, create_heatmap_interactive
)
from forecasting import forecast_with_arima
from alerts import setup_alert_system
from reporting import generate_monthly_report, export_data, generate_final_summary
from aggregator import create_aggregator_html
from datetime import datetime


def run_alert_checks(alert_system, future_values, model_forecasts, df_region_yearly,
                     ALERT_THRESHOLD_OVERALL, model_thresholds, region_thresholds,
                     unique_regions, latest_year):
    """Run all alert checks and return populated alert system"""
    overall_alerts = alert_system.check_overall_forecast(future_values, ALERT_THRESHOLD_OVERALL)
    alert_system.alerts.extend(overall_alerts)
    
    for model, forecast_data in model_forecasts.items():
        model_alerts = alert_system.check_model_performance(
            forecast_data, model, 
            model_thresholds.get(model, ALERT_THRESHOLD_OVERALL)
        )
        alert_system.alerts.extend(model_alerts)
        
        decline_alerts = alert_system.check_declining_trend(
            forecast_data['historical'], model, decline_threshold=DECLINE_THRESHOLD
        )
        alert_system.alerts.extend(decline_alerts)
    
    for region in unique_regions:
        region_latest = df_region_yearly[
            (df_region_yearly['Region'] == region) & 
            (df_region_yearly['Year'] == latest_year)
        ]['Sales_Volume'].values
        
        if len(region_latest) > 0:
            region_threshold = region_thresholds.get(region, ALERT_THRESHOLD_OVERALL)
            if region_latest[0] < region_threshold:
                alert_system.alerts.append({
                    'type': 'REGION_UNDERPERFORMANCE',
                    'severity': 'MEDIUM',
                    'region': region,
                    'message': f'ALERT: Region {region} sales ({region_latest[0]:,.0f}) '
                               f'below threshold ({region_threshold:,.0f})',
                })
    
    return alert_system


def inject_test_metrics(future_values, model_forecasts, df_region_yearly,
                        ALERT_THRESHOLD_OVERALL, model_thresholds, region_thresholds,
                        latest_year, unique_regions, top_models):
    """Inject bad metrics for testing alert system"""
    print("\n" + "🧪 TEST MODE ENABLED - Injecting bad metrics for alert testing")
    
    print("\n" + "="*80)
    print("🧪 TEST MODE: INJECTING BAD METRICS")
    print("="*80)
    
    original_future_values = future_values.copy()
    
    # Scenario 1: Make overall forecast drop below threshold
    if TEST_OVERALL_FORECAST_LOW:
        future_values_test = np.array([
            ALERT_THRESHOLD_OVERALL * 0.6,
            ALERT_THRESHOLD_OVERALL * 0.7,
            ALERT_THRESHOLD_OVERALL * 0.5
        ])
        future_values = future_values_test
        print(f"\n✓ Overall Forecast: Set to 50-70% of threshold")
        print(f"  Original: {original_future_values}")
        print(f"  Test: {future_values_test}")
    
    # Scenario 2: Make top models underperform
    if TEST_MODEL_UNDERPERFORMANCE:
        for model in top_models:
            model_forecasts[model]['historical'] = model_forecasts[model]['historical'].copy()
            model_forecasts[model]['historical'][-1] = model_thresholds[model] * 0.5
            print(f"✓ Model '{model}': Recent sales reduced to 50% of threshold")
    
    # Scenario 3: Create steep regional decline
    if TEST_REGION_DECLINE:
        for region in unique_regions:
            df_region_yearly.loc[
                (df_region_yearly['Region'] == region) & 
                (df_region_yearly['Year'] == latest_year), 
                'Sales_Volume'
            ] = region_thresholds[region] * 0.5
        print(f"✓ Regional Sales: Set to 50% of threshold for latest year")
    
    # Scenario 4: Create declining trend
    if TEST_DECLINING_TREND:
        for model in top_models[:2]:
            if model in model_forecasts:
                hist = model_forecasts[model]['historical'].copy()
                if len(hist) >= 2:
                    hist[-1] = hist[-2] * 0.8
                    model_forecasts[model]['historical'] = hist
                    print(f"✓ Model '{model}': Created 20% decline in recent years")
    
    print("\n" + "="*80)
    print("All test metrics injected. Re-running alert checks below...")
    print("="*80)
    
    return future_values


def main():
    """Main execution function"""
    print_section("BMW SALES TREND FORECASTING & ALERT SYSTEM")
    
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version.splitlines()[0]}")
    
    # ===== DATA LOADING & PREPROCESSING =====
    download_required_files()
    df = load_and_explore_data(DATA_CSV_FILE)
    df_clean = preprocess_data(df)
    exploratory_data_analysis(df_clean)
    
    # ===== TIME SERIES AGGREGATION =====
    df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly = aggregate_time_series(df_clean)
    
    # ===== STATIC VISUALIZATIONS =====
    create_overview_visualizations(df_yearly, df_clean)
    create_heatmap(df_clean)
    
    # ===== ARIMA FORECASTING =====
    train_size, forecast_test_values, forecast_test_ci, future_values, future_years, future_ci = \
        forecast_with_arima(ts_data, ts_years)
    visualize_forecast(ts_data, ts_years, train_size, forecast_test_values, forecast_test_ci, 
                      future_values, future_years, future_ci)
    
    # ===== MODEL-SPECIFIC FORECASTS =====
    top_models = df_clean.groupby('Model')['Sales_Volume'].sum().nlargest(5).index.tolist()
    model_forecasts = forecast_model_specific(df_model_yearly, top_models, {})
    
    # ===== ALERT SYSTEM SETUP =====
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
    create_interactive_dashboard(ts_years, ts_data, future_years, future_values, 
                                 df_yearly, df_clean)
    create_heatmap_interactive(df_model_yearly)
    
    # ===== DATA EXPORT =====
    export_data(future_years, future_values, ALERT_THRESHOLD_OVERALL, alert_system, 
                model_forecasts, model_thresholds, df_clean)
    
    # ===== AGGREGATOR & BROWSER =====
    create_aggregator_html()
    
    # ===== FINAL SUMMARY =====
    generate_final_summary(df_clean, average_sales, ts_years, ts_data, future_years, 
                          future_values, model_forecasts, alert_system)
    
    print("\n" + "="*80)
    print("SUCCESS: All tasks completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
