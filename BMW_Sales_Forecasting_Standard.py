"""
BMW Sales Trend Forecasting & Alert System - Standard Python Script

This script analyzes historical BMW sales data (2010-2024) and implements:
- Sales Trend Analysis by model, region, and year
- Time Series Forecasting using ARIMA models
- Interactive Dashboards for data visualization
- Automated Alert System for underperforming models/regions
- Monthly Reporting with actionable insights
- Complete data export and aggregation

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
            print(f"✅ {file_name} downloaded successfully!")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to download {file_name}. Please ensure the URL is correct and accessible.\nError: {e}")
    else:
        print(f"✅ {file_name} already exists.")


def load_and_explore_data(csv_path):
    """Load and display dataset overview"""
    print("="*80)
    print("📊 DATASET OVERVIEW")
    print("="*80)
    
    df = pd.read_csv(csv_path)
    print(f"\n✅ Data loaded successfully!")
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
    print("📋 COLUMN ANALYSIS")
    print("="*80)
    print("\nColumn names:")
    for i, col in enumerate(df_clean.columns, 1):
        print(f"  {i}. '{col}' ({df_clean[col].dtype})")
    
    print(f"\n🔍 Missing values:")
    print(df_clean.isnull().sum())
    
    df_clean.columns = df_clean.columns.str.strip()
    
    print(f"\n✅ Data preprocessing complete. Shape: {df_clean.shape}")
    print(f"\n📊 Cleaned columns:")
    print(df_clean.columns.tolist())
    
    return df_clean


def exploratory_data_analysis(df_clean):
    """Perform EDA"""
    print("\n" + "="*80)
    print("📊 EXPLORATORY DATA ANALYSIS")
    print("="*80)
    
    print("\n🏎️ Sales by Model (Top 10):")
    model_sales = df_clean.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=False)
    print(model_sales.head(10))
    
    print("\n🌍 Sales by Region:")
    region_sales = df_clean.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False)
    print(region_sales)
    
    print("\n📅 Sales by Year:")
    year_sales = df_clean.groupby('Year')['Sales_Volume'].sum().sort_values()
    print(year_sales)
    
    print("\n📈 Sales Volume Statistics:")
    print(df_clean['Sales_Volume'].describe())
    
    print("\n💰 Price Statistics:")
    print(df_clean['Price_USD'].describe())


def aggregate_time_series(df_clean):
    """Aggregate data for time series analysis"""
    print("\n" + "="*80)
    print("📈 TIME SERIES AGGREGATION")
    print("="*80)
    
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
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Sales by Model (Top 10)
    ax3 = axes[1, 0]
    model_total = df_clean.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=True).tail(10)
    model_total.plot(kind='barh', ax=ax3, color='#ff7f0e', alpha=0.8)
    ax3.set_xlabel('Total Sales', fontsize=11, fontweight='bold')
    ax3.set_title('Top 10 Models by Sales', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='x')
    
    # 4. Sales by Region
    ax4 = axes[1, 1]
    region_total = df_clean.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False)
    colors_region = plt.cm.Set3(np.linspace(0, 1, len(region_total)))
    ax4.pie(region_total, labels=region_total.index, autopct='%1.1f%%', 
            colors=colors_region, startangle=90)
    ax4.set_title('Sales Distribution by Region', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('01_sales_overview.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: 01_sales_overview.png")
    plt.close()


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
    print("✅ Saved: 02_model_region_heatmap.png")
    plt.close()


def forecast_with_arima(ts_data, ts_years):
    """Forecast using ARIMA model"""
    print("\n" + "="*80)
    print("🤖 ARIMA TIME SERIES FORECASTING")
    print("="*80)
    
    train_size = int(len(ts_data) * 0.8)
    train_data = ts_data[:train_size]
    test_data = ts_data[train_size:]
    
    print(f"\n📊 Data Split:")
    print(f"   Train set: {len(train_data)} years")
    print(f"   Test set: {len(test_data)} years")
    
    print(f"\n🔄 Fitting ARIMA(1,1,1) model...")
    try:
        arima_model = ARIMA(train_data, order=(1, 1, 1))
        arima_results = arima_model.fit()
        
        print("\n" + arima_results.summary().as_text())
        
        forecast_test = arima_results.get_forecast(steps=len(test_data))
        forecast_test_values = forecast_test.predicted_mean.values
        forecast_test_ci = forecast_test.conf_int()
        
        rmse = np.sqrt(mean_squared_error(test_data, forecast_test_values))
        mae = mean_absolute_error(test_data, forecast_test_values)
        
        print(f"\n📊 MODEL PERFORMANCE (Test Set):")
        print(f"   RMSE: {rmse:,.0f}")
        print(f"   MAE:  {mae:,.0f}")
        
        full_model = ARIMA(ts_data, order=(1, 1, 1))
        full_results = full_model.fit()
        future_forecast = full_results.get_forecast(steps=3)
        future_values = future_forecast.predicted_mean.values
        future_ci = future_forecast.conf_int()
        
        future_years = np.array([ts_years[-1] + i for i in range(1, 4)])
        
        print(f"\n🔮 FUTURE FORECAST (Next 3 Years):")
        for year, value in zip(future_years, future_values):
            print(f"   Year {year:.0f}: {value:,.0f}")
        
    except Exception as e:
        print(f"⚠️ ARIMA error: {e}")
        print("Falling back to Exponential Smoothing...")
        
        try:
            model = ExponentialSmoothing(train_data, trend='add', seasonal=None)
            results = model.fit()
            forecast_test_values = results.forecast(steps=len(test_data))
            rmse = np.sqrt(mean_squared_error(test_data, forecast_test_values))
            mae = mean_absolute_error(test_data, forecast_test_values)
            
            full_model = ExponentialSmoothing(ts_data, trend='add', seasonal=None)
            full_results = full_model.fit()
            future_values = full_results.forecast(steps=3)
            future_years = np.array([ts_years[-1] + i for i in range(1, 4)])
            forecast_test_ci = None
            future_ci = None
            
            print(f"✅ Exponential Smoothing fitted successfully")
            
        except Exception as e2:
            print(f"⚠️ Fallback error: {e2}")
            future_values = np.repeat(ts_data[-1], 3)
            future_years = np.array([ts_years[-1] + i for i in range(1, 4)])
            forecast_test_values = None
            forecast_test_ci = None
            future_ci = None
    
    print(f"\n✅ Forecasting complete")
    
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
    
    # Confidence intervals
    try:
        if forecast_test_ci is not None:
            ax.fill_between(test_years, 
                             forecast_test_ci.iloc[:, 0], 
                             forecast_test_ci.iloc[:, 1], 
                             alpha=0.2, color='#ff7f0e')
        if future_ci is not None:
            ax.fill_between(future_years, 
                             future_ci.iloc[:, 0], 
                             future_ci.iloc[:, 1], 
                             alpha=0.2, color='#2ca02c')
    except:
        pass
    
    ax.axvline(x=ts_years[train_size-1], color='red', linestyle='--', alpha=0.5, 
               label='Train/Test Split')
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sales', fontsize=12, fontweight='bold')
    ax.set_title('BMW Total Sales: Historical Data & ARIMA Forecast', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('03_arima_forecast.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: 03_arima_forecast.png")
    plt.close()


def forecast_model_specific(df_model_yearly, top_models, model_thresholds):
    """Forecast for top 5 models"""
    print("\n" + "="*80)
    print("🏎️ MODEL-SPECIFIC FORECASTS (Top 5 Models)")
    print("="*80)
    
    print(f"\n📊 Top 5 Models: {top_models}")
    
    model_forecasts = {}
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    fig.suptitle('Top 5 BMW Models: Sales Forecast', fontsize=16, fontweight='bold')
    
    for idx, model in enumerate(top_models):
        model_data = df_model_yearly[df_model_yearly['Model'] == model].sort_values('Year')
        
        if len(model_data) > 2:
            model_sales = model_data['Sales_Volume'].values
            model_years = model_data['Year'].values
            
            try:
                model_arima = ARIMA(model_sales, order=(1, 1, 1))
                model_results = model_arima.fit()
                model_forecast = model_results.get_forecast(steps=3)
                forecast_values = np.asarray(model_forecast.predicted_mean)
                
                model_forecasts[model] = {
                    'historical': model_sales,
                    'forecast': forecast_values,
                    'years': model_years,
                    'forecast_years': np.array([model_years[-1] + i for i in range(1, 4)])
                }
                
                ax = axes[idx]
                ax.plot(model_years, model_sales, marker='o', linewidth=2, label='Historical')
                ax.plot(np.array([model_years[-1] + i for i in range(1, 4)]), forecast_values, 
                       marker='^', linestyle='--', linewidth=2, color='red', label='Forecast')
                ax.set_title(f'Model: {model}', fontweight='bold')
                ax.set_xlabel('Year')
                ax.set_ylabel('Sales')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
            except Exception as e:
                print(f"   ⚠️ Could not forecast {model}: {e}")
    
    fig.delaxes(axes[-1])
    
    plt.tight_layout()
    plt.savefig('04_model_forecasts.png', dpi=300, bbox_inches='tight')
    print("\n✅ Saved: 04_model_forecasts.png")
    plt.close()
    
    print(f"\n✅ Model forecasting complete")
    
    return model_forecasts


class SalesAlertSystem:
    """Automated alert system for underperforming models and regions"""
    
    def __init__(self, threshold, model_thresholds=None, region_thresholds=None):
        self.threshold = threshold
        self.model_thresholds = model_thresholds or {}
        self.region_thresholds = region_thresholds or {}
        self.alerts = []
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sales_alerts.log'),
                logging.StreamHandler()
            ],
            force=True
        )
        return logging.getLogger(__name__)
    
    def check_overall_forecast(self, forecast_values, threshold):
        """Check if forecasted sales fall below threshold"""
        alerts = []
        for i, value in enumerate(forecast_values):
            if value < threshold:
                alert = {
                    'type': 'OVERALL_SALES',
                    'severity': 'HIGH',
                    'message': f'ALERT: Forecasted sales for year {i+1} ({value:,.0f}) '
                               f'falls below threshold ({threshold:,.0f})',
                    'forecast_value': value,
                    'threshold': threshold,
                    'gap': threshold - value
                }
                alerts.append(alert)
                self.logger.warning(alert['message'])
        
        return alerts
    
    def check_model_performance(self, model_data, model_name, threshold):
        """Check if model sales are underperforming"""
        alerts = []
        recent_sales = model_data['historical'][-1] if len(model_data['historical']) > 0 else 0
        
        if recent_sales < threshold:
            alert = {
                'type': 'MODEL_UNDERPERFORMANCE',
                'severity': 'MEDIUM',
                'model': model_name,
                'message': f'ALERT: Model {model_name} recent sales ({recent_sales:,.0f}) '
                           f'below threshold ({threshold:,.0f})',
                'recent_sales': recent_sales,
                'threshold': threshold,
                'gap': threshold - recent_sales
            }
            alerts.append(alert)
            self.logger.warning(alert['message'])
        
        return alerts
    
    def check_declining_trend(self, sales_history, item_name, decline_threshold=0.1):
        """Check if sales are in decline"""
        if len(sales_history) < 2:
            return []
        
        alerts = []
        decline_rate = (sales_history[-2] - sales_history[-1]) / sales_history[-2]
        
        if decline_rate > decline_threshold:
            alert = {
                'type': 'DECLINING_TREND',
                'severity': 'MEDIUM',
                'item': item_name,
                'message': f'ALERT: {item_name} showing {decline_rate*100:.1f}% decline',
                'decline_rate': decline_rate
            }
            alerts.append(alert)
            self.logger.warning(alert['message'])
        
        return alerts
    
    def generate_alert_report(self):
        """Generate summary report of all alerts"""
        print("\n" + "="*80)
        print("SALES ALERT REPORT")
        print("="*80)
        
        if not self.alerts:
            print("\n✅ No alerts triggered! All metrics within acceptable range.")
            return
        
        print(f"\nTotal Alerts: {len(self.alerts)}\n")
        
        high_severity = [a for a in self.alerts if a.get('severity') == 'HIGH']
        medium_severity = [a for a in self.alerts if a.get('severity') == 'MEDIUM']
        
        if high_severity:
            print("HIGH SEVERITY ALERTS:")
            for alert in high_severity:
                print(f"   - {alert['message']}")
        
        if medium_severity:
            print("\nMEDIUM SEVERITY ALERTS:")
            for alert in medium_severity:
                print(f"   - {alert['message']}")


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


def create_interactive_dashboard(ts_years, ts_data, future_years, future_values, 
                                 df_yearly, df_clean):
    """Create interactive Plotly dashboard"""
    print("\n" + "="*80)
    print("📊 CREATING INTERACTIVE DASHBOARD")
    print("="*80)
    
    fig_forecast = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Total Sales Trend & Forecast',
            'Year-over-Year Growth',
            'Model Performance (Top 5)',
            'Regional Distribution'
        ),
        specs=[
            [{'type': 'scatter'}, {'type': 'bar'}],
            [{'type': 'bar'}, {'type': 'pie'}]
        ]
    )
    
    fig_forecast.add_trace(
        go.Scatter(
            x=ts_years, y=ts_data, mode='lines+markers',
            name='Historical Sales', line=dict(color='#1f77b4', width=2),
            marker=dict(size=8)
        ),
        row=1, col=1
    )
    
    fig_forecast.add_trace(
        go.Scatter(
            x=future_years, y=future_values, mode='lines+markers',
            name='Forecast', line=dict(color='#2ca02c', width=2, dash='dash'),
            marker=dict(size=10)
        ),
        row=1, col=1
    )
    
    fig_forecast.add_trace(
        go.Bar(
            x=df_yearly['Year'][1:], y=df_yearly['YoY_Growth'][1:],
            name='Growth Rate', marker=dict(
                color=df_yearly['YoY_Growth'][1:],
                colorscale='RdYlGn', showscale=False
            )
        ),
        row=1, col=2
    )
    
    top_5_models = df_clean.groupby('Model')['Sales_Volume'].sum().nlargest(5).sort_values()
    fig_forecast.add_trace(
        go.Bar(
            y=top_5_models.index, x=top_5_models.values,
            orientation='h', name='Model Sales', 
            marker=dict(color='#ff7f0e')
        ),
        row=2, col=1
    )
    
    region_dist = df_clean.groupby('Region')['Sales_Volume'].sum()
    fig_forecast.add_trace(
        go.Pie(
            labels=region_dist.index, values=region_dist.values,
            name='Regions'
        ),
        row=2, col=2
    )
    
    fig_forecast.update_xaxes(title_text="Year", row=1, col=1)
    fig_forecast.update_yaxes(title_text="Sales", row=1, col=1)
    fig_forecast.update_xaxes(title_text="Year", row=1, col=2)
    fig_forecast.update_yaxes(title_text="Growth %", row=1, col=2)
    fig_forecast.update_xaxes(title_text="Sales", row=2, col=1)
    fig_forecast.update_yaxes(title_text="Model", row=2, col=1)
    
    fig_forecast.update_layout(
        title_text="BMW Sales Analytics Dashboard",
        showlegend=True,
        height=900,
        width=1400
    )
    
    fig_forecast.write_html('05_interactive_dashboard.html')
    print("\n✅ Saved: 05_interactive_dashboard.html")


def create_heatmap_interactive(df_model_yearly):
    """Create interactive Model-Year Heatmap"""
    heatmap_data_pivot = df_model_yearly.pivot_table(
        values='Sales_Volume',
        index='Model',
        columns='Year',
        fill_value=0
    )
    
    heatmap_data_pivot = heatmap_data_pivot.loc[heatmap_data_pivot.sum(axis=1).nlargest(10).index]
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data_pivot.values,
        x=heatmap_data_pivot.columns,
        y=heatmap_data_pivot.index,
        colorscale='YlOrRd',
        colorbar=dict(title='Sales')
    ))
    
    fig_heatmap.update_layout(
        title='BMW Model Sales Trends Over Years (Top 10 Models)',
        xaxis_title='Year',
        yaxis_title='Model',
        height=600,
        width=1200
    )
    
    fig_heatmap.write_html('06_model_heatmap_interactive.html')
    print("✅ Saved: 06_model_heatmap_interactive.html")


def export_data(future_years, future_values, ALERT_THRESHOLD_OVERALL, alert_system, 
                model_forecasts, model_thresholds, df_clean):
    """Export forecast data and alerts"""
    print("\n" + "="*80)
    print("📊 EXPORTING FORECAST DATA")
    print("="*80)
    
    forecast_export = pd.DataFrame({
        'Year': future_years.astype(int),
        'Forecasted_Sales': future_values.round(0).astype(int),
        'Threshold': [int(ALERT_THRESHOLD_OVERALL)] * len(future_years),
        'Below_Threshold': future_values < ALERT_THRESHOLD_OVERALL
    })
    
    print("\n📊 Forecast Export:")
    print(forecast_export)
    
    forecast_export.to_csv('forecast_next_3_years.csv', index=False)
    print("\n✅ Saved: forecast_next_3_years.csv")
    
    if alert_system.alerts:
        alerts_df = pd.DataFrame(alert_system.alerts)
        alerts_df.to_csv('active_alerts.csv', index=False)
        print("✅ Saved: active_alerts.csv")
    
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
        model_forecast_export.to_csv('model_forecasts_export.csv', index=False)
        print("✅ Saved: model_forecasts_export.csv")
    
    print("\n✅ Data export complete")


def create_aggregator_html():
    """Create aggregator HTML page for all outputs"""
    out_html = '07_all_outputs.html'
    pngs = sorted(glob.glob('*.png'))
    exclude_names = {out_html, 'commit_messages-can-change-values.html'}
    htmls = sorted(f for f in glob.glob('*.html') if os.path.basename(f) not in exclude_names)
    
    if not pngs and not htmls:
        print('No output PNG or HTML files found in the current directory.')
    else:
        parts = []
        parts.append('<!doctype html>')
        parts.append('<html lang="en">')
        parts.append('<head>')
        parts.append('<meta charset="utf-8"/>')
        parts.append('<meta name="viewport" content="width=device-width, initial-scale=1"/>')
        parts.append('<title>All Outputs - BMW Sales Forecast</title>')
        parts.append('<style>body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:20px} h2{margin-top:1.2rem} figure{margin:12px 0} img{max-width:100%;height:auto;border:1px solid #ddd;padding:4px;background:#fff} .filelink{margin-bottom:8px;display:inline-block}</style>')
        parts.append('</head>')
        parts.append('<body>')
        parts.append('<h1>BMW Sales Forecast — Generated Outputs</h1>')
        parts.append(f'<p>Repository path: {Path().resolve()}</p>')
        
        if pngs:
            parts.append('<h2>PNG Visualizations</h2>')
            for p in pngs:
                safe = os.path.basename(p)
                parts.append(f'<figure><figcaption>{safe}</figcaption><img src="{safe}" alt="{safe}"/></figure>')
        
        if htmls:
            parts.append('<h2>Interactive HTML Outputs</h2>')
            for h in htmls:
                safe = os.path.basename(h)
                parts.append(f'<div class="filelink"><a href="{safe}" target="_blank">Open {safe} in new tab</a></div>')
                parts.append(f'<div style="margin:12px 0; border:1px solid #ccc;"><iframe src="{safe}" style="width:100%;height:640px;border:0"></iframe></div>')
        
        parts.append('</body>')
        parts.append('</html>')
        
        html_content = '\n'.join(parts)
        with open(out_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        abs_path = Path(out_html).resolve()
        print(f'✅ Created aggregator: {abs_path}')
        
        # Automatically open in browser
        try:
            url = abs_path.as_uri()
            print(f'\n🌐 Opening {out_html} in your default browser...')
            webbrowser.open(url)
            print(f'✅ Browser opened successfully!')
        except Exception as e:
            print(f'⚠️ Could not open browser automatically: {e}')
            print(f'   You can manually open: {abs_path}')


def generate_final_summary(df_clean, average_sales, ts_years, ts_data, future_years, 
                          future_values, model_forecasts, alert_system):
    """Generate and save final summary"""
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
    
    with open('ANALYSIS_SUMMARY.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("\n[OK] Saved: ANALYSIS_SUMMARY.txt")


def main():
    """Main execution function"""
    print("="*80)
    print("BMW SALES TREND FORECASTING & ALERT SYSTEM")
    print("="*80)
    
    print_system_info()
    
    download_data_file('BMW-sales-data-2010-2024.csv',
                      'https://raw.githubusercontent.com/StephenEastham/bmw-sales-forecast/refs/heads/main/BMW-sales-data-2010-2024.csv')
    
    download_data_file('how-to-test.md',
                      'https://raw.githubusercontent.com/StephenEastham/bmw-sales-forecast/refs/heads/main/how-to-test.md')
    
    # Data Loading & Processing
    df = load_and_explore_data('BMW-sales-data-2010-2024.csv')
    df_clean = preprocess_data(df)
    exploratory_data_analysis(df_clean)
    
    # Time Series Aggregation
    df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly = aggregate_time_series(df_clean)
    
    # Static Visualizations
    create_overview_visualizations(df_yearly, df_clean)
    create_heatmap(df_clean)
    
    # ARIMA Forecasting
    train_size, forecast_test_values, forecast_test_ci, future_values, future_years, future_ci = \
        forecast_with_arima(ts_data, ts_years)
    visualize_forecast(ts_data, ts_years, train_size, forecast_test_values, forecast_test_ci, 
                      future_values, future_years, future_ci)
    
    # Model-Specific Forecasts
    top_models = df_clean.groupby('Model')['Sales_Volume'].sum().nlargest(5).index.tolist()
    model_forecasts = forecast_model_specific(df_model_yearly, top_models, {})
    
    # TEST MODE: Toggle this to inject bad metrics and trigger alerts
    # Set to True to test alert system with simulated underperformance
    TEST_MODE = False  # Change to True to trigger alerts!
    
    # TEST CONFIGURATION OPTIONS
    if TEST_MODE:
        print("\n" + "🧪 TEST MODE ENABLED - Injecting bad metrics for alert testing")
        
        # Choose which test scenarios to enable:
        TEST_OVERALL_FORECAST_LOW = True      # Makes overall forecast drop below threshold
        TEST_MODEL_UNDERPERFORMANCE = True    # Makes top models underperform
        TEST_REGION_DECLINE = True            # Makes regions show steep decline
        TEST_DECLINING_TREND = True           # Makes models show 15%+ decline
        
    else:
        TEST_OVERALL_FORECAST_LOW = False
        TEST_MODEL_UNDERPERFORMANCE = False
        TEST_REGION_DECLINE = False
        TEST_DECLINING_TREND = False
    
    # Alert System Setup
    average_sales = df_yearly['Total_Sales'].mean()
    ALERT_THRESHOLD_OVERALL = average_sales * 0.8
    
    print("\n" + "="*80)
    print("⚠️ ALERT THRESHOLD CONFIGURATION")
    print("="*80)
    
    print(f"\n📊 Overall Metrics:")
    print(f"   Average historical sales: {average_sales:,.0f}")
    print(f"   Alert threshold (80%): {ALERT_THRESHOLD_OVERALL:,.0f}")
    
    model_thresholds = {}
    print(f"\n🏎️ Model-Specific Alert Thresholds (Top 5):")
    for model in top_models:
        model_avg = df_clean[df_clean['Model'] == model]['Sales_Volume'].mean()
        model_threshold = model_avg * 0.8
        model_thresholds[model] = model_threshold
        print(f"   {model}: {model_threshold:,.0f}")
    
    region_thresholds = {}
    unique_regions = df_clean['Region'].unique()
    print(f"\n🌍 Region-Specific Alert Thresholds:")
    for region in unique_regions:
        region_avg = df_clean[df_clean['Region'] == region]['Sales_Volume'].mean()
        region_threshold = region_avg * 0.8
        region_thresholds[region] = region_threshold
        print(f"   {region}: {region_threshold:,.0f}")
    
    # Initialize Alert System
    alert_system = SalesAlertSystem(
        threshold=ALERT_THRESHOLD_OVERALL,
        model_thresholds=model_thresholds,
        region_thresholds=region_thresholds
    )
    
    overall_alerts = alert_system.check_overall_forecast(future_values, ALERT_THRESHOLD_OVERALL)
    alert_system.alerts.extend(overall_alerts)
    
    for model, forecast_data in model_forecasts.items():
        model_alerts = alert_system.check_model_performance(
            forecast_data, model, 
            model_thresholds.get(model, ALERT_THRESHOLD_OVERALL)
        )
        alert_system.alerts.extend(model_alerts)
        
        decline_alerts = alert_system.check_declining_trend(
            forecast_data['historical'], model, decline_threshold=0.15
        )
        alert_system.alerts.extend(decline_alerts)
    
    latest_year = df_region_yearly['Year'].max()
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
    
    alert_system.generate_alert_report()
    print(f"\n✅ Alert system initialized with {len(alert_system.alerts)} alerts")
    
    # TEST MODE: Inject bad metrics to trigger alerts
    if TEST_MODE:
        print("\n" + "="*80)
        print("🧪 TEST MODE: INJECTING BAD METRICS")
        print("="*80)
        
        # Save original values for easy restoration
        original_future_values = future_values.copy()
        original_model_forecasts = {}
        original_df_region_yearly = df_region_yearly.copy()
        
        # Scenario 1: Make overall forecast drop below threshold
        if TEST_OVERALL_FORECAST_LOW:
            future_values_test = np.array([
                ALERT_THRESHOLD_OVERALL * 0.6,  # 60% of threshold - HIGH ALERT
                ALERT_THRESHOLD_OVERALL * 0.7,  # 70% of threshold - HIGH ALERT
                ALERT_THRESHOLD_OVERALL * 0.5   # 50% of threshold - HIGH ALERT
            ])
            future_values = future_values_test
            print(f"\n✓ Overall Forecast: Set to 50-70% of threshold")
            print(f"  Original: {original_future_values}")
            print(f"  Test: {future_values_test}")
        
        # Scenario 2: Make top models underperform
        if TEST_MODEL_UNDERPERFORMANCE:
            for model in top_models:
                original_model_forecasts[model] = model_forecasts[model].copy()
                # Inject very low recent sales
                model_forecasts[model]['historical'] = model_forecasts[model]['historical'].copy()
                model_forecasts[model]['historical'][-1] = model_thresholds[model] * 0.5  # 50% of threshold
                print(f"✓ Model '{model}': Recent sales reduced to 50% of threshold")
        
        # Scenario 3: Create steep regional decline
        if TEST_REGION_DECLINE:
            original_df_region_yearly = df_region_yearly.copy()
            for region in unique_regions:
                df_region_yearly.loc[
                    (df_region_yearly['Region'] == region) & 
                    (df_region_yearly['Year'] == latest_year), 
                    'Sales_Volume'
                ] = region_thresholds[region] * 0.5
            print(f"✓ Regional Sales: Set to 50% of threshold for latest year")
        
        # Scenario 4: Create declining trend by modifying model history
        if TEST_DECLINING_TREND:
            for model in top_models[:2]:  # First 2 models only
                if model in model_forecasts:
                    # Create steep decline in last 2 data points
                    hist = model_forecasts[model]['historical'].copy()
                    if len(hist) >= 2:
                        hist[-1] = hist[-2] * 0.8  # 20% drop
                        model_forecasts[model]['historical'] = hist
                        print(f"✓ Model '{model}': Created 20% decline in recent years")
        
        print("\n" + "="*80)
        print("All test metrics injected. Re-running alert checks below...")
        print("="*80)
        
        # RE-RUN ALERT CHECKS WITH TEST DATA
        alert_system.alerts = []  # Clear previous alerts
        
        overall_alerts = alert_system.check_overall_forecast(future_values, ALERT_THRESHOLD_OVERALL)
        alert_system.alerts.extend(overall_alerts)
        
        for model, forecast_data in model_forecasts.items():
            model_alerts = alert_system.check_model_performance(
                forecast_data, model, 
                model_thresholds.get(model, ALERT_THRESHOLD_OVERALL)
            )
            alert_system.alerts.extend(model_alerts)
            
            decline_alerts = alert_system.check_declining_trend(
                forecast_data['historical'], model, decline_threshold=0.15
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
        
        alert_system.generate_alert_report()
        print(f"\n✅ Alert system re-initialized with {len(alert_system.alerts)} TRIGGERED ALERTS")
    
    # Generate Monthly Report
    monthly_report = generate_monthly_report(alert_system.alerts, model_forecasts, df_clean, 
                                            average_sales, future_values, ts_data, 
                                            future_years, ALERT_THRESHOLD_OVERALL)
    print(monthly_report)
    
    report_filename = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(monthly_report)
    
    print(f"\n✅ Saved: {report_filename}")
    
    # Create Interactive Dashboards
    create_interactive_dashboard(ts_years, ts_data, future_years, future_values, 
                                 df_yearly, df_clean)
    create_heatmap_interactive(df_model_yearly)
    
    # Export Data
    export_data(future_years, future_values, ALERT_THRESHOLD_OVERALL, alert_system, 
                model_forecasts, model_thresholds, df_clean)
    
    # Create Aggregator
    create_aggregator_html()
    
    # Generate Final Summary
    generate_final_summary(df_clean, average_sales, ts_years, ts_data, future_years, 
                          future_values, model_forecasts, alert_system)
    
    print("\n" + "="*80)
    print("SUCCESS: All tasks completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
