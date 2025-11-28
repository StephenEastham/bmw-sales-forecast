"""
Reporting and data export
"""

import pandas as pd
from datetime import datetime
from config import out_path
from utils import print_section


def generate_monthly_report(df_clean, average_sales):
    """Generate a monthly report."""

    timestamp = datetime.now()

    report = f"""
{'='*80}
BMW SALES ANALYTICS - MONTHLY REPORT
Generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

1. EXECUTIVE SUMMARY
{'─'*80}
   • Report Period: {timestamp.strftime('%B %Y')}
   • Number of Active Alerts: 0 (alerting disabled)

2. KEY METRICS
{'─'*80}
   • Historical Average Sales: {average_sales:,.0f}
   • Year-over-Year Change: N/A

3. ALERTS & ACTION ITEMS
{'─'*80}
   No alerts configured for this simplified run.
"""

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



def generate_final_summary(df_clean, average_sales, ts_years, ts_data):
     """Create summary of data processing/analysis."""
     import numpy as np

     total_records = len(df_clean) if df_clean is not None else 0
     year_min = int(df_clean['Year'].min()) if (df_clean is not None and 'Year' in df_clean.columns) else 'N/A'
     year_max = int(df_clean['Year'].max()) if (df_clean is not None and 'Year' in df_clean.columns) else 'N/A'
     top_model = df_clean.groupby('Model')['Sales_Volume'].sum().idxmax() if (df_clean is not None and 'Model' in df_clean.columns) else 'N/A'
     top_region = df_clean.groupby('Region')['Sales_Volume'].sum().idxmax() if (df_clean is not None and 'Region' in df_clean.columns) else 'N/A'

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

     summary = f"""
{'='*80}
BMW SALES ANALYTICS - ANALYSIS COMPLETE
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

3. Visualizations Generated:
    [OK] 01_sales_overview.png - Overview charts (4-panel analysis)
    [OK] 02_model_region_heatmap.png - Performance matrix
    [OK] 05_interactive_dashboard.html - Main interactive dashboard
    [OK] 06_model_heatmap_interactive.html - Interactive heatmap
    [OK] 07_all_outputs.html - Aggregated outputs page

4. Data Files Generated:
    [OK] sales_report_[timestamp].txt - Detailed report
    [OK] ANALYSIS_SUMMARY.txt - This summary

5. Top Insights:
    • Top Model: {top_model}
    • Top Region: {top_region}

{'='*80}
PROJECT STATUS: ANALYSIS COMPLETE (Forecasting & Alerts Removed)
{'='*80}
"""

     print(summary)

     with open(out_path('ANALYSIS_SUMMARY.txt'), 'w', encoding='utf-8') as f:
          f.write(summary)

     print(f"\n[OK] Saved: {out_path('ANALYSIS_SUMMARY.txt')}")
