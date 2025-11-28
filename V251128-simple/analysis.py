"""
Exploratory Data Analysis and time series aggregation
"""

import numpy as np
from utils import print_section


def aggregate_time_series(df_clean):
    """Aggregate data for time series analysis"""
    print_section("📈 TIME SERIES AGGREGATION")
    
    df_yearly = df_clean.groupby('Year')['Sales_Volume'].sum().reset_index()
    df_yearly = df_yearly.sort_values('Year')
    df_yearly.columns = ['Year', 'Total_Sales']
    
    print(f"\n✅ Yearly Sales Aggregation:")
    print(df_yearly)
    
    ts_data = df_yearly['Total_Sales'].values
    ts_years = df_yearly['Year'].values
    
    print(f"\n📊 Time Series Summary:")
    print(f"   Total years: {len(ts_years)}")
    print(f"   Date range: {ts_years[0]:.0f} - {ts_years[-1]:.0f}")
    print(f"   Average annual sales: {ts_data.mean():,.0f}")
    print(f"   Peak sales: {ts_data.max():,.0f} (Year {ts_years[np.argmax(ts_data)]:.0f})")
    print(f"   Lowest sales: {ts_data.min():,.0f} (Year {ts_years[np.argmin(ts_data)]:.0f})")
    
    df_yearly['YoY_Growth'] = df_yearly['Total_Sales'].pct_change() * 100
    
    print(f"\n📊 Year-over-Year Growth:")
    print(df_yearly[['Year', 'Total_Sales', 'YoY_Growth']].to_string(index=False))
    
    df_model_yearly = df_clean.groupby(['Year', 'Model'])['Sales_Volume'].sum().reset_index()
    df_region_yearly = df_clean.groupby(['Year', 'Region'])['Sales_Volume'].sum().reset_index()
    
    print(f"\n✅ Model and Region time series aggregations complete")
    
    return df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly
