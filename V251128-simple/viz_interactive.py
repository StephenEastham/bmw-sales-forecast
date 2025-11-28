"""
Interactive visualizations (Plotly)
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import out_path
from utils import print_section

def create_interactive_dashboard(ts_years, ts_data, df_yearly, df_clean):
    """Create interactive Plotly dashboard (no forecasting traces)."""
    print_section("📊 CREATING INTERACTIVE DASHBOARD")
    
    fig_forecast = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Total Sales Trend',
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
