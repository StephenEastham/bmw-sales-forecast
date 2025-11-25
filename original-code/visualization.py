"""
Static and interactive visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import out_path
from utils import print_section


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
    p = out_path('01_sales_overview.png')
    plt.savefig(p, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {p}")
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
    p = out_path('02_model_region_heatmap.png')
    plt.savefig(p, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {p}")
    plt.close()


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
    p = out_path('03_arima_forecast.png')
    plt.savefig(p, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {p}")
    plt.close()


def forecast_model_specific(df_model_yearly, top_models, model_thresholds):
    """Forecast for top 5 models"""
    print_section("🏎️ MODEL-SPECIFIC FORECASTS (Top 5 Models)")
    
    from statsmodels.tsa.arima.model import ARIMA
    
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
    p = out_path('04_model_forecasts.png')
    plt.savefig(p, dpi=300, bbox_inches='tight')
    print(f"\n✅ Saved: {p}")
    plt.close()
    
    print(f"\n✅ Model forecasting complete")
    
    return model_forecasts


def create_interactive_dashboard(ts_years, ts_data, future_years, future_values, 
                                 df_yearly, df_clean):
    """Create interactive Plotly dashboard"""
    print_section("📊 CREATING INTERACTIVE DASHBOARD")
    
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
    
    p = out_path('05_interactive_dashboard.html')
    fig_forecast.write_html(p)
    print(f"\n✅ Saved: {p}")


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
    
    p = out_path('06_model_heatmap_interactive.html')
    fig_heatmap.write_html(p)
    print(f"✅ Saved: {p}")
