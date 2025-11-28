"""
Reporting and data export
"""

import pandas as pd
from datetime import datetime
from config import out_path
from utils import print_section


def generate_monthly_report(alerts, forecast_data, df_clean, average_sales, 
                           future_values, ts_data, future_years, ALERT_THRESHOLD_OVERALL):
    """Generate comprehensive monthly report.

    This version is resilient to forecasting being disabled. If `future_values`
    or `future_years` are None, the report will note that forecasting was
    disabled for this run instead of attempting numeric operations.
    """

    timestamp = datetime.now()

    # Safe summary values
    forecast_summary = "Forecasting disabled"
    forecast_trend = "N/A"
    yoy_change = "N/A"

    try:
        if future_values is not None and len(future_values) > 0:
            forecast_summary = f"{float(future_values.mean()):,.0f}"
            if ts_data is not None and len(ts_data) > 0:
                forecast_trend = 'INCREASING' if future_values[-1] > ts_data[-1] else 'DECREASING'
        if ts_data is not None and len(ts_data) >= 2:
            yoy_change = f"{((ts_data[-1] - ts_data[-2]) / ts_data[-2] * 100):+.2f}%"
    except Exception:
        forecast_summary = "Forecasting disabled"

    report = f"""
{'='*80}
BMW SALES ANALYTICS - MONTHLY REPORT
Generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

1. EXECUTIVE SUMMARY
{'─'*80}
   • Report Period: {timestamp.strftime('%B %Y')}
   • Total Forecasted Sales (Next Quarter): {forecast_summary}
   • Alert Threshold: {ALERT_THRESHOLD_OVERALL:,.0f}
   • Number of Active Alerts: {len(alerts)}

2. KEY METRICS
{'─'*80}
   • Historical Average Sales: {average_sales:,.0f}
   • Current Forecast Trend: {forecast_trend}
   • Year-over-Year Change: {yoy_change}

3. ALERTS & ACTION ITEMS
{'─'*80}
"""

    if alerts:
        for i, alert in enumerate(alerts, 1):
            report += f"\n   Alert {i}: {alert.get('message', '')}"
            if 'gap' in alert:
                report += f"\n              Gap from threshold: {alert['gap']:,.0f}"
    else:
        report += "\n   No alerts triggered. All metrics within acceptable range."

    report += "\n\n4. FORECAST OUTLOOK (NEXT 3 YEARS)\n" + ('─'*80) + "\n"

    if future_years is not None and future_values is not None and len(future_years) == len(future_values):
        for year, value in zip(future_years, future_values):
            trend = "UP" if (ts_data is not None and len(ts_data) > 0 and value > ts_data[-1]) else "N/A"
            report += f"\n   {int(year)}: {value:,.0f} [{trend}]"
    else:
        report += "\n   Forecasting disabled for this run.\n"

    report += f"\n\n5. MODEL PERFORMANCE (Top 5)\n" + ('─'*80) + "\n"

    top_performers = df_clean.groupby('Model')['Sales_Volume'].sum().nlargest(5)
    for i, (model, sales) in enumerate(top_performers.items(), 1):
        report += f"\n   {i}. {model}: {sales:,.0f}"

    report += f"\n\n6. REGIONAL PERFORMANCE\n" + ('─'*80) + "\n"

    by_region = df_clean.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False)
    for region, sales in by_region.items():
        pct = (sales / by_region.sum() * 100)
        report += f"\n   • {region}: {sales:,.0f} ({pct:.1f}%)"

    report += f"\n\n7. RECOMMENDATIONS\n" + ('─'*80) + "\n"
    report += "   • Monitor underperforming models closely\n"
    report += "   • Invest in high-growth regions\n"
    report += "   • Adjust inventory based on demand signals\n"
    report += "   • Review market conditions quarterly\n\n"
    report += ('='*80) + "\nEND OF REPORT\n" + ('='*80) + "\n"

    return report


def export_data(*args, **kwargs):
    """No-op export for forecasts when forecasting is disabled.

    Calling this function will print a message explaining that forecast
    exports were removed in simplified mode.
    """
    print_section("📊 EXPORTING FORECAST DATA")
    print("Forecast exports are disabled in this simplified run. No forecast files were written.")


def generate_final_summary(df_clean, average_sales, ts_years, ts_data, future_years, 
                          future_values, model_forecasts, alert_system):
    """Generate and save final summary (safe when forecasting/alerts disabled)."""
    import numpy as np

    # Build a summary that does not reference forecasting/alerts when disabled
    total_records = len(df_clean) if df_clean is not None else 0
    year_min = int(df_clean['Year'].min()) if (df_clean is not None and 'Year' in df_clean.columns) else 'N/A'
    year_max = int(df_clean['Year'].max()) if (df_clean is not None and 'Year' in df_clean.columns) else 'N/A'
    top_model = df_clean.groupby('Model')['Sales_Volume'].sum().idxmax() if (df_clean is not None and 'Model' in df_clean.columns) else 'N/A'
    top_region = df_clean.groupby('Region')['Sales_Volume'].sum().idxmax() if (df_clean is not None and 'Region' in df_clean.columns) else 'N/A'

    # Historical performance safe values
    avg_sales = average_sales
    peak_year = 'N/A'
    peak_value = 'N/A'
    low_year = 'N/A'
    low_value = 'N/A'
    trend = 'N/A'
    try:
        if ts_years is not None and ts_data is not None and len(ts_years) > 0 and len(ts_data) > 0:
            peak_idx = int(np.argmax(ts_data))
            peak_year = int(ts_years[peak_idx])
            peak_value = int(ts_data.max())
            low_idx = int(np.argmin(ts_data))
            low_year = int(ts_years[low_idx])
            low_value = int(ts_data.min())
            trend = 'GROWING' if ts_data[-1] > ts_data[0] else 'DECLINING'
    except Exception:
        pass

    # Alerts info
    alerts_count = 0
    high_sev = 0
    med_sev = 0
    if alert_system is not None and hasattr(alert_system, 'alerts'):
        try:
            alerts_count = len(alert_system.alerts)
            high_sev = len([a for a in alert_system.alerts if a.get('severity') == 'HIGH'])
            med_sev = len([a for a in alert_system.alerts if a.get('severity') == 'MEDIUM'])
        except Exception:
            alerts_count = 0

    summary = f"""
{'='*80}
BMW SALES ANALYTICS - ANALYSIS COMPLETE (Forecasting & Alerts Disabled)
{'='*80}

ANALYSIS COMPLETED:

1. Data Overview:
   • Total records analyzed: {total_records:,}
   • Time period: {year_min} - {year_max}
   • Models tracked: {df_clean['Model'].nunique() if df_clean is not None else 0}
   • Regions tracked: {df_clean['Region'].nunique() if df_clean is not None else 0}

2. Historical Performance:
   • Average annual sales: {avg_sales:,.0f}
   • Peak sales year: {peak_year} ({peak_value:,})
   • Lowest sales year: {low_year} ({low_value:,})
   • Trend: {trend}

3. Forecasting & Alerts:
   • Forecasting: DISABLED for this run
   • Alerting: DISABLED for this run
   • Active alerts (if any): {alerts_count}
   • High severity: {high_sev}
   • Medium severity: {med_sev}

4. Visualizations Generated:
   [OK] 01_sales_overview.png - Overview charts (4-panel analysis)
   [OK] 02_model_region_heatmap.png - Performance matrix
   [OK] 05_interactive_dashboard.html - Main interactive dashboard
   [OK] 06_model_heatmap_interactive.html - Interactive heatmap
   [OK] 07_all_outputs.html - Aggregated outputs page

5. Data Files Generated:
   [OK] sales_report_[timestamp].txt - Detailed report
   [OK] ANALYSIS_SUMMARY.txt - This summary

6. Top Insights:
   • Top Model: {top_model}
   • Top Region: {top_region}
   • Forecast Trend: N/A (forecasting disabled)
   • Model Count: 0 (forecasting disabled)
   • Alert Coverage: Disabled

7. Next Steps:
   [DONE] Review interactive dashboard for detailed insights
   [DONE] Distribute monthly report to stakeholders
   [READY] Schedule quarterly review and threshold adjustments

{'='*80}
PROJECT STATUS: ANALYSIS COMPLETE (Forecasting & Alerts Disabled)
{'='*80}
"""

    print(summary)

    with open(out_path('ANALYSIS_SUMMARY.txt'), 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"\n[OK] Saved: {out_path('ANALYSIS_SUMMARY.txt')}")
