"""
BMW Sales Trend Forecasting & Alert System

This script analyzes historical BMW sales data (2010-2024) and implements:
- Sales Trend Analysis by model, region, and year
- Time Series Forecasting using ARIMA models
- Interactive Dashboards for data visualization
- Automated Alert System for underperforming models/regions
- Monthly Reporting with actionable insights

Key Objectives:
1. Identify which models are declining and need action
2. Predict inventory needs and market demand
3. Create early warning system for sales dips
4. Automate monthly reports and alerts
"""

import sys
import os
import requests
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import logging
import glob
from pathlib import Path
import webbrowser

# Time series and forecasting
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Plotting libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuration
warnings.filterwarnings('ignore')
matplotlib.use('Agg')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)


def print_system_info():
    """Print Python environment information"""
    print("Notebook sys.executable:", sys.executable)
    print("Notebook sys.version:", sys.version.splitlines()[0])


def download_data_file(file_name, data_url):
    """Download data file from URL if not exists"""
    if not os.path.exists(file_name):
        try:
            print(f"Attempting to download {file_name} from {data_url}...")
            response = requests.get(data_url)
            response.raise_for_status()
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"[OK] {file_name} downloaded successfully!")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to download {file_name}. Error: {e}")
    else:
        print(f"[OK] {file_name} already exists.")


def load_and_explore_data(csv_path):
    """Load and display dataset overview"""
    print("="*80)
    print("[DATA] DATASET OVERVIEW")
    print("="*80)
    
    df = pd.read_csv(csv_path)
    print(f"\n[OK] Data loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head(10))
    print(f"\nColumn names and types:")
    print(df.dtypes)
    print(f"\nData summary:")
    print(df.describe())
    
    return df


def preprocess_data(df):
    """Clean and preprocess data"""
    df_clean = df.copy()
    
    print("\n" + "="*80)
    print("[INFO] COLUMN ANALYSIS")
    print("="*80)
    print("\nColumn names:")
    for i, col in enumerate(df_clean.columns, 1):
        print(f"  {i}. '{col}' ({df_clean[col].dtype})")
    
    print(f"\n[FIND] Missing values:")
    print(df_clean.isnull().sum())
    
    df_clean.columns = df_clean.columns.str.strip()
    
    print(f"\n[OK] Data preprocessing complete. Shape: {df_clean.shape}")
    print(f"\n[DATA] Cleaned columns:")
    print(df_clean.columns.tolist())
    
    return df_clean


def exploratory_data_analysis(df_clean):
    """Perform EDA"""
    print("\n" + "="*80)
    print("[DATA] EXPLORATORY DATA ANALYSIS")
    print("="*80)
    
    print("\n[MODEL] Sales by Model (Top 10):")
    model_sales = df_clean.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=False)
    print(model_sales.head(10))
    
    print("\n[REGION] Sales by Region:")
    region_sales = df_clean.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False)
    print(region_sales)
    
    print("\n[TREND] Sales Volume Statistics:")
    print(df_clean['Sales_Volume'].describe())


def aggregate_time_series(df_clean):
    """Aggregate data for time series analysis"""
    print("\n" + "="*80)
    print("[TREND] TIME SERIES AGGREGATION")
    print("="*80)
    
    df_yearly = df_clean.groupby('Year')['Sales_Volume'].sum().reset_index()
    df_yearly = df_yearly.sort_values('Year')
    df_yearly.columns = ['Year', 'Total_Sales']
    
    print(f"\n[OK] Yearly Sales Aggregation:")
    print(df_yearly)
    
    ts_data = df_yearly['Total_Sales'].values
    ts_years = df_yearly['Year'].values
    
    print(f"\n[DATA] Time Series Summary:")
    print(f"   Total years: {len(ts_years)}")
    print(f"   Average annual sales: {ts_data.mean():,.0f}")
    print(f"   Peak sales: {ts_data.max():,.0f}")
    print(f"   Lowest sales: {ts_data.min():,.0f}")
    
    df_yearly['YoY_Growth'] = df_yearly['Total_Sales'].pct_change() * 100
    df_model_yearly = df_clean.groupby(['Year', 'Model'])['Sales_Volume'].sum().reset_index()
    df_region_yearly = df_clean.groupby(['Year', 'Region'])['Sales_Volume'].sum().reset_index()
    
    return df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly


def create_overview_visualizations(df_yearly, df_clean):
    """Create static overview visualizations"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('BMW Sales Overview (2010-2024)', fontsize=16, fontweight='bold')
    
    # 1. Overall Sales Trend
    ax1 = axes[0, 0]
    ax1.plot(df_yearly['Year'], df_yearly['Total_Sales'], marker='o', linewidth=2.5, 
             markersize=8, color='#1f77b4', label='Total Sales')
    ax1.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Sales', fontsize=11, fontweight='bold')
    ax1.set_title('Total Sales Trend', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 2. Year-over-Year Growth Rate
    ax2 = axes[0, 1]
    colors = ['green' if x > 0 else 'red' for x in df_yearly['YoY_Growth'].fillna(0)]
    ax2.bar(df_yearly['Year'][1:], df_yearly['YoY_Growth'][1:], color=colors[1:], alpha=0.7)
    ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Growth Rate (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Year-over-Year Growth Rate', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Sales by Model (Top 10)
    ax3 = axes[1, 0]
    model_total = df_clean.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=True).tail(10)
    model_total.plot(kind='barh', ax=ax3, color='#ff7f0e', alpha=0.8)
    ax3.set_xlabel('Total Sales', fontsize=11, fontweight='bold')
    ax3.set_title('Top 10 Models by Sales', fontsize=12, fontweight='bold')
    
    # 4. Sales by Region
    ax4 = axes[1, 1]
    region_total = df_clean.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False)
    colors_region = plt.cm.Set3(np.linspace(0, 1, len(region_total)))
    ax4.pie(region_total, labels=region_total.index, autopct='%1.1f%%', colors=colors_region)
    ax4.set_title('Sales Distribution by Region', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('01_sales_overview.png', dpi=300, bbox_inches='tight')
    print("[OK] Saved: 01_sales_overview.png")
    plt.show()


def create_heatmap(df_clean):
    """Create model-region heatmap"""
    heatmap_data = df_clean.pivot_table(
        values='Sales_Volume',
        index='Model',
        columns='Region',
        aggfunc='sum',
        fill_value=0
    )
    
    heatmap_data = heatmap_data.loc[heatmap_data.sum(axis=1).nlargest(15).index]
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Sales'})
    plt.title('Sales Heatmap: Model vs Region (Top 15 Models)', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Region', fontsize=12, fontweight='bold')
    plt.ylabel('Model', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('02_model_region_heatmap.png', dpi=300, bbox_inches='tight')
    print("[OK] Saved: 02_model_region_heatmap.png")
    plt.show()


def forecast_with_arima(ts_data, ts_years):
    """Forecast using ARIMA model"""
    print("\n" + "="*80)
    print("[AI] ARIMA TIME SERIES FORECASTING")
    print("="*80)
    
    train_size = int(len(ts_data) * 0.8)
    train_data = ts_data[:train_size]
    test_data = ts_data[train_size:]
    
    try:
        arima_model = ARIMA(train_data, order=(1, 1, 1))
        arima_results = arima_model.fit()
        
        forecast_test = arima_results.get_forecast(steps=len(test_data))
        forecast_test_values = forecast_test.predicted_mean.values
        forecast_test_ci = forecast_test.conf_int()
        
        full_model = ARIMA(ts_data, order=(1, 1, 1))
        full_results = full_model.fit()
        future_forecast = full_results.get_forecast(steps=3)
        future_values = future_forecast.predicted_mean.values
        future_ci = future_forecast.conf_int()
        future_years = np.array([ts_years[-1] + i for i in range(1, 4)])
        
    except Exception as e:
        print(f"[WARNING] ARIMA error: {e}")
        try:
            model = ExponentialSmoothing(train_data, trend='add', seasonal=None)
            results = model.fit()
            forecast_test_values = results.forecast(steps=len(test_data))
            
            full_model = ExponentialSmoothing(ts_data, trend='add', seasonal=None)
            full_results = full_model.fit()
            future_values = full_results.forecast(steps=3)
            future_years = np.array([ts_years[-1] + i for i in range(1, 4)])
            forecast_test_ci = None
            future_ci = None
            
        except Exception as e2:
            print(f"[WARNING] Fallback error: {e2}")
            future_values = np.repeat(ts_data[-1], 3)
            future_years = np.array([ts_years[-1] + i for i in range(1, 4)])
            forecast_test_values = None
            forecast_test_ci = None
            future_ci = None
    
    return train_size, forecast_test_values, forecast_test_ci, future_values, future_years, future_ci


def visualize_forecast(ts_data, ts_years, train_size, forecast_test_values, forecast_test_ci, 
                       future_values, future_years, future_ci):
    """Visualize forecast results"""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(ts_years, ts_data, marker='o', linewidth=2.5, markersize=8, 
            label='Historical Sales', color='#1f77b4')
    
    test_years = ts_years[train_size:]
    if forecast_test_values is not None:
        ax.plot(test_years, forecast_test_values, marker='s', linestyle='--', 
                linewidth=2, markersize=6, label='Test Forecast', color='#ff7f0e', alpha=0.8)
    
    ax.plot(future_years, future_values, marker='^', linestyle=':', linewidth=2.5, 
            markersize=10, label='Future Forecast', color='#2ca02c')
    
    ax.axvline(x=ts_years[train_size-1], color='red', linestyle='--', alpha=0.5, 
               label='Train/Test Split')
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sales', fontsize=12, fontweight='bold')
    ax.set_title('BMW Total Sales: Historical Data & ARIMA Forecast', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('03_arima_forecast.png', dpi=300, bbox_inches='tight')
    print("[OK] Saved: 03_arima_forecast.png")
    plt.show()


def main():
    """Main execution function"""
    print("="*80)
    print("BMW SALES TREND FORECASTING & ALERT SYSTEM")
    print("="*80)
    
    print_system_info()
    
    download_data_file('BMW-sales-data-2010-2024.csv',
                      'https://raw.githubusercontent.com/StephenEastham/bmw-sales-forecast/refs/heads/main/BMW-sales-data-2010-2024.csv')
    
    df = load_and_explore_data('BMW-sales-data-2010-2024.csv')
    df_clean = preprocess_data(df)
    exploratory_data_analysis(df_clean)
    
    df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly = aggregate_time_series(df_clean)
    
    create_overview_visualizations(df_yearly, df_clean)
    create_heatmap(df_clean)
    
    train_size, forecast_test_values, forecast_test_ci, future_values, future_years, future_ci = \
        forecast_with_arima(ts_data, ts_years)
    visualize_forecast(ts_data, ts_years, train_size, forecast_test_values, forecast_test_ci, 
                      future_values, future_years, future_ci)
    
    print("\n" + "="*80)
    print("SUCCESS: Analysis completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
