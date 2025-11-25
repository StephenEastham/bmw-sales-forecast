"""
Time series forecasting: ARIMA and fallback methods
"""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from config import ARIMA_ORDER, FORECAST_STEPS, TRAIN_TEST_SPLIT
from utils import print_section


def forecast_with_arima(ts_data, ts_years):
    """Forecast using ARIMA model with fallback to ExponentialSmoothing"""
    print_section("🤖 ARIMA TIME SERIES FORECASTING")
    
    train_size = int(len(ts_data) * TRAIN_TEST_SPLIT)
    train_data = ts_data[:train_size]
    test_data = ts_data[train_size:]
    
    print(f"\n📊 Data Split:")
    print(f"   Train set: {len(train_data)} years")
    print(f"   Test set: {len(test_data)} years")
    
    print(f"\n🔄 Fitting ARIMA{ARIMA_ORDER} model...")
    try:
        arima_model = ARIMA(train_data, order=ARIMA_ORDER)
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
        
        full_model = ARIMA(ts_data, order=ARIMA_ORDER)
        full_results = full_model.fit()
        future_forecast = full_results.get_forecast(steps=FORECAST_STEPS)
        future_values = future_forecast.predicted_mean.values
        future_ci = future_forecast.conf_int()
        
        future_years = np.array([ts_years[-1] + i for i in range(1, FORECAST_STEPS + 1)])
        
        print(f"\n🔮 FUTURE FORECAST (Next {FORECAST_STEPS} Years):")
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
            future_values = full_results.forecast(steps=FORECAST_STEPS)
            future_years = np.array([ts_years[-1] + i for i in range(1, FORECAST_STEPS + 1)])
            forecast_test_ci = None
            future_ci = None
            
            print(f"✅ Exponential Smoothing fitted successfully")
            
        except Exception as e2:
            print(f"⚠️ Fallback error: {e2}")
            future_values = np.repeat(ts_data[-1], FORECAST_STEPS)
            future_years = np.array([ts_years[-1] + i for i in range(1, FORECAST_STEPS + 1)])
            forecast_test_values = None
            forecast_test_ci = None
            future_ci = None
    
    print(f"\n✅ Forecasting complete")
    
    return train_size, forecast_test_values, forecast_test_ci, future_values, future_years, future_ci
