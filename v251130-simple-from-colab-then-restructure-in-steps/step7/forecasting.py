"""Forecasting module.

Implements simple forecasting logic.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import out_path
from utils import print_section

def simple_forecast(df_yearly, years_to_forecast=3):
    print_section("🔮 SIMPLE FORECASTING")
    
    # Prepare data
    X = df_yearly['Year'].values
    y = df_yearly['Total_Sales'].values
    
    # Simple Linear Regression (y = mx + c)
    # Using numpy.polyfit for simplicity (degree 1)
    slope, intercept = np.polyfit(X, y, 1)
    
    print(f"Linear Trend: Sales = {slope:.2f} * Year + {intercept:.2f}")
    
    # Forecast
    last_year = int(X.max())
    future_years = np.arange(last_year + 1, last_year + 1 + years_to_forecast)
    future_sales = slope * future_years + intercept
    
    # Create forecast DataFrame
    df_forecast = pd.DataFrame({
        'Year': future_years,
        'Forecast_Sales': future_sales
    })
    
    print("\n📅 Forecast Results:")
    print(df_forecast)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(X, y, 'o-', label='Historical Data')
    plt.plot(future_years, future_sales, 'x--', color='red', label='Forecast')
    
    # Plot trend line for historical part too
    plt.plot(X, slope * X + intercept, ':', color='gray', alpha=0.5, label='Trend Line')
    
    plt.title('Sales Forecast (Linear Trend)')
    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.legend()
    plt.grid(True)
    
    output_file = out_path('08_sales_forecast.png')
    plt.savefig(output_file)
    plt.close()
    print(f"\n✅ Forecast plot saved to: {output_file}")
    
    return df_forecast
