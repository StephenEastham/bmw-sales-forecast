Forecasting Math — Linear Trend

This document explains the simple linear forecasting logic used in `step7/forecasting.py`.

- **Model:** We fit a straight-line model to annual sales:

  $y = m\,x + c$

  where `y` = total sales and `x` = year.

- **Fitting (Least Squares):** The slope `m` and intercept `c` are chosen to minimize the sum of squared residuals. Analytic formulae (equivalent to `numpy.polyfit(x, y, 1)`) are:

  $$
  m = \frac{\sum_i (x_i-\bar{x})(y_i-\bar{y})}{\sum_i (x_i-\bar{x})^2},\\
  c = \bar{y} - m\,\bar{x}
  $$

  where $\bar{x}$ and $\bar{y}$ are the sample means of the years and sales.

- **Interpretation:**
  - The slope $m$ gives the average change in sales per year (units: sales per year).
  - The intercept $c$ is the model value at year 0; it is usually not directly meaningful when `x` uses large calendar years, but it is required by the linear equation.

- **Forecasting:** For future years $x^*$ the predicted sales are

  $$\hat{y} = m\,x^* + c.$$

  In code this is computed as `future_sales = slope * future_years + intercept`.

- **Plotting:** The visual output shows three elements: historical data points `(x_i,y_i)`, the fitted trend line $m x + c$ over the historical range, and forecast points `(x^*, \hat{y})` for future years.

- **Assumptions & Limits:**
  - Assumes a linear trend: no seasonality, cyclic behavior, or structural breaks are modeled.
  - Forecasts are point estimates — no confidence intervals or uncertainty estimates are provided by this simple method.
  - Outliers and non-linear patterns can bias the linear fit.

- **Numeric note:** Using raw calendar years (e.g., 2010–2024) is fine numerically for typical datasets, but centering years (subtracting the mean year) improves numerical stability and makes `c` easier to interpret (it becomes the fitted value at the mean year).

- **Practical advice:** If you need realistic intervals or to model autocorrelation/seasonality, consider time-series methods (ARIMA, ETS, Prophet) or regression with additional covariates and compute prediction intervals.
