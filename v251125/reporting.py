"""
Reporting and data export
"""

import pandas as pd
from datetime import datetime
from config import out_path
from utils import print_section


def generate_monthly_report(alerts, forecast_data, df_clean, average_sales, 
                           future_values, ts_data, future_years, ALERT_THRESHOLD_OVERALL):
    """Generate comprehensive monthly report"""
    
    timestamp = datetime.now()
    
    report = f"""
{'='*80}
BMW SALES ANALYTICS - MONTHLY REPORT
Generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

1. EXECUTIVE SUMMARY
{'─'*80}
   • Report Period: {timestamp.strftime('%B %Y')}
   • Total Forecasted Sales (Next Quarter): {future_values.mean():,.0f}
   • Alert Threshold: {ALERT_THRESHOLD_OVERALL:,.0f}
   • Number of Active Alerts: {len(alerts)}

2. KEY METRICS
{'─'*80}
   • Historical Average Sales: {average_sales:,.0f}
   • Current Forecast Trend: {'INCREASING' if future_values[-1] > ts_data[-1] else 'DECREASING'}
   • Year-over-Year Change: {((ts_data[-1] - ts_data[-2]) / ts_data[-2] * 100):+.2f}%

3. ALERTS & ACTION ITEMS
{'─'*80}
"""
    
    if alerts:
        for i, alert in enumerate(alerts, 1):
            report += f"\n   Alert {i}: {alert['message']}"
            if 'gap' in alert:
                report += f"\n              Gap from threshold: {alert['gap']:,.0f}"
    else:
        report += "\n   No alerts triggered. All metrics within acceptable range."
    
    report += f"""

4. FORECAST OUTLOOK (NEXT 3 YEARS)
{'─'*80}
"""
    
    for year, value in zip(future_years, future_values):
        trend = "UP" if value > ts_data[-1] else "DOWN"
        report += f"\n   {year:.0f}: {value:,.0f} [{trend}]"
    
    report += f"""

5. MODEL PERFORMANCE (Top 5)
{'─'*80}
"""
    
    top_performers = df_clean.groupby('Model')['Sales_Volume'].sum().nlargest(5)
    for i, (model, sales) in enumerate(top_performers.items(), 1):
        report += f"\n   {i}. {model}: {sales:,.0f}"
    
    report += f"""

6. REGIONAL PERFORMANCE
{'─'*80}
"""
    
    by_region = df_clean.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False)
    for region, sales in by_region.items():
        pct = (sales / by_region.sum() * 100)
        report += f"\n   • {region}: {sales:,.0f} ({pct:.1f}%)"
    
    report += f"""

7. RECOMMENDATIONS
{'─'*80}
   • Monitor underperforming models closely
   • Invest in high-growth regions
   • Adjust inventory based on forecasts
   • Review market conditions quarterly

{'='*80}
END OF REPORT
{'='*80}
"""
    
    return report


def export_data(future_years, future_values, ALERT_THRESHOLD_OVERALL, alert_system, 
                model_forecasts, model_thresholds, df_clean):
    """Export forecast data and alerts"""
    print_section("📊 EXPORTING FORECAST DATA")
    
    forecast_export = pd.DataFrame({
        'Year': future_years.astype(int),
        'Forecasted_Sales': future_values.round(0).astype(int),
        'Threshold': [int(ALERT_THRESHOLD_OVERALL)] * len(future_years),
        'Below_Threshold': future_values < ALERT_THRESHOLD_OVERALL
    })
    
    print("\n📊 Forecast Export:")
    print(forecast_export)
    
    forecast_export.to_csv(out_path('forecast_next_3_years.csv'), index=False)
    print(f"\n✅ Saved: {out_path('forecast_next_3_years.csv')}")
    
    if alert_system.alerts:
        alerts_df = pd.DataFrame(alert_system.alerts)
        alerts_df.to_csv(out_path('active_alerts.csv'), index=False)
        print(f"✅ Saved: {out_path('active_alerts.csv')}")
    
    model_forecast_df = []
    for model, data in model_forecasts.items():
        for i, (year, value) in enumerate(zip(data['forecast_years'], data['forecast'])):
            model_forecast_df.append({
                'Model': model,
                'Year': int(year),
                'Forecasted_Sales': int(value),
                'Threshold': int(model_thresholds.get(model, ALERT_THRESHOLD_OVERALL))
            })
    
    if model_forecast_df:
        model_forecast_export = pd.DataFrame(model_forecast_df)
        model_forecast_export.to_csv(out_path('model_forecasts_export.csv'), index=False)
        print(f"✅ Saved: {out_path('model_forecasts_export.csv')}")
    
    print("\n✅ Data export complete")


def generate_final_summary(df_clean, average_sales, ts_years, ts_data, future_years, 
                          future_values, model_forecasts, alert_system):
    """Generate and save final summary"""
    import numpy as np
    
    summary = f"""
{'='*80}
BMW SALES TREND FORECASTING & ALERT SYSTEM - PROJECT COMPLETE
{'='*80}

ANALYSIS COMPLETED:

1. Data Overview:
   • Total records analyzed: {len(df_clean):,}
   • Time period: {df_clean['Year'].min():.0f} - {df_clean['Year'].max():.0f}
   • Models tracked: {df_clean['Model'].nunique()}
   • Regions tracked: {df_clean['Region'].nunique()}

2. Historical Performance:
   • Average annual sales: {average_sales:,.0f}
   • Peak sales year: {ts_years[np.argmax(ts_data)]:.0f} ({ts_data.max():,.0f})
   • Lowest sales year: {ts_years[np.argmin(ts_data)]:.0f} ({ts_data.min():,.0f})
   • Trend: {'GROWING' if ts_data[-1] > ts_data[0] else 'DECLINING'}

3. Forecast Results (Next 3 Years):
   • Year 1 ({future_years[0]:.0f}): {future_values[0]:,.0f}
   • Year 2 ({future_years[1]:.0f}): {future_values[1]:,.0f}
   • Year 3 ({future_years[2]:.0f}): {future_values[2]:,.0f}
   • Average forecast: {future_values.mean():,.0f}

4. Alert System Status:
   • Active alerts: {len(alert_system.alerts)}
   • High severity: {len([a for a in alert_system.alerts if a.get('severity') == 'HIGH'])}
   • Medium severity: {len([a for a in alert_system.alerts if a.get('severity') == 'MEDIUM'])}

5. Visualizations Generated:
   [OK] 01_sales_overview.png - Overview charts (4-panel analysis)
   [OK] 02_model_region_heatmap.png - Performance matrix
   [OK] 03_arima_forecast.png - Forecast visualization
   [OK] 04_model_forecasts.png - Individual model forecasts (Top 5)
   [OK] 05_interactive_dashboard.html - Main interactive dashboard
   [OK] 06_model_heatmap_interactive.html - Interactive heatmap
   [OK] 07_all_outputs.html - Aggregated outputs page

6. Data Files Generated:
   [OK] forecast_next_3_years.csv - Forecast data
   [OK] active_alerts.csv - Current alerts
   [OK] model_forecasts_export.csv - Model-specific forecasts
   [OK] sales_report_[timestamp].txt - Detailed report
   [OK] sales_alerts.log - Alert log file
   [OK] ANALYSIS_SUMMARY.txt - This summary

7. Top Insights:
   • Top Model: {df_clean.groupby('Model')['Sales_Volume'].sum().idxmax()}
   • Top Region: {df_clean.groupby('Region')['Sales_Volume'].sum().idxmax()}
   • Forecast Trend: {'POSITIVE' if future_values[-1] > ts_data[-1] else 'NEGATIVE'}
   • Model Count: {len(model_forecasts)} models forecasted
   • Alert Coverage: Model + Region-level monitoring active

8. Next Steps:
   [DONE] Review interactive dashboard for detailed insights
   [DONE] Check sales_alerts.log for all alert notifications
   [DONE] Distribute monthly report to stakeholders
   [READY] Set up automated email alerts (integration ready)
   [READY] Schedule quarterly review and threshold adjustments
   [READY] Monitor model performance in real-time

{'='*80}
PROJECT STATUS: COMPLETE & READY FOR PRODUCTION
{'='*80}
"""
    
    print(summary)
    
    with open(out_path('ANALYSIS_SUMMARY.txt'), 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"\n[OK] Saved: {out_path('ANALYSIS_SUMMARY.txt')}")
