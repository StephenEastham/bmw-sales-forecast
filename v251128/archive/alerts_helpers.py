"""
Archived: alerts_helpers (moved from active pipeline)
"""

import numpy as np
from config import (
    TEST_OVERALL_FORECAST_LOW, TEST_MODEL_UNDERPERFORMANCE,
    TEST_REGION_DECLINE, TEST_DECLINING_TREND, DECLINE_THRESHOLD
)

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
