"""
Exploratory Data Analysis module
"""

from utils import print_section

def exploratory_data_analysis(df_clean):
    """Perform EDA"""
    print_section("📊 EXPLORATORY DATA ANALYSIS")
    
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
