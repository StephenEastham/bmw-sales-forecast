"""
Static visualizations (Matplotlib/Seaborn)
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import out_path

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
