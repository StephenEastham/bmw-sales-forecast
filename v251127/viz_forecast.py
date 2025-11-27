"""
Forecast visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
from config import out_path
from utils import print_section

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


def plot_model_forecasts(model_forecasts):
    """Plot forecasts for top models"""
    print_section("📊 PLOTTING MODEL FORECASTS")
    
    if not model_forecasts:
        print("   ⚠️ No model forecasts to plot.")
        return

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    fig.suptitle('Top 5 BMW Models: Sales Forecast', fontsize=16, fontweight='bold')
    
    for idx, (model, data) in enumerate(model_forecasts.items()):
        if idx >= 5: break
        
        ax = axes[idx]
        ax.plot(data['years'], data['historical'], marker='o', linewidth=2, label='Historical')
        ax.plot(data['forecast_years'], data['forecast'], 
               marker='^', linestyle='--', linewidth=2, color='red', label='Forecast')
        ax.set_title(f'Model: {model}', fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Sales')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Hide unused subplots
    for i in range(len(model_forecasts), len(axes)):
        fig.delaxes(axes[i])
    
    plt.tight_layout()
    p = out_path('04_model_forecasts.png')
    plt.savefig(p, dpi=300, bbox_inches='tight')
    print(f"\n✅ Saved: {p}")
