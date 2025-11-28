# Alert System TEST MODE - Quick Guide

## Overview
The notebook now includes a **TEST MODE** that lets you easily trigger alerts to verify the alert system is working correctly. No need to wait for real performance issues!

---

## How to Enable Test Mode

### Step 1: Set TEST_MODE to True
Find the cell in **SECTION 9: Alert Thresholds & Configuration** and change:

```python
TEST_MODE = False  # Change to True to trigger alerts!
```

to:

```python
TEST_MODE = True  # Change to True to trigger alerts!
```

### Step 2: Configure Test Scenarios (Optional)
In the same cell, you can enable/disable specific alert scenarios:

```python
# Choose which test scenarios to enable:
TEST_OVERALL_FORECAST_LOW = True      # Makes overall forecast drop below threshold
TEST_MODEL_UNDERPERFORMANCE = True    # Makes top models underperform
TEST_REGION_DECLINE = True            # Makes regions show steep decline
TEST_DECLINING_TREND = True           # Makes models show 15%+ decline
```

You can set individual scenarios to `False` if you only want to test specific alerts.

### Step 3: Run the Cells in Order

1. **Cell 1 (SECTION 9)**: Alert Thresholds & Configuration
   - Shows baseline thresholds
2. **Cell 2 (Test Injection)**: Injects bad metrics
   - Displays what test metrics were applied
3. **Cell 3 (Alert System)**: Runs all alert checks
   - **Now shows multiple 🔴 HIGH and 🟡 MEDIUM severity alerts!**
4. **Cell 4 (Report Generation)**: Creates monthly report
   - Report includes all triggered alerts
5. **Cell 5 (Cleanup)**: Restores original data
   - Automatically cleans up test data

---

## What Gets Tested

### Test Scenarios Explained

| Scenario | What It Does | Result |
|----------|------------|--------|
| **OVERALL_FORECAST_LOW** | Sets forecast to 50-70% of threshold | 3 HIGH severity alerts |
| **MODEL_UNDERPERFORMANCE** | Reduces top 5 models to 50% of threshold | 5 MEDIUM severity alerts |
| **REGION_DECLINE** | Sets all regions to 50% of threshold | 6 MEDIUM severity alerts |
| **DECLINING_TREND** | Creates 20% decline in top 2 models | 2 MEDIUM severity alerts |

**Total when all enabled: ~17 alerts** ✅

---

## Example Test Run Output

```
================================================================================
🧪 TEST MODE: INJECTING BAD METRICS
================================================================================

✓ Overall Forecast: Set to 50-70% of threshold
✓ Model '7 Series': Recent sales reduced to 50% of threshold
✓ Model 'i8      ': Recent sales reduced to 50% of threshold
✓ Model 'X1      ': Recent sales reduced to 50% of threshold
✓ Model '3 Series': Recent sales reduced to 50% of threshold
✓ Model 'i3      ': Recent sales reduced to 50% of threshold
✓ Regional Sales: Set to 50% of threshold for latest year
✓ Model '7 Series': Created 20% decline in recent years
✓ Model 'i8      ': Created 20% decline in recent years

================================================================================

...then when alert system runs:

🚨 SALES ALERT REPORT
================================================================================

📊 Total Alerts: 17

🔴 HIGH SEVERITY ALERTS:
   - 🚨 ALERT: Forecasted sales for year 1 (8,108,023) falls below threshold (13,513,372)
   - 🚨 ALERT: Forecasted sales for year 2 (9,459,361) falls below threshold (13,513,372)
   - 🚨 ALERT: Forecasted sales for year 3 (6,756,686) falls below threshold (13,513,372)

🟡 MEDIUM SEVERITY ALERTS:
   - 📉 ALERT: 7 Series showing 20.0% decline
   - 📉 ALERT: i8       showing 20.0% decline
   - ⚠️ ALERT: Model X1       recent sales below threshold
   ... (11 more alerts)
```

---

## How to Clean Up After Testing

### Automatic Cleanup
When you run the **Cleanup Cell** (after Report Generation), it automatically:
- ✅ Restores original forecast values
- ✅ Restores model data
- ✅ Restores regional data
- ✅ Prints confirmation

### Manual Cleanup (Just in Case)
If you want to reset without running the cleanup cell:

1. Change `TEST_MODE = False`
2. Re-run the threshold configuration cell
3. Re-run the test injection cell (it won't inject anything with TEST_MODE=False)

---

## Return to Production

### Step 1: Disable Test Mode
```python
TEST_MODE = False  # Back to normal!
```

### Step 2: Run Alert Checks Again
Now you'll see:
```
🚨 SALES ALERT REPORT
================================================================================

📊 Total Alerts: 0

✅ No alerts triggered! All metrics within acceptable range.
```

---

## Use Cases

### When to Use Test Mode
- ✅ **First Setup**: Verify the alert system actually works
- ✅ **Training**: Show stakeholders how alerts look when triggered
- ✅ **Debugging**: Test individual alert types without changing real data
- ✅ **Integration Testing**: Ensure reports generate correctly with alerts
- ✅ **CI/CD Pipeline**: Automated testing of alert logic

### Production Usage
- ❌ Don't leave TEST_MODE enabled in production
- ✅ Always set `TEST_MODE = False` before sharing reports
- ✅ Monitor `sales_alerts.log` for real alerts

---

## Files Generated During Tests

When test alerts are triggered, the following files are created:
- `sales_report_[timestamp].txt` - Monthly report with alerts
- `sales_alerts.log` - Log file with all alert details
- `forecast_next_3_years.csv` - Forecast data
- `active_alerts.csv` - All triggered alerts

**All test data is automatically removed** when cleanup runs, so production data remains clean!

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Alerts not appearing | Check `TEST_MODE = True` in cell 1 |
| Data not restored | Run the Cleanup cell manually |
| Cleanup not working | Set `TEST_MODE = False` and re-run alert cell |
| Forecast still showing test values | Run threshold config cell again |

---

## Summary

The TEST MODE makes it **super easy** to:
1. Toggle alerts on/off with a single boolean
2. Test individual alert scenarios independently
3. Automatically clean up test data without manual intervention
4. Verify the alert system works before production deployment

**Just change `TEST_MODE = True` → see all alerts → change `TEST_MODE = False` → production ready!**
