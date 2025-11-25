"""
Alert system for detecting underperforming models and regions
"""

import logging
from utils import setup_logger


class SalesAlertSystem:
    """Automated alert system for underperforming models and regions"""
    
    def __init__(self, threshold, model_thresholds=None, region_thresholds=None):
        self.threshold = threshold
        self.model_thresholds = model_thresholds or {}
        self.region_thresholds = region_thresholds or {}
        self.alerts = []
        self.logger = setup_logger()
    
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


def setup_alert_system(df_clean, df_yearly, top_models):
    """Setup alert thresholds and system"""
    from utils import print_section
    from config import OVERALL_THRESHOLD_MULTIPLIER, MODEL_THRESHOLD_MULTIPLIER, REGION_THRESHOLD_MULTIPLIER
    
    print_section("⚠️ ALERT THRESHOLD CONFIGURATION")
    
    average_sales = df_yearly['Total_Sales'].mean()
    ALERT_THRESHOLD_OVERALL = average_sales * OVERALL_THRESHOLD_MULTIPLIER
    
    print(f"\n📊 Overall Metrics:")
    print(f"   Average historical sales: {average_sales:,.0f}")
    print(f"   Alert threshold (80%): {ALERT_THRESHOLD_OVERALL:,.0f}")
    
    model_thresholds = {}
    print(f"\n🏎️ Model-Specific Alert Thresholds (Top 5):")
    for model in top_models:
        model_avg = df_clean[df_clean['Model'] == model]['Sales_Volume'].mean()
        model_threshold = model_avg * MODEL_THRESHOLD_MULTIPLIER
        model_thresholds[model] = model_threshold
        print(f"   {model}: {model_threshold:,.0f}")
    
    region_thresholds = {}
    unique_regions = df_clean['Region'].unique()
    print(f"\n🌍 Region-Specific Alert Thresholds:")
    for region in unique_regions:
        region_avg = df_clean[df_clean['Region'] == region]['Sales_Volume'].mean()
        region_threshold = region_avg * REGION_THRESHOLD_MULTIPLIER
        region_thresholds[region] = region_threshold
        print(f"   {region}: {region_threshold:,.0f}")
    
    return SalesAlertSystem(
        threshold=ALERT_THRESHOLD_OVERALL,
        model_thresholds=model_thresholds,
        region_thresholds=region_thresholds
    ), ALERT_THRESHOLD_OVERALL, model_thresholds, region_thresholds, unique_regions
