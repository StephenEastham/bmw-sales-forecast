"""Reporting module.

Generates text reports and summaries of the analysis.
"""
import numpy as np
from datetime import datetime
from config import out_path

def generate_monthly_report(df_clean, average_sales):
    timestamp = datetime.now()
    report = ('='*80) + '\n' + 'BMW SALES ANALYTICS - MONTHLY REPORT' + '\n' + f'Generated: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}' + '\n' + ('='*80) + '\n\n'
    report += '1. EXECUTIVE SUMMARY\n' + ('-'*80) + '\n'
    report += f'   • Report Period: {timestamp.strftime("%B %Y")}\n'
    report += '   • Number of Active Alerts: 0 (alerting disabled)\n\n'
    report += '2. KEY METRICS\n' + ('-'*80) + '\n'
    report += f'   • Historical Average Sales: {average_sales:,.0f}\n'
    report += '   • Year-over-Year Change: N/A\n\n'
    report += '3. ALERTS & ACTION ITEMS\n' + ('-'*80) + '\n'
    report += '   No alerts configured for this simplified run.\n\n'
    report += '\n5. MODEL PERFORMANCE (Top 5)\n' + ('-'*80) + '\n'
    top_performers = df_clean.groupby('Model')['Sales_Volume'].sum().nlargest(5)
    for i, (model, sales) in enumerate(top_performers.items(), 1):
        report += f'   {i}. {model}: {sales:,.0f}\n'
    report += '\n6. REGIONAL PERFORMANCE\n' + ('-'*80) + '\n'
    by_region = df_clean.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False)
    for region, sales in by_region.items():
        pct = (sales / by_region.sum() * 100)
        report += f'   • {region}: {sales:,.0f} ({pct:.1f}%)\n'
    report += '\n7. RECOMMENDATIONS\n' + ('-'*80) + '\n'
    report += '   • Monitor underperforming models closely\n'
    report += '   • Invest in high-growth regions\n'
    report += '   • Adjust inventory based on demand signals\n'
    report += '   • Review market conditions quarterly\n\n'
    report += ('='*80) + '\nEND OF REPORT\n' + ('='*80) + '\n'
    return report

def generate_final_summary(df_clean, average_sales, ts_years, ts_data):
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
     summary = ('='*80) + '\n' + 'BMW SALES ANALYTICS - ANALYSIS COMPLETE' + '\n' + ('='*80) + '\n\n'
     summary += f'ANALYSIS COMPLETED:\n\n1. Data Overview:\n    • Total records analyzed: {total_records:,}\n    • Time period: {year_min} - {year_max}\n    • Models tracked: {df_clean["Model"].nunique() if df_clean is not None else 0}\n    • Regions tracked: {df_clean["Region"].nunique() if df_clean is not None else 0}\n\n'
     summary += f'2. Historical Performance:\n    • Average annual sales: {avg_sales:,.0f}\n    • Peak sales year: {peak_year} ({peak_value:,})\n    • Lowest sales year: {low_year} ({low_value:,})\n    • Trend: {trend}\n\n'
     summary += '3. Visualizations Generated:\n    [OK] 01_sales_overview.png - Overview charts (4-panel analysis)\n    [OK] 02_model_region_heatmap.png - Performance matrix\n    [OK] 05_interactive_dashboard.html - Main interactive dashboard\n    [OK] 06_model_heatmap_interactive.html - Interactive heatmap\n    [OK] 07_all_outputs.html - Aggregated outputs page\n\n'
     summary += '4. Data Files Generated:\n    [OK] sales_report_[timestamp].txt - Detailed report\n    [OK] ANALYSIS_SUMMARY.txt - This summary\n\n'
     summary += f'5. Top Insights:\n    • Top Model: {top_model}\n    • Top Region: {top_region}\n\n'
     summary += ('='*80) + '\nPROJECT STATUS: ANALYSIS COMPLETE (Forecasting & Alerts Removed)\n' + ('='*80) + '\n'
     print(summary)
     with open(out_path('ANALYSIS_SUMMARY.txt'), 'w', encoding='utf-8') as f:
          f.write(summary)
     print(f"\n[OK] Saved: {out_path('ANALYSIS_SUMMARY.txt')}")
